from langchain_core.messages import HumanMessage
from graph import triage
from tickets import TICKETS

correct = 0
for text, expected in TICKETS:
    got = triage({"messages": [HumanMessage(text)]})["category"]
    ok = got == expected
    correct += ok
    print(("PASS" if ok else "FAIL"), "|", text, "| expected", expected, "| got", got)

print(f"\nRouting accuracy: {correct}/{len(TICKETS)}")