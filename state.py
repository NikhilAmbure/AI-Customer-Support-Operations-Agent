from typing import Literal, TypedDict
from pydantic import BaseModel, Field

class State(TypedDict, total=False):
    ticket: str
    category: str
    reply: str
    needs_approval: bool

class TriageResult(BaseModel):
    category: Literal["billing", "technical", "general"] = Field(
        description=(
            "billing: payments, refunds, invoices, orders. "
            "technical: bugs, errors, outages, how-to questions. "
            "general: everything else."
        )
    )