from openai import OpenAI
import dotenv
import os

dotenv.load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
vector_store_id = os.getenv("ECTOR_STORE_ID")
pdf_folder = r"C:\Users\aryan\.vscode\AI_And_Design_Innovation\backend\vector_database\pdf_files"

client = OpenAI()

#vector_store = client.vector_stores.create(name="Library",) # Create Library vector store

#Load what files are in VectorDB into a set
existing_files = client.vector_stores.files.list(vector_store_id=vector_store_id)
existing_file_names = set()

for item in existing_files.data:
    file_info = client.files.retrieve(item.id)
    existing_file_names.add(file_info.filename)

#Add new files that don't exist in the set
for file_name in os.listdir(pdf_folder):
    full_path = os.path.join(pdf_folder, file_name)

    if file_name in existing_file_names:
        continue

    print(f"Uploading: {file_name}")

    with open(full_path, "rb") as f:
        file = client.files.create(file=f, purpose="assistants")

    client.vector_stores.files.create(vector_store_id=vector_store_id, file_id=file.id)