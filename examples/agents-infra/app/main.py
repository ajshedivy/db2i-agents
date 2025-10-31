"""AgentOS for IBM i Db2 Agents"""

import asyncio
import os
from pathlib import Path

# Ensure PostgreSQL is used for AgentOS (not SQLite)
os.environ["USE_SQLITE"] = "false"

from agno.os import AgentOS

from agents.agno_assist import get_agno_assist
from agents.web_agent import get_web_agent
from agents.performance.metrics_assistant import get_metrics_assistant
from agents.services.ptf.ptf_assistant import get_ptf_assistant
from agents.services.ifs.storage_assistant import get_storage_assistant
from agents.security.security_assistant import get_security_assistant
from agents.sample.employee_info import get_employee_info_agent
from teams.ibmi_teams import (
    get_ptf_team,
    get_performance_routing_team,
    get_performance_coordination_team,
    get_performance_collaboration_team,
)
from workflows.ibmi_workflows import (
    get_quick_performance_workflow,
    get_comprehensive_workflow,
    get_iterative_analysis_workflow,
)

from utils.model_selector import COMMON_MODELS

os_config_path = str(Path(__file__).parent.joinpath("config.yaml"))

# Default model specification to use for all agents/teams/workflows
DEFAULT_MODEL = COMMON_MODELS['claude4-5']  # "anthropic:claude-sonnet-4-5"

# Create demo agents
web_agent = get_web_agent(model_id=DEFAULT_MODEL)
agno_assist = get_agno_assist(model_id=DEFAULT_MODEL)

# Create IBM i agents
metrics_assistant = get_metrics_assistant(model_id=DEFAULT_MODEL)
ptf_assistant = get_ptf_assistant(model_id=DEFAULT_MODEL)
storage_assistant = get_storage_assistant(model_id=DEFAULT_MODEL)
security_assistant = get_security_assistant(model_id=DEFAULT_MODEL)
employee_info = get_employee_info_agent(model_id=DEFAULT_MODEL)

# Create IBM i teams
ptf_team = get_ptf_team(model_id=DEFAULT_MODEL)
performance_routing_team = get_performance_routing_team(model_id=DEFAULT_MODEL)
performance_coordination_team = get_performance_coordination_team(
    model_id=DEFAULT_MODEL
)
performance_collaboration_team = get_performance_collaboration_team(
    model_id=DEFAULT_MODEL
)

# Create IBM i workflows
quick_performance_workflow = get_quick_performance_workflow(model_id=DEFAULT_MODEL)
comprehensive_workflow = get_comprehensive_workflow(model_id=DEFAULT_MODEL)
iterative_analysis_workflow = get_iterative_analysis_workflow(model_id=DEFAULT_MODEL)

# Create the AgentOS
agent_os = AgentOS(
    os_id="db2i-agentos",
    agents=[
        # Demo agents
        web_agent,
        agno_assist,
        # IBM i Performance agents
        metrics_assistant,
        # IBM i Service agents
        ptf_assistant,
        storage_assistant,
        # IBM i Security agents
        security_assistant,
        # Sample agents
        employee_info,
    ],
    teams=[
        # IBM i Teams
        ptf_team,
        performance_routing_team,
        performance_coordination_team,
        performance_collaboration_team,
    ],
    workflows=[
        # IBM i Workflows
        quick_performance_workflow,
        comprehensive_workflow,
        iterative_analysis_workflow,
    ],
    # Configuration for the AgentOS
    config=os_config_path,
    enable_mcp=True,
)
app = agent_os.get_app()

if __name__ == "__main__":
    # Add knowledge to Agno Assist agent
    asyncio.run(
        agno_assist.knowledge.add_content_async(  # type: ignore
            name="Agno Docs",
            url="https://docs.agno.com/llms-full.txt",
        )
    )
    # Simple run to generate and record a session
    agent_os.serve(app="main:app", reload=True)
