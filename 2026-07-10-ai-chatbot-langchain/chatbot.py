# chatbot.py
# Run: pip install langchain-openai langgraph
#      export OPENAI_API_KEY="sk-..."
#      python chatbot.py

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.checkpoint.memory import InMemorySaver

# 1. Model
model = ChatOpenAI(model="gpt-5-mini", timeout=30, max_retries=2)

# 2. System prompt — bot ka behaviour
SYSTEM = SystemMessage(
    "Tu ek friendly e-commerce support agent hai. Short, practical jawab de."
)

# 3. Node — model ko call karta hai, system msg + puri history ke saath
def call_model(state: MessagesState):
    response = model.invoke([SYSTEM] + state["messages"])
    return {"messages": response}   # reply history me append ho jayega

# 4. Graph banao
builder = StateGraph(MessagesState)
builder.add_node("chat", call_model)
builder.add_edge(START, "chat")

# 5. Checkpointer = memory. Dev me in-memory; prod me SqliteSaver/PostgresSaver.
checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer)

# 6. Terminal chat loop
def main():
    print("Bot ready. 'quit' likh ke nikal.\n")
    config = {"configurable": {"thread_id": "user-session-1"}}  # ek conversation

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"quit", "exit"}:
            print("Bye.")
            break
        if not user_input:
            continue

        # Sirf naya message bhej — checkpointer purani history khud load karega
        result = graph.invoke(
            {"messages": [{"role": "user", "content": user_input}]},
            config,
        )
        print("Bot:", result["messages"][-1].content, "\n")

if __name__ == "__main__":
    main()