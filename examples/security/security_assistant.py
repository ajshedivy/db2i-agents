import argparse
import asyncio
import os
from typing import Optional

from agent import agent
from db2i_shared_utils.cli import CLIConfig, InteractiveCLI, get_model
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection credentials
credentials = {
    "host": os.getenv("HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("PASSWORD"),
    "port": os.getenv("DB_PORT"),
}


async def run_db2i_cli(
    debug_mode: bool = False,
    model_id: Optional[str] = None,
    stream: bool = False,
) -> None:
    """Run the Db2i interactive CLI."""
    db_path = "tmp/agents.db"

    agent.model = get_model(model_id=model_id)
    if debug_mode:
        agent.debug_mode = debug_mode
    # Configure the CLI
    config = CLIConfig(
        title="Db2i Security Assistant CLI",
        agent_title="Db2i Security Agent",
        db_path=db_path,
    )

    cli = InteractiveCLI(agent=agent, config=config, stream=stream)
    await cli.start()


# Example usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "uv run agent.py", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--model-id", default="openai:gpt-4.1", help="Use Ollama model")
    parser.add_argument(
        "--debug", action="store_true", default=False, help="Enable debug mode"
    )
    parser.add_argument(
        "--stream", action="store_true", help="Enable streaming", default=False
    )

    args = parser.parse_args()
    asyncio.run(
        run_db2i_cli(
            debug_mode=args.debug,
            model_id=args.model_id,
            stream=args.stream,
        )
    )
