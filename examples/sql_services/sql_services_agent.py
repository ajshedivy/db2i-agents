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
from pep249 import QueryParameters
from pydantic import BaseModel

from db2i_shared_utils.cli import get_model, CLIConfig, InteractiveCLI
import argparse

load_dotenv()


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


@tool(
    name="build_sql_services_tools",
    description="Build a collection of Available IBM i SQL services",
    show_result=False,
    stop_after_tool_call=False,
)
def build_sql_services_tools(catagory: str = None) -> List[ServiceInfo]:
    if catagory not in service_catagories.keys():
        raise KeyError(f"Invalid category '{catagory}'. Valid categories are: {', '.join(service_catagories.keys())}")
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
                return f"No Data found for employee: {id}"


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
        tools=[ReasoningTools(add_instructions=True)],  # attach mcp_tools later
        storage=SqliteAgentStorage(table_name="db2i_mcp", db_file=db_path),
        context={"service_counts": service_catagories},
        instructions=dedent(
            f"""\
            You are an IBM i Services assistant specializing in IBM Db2 for i database services. Help users navigate and utilize the powerful IBM i Services for database administration, system monitoring, and performance analysis.

            Here are the tools you can use:
            - `build_sql_services_tools`: List available IBM i Services for a specific category
            - `run-sql-query`: Execute SQL queries using IBM i Services to retrieve system information

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

            3. **Evaluate Available Services**: Review the returned services to determine if any can answer the user's question. Pay attention to:
               - SERVICE_NAME: The actual service/view name
               - SERVICE_SCHEMA_NAME: The schema (usually QSYS2)
               - EXAMPLE: Sample SQL usage
               - SQL_OBJECT_TYPE: Type of SQL object (VIEW, FUNCTION, etc.)

            4. **Execute SQL if Applicable**: If you find a relevant service:
               a. Use the EXAMPLE field as a starting point for your SQL query
               b. Modify the example SQL to specifically answer the user's question
               c. Always use the correct SERVICE_SCHEMA_NAME and SERVICE_NAME
               d. DO NOT hallucinate service names, schema names, or column names
               e. Use `run-sql-query` to execute the constructed SQL

            5. **Provide Results**: Format the results clearly, including:
               - Explanation of what the results show
               - Which IBM i Service was used
               - Any limitations or considerations
               - Suggestions for related services if applicable

            If no services in the initial category seem relevant, consider trying a related category that might contain the needed information.

            Remember: IBM i Services provide SQL-based access to system information, replacing traditional IBM i commands with modern SQL interfaces.
            \
        """
        ),
        markdown=True,
        show_tool_calls=True,
        add_history_to_messages=True,
        num_history_responses=3,
        read_chat_history=True,
        add_datetime_to_instructions=True,
        debug_mode=debug_mode,
    )

    return agent


async def run_db2i_cli(
    debug_mode: bool = False, provider: str = "ollama", model_id: Optional[str] = None, stream: bool = False
) -> None:
    """Run the Db2i interactive CLI."""
    db_path = "tmp/agents.db"

    # Configure the CLI
    config = CLIConfig(
        title="Db2i Database Assistant CLI", agent_title="Db2i Agent", db_path=db_path
    )
    
    env_vars = dotenv_values()
    server_args = ["db2i-mcp-server", "--use-env"]
    if "IGNORED_TABLES" in env_vars and env_vars["IGNORED_TABLES"]:
        server_args.extend(["--ignore-tables", env_vars["IGNORED_TABLES"]])

    # Create the agent and CLI
    async with MCPTools(
        server_params=StdioServerParameters(
            command="uvx", args=server_args, env=env_vars
        )
    ) as mcp_tools:
        agent = create_db2i_agent(
            db_path=db_path,
            provider=provider,
            model_id=model_id,
            debug_mode=debug_mode
        )
        agent.tools.append(mcp_tools)
        agent.tools.append(build_sql_services_tools)

        cli = InteractiveCLI(agent=agent, config=config, stream=stream)
        await cli.start()


# Example usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "uv run agent.py", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--provider", type=str, required=True, choices=["ollama", "openai", "watsonx"], help="Model provider"
    )
    parser.add_argument("--model-id", default="qwen2.5:latest", help="Use Ollama model")
    parser.add_argument(
        "--debug", action="store_true", default=False, help="Enable debug mode"
    )
    parser.add_argument(
        "--stream", action="store_true", help="Enable streaming", default=False
    )

    args = parser.parse_args()
    print(args)
    asyncio.run(run_db2i_cli(debug_mode=args.debug, provider=args.provider, model_id=args.model_id, stream=args.stream))
