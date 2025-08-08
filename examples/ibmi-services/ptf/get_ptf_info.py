import os
from textwrap import dedent
from typing import Any, Dict, Optional

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.models.ollama import Ollama
from agno.tools import tool
from dotenv import load_dotenv, find_dotenv
from mapepire_python import connect
from pep249 import QueryParameters

load_dotenv(find_dotenv())

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
    stop_after_tool_call=False,
)
def get_ptf_currency() -> str:
    return run_sql_statement(sql=ptf_currency)


agent = Agent(
    model=Ollama(id="devstral"), #OpenAIChat(id="gpt-4o", api_key=os.getenv("OPENAI_API_KEY")),
    tools=[get_ptf_currency],
    markdown=True,
    debug_mode=True,
)
agent.print_response("Are there any PTF group updates available?", stream=True)
