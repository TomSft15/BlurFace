#!/bin/bash
# debug_start.sh - Launch the app in debug mode

# Define the debug port
DEBUG_PORT=5678

echo "🔍 Starting application in debug mode on port $DEBUG_PORT"
echo "⏳ Waiting for VS Code debugger to attach..."

# Launch the app with debugpy
python -m debugpy --listen 127.0.0.1:$DEBUG_PORT --wait-for-client -m main

echo "✅ Debug session ended"