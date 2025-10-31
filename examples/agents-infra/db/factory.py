"""Database factory for agent storage configuration.

Provides database instances based on environment configuration:
- PostgreSQL for docker deployment (default)
- SQLite for CLI usage (when USE_SQLITE=true)
"""

import os
from typing import TYPE_CHECKING, Optional, Union

from agno.db.sqlite import SqliteDb

from agno.db.postgres import PostgresDb    
from agno.knowledge.knowledge import Knowledge


def get_database(db_id: str = "agno-storage") -> Union["PostgresDb", SqliteDb]:
    """
    Get database instance based on environment configuration.

    Args:
        db_id: Database identifier

    Returns:
        PostgresDb for docker deployment, SqliteDb for CLI

    Environment Variables:
        USE_SQLITE: Set to "true" to use SQLite instead of PostgreSQL
    """
    use_sqlite = os.getenv("USE_SQLITE", "").lower() == "true"

    if use_sqlite:
        # Use SQLite for local CLI
        db_path = os.getenv("SQLITE_DB_PATH", "tmp/agents.db")
        return SqliteDb(id=db_id, db_file=db_path, memory_table="agent_memories", metrics_table="agent_metrics")
    else:
        # Use PostgreSQL for docker deployment
        # Import here to avoid errors when PostgreSQL is not available
        from agno.db.postgres import PostgresDb
        from db.session import db_url

        return PostgresDb(id=db_id, db_url=db_url)


def get_knowledge_base(
    table_name: str = "knowledge",
    embedder_model: str = "text-embedding-3-small",
) -> Optional[Knowledge]:
    """
    Get knowledge base instance based on environment configuration.

    Knowledge bases with vector search require PostgreSQL with pgvector.
    Returns None when using SQLite (CLI mode).

    Args:
        table_name: Name of the vector database table
        embedder_model: OpenAI embedding model to use

    Returns:
        Knowledge instance for PostgreSQL, None for SQLite

    Environment Variables:
        USE_SQLITE: Set to "true" to disable knowledge base features
    """
    use_sqlite = os.getenv("USE_SQLITE", "").lower() == "true"

    if use_sqlite:
        # Knowledge base with vector search not available in SQLite mode
        return None
    else:
        # Import here to avoid errors when PostgreSQL is not available
        from agno.db.postgres import PostgresDb
        from agno.knowledge.embedder.openai import OpenAIEmbedder
        from agno.vectordb.pgvector import PgVector, SearchType
        from db.session import db_url

        return Knowledge(
            contents_db=PostgresDb(id="agno-storage", db_url=db_url),
            vector_db=PgVector(
                db_url=db_url,
                table_name=table_name,
                search_type=SearchType.hybrid,
                embedder=OpenAIEmbedder(id=embedder_model),
            ),
        )
