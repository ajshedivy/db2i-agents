from agno.agent import Agent
from agno.models.ibm import WatsonX
from dotenv import load_dotenv
import asyncio

from dotenv import dotenv_values
from mcp import StdioServerParameters

from agno.agent import Agent
from agno.tools.mcp import MCPTools

load_dotenv()


async def run():
    try:
        # Create server parameters
        server_params = StdioServerParameters(
            command="uvx", args=["db2i-mcp-server", "--use-env"], env=dotenv_values()
        )

        # Initialize the MCP tools with explicit schema definition
        async with MCPTools(server_params=server_params) as mcp_tools:
            # Configure the model with proper tools support
            model = WatsonX(
                id="meta-llama/llama-3-3-70b-instruct",
                project_id="0a76f494-f5a7-4798-9529-e35487c6702a",
                url="https://us-south.ml.cloud.ibm.com",
            )

            agent = Agent(
                model=model, markdown=True, tools=[mcp_tools], show_tool_calls=True
            )

            # Print the response in the terminal
            print("Sending query to agent...")
            await agent.aprint_response(
                "what tables do I have access to?", stream=False
            )

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(run())
