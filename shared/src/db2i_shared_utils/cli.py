from dataclasses import dataclass
import os
from typing import Optional
import argparse

from dotenv import dotenv_values, load_dotenv

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.formatted_text import HTML

from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.models.openai import OpenAIChat
from agno.models.base import Model
from agno.models.ibm import WatsonX


def get_model(model_id: str = None) -> Model:
    env_paths = [
        ".env",  # Current directory
        "../.env",  # Parent directory
        "../../.env",  # Two levels up
        "../../../config/.env.central",  # Central config
    ]
    
    env = {}
    for path in env_paths:
        if os.path.exists(path):
            load_dotenv(path)
            env.update(dotenv_values(path))
            break
    
    # Also load from system environment as fallback
    env.update(os.environ)
    
    if model_id is None:
        return Ollama(id="qwen2.5:latest")  # Default model
    
    try:
        provider, model = model_id.split(":", 1)
    except ValueError:
        # Handle case where model_id doesn't contain ":"
        return Ollama(id="qwen2.5:latest")  # Default to Ollama
    
    match provider.lower():
        case "ollama":
            return Ollama(id=model)
        case "openai":
            if env.get("OPENAI_API_KEY") is None:
                raise ValueError("OPENAI_API_KEY environment variable is required for OpenAI models")
            return OpenAIChat(id=model, api_key=env.get("OPENAI_API_KEY"))
        case "anthropic":
            if env.get("ANTHROPIC_API_KEY") is None:
                raise ValueError("ANTHROPIC_API_KEY environment variable is required for Anthropic models")
            # Need to import Anthropic model
            from agno.models.anthropic import Anthropic
            return Anthropic(id=model, api_key=env.get("ANTHROPIC_API_KEY"))
        case "watsonx":
            if any(env.get(key) is None for key in ["IBM_WATSONX_API_KEY", "IBM_WATSONX_PROJECT_ID", "IBM_WATSONX_BASE_URL"]):
                raise ValueError("IBM_WATSONX_API_KEY, IBM_WATSONX_PROJECT_ID, and IBM_WATSONX_BASE_URL environment variables are required for WatsonX models")
            return WatsonX(
                id=model,
                url=env.get("IBM_WATSONX_BASE_URL"),
                api_key=env.get("IBM_WATSONX_API_KEY"),
                project_id=env.get("IBM_WATSONX_PROJECT_ID"),
            )
        case _:
            return Ollama(id="qwen2.5:latest")  # Default to Ollama
        


def create_cli_parser() -> argparse.ArgumentParser:
    """
    Create a command-line argument parser with common agent options.
    
    Returns:
        argparse.ArgumentParser: Configured argument parser
    """
    parser = argparse.ArgumentParser(description="Run an interactive agent CLI")
    
    parser.add_argument(
        "--model-id", 
        type=str,
        default="openai:gpt-4o",
        help="Model identifier in the format 'provider:model'. Supported providers: "
             "ollama (e.g., ollama:qwen2.5:latest), "
             "openai (e.g., openai:gpt-4o), "
             "anthropic (e.g., anthropic:claude-3-sonnet), "
             "watsonx (e.g., watsonx:granite-13b)"
    )
    
    parser.add_argument(
        "--stream",
        action="store_true",
        help="Enable streaming mode for response generation"
    )
    
    return parser


@dataclass
class CLIConfig:
    """Configuration for the interactive CLI."""

    title: str = "Agent CLI"
    subtitle: str = "Type 'exit', 'quit', or Ctrl+C to end the conversation"
    prompt_text: str = ">"
    user_title: str = "You"
    agent_title: str = "Agent"
    border_style_user: str = "green"
    border_style_agent: str = "blue"
    db_path: str = "tmp/agents.db"
    history_file: str = "tmp/history.txt"


class InteractiveCLI:
    """A reusable interactive CLI for working with any Agent."""

    def __init__(
        self,
        agent: Agent,
        config: Optional[CLIConfig] = None,
        console: Optional[Console] = None,
        stream: bool = False
    ):
        """Initialize the CLI with an agent and optional configuration."""
        self.agent = agent
        self.config = config or CLIConfig()
        self.console = console or Console()
        self.stream = stream
        self._model_choices = [
            ("Qwen 2.5 (Ollama)", lambda: Ollama(id="qwen2.5:latest")),
            ("GPT-4o (OpenAI)", lambda: OpenAIChat(id="gpt-4o")),
        ]
        
        # Setup persistent file history
        os.makedirs(os.path.dirname(self.config.history_file), exist_ok=True)
        self.history = FileHistory(self.config.history_file)
        self.prompt_session = PromptSession(history=self.history)

    async def run_agent(self, message: str) -> None:
        """Run the agent with the given message."""

        # Create a custom callback to format the response with rich
        async def rich_formatter(content: str):
            if content.strip():
                md = Markdown(content)
                self.console.print(md)

        await self.agent.aprint_response(
            message,
            stream=self.stream,
            callback=rich_formatter,
            markdown=True,
            show_full_reasoning=True,
        )

    async def start(self) -> None:
        """Start the interactive CLI session."""

        # Show the main panel
        self.console.print(
            Panel.fit(
                f"[bold blue]{self.config.title}[/bold blue]\n"
                f"{self.config.subtitle}",
                title=self.config.agent_title,
                border_style=self.config.border_style_agent,
            )
        )

        try:
            while True:
                # Use HTML formatted prompt which is natively supported by prompt_toolkit
                prompt = f"\n<ansigreen><b>></b></ansigreen> "
                
                # Use prompt_toolkit to handle user input with history
                user_input = await self.prompt_session.prompt_async(
                    HTML(prompt),
                )
                
                if user_input.lower() in ["exit", "quit"]:
                    self.console.print("[italic]Ending conversation. Goodbye![/italic]")
                    break

                if user_input.strip():
                    await self.run_agent(user_input)
        except KeyboardInterrupt:
            self.console.print("\n[italic]Ending conversation. Goodbye![/italic]")
