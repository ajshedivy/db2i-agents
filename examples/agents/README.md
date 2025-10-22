# 🤖 AI Agents for Db2 for i (Legacy)

⚠️ **Deprecated**: This directory contains legacy AI agent examples for Db2 for i. All of these agents have been updated and added to [IBM i Agents OS](../ibmi-agent-os/)


This directory contains AI agent examples organized by category, each demonstrating different approaches to using AI with IBM i systems and Db2 for i databases.

## 📂 Categories Overview

| Category | Description | Examples Count | Difficulty |
|----------|-------------|----------------|------------|
| 👥 [**sample/**](sample/) | Quick examples using the IBM SAMPLE database | 3 | Beginner ⭐ |
| 📊 [**performance/**](performance/) | System performance monitoring and analysis | 4 | Intermediate ⭐⭐ |
| 🔒 [**security/**](security/) | Security assessment and remediation tools | 2 | Intermediate ⭐⭐ |
| 🛠️ [**services/**](services/) | IBM i Services integration examples | 7 | Beginner to Advanced ⭐⭐⭐ |

## 🚀 Quick Start

### Prerequisites

- Python 3.9+ with the `uv` package manager
- Access to a Db2 for i database
- Mapepire service running on your IBM i system
- OpenAI API key (or other LLM provider)

### Environment Setup

1. **Important**: First, run the environment setup script from the parent directory:
   ```bash
   cd ../examples/ # Navigate to the examples directory 
   ./setup_env.sh
   cd agents
   ```

2. Choose a category directory and navigate to it
3. Follow the specific instructions in each category's README

## 📋 Example Categories

### 👥 Sample Database Examples
- **Purpose**: Learn basic AI agent concepts with familiar data
- **Database**: IBM SAMPLE database
- **Examples**: Employee info retrieval, workflow automation, MCP client
- **Best for**: Getting started with AI agents

### 📊 Performance Monitoring Examples  
- **Purpose**: Monitor and analyze IBM i system performance
- **Focus**: CPU, memory, jobs, Collection Services
- **Examples**: Interactive metrics CLI, RAG-enhanced SQL examples
- **Best for**: System administrators and performance analysts

### 🔒 Security Examples
- **Purpose**: Identify and remediate security vulnerabilities
- **Focus**: User profiles, authorities, system security
- **Examples**: Security assistant CLI, vulnerability analysis
- **Best for**: Security administrators and auditors

### 🛠️ Services Examples
- **Purpose**: Interact with various IBM i Services
- **Focus**: PTF management, IFS operations, JVM monitoring, SQL services
- **Examples**: File system tools, patch management, Java monitoring
- **Best for**: System administrators and developers

## 📚 Learning Path

For beginners, we recommend this progression:

1. **Start Simple**: Try the [sample/](sample/) examples to understand basic concepts
2. **Explore Services**: Move to [services/](services/) to see real system integration
3. **Monitor Performance**: Use [performance/](performance/) examples for system insights
4. **Secure Systems**: Apply [security/](security/) tools for vulnerability assessment

## 🔧 Common Features

All examples share these characteristics:

- **Interactive CLIs**: Most examples provide command-line interfaces
- **AI-Powered**: Uses LLMs for intelligent analysis and recommendations
- **Real-time Data**: Connects to live IBM i systems via Mapepire
- **Customizable**: Easy to modify for specific environments
- **Well-documented**: Clear setup and usage instructions

## 📌 Next Steps

After exploring these agent examples, you can:

1. Combine multiple examples for complex workflows
2. Build custom agents for your specific use cases
3. Explore the complete applications in the [../apps/](../apps/) directory
4. Contribute improvements or new examples to the repository

## 🤝 Contributing

Each category has its own README with specific contribution guidelines. Please follow the established patterns when adding new examples.