import os
from textwrap import dedent
from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools import tool
from dotenv import load_dotenv
from mapepire_python import connect

load_dotenv()

creds = {
    k: os.getenv(v)
    for k, v in {
        "host": "HOST",
        "user": "DB_USER",
        "password": "PASSWORD",
        "port": "DB_PORT",
    }.items()
}

ptf_sql = """
    With iLevel(iVersion, iRelease) AS
    (select OS_VERSION, OS_RELEASE from sysibmadm.env_sys_info)
    SELECT P.*
        FROM iLevel, systools.group_ptf_currency P
        WHERE ptf_group_release = 'R' CONCAT iVersion CONCAT iRelease concat '0'
        ORDER BY ptf_group_level_available - ptf_group_level_installed DESC
"""


@tool(
    name="get_ptf_currency_info",
    description="Determine PTF Groups currency level",
    show_result=False,
    stop_after_tool_call=False,
)
def get_ptf_currency():
    with connect(creds) as conn:
        with conn.execute(dedent(ptf_sql)) as cur:
            return str(cur.fetchall()["data"]) if cur.has_results else "No data found"


Agent(
    model=Ollama(id="qwen3:8b"),
    tools=[get_ptf_currency],
    markdown=True,
    debug_mode=True,
).print_response("Are there any PTF group updates available?", stream=True)
