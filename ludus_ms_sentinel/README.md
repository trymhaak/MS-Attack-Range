# Microsoft Sentinel Attack Range for Ludus

This Ansible collection simulates a Microsoft Sentinel environment in Ludus, providing a framework to test and validate various attack techniques and detection capabilities.

## Overview

The Microsoft Sentinel Attack Range for Ludus deploys a test environment with:

- Windows Domain Controller
- Windows Workstation
- Kali Linux attack machine
- Pre-configured attack simulations

The collection simulates attack techniques aligned with the MITRE ATT&CK framework, providing a controlled environment to test detection rules and incident response procedures.

## Installation

1. Add the collection to your Ludus server:

```bash
ludus ansible collection add albert.ludus_ms_sentinel
```

2. Create a configuration file for your Ludus range:

```bash
ludus range config get > config.yml
```

3. Edit the configuration file using the template below

4. Apply the configuration:

```bash
ludus range config set -f config.yml
```

5. Deploy the range:

```bash
ludus range deploy
```

## Configuration Template

Here's a sample configuration that deploys a Domain Controller, Workstation, and Kali Linux machine, and runs a series of attack simulations after deployment:

```yaml
ludus:
  - vm_name: "{{ range_id }}-DC01"
    hostname: "DC01"
    template: win2022-server-x64-template
    vlan: 10
    ip_last_octet: 10
    ram_gb: 4
    cpus: 2
    windows:
      sysprep: true
    domain:
      fqdn: sentinel.lab
      role: primary-dc
    roles:
      - albert.ludus_ms_sentinel.setup_windows
      - albert.ludus_ms_sentinel.disable_defender

  - vm_name: "{{ range_id }}-Workstation"
    hostname: "Workstation"
    template: win11-22h2-x64-enterprise-template
    vlan: 10
    ip_last_octet: 11
    ram_gb: 4
    cpus: 2
    windows:
      sysprep: true
    domain:
      fqdn: sentinel.lab
      role: member
    roles:
      - albert.ludus_ms_sentinel.setup_windows
      - albert.ludus_ms_sentinel.disable_defender

  - vm_name: "{{ range_id }}-Kali"
    hostname: "Kali"
    template: kali-template
    vlan: 10
    ip_last_octet: 12
    ram_gb: 4
    cpus: 2
    roles:
      - albert.ludus_ms_sentinel.setup_kali

  # Run attacks post-deployment
  - ludus:
      when: post-deploy
      host: Kali
    roles:
      - albert.ludus_ms_sentinel.attack_sequence
    role_vars:
      attack_types:
        - network_discovery
        - credential_access
        - persistence
        - defense_evasion
      target_ip: "10.10.10.11"  # IP of the Workstation
```

## Available Roles

This collection includes the following roles:

### Setup Roles

- **setup_windows**: Configures Windows machines for attack simulations
- **setup_kali**: Installs necessary tools on Kali Linux
- **disable_defender**: Disables Windows Defender for attack simulations

### Attack Simulation Roles

- **attack_sequence**: Runs a sequence of attack simulations
- **network_discovery**: Performs network scanning and reconnaissance
- **credential_access**: Simulates credential theft techniques
- **persistence**: Tests persistence mechanisms
- **defense_evasion**: Demonstrates evasion techniques
- **lateral_movement**: Simulates lateral movement
- **exfiltration**: Performs data exfiltration
- **impact**: Simulates impact techniques like ransomware
- **install_atomic**: Installs and runs Atomic Red Team tests

## Running Additional Attacks

You can run additional attacks manually after deployment by creating a Ludus Ansible task:

```bash
ludus ansible task create --hosts Kali --playbook attack_sequence.yml --vars '{"attack_types": ["lateral_movement", "impact"], "target_ip": "10.10.10.11"}'
```

Or by using the Atomic Red Team with specific technique IDs:

```bash
ludus ansible task create --hosts Kali --playbook install_atomic.yml --vars '{"technique_id": "T1003.001"}'
```

## Attack Techniques

The collection supports various MITRE ATT&CK techniques:

| Category | Supported Techniques |
|----------|----------------------|
| Discovery | Process Discovery, Network Discovery, Account Discovery, System Info Discovery |
| Credential Access | Credential Dumping, Brute Force, Mimikatz, Credential Vault Access |
| Execution | PowerShell, Command Shell, Scheduled Tasks |
| Persistence | Registry Run Keys, Scheduled Tasks, Startup Folder, Multi-Persistence |
| Defense Evasion | Timestomp, Clear Logs, Disable Defender, Defense Evasion Chain |
| Lateral Movement | Network Share Enumeration, Remote Execution, WMI |
| Exfiltration | Data Staging, Archive Creation, HTTP/DNS Exfiltration |
| Impact | Ransomware Simulation, Service Stopping, System Recovery Sabotage |

## Security Note

This collection creates intentionally vulnerable environments for security testing. Always deploy in isolated environments and never connect to production networks or use production credentials.

Windows Defender is intentionally disabled on the VMs in this environment to allow attack simulations to run successfully. In a production environment, you would never want to disable these protections.
