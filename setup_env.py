#!/usr/bin/env python3
"""
Db2i Agents Environment Setup

This script helps configure database credentials across all examples and agent frameworks
in the repository. It creates a central configuration file and links it to all relevant 
directories, eliminating the need to manage multiple .env files.

Usage:
    python setup_env.py

Note: The MCP server has different configuration requirements and is not handled by this script.
"""

import os
import sys
import shutil
import platform
from pathlib import Path
import getpass
import glob

# Banner and welcome
def print_banner():
    print("""
╔═══════════════════════════════════════════════════╗
║                                                   ║
║  🤖 Db2 for i AI Agents - Environment Setup 🤖    ║
║                                                   ║
╚═══════════════════════════════════════════════════╝
    """)

print_banner()
print("This script will help you set up database credentials for all examples and frameworks.")
print("Your configuration will be stored in a central location and linked to all examples.\n")

# Check if running on Windows
is_windows = platform.system() == "Windows"
if is_windows:
    print("⚠️  Windows detected. Symbolic links require administrator privileges.")
    print("   Please run this script as administrator if you encounter permission errors.\n")

# Get user input for credentials with defaults
def get_input(prompt, default="", password=False):
    if default:
        prompt = f"{prompt} [{default}]: "
    else:
        prompt = f"{prompt}: "
    
    if password:
        value = getpass.getpass(prompt)
    else:
        value = input(prompt)
    
    return value if value else default

# Get credentials
host = get_input("Enter Db2i host")
user = get_input("Enter database username")
password = get_input("Enter database password", password=True)
port = get_input("Enter port", "8076")
schema = get_input("Enter schema", "SAMPLE")
readonly = get_input("Set readonly mode? (TRUE/FALSE)", "TRUE")

api_key_providers = {
    "OpenAI": "OPENAI_API_KEY",
    "Anthropic": "ANTHROPIC_API_KEY",
    "IBM watsonx.ai": "IBM_CLOUD_API_KEY"
}

print("\nWhich AI providers would you like to configure? (Leave blank to skip)")
ai_provider_keys = {}
for provider, env_var in api_key_providers.items():
    answer = get_input(f"Configure {provider}? (y/n)", "n").lower()
    if answer == "y":
        ai_provider_keys[env_var] = get_input(f"Enter {provider} API key", password=True)

# Create central config directory
config_dir = Path("config")
config_dir.mkdir(exist_ok=True)

# Create central .env file
env_content = f"""# Db2 for i database credentials
HOST={host}
DB_USER={user}
PASSWORD={password}
PORT={port}
SCHEMA={schema}
READONLY={readonly}
"""

# Add AI provider API keys
for env_var, api_key in ai_provider_keys.items():
    env_content += f"\n# {env_var}\n{env_var}={api_key}\n"

central_env = config_dir / ".env.central"
with open(central_env, "w") as f:
    f.write(env_content)

print(f"\n✅ Created central configuration at {central_env}")

# Create sample .env.sample file showing the format but without credentials
sample_content = """# Db2 for i database credentials
HOST=your_host_name
DB_USER=your_username
PASSWORD=your_password
PORT=8076
SCHEMA=SAMPLE
READONLY=TRUE

# AI provider API keys (uncomment and add your keys as needed)
# OPENAI_API_KEY=your_openai_key
# ANTHROPIC_API_KEY=your_anthropic_key
# IBM_CLOUD_API_KEY=your_ibm_cloud_key
"""

sample_env = config_dir / "env.sample"
with open(sample_env, "w") as f:
    f.write(sample_content)

# Discover directories that need .env files
print("\n🔍 Scanning repository for examples and frameworks...")

# Define base directories to search
base_dirs = [
    "examples",
]

# Exclude MCP directories
exclude_dirs = [
    "examples/shared"
]

# Find all directories with Python files or with existing .env.sample files
env_dirs = []

for base_dir in base_dirs:
    base_path = Path(base_dir)
    if not base_path.exists():
        continue
        
    # Look for directories with Python files
    for py_file in glob.glob(f"{base_dir}/**/*.py", recursive=True):
        dir_path = os.path.dirname(py_file)
        
        # Skip excluded directories
        if any(ex_dir in dir_path for ex_dir in exclude_dirs):
            continue
            
        env_dirs.append(dir_path)
    
    # Also look for directories with .env.sample files
    for env_sample in glob.glob(f"{base_dir}/**/.env.sample", recursive=True):
        dir_path = os.path.dirname(env_sample)
        
        # Skip excluded directories
        if any(ex_dir in dir_path for ex_dir in exclude_dirs):
            continue
            
        env_dirs.append(dir_path)

# Unique directories
env_dirs = sorted(set(env_dirs))

# Create symbolic links or copy the central .env file
print(f"\n🔗 Setting up environment files in {len(env_dirs)} directories...\n")

success_count = 0
skip_count = 0
error_count = 0

for directory in env_dirs:
    dir_path = Path(directory)
    target_env = dir_path / ".env"
    
    # Skip if excluded
    if any(ex_dir in directory for ex_dir in exclude_dirs):
        print(f"⏩ Skipping excluded directory: {directory}")
        skip_count += 1
        continue
    
    try:
        # Remove existing .env file or symlink
        if target_env.exists() or os.path.islink(str(target_env)):
            os.remove(target_env)
        
        if is_windows:
            # On Windows, copy the file instead of symlinking
            shutil.copy2(central_env, target_env)
        else:
            # Create relative symlink on Unix-like systems
            rel_path = os.path.relpath(central_env, dir_path)
            os.symlink(rel_path, target_env)
        
        print(f"✅ Configured environment for {directory}")
        success_count += 1
    except Exception as e:
        print(f"❌ Error configuring {directory}: {e}")
        error_count += 1

print(f"\n📊 Configuration summary:")
print(f"   - {success_count} directories configured successfully")
print(f"   - {skip_count} directories skipped")
print(f"   - {error_count} directories had errors")

if error_count > 0:
    print("\n⚠️  Some directories could not be configured. See errors above.")
    
print("\n🚀 Setup complete!")
print("You can now run any example without configuring individual .env files.")
print("If you need to update your credentials, simply run this script again,")
print("or edit the central configuration file at config/.env.central")

print("\n⚠️  Note: MCP framework uses a different configuration approach and is not")
print("   managed by this script. Please configure it separately.")

# Check for example directories without configurations
all_example_dirs = []
for base_dir in ["examples", "frameworks"]:
    for root, dirs, files in os.walk(base_dir):
        has_py = any(f.endswith('.py') for f in files)
        if has_py:
            all_example_dirs.append(root)

missing_dirs = set(all_example_dirs) - set(env_dirs)
if missing_dirs and not any(d.startswith(tuple(exclude_dirs)) for d in missing_dirs):
    print("\n⚠️  Some directories with Python files weren't configured:")
    for d in sorted(missing_dirs):
        print(f"   - {d}")
    print("   You may need to configure these manually if they need database access.")