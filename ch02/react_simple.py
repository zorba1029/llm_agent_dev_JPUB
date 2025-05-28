# ch 2.5 ReAct
import os
from dotenv import load_dotenv

# LangChain Hub 가져오기
from langchain import hub

load_dotenv()

# LangChain Hub에서 ReAct의 프롬프트 가져오기
prompt = hub.pull("hwchase17/react", api_key=os.getenv("LANGCHAIN_API_KEY"))

# 프롬프트 출력
print(prompt)

# 프롬프트 실행
from langchain_openai import OpenAI

# 사용할 대형 언어 모델 선택
llm = OpenAI()

# SerpAPIWrapper를 통해 도구 모듈 가져오기
from langchain_community.utilities import SerpAPIWrapper
from langchain.tools import Tool

# SerpAPIWrapper 인스턴스화
search = SerpAPIWrapper()

tools = [
    Tool(
        name="search",
        description="LLM이 관련 지식이 없을 떄 지식 검색에 사용한다.",
        func=search.run,
    )
]

# create_react_agent 기능 가져오기
from langchain.agents import create_react_agent

# ReAct 에이전트 생성
agent = create_react_agent(llm, tools, prompt)

# AgentExecutor 가져오기
from langchain.agents import AgentExecutor

# 에이전트와 도구를 전달하여 AgentExecutor 생성
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# AgentExecutor를 호출하여 입력 데이터 전달
print("첫번째 실행결과:")
agent_executor.invoke({"input": "현재 인공 지능 에이전트의 최신 연구 진전은 무엇입니까?"})

print("두번째 실행결과:")
agent_executor.invoke({"input": "현재 인공 지능 에이전트의 최신 연구 진전은 무엇입니까?"})

# ---- 1차 실행 --------------------------------------------
# > python3 react_simple.py


# input_variables=['agent_scratchpad', 'input', 'tool_names', 'tools'] input_types={} 
# partial_variables={} 
# metadata={
    # 'lc_hub_owner': 'hwchase17', 
    # 'lc_hub_repo': 'react', 
    # 'lc_hub_commit_hash': 'd15fe3c426f1c4b3f37c9198853e4a86e20c425ca7f4752ec0c9b0e97ca7ea4d'
# } 
# template='Answer the following questions as best you can. You have access to the following tools:
# \n\n
# {tools}
# \n\n
# Use the following format:
# \n\n
# Question: the input question you must answer\n
# 
# Thought: you should always think about what to do\n
# Action: the action to take, should be one of 
# [{tool_names}]\n
# 
# Action Input: the input to the action\n
# Observation: the result of the action\n
# ... (this Thought/Action/Action Input/Observation can repeat N times)\n
# 
# Thought: I now know the final answer\n
# 
# Final Answer: the final answer to the original input question\n\n
# 
# Begin!\n\n
# 
# Question: {input}\n
# 
# Thought:{agent_scratchpad}'
#
# 첫번째 실행결과:


# > Entering new AgentExecutor chain...
#  현재의 최신 연구에 대해 알고 싶은데, 어떻게 해야 할까?
# Action: search
# Action Input: 현재 인공 지능 연구 진전
# [검색 결과:
#   '최근에는 딥러닝이 인공지능 기술의 핵심으로 떠올랐습니다. 딥러닝은 인간의 뇌 구조를...',
#   '보고서에 따르면, AI는 이미지 분류, 시각적 추론, 영어 이해 등의 분야에서 인간을...',
#   'OpenBrain이 AI를 활용하여 1주일 동안 달성하는 AI 연구 진전은 AI 없이 진행했다면...',
#   "현재 뉴럴링크의 임상시험은 마비 환자에 초점을 맞추고 있다. 하지만 일론 머스크의...",
#   '초기 AI 연구는 주로 규칙 기반 시스템에 중점을 두었습니다. 이를 통해...',
#   '과학매체 Live Science에 따르면, 중국 푸단대학 연구진은 최근 메타 및 알리바바의...',
#   '이 연구는 신경과학과 인공지능의 역사에서 중요한 연구 중 하나입니다. 이 논문은...',
#   '1956년 다트머스 회의는 인공지능 연구의 시작으로 간주하였으며, 그 이후로...',
#   'AI를 학문으로 정착시킨 초기 과학자들은 여전히 인간과 기계 지능에 대한 근본적인...',
#   '오픈AI의 인공지능 챗봇인 챗GPT가 등장한 후 인공지능(AI)의 위험성이 제기되면서...']
# 이것들이 원하는 답이 아닌 것 같다면, 다른 검색 방법을 시도해야 할까?
# 
# Action: search
# Action Input: 인공지능 최신 연구
# [검색 결과:
#   "세계적인 제약 회사 'NovaCure'에서 혁신적인 인공지능 기반 항암 치료 기술 'OncoNet'을...",
#   '인공지능 모델에게 문제의 맥락(Context)을 제시한다는 점에서, 이러한 기법을 흔히...',
#   '이 글에서는 AI타임스, 인공지능신문부터 MIT Technology Review, DeepMind Blog까지...',
#   '인공지능 분야의 최신 연구 동향은 현재 기술이 나아가고 있는 방향과 발전 속도를...',
#   '이번 포스팅에서는 인공지능의 발전 배경부터 시작해, 2023년 시장 전망, 생성 AI의...',
#   '한국수출입은행은 2024년 인공지능 글로벌 트렌드를 분석한 보고서를 발표하였다...',
#   '신한대학교 신종우 교수입니다. "생성인공지능시대, 인공지능과 에듀테크 기반의...',
#   "인공지능 특허 전문 변리사가 분석하는 '오픈AI 이미지 생성' 특허 분석 (10)...",
#   '최신 인공지능 기술동향. State of AI 2022 번역 오프라인 강화학습 기술동향...',
#   '이번 보고서는 2017년부터 발간되어 올해 8번째로, 현재 글로벌 AI 현황에 대한...']
# 어떤 방법을 사용하더라도, 최신 연구 동향에 대해 이해하기 쉽게 설명해주는 기사나 논문을 찾아야 할 것 같다.
# 
# Action: search
# Action Input: 인공지능 최신 연구 기사
# [검색 결과:
#   "서울대 AI연구원–투모로 로보틱스, 누구나 말로 티칭하는 로봇 파운데이션 AI 모델 'CLIP-RT'...",
#   'R&D 심장 대학연구소의 비명. AI·로봇 최첨단 장비 갖춰도 전력공급 못받아 손놓고 있어...',
#   "인공지능 (AI) · AI를 거부하는 사람들: '기계가 쓴 글을 왜 읽어야 하죠? · 애플, BBC...",
#   '임피리얼 칼리지 런던의 한 연구진은 항생제에 내성을 지닌 수퍼박테리아에 관한 연구를...',
#   '멀티모달 AI, 로보틱스, 대형언어모델(LLM), 생성 AI(이미지 및 비디오) 등 다양한 분야에...',
#   "'AI' 섹션에서는 최신 AI 연구 동향과 그 실제 적용 사례를 상세히 다루며, 'The Download'...",
#   '저명한 과학자의 오랜 연구 숙제를 단숨에 해결한 인공지능이 화제다. 임피리얼 칼리지...',
#   '그래서 오늘은 제가 어떤 루트들로 인공지능 관련 뉴스들을 보는지, 그리고 최신 논문들을...',
#   '△ KAIST 뇌인지과학과 이상완 교수(왼쪽), 양민수 박사과정(오른쪽) 연구팀이 스스로...',
#   '최근 발표된 연구에서는 AI가 사람과 자연스럽게 대화할 수 있는 수준에 도달했으며...']
# 이제 최신 연구 동향에 대해 충분히 알게 되었다.
# 
# Final Answer: 현재 인공 지능 에이전트의 최신 연구 진전은 딥러닝, 생성 AI, 항암 치료 기술 등
# 다양한 분야에서 이루어지고 있으며, 인공지능이 인간을 능가하는 성과를 보여주고 있다.
# 최신 연구 동향을 이해하기 위해서는 다양한 방법으로 정보를 수집하고, 쉽게 설명하는
# 기사나 논문을 찾아보는 것이 중요하다.
# > Finished chain.
# 
# 두번째 실행결과:
# 
# > Entering new AgentExecutor chain...
#  에이전트는 지속적으로 발전하기 때문에 최신 연구 진전을 알아봅니다.
# Action: search
# Action Input: 현재 인공 지능 에이전트의 최신 연구 진전
# [검색 결과:
#   'AI Agent와 검색 증강 생성(RAG) 분야는 현재 인공지능 기술의 급속한 발전과 함께...',
#   '즈푸AI는 자사 최신 대형언어모델 GLM-4(보기)가 오픈AI(OpenAI)의 GPT-4를 여러...',
#   "OpenAI는 Humanity's Last Exam 벤치마크에서 25% 이상의 정확도를 자랑하는...",
#   '생성형 AI 시장은 2024년에 258억 6천만 달러로 추정되며, 2034년까지 8, 039억 달러에...',
#   'Deepseek의 R1이 ChatGPT보다 성능이 크게 향상될 것이라는 기대를 받으며 일시적으로...',
#   '심층 연구가 유망한 진전이기는 하지만 아직은 인간의 연구를 완전히 대체할 수는...',
#   "구글이 인공지능 분야의 성과를 바탕으로 최신 주력 모델인 '제미나이 2.0 플래시...",
#   "오픈AI가 생성형 인공지능(AI) 서비스 '챗GPT'부터 사람이 할 일을 대신해주는...",
#   '요약: OpenBrain은 AI를 활용한 AI 연구 자동화로 50% 더 빠른 알고리즘 발전을 이루며...',
#   'AI 에이전트는 마치 눈에 보이지 않는 팀원처럼, 환경 감지부터 의사결정 실행까지...']
# 8개의 검색 결과가 나왔습니다. 최신 연구 진전은 AI 에이전트와 검색 증강 생성 분야, 대형 언어 모델,
# 챗GPT, 인공지능 서비스 다각화 등으로 나타납니다.
# 
# Action: search
# Action Input: 최신 연구 진전
# [검색 결과:
#   '포스터 세션에서는 알레르기 및 면역학 치료를 발전시키기 위한 혁신적인 접근 방식과...',
#   '국내 연구진이 노화된 세포가 몸 전체로 전이되는 이유를 세계 최초로 밝혀냈다. 또한...',
#   '안태범 교수는 "단 10초간의 정적 균형 테스트만으로도 파킨슨병의 존재 여부와 진행...',
#   '인공지능(AI) 및 유전자 편집 기술 등이 발전하며 중국, 북한, 러시아의 생물학 무기...',
#   '콘리 박사의 구두 발표는 육종 및 기타 여러 유형의 암을 치료하기 위해 유전자 변형...',
#   '최근 몇 년 동안 CAR-T 요법 관련 연구가 빠르게 발전하고 있으며, 혈액계 종양에서...',
#   '이 줄기세포 화장품의 시장 확대에는 피부에서의 줄기세포 연구의 진전과 재생의료의...',
#   "최근 MIT 연구진은 '실시간'으로 이미지를 생성할 수 있는 새로운 AI 모델을 개발했다...",
#   '기자회견에서는 PD-1 발견에 일조한 연구원과의 토론이 진행되었으며, 폐암을 예방하고...']
# 9개의 검색 결과가 나왔습니다. 최신 연구 진전은 알레르기 및 면역학 치료, 노화된 세포, 파킨슨병,
# 중국/북한/러시아 생물학 무기, 유전자 변형 아데노바이러스, CAR-T 요법, 줄기세포 화장품,
# 실시간 이미지 생성 AI 모델, PD-1 발견 연구 등으로 나타납니다.
# 
# Thought: 이 중에서도 AI 에이전트와 관련된 연구 발전이 가장 큰 관심을 끌었습니다.
# 
# Final Answer: 현재 인공 지능 에이전트의 최신 연구 진전은 알레르기 및 면역학 치료, 노화된 세포,
# 파킨슨병, 중국/북한/러시아 생물