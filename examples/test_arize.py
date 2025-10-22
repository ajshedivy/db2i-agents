import asyncio
import os

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from phoenix.otel import register
from dotenv import load_dotenv, find_dotenv

env = find_dotenv()
load_dotenv(env, override=True)
env = find_dotenv()

# Set environment variables for Arize Phoenix
os.environ["PHOENIX_CLIENT_HEADERS"] = f"api_key={os.getenv('PHOENIX_API_KEY')}"
os.environ["PHOENIX_COLLECTOR_ENDPOINT"] = "https://app.phoenix.arize.com"

# Configure the Phoenix tracer
tracer_provider = register(
  project_name="default",
  endpoint=os.getenv("PHOENIX_ENDPOINT"),
  auto_instrument=True
)

# Create and configure the agent
agent = Agent(
    name="Research Agent",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions="You are a research agent. Answer questions in the style of a professional researcher.",
    debug_mode=True,
)

# Use the agent
agent.print_response("Write a jokeabout cats")