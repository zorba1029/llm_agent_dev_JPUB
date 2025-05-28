import json

from dotenv import load_dotenv

load_dotenv()

# OpenAI 인스턴스 생성
from openai import OpenAI

client = OpenAI()

# 지정된 도시의 꽃 재고 조회 함수
def get_flower_inventory(city):
    if "서울" in city:
        return json.dumps({"city": "서울", "inventory": "장미: 100, 듈립: 150"})
    elif "대전" in city:
        return json.dumps({"city": "대전", "inventory": "백합: 80, 카네이션: 120"})
    elif "광주" in city:
        return json.dumps({"city": "광주", "inventory": "해바라기: 200, 목련: 90"})
    else:
        return json.dumps({"city": city, "inventory": "알 수 없음"})

# 도구 목록 정의 (함수 속정 정보)
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_flower_inventory",
            "description": "지정된 도시의 꽃 재고 조회",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "도시, 예: 서울, 대전, 광주"
                    }
                },
                "required": ["city"]
            }
        }
    }
]

# 대화내용 초기화
messages = [
    {
        "role": "user",
        "content": "서울, 대전, 광주의 꽃 재고는 얼마 인가요?"
    }
]

print(f"\n[1] 대화내용 초기화: {messages}")

# 첫번째 대화 응답
first_response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    tools=tools,
    tool_choice="auto",
)

# 응답내용 출력
print(f"\n[2] 첫번째 대화 응답: {first_response}")

response_message = first_response.choices[0].message
print(f"\n[2] 첫번째 대화 응답 메시지만 출력: {response_message}")

# 도구 호출 필요 여부 확인
tool_calls = response_message.tool_calls

if tool_calls:
    messages.append(response_message)

# 도구 호출이 필요한 경우, 도구를 호출하고 재고 조회결과 추가
for tool_call in tool_calls:
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments)
    function_response = get_flower_inventory(
        city=function_args["city"]
    )
    messages.append(
        {
            "tool_call_id": tool_call.id,
            "role": "tool",
            "name": function_name,
            "content": function_response,
        }
    )

# 현재 메시지 목록 출력
print(f"\n[3] 현재 메시지 목록: {messages}")

# 두번째 요청을 통해 최종 응답 받기
final_response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
)

# 최종 응답 출력
print(f"\n[4] 최종 응답: {final_response}")

# 최종 내용만 출력
content = final_response.choices[0].message.content

print(f"\n[5] 최종 내용만 출력: {content}")

#-----------------------------------------
# > python3 fn_calling_via_chatcompletion_api.py

# [1] 대화내용 초기화: [{'role': 'user', 'content': '서울, 대전, 광주의 꽃 재고는 얼마 인가요?'}]

# [2] 첫번째 대화 응답: ChatCompletion(id='chatcmpl-Bbmc8Wos901W1aEX8of2cbJ6ZVvQq', choices=[Choice(finish_reason='tool_calls', index=0, logprobs=None, message=ChatCompletionMessage(content=None, refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=[ChatCompletionMessageToolCall(id='call_6OrB876GIGUPkZg7IOHL9P0A', function=Function(arguments='{"city": "서울"}', name='get_flower_inventory'), type='function'), ChatCompletionMessageToolCall(id='call_e7YNWtFLfr8LVk89xgvEe01T', function=Function(arguments='{"city": "대전"}', name='get_flower_inventory'), type='function'), ChatCompletionMessageToolCall(id='call_K9fIqMa2FaaMlvbN7NChiYiI', function=Function(arguments='{"city": "광주"}', name='get_flower_inventory'), type='function')]))], created=1748344708, model='gpt-4o-mini-2024-07-18', object='chat.completion', service_tier='default', system_fingerprint='fp_54eb4bd693', usage=CompletionUsage(completion_tokens=66, prompt_tokens=77, total_tokens=143, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=0, audio_tokens=0, reasoning_tokens=0, rejected_prediction_tokens=0), prompt_tokens_details=PromptTokensDetails(audio_tokens=0, cached_tokens=0)))

# [3] 현재 메시지 목록: [{'role': 'user', 'content': '서울, 대전, 광주의 꽃 재고는 얼마 인가요?'}, ChatCompletionMessage(content=None, refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=[ChatCompletionMessageToolCall(id='call_6OrB876GIGUPkZg7IOHL9P0A', function=Function(arguments='{"city": "서울"}', name='get_flower_inventory'), type='function'), ChatCompletionMessageToolCall(id='call_e7YNWtFLfr8LVk89xgvEe01T', function=Function(arguments='{"city": "대전"}', name='get_flower_inventory'), type='function'), ChatCompletionMessageToolCall(id='call_K9fIqMa2FaaMlvbN7NChiYiI', function=Function(arguments='{"city": "광주"}', name='get_flower_inventory'), type='function')]), {'tool_call_id': 'call_6OrB876GIGUPkZg7IOHL9P0A', 'role': 'tool', 'name': 'get_flower_inventory', 'content': '{"city": "\\uc11c\\uc6b8", "inventory": "\\uc7a5\\ubbf8: 100, \\ub4c8\\ub9bd: 150"}'}, {'tool_call_id': 'call_e7YNWtFLfr8LVk89xgvEe01T', 'role': 'tool', 'name': 'get_flower_inventory', 'content': '{"city": "\\ub300\\uc804", "inventory": "\\ubc31\\ud569: 80, \\uce74\\ub124\\uc774\\uc158: 120"}'}, {'tool_call_id': 'call_K9fIqMa2FaaMlvbN7NChiYiI', 'role': 'tool', 'name': 'get_flower_inventory', 'content': '{"city": "\\uad11\\uc8fc", "inventory": "\\ud574\\ubc14\\ub77c\\uae30: 200, \\ubaa9\\ub828: 90"}'}]

# [4] 최종 응답: ChatCompletion(id='chatcmpl-BbmcBXUv0FC2GGk4maQtDV2RB7svr', choices=[Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='각 도시의 꽃 재고는 다음과 같습니다:\n\n- **서울**: 장미 100개, 튤립 150개\n- **대전**: 백합 80개, 카네이션 120개\n- **광주**: 해바라기 200개, 몬스테라 90개', refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=None))], created=1748344711, model='gpt-4o-mini-2024-07-18', object='chat.completion', service_tier='default', system_fingerprint='fp_34a54ae93c', usage=CompletionUsage(completion_tokens=70, prompt_tokens=223, total_tokens=293, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=0, audio_tokens=0, reasoning_tokens=0, rejected_prediction_tokens=0), prompt_tokens_details=PromptTokensDetails(audio_tokens=0, cached_tokens=0)))

# [5] 최종 내용만 출력: 각 도시의 꽃 재고는 다음과 같습니다:

# - **서울**: 장미 100개, 튤립 150개
# - **대전**: 백합 80개, 카네이션 120개
# - **광주**: 해바라기 200개, 몬스테라 90개
