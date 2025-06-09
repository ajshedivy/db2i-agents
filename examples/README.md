# 💡 Db2 for i AI Examples

This directory contains practical, ready-to-run examples that demonstrate how to use AI with Db2 for i databases. From simple scripts to complete applications, these examples provide clear starting points for your own AI projects.

## 🧪 Example Categories

This repository is organized into several main categories:

1. **`sample/`**: Quick examples using the IBM SAMPLE database
2. **`ibmi-services/`**: Examples that interact with IBM i Services
3. **`performance/`**: Tools for monitoring and analyzing system performance
4. **`security/`**: Security assessment and remediation tools
5. **`sql_services/`**: SQL services exploration and interaction
6. **`apps/`**: Complete applications with multiple components

## 📋 Current Examples

### Sample Database Examples
- 👥 [Employee Information Retrieval](sample/get_employee_info_agent.py) - Simple agent that queries employee data from the SAMPLE database 
- 🔄 [Employee Info Workflow](sample/get_employee_info_workflow.py) - LangChain workflow for employee data analysis
- 🔌 [Simple MCP Database Client](sample/mcp_simple.py) - Basic MCP client for database queries

### IBM i Services Examples
- 🔍 [Basic PTF Information Retrieval](ibmi-services/ptf/get_ptf_info.py) - Retrieve basic PTF information using AI
- 🔬 [Enhanced PTF Analysis](ibmi-services/ptf/get_ptf_info_extended.py) - Retrieve detailed PTF information with enhanced AI analysis
- 📂 [IFS File Reader](ibmi-services/ifs/read_stream_file.py) - Read and search file contents in the Integrated File System
- 💾 [IFS Storage Analyzer](ibmi-services/ifs/storage_assistant.py) - Find and analyze large files in the Integrated File System
- ☕ [JVM Performance Monitor](ibmi-services/java/jvm_assistant.py) - Monitor and optimize Java Virtual Machines on IBM i

### Performance Monitoring Examples
- 📈 [Metrics Assistant CLI](performance/metrics_assistant_cli.py) - Interactive CLI for monitoring system performance metrics
- 🔍 [SQL Examples RAG](performance/sql_examples_rag.py) - Retrieval-augmented generation for SQL performance examples

### Security Examples
- 🛡️ [Security Assistant](security/security_assistant.py) - Interactive CLI for analyzing security vulnerabilities
- 📝 [Security Agent Playground](security/playground.py) - Testing environment for security analysis capabilities

### SQL Services Examples
- 🗃️ [SQL Services Agent](sql_services/sql_services_agent.py) - Interactive CLI for exploring IBM i SQL services
- 📓 [SQL Services Info Notebook](sql_services/sql_services_info.ipynb) - Jupyter notebook demonstrating SQL services queries

### Complete Applications
- 🧠 [SQL Agent with Knowledge Base](apps/sql_agent_with_knowledge/) - Interactive SQL assistant with built-in database knowledge

## 🚀 Running the Examples

### Prerequisites

- Python 3.9+ with the `uv` package manager
- Access to a Db2 for i database
- Mapepire service running on your IBM i system

### Quick Start

> 💡 **Note**: Make sure to setup your central `.env` file [here](../README.md#configure-mapepire-and-api-keys) first

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

![alt text](images/image2.png)

### IBM i Services Examples

These showcase how AI agents can interact with IBM i Services (SQL interfaces to system information). Examples include PTF (Program Temporary Fix) information retrieval, Integrated File System (IFS) interaction, and Java Virtual Machine (JVM) monitoring.

![alt text](images/image1.png)

### Performance Monitoring Examples

These examples demonstrate how to use AI agents to monitor and analyze system performance using SQL services. The interactive CLI provides real-time metrics and insights into system resources, memory usage, and job performance.

### Security Examples

These tools help analyze and remediate security vulnerabilities on IBM i systems. The security assistant identifies issues like exposed user profiles and provides automatic fix generation with proper authority settings.

### SQL Services Examples

These examples showcase how to interact with IBM i SQL services using AI agents. They provide tools for exploring available services, executing queries, and getting intelligent interpretations of the results.

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
├── security/                # Security assessment tools
├── sql_services/            # SQL services examples
└── apps/                    # Complete application examples
    └── sql_agent_with_knowledge/ # SQL agent with knowledge base
```

## 📚 Learning Path

If you're new to AI agents with Db2 for i, we recommend this learning path:

1. Start with 👥 [Employee Information Retrieval](sample/get_employee_info_agent.py) to understand basic agent concepts
2. Try the 🔍 [Basic PTF Information Retrieval](ibmi-services/ptf/get_ptf_info.py) to see how agents can work with system information
3. Explore the 📂 [IFS File Reader](ibmi-services/ifs/read_stream_file.py) to learn how agents can work with the file system
4. Check out the 📈 [Metrics Assistant CLI](performance/metrics_assistant_cli.py) to see how agents can monitor system performance
5. Try the 🛡️ [Security Assistant](security/security_assistant.py) to learn about security assessment
6. Explore the 🧠 [SQL Agent with Knowledge Base](apps/sql_agent_with_knowledge/) to learn about more complex implementations