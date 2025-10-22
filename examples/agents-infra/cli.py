#!/usr/bin/env python3
"""
CLI for running agents-infra agents, teams, and workflows locally without Docker/PostgreSQL.

Usage:
    # List agents, teams, and workflows
    python cli.py --list-agents
    python cli.py --list-teams
    python cli.py --list-workflows

    # Run agents
    python cli.py --agent web-search
    python cli.py --agent metrics --model-id watsonx:mistralai/mistral-large --stream
    python cli.py --agent ptf --debug

    # Run teams
    python cli.py --team ptf-team
    python cli.py --team performance-routing --stream

    # Run workflows
    python cli.py --workflow quick-performance --input "Check system performance"
    python cli.py --workflow comprehensive-analysis --input "Analyze bottlenecks" --debug
"""

import argparse
import asyncio
import os
import sys
from pathlib import Path

# Set SQLite mode BEFORE importing any agents
# This prevents PostgreSQL import errors
os.environ["USE_SQLITE"] = "true"
os.environ["SQLITE_DB_PATH"] = str(Path(__file__).parent / "tmp" / "agents.db")

# Import agents, teams, and workflows with error handling for missing dependencies
# Items with missing dependencies will be excluded from the registry

from agno.workflow import Workflow

AGENTS = {}
TEAMS = {}
WORKFLOWS = {}

# Try importing each agent - skip if dependencies are missing
try:
    from agents.web_agent import get_web_agent

    AGENTS["web-search"] = {
        "factory": get_web_agent,
        "description": "Web search agent using DuckDuckGo",
        "name": "Web Search Agent",
    }
except ImportError as e:
    print(f"Warning: Skipping web-search agent - {e}", file=sys.stderr)

try:
    from agents.agno_assist import get_agno_assist

    AGENTS["agno-assist"] = {
        "factory": get_agno_assist,
        "description": "Agno framework documentation assistant (knowledge disabled in CLI mode)",
        "name": "Agno Assist",
    }
except ImportError as e:
    print(f"Warning: Skipping agno-assist agent - {e}", file=sys.stderr)

try:
    from agents.performance.metrics_assistant import get_metrics_assistant

    AGENTS["metrics"] = {
        "factory": get_metrics_assistant,
        "description": "IBM i performance metrics and monitoring",
        "name": "Performance Metrics Assistant",
    }
except ImportError as e:
    print(f"Warning: Skipping metrics agent - {e}", file=sys.stderr)

try:
    from agents.services.ptf.ptf_assistant import get_ptf_assistant

    AGENTS["ptf"] = {
        "factory": get_ptf_assistant,
        "description": "IBM i PTF (Program Temporary Fix) management",
        "name": "PTF Assistant",
    }
except ImportError as e:
    print(f"Warning: Skipping ptf agent - {e}", file=sys.stderr)

try:
    from agents.services.ifs.storage_assistant import get_storage_assistant

    AGENTS["storage"] = {
        "factory": get_storage_assistant,
        "description": "IBM i IFS storage analysis",
        "name": "Storage Assistant",
    }
except ImportError as e:
    print(f"Warning: Skipping storage agent - {e}", file=sys.stderr)

try:
    from agents.security.security_assistant import get_security_assistant

    AGENTS["security"] = {
        "factory": get_security_assistant,
        "description": "IBM i security analysis and recommendations",
        "name": "Security Assistant",
    }
except ImportError as e:
    print(f"Warning: Skipping security agent - {e}", file=sys.stderr)

try:
    from agents.sample.employee_info import get_employee_info_agent

    AGENTS["employee-info"] = {
        "factory": get_employee_info_agent,
        "description": "Sample employee information queries",
        "name": "Employee Info Agent",
    }
except ImportError as e:
    print(f"Warning: Skipping employee-info agent - {e}", file=sys.stderr)

# Ensure at least one agent loaded
if not AGENTS:
    print("Error: No agents could be loaded. Check dependencies.", file=sys.stderr)
    sys.exit(1)

# Try importing each team - skip if dependencies are missing
try:
    from teams.ibmi_teams import get_ptf_team

    TEAMS["ptf-team"] = {
        "factory": get_ptf_team,
        "description": "PTF specialist team for maintenance analysis",
        "name": "PTF Specialist Team",
    }
except ImportError as e:
    print(f"Warning: Skipping ptf-team - {e}", file=sys.stderr)

try:
    from teams.ibmi_teams import get_performance_routing_team

    TEAMS["performance-routing"] = {
        "factory": get_performance_routing_team,
        "description": "Routes performance questions to appropriate specialists",
        "name": "Performance Routing Team",
    }
except ImportError as e:
    print(f"Warning: Skipping performance-routing team - {e}", file=sys.stderr)

try:
    from teams.ibmi_teams import get_performance_coordination_team

    TEAMS["performance-coordination"] = {
        "factory": get_performance_coordination_team,
        "description": "Coordinated performance analysis across specialists",
        "name": "Performance Coordination Team",
    }
except ImportError as e:
    print(f"Warning: Skipping performance-coordination team - {e}", file=sys.stderr)

try:
    from teams.ibmi_teams import get_performance_collaboration_team

    TEAMS["performance-collaboration"] = {
        "factory": get_performance_collaboration_team,
        "description": "Full collaboration for comprehensive performance analysis",
        "name": "Performance Collaboration Team",
    }
except ImportError as e:
    print(f"Warning: Skipping performance-collaboration team - {e}", file=sys.stderr)

# Try importing each workflow - skip if dependencies are missing
try:
    from workflows.ibmi_workflows import get_quick_performance_workflow

    WORKFLOWS["quick-performance"] = {
        "factory": get_quick_performance_workflow,
        "description": "Fast performance overview with key system metrics",
        "name": "Quick Performance Check",
    }
except ImportError as e:
    print(f"Warning: Skipping quick-performance workflow - {e}", file=sys.stderr)

try:
    from workflows.ibmi_workflows import get_comprehensive_workflow

    WORKFLOWS["comprehensive-analysis"] = {
        "factory": get_comprehensive_workflow,
        "description": "Full performance analysis with quality checks",
        "name": "Comprehensive Analysis",
    }
except ImportError as e:
    print(f"Warning: Skipping comprehensive-analysis workflow - {e}", file=sys.stderr)

try:
    from workflows.ibmi_workflows import get_iterative_analysis_workflow

    WORKFLOWS["iterative-analysis"] = {
        "factory": get_iterative_analysis_workflow,
        "description": "Iterative performance analysis with refinement loops",
        "name": "Iterative Analysis",
    }
except ImportError as e:
    print(f"Warning: Skipping iterative-analysis workflow - {e}", file=sys.stderr)


def list_agents():
    """Print table of available agents."""
    print("\nAvailable Agents:")
    print("=" * 80)
    print(f"{'Agent ID':<25} {'Name':<35} {'Description'}")
    print("-" * 80)

    for agent_id, agent_info in sorted(AGENTS.items()):
        print(f"{agent_id:<25} {agent_info['name']:<35} {agent_info['description']}")

    print("=" * 80)
    print(f"\nTotal: {len(AGENTS)} agents available\n")


def list_teams():
    """Print table of available teams."""
    print("\nAvailable Teams:")
    print("=" * 80)
    print(f"{'Team ID':<25} {'Name':<35} {'Description'}")
    print("-" * 80)

    for team_id, team_info in sorted(TEAMS.items()):
        print(f"{team_id:<25} {team_info['name']:<35} {team_info['description']}")

    print("=" * 80)
    print(f"\nTotal: {len(TEAMS)} teams available\n")


def list_workflows():
    """Print table of available workflows."""
    print("\nAvailable Workflows:")
    print("=" * 80)
    print(f"{'Workflow ID':<25} {'Name':<35} {'Description'}")
    print("-" * 80)

    for workflow_id, workflow_info in sorted(WORKFLOWS.items()):
        print(
            f"{workflow_id:<25} {workflow_info['name']:<35} {workflow_info['description']}"
        )

    print("=" * 80)
    print(f"\nTotal: {len(WORKFLOWS)} workflows available\n")


def run_agent(agent_id: str, model_id: str, debug: bool, stream: bool):
    """
    Run the specified agent with given configuration.

    Args:
        agent_id: Agent identifier from AGENTS registry
        model_id: Model specification (e.g., "openai:gpt-4o")
        debug: Enable debug mode
        stream: Enable streaming responses
    """
    if agent_id not in AGENTS:
        print(f"Error: Unknown agent '{agent_id}'")
        print(f"Use --list-agents to see available agents")
        sys.exit(1)

    agent_info = AGENTS[agent_id]

    print(f"\n{'='*80}")
    print(f"Starting: {agent_info['name']}")
    print(f"Model: {model_id}")
    print(f"Storage: SQLite (tmp/agents.db)")
    print(f"Debug: {debug}")
    print(f"Stream: {stream}")
    print(f"{'='*80}\n")

    # Create agent instance
    agent = agent_info["factory"](
        model_id=model_id,
        debug_mode=debug,
    )

    # Run interactive CLI using Agno's built-in CLI
    agent.cli_app(markdown=True, stream=stream)


def run_team(team_id: str, model_id: str, debug: bool, stream: bool):
    """
    Run the specified team with given configuration.

    Args:
        team_id: Team identifier from TEAMS registry
        model_id: Model specification (e.g., "openai:gpt-4o")
        debug: Enable debug mode
        stream: Enable streaming responses
    """
    if team_id not in TEAMS:
        print(f"Error: Unknown team '{team_id}'")
        print(f"Use --list-teams to see available teams")
        sys.exit(1)

    team_info = TEAMS[team_id]

    print(f"\n{'='*80}")
    print(f"Starting: {team_info['name']}")
    print(f"Model: {model_id}")
    print(f"Storage: SQLite (tmp/agents.db)")
    print(f"Debug: {debug}")
    print(f"Stream: {stream}")
    print(f"{'='*80}\n")

    # Create team instance
    team = team_info["factory"](
        model_id=model_id,
        debug_mode=debug,
    )

    # Run interactive CLI using Agno's built-in CLI
    team.cli_app(markdown=True, stream=stream)


async def run_workflow(
    workflow_id: str, model_id: str, debug: bool, user_input: str, stream: bool = False
):
    """
    Run the specified workflow with given configuration.

    Args:
        workflow_id: Workflow identifier from WORKFLOWS registry
        model_id: Model specification (e.g., "openai:gpt-4o")
        debug: Enable debug mode
        user_input: User input/query for the workflow
    """
    if workflow_id not in WORKFLOWS:
        print(f"Error: Unknown workflow '{workflow_id}'")
        print(f"Use --list-workflows to see available workflows")
        sys.exit(1)

    workflow_info = WORKFLOWS[workflow_id]

    print(f"\n{'='*80}")
    print(f"Starting: {workflow_info['name']}")
    print(f"Model: {model_id}")
    print(f"Storage: SQLite (tmp/agents.db)")
    print(f"Debug: {debug}")
    print(f"Input: {user_input}")
    print(f"{'='*80}\n")

    # Create workflow instance
    workflow: Workflow = workflow_info["factory"](
        model_id=model_id,
        debug_mode=debug,
    )

    # Run workflow with user input
    await workflow.aprint_response(user_input, stream=stream)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="CLI for running agents-infra agents, teams, and workflows locally",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List all available agents, teams, and workflows
  python cli.py --list-agents
  python cli.py --list-teams
  python cli.py --list-workflows

  # Run an agent
  python cli.py --agent web-search
  python cli.py --agent metrics --model-id watsonx:mistralai/mistral-large --stream
  python cli.py --agent ptf --debug

  # Run a team
  python cli.py --team ptf-team
  python cli.py --team performance-routing --model-id anthropic:claude-sonnet-4-5
  python cli.py --team performance-collaboration --stream

  # Run a workflow
  python cli.py --workflow quick-performance --input "Check system performance"
  python cli.py --workflow comprehensive-analysis --input "Analyze performance bottlenecks"
  python cli.py --workflow iterative-analysis --input "Find and fix performance issues" --debug
        """,
    )

    parser.add_argument(
        "--agent",
        type=str,
        help="Agent to run (use --list-agents to see options)",
    )

    parser.add_argument(
        "--team",
        type=str,
        help="Team to run (use --list-teams to see options)",
    )

    parser.add_argument(
        "--workflow",
        type=str,
        help="Workflow to run (use --list-workflows to see options)",
    )

    parser.add_argument(
        "--prompt",
        type=str,
        help="Input/query for the workflow (required when using --workflow)",
    )

    parser.add_argument(
        "--model-id",
        type=str,
        default="openai:gpt-4o",
        help="Model specification (default: openai:gpt-4o). Format: provider:model",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode for verbose output",
    )

    parser.add_argument(
        "--stream",
        action="store_true",
        help="Enable streaming responses",
    )

    parser.add_argument(
        "--list-agents",
        action="store_true",
        help="List all available agents and exit",
    )

    parser.add_argument(
        "--list-teams",
        action="store_true",
        help="List all available teams and exit",
    )

    parser.add_argument(
        "--list-workflows",
        action="store_true",
        help="List all available workflows and exit",
    )

    args = parser.parse_args()

    # Handle --list-agents
    if args.list_agents:
        list_agents()
        sys.exit(0)

    # Handle --list-teams
    if args.list_teams:
        list_teams()
        sys.exit(0)

    # Handle --list-workflows
    if args.list_workflows:
        list_workflows()
        sys.exit(0)

    # Count how many run modes are specified
    run_modes = sum([bool(args.agent), bool(args.team), bool(args.workflow)])

    # Ensure --agent, --team, and --workflow are mutually exclusive
    if run_modes > 1:
        parser.print_help()
        print(
            "\nError: --agent, --team, and --workflow are mutually exclusive. Choose one."
        )
        sys.exit(1)

    # Require either --agent, --team, or --workflow
    if run_modes == 0:
        parser.print_help()
        print("\nError: One of --agent, --team, or --workflow is required")
        print("       (or use --list-agents / --list-teams / --list-workflows)")
        sys.exit(1)

    # Validate --workflow requires --input
    if args.workflow and not args.input:
        parser.print_help()
        print("\nError: --workflow requires --input to specify the workflow query")
        sys.exit(1)

    # Ensure tmp directory exists for SQLite database
    tmp_dir = Path(__file__).parent / "tmp"
    tmp_dir.mkdir(exist_ok=True)

    # Run the agent, team, or workflow
    try:
        if args.agent:
            run_agent(
                agent_id=args.agent,
                model_id=args.model_id,
                debug=args.debug,
                stream=args.stream,
            )
        elif args.team:
            run_team(
                team_id=args.team,
                model_id=args.model_id,
                debug=args.debug,
                stream=args.stream,
            )
        elif args.workflow:
            asyncio.run(
                run_workflow(
                    workflow_id=args.workflow,
                    model_id=args.model_id,
                    debug=args.debug,
                    user_input=args.prompt,
                    stream=args.stream,
                )
            )
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        if args.debug:
            raise
        sys.exit(1)


if __name__ == "__main__":
    main()
