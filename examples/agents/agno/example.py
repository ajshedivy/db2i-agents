import asyncio
from agno.agent import Agent
from agno.models.ollama import Ollama
from utils.cli import InteractiveCLI, CLIConfig

async def main():
    # Create a simple agent with Ollama
    agent = Agent(
        model=Ollama(id="qwen2.5:latest"),
        instructions="You are a helpful cooking assistant who specializes in recipes and culinary advice.",
        markdown=True,
        add_history_to_messages=True,
    )
    
    # Configure the CLI with custom settings
    config = CLIConfig(
        title="Cooking Assistant",
        subtitle="Ask for recipe ideas and cooking advice. Type 'exit' or 'quit' to end.",
        prompt_text="🍳>",
        agent_title="Chef",
        user_title="Hungry User",
        border_style_agent="red",
        border_style_user="green",
    )
    
    # Create and start the CLI
    cli = InteractiveCLI(agent=agent, config=config)
    await cli.start()

if __name__ == "__main__":
    asyncio.run(main())