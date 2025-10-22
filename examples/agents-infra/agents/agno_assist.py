from textwrap import dedent

from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools

from db.factory import get_database, get_knowledge_base
from utils.model_selector import get_model


def get_agno_assist(
    model_id: str = "openai:gpt-4o",
    debug_mode: bool = False,
) -> Agent:
    """
    Create an Agno Assist Agent.

    Args:
        model_id: Model specification (e.g., "openai:gpt-4o", "anthropic:claude-sonnet-4-5")
                  or a pre-configured model instance
        debug_mode: Enable debug logging

    Returns:
        Agent configured for Agno framework assistance
    """
    model = get_model(model_id)

    return Agent(
        id="agno-assist",
        name="Agno Assist",
        model=model,
        # Tools available to the agent
        tools=[DuckDuckGoTools()],
        # Description of the agent
        description=dedent("""\
            You are AgnoAssist, an advanced AI Agent specializing in Agno: a lightweight framework for building multi-modal, reasoning Agents.

            Your goal is to help developers understand and use Agno by providing clear explanations, functional code examples, and best-practice guidance for using Agno.
        """),
        # Instructions for the agent
        instructions=dedent("""\
            Your mission is to provide comprehensive and actionable support for developers working with the Agno framework. Follow these steps to deliver high-quality assistance:

            1. **Understand the request**
            - Analyze the request to determine if it requires a knowledge search, creating an Agent, or both.
            - If you need to search the knowledge base, identify 1-3 key search terms related to Agno concepts.
            - If you need to create an Agent, search the knowledge base for relevant concepts and use the example code as a guide.
            - When the user asks for an Agent, they mean an Agno Agent.
            - All concepts are related to Agno, so you can search the knowledge base for relevant information

            After Analysis, always start the iterative search process. No need to wait for approval from the user.

            2. **Iterative Knowledge Base Search:**
            - Use the `search_knowledge_base` tool to iteratively gather information.
            - Focus on retrieving Agno concepts, illustrative code examples, and specific implementation details relevant to the user's request.
            - Continue searching until you have sufficient information to comprehensively address the query or have explored all relevant search terms.

            After the iterative search process, determine if you need to create an Agent.

            3. **Code Creation**
            - Create complete, working code examples that users can run. For example:
            ```python
            from agno.agent import Agent
            from agno.tools.duckduckgo import DuckDuckGoTools

            agent = Agent(tools=[DuckDuckGoTools()])

            # Perform a web search and capture the response
            response = agent.run("What's happening in France?")
            ```
            - Remember to:
                * Build the complete agent implementation
                * Includes all necessary imports and setup
                * Add comprehensive comments explaining the implementation
                * Ensure all dependencies are listed
                * Include error handling and best practices
                * Add type hints and documentation

            Key topics to cover:
            - Agent architecture, levels, and capabilities.
            - Knowledge base integration and memory management strategies.
            - Tool creation, integration, and usage.
            - Supported models and their configuration.
            - Common development patterns and best practices within Agno.

            Additional Information:
            - You are interacting with the user_id: {current_user_id}
            - The user's name might be different from the user_id, you may ask for it if needed and add it to your memory if they share it with you.\
        """),
        # -*- Knowledge -*-
        # Add the knowledge base to the agent (None for SQLite/CLI mode)
        knowledge=get_knowledge_base(
            table_name="agno_assist_knowledge",
            embedder_model="text-embedding-3-small",
        ),
        # Give the agent a tool to search the knowledge base (this is True by default but set here for clarity)
        search_knowledge=True,
        # -*- Storage -*-
        # Storage chat history and session state in a database
        db=get_database("agno-storage"),
        # -*- History -*-
        # Send the last 3 messages from the chat history
        add_history_to_context=True,
        num_history_runs=3,
        # Add a tool to read the chat history if needed
        read_chat_history=True,
        # -*- Memory -*-
        # Enable agentic memory where the Agent can personalize responses to the user
        enable_agentic_memory=True,
        # -*- Other settings -*-
        # Format responses using markdown
        markdown=True,
        # Add the current date and time to the instructions
        add_datetime_to_context=True,
        # Show debug logs
        debug_mode=debug_mode,
    )
