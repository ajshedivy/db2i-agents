# db2i-mcp-server

A Model Context Protocol (MCP) server implementation for Db2 for i that enables AI agents to interact with Db2 for i databases through Claude and other MCP-compatible AI assistants.

## Overview

The Db2i MCP Server provides a standardized interface for AI assistants to work with Db2 for i databases, enabling intelligent data exploration, querying, and analysis capabilities. This server acts as a bridge between AI assistants and your Db2 for i data, leveraging the [Mapepire](https://mapepire-ibmi.github.io/) database driver for seamless connectivity.

### Key Features

- **Db2 for i Integration**: Connects directly to Db2 for i databases using Mapepire
- **Data Exploration**: Discover and explore available tables in your schema
- **Safe Query Execution**: Execute SQL queries with built-in safeguards
- **MCP-Compatible**: Works with Claude and other AI assistants supporting the Model Context Protocol

## Components

### Resources (In Progress)

(example for testing): The server implements a simple note storage system with:
- Custom note:// URI scheme for accessing individual notes
- Each note resource has a name, description and text/plain mimetype
- Notes persist during the session for referring to important information

### Prompts (In Progress)

(example for testing): The server generates prompts dynamically based on available notes:
- **summarize-notes**: Creates summaries of all stored notes
  - Optional "style" argument to control detail level (brief/detailed)
  - Generates prompt combining all current notes with style preference

### Tools

The server implements the following database interaction tools:

- **list-usable-tables**: Lists all usable tables in the configured schema
  - Call this first to discover available tables before querying
  - Filters tables based on configuration (include/ignore lists)

- **describe-table**: Returns the definition and sample rows for a specific table
  - Provides DDL schema definition and column information
  - Shows sample data rows to understand the table structure

- **run-sql-query**: Executes a SQL query and returns the results
  - Limited to SELECT statements for data safety
  - Handles parameters and formatting of results

- **add-note**: Adds a new note to the server (example tool for testing)
  - Takes "name" and "content" as required string arguments
  - Updates server state and notifies clients of resource changes

## Setup and Configuration

### Prerequisites

- [uv](https://github.com/astral-sh/uv?tab=readme-ov-file#installation)
- Access to a Db2 for i database
- [Mapepire](https://mapepire-ibmi.github.io/) database driver


### Mapepire Configuration

Create a `.env` file with your DB2 for i connection details:
```base
cd examples/mcp/db2i-mcp-server
cp .env.example .env
```

```
# Mapepire Credentials
HOST=hostname
DB_USER=username
PASSWORD=password
DB_PORT=8076           # default port for Mapepire
SCHEMA=schema_name
READONLY=True          # Only read access is supported

ENABLE_LOGGING=True
LOG_LEVEL=DEBUG
```

### Testing Your Mapepire Connection

You can test the Mapepire connection before starting the server:

```bash
uv run test_mapepire.py
```

A successful connection will display sample data from the SAMPLE.EMPLOYEE table.

## Quickstart

### Simple Client script

You can test the Db2i MCP server using a simple python script that creates a minimal MCP client:

This script requires the `SAMPLE` schema to be available in your Db2 for i database. make sure to set the `SCHEMA` environment variable in your `.env` file to `SAMPLE`.

```env
SCHEMA=SAMPLE
```

Run the client script:

```bash
cd examples/mcp/db2i-mcp-server
uv run client.py
```

Expected output:


```text
$ uv run client.py

===== AVAILABLE TOOLS =====

Tool: list-usable-tables
Description: List the usable tables in the schema. This tool should be called before running any other tool.
Input Schema: {
  "type": "object",
  "properties": {}
}

Tool: describe-table
Description: Describe a specific table including ites columns and sample rows. This tool should be called after list-usable-tables.
Input Schema: {
  "type": "object",
  "properties": {
    "table_name": {
      "type": "string",
      "description": "The name of the table to describe"
    }
  },
  "required": [
    "table_name"
  ]
}

Tool: run-sql-query
Description: run a valid Db2 for i SQL query. This tool should be called after list-usable-tables and describe-table.
Input Schema: {
  "type": "object",
  "properties": {
    "sql": {
      "type": "string",
      "description": "SELECT SQL query to execute"
    }
  },
  "required": [
    "sql"
  ]
}

Tool: add-note
Description: Add a new note
Input Schema: {
  "type": "object",
  "properties": {
    "name": {
      "type": "string"
    },
    "content": {
      "type": "string"
    }
  },
  "required": [
    "name",
    "content"
  ]
}

===== LIST OF TABLES =====

Available tables:
- ACT
- CL_SCHED
- DELETEME
- DEPARTMENT
- EMPLOYEE
- EMPPROJACT
- EMP_PHOTO
- EMP_RESUME
- IN_TRAY
- ORG
- PROJACT
- PROJECT
- SALES
- STAFF

===== TABLE DESCRIPTION: EMPLOYEE =====

Table Schema:
  --  Generate SQL
  --  Version:                   V7R4M0 190621
  --  Generated on:              03/11/25 18:09:14
  --  Relational Database:       IHOST
  --  Standards Option:          Db2 for i
  
  CREATE OR REPLACE TABLE SAMPLE.EMPLOYEE (
  EMPNO CHAR(6) CCSID 37 NOT NULL ,
  FIRSTNME VARCHAR(12) CCSID 37 NOT NULL ,
  MIDINIT CHAR(1) CCSID 37 NOT NULL ,
  LASTNAME VARCHAR(15) CCSID 37 NOT NULL ,
  WORKDEPT CHAR(3) CCSID 37 DEFAULT NULL ,
  PHONENO CHAR(4) CCSID 37 DEFAULT NULL ,
  HIREDATE DATE DEFAULT NULL ,
  JOB CHAR(8) CCSID 37 DEFAULT NULL ,
  EDLEVEL SMALLINT NOT NULL ,
  SEX CHAR(1) CCSID 37 DEFAULT NULL ,
  BIRTHDATE DATE DEFAULT NULL ,
  SALARY DECIMAL(9, 2) DEFAULT NULL ,
  BONUS DECIMAL(9, 2) DEFAULT NULL ,
  COMM DECIMAL(9, 2) DEFAULT NULL ,
  CONSTRAINT SAMPLE.Q_SAMPLE_EMPLOYEE_EMPNO_00001 PRIMARY KEY( EMPNO ) )
  
  RCDFMT EMPLOYEE   ;
  
  ALTER TABLE SAMPLE.EMPLOYEE
  ADD CONSTRAINT SAMPLE.RED
  FOREIGN KEY( WORKDEPT )
  REFERENCES SAMPLE.DEPARTMENT ( DEPTNO )
  ON DELETE SET NULL
  ON UPDATE NO ACTION ;
  
  ALTER TABLE SAMPLE.EMPLOYEE
  ADD CONSTRAINT SAMPLE.NUMBER
  CHECK( PHONENO >= '0000' AND PHONENO <= '9999' ) ;

Sample Data:
  3 sample rows from EMPLOYEE:
  EMPNO FIRSTNME        MIDINIT LASTNAME        WORKDEPT        PHONENO HIREDATE        JOB     EDLEVEL SEX     BIRTHDATE       SALARY      BONUS   COMM
  000010        CHRISTINE       I       HAAS    A00     3978    01/01/65        PRES    18      F       NULL    52750.0 1000.0  4220.0
  000020        MICHAEL L       THOMPSON        B01     3476    10/10/73        MANAGER 18      M       02/02/48        41250.0 800.0       3300.0
  000030        SALLY   A       KWAN    C01     4738    04/05/75        MANAGER 20      F       05/11/41        38250.0 800.0   3060.0

```




### Using with Claude Desktop

To use with [Claude Desktop](https://claude.ai/desktop), add the server configuration to Claude Desktop's config file:

- On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
- On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

<details>
  <summary>Development/Unpublished Servers Configuration</summary>

  ```json
  "mcpServers": {
    "db2i-mcp-server": {
      "command": "uv",
      "args": [
        "--directory",
        "PATH_TO_THIS_REPO/db2i-agents/examples/mcp/db2i-mcp-server",
        "run",
        "db2i-mcp-server"
      ]
    }
  }
  ```
</details>

<details>
  <summary>Published Servers Configuration</summary>

  ```json
  "mcpServers": {
    "db2i-mcp-server": {
      "command": "uvx",
      "args": [
        "db2i-mcp-server"
      ]
    }
  }
  ```
</details>

After configuring, you can enable the server in Claude Desktop and interact with your Db2 for i database through Claude.

Here is an example chat using the MCP server with Claude Desktop: [link](https://claude.ai/share/f4420035-4476-4877-9243-7bb8bb689130)

## Development

### Building and Publishing

To prepare the package for distribution:

1. Sync dependencies and update lockfile:
```bash
uv sync
```

2. Build package distributions:
```bash
uv build
```

This will create source and wheel distributions in the `dist/` directory.

3. Publish to PyPI:
```bash
uv publish
```

Note: You'll need to set PyPI credentials via environment variables or command flags:
- Token: `--token` or `UV_PUBLISH_TOKEN`
- Or username/password: `--username`/`UV_PUBLISH_USERNAME` and `--password`/`UV_PUBLISH_PASSWORD`

### Debugging

Since MCP servers run over stdio, debugging can be challenging. For the best debugging
experience, we strongly recommend using the [MCP Inspector](https://github.com/modelcontextprotocol/inspector).

You can launch the MCP Inspector via [`npm`](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) with this command:

```bash
npx @modelcontextprotocol/inspector uv --directory /Users/adamshedivy/Documents/IBM/sandbox/oss/ai/db2i-ai/db2i-agents/examples/mcp/db2i-mcp-server run db2i-mcp-server
```

Upon launching, the Inspector will display a URL that you can access in your browser to begin debugging.

