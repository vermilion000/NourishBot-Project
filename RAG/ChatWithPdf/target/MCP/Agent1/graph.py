from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_google_vertexai import ChatVertexAI

llm = ChatVertexAI(
    model="gemini-2.5-flash",
    temperature=0,
    max_tokens=None
)

async def run(query: str):
    async with MultiServerMCPClient({
        "analyst-tools": {
            "command": "python",
            "args": ["./mcp_server.py"],
            "transport": "stdio",
        }
    }) as client:

        tools = await client.get_tools()
        llm_with_tools = llm.bind_tools(tools)

        def agent_node(state: MessagesState):
            return {"messages": [llm_with_tools.invoke(state["messages"])]}

        graph = StateGraph(MessagesState)
        graph.add_node("agent", agent_node)
        graph.add_node("tools", ToolNode(tools))
        graph.add_edge(START, "agent")
        graph.add_conditional_edges("agent", tools_condition)
        graph.add_edge("tools", "agent")

        app = graph.compile()
        result = await app.ainvoke({
            "messages": [{"role": "user", "content": query}]
        })

        print(result["messages"][-1].content)

"""
SENSITIVE_TOOLS = frozenset({"write_to_db", "send_notification", "trigger_webhook"})

async def gated_call(tool_name: str, arguments: dict, execute) -> dict:
    if tool_name in SENSITIVE_TOOLS:
        # In production: push to Slack / internal UI / audit queue
        print(f"\nAPPROVAL REQUIRED {tool_name}")
        print(f"Arguments: {arguments}")
        decision = input("Approve? (y/n): ").strip().lower()

        if decision != "y":
            return {
                "status": "rejected",
                "reason": f"Operator declined '{tool_name}'."
            }

    return await execute(tool_name, arguments)
"""
