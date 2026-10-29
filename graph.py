from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from state import State, TriageResult

load_dotenv()

import os 
os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")

llm = init_chat_model(
    model="gemini-2.5-flash",
    model_provider="google-genai"
) 

triage_llm = llm.with_structured_output(TriageResult)

def triage(state: State):
    result = triage_llm.invoke(
        f"Classify this customer support ticket.\nTicket: {state['ticket']}"
    )
    return {"category": result.category}

def route(state: State) -> str:
    return state["category"]            

# stubs for now; real agents come in the next step
def billing(state: State):
     return {"reply": "[billing agent stub]"}

def technical(state: State):
    return {"reply": "[technical agent stub]"}

def general(state: State): 
    return {"reply": "[general agent stub]"}

g = StateGraph(State)
g.add_node("triage", triage)
g.add_node("billing", billing)
g.add_node("technical", technical)
g.add_node("general", general)

g.add_edge(START, "triage")
g.add_conditional_edges(
    "triage", route,
    {"billing": "billing", "technical": "technical", "general": "general"},
)
for name in ("billing", "technical", "general"):
    g.add_edge(name, END)

app = g.compile()

if __name__ == "__main__":
    tickets = [
        "I was charged twice for order A100",
        "The app crashes when I upload a PDF",
    ]
    for t in tickets:
        out = app.invoke({"ticket": t})
        print(t, "->", out["category"], "|", out["reply"])