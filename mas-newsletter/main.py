import autogen
from dotenv import load_dotenv

load_dotenv()


llm_config = {
    "config_list": autogen.config_list_from_json(env_or_file="AOAI_CONFIG_LIST"),
    "cache_seed": 42,
}

user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    system_message="A human admin.",
    code_execution_config={
        "last_n_messages": 2,
        "work_dir": "groupchat",
        "use_docker": False,  # use_docker=True if possible, safer
    },
    human_input_mode="TERMINATE",
)
coder = autogen.AssistantAgent(
    name="Coder",
    llm_config=llm_config,
)
pm = autogen.AssistantAgent(
    name="Product_manager",
    system_message="Creative in software product ideas.",
    llm_config=llm_config,
)
groupchat = autogen.GroupChat(agents=[user_proxy, coder, pm], messages=[], max_round=12)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

user_proxy.initiate_chat(
    manager,
    message="Find a latest paper about gpt-4 on arxiv and find its potential applications in software.",
)
# type exit to terminate the chat
