# MS-Attack-Range
Microsoft Sentinel Attack Range

# Overview of the MS-Attack-Range
The Microsoft Sentinel Attack Range is a tool that allows security teams to create a small lab environment to simulate attacks and generate data in Microsoft Sentinel for detection testing and validation. It allows you to:

Deploy a complete Azure infrastructure using Terraform
- Set up a simulated network with Windows and Linux machines
- Configure Microsoft Sentinel for logging and monitoring
- Run attack simulations based on MITRE ATT&CK techniques
- Test detection capabilities in Microsoft Sentinel

# Key Components
From the files you've provided, here's how the solution is structured:

# Terraform Infrastructure:

- Windows Domain Controller
- Windows Workstation
- Kali Linux attack machine
- Azure Log Analytics Workspace with Microsoft Sentinel
- Network configuration and security groups
- Data collection rules and connectors


# Attack Simulation:

- Uses Ansible playbooks to run attacks
- Incorporates Atomic Red Team tests
- Supports individual attack techniques and pre-defined sequences
- Covers various MITRE ATT&CK tactics and techniques


# Python Control Script:

- attack-range.py as the main control interface
- Commands for building, destroying, and updating the infrastructure
- Functions to run individual attacks or attack sequences

![image](https://github.com/user-attachments/assets/fc084318-da2c-46a0-91c3-3c09899ee775)
Time for the real fun begins!
  
