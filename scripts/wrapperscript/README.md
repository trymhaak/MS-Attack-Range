**This approach:**

- Creates a virtual environment in the .venv directory
- Installs all requirements into that environment
- Creates a wrapper script attack-range.sh that automatically activates the virtual environment before running the Python script
- Makes the wrapper script executable

  use ./attack-range.sh instead of directly calling the Python script ./attack-range.py.



  # Quick Fix Guide for Common MS-Attack-Range Issues

If you're experiencing issues with the Microsoft Sentinel Attack Range, follow these steps to quickly resolve the most common problems:

## Quick Fix for WinRM Module Error

If you see the error `winrm or requests is not installed: No module named 'winrm'`:

1. Make sure your virtual environment is activated:
   ```bash
   source attack_range_env/bin/activate
   # OR 
   source .venv/bin/activate
   ```

2. Install the required module:
   ```bash
   pip install pywinrm requests cryptography
   ```

3. Try running your command again.

## Quick Fix for Ansible Module Redirection

For errors about redirecting `ansible.builtin.setup` to `ansible.windows.setup`:

1. Create an `ansible.cfg` file in the project root:
   ```bash
   echo "[defaults]
   deprecation_warnings = False
   host_key_checking = False" > ansible.cfg
   ```

2. Try running your command again.

## Quick Fix for IP Access Issues

If you can't access the VMs and suspect your IP might have changed:

1. Check your current public IP:
   ```bash
   curl ifconfig.me
   ```

2. Update the allowed IP in `terraform/terraform.tfvars`:
   ```
   allowed_ip = "YOUR_IP/32"
   ```

3. Apply the changes:
   ```bash
   python attack-range.py update
   ```

## Quick Fix for Missing SSH Key

If you need to generate an SSH key:

```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""
```

Then update the public key in `terraform/terraform.tfvars`.

## Script-Based Quick Fix

For a comprehensive fix of common issues, run the `fix-dependencies.sh` script:

1. Download the script from the repository
2. Make it executable:
   ```bash
   chmod +x fix-dependencies.sh
   ```
3. Run it:
   ```bash
   ./fix-dependencies.sh
   ```

## If All Else Fails

If you continue to experience issues:

1. Destroy the environment:
   ```bash
   python attack-range.py destroy
   ```

2. Fix your local dependencies using the script above

3. Rebuild the environment:
   ```bash
   python attack-range.py build
   ```

For more detailed troubleshooting, refer to the comprehensive troubleshooting guide in the project repository.
