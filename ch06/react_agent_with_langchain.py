import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain_community.utilities import SerpAPIWrapper
from langchain_experimental.tools.python.tool import PythonREPLTool

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

search = SerpAPIWrapper()

search_tool = Tool(
    name="search",
    func=search.run,
    description="현재 정보를 검색하는 도구",
)

math_prompt = ChatPromptTemplate.from_messages([
    ("system", "Solve the math problem carefully."),
    ("user", "{question}")
])

# pipeline chain 생성
llm_math_chain = math_prompt | llm

math_tool = Tool(
    name="llm-math",
    func=lambda x: llm_math_chain.invoke({"question": x}),
    description="수학 문제를 풀어주는 도구",
)

python_tool = PythonREPLTool()

# tools list
tools = [search_tool, math_tool, python_tool]

react_prompt = ChatPromptTemplate.from_messages([
    (
        "system", 
        "You are a helpful AI agent that follows the ReAct framework.\n\n"
        "You can use the following tools:\n"
        "{tools}\n\n"
        "Use the following format:\n\n"
        "Question: the input question you must answer\n"
        "Thought: you should always think about what to do\n"
        "Action: the action to take, should be one of [{tool_names}]\n"
        "Action Input: the input to the action\n"
        "Observation: the result of the action\n"
        "... (this Thought/Action/Action Input/Observation can repeat N times)\n"
        "Thought: I now know the final answer\n"
        "Final Answer: the final answer to the original input question\n\n"
        "Begin!\n\n"
    ),
    (
        "user",
        "{input}"
    ),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# React Agent 생성
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    agent_kwargs={"prompt": react_prompt},
    verbose=True,
)

# Execute Agent
input_question = {
    "현재 시장에서 장미의 일반적인 구매 가젹은 얼마인가요?\n"
    "이 가격에 마진을 5%를 추가하려면 어떻게 가격을 책정해야 합니까?"
}

result = agent.invoke(input_question)

# 결과 출력
print(result)

# 결과를 한국어로 출력하도록 유도하는 프롬프트 템플릿
react_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "최선을 다해 다음 질문에 답해 주세요."
     "능력이 부족할 경우, 아래 도구를 사용할 수 있습니다:\n\n"
     "You are a helpful AI agent that follows the ReAct framework.\n\n"
     "You can use the following tools:\n"
     "{tools}\n\n"
     "Use the following format:\n\n"
     "Question: the input question you must answer\n"
     "Thought: you should always think about what to do\n"
     "Action: the action to take, should be one of [{tool_names}]\n"
     "Action Input: the input to the action\n"
     "Observation: the result of the action\n"
     "... (this Thought/Action/Action Input/Observation can repeat N times)\n"
     "Thought: I now know the final answer\n"
     "Final Answer: the final answer to the original input question\n\n"
     "Begin!\n\n"
    ),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

#--------------------------------------------------
# > python3 react_agent_with_langchain.py
# /Volumes/SSD_01/zorba/brain/deep-learning/llm-ai-agent-dev/mytrial/ch06/react_agent_with_langchain.py:67: LangChainDeprecationWarning: LangChain agents will continue to be supported, but it is recommended for new use cases to be built with LangGraph. LangGraph offers a more flexible and full-featured framework for building agents, including support for tool-calling, persistence of state, and human-in-the-loop workflows. For details, refer to the `LangGraph documentation <https://langchain-ai.github.io/langgraph/>`_ as well as guides for `Migrating from AgentExecutor <https://python.langchain.com/docs/how_to/migrate_agent/>`_ and LangGraph's `Pre-built ReAct agent <https://langchain-ai.github.io/langgraph/how-tos/create-react-agent/>`_.
#   agent = initialize_agent(


# > Entering new AgentExecutor chain...
# 현재 시장에서 장미의 일반적인 구매 가격을 알아야 하며, 그 가격에 5%의 마진을 추가하는 방법을 계산해야 합니다. 먼저 장미의 일반적인 구매 가격을 검색해 보겠습니다.  
# Action: search  
# Action Input: "현재 시장에서 장미의 일반적인 구매 가격"  
# Observation: ['이 집 장미 컬러가 제일 예뻐 보이구 싱싱해보였다! 윗줄의 엘리자베스장미는 1단에 18000원, 아랫줄의 엘리자베스는 1단 15000원 이었다! 18000원 짜리 ...', '총 오늘 장미꽃 가격은 1만 4천원입니다 :-) 장미의 꽃말은 컬러에 따라서 달라져요 꽃말에 맞춰서 꽃선물을 ...', 'A씨는 정상 시세 7000~1만5000원 꼴인 장미 한단이 현재 4만5000원에서 7만원까지 올랐다고 말했다. 심지어 고속버스터미널 꽃 시장의 상인들은 가격 몇 ...', '... 의 3~40%를 수출 하고 있습니다. 현재 국내 장미가격이 오르고 있어 오히려 일본시장보다 국내시장이 더 좋은 편입니다.”고 말한다. 더불어 정 대표 ...', '꽃값도 지난 5일 2만원을 넘었던 장미 평균단가는 7일 1만1841원으로 40% 이상 내린 뒤 10일 8998원으로 평년 수준으로 돌아갔다. 하지만 설연휴 이후 ...', '오소형 자문위원 또한 “1단에 평균 1만5천원하는 장미가 얼마전 가보니 경매가가 5만원이더라. 그래도 단골손님들을 위해 울며 겨자먹기로 사야한다”며 ...', '... 장미의 봉우리 크기가 일본시장에서. 요구하는 사이즈와 맞지가 않아서 ... - 리쥐스키 꽃시장은 도심에서 판매되는 가격의 절반 정도에 꽃을 구매할 수 있으며, 더.', '현재 국내에서 재배되는 장미의 품종은 화란, 독일, 일본 등지에서 개발한 품종을 ... 최근 장미가격의 하락으로 농가에서 수취가격 제고를 위하여 신품종에 대한 ...', '봄(3월)은 장미 구매하는 시기(장미구매하는곳,주의할점). 2.9K views · 2 years ago #대림원예종묘 #사이트 #장미 ...more ...']
# Thought:장미의 일반적인 구매 가격에 대한 정보가 여러 개의 출처에서 나왔습니다. 대체로 장미 한 단의 가격은 7,000원에서 15,000원 사이로 보입니다. 평균적으로 10,000원 정도로 가정하겠습니다. 이제 이 가격에 5%의 마진을 추가하는 방법을 계산해 보겠습니다.  
# Action: llm-math  
# Action Input: 10000 * 1.05  
# Observation: content='10000 * 1.05 = 10500.' additional_kwargs={'refusal': None} response_metadata={'token_usage': {'completion_tokens': 12, 'prompt_tokens': 24, 'total_tokens': 36, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_54eb4bd693', 'id': 'chatcmpl-BbqDQnYy6hQKfMyidF59TlH5tZVKg', 'service_tier': 'default', 'finish_reason': 'stop', 'logprobs': None} id='run--b554d456-d685-4f46-8f95-d73b989b6e98-0' usage_metadata={'input_tokens': 24, 'output_tokens': 12, 'total_tokens': 36, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
# Thought:장미의 평균 구매 가격이 10,000원이고, 여기에 5%의 마진을 추가하면 최종 가격은 10,500원이 됩니다.  
# Final Answer: 장미의 일반적인 구매 가격은 약 10,000원이며, 5%의 마진을 추가한 가격은 10,500원입니다.

# > Finished chain.
# {'input': {'현재 시장에서 장미의 일반적인 구매 가젹은 얼마인가요?\n이 가격에 마진을 5%를 추가하려면 어떻게 가격을 책정해야 합니까?'}, 'output': '장미의 일반적인 구매 가격은 약 10,000원이며, 5%의 마진을 추가한 가격은 10,500원입니다.'}
