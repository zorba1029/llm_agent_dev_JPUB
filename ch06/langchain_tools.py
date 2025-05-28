import os
from dotenv import load_dotenv
# from langchain.prebuilt import create_react_agent
from langchain.agents import create_react_agent
from langchain_google_community import GmailToolkit
from langchain_openai import OpenAI
from langchain import hub 

load_dotenv()

llm = OpenAI(temperature=0)

tools = []

prompt = hub.pull("hwchase17/react")

# toolkit = GmailToolkit()

# tools = toolkit.get_tools()


agent_executor = create_react_agent(llm, tools, prompt)

# agent_executor.invoke({"input": "What is the weather in Tokyo?"})