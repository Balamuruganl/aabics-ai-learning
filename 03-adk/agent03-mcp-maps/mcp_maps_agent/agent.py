import os
from dotenv import load_dotenv

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams

load_dotenv()  # Load environment variables from .env file

MAPS_API_KEY = os.getenv("MAPS_API_KEY")

MAPS_MCP_URL = "https://mapstools.googleapis.com/mcp"  # Google-hosted Maps MCP endpoint

maps_toolset = MCPToolset(
    connection_params=StreamableHTTPConnectionParams(
        url=MAPS_MCP_URL,
        headers={
            "X-Goog-Api-Key": MAPS_API_KEY, 
        },
    )
)

root_agent = LlmAgent(
    model="gemini-3.5-flash-lite",
    name="mcp_maps_agent",

instruction="""
You are a helpful Google Maps assistant.

Use the Maps MCP tools for place searches,
weather lookups, and route calculations.

For route requests:
- Call the compute_routes tool.
- Provide the route distance and duration returned.
- Do not claim to provide step-by-step navigation.

If a tool call fails, do not hide the failure
behind a generic temporary-service message.
Explain that the tool failed and include any
safe, useful error details available to you.

Never invent route information.
"""
,
    tools=[maps_toolset]
)
