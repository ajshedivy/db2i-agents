import argparse
import asyncio
import os
from textwrap import dedent
from typing import Any, Dict, Optional

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools import tool
from agno.tools.reasoning import ReasoningTools
from db2i_shared_utils.cli import CLIConfig, InteractiveCLI, get_model
from dotenv import load_dotenv, find_dotenv
from mapepire_python import connect
from pep249 import QueryParameters
from agno.storage.sqlite import SqliteStorage
import weave

# Load environment variables
load_dotenv(find_dotenv())

# Initialize Weave for observability if API key is provided
if os.getenv("WANDB_API_KEY"):
    weave.init("db2i-agents")

# Database connection credentials
credentials = {
    "host": os.getenv("HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("PASSWORD"),
    "port": os.getenv("DB_PORT"),
}

# Performance metrics configuration
performance_metrics = {
    "system_status": {
        "name": "System Statistics",
        "description": "Overall system performance statistics with CPU, memory, and I/O metrics",
        "interval": 60,
        "sql": """
            SELECT * FROM TABLE(QSYS2.SYSTEM_STATUS(RESET_STATISTICS=>'YES',DETAILED_INFO=>'ALL')) X
        """,
    },
    "system_activity": {
        "name": "System Activity",
        "description": "Current system activity information including active jobs and resource utilization",
        "interval": 20,
        "sql": """
            SELECT * FROM TABLE(QSYS2.SYSTEM_ACTIVITY_INFO())
        """,
    },
    "remote_connections": {
        "name": "Remote Connections",
        "description": "Number of established remote connections to the system",
        "interval": 30,
        "sql": """
            SELECT COUNT(REMOTE_ADDRESS) as REMOTE_CONNECTIONS 
            FROM qsys2.netstat_info 
            WHERE TCP_STATE = 'ESTABLISHED' 
            AND REMOTE_ADDRESS != '::1' 
            AND REMOTE_ADDRESS != '127.0.0.1'
        """,
    },
    "memory_pools": {
        "name": "Memory Pool Information",
        "description": "Information about memory pool sizes and thread utilization",
        "interval": 100,
        "sql": """
            SELECT POOL_NAME, CURRENT_SIZE, DEFINED_SIZE, 
                   MAXIMUM_ACTIVE_THREADS, CURRENT_THREADS, RESERVED_SIZE 
            FROM TABLE(QSYS2.MEMORY_POOL(RESET_STATISTICS=>'YES')) X
        """,
    },
    "temp_storage_buckets": {
        "name": "Named Temporary Storage Buckets",
        "description": "Information about named temporary storage usage",
        "interval": 90,
        "sql": """
            SELECT REPLACE(UPPER(REPLACE(GLOBAL_BUCKET_NAME, '*','')), ' ', '_') as NAME, 
                   BUCKET_CURRENT_SIZE as CURRENT_SIZE, BUCKET_PEAK_SIZE as PEAK_SIZE 
            FROM QSYS2.SystmpSTG 
            WHERE GLOBAL_BUCKET_NAME IS NOT NULL
        """,
    },
    "unnamed_temp_storage": {
        "name": "Unnamed Temporary Storage Usage",
        "description": "Total usage of unnamed temporary storage buckets",
        "interval": 90,
        "sql": """
            SELECT SUM(BUCKET_CURRENT_SIZE) as CURRENT_SIZE, 
                   SUM(BUCKET_PEAK_SIZE) as PEAK_SIZE 
            FROM QSYS2.SystmpSTG 
            WHERE GLOBAL_BUCKET_NAME IS NULL
        """,
    },
    "http_server": {
        "name": "HTTP Server Metrics",
        "description": "Performance metrics for HTTP servers including connections and request handling",
        "interval": 60,
        "sql": """
            SELECT SERVER_NAME CONCAT '_' CONCAT REPLACE(HTTP_FUNCTION, ' ','_') as SERVER_FUNC, 
                   SERVER_NORMAL_CONNECTIONS, SERVER_SSL_CONNECTIONS, SERVER_ACTIVE_THREADS, 
                   SERVER_IDLE_THREADS, SERVER_TOTAL_REQUESTS, SERVER_TOTAL_REQUESTS_REJECTED, 
                   SERVER_TOTAL_RESPONSES, REQUESTS, RESPONSES, NONCACHE_RESPONSES, 
                   BYTES_RECEIVED, BYTES_SENT, NONCACHE_PROCESSING_TIME, CACHE_PROCESSING_TIME 
            FROM QSYS2.HTTP_SERVER_INFO
        """,
    },
    "system_values": {
        "name": "System Values",
        "description": "Current numeric system values that affect performance",
        "interval": 333,
        "sql": """
            SELECT SYSTEM_VALUE_NAME, CURRENT_NUMERIC_VALUE 
            FROM QSYS2.SYSTEM_VALUE_INFO 
            WHERE CURRENT_NUMERIC_VALUE IS NOT NULL
        """,
    },
    "collection_services": {
        "name": "Collection Services Configuration",
        "description": "Current configuration of Collection Services",
        "interval": 600,
        "sql": """
            SELECT * FROM QSYS2.COLLECTION_SERVICES_INFO
        """,
    },
    "collection_categories": {
        "name": "Collection Services Categories",
        "description": "Collection Services category settings and intervals",
        "interval": 600,
        "sql": """
            SELECT cs_category, cs_interval
            FROM QSYS2.COLLECTION_SERVICES_INFO, 
                 LATERAL (SELECT * FROM JSON_TABLE(CATEGORY_LIST, 'lax $.category_list[*]' 
                 COLUMNS(cs_category CLOB(1K) CCSID 1208 PATH 'lax $."category"', 
                         cs_interval CLOB(1K) CCSID 1208 PATH 'lax $."interval"'))) a
        """,
    },
    "active_job_info": {
        "name": "Active Job Info",
        "description": "Find the top 10 consumers of CPU in the QUSRWRK and QSYSWRK subsystems",
        "sql": """
            select CPU_TIME, A.* FROM 
            table(QSYS2.ACTIVE_JOB_INFO(SUBSYSTEM_LIST_FILTER => 'QUSRWRK,QSYSWRK')) A 
            ORDER BY CPU_TIME DESC 
            LIMIT ?
        """,
    },
}


@tool(
    name="get_top_cpu_jobs",
    description="Get the top N CPU consuming jobs in QUSRWRK and QSYSWRK subsystems",
    show_result=False,
    stop_after_tool_call=False,
)
def get_top_cpu_jobs(num_jobs: int = 10) -> str:
    """Get the top N CPU consuming jobs in QUSRWRK and QSYSWRK subsystems

    Args:
        num_jobs: (int) number of jobs

    Returns:
        Information about the top CPU consuming jobs
    """
    return run_sql_statement(
        dedent(performance_metrics["active_job_info"]["sql"]), parameters=[num_jobs]
    )


def get_metrics_summary():
    summary = {}
    for key, metric in performance_metrics.items():
        summary[key] = {"name": metric["name"], "description": metric["description"]}
    return summary


def run_sql_statement(
    sql: str,
    parameters: Optional[QueryParameters] = None,
    creds: Dict[str, Any] = credentials,
) -> str:
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
                return str(result["data"])
            else:
                return "SQL executed successfully. No results returned."


@tool(
    name="get_collection_services_config",
    description="Get Collection Services configuration and category settings",
    show_result=False,
    stop_after_tool_call=False,
)
def get_collection_services_config() -> str:
    """Get Collection Services configuration and category settings

    Returns:
        Configuration details of Collection Services including categories and intervals
    """
    config = run_sql_statement(
        dedent(performance_metrics["collection_services"]["sql"])
    )
    categories = run_sql_statement(
        dedent(performance_metrics["collection_categories"]["sql"])
    )
    return (
        f"Collection Services Config:\n{config}\n\nCollection Categories:\n{categories}"
    )


@tool(
    name="analyze_system_performance",
    description="Analyze system performance using multiple metrics",
    show_result=False,
    stop_after_tool_call=False,
)
def analyze_system_performance() -> str:
    """Analyze system performance using multiple key metrics

    Returns:
        Comprehensive analysis of system performance using multiple data sources
    """
    status = run_sql_statement(dedent(performance_metrics["system_status"]["sql"]))
    memory = run_sql_statement(dedent(performance_metrics["memory_pools"]["sql"]))
    activity = run_sql_statement(dedent(performance_metrics["system_activity"]["sql"]))

    return f"System Status:\n{status}\n\nMemory Pool Usage:\n{memory}\n\nSystem Activity:\n{activity}"


@tool(
    name="get_performance_metrics",
    description=f"Gather relevant performance metrics by running one of {performance_metrics.keys()}",
    show_result=False,
    stop_after_tool_call=False,
)
def get_metrics(id: str = None) -> str:
    if id not in performance_metrics.keys():
        return f"{id} not valid metric"

    if id == "active_job_info":
        return

    return run_sql_statement(dedent(performance_metrics[id]["sql"]))

performance_agent = Agent(
    name="Performance Agent",
    monitoring=True,
    model=OpenAIChat(),
    tools=[
        get_collection_services_config,
        analyze_system_performance,
        get_top_cpu_jobs,
        ReasoningTools(add_instructions=True),
        get_metrics,
    ],
    storage=SqliteStorage(
        table_name="agent_sessions", db_file="tmp/data.db", auto_upgrade_schema=True
    ),
    context={"performance_metrics": get_metrics_summary()},
    instructions=dedent(
        """\
        You are a helpful IBM i Performance Monitoring CLI assistant. Have natural conversations 
        with users about their IBM i system performance. Only gather data when specifically requested.
        
        ## Interaction Guidelines:
        - Respond naturally to greetings, questions, and general conversation
        - Only call tools when users ask specific questions about performance data
        - Provide context and explanations before presenting raw data
        - Ask clarifying questions when requests are ambiguous
        - Offer suggestions for what to investigate based on common performance issues
        
        ## Available Performance Metrics:
        You can gather data about: {performance_metrics}
        
        ## When to Use Tools:
        - User asks about specific metrics (CPU usage, memory, etc.)
        - User wants to see current system status
        - User requests performance analysis or comparison
        - User asks about top consuming jobs
        - User wants Collection Services information
        
        ## Performance Analysis Guidelines:
        When analyzing data you've gathered:
        - Explain what the metrics mean in plain language
        - Highlight concerning values (CPU >80%, memory pool issues, etc.)
        - Provide actionable recommendations
        - Suggest follow-up investigations when appropriate
        
        ## Example Interactions:
        - "How's my system doing?" → Gather system status and provide summary
        - "What are the top CPU jobs?" → Use get_top_cpu_jobs tool
        - "Tell me about performance monitoring" → Explain concepts without gathering data
        - "Hello" → Respond naturally, offer to help with performance questions
        
        Be conversational, helpful, and only gather data when it's actually needed to answer 
        the user's question.
        """
    ),
    add_context=True,
    add_state_in_messages=True,
    markdown=True,
    add_datetime_to_instructions=True,
    add_history_to_messages=True,
    num_history_responses=5,
    debug_mode=False,
)

@weave.op()
async def run_db2i_cli(
    debug_mode: bool = False,
    model_id: Optional[str] = None,
    stream: bool = False,
) -> None:
    """Run the Db2i interactive CLI."""
    db_path = "tmp/agents.db"

    performance_agent.model = get_model(model_id)
    performance_agent.debug_mode = debug_mode
    config = CLIConfig(
        title="Db2i Database Assistant CLI",
        agent_title="Db2i Performance Agent",
        db_path=db_path,
    )



    # Configure the CLI
    cli = InteractiveCLI(agent=performance_agent, config=config, stream=stream)
    await cli.start()


# Example usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "uv run agent.py", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--model-id", default="watsonx:mistralai/mistral-large", help="Use Ollama model"
    )
    parser.add_argument(
        "--debug", action="store_true", default=False, help="Enable debug mode"
    )
    parser.add_argument(
        "--stream", action="store_true", help="Enable streaming", default=False
    )

    args = parser.parse_args()
    asyncio.run(
        run_db2i_cli(
            debug_mode=args.debug,
            model_id=args.model_id,
            stream=args.stream,
        )
    )
