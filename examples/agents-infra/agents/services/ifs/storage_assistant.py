"""IBM i IFS (Integrated File System) Storage Assistant Agent"""
from textwrap import dedent

from agno.agent import Agent
from agno.tools import tool

from db.factory import get_database
from db.ibmi import run_sql_statement
from utils.model_selector import get_model

# Common file types with friendly descriptions
file_types = {
    "STMF": "Stream file (standard file)",
    "DIR": "Directory"
}

# Predefined size thresholds (in MB)
size_categories = {
    "LARGE": 100,  # Files larger than 100 MB
    "MEDIUM": 10,  # Files between 10-100 MB
    "SMALL": 1     # Files between 1-10 MB
}

# SQL query to get IFS files by user
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

# SQL query to get IFS files by size threshold
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


@tool(
    name="get_largest_user_files",
    description="Find the largest files owned by a specific user in the IBM i IFS",
    show_result=False,
    stop_after_tool_call=False,
)
def get_largest_files(username: str = "QSYS", limit: int = 10) -> str:
    """
    Find the largest files owned by a specific user in the IBM i IFS.

    Args:
        username: The IBM i user profile to check
        limit: Maximum number of results to return

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
def get_files_by_size(username: str = "QSYS", min_size_mb: float = 10.0, limit: int = 20) -> str:
    """
    Find files owned by a user that exceed a specific size threshold.

    Args:
        username: The IBM i user profile to check
        min_size_mb: Minimum file size in megabytes
        limit: Maximum number of results to return

    Returns:
        str: List of files that exceed the specified size threshold
    """
    return run_sql_statement(sql=ifs_files_by_size, parameters=[username, min_size_mb, limit])


def get_storage_assistant(
    model_id: str = "openai:gpt-4o",
    debug_mode: bool = False,
) -> Agent:
    """
    Create an IBM i IFS Storage Assistant agent.

    Args:
        model_id: Model specification (e.g., "openai:gpt-4o", "anthropic:claude-sonnet-4-5")
                  or a pre-configured model instance
        debug_mode: Enable debug logging

    Returns:
        Agent configured for IBM i IFS storage analysis
    """
    model = get_model(model_id)

    return Agent(
        id="storage-assistant",
        name="IBM i IFS Storage Assistant",
        model=model,
        tools=[get_largest_files, get_files_by_size],
        dependencies={"file_types": file_types, "size_categories": size_categories},
        add_dependencies_to_context=True,
        description=dedent("""\
            You are an IBM i IFS (Integrated File System) storage analyzer assistant. Help users
            identify large files and understand their IFS storage usage patterns.
        """),
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

            When analyzing storage:
            - Look for unexpectedly large files
            - Identify old files that may no longer be needed
            - Suggest cleanup opportunities for temporary or log files
            - Help users understand their storage consumption patterns

            Additional Information:
            - You are interacting with the user_id: {current_user_id}
            - The user's name might be different from the user_id, you may ask for it if needed.
            """
        ),
        # -*- Storage -*-
        db=get_database("agno-storage"),
        # -*- History -*-
        add_history_to_context=True,
        num_history_runs=3,
        read_chat_history=True,
        # -*- Memory -*-
        enable_agentic_memory=True,
        # -*- Other settings -*-
        markdown=True,
        add_datetime_to_context=True,
        debug_mode=debug_mode,
    )
