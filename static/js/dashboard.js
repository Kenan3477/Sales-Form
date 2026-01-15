// ASIS Dashboard JavaScript

class ASISDashboard {
    constructor() {
        this.reportContent = document.getElementById('reportContent');
        this.reportSpinner = document.getElementById('reportSpinner');
        this.tabButtons = document.querySelectorAll('.tab-btn');
        this.actionButtons = document.querySelectorAll('.action-btn');
        this.refreshButton = document.getElementById('refreshReports');
        
        this.currentTab = 'evidence';
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.updateSystemStatus();
        this.loadReport(this.currentTab);
        
        // Auto-refresh every 2 minutes
        setInterval(() => {
            this.loadReport(this.currentTab);
        }, 120000);
    }
    
    bindEvents() {
        // Tab buttons
        this.tabButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                const tab = btn.dataset.tab;
                this.switchTab(tab);
            });
        });
        
        // Action buttons
        this.actionButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                const action = btn.dataset.action;
                this.executeAction(action);
            });
        });
        
        // Refresh button
        this.refreshButton.addEventListener('click', () => {
            this.loadReport(this.currentTab);
        });
    }
    
    switchTab(tab) {
        // Update active tab
        this.tabButtons.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.tab === tab);
        });
        
        this.currentTab = tab;
        this.loadReport(tab);
    }
    
    async loadReport(reportType) {
        this.showSpinner();
        
        try {
            const response = await fetch(`/api/features/${reportType}`);
            const data = await response.json();
            
            if (data.success) {
                this.showReport(data.data);
            } else {
                this.showReport(`❌ Error: ${data.error}`);
            }
            
        } catch (error) {
            console.error('Error loading report:', error);
            this.showReport(`❌ Connection error: ${error.message}`);
        }
    }
    
    showSpinner() {
        this.reportSpinner.style.display = 'flex';
        this.reportContent.style.display = 'none';
    }
    
    showReport(content) {
        this.reportContent.textContent = content;
        this.reportSpinner.style.display = 'none';
        this.reportContent.style.display = 'block';
    }
    
    async executeAction(action) {
        // Temporarily disable button
        const button = document.querySelector(`[data-action="${action}"]`);
        const originalText = button.innerHTML;
        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
        button.disabled = true;
        
        try {
            const response = await fetch(`/api/features/${action}`);
            const data = await response.json();
            
            if (data.success) {
                // Switch to the corresponding tab and show result
                this.switchTab(action);
            } else {
                alert(`Error: ${data.error}`);
            }
            
        } catch (error) {
            console.error('Error executing action:', error);
            alert(`Connection error: ${error.message}`);
        } finally {
            // Re-enable button
            button.innerHTML = originalText;
            button.disabled = false;
        }
    }
    
    async updateSystemStatus() {
        try {
            const response = await fetch('/api/status');
            const status = await response.json();
            
            // Update status elements
            document.getElementById('systemHealth').textContent = status.system_health;
            document.getElementById('systemActivated').textContent = status.activated ? 'Yes' : 'No';
            document.getElementById('lastUpdate').textContent = new Date(status.last_update).toLocaleString();
            
        } catch (error) {
            console.error('Error updating status:', error);
        }
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ASISDashboard();
    
    // Periodic status update
    setInterval(async () => {
        try {
            const response = await fetch('/api/status');
            const status = await response.json();
            
            document.getElementById('systemHealth').textContent = status.system_health;
            document.getElementById('systemActivated').textContent = status.activated ? 'Yes' : 'No';
            document.getElementById('lastUpdate').textContent = new Date(status.last_update).toLocaleString();
            
        } catch (error) {
            console.error('Status update failed:', error);
        }
    }, 30000); // Update every 30 seconds
});
