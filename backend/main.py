import os
from dotenv import load_dotenv
from pathlib import Path
from openai import OpenAI

dotenv_path = Path('../.env')
load_dotenv(dotenv_path=dotenv_path)

OPENAI_API_KEY = os.getenv('HF_API_KEY')

client = OpenAI(
    base_url="https://router.huggingface.co/hyperbolic/v1",
    api_key=OPENAI_API_KEY,
)

completion = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-V3-0324",
    messages=[
        {
            "role": "user",
            "content": "What is the capital of France?"
        }
    ],
    max_tokens=512,
)

print(completion.choices[0].message)