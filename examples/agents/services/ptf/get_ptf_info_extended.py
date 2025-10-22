import os
from textwrap import dedent
from typing import Any, Dict, Optional

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools import tool
from dotenv import load_dotenv, find_dotenv
from mapepire_python import connect
from pep249 import QueryParameters
from agno.storage.sqlite import SqliteStorage


load_dotenv(find_dotenv())

ptf_groups = {
    "SF99675": "HARDWARE AND RELATED PTFS",
    "SF99668": "IBM DB2 MIRROR FOR I",
    "SF99667": "740 TCP/IP PTF",
    "SF99737": "TECHNOLOGY REFRESH",
    "SF99666": "HIGH AVAILABILITY FOR IBM I",
    "SF99661": "WEBSPHERE APP SERVER V8.5",
    "SF99739": "GROUP HIPER",
    "SF99662": "IBM HTTP SERVER FOR I",
    "SF99704": "DB2 FOR IBM I",
    "SF99665": "JAVA",
    "SF99663": "PERFORMANCE TOOLS",
    "SF99738": "GROUP SECURITY",
    "SF99664": "BACKUP RECOVERY SOLUTIONS",
    "SF99225": "Open Source"
}

credentials = {
    "host": os.getenv("HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("PASSWORD"),
    "port": os.getenv("DB_PORT"),
}

missing_ptfs = dedent(
    f"""
    SELECT *
    FROM TABLE(systools.group_ptf_details(?)) a
        WHERE PTF_STATUS = 'PTF MISSING'
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
    name="get_missing_ptf_info",
    description="Determine if this IBM i is missing any PTFs",
    show_result=False,
    stop_after_tool_call=False,
)
def get_missing_ptfs(name: str) -> str:
    """Determine if this IBM i is missing any PTFs

    Args:
        name (str): name id of the PTF group

    Returns:
        str: _description_
    """
    if name not in ptf_groups.keys():
        return "PTF name: {name} not valid"
    
    return run_sql_statement(sql=missing_ptfs, parameters=[name])


ptf_extended_agent = Agent(
    name="Missing PTF Agent",
    model=OpenAIChat(id="gpt-4o", api_key=os.getenv("OPENAI_API_KEY")),
    tools=[get_missing_ptfs],
    context={"ptf_groups": ptf_groups},
    storage=SqliteStorage(
        table_name="ptf_extended_agent_sessions", db_file="tmp/data.db", auto_upgrade_schema=True
    ),
    instructions=dedent(
        """\
        You are an IBM i PTF assistant. Help users check for missing PTFs 
        (Program Temporary Fixes) on their system.
        
        Available PTF Groups to check:
        {ptf_groups}
        
        When asked about missing PTFs, use the get_missing_ptf_info tool 
        and provide the appropriate PTF group code as parameter.
        Explain findings clearly to the user with relevant PTF details.
        """
    ),
    add_context=True,
    add_state_in_messages=True,
    markdown=True,
    debug_mode=False,
)
# ptf_extended_agent.print_response("Are there any missing technology refresh PTFs?", stream=True)
