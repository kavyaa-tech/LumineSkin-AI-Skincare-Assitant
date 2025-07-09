import os
import pandas as pd
from sentence_transformers import SentenceTransformer
from uuid import uuid4
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = "lumineskin"
REGION = "us-east-1"  

# Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)

if INDEX_NAME in pc.list_indexes().names():
    print(f"Deleting existing index: {INDEX_NAME}")
    pc.delete_index(INDEX_NAME)

print(f"Creating index: {INDEX_NAME} with dimension 384")
pc.create_index(
    name=INDEX_NAME,
    dimension=384,
    metric="cosine",
    spec=ServerlessSpec(cloud="aws", region=REGION)
)

index = pc.Index(INDEX_NAME)

data_files = [
    "data/skincare_products_dataset.csv",
    "data/lumine_skin_faq_dataset.csv",
    "data/skincare_routine_guide.csv"
]

print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

vectors = []

for file_path in data_files:
    print(f"Processing {file_path}...")
    df = pd.read_csv(file_path)
    for row in df.itertuples(index=False):
        text = " | ".join(str(field) for field in row if pd.notna(field))
        embedding = model.encode(text).tolist()
        vectors.append({
            "id": str(uuid4()),
            "values": embedding,
            "metadata": {"text": text}
        })

print(f"Uploading {len(vectors)} vectors to Pinecone...")
batch_size = 100
for i in range(0, len(vectors), batch_size):
    batch = vectors[i:i + batch_size]
    ids = [v["id"] for v in batch]
    embeds = [v["values"] for v in batch]
    metadata = [v["metadata"] for v in batch]
    index.upsert(vectors=list(zip(ids, embeds, metadata)))

print("Ingestion complete.")
