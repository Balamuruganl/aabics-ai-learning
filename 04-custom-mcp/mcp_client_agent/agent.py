
from pathlib import Path

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import (
    McpToolset,
    StdioConnectionParams,
)
from google.adk.tools.mcp_tool import (
    McpToolset,
    StreamableHTTPConnectionParams,
)
from mcp import StdioServerParameters

"""
SERVER_SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "mcp_server"
    / "server.py"
)

organic_shop_tools = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="python",
            args=[str(SERVER_SCRIPT)],
        )
    )
)
"""
organic_shop_tools = McpToolset(
    connection_params=StreamableHTTPConnectionParams(
        url="http://127.0.0.1:8001/mcp",
    )
)
root_agent = LlmAgent(
    name="organic_shop_agent",
    model="gemini-3.5-flash-lite",
    description="Assistant for searching organic shop products.",
    instruction="""
    You are an assistant for an organic food shop.

    Use the search_products tool to find products.
    You can filter by product name, category, maximum price,
    and stock availability.

    Prices are in INR.
    Only report information returned by the tool.
    If no products match, say that no matching products were found.
    """,
    tools=[organic_shop_tools],
)
