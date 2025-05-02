"""💎 Reasoning SQL Agent - Your AI Data Analyst!

This advanced example shows how to build a sophisticated text-to-SQL system that
leverages Reasoning Agents to provide deep insights into any data.

View the README for instructions on how to run the application.
"""

import argparse
import asyncio
import json
from pathlib import Path
from textwrap import dedent
from typing import Optional

from agno.agent import Agent
from agno.embedder.ollama import OllamaEmbedder
from agno.knowledge.combined import CombinedKnowledgeBase
from agno.knowledge.json import JSONKnowledgeBase
from agno.knowledge.text import TextKnowledgeBase
from agno.models.anthropic import Claude
from agno.models.google import Gemini
from agno.models.groq import Groq
from agno.models.ollama import Ollama
from agno.models.openai import OpenAIChat
from agno.storage.sqlite import SqliteStorage
from agno.tools.mcp import MCPTools
from agno.tools.reasoning import ReasoningTools
from agno.vectordb.lancedb import LanceDb
from agno.vectordb.search import SearchType
from dotenv import dotenv_values
from mcp import StdioServerParameters

from cli import CLIConfig, InteractiveCLI

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


def get_sql_agent(
    name: str = "SQL Agent",
    user_id: Optional[str] = None,
    model_id: str = "qwen2.5",
    session_id: Optional[str] = None,
    debug_mode: bool = True,
) -> Agent:
    """Returns an instance of the SQL Agent.

    Args:
        user_id: Optional user identifier
        debug_mode: Enable debug logging
        model_id: Model identifier in format 'provider:model_name'
    """
    model_options = {
        "o4-mini": "openai:o4-mini",
        "claude-3-7-sonnet": "anthropic:claude-3-7-sonnet-latest",
        "gpt-4.1": "openai:gpt-4.1",
        "o3": "openai:o3",
        "gemini-2.5-pro": "google:gemini-2.5-pro-preview-03-25",
        "llama-4-scout": "groq:meta-llama/llama-4-scout-17b-16e-instruct",
        "gpt-4o": "openai:gpt-4o",
        "qwen3:30b-a3b": "ollama:qwen3:30b-a3b",
        "qwen3:8b": "ollama:qwen3:8b",
        "qwen2.5": "ollama:qwen2.5"
    }
    
    model_config = model_options.get(model_id, "ollama:qwen2.5")
    # Parse model provider and name
    provider, model_name = model_config.split(":", 1)

    # Select appropriate model class based on provider
    if provider == "openai":
        model = OpenAIChat(id=model_name)
    elif provider == "google":
        model = Gemini(id=model_name)
    elif provider == "anthropic":
        model = Claude(id=model_name)
    elif provider == "groq":
        model = Groq(id=model_name)
    elif provider == "ollama":
        model = Ollama(id=model_name)
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
        num_history_responses=5,
        # Add tools to the agent
        tools=[
            ReasoningTools(add_instructions=True)
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
            You are a Db2i Database assistant. Help users answer questions about the database.
            Here are the tools you can use:
            - `list-usable-tables`: List the tables in the database.
            - `describe-table`: Describe a table in the database.
            - `run-sql-query`: Run a SQL query on the database.
            - `search_knowledge_base(table_name)`: Get detailed information about a specific table.
            
            When a user asks a question, follow these steps:
            1. First, carefully think about what the user is asking and create a plan. DO NOT rush this step.
            2. Check if the question can be answered directly from the semantic_model information:
                - For questions about table relationships, available tables, or general table purposes, reference the semantic_model FIRST
                - If the semantic_model contains sufficient information, answer directly without using tools
                - Only use tools when you need specific details not found in the semantic_model

            3. For questions requiring database details beyond what's in the semantic_model:
                a. Use `list-usable-tables` to confirm available tables
                b. Use `search_knowledge_base(table_name)` to get detailed schema and sample queries
                c. Use `describe-table` only if you need additional column information

            4. If you need to query the database to answer the user's question:
                a. First identify the tables you need to query from the semantic model
                b. ALWAYS use the `search_knowledge_base(table_name)` tool for EACH relevant table to get table metadata, rules and sample queries
                c. If table rules are provided, ALWAYS follow them
                d. "Think" about query construction using a chain of thought approach - don't rush this step
                e. If sample queries are available, use them as a reference
                f. Construct a syntactically correct Db2 for i SQL query using validated table and column names
                g. For table joins:
                - Check the semantic_model for relationships between tables first
                - If a relationship exists in the semantic_model, use that relationship even if column names differ
                - If no relationship is found, only join on columns with the same name and data type
                - If you cannot determine a valid relationship, ask the user for clarification
                h. Run the query using `run-sql-query` (without adding a semicolon at the end)
                i. Always include a FETCH FIRST n ROWS ONLY clause unless the user explicitly asks for all results
                j. Thoroughly analyze the results - consider whether they make sense, are complete, correct, and check for potential data quality issues
                k. Format results clearly as tables or charts when appropriate

            5. Always display the SQL statement you executed to the user
            6. Provide meaningful insights related to the user's question based on your analysis
            7. After completing your response, suggest relevant follow-up questions or analyses

            <rules>
            IMPORTANT RULES:
            - ALWAYS check the semantic_model first before using any tools
            - For structure/schema questions, prefer information from the semantic_model when possible
            - Only use tools when you need specific details not available in the semantic_model
            - Always use the `search_knowledge_base(table_name)` tool before constructing SQL queries
            - Always follow Db2 for i syntax (not PostgreSQL or other dialects)
            - All SQL queries must use a valid table reference format (SCHEMA.TABLE_NAME)
            - Use FETCH FIRST n ROWS ONLY for pagination (not LIMIT)
            - Properly handle potential NULL values
            - NEVER execute DELETE, UPDATE, or INSERT operations
            - NEVER hallucinate tables, columns, or data that don't exist
            - Always validate your SQL before executing
            - Always analyze the results after executing a query to verify they're logical and answer the question
            - When analyzing results, consider completeness, correctness, and potential data quality issues
            - Always derive your answer from the data and the query
            
            If the user wants to modify a previous query:
            - Use `get_tool_call_history(num_calls=3)` to retrieve the previous query
            - Make the requested modifications while following all the rules above
            
            After completing your response, suggest relevant follow-up questions or analyses that might be valuable to the user.
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
    
    
    
async def run_db2i_cli(
    debug_mode: bool = False, model_id: Optional[str] = None, stream: bool = False
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
        agent = get_sql_agent(
            model_id=model_id,
            debug_mode=debug_mode
        )
        agent.tools.append(mcp_tools)

        cli = InteractiveCLI(agent=agent, config=config, stream=stream)
        await cli.start()


# Example usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "uv run agent.py", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--model-id", default="ollama:qwen2.5:latest", help="Use Ollama model")
    parser.add_argument(
        "--debug", action="store_true", default=False, help="Enable debug mode"
    )
    parser.add_argument(
        "--stream", action="store_true", help="Enable streaming", default=False
    )

    args = parser.parse_args()
    
    asyncio.run(run_db2i_cli(debug_mode=args.debug, model_id=args.model_id, stream=args.stream))
