import dotenv
import os
from openai import OpenAI

dotenv.load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()

tools = [{
    "type": "function",
    "name": "save_book",
    "description": "Save a book to the users favorites.",
    "parameters": {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "The title of the book to save. e.g. 'The Great Gatsby'",
            },
            "author": {
                "type": "string",
                "description": "The author of the book to save. e.g. 'F. Scott Fitzgerald'",
            },
            "publisher": {
                "type": "string",
                "description": "The publisher of the book to save. e.g. 'Charles Scribner's Sons'",
            },
            "year": {
                "type": "integer",
                "description": "The year the book was published. e.g. 1925",
                "minimum": 868,
                "maximum": 2100,
            },
            "description": {
                "type": "string",
                "description": "A short description of the book. e.g. 'A novel about the American dream.'",
            },
        },
        "required": [
            "title", 
            "author"
        ],
        "additionalProperties": False
    }
}]

response = client.responses.create(
    model="gpt-4o",
    input=[{"role": "user", "content": "Save a book to my favorites."}],
    tools=tools,
)

print(response.output)


