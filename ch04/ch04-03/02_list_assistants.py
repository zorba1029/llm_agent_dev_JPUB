from dotenv import load_dotenv

load_dotenv()

from openai import OpenAI

client = OpenAI()

assistants = client.beta.assistants.list()

print(assistants)

# --- 출력 결과 1 ----
# > python3 run_response.py
# SyncCursorPage[Assistant](
#     data=[
#         Assistant(
#             id='asst_Fe4ClFqfnV758pufAm9sHAXA',
#             created_at=1747297133,
#             description=None,
#             instructions='당신은 꽃 가격 계산기입니다. 사용자가 입력한 문장에서 가격을 찾아서 계산하는 일을 합니다.',
#             metadata={},
#             model='gpt-4o-mini',
#             name='꽃 가격 계산기',
#             object='assistant',
#             tools=[
#                 CodeInterpreterTool(type='code_interpreter')
#             ],
#             response_format='auto',
#             temperature=1.0,
#             tool_resources=ToolResources(
#                 code_interpreter=ToolResourcesCodeInterpreter(file_ids=[]),
#                 file_search=None
#             ),
#             top_p=1.0,
#             reasoning_effort=None
#         ),
#         Assistant(
#             id='asst_oo03LSeW0zL568N2pmBKmgx8',
#             created_at=1747297121,
#             description=None,
#             instructions='당신은 꼭 가격 계산기입니다. 사용자가 입력한 문장에서 가격을 찾아서 계산하는 일을 합니다.',
#             metadata={},
#             model='gpt-4o-mini',
#             name='꼭 가격 계산기',
#             object='assistant',
#             tools=[
#                 CodeInterpreterTool(type='code_interpreter')
#             ],
#             response_format='auto',
#             temperature=1.0,
#             tool_resources=ToolResources(
#                 code_interpreter=ToolResourcesCodeInterpreter(file_ids=[]),
#                 file_search=None
#             ),
#             top_p=1.0,
#             reasoning_effort=None
#         ),
#         Assistant(
#             id='asst_QDz2ScRc7qvXy1IrXfU4f1bA',
#             created_at=1747297053,
#             description=None,
#             instructions='당신은 꼭 가격 계산기입니다. 사용자가 입력한 문장에서 가격을 찾아서 계산하는 일을 합니다.',
#             metadata={},
#             model='gpt-4o-mini',
#             name='꼭 가격 계산기',
#             object='assistant',
#             tools=[
#                 CodeInterpreterTool(type='code_interpreter')
#             ],
#             response_format='auto',
#             temperature=1.0,
#             tool_resources=ToolResources(
#                 code_interpreter=ToolResourcesCodeInterpreter(file_ids=[]),
#                 file_search=None
#             ),
#             top_p=1.0,
#             reasoning_effort=None
#         ),
#         Assistant(
#             id='asst_AIlcj7mhPtwLx14swCTwuJpo',
#             created_at=1747296407,
#             description=None,
#             instructions='당신은 꼭 가격 계산기입니다. 사용자가 입력한 문장에서 가격을 찾아서 계산하는 일을 합니다.',
#             metadata={},
#             model='gpt-4o-mini',
#             name='꼭 가격 계산기',
#             object='assistant',
#             tools=[
#                 CodeInterpreterTool(type='code_interpreter')
#             ],
#             response_format='auto',
#             temperature=1.0,
#             tool_resources=ToolResources(
#                 code_interpreter=ToolResourcesCodeInterpreter(file_ids=[]),
#                 file_search=None
#             ),
#             top_p=1.0,
#             reasoning_effort=None
#         ),
#         Assistant(
#             id='asst_dxupNYxEAKdMokvBRSJhP828',
#             created_at=1747296368,
#             description=None,
#             instructions='당신은 꼭 가격 계산기입니다. 사용자가 입력한 문장에서 가격을 찾아서 계산하는 일을 합니다.',
#             metadata={},
#             model='gpt-4o-mini',
#             name='꼭 가격 계산기',
#             object='assistant',
#             tools=[
#                 CodeInterpreterTool(type='code_interpreter')
#             ],
#             response_format='auto',
#             temperature=1.0,
#             tool_resources=ToolResources(
#                 code_interpreter=ToolResourcesCodeInterpreter(file_ids=[]),
#                 file_search=None
#             ),
#             top_p=1.0,
#             reasoning_effort=None
#         )
#     ],
#     has_more=False,
#     object='list',
#     first_id='asst_Fe4ClFqfnV758pufAm9sHAXA',
#     last_id='asst_dxupNYxEAKdMokvBRSJhP828'
# )
