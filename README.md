# Db2 for i AI Agents Cookbook

This repository contains a collection of example AI agents that demonstrate integration with Db2 for i across various AI agent frameworks.

## Repository Structure

- `demos/`: Contains individual agent examples organized by framework and language
  - `mcp/`: Model-Control-Processor framework demos
  - `crewai/`: CrewAI framework demos
  - `langchain/`: LangChain framework demos
  - `agno/`: Agno framework demos
  - `beeai/`: BeeAI framework demos
  - Each framework folder contains:
    - `python/`: Python implementations
    - `typescript/`: TypeScript implementations
    
- `shared/`: Common utilities and components used across demos
  - `auth/`: Authentication utilities for Db2 for i
  - `models/`: Shared data models and schemas
  - `utils/`: General utilities and helpers

- `docs/`: Additional documentation and guides

## Getting Started

Each demo has its own README with specific setup instructions. Python examples use the `uv` package manager for dependency management.

## Requirements

- For Python demos: Python 3.9+ and `uv` package manager
- For TypeScript demos: Node.js 18+ and npm/yarn
- Access to a Db2 for i instance