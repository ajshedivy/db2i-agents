<details>
   <summary>Table of Contents</summary>
   
- [🤖 Db2 for i AI Agents Cookbook](#-db2-for-i-ai-agents-cookbook)
  - [💡 Agentic Patterns for Db2 for i](#-agentic-patterns-for-db2-for-i)
    - [🧠 What is Agentic AI?](#-what-is-agentic-ai)
  - [📂 Repository Structure](#-repository-structure)
  - [📋 Requirements](#-requirements)
  - [🚀 Getting Started](#-getting-started)
    - [🛠️ Mapepire Database Access](#️-mapepire-database-access)
      - [Why Mapepire? ✨](#why-mapepire-)
      - [Setting Up Mapepire](#setting-up-mapepire)
    - [Configure Mapepire and API keys](#configure-mapepire-and-api-keys)
    - [Setup Ollama (recommended)](#setup-ollama-recommended)
  - [Install `uv` - a fast Python package manager](#install-uv---a-fast-python-package-manager)
  - [🔥 Quickstart - Run an example](#-quickstart---run-an-example)
  - [🧩 Explore Agent Frameworks](#-explore-agent-frameworks)
    - [Getting Started with Frameworks](#getting-started-with-frameworks)
  - [🧠 Agent Concepts](#-agent-concepts)
  - [📊 Agent Framework Comparison](#-agent-framework-comparison)
  - [🌟 Highlighted Demos](#-highlighted-demos)
    - [LangChain 🔍](#langchain-)
    - [MCP Server in Continue: 🚀](#mcp-server-in-continue-)
  - [📚 SAMPLE Database](#-sample-database)
</details>


# 🤖 Db2 for i AI Agents Cookbook

This repository helps you explore and implement AI agents that work with Db2 for i and IBM i systems. Whether you're new to AI or an experienced developer, you'll find examples, frameworks, and educational resources to help you build powerful AI solutions. ✨

## 💡 Agentic Patterns for Db2 for i

![alt text](docs/image-1.png)

### 🧠 What is Agentic AI?

AI agents are software programs that can:

- 🔍 Understand what you're asking them to do
- ✏️ Plan a series of steps to accomplish tasks
- 🔧 Use tools to interact with databases and systems
- 📈 Learn from their actions and your feedback

Unlike basic AI chat interfaces, agents can maintain context across conversations, work with your data, and execute multi-step operations. For Db2 and IBM i users, this means AI can help with:

- 💻 Writing and troubleshooting SQL queries
- 🔎 Finding and analyzing information in your databases
- ⚙️ Automating repetitive database tasks
- 📊 Building reports and visualizations
- 🙌 Helping less technical users access database information

Agents work by combining large language models with specialized tools that connect to your systems. Think of them as AI assistants that can actually take actions on your behalf! 🤝



## 📂 Repository Structure

This repository is organized into three main sections:

- **🏗️ [`frameworks/`](frameworks/)**: Ready-to-use agent implementations 
  - [`frameworks/agents/`](frameworks/agents/): Different AI frameworks (LangChain, Agno, CrewAI, etc.)
  - [`frameworks/mcp/`](frameworks/mcp/): Model Context Protocol for advanced AI-database communication

- **🎓 [`concepts/`](concepts/)**: Educational resources to learn about agent capabilities 
  - [`concepts/knowledge/`](concepts/knowledge/): How agents store and access information
  - [`concepts/memory/`](concepts/memory/): How agents remember past interactions
  - [`concepts/reasoning/`](concepts/reasoning/): How agents think through problems
  - [`concepts/tools/`](concepts/tools/): What agents can do with your systems

- **☕ [`examples/`](examples/)**: Simple demonstrations and complete applications
  - [`examples/sample/`](examples/sample/): Quick single-file examples to get started
  - [`examples/ibmi-services/`](examples/ibmi-services/): Working with IBM i services
  - [`examples/apps/`](examples/apps/): Full applications like SQL agents with knowledge bases

- **📄 [`docs/`](docs/)**: Additional documentation and guides

## 📋 Requirements

- For Python examples: Python 3.9+ and the `uv` package manager
- For TypeScript examples: Node.js 18+ and npm/yarn
- Access to a Db2 for i instance
- Mapepire database access layer

## 🚀 Getting Started

### 🛠️ Mapepire Database Access

[Mapepire](https://mapepire-ibmi.github.io/) is a modern database connector for IBM i that makes it easy for AI agents to work with your Db2 data. Think of it as a bridge between AI and your database. 🌉

#### Why Mapepire? ✨

- **Simple connection**: Works over standard ports - no special setup needed
- **Secure**: Supports proper authentication and SSL 🔒
- **Full-featured**: Handles all SQL operations and IBM i data types
- **AI-friendly**: Designed to work well with language models 🤖

#### Setting Up Mapepire

1. Install on your IBM i system:
   ```bash
   yum install service-commander
   yum install mapepire
   ```

2. Start the service:
   ```bash
   sc start mapepire
   ```

That's it! Mapepire runs on port 8076 by default. 🎉

### Configure Mapepire and API keys

Create a central `.env` file in the `config/` directory with your database connection details. This file can be used by all examples and frameworks in this repository.

This simple approach helps you manage database credentials and API keys across multiple examples without duplicating sensitive information.

1. Clone the repository:
   ```bash
   git clone https://github.com/ajshedivy/db2i-agents.git
   ```

2. Navigate to the `config/` directory:
   ```bash
   cd db2i-agents/config
   ```
3. Create your central configuration file:
   ```bash
   # Copy the template file
   cp env.sample .env.central
   ```
4. Edit with your credentials and API keys:
   ```bash
   nano .env.central  # or use your preferred editor
   ```

   ```env
   # Db2 for i database credentials
   # Copy this file to .env.central and update with your credentials

   # Database connection settings
   HOST=your_host_name
   DB_USER=your_username
   PASSWORD=your_password
   DB_PORT=8076
   SCHEMA=SAMPLE
   READONLY=TRUE

   # AI provider API keys (uncomment and add your keys as needed)
   # OPENAI_API_KEY=
   # ANTHROPIC_API_KEY=
   # IBM_WATSONX_API_KEY=
   # IBM_WATSONX_PROJECT_ID=
   # IBM_WATSONX_BASE_URL=
   # IBM_WATSONX_MODEL_ID=
   ```
   > 💡 **Note**: If you are using OpenAI, Anthropic, watonx, etc, set the API keys in the central config (config/.env.central) to make it easier to test with multiple models
### Setup Ollama (recommended)

   1. Install [Ollama](https://ollama.com/) on your system. This is a local LLM model provider that allows you to run models like Llama 3.1, Qwen 2.5, etc.
   
   2. Pull the model you want to use, For the agent examples I use `llama3.1` and `qwen2.5`:
      ```bash
      ollama pull llama3.1
      ollama pull qwen2.5:latest
      ```

## Install `uv` - a fast Python package manager

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
   More details on `uv` can be found in the [uv documentation](https://docs.astral.sh/uv/)

## 🔥 Quickstart - Run an example

Pull Ollama model:
   ```bash
   ollama pull llama3.1
   ```

   Run the example:
   ```bash
   cd examples/sample
   ../setup_env.sh    # copy central env file
   uv run get_employee_info_workflow.py --chain --question "how many employees are there?"
   ```

   More examples can be found in the [`examples/`](examples/) directory.

## 🧩 Explore Agent Frameworks

This repository includes several powerful frameworks for building AI agents, each with unique strengths:

### Getting Started with Frameworks

| Framework | Best For | Key Feature |
|:----------|:---------|:------------|
| [🔗 LangChain](frameworks/agents/langchain/README.md) | Production-ready solutions | Robust ecosystem with extensive integrations |
| [🏗️ Agno](frameworks/agents/agno/README.md) | Learning agent fundamentals | Transparent architecture that reveals core agent concepts |
| [📡 MCP](frameworks/mcp/README.md) | Standardized context | Consistent way to provide context to LLMs |

To explore these frameworks:
1. Navigate to the framework directory (e.g., `cd frameworks/agents/langchain`)
2. Follow the framework-specific README instructions
3. Run the included demos to see agents in action

> 💡 **Recommendation**: Choose LangChain when you need comprehensive, battle-tested solutions with extensive documentation. Use Agno when you want to deeply understand agent architecture or need a lightweight framework that makes the concepts behind agent construction more transparent.

## 🧠 Agent Concepts

Understanding how agents work is key to building effective solutions. Our [`concepts/`](concepts/README.md) directory breaks down the essential components:

- **📚 Knowledge**: How agents store, retrieve, and use information
  - Vector databases, embeddings, retrieval techniques
  
- **🔄 Memory**: How agents maintain conversation history and context
  - Short-term and long-term memory approaches

- **🤔 Reasoning**: How agents make decisions and solve problems
  - Chain-of-thought, tree-of-thought, and other reasoning patterns

- **🔧 Tools**: How agents interact with systems and data
  - Function calling, API integration, database connections

- **💾 Storage**: How agents persist and access data
  - Databases, file systems, caching strategies

Each concept includes code examples and explanations to help you implement these capabilities in your own agents.

## 📊 Agent Framework Comparison

| Framework | Languages | Implementation Status | Db2i Access Method | Supports MCP | Description |
|:----------|:----------|:----------------------|:------------------|:-------------|:--------------|
| [🔗 LangChain](frameworks/agents/langchain/) | Python ✅ | Complete ✅ | Mapepire 🔌 | Yes ✅ | Popular framework for developing applications powered by LLMs  |
| [🏗️ MCP](frameworks/mcp/) | Python ✅<br>TypeScript ✅ | Complete ✅ | Mapepire 🔌 | Yes ✅ | An open protocol that standardizes how applications provide context to LLMs. |
| [🧩 Agno](frameworks/agents/agno/) | Python ✅ | Complete ✅  | Mapepire 🔌 | Yes ✅ | A lightweight library for building Agents with memory, knowledge, tools and reasoning. |
| [🐝 BeeAI](frameworks/agents/beeai/) | Python ✅<br>TypeScript ✅ | Coming soon ⏳| Mapepire 🔌 | Yes ✅ | An open-source ecosystem that empowers developers to discover, run, and compose AI agents from any framework. |
| [👥 CrewAI](frameworks/agents/crewai/) | Python ✅ | Coming soon ⏳ | Mapepire 🔌 | No ❌ | Fast and flexible Python Multi-Agent automation framework |

## 🌟 Highlighted Demos

### LangChain 🔍
https://github.com/user-attachments/assets/54c7335e-da98-4c92-ba8d-66836c39f79d

### MCP Server in Continue: 🚀
https://github.com/user-attachments/assets/f72f2982-0b0c-4da0-b488-59ae7f311fde



## 📚 SAMPLE Database

Most examples use the IBM-provided SAMPLE database. To create it on your system, run:

```sql
CALL QSYS.CREATE_SQL_SAMPLE('SAMPLE')
```

This creates tables with employee, department, and project data that the examples will work with! 🏢👩‍💼👨‍💼