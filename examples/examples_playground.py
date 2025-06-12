from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.playground import Playground, serve_playground_app

from agents.performance.metrics_assistant_cli import performance_agent
from agents.security.agent import profile_security_agent
from agents.services.ifs.storage_assistant import storage_agent_simple
from agents.services.java.jvm_assistant import jvm_agent
from agents.services.ptf.get_ptf_info import ptf_agent
from agents.services.ptf.get_ptf_info_extended import ptf_extended_agent

model = OpenAIChat(id="gpt-4.1")

agents_list = [
    performance_agent,
    ptf_agent,
    ptf_extended_agent,
    storage_agent_simple,
    jvm_agent,
    profile_security_agent
]

# Apply model to all agents
for agent in agents_list:
    agent.model = model


agent_storage: str = "tmp/agents.db"

app = Playground(agents=agents_list).get_app()

if __name__ == "__main__":
    serve_playground_app("examples_playground:app", reload=True)