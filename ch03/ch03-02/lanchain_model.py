import os
from dotenv import load_dotenv

from langchain_openai import OpenAI

from langchain_anthropic import ChatAnthropic

load_dotenv()

# openai_model = OpenAI(temperature=0.1, model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))
openai_model = OpenAI(temperature=0.1, api_key=os.getenv("OPENAI_API_KEY"))

anthropic_model = ChatAnthropic(
    temperature=0.1, 
    model="claude-3-5-sonnet-20240620", 
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

from langchain.model_laboratory import ModelLaboratory

model_lab = ModelLaboratory.from_llms([openai_model, anthropic_model])

model_lab.compare("백합은 어느 나라에서 유래 되었나요?")

# -- 출력 결과 1 ----
# > python3 lanchain_model.py
# Input:
# 백합은 어느 나라에서 유래 되었나요?

# OpenAI
# Lily originated in Europe, featured in Greek mythology as Aphrodite's flower,
# and became sacred in medieval Christianity.

# Params: {'model_name': 'gpt-3.5-turbo-instruct', 'temperature': 0.1, 'top_p': 1, 'frequency_penalty': 0, 'presence_penalty': 0, 'n': 1, 'seed': None, 'logprobs': None, 'max_tokens': 256}

# 백합은 유럽 지역에서 유래되었습니다. 특히 그리스 신화에서 아프로디테의 꽃으로 언급되어
# 유명해졌습니다. 그리고 중세 유럽에서는 기독교의 신성한 꽃으로 여겨졌습니다. 현재는
# 전 세계적으로 재배되고 있으며, 일본에서는 꽃말로서의 의미가 강조되어 사랑과 순결을
# 상징하는 꽃으로 인기가 있습니다.

# model='claude-3-5-sonnet-20240620' temperature=0.1
# anthropic_api_url='https://api.anthropic.com'
# anthropic_api_key=SecretStr('**********') model_kwargs={}
# 백합의 정확한 기원을 단일 국가로 특정하기는 어렵습니다. 백합은 전 세계 여러 지역에서
# 자생하며 오랜 역사를 가진 꽃입니다. 하지만 백합의 역사와 문화적 중요성에 대해
# 몇 가지 중요한 점을 말씀드릴 수 있습니다:

# 1. 자생지: 백합은 주로 북반구의 온대 지역에서 자생합니다. 특히 아시아, 유럽, 북미에 널리 분포되어 있습니다.
# 2. 고대 문명: 백합은 고대 이집트, 그리스, 로마 문명에서 이미 중요한 꽃으로 여겨졌습니다.
# 3. 아시아의 중요성: 중국, 일본, 한국 등 동아시아 국가들에서 백합은 오랫동안 중요한 문화적, 예술적 소재로 사용되었습니다.
# 4. 품종 개발: 현대의 다양한 백합 품종들은 주로 19세기 이후 유럽과 북미에서 개발되었습니다.
# 5. 상징성: 기독교 문화권에서 백합은 순결과 순수의 상징으로 여겨집니다.

# 따라서 백합은 특정 한 나라에서 유래했다기보다는, 여러 문화와 지역에서 오랜 시간에
# 걸쳐 중요하게 여겨져 온 꽃이라고 할 수 있습니다.

# Claude-3.5-Sonnet
# Lilies have diverse origins across Northern Hemisphere. Important in ancient
# Egypt, Greece, Rome, and East Asia. Symbolizes purity in Christianity.