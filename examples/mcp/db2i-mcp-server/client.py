import asyncio
import json
import os
import argparse
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client
import pprint


async def main(server_path=None):
    # Use current working directory as default if not provided
    if server_path is None:
        server_path = os.path.dirname(os.path.abspath(__file__))
    
    async with stdio_client(
        StdioServerParameters(
            command="uv",
            args=[
                "--directory",
                server_path,
                "run",
                "db2i-mcp-server",
            ],
        )
    ) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # List available tools
            print("\n===== AVAILABLE TOOLS =====")
            tools = await session.list_tools()
            for tool in tools.tools:
                print(f"\nTool: {tool.name}")
                print(f"Description: {tool.description}")
                print(f"Input Schema: {json.dumps(tool.inputSchema, indent=2)}")
            
            # Call the fetch tool
            print("\n===== LIST OF TABLES =====")
            result = await session.call_tool("list-usable-tables")
            if not result.isError and result.content:
                for content in result.content:
                    if content.type == "text":
                        tables_text = content.text.replace("Usable tables: ", "")
                        tables = eval(tables_text)  # Convert string representation of list to actual list
                        print("\nAvailable tables:")
                        for table in sorted(tables):
                            print(f"- {table}")
            
            # Call describe tool
            print("\n===== TABLE DESCRIPTION: EMPLOYEE =====")
            result = await session.call_tool(
                "describe-table",
                {"table_name": "EMPLOYEE"}
            )
            if not result.isError and result.content:
                for content in result.content:
                    if content.type == "text":
                        # Format the table description more readably
                        print("\nTable Schema:")
                        lines = content.text.split("\n")
                        
                        # Find the sample rows section
                        sample_idx = -1
                        for i, line in enumerate(lines):
                            if "sample rows" in line:
                                sample_idx = i
                                break
                        
                        # Print schema definition with indentation
                        for line in lines[:sample_idx]:
                            print(f"  {line}")
                        
                        if sample_idx > 0:
                            print("\nSample Data:")
                            # Format sample data as a table
                            sample_data = lines[sample_idx:]
                            for line in sample_data:
                                print(f"  {line}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Db2i MCP Client")
    parser.add_argument(
        "--server-path", 
        default=None,
        help="Path to the directory containing the db2i-mcp-server (defaults to current script directory)"
    )
    
    args = parser.parse_args()
    asyncio.run(main(args.server_path))