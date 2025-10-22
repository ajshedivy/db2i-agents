"""IBM i PTF (Program Temporary Fix) Assistant Agent"""
from textwrap import dedent

from agno.agent import Agent
from agno.tools import tool

from db.factory import get_database
from db.ibmi import run_sql_statement
from utils.model_selector import get_model

# Known PTF Groups for IBM i
ptf_groups = {
    "SF99675": "HARDWARE AND RELATED PTFS",
    "SF99668": "IBM DB2 MIRROR FOR I",
    "SF99667": "740 TCP/IP PTF",
    "SF99737": "TECHNOLOGY REFRESH",
    "SF99666": "HIGH AVAILABILITY FOR IBM I",
    "SF99661": "WEBSPHERE APP SERVER V8.5",
    "SF99739": "GROUP HIPER",
    "SF99662": "IBM HTTP SERVER FOR I",
    "SF99704": "DB2 FOR IBM I",
    "SF99665": "JAVA",
    "SF99663": "PERFORMANCE TOOLS",
    "SF99738": "GROUP SECURITY",
    "SF99664": "BACKUP RECOVERY SOLUTIONS",
    "SF99225": "Open Source"
}

# SQL query to check PTF currency
ptf_currency = dedent(
    """
    With iLevel(iVersion, iRelease) AS
    (
    select OS_VERSION, OS_RELEASE from sysibmadm.env_sys_info
    )
    SELECT P.*
        FROM iLevel, systools.group_ptf_currency P
        WHERE ptf_group_release =
            'R' CONCAT iVersion CONCAT iRelease concat '0'
        ORDER BY ptf_group_level_available -
            ptf_group_level_installed DESC
    """
)

# SQL query to check missing PTFs
missing_ptfs = dedent(
    """
    SELECT *
    FROM TABLE(systools.group_ptf_details(?)) a
        WHERE PTF_STATUS = 'PTF MISSING'
    """
)


@tool(
    name="get_ptf_currency_info",
    description="Derive the IBM i operating system level and then determine the level of currency of PTF Groups",
    show_result=False,
    stop_after_tool_call=False
)
def get_ptf_currency() -> str:
    """Get PTF currency information for the IBM i system"""
    return run_sql_statement(sql=ptf_currency)


@tool(
    name="get_missing_ptf_info",
    description="Determine if this IBM i is missing any PTFs for a specific PTF group",
    show_result=False,
    stop_after_tool_call=False,
)
def get_missing_ptfs(name: str) -> str:
    """
    Determine if this IBM i is missing any PTFs.

    Args:
        name: PTF group name (e.g., SF99737 for Technology Refresh)

    Returns:
        str: List of missing PTFs or confirmation that all are installed
    """
    if name not in ptf_groups.keys():
        return f"PTF name: {name} not valid. Valid PTF groups are: {', '.join(ptf_groups.keys())}"

    return run_sql_statement(sql=missing_ptfs, parameters=[name])


def get_ptf_assistant(
    model_id: str = "openai:gpt-4o",
    debug_mode: bool = False,
) -> Agent:
    """
    Create an IBM i PTF Assistant agent.

    Args:
        model_id: Model specification (e.g., "openai:gpt-4o", "anthropic:claude-sonnet-4-5")
                  or a pre-configured model instance
        debug_mode: Enable debug logging

    Returns:
        Agent configured for IBM i PTF management
    """
    model = get_model(model_id)

    return Agent(
        id="ptf-assistant",
        name="IBM i PTF Assistant",
        model=model,
        tools=[get_ptf_currency, get_missing_ptfs],
        dependencies={"ptf_groups": ptf_groups},
        add_dependencies_to_context=True,
        description=dedent("""\
            You are an IBM i PTF (Program Temporary Fix) Assistant. Help users check for missing PTFs,
            understand PTF currency, and maintain their IBM i system with the latest fixes.
        """),
        instructions=dedent(
            """\
            You are an IBM i PTF assistant. Help users check for missing PTFs
            (Program Temporary Fixes) on their system and understand their PTF currency.

            Available PTF Groups to check:
            {ptf_groups}

            When asked about PTF currency:
            - Use get_ptf_currency_info to check overall PTF group currency
            - This shows which PTF groups have updates available

            When asked about missing PTFs:
            - Use get_missing_ptf_info with the appropriate PTF group code
            - Explain findings clearly with relevant PTF details
            - Provide recommendations for installing missing PTFs

            Important PTF Groups:
            - SF99737: Technology Refresh - Important system updates
            - SF99739: GROUP HIPER - High-impact pervasive fixes
            - SF99738: GROUP SECURITY - Security-related fixes
            - SF99704: DB2 FOR IBM I - Database fixes
            - SF99225: Open Source - Open source package fixes

            Additional Information:
            - You are interacting with the user_id: {current_user_id}
            - The user's name might be different from the user_id, you may ask for it if needed.
            """
        ),
        # -*- Storage -*-
        db=get_database("agno-storage"),
        # -*- History -*-
        add_history_to_context=True,
        num_history_runs=3,
        read_chat_history=True,
        # -*- Memory -*-
        enable_agentic_memory=True,
        # -*- Other settings -*-
        markdown=True,
        add_datetime_to_context=True,
        debug_mode=debug_mode,
    )
