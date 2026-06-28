from fastapi import APIRouter
from pydantic import BaseModel
from app.agents.tasforce_agent import run_agent

router = APIRouter()

class AgentRequest(BaseModel):
    question: str

class AgentResponse(BaseModel):
    answer: str
    tool_used: str

@router.post("/ask", response_model=AgentResponse)
async def agent_ask(request: AgentRequest):
    result = run_agent(request.question)
    return AgentResponse(
        answer=result["answer"],
        tool_used=result["tool_used"]
    )