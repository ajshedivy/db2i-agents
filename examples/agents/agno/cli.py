from dataclasses import dataclass
from typing import Optional

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt

from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.models.openai import OpenAIChat


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
    ):
        """Initialize the CLI with an agent and optional configuration."""
        self.agent = agent
        self.config = config or CLIConfig()
        self.console = console or Console()
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
            stream=True,
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
