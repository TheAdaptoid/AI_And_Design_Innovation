from openai import OpenAI
import dotenv
import os

dotenv.load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
vector_store_id = os.getenv("VECTOR_STORE_ID")
pdf_folder = r"C:\Users\aryan\OneDrive\Documents\AI_AND_DESIGN_INNOVATION"

client = OpenAI()

#vector_store = client.vector_stores.create(name="Library",) # Create Library vector store

#Load what files are in VectorDB into a set
existing_files = client.vector_stores.files.list(vector_store_id=vector_store_id)
print(existing_files)

def upload_new_pdfs_to_vector_store(client, vector_store_id, pdf_folder):
    """
    Uploads new PDF files from a folder to a given vector store. Skips files that already exist.

    Args:
        client: An instance of OpenAI client.
        vector_store_id (str): The ID of the target vector store.
        pdf_folder (str): Path to the folder containing PDF files.
    """
    print(f"\n📂 Scanning folder: {pdf_folder}")

    # Step 1: Load existing files in the vector store
    existing_files = client.vector_stores.files.list(vector_store_id=vector_store_id)
    existing_file_names = set()

    for item in existing_files.data:
        file_info = client.files.retrieve(item.id)
        existing_file_names.add(file_info.filename)

    print(f"📄 {len(existing_file_names)} files already in vector store.")

    # Step 2: Upload new PDF files
    for file_name in os.listdir(pdf_folder):
        full_path = os.path.join(pdf_folder, file_name)

        if not os.path.isfile(full_path) or not file_name.lower().endswith(".pdf"):
            continue  # skip folders and non-PDFs

        if file_name in existing_file_names:
            print(f"⏩ Skipping already uploaded: {file_name}")
            continue

        try:
            print(f"⬆️ Uploading: {file_name}")
            with open(full_path, "rb") as f:
                file = client.files.create(file=f, purpose="assistants")

            client.vector_stores.files.create(
                vector_store_id=vector_store_id,
                file_id=file.id
            )
            print(f"✅ Uploaded and added: {file_name}")
        except Exception as e:
            print(f"❌ Failed to upload {file_name}: {e}")

def wipe_vector_store(client, vector_store_id, delete_files_from_storage=False):
    """
    Remove all files from a given vector store. Optionally delete the files from OpenAI's file storage.

    Args:
        client: An instance of OpenAI client.
        vector_store_id (str): The ID of the vector store to wipe.
        delete_files_from_storage (bool): If True, also deletes files from OpenAI's file storage.
    """
    print(f"\n🧹 Wiping vector store: {vector_store_id}")

    # Step 1: List all files in the vector store
    vector_store_files = client.vector_stores.files.list(vector_store_id=vector_store_id)

    if not vector_store_files.data:
        print("Vector store is already empty.")
        return

    # Step 2: Remove each file from the vector store
    for item in vector_store_files.data:
        try:
            print(f"Removing from vector store: {item.id}")
            client.vector_stores.files.delete(vector_store_id=vector_store_id,file_id=item.id)
        except Exception as e:
            print(f"❌ Error removing file {item.id}: {e}")

    # Step 3: (Optional) Delete the files from OpenAI's file storage
    if delete_files_from_storage:
        for item in vector_store_files.data:
            try:
                print(f"Deleting from OpenAI storage: {item.id}")
                client.files.delete(file_id=item.id)
            except Exception as e:
                print(f"❌ Error deleting file {item.id} from storage: {e}")

    print("✅ Vector store wipe complete.")

upload_new_pdfs_to_vector_store(client, vector_store_id, pdf_folder)