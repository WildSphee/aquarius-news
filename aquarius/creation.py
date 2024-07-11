import os
from typing import Dict

import autogen
from autogen import ChatResult, register_function
from autogen.agentchat.contrib.capabilities import transform_messages, transforms
from dotenv import load_dotenv
import agentops

from aquarius.tools import fetch_arxiv_articles, fetch_reddit_posts

load_dotenv()

# Initialize AgentOps
AGENTOPS_API_KEY = os.getenv("AGENTOPS_API_KEY")
if not AGENTOPS_API_KEY:
    raise ValueError("AGENTOPS_API_KEY not found in environment variables")

agentops.init(AGENTOPS_API_KEY)

gpt4_config = {
    "cache_seed": 69,
    "temperature": 0.5,
    "config_list": autogen.config_list_from_json(env_or_file="OAI_CONFIG_LIST"),
    "timeout": 120,
}

@agentops.record_function('create_chat_results')
def create_chat_results(gpt4_config: Dict = gpt4_config) -> str:
    """
    start a autogen group chat and generate chat completion.

    attribute:
        gpt4_config (Dict): a config dictionary for the LLMs
    return:
        str: Summary of the chat - default to final output
    """

    @agentops.track_agent(name='user_proxy')
    class UserProxyAgent(autogen.UserProxyAgent):
        pass

    @agentops.track_agent(name='executor')
    class ExecutorAgent(autogen.UserProxyAgent):
        pass

    @agentops.track_agent(name='scientist')
    class ScientistAgent(autogen.AssistantAgent):
        pass

    @agentops.track_agent(name='planner')
    class PlannerAgent(autogen.AssistantAgent):
        pass

    @agentops.track_agent(name='critic')
    class CriticAgent(autogen.AssistantAgent):
        pass

    user_proxy = UserProxyAgent(
        name="Admin",
        code_execution_config=False,
        human_input_mode="NEVER",
        is_termination_msg=lambda x: x.get("content", "")
        .rstrip()
        .endswith("TERMINATE"),
    )
    executor = ExecutorAgent(
        name="Executor",
        system_message="Executor. Execute the code written by the engineer and report the result.",
        human_input_mode="NEVER",
        code_execution_config={
            "last_n_messages": 3,
            "work_dir": os.getenv("TEMP_OUTPUT_DIR") or "temp",
            "use_docker": True,
        },
    )

    scientist = ScientistAgent(
        name="Scientist",
        llm_config=gpt4_config,
        system_message="""Scientist. You follow an approved plan. You are able to categorize papers after seeing their abstracts printed. You know how to approach a research plan. You don't write code but you can choose what to execute.""",
    )

    @agentops.record_function('register_functions')
    def register_functions():
        for func in [fetch_reddit_posts, fetch_arxiv_articles]:
            register_function(
                func,
                caller=scientist,
                executor=executor,
                name=func.__name__,
                description=func.__doc__,
            )

    register_functions()

    planner = PlannerAgent(
        name="Planner",
        system_message="""Planner. Suggest a plan. Revise the plan based on feedback from admin and critic, until admin approval.
    The plan may involve an engineer who can write code and a scientist who doesn't write code.
    Explain the plan first. Be clear which step is performed by an engineer, and which step is performed by a scientist.
    """,
        llm_config=gpt4_config,
    )

    critic = CriticAgent(
        name="Critic",
        system_message="Critic. Double check plan, claims, code from other agents and provide feedback. Check whether the plan includes adding verifiable info such as source URL. Be concise",
        llm_config=gpt4_config,
    )
    transform_messages.TransformMessages(
        transforms=[
            transforms.MessageHistoryLimiter(max_messages=4),
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

    @agentops.record_function('initiate_chat')
    def initiate_chat():
        return user_proxy.initiate_chat(
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

    results: ChatResult = initiate_chat()

    print(f"{results.chat_history[-1]=}")
    return results.chat_history[-1]["content"].strip().rstrip("TERMINATE")

if __name__ == "__main__":
    try:
        result = create_chat_results()
        print(result)
    except Exception as e:
        agentops.log_error(str(e))
        raise
    finally:
        agentops.end_session('Success')