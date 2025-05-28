import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-4o-mini",
    response_format={"type": "json_object"},
    messages=[
        {"role": "system", "content": "당신은 사용자가 꽃에 대한 정보를 이해하도록 돕는 지능형 비서이며, JSON 형식의 내용을 출력할 수 있습니다."},
        {"role": "user", "content": "생일 선물로 어떤 꽃이 가장 좋을까요?"},
        {"role": "assistant", "content": "장미꽃은 생일 선물로 인기 있는 선택입니다."},
        {"role": "user", "content": "배송에는 얼마나 걸리나요?"},
    ],
)

# import json
# from pprint import pprint
# 응답 출력
print(response)

# 응답에서 메시지 내용만 출력
print(response.choices[0].message.content)
