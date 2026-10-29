ORDERS = {
    "A100": {"status": "delivered", "amount": 499, "paid": True},
    "A101": {"status": "shipped", "amount": 1299, "paid": True},
    "A102": {"status": "processing", "amount": 250, "paid": False},
}

KB = [
    "Refunds are processed within 5-7 business days after approval.",
    "If the app crashes on upload, update to the latest version and clear the cache.",
    "Support hours are 9am to 6pm IST, Monday to Saturday.",
]


from langchain.tools import tool


@tool
def looking_order(order_id: str) -> str:
    """Look up an order's status, amount and payment state. order_id looks like A100."""
    order = ORDERS.get(order_id.upper())

    if not order:
        return f"No order found with id: {order_id}"

    return f"Order {order_id}: status={order['status']}, amount={order['amount']}, paid={order['paid']}"

@tool
def get_invoice(order_id: str) -> str:
    """Get the invoice summary for an order."""
    order = ORDERS.get(order_id.upper())

    if not order:
        return f"No order found with id {order_id}."
    
    return f"Invoice for {order_id}: total {order['amount']} INR, payment {'received' if order['paid'] else 'pending'}."

@tool
def issue_refund(order_id: str) -> str:
    """Issue a refund for a paid order. A human approves this call before it runs."""
    o = ORDERS.get(order_id.upper())

    if not o:
        return f"No order found with id {order_id}."

    if o["status"] == "refunded":
        return f"Order {order_id.upper()} was already refunded."

    if not o["paid"]:
        return f"Order {order_id} is unpaid, so there is nothing to refund."
    
    o["status"] = "refunded"

    return f"Refund of {o['amount']} INR issued for order {order_id.upper()}."

@tool
def search_kb(query: str) -> str:
    """Search the help center for articles relevant to the query."""
    words = [w.lower() for w in query.split() if len(w) > 3]
    hits = [a for a in KB if any(w in a.lower() for w in words)]
    return "\n".join(hits) if hits else "No matching article found."

@tool
def get_status() -> str:
    """Get the current service status."""
    return "All systems operational."

@tool
def create_ticket(summary: str) -> str:
    """Create an engineering ticket for an issue that needs human follow-up."""
    return "TICKET-1001 created: " + summary