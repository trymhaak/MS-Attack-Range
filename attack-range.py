#!/usr/bin/env python3

import argparse
import sys
import os
import yaml
import time
import requests
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient

sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

# Import our modular components
from attack_range_core import AzureAttackRangeCore
from attack_range_attacks import AttackExecutor

class AzureAttackRange:
    """Main Azure Attack Range class that integrates all components"""
    
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
        
        # Initialize our modular components
        self.core = AzureAttackRangeCore(self.config, self.credential)
        self.attack_executor = AttackExecutor(self.config)
    
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
        self.core.build()

    def destroy(self):
        """Destroy the complete attack range infrastructure"""
        self.core.destroy()

    def update(self):
        """Update the infrastructure with new resources"""
        self.core.update()

    def create_ansible_inventory(self):
        """Create Ansible inventory file with VM information"""
        return self.core.create_ansible_inventory()
    
    def run_attack(self, attack_type, target=None):
        """Run individual attack"""
        if not self.create_ansible_inventory():
            print("Error: Failed to create Ansible inventory")
            return False
        
        return self.attack_executor.run_attack(attack_type, target)

    def run_attack_sequence(self, sequence_name):
        """Run a predefined attack sequence"""
        if not self.create_ansible_inventory():
            print("Error: Failed to create Ansible inventory")
            return False
        
        return self.attack_executor.run_attack_sequence(sequence_name)

def main():
    parser = argparse.ArgumentParser(description='Azure Attack Range')
    parser.add_argument('action', 
                       choices=['build', 'destroy', 'simulate', 'show', 'access', 'update', 'attack', 'sequence'],
                       help='Action to perform')
    parser.add_argument('-t', '--target', help='Target machine for simulation')
    parser.add_argument('-tid', '--technique_id', help='MITRE ATT&CK technique ID')
    parser.add_argument('-a', '--attack_type', help='Type of attack to perform')
    parser.add_argument('-s', '--sequence', 
                       choices=['recon', 'credential_theft', 'persistence', 'full_chain', 'cross_platform',
                               'enhanced_recon', 'advanced_persistence', 'full_attack_simulation'],
                       help='Attack sequence to run')
    
    args = parser.parse_args()
    attack_range = AzureAttackRange()
    
    try:
        if args.action == 'build':
            attack_range.build()
        elif args.action == 'destroy':
            attack_range.destroy()
        elif args.action == 'update':
            attack_range.update()
        elif args.action == 'attack':
            if not args.attack_type:
                print("Available attack types:")
                for attack in attack_range.attack_executor.ATTACK_SCENARIOS.keys():
                    print(f"  - {attack}")
                sys.exit(1)
            attack_range.run_attack(args.attack_type, args.target)
        elif args.action == 'sequence':
            if not args.sequence:
                print("Available attack sequences:")
                for seq in attack_range.attack_executor.ATTACK_SEQUENCES.keys():
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
