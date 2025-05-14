# 📊 Sample Database Examples

This directory contains simple, single-file examples that demonstrate AI agents interacting with the IBM SAMPLE database. These examples are designed to help you get started quickly with AI agents for Db2 for i.

## 📋 Available Examples

| Example | Description | Difficulty |
|---------|-------------|------------|
| 👥 [Employee Information Retrieval](get_employee_info_agent.py) | Retrieve and analyze employee data using AI | Beginner ⭐ |
| 🔄 [Employee Info Workflow](get_employee_info_workflow.py) | LangChain workflow for employee data analysis | Beginner ⭐ |
| 🔌 [Simple MCP Database Client](mcp_simple.py) | Basic Model Context Protocol client for database queries | Beginner ⭐ |

## 🚀 Running the Examples

### Prerequisites

- Python 3.9+
- The `uv` package manager
- Access to a Db2 for i database with the SAMPLE schema
- Mapepire service running on your IBM i system

### Environment Setup

1. **Important**: First, run the environment setup script from the parent directory:
   ```bash
   cd ../examples/ # Navigate to the examples directory 
   ./setup_env.sh
   cd sample
   ```
   This will create a `.env` file template in the examples directory.

2. (Optional) create the `.env` file in the `sample` directory with your specific credentials:
   ```
   HOST=your_ibmi_host
   DB_USER=your_username
   PASSWORD=your_password
   DB_PORT=your_db_port
   OPENAI_API_KEY=your_openai_api_key
   ```
   this will overwrite the `.env` file created in the parent directory.
   ```

### Running an Example

To run any example in this directory:

```bash
uv run get_employee_info_agent.py
```

> 💡 **Note**: This example requires your `OPENAI_API_KEY` to be set in the central config. 



```bash
uv run mcp_simple.py
```

> 💡 **Note**: This example requires your `OPENAI_API_KEY` to be set in the central config.

```bash
uv run get_employee_info_workflow.py --chain --question "How many employees are in each department?"
```

> 💡 **Note**: This example uses Ollama by default with the llama3.1 model. Make sure you have Ollama installed and the model available, or you can specify a different model with `--model modelname`.

## 🔍 Example Details

### 👥 Employee Information Retrieval

This example demonstrates:
- Creating an AI agent with the Agno framework
- Connecting to the SAMPLE database
- Querying employee information
- Using AI to analyze and present the results

### 🔌 Simple MCP Database Client

This example demonstrates:
- Basic setup of an MCP (Model Context Protocol) client
- Connecting to a database using Mapepire
- Running SQL queries through MCP
- Receiving and processing the results

## 📚 SAMPLE Database

These examples use the IBM-provided SAMPLE database. If you don't have it set up, you can create it on your IBM i system with:

```sql
CALL QSYS.CREATE_SQL_SAMPLE('SAMPLE')
```

This command creates tables with employee, department, and project data that the examples will use.

## 🛠️ Customizing Examples

Each example can be customized by:

1. Modifying the database connection details in the `.env` file
2. Changing the queries to explore different data
3. Adjusting the AI model parameters
4. Adding new functionality based on the example patterns

## 📌 Next Steps

After exploring these examples, you can:

1. Try more complex examples in the [ibmi-services](../ibmi-services/) directory
2. Explore complete applications in the [apps](../apps/) directory
3. Create your own examples using these as templates