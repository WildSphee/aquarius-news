import os
from typing import Dict

import autogen
from autogen import ChatResult
from dotenv import load_dotenv

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
        system_message="""Scientist. You follow an approved plan. You are able to categorize papers after seeing their abstracts printed. You don't write code.""",
    )
    planner = autogen.AssistantAgent(
        name="Planner",
        system_message="""Planner. Suggest a plan. Revise the plan based on feedback from admin and critic, until admin approval.
    The plan may involve an engineer who can write code and a scientist who doesn't write code.
    Explain the plan first. Be clear which step is performed by an engineer, and which step is performed by a scientist.
    """,
        llm_config=gpt4_config,
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
    critic = autogen.AssistantAgent(
        name="Critic",
        system_message="Critic. Double check plan, claims, code from other agents and provide feedback. Check whether the plan includes adding verifiable info such as source URL.",
        llm_config=gpt4_config,
    )
    groupchat = autogen.GroupChat(
        agents=[user_proxy, engineer, scientist, planner, executor, critic],
        messages=[],
        max_round=50,
    )
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=gpt4_config)

    results: ChatResult = user_proxy.initiate_chat(
        manager,
        message="""
    generate an article of the week for the latest Gen-AI / LLM trends and developments. 
    With the following sections:

    1. summary
    2. highlights 
        pointform about what are the latest developments in the field
    3. deep dive
        talk about each point with relevant link references
    """,
    )

    return results.summary
