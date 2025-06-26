import asyncio
import os
from textwrap import dedent
from typing import Any, Dict, List, Optional

from agno.agent import Agent
from agno.storage.agent.sqlite import SqliteAgentStorage
from agno.tools import tool
from agno.tools.mcp import MCPTools
from agno.tools.reasoning import ReasoningTools
from dotenv import dotenv_values, load_dotenv
from mapepire_python import connect
from mcp import StdioServerParameters
from pep249 import QueryParameters, DataError
from pydantic import BaseModel

from db2i_shared_utils.cli import get_model, CLIConfig, InteractiveCLI
import argparse
import json

load_dotenv()

credentials = {
    "host": os.getenv("HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("PASSWORD"),
    "port": os.getenv("DB_PORT"),
}



class ServiceInfo(BaseModel):
    SERVICE_CATEGORY: str
    SERVICE_SCHEMA_NAME: str
    SERVICE_NAME: str
    SQL_OBJECT_TYPE: str
    OBJECT_TYPE: Optional[str]
    SYSTEM_OBJECT_NAME: Optional[str]
    LATEST_DB2_GROUP_LEVEL: Optional[int] = None
    INITIAL_DB2_GROUP_LEVEL: Optional[int] = None
    EARLIEST_POSSIBLE_RELEASE: Optional[str] = None
    EXAMPLE: Optional[str] = None

    model_config = {"from_attributes": True}  # For ORM compatibility


service_catagories = {
    "PTF": 8,
    "SECURITY": 22,
    "WORK MANAGEMENT": 35,
    "MESSAGE HANDLING": 8,
    "LIBRARIAN": 5,
    "STORAGE": 17,
    "BACKUP AND RECOVERY": 5,
    "PRODUCT": 4,
    "SPOOL": 9,
    "SYSTEM HEALTH": 4,
    "JOURNAL": 50,
    "JAVA": 3,
    "APPLICATION": 45,
    "COMMUNICATION": 21,
    "DATABASE-APPLICATION": 9,
    "DATABASE-PERFORMANCE": 10,
    "DATABASE-PLAN CACHE": 14,
    "DATABASE-UTILITY": 18,
    "MIRROR-COMMUNICATION": 8,
    "MIRROR-PRODUCT": 27,
    "MIRROR-REPLICATION": 8,
    "MIRROR-RESYNCHRONIZATION": 5,
    "MIRROR-SERVICEABILITY": 7,
    "IFS": 12,
    "MIRROR-RECLONE": 6,
    "PERFORMANCE": 1,
    "CONFIGURATION": 4,
    "MIGRATE WHILE ACTIVE": 9,
}

service_names = None


credentials = {
    "host": os.getenv("HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("PASSWORD"),
    "port": os.getenv("DB_PORT"),
}

services_info = dedent(
    """
    select * from qsys2.services_info where service_category = ?
    """
)

generate_sql = dedent(
    """
    CALL QSYS2.GENERATE_SQL(
        DATABASE_OBJECT_NAME => ?,
        DATABASE_OBJECT_LIBRARY_NAME => ?,
        DATABASE_OBJECT_TYPE => ?,
        CREATE_OR_REPLACE_OPTION => '1',
        PRIVILEGES_OPTION => '0',
        STATEMENT_FORMATTING_OPTION => '0',
        SOURCE_STREAM_FILE_END_OF_LINE => 'LF',
        SOURCE_STREAM_FILE_CCSID => 1208
    )
    """
)

get_more_info = dedent(
    """
    select * from qsys2.services_info where service_name = ?
    """
)

@tool(
    name="generate_sql_service_definition",
    description=" generate DDL for specific service",
    show_result=False,
    stop_after_tool_call=False
)
def generate_sql_service_definition(object_name, schema_name, object_type):
    if object_name not in service_names:
        raise KeyError(
            f"Invalid Service name: {object_name}"
        )
    
    try:
        result = run_sql_statement(generate_sql, parameters=[object_name, schema_name, object_type])
        
        # Handle the result which could be a list of dictionaries
        if isinstance(result, list):
            # Build the result string safely
            result_strings = []
            for res in result:
                if isinstance(res, dict):
                    # Use dictionary get() method for dictionaries
                    src_data = res.get("SRCDTA", "")
                    result_strings.append(str(src_data))
            return "\n".join(result_strings)
    except DataError:
        return f"No generated sql for service: {schema_name}.{object_name} of type: {object_type}"
    
    
@tool(
    name="get_more_info_on_service",
    description="get more info from qsys2.service_info",
    show_result=False,
    stop_after_tool_call=False
)
def get_more_info_on_service(object_name):
    if object_name not in service_names:
        raise KeyError(
            f"Invalid Service name: {object_name}"
        )
        
    result = run_sql_statement(get_more_info, parameters=[object_name])
    
    return result
        
    

@tool(
    name="build_sql_services_tools",
    description="Build a collection of Available IBM i SQL services",
    show_result=False,
    stop_after_tool_call=False,
)
def build_sql_services_tools(catagory: str = None) -> List[ServiceInfo]:
    if catagory not in service_catagories.keys():
        raise KeyError(
            f"Invalid category '{catagory}'. Valid categories are: {', '.join(service_catagories.keys())}"
        )
    services = run_sql_statement(services_info, parameters=[catagory])

    # build services map
    services_collection = []
    for item in services:
        services_collection.append(ServiceInfo(**item))

    return services_collection


def run_sql_statement(
    sql: str,
    parameters: Optional[QueryParameters] = None,
    creds: Dict[str, Any] = credentials,
) -> List[Any]:
    with connect(creds) as conn:
        with conn.execute(sql, parameters=parameters) as cur:
            if cur.has_results:
                result = cur.fetchall()
                return result["data"]
            else:
                raise DataError(f"No data returned from query: {sql}")


def create_db2i_agent(
    db_path: str = "tmp/agents.db",
    provider: str = "ollama",
    model_id: Optional[str] = None,
    debug_mode: bool = True,
) -> Agent:
    """Create and configure a Db2i agent with MCP tools."""

    # Create the agent
    agent = Agent(
        model=get_model(model_id),
        tools=[],  # attach mcp_tools later
        storage=SqliteAgentStorage(table_name="db2i_mcp", db_file=db_path),
        context={"service_counts": service_catagories},
        instructions=dedent(
            f"""\
            You are an IBM i Services assistant specializing in IBM Db2 for i database services. Help users navigate and utilize the powerful IBM i Services for database administration, system monitoring, and performance analysis.

            Here are the tools you can use:
            - `build_sql_services_tools`: List available IBM i Services for a specific category
            - `get_more_info_on_service`: Get detailed information about a specific service
            - `generate_sql_service_definition`: Generate DDL for a specific service

            Available service categories and their counts:
            {dict(service_catagories)}

            When a user asks a question, follow these steps:

            1. **Determine Service Category**: Analyze the user's question and determine which service category from the available categories would be most relevant:
               - PTF: Program Temporary Fix information
               - SECURITY: Security-related services  
               - WORK MANAGEMENT: Job and work management
               - MESSAGE HANDLING: System message services
               - LIBRARIAN: Library and object management
               - STORAGE: Storage and disk management
               - BACKUP AND RECOVERY: Backup and recovery operations
               - PRODUCT: Product and licensing information
               - SPOOL: Spool file management
               - SYSTEM HEALTH: System health monitoring
               - JOURNAL: Journal and audit services
               - JAVA: Java-related services
               - APPLICATION: Application monitoring
               - COMMUNICATION: Communication services
               - DATABASE-APPLICATION: Database application services
               - DATABASE-PERFORMANCE: Database performance monitoring
               - DATABASE-PLAN CACHE: SQL plan cache services
               - DATABASE-UTILITY: Database utility services
               - MIRROR-*: Various mirror/high availability services
               - IFS: Integrated File System services
               - PERFORMANCE: System performance monitoring
               - CONFIGURATION: System configuration
               - MIGRATE WHILE ACTIVE: Migration services

            2. **Call build_sql_services_tools**: Once you've identified the most relevant category, call `build_sql_services_tools` with that specific category name to get available services. This returns a list of `ServiceInfo` objects:
            {ServiceInfo}

            3. **Get Detailed Service Information**: For each relevant service identified in step 2, call `get_more_info_on_service` with the service name to get comprehensive details about the service including:
               - Complete service metadata
               - Usage examples and parameters
               - Data types and constraints

            4. **Generate Service DDL (if creating SQL queries)**: If the user is asking to create an SQL query or needs the service structure, call `generate_sql_service_definition` using the object name, schema, and type from the detailed service information obtained in step 3. This will provide the complete DDL definition of the service.

            5. **Construct and Execute SQL (if applicable)**: If the user needs data retrieved:
               a. Use the information gathered from steps 3 and 4 to understand the service structure
               b. Construct a valid SQL query based on the service definition and user requirements
               c. Use the correct SERVICE_SCHEMA_NAME and SERVICE_NAME from the detailed service info
               d. DO NOT hallucinate service names, schema names, or column names
               e. Use `run-sql-query` to execute the constructed SQL

            6. **Provide Comprehensive Results**: Format the results clearly, including:
               - **SQL Statement**: Display the formatted SQL query used
               - **Explanation**: Clear explanation of what the query does and what the results show
               - **Services Used**: List which IBM i Service(s) were utilized
               - **Service Details**: Brief description of the service purpose and capabilities
               - **Results**: The actual query results if data was retrieved
               - **Additional Considerations**: Any limitations, performance notes, or suggestions for related services

            **Important Guidelines**:
            - Always gather detailed service information before constructing queries
            - Use the DDL definition to understand available columns and their purposes
            - Provide clear, formatted SQL statements when queries are involved
            - Explain the business value and context of the information retrieved
            - If no services in the initial category seem relevant, consider trying related categories

            Remember: IBM i Services provide SQL-based access to system information, replacing traditional IBM i commands with modern SQL interfaces. Always leverage the detailed service metadata to provide accurate and helpful responses.
            \
        """
        ),
        markdown=True,
        show_tool_calls=True,
        add_history_to_messages=True,
        num_history_responses=5,
        read_chat_history=True,
        add_datetime_to_instructions=True,
        debug_mode=debug_mode,
    )

    return agent


async def run_db2i_cli(
    debug_mode: bool = False,
    provider: str = "ollama",
    model_id: Optional[str] = None,
    stream: bool = False,
) -> None:
    """Run the Db2i interactive CLI."""
    db_path = "tmp/agents.db"

    # Configure the CLI
    config = CLIConfig(
        title="Db2i Database Assistant CLI", agent_title="Db2i Agent", db_path=db_path
    )

    agent = create_db2i_agent(
        db_path=db_path, provider=provider, model_id=model_id, debug_mode=debug_mode
    )
    agent.tools.extend([ReasoningTools(add_instructions=True), build_sql_services_tools, get_more_info_on_service, generate_sql_service_definition])

    cli = InteractiveCLI(agent=agent, config=config, stream=stream)
    await cli.start()


# Example usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "uv run agent.py", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument("--model-id", default="qwen2.5:latest", help="Use Ollama model")
    parser.add_argument(
        "--debug", action="store_true", default=False, help="Enable debug mode"
    )
    parser.add_argument(
        "--stream", action="store_true", help="Enable streaming", default=False
    )

    args = parser.parse_args()

    with open('service_names.json', 'r') as f:
        data = json.load(f)
    
    service_names = [d['SERVICE_NAME'] for d in data]
    
    asyncio.run(
        run_db2i_cli(
            debug_mode=args.debug,
            model_id=args.model_id,
            stream=args.stream,
        )
    )
