import os
from textwrap import dedent
from typing import Any, Dict, Optional

from mapepire_python import connect
from pep249 import QueryParameters
from agno.tools import tool
from agno.agent import Agent
from agno.models.anthropic import Claude

credentials = {
    "host": os.getenv("HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("PASSWORD"),
    "port": os.getenv("DB_PORT"),
}

system_status = "SELECT * FROM TABLE(QSYS2.SYSTEM_STATUS(RESET_STATISTICS=>'YES',DETAILED_INFO=>'ALL')) X"

system_activity = "SELECT * FROM TABLE(QSYS2.SYSTEM_ACTIVITY_INFO())"


@tool(
    name="Get System Status",
    description="Retrieve overall system performance statistics",
)
def get_system_status() -> str:
    """Retrieve overall system performance statistics"""
    return run_sql_statement(system_status)


@tool(
    name="Get System Activity",
    description="Retrieve current system activity information",
)
def get_system_activity() -> str:
    """Retrieve current system activity information"""
    return run_sql_statement(system_activity)


def run_sql_statement(
    sql: str,
    parameters: Optional[QueryParameters] = None,
    creds: Dict[str, Any] = credentials,
) -> str:
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
                return str(result["data"])
            else:
                return "SQL executed successfully. No results returned."
            
            
import smtplib
from email.mime.text import MIMEText

# @tool(
#     name="Send Email Report",
#     description="Send a performance report via email",
# )
def send_email_report(recipient: str, subject: str, body: str) -> str:
    """Send an email with the specified content"""
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = "ajshedivyaj@gmail.com"
    msg['To'] = recipient
    
    with smtplib.SMTP(os.getenv("SMTP_SERVER")) as server:
        server.send_message(msg)
    return f"Email sent successfully to {recipient}"


agent = Agent(
    name="Performance Metrics Assistant",
    model=Claude(id="claude-sonnet-4-20250514"),
    tools=[
        get_system_status,
        get_system_activity,
    ],
    instructions=dedent("""
        You are an expert IBM i performance metrics assistant. Your role is to help users 
        retrieve and analyze performance-related data from the IBM i system using SQL queries.
    """),
    markdown=True,
)

send_email_report(recipient="ajshedivyaj@gmail.com", subject="Test Report", body="This is a test email from the Performance Metrics Assistant.")
