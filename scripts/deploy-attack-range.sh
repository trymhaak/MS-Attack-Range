#!/bin/bash
# Script to deploy the MS-Attack-Range

echo "Starting MS-Attack-Range deployment at $(date)"

# Navigate to the terraform directory
cd "$(dirname "$0")/../terraform"

# Initialize and apply Terraform
terraform init
terraform apply -auto-approve

echo "MS-Attack-Range deployment completed at $(date)"

# Optional: Send notification that deployment is complete
# Replace with your preferred notification method (email, Slack, etc.)
# mail -s "MS-Attack-Range Deployed" your-email@example.com <<< "The MS-Attack-Range has been deployed and is ready for testing."
