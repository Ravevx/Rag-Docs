from app.rag.retriever import search_documents   # YOUR existing function
from app.rag.generator import generate_answer    # YOUR existing function
from app.core.config import get_settings
from groq import Groq

settings = get_settings()

def get_groq_client():
    return Groq(api_key=settings.groq_api_key)

def tool_extract(question: str) -> str:
    chunks = search_documents(question, top_k=5)
    context = "\n\n".join(chunks)
    client = get_groq_client()
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "Extract and list the requested information clearly in bullet points from the context. Be concise."},
            {"role": "user", "content": f"Context:\n{context}\n\nExtract: {question}"}
        ],
        temperature=0.1
    )
    return response.choices[0].message.content

def tool_generate(question: str) -> str:
    chunks = search_documents(question, top_k=2)
    context = "\n\n".join(chunks)
    client = get_groq_client()
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": """You are a helpful assistant for TASForce's website.
Be professional, friendly, and helpful.
Answer only based on the provided context."""},
            {"role": "user", "content": f"Context:\n{context}\n\nVisitor asks: {question}"}
        ],
        temperature=0.4
    )
    return response.choices[0].message.content

def decide_tool(question: str) -> str:
    client = get_groq_client()
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": """Decide which tool to use. Reply with ONE word only:
- EXTRACT → listing services, features, team, clients, pricing
- CONTACT → contacting, reaching out, getting in touch
- GENERATE → recommendations, comparisons, tailored answers, general questions"""},
            {"role": "user", "content": question}
        ],
        temperature=0
    )
    return response.choices[0].message.content.strip().upper()

def run_agent(question: str) -> dict:
    tool = decide_tool(question)

    if "EXTRACT" in tool:
        answer = tool_extract(question)
        tool_used = "extract"
    elif "CONTACT" in tool:
        answer = tool_generate(question)
        answer += "\n\nFeel free to reach out the TASForce team will be happy to assist you!"
        tool_used = "contact"
    else:  # GENERATE (default)
        answer = tool_generate(question)
        tool_used = "generate"

    return {"answer": answer, "tool_used": tool_used}