#!/bin/bash
# Simple script to copy the central .env file to the current directory

# Banner
echo "🔄 Db2i AI Agents - Environment Setup"
echo "======================================="

# Check if central config exists
CENTRAL_ENV="../../config/.env.central"
PARENT_CENTRAL_ENV="../config/.env.central"
LOCAL_ENV="./.env"

# Find the central .env file
if [ -f "$CENTRAL_ENV" ]; then
  SOURCE_ENV="$CENTRAL_ENV"
elif [ -f "$PARENT_CENTRAL_ENV" ]; then
  SOURCE_ENV="$PARENT_CENTRAL_ENV"
else
  echo "❌ Error: Central environment file not found!"
  echo "Please create one first:"
  echo "1. Copy config/env.sample to config/.env.central"
  echo "2. Edit config/.env.central with your credentials"
  exit 1
fi

# Always copy the central .env file to the current directory
cp -f "$SOURCE_ENV" "$LOCAL_ENV"

if [ $? -eq 0 ]; then
  echo "✅ Successfully copied environment configuration"
  echo "Environment is now set up for this example!"
else
  echo "❌ Failed to copy environment configuration"
  exit 1
fi