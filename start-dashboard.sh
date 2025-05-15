#!/bin/bash
# Simple script to start the MS-Attack-Range Dashboard
# This makes it easy for team members to launch the dashboard without any coding knowledge

echo "Starting MS-Attack-Range Dashboard..."

# Make the Python script executable
chmod +x dashboard/serve.py

# Run the dashboard server
python3 dashboard/serve.py

# Note: The server will automatically open a browser window with the dashboard
