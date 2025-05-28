from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader
from llama_index.core import VectorStoreIndex
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.llms.openai import OpenAI
from llama_index.core.agent import ReActAgent

load_dotenv()

# 재무 보고서 화일 로드
A_docs = SimpleDirectoryReader(
    input_files=["./data/E-commerce A - Third Quarter 2023 Results.pdf"]
).load_data()
B_docs = SimpleDirectoryReader(
    input_files=["./data/E-commerce B - Third Quarter 2023 Results.pdf"]
).load_data()

# 재무보고서를 벡터 데이터로 변환 (화일기반 벡터DB)
A_index = VectorStoreIndex.from_documents(A_docs)
B_index = VectorStoreIndex.from_documents(B_docs)

# 색앤 영속화 (벡터DB 영속화)

try:
    # index A 가져오기
    A_storage_context = StorageContext.from_defaults(persist_dir="./storage/A")
    A_index = load_index_from_storage(A_storage_context)
    
    # index B 가져오기
    B_storage_context = StorageContext.from_defaults(persist_dir="./storage/B")
    B_index = load_index_from_storage(B_storage_context)
    
    print("Index loaded successfully")
    index_loaded = True
except Exception as e:
    print(f"Error loading index A: {e}")
    index_loaded = False

# 요청 엔진 생성
A_engine = A_index.as_query_engine(similarity_top_k=3)
B_engine = B_index.as_query_engine(similarity_top_k=3)

# 요청 도구 구성
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

# LLM 설정
llm = OpenAI(model="gpt-4o-mini", temperature=0)

# ReActAgent 생성
agent = ReActAgent.from_tools(query_engine_tools, llm=llm, verbose=True)

# 요청 엔진 실행
response = agent.chat("온라인 쇼핑몰 업체 A와 온라인 쇼핑몰 업체 B의 매출을 비교 분석해 주세요.")