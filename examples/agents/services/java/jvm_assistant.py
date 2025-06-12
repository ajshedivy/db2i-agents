import os
import re
from textwrap import dedent
from typing import Any, Dict, Optional, List

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools import tool
from dotenv import load_dotenv
from mapepire_python import connect
from pep249 import QueryParameters
from agno.storage.sqlite import SqliteStorage


load_dotenv()

credentials = {
    "host": os.getenv("HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("PASSWORD"),
    "port": os.getenv("DB_PORT"),
}

# Available JVM options for management
# Available JVM options for management
jvm_options = {
    "GC_ENABLE_VERBOSE": "Enable verbose garbage collection detail for diagnostic tracking",
    "GC_DISABLE_VERBOSE": "Disable verbose garbage collection detail",
    "GENERATE_HEAP_DUMP": "Generate a dump of all heap space allocations that have not yet been freed",
    "GENERATE_SYSTEM_DUMP": "Generate a binary format raw memory image of the job for comprehensive analysis",
    "GENERATE_JAVA_DUMP": "Generate multiple diagnostic files containing JVM and Java application details"
}


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
                return "SQL executed successfully. No results returned."


@tool(
    name="get_top_gc_jobs",
    description="Find the top JVM jobs by time spent in Garbage Collection",
    show_result=False,
    stop_after_tool_call=False,
)
def get_top_gc_jobs(limit: int = 10) -> str:
    """Find the top JVM jobs by time spent in Garbage Collection.

    Args:
        limit (int): Maximum number of results to return (default: 10)

    Returns:
        str: List of JVMs ordered by garbage collection time
    """
    sql = f"""
    SELECT TOTAL_GC_TIME, GC_CYCLE_NUMBER, JAVA_THREAD_COUNT,
           JOB_NAME, JOB_NAME_SHORT, JOB_USER, JOB_NUMBER, 
           PROCESS_ID, START_TIME, MAX_HEAP_SIZE, CURRENT_HEAP_SIZE, 
           IN_USE_HEAP_SIZE, GC_POLICY_NAME 
    FROM QSYS2.JVM_INFO
    ORDER BY TOTAL_GC_TIME DESC
    FETCH FIRST {limit} ROWS ONLY
    """

    return run_sql_statement(sql=dedent(sql))


@tool(
    name="get_jvm_by_user",
    description="Find all JVM jobs for a specific user",
    show_result=False,
    stop_after_tool_call=False,
)
def get_jvm_by_user(user: str) -> str:
    """Find all JVM jobs for a specific user.

    Args:
        user (str): User profile to search for

    Returns:
        str: List of JVMs owned by the specified user
    """
    sql = """
    SELECT JOB_NAME, JOB_NAME_SHORT, JOB_NUMBER, PROCESS_ID, 
           START_TIME, TOTAL_GC_TIME, GC_CYCLE_NUMBER, 
           CURRENT_HEAP_SIZE, IN_USE_HEAP_SIZE, MAX_HEAP_SIZE, 
           GC_POLICY_NAME, JAVA_THREAD_COUNT
    FROM QSYS2.JVM_INFO
    WHERE JOB_USER = ?
    ORDER BY TOTAL_GC_TIME DESC
    """

    return run_sql_statement(sql=dedent(sql), parameters=[user])


@tool(
    name="get_large_heap_jobs",
    description="Find JVM jobs with the largest heap sizes",
    show_result=False,
    stop_after_tool_call=False,
)
def get_large_heap_jobs(limit: int = 10) -> str:
    """Find JVM jobs with the largest heap sizes.

    Args:
        limit (int): Maximum number of results to return (default: 10)

    Returns:
        str: List of JVMs ordered by heap size
    """
    sql = f"""
    SELECT CURRENT_HEAP_SIZE, IN_USE_HEAP_SIZE, MAX_HEAP_SIZE, INITIAL_HEAP_SIZE,
           TOTAL_GC_TIME, GC_CYCLE_NUMBER, GC_POLICY_NAME,
           JOB_NAME, JOB_NAME_SHORT, JOB_USER, JOB_NUMBER, PROCESS_ID, START_TIME, 
           JAVA_THREAD_COUNT
    FROM QSYS2.JVM_INFO
    ORDER BY CURRENT_HEAP_SIZE DESC
    FETCH FIRST {limit} ROWS ONLY
    """

    return run_sql_statement(sql=dedent(sql))


jvm_agent = Agent(
    name="JVM Agent",
    model=OpenAIChat(id="gpt-4o", api_key=os.getenv("OPENAI_API_KEY")),
    storage=SqliteStorage(
        table_name="jvm_agent_sessions", db_file="tmp/data.db", auto_upgrade_schema=True
    ),
    tools=[get_top_gc_jobs, get_jvm_by_user, get_large_heap_jobs],
    context={"jvm_options": jvm_options},
    instructions=dedent(
        """\
        You are a Java Virtual Machine (JVM) performance specialist for IBM i systems.
        Help users monitor and optimize JVMs running on their system.
        
        You can assist with:
        - Finding JVMs with high garbage collection times
        - Identifying JVMs with large heap sizes
        - Getting detailed information about specific JVM jobs
        - Finding all JVMs for a particular user
        - Changing JVM properties (like enabling verbose garbage collection)
        
        When discussing JVM jobs, explain:
        - What high GC times might indicate (memory pressure, inefficient code)
        - Whether heap sizes are appropriate for the workload
        - Potential optimizations for problematic JVMs
        
        Available JVM property options:
        {jvm_options}
        
        Job names in IBM i are typically in the format: JOB_NUMBER/USER/JOB_NAME
        """
    ),
    add_context=True,
    add_state_in_messages=True,
    markdown=True,
    debug_mode=False,
)

# if __name__ == "__main__":
#     jvm_agent.print_response(
#         "Which JVMs are spending the most time in garbage collection? What should I do about it?",
#         stream=True,
#     )

    # agent.print_response(
    #     "Which JVM jobs are under ASHEDIVY? how are they performing?",
    #     stream=True
    # )
