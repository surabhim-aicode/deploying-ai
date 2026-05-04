from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph
from typing import TypedDict, List, Dict, Any

# -----------------------------
# 1. Define State Structure
# -----------------------------
class ChatState(TypedDict):
    messages: List[Dict[str, Any]]

# -----------------------------
# 2. Memory Checkpointer
# -----------------------------
checkpointer = InMemorySaver()

# -----------------------------
# 3. Build LangGraph
# -----------------------------
builder = StateGraph(ChatState)

def passthrough(state: ChatState):
    """
    This node does nothing except pass messages through.
    Memory is handled by checkpointer.
    """
    return state

builder.add_node("chat", passthrough)
builder.set_entry_point("chat")

graph = builder.compile(checkpointer=checkpointer)


# -----------------------------
# 4. Memory Manager Wrapper
# -----------------------------
class MemoryManager:
    def __init__(self):
        self.graph = graph

    def invoke(self, user_input: str, thread_id: str):
        """
        Add user message + return full conversation state
        """

        result = self.graph.invoke(
            {
                "messages": [
                    {"role": "user", "content": user_input}
                ]
            },
            {
                "configurable": {
                    "thread_id": thread_id
                }
            }
        )

        return result

    def get_messages(self, thread_id: str):
        """
        Retrieve stored conversation for a thread
        """
        state = self.graph.get_state(
            {"configurable": {"thread_id": thread_id}}
        )

        if state and "messages" in state.values:
            return state.values["messages"]

        return []