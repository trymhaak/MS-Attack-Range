# Cost Management for MS-Attack-Range

This document outlines strategies to minimize costs when using the MS-Attack-Range environment.

## Cost Overview

The MS-Attack-Range environment includes the following billable resources:

- 3 Virtual Machines (Windows DC, Windows Workstation, Kali Linux)
- Storage accounts for VM disks
- Log Analytics Workspace with Microsoft Sentinel
- Network resources (Public IPs, data transfer)

**Estimated monthly cost if running 24/7**: $300-400 USD

## Automated Deployment and Destruction

To minimize costs, we've implemented automated deployment and destruction of the environment using GitHub Actions. This ensures the environment is only active when needed.

### Scheduled Operation

The GitHub Actions workflow (`schedule-attack-range.yml`) is configured to:

1. **Deploy** the environment every Monday at 8:00 AM UTC
2. **Destroy** the environment every Friday at 5:00 PM UTC

This schedule limits the environment to approximately 105 hours per week (vs. 168 hours if running 24/7), reducing costs by ~40%.

### Manual Operation

You can also manually trigger deployment or destruction:

1. Go to the GitHub repository
2. Navigate to Actions > Schedule MS-Attack-Range
3. Click "Run workflow"
4. Select either "deploy" or "destroy"
5. Click "Run workflow"

### Local Scripts

For local operation, use the provided scripts:

```bash
# Deploy the environment
./scripts/deploy-attack-range.sh

# Destroy the environment
./scripts/destroy-attack-range.sh
```

## Additional Cost Optimization Strategies

### 1. VM Auto-Shutdown

Configure auto-shutdown for VMs during non-working hours:

1. In Azure Portal, navigate to each VM
2. Select "Auto-shutdown" from the left menu
3. Set a shutdown time (e.g., 6:00 PM your local time)
4. Enable notifications if desired

### 2. Use B-Series VMs for Less Intensive Testing

Modify `terraform/vm.tf` to use B-series VMs instead of D-series:

```hcl
# Example change for the DC VM
resource "azurerm_windows_virtual_machine" "dc" {
  # ...
  size = "Standard_B2s"  # Instead of Standard_D2s_v3
  # ...
}
```

This can reduce VM costs by 50-70%.

### 3. Reduce Log Retention Period

Modify `terraform/main.tf` to reduce the Log Analytics retention period:

```hcl
resource "azurerm_log_analytics_workspace" "law" {
  # ...
  retention_in_days = 7  # Instead of 30
  # ...
}
```

### 4. Implement Budget Alerts

Set up Azure Budget Alerts to monitor costs:

1. In Azure Portal, navigate to Subscriptions
2. Select your subscription
3. Click on "Budgets" in the left menu
4. Create a new budget with appropriate thresholds
5. Configure alerts at 50%, 75%, and 90% of your budget

## Best Practices

1. **Never leave the environment running over weekends or holidays**
2. **Destroy the environment immediately after testing is complete**
3. **Regularly review Azure Cost Analysis to identify unexpected charges**
4. **Consider reserving VMs if you plan to use them regularly over a long period**

By following these guidelines, you can reduce the monthly cost to approximately $100-150 USD.
