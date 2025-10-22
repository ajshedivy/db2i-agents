"""
Workflow Functions for IBM i Performance Analysis

This module contains custom functions used in workflow steps, including data processors,
quality checks, routers, and other workflow logic components.
"""

from typing import List
from datetime import datetime
from agno.workflow import StepInput, StepOutput


# ==================== WORKFLOW FUNCTIONS ====================

def performance_data_processor(step_input: StepInput) -> StepOutput:
    """
    Process and consolidate performance data from multiple analysis steps.
    Performs data quality checks and prepares structured analysis summaries.
    """
    try:
        # Get analysis results from previous steps
        analysis_content = step_input.previous_step_content or ""

        # Extract key performance indicators
        cpu_analysis = "CPU analysis completed" if "cpu" in analysis_content.lower() else "CPU analysis missing"
        memory_analysis = "Memory analysis completed" if "memory" in analysis_content.lower() else "Memory analysis missing"
        storage_analysis = "Storage analysis completed" if "storage" in analysis_content.lower() else "Storage analysis missing"

        # Calculate completeness score
        analyses = [cpu_analysis, memory_analysis, storage_analysis]
        completed_count = sum(1 for analysis in analyses if "completed" in analysis)
        completeness_score = (completed_count / len(analyses)) * 100

        # Create structured performance summary
        performance_summary = f"""
## Performance Analysis Data Processing Summary

**Analysis Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**Data Quality Assessment:**
- Completeness Score: {completeness_score:.1f}%
- Total Analysis Components: {len(analyses)}
- Completed Components: {completed_count}

**Analysis Component Status:**
- {cpu_analysis}
- {memory_analysis}
- {storage_analysis}

**Raw Analysis Data:**
{analysis_content}

**Processing Status:** {"✓ High Quality Data" if completeness_score >= 80 else "⚠ Incomplete Analysis Data"}
        """.strip()

        return StepOutput(
            content=performance_summary,
            success=True,
        )

    except Exception as e:
        return StepOutput(
            content=f"Performance data processing failed: {str(e)}",
            success=False,
            error=str(e)
        )


def quality_assurance_check(step_outputs: List[StepOutput]) -> bool:
    """
    Quality check function for the performance analysis loop.
    Returns True to break the loop when analysis quality is sufficient.
    """
    if not step_outputs:
        return False

    # Check the most recent output
    latest_output = step_outputs[-1]
    content = latest_output.content.lower()

    # Quality criteria
    has_system_data = any(keyword in content for keyword in ['cpu', 'memory', 'system status'])
    has_recommendations = any(keyword in content for keyword in ['recommend', 'suggest', 'optimize'])

    # Minimum content length check
    sufficient_content = len(latest_output.content) > 500

    # Return True to break loop if quality criteria are met
    quality_score = sum([has_system_data, has_recommendations, sufficient_content])
    return quality_score >= 2  # Need at least 2 out of 3 quality criteria


def comprehensive_quality_check(step_outputs: List[StepOutput]) -> bool:
    """
    Enhanced quality check for comprehensive analysis workflows.
    """
    if not step_outputs:
        return False

    latest_output = step_outputs[-1]
    content = latest_output.content.lower()

    # Enhanced quality criteria for comprehensive analysis
    has_system_metrics = any(keyword in content for keyword in ['cpu', 'memory', 'i/o', 'utilization'])
    has_recommendations = any(keyword in content for keyword in ['recommend', 'suggest', 'optimize', 'improve'])
    has_metrics = any(keyword in content for keyword in ['%', 'mb', 'gb', 'bytes', 'seconds'])

    # Comprehensive content requirements
    sufficient_length = len(latest_output.content) > 800
    has_structure = any(keyword in content for keyword in ['summary', 'analysis', 'findings', 'conclusion'])

    # Calculate comprehensive quality score
    quality_criteria = [
        has_system_metrics, has_recommendations, has_metrics,
        sufficient_length, has_structure
    ]

    quality_score = sum(quality_criteria)
    return quality_score >= 4  # Need at least 4 out of 5 criteria for comprehensive analysis


# Export all functions
__all__ = [
    'performance_data_processor',
    'quality_assurance_check',
    'comprehensive_quality_check',
]
