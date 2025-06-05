# filename: create_flower_inventory.py
import pandas as pd

# 데이터프레임 생성
data = {
    'flower_name': ['rose', 'tulip', 'sunflower', 'lily'],
    'quantity': [10, 2, 0, 5]
}

df = pd.DataFrame(data)

# CSV 파일로 저장
df.to_csv('flower_inventory.csv', index=False)

print("flower_inventory.csv 파일이 생성되었습니다.")