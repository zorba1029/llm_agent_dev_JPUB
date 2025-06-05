from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader
from llama_index.core import VectorStoreIndex
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.llms.openai import OpenAI
from llama_index.core.agent import ReActAgent

load_dotenv()

# [1] 재무 보고서 화일 로드
print("[1] 재무 보고서 화일 로드")
A_docs = SimpleDirectoryReader(
    input_files=["./data/E-commerce A - Third Quarter 2023 Results.pdf"]
).load_data()
B_docs = SimpleDirectoryReader(
    input_files=["./data/E-commerce B - Third Quarter 2023 Results.pdf"]
).load_data()

# [2] 재무보고서를 벡터 데이터로 변환 (화일기반 벡터DB)
print("[2] 재무 보고서를 벡터 데이터로 변환 (화일기반 벡터DB)")
A_index = VectorStoreIndex.from_documents(A_docs)
B_index = VectorStoreIndex.from_documents(B_docs)

# [3] 색앤 영속화 (벡터DB 영속화)
print("[3] 색앤 영속화 (벡터DB 영속화)")
A_index.storage_context.persist(persist_dir="./storage/A")
B_index.storage_context.persist(persist_dir="./storage/B")

# [4] index 로드하기
print("[4] index 로드하기")
try:
    # [4-1] index A 가져오기
    print("   [4-1] index A 가져오기")
    A_storage_context = StorageContext.from_defaults(persist_dir="./storage/A")
    A_index = load_index_from_storage(A_storage_context)
    
    # [4-2] index B 가져오기
    print("   [4-2] index B 가져오기")
    B_storage_context = StorageContext.from_defaults(persist_dir="./storage/B")
    B_index = load_index_from_storage(B_storage_context)
    
    print("   [4-3] Index loaded successfully")
    index_loaded = True
except Exception as e:
    print(f"   [4-3] Error loading index A: {e}")
    index_loaded = False

# [5] 요청 엔진 생성
print("[5] 요청 엔진 생성")
A_engine = A_index.as_query_engine(similarity_top_k=3)
B_engine = B_index.as_query_engine(similarity_top_k=3)

# [6] 요청 도구 구성
print("[6] 요청 도구 구성")
query_engine_tools = [
    QueryEngineTool(
        query_engine=A_engine,
        metadata=ToolMetadata(
            name="A_Finance",
            description="온라인 쇼핑몰 업체 A의 재무 정보를 제공하는 도구",
        ),
    ),
    QueryEngineTool(
        query_engine=B_engine,
        metadata=ToolMetadata(
            name="B_Finance",
            description="온라인 쇼핑몰 업체 B의 재무 정보를 제공하는 도구",
        ),
    )
]

# [7] LLM 설정
print("[7] LLM 설정")
llm = OpenAI(model="gpt-4o-mini", temperature=0)

# [8] ReActAgent 생성
print("[8] ReActAgent 생성")
agent = ReActAgent.from_tools(query_engine_tools, llm=llm, verbose=True)

# [9] 요청 엔진 실행
print("[9] 요청 엔진 실행")
response = agent.chat("온라인 쇼핑몰 업체 A와 온라인 쇼핑몰 업체 B의 매출을 비교 분석해 주세요.")
print(response)

# ==========================================================
# > python3 react_rag_agent.py
# [1] 재무 보고서 화일 로드
# [2] 재무 보고서를 벡터 데이터로 변환 (화일기반 벡터DB)
# [3] 색앤 영속화 (벡터DB 영속화)
# [4] index 로드하기
#    [4-1] index A 가져오기
#    [4-2] index B 가져오기
# Index loaded successfully
# [5] 요청 엔진 생성
# [6] 요청 도구 구성
# [7] LLM 설정
# [8] ReActAgent 생성
# [9] 요청 엔진 실행
# > Running step a424be40-5009-469e-8347-59c1e270a083. Step input: 온라인 쇼핑몰 업체 A와 온라인 쇼핑몰 업체 B의 매출을 비교 분석해 주세요.
# Thought: The current language of the user is: Korean. I need to use tools to gather financial information about both online shopping mall companies A and B to compare their sales.
# Action: A_Finance
# Action Input: {'input': '매출'}
# Observation: Sales and marketing expenses increased by 12.4% to US$918.0 million in the third quarter of 2023 from US$816.7 million in the third quarter of 2022. Core marketplace revenue, including transaction-based fees and advertising revenues, was up 31.7% year-on-year to US$1.3 billion. E-commerce GAAP revenue was US$2.2 billion, showing a 16.2% increase year-on-year.
# > Running step 3332462d-f7dc-439a-8cb8-4d5fb245ee8f. Step input: None
# Thought: I have obtained the sales information for online shopping mall company A. Now, I will gather the sales information for online shopping mall company B.
# Action: B_Finance
# Action Input: {'input': '매출'}
# Observation: Total segment revenue for the period was RMB492,965 million (US$67,566 million), showing an 11% increase year-over-year.
# > Running step 6ac80abc-c8c9-4b9e-aee3-0d8d2ed45b38. Step input: None
# Thought: I have obtained the sales information for both online shopping mall companies A and B. Now I can compare their sales.
# Answer: 온라인 쇼핑몰 업체 A의 매출은 다음과 같습니다:
# - 핵심 마켓플레이스 수익: 13억 달러 (31.7% 증가)
# - 전자상거래 GAAP 수익: 22억 달러 (16.2% 증가)

# 온라인 쇼핑몰 업체 B의 매출은 다음과 같습니다:
# - 총 세그먼트 수익: 675억 6600만 달러 (11% 증가)

# 비교 분석 결과:
# - 업체 A의 전자상거래 GAAP 수익이 업체 B의 총 세그먼트 수익보다 높습니다.
# - 업체 A는 전년 대비 더 높은 성장률(16.2% 및 31.7%)을 보이고 있으며, 업체 B는 11%의 증가율을 기록했습니다.

# 결론적으로, 업체 A가 매출과 성장률 모두에서 업체 B보다 우수한 성과를 보이고 있습니다.
# 온라인 쇼핑몰 업체 A의 매출은 다음과 같습니다:
# - 핵심 마켓플레이스 수익: 13억 달러 (31.7% 증가)
# - 전자상거래 GAAP 수익: 22억 달러 (16.2% 증가)

# 온라인 쇼핑몰 업체 B의 매출은 다음과 같습니다:
# - 총 세그먼트 수익: 675억 6600만 달러 (11% 증가)

# 비교 분석 결과:
# - 업체 A의 전자상거래 GAAP 수익이 업체 B의 총 세그먼트 수익보다 높습니다.
# - 업체 A는 전년 대비 더 높은 성장률(16.2% 및 31.7%)을 보이고 있으며, 업체 B는 11%의 증가율을 기록했습니다.

# 결론적으로, 업체 A가 매출과 성장률 모두에서 업체 B보다 우수한 성과를 보이고 있습니다.
