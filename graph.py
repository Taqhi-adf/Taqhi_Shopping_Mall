import re
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from tools import weather_tool, product_lookup_tool, product_rag_tool, transport_assessment_tool
from config import OLLAMA_BASE_URL, OLLAMA_MODEL

class MallState(TypedDict, total=False):
    question: str
    product_id: str | None
    weather: dict
    product: dict
    rag_evidence: str
    assessment: dict
    answer: str

llm = ChatOllama(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=0,
)

def detect_product_id(question: str):
    match = re.search(
        r"\b(?:GROC|FROZ|BAKE|COSM|ELEC|HOME|TOY|CHEM|BABY)-\d{3}\b",
        question.upper(),
    )
    return match.group(0) if match else None

def collect_data(state: MallState):
    question = state["question"]
    product_id = state.get("product_id") or detect_product_id(question)

    weather = weather_tool.invoke({})
    rag = product_rag_tool.invoke(question)
    product = product_lookup_tool.invoke(product_id) if product_id else {}
    assessment = (
        transport_assessment_tool.invoke(product_id)
        if product_id else {}
    )

    return {
        "product_id": product_id,
        "weather": weather,
        "product": product,
        "rag_evidence": rag,
        "assessment": assessment,
    }

def synthesize(state: MallState):
    prompt = f"""
You are the Taqhi Shopping Mall operations assistant.

Use ONLY the supplied evidence. Never invent product limits.
Clearly distinguish demo data from approved manufacturer/SDS requirements.
Pressure is informational unless a numeric pressure limit is explicitly documented.
Do not provide medical, legal, hazardous-material authorization, or release decisions.

QUESTION:
{state["question"]}

WEATHER:
{state.get("weather")}

PRODUCT FROM SQL:
{state.get("product")}

DETERMINISTIC ASSESSMENT:
{state.get("assessment")}

PDF/RAG EVIDENCE:
{state.get("rag_evidence")}

Return:
1. Answer
2. Product details
3. Environmental readings
4. Expiry status
5. Temperature/humidity/pressure checks
6. Risk/status
7. Recommended operational next step
"""

    response = llm.invoke([
        SystemMessage(content="You are a careful retail operations AI assistant."),
        HumanMessage(content=prompt),
    ])
    return {"answer": response.content}

builder = StateGraph(MallState)
builder.add_node("collect_data", collect_data)
builder.add_node("synthesize", synthesize)
builder.set_entry_point("collect_data")
builder.add_edge("collect_data", "synthesize")
builder.add_edge("synthesize", END)

graph = builder.compile()
