import os
import pprint
from textwrap import dedent
from typing import Any, Callable, Dict, Optional

from agno.agent import Agent
from agno.exceptions import StopAgentRun
from agno.models.openai import OpenAIChat
from agno.models.ollama import Ollama
from agno.tools import tool
from dotenv import load_dotenv
from mapepire_python import connect
from pep249 import QueryParameters
from rich.console import Console
from rich.prompt import Prompt
from agno.utils import pprint
from agno.storage.sqlite import SqliteStorage

console = Console()


def confirmation_hook(
    function_name: str, function_call: Callable, arguments: Dict[str, Any]
):
    # Get the live display instance from the console if it exists
    live = getattr(console, '_live', None)

    # Stop the live display temporarily so we can ask for user confirmation
    if live:
        live.stop()  # type: ignore

    # Ask for confirmation
    console.print(f"\nAbout to run [bold blue]{function_name}[/]")
    message = (
        Prompt.ask("Do you want to continue?", choices=["y", "n"], default="y")
        .strip()
        .lower()
    )

    # Restart the live display
    if live:
        live.start()  # type: ignore

    # If the user does not want to continue, raise a StopExecution exception
    if message != "y":
        raise StopAgentRun(
            "Tool call cancelled by user",
            agent_message="Stopping execution as permission was not granted.",
        )
    
    # Call the function
    result = function_call(**arguments)

    # Optionally transform the result

    return result

load_dotenv()

credentials = {
    "host": os.getenv("HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("PASSWORD"),
    "port": os.getenv("DB_PORT"),
}

ptf_currency = dedent(
    """
    With iLevel(iVersion, iRelease) AS
    (
    select OS_VERSION, OS_RELEASE from sysibmadm.env_sys_info
    )
    SELECT P.*
        FROM iLevel, systools.group_ptf_currency P
        WHERE ptf_group_release = 
            'R' CONCAT iVersion CONCAT iRelease concat '0'
        ORDER BY ptf_group_level_available -
            ptf_group_level_installed DESC
    """
)

def run_sql_statement(
    sql: str,
    parameters: Optional[QueryParameters] = None,
    creds: Dict[str, Any] = credentials,
) -> str:
    with connect(creds) as conn:
        with conn.execute(sql, parameters=parameters) as cur:
            if cur.has_results:
                result = cur.fetchall()
                return str(result["data"])
            else:
                return f"No Data found for employee: {id}"

@tool(
    name="get_ptf_currency_info",
    description="Derive the IBM i operating system level and then determine the level of currency of PTF Groups",
    show_result=False,
    stop_after_tool_call=False
)
def get_ptf_currency() -> str:
    return run_sql_statement(sql=ptf_currency)


ptf_agent = Agent(
    name="Simple PTF Agent",
    monitoring=True,
    storage=SqliteStorage(
        table_name="ptf_agent_sessions", db_file="tmp/data.db", auto_upgrade_schema=True
    ),
    model=OpenAIChat(id="gpt-4o", api_key=os.getenv("OPENAI_API_KEY")),
    tools=[get_ptf_currency],
    markdown=True,
    debug_mode=False,
)
# ptf_agent.print_response("Are there any PTF group updates available?", stream=True)
