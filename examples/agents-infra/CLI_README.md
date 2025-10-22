# CLI for agents-infra

A simple command-line interface alternative to AgentOS for running agents, teams, and workflows locally without Docker or PostgreSQL.

## Overview

The CLI (`cli.py`) allows you to run any of the agents-infra agents, teams, and workflows directly from the command line using SQLite for storage instead of PostgreSQL. This is useful for:

- Local development and testing
- Running agents, teams, and workflows without Docker infrastructure
- Quick agent/team/workflow interactions without starting the full AgentOS server
- Testing multi-step workflows with automated execution

## Features

- **Agents, Teams & Workflows**: Run individual agents, multi-agent teams, or multi-step workflows
- **No PostgreSQL required**: Uses SQLite for storage and history
- **No Docker required**: Runs directly in your Python environment
- **Model selection**: Choose any supported model via `--model-id`
- **Streaming support**: Enable streaming responses with `--stream` (agents/teams)
- **Debug mode**: Verbose output with `--debug`
- **Workflow input**: Provide workflow queries via `--prompt` parameter
- **Graceful degradation**: Items with missing dependencies are skipped automatically

## Requirements

The CLI uses the same dependencies as the Docker deployment, but:
- PostgreSQL and pgvector are not required
- Some agents may require additional packages (e.g., `ddgs` for web search)

## Quick Start

### List Available Agents, Teams, and Workflows

```bash
python cli.py --list-agents
python cli.py --list-teams
python cli.py --list-workflows
```

### Run an Agent

```bash
# Run with default model (OpenAI GPT-4o)
python cli.py --agent metrics

# Run with specific model
python cli.py --agent ptf --model-id watsonx:mistralai/mistral-large

# Run with streaming
python cli.py --agent security --stream

# Run with debug mode
python cli.py --agent storage --debug
```

### Run a Team

```bash
# Run PTF team
python cli.py --team ptf-team

# Run performance routing team with specific model
python cli.py --team performance-routing --model-id anthropic:claude-sonnet-4-5

# Run collaboration team with streaming
python cli.py --team performance-collaboration --stream
```

### Run a Workflow

```bash
# Run quick performance check workflow
python cli.py --workflow quick-performance --prompt "Check current system performance"

# Run comprehensive analysis with specific model
python cli.py --workflow comprehensive-analysis --prompt "Analyze performance bottlenecks" --model-id watsonx:mistralai/mistral-large

# Run iterative analysis with debug mode
python cli.py --workflow iterative-analysis --prompt "Find and resolve performance issues" --debug
```

## Available Agents

| Agent ID | Name | Description |
|----------|------|-------------|
| `metrics` | Performance Metrics Assistant | IBM i performance metrics and monitoring |
| `ptf` | PTF Assistant | IBM i PTF (Program Temporary Fix) management |
| `storage` | Storage Assistant | IBM i IFS storage analysis |
| `security` | Security Assistant | IBM i security analysis and recommendations |
| `employee-info` | Employee Info Agent | Sample employee information queries |
| `web-search` | Web Search Agent | Web search using DuckDuckGo (requires `ddgs`) |
| `agno-assist` | Agno Assist | Agno framework help (requires `ddgs`, knowledge disabled) |

## Available Teams

| Team ID | Name | Description |
|---------|------|-------------|
| `ptf-team` | PTF Specialist Team | PTF specialist team for maintenance analysis |
| `performance-routing` | Performance Routing Team | Routes performance questions to appropriate specialists |
| `performance-coordination` | Performance Coordination Team | Coordinated performance analysis across specialists |
| `performance-collaboration` | Performance Collaboration Team | Full collaboration for comprehensive performance analysis |

## Available Workflows

| Workflow ID | Name | Description |
|-------------|------|-------------|
| `quick-performance` | Quick Performance Check | Fast performance overview with key system metrics |
| `comprehensive-analysis` | Comprehensive Analysis | Full performance analysis with quality checks |
| `iterative-analysis` | Iterative Analysis | Iterative performance analysis with refinement loops |

## Model Selection

Specify models using the format `provider:model_id`:

### OpenAI
```bash
--model-id openai:gpt-4o
--model-id openai:gpt-4o-mini
--model-id openai:gpt-4-turbo
```

### Anthropic
```bash
--model-id anthropic:claude-sonnet-4-5
```

### IBM watsonx
```bash
--model-id watsonx:mistralai/mistral-large
--model-id watsonx:meta-llama/llama-3-3-70b-instruct
--model-id watsonx:ibm/granite-3-8b-instruct
```

### Ollama (if configured)
```bash
--model-id ollama:qwen2.5
```

## Storage

- **Location**: `examples/agents-infra/tmp/agents.db`
- **Type**: SQLite
- **Persistence**: Chat history and session state are saved between runs
- **Cleanup**: Delete `tmp/agents.db` to clear all history

## Differences from Docker Deployment

### What Works Differently

1. **Storage Backend**: SQLite instead of PostgreSQL
2. **Knowledge Base**: Disabled for agents that use pgvector (e.g., agno-assist)
3. **Dependencies**: Optional agent/team/workflow dependencies are skipped if not installed
4. **Workflow Interaction**: Single input via `--prompt` parameter (not interactive)

### What Works the Same

- All agent, team, and workflow tools and capabilities
- Multi-agent team collaboration
- Multi-step workflow execution
- Model selection
- Chat history and memory
- Tool execution
- Streaming responses (agents and teams)

## Implementation Details

### Database Factory Pattern

The CLI uses a database factory (`db/factory.py`) that:
- Checks the `USE_SQLITE` environment variable
- Returns `SqliteDb` for CLI mode
- Returns `PostgresDb` for Docker mode
- Prevents PostgreSQL import errors when running locally

### Agent Loading

Agents are imported with error handling:
- Missing dependencies are caught and logged
- Agents with errors are excluded from the registry
- CLI continues to work with available agents

## Examples

### Performance Monitoring

```bash
python cli.py --agent metrics --stream
# Then ask: "What is the current CPU utilization?"
```

### PTF Management

```bash
python cli.py --agent ptf --model-id watsonx:mistralai/mistral-large
# Then ask: "Check the PTF currency status"
```

### Security Analysis

```bash
python cli.py --agent security --debug
# Then ask: "Are there any exposed user profiles?"
```

### Team Collaboration

```bash
python cli.py --team performance-collaboration --stream
# Then ask: "Analyze the current system performance and identify bottlenecks"
```

### Workflow Execution

```bash
python cli.py --workflow comprehensive-analysis --prompt "Perform a complete performance analysis and generate a detailed report" --debug
# Workflow executes all steps automatically and displays results
```

## Troubleshooting

### Agent, Team, or Workflow Not Listed

If an agent doesn't appear in `--list-agents`, a team in `--list-teams`, or a workflow in `--list-workflows`, check for:
- Missing dependencies (warnings shown on startup)
- Import errors in the agent file
- Run with `--debug` for more information

### Model Not Found

Ensure your API keys are configured:
- OpenAI: `OPENAI_API_KEY`
- Anthropic: `ANTHROPIC_API_KEY`
- watsonx: `WATSONX_API_KEY`, `WATSONX_PROJECT_ID`

### IBM i Connection Issues

Some agents require IBM i database connection:
- Set `HOST`, `DB_USER`, `PASSWORD`, `DB_PORT` in `.env`
- Ensure Mapepire server is accessible

## Architecture

```
cli.py
├── Sets USE_SQLITE=true
├── Imports agent factories
├── Creates agent registry
└── Runs agent.cli_app()

db/factory.py
├── get_database() → SqliteDb or PostgresDb
└── get_knowledge_base() → None (SQLite) or Knowledge (PostgreSQL)

agents/*.py
└── Use get_database() for storage
```

## Future Enhancements

Potential improvements:
- Interactive workflow mode (currently single input only)
- Custom database path configuration
- Agent/team/workflow-specific configuration files
- Plugin system for additional agents/teams/workflows
- Workflow result persistence and retrieval
