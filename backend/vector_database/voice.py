import asyncio
import os
import dotenv

from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer

dotenv.load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

openai = AsyncOpenAI()

async def main() -> None:
    # Get user prompt
    user_prompt = input("You: ")

    # Generate AI response
    completion = await openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a cheerful and positive assistant."},
            {"role": "user", "content": user_prompt},
        ],
    )

    ai_response = completion.choices[0].message.content
    print(f"Assistant: {ai_response}")

    # Speak the AI response
    async with openai.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="onyx",
        input=ai_response,
        instructions="Speak in a calming professional tone.",
        response_format="pcm",
    ) as response:
        await LocalAudioPlayer().play(response)

if __name__ == "__main__":
    asyncio.run(main())
