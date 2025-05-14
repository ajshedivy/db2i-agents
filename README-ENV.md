# Environment Configuration for Db2i AI Agents

This simple approach helps you manage database credentials and API keys across multiple examples without duplicating sensitive information.

## Setup Instructions

### 1. Create Your Central Configuration

```bash
# Copy the template file
cp config/env.sample config/.env.central

# Edit with your credentials
nano config/.env.central  # or use your preferred editor
```

### 2. Using Configuration in Examples

When you want to run an example, use the provided script to copy the configuration:

```bash
# Navigate to the example directory
cd examples/sample

# Run the setup script (available in the examples directory)
../use-env.sh

# Now the example has its own .env file with your credentials
```

### What This Does

The `use-env.sh` script:
- Looks for a central configuration file in the `config/` directory
- Creates a local copy of that configuration in the current directory
- Always overwrites any existing `.env` file to ensure the latest settings are used

## Benefits of This Approach

- **Simple**: No symlinks, complex scripting, or dependencies required
- **Portable**: Works on all operating systems (Windows, macOS, Linux)
- **Flexible**: Each example can modify its local `.env` file if needed (but changes will be lost when use-env.sh is run again)
- **Secure**: Your credentials remain in your local repository only

## After Updating Central Config

If you update your central configuration, simply run the script again in each example directory where you want to use the new settings:

```bash
../use-env.sh
```

## Cleaning Up

To remove a local configuration:

```bash
# Simply delete the .env file
rm .env
```

## Note About MCP Framework

The MCP server requires a different configuration approach and is not managed by this simple script. Please refer to the MCP documentation for setup instructions.