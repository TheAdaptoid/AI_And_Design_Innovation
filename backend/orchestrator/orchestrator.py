from os import getenv
from datetime import datetime
from json import loads

from openai import AsyncOpenAI
from dotenv import load_dotenv

from backend.orchestrator.types import Message


def get_client() -> AsyncOpenAI:
    load_dotenv()
    return AsyncOpenAI(
        api_key=getenv("OPENAI_API_KEY"),
    )


def load_prompt() -> str:
    with open(file="backend/orchestrator/prompt.txt", mode="r", encoding="utf-8") as f:
        return f.read()


def load_tools() -> list[dict]:
    with open(file="backend/orchestrator/tools.json", mode="r", encoding="utf-8") as f:
        return loads(f.read())


def serialize_messages(messages: list[Message]) -> list[dict]:
    return [
        {
            "role": message.role,
            "content": message.content,
        }
        for message in messages
    ]


class Agent:
    client: AsyncOpenAI
    prompt: str
    tools: list[dict]
    model_name: str = "gpt-4o-mini"

    def __init__(self):
        self.client = get_client()
        self.prompt = load_prompt()
        self.tools = load_tools()

    async def chat(self, messages: list[Message]) -> Message:
        serialized_messages = serialize_messages(messages)

        response = await self.client.responses.create(
            model=self.model_name,
            instructions=self.prompt,
            input=serialized_messages,
            tools=self.tools,
        )

        return Message(
            content=response.output_text,
            role="assistant",
            timestamp=datetime.now(),
        )
