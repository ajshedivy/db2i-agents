# Agno Db2i Agent

A collection of agents for interacting with DB2i databases using the Agno framework. This package includes a command-line interface and a web-based playground for database exploration and querying.

## Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) for package management
- [Ollama](https://ollama.ai/) (optional, for local LLM support)
- [OpenAI API key](https://platform.openai.com/api-keys) (optional, for OpenAI model support)

## Run the Db2i Agent CLI

Install the dependencies:

- uv:  
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

- Install Ollama from [Ollama](https://ollama.com/)
---

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ajshedivy/db2i-agents.git
   cd db2i-agents/examples/agents/langchain
   ```
2. **Prepare Ollama model:**
    ```bash
    ollama pull qwen2.5:latest
    ```
3. **Run the CLI:**
    ```bash
    uv run agent.py
    ```
![alt text](images/image.png)

4. **Chat wth the agent**


### Demo
Once the agent is running, you can interact with it through the command line. You can ask questions about the database, and the agent will respond with relevant information.

here are some example queries you can try:
```text
What tables to I have access to?
which employee has the highest salary?
How many employees are in each department?
```

Here is quick demo of the agent in debug mode to show the tool calls and thinking process:


