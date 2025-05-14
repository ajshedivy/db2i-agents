import random
import os
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools import tool
from dotenv import load_dotenv
import requests

load_dotenv()


@tool(show_result=True, stop_after_tool_call=True)
def get_weather(city: str) -> str:
    """Return current conditions from wttr.in in plain English."""

    url = f"https://wttr.in/{city}?format=j1"

    response = requests.get(url, timeout=10)

    data = response.json()
    cond = data["current_condition"][0]
    temp_f = cond["temp_F"]
    desc = cond["weatherDesc"][0]["value"]

    result = f"{temp_f} °F, {desc} in {city.capitalize()}"
    return result


agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY")),
    tools=[get_weather],
    markdown=True,
)
agent.print_response("What is the weather in Rochester MN?", stream=True)