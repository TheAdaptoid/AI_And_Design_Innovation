from openai import OpenAI
import dotenv
import os

dotenv.load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()

#vector_store = client.vector_stores.create(name="Library",) # Create Library vector store

vector_store_id = os.getenv("ECTOR_STORE_ID")

pdf_folder = r"C:\Users\aryan\.vscode\AI_And_Design_Innovation\backend\vector_database\pdf_files"

for file_name in os.listdir(pdf_folder):
    full_path = os.path.join(pdf_folder, file_name)
    print(f"Processing: {full_path}")