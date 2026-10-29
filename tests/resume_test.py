from langgraph.types import Command
from graph import app

config = {"configurable": {"thread_id": "kill-test"}}
print(app.get_state(config).next)        # should be non-empty: the run is still paused
out = app.invoke(Command(resume={"decisions": [{"type": "approve"}]}), config)
print(out["messages"][-1].content)