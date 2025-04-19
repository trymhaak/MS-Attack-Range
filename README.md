# MS-Attack-Range
Microsoft Sentinel Attack Range

# Overview of the MS-Attack-Range
The Microsoft Sentinel Attack Range is a tool that allows security teams to create a small lab environment to simulate attacks and generate data in Microsoft Sentinel for detection testing and validation. It allows you to:

Deploy a complete Azure infrastructure using Terraform
- Set up a simulated network with Windows and Linux machines
- Configure Microsoft Sentinel for logging and monitoring
- Run attack simulations based on MITRE ATT&CK techniques
- Test detection capabilities in Microsoft Sentinel

A modular and automated deployment solution for setting up and testing Microsoft Sentinel detection capabilities against simulated attack scenarios.

![image](https://github.com/user-attachments/assets/0bdb9e6a-1371-461c-9411-c89ae4b31dba)


## Overview

The Microsoft Sentinel Attack Range is a framework for security professionals to:

- Deploy a controlled, isolated environment in Azure cloud
- Generate security events from simulated attacks based on MITRE ATT&CK techniques
- Test and validate Microsoft Sentinel detection rules and analytics
- Improve security monitoring capabilities and incident response procedures

## Components

- **Windows Domain Controller**: A Windows Server virtual machine configured as a domain controller
- **Windows Workstation**: A Windows 10 machine joined to the domain
- **Kali Linux**: An attack machine preloaded with security testing tools
- **Microsoft Sentinel**: A cloud-native SIEM and SOAR solution for security monitoring
- **Attack Simulation Framework**: Ansible-based attack automation using Atomic Red Team tests
- **Data Collection Rules**: Automated log collection from all VMs
- **Attack Simulation Framework**: Ansible-based attack automation using Atomic Red Team tests
- **Data Connectors**: 5 pre-configured data sources (Windows Events, Syslog, Microsoft Defender for Endpoint, Entra ID, Microsoft XDR)

## Prerequisites

- Azure subscription with Contributor and Security Admin permissions
- Terraform 1.0.0+
- Python 3.7+
- Ansible 2.9+
- Azure CLI (for newbie)
- SSH key pair for accessing Linux machines
- At least 12 vCPUs available in your subscription for the VMs

  If you're using a service principal for deployment, ensure it has these role assignments.

## Quick Start

1. **Clone the repository**
   ```
   git clone https://github.com/oloruntolaallbert/MS-Attack-Range
   cd ms-attack-range
   ```

2. **Set up your environment**
   ```
   ./Setup.sh
   ```

3. **Configure your deployment**
   - Edit `terraform/terraform.tfvars` with your specific settings
   - Edit `attack-range.yml` to configure attack scenarios
Security Considerations:
- Change default passwords in terraform.tfvars before deployment
- The current NSG allows RDP (3389) and SSH (22) from any source - restrict to specific IPs
- Rotate SSH keys periodically

4. **Build the attack range**
   ```
   python attack-range.py build
   ```

5. **Run attack simulations**
   ```
   # Run a predefined attack sequence
   python attack-range.py sequence -s recon
   
   # Run an individual attack
   python attack-range.py attack -a network_discovery
   ```

6. **Destroy the environment when finished**
   ```
   python attack-range.py destroy
   ```

## Architecture

The Microsoft Sentinel Attack Range deploys a complete Azure infrastructure:

- Virtual Network with appropriate subnets
- Network Security Groups with controlled access
- Virtual Machines for Windows and Linux systems
- Log Analytics Workspace and Microsoft Sentinel
- Data collection rules and analytics

## Attack Techniques

The attack range supports various MITRE ATT&CK techniques:

| Category | Supported Techniques |
|----------|----------------------|
| Discovery | Process Discovery, Network Discovery, Account Discovery, System Info Discovery |
| Credential Access | Credential Dumping, Brute Force, Mimikatz |
| Execution | PowerShell, Command Shell, Scheduled Tasks |
| Persistence | Registry Run Keys, Scheduled Tasks, Startup Folder |
| Defense Evasion | Timestomp, Clear Logs, Disable Defender |
| Network | Network Scanning, Port Scanning, SMB Scanning |

## Attack Sequences

Pre-configured attack sequences are available:

- **recon**: Basic reconnaissance techniques
- **credential_theft**: Credential-focused attacks
- **persistence**: Techniques for maintaining access
- **full_chain**: Complete attack chain simulation
- **cross_platform**: Attacks targeting both Windows and Linux
- **network_recon**: Network-based discovery techniques

## Analytics Rules

The deployment includes pre-configured Microsoft Sentinel analytics rules for detecting:

- Brute force attempts
- Credential dumping
- Suspicious PowerShell execution
- Scheduled task creation
- Registry persistence
- Process discovery
- Log clearing
- Network discovery

## Security Note

This project creates intentionally vulnerable environments for security testing. Always deploy in isolated environments and never connect to production networks or use production credentials.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License



## Acknowledgments

- Inspired by the [Splunk Attack Range](https://github.com/splunk/attack_range)
- Uses [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team) for attack simulation
- Built with Terraform, Ansible, and Python
  
