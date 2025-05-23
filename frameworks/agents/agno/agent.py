import argparse
import asyncio
from textwrap import dedent
from typing import Optional

from dotenv import dotenv_values
from mcp import StdioServerParameters

from agno.agent import Agent
from agno.storage.agent.sqlite import SqliteAgentStorage
from agno.tools.mcp import MCPTools
from utils.cli import CLIConfig, InteractiveCLI, get_model
from agno.tools.reasoning import ReasoningTools


def create_db2i_agent(
    db_path: str = "tmp/agents.db",
    provider: str = "ollama",
    model_id: Optional[str] = None,
    debug_mode: bool = True,
) -> Agent:
    """Create and configure a Db2i agent with MCP tools."""

    # Create the agent
    agent = Agent(
        model=get_model(provider, model_id),
        tools=[ReasoningTools(add_instructions=True)],  # attach mcp_tools later
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
        add_datetime_to_instructions=True,
        debug_mode=debug_mode,
    )

    return agent


async def run_db2i_cli(
    debug_mode: bool = False, provider: str = "ollama", model_id: Optional[str] = None, stream: bool = False
) -> None:
    """Run the Db2i interactive CLI."""
    db_path = "tmp/agents.db"

    # Configure the CLI
    config = CLIConfig(
        title="Db2i Database Assistant CLI", agent_title="Db2i Agent", db_path=db_path
    )
    
    env_vars = dotenv_values()
    server_args = ["db2i-mcp-server", "--use-env"]
    if "IGNORED_TABLES" in env_vars and env_vars["IGNORED_TABLES"]:
        server_args.extend(["--ignore-tables", env_vars["IGNORED_TABLES"]])

    # Create the agent and CLI
    async with MCPTools(
        server_params=StdioServerParameters(
            command="uvx", args=server_args, env=env_vars
        )
    ) as mcp_tools:
        agent = create_db2i_agent(
            db_path=db_path,
            provider=provider,
            model_id=model_id,
            debug_mode=debug_mode
        )
        agent.tools.append(mcp_tools)

        cli = InteractiveCLI(agent=agent, config=config, stream=stream)
        await cli.start()


# Example usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "uv run agent.py", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--provider", type=str, required=True, choices=["ollama", "openai", "watsonx"], help="Model provider"
    )
    parser.add_argument("--model-id", default="qwen2.5:latest", help="Use Ollama model")
    parser.add_argument(
        "--debug", action="store_true", default=False, help="Enable debug mode"
    )
    parser.add_argument(
        "--stream", action="store_true", help="Enable streaming", default=False
    )

    args = parser.parse_args()
    
    asyncio.run(run_db2i_cli(debug_mode=args.debug, provider=args.provider, model_id=args.model_id, stream=args.stream))