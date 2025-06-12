import os
from textwrap import dedent
from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools import tool
from dotenv import load_dotenv
from mapepire_python import connect

load_dotenv()

# Simplified credentials dictionary using dictionary comprehension
creds = {k: os.getenv(v) for k, v in {
    "host": "HOST",
    "user": "DB_USER",
    "password": "PASSWORD",
    "port": "DB_PORT"
}.items()}

# Key performance metrics SQL
system_metrics_sql = """
    SELECT CAST(CURRENT_TIMESTAMP AS VARCHAR(26)) AS TIMESTAMP,
           CAST(CPU_USED_AVERAGE AS DECIMAL(5,2)) AS CPU_PCT,
           ACTIVE_JOBS_IN_SYSTEM AS ACTIVE_JOBS,
           ELAPSED_TIME,
           INTERACTIVE_FEATURE_AVAILABLE,
           CURRENT_INTERACTIVE_PERFORMANCE,
           MAXIMUM_INTERACTIVE_PERFORMANCE
    FROM TABLE(QSYS2.SYSTEM_STATUS(RESET_STATISTICS=>'YES')) X
"""

memory_metrics_sql = """
    SELECT SYSTEM_POOL_ID, POOL_NAME, CURRENT_SIZE / 1024 / 1024 AS SIZE_MB,
           DEFINED_SIZE / 1024 / 1024 AS DEFINED_MB,
           MAXIMUM_ACTIVE_THREADS, CURRENT_THREADS
    FROM TABLE(QSYS2.MEMORY_POOL(RESET_STATISTICS=>'YES'))
    ORDER BY SYSTEM_POOL_ID
"""

job_metrics_sql = """
    SELECT SUBSYSTEM_DESCRIPTION_LIBRARY, SUBSYSTEM_DESCRIPTION_NAME, 
           CURRENT_ACTIVE_JOBS, MAXIMUM_ACTIVE_JOBS
    FROM QSYS2.SUBSYSTEM_POOL_INFO
    ORDER BY CURRENT_ACTIVE_JOBS DESC
    FETCH FIRST 5 ROWS ONLY
"""

temp_storage_sql = """
    SELECT SUM(BUCKET_CURRENT_SIZE) / 1024 / 1024 AS CURRENT_MB, 
           SUM(BUCKET_PEAK_SIZE) / 1024 / 1024 AS PEAK_MB
    FROM QSYS2.SystmpSTG
"""

@tool(
    name="get_key_metrics",
    description="Get key IBM i performance metrics in a concise format",
    show_result=False,
    stop_after_tool_call=False,
)
def get_key_metrics():
    """Get key IBM i performance metrics in a concise format
    
    Returns:
        str: Summary of CPU, memory, job, and temporary storage metrics
    """
    result = {}
    
    # Execute each query and capture results
    with connect(creds) as conn:
        with conn.execute(dedent(system_metrics_sql)) as cur:
            if cur.has_results:
                result["system"] = cur.fetchall()["data"]
        
        with conn.execute(dedent(memory_metrics_sql)) as cur:
            if cur.has_results:
                result["memory"] = cur.fetchall()["data"]
        
        with conn.execute(dedent(job_metrics_sql)) as cur:
            if cur.has_results:
                result["jobs"] = cur.fetchall()["data"]
        
        with conn.execute(dedent(temp_storage_sql)) as cur:
            if cur.has_results:
                result["temp"] = cur.fetchall()["data"]
    
    # Format the output in a concise way
    output = []
    
    # System metrics
    if "system" in result and result["system"]:
        sys_data = result["system"][0]
        output.append(f"SYSTEM METRICS ({sys_data[0]})")
        output.append(f"CPU: {sys_data[1]}% | Active Jobs: {sys_data[2]} | Performance: {sys_data[5]}/{sys_data[6]}")
        output.append("")
    
    # Memory pools
    if "memory" in result and result["memory"]:
        output.append("MEMORY POOLS")
        for pool in result["memory"]:
            output.append(f"Pool {pool[0]} ({pool[1]}): {pool[2]}MB/{pool[3]}MB | Threads: {pool[5]}/{pool[4]}")
        output.append("")
    
    # Top subsystems
    if "jobs" in result and result["jobs"]:
        output.append("TOP SUBSYSTEMS BY ACTIVE JOBS")
        for subsys in result["jobs"]:
            output.append(f"{subsys[1]}: {subsys[2]}/{subsys[3]} active jobs")
        output.append("")
    
    # Temp storage
    if "temp" in result and result["temp"]:
        temp_data = result["temp"][0]
        output.append(f"TEMP STORAGE: Current {temp_data[0]}MB | Peak {temp_data[1]}MB")
    
    return "\n".join(output)

# Create a simple agent with the tool
Agent(
    model=Ollama(id="qwen3:8b"),
    tools=[get_key_metrics],
    markdown=True,
    debug_mode=True,
).print_response("What's the current system performance status?", stream=True)