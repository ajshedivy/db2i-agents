import asyncio
import os
import sys
from textwrap import dedent
from typing import Optional

from agno.agent import Agent
from agno.storage.agent.sqlite import SqliteAgentStorage
from agno.tools.mcp import MCPTools
from dotenv import dotenv_values
from mcp import StdioServerParameters

from db2i_shared_utils.cli import get_model


async def create_db2i_agent(
    db_path: str = "tmp/agents.db",
    provider: str = "ollama",
    model_id: Optional[str] = None,
    debug_mode: bool = True,
) -> Agent:
    """Create and configure a Db2i agent with MCP tools."""
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
        # Create the agent
        agent = Agent(
            model=get_model(provider, model_id),
            tools=[mcp_tools],  # attach mcp_tools later
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
            add_state_in_messages=True,
            num_history_responses=3,
            read_chat_history=True,
            stream_intermediate_steps=True,
            add_datetime_to_instructions=True,
            debug_mode=debug_mode,
        )

        await agent.aprint_response(
            "How many employees are in each department?", stream=True
        )


# Example usage
if __name__ == "__main__":

    asyncio.run(create_db2i_agent(provider="openai", debug_mode=False))
