#!/usr/bin/env python3
"""
DB2i Agent - LangChain Script

This script converts the db2i_agent.ipynb notebook into a Python script
that takes a question parameter as an argument.

Usage:
    python main.py --question "How many employees are in each department?" [--model llama3.1]
"""

import os
import argparse
from typing_extensions import TypedDict, Annotated
from dotenv import load_dotenv

from tools.database import Db2iDatabase
from tools.tools import QuerySQLDatabaseTool

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_anthropic import ChatAnthropic
from langgraph.graph import START, StateGraph


class State(TypedDict):
    question: str
    query: str
    result: str
    answer: str


class QueryOutput(TypedDict):
    """Generated SQL query."""
    query: Annotated[str, ..., "Syntactically valid SQL query."]


def load_connection():
    """Load database connection details from environment variables"""
    print("📡 Loading database connection details...")
    connection_details = {
        "host": os.getenv("HOST"),
        "user": os.getenv("DB_USER"),
        "port": os.getenv("PORT", 8075),
        "password": os.getenv("PASSWORD"),
        "schema": os.getenv("SCHEMA"),
    }
    print(f"✅ Connection details loaded for host: {connection_details['host']}, schema: {connection_details['schema']}")
    return connection_details


def get_llm(model_name="llama3.1"):
    """Get the LLM based on environment variables"""
    print("🧠 Initializing language model...")
    if os.getenv("ANTHROPIC_API_KEY"):
        print(f"🔄 Using Claude (claude-3-sonnet-20240229)")
        return ChatAnthropic(model="claude-3-sonnet-20240229")
    else:
        print(f"🔄 Using Ollama with model: {model_name}")
        return ChatOllama(model=model_name)


def write_query(state, test_tables, llm):
    """Generate a SQL query based on the user question and database schema."""
    print("🔍 Generating SQL query based on user question...")
    
    # Create prompt for SQL query generation
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                f"""You are a helpful SQL assistant that generates DB2 for i SQL queries based on user questions. 
                Do not append ; to the end of the query.
                
                Database schema:
                {test_tables}
                
                Generate a clear and efficient SQL query that answers the user's question."""
            ),
            ("human", "{question}"),
        ]
    )
    
    structured_llm = llm.with_structured_output(QueryOutput)
    chain = prompt | structured_llm
    
    result = chain.invoke({"question": state["question"]})
    
    print(f"✨ Generated SQL query: {result['query']}")
    return {"query": result["query"]}


def execute_query(state, db):
    """Execute SQL query."""
    print("🔄 Executing SQL query against database...")
    execute_query_tool = QuerySQLDatabaseTool(db=db)
    result = execute_query_tool.invoke(state["query"])
    print("✅ Query execution complete")
    return {"result": result}


def generate_answer(state, llm):
    """Answer question using retrieved information as context."""
    print("🤔 Generating natural language answer from query results...")
    prompt = (
        "Given the following user question, corresponding SQL query, "
        "and SQL result, answer the user question.\n\n"
        f'Question: {state["question"]}\n'
        f'SQL Query: {state["query"]}\n'
        f'SQL Result: {state["result"]}'
    )
    response = llm.invoke(prompt)
    print("💬 Answer generation complete")
    return {"answer": response.content}


def main():
    """Main function to run the agent"""
    print("\n🚀 Starting DB2i Agent with LangChain")
    print("=" * 50)
    
    parser = argparse.ArgumentParser(description="DB2i Agent with LangChain")
    parser.add_argument("--question", type=str, required=True, help="The question to ask the agent")
    parser.add_argument("--model", type=str, default="llama3.1", help="The Ollama model to use (default: llama3.1)")
    args = parser.parse_args()
    
    print(f"📝 Question: {args.question}")
    print("-" * 50)

    # Load environment variables
    print("⚙️  Loading environment variables...")
    load_dotenv()
    config = load_connection()
    schema = os.getenv("SCHEMA")

    # Initialize database
    print("🗄️  Initializing database connection...")
    db = Db2iDatabase(schema=schema, server_config=config)
    print("✅ Database connection initialized")
    
    # Get LLM
    llm = get_llm(args.model)
    
    # Get table info for the schema
    print("📊 Retrieving table information...")
    test_tables = db.get_table_info(['DEPARTMENT', 'EMPLOYEE'])
    print("✅ Table information retrieved")
    
    # Create the agent graph
    print("\n🔄 Creating workflow...")
    def create_flow(state):
        output = state.copy()
        
        print("\n📋 WORKFLOW EXECUTION")
        print("-" * 50)
        
        # Step 1: Write SQL query
        print("\n🔄 STEP 1: SQL Query Generation")
        query_output = write_query(state, test_tables, llm)
        output.update(query_output)
        
        # Step 2: Execute query
        print("\n🔄 STEP 2: SQL Query Execution")
        exec_output = execute_query(output, db)
        output.update(exec_output)
        
        # Step 3: Generate answer
        print("\n🔄 STEP 3: Answer Generation")
        answer_output = generate_answer(output, llm)
        output.update(answer_output)
        
        return output

    # Initialize state with user question
    print("🏁 Initializing workflow state...")
    state = {"question": args.question, "query": "", "result": "", "answer": ""}
    
    # Run the workflow
    print("\n🚀 Running workflow...")
    final_state = create_flow(state)
    
    # Print the final results
    print("\n📊 RESULTS")
    print("=" * 50)
    print(f"❓ Question: {final_state['question']}")
    print(f"🔍 SQL Query: {final_state['query']}")
    print(f"💬 Answer: {final_state['answer']}")
    print("=" * 50)
    print("✅ Process completed successfully")


if __name__ == "__main__":
    main()
