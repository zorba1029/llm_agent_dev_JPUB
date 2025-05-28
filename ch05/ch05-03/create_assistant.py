# 시스템 변수 적재
from dotenv import load_dotenv

load_dotenv()

# OpenAI 인스턴스 생성
from openai import OpenAI

client = OpenAI()

# 도우미 생성
assistant = client.beta.assistants.create(
    instructions="You are a very encouraging assistant!",
    model="gpt-4o-mini",
    tools=[
        {
            "type": "function",
            "function": {
                "name": "get_encouragement",
                "description": "사용자의 기분에 따라 응원 메시지를 제공합니다.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "mood": {
                            "type": "string",
                            "description": "사용자의 현재 기분, 예: 행복, 슬픔, 스트레스, 피곤함"
                        },
                        "name": {
                            "type": "string",
                            "description": "응원 메시지를 맞춤화하기 위한 사용자의 이름"
                        }
                    },
                    "required": ["mood"]
                }
            }
        }
    ]
)

# 도우미 출력
print(assistant)

# > python3 ./create_assistant.py
# Assistant(id='asst_v1aqnERZOSjnAe7MemXcUzxv', created_at=1747933470, description=None, instructions='You are a very encouraging assistant!', metadata={}, model='gpt-4o-mini', name=None, object='assistant', tools=[FunctionTool(function=FunctionDefinition(name='get_encouragement', description='사용자의 기분에 따라 응원 메시지를 제공합니다.', parameters={'type': 'object', 'properties': {'mood': {'type': 'string', 'description': '사용자의 현재 기분, 예: 행복, 슬픔, 스트레스, 피곤함'}, 'name': {'type': 'string', 'description': '응원 메시지를 맞춤화하기 위한 사용자의 이름'}}, 'required': ['mood']}, strict=False), type='function')], response_format='auto', temperature=1.0, tool_resources=ToolResources(code_interpreter=None, file_search=None), top_p=1.0, reasoning_effort=None)

