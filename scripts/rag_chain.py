
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import os
from dotenv import load_dotenv
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from scripts.llm_groq import chat_with_groq  # custom Groq wrapper
import numpy as np

load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = "lumineskin"

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME)

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_from_pinecone(query, top_k=5):
    """
    Retrieve top_k most relevant documents for a query.
    """
    query_vector = embedding_model.encode(query).tolist()
    results = index.query(vector=query_vector, top_k=top_k, include_metadata=True)

    contexts = []
    for match in results["matches"]:
        context_text = match["metadata"].get("text", "")
        contexts.append(context_text)
    return contexts

def generate_rag_answer(user_query):
    """
    Full RAG flow: retrieves relevant context and generates answer using Groq LLM.
    """
    context = retrieve_from_pinecone(user_query)
    prompt = f"""You are LumineSkin's helpful skincare assistant.

Use the following context to answer the user's question, but remember:
- Do NOT promote or discuss other skincare brands in detail.
- Politely inform the user that you represent LumineSkin.
- Redirect the user toward LumineSkin own products or routines.
- give users clear answers detailed way
-"When listing ingredients or answering any questions, format them one-by-one as a numbered or bulleted list. Include a short benefit or description of each."
-Use the context below to answer the user's question clearly and concisely in 3 to 4 short lines max. Avoid unnecessary details.
Answer the user's skincare question briefly, clearly, and politely — in no more than 3–4 lines. Do not repeat the question, and avoid unnecessary explanations. Just give the user the key insight.
-“If the answer contains a list of products, always format each item on a new line with a bullet or number and a short description.”


Use the following context to answer the user's question.
Context:
{chr(10).join(context)}

Question: {user_query}
Answer:"""

    messages = [
    {"role": "system", "content": "You are a helpful skincare advisor for a brand called LumineSkin."},
    {"role": "user", "content": prompt}]
    answer = chat_with_groq(messages)
    return answer
    
"""if __name__ == "__main__":
    while True:
        q = input("Ask a skincare question (or type 'exit'): ")
        if q.lower() == "exit":
            break
        print(generate_rag_answer(q))"""
