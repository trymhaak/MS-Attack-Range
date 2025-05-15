#!/bin/bash
# Script to destroy the MS-Attack-Range

echo "Starting MS-Attack-Range destruction at $(date)"

# Navigate to the terraform directory
cd "$(dirname "$0")/../terraform"

# Destroy the Terraform infrastructure
terraform destroy -auto-approve

echo "MS-Attack-Range destruction completed at $(date)"

# Optional: Send notification that destruction is complete
# Replace with your preferred notification method (email, Slack, etc.)
# mail -s "MS-Attack-Range Destroyed" your-email@example.com <<< "The MS-Attack-Range has been destroyed to save costs."
