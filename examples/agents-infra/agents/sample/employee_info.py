"""Sample IBM i Employee Information Agent"""
from textwrap import dedent

from agno.agent import Agent
from agno.tools import tool

from db.factory import get_database
from db.ibmi import run_sql_statement
from utils.model_selector import get_model


@tool(
    name="fetch_employee_info",
    description="Get employee information for provided employee id",
    show_result=True,
    stop_after_tool_call=False
)
def get_employee(id: str) -> str:
    """
    Fetch employee information by employee ID.

    Args:
        id: Employee ID (e.g., '000010')

    Returns:
        str: Employee information including name, salary, department, etc.
    """
    return run_sql_statement(
        "select * from sample.employee where empno = ?",
        parameters=[id]
    )


def get_employee_info_agent(
    model_id: str = "openai:gpt-4o",
    debug_mode: bool = False,
) -> Agent:
    """
    Create a sample Employee Information agent.

    Args:
        model_id: Model specification (e.g., "openai:gpt-4o", "anthropic:claude-sonnet-4-5")
                  or a pre-configured model instance
        debug_mode: Enable debug logging

    Returns:
        Agent configured to query employee information
    """
    model = get_model(model_id)

    return Agent(
        id="employee-info",
        name="Employee Info Assistant",
        model=model,
        tools=[get_employee],
        description=dedent("""\
            You are a helpful assistant that can retrieve employee information from the SAMPLE database.
        """),
        instructions=dedent(
            """\
            You are a helpful assistant that can retrieve employee information from the SAMPLE database.

            When users ask about employees:
            - Use the fetch_employee_info tool with the employee ID
            - Provide clear summaries of employee data
            - Calculate totals when asked (e.g., total compensation = salary + bonus + commission)
            - Format currency values appropriately

            Be helpful and informative in your responses.

            Additional Information:
            - You are interacting with the user_id: {current_user_id}
            """
        ),
        # -*- Storage -*-
        db=get_database("agno-storage"),
        # -*- History -*-
        add_history_to_context=True,
        num_history_runs=3,
        # -*- Other settings -*-
        markdown=True,
        debug_mode=debug_mode,
    )
