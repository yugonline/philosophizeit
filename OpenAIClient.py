import logging
import requests
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_data(prompt: str) -> dict:
    return {
        "prompt": prompt,
        "temperature": 0.5,
        "max_tokens": 200,
        "n": 1,
        "stop": None,
    }


class OpenAiClient:

    def __init__(self, api_key: str, max_retries: int = 1):
        self.api_key = api_key
        self.base_url = "https://api.openai.com/v1/engines/text-davinci-002/completions"
        self.max_retries = max_retries

    def create_headers(self) -> dict:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

    def generate_completion(self, prompt: str) -> str:
        headers = self.create_headers()
        data = create_data(prompt)
        retries = 0
        while retries <= self.max_retries:
            try:
                logger.info(f"Sending request to OpenAI API: {data}")
                response = requests.post(self.base_url, headers=headers, json=data)
                response_data = response.json()
                generated_text = response_data["choices"][0]["text"]
                usage = response.headers.get("openai-usage")
                if usage:
                    logger.info(f"OpenAI API usage: {usage}")
                return generated_text
            except Exception as e:
                logger.error(f"Error during API request: {e}")
                retries += 1
                if retries <= self.max_retries:
                    time.sleep(1)  # Add a delay before retrying
                else:
                    logger.error("Max retries reached, dropping the request.")
                    return "Error: Unable to generate response"
        del headers, data  # Clean up memory
