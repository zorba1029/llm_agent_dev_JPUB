from dotenv import load_dotenv

load_dotenv()

from llama_index.core import SimpleDirectoryReader

documents = SimpleDirectoryReader("data").load_data()

from llama_index.core import VectorStoreIndex

index = VectorStoreIndex.from_documents(documents)

# 요청 엔진 생성 
agent = index.as_query_engine()

# 요청 예제
response = agent.query("꽃말의 비밀 정원의 직원에게는 몇 가지 역할이 있나요?")
print("꽃말의 비밀 정원의 직원들에게는 몇 가지 역할이 있나요?", response)

response = agent.query("꽃말의 비밀 정원의 에이전트 이름은 무엇인가요?")
print("꽃말의 비밀 정원의 에이전트 이름은 무엇인가요?", response)

# 색인을 로컬에 저장
index.storage_context.persist()

# 색인 로드
# index = VectorStoreIndex.from_defaults(storage_context=storage_context)

# --- 출력 결과 1 ----
# > python3 llamaindex_ex.py
# 꽃말의 비밀 정원의 직원들에게는 몇 가지 역할이 있나요? 
# -- 직원들에게는 마케팅 전문가, 기술 천재, 고객 서비스의 천사 등 다양한 역할이 있습니다. 
# 이 모험에서 각 직원은 중요한 영웅으로서 꽃말의 비밀 정원의 성장과 발전에 직접적인 영향을 미칠 것입니다.
# 
# 꽃말의 비밀 정원의 에이전트 이름은 무엇인가요? 
# -- 꽃말의 비밀 정원의 에이전트 이름은 "꽃말 요정"입니다.
