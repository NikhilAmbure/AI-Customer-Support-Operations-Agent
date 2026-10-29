import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.types import Command
from langgraph.graph import StateGraph, START, END
from state import State, TriageResult
from agents import billing_agent, technical_agent, general_agent
from llm import llm


triage_llm = llm.with_structured_output(TriageResult)

def triage(state: State):
    ticket = state["messages"][-1].content
    result = triage_llm.invoke(f"Classify this customer support ticket.\nTicket: {ticket}")
    return {"category": result.category}

def route(state: State) -> str:
    return state["category"]       
     

graph = StateGraph(State)

graph.add_node("triage", triage)
graph.add_node("billing", billing_agent)
graph.add_node("technical", technical_agent)
graph.add_node("general", general_agent)


graph.add_edge(START, "triage")
graph.add_conditional_edges(
    "triage", route,
    {"billing": "billing", "technical": "technical", "general": "general"},
)

for name in ("billing", "technical", "general"):
    graph.add_edge(name, END)

checkpointer = SqliteSaver(sqlite3.connect("checkpoints.db", check_same_thread=False))
app = graph.compile(checkpointer=checkpointer)


# test
# ---- delete checkpoints.db, or use a new thread_id, before rerunning.----
if __name__ == "__main__":
    config = {"configurable": {"thread_id": "t4"}}
    # out = app.invoke({"messages": [("user", "Please refund order A101")]}, config)
    out = app.invoke({"messages": [("user", "Where is my invoice for A102?")]}, config)

    if "__interrupt__" in out:
        print(out["__interrupt__"])          # shows the pending issue_refund call
        ok = input("approve? y/n ").strip().lower() == "y"
        decision = {"type": "approve"} if ok else {"type": "reject", "message": "Refund declined."}
        out = app.invoke(Command(resume={"decisions": [decision]}), config)

    for m in out["messages"]:
        m.pretty_print()