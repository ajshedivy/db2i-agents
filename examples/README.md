# 💡 Db2 for i AI Examples

This directory contains practical, ready-to-run examples that demonstrate how to use AI with Db2 for i databases. From simple scripts to complete applications, these examples provide clear starting points for your own AI projects.

## 🧪 Example Categories

This repository is organized into four main categories:

1. **`sample/`**: Quick examples using the IBM SAMPLE database
2. **`ibmi-services/`**: Examples that interact with IBM i Services
3. **`performance/`**: Tools for monitoring and analyzing system performance
4. **`apps/`**: Complete applications with multiple components

## 📋 Current Examples

### Sample Database Examples
- 👥 [Employee Information Retrieval](sample/get_employee_info.py) - Simple agent that queries employee data from the SAMPLE database 
- 🔌 [Simple MCP Database Client](sample/mcp_simple.py) - Basic MCP client for database queries

### IBM i Services Examples
- 🔍 [Basic PTF Information Retrieval](ibmi-services/ptf/get_ptf_info.py) - Retrieve basic PTF information using AI
- 🔬 [Enhanced PTF Analysis](ibmi-services/ptf/get_ptf_info_extended.py) - Retrieve detailed PTF information with enhanced AI analysis
- 📂 [IFS File Reader](ibmi-services/ifs/read_stream_file.py) - Read and search file contents in the Integrated File System
- 💾 [IFS Storage Analyzer](ibmi-services/ifs/storage_assistant.py) - Find and analyze large files in the Integrated File System
- ☕ [JVM Performance Monitor](ibmi-services/java/jvm_assistant.py) - Monitor and optimize Java Virtual Machines on IBM i

### Performance Monitoring Examples
- 📊 [System Metrics Dashboard](performance/metrics_golf.py) - Lightweight system metrics dashboard for quick performance monitoring
- 📈 [Performance Metrics Assistant](performance/metrics_assistant.py) - AI-powered performance analysis and recommendations

### Complete Applications
- 🧠 [SQL Agent with Knowledge Base](apps/sql_agent_with_knowledge/) - Interactive SQL assistant with built-in database knowledge

## 🚀 Running the Examples

### Prerequisites

- Python 3.9+ with the `uv` package manager
- Access to a Db2 for i database
- Mapepire service running on your IBM i system

### Quick Start

1. First, run the setup script to pull the environment file into the examples directory:
   ```bash
   cd examples/ # Navigate to the examples directory
   ./setup_env.sh
   ```

2. Choose an example directory
3. Navigate to its directory
4. Run the example: `uv run <script_name>.py`

## 📚 Example Categories Explained

### Sample Examples

These work with the IBM SAMPLE database (created with `CALL QSYS.CREATE_SQL_SAMPLE('SAMPLE')`) and demonstrate basic AI agent capabilities in simple, single-file implementations.

### IBM i Services Examples

These showcase how AI agents can interact with IBM i Services (SQL interfaces to system information). Examples include PTF (Program Temporary Fix) information retrieval, Integrated File System (IFS) interaction, and Java Virtual Machine (JVM) monitoring.

### Performance Monitoring Examples

These examples demonstrate how to use AI agents to monitor, analyze, and visualize system performance metrics. They provide both lightweight dashboards and comprehensive performance analysis with AI-powered recommendations.

### Complete Applications

Full applications that demonstrate more complex AI agent scenarios, including the SQL agent with knowledge base that can answer questions about database schemas.

## 📁 Directory Structure

```
examples/
├── sample/                  # Examples using the SAMPLE database
├── ibmi-services/           # Examples using IBM i services
│   ├── ptf/                 # PTF information services
│   ├── ifs/                 # Integrated File System tools
│   └── java/                # Java and JVM monitoring tools
├── performance/             # Performance monitoring examples
└── apps/                    # Complete application examples
    └── sql_agent_with_knowledge/ # SQL agent with knowledge base
```

## 📚 Learning Path

If you're new to AI agents with Db2 for i, we recommend this learning path:

1. Start with 👥 [Employee Information Retrieval](sample/get_employee_info.py) to understand basic agent concepts
2. Try the 🔍 [Basic PTF Information Retrieval](ibmi-services/ptf/get_ptf_info.py) to see how agents can work with system information
3. Explore the 📂 [IFS File Reader](ibmi-services/ifs/read_stream_file.py) and 💾 [IFS Storage Analyzer](ibmi-services/ifs/storage_assistant.py) to learn how agents can work with the file system
4. Check out the 📊 [System Metrics Dashboard](performance/metrics_golf.py) to see how agents can monitor system performance
5. Explore the 🧠 [SQL Agent with Knowledge Base](apps/sql_agent_with_knowledge/) to learn about more complex implementations