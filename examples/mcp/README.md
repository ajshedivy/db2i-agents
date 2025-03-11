# 🚀 DB2i MCP (Model Context Protocol) Examples 

This repository contains a DB2i MCP server and client examples that enable AI assistants to interact with DB2 for i databases through the Model Context Protocol (MCP). 🤖💬

## 🔍 What is MCP?

The Model Context Protocol (MCP) is a communication protocol that enhances AI assistants with additional capabilities by enabling them to interact with external tools and access structured data. MCP allows AI models to:

- 🛠️ Call tools and receive their outputs
- 🔗 Access resources through standardized URIs
- ✨ Generate prompts dynamically
- 💾 Maintain session state

In this repository, MCP enables Claude and other compatible AI assistants to directly interact with DB2 for i databases.

## 📁 Repository Structure

```
mcp/
├── README.md              # This file - overview and getting started
├── db2i-mcp-server/       # The MCP server implementation for DB2i
│   ├── README.md          # Detailed server documentation and setup
│   ├── src/               # Server source code
│   └── ...
├── python/                # Python client example implementation 
│   └── README.md          # Python client setup and usage guide
└── typescript/            # TypeScript client example implementation
    └── README.md          # TypeScript client setup and usage guide
```

## 🚦 Getting Started

### 1. 🔧 Set Up the DB2i MCP Server

The `db2i-mcp-server` directory contains the core MCP server that connects to your DB2 for i database. This server must be setup and configured for any client examples to work.

```bash
cd db2i-mcp-server
```

Follow the detailed setup instructions in the [server README](./db2i-mcp-server/README.md) to:
1. 📝 Configure your DB2 for i connection details (.env file)
2. 🧪 Test your connection
3. 🚀 Start the server

### 2. 🔄 Choose a Client Example

Once your server is running, you can interact with it using one of these options:

- **🧩 Built-in Test Client**: The simplest way to test the server functionality:
  ```bash
  cd db2i-mcp-server
  uv run client.py
  ```

- **🤖 Claude Desktop**: For a full AI assistant experience, see the [server README](./db2i-mcp-server/README.md#using-with-claude-desktop) for setup instructions.

- **🛠️ Custom Clients**: The `/python` and `/typescript` directories contain example client implementations for building your own applications that utilize the DB2i MCP server.

## ✨ Features

The DB2i MCP server provides these key capabilities to AI assistants:

- **🔍 Database Discovery**: List and explore tables in the configured schema
- **📊 Schema Inspection**: View detailed table definitions and sample data
- **⚡ Query Execution**: Run SQL queries against the database
- **📝 Note Management**: Save and organize information during database exploration

## 👩‍💻 Development and Contribution

For development details, debugging tips, and how to contribute, see the [server README](./db2i-mcp-server/README.md#development).