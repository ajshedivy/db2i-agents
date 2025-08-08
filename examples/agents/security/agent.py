from textwrap import dedent
import os
from textwrap import dedent
from typing import Any, Dict, Optional

from agno.agent import Agent
from agno.tools import tool
from db2i_shared_utils.cli import get_model
from dotenv import load_dotenv, find_dotenv
from mapepire_python import connect
from pep249 import QueryParameters, ResultSet
from agno.tools.reasoning import ReasoningTools
from dotenv import load_dotenv, find_dotenv
from agno.storage.sqlite import SqliteStorage


# Load environment variables
load_dotenv(find_dotenv())

# Database connection credentials
credentials = {
    "host": os.getenv("HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("PASSWORD"),
    "port": os.getenv("DB_PORT"),
}

sql = {
    "security_metrics": {
        "count_exposed_profiles": {
            "name": "Count Exposed User Profiles",
            "description": "How many *USRPRF's do not have *PUBLIC set to *EXCLUDE?",
            "sql": dedent(
                """
                SELECT COUNT(*)
                FROM qsys2.object_privileges
                WHERE system_object_schema = 'QSYS' AND object_type = '*USRPRF' AND object_name NOT IN ('QDBSHR',
                        'QDBSHRDO', 'QDOC', 'QTMPLPD') AND user_name = '*PUBLIC' AND object_authority <>
                        '*EXCLUDE'
                """
            ),
        },
        "list_exposed_profiles": {
            "name": "List Exposed User Profiles",
            "description": "Which *USRPRF's do not have *PUBLIC set to *EXCLUDE?",
            "sql": dedent(
                """
                SELECT object_name AS user_name, object_authority
                FROM qsys2.object_privileges
                WHERE system_object_schema = 'QSYS' AND object_type = '*USRPRF' AND object_name NOT IN ('QDBSHR',
                        'QDBSHRDO', 'QDOC', 'QTMPLPD') AND user_name = '*PUBLIC' AND object_authority <>
                        '*EXCLUDE'
                
                """
            ),
        },
        "fix_exposed_profiles": {
            "name": "Fix Exposed User Profiles",
            "description": "Which *USRPRF's do not have *PUBLIC set to *EXCLUDE? Include a query that corrects the exposure",
            "sql": dedent(
                """
                SELECT object_name AS user_name, object_authority,
                'SELECT qsys2.qcmdexc(''GRTOBJAUT OBJ(QSYS/' || object_name || ') OBJTYPE(*USRPRF) USER(*PUBLIC) AUT(*EXCLUDE)'') FROM sysibm.sysdummy1'
                    AS corrective_query
                FROM qsys2.object_privileges
                WHERE system_object_schema = 'QSYS' AND object_type = '*USRPRF' AND object_name NOT IN ('QDBSHR',
                        'QDBSHRDO', 'QDOC', 'QTMPLPD') AND user_name = '*PUBLIC' AND object_authority <>
                        '*EXCLUDE'
            
            """
            ),
        },
    }
}


@tool(
    name="count_exposed_profiles",
    description="Count how many user profiles don't have *PUBLIC set to *EXCLUDE",
    show_result=False,
    stop_after_tool_call=False,
)
def count_exposed_profiles() -> str:
    """Count the number of user profiles that don't have *PUBLIC set to *EXCLUDE

    Returns:
        The count of exposed user profiles
    """
    return run_sql_statement(
        dedent(sql["security_metrics"]["count_exposed_profiles"]["sql"])
    )


@tool(
    name="list_exposed_profiles",
    description="List all user profiles that don't have *PUBLIC set to *EXCLUDE",
    show_result=False,
    stop_after_tool_call=False,
)
def list_exposed_profiles() -> str:
    """List all user profiles that don't have *PUBLIC set to *EXCLUDE

    Returns:
        List of exposed user profiles and their authority
    """
    return run_sql_statement(
        dedent(sql["security_metrics"]["list_exposed_profiles"]["sql"])
    )


@tool(
    name="fix_exposed_profiles",
    description="Generate corrective queries for user profiles that don't have *PUBLIC set to *EXCLUDE",
    show_result=False,
    stop_after_tool_call=False,
)
def fix_exposed_profiles() -> str:
    """Generate corrective queries for user profiles that don't have *PUBLIC set to *EXCLUDE

    Returns:
        List of exposed user profiles with corrective SQL queries
    """
    return run_sql_statement(
        dedent(sql["security_metrics"]["fix_exposed_profiles"]["sql"])
    )


@tool(
    name="run_corrective_query",
    description="Execute corrective SQL queries to fix exposed user profiles",
    show_result=False,
    stop_after_tool_call=False,
)
def run_corrective_query(profile_name: str = None) -> str:
    """Execute the corrective SQL query to fix an exposed user profile

    Args:
        profile_name: The name of the user profile to fix. If not provided,
                      all exposed profiles will be fixed.

    Returns:
        Results of executing the corrective queries
    """
    # First get the list of exposed profiles with their corrective queries
    result = run_sql_statement(
        dedent(sql["security_metrics"]["fix_exposed_profiles"]["sql"])
    )

    # Parse the result to extract user profiles and their corrective queries
    import json
    import re

    try:
        data = result
        results = []

        for row in data:
            current_profile = row.get("USER_NAME")
            corrective_query = row.get("CORRECTIVE_QUERY")

            # If a specific profile was requested, only fix that one
            if profile_name and profile_name.upper() != current_profile.upper():
                continue

            # Execute the corrective query
            query_result = run_sql_statement(corrective_query)
            results.append(f"Fixed profile {current_profile}: {query_result}")

        if not results:
            if profile_name:
                return f"No exposed profile found with name '{profile_name}'"
            else:
                return "No exposed profiles found that need fixing"

        return "\n".join(results)
    except Exception as e:
        return f"Error executing corrective queries: {str(e)}\nRaw result: {result}"


@tool(
    name="get_security_metrics",
    description=f"Gather security metrics by running one of {list(sql['security_metrics'].keys())}",
    show_result=False,
    stop_after_tool_call=False,
)
def get_security_metrics(id: str = None) -> str:
    """Get security metrics based on the metric ID

    Args:
        id: The security metric ID to run

    Returns:
        Security metric results
    """
    if id not in sql["security_metrics"].keys():
        return f"{id} not valid metric"

    return run_sql_statement(dedent(sql["security_metrics"][id]["sql"]))


def get_security_metrics_summary():
    summary = {}
    for key, metric in sql["security_metrics"].items():
        summary[key] = {"name": metric["name"], "description": metric["description"]}
    return summary


def run_sql_statement(
    sql: str,
    parameters: Optional[QueryParameters] = None,
    creds: Dict[str, Any] = credentials,
) -> ResultSet:
    """Execute SQL statement and return formatted results

    Args:
        sql: SQL statement to execute
        parameters: Optional parameters for prepared statements
        creds: Database connection credentials

    Returns:
        Formatted string with SQL results
    """
    with connect(creds) as conn:
        with conn.execute(sql, parameters=parameters) as cur:
            if cur.has_results:
                result = cur.fetchall()
                return result["data"]
            else:
                return "SQL executed successfully. No results returned."


profile_security_agent = Agent(
    name="Profile Security Agent",
    model=get_model("watsonx:meta-llama/llama-3-3-70b-instruct"),
    tools=[
        count_exposed_profiles,
        list_exposed_profiles,
        fix_exposed_profiles,
        run_corrective_query,
        ReasoningTools(add_instructions=True),
    ],
    storage=SqliteStorage(
        table_name="prf_agent_sessions", db_file="tmp/data.db", auto_upgrade_schema=True
    ),
    context={"security_metrics": get_security_metrics_summary()},
    instructions=dedent(
        """\
    You are an IBM i Security expert. Assist users in analyzing security vulnerabilities
    and identifying potential security risks on their IBM i system.
    
    CRITICAL: NEVER call tools when users ask you to describe yourself, your capabilities, 
    or what you can do. ONLY call tools when users ask for actual data from their system.
    
    Examples of when NOT to call tools:
    - "describe yourself" - Just explain your role, don't call any tools
    - "what can you do?" - List capabilities, don't call any tools  
    - "what tools do you have?" - Describe tools, don't call any tools
    - "how do you work?" - Explain your process, don't call any tools
    - General security questions or best practices - Provide guidance, don't call tools
    
    Examples of when TO call tools:
    - "how many profiles are exposed?" - Call count_exposed_profiles
    - "show me the exposed profiles" - Call list_exposed_profiles
    - "fix the security issues" - Call fix_exposed_profiles or run_corrective_query
    - "analyze my system security" - Call appropriate tools to get actual data
    
    Available security metrics:
    - User profiles exposed to attack (not having *PUBLIC authority set to *EXCLUDE)
    - Detailed lists of vulnerable user profiles
    - Corrective measures for security vulnerabilities
    
    Available tools (use ONLY when actual system data is needed):
    - count_exposed_profiles: Count how many user profiles don't have *PUBLIC set to *EXCLUDE
    - list_exposed_profiles: List all user profiles that don't have *PUBLIC set to *EXCLUDE
    - fix_exposed_profiles: Generate corrective queries for user profiles that don't have *PUBLIC set to *EXCLUDE
    - run_corrective_query: Execute corrective SQL queries to fix exposed user profiles (pass profile_name or fix all)
    - get_security_metrics: Run a specific security metric by ID
    
    Decision process:
    1. Does the user want actual data from their system? → Call appropriate tool
    2. Does the user want to know about capabilities or general info? → Answer without calling tools
    3. Does the user want explanations or best practices? → Answer without calling tools
    
    When you do retrieve data from tools:
    - Look for exposed user profiles
    - Recommend corrective actions for security vulnerabilities
    - Explain the importance of proper security settings
    - Provide exact SQL commands to fix issues
    
    Always think before acting: "Does this question require me to get actual data from the user's system?"
    If NO, just answer the question. If YES, then call the appropriate tool.
    """
    ),
    add_context=True,
    add_state_in_messages=True,
    show_tool_calls=True,
    add_datetime_to_instructions=True,
    add_history_to_messages=True,
    num_history_responses=3,
    markdown=True,
    debug_mode=False,
)
