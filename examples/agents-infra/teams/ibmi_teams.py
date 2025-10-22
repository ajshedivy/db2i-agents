"""
IBM i Teams Configuration for AgentOS

This module defines team configurations for IBM i system management,
demonstrating various collaboration patterns including routing, coordination,
and collaboration modes.
"""
from pathlib import Path
from textwrap import dedent

from agno.team import Team

from db.factory import get_database
from utils.model_selector import get_model

# Import agent factory functions
from agents.performance.metrics_assistant import get_metrics_assistant
from agents.services.ptf.ptf_assistant import get_ptf_assistant
from agents.services.ifs.storage_assistant import get_storage_assistant
from agents.security.security_assistant import get_security_assistant



# ==================== TEAM FACTORY FUNCTIONS ====================

def get_ptf_team(
    model_id: str = "openai:gpt-4o",
    debug_mode: bool = False,
) -> Team:
    """
    Create a PTF Specialist Team that routes to appropriate PTF specialists.

    Args:
        model_id: Model specification (e.g., "openai:gpt-4o", "anthropic:claude-sonnet-4-5")
                  or a pre-configured model instance
        debug_mode: Enable debug logging

    Returns:
        Team configured for PTF analysis and maintenance
    """
    model = get_model(model_id)

    # Create PTF agent instances for the team
    ptf_assistant = get_ptf_assistant(model_id=model_id, debug_mode=debug_mode)

    return Team(
        name="PTF Specialist Team",
        model=model,
        members=[ptf_assistant],
        description="Team specializing in PTF analysis and maintenance",
        instructions=dedent(
            """
            You are a team of IBM i PTF specialists. Route requests to the right specialist based on intent:

            Specialists:
            - PTF Assistant: Checks PTF currency and identifies missing PTFs for PTF groups.
              Use when users ask about: "Are we current?", "What maintenance is available?",
              "Are there missing PTFs?", or specific PTF group queries.

            Routing rules:
            - If the user mentions a specific PTF group name/ID → route to PTF Assistant
            - If the user asks about general PTF status/currency → route to PTF Assistant
            - If unclear, ask: "Do you want to check PTF currency or look for missing PTFs in a specific group?"

            Responses should:
            - State current status and any missing/available updates
            - Highlight critical/security items
            - Note prerequisites, IPL considerations, and next steps
            """
        ),
        db=get_database("agno-storage"),
        enable_user_memories=True,
        enable_agentic_memory=True,
        show_members_responses=True,
        stream_intermediate_steps=True,
        markdown=True,
        debug_mode=debug_mode,
    )


def get_performance_routing_team(
    model_id: str = "openai:gpt-4o",
    debug_mode: bool = False,
) -> Team:
    """
    Create a Performance Routing Team that directs questions to appropriate specialists.

    Args:
        model_id: Model specification (e.g., "openai:gpt-4o", "anthropic:claude-sonnet-4-5")
                  or a pre-configured model instance
        debug_mode: Enable debug logging

    Returns:
        Team configured to route performance questions
    """
    model = get_model(model_id)

    # Create agent instances
    metrics_assistant = get_metrics_assistant(model_id=model_id, debug_mode=debug_mode)
    ptf_team = get_ptf_team(model_id=model_id, debug_mode=debug_mode)
    storage_assistant = get_storage_assistant(model_id=model_id, debug_mode=debug_mode)
    security_assistant = get_security_assistant(model_id=model_id, debug_mode=debug_mode)

    return Team(
        name="IBM i Performance Routing Team",
        model=model,
        members=[
            metrics_assistant,
            ptf_team,
            storage_assistant,
            security_assistant,
        ],
        description="Smart routing team that directs performance questions to the most appropriate specialist",
        instructions=dedent(
            """
            Analyze the user's request and route to the most appropriate specialist:

            - Metrics Assistant: CPU, memory, I/O, system metrics, job performance, Collection Services
            - PTF Specialist Team: Missing PTFs, maintenance, security updates, system patches
            - Storage Assistant: IFS files, disk usage, storage optimization, file cleanup
            - Security Assistant: User profile security, exposed profiles, vulnerability analysis

            Route to the single most relevant specialist based on the primary focus of the request.
            If the request spans multiple domains, route to the Metrics Assistant as the primary coordinator.
            """
        ),
        db=get_database("agno-storage"),
        enable_user_memories=True,
        enable_agentic_memory=True,
        show_members_responses=True,
        stream_intermediate_steps=True,
        markdown=True,
        debug_mode=debug_mode,
    )


def get_performance_coordination_team(
    model_id: str = "openai:gpt-4o",
    debug_mode: bool = False,
) -> Team:
    """
    Create a Performance Coordination Team that orchestrates multiple specialists.

    Args:
        model_id: Model specification (e.g., "openai:gpt-4o", "anthropic:claude-sonnet-4-5")
                  or a pre-configured model instance
        debug_mode: Enable debug logging

    Returns:
        Team configured to coordinate comprehensive system analysis
    """
    model = get_model(model_id)

    # Create agent instances
    metrics_assistant = get_metrics_assistant(model_id=model_id, debug_mode=debug_mode)
    ptf_assistant = get_ptf_assistant(model_id=model_id, debug_mode=debug_mode)
    storage_assistant = get_storage_assistant(model_id=model_id, debug_mode=debug_mode)
    security_assistant = get_security_assistant(model_id=model_id, debug_mode=debug_mode)

    return Team(
        name="IBM i Performance Coordination Team",
        model=model,
        members=[
            metrics_assistant,
            ptf_assistant,
            storage_assistant,
            security_assistant,
        ],
        description="Coordinates multiple specialists to provide comprehensive system analysis",
        instructions=dedent(
            """
            You are the team leader coordinating a comprehensive IBM i system analysis.

            **Coordination Strategy:**
            1. Start with Metrics Assistant for overall system baseline
            2. Engage PTF Assistant for maintenance status assessment
            3. Involve Storage Assistant for disk and file system analysis
            4. Include Security Assistant for security vulnerability assessment

            **Delegation Guidelines:**
            - Assign specialists based on their expertise domains
            - Coordinate parallel analysis when appropriate
            - Ensure comprehensive coverage of all system aspects
            - Synthesize specialist findings into cohesive recommendations

            Provide integrated analysis with actionable recommendations.
            """
        ),
        db=get_database("agno-storage"),
        enable_user_memories=True,
        enable_agentic_memory=True,
        add_history_to_context=True,
        num_history_runs=3,
        show_members_responses=True,
        markdown=True,
        debug_mode=debug_mode,
    )


def get_performance_collaboration_team(
    model_id: str = "openai:gpt-4o",
    debug_mode: bool = False,
) -> Team:
    """
    Create a Performance Collaboration Team where all specialists work simultaneously.

    Args:
        model_id: Model specification (e.g., "openai:gpt-4o", "anthropic:claude-sonnet-4-5")
                  or a pre-configured model instance
        debug_mode: Enable debug logging

    Returns:
        Team configured for collaborative analysis
    """
    model = get_model(model_id)

    # Create agent instances
    metrics_assistant = get_metrics_assistant(model_id=model_id, debug_mode=debug_mode)
    ptf_assistant = get_ptf_assistant(model_id=model_id, debug_mode=debug_mode)
    storage_assistant = get_storage_assistant(model_id=model_id, debug_mode=debug_mode)
    security_assistant = get_security_assistant(model_id=model_id, debug_mode=debug_mode)

    return Team(
        name="IBM i Performance Collaboration Team",
        model=model,
        members=[
            metrics_assistant,
            storage_assistant,
            ptf_assistant,
            security_assistant,
        ],
        description="All specialists collaborate simultaneously on performance analysis",
        instructions=dedent(
            """
            All team members will analyze the same performance question from their specialized perspectives.

            **Collaboration Approach:**
            - Each specialist provides analysis from their domain expertise
            - All perspectives are gathered simultaneously for comprehensive coverage
            - The team leader synthesizes all inputs into unified recommendations

            **Expected Specialist Contributions:**
            - Metrics Assistant: System metrics and bottleneck analysis
            - Storage Assistant: Storage-related performance impacts
            - PTF Assistant: Missing fixes that might affect performance
            - Security Assistant: Security configurations affecting performance

            Synthesize all specialist inputs into cohesive, prioritized recommendations.
            """
        ),
        db=get_database("agno-storage"),
        enable_user_memories=True,
        enable_agentic_memory=True,
        add_history_to_context=True,
        num_history_runs=3,
        show_members_responses=True,
        markdown=True,
        debug_mode=debug_mode,
    )


# Export all team factory functions
__all__ = [
    'get_ptf_team',
    'get_performance_routing_team',
    'get_performance_coordination_team',
    'get_performance_collaboration_team',
    'get_team_memory',
]
