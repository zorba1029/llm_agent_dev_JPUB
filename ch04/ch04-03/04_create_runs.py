# 환경 변수 적재하기
from dotenv import load_dotenv

load_dotenv()

# OpenAI 인스턴스 생성
from openai import OpenAI

client = OpenAI()

# ------------------------------------------------------------
# [1] 잎에서 실행한, run_thread.py 에서 생성한 스레드에 대한 실행 세션 생성
# ------------------------------------------------------------
run = client.beta.threads.runs.create(
    thread_id = 'thread_GEDDJlbylJ8PBXOiOUvFVkKh',
    assistant_id = 'asst_Fe4ClFqfnV758pufAm9sHAXA',
    instructions = "질문에 대답 해주세요."
)

print(run)

#-------------------------------------------------
# [2] 실행 세션 상태 다시 가져오기
# ------------------------------------------------
run = client.beta.threads.runs.retrieve(
    thread_id = 'thread_GEDDJlbylJ8PBXOiOUvFVkKh',
    run_id = run.id
)

print(run)

#--- 출력 결과 1 ----
# > python3 run.py
# Run(
#     id='run_KtjoyMzSKbrRFxOyPD8Qz731',
#     assistant_id='asst_Fe4ClFqfnV758pufAm9sHAXA',
#     cancelled_at=None,
#     completed_at=None,
#     created_at=1747298203,
#     expires_at=1747298803,
#     failed_at=None,
#     incomplete_details=None,
#     instructions='질문에 대답 해주세요.',
#     last_error=None,
#     max_completion_tokens=None,
#     max_prompt_tokens=None,
#     metadata={},
#     model='gpt-4o-mini',
#     object='thread.run',
#     parallel_tool_calls=True,
#     required_action=None,
#     response_format='auto',
#     started_at=None,
#     status='queued',
#     thread_id='thread_GEDDJlbylJ8PBXOiOUvFVkKh',
#     tool_choice='auto',
#     tools=[
#         CodeInterpreterTool(type='code_interpreter')
#     ],
#     truncation_strategy=TruncationStrategy(
#         type='auto',
#         last_messages=None
#     ),
#     usage=None,
#     temperature=1.0,
#     top_p=1.0,
#     tool_resources={},
#     reasoning_effort=None
# )

#--- 출력 결과 2 ----
# Run(
#     id='run_KtjoyMzSKbrRFxOyPD8Qz731',
#     assistant_id='asst_Fe4ClFqfnV758pufAm9sHAXA',
#     cancelled_at=None,
#     completed_at=None,
#     created_at=1747298203,
#     expires_at=1747298803,
#     failed_at=None,
#     incomplete_details=None,
#     instructions='질문에 대답 해주세요.',
#     last_error=None,
#     max_completion_tokens=None,
#     max_prompt_tokens=None,
#     metadata={},
#     model='gpt-4o-mini',
#     object='thread.run',
#     parallel_tool_calls=True,
#     required_action=None,
#     response_format='auto',
#     started_at=None,
#     status='queued',
#     thread_id='thread_GEDDJlbylJ8PBXOiOUvFVkKh',
#     tool_choice='auto',
#     tools=[
#         CodeInterpreterTool(type='code_interpreter')
#     ],
#     truncation_strategy=TruncationStrategy(
#         type='auto',
#         last_messages=None
#     ),
#     usage=None,
#     temperature=1.0,
#     top_p=1.0,
#     tool_resources={},
#     reasoning_effort=None
# )
