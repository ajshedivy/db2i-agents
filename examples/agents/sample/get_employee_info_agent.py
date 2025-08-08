import os

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools import tool
from dotenv import load_dotenv, find_dotenv
from mapepire_python import connect

load_dotenv(find_dotenv())

credentials = {
    "host": os.getenv("HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("PASSWORD"),
    "port": os.getenv("DB_PORT"),
}


@tool(
    name="fetch_employee_info",
    description="Get employee information for provided employee id",
    show_result=True,
    stop_after_tool_call=False
)
def get_employee(id: str) -> str:
    with connect(credentials) as conn:
        with conn.execute(
            "select * from sample.employee where empno = ?", parameters=[id]
        ) as cur:
            if cur.has_results:
                result = cur.fetchall()
                return str(result["data"])
            else:
                return f"No Data found for employee: {id}"


agent = Agent(
    model=OpenAIChat(id="gpt-4o", api_key=os.getenv("OPENAI_API_KEY")),
    tools=[get_employee],
    markdown=True,
    debug_mode=False
)
agent.print_response("What is the total compensation of employee 000010?", stream=True)
