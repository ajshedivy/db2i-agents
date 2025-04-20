import argparse
import asyncio
from textwrap import dedent
from typing import Optional

from dotenv import dotenv_values
from mcp import StdioServerParameters

from agno.agent import Agent
from agno.storage.agent.sqlite import SqliteAgentStorage
from agno.tools.mcp import MCPTools
from cli import CLIConfig, InteractiveCLI, get_model


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
        storage=SqliteAgentStorage(table_name="db2i_mcp", db_file=db_path),
        instructions=dedent(
            """\
            You are a Db2i Database assistant. Help users answer questions about the database.
            here are the tools you can use:
            - `list-usable-tables`: List the tables in the database.
            - `describe-table`: Describe a table in the database.
            - `run-sql-query`: Run a SQL query on the database.
            
            When a user asks a question, you can use the tools to answer it. Follow these steps:
            1. Identify the user's question and determine if it can be answered using the tools.
            2. always call `list-usable-tables` first to get the list of tables in the database.
            3. Once you have the list of tables, you can use `describe-table` to get more information about a specific table.
            4. If an SQL query is needed, use the table references and column information from `list-usable-tables` and `describe-table` to construct the query.
                a. DO NOT HALLUCINATE table names or column names.
            5. Use `run-sql-query` to execute the SQL query and get the results.
            6. Format the results in a user-friendly way and return them to the user.
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
            command="uvx", args=["db2i-mcp-server", "--use-env"], env=dotenv_values()
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

    args = parser.parse_args()

    if args.openai:
        prefer_ollama = False
        asyncio.run(run_db2i_cli(args.debug, prefer_ollama=False))
    else:
        asyncio.run(
            run_db2i_cli(args.debug, model_id=args.model_id if args.model_id else None)
        )
