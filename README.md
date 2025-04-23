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

![image](https://github.com/user-attachments/assets/e2a6bb02-04aa-4abf-9732-ec6a56504b36)



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

## Premium Microsoft Sentinel Connectors

By default, the Attack Range deploys with basic connectors. Optional premium connectors require specific licenses and permissions.

### Requirements for Premium Connectors

To enable these connectors, you need:

1. **Appropriate Licenses**:
   - Microsoft 365 E5 license (or similar) 
   - Office 365 E3/E5 license
   - Entra ID Premium license (P1/P2)
   - Microsoft Defender XDR license

3. **Required Permissions**:
   - Global Administrator or Security Administrator role in Entra ID
   - Workspace Contributor permissions to the Log Analytics workspace
   - Microsoft Sentinel Contributor permissions

### Enabling Premium Connectors

Set `enable_premium_connectors = true` in your `terraform/terraform.tfvars` file:

```hcl
enable_premium_connectors = true

## Prerequisites

- Azure subscription with Contributor and Security Admin permissions
- Terraform 1.0.0+
- Python 3.7+
- Ansible 2.9+
- Azure CLI (for newbie)
- SSH key pair for accessing Linux machines
- At least 12 vCPUs available in your subscription for the VMs



![image](https://github.com/user-attachments/assets/213c3625-e8ab-46eb-8360-866dbc26c94a)

## Quick Start

1. **Clone the repository**
   ```
   git clone https://github.com/oloruntolaallbert/ms-attack-range.git
   cd ms-attack-range
   ```

2. **Set up your environment**
   ```
   ./Setup.sh
   ```

3. **Configure your deployment**
   - Edit `terraform/terraform.tfvars` with your specific settings
   - Edit `attack-range.yml` to configure attack scenarios

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
| Discovery | Process Discovery, Network Discovery, Account Discovery, System Info Discovery, Advanced Network Discovery |
| Credential Access | Credential Dumping, Brute Force, Mimikatz, Credential Vault Access |
| Execution | PowerShell, Command Shell, Scheduled Tasks |
| Persistence | Registry Run Keys, Scheduled Tasks Persistence, Startup Folder, Multi Persistence |
| Defense Evasion | Timestomp, Clear Logs, Disable Defender, Defense Evasion Chain |
| Network | Network Scanning, Port Scanning, SMB Scanning, Lateral Movement Scan |
| Collection | Data Staging |
| Exfiltration | Exfiltration Attempt |
| Impact | Impact Simulation |

To list all available attack types, run:
```
python attack-range.py attack
```

## Attack Sequences

Pre-configured attack sequences are available:

- **recon**: Basic reconnaissance techniques
- **credential_theft**: Credential-focused attacks
- **persistence**: Techniques for maintaining access
- **full_chain**: Complete attack chain simulation
- **cross_platform**: Attacks targeting both Windows and Linux
- **enhanced_recon**: Advanced discovery operations
- **advanced_persistence**: Sophisticated persistence mechanisms
- **full_attack_simulation**: Comprehensive multi-stage attack

To list all available sequences, run:
```
python attack-range.py sequence
```

## Analytics Rules

The deployment includes 20+ pre-configured Microsoft Sentinel analytics rules covering a wide range of attack techniques including:

- Brute force attempts
- Credential dumping and theft
- Suspicious PowerShell execution
- Scheduled task creation
- Registry persistence
- Process and account discovery
- Log clearing and tampering
- Network reconnaissance
- Defense evasion techniques
- Security tool manipulation
- Data exfiltration attempts

These rules are deployed automatically through the Terraform deployment, using an ARM template that configures all detection logic, query periods, and entity mappings.

## Security Note

This project creates intentionally vulnerable environments for security testing. Always deploy in isolated environments and never connect to production networks or use production credentials.

**Important**: Microsoft Defender for Endpoint (MDE) is intentionally disabled on the VMs in this environment to allow attack simulations to run successfully. In a production environment, you would never want to disable these protections. The VMs are tagged with `Defender-Off = true` to indicate this configuration. The attack techniques used would typically be blocked by properly configured security tools.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

- Albert Timileyin [x](https://x.com/x_Timileyin)
- Blog [Medium](https://medium.com/cybrush-entity-enrichment-in-microsoft-sentinel/building-a-microsoft-sentinel-attack-range-for-security-testing-6cc983b4b690) 
## Acknowledgments

- Inspired by the [Splunk Attack Range](https://github.com/splunk/attack_range)
- Uses [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team) for attack simulation
- Built with Terraform, Ansible, and Python
