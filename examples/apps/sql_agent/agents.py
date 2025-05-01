"""💎 Reasoning SQL Agent - Your AI Data Analyst!

This advanced example shows how to build a sophisticated text-to-SQL system that
leverages Reasoning Agents to provide deep insights into any data.

Example queries to try:
- "Who are the top 5 drivers with the most race wins?"
- "Compare Mercedes vs Ferrari performance in constructors championships"
- "Show me the progression of fastest lap times at Monza"
- "Which drivers have won championships with multiple teams?"
- "What tracks have hosted the most races?"
- "Show me Lewis Hamilton's win percentage by season"

Examples with table joins:
- "How many races did the championship winners win each year?"
- "Compare the number of race wins vs championship positions for constructors in 2019"
- "Show me Lewis Hamilton's race wins and championship positions by year"
- "Which drivers have both won races and set fastest laps at Monaco?"
- "Show me Ferrari's race wins and constructor championship positions from 2015-2020"

View the README for instructions on how to run the application.
"""

import json
from pathlib import Path
from textwrap import dedent
from typing import Optional
from contextlib import asynccontextmanager

from agno.agent import Agent
from agno.embedder.openai import OpenAIEmbedder
from agno.knowledge.combined import CombinedKnowledgeBase
from agno.knowledge.json import JSONKnowledgeBase
from agno.knowledge.text import TextKnowledgeBase
from agno.models.anthropic import Claude
from agno.models.google import Gemini
from agno.models.groq import Groq
from agno.models.openai import OpenAIChat
from agno.storage.agent.postgres import PostgresAgentStorage
from agno.storage.sqlite import SqliteStorage
from agno.tools.file import FileTools
from agno.tools.reasoning import ReasoningTools
from agno.tools.sql import SQLTools
from agno.vectordb.pgvector import PgVector
from agno.vectordb.lancedb import LanceDb
from agno.vectordb.search import SearchType
from agno.embedder.ollama import OllamaEmbedder
from agno.tools.mcp import MCPTools
from agno.utils.log import logger
from dotenv import dotenv_values

from Db2iTools import Db2iTools

env = dotenv_values()

# ************* Database Connection *************
db_url = "tmp/agent_data.db"
# *******************************

# ************* Paths *************
cwd = Path(__file__).parent
knowledge_dir = cwd.joinpath("knowledge/sample")
output_dir = cwd.joinpath("output")

# Create the output directory if it does not exist
output_dir.mkdir(parents=True, exist_ok=True)
# *******************************

# ************* Storage & Knowledge *************
agent_storage = SqliteStorage(
    # Store agent sessions in the ai.sql_agent_sessions table
    table_name="sql_agent_sessions",
    db_file=db_url,
    auto_upgrade_schema=True,
)

agent_knowledge = CombinedKnowledgeBase(
    sources=[
        # Reads text files, SQL files, and markdown files
        TextKnowledgeBase(
            path=knowledge_dir,
            formats=[".txt", ".sql", ".md"],
        ),
        # Reads JSON files
        JSONKnowledgeBase(path=knowledge_dir),
    ],
    # Store agent knowledge in the ai.sql_agent_knowledge table
    vector_db=LanceDb(
        uri="tmp/lancedb",
        table_name="sql_agent_knowledge",
        search_type=SearchType.hybrid,
        # Use OpenAI embeddings
        embedder=OllamaEmbedder(),
    ),
    # 5 references are added to the prompt
    num_documents=5,
)

# *******************************

# ************* Semantic Model *************
# The semantic model helps the agent identify the tables and columns to use
# This is sent in the system prompt, the agent then uses the `search_knowledge_base` tool to get table metadata, rules and sample queries
# This is very much how data analysts and data scientists work:
#  - We start with a set of tables and columns that we know are relevant to the task
#  - We then use the `search_knowledge_base` tool to get more information about the tables and columns
#  - We then use the `describe_table` tool to get more information about the tables and columns
#  - We then use the `search_knowledge_base` tool to get sample queries for the tables and columns
semantic_model = {
    "dataset_overview": {
        "organizational_structure": ["DEPARTMENT", "ORG"],
        "personnel_data": ["EMPLOYEE", "STAFF", "EMP_PHOTO", "EMP_RESUME"],
        "project_management": ["PROJECT", "PROJACT", "ACT", "EMPPROJACT"],
        "business_operations": ["SALES", "IN_TRAY", "CL_SCHED"],
    },
    "tables": [
        {
            "table_name": "DEPARTMENT",
            "table_description": "The department table describes each department in the enterprise and identifies its manager and the department that it reports to.",
            "Use Case": "Use this table when analyzing organizational structure, department hierarchies, or when needing information about department managers.",
        },
        {
            "table_name": "EMPLOYEE",
            "table_description": "The employee table identifies every employee by an employee number and lists basic personnel information.",
            "Use Case": "Use this table for employee demographics, contact information, or when analyzing workforce distribution across departments.",
        },
        {
            "table_name": "EMP_PHOTO",
            "table_description": "The employee photo table contains a photo of each employee identified by an employee number.",
            "Use Case": "Use this table when retrieving employee photos for ID badges, company directory, or personnel files.",
        },
        {
            "table_name": "EMP_RESUME",
            "table_description": "The employee resumé table contains a resumé for each employee identified by an employee number.",
            "Use Case": "Use this table when reviewing employee qualifications, skill sets, or work history for project assignments or promotions.",
        },
        {
            "table_name": "EMPPROJACT",
            "table_description": "The employee to project activity table identifies the employee who participates in each activity listed for each project. The employee's level of involvement (full-time or part-time) and the activity schedule are also included in the table.",
            "Use Case": "Use this table for resource allocation analysis, employee utilization tracking, or project staffing reports.",
        },
        {
            "table_name": "PROJECT",
            "table_description": "The project table describes each project that the business is currently undertaking. Data contained in each row include the project number, name, person responsible, and schedule dates.",
            "Use Case": "Use this table for project portfolio management, deadline tracking, or when reporting on project ownership.",
        },
        {
            "table_name": "PROJACT",
            "table_description": "The project activity table describes each project activity that the business is currently undertaking. Data contained in each row includes the project number, activity number, and schedule dates.",
            "Use Case": "Use this table for detailed project planning, activity scheduling, or timeline analysis.",
        },
        {
            "table_name": "ACT",
            "table_description": "The activity table describes each activity.",
            "Use Case": "Use this table when looking up activity definitions, categorizing work efforts, or standardizing activity types across projects.",
        },
        {
            "table_name": "CL_SCHED",
            "table_description": "The class schedule table describes each class, the start time for the class, the end time for the class, and the class code.",
            "Use Case": "Use this table for training coordination, classroom scheduling, or employee development program management.",
        },
        {
            "table_name": "IN_TRAY",
            "table_description": "The in-tray table describes an electronic in-basket that contains the timestamp when a message is received, the user ID of the person who sent the message, and the content of the message.",
            "Use Case": "Use this table for internal communication analysis, message tracking, or workflow notification history.",
        },
        {
            "table_name": "ORG",
            "table_description": "The organization table describes the organization of the corporation.",
            "Use Case": "Use this table for corporate structure analysis, organizational planning, or division/department relationship mapping.",
        },
        {
            "table_name": "STAFF",
            "table_description": "The staff table describes the background information about employees.",
            "Use Case": "Use this table for staff qualification analysis, compensation reviews, or when seeking employees with specific backgrounds.",
        },
        {
            "table_name": "SALES",
            "table_description": "The sales table describes the information about each sale for each sales person.",
            "Use Case": "Use this table for sales performance analysis, commission calculations, or regional sales reporting.",
        },
    ],
}
semantic_model_str = json.dumps(semantic_model, indent=2)
# *******************************


@asynccontextmanager
async def sql_agent_session(
    model_id: str = "openai:gpt-4o",
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
    debug_mode: bool = True,
    name: str = "SQL Agent",
    env_vars: Optional[dict] = None,
):
    """Create an SQL agent with MCP tools as a context manager.

    This function creates a temporary agent for a single request, with MCP tools
    properly initialized. It handles connection setup and cleanup automatically.

    The agent maintains conversation context between requests through the session_id.
    By using the same session_id, follow-up questions will have access to the full
    conversation history, allowing for more natural conversational interactions.

    Args:
        model_id: The model ID in format 'provider:model_name'
        user_id: Optional user identifier
        session_id: Optional session ID for continuity between requests
        debug_mode: Enable debug logging
        name: Agent name
        env_vars: Environment variables for the MCP server

    Yields:
        A configured SQL Agent with MCP tools ready to use
    """
    from mcp import StdioServerParameters
    from agno.tools.mcp import MCPTools
    from dotenv import dotenv_values

    # Get environment variables
    if env_vars is None:
        env_vars = dotenv_values()

    # Create the agent first (without MCP tools)
    # Using the same session_id ensures conversation continuity
    agent = get_sql_agent(
        name=name,
        user_id=user_id,
        model_id=model_id,
        session_id=session_id,  # Critical for maintaining conversation context
        debug_mode=debug_mode,
    )

    # Log that we're using an existing session
    if session_id:
        logger.info(
            f"Created agent with existing session ID: {session_id} for conversation continuity"
        )

        # CRITICAL: Make sure the agent loads the session data from the database
        # This ensures the agent has access to the conversation history
        agent.load_session()

    # Set up MCP tools
    server_args = ["db2i-mcp-server", "--use-env"]
    mcp_tools = None

    try:
        # Initialize MCP tools and add to agent
        mcp_tools = MCPTools(
            server_params=StdioServerParameters(
                command="uvx", args=server_args, env=env_vars
            ),
            exclude_tools=["describe-table", "list-usable-tables"],
        )

        # Enter the context manager for MCPTools
        await mcp_tools.__aenter__()

        # Add MCP tools to the agent
        agent.tools.append(mcp_tools)

        # Yield the fully configured agent
        yield agent

    finally:
        # Always clean up MCP tools and remove from agent
        if mcp_tools is not None:
            # Remove MCP tools from agent
            if mcp_tools in agent.tools:
                agent.tools.remove(mcp_tools)

            # Close MCP tools context
            try:
                await mcp_tools.__aexit__(None, None, None)
            except Exception as e:
                logger.warning(f"Error closing MCP tools: {e}")


def get_sql_agent(
    name: str = "SQL Agent",
    user_id: Optional[str] = None,
    model_id: str = "openai:gpt-4o",
    session_id: Optional[str] = None,
    debug_mode: bool = True,
) -> Agent:
    """Returns an instance of the SQL Agent.

    Args:
        user_id: Optional user identifier
        debug_mode: Enable debug logging
        model_id: Model identifier in format 'provider:model_name'
    """
    # Parse model provider and name
    provider, model_name = model_id.split(":")

    # Select appropriate model class based on provider
    if provider == "openai":
        model = OpenAIChat(id=model_name)
    elif provider == "google":
        model = Gemini(id=model_name)
    elif provider == "anthropic":
        model = Claude(id=model_name)
    elif provider == "groq":
        model = Groq(id=model_name)
    else:
        raise ValueError(f"Unsupported model provider: {provider}")

    return Agent(
        name=name,
        model=model,
        user_id=user_id,
        session_id=session_id,
        storage=agent_storage,
        knowledge=agent_knowledge,
        # Enable Agentic RAG i.e. the ability to search the knowledge base on-demand
        search_knowledge=True,
        # Enable the ability to read the chat history
        read_chat_history=True,
        # Enable the ability to read the tool call history
        read_tool_call_history=True,
        # Add tools to the agent
        tools=[
            FileTools(base_dir=output_dir),
            ReasoningTools(add_instructions=True, add_few_shot=True),
            Db2iTools(
                env["SCHEMA"],
                {
                    "host": env["HOST"],
                    "user": env["DB_USER"],
                    "password": env["PASSWORD"],
                    "port": 8076,
                },
                describe_table=False,
            ),
        ],
        debug_mode=debug_mode,
        description=dedent(
            """\
        You are SQrL, an elite Db2 for IBM i SQL specialist focusing on:

        - Enterprise data analytics
          * Employee and department information
          * Project management and resource allocation
          * Organization structure and staffing analysis
          * Sales performance tracking
          
        - Dataset Overview:
          * Organizational structure (DEPARTMENT, ORG)
          * Personnel data (EMPLOYEE, STAFF, EMP_PHOTO, EMP_RESUME)
          * Project management (PROJECT, PROJACT, ACT, EMPPROJACT)
          * Business operations (SALES, IN_TRAY, CL_SCHED)

        You combine deep domain knowledge of IBM Db2 for i with advanced SQL expertise to uncover insights from comprehensive enterprise data from the IBM Db2i sample dataset."""
        ),
        instructions=dedent(
            f"""\
            You are a SQL expert focused on writing precise, efficient queries.

            When a user messages you, determine if you need query the database or can respond directly.
            If you can respond directly, do so.

            If you need to query the database to answer the user's question, follow these steps:
            1. First identify the tables you need to query from the semantic model.
            2. Then, ALWAYS use the `search_knowledge_base(table_name)` tool to get table metadata, rules and sample queries.
            3. If table rules are provided, ALWAYS follow them.
            4. Then, "think" about query construction, don't rush this step.
            5. Follow a chain of thought approach before writing SQL, ask clarifying questions where needed.
            6. If sample queries are available, use them as a reference.
            7. If you need more information about the table, use the `describe_table` tool.
            8. Then, using all the information available, create one single syntactically correct Db2 for i query to accomplish your task.
            9. If you need to join tables, check the `semantic_model` for the relationships between the tables.
                - If the `semantic_model` contains a relationship between tables, use that relationship to join the tables even if the column names are different.
                - If you cannot find a relationship in the `semantic_model`, only join on the columns that have the same name and data type.
                - If you cannot find a valid relationship, ask the user to provide the column name to join.
            10. If you cannot find relevant tables, columns or relationships, stop and ask the user for more information.
            11. Once you have a syntactically correct query, run it using the `run_sql_query` function.
            12. When running a query:
                - Do not add a `;` at the end of the query.
                - Always provide a limit unless the user explicitly asks for all results.
            13. After you run the query, "analyze" the results and return the answer in markdown format.
            14. Make sure to always "analyze" the results of the query before returning the answer.
            15. You Analysis should Reason about the results of the query, whether they make sense, whether they are complete, whether they are correct, could there be any data quality issues, etc.
            16. It is really important that you "analyze" and "validate" the results of the query.
            17. Always show the user the SQL you ran to get the answer.
            18. Continue till you have accomplished the task.
            19. Show results as a table or a chart if possible.

            After finishing your task, ask the user relevant followup questions like "was the result okay, would you like me to fix any problems?"
            If the user says yes, get the previous query using the `get_tool_call_history(num_calls=3)` function and fix the problems.
            If the user wants to see the SQL, get it using the `get_tool_call_history(num_calls=3)` function.


            Finally, here are the set of rules that you MUST follow:

            <rules>
            - All SQL queries must be syntactically correct and valid for Db2 for IBM i.
            - All SQL queries must use a valid table reference format (SCHEMA.TABLE_NAME).
            - Always use the `search_knowledge_base(table_name)` tool to get table information before using `describe-table`.
            - Always call `describe-table` before creating and running a query.
            - Use Db2 for i specific functions like LISTAGG, REGEXP_COUNT, or DATE functions when needed.
            - For pagination, use FETCH FIRST n ROWS ONLY instead of LIMIT.
            - Use CONCAT or || for string concatenation in Db2 for i.
            - When working with dates, use Db2 for i date formats and functions (DATE, TIMESTAMP).
            - Remember that Db2 for i uses VALUES clause for literal row construction, not the PostgreSQL syntax.
            - Make sure your query accounts for duplicate records.
            - Make sure your query accounts for null values.
            - If you run a query, explain why you ran it.
            - Always derive your answer from the data and the query.
            - **NEVER, EVER RUN CODE TO DELETE, UPDATE, OR INSERT DATA.**
            - **Always use valid column references from the table definitions.**
            - **DO NOT HALLUCINATE TABLES, COLUMNS OR DATA.**
            </rules>\
        """
        ),
        additional_context=dedent(
            """\n
        The `semantic_model` contains information about tables and the relationships between them.
        If the users asks about the tables you have access to, simply share the table names from the `semantic_model`.
        <semantic_model>
        """
        )
        + semantic_model_str
        + dedent(
            """
        </semantic_model>\
        """
        ),
    )
