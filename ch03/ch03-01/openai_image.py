import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.images.generate(
    model="dall-e-3",
    prompt="'꽃말의 비밀 정원' 온라인 쇼핑몰 앱의 새해 장미 꽃 홍보 포스터, 문구는 영어로 작성해주세요.",
    size="1024x1024",
    quality="standard",
    n=1,
)

# 이미지 URL 가져오기
image_url = response.data[0].url

# 이미지 읽어오기
import requests

image = requests.get(image_url).content 

# 이미지 저장
with open("generated_image.png", "wb") as f:
    f.write(image)

# 이미지 저장 경로 출력
print(f"이미지 저장 경로: {os.path.abspath('generated_image.png')}")

# # Jupyter Notebook에서 이미지 표시
# from IPython.display import Image

# Image(image)
