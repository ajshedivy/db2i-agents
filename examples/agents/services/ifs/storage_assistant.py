import os
from textwrap import dedent
from typing import Any, Dict, Optional, List

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools import tool
from dotenv import load_dotenv, find_dotenv
from mapepire_python import connect
from pep249 import QueryParameters
from agno.storage.sqlite import SqliteStorage


load_dotenv(find_dotenv())

# Common file types with friendly descriptions
file_types = {
    "STMF": "Stream file (standard file)",
    "DIR": "Directory"
}

# Predefined size thresholds
size_categories = {
    "LARGE": 100,  # Files larger than 100 MB
    "MEDIUM": 10,  # Files between 10-100 MB
    "SMALL": 1     # Files between 1-10 MB
}

credentials = {
    "host": os.getenv("HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("PASSWORD"),
    "port": os.getenv("DB_PORT"),
}

ifs_files_by_user = dedent(
    """
    with ifsobjs (path, type) as (
      select path_name, object_type
        from table(qsys2.object_ownership(?)) a
          where path_name is not null
    )
    select i.path, 
           i.type, 
           data_size as size_bytes, 
           data_size / 1024 / 1024 as size_mb,
           last_used_timestamp
      from ifsobjs i, lateral (
        select * from 
          table(qsys2.ifs_object_statistics(
                  start_path_name => path, 
                  subtree_directories => 'NO'))) z
    order by data_size desc
    limit ?
    """
)

ifs_files_by_size = dedent(
    """
    with ifsobjs (path, type) as (
      select path_name, object_type
        from table(qsys2.object_ownership(?)) a
          where path_name is not null
    )
    select i.path, 
           i.type, 
           data_size as size_bytes, 
           data_size / 1024 / 1024 as size_mb,
           last_used_timestamp
      from ifsobjs i, lateral (
        select * from 
          table(qsys2.ifs_object_statistics(
                  start_path_name => path, 
                  subtree_directories => 'NO'))) z
    where data_size / 1024 / 1024 >= ?
    order by data_size desc
    limit ?
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
                return "No data found matching the criteria"


@tool(
    name="get_largest_user_files",
    description="Find the largest files owned by a specific user in the IBM i IFS",
    show_result=False,
    stop_after_tool_call=False,
)
def get_largest_files(username: str = "QSYS", limit: int = 10) -> str:
    """Find the largest files owned by a specific user in the IBM i IFS.
    
    Args:
        username (str): The IBM i user profile to check
        limit (int): Maximum number of results to return
        
    Returns:
        str: List of the largest files owned by the specified user
    """
    return run_sql_statement(sql=ifs_files_by_user, parameters=[username, limit])


@tool(
    name="get_files_by_size_threshold",
    description="Find files owned by a user that exceed a specific size threshold in MB",
    show_result=False,
    stop_after_tool_call=False,
)
def get_files_by_size(username: str, min_size_mb: float, limit: int = 20) -> str:
    """Find files owned by a user that exceed a specific size threshold.
    
    Args:
        username (str): The IBM i user profile to check
        min_size_mb (float): Minimum file size in megabytes
        limit (int): Maximum number of results to return
        
    Returns:
        str: List of files that exceed the specified size threshold
    """
    return run_sql_statement(sql=ifs_files_by_size, parameters=[username, min_size_mb, limit])


storage_agent_simple = Agent(
    name="Simple Storage Agent",
    model=OpenAIChat(id="gpt-4o", api_key=os.getenv("OPENAI_API_KEY")),
    storage=SqliteStorage(
        table_name="storage_agent_sessions", db_file="tmp/data.db", auto_upgrade_schema=True
    ),
    tools=[get_largest_files, get_files_by_size],
    context={"file_types": file_types, "size_categories": size_categories},
    instructions=dedent(
        """\
        You are an IBM i IFS (Integrated File System) storage analyzer assistant. Help users 
        identify large files and understand their IFS storage usage patterns.
        
        File types you can identify:
        {file_types}
        
        Size thresholds (in MB):
        {size_categories}
        
        When asked about file sizes or storage usage, use the appropriate tool:
        - get_largest_user_files: To find a user's largest files overall
        - get_files_by_size_threshold: To find files exceeding a specific size threshold
        
        Explain findings clearly, including:
        - The file path and type
        - The file size in appropriate units (MB/GB)
        - Last modification date
        - Recommendations for large files that might be candidates for archiving
        """
    ),
    add_context=True,
    add_state_in_messages=True,
    markdown=True,
    debug_mode=False,
)
# storage_agent_simple.print_response("What are the largest files owned by ASHEDIVY? Are there any over 50MB?", stream=True)