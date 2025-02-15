import os
from typing import Dict

import autogen
from autogen import ChatResult, register_function
from autogen.agentchat.contrib.capabilities import transform_messages, transforms
from dotenv import load_dotenv

from aquarius.tools import fetch_arxiv_articles, fetch_reddit_posts

load_dotenv()

gpt4_config = {
    "cache_seed": 69,
    "temperature": 0.5,
    "config_list": autogen.config_list_from_json(env_or_file="OAI_CONFIG_LIST"),
    "timeout": 120,
}


def create_chat_results(gpt4_config: Dict = gpt4_config) -> str:
    """
    start a autogen group chat and generate chat completion.

    attribute:
        gpt4_config (Dict): a config dictionary for the LLMs
    return:
        str: Summary of the chat - default to final output
    """

    user_proxy = autogen.UserProxyAgent(
        name="Admin",
        code_execution_config=False,
        human_input_mode="NEVER",
        is_termination_msg=lambda x: x.get("content", "")
        .rstrip()
        .endswith("TERMINATE"),
    )
    executor = autogen.UserProxyAgent(
        name="Executor",
        system_message="Executor. Execute the code written by the engineer and report the result.",
        human_input_mode="NEVER",
        code_execution_config={
            "last_n_messages": 3,
            "work_dir": os.getenv("TEMP_OUTPUT_DIR") or "temp",
            "use_docker": True,
        },  # set use_docker=True if docker is available
    )

    scientist = autogen.AssistantAgent(
        name="Scientist",
        llm_config=gpt4_config,
        system_message="""Scientist. You follow an approved plan. You are able to categorize papers after seeing their abstracts printed. You know how to approach a research plan. You don't write code but you can choose what to execute.""",
    )
    # allow the scientist to call for latest posts
    for func in [fetch_reddit_posts, fetch_arxiv_articles]:
        register_function(
            func,
            caller=scientist,
            executor=executor,
            name=func.__name__,
            description=func.__doc__,
        )

    planner = autogen.AssistantAgent(
        name="Planner",
        system_message="""Planner. Suggest a plan. Revise the plan based on feedback from admin and critic, until admin approval.
    The plan may involve an engineer who can write code and a scientist who doesn't write code.
    Explain the plan first. Be clear which step is performed by an engineer, and which step is performed by a scientist.
    """,
        llm_config=gpt4_config,
    )

    critic = autogen.AssistantAgent(
        name="Critic",
        system_message="Critic. Double check plan, claims, code from other agents and provide feedback. Check whether the plan includes adding verifiable info such as source URL. Be concise",
        llm_config=gpt4_config,
    )
    transform_messages.TransformMessages(
        transforms=[
            transforms.MessageHistoryLimiter(max_messages=4),
            # transforms.MessageTokenLimiter(max_tokens=1000, max_tokens_per_message=50, min_tokens=500),
        ]
    ).add_to_agent(critic)

    groupchat = autogen.GroupChat(
        agents=[user_proxy, scientist, planner, executor],
        messages=[],
    )
    manager = autogen.GroupChatManager(
        groupchat=groupchat,
        llm_config=gpt4_config,
        is_termination_msg=lambda x: x.get("content", "")
        .rstrip()
        .endswith("TERMINATE"),
    )

    results: ChatResult = user_proxy.initiate_chat(
        manager,
        message="""
    generate an article of the week for the latest Gen-AI / LLM trends and developments.
    Gather sources from all origins. This article is sent by email so make sure its email formatted.
    With the following sections:

    1. summary
    2. highlights 
        pointform about what are the latest developments in the field, short and concise
    3. deep dive
        elaborate on each highlights with relevant link references

    Reply TERMINATE in the end of the article when everything is done
    """,
    )

    print(f"{results.chat_history[-1]=}")
    return results.chat_history[-1]["content"].strip().rstrip("TERMINATE")
