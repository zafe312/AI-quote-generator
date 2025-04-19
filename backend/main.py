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

def chat_completion(content):
    completion = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-V3-0324",
        messages=[
            {
                "role": "user",
                "content": content
            }
        ],
        max_tokens=512,
    )
    return completion.choices[0].message.content

def promt_generator(format,tone,topic):
    return f"Write a {format} in a {tone} tone about {topic}. Do not answer anything else just the {format}."

if __name__=="__main__":
    format = "caption"
    tone = "enthusiastic"
    topic = "my picture"
    content = promt_generator(format,tone,topic)
    message = chat_completion(content)
    print(message)