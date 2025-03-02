#!/bin/bash
set -e

# Print Python version and path for debugging
echo "Python version:"
python --version
echo "Python path:"
python -c "import sys; print(sys.path)"

# Execute the Python script directly
cd /app
python /app/src/run_servers.py
