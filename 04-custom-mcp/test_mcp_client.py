
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    server = StdioServerParameters(
        command="python",
        args=["mcp_server/server.py"],
    )

    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.call_tool(
                "search_products",
                arguments={
                    "search_term": "millet",
                    "max_price": 300,
                    "in_stock_only": True,
                },
            )

            for item in result.content:
                if hasattr(item, "text"):
                    print(item.text)


asyncio.run(main())
