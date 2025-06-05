# filename: flower_inventory_check.py

# 현재 재고에 있는 꽃의 종류와 수량
inventory = {
    "장미": 15,
    "백합": 2,
    "해바라기": 8,
    "국화": 0,
    "튤립": 5
}

# 부족한 재고를 체크할 임계값
threshold = 5

# 부족한 꽃을 찾기
low_stock_flowers = {flower: quantity for flower, quantity in inventory.items() if quantity < threshold}

# 결과 출력
print("부족한 꽃의 목록:")
for flower, quantity in low_stock_flowers.items():
    print(f"{flower}: {quantity}개")