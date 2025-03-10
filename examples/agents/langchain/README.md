# Langchain Tools Demo

**in progress**

This project demonstrates how to create SQL database tools for Langchain, specifically designed to work with Db2i Database.

## Overview

The codebase contains several tools that can be used with Langchain's agent framework to interact with Db2i databases:

1. `QuerySQLDatabaseTool` - Execute SQL queries against a database
2. `InfoSQLDatabaseTool` - Get schema information about database tables

## Components

### Base Tool

- `BaseDb2iDatabaseTool` - A base class that all Db2i database tools inherit from, containing the database connection

### Database Query Tool

- `QuerySQLDatabaseTool` - Allows executing SQL queries against the database
  - Input: SQL query string
  - Output: Query results or error message
  - Alias: `QuerySQLDataBaseTool` (deprecated but maintained for backward compatibility)

### Database Information Tool

- `InfoSQLDatabaseTool` - Retrieves schema information for specified tables
  - Input: Comma-separated list of table names
  - Output: Schema information and sample rows for the specified tables


