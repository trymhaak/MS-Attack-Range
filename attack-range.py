#!/usr/bin/env python3

import argparse
import sys
import os
import yaml
import json
import time
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient

class AzureAttackRange:
    # Add attack scenarios and sequences
    ATTACK_SCENARIOS = {
        # Discovery Attacks
        "process_discovery": "T1057",
        "network_discovery": "T1046",
        "account_discovery": "T1087",
        "system_info_discovery": "T1082",
        
        # Credential Access
        "credential_dump": "T1003.001",
        "brute_force": "T1110",
        "credential_mimikatz": "T1003.002",
        
        # Execution
        "powershell_exec": "T1059.001",
        "command_shell": "T1059.003",
        "scheduled_task": "T1053.005",
        
        # Persistence
        "registry_run_keys": "T1547.001",
        "scheduled_task_persist": "T1053.005",
        "startup_folder": "T1547.001",
        
        # Defense Evasion
        "timestomp": "T1070.006",
        "clear_logs": "T1070.001",
        "disable_defender": "T1562.001",
        
        # Network Attacks
        "network_scan": "network_scan",
        "port_scan": "port_scan",
        "smb_scan": "smb_scan"
    }

    ATTACK_SEQUENCES = {
        "recon": [
            "process_discovery",
            "network_discovery",
            "system_info_discovery"
        ],
        "credential_theft": [
            "account_discovery",
            "credential_dump",
            "credential_mimikatz"
        ],
        "persistence": [
            "registry_run_keys",
            "scheduled_task_persist",
            "startup_folder"
        ],
        "full_chain": [
            "network_discovery",
            "account_discovery",
            "credential_dump",
            "powershell_exec",
            "registry_run_keys",
            "clear_logs"
        ],
        "cross_platform": [
            # Initial Discovery Phase (Works on both Windows/Linux)
            "network_discovery",     # Network scanning
            "system_info_discovery", # System information gathering
            "account_discovery",     # User and group enumeration
            "process_discovery",     # Process listing

            # Execution Phase
            "command_shell",        # Shell commands
            "powershell_exec",      # PowerShell (Windows) / bash (Linux)

            # Credential Access
            "brute_force",          # Password bruteforcing
            "credential_dump",      # Credential harvesting

            # Persistence
            "scheduled_task",       # Task scheduling
            "startup_folder",       # Startup modifications

            # Defense Evasion
            "clear_logs",          # Log clearing
            "timestomp",           # Timestamp manipulation

            # Network Activities
            "port_scan",           # Port scanning
            "smb_scan"            # SMB enumeration
        ],
        "discovery_only": [
            "network_discovery",
            "system_info_discovery",
            "account_discovery",
            "process_discovery"
        ],
        "network_recon": [
            "network_discovery",
            "port_scan",
            "smb_scan"
        ]}
    def __init__(self):
        """Initialize Azure Attack Range with configuration and credentials"""
        self.config = self.load_config()
        self.credential = DefaultAzureCredential()
        self.resource_client = ResourceManagementClient(
            self.credential, 
            self.config['subscription_id']
        )
        self.network_client = NetworkManagementClient(
            self.credential, 
            self.config['subscription_id']
        )
    
    # Keep your existing methods unchanged
    def load_config(self):
        """Load configuration from YAML file"""
        try:
            with open('attack-range.yml', 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            print("Error: attack-range.yml configuration file not found")
            sys.exit(1)
        except yaml.YAMLError as e:
            print(f"Error parsing configuration file: {e}")
            sys.exit(1)

    def build(self):
        """Build the complete attack range infrastructure"""
        print("[+] Building Azure Attack Range infrastructure...")
        try:
            os.system(f"terraform -chdir=terraform init")
            result = os.system(f"terraform -chdir=terraform apply -auto-approve")
            if result != 0:
                print("Error: Terraform apply failed")
                sys.exit(1)
            print("[+] Infrastructure built successfully")
        except Exception as e:
            print(f"Error building infrastructure: {e}")
            sys.exit(1)

    def destroy(self):
        """Destroy the complete attack range infrastructure"""
        print("[+] Destroying Azure Attack Range infrastructure...")
        try:
            result = os.system(f"terraform -chdir=terraform destroy -auto-approve")
            if result != 0:
                print("Error: Terraform destroy failed")
                sys.exit(1)
            print("[+] Infrastructure destroyed successfully")
        except Exception as e:
            print(f"Error destroying infrastructure: {e}")
            sys.exit(1)

    def update(self):
        """Update the infrastructure with new resources"""
        print("[+] Updating Azure Attack Range infrastructure...")
        try:
            result = os.system(f"terraform -chdir=terraform apply -auto-approve")
            if result != 0:
                print("Error: Terraform apply failed")
                sys.exit(1)
            print("[+] Infrastructure updated successfully")
        except Exception as e:
            print(f"Error updating infrastructure: {e}")
            sys.exit(1)

    # Keep other existing methods (show, get_access_info, etc.)
    def create_ansible_inventory(self):
        """Create Ansible inventory file with VM information"""
        print("[+] Creating Ansible inventory file...")
        
        admin_username = self.config.get('admin_username', 'azureuser')
        admin_password = self.config.get('admin_password')
        rg_name = self.config.get('resource_group', 'attack-range-rg')

        if not admin_password:
            print("Error: admin_password not found in configuration")
            return False

        inventory = {
            'all': {
                'children': {
                    'windows': {
                        'hosts': {},
                        'vars': {
                            'ansible_user': admin_username,
                            'ansible_password': admin_password,
                            'ansible_connection': 'winrm',
                            'ansible_winrm_server_cert_validation': 'ignore',
                            'ansible_port': '5985',
                            'ansible_winrm_scheme': 'http',
                            'ansible_winrm_transport': 'ntlm'
                        }
                    },
                    'linux': {
                        'hosts': {},
                        'vars': {
                            'ansible_user': 'kali',
                            'ansible_ssh_private_key_file': '~/.ssh/id_rsa',
                            'ansible_connection': 'ssh'
                        }
                    }
                }
            }
        }

        try:
            compute_client = ComputeManagementClient(self.credential, self.config['subscription_id'])
            vms = compute_client.virtual_machines.list(rg_name)
            
            for vm in vms:
                try:
                    vm_name = vm.name
                    print(f"Processing VM: {vm_name}")

                    # Get network interface
                    network_interfaces = vm.network_profile.network_interfaces
                    if not network_interfaces:
                        continue

                    primary_nic_id = network_interfaces[0].id
                    nic_name = primary_nic_id.split('/')[-1]
                    nic = self.network_client.network_interfaces.get(rg_name, nic_name)
                    
                    if not nic.ip_configurations[0].public_ip_address:
                        continue

                    pip_id = nic.ip_configurations[0].public_ip_address.id
                    pip_name = pip_id.split('/')[-1]
                    pip = self.network_client.public_ip_addresses.get(rg_name, pip_name)
                    public_ip = pip.ip_address

                    print(f"Found IP {public_ip} for VM {vm_name}")

                    # Explicitly check for DC or workstation in the name
                    if "dc" in vm_name.lower() or "workstation" in vm_name.lower():
                        inventory['all']['children']['windows']['hosts'][vm_name] = {
                            'ansible_host': public_ip,
                            'ansible_winrm_operation_timeout_sec': 60,
                            'ansible_winrm_read_timeout_sec': 70
                        }
                    elif "kali" in vm_name.lower():
                        inventory['all']['children']['linux']['hosts'][vm_name] = {
                            'ansible_host': public_ip
                        }
                    
                except Exception as e:
                    print(f"Warning: Error processing VM {vm_name}: {str(e)}")
                    continue

            os.makedirs('playbooks', exist_ok=True)
            with open('playbooks/inventory.yml', 'w') as f:
                yaml.dump(inventory, f, default_flow_style=False)
            
            print("\nGenerated Inventory:")
            print(yaml.dump(inventory))
            
            return True

        except Exception as e:
            print(f"Error creating Ansible inventory: {str(e)}")
            return False
    
    # Add new attack methods
    def run_attack(self, attack_type, target=None):
        """Run individual attack"""
        print(f"[+] Running {attack_type} attack simulation...")

        if not self.create_ansible_inventory():
            print("Error: Failed to create Ansible inventory")
            return False

        technique_id = self.ATTACK_SCENARIOS.get(attack_type)
        if not technique_id:
            print(f"Unknown attack type: {attack_type}")
            return False

        if technique_id.startswith("T"):
            # It's an Atomic Red Team test
            cmd = f"ansible-playbook -i playbooks/inventory.yml playbooks/install_atomic.yml -e technique_id={technique_id} -vv"
        else:
            # It's a network-based attack
            cmd = f"ansible-playbook -i playbooks/inventory.yml playbooks/attack_simulation.yml -e simulation_type={attack_type} -e target_ip={target} -vv"

        try:
            print(f"Executing command: {cmd}")
            result = os.system(cmd)
            if result != 0:
                print(f"Error: Attack {attack_type} failed")
                return False
            print(f"[+] Attack {attack_type} completed successfully")
            return True
        except Exception as e:
            print(f"Error running {attack_type}: {e}")
            return False

    def run_attack_sequence(self, sequence_name):
        """Run a predefined attack sequence"""
        if sequence_name not in self.ATTACK_SEQUENCES:
            print(f"Unknown attack sequence: {sequence_name}")
            return

        print(f"[+] Starting attack sequence: {sequence_name}")
        attacks = self.ATTACK_SEQUENCES[sequence_name]
        
        successful = 0
        failed = 0
        
        for attack in attacks:
            print(f"\n[+] Running attack: {attack}")
            if self.run_attack(attack):
                successful += 1
            else:
                failed += 1
            time.sleep(30)  # Wait between attacks

        print(f"\n[+] Attack sequence {sequence_name} complete")
        print(f"Successful attacks: {successful}")
        print(f"Failed attacks: {failed}")

def main():
    parser = argparse.ArgumentParser(description='Azure Attack Range')
    parser.add_argument('action', 
                       choices=['build', 'destroy', 'simulate', 'show', 'access', 'update', 'attack', 'sequence'],
                       help='Action to perform')
    parser.add_argument('-t', '--target', help='Target machine for simulation')
    parser.add_argument('-tid', '--technique_id', help='MITRE ATT&CK technique ID')
    parser.add_argument('-a', '--attack_type', help='Type of attack to perform')
    parser.add_argument('-s', '--sequence', 
                       choices=['recon', 'credential_theft', 'persistence', 'full_chain'],
                       help='Attack sequence to run')
    
    args = parser.parse_args()
    attack_range = AzureAttackRange()
    
    try:
        if args.action == 'build':
            attack_range.build()
        elif args.action == 'destroy':
            attack_range.destroy()
        elif args.action == 'simulate':
            if not args.technique_id or not args.target:
                print("Error: technique_id and target required for simulate")
                sys.exit(1)
            attack_range.simulate(args.technique_id, args.target)
        elif args.action == 'show':
            attack_range.show()
        elif args.action == 'access':
            attack_range.get_access_info()
        elif args.action == 'update':
            attack_range.update()
        elif args.action == 'attack':
            if not args.attack_type:
                print("Available attack types:")
                for attack in attack_range.ATTACK_SCENARIOS.keys():
                    print(f"  - {attack}")
                sys.exit(1)
            attack_range.run_attack(args.attack_type, args.target)
        elif args.action == 'sequence':
            if not args.sequence:
                print("Available attack sequences:")
                for seq in attack_range.ATTACK_SEQUENCES.keys():
                    print(f"  - {seq}")
                sys.exit(1)
            attack_range.run_attack_sequence(args.sequence)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
