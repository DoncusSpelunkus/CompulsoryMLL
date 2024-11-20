import autogen
import os
from autogen import ConversableAgent
from autogen.coding import LocalCommandLineCodeExecutor

config_list = [
    {
        "model": "mistral-7B-Instruct-v0.1-GGUF",
        "base_url": "http://localhost:1234/v1",
        "api_key": "NULL",
        "api_type": "completion"  
    }
]

llm_config = {
    "seed": 42,
    "config_list": config_list,
    "temperature": 0,
}

# Simplified agent configuration
assistant = autogen.AssistantAgent(
    name="Coder",
    llm_config=llm_config,
)

# Create a local command line code executor.
executor = LocalCommandLineCodeExecutor(
    timeout=10,  # Timeout for each code execution in seconds.
    work_dir= "web",  # Use the temporary directory to store the code files. # No execution policies for now
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    code_execution_config={"executor": executor},
    human_input_mode="NEVER",
    max_consecutive_auto_reply=1,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    llm_config=llm_config
)

# Simple prompt
task = "Write a Python function that takes a list of numbers and returns the average of the numbers."

result = user_proxy.initiate_chat(
    assistant,
    message=task,
)

print(os.listdir("web"))