# 📊 Performance Monitoring Examples

This directory contains examples that demonstrate how to use AI agents to monitor and analyze IBM i system performance. These examples leverage SQL services to provide insights into system metrics.

## 📋 Available Examples

| Example | Description | Difficulty |
|---------|-------------|------------|
| 📈 [Metrics Assistant CLI](metrics_assistant_cli.py) | Interactive CLI for monitoring system performance metrics | Intermediate ⭐⭐ |
| 🔍 [SQL Examples RAG](sql_examples_rag.py) | Retrieval-augmented generation for SQL performance examples | Intermediate ⭐⭐ |

## 🚀 Running the Examples

### Prerequisites

- Python 3.9+
- The `uv` package manager
- Access to a Db2 for i database with appropriate permissions
- Mapepire service running on your IBM i system

### Environment Setup

1. **Important**: First, run the environment setup script from the parent directory:
   ```bash
   cd ../examples/ # Navigate to the examples directory 
   ./setup_env.sh
   cd performance
   ```
   This will create a `.env` file template in the examples directory.

2. (Optional) create the `.env` file in the `performance` directory with your specific credentials:
   ```
   HOST=your_ibmi_host
   DB_USER=your_username
   PASSWORD=your_password
   DB_PORT=your_db_port
   OPENAI_API_KEY=your_openai_api_key
   ```
   this will overwrite the `.env` file created in the parent directory.

### Running the Metrics Assistant CLI

The Metrics Assistant CLI provides an interactive interface for monitoring system performance:

```bash
uv run metrics_assistant_cli.py
```

You can customize the CLI with these options:

```bash
uv run metrics_assistant_cli.py --model-id openai:gpt-4o --stream --debug
```

> 💡 **Note**: By default, this example uses OpenAI's GPT-4.1 model. You can specify a different model with `--model-id`.

### Example CLI Commands

Once the CLI is running, you can use these commands:

```
analyze system           - Get comprehensive system performance analysis
top cpu jobs             - Show top CPU consuming jobs
check memory             - Analyze memory pool usage
collection config        - View Collection Services configuration
exit                     - Exit the application
```

## 🔍 Example Details

### 📈 Metrics Assistant CLI

This example demonstrates:
- Creating an interactive CLI using the Agno framework
- Connecting to IBM i using Mapepire
- Using SQL services to gather performance metrics
- Analyzing system performance data with AI
- Providing insights and recommendations for performance optimization

Available performance metrics include:
- System status (CPU, memory, I/O)
- Memory pool usage
- Collection Services configuration
- HTTP server metrics
- Temporary storage usage
- Active job information

### 🔍 SQL Examples RAG

This example demonstrates:
- Using retrieval-augmented generation (RAG) to improve SQL query suggestions
- Analyzing SQL performance data
- Providing optimized query examples based on context

## 📚 Performance Monitoring Resources

These examples use IBM i SQL services for performance monitoring. Key services include:

```sql
-- System status
SELECT * FROM TABLE(QSYS2.SYSTEM_STATUS(RESET_STATISTICS=>'YES')) X

-- Memory pool information
SELECT * FROM TABLE(QSYS2.MEMORY_POOL(RESET_STATISTICS=>'YES')) X

-- Top CPU consuming jobs
SELECT * FROM TABLE(QSYS2.ACTIVE_JOB_INFO()) ORDER BY CPU_TIME DESC LIMIT 10
```

## 🛠️ Customizing Examples

Each example can be customized by:

1. Modifying the database connection details in the `.env` file
2. Adding new performance metrics to monitor
3. Adjusting the AI model parameters
4. Extending the CLI functionality

## 📌 Next Steps

After exploring these examples, you can:

1. Combine performance monitoring with other IBM i services
2. Create automated performance analysis workflows
3. Build custom dashboards based on the performance data
4. Explore security examples in the [security](../security/) directory