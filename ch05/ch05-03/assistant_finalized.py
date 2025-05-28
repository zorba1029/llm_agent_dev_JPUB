# 시스템 변수 적재
from dotenv import load_dotenv

load_dotenv()

# OpenAI 인스턴스 생성
from openai import OpenAI

client = OpenAI()

# 1] 이전에 생성한 assistant 획득
assistant_id = 'asst_v1aqnERZOSjnAe7MemXcUzxv' 
assistant = client.beta.assistants.retrieve(assistant_id)
print(f"[1] assistant 정보:\n{assistant}\n")

# 2] 새로운 대화 흐름 생성
thread = client.beta.threads.create()

print(f"[2] thread (대화 흐름) 정보:\n{thread}\n")

# 3] 대화 흐름에 사용자 메시지 추가
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="안녕하세요, 슬픈 예나를 위로해 주세요!"  # 변경 부분
)

print(f"[3] 메시지 정보:\n{message}\n")

# 4] 실행 세션을 생성하여 대화 흐름 처리
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant_id
)

print(f"[4] 실행 세션 초기 정보:\n{run}\n")

import time

# 실행 세션 상태 확인 함수
def poll_run_status(client, thread_id, run_id, interval=5):
    n = 0

    while True:
        n += 1

        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)

        print(f"    <{n}> 번째 실행 세션 정보:\n{run}\n")

        if run.status in ['requires_action', 'completed']:
            return run

        time.sleep(interval)  # 일정 시간 대기 후 다시 상태 확인

# 5] 실행 세션 상태 확인
run = poll_run_status(client, thread.id, run.id)
print(f"[5] 실행 세션 상태 확인:\n{run}\n")

# 실행 세션에서 함수 속성 정보를 획득하는 함수
def get_function_details(run):
    function_name = run.required_action.submit_tool_outputs.tool_calls[0].function.name
    arguments = run.required_action.submit_tool_outputs.tool_calls[0].function.arguments
    function_id = run.required_action.submit_tool_outputs.tool_calls[0].id
    return function_name, arguments, function_id

# 6] 함수 속성 정보 가져오가
function_name, arguments, function_id = get_function_details(run)

print(f"[6] 함수 속성 정보 확인:")
print(f"[6] function_name: {function_name}")
print(f"[6] arguments: {arguments}")
print(f"[6] function_id: {function_id}")

# 응원 메시지 함수
def get_encouragement(mood, name=None):
    # 응원 메시지
    messages = {
        "행복": "당신이 이렇게 밝게 웃고 있는 걸 보니 기분이 좋아요! 긍정적인 마음을 계속 유지하세요!",
        "슬픔": "기억하세요. 가장 어두운 구름 뒤에도 항상 햇살이 당신을 기다리고 있어요.",
        "피곤함": "당신은 이미 충분히 잘했어요. 이제 잠시 쉬어 갈 시간이예요.",
        "스트레스": "깊게 숨을 들이마시고, 천천히 내쉬세요. 모든 것이 잘 될 거예요."
    }

    # 기분에 맞는 응원 메시지 가져오기
    if name:
        message = f"{name}님, {messages.get(mood, '오늘 기분이 어떠신가요? 저는 항상 당신을 응원하고 있어요!')}"
    else:
        message = messages.get(mood, "오늘 기분이 어떠신가요? 저는 항상 당신을 응원하고 있어요!")

    # 맞춤형 응원 메시지 반환
    return message

# JSON 문자열을 사전으로 변환
import json

arguments_dict = json.loads(arguments)

# 사전에서 'name'과 'mood' 추출
name = arguments_dict['name']
mood = arguments_dict['mood']

# 7] 함수 호출
encouragement_message = get_encouragement(mood, name)

# 결과 출력
print(f"\n[7] 함수 호출 결과: {encouragement_message}")

# 8] 동적 함수 호출을 위한 사전 정의
available_functions = {
    "get_encouragement": get_encouragement
}
print(f"\n[8] 동적 함수 호출을 위한 사전 정의: {available_functions}")

# 매개 변수 처리
import json

function_args = json.loads(arguments)

# 9] 동적 함수 호출
function_to_call = available_functions[function_name]
encouragement_message = function_to_call(
    name=function_args.get("name"),
    mood=function_args.get("mood")
)

# 결과 출력
print(f"\n[9] 동적 함수 호출 결과: {encouragement_message}")

# 결과 제출 함수
def submit_tool_outputs(run, thread, function_id, function_response):
    run = client.beta.threads.runs.submit_tool_outputs(
        thread_id=thread.id,
        run_id=run.id,
        tool_outputs=[
            {
                "tool_call_id": function_id,
                "output": str(function_response),
            }
        ]
    )

    return run

# 10] 실행 세션에 결과 제출
run = submit_tool_outputs(run, thread, function_id, encouragement_message)

print(f"\n[10] 실행 세션이 결과를 받았습니다.")
print(f"[10] 실행 세션 정보:\n{run}\n")

# 11] 실행 세션 상태를 확인하여 완료될 때까지 대기
run = poll_run_status(client, thread.id, run.id)

print(f"\n[11] 실행 세션이 완료될 때까지 계속 실행됩니다.")
print(f"[11] 실행 세션 정보:\n{run}\n")

# 12] 대화 흐름에서 도우미의 응답 가져오기
messages = client.beta.threads.messages.list(thread_id=thread.id)
print(f"\n[12] 대화 흐름에서 도우미의 응답 가져오기:")

# 13] 도우미의 응답 출력
print(f"\n[13] 최종 메시지 출력:--------------------------------")
for message in messages.data:
    if message.role == "assistant":
        print(f"[13] 최종 반환 정보:-------------\n{message.content}\n")


#-----------------------------------------
# > python3 assistant_finalized.py
# [1] assistant 정보:
# Assistant(id='asst_v1aqnERZOSjnAe7MemXcUzxv', created_at=1747933470, description=None, instructions='You are a very encouraging assistant!', metadata={}, model='gpt-4o-mini', name=None, object='assistant', tools=[FunctionTool(function=FunctionDefinition(name='get_encouragement', description='사용자의 기분에 따라 응원 메시지를 제공합니다.', parameters={'type': 'object', 'properties': {'mood': {'type': 'string', 'description': '사용자의 현재 기분, 예: 행복, 슬픔, 스트레스, 피곤함'}, 'name': {'type': 'string', 'description': '응원 메시지를 맞춤화하기 위한 사용자의 이름'}}, 'required': ['mood']}, strict=False), type='function')], response_format='auto', temperature=1.0, tool_resources=ToolResources(code_interpreter=None, file_search=None), top_p=1.0, reasoning_effort=None)

# [2] thread (대화 흐름) 정보:
# Thread(id='thread_1unghIy5gjIPkIe02RnPQOn1', created_at=1748340249, metadata={}, object='thread', tool_resources=ToolResources(code_interpreter=None, file_search=None))

# [3] 메시지 정보:
# Message(id='msg_WBc9Ozzcvcak3PtbSOjx1eIz', assistant_id=None, attachments=[], completed_at=None, content=[TextContentBlock(text=Text(annotations=[], value='안녕하세요, 슬픈 예나를 위로해 주세요!'), type='text')], created_at=1748340250, incomplete_at=None, incomplete_details=None, metadata={}, object='thread.message', role='user', run_id=None, status=None, thread_id='thread_1unghIy5gjIPkIe02RnPQOn1')

# [4] 실행 세션 초기 정보:
# Run(id='run_i71jSWKCh8jNpkw0eBBxGoIl', assistant_id='asst_v1aqnERZOSjnAe7MemXcUzxv', cancelled_at=None, completed_at=None, created_at=1748340251, expires_at=1748340851, failed_at=None, incomplete_details=None, instructions='You are a very encouraging assistant!', last_error=None, max_completion_tokens=None, max_prompt_tokens=None, metadata={}, model='gpt-4o-mini', object='thread.run', parallel_tool_calls=True, required_action=None, response_format='auto', started_at=None, status='queued', thread_id='thread_1unghIy5gjIPkIe02RnPQOn1', tool_choice='auto', tools=[FunctionTool(function=FunctionDefinition(name='get_encouragement', description='사용자의 기분에 따라 응원 메시지를 제공합니다.', parameters={'type': 'object', 'properties': {'mood': {'type': 'string', 'description': '사용자의 현재 기분, 예: 행복, 슬픔, 스트레스, 피곤함'}, 'name': {'type': 'string', 'description': '응원 메시지를 맞춤화하기 위한 사용자의 이름'}}, 'required': ['mood']}, strict=False), type='function')], truncation_strategy=TruncationStrategy(type='auto', last_messages=None), usage=None, temperature=1.0, top_p=1.0, tool_resources={}, reasoning_effort=None)

#     <1> 번째 실행 세션 정보:
# Run(id='run_i71jSWKCh8jNpkw0eBBxGoIl', assistant_id='asst_v1aqnERZOSjnAe7MemXcUzxv', cancelled_at=None, completed_at=None, created_at=1748340251, expires_at=1748340851, failed_at=None, incomplete_details=None, instructions='You are a very encouraging assistant!', last_error=None, max_completion_tokens=None, max_prompt_tokens=None, metadata={}, model='gpt-4o-mini', object='thread.run', parallel_tool_calls=True, required_action=None, response_format='auto', started_at=None, status='queued', thread_id='thread_1unghIy5gjIPkIe02RnPQOn1', tool_choice='auto', tools=[FunctionTool(function=FunctionDefinition(name='get_encouragement', description='사용자의 기분에 따라 응원 메시지를 제공합니다.', parameters={'type': 'object', 'properties': {'mood': {'type': 'string', 'description': '사용자의 현재 기분, 예: 행복, 슬픔, 스트레스, 피곤함'}, 'name': {'type': 'string', 'description': '응원 메시지를 맞춤화하기 위한 사용자의 이름'}}, 'required': ['mood']}, strict=False), type='function')], truncation_strategy=TruncationStrategy(type='auto', last_messages=None), usage=None, temperature=1.0, top_p=1.0, tool_resources={}, reasoning_effort=None)

#     <2> 번째 실행 세션 정보:
# Run(id='run_i71jSWKCh8jNpkw0eBBxGoIl', assistant_id='asst_v1aqnERZOSjnAe7MemXcUzxv', cancelled_at=None, completed_at=None, created_at=1748340251, expires_at=1748340851, failed_at=None, incomplete_details=None, instructions='You are a very encouraging assistant!', last_error=None, max_completion_tokens=None, max_prompt_tokens=None, metadata={}, model='gpt-4o-mini', object='thread.run', parallel_tool_calls=True, required_action=RequiredAction(submit_tool_outputs=RequiredActionSubmitToolOutputs(tool_calls=[RequiredActionFunctionToolCall(id='call_pGgJT6m8ZqGzxfZMXlrDw8aB', function=Function(arguments='{"mood":"슬픔","name":"예나"}', name='get_encouragement'), type='function')]), type='submit_tool_outputs'), response_format='auto', started_at=1748340252, status='requires_action', thread_id='thread_1unghIy5gjIPkIe02RnPQOn1', tool_choice='auto', tools=[FunctionTool(function=FunctionDefinition(name='get_encouragement', description='사용자의 기분에 따라 응원 메시지를 제공합니다.', parameters={'type': 'object', 'properties': {'mood': {'type': 'string', 'description': '사용자의 현재 기분, 예: 행복, 슬픔, 스트레스, 피곤함'}, 'name': {'type': 'string', 'description': '응원 메시지를 맞춤화하기 위한 사용자의 이름'}}, 'required': ['mood']}, strict=False), type='function')], truncation_strategy=TruncationStrategy(type='auto', last_messages=None), usage=None, temperature=1.0, top_p=1.0, tool_resources={}, reasoning_effort=None)

# [5] 실행 세션 상태 확인:
# Run(id='run_i71jSWKCh8jNpkw0eBBxGoIl', assistant_id='asst_v1aqnERZOSjnAe7MemXcUzxv', cancelled_at=None, completed_at=None, created_at=1748340251, expires_at=1748340851, failed_at=None, incomplete_details=None, instructions='You are a very encouraging assistant!', last_error=None, max_completion_tokens=None, max_prompt_tokens=None, metadata={}, model='gpt-4o-mini', object='thread.run', parallel_tool_calls=True, required_action=RequiredAction(submit_tool_outputs=RequiredActionSubmitToolOutputs(tool_calls=[RequiredActionFunctionToolCall(id='call_pGgJT6m8ZqGzxfZMXlrDw8aB', function=Function(arguments='{"mood":"슬픔","name":"예나"}', name='get_encouragement'), type='function')]), type='submit_tool_outputs'), response_format='auto', started_at=1748340252, status='requires_action', thread_id='thread_1unghIy5gjIPkIe02RnPQOn1', tool_choice='auto', tools=[FunctionTool(function=FunctionDefinition(name='get_encouragement', description='사용자의 기분에 따라 응원 메시지를 제공합니다.', parameters={'type': 'object', 'properties': {'mood': {'type': 'string', 'description': '사용자의 현재 기분, 예: 행복, 슬픔, 스트레스, 피곤함'}, 'name': {'type': 'string', 'description': '응원 메시지를 맞춤화하기 위한 사용자의 이름'}}, 'required': ['mood']}, strict=False), type='function')], truncation_strategy=TruncationStrategy(type='auto', last_messages=None), usage=None, temperature=1.0, top_p=1.0, tool_resources={}, reasoning_effort=None)

# [6] 함수 속성 정보 확인:
# [6] function_name: get_encouragement
# [6] arguments: {"mood":"슬픔","name":"예나"}
# [6] function_id: call_pGgJT6m8ZqGzxfZMXlrDw8aB

# [7] 함수 호출 결과: 예나님, 기억하세요. 가장 어두운 구름 뒤에도 항상 햇살이 당신을 기다리고 있어요.

# [8] 동적 함수 호출을 위한 사전 정의: {'get_encouragement': <function get_encouragement at 0x107948fe0>}

# [9] 동적 함수 호출 결과: 예나님, 기억하세요. 가장 어두운 구름 뒤에도 항상 햇살이 당신을 기다리고 있어요.

# [10] 실행 세션이 결과를 받았습니다.
# [10] 실행 세션 정보:
# Run(id='run_i71jSWKCh8jNpkw0eBBxGoIl', assistant_id='asst_v1aqnERZOSjnAe7MemXcUzxv', cancelled_at=None, completed_at=None, created_at=1748340251, expires_at=1748340851, failed_at=None, incomplete_details=None, instructions='You are a very encouraging assistant!', last_error=None, max_completion_tokens=None, max_prompt_tokens=None, metadata={}, model='gpt-4o-mini', object='thread.run', parallel_tool_calls=True, required_action=None, response_format='auto', started_at=1748340252, status='queued', thread_id='thread_1unghIy5gjIPkIe02RnPQOn1', tool_choice='auto', tools=[FunctionTool(function=FunctionDefinition(name='get_encouragement', description='사용자의 기분에 따라 응원 메시지를 제공합니다.', parameters={'type': 'object', 'properties': {'mood': {'type': 'string', 'description': '사용자의 현재 기분, 예: 행복, 슬픔, 스트레스, 피곤함'}, 'name': {'type': 'string', 'description': '응원 메시지를 맞춤화하기 위한 사용자의 이름'}}, 'required': ['mood']}, strict=False), type='function')], truncation_strategy=TruncationStrategy(type='auto', last_messages=None), usage=None, temperature=1.0, top_p=1.0, tool_resources={}, reasoning_effort=None)

#     <1> 번째 실행 세션 정보:
# Run(id='run_i71jSWKCh8jNpkw0eBBxGoIl', assistant_id='asst_v1aqnERZOSjnAe7MemXcUzxv', cancelled_at=None, completed_at=None, created_at=1748340251, expires_at=1748340851, failed_at=None, incomplete_details=None, instructions='You are a very encouraging assistant!', last_error=None, max_completion_tokens=None, max_prompt_tokens=None, metadata={}, model='gpt-4o-mini', object='thread.run', parallel_tool_calls=True, required_action=None, response_format='auto', started_at=1748340252, status='queued', thread_id='thread_1unghIy5gjIPkIe02RnPQOn1', tool_choice='auto', tools=[FunctionTool(function=FunctionDefinition(name='get_encouragement', description='사용자의 기분에 따라 응원 메시지를 제공합니다.', parameters={'type': 'object', 'properties': {'mood': {'type': 'string', 'description': '사용자의 현재 기분, 예: 행복, 슬픔, 스트레스, 피곤함'}, 'name': {'type': 'string', 'description': '응원 메시지를 맞춤화하기 위한 사용자의 이름'}}, 'required': ['mood']}, strict=False), type='function')], truncation_strategy=TruncationStrategy(type='auto', last_messages=None), usage=None, temperature=1.0, top_p=1.0, tool_resources={}, reasoning_effort=None)

#     <2> 번째 실행 세션 정보:
# Run(id='run_i71jSWKCh8jNpkw0eBBxGoIl', assistant_id='asst_v1aqnERZOSjnAe7MemXcUzxv', cancelled_at=None, completed_at=1748340261, created_at=1748340251, expires_at=None, failed_at=None, incomplete_details=None, instructions='You are a very encouraging assistant!', last_error=None, max_completion_tokens=None, max_prompt_tokens=None, metadata={}, model='gpt-4o-mini', object='thread.run', parallel_tool_calls=True, required_action=None, response_format='auto', started_at=1748340259, status='completed', thread_id='thread_1unghIy5gjIPkIe02RnPQOn1', tool_choice='auto', tools=[FunctionTool(function=FunctionDefinition(name='get_encouragement', description='사용자의 기분에 따라 응원 메시지를 제공합니다.', parameters={'type': 'object', 'properties': {'mood': {'type': 'string', 'description': '사용자의 현재 기분, 예: 행복, 슬픔, 스트레스, 피곤함'}, 'name': {'type': 'string', 'description': '응원 메시지를 맞춤화하기 위한 사용자의 이름'}}, 'required': ['mood']}, strict=False), type='function')], truncation_strategy=TruncationStrategy(type='auto', last_messages=None), usage=Usage(completion_tokens=69, prompt_tokens=712, total_tokens=781, prompt_token_details={'cached_tokens': 0}, completion_tokens_details={'reasoning_tokens': 0}), temperature=1.0, top_p=1.0, tool_resources={}, reasoning_effort=None)


# [11] 실행 세션이 완료될 때까지 계속 실행됩니다.
# [11] 실행 세션 정보:
# Run(id='run_i71jSWKCh8jNpkw0eBBxGoIl', assistant_id='asst_v1aqnERZOSjnAe7MemXcUzxv', cancelled_at=None, completed_at=1748340261, created_at=1748340251, expires_at=None, failed_at=None, incomplete_details=None, instructions='You are a very encouraging assistant!', last_error=None, max_completion_tokens=None, max_prompt_tokens=None, metadata={}, model='gpt-4o-mini', object='thread.run', parallel_tool_calls=True, required_action=None, response_format='auto', started_at=1748340259, status='completed', thread_id='thread_1unghIy5gjIPkIe02RnPQOn1', tool_choice='auto', tools=[FunctionTool(function=FunctionDefinition(name='get_encouragement', description='사용자의 기분에 따라 응원 메시지를 제공합니다.', parameters={'type': 'object', 'properties': {'mood': {'type': 'string', 'description': '사용자의 현재 기분, 예: 행복, 슬픔, 스트레스, 피곤함'}, 'name': {'type': 'string', 'description': '응원 메시지를 맞춤화하기 위한 사용자의 이름'}}, 'required': ['mood']}, strict=False), type='function')], truncation_strategy=TruncationStrategy(type='auto', last_messages=None), usage=Usage(completion_tokens=69, prompt_tokens=712, total_tokens=781, prompt_token_details={'cached_tokens': 0}, completion_tokens_details={'reasoning_tokens': 0}), temperature=1.0, top_p=1.0, tool_resources={}, reasoning_effort=None)


# [12] 대화 흐름에서 도우미의 응답 가져오기:

# [13] 최종 메시지 출력:--------------------------------
# [13] 최종 반환 정보:-------------
# [TextContentBlock(text=Text(annotations=[], value='예나님, 기억하세요. 가장 어두운 구름 뒤에도 항상 햇살이 당신을 기다리고 있어요. 힘내세요! 어려운 순간들도 지나갈 거예요. 😊'), type='text')]
