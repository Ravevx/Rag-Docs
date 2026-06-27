import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def get_client():
    return Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_answer(question: str, chunks: list[str]) -> str:
    client = get_client()
    context = "\n\n".join(chunks)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. Answer questions based only on the provided context. Be concise and precise."
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}"
            }
        ],
        temperature=0.3,
        max_tokens=512
    )

    return response.choices[0].message.content