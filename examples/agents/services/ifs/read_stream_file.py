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

load_dotenv()

credentials = {
    "host": os.getenv("HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("PASSWORD"),
    "port": os.getenv("DB_PORT"),
}

# SQL for reading a file
read_file_sql = dedent(
    """
    select line_number, line
      from table (
          qsys2.ifs_read(
            path_name => ?, 
            end_of_line => 'ANY',
            maximum_line_length => default, 
            ignore_errors => 'NO')
        )
    """
)

# SQL for reading specific lines of a file
read_file_range_sql = dedent(
    """
    select line_number, line
      from table (
          qsys2.ifs_read(
            path_name => ?, 
            end_of_line => 'ANY',
            maximum_line_length => default, 
            ignore_errors => 'NO')
        )
      where line_number between ? and ?
    """
)

# SQL for searching file content
search_file_sql = dedent(
    """
    select line_number, line
      from table (
          qsys2.ifs_read(
            path_name => ?, 
            end_of_line => 'ANY',
            maximum_line_length => default, 
            ignore_errors => 'NO')
        )
      where upper(line) like upper(?)
    """
)

# SQL to check if a file exists
check_file_exists_sql = dedent(
    """
    select count(*) as file_count
        from table(qsys2.IFS_OBJECT_STATISTICS( 
            start_path_name => ?,
            subtree_directories => 'NO'))
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
                return "No data found"


def check_if_file_exists(file_path: str) -> bool:
    """Internal helper function to check if a file exists
    
    Args:
        file_path (str): Full path to the file in the IFS
        
    Returns:
        bool: True if the file exists, False otherwise
    """
    result = run_sql_statement(sql=check_file_exists_sql, parameters=[file_path])
    match = re.search(r"FILE_COUNT': (\d+)", result)
    return match is not None and int(match.group(1)) > 0


@tool(
    name="check_file_exists",
    description="Check if a specified file exists in the IFS",
    show_result=False,
    stop_after_tool_call=False,
)
def check_file_exists(file_path: str) -> str:
    """Check if a specified file exists in the IFS.
    
    Args:
        file_path (str): Full path to the file in the IFS
        
    Returns:
        str: Confirmation if the file exists or not
    """
    exists = check_if_file_exists(file_path)
    if exists:
        return f"File {file_path} exists."
    else:
        return f"File {file_path} does not exist."


@tool(
    name="read_file",
    description="Read the entire contents of a file from the IBM i IFS",
    show_result=False,
    stop_after_tool_call=False,
)
def read_file(file_path: str) -> str:
    """Read the entire contents of a file from the IBM i IFS.
    
    Args:
        file_path (str): Full path to the file in the IFS
        
    Returns:
        str: The contents of the file with line numbers
    """
    if not check_if_file_exists(file_path):
        return f"File {file_path} does not exist."
        
    return run_sql_statement(sql=read_file_sql, parameters=[file_path])


@tool(
    name="read_file_lines",
    description="Read specific lines from a file in the IBM i IFS",
    show_result=False,
    stop_after_tool_call=False,
)
def read_file_lines(file_path: str, start_line: int, end_line: int) -> str:
    """Read specific lines from a file in the IBM i IFS.
    
    Args:
        file_path (str): Full path to the file in the IFS
        start_line (int): First line to read (inclusive)
        end_line (int): Last line to read (inclusive)
        
    Returns:
        str: The specified lines of the file with line numbers
    """
    if not check_if_file_exists(file_path):
        return f"File {file_path} does not exist."
        
    return run_sql_statement(sql=read_file_range_sql, parameters=[file_path, start_line, end_line])


@tool(
    name="search_file",
    description="Search for text within a file in the IBM i IFS",
    show_result=False,
    stop_after_tool_call=False,
)
def search_file(file_path: str, search_text: str) -> str:
    """Search for text within a file in the IBM i IFS.
    
    Args:
        file_path (str): Full path to the file in the IFS
        search_text (str): Text to search for (can use % as wildcards)
        
    Returns:
        str: Lines containing the search text with line numbers
    """
    if not check_if_file_exists(file_path):
        return f"File {file_path} does not exist."
        
    # Add wildcards if not already present
    if '%' not in search_text:
        search_pattern = f'%{search_text}%'
    else:
        search_pattern = search_text
        
    return run_sql_statement(sql=search_file_sql, parameters=[file_path, search_pattern])

agent = Agent(
    model=OpenAIChat(id="gpt-4o", api_key=os.getenv("OPENAI_API_KEY")),
    tools=[check_file_exists, read_file, read_file_lines, search_file],
    instructions=dedent(
        """\
        You are an IBM i IFS file reader assistant. Help users view and analyze contents of 
        stream files in the Integrated File System.
        
        You can perform the following actions:
        - Check if files exist in the IFS
        - Read the entire contents of text files
        - Read specific line ranges from text files
        - Search for text patterns within files
        
        When reading files:
        - For large files, suggest reading specific line ranges instead of the entire file
        - When searching, remind users they can use % as wildcards in their search patterns
        - If a file doesn't exist, clearly inform the user
        - Provide insights about the file content when possible
        """
    ),
    add_context=True,
    add_state_in_messages=True,
    markdown=True,
    debug_mode=False,
)
agent.print_response("Can you show me the contents of /usr/local/install.log?", stream=True)