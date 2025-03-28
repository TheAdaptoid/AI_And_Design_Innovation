from os import getenv
from datetime import datetime
import json

from openai import AsyncOpenAI
from openai.types.responses.response import Response
from openai.helpers import LocalAudioPlayer
from dotenv import load_dotenv

from backend.types import Message
from backend.tools import locate_book, place_on_hold, renew_book


def get_client() -> AsyncOpenAI:
    """
    Return an instance of the OpenAI client.
    This function loads the `.env` file to get the
    API key from the `OPENAI_API_KEY` environment variable.

    Returns:
        AsyncOpenAI: An instance of the OpenAI client.
    """
    load_dotenv()
    return AsyncOpenAI(
        api_key=getenv("OPENAI_API_KEY"),
    )


def load_prompt() -> str:
    """
    Return the contents of the prompt.txt file.
    The prompt.txt file is expected to be in the same directory as this module
    and contain the prompt to be given to the AI model.

    Returns:
        str: The contents of the prompt.txt file.
    """
    with open(file="backend/orchestrator/prompt.txt", mode="r", encoding="utf-8") as f:
        return f.read()


def load_tools() -> list[dict]:
    """
    Load and return the tool configurations from a JSON file.
    The JSON file should be located at 'backend/orchestrator/tools.json' and
    contains a list of tool configurations, each represented as a dictionary.

    Returns:
        list[dict]: A list of dictionaries, where each dictionary represents
        a tool configuration.
    """
    with open(file="backend/orchestrator/tools.json", mode="r", encoding="utf-8") as f:
        return json.loads(f.read())


def serialize_messages(messages: list[Message]) -> list[dict]:
    """
    Serialize a list of Message objects into a list of dictionaries.

    Args:
        messages (list[Message]): A list of Message objects to be serialized.

    Returns:
        list[dict]: A list of dictionaries, each containing the 'role' and
            'content' of a Message object.
    """

    return [{"role": message.role, "content": message.content} for message in messages]


class Agent:
    """
    Orchestrates the interaction between the agent and the OpenAI API.
    """

    client: AsyncOpenAI
    prompt: str
    tools: list[dict]
    model_name: str = "gpt-4o-mini"

    def __init__(self):
        self.client = get_client()
        self.prompt = load_prompt()
        self.tools = load_tools()

    async def chat(self, messages: list[Message]) -> Message:
        """
        Engage in a chat session with the agent.

        Args:
            messages (list[Message]): A list of Message objects to send to the agent.

        Returns:
            Message: The final response from the agent.
        """
        # Serialize messages
        serialized_messages = serialize_messages(messages)

        # Set state
        is_finished: bool = False

        # Loop until finished
        while not is_finished:
            response = await self.handle_chat(serialized_messages)

            if response.output[0].type == "function_call":
                function_response = await self.handle_function_call(response)
                serialized_messages.extend(function_response)
            else:
                is_finished = True

        await self.handle_speach(response.output_text)

        return Message(
            content=response.output_text,
            role="assistant",
            timestamp=datetime.now(),
        )

    async def handle_speach(self, text: str) -> None:
        async with self.client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice="onyx",
            input=text,
            instructions="Speak in a calming professional tone.",
            response_format="pcm",
        ) as response:
            await LocalAudioPlayer().play(response)

    async def handle_chat(self, messages: list[dict[str, str]]) -> Response:
        """
        Handle a chat session with the agent.

        Args:
            messages (list[dict[str, str]]): A list of dictionaries, each containing
                the 'role' and 'content' of a message to send to the agent.

        Returns:
            Response: The response from the agent.
        """
        # tools: list[dict] = self.tools
        tools = [{
            "type": "file_search",
            "vector_store_ids": [getenv("VECTOR_STORE_ID")],
        }]

        return await self.client.responses.create(
            model=self.model_name,
            instructions=self.prompt,
            tools=tools,
            input=messages,
        )

    async def handle_function_call(self, response: Response) -> list[dict[str, str]]:
        """
        Handle a function call response from the agent.

        Args:
            response (Response): The response from the agent, which contains
                the function call to be executed.

        Returns:
            list[dict[str, str]]: A list of dictionaries, each representing a
                function call or function call output. The first dictionary
                represents the function call, and the second dictionary
                represents the output of the function call.
        """
        function_call: dict[str, str] = response.output[0]

        # Parse arguments into a keyword dict
        args: dict[str, str] = json.loads(function_call.arguments)
        function_name: str = function_call.name

        # Execute function
        result: str = ""
        match function_name:
            case "locate_book":
                result = json.dumps(locate_book(args["book_title"]))
            case "place_on_hold":
                result = json.dumps(place_on_hold(args["book_title"]))
            case "renew_book":
                result = json.dumps(renew_book(args["book_title"]))
            case _:
                result = "Function not found"

        return [
            {
                "type": "function_call",
                "id": function_call.id,
                "call_id": function_call.call_id,
                "name": function_call.name,
                "arguments": function_call.arguments,
            },
            {
                "type": "function_call_output",
                "call_id": function_call.call_id,
                "output": result,
            },
        ]
