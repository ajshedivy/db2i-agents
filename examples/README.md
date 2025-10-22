# 💡 Db2 for i AI Examples

This directory contains practical, ready-to-run examples that demonstrate how to use AI with Db2 for i databases. From simple scripts to complete applications, these examples provide clear starting points for your own AI projects.

## 🚨 Before You Start

**Have you completed the main setup?** These examples require the environment setup from the main README.

✅ **Required**: Complete the [Getting Started guide](../README.md#-getting-started) first, which covers:
- Setting up Mapepire on IBM i
- Creating your `.env` file with database credentials  
- Installing uv package manager
- Choosing your AI model provider

If you haven't done this yet, **stop here** and complete the main setup first.

## 🧪 Example Categories

### ⭐ **NEW: `agents-infra/` - Production-Ready Agno AgentOS Implementation**

The **primary examples** are now in `agents-infra/`, which implements [Agno's AgentOS](https://docs.agno.com/agent-os/introduction) framework. This provides a complete multi-agent platform with:

- 🤖 **7 Individual Agents** - Specialized agents for different IBM i tasks
- 👥 **4 Multi-Agent Teams** - Collaborative agent teams with routing and coordination
- 🔄 **3 Multi-Step Workflows** - Automated pipeline execution for complex analysis
- 🐳 **Docker Deployment** - Full AgentOS server with PostgreSQL and pgvector
- 💻 **CLI Alternative** - Run agents/teams/workflows locally without Docker

**Quick Start Options:**

1. **CLI (Recommended for Quick Testing)**
   ```bash
   cd agents-infra
   python cli.py --list-agents      # List available agents
   python cli.py --list-teams       # List available teams
   python cli.py --list-workflows   # List available workflows

   # Run an agent
   python cli.py --agent metrics --stream

   # Run a team
   python cli.py --team performance-collaboration --stream

   # Run a workflow
   python cli.py --workflow comprehensive-analysis --prompt "Analyze system performance"
   ```

2. **Docker AgentOS (Recommended for Production)**
   ```bash
   cd agents-infra
   docker-compose up
   # Access at http://localhost:8000
   ```

📖 **Documentation:**
- [`agents-infra/CLI_README.md`](agents-infra/CLI_README.md) - Detailed CLI documentation
- [`agents-infra/README.md`](agents-infra/README.md) - Full AgentOS deployment guide

---

### 📂 Available Agents, Teams, and Workflows

#### **Agents** (`agents-infra/agents/`)

| Category | Agent | Description | CLI Command |
|----------|-------|-------------|-------------|
| **Demo** | Web Search | Search the web using DuckDuckGo | `--agent web-search` |
| **Demo** | Agno Assist | Agno framework documentation assistant | `--agent agno-assist` |
| **Performance** | Metrics Assistant | IBM i performance metrics and monitoring | `--agent metrics` |
| **Services** | PTF Assistant | PTF (Program Temporary Fix) management | `--agent ptf` |
| **Services** | Storage Assistant | IFS storage analysis and optimization | `--agent storage` |
| **Security** | Security Assistant | Security vulnerability assessment | `--agent security` |
| **Sample** | Employee Info | Sample database queries | `--agent employee-info` |

#### **Teams** (`agents-infra/teams/`)

| Team | Type | Description | CLI Command |
|------|------|-------------|-------------|
| PTF Specialist Team | Routing | Routes PTF-related queries to specialists | `--team ptf-team` |
| Performance Routing | Routing | Routes performance questions to appropriate agents | `--team performance-routing` |
| Performance Coordination | Coordination | Coordinated analysis across multiple agents | `--team performance-coordination` |
| Performance Collaboration | Collaboration | Full collaboration for comprehensive analysis | `--team performance-collaboration` |

#### **Workflows** (`agents-infra/workflows/`)

| Workflow | Steps | Description | CLI Command |
|----------|-------|-------------|-------------|
| Quick Performance Check | 2 steps | Fast performance overview with key metrics | `--workflow quick-performance` |
| Comprehensive Analysis | 4 steps | Full performance analysis with quality checks | `--workflow comprehensive-analysis` |
| Iterative Analysis | Loop-based | Iterative performance analysis with refinement | `--workflow iterative-analysis` |

---

### 📚 Legacy Examples (`agents/` - Reference Only)

> **⚠️ DEPRECATED:** The `agents/` directory contains legacy examples for **reference only**.
>
> **For new development, use `agents-infra/`** which provides:
> - Better architecture with Agno AgentOS
> - Multi-agent team support
> - Production deployment options
> - Local CLI and Docker deployment

#### Sample Database Examples (Legacy)
- 👥 [Employee Information Retrieval](agents/sample/get_employee_info_agent.py) - Simple agent that queries employee data
- 🔄 [Employee Info Workflow](agents/sample/get_employee_info_workflow.py) - LangChain workflow for employee data analysis
- 🔌 [Simple MCP Database Client](agents/sample/mcp_simple.py) - Basic MCP client for database queries

#### Performance Monitoring Examples (Legacy)
- 📈 [Metrics Assistant CLI](agents/performance/metrics_assistant_cli.py) - Interactive CLI for system performance metrics
- 🔍 [SQL Examples RAG](agents/performance/sql_examples_rag.py) - Retrieval-augmented generation for SQL performance

#### Security Examples (Legacy)
- 🛡️ [Security Assistant](agents/security/security_assistant.py) - Interactive CLI for security vulnerability analysis
- 📝 [Security Agent Playground](agents/security/playground.py) - Testing environment for security analysis

#### IBM i Services Examples (Legacy)
- 🔍 [PTF Information Retrieval](agents/services/ptf/get_ptf_info.py) - Basic PTF information retrieval
- 🔬 [Enhanced PTF Analysis](agents/services/ptf/get_ptf_info_extended.py) - Detailed PTF information with enhanced AI
- 📂 [IFS File Reader](agents/services/ifs/read_stream_file.py) - Read and search IFS file contents
- 💾 [IFS Storage Analyzer](agents/services/ifs/storage_assistant.py) - Find and analyze large files
- ☕ [JVM Performance Monitor](agents/services/java/jvm_assistant.py) - Monitor Java Virtual Machines on IBM i
- 🗃️ [SQL Services Agent](agents/services/sql_services_agent.py) - Interactive CLI for SQL services
- 📓 [SQL Services Info Notebook](agents/services/sql_services_info.ipynb) - Jupyter notebook for SQL services

#### Complete Applications (Legacy)
- 🧠 [SQL Agent with Knowledge Base](apps/sql_agent_with_knowledge/) - Interactive SQL assistant with database knowledge

---

## 🚀 Running the Examples

### AgentOS Examples (Recommended)

```bash
cd agents-infra

# List what's available
python cli.py --list-agents
python cli.py --list-teams
python cli.py --list-workflows

# Run an agent
python cli.py --agent metrics

# Run a team
python cli.py --team performance-routing

# Run a workflow
python cli.py --workflow quick-performance --prompt "Check system status"
```

### Legacy Examples (Reference)

```bash
cd agents/sample/  # or your chosen example directory
uv run <script_name>.py
```

The examples will automatically find your root `.env` file with database credentials.

## 📁 Directory Structure

```
examples/
├── agents-infra/              ⭐ PRIMARY - Production-ready Agno AgentOS implementation
│   ├── agents/                # Individual specialized agents
│   ├── teams/                 # Multi-agent teams
│   ├── workflows/             # Multi-step workflows
│   ├── cli.py                 # CLI for local execution
│   ├── compose.yaml           # Docker deployment
│   └── CLI_README.md          # CLI documentation
├── agents/                    ⚠️  DEPRECATED - Legacy examples (reference only)
│   ├── sample/                # Examples using the SAMPLE database
│   ├── performance/           # Performance monitoring examples
│   ├── security/              # Security assessment tools
│   └── services/              # Examples using IBM i services
│       ├── ifs/               # Integrated File System tools
│       ├── java/              # Java and JVM monitoring tools
│       └── ptf/               # PTF information services
└── apps/                      # Complete application examples
    └── sql_agent_with_knowledge/   # SQL agent with knowledge base
```

## 📚 Learning Path

**Recommended path for new users:**

### 1️⃣ **Start with AgentOS CLI** (5 minutes)
```bash
cd agents-infra
python cli.py --agent employee-info
# Ask: "Who are the employees in department D11?"
```
**Learn:** Basic agent interaction

### 2️⃣ **Try a Performance Agent** (10 minutes)
```bash
python cli.py --agent metrics --stream
# Ask: "What is the current CPU utilization?"
```
**Learn:** How agents interact with IBM i system services

### 3️⃣ **Explore Multi-Agent Teams** (15 minutes)
```bash
python cli.py --team performance-collaboration --stream
# Ask: "Analyze the current system performance and identify bottlenecks"
```
**Learn:** How multiple agents collaborate

### 4️⃣ **Run an Automated Workflow** (10 minutes)
```bash
python cli.py --workflow comprehensive-analysis --prompt "Perform a full performance analysis"
```
**Learn:** Multi-step automated execution

### 5️⃣ **Deploy with Docker** (Optional - for production)
```bash
docker-compose up
# Access AgentOS at http://localhost:8000
```
**Learn:** Production deployment with FastAPI server

### 6️⃣ **Explore Legacy Examples** (Reference)
Review `agents/` directory for alternative implementation patterns