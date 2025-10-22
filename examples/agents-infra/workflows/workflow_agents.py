"""
IBM i Performance Analysis Agents for Workflows

This module defines specialized agents used in workflow-based performance analysis.
Each agent has specific expertise optimized for workflow execution.
"""

from textwrap import dedent
from agno.agent import Agent
from agno.tools.reasoning import ReasoningTools

from utils.model_selector import get_model

# Import tools from migrated agents
from agents.performance.metrics_assistant import (
    get_metrics,
    get_collection_services_config,
    analyze_system_performance,
    get_metrics_summary
)


# ==================== WORKFLOW AGENTS ====================

def get_system_analyzer(model_id: str = "openai:gpt-4o") -> Agent:
    """
    Create System Resource Analyzer agent for workflows.

    Args:
        model_id: Model specification (e.g., "openai:gpt-4o", "anthropic:claude-sonnet-4-5")
                  or a pre-configured model instance

    Returns:
        Agent configured for system resource analysis
    """
    model = get_model(model_id)

    return Agent(
        name="System Resource Analyzer",
        model=model,
        tools=[
            get_metrics,
            analyze_system_performance,
            ReasoningTools()
        ],
        instructions=dedent("""
            You are an expert IBM i system resource analyst optimized for workflow execution. Focus on:

            **Core Responsibilities:**
            - Analyze CPU utilization patterns and identify bottlenecks
            - Evaluate memory pool efficiency and allocation
            - Monitor I/O performance and storage utilization
            - Identify resource contention issues

            **Analysis Approach:**
            - Gather comprehensive system status and activity metrics
            - Focus on resource utilization percentages and trends
            - Identify abnormal patterns or threshold breaches
            - Provide specific recommendations for optimization

            **Key Metrics to Monitor:**
            - CPU utilization (normal < 80%, critical > 90%)
            - Memory pool usage and thread allocation
            - System activity levels and job distribution
            - I/O wait times and storage performance

            **Workflow Integration:**
            - Provide concise, data-driven analysis suitable for workflow chaining
            - Structure output for easy consumption by downstream workflow steps
            - Focus on actionable findings that support decision-making

            Always provide context for your findings and actionable recommendations.
        """),
        dependencies={"performance_metrics": get_metrics_summary()},
        add_dependencies_to_context=True,
        markdown=True
    )


def get_report_generator(model_id: str = "openai:gpt-4o") -> Agent:
    """
    Create Performance Report Generator agent for workflows.

    Args:
        model_id: Model specification (e.g., "openai:gpt-4o", "anthropic:claude-sonnet-4-5")
                  or a pre-configured model instance

    Returns:
        Agent configured for performance report generation
    """
    model = get_model(model_id)

    return Agent(
        name="Performance Report Generator",
        model=model,
        tools=[ReasoningTools()],
        instructions=dedent("""
            You are an expert technical report writer specializing in IBM i system performance analysis
            within workflow-based analysis systems.

            **Report Structure Requirements:**
            1. **Executive Summary** - Key findings and critical issues
            2. **System Overview** - Current state and baseline metrics
            3. **Detailed Analysis** - Component-by-component breakdown
            4. **Issues & Recommendations** - Problems found with solutions
            5. **Performance Trends** - Pattern analysis and predictions
            6. **Action Items** - Prioritized recommendations with timelines

            **Writing Guidelines:**
            - Use clear, professional language suitable for both technical and management audiences
            - Include specific metrics and thresholds in findings
            - Prioritize recommendations by impact and urgency
            - Provide context for all performance metrics
            - Use formatting (headers, bullet points, tables) for readability

            **Quality Standards:**
            - Ensure all findings are backed by data from the analysis
            - Provide actionable recommendations with clear next steps
            - Include both immediate and long-term optimization strategies
            - Correlate findings across different system components

            **Workflow Integration:**
            - Synthesize inputs from multiple workflow steps
            - Structure reports for both human consumption and workflow processing
            - Provide summary data that can be used by downstream workflow decisions
            - Include workflow execution metadata and analysis quality metrics

            Generate comprehensive, well-structured performance reports that drive actionable insights
            and support automated workflow decision-making.
        """),
        markdown=True
    )


# Export agent factory functions
__all__ = [
    'get_system_analyzer',
    'get_report_generator',
]
