import weave
import requests
from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools import tool

# Initialize Weave with your project name
weave.init("db2i-agents")

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

# Create and configure the agent
agent = Agent(model=Ollama(id="qwen2.5"),tools=[get_weather], markdown=True, debug_mode=True)

# Define a function to run the agent, decorated with weave.op()
@weave.op()
def run(content: str):
    return agent.run(content)

# Use the function to log a model call
run("what is the weather like in Split, Croatia?")