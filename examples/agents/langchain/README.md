# 🔗 Langchain Tools Demo

This project demonstrates how to create SQL database tools for Langchain, specifically designed to work with Db2i Database.

## 🔍 Overview

The codebase contains several tools that can be used with Langchain's agent framework to interact with Db2i databases:

1. `QuerySQLDatabaseTool` - Execute SQL queries against a database
2. `InfoSQLDatabaseTool` - Get schema information about database tables

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.12 or later
- [uv](https://github.com/astral-sh/uv) package manager
- Access to a Db2i database instance

### Setting Up Your Environment

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/db2i-ai.git
   cd db2i-ai/db2i-agents/examples/agents/langchain
   ```

2. **Create and activate a virtual environment using uv:**
   ```bash
   uv venv
   source .venv/bin/activate  # On Linux/macOS
   # OR
   .venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies:**
   ```bash
   uv pip install -e .
   ```

4. **Set up environment variables:**
   
   Create a `.env` file in the project root with the following content:

   ```
   HOST=your_db2i_host
   DB_USER=your_username
   PORT=8075
   PASSWORD=your_password
   SCHEMA=SAMPLE  # Or your preferred schema
   ```

   These environment variables are required for connecting to your Db2i database.

## 🧩 Components

### Base Tool

- `BaseDb2iDatabaseTool` - A base class that all Db2i database tools inherit from, containing the database connection

### Database Query Tool

- `QuerySQLDatabaseTool` - Allows executing SQL queries against the database
  - Input: SQL query string
  - Output: Query results or error message
  - Alias: `QuerySQLDataBaseTool` (deprecated but maintained for backward compatibility)

### Database Information Tool

- `InfoSQLDatabaseTool` - Retrieves schema information for specified tables
  - Input: Comma-separated list of table names
  - Output: Schema information and sample rows for the specified tables

## 🚀 Running the Example

1. Make sure your `.env` file is set up correctly
2. Run the notebook example:
   ```bash
   jupyter notebook db2i_agent.ipynb
   ```

or open this project in VSCode. you can then open the `db2i_agent.ipynb` notebook and run the cells to see the tools in action.

## 📊 Testing

Some makeshift test are available in `tools/test_database.py`.

uncomment the test you want to run in `tools/test_database.py` and run:
```bash
uv run tools/test_database.py
```

## 🔌 Database Connection Details

### Mapepire Database Client

This project uses [Mapepire-python](https://github.com/Mapepire-IBMi/mapepire-python) as the underlying database client for connecting to Db2 for i. Mapepire is a modern database access layer for IBM i database access that provides:

- A PEP249-compliant DB API interface
- Connection management
- Both synchronous and asynchronous operation modes
- Native support for JSON and other DB2 for i data types

### How the Database Tool Works

The `Db2iDatabase` class (in `tools/database.py`) serves as a wrapper around the Mapepire client that makes it easy to use with LangChain. At a high level:

1. **Connection Management**: 
   - The class establishes and manages connections to the Db2i database using the configuration provided in the `.env` file
   - It uses the `connect()` function from Mapepire to create a connection to the database

2. **Schema and Table Information**:
   - The tool can retrieve metadata about tables in the database, including column names, data types, and sample data
   - It uses system tables like `QSYS2.SYSTABLES` to query this information
   - The `get_table_info()` method generates comprehensive schema information enhanced with sample rows

3. **Query Execution**:
   - The `run()` method executes SQL queries against the database and formats the results
   - Built-in error handling with the `run_no_throw()` method captures and formats database errors in a way that's useful for LLMs
   - Results are formatted as strings for easy consumption by LangChain agents

4. **Integration with LangChain**:
   - The database class is wrapped by LangChain tool classes that expose its functionality to agents
   - These tools follow LangChain's interface conventions, making them compatible with various agent frameworks

This architecture enables LLM agents to safely and effectively query Db2 for i databases without needing to understand the underlying connection details.

