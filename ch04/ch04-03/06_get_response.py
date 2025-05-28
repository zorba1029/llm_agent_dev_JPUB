# 환경 변수 적재하기
from dotenv import load_dotenv

load_dotenv()

# OpenAI 인스턴스 생성
from openai import OpenAI

client = OpenAI()

# thread id 설정
thread_id = 'thread_GEDDJlbylJ8PBXOiOUvFVkKh'

# thread에서 메시지 읽기
messages = client.beta.threads.messages.list(
    thread_id = thread_id
)

# 메시지 목록 출력
print(messages)

# --- 출력 결과 1 ------------
# > python3 06_get_response.py
# SyncCursorPage[Message](
#     data=[
#         Message(
#             id='msg_XcqN9g7ukpkOS0nFBJvu8QRo',
#             assistant_id='asst_Fe4ClFqfnV758pufAm9sHAXA',
#             attachments=[],
#             completed_at=None,
#             content=[
#                 TextContentBlock(
#                     text=Text(
#                         annotations=[],
#                         value='더 궁금한 점이나 추가로 알고 싶은 사항이 있으신가요?'
#                     ),
#                     type='text'
#                 )
#             ],
#             created_at=1747299446,
#             incomplete_at=None,
#             incomplete_details=None,
#             metadata={},
#             object='thread.message',
#             role='assistant',
#             run_id='run_1GVhB0OhA3CKdIdVchGhAboi',
#             status=None,
#             thread_id='thread_GEDDJlbylJ8PBXOiOUvFVkKh'
#         ),
#         Message(
#             id='msg_s7IVvFIRFSKtkjEBZZcK3hDr',
#             assistant_id='asst_Fe4ClFqfnV758pufAm9sHAXA',
#             attachments=[],
#             completed_at=None,
#             content=[
#                 TextContentBlock(
#                     text=Text(
#                         annotations=[],
#                         value='원가가 1600원일 때, 판매 가격은 1920원입니다.'
#                     ),
#                     type='text'
#                 )
#             ],
#             created_at=1747299393,
#             incomplete_at=None,
#             incomplete_details=None,
#             metadata={},
#             object='thread.message',
#             role='assistant',
#             run_id='run_Pj5pAt3ruoDudnSk0zSdLors',
#             status=None,
#             thread_id='thread_GEDDJlbylJ8PBXOiOUvFVkKh'
#         ),
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
#     first_id='msg_XcqN9g7ukpkOS0nFBJvu8QRo',
#     last_id='msg_fvAnwvZkQUG8e91h5cG96dcj'
# )
