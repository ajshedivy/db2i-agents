# IBM i Services Examples

This directory contains samples demonstrating how to use IBM i Services with AI agents to access and analyze system information.

## Setup Instructions

1. **Important**: First, run the environment setup script from the parent directory:
   ```bash
   cd ../examples/ # Navigate to the examples directory
   ./setup_env.sh
   cd ibmi-services
   ```
   This will create a `.env` file template in the examples directory.

2. (Optional) create the `.env` file in the `ibmi-services` directory with your specific credentials:
   ```
   HOST=your_ibmi_host
   DB_USER=your_username
   PASSWORD=your_password
   DB_PORT=your_db_port
   OPENAI_API_KEY=your_openai_api_key
   ```
   this will overwrite the `.env` file created in the parent directory.

## Available Examples

### PTF (Program Temporary Fix) Services

The PTF directory contains utilities to check PTF status and availability on IBM i systems:

#### Simple PTF Currency Check

Checks the current PTF group currency levels on your IBM i system.

```bash
cd ptf
uv run get_ptf_info.py
```

This script will:
- Determine your IBM i OS version and release level
- Show PTF groups with available updates
- Display the difference between installed and available PTF levels

#### Extended PTF Missing Check

Checks for specific missing PTFs within PTF groups.

```bash
cd ptf
uv run get_ptf_info_extended.py
```

This script:
- Provides an AI assistant for checking missing PTFs
- Allows querying specific PTF groups including:
  - SF99675 (Hardware and related PTFs)
  - SF99737 (Technology Refresh)
  - SF99739 (Group HIPER)
  - SF99738 (Group Security)
  - SF99704 (DB2 for IBM i)
  - And more

## Requirements

- Access to an IBM i system
- Python 3.x
- Environment setup with required dependencies
- OpenAI API key (for AI-assisted analysis)
- mapepire-python package (for IBM i database connectivity)