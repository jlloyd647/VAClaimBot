import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from tqdm import tqdm

# Setup
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

chunks_dir = "data/chunks"
output_path = "data/embeddings/embedded_chunks.jsonl"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Open output file
with open(output_path, "w", encoding="utf-8") as out_file:
    # Loop through chunk files
    for filename in tqdm(os.listdir(chunks_dir)):
        if not filename.endswith(".json"):
            continue

        with open(os.path.join(chunks_dir, filename), "r", encoding="utf-8") as f:
            chunk = json.load(f)

        chunk_id = os.path.splitext(filename)[0]
        text = chunk.get("text", "")

        try:
            response = client.embeddings.create(
                input=text,
                model="text-embedding-ada-002"
            )
            embedding = response.data[0].embedding
        except Exception as e:
            print(f"❌ Failed on {filename}: {e}")
            continue

        # Combine into a single object
        result = {
            "id": chunk_id,
            "embedding": embedding,
            "text": text,
            "title": chunk.get("title"),
            "citation": chunk.get("citation"),
            "source": chunk.get("source"),
        }

        out_file.write(json.dumps(result) + "\n")
