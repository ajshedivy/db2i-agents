import argparse
import os
from textwrap import dedent

from dotenv import dotenv_values
from mcp import StdioServerParameters

from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.models.openai import OpenAIChat
from agno.playground import Playground, serve_playground_app
from agno.storage.agent.sqlite import SqliteAgentStorage
from agno.tools.mcp import MCPTools
from agno.utils.log import log_debug
from utils.cli import get_model
from agno.tools.reasoning import ReasoningTools

server_path = "/Users/adamshedivy/Documents/IBM/sandbox/oss/ai/db2i-ai/db2i-agents/frameworks/mcp/db2i-mcp-server"
agent_storage: str = "tmp/agents.db"

# Use environment variables instead of module globals for configuration
# This allows the configuration to persist across module reloads
if "DB2I_PROVIDER" not in os.environ:
    os.environ["DB2I_PROVIDER"] = "ollama"
if "DB2I_MODEL_ID" not in os.environ:
    os.environ["DB2I_MODEL_ID"] = "qwen2.5:latest"
if "DB2I_DEBUG" not in os.environ:
    os.environ["DB2I_DEBUG"] = "false"
if "DB2I_STREAM" not in os.environ:
    os.environ["DB2I_STREAM"] = "false"

# Helper function to access config with defaults
def get_config():
    return {
        "provider": os.environ["DB2I_PROVIDER"],
        "model_id": os.environ["DB2I_MODEL_ID"],
        "debug": os.environ["DB2I_DEBUG"].lower() == "true",
        "stream": os.environ["DB2I_STREAM"].lower() == "true"
    }


async def get_tools() -> StdioServerParameters:
    """Run the filesystem agent with the given message."""
    
    env_vars = dotenv_values()
    server_args = ["db2i-mcp-server", "--use-env"]
    if "IGNORED_TABLES" in env_vars and env_vars["IGNORED_TABLES"]:
        server_args.extend(["--ignore-tables", env_vars["IGNORED_TABLES"]])

    # MCP parameters for the Filesystem server accessed via `npx`
    server_params = StdioServerParameters(
        command="uvx", args=server_args, env=env_vars
    )

    tools = MCPTools(server_params=server_params)
    await tools.__aenter__()
    return tools


def get_agent(tools: MCPTools, config) -> None:

    # Create a client session to connect to the MCP server
    agent = Agent(
        name="Db2i Agent",
        model=get_model(
            provider=config["provider"],
            model_id=config["model_id"]
        ),
        tools=[ReasoningTools(add_instructions=True), tools],
        storage=SqliteAgentStorage(table_name="db2i_playground", db_file=agent_storage),
        instructions=dedent(
            """\
            You are a Db2i Database assistant. Help users answer questions about the database.
            here are the tools you can use:
            - `list-usable-tables`: List the tables in the database.
            - `describe-table`: Describe a table in the database.
            - `run-sql-query`: Run a SQL query on the database.
            
            When a user asks a question, you can use the tools to answer it. Follow these steps:
            1. Identify the user's question and determine if it can be answered using the tools.
            2. always call `list-usable-tables` first to get the list of tables in the database.
            3. Once you have the list of tables, you can use `describe-table` to get more information about a specific table.
            4. If an SQL query is needed, use the table references and column information from `list-usable-tables` and `describe-table` to construct the query.
                a. DO NOT HALLUCINATE table names or column names.
            5. Use `run-sql-query` to execute the SQL query and get the results.
            6. Format the results in a user-friendly way and return them to the user.

            \
        """
        ),
        markdown=True,
        show_tool_calls=True,
        debug_mode=config["debug"],
    )

    return agent


# app = Playground(agents=[agent]).get_async_router()

tools = None
playground = None


# Cleanup function
async def cleanup_tools():
    global tools
    if tools is not None:
        try:
            await tools.__aexit__(None, None, None)
            log_debug("Tools cleaned up successfully")
        except Exception as e:
            log_debug(f"Error cleaning up tools: {e}")


# This will be called on app startup and will initialize tools
async def initialize_tools_on_startup():
    global tools
    tools = await get_tools()
    return tools


# Non-async init_app function that returns the app
def init_app():
    """Return a Playground app with lazy initialization of tools."""
    config = get_config()
    # Create a placeholder agent that will be initialized with real tools on first use
    placeholder_agent = Agent(
        name="Db2i Agent",
        model=get_model(
            provider=config["provider"],
            model_id=config["model_id"]
        ),
        storage=SqliteAgentStorage(table_name="db2i_playground", db_file=agent_storage),
        markdown=True,
        show_tool_calls=True,
        debug_mode=config["debug"],
    )

    playground = Playground(agents=[placeholder_agent])
    app = playground.get_app()

    # Add startup event to initialize tools
    @app.on_event("startup")
    async def startup_event():
        global tools
        tools = await initialize_tools_on_startup()
        # Update the agent with the initialized tools
        playground.agents[0] = get_agent(tools, config)

    # Add shutdown event to clean up tools
    @app.on_event("shutdown")
    async def shutdown_event():
        await cleanup_tools()

    return app


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "uv run db2i_playground.py",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--provider", 
        type=str, 
        required=True, 
        choices=["ollama", "openai", "watsonx"], 
        help="Model provider"
    )
    parser.add_argument("--model-id", default="qwen2.5:latest", help="Use Ollama model")
    parser.add_argument(
        "--debug", action="store_true", default=False, help="Enable debug mode"
    )
    parser.add_argument(
        "--stream", action="store_true", help="Enable streaming", default=False
    )

    args = parser.parse_args()

    # Update environment variables with CLI args
    os.environ["DB2I_PROVIDER"] = args.provider
    os.environ["DB2I_MODEL_ID"] = args.model_id
    os.environ["DB2I_DEBUG"] = str(args.debug).lower()
    os.environ["DB2I_STREAM"] = str(args.stream).lower()

    # Print configuration for debugging
    config = get_config()
    print(f"Configuration: {config}")
    
    serve_playground_app("db2i_playground:init_app", factory=True)
