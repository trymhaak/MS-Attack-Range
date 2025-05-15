# MS-Attack-Range Dashboard

A user-friendly interface for managing the Microsoft Sentinel Attack Range environment. This dashboard makes it easy for team members to deploy and destroy the environment without needing to understand the underlying code.

## Features

- One-click deployment and destruction of the MS-Attack-Range
- Real-time status monitoring
- Cost tracking and estimation
- Easy access to connection information
- Automatic scheduling with failsafe destruction

## Getting Started

### For Team Members

1. **Launch the Dashboard**:
   ```bash
   # On macOS/Linux
   ./start-dashboard.sh
   ```

   This will start a local web server and open the dashboard in your browser.

2. **Deploy the Environment**:
   - Click the "Deploy Environment" button
   - Confirm the action
   - Wait for deployment to complete (approximately 30 minutes)

3. **Access the Environment**:
   - Use the connection details provided in the "Access Information" section
   - For Windows VMs: Use RDP with the provided credentials
   - For Kali Linux: Use SSH with the provided key

4. **Destroy the Environment When Done**:
   - Click the "Destroy Environment" button
   - Confirm the action
   - Wait for destruction to complete

### Important Notes

- The environment costs approximately $0.50 per hour when running
- The environment will be automatically destroyed on Friday at 5:00 PM UTC
- Always destroy the environment when you're done to minimize costs

## Cost Management

The dashboard includes cost tracking features:
- Real-time cost estimation based on running time
- Daily, weekly, and monthly cost projections
- Budget usage visualization

## Technical Details

The dashboard is a simple web application that interacts with:
1. GitHub Actions workflows for deployment/destruction
2. Azure resources for status checking
3. Local storage for session management

## Troubleshooting

If you encounter issues:

1. **Dashboard won't start**:
   - Ensure Python 3 is installed
   - Try running on a different port: `python3 dashboard/serve.py -p 8081`

2. **Deployment fails**:
   - Check GitHub Actions logs for errors
   - Verify that GitHub secrets are correctly configured

3. **Can't connect to VMs**:
   - Ensure the environment is fully deployed
   - Check that you're using the correct credentials
   - Verify your network allows the required connections

## Support

If you need assistance, please contact the system administrator.
