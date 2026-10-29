from langchain.agents import create_agent
from llm import llm
from tools import (looking_order, get_invoice, issue_refund,
search_kb, get_status, create_ticket)
from langchain.agents.middleware import HumanInTheLoopMiddleware

billing_agent = create_agent(
    llm,
    tools=[looking_order, get_invoice, issue_refund],
    system_prompt=(
        "You are a billing support agent. Check the order with looking_order first. "
        "If the customer wants a refund, call issue_refund. "
        "After the tool returns, report exactly what the tool result says. "
        "If the result says the refund was issued, say it is done. "
        "If the tool was rejected or returned an error, say the refund was not issued. "
        "Never describe a refund as pending after the tool has returned."
        "Always call looking_order for the current state of an order, even if it appears "
        "earlier in the conversation. Never rely on earlier messages for order status or payment."
    ),
    middleware=[HumanInTheLoopMiddleware(interrupt_on={"issue_refund": True})]
)

technical_agent = create_agent(
    llm,
    tools=[search_kb, get_status, create_ticket],
    system_prompt=("You are a technical support agent. Search the help center first. "
                   "Create a ticket only if the help center does not solve the issue."),
)

general_agent = create_agent(
    llm,
    tools=[search_kb],
    system_prompt="You are a friendly support agent. Answer using the help center only.",
)