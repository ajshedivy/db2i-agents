"""Define a custom Reasoning and Action agent.

Works with a chat model with tool calling support.
"""

from datetime import datetime, timezone
from textwrap import dedent
from typing import Dict, List, Literal, cast

from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode

from langchain_anthropic import ChatAnthropic
from react_agent.database import Db2iDatabase
from react_agent.toolkit import Db2iDatabaseToolkit

from react_agent.configuration import Configuration
from react_agent.state import InputState, State
from react_agent.tools import TOOLS
from react_agent.utils import load_chat_model

from langgraph.prebuilt import create_react_agent

# Define the function that calls the model

###########################################################################################################################
'''
The following code is placeholder code for a custom graph that uses the ReAct agent to interact with a SQL database.

Instead, we can use the prebuilt `create_react_agent` function to create a ReAct agent that interacts with a SQL database.

'''

# async def call_model(
#     state: State, config: RunnableConfig
# ) -> Dict[str, List[AIMessage]]:
#     """Call the LLM powering our "agent".

#     This function prepares the prompt, initializes the model, and processes the response.

#     Args:
#         state (State): The current state of the conversation.
#         config (RunnableConfig): Configuration for the model run.

#     Returns:
#         dict: A dictionary containing the model's response message.
#     """
#     configuration = Configuration.from_runnable_config(config)

#     # Initialize the model with tool binding. Change the model or add more tools here.
#     model = load_chat_model(configuration.model).bind_tools(TOOLS)

#     # Format the system prompt. Customize this to change the agent's behavior.
#     system_message = configuration.system_prompt.format(
#         system_time=datetime.now(tz=timezone.utc).isoformat()
#     )

#     # Get the model's response
#     response = cast(
#         AIMessage,
#         await model.ainvoke(
#             [{"role": "system", "content": system_message}, *state.messages], config
#         ),
#     )

#     # Handle the case when it's the last step and the model still wants to use a tool
#     if state.is_last_step and response.tool_calls:
#         return {
#             "messages": [
#                 AIMessage(
#                     id=response.id,
#                     content="Sorry, I could not find an answer to your question in the specified number of steps.",
#                 )
#             ]
#         }

#     # Return the model's response as a list to be added to existing messages
#     return {"messages": [response]}


# # Define a new graph

# builder = StateGraph(State, input=InputState, config_schema=Configuration)

# # Define the two nodes we will cycle between
# builder.add_node(call_model)
# builder.add_node("tools", ToolNode(TOOLS))

# # Set the entrypoint as `call_model`
# # This means that this node is the first one called
# builder.add_edge("__start__", "call_model")


# def route_model_output(state: State) -> Literal["__end__", "tools"]:
#     """Determine the next node based on the model's output.

#     This function checks if the model's last message contains tool calls.

#     Args:
#         state (State): The current state of the conversation.

#     Returns:
#         str: The name of the next node to call ("__end__" or "tools").
#     """
#     last_message = state.messages[-1]
#     if not isinstance(last_message, AIMessage):
#         raise ValueError(
#             f"Expected AIMessage in output edges, but got {type(last_message).__name__}"
#         )
#     # If there is no tool call, then we finish
#     if not last_message.tool_calls:
#         return "__end__"
#     # Otherwise we execute the requested actions
#     return "tools"


# # Add a conditional edge to determine the next step after `call_model`
# builder.add_conditional_edges(
#     "call_model",
#     # After call_model finishes running, the next node(s) are scheduled
#     # based on the output from route_model_output
#     route_model_output,
# )

# # Add a normal edge from `tools` to `call_model`
# # This creates a cycle: after using tools, we always return to the model
# builder.add_edge("tools", "call_model")

# # Compile the builder into an executable graph
# # You can customize this by adding interrupt points for state updates
# graph = builder.compile(
#     interrupt_before=[],  # Add node names here to update state before they're called
#     interrupt_after=[],  # Add node names here to update state after they're called
# )
# graph.name = "ReAct Agent"  # This customizes the name in LangSmith

###########################################################################################################################

def get_system_message():
    """Get system message for the agent"""
    template = dedent("""
        ================================ System Message ================================

        You are an agent designed to interact with a SQL database.
        Given an input question, create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
        Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most {top_k} results.
        You can order the results by a relevant column to return the most interesting examples in the database.
        Never query for all the columns from a specific table, only ask for the relevant columns given the question.
        You have access to tools for interacting with the database.
        Only use the below tools. Only use the information returned by the below tools to construct your final answer.
        You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

        DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.
        
        DO NOT add ; to the end of sql queries.
        
        ALWAYS use SCHEMA.TABLE_NAME to reference tables in the database.

        To start you should ALWAYS look at the tables in the database to see what you can query.
        Do NOT skip this step.
        Then you should query the schema of the most relevant tables.  
    """)
    
    return template.format(dialect="Db2i", top_k=100)



from dotenv import load_dotenv
import os
from langchain import hub

prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")

assert len(prompt_template.messages) == 1
system_message = get_system_message()

def load_connection():
    connection_details = {
        "host": os.getenv("HOST"),
        "user": os.getenv("DB_USER"),
        "port": os.getenv("PORT", 8075),
        "password": os.getenv("PASSWORD"),
        "schema": os.getenv("SCHEMA"),
    }
    return connection_details

load_dotenv()

config = load_connection()
SCHEMA = os.getenv("SCHEMA")

llm = ChatAnthropic(model="claude-3-sonnet-20240229")
db = Db2iDatabase(schema=SCHEMA, server_config=config, ignore_tables=["EMPLOYEES"])
toolkit = Db2iDatabaseToolkit(db=db, llm=llm)
tools = toolkit.get_tools()

graph = create_react_agent(llm, tools=tools, prompt=system_message, interrupt_before=["tools"])
graph.name = "ReAct Agent"





