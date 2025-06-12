# 🔒 Security Assistant Examples

This directory contains examples that demonstrate how to use AI agents to analyze and improve security on IBM i systems. These examples leverage SQL services to identify and address security vulnerabilities.

## 📋 Available Examples

| Example | Description | Difficulty |
|---------|-------------|------------|
| 🛡️ [Security Assistant](security_assistant.py) | Interactive CLI for analyzing security vulnerabilities | Intermediate ⭐⭐ |
| 📝 [Security Agent Playground](playground.py) | Testing environment for security analysis capabilities | Beginner ⭐ |
| 🤖 [Agent](agent.py) | Core security analysis agent implementation | Intermediate ⭐⭐ |
| 📓 [Security Test Notebook](test_security_assistant.ipynb) | Jupyter notebook for testing security analysis | Beginner ⭐ |

## 🚀 Running the Examples

### Prerequisites

- Python 3.9+
- The `uv` package manager
- Access to a Db2 for i database with appropriate permissions
- Mapepire service running on your IBM i system

### Environment Setup

1. **Important**: First, run the environment setup script from the parent directory:
   ```bash
   cd ../../examples/ # Navigate to the examples directory 
   ./setup_env.sh
   cd agents/security
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
What tools do you have access to?   - List available tools and capabilities
check exposed profiles              - Check for user profiles with insufficient security
analyze user authorities            - Review user profile authorities and permissions
security audit                      - Perform comprehensive security audit
how can I fix the profiles          - Generate commands to fix security issues
fix them for me                     - Allow the agent to fix the vulnerabilities
system security status              - Get overall system security assessment
exit                                - Exit the application
```

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

### 🤖 Core Agent

Run the core security agent implementation:

```bash
uv run agent.py
```

### 📓 Security Test Notebook

Open the Jupyter notebook for interactive security testing:

```bash
jupyter notebook test_security_assistant.ipynb
```

## 🔍 Example Details

### 🛡️ Security Assistant

This example demonstrates:
- Interactive CLI for security analysis
- User profile vulnerability detection
- Authority and permission analysis
- Automated fix generation
- Real-time security monitoring

**Key Features:**
- Exposed profile detection
- Authority analysis
- Security recommendation engine
- Automated remediation commands
- Compliance checking

### 📝 Security Agent Playground

This example provides:
- Chat-based security analysis interface
- Visual security assessment tools
- Interactive vulnerability exploration
- Real-time security insights

### 🤖 Agent Implementation

Core security agent featuring:
- Modular security analysis components
- Extensible vulnerability detection
- Custom security rule engine
- Integration with IBM i security services

### 📓 Test Notebook

Jupyter notebook for:
- Interactive security testing
- Vulnerability analysis workflows
- Security metric visualization
- Educational security exploration

## 📚 Security Monitoring Resources

These examples use IBM i SQL services for security monitoring. Check out the raw SQL queries used in the examples:
- [User Profile attacks and Corrective measures](sql/User%20profiles%20exposed%20to%20attack%20and%20corrective%20measures.sql)

## 🛡️ Security Analysis Areas

These examples cover multiple security aspects:

### User Profile Security
- Exposed profiles detection
- Default password analysis
- Inactive user identification
- Special authority review

### Authority Management
- Public authority assessment
- Excessive privilege detection
- Authority inheritance analysis
- Object-level permissions

### System Security
- Security policy compliance
- Audit configuration review
- System value analysis
- Network security assessment

### Compliance Monitoring
- Regulatory compliance checking
- Security baseline validation
- Change tracking and monitoring
- Risk assessment reporting

## 🛠️ Customizing Examples

Each example can be customized by:

1. **Database Connection**: Modify connection details in the `.env` file
2. **Security Rules**: Add custom security checks and policies
3. **AI Model Configuration**: Adjust model parameters for analysis
4. **CLI Functionality**: Extend command capabilities
5. **Reporting**: Customize security report formats
6. **Integration**: Connect with external security tools

### Example Customizations:

```python
# Add custom security checks
CUSTOM_SECURITY_CHECKS = [
    "SELECT * FROM QSYS2.USER_INFO() WHERE DAYS_UNTIL_PASSWORD_EXPIRES < 7",
    "SELECT * FROM QSYS2.OBJECT_PRIVILEGES WHERE OBJECT_AUTHORITY = '*ALL'"
]

# Configure security thresholds
SECURITY_THRESHOLDS = {
    "max_exposed_profiles": 5,
    "password_expiry_warning": 14,
    "inactive_user_days": 90
}
```

## 🎯 Security Best Practices

When using these examples:

1. **Regular Audits**: Schedule regular security assessments
2. **Least Privilege**: Follow principle of least privilege
3. **Monitoring**: Implement continuous security monitoring
4. **Documentation**: Maintain security configuration documentation
5. **Training**: Ensure team understanding of security policies

## 📈 Security Workflows

Typical security analysis workflows:

1. **Initial Assessment**: Run comprehensive security audit
2. **Vulnerability Identification**: Check for exposed profiles and excessive authorities
3. **Risk Analysis**: Assess impact and likelihood of security issues
4. **Remediation Planning**: Generate fix commands and procedures
5. **Implementation**: Apply security fixes with proper testing
6. **Monitoring**: Ongoing security monitoring and alerting

## 📌 Next Steps

After exploring these examples, you can:

1. Integrate security monitoring with performance analysis
2. Create automated security audit workflows
3. Build custom security dashboards
4. Develop compliance reporting tools
5. Explore other agent categories in the [performance](../performance/) or [services](../services/) directories

## 🚨 Important Security Notes

- **Permissions**: Ensure you have appropriate permissions for security analysis
- **Testing**: Always test security changes in non-production environments first
- **Backup**: Take appropriate backups before making security modifications
- **Compliance**: Verify changes align with organizational security policies
- **Documentation**: Document all security changes and their rationale

## 🤝 Contributing

To contribute new security examples:

1. Follow established security analysis patterns
2. Include comprehensive testing procedures
3. Document security implications clearly
4. Ensure compatibility with various IBM i security configurations
5. Provide clear usage examples and best practices