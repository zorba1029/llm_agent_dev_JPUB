# 환경 변수 적재하기
from dotenv import load_dotenv

load_dotenv()

import time

# OpenAI 인스턴스 생성
from openai import OpenAI

client = OpenAI()

# ------------------------------------------------------------
# 스레드 아이디와 어시스턴트 아이디 설정 - 이전 단계에서 생성한 스레드와 어시스턴트
# ------------------------------------------------------------
thread_id = 'thread_GEDDJlbylJ8PBXOiOUvFVkKh'
assistant_id = 'asst_Fe4ClFqfnV758pufAm9sHAXA'

# ------------------------------------------------------------
# [1] 실행 세션 생성
# ------------------------------------------------------------
run = client.beta.threads.runs.create(
    thread_id = thread_id,
    assistant_id = assistant_id,
    instructions = "질문에 답변 해 주세요."
)

# 확인 시간간격 설정(5초)
polling_interval = 5

# 실행 세션 상태 확인 시작
while True:
    run = client.beta.threads.runs.retrieve(
        thread_id = thread_id,
        run_id = run.id
    )
    
    # 실행 세션 객체의 속성에 대한 접근
    status = run.status
    
    print(f"현재 실행 세션 상태: {status}")
    
    # 실행 세션의 상태가 'completed', 'failed', 'expired' 중 경우 종료
    if status in ['completed', 'failed', 'expired']:
        break
    
    # 확인 시간간격 만큼 대기 후 반복
    time.sleep(polling_interval)

# 실행 세션 완료 후 결과 출력
if status == 'completed':
    print("\n실행 세션이 완료되었습니다.")
    print(f"실행 세션 아이디: {run.id}")
    print(f"실행 세션 상태: {status}")
elif status in ['failed', 'expired']:
    print(f"\n실행 세션 실패 또는 종료: {run.last_error.message}")
    
    

# --- 출력 결과 1 ------------
# > python3 05_get_run_status.py
# 현재 실행 세션 상태: in_progress
# 현재 실행 세션 상태: completed

# 실행 세션이 완료되었습니다.
# 실행 세션 아이디: run_Pj5pAt3ruoDudnSk0zSdLors
# 실행 세션 상태: completed

# --- 출력 결과 2 ------------
# > python3 05_get_run_status.py
# 현재 실행 세션 상태: in_progress
# 현재 실행 세션 상태: completed

# 실행 세션이 완료되었습니다.
# 실행 세션 아이디: run_1GVhB0OhA3CKdIdVchGhAboi
# 실행 세션 상태: completed