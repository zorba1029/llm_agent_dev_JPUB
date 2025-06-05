import fire 

from metagpt.actions import Action, UserRequirement
from metagpt.logs import logger
from metagpt.roles import Role
from metagpt.schema import Message
from metagpt.team import Team

# 주문처리 작업 정의
class PrpcessOrderAction(Action):
    PROMPT_TEMPLATE = """
    Process the following order: {order_details}
    """
    name: str = "ProcessOrderAction"
    
    async def run(self, order_details: str):
        prompt = self.PROMPT_TEMPLATE.format(order_details=order_details)
        rsp = await self._watch(prompt)
        return rsp.strip()
    
# 주문처리 역할 정의
class OrderProcessorRole(Role):
    name: str = "OrderProcessorRole"
    profile: str = "Process orders"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._watch([UserRequirement])
        self._set_actions([PrpcessOrderAction])

# 재고관리 작업 정의
class ManageInventoryAction(Action):
    PROMPT_TEMPLATE = """
    Update the inventory based on the following order: {order_details}
    """
    name: str = "ManageInventoryAction"
    
    async def run(self, order_details: str):
        prompt = self.PROMPT_TEMPLATE.format(order_details=order_details)
        rsp = await self._watch(prompt)
        return rsp.strip()
    
# 재고관리 역할 정의
class InventoryManagerRole(Role):
    name: str = "InventoryManagerRole"
    profile: str = "Manage inventory"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._watch([UserRequirement])
        self._set_actions([ManageInventoryAction])
        
# 고객 서비스 작업 정의
class HandleCustomerServiceAction(Action):
    PROMPT_TEMPLATE = """
    Handle the following customer service request: {request_details}
    """
    name: str = "HandleCustomerServiceAction"
    
    async def run(self, request_details: str):
        prompt = self.PROMPT_TEMPLATE.format(request_details=request_details)
        rsp = await self._watch(prompt)
        return rsp.strip()
    
# 고객 서비스 역할 정의
class CustomerServiceRepresentativeRole(Role):
    name: str = "CustomerServiceRepresentativeRole"
    profile: str = "Handle customer service"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._watch([UserRequirement])
        self._set_actions([HandleCustomerServiceAction])
        
# main 함수
async def main(
    order_details: str = "A bouquet of red roses",
    investment: float = 3.0,
    n_round: int = 5,
    add_human: bool = False,
):
    logger.info(order_details)
    
    # 팀 구성 및 역할 추가
    team = Team()
    team.hire(
        [
            OrderProcessorRole(),
            InventoryManagerRole(),
            CustomerServiceRepresentativeRole(),
        ]
    )
    
    # 투자 및 프로젝트 실행
    team.invest(investment=investment)
    team.run_project(order_details)
    
    # 지정된 라운드 동안 실행
    await team.run(n_round=n_round)

# ----------------------------------
if __name__ == "__main__":
    fire.Fire(main)

    