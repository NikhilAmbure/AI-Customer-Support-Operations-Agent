from typing import Literal, TypedDict
from langgraph.graph import MessagesState
from pydantic import BaseModel, Field

class State(MessagesState, total=False):
    ticket: str
    category: str
    reply: str
    needs_approval: bool
    refund_order_id: str

class TriageResult(BaseModel):
    category: Literal["billing", "technical", "general"] = Field(
        description=(
            "billing: payments, refunds, invoices, orders. "
            "technical: bugs, errors, outages, how-to questions. "
            "general: everything else."
        )
    )