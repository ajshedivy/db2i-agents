import asyncio
import os
from textwrap import dedent

from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.storage.agent.sqlite import SqliteAgentStorage
from agno.tools.mcp import MCPTools
from mcp import StdioServerParameters
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown
from dotenv import load_dotenv, dotenv_values

# get path of agents directory
db_path = "tmp/agents.db"

server_path = os.path.abspath("db2i-agents/examples/mcp/db2i-mcp-server")
print(f"Server path: {server_path}")


async def run_agent(message: str, agent: Agent, console: Console) -> None:
    """Run the agent with the given message."""

    # Create a custom callback to format the response with rich
    async def rich_formatter(content: str):
        if content.strip():
            md = Markdown(content)
            console.print(md)

    await agent.aprint_response(message, stream=True, callback=rich_formatter)


async def interactive_cli() -> None:
    """Run an interactive CLI session with the DB2i agent."""
    console = Console()

    console.print(
        Panel.fit(
            "[bold blue]DB2i Database Assistant CLI[/bold blue]\n"
            "Type [bold yellow]'exit'[/bold yellow], [bold yellow]'quit'[/bold yellow], or [bold yellow]Ctrl+C[/bold yellow] to end the conversation",
            title="DB2i Agent",
            border_style="blue",
        )
    )

    server_params = StdioServerParameters(
        command="uvx",
        args=[
            "db2i-mcp-server",
            "--use-env"
        ],
        env= dotenv_values()
    )

    # Create a client session to connect to the MCP server
    async with MCPTools(server_params=server_params) as mcp_tools:
        agent = Agent(
            model=Ollama(id="qwen2.5:latest"),  # OpenAIChat(id="gpt-4o"),
            tools=[mcp_tools],
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
            debug_mode=True,
        )

        try:
            while True:
                user_input = Prompt.ask("\n[bold green]>[/bold green]")
                if user_input.lower() in ["exit", "quit"]:
                    console.print("[italic]Ending conversation. Goodbye![/italic]")
                    break

                if user_input.strip():
                    console.print(
                        Panel(
                            f"[cyan]{user_input}[/cyan]",
                            title="You",
                            border_style="green",
                        )
                    )
                    console.print(Panel("", title="DB2i Agent", border_style="blue"))
                    await run_agent(user_input, agent, console)
        except KeyboardInterrupt:
            console.print("\n[italic]Ending conversation. Goodbye![/italic]")


# Example usage
if __name__ == "__main__":
    asyncio.run(interactive_cli())
