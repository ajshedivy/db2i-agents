from agents import agent_knowledge
from agno.utils.log import logger
from mapepire_python import Connection, connect
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
from dotenv import dotenv_values
import asyncio
import os
import argparse

env_values = dotenv_values()

# Sanitize any password information before logging
sanitized_env = {}
for key, value in env_values.items():
    if "password" in key.lower() or "secret" in key.lower() or "key" in key.lower():
        sanitized_env[key] = "******"
    else:
        sanitized_env[key] = value

logger.info(sanitized_env)

server_params = StdioServerParameters(
    command="uvx", args=["db2i-mcp-server", "--use-env"], env=env_values
)


async def run(destination="knowledge/sample", recreate=False, load_to_agent=True):
    # Check if destination directory exists and has files
    if os.path.exists(destination) and os.listdir(destination):
        if not recreate:
            logger.info(f"Destination '{destination}' already exists and contains files.")
            logger.info("Use --recreate flag to overwrite existing files.")
            # If we don't want to recreate but want to load existing knowledge, load it and return
            if load_to_agent:
                logger.info("Loading existing knowledge into agent...")
                load_knowledge_to_agent(destination)
            return
        else:
            logger.info(f"Recreating knowledge base in '{destination}'...")
    
    # Create destination directory if it doesn't exist
    os.makedirs(destination, exist_ok=True)
    
    # Fetch table descriptions from DB2i
    await fetch_table_descriptions(destination)
    
    # Load the knowledge into agent if requested
    if load_to_agent:
        logger.info("Loading knowledge into agent...")
        load_knowledge_to_agent(destination, recreate)


async def fetch_table_descriptions(destination):
    """Fetch table descriptions from DB2i server and save to files"""
    async with stdio_client(server=server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # list tools
            tools = await session.list_tools()

            logger.info("\n===== LIST OF TABLES =====")
            result = await session.call_tool("list-usable-tables")
            tables = []
            if not result.isError and result.content:
                for content in result.content:
                    if content.type == "text":
                        tables_text = content.text.replace("Usable tables: ", "")
                        tables = eval(
                            tables_text
                        )  # Convert string representation of list to actual list
                        logger.info("\nAvailable tables:")
                        for table in sorted(tables):
                            logger.info(f" fetching table description for: {table}")
                            table_result = await session.call_tool(
                                "describe-table", {"table_name": table}
                            )

                            if not table_result.isError and table_result.content:
                                for content in table_result.content:
                                    if content.type == "text":
                                        
                                        data_file = f"{destination}/{table}.txt"
                                        with open(data_file, "w") as file:
                                            file.write(content.text)

                                        logger.info(
                                            f"Wrote description data for the {table} table to {data_file}"
                                        )


def load_knowledge_to_agent(destination, recreate = False):
    """Load knowledge base into agent"""
    try:
        # Use agent_knowledge from agents.py to load knowledge
        agent_knowledge.load(recreate=recreate)
        logger.info(f"Successfully loaded knowledge from '{destination}' into agent")
    except Exception as e:
        logger.error(f"Failed to load knowledge into agent: {str(e)}")


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Load database table descriptions.")
    parser.add_argument("--destination", "-d", default="knowledge/sample",
                      help="Directory path where description files will be saved (default: knowledge/sample)")
    parser.add_argument("--recreate", action="store_true", 
                      help="Overwrite existing files if destination directory already exists (default: False)")
    parser.add_argument("--no-load", action="store_true", 
                      help="Skip loading knowledge into agent (default: False, knowledge is loaded)")
    
    args = parser.parse_args()
    
    # Run with provided arguments (note: no-load inverts the load_to_agent parameter)
    asyncio.run(run(destination=args.destination, recreate=args.recreate, load_to_agent=not args.no_load))
