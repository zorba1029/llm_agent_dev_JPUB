# 환경 변수 적재하기
from dotenv import load_dotenv

load_dotenv()

# OpenAI 인스턴스 생성
from openai import OpenAI

client = OpenAI()

# ------------------------------------------------------------
# [1] 스레드 생성 (대화 흐름))
# ------------------------------------------------------------
thread = client.beta.threads.create()

# 스레드 조회/출력
print(thread)

# --- 출력 결과 1 ------------
# > python3 ./run_thread.py
# Thread(
#     id='thread_GEDDJlbylJ8PBXOiOUvFVkKh',
#     created_at=1747297666,
#     metadata={},
#     object='thread',
#     tool_resources=ToolResources(
#         code_interpreter=None,
#         file_search=None
#     )
# )

#-------------------------------------------------
# [2] 쓰레드 흐름에 대한 메시지 추가
# ------------------------------------------------
print("\n---- 쓰레드 흐름에 대한 메시지 추가 ----\n")
message = client.beta.threads.messages.create(
    thread_id = thread.id,
    role = "user",
    content="각 꽃다발의 가격을 원가에 20%를 더한 가격으로 책정합니다. 원가가 1600원일 때, 제 판매 가격은 얼마인가요?" 
)

print(message)

#-------------------------------------------------
# [3] 쓰레드 흐름에 대한 메시지 목록 가져오기 (조회)
# ------------------------------------------------
messages = client.beta.threads.messages.list(
    thread_id = thread.id
)

print(messages)

# "\n---- 쓰레드 흐름에 대한 메시지 추가 ----\n"
#-------------------------------------------------
# Message(
#     id='msg_fvAnwvZkQUG8e91h5cG96dcj',
#     assistant_id=None,
#     attachments=[],
#     completed_at=None,
#     content=[
#         TextContentBlock(
#             text=Text(
#                 annotations=[],
#                 value='각 꽃다발의 가격을 원가에 20%를 더한 가격으로 책정합니다. 원가가 1600원일 때, 제 판매 가격은 얼마인가요?'
#             ),
#             type='text'
#         )
#     ],
#     created_at=1747297667,
#     incomplete_at=None,
#     incomplete_details=None,
#     metadata={},
#     object='thread.message',
#     role='user',
#     run_id=None,
#     status=None,
#     thread_id='thread_GEDDJlbylJ8PBXOiOUvFVkKh'
# )

#-------------------------------------------------
# SyncCursorPage[Message](
#     data=[
#         Message(
#             id='msg_fvAnwvZkQUG8e91h5cG96dcj',
#             assistant_id=None,
#             attachments=[],
#             completed_at=None,
#             content=[
#                 TextContentBlock(
#                     text=Text(
#                         annotations=[],
#                         value='각 꽃다발의 가격을 원가에 20%를 더한 가격으로 책정합니다. 원가가 1600원일 때, 제 판매 가격은 얼마인가요?'
#                     ),
#                     type='text'
#                 )
#             ],
#             created_at=1747297667,
#             incomplete_at=None,
#             incomplete_details=None,
#             metadata={},
#             object='thread.message',
#             role='user',
#             run_id=None,
#             status=None,
#             thread_id='thread_GEDDJlbylJ8PBXOiOUvFVkKh'
#         )
#     ],
#     has_more=False,
#     object='list',
#     first_id='msg_fvAnwvZkQUG8e91h5cG96dcj',
#     last_id='msg_fvAnwvZkQUG8e91h5cG96dcj'
# )