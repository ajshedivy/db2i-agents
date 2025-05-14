# 🏗️ AI Agent Frameworks for Db2 for i

This directory contains ready-to-use AI agent implementations that work with Db2 for i databases. These frameworks provide different approaches to creating intelligent agents that can help users interact with database systems.

## 🧩 What's in this Directory?

This directory is organized into two main sections:

- **`agents/`**: Complete implementations of various AI agent frameworks
- **`mcp/`**: Model Context Protocol server and clients for Db2 for i

## 🤖 Available Frameworks

| Framework | Description | Key Features | Best For |
|-----------|-------------|--------------|----------|
| [LangChain](agents/langchain/) | Popular framework for building LLM applications | ReAct agents, SQL chains, vector knowledge | Production applications |
| [Agno](agents/agno/) | Lightweight framework with reasoning capabilities | Memory, knowledge tools, UI components | Interactive applications |
| [BeeAI](agents/beeai/) | Open ecosystem for composition across frameworks | Discovery, running, and composition of agents | Multi-framework projects |
| [CrewAI](agents/crewai/) | Framework for multi-agent collaboration | Teams of specialized agents, role-based workflows | Complex workflows |

## 🔌 Model Context Protocol (MCP)

The [MCP directory](mcp/) contains an implementation of the [Model Context Protocol](https://github.com/anthropics/anthropic-cookbook/tree/main/mcp/simple-mcp-server). This powerful protocol allows AI assistants (like Claude) to use tools and access external data.

### MCP Features

- **Server**: A complete MCP server implementation for Db2 for i
- **Clients**: Examples of how to connect various AI tools to the MCP server
- **Integration Guides**: Instructions for using with Claude Desktop, VS Code, and other environments

## 🚀 Getting Started

Each framework has its own README with specific setup instructions, but here's a general approach:

1. Choose a framework that fits your needs
2. Set up your database connection (most examples use Mapepire)
3. Install the required dependencies
4. Run the examples or build your own agent

## 🔄 Framework Comparison

| Feature | LangChain | Agno | BeeAI | CrewAI |
|---------|-----------|------|-------|--------|
| **Maturity** | High | Medium | Early | Medium |
| **Complexity** | Medium | Low | Medium | High |
| **Languages** | Python | Python | Python, TypeScript | Python |
| **Memory** | Yes | Yes | Yes | Yes |
| **Reasoning** | Yes | Advanced | Yes | Yes |
| **Multi-agent** | Limited | Yes | Yes | Specialized |
| **UI Components** | No | Yes | No | No |
| **Learning Curve** | Medium | Low | Medium | Medium |

## 📋 Requirements

- Python 3.9+ (for Python implementations)
- Node.js 18+ (for TypeScript implementations)
- Access to a Db2 for i instance
- Mapepire database connector (installed on your IBM i system)

## 🔗 Useful Resources

- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
- [Agno GitHub Repository](https://github.com/agno-ai/agno)
- [Model Context Protocol Documentation](https://docs.anthropic.com/claude/docs/model-context-protocol-mcp)