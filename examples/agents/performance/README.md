# 📊 Performance Monitoring Examples

This directory contains examples that demonstrate how to use AI agents to monitor and analyze IBM i system performance. These examples leverage SQL services to provide insights into system metrics, resource usage, and performance optimization opportunities.

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
| 📈 [Metrics Assistant CLI](metrics_assistant_cli.py) | Interactive CLI for monitoring system performance metrics | Intermediate ⭐⭐ |
| 🎯 [Metrics Assistant](metrics_assistant.py) | Core metrics monitoring agent with AI analysis | Intermediate ⭐⭐ |
| ⛳ [Metrics Golf](metrics_golf.py) | Compact performance monitoring implementation | Intermediate ⭐⭐ |
| 🔍 [SQL Examples RAG](sql_examples_rag.py) | Retrieval-augmented generation for SQL performance examples | Intermediate ⭐⭐ |

## 🚀 Running the Examples

Since you've completed the main setup, you can run these performance examples directly:

### 📊 Optional: Weave Observability Setup

For enhanced observability and tracing of your AI agents, you can optionally set up Weave:

1. **Install Weave:**
   ```bash
   pip install weave
   ```

2. **Get your Weights & Biases API key** from [WandB Dashboard](https://wandb.ai/authorize)

3. **Add to your root `.env` file:**
   ```env
   WANDB_API_KEY=your_wandb_api_key
   ```

4. **Learn more** about Weave integration at [docs.agno.com/observability/weave](https://docs.agno.com/observability/weave)

> 💡 **Note**: Weave setup is completely optional. The examples work without it, but Weave provides valuable insights into agent behavior, token usage, and performance metrics.

### Running the Metrics Assistant CLI

The Metrics Assistant CLI provides an interactive interface for monitoring system performance:

```bash
uv run metrics_assistant_cli.py
```

You can customize the CLI with these options:

```bash
uv run metrics_assistant_cli.py --model-id openai:gpt-4o --stream --debug
# OR try with the recommended Ollama model:
uv run metrics_assistant_cli.py --model-id ollama:gpt-oss:20b --stream --debug
```

> 💡 **Note**: By default, this example uses OpenAI's GPT-4.1 model. You can specify a different model with `--model-id`.
> 
> **Recommended**: Try `ollama:gpt-oss:20b` for excellent performance with local models!

### Example CLI Commands

Once the CLI is running, you can use these commands:

```
analyze system           - Get comprehensive system performance analysis
top cpu jobs             - Show top CPU consuming jobs
check memory             - Analyze memory pool usage
collection config        - View Collection Services configuration
disk usage               - Check disk space and storage usage
http server stats        - Monitor HTTP server performance
temp storage             - Analyze temporary storage usage
exit                     - Exit the application
```

### Running Other Examples

```bash
# Core metrics assistant
uv run metrics_assistant.py

# Compact implementation
uv run metrics_golf.py

# SQL examples with RAG
uv run sql_examples_rag.py
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
- Disk usage and storage analysis

### 🎯 Metrics Assistant

Core performance monitoring agent that provides:
- Real-time system metrics collection
- AI-powered analysis and recommendations
- Customizable monitoring thresholds
- Performance trend analysis

### ⛳ Metrics Golf

A compact implementation focusing on:
- Minimal code footprint
- Essential performance metrics
- Quick system health checks
- Efficient data collection

### 🔍 SQL Examples RAG

This example demonstrates:
- Using retrieval-augmented generation (RAG) to improve SQL query suggestions
- Analyzing SQL performance data
- Providing optimized query examples based on context
- Building a knowledge base of performance queries

## 📚 Performance Monitoring Resources

These examples use IBM i SQL services for performance monitoring. Key services include:

```sql
-- System status
SELECT * FROM TABLE(QSYS2.SYSTEM_STATUS(RESET_STATISTICS=>'YES')) X

-- Memory pool information
SELECT * FROM TABLE(QSYS2.MEMORY_POOL(RESET_STATISTICS=>'YES')) X

-- Top CPU consuming jobs
SELECT * FROM TABLE(QSYS2.ACTIVE_JOB_INFO()) ORDER BY CPU_TIME DESC LIMIT 10

-- Collection Services configuration
SELECT * FROM QSYS2.COLLECTION_SERVICES_CONFIG

-- HTTP server statistics
SELECT * FROM TABLE(QSYS2.HTTP_SERVER_INFO()) X

-- Temporary storage usage
SELECT * FROM TABLE(QSYS2.TEMP_STORAGE_INFO()) X
```

## 🛠️ Customizing Examples

Each example can be customized by:

1. Modifying the database connection details in the `.env` file
2. Adding new performance metrics to monitor
3. Adjusting the AI model parameters
4. Extending the CLI functionality
5. Creating custom alerts and thresholds
6. Adding performance visualization components

## 📈 Performance Monitoring Best Practices

When using these examples:

1. **Regular Monitoring**: Set up scheduled monitoring for consistent system insights
2. **Baseline Establishment**: Use the tools to establish performance baselines
3. **Trend Analysis**: Monitor performance trends over time
4. **Proactive Alerts**: Configure alerts for performance thresholds
5. **Correlation Analysis**: Look for correlations between different metrics

## 📌 Next Steps

After exploring these examples, you can:

1. Combine performance monitoring with security assessment tools
2. Create automated performance analysis workflows
3. Build custom dashboards based on the performance data
4. Integrate with existing monitoring solutions
5. Explore other agent categories in the [security](../security/) or [services](../services/) directories

## 🤝 Contributing

To contribute new performance monitoring examples:

1. Follow the established file naming patterns
2. Include comprehensive documentation
3. Add example usage and CLI commands
4. Ensure compatibility with the existing environment setup
5. Test with various IBM i system configurations