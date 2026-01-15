// ASIS Chat Interface JavaScript

class ASISChat {
    constructor() {
        this.socket = io();
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.chatMessages = document.getElementById('chatMessages');
        this.charCount = document.getElementById('charCount');
        this.typingIndicator = document.getElementById('typingIndicator');
        this.statusDot = document.getElementById('statusDot');
        this.statusText = document.getElementById('statusText');
        this.featureModal = document.getElementById('featureModal');
        this.modalTitle = document.getElementById('modalTitle');
        this.modalContent = document.getElementById('modalContent');
        this.modalSpinner = document.getElementById('modalSpinner');
        this.modalClose = document.getElementById('modalClose');
        
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.checkSystemStatus();
        this.setupSocket();
        
        // Auto-focus input
        this.messageInput.focus();
    }
    
    bindEvents() {
        // Message input events
        this.messageInput.addEventListener('input', () => {
            this.updateCharCount();
            this.toggleSendButton();
        });
        
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Send button
        this.sendButton.addEventListener('click', () => {
            this.sendMessage();
        });
        
        // Feature buttons
        document.querySelectorAll('.feature-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const feature = btn.dataset.feature;
                this.loadFeature(feature);
            });
        });
        
        // Modal events
        this.modalClose.addEventListener('click', () => {
            this.closeModal();
        });
        
        this.featureModal.addEventListener('click', (e) => {
            if (e.target === this.featureModal) {
                this.closeModal();
            }
        });
        
        // Escape key to close modal
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.featureModal.classList.contains('show')) {
                this.closeModal();
            }
        });
    }
    
    setupSocket() {
        this.socket.on('connect', () => {
            console.log('Connected to ASIS');
            this.updateStatus('Connected', 'success');
        });
        
        this.socket.on('disconnect', () => {
            console.log('Disconnected from ASIS');
            this.updateStatus('Disconnected', 'error');
        });
        
        this.socket.on('status_update', (status) => {
            this.updateSystemStatus(status);
        });
        
        this.socket.on('chat_response', (data) => {
            this.hideTypingIndicator();
            this.displayMessage(data.response, 'asis', data.type || 'conversation');
            this.scrollToBottom();
        });
    }
    
    updateCharCount() {
        const count = this.messageInput.value.length;
        this.charCount.textContent = `${count}/1000`;
        
        if (count > 800) {
            this.charCount.style.color = '#f56565';
        } else if (count > 600) {
            this.charCount.style.color = '#ed8936';
        } else {
            this.charCount.style.color = '#718096';
        }
    }
    
    toggleSendButton() {
        const hasText = this.messageInput.value.trim().length > 0;
        this.sendButton.disabled = !hasText;
    }
    
    sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message) return;
        
        // Display user message
        this.displayMessage(message, 'user');
        
        // Clear input
        this.messageInput.value = '';
        this.updateCharCount();
        this.toggleSendButton();
        
        // Show typing indicator
        this.showTypingIndicator();
        
        // Send via HTTP API (more reliable than socket for this use case)
        this.sendMessageHTTP(message);
        
        // Scroll to bottom
        this.scrollToBottom();
    }
    
    async sendMessageHTTP(message) {
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message })
            });
            
            const data = await response.json();
            
            this.hideTypingIndicator();
            
            if (data.error) {
                this.displayMessage(`❌ Error: ${data.error}`, 'asis', 'error');
            } else {
                this.displayMessage(data.response, 'asis', data.type || 'conversation', data.title);
            }
            
            this.scrollToBottom();
            
        } catch (error) {
            console.error('Error sending message:', error);
            this.hideTypingIndicator();
            this.displayMessage('❌ Connection error. Please try again.', 'asis', 'error');
            this.scrollToBottom();
        }
    }
    
    displayMessage(content, sender, type = 'conversation', title = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const avatarDiv = document.createElement('div');
        avatarDiv.className = 'message-avatar';
        avatarDiv.innerHTML = sender === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        const headerDiv = document.createElement('div');
        headerDiv.className = 'message-header';
        headerDiv.innerHTML = `
            <span class="message-author">${sender === 'user' ? 'You' : 'ASIS'}</span>
            <span class="message-time">${new Date().toLocaleTimeString()}</span>
        `;
        
        const textDiv = document.createElement('div');
        textDiv.className = `message-text ${type === 'conversation' ? '' : 'feature-response'}`;
        
        if (title && type !== 'conversation') {
            textDiv.innerHTML = `<strong>${title}</strong>\n\n${content}`;
        } else {
            textDiv.innerHTML = this.formatMessage(content);
        }
        
        contentDiv.appendChild(headerDiv);
        contentDiv.appendChild(textDiv);
        
        messageDiv.appendChild(avatarDiv);
        messageDiv.appendChild(contentDiv);
        
        this.chatMessages.appendChild(messageDiv);
    }
    
    formatMessage(content) {
        // Convert newlines to <br> for regular messages
        if (typeof content === 'string') {
            return content.replace(/\n/g, '<br>');
        }
        return content;
    }
    
    showTypingIndicator() {
        this.typingIndicator.style.display = 'flex';
    }
    
    hideTypingIndicator() {
        this.typingIndicator.style.display = 'none';
    }
    
    scrollToBottom() {
        setTimeout(() => {
            this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        }, 100);
    }
    
    updateStatus(text, type = 'success') {
        this.statusText.textContent = text;
        this.statusDot.className = `status-dot ${type === 'error' ? 'error' : type === 'warning' ? 'warning' : ''}`;
    }
    
    updateSystemStatus(status) {
        if (status.activated) {
            this.updateStatus('Active & Ready', 'success');
        } else if (status.initialized) {
            this.updateStatus('Initializing...', 'warning');
        } else {
            this.updateStatus('Offline', 'error');
        }
    }
    
    async checkSystemStatus() {
        try {
            const response = await fetch('/api/status');
            const status = await response.json();
            this.updateSystemStatus(status);
        } catch (error) {
            console.error('Error checking status:', error);
            this.updateStatus('Connection Error', 'error');
        }
    }
    
    async loadFeature(featureType) {
        this.openModal(`Loading ${featureType}...`);
        
        try {
            const response = await fetch(`/api/features/${featureType}`);
            const data = await response.json();
            
            if (data.success) {
                this.showModalContent(data.title, data.data);
            } else {
                this.showModalContent('Error', `❌ ${data.error}`);
            }
            
        } catch (error) {
            console.error('Error loading feature:', error);
            this.showModalContent('Error', `❌ Connection error: ${error.message}`);
        }
    }
    
    openModal(title) {
        this.modalTitle.textContent = title;
        this.modalSpinner.style.display = 'flex';
        this.modalContent.style.display = 'none';
        this.featureModal.classList.add('show');
        document.body.style.overflow = 'hidden';
    }
    
    showModalContent(title, content) {
        this.modalTitle.textContent = title;
        this.modalContent.textContent = content;
        this.modalSpinner.style.display = 'none';
        this.modalContent.style.display = 'block';
    }
    
    closeModal() {
        this.featureModal.classList.remove('show');
        document.body.style.overflow = 'auto';
    }
}

// Initialize chat when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ASISChat();
    
    // Periodic status check
    setInterval(async () => {
        try {
            const response = await fetch('/api/status');
            const status = await response.json();
            // Update status indicator if needed
        } catch (error) {
            console.error('Status check failed:', error);
        }
    }, 30000); // Check every 30 seconds
});
