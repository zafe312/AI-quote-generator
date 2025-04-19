import os
import logging
from dotenv import load_dotenv
from pathlib import Path
from openai import OpenAI, OpenAIError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PromptGenerator:
    def __init__(self, format: str, tone: str, topic: str):
        self.format = format
        self.tone = tone
        self.topic = topic

    def generate(self) -> str:
        return (
            f"Write a {self.format} in a {self.tone} tone about {self.topic}. "
            f"Do not answer anything else just the {self.format}."
        )

class ChatClient:
    def __init__(self, base_url: str, api_key: str):
        self.client = OpenAI(base_url=base_url, api_key=api_key)

    def get_chat_completion(self, content: str, model: str = "deepseek-ai/DeepSeek-V3-0324", max_tokens: int = 512) -> str:
        try:
            logging.info("Sending request to chat model...")
            completion = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": content}],
                max_tokens=max_tokens,
            )
            response = completion.choices[0].message.content
            logging.info("Received response from chat model.")
            return response
        except OpenAIError as e:
            logging.error(f"OpenAI API error: {e}")
            return "Error: Unable to get a response from the chat model."
        except Exception as e:
            logging.exception("Unexpected error during chat completion.")
            return "Error: An unexpected error occurred."

class App:
    def __init__(self):
        dotenv_path = Path('../.env')
        if not dotenv_path.exists():
            logging.warning(f".env file not found at {dotenv_path}")
        load_dotenv(dotenv_path=dotenv_path)

        api_key = os.getenv('HF_API_KEY')
        if not api_key:
            raise ValueError("HF_API_KEY not found in environment variables.")
        
        self.chat_client = ChatClient(
            base_url="https://router.huggingface.co/hyperbolic/v1",
            api_key=api_key
        )

    def run(self, format: str, tone: str, topic: str):
        prompt = PromptGenerator(format, tone, topic).generate()
        logging.info(f"Generated prompt: {prompt}")
        message = self.chat_client.get_chat_completion(prompt)
        print(message)

if __name__ == "__main__":
    try:
        app = App()
        app.run(format="caption", tone="enthusiastic", topic="my picture")
    except Exception as e:
        logging.critical(f"Fatal error: {e}")