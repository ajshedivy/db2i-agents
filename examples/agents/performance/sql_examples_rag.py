from pathlib import Path
import os
from dotenv import load_dotenv, find_dotenv
from agno.agent import Agent
from agno.knowledge.markdown import MarkdownKnowledgeBase
from agno.vectordb.pgvector import PgVector
from agno.models.openai import OpenAIChat

load_dotenv(find_dotenv())
db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"


knowledge_base = MarkdownKnowledgeBase(
    path=Path("data/ACS insert from examples may28-2025.md"),  # Path to your markdown file(s)
    vector_db=PgVector(
        table_name="markdown_documents",
        db_url=db_url,
    ),
    num_documents=5,  # Number of documents to return on search
)

# Load the knowledge base
knowledge_base.load(recreate=False)

# Initialize the Assistant with the knowledge_base
agent = Agent(
    model=OpenAIChat(id="gpt-4o", api_key=os.getenv("OPENAI_API_KEY")),
    knowledge=knowledge_base,
    search_knowledge=True,
)

# Ask the agent about the documents in the knowledge base
agent.print_response(
    "What SQL statements can I use to monitor system performance?",
    markdown=True,
)