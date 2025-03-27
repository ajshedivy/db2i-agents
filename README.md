<details>
   <summary>Table of Contents</summary>
   
- [🤖 Db2 for i AI Agents Cookbook](#-db2-for-i-ai-agents-cookbook)
  - [🧠 What are AI Agents?](#-what-are-ai-agents)
  - [📊 Agent Framework Comparison](#-agent-framework-comparison)
  - [📂 Repository Structure](#-repository-structure)
  - [📋 Requirements](#-requirements)
  - [🚀 Getting Started](#-getting-started)
  - [🔥 Quickstart](#-quickstart)
  - [🌟 Highlighted Demos](#-highlighted-demos)
    - [LangChain](#langchain)
    - [MCP Server in Continue:](#mcp-server-in-continue)
  - [🛠️ Mapepire Setup](#️-mapepire-setup)
    - [Recommended Installation (Service Commander)](#recommended-installation-service-commander)
    - [Port Configuration](#port-configuration)
  - [🤔 How Mapepire is used in the examples](#-how-mapepire-is-used-in-the-examples)
  - [📚 SAMPLE database](#-sample-database)
</details>


# 🤖 Db2 for i AI Agents Cookbook

This repository contains a collection of example AI agents that demonstrate integration with Db2 for i across various AI agent frameworks.

## 🧠 What are AI Agents?

AI agents are autonomous or semi-autonomous software entities powered by large language models (LLMs) that can:

- 🔍 Perceive their environment through tools and APIs
- 🤔 Make decisions based on reasoning and planning
- 🛠️ Execute actions to accomplish specific tasks
- 🔄 Learn and adapt from feedback and experience

Unlike basic LLM applications, agents can maintain context, use specialized tools, chain together operations, and solve complex problems that require multiple steps and data interactions.

## 📊 Agent Framework Comparison

| Framework | Languages | Implementation Status | DB2 Access Method | Supports MCP | LLM Providers | Tool Integration |
|:----------|:----------|:----------------------|:------------------|:-------------|:--------------|:----------------|
| [🔗 LangChain](examples/agents/langchain/) | Python ✅ | Complete ✅ | Mapepire 🔌 | Yes ✅ | Anthropic 🧠<br>Ollama 🦙 | Medium 🟡 |
| [👥 CrewAI](examples/agents/crewai/) | Python ✅ | Coming soon ⏳ | Mapepire 🔌 | No ❌ | - | - |
| [🏗️ MCP](examples/mcp/) | Python ✅<br>TypeScript ✅ | In Progress 🚧 | Mapepire 🔌 | Yes ✅ | - | Implemetation: hard 💀 <br> integration: easy 😊   |
| [🐝 BeeAI](examples/agents/beeai/) | Python ✅<br>TypeScript ✅ | Coming soon ⏳| Mapepire 🔌 | Yes ✅ | - | - |
| [🧩 Agno](examples/agents/agno/) | Python ✅ | Coming soon ⏳ | Mapepire 🔌 | Yes ✅ | - | - |

## 📂 Repository Structure

- `examples/`: Contains individual agent examples organized by framework and language
  - `agents/`: Agent framework implementations
    - `agno/`: Agno framework demos 
    - `beeai/`: BeeAI framework demos 
    - `crewai/`: CrewAI framework demos
    - `langchain/`: LangChain framework demos
  - `mcp/`: Model Context Protocol (MCP) Db2i server and client examples
    - `db2i-mcp-server/`: MCP server implementation
    
- `shared/`: Common utilities and components used across demos

- `docs/`: Additional documentation and guides

## 📋 Requirements

- For Python demos: Python 3.9+ and `uv` package manager
- For TypeScript demos: Node.js 18+ and npm/yarn
- Access to a Db2 for i instance

## 🚀 Getting Started

Each demo has its own README with specific setup instructions. Python examples use the `uv` package manager for dependency management.

1. Clone the repository:
   ```bash
   git clone https://github.com/ajshedivy/db2i-agents.git
   ```
2. Install [`uv`](https://docs.astral.sh/uv/getting-started/installation/#__tabbed_1_1):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
3. navtivate to the example you want to run:
   ```bash
   cd examples/agents/langchain
   ```
4. Follow the setup instructions in the README for that example.


## 🔥 Quickstart

To get started with the the Db2 for i Agent examples, I recommend starting with the [LangChain](examples/agents/langchain/) framework. Which offers a complete implementation and a good starting point for understanding how to build AI agents that interact with Db2 for i databases.

```bash
cd examples/agents/langchain
uv run main.py --chain --question "how many employees are there?"
```
More on the LangChain framework can be found in the [LangChain README](examples/agents/langchain/README.md#-running-the-example).

## 🌟 Highlighted Demos

### LangChain
https://github.com/user-attachments/assets/54c7335e-da98-4c92-ba8d-66836c39f79d

More on LangChain can be found in the [LangChain README](examples/agents/langchain/README.md#-running-the-example).

### MCP Server in Continue:
https://github.com/user-attachments/assets/f72f2982-0b0c-4da0-b488-59ae7f311fde

More on the MCP server can be found in the [MCP README](examples/mcp/README.md#-getting-started).

## 🛠️ Mapepire Setup

Almost all of the examples in this repository use the [Mapepire](https://mapepire-ibmi.github.io/) database access layer to connect to Db2 for i databases.

### Recommended Installation (Service Commander)

This approach requires the RPM installed version of Mapepire.

1. Install service commander:
   ```bash
   yum install service-commander
   ```

2. Install Mapepire on your IBM i system:
   ```bash
   yum install mapepire
   ```

3. Start Mapepire:
   ```bash
   sc start mapepire
   ```

### Port Configuration

By default, the port used by the Mapepire server is 8076. It is not recommended to change it. If needed, however, the port can be manipulated with the PORT environment variable, or if using Service Commander, by changing the port number in the check_alive field of the server definition.

For more detailed information, visit the [Mapepire System Administration Guide](https://mapepire-ibmi.github.io/guides/sysadmin/).

## 🤔 How Mapepire is used in the examples

The examples in this repository use Mapepire to connect to Db2 for i databases. The connection details are stored in a `.env` file in the root of each example directory.

```env
HOST=XXX
DB_USER=XXX
PASSWORD=XXX
PORT=8076
SCHEMA=XXX
READONLY=XXX
```

In the future, I plan to add better configuration management for Mapepire. 

## 📚 SAMPLE database

Unless explicitly specified, all examples in this repository use the `SAMPLE` database schema by default. If you want to use a different schema, you can change the `SCHEMA` environment variable in the `.env` file.

To setup the SAMPLE database, you can use the following SQL script:

```sql
CALL QSYS.CREATE_SQL_SAMPLE('SAMPLE')
```

