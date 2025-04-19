#!/bin/bash
# Microsoft Sentinel Attack Range Setup Script

echo "=== Microsoft Sentinel Attack Range Setup ==="
echo "This script will help you set up your environment for MS Attack Range."

# Check for Python
if ! command -v python3 &>/dev/null; then
    echo "Python 3 is required but not found. Please install Python 3.7 or later."
    exit 1
fi

# Check for Terraform
if ! command -v terraform &>/dev/null; then
    echo "Terraform is required but not found. Please install Terraform 1.0.0 or later."
    exit 1
fi

# Check for Ansible
if ! command -v ansible &>/dev/null; then
    echo "Ansible is required but not found. Please install Ansible 2.9 or later."
    exit 1
fi

# Check for Azure CLI
if ! command -v az &>/dev/null; then
    echo "Azure CLI is required but not found. Please install Azure CLI."
    exit 1
fi

# Install Python requirements
echo "Installing Python requirements..."
pip install -r requirements.txt

# Check if terraform.tfvars exists
if [ ! -f "terraform/terraform.tfvars" ]; then
    echo "terraform.tfvars not found. Creating from template..."
    cp terraform/terraform.tfvars.example terraform/terraform.tfvars
    echo "Please edit terraform/terraform.tfvars to add your SSH public key and other preferences."
fi

# Check if attack-range.yml exists
if [ ! -f "attack-range.yml" ]; then
    echo "attack-range.yml not found. Creating from template..."
    cp attack-range.yml.example attack-range.yml
    echo "Please edit attack-range.yml to configure your environment."
fi

# Check Azure login status
echo "Checking Azure login status..."
az account show &>/dev/null
if [ $? -ne 0 ]; then
    echo "You need to log in to Azure. Running 'az login'..."
    az login
fi

echo "Getting Azure subscription information..."
SUBSCRIPTION_ID=$(az account show --query id -o tsv)
echo "Your Azure subscription ID is: $SUBSCRIPTION_ID"
echo "Please make sure this is set correctly in your attack-range.yml file."

# Generate SSH key if needed
if [ ! -f ~/.ssh/id_rsa ]; then
    echo "SSH key not found. Would you like to generate one? (y/n)"
    read generate_key
    if [[ $generate_key == "y" ]]; then
        ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""
        echo "SSH key generated. Public key:"
        cat ~/.ssh/id_rsa.pub
        echo "Please add this public key to terraform/terraform.tfvars"
    else
        echo "Please ensure you have an SSH key at ~/.ssh/id_rsa or update the path in attack-range.yml"
    fi
fi

echo ""
echo "Setup complete! You can now build your attack range with:"
echo "python attack-range.py build"
echo ""
echo "For more information and commands, run:"
echo "python attack-range.py --help"
