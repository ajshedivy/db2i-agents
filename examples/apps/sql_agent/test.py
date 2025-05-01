from agno.agent import AgentKnowledge
from agno.embedder.ollama import OllamaEmbedder
from agno.vectordb.lancedb import LanceDb

embeddings = OllamaEmbedder().get_embedding(
    "The quick brown fox jumps over the lazy dog."
)

# Print the embeddings and their dimensions
print(f"Embeddings: {embeddings[:5]}")
print(f"Dimensions: {len(embeddings)}")

# Example usage:
knowledge_base = AgentKnowledge(
    vector_db=LanceDb(
        uri="tmp/testlancedb",
        table_name="ollama_embeddings",
        embedder=OllamaEmbedder(),
    ),
    num_documents=2,
)
