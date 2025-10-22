"""IBM i database connection utilities."""
import os
from typing import Any, Dict, Optional

from dotenv import load_dotenv, find_dotenv
from mapepire_python import connect
from pep249 import QueryParameters

# Load environment variables
load_dotenv(find_dotenv())


def get_ibmi_credentials() -> Dict[str, Any]:
    """
    Get IBM i database connection credentials from environment variables.

    Returns:
        Dict containing host, user, password, and port for IBM i connection
    """
    return {
        "host": os.getenv("HOST"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("PASSWORD"),
        "port": 8076,
    }


def run_sql_statement(
    sql: str,
    parameters: Optional[QueryParameters] = None,
    creds: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Execute SQL statement on IBM i and return formatted results.

    Args:
        sql: SQL statement to execute
        parameters: Optional parameters for prepared statements
        creds: Database connection credentials (defaults to environment credentials)

    Returns:
        Formatted string with SQL results or error message
    """
    if creds is None:
        creds = get_ibmi_credentials()

    with connect(creds) as conn:
        with conn.execute(sql, parameters=parameters) as cur:
            if cur.has_results:
                result = cur.fetchall()
                return str(result["data"])
            else:
                return "SQL executed successfully. No results returned."
