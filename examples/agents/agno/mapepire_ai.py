import argparse
import asyncio
from textwrap import dedent
from typing import Optional
import os

from dotenv import load_dotenv
from mcp import StdioServerParameters

from agno.agent import Agent
from agno.storage.agent.sqlite import SqliteAgentStorage
from agno.tools.mcp import MCPTools
from utils.cli import CLIConfig, InteractiveCLI, get_model


def create_db2i_agent(
    db_path: str = "tmp/agents.db",
    model_id: Optional[str] = None,
    prefer_ollama: Optional[bool] = True,
    debug_mode: bool = True,
) -> Agent:
    """Create and configure a Db2i agent with MCP tools."""

    # Create the agent
    agent = Agent(
        model=get_model(model_id, prefer_ollama),
        tools=[],  # attach mcp_tools later
        storage=SqliteAgentStorage(table_name="mapepire_ai", db_file=db_path),
        instructions=dedent(
            """\
            # Mapepire AI Database Assistant

            You are a Db2i Database assistant powered by Mapepire AI. Help users answer questions about their database using the available SQL tools.

            ## About Your Tools
            - The tools are provided by Mapepire AI, a platform for IBM i systems
            - Each tool runs a predefined SQL statement with parameters
            - You don't have direct access to the SQL statements themselves
            - You must rely on tool descriptions and parameter specifications

            ## Working Process

            1. **Tool Discovery**
            - When a user asks a question, first identify what tools are available
            - Examine tool descriptions and required parameters carefully
            - Map the user's question to the most appropriate tool(s)

            2. **Question Analysis**
            - Determine if the user's question can be answered with available tools
            - If the question is unclear or impossible to answer with available tools, ask for clarification
            - NEVER hallucinate tool capabilities or make up tool names

            3. **Tool Selection & Parameter Preparation**
            - Choose the appropriate tool(s) based on the user's question
            - Prepare parameters according to their specified data types
            - For date/time values, ensure proper formatting
            - For numeric parameters, ensure proper typing
            - For string parameters, ensure proper quoting if needed

            4. **Tool Execution**
            - Only call tools when you have ALL required parameters
            - If a parameter is missing, ask the user for the specific information
            - If a tool call fails, analyze the error and either:
                - Retry with corrected parameters
                - Explain the issue to the user

            5. **Response Formulation**
            - Use tool outputs directly to answer the user's question
            - Present results in a clear, readable format
            - Explain the data in business terms when appropriate
            - If multiple tool calls were needed, explain how they connect

            ## Important Guidelines
            - The tools execute SQL statements you cannot directly modify
            - Each tool has specific parameters - respect their data types
            - Always verify you have all required information before making a tool call
            - If unsure about a parameter value, ask the user rather than guessing
            - Present results in a well-formatted, easy-to-read manner

            Remember that you are a helpful assistant. If you can't answer a question with the available tools, explain why and suggest what additional information might help.
            \
        """
        ),
        markdown=True,
        show_tool_calls=True,
        add_history_to_messages=True,
        num_history_responses=3,
        read_chat_history=True,
        debug_mode=debug_mode,
    )

    return agent


async def run_db2i_cli(
    debug_mode: bool = False, prefer_ollama: bool = True, model_id: Optional[str] = None
) -> None:
    """Run the Db2i interactive CLI."""
    db_path = "tmp/agents.db"

    # Configure the CLI
    config = CLIConfig(
        title="Db2i Database Assistant CLI", agent_title="Db2i Agent", db_path=db_path
    )

    # Create the agent and CLI
    async with MCPTools(
        server_params=StdioServerParameters(
            command="npx", args=["-y","supergateway", "--sse", os.getenv("MAPEPIRE_AI_MCP_URL")]
        )
    ) as mcp_tools:
        agent = create_db2i_agent(
            db_path=db_path,
            model_id=model_id,
            debug_mode=debug_mode,
            prefer_ollama=prefer_ollama,
        )
        agent.tools.append(mcp_tools)

        cli = InteractiveCLI(agent=agent, config=config)
        await cli.start()


# Example usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "uv run agent.py", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--openai", action="store_true", default=False, help="Use gpt-4o model from OpenAI"
    )
    parser.add_argument("--model-id", default="qwen2.5:latest", help="Use Ollama model")
    parser.add_argument(
        "--debug", action="store_true", default=False, help="Enable debug mode"
    )
    
    load_dotenv()

    args = parser.parse_args()

    if args.openai:
        prefer_ollama = False
        asyncio.run(run_db2i_cli(args.debug, prefer_ollama=False))
    else:
        asyncio.run(
            run_db2i_cli(args.debug, model_id=args.model_id if args.model_id else None)
        )
