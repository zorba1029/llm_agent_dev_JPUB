# 시스템 변수 적재
from dotenv import load_dotenv

load_dotenv()

# OpenAI 인스턴스 생성
from openai import OpenAI

client = OpenAI()

#==============================================
# 이전에 생성한 assistant id
assistant_id = "asst_v1aqnERZOSjnAe7MemXcUzxv"

# 새로운 thread (대화흐름) 생성
thread = client.beta.threads.create()

print(f"대화흐름 thread 정보: \n{thread}\n")

#==============================================
# 새로운 메시지 추가
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="안녕하세요! 슬픈 예나를 위로 해 주세요!"
)

print(f"메시지 정보: \n{message}\n")

#==============================================
# 실행세션 생성하여 대화 흐름 처리
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant_id
)

print(f"실행세션 정보: \n{run}\n")

#==============================================
# 실행세션 상태 확인
import time

n = 0
while True:
    run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )

    print(f"-------------------\n{n} 번째 실행세션 상태: {run}\n-------------------\n")

    if run.status == "completed":
        break

    n += 1
    time.sleep(5)

#==============================================
# 대화 흐름에서 assistant 응답 가져오기
messages = client.beta.threads.messages.list(
    thread_id=thread.id
)

# print(f"대화 흐름에서 assistant 응답 가져오기: \n{messages}\n")
# assistant 응답 출력
for message in messages:
    print(f"assistant 응답 메시지 내용: {message.content[0].text.value}")
