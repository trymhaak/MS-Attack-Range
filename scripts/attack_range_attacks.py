import os
import sys
import time

class AttackExecutor:
    """Attack execution management for Azure Attack Range"""
    
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
        "credential_vault_access": "T1003",  # Enhanced
        
        # Execution
        "powershell_exec": "T1059.001",
        "command_shell": "T1059.003",
        "scheduled_task": "T1053.005",
        
        # Persistence
        "registry_run_keys": "T1547.001",
        "scheduled_task_persist": "T1053.005",
        "startup_folder": "T1547.001",
        "multi_persistence": "T1547",  # Enhanced
        
        # Defense Evasion
        "timestomp": "T1070.006",
        "clear_logs": "T1070.001",
        "disable_defender": "T1562.001",
        "defense_evasion_chain": "T1562",  # Enhanced
        
        # Network Attacks
        "network_scan": "network_scan",
        "port_scan": "port_scan",
        "smb_scan": "smb_scan",
        "advanced_network_discovery": "T1046",  # Enhanced
        
        # Lateral Movement
        "lateral_movement_scan": "T1021",  # Enhanced
        
        # Exfiltration
        "data_staging": "T1074",  # Enhanced
        "exfiltration_attempt": "T1041",  # Enhanced
        
        # Impact
        "impact_simulation": "T1486",  # Enhanced
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
            "network_discovery",
            "system_info_discovery",
            "account_discovery",
            "process_discovery",
            "command_shell",
            "powershell_exec",
            "brute_force",
            "credential_dump",
            "scheduled_task",
            "startup_folder",
            "clear_logs",
            "timestomp",
            "port_scan",
            "smb_scan"
        ],
        # Enhanced sequences from the new guide
        "enhanced_recon": [
            "advanced_network_discovery",
            "process_discovery",
            "system_info_discovery",
            "account_discovery"
        ],
        "advanced_persistence": [
            "multi_persistence",
            "registry_run_keys",
            "scheduled_task",
            "startup_folder"
        ],
        "full_attack_simulation": [
            "advanced_network_discovery",
            "process_discovery",
            "credential_vault_access",
            "multi_persistence",
            "defense_evasion_chain",
            "data_staging",
            "exfiltration_attempt",
            "impact_simulation"
        ]
    }
    
    def __init__(self, config):
        self.config = config
    
    def get_playbook_path(self, attack_type):
        """Determine the correct playbook path for an attack type"""
        # Check if it's an enhanced attack that has its own playbook
        enhanced_attacks = {
            "advanced_network_discovery": "enhanced/network_discovery.yml",
            "credential_vault_access": "enhanced/credential_access.yml",
            "multi_persistence": "enhanced/persistence.yml",
            "defense_evasion_chain": "enhanced/defense_evasion.yml",
            "lateral_movement_scan": "enhanced/lateral_movement.yml",
            "data_staging": "enhanced/exfiltration.yml",
            "exfiltration_attempt": "enhanced/exfiltration.yml",
            "impact_simulation": "enhanced/impact.yml",
        }
        
        if attack_type in enhanced_attacks:
            return enhanced_attacks[attack_type]
        
        # Default behavior for standard attacks
        technique_id = self.ATTACK_SCENARIOS.get(attack_type)
        if technique_id and technique_id.startswith("T"):
            return "install_atomic.yml"
        else:
            return "attack_simulation.yml"
    
    def run_attack(self, attack_type, target=None):
        """Run individual attack"""
        print(f"[+] Running {attack_type} attack simulation...")

        technique_id = self.ATTACK_SCENARIOS.get(attack_type)
        if not technique_id:
            print(f"Unknown attack type: {attack_type}")
            return False

        # Get the appropriate playbook
        playbook = self.get_playbook_path(attack_type)
        
        # Build the command based on attack type
        if attack_type in ["advanced_network_discovery", "credential_vault_access", "multi_persistence", 
                          "defense_evasion_chain", "lateral_movement_scan", "data_staging", 
                          "exfiltration_attempt", "impact_simulation"]:
            # Enhanced attacks with their own playbooks
            cmd = f"ansible-playbook -i playbooks/inventory.yml playbooks/{playbook} -e target_ip={target} -vv"
        elif technique_id.startswith("T"):
            # It's an Atomic Red Team test
            cmd = f"ansible-playbook -i playbooks/inventory.yml playbooks/install_atomic.yml -e technique_id={technique_id} -vv"
        else:
            # It's a network-based attack from the standard attack_simulation.yml
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
