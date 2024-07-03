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
        system_message="A human admin. Interact with the planner to discuss the plan. Plan execution needs to be approved by this admin.",
        code_execution_config=False,
    )
    executor = autogen.UserProxyAgent(
        name="Executor",
        system_message="Executor. Execute the code written by the engineer and report the result.",
        human_input_mode="NEVER",
        code_execution_config={
            "last_n_messages": 3,
            "work_dir": os.getenv("TEMP_OUTPUT_DIR") or "temp",
            "use_docker": True,
        },  # Please set use_docker=True if docker is available
    )
    engineer = autogen.AssistantAgent(
        name="Engineer",
        llm_config=gpt4_config,
        system_message="""Engineer. You follow an approved plan. You write python/shell code to solve tasks. Wrap the code in a code block that specifies the script type. The user can't modify your code. So do not suggest incomplete code which requires others to modify. Don't use a code block if it's not intended to be executed by the executor.
    Don't include multiple code blocks in one response. Do not ask others to copy and paste the result. Check the execution result returned by the executor.
    If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try.
    """,
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
            caller=scientist,  # The assistant agent can suggest calls to the calculator.
            executor=executor,  # The user proxy agent can execute the calculator calls.
            name=func.__name__,  # func name
            description=func.__doc__,  # doc string
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
        agents=[scientist, planner, executor],
        messages=[],
        max_round=30,
    )
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=gpt4_config)

    results: ChatResult = user_proxy.initiate_chat(
        manager,
        message="""
    generate an article of the week for the latest Gen-AI / LLM trends and developments.
    Gather sources from all origins.
    With the following sections:

    1. summary
    2. highlights 
        pointform about what are the latest developments in the field, short and concise
    3. deep dive
        elaborate on each highlights with relevant link references
    """,
    )

    print(f"{results.chat_history[-1]=}")
    return results.chat_history[-1]
