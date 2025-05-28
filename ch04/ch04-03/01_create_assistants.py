from dotenv import load_dotenv

load_dotenv()

import os

from openai import OpenAI

client = OpenAI()

assistant = client.beta.assistants.create(
    model = "gpt-4o-mini",
    name = "꽃 가격 계산기",
    instructions = "당신은 꽃 가격 계산기입니다. 사용자가 입력한 문장에서 가격을 찾아서 계산하는 일을 합니다.",
    tools = [
        { "type": "code_interpreter" }
    ],
)

print(assistant)

# --- 출력 결과 1 ----
# > python3 assistants_api.py
# Assistant(
#     id='asst_Fe4ClFqfnV758pufAm9sHAXA',
#     created_at=1747297133,
#     description=None,
#     instructions='당신은 꽃 가격 계산기입니다. 사용자가 입력한 문장에서 가격을 찾아서 계산하는 일을 합니다.',
#     metadata={},
#     model='gpt-4o-mini',
#     name='꽃 가격 계산기',
#     object='assistant',
#     tools=[
#         CodeInterpreterTool(type='code_interpreter')
#     ],
#     response_format='auto',
#     temperature=1.0,
#     tool_resources=ToolResources(
#         code_interpreter=ToolResourcesCodeInterpreter(file_ids=[]),
#         file_search=None
#     ),
#     top_p=1.0,
#     reasoning_effort=None
# )

