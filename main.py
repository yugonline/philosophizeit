import os

from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

from OpenAIClient import OpenAiClient

app = FastAPI()


class Prompt(BaseModel):
    prompt_type: str
    text: str


class Response(BaseModel):
    response_text: str


class DialecticPrompt(Prompt):
    prompt_type: str = "dialectic"


class HermeneuticsPrompt(Prompt):
    prompt_type: str = "hermeneutics"


load_dotenv()  # Load environment variables from .env file
api_key = os.getenv("OPENAI_API_KEY")  # Add your OPEN AI API Key here
if not api_key:
    raise ValueError("OpenAI API key not found in environment variables")

openai_client = OpenAiClient(api_key)


def build_prompt(prompt: Prompt) -> str:
    return f"Apply {prompt.prompt_type.capitalize()} on -{prompt.text}- "


def generate_response(prompt: Prompt) -> str | Response:
    if prompt.prompt_type not in {"dialectic", "hermeneutics"}:
        return "Invalid prompt type"

    primary_prompt = build_prompt(prompt)
    generated_text = openai_client.generate_completion(primary_prompt)
    return Response(response_text=generated_text)


@app.post("/generate-response")
async def generate_response_endpoint(prompt: Prompt):
    response = generate_response(prompt)
    return response
