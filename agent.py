import os
from textwrap import dedent
from typing import Any, Dict, Optional

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools import tool
from dotenv import load_dotenv, find_dotenv
from mapepire_python import connect
from pep249 import QueryParameters

# Load environment variables
load_dotenv(find_dotenv())

# Database connection credentials
credentials = {
    "host": os.getenv("HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("PASSWORD"),
    "port": os.getenv("DB_PORT"),
}


def run_sql_statement(
    sql: str,
    parameters: Optional[QueryParameters] = None,
    creds: Dict[str, Any] = credentials,
) -> str:
    """Execute SQL statement and return results"""
    with connect(creds) as conn:
        with conn.execute(sql, parameters=parameters) as cur:
            if cur.has_results:
                result = cur.fetchall()
                return str(result["data"])
            else:
                return "SQL executed successfully. No results returned."

@tool(
    name="count_exposed_profiles",
    description="Count how many user profiles don't have *PUBLIC set to *EXCLUDE",
    show_result=True,
    stop_after_tool_call=False,
)
def count_exposed_profiles() -> str:
    sql = """
        SELECT COUNT(*) AS exposed_profile_count
        FROM qsys2.object_privileges
        WHERE system_object_schema = 'QSYS' 
            AND object_type = '*USRPRF' 
            AND object_name NOT IN ('QDBSHR', 'QDBSHRDO', 'QDOC', 'QTMPLPD') 
            AND user_name = '*PUBLIC' 
            AND object_authority <> '*EXCLUDE'
    """

    result = run_sql_statement(sql)
    return result

# Create the simple agent
agent = Agent(
    model=OpenAIChat(),
    tools=[count_exposed_profiles],
    show_tool_calls=True,
    markdown=True,
)
