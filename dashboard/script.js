// MS-Attack-Range Dashboard Script
document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const statusIndicator = document.getElementById('statusIndicator');
    const statusText = document.getElementById('statusText');
    const deployBtn = document.getElementById('deployBtn');
    const destroyBtn = document.getElementById('destroyBtn');
    const deploymentInfo = document.getElementById('deploymentInfo');
    const resourceList = document.getElementById('resourceList');
    const activeSession = document.getElementById('activeSession');
    const runningTime = document.getElementById('runningTime');
    const costEstimate = document.getElementById('costEstimate');
    const accessInfo = document.getElementById('accessInfo');
    const scheduleSwitch = document.getElementById('scheduleSwitch');
    const budgetProgress = document.getElementById('budgetProgress');
    const confirmationModal = new bootstrap.Modal(document.getElementById('confirmationModal'));
    const modalTitle = document.getElementById('modalTitle');
    const modalBody = document.getElementById('modalBody');
    const confirmBtn = document.getElementById('confirmBtn');
    
    // Constants
    const HOURLY_COST = 0.5; // $0.50 per hour
    const API_URL = 'https://api.github.com/repos/trymhaak/iSkysikkerhet/actions/workflows/schedule-attack-range.yml/dispatches';
    const GITHUB_TOKEN = ''; // This should be set by the user in localStorage
    
    // Variables
    let environmentStatus = 'unknown';
    let deploymentStartTime = null;
    let runningTimer = null;
    
    // Check if user has set GitHub token
    if (!localStorage.getItem('github_token')) {
        promptForGitHubToken();
    }
    
    // Initialize
    checkEnvironmentStatus();
    
    // Event Listeners
    deployBtn.addEventListener('click', function() {
        showConfirmation('Deploy Environment', 'Are you sure you want to deploy the MS-Attack-Range? This will incur costs.', deployEnvironment);
    });
    
    destroyBtn.addEventListener('click', function() {
        showConfirmation('Destroy Environment', 'Are you sure you want to destroy the MS-Attack-Range? All resources will be removed.', destroyEnvironment);
    });
    
    scheduleSwitch.addEventListener('change', function() {
        // In a real implementation, this would enable/disable the GitHub Actions schedule
        localStorage.setItem('schedule_enabled', scheduleSwitch.checked);
        alert(scheduleSwitch.checked ? 'Auto-scheduling enabled' : 'Auto-scheduling disabled');
    });
    
    // Functions
    function checkEnvironmentStatus() {
        // In a real implementation, this would check the actual status from Azure
        // For demo purposes, we'll use localStorage to simulate status
        const savedStatus = localStorage.getItem('environment_status') || 'destroyed';
        const savedTime = localStorage.getItem('deployment_time');
        
        updateStatus(savedStatus);
        
        if (savedStatus === 'deployed' && savedTime) {
            deploymentStartTime = new Date(parseInt(savedTime));
            startRunningTimer();
            showDeploymentInfo();
        }
        
        // Refresh status every minute
        setTimeout(checkEnvironmentStatus, 60000);
    }
    
    function updateStatus(status) {
        environmentStatus = status;
        statusIndicator.className = 'status-indicator status-' + status;
        
        switch(status) {
            case 'deployed':
                statusText.textContent = 'Deployed';
                deployBtn.disabled = true;
                destroyBtn.disabled = false;
                break;
            case 'destroyed':
                statusText.textContent = 'Destroyed';
                deployBtn.disabled = false;
                destroyBtn.disabled = true;
                activeSession.classList.add('d-none');
                accessInfo.innerHTML = '<p>Deploy the environment to see access information.</p>';
                break;
            case 'deploying':
                statusText.textContent = 'Deploying...';
                deployBtn.disabled = true;
                destroyBtn.disabled = true;
                break;
            case 'destroying':
                statusText.textContent = 'Destroying...';
                deployBtn.disabled = true;
                destroyBtn.disabled = true;
                break;
            default:
                statusText.textContent = 'Unknown';
                deployBtn.disabled = false;
                destroyBtn.disabled = false;
        }
    }
    
    function deployEnvironment() {
        updateStatus('deploying');
        localStorage.setItem('environment_status', 'deploying');
        
        // In a real implementation, this would trigger the GitHub Actions workflow
        triggerGitHubAction('deploy').then(() => {
            // Simulate deployment completion after 30 seconds
            setTimeout(() => {
                deploymentStartTime = new Date();
                localStorage.setItem('deployment_time', deploymentStartTime.getTime().toString());
                updateStatus('deployed');
                localStorage.setItem('environment_status', 'deployed');
                startRunningTimer();
                showDeploymentInfo();
            }, 30000);
        }).catch(error => {
            alert('Deployment failed: ' + error.message);
            updateStatus('destroyed');
            localStorage.setItem('environment_status', 'destroyed');
        });
    }
    
    function destroyEnvironment() {
        updateStatus('destroying');
        localStorage.setItem('environment_status', 'destroying');
        
        // In a real implementation, this would trigger the GitHub Actions workflow
        triggerGitHubAction('destroy').then(() => {
            // Simulate destruction completion after 20 seconds
            setTimeout(() => {
                stopRunningTimer();
                updateStatus('destroyed');
                localStorage.setItem('environment_status', 'destroyed');
                localStorage.removeItem('deployment_time');
            }, 20000);
        }).catch(error => {
            alert('Destruction failed: ' + error.message);
            updateStatus('deployed');
            localStorage.setItem('environment_status', 'deployed');
        });
    }
    
    function startRunningTimer() {
        if (runningTimer) {
            clearInterval(runningTimer);
        }
        
        activeSession.classList.remove('d-none');
        
        runningTimer = setInterval(() => {
            const now = new Date();
            const diff = now - deploymentStartTime;
            
            const hours = Math.floor(diff / 3600000);
            const minutes = Math.floor((diff % 3600000) / 60000);
            const seconds = Math.floor((diff % 60000) / 1000);
            
            runningTime.textContent = `${padZero(hours)}:${padZero(minutes)}:${padZero(seconds)}`;
            
            // Update cost estimate
            const hoursFraction = diff / 3600000;
            const cost = hoursFraction * HOURLY_COST;
            costEstimate.textContent = cost.toFixed(2);
            
            // Update budget progress
            const monthlyBudget = 100; // $100
            const percentUsed = (cost / monthlyBudget) * 100;
            budgetProgress.style.width = `${Math.min(percentUsed, 100)}%`;
            budgetProgress.textContent = `${Math.round(percentUsed)}%`;
            
            if (percentUsed > 75) {
                budgetProgress.className = 'progress-bar bg-danger';
            } else if (percentUsed > 50) {
                budgetProgress.className = 'progress-bar bg-warning';
            } else {
                budgetProgress.className = 'progress-bar bg-success';
            }
        }, 1000);
    }
    
    function stopRunningTimer() {
        if (runningTimer) {
            clearInterval(runningTimer);
            runningTimer = null;
        }
        activeSession.classList.add('d-none');
    }
    
    function showDeploymentInfo() {
        deploymentInfo.classList.remove('d-none');
        
        // In a real implementation, this would fetch actual resource information from Azure
        resourceList.innerHTML = `
            <ul class="list-group">
                <li class="list-group-item d-flex justify-content-between align-items-center">
                    Resource Group
                    <span class="badge bg-primary">iskysikkerhet-attack-range-rg</span>
                </li>
                <li class="list-group-item d-flex justify-content-between align-items-center">
                    Windows Domain Controller
                    <span class="badge bg-success">Running</span>
                </li>
                <li class="list-group-item d-flex justify-content-between align-items-center">
                    Windows Workstation
                    <span class="badge bg-success">Running</span>
                </li>
                <li class="list-group-item d-flex justify-content-between align-items-center">
                    Kali Linux
                    <span class="badge bg-success">Running</span>
                </li>
                <li class="list-group-item d-flex justify-content-between align-items-center">
                    Microsoft Sentinel
                    <span class="badge bg-success">Active</span>
                </li>
            </ul>
        `;
        
        // Show access information
        accessInfo.innerHTML = `
            <h5>Connection Details</h5>
            <div class="mb-3">
                <h6>Domain Controller (Windows Server 2019)</h6>
                <p><strong>IP Address:</strong> 40.118.65.224</p>
                <p><strong>Username:</strong> azureuser</p>
                <p><strong>Password:</strong> P@ssw0rd1234!</p>
                <button class="btn btn-sm btn-outline-primary copy-btn" data-clipboard="rdp://azureuser@40.118.65.224">Copy RDP Command</button>
            </div>
            
            <div class="mb-3">
                <h6>Workstation (Windows 10)</h6>
                <p><strong>IP Address:</strong> 40.115.9.222</p>
                <p><strong>Username:</strong> azureuser</p>
                <p><strong>Password:</strong> P@ssw0rd1234!</p>
                <button class="btn btn-sm btn-outline-primary copy-btn" data-clipboard="rdp://azureuser@40.115.9.222">Copy RDP Command</button>
            </div>
            
            <div class="mb-3">
                <h6>Kali Linux</h6>
                <p><strong>IP Address:</strong> 40.68.59.93</p>
                <p><strong>Username:</strong> azureuser</p>
                <p><strong>SSH Key:</strong> /Users/trym.haakansson/code/MS-Attack-Range/attack_range_key</p>
                <button class="btn btn-sm btn-outline-primary copy-btn" data-clipboard="ssh -i /Users/trym.haakansson/code/MS-Attack-Range/attack_range_key azureuser@40.68.59.93">Copy SSH Command</button>
            </div>
            
            <div>
                <h6>Microsoft Sentinel</h6>
                <p><strong>Workspace ID:</strong> d29c6af8-6931-4c59-8c3c-556703d13b96</p>
                <a href="https://portal.azure.com/#blade/Microsoft_Azure_Security_Insights/MainMenuBlade/0/id/%2Fsubscriptions%2F4b724e61-b32c-4989-ba82-a3469ad44f98%2FresourceGroups%2Fiskysikkerhet-attack-range-rg%2Fproviders%2FMicrosoft.OperationalInsights%2Fworkspaces%2Fiskysikkerhet-ar-law" 
                   target="_blank" class="btn btn-primary">Open in Azure Portal</a>
            </div>
        `;
        
        // Add event listeners to copy buttons
        document.querySelectorAll('.copy-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const text = this.getAttribute('data-clipboard');
                navigator.clipboard.writeText(text).then(() => {
                    const originalText = this.textContent;
                    this.textContent = 'Copied!';
                    setTimeout(() => {
                        this.textContent = originalText;
                    }, 2000);
                });
            });
        });
    }
    
    function showConfirmation(title, message, callback) {
        modalTitle.textContent = title;
        modalBody.textContent = message;
        
        // Remove previous event listener
        const newConfirmBtn = confirmBtn.cloneNode(true);
        confirmBtn.parentNode.replaceChild(newConfirmBtn, confirmBtn);
        
        // Add new event listener
        newConfirmBtn.addEventListener('click', function() {
            confirmationModal.hide();
            callback();
        });
        
        confirmationModal.show();
    }
    
    function triggerGitHubAction(action) {
        const token = localStorage.getItem('github_token');
        
        if (!token) {
            return Promise.reject(new Error('GitHub token not set'));
        }
        
        return fetch(API_URL, {
            method: 'POST',
            headers: {
                'Authorization': `token ${token}`,
                'Accept': 'application/vnd.github.v3+json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                ref: 'main',
                inputs: {
                    action: action
                }
            })
        }).then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        });
    }
    
    function promptForGitHubToken() {
        const token = prompt('Please enter your GitHub Personal Access Token to enable deployment control:');
        if (token) {
            localStorage.setItem('github_token', token);
        }
    }
    
    function padZero(num) {
        return num.toString().padStart(2, '0');
    }
});
