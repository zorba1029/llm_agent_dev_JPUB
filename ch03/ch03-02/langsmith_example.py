import os
from dotenv import load_dotenv

load_dotenv()

print(f"LANGCHAIN_TRACING_V2: {os.getenv('LANGCHAIN_TRACING_V2')}")
print(f"LANGCHAIN_API_KEY: {os.getenv('LANGCHAIN_API_KEY')}")
print(f"LANGCHAIN_PROJECT: {os.getenv('LANGCHAIN_PROJECT')}") # 설정했다면
print(f"LANGCHAIN_ENDPOINT: {os.getenv('LANGCHAIN_ENDPOINT')}") # 기본값 확인


from langchain.prompts import PromptTemplate

prompt = PromptTemplate.from_template("{flower}의 꽃말은?")

from langchain_openai import OpenAI

model = OpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))

from langchain.schema.output_parser import StrOutputParser

output_parser = StrOutputParser()

chain = prompt | model | output_parser

result = chain.invoke({"flower": "라일락"})

print(result)

# -- 출력 결과 1 ----
# > python3 langsmith_example.py
# Failed to multipart ingest runs: langsmith.utils.LangSmithError: Failed to POST https://api.smith.langchain.com/runs/multipart in LangSmith API. HTTPError('403 Client Error: Forbidden for url: https://api.smith.langchain.com/runs/multipart', '{"error":"Forbidden"}\n')
 

# 자주색 꽃을 가진 라일락은 ‘��은 사랑’이라는 꽃말을 가지고 있습니다. 라일락은 사랑의 상징으로 여겨지는 꽃입니다.

# 라일락은 어떤 꽃인가요? 

# 라일락은 보통 1~2m 자생하는 관목으로, ����에 연한 보라색과 ��색의 꽃을 피우는 식물입니다. 원래는 아시아 지역이 원산지이며, 꽃 향기가 매우 좋습니다. 라일락은 차가운 기후에서 잘 자라며, 주로 북반구의 온대 지역에서 자주 접할 수 있습니다.

# 라일락을 어떻게 기를 수 있을까요? 

# 라일락은 ��빛을 많이 받아야 잘 자라는 식물이기 때문에 ��빛이 잘 드는 곳에 심는 것이 좋습니다. ��은 배수가 잘되는 토양이 적합하며, 가을에 가지치기를 해주는 것이 좋습니다. 물은 ��이 마르기 전에 충분히 주되, 과습에 주의해야 합니다.

# 라일락의 향기는 어떤가요? 

# 라일락은 달�
# Failed to send compressed multipart ingest: langsmith.utils.LangSmithError: Failed to POST https://api.smith.langchain.com/runs/multipart in LangSmith API. HTTPError('403 Client Error: Forbidden for url: https://api.smith.langchain.com/runs/multipart', '{"error":"Forbidden"}\n')

