from textwrap import dedent
from typing import Any, Dict, Iterator, Optional

from agno.agent import Agent, RunResponse
from agno.models.openai import OpenAIChat
from agno.utils.log import logger
from agno.utils.pprint import pprint_run_response
from agno.workflow import Workflow
from dotenv import load_dotenv
import os
from mapepire_python import connect
from pep249 import QueryParameters, ResultSet
import json
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()

# Database connection credentials
credentials = {
    "host": os.getenv("HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("PASSWORD"),
    "port": os.getenv("DB_PORT"),
}


class SQLResponse(BaseModel):
    sql: str = Field(..., description="The SQL statement")
    description: str = Field(..., description="SQL description")
    result_set: ResultSet


class HealthReport(BaseModel):
    title: str = Field(..., description="Health Report")
    checks: list[SQLResponse]


def run_sql_statement(
    sql: str,
    parameters: Optional[QueryParameters] = None,
    creds: Dict[str, Any] = credentials,
) -> ResultSet:
    """Execute SQL statement and return formatted results

    Args:
        sql: SQL statement to execute
        parameters: Optional parameters for prepared statements
        creds: Database connection credentials

    Returns:
        Formatted string with SQL results
    """
    with connect(creds) as conn:
        with conn.execute(sql, parameters=parameters) as cur:
            if cur.has_results:
                result = cur.fetchall()
                return result["data"]
            else:
                return "SQL executed successfully. No results returned."


class HealthCheckWorkflow(Workflow):
    description: str = (
        "If any of these health checks fail, the user will not be able to understand how the IBM i got into its current state"
    )

    agent = Agent(
        model=OpenAIChat(api_key=os.getenv("OPENAI_API_KEY")),
        description=dedent(
            """
            Summarize the results sets from a collection of SQL health checks.
            """
        ),
        markdown=True,
    )

    file_path: str = "sql/health_checks.json"

    def run(self) -> RunResponse:
        checks = self.get_health_checks()

        agent_input = {"checks": checks}

        return self.agent.run(json.dumps(agent_input), stream=True)

    def get_health_checks(self, file_path: str = None):

        if not file_path:
            file_path = self.file_path

        result = []
        with open(file_path, "r") as f:
            data = json.load(f)

        for check in data["checks"]:
            run_check = run_sql_statement(check["sql"])
            if run_check:
                result.append(run_check)

        return result


if __name__ == "__main__":

    healthChecker = HealthCheckWorkflow(debug_mode=True)
    summary = healthChecker.run()
    pprint_run_response(summary)
