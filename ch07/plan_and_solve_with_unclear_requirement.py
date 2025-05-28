# API 키 설정
from dotenv import load_dotenv

load_dotenv()

from langchain.tools import tool

# 재고 조회 함수
@tool
def check_inventory(flower_type: str) -> int:
    """
    특정 종류의 꽃의 재고 수량을 조회합니다.

    매개 변수:
    - flower_type: 꽃의 종류

    반환 값:
    - 재고 수량 (현재는 고정된 숫자를 반환)
    """
    # 실제 환경에서는 실제 재고 확인 처리 필요
    return 100

# 가격 계산 함수
@tool
def calculate_price(base_price: float, markup: float) -> float:
    """
    기본 가격과 마진 비율을 기반으로 최종 가격을 계산합니다.

    매개 변수:
    - base_price: 기본 가격
    - markup: 마진 비율

    반환 값:
    - 최종 가격
    """
    return base_price * (1 + markup)

# 배송 일정 설정 함수
@tool
def schedule_delivery(order_id: int, delivery_date: str) -> str:
    """
    주문의 배송을 일정에 맞춰 설정합니다.

    매개 변수:
    - order_id: 주문 번호
    - delivery_date: 배송 날짜

    반환 값:
    - 배송 상태 또는 확인 정보
    """
    # 실제 환경에서는 배송 시스템과의 연동 과정 필요
    return f"주문 {order_id}의 {delivery_date}에 배송 예정입니다."

#--------------------------------
# 사용 가능한 도구 목록
tools = [check_inventory, calculate_price]

# 언어모델 설정
from langchain_openai import ChatOpenAI

model = ChatOpenAI(temperature=0)

# 계획자와 실행자 설정 planner, executor
from langchain_experimental.plan_and_execute import (
    load_chat_planner,
    load_agent_executor,
    PlanAndExecute,
)

planner = load_chat_planner(llm=model)
executor = load_agent_executor(llm=model, tools=tools, verbose=True)

# 계획과 실행 agent 초기화
agent = PlanAndExecute(planner=planner, executor=executor)

result = agent.run("장미 재고를 확인한 후 출하 계획을 제시 해 주세요")

print(result)