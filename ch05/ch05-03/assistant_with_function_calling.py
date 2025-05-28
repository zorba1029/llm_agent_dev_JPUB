from dotenv import load_dotenv

load_dotenv()

from openai import OpenAI

client = OpenAI()

#----------------------------------------------------
# assistant 생성
# print('--- assistant 생성 시작 ---')
def make_new_assistant_id():
    assistant = client.beta.assistants.create(
        instructions='당신은 친절한 도우미입니다. 사용자의 요청에 따라 적절한 응답을 합니다.',
        model='gpt-4o-mini',
        tools=[
            {
                'type': 'function',
                'function': {
                    'name': 'get_encouragement',
                    'description': '사용자의 기분에 따라 응원 메시지를 제공한다.',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'mood': {
                                'type': 'string',
                                'description': '사용자의 현재 기분, 예: 행복, 슬픔, 스트레스, 피곤함'
                            },
                            'name': {
                                'type': 'string', 
                                'description': '응원 메시지를 맞춤화하기 위한 사용자의 이름'
                            }
                        },
                        'required': ['mood']
                    }
                }
            }
        ]
    )
    return assistant.id

#------------------------------------------
# assistant 정보 출력
# 이전에 생성한 assistant id
def use_existing_assistant(assistant_id):
    assistant = client.beta.assistants.retrieve(assistant_id)
    return assistant

#------------------------------------------
# 새로운 thread (대화흐름) 생성
def create_new_thread():
    thread = client.beta.threads.create()
    print(f"대화흐름 thread 정보: \n{thread}\n")
    return thread


#------------------------------------------
# 새로운 메시지 추가
def create_new_message(thread_id, content):
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=content
    )
    print(f"메시지 정보: \n{message}\n")
    return message


#------------------------------------------
# 실행세션 생성하여 thread  처리
def create_new_run(thread_id, assistant_id):
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )
    print(f"실행세션 초기 정보: \n{run}\n")
    return run

#------------------------------------------
# 실행세션 상태 확인
import time

def check_run_status(thread_id, run_id):
    n = 0
    while True:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
        )

        print(f"----------------\n{n} 번째 실행세션 상태: {run}\n")
        print(f"실행세션 상태: {run.status} \n----------------\n")
    
        if run.status == 'completed':
            return True 

        n += 1
        time.sleep(5)
    return False

#------------------------------------------
# 대화 흐름에서 assistant 응답 가져오기
def get_assistant_response(thread_id):
    messages = client.beta.threads.messages.list(
        thread_id=thread_id
    )

    print(f"대화 흐름에서 assistant 응답 가져오기: \n{messages}\n")

    for message in messages:
       print(f"assistant 응답 메시지 내용: {message.content[0].text.value}")

#===========================================================
# 메인 함수
#===========================================================

def main():
    # 1. assistant 생성
    assistant = use_existing_assistant("asst_v1aqnERZOSjnAe7MemXcUzxv")
    # assistant_id = make_new_assistant_id()

    # 2. thread 생성
    thread = create_new_thread()

    # 3. 메시지 추가
    create_new_message(thread.id, "안녕하세요! 슬픈 예나를 위로 해 주세요!")

    # 4. 실행세션 생성
    run = create_new_run(thread.id, assistant.id)

    # 5. 실행세션 상태 확인
    check_run_status(thread.id, run.id)

    # 6. assistant 응답 가져오기
    get_assistant_response(thread.id)

if __name__ == "__main__":
    main()


# print('--- assistant 생성 완료 ---')
# print(assistant)
#-- assistan_id = 'asst_v1aqnERZOSjnAe7MemXcUzxv'
