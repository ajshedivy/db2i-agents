# 🔒 Security Assistant Examples

This directory contains examples that demonstrate how to use AI agents to analyze and improve security on IBM i systems. These examples leverage SQL services to identify and address security vulnerabilities.

## 📋 Available Examples

| Example | Description | Difficulty |
|---------|-------------|------------|
| 🛡️ [Security Assistant](security_assistant.py) | Interactive CLI for analyzing security vulnerabilities | Intermediate ⭐⭐ |
| 📝 [Security Agent Playground](playground.py) | Testing environment for security analysis capabilities | Beginner ⭐ |

## 🚀 Running the Examples

### Prerequisites

- Python 3.9+
- The `uv` package manager
- Access to a Db2 for i database with appropriate permissions
- Mapepire service running on your IBM i system

### Environment Setup

1. **Important**: First, run the environment setup script from the parent directory:
   ```bash
   cd ../examples/ # Navigate to the examples directory 
   ./setup_env.sh
   cd security
   ```
   This will create a `.env` file template in the examples directory.

2. (Optional) create the `.env` file in the `security` directory with your specific credentials:
   ```
   HOST=your_ibmi_host
   DB_USER=your_username
   PASSWORD=your_password
   DB_PORT=your_db_port
   OPENAI_API_KEY=your_openai_api_key
   ```
   this will overwrite the `.env` file created in the parent directory.

### Running the Security Assistant

The Security Assistant provides an interactive interface for analyzing system security:

```bash
uv run security_assistant.py
```

You can customize the CLI with these options:

```bash
uv run security_assistant.py --model-id ollama:qwen2.5 --stream --debug
```

> 💡 **Note**: By default, this example uses OpenAI's GPT-4.1 model. You can specify a different model with `--model-id`.

### Example CLI Commands

Once the CLI is running, you can use these commands:

```
What tools do you have access to.  - list the tools the agent can use
check exposed profiles             - Check for user profiles with insufficient security
how can I fix the profiles         - Generate commands to fix security issues
fix them for me                    - Allow the agent to fix the vulnerabilities
exit                               - Exit the application
```




https://github.com/user-attachments/assets/a0b1e772-78d7-4b7b-8156-a8fb7fad939b




### 📝 Security Agent Playground

This example provides a chat UI testing environment for the security agent.

Follow these steps to run the playground:


1. Setup Agno agent playground:
   - Follow the instructions in the [Playground docs](https://docs.agno.com/introduction/playground)
   - Once the playground is setup, you can interact with the security agent in a chat-like interface.
2. Start the playground server:
   ```bash
   uv run playground.py
   ```




https://github.com/user-attachments/assets/8e7d932b-f47d-4446-95c7-655693b12005






## 📚 Security Monitoring Resources

These examples use IBM i SQL services for security monitoring. Key services include:

```sql
-- Check for exposed user profiles
SELECT COUNT(*)
FROM qsys2.object_privileges
WHERE system_object_schema = 'QSYS' 
   AND object_type = '*USRPRF' 
   AND object_name NOT IN ('QDBSHR', 'QDBSHRDO', 'QDOC', 'QTMPLPD') 
   AND user_name = '*PUBLIC' 
   AND object_authority <> '*EXCLUDE';
```

## 🛠️ Customizing Examples

Each example can be customized by:

1. Modifying the database connection details in the `.env` file
2. Adding new security checks and metrics
3. Adjusting the AI model parameters
4. Extending the CLI functionality

## 📌 Next Steps

After exploring these examples, you can:

1. Combine security monitoring with other IBM i services
2. Create automated security audit workflows
3. Build custom security dashboards
4. Explore performance examples in the [performance](../performance/) directory
