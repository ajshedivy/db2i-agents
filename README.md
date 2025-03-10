# 🤖 Db2 for i AI Agents Cookbook

This repository contains a collection of example AI agents that demonstrate integration with Db2 for i across various AI agent frameworks.

## 🧠 What are AI Agents?

AI agents are autonomous or semi-autonomous software entities powered by large language models (LLMs) that can:

- 🔍 Perceive their environment through tools and APIs
- 🤔 Make decisions based on reasoning and planning
- 🛠️ Execute actions to accomplish specific tasks
- 🔄 Learn and adapt from feedback and experience

Unlike basic LLM applications, agents can maintain context, use specialized tools, chain together operations, and solve complex problems that require multiple steps and data interactions.

## 📂 Repository Structure

- `examples/`: Contains individual agent examples organized by framework and language
  - `langchain/`: LangChain framework demos with Python implementation
  - `mcp/`: Model-Control-Processor framework demos
  - `crewai/`: CrewAI framework demos
  - `agno/`: Agno framework demos
  - `beeai/`: BeeAI framework demos
  - Each framework folder typically contains:
    - `python/`: Python implementations
    - `typescript/`: TypeScript implementations
    
- `shared/`: Common utilities and components used across demos

- `docs/`: Additional documentation and guides

## 🚀 Getting Started

Each demo has its own README with specific setup instructions. Python examples use the `uv` package manager for dependency management.

## 📋 Requirements

- For Python demos: Python 3.9+ and `uv` package manager
- For TypeScript demos: Node.js 18+ and npm/yarn
- Access to a Db2 for i instance

## 📊 Agent Framework Comparison

| Framework | Languages | Implementation Status | DB2 Access Method | Supports MCP | LLM Providers | Tool Integration |
|:----------|:----------|:----------------------|:------------------|:-------------|:--------------|:----------------|
| [🔗 LangChain](examples/agents/langchain/) | Python ✅ | Complete ✅ | Mapepire 🔌 | Yes ✅ | Anthropic 🧠<br>Ollama 🦙 | Medium 🟡 |
| [👥 CrewAI](examples/agents/crewai/) | Python ✅ | In Progress 🚧 | Mapepire 🔌 | No ❌ | - | - |
| [🏗️ MCP](examples/agents/mcp/) | Python ✅<br>TypeScript ✅ | In Progress 🚧 | Mapepire 🔌 | Yes ✅ | - | - |
| [🐝 BeeAI](examples/agents/beeai/) | Python ✅<br>TypeScript ✅ | In Progress 🚧 | Mapepire 🔌 | Yes ✅ | - | - |
| [🧩 Agno](examples/agents/agno/) | Python ✅ | In Progress 🚧 | Mapepire 🔌 | Yes ✅ | - | - |