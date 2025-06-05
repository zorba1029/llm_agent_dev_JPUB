# filename: check_flower_inventory.py
import pandas as pd

# CSV 파일을 읽어옵니다.
df = pd.read_csv('flower_inventory.csv')

# 각 꽃의 재고 수량을 출력합니다.
print("현재 재고:")
print(df)

# 재고가 부족한 꽃을 체크합니다.
low_stock = df[df['quantity'] <= 2]

# 재고 부족 꽃 출력
if not low_stock.empty:
    print("\n재고가 부족한 꽃:")
    print(low_stock)
else:
    print("\n재고가 부족한 꽃이 없습니다.")