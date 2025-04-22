from dataclasses import dataclass
from typing import Optional

from dotenv import dotenv_values

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt

from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.models.openai import OpenAIChat
from agno.models.base import Model
from agno.models.ibm import WatsonX


def get_model(provider: str, model_id: str = None) -> Model:
    env = dotenv_values()
    match provider:
        case "ollama":
            ollama_model = model_id if model_id else "qwen2.5:latest"
            return Ollama(id=ollama_model)
        case "openai":
            openai_model = (
                model_id if model_id and model_id.startswith("gpt") else "gpt-4o"
            )
            if env.get("OPENAI_API_KEY") is not None:
                return OpenAIChat(id=openai_model)
        case "watsonx":
            watsonx_model = env.get("IBM_WATSONX_MODEL_ID")

            return WatsonX(
                id=watsonx_model,
                url=env.get("IBM_WATSONX_BASE_URL"),
                api_key=env.get("IBM_WATSONX_API_KEY"),
                project_id=env.get("IBM_WATSONX_PROJECT_ID"),
            )
        case _:
            return Ollama(id="qwen2.5:latest")


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

        # Then show the main panel
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
                user_input = Prompt.ask(
                    f"\n[bold {self.config.border_style_user}]{self.config.prompt_text}[/bold {self.config.border_style_user}]"
                )
                if user_input.lower() in ["exit", "quit"]:
                    self.console.print("[italic]Ending conversation. Goodbye![/italic]")
                    break

                if user_input.strip():
                    await self.run_agent(user_input)
        except KeyboardInterrupt:
            self.console.print("\n[italic]Ending conversation. Goodbye![/italic]")
