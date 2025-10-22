"""IBM i Security Assistant Agent"""
from textwrap import dedent

from agno.agent import Agent
from agno.tools import tool
from agno.tools.reasoning import ReasoningTools

from db.factory import get_database
from db.ibmi import run_sql_statement
from utils.model_selector import get_model

# Security check SQL queries
sql = {
    "security_metrics": {
        "count_exposed_profiles": {
            "name": "Count Exposed User Profiles",
            "description": "How many *USRPRF's do not have *PUBLIC set to *EXCLUDE?",
            "sql": dedent(
                """
                SELECT COUNT(*)
                FROM qsys2.object_privileges
                WHERE system_object_schema = 'QSYS' AND object_type = '*USRPRF' AND object_name NOT IN ('QDBSHR',
                        'QDBSHRDO', 'QDOC', 'QTMPLPD') AND user_name = '*PUBLIC' AND object_authority <>
                        '*EXCLUDE'
                """
            ),
        },
        "list_exposed_profiles": {
            "name": "List Exposed User Profiles",
            "description": "Which *USRPRF's do not have *PUBLIC set to *EXCLUDE?",
            "sql": dedent(
                """
                SELECT object_name AS user_name, object_authority
                FROM qsys2.object_privileges
                WHERE system_object_schema = 'QSYS' AND object_type = '*USRPRF' AND object_name NOT IN ('QDBSHR',
                        'QDBSHRDO', 'QDOC', 'QTMPLPD') AND user_name = '*PUBLIC' AND object_authority <>
                        '*EXCLUDE'
                """
            ),
        },
        "fix_exposed_profiles": {
            "name": "Fix Exposed User Profiles",
            "description": "Which *USRPRF's do not have *PUBLIC set to *EXCLUDE? Include a query that corrects the exposure",
            "sql": dedent(
                """
                SELECT object_name AS user_name, object_authority,
                'SELECT qsys2.qcmdexc(''GRTOBJAUT OBJ(QSYS/' || object_name || ') OBJTYPE(*USRPRF) USER(*PUBLIC) AUT(*EXCLUDE)'') FROM sysibm.sysdummy1'
                    AS corrective_query
                FROM qsys2.object_privileges
                WHERE system_object_schema = 'QSYS' AND object_type = '*USRPRF' AND object_name NOT IN ('QDBSHR',
                        'QDBSHRDO', 'QDOC', 'QTMPLPD') AND user_name = '*PUBLIC' AND object_authority <>
                        '*EXCLUDE'
            """
            ),
        },
    }
}


def get_security_metrics_summary():
    """Get summary of available security metrics"""
    summary = {}
    for key, metric in sql["security_metrics"].items():
        summary[key] = {"name": metric["name"], "description": metric["description"]}
    return summary


@tool(
    name="count_exposed_profiles",
    description="Count how many user profiles don't have *PUBLIC set to *EXCLUDE",
    show_result=False,
    stop_after_tool_call=False,
)
def count_exposed_profiles() -> str:
    """Count the number of user profiles that don't have *PUBLIC set to *EXCLUDE"""
    return run_sql_statement(dedent(sql["security_metrics"]["count_exposed_profiles"]["sql"]))


@tool(
    name="list_exposed_profiles",
    description="List all user profiles that don't have *PUBLIC set to *EXCLUDE",
    show_result=False,
    stop_after_tool_call=False,
)
def list_exposed_profiles() -> str:
    """List all user profiles that don't have *PUBLIC set to *EXCLUDE"""
    return run_sql_statement(dedent(sql["security_metrics"]["list_exposed_profiles"]["sql"]))


@tool(
    name="fix_exposed_profiles",
    description="Generate corrective queries for user profiles that don't have *PUBLIC set to *EXCLUDE",
    show_result=False,
    stop_after_tool_call=False,
)
def fix_exposed_profiles() -> str:
    """Generate corrective queries for user profiles that don't have *PUBLIC set to *EXCLUDE"""
    return run_sql_statement(dedent(sql["security_metrics"]["fix_exposed_profiles"]["sql"]))


def get_security_assistant(
    model_id: str = "openai:gpt-4o",
    debug_mode: bool = False,
) -> Agent:
    """
    Create an IBM i Security Assistant agent.

    Args:
        model_id: Model specification (e.g., "openai:gpt-4o", "anthropic:claude-sonnet-4-5")
                  or a pre-configured model instance
        debug_mode: Enable debug logging

    Returns:
        Agent configured for IBM i security analysis
    """
    model = get_model(model_id)

    return Agent(
        id="security-assistant",
        name="IBM i Security Assistant",
        model=model,
        tools=[
            count_exposed_profiles,
            list_exposed_profiles,
            fix_exposed_profiles,
            ReasoningTools(add_instructions=True),
        ],
        dependencies={"security_metrics": get_security_metrics_summary()},
        add_dependencies_to_context=True,
        description=dedent("""\
            You are an IBM i Security expert. Assist users in analyzing security vulnerabilities
            and identifying potential security risks on their IBM i system.
        """),
        instructions=dedent(
            """\
            You are an IBM i Security expert. Assist users in analyzing security vulnerabilities
            and identifying potential security risks on their IBM i system.

            CRITICAL: NEVER call tools when users ask you to describe yourself, your capabilities,
            or what you can do. ONLY call tools when users ask for actual data from their system.

            Examples of when NOT to call tools:
            - "describe yourself" - Just explain your role, don't call any tools
            - "what can you do?" - List capabilities, don't call any tools
            - "what tools do you have?" - Describe tools, don't call any tools
            - "how do you work?" - Explain your process, don't call any tools
            - General security questions or best practices - Provide guidance, don't call tools

            Examples of when TO call tools:
            - "how many profiles are exposed?" - Call count_exposed_profiles
            - "show me the exposed profiles" - Call list_exposed_profiles
            - "fix the security issues" - Call fix_exposed_profiles
            - "analyze my system security" - Call appropriate tools to get actual data

            Available security metrics:
            - User profiles exposed to attack (not having *PUBLIC authority set to *EXCLUDE)
            - Detailed lists of vulnerable user profiles
            - Corrective measures for security vulnerabilities

            Available tools (use ONLY when actual system data is needed):
            - count_exposed_profiles: Count how many user profiles don't have *PUBLIC set to *EXCLUDE
            - list_exposed_profiles: List all user profiles that don't have *PUBLIC set to *EXCLUDE
            - fix_exposed_profiles: Generate corrective queries for user profiles that don't have *PUBLIC set to *EXCLUDE

            Decision process:
            1. Does the user want actual data from their system? → Call appropriate tool
            2. Does the user want to know about capabilities or general info? → Answer without calling tools
            3. Does the user want explanations or best practices? → Answer without calling tools

            When you do retrieve data from tools:
            - Look for exposed user profiles
            - Recommend corrective actions for security vulnerabilities
            - Explain the importance of proper security settings
            - Provide exact SQL commands to fix issues

            Always think before acting: "Does this question require me to get actual data from the user's system?"
            If NO, just answer the question. If YES, then call the appropriate tool.

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
