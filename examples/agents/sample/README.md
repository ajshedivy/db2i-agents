# 👥 Sample Database Examples

This directory contains simple, single-file examples that demonstrate AI agents interacting with the IBM SAMPLE database. These examples are designed to help you get started quickly with AI agents for Db2 for i.

## 🚨 Before You Start

**Have you completed the main setup?** These examples require the environment setup from the main README.

✅ **Required**: Complete the [Getting Started guide](../../../README.md#-getting-started) first, which covers:
- Setting up Mapepire on IBM i
- Creating your `.env` file with database credentials  
- Installing uv package manager
- Choosing your AI model provider

If you haven't done this yet, **stop here** and complete the main setup first.

## 📋 Available Examples

| Example | Description | Difficulty |
|---------|-------------|------------|
| 👥 [Employee Information Retrieval](get_employee_info_agent.py) | Retrieve and analyze employee data using AI | Beginner ⭐ |
| 🔄 [Employee Info Workflow](get_employee_info_workflow.py) | LangChain workflow for employee data analysis | Beginner ⭐ |
| 🔌 [Simple MCP Database Client](mcp_simple.py) | Basic Model Context Protocol client for database queries | Beginner ⭐ |

## 🚀 Running the Examples

Since you've completed the main setup, you can run these sample examples directly:

### Running the Examples

#### 👥 Employee Information Retrieval

Simple AI agent that queries and analyzes employee data:

```bash
uv run get_employee_info_agent.py
```

> 💡 **Note**: This example requires your `OPENAI_API_KEY` to be set in the central config.

#### 🔌 Simple MCP Database Client

Basic MCP client for database interactions:

```bash
uv run mcp_simple.py
```

> 💡 **Note**: This example requires your `OPENAI_API_KEY` to be set in the central config.

#### 🔄 Employee Info Workflow

LangChain-based workflow for employee data analysis:

```bash
uv run get_employee_info_workflow.py --chain --question "How many employees are in each department?"
```

You can customize the workflow with these options:

```bash
# Use a specific model
uv run get_employee_info_workflow.py --model gpt-4o --question "Who are the top 5 highest paid employees?"

# Run in interactive mode
uv run get_employee_info_workflow.py --interactive
```

> 💡 **Note**: This example uses Ollama by default with the llama3.1 model. Make sure you have Ollama installed and the model available, or specify a different model with `--model modelname`.
> 
> **Recommended**: Try `gpt-oss:20b` for better performance: `--model ollama:gpt-oss:20b`

## 🔍 Example Details

### 👥 Employee Information Retrieval

This example demonstrates:
- Creating an AI agent with the Agno framework
- Connecting to the SAMPLE database
- Querying employee information
- Using AI to analyze and present the results
- Basic error handling and data validation

**Sample interactions:**
```
> Tell me about employee 000010
> How many employees work in department A00?
> What's the average salary by department?
```

### 🔄 Employee Info Workflow

This example demonstrates:
- LangChain workflow implementation
- Structured data processing with AI
- Chain-based query execution
- Custom prompt engineering for database queries

**Sample questions:**
```
> How many employees are in each department?
> Who are the managers in the company?
> What's the salary distribution across departments?
```

### 🔌 Simple MCP Database Client

This example demonstrates:
- Basic setup of an MCP (Model Context Protocol) client
- Connecting to a database using Mapepire
- Running SQL queries through MCP
- Receiving and processing the results
- Protocol-level database communication

**Features:**
- Direct SQL query execution
- Result formatting and display
- Connection management
- Error handling

## 📚 SAMPLE Database

These examples use the IBM-provided SAMPLE database. If you don't have it set up, you can create it on your IBM i system with:

```sql
CALL QSYS.CREATE_SQL_SAMPLE('SAMPLE')
```

This command creates tables with employee, department, and project data:

### Key Tables:
- **EMPLOYEE**: Employee information (ID, name, job, salary, etc.)
- **DEPARTMENT**: Department details (ID, name, manager, etc.)
- **PROJECT**: Project information (ID, name, department, etc.)
- **EMP_ACT**: Employee activities and project assignments

### Sample Queries:
```sql
-- Get all employees
SELECT * FROM SAMPLE.EMPLOYEE

-- Employee count by department
SELECT WORKDEPT, COUNT(*) FROM SAMPLE.EMPLOYEE GROUP BY WORKDEPT

-- Salary statistics
SELECT AVG(SALARY), MIN(SALARY), MAX(SALARY) FROM SAMPLE.EMPLOYEE
```

## 🛠️ Customizing Examples

Each example can be customized by:

1. **Database Connection**: Modify connection details in the `.env` file
2. **Query Modification**: Change the queries to explore different data
3. **AI Model Configuration**: Adjust model parameters and prompts
4. **Output Formatting**: Customize how results are displayed
5. **Error Handling**: Add more robust error handling
6. **Interactive Features**: Enhance CLI functionality

### Example Customizations:

```python
# Modify queries in get_employee_info_agent.py
SAMPLE_QUERIES = [
    "SELECT * FROM SAMPLE.EMPLOYEE WHERE SALARY > 50000",
    "SELECT WORKDEPT, AVG(SALARY) FROM SAMPLE.EMPLOYEE GROUP BY WORKDEPT"
]

# Adjust AI model settings
model_config = {
    "model": "gpt-4o",
    "temperature": 0.3,
    "max_tokens": 1000
}
```

## 📈 Learning Progression

These examples are designed for progressive learning:

1. **Start with Employee Info Retrieval**: Learn basic agent concepts
2. **Try the MCP Client**: Understand protocol-level communication
3. **Explore the Workflow**: See structured data processing with LangChain

## 📌 Next Steps

After exploring these examples, you can:

1. Try more complex examples in the [services](../services/) directory
2. Explore performance monitoring in the [performance](../performance/) directory
3. Learn about security assessment in the [security](../security/) directory
4. Create your own examples using these as templates
5. Explore complete applications in the [../../apps/](../../apps/) directory

## 🤝 Contributing

To contribute new sample examples:

1. Keep examples simple and focused on specific concepts
2. Use the IBM SAMPLE database for consistency
3. Include clear documentation and usage examples
4. Follow the established naming patterns
5. Ensure compatibility with the existing environment setup

## 🎯 Best Practices

When using these examples:

1. **Start Simple**: Begin with basic queries before complex analysis
2. **Understand the Data**: Familiarize yourself with the SAMPLE database schema
3. **Experiment**: Modify queries and prompts to see different results
4. **Error Handling**: Pay attention to connection and query errors
5. **Security**: Never hardcode credentials in your examples