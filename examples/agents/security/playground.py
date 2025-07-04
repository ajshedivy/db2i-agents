from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.playground import Playground, serve_playground_app
from agent import profile_security_agent

agent_storage: str = "tmp/agents.db"

app = Playground(agents=[profile_security_agent]).get_app()

if __name__ == "__main__":
    serve_playground_app("playground:app", reload=True)