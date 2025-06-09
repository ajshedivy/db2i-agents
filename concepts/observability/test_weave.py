import weave
from agno.agent import Agent
from agno.models.ollama import Ollama

# Initialize Weave with your project name
weave.init("db2i-agents")

# Create and configure the agent
agent = Agent(model=Ollama(id="qwen2.5"), markdown=True, debug_mode=True)

# Define a function to run the agent, decorated with weave.op()
@weave.op()
def run(content: str):
    return agent.run(content)

# Use the function to log a model call
run("Share a 2 sentence horror story")