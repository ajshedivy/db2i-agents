"""
IBM i Performance Analysis Workflows for AgentOS

This module defines workflow configurations for IBM i performance analysis,
demonstrating various workflow patterns including sequential, parallel, loop,
and conditional execution.
"""

from agno.workflow import Step, Workflow, Loop

from db.factory import get_database
from workflows.workflow_agents import get_system_analyzer, get_report_generator
from workflows.workflow_functions import (
    performance_data_processor,
    quality_assurance_check,
    comprehensive_quality_check,
)


# ==================== WORKFLOW FACTORY FUNCTIONS ====================

def get_quick_performance_workflow(
    model_id: str = "gpt-4o",
    debug_mode: bool = False,
) -> Workflow:
    """
    Create a Quick Performance Check Workflow.

    Args:
        model_id: The model to use for workflow agents
        debug_mode: Enable debug logging

    Returns:
        Workflow for fast performance overview
    """
    # Create agent instances
    system_analyzer = get_system_analyzer(model_id=model_id)
    report_generator = get_report_generator(model_id=model_id)

    return Workflow(
        name="Quick IBM i Performance Check",
        description="Fast performance overview with key system metrics",
        steps=[
            Step(name="System Status Check", agent=system_analyzer),
            # Step(name="Generate Quick Report", agent=report_generator),
        ],
        db=get_database("agno-storage"),
        debug_mode=debug_mode,
    )


def get_comprehensive_workflow(
    model_id: str = "gpt-4o",
    debug_mode: bool = False,
) -> Workflow:
    """
    Create a Comprehensive Performance Analysis Workflow.

    Args:
        model_id: The model to use for workflow agents
        debug_mode: Enable debug logging

    Returns:
        Workflow for complete system performance analysis
    """
    # Create agent instances
    system_analyzer = get_system_analyzer(model_id=model_id)
    report_generator = get_report_generator(model_id=model_id)

    return Workflow(
        name="Comprehensive IBM i Performance Analysis",
        description="Complete system performance analysis with detailed reporting",
        steps=[
            # Phase 1: System analysis
            Step(name="System Resource Analysis", agent=system_analyzer),

            # Phase 2: Data processing and quality check
            Step(
                name="Performance Data Processing",
                executor=performance_data_processor,
                description="Process and consolidate performance analysis data"
            ),

            # Phase 3: Report generation with quality loop
            Loop(
                name="Quality Report Generation",
                steps=[Step(name="Generate Performance Report", agent=report_generator)],
                end_condition=comprehensive_quality_check,
                max_iterations=2
            ),
        ],
        db=get_database("agno-storage"),
        debug_mode=debug_mode,
    )


def get_iterative_analysis_workflow(
    model_id: str = "gpt-4o",
    debug_mode: bool = False,
) -> Workflow:
    """
    Create an Iterative Quality-Driven Workflow.

    Args:
        model_id: The model to use for workflow agents
        debug_mode: Enable debug logging

    Returns:
        Workflow that iterates until analysis standards are met
    """
    # Create agent instances
    system_analyzer = get_system_analyzer(model_id=model_id)
    report_generator = get_report_generator(model_id=model_id)

    return Workflow(
        name="Iterative IBM i Performance Analysis",
        description="Quality-driven workflow that iterates until analysis standards are met",
        steps=[
            # Initial assessment
            Step(name="Baseline Assessment", agent=system_analyzer),

            # Quality-driven analysis loop
            Loop(
                name="Analysis Refinement Loop",
                steps=[
                    Step(name="System Analysis", agent=system_analyzer),
                    Step(
                        name="Analysis Processing",
                        executor=performance_data_processor,
                        description="Process and evaluate analysis quality"
                    )
                ],
                end_condition=comprehensive_quality_check,
                max_iterations=3
            ),

            # Final comprehensive report
            Step(name="Quality-Assured Report", agent=report_generator),
        ],
        db=get_database("agno-storage"),
        debug_mode=debug_mode,
    )


# Export all workflow factory functions
__all__ = [
    'get_quick_performance_workflow',
    'get_comprehensive_workflow',
    'get_iterative_analysis_workflow',
]
