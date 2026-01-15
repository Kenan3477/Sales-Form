#!/usr/bin/env python3
"""
ASIS Mobile-Responsive Design Enhancement
=========================================

Mobile-first responsive design system for all ASIS web interfaces with
progressive web app capabilities and touch-optimized interactions.

Author: ASIS Development Team
Date: September 18, 2025
Version: 1.0
"""

def create_responsive_styles():
    """Create comprehensive responsive CSS styles"""
    return '''
/* ASIS Mobile-Responsive Design System */
/* ===================================== */

:root {
    --primary-green: #00ff88;
    --bg-primary: #0a0a0a;
    --bg-secondary: #1a1a1a;
    --bg-tertiary: #1e1e1e;
    --text-primary: #e0e0e0;
    --text-secondary: #ccc;
    --border-color: #333;
    --warning-color: #ffaa00;
    --error-color: #ff4444;
    --success-color: #00ff88;
    
    /* Mobile-specific variables */
    --mobile-padding: 16px;
    --mobile-margin: 12px;
    --touch-target-min: 44px;
    --mobile-font-base: 16px;
    --mobile-line-height: 1.5;
}

/* Base responsive reset */
* {
    box-sizing: border-box;
    -webkit-tap-highlight-color: transparent;
    -webkit-touch-callout: none;
}

/* Touch-friendly scrollbars */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: var(--bg-secondary);
}

::-webkit-scrollbar-thumb {
    background: var(--border-color);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--primary-green);
}

/* Mobile-first base styles */
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    font-size: var(--mobile-font-base);
    line-height: var(--mobile-line-height);
    margin: 0;
    padding: 0;
    background: var(--bg-primary);
    color: var(--text-primary);
    overflow-x: hidden;
    -webkit-text-size-adjust: 100%;
    -ms-text-size-adjust: 100%;
}

/* Mobile navigation */
.mobile-nav {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1000;
    background: var(--bg-secondary);
    border-bottom: 1px solid var(--border-color);
    padding: var(--mobile-padding);
}

.mobile-nav-toggle {
    background: none;
    border: none;
    color: var(--text-primary);
    font-size: 24px;
    cursor: pointer;
    padding: 8px;
    min-width: var(--touch-target-min);
    min-height: var(--touch-target-min);
    display: flex;
    align-items: center;
    justify-content: center;
}

.mobile-nav-title {
    flex: 1;
    text-align: center;
    font-weight: bold;
    color: var(--primary-green);
}

/* Mobile sidebar overlay */
.mobile-sidebar-overlay {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.8);
    z-index: 999;
}

.mobile-sidebar {
    position: fixed;
    top: 0;
    left: -300px;
    width: 300px;
    height: 100vh;
    background: var(--bg-secondary);
    border-right: 1px solid var(--border-color);
    z-index: 1000;
    transition: left 0.3s ease;
    overflow-y: auto;
    -webkit-overflow-scrolling: touch;
}

.mobile-sidebar.open {
    left: 0;
}

/* Touch-optimized buttons */
.btn, button, .nav-link, .filter-btn, .mode-button {
    min-height: var(--touch-target-min);
    min-width: var(--touch-target-min);
    padding: 12px 16px;
    border-radius: 8px;
    transition: all 0.2s ease;
    cursor: pointer;
    user-select: none;
    -webkit-user-select: none;
    touch-action: manipulation;
}

.btn:active, button:active, .nav-link:active, .filter-btn:active, .mode-button:active {
    transform: scale(0.98);
}

/* Mobile-optimized forms */
input, textarea, select {
    font-size: var(--mobile-font-base);
    padding: 12px 16px;
    border-radius: 8px;
    border: 1px solid var(--border-color);
    background: var(--bg-tertiary);
    color: var(--text-primary);
    min-height: var(--touch-target-min);
}

input:focus, textarea:focus, select:focus {
    outline: none;
    border-color: var(--primary-green);
    box-shadow: 0 0 0 2px rgba(0, 255, 136, 0.2);
}

/* Mobile chat interface */
.mobile-chat-input {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: var(--bg-secondary);
    border-top: 1px solid var(--border-color);
    padding: var(--mobile-padding);
    display: none;
}

.mobile-input-container {
    display: flex;
    gap: 12px;
    align-items: flex-end;
}

.mobile-message-input {
    flex: 1;
    max-height: 120px;
    resize: none;
    font-family: inherit;
}

.mobile-send-button {
    background: var(--primary-green);
    color: #000;
    border: none;
    font-weight: bold;
    border-radius: 50%;
    width: var(--touch-target-min);
    height: var(--touch-target-min);
    display: flex;
    align-items: center;
    justify-content: center;
}

/* Mobile card layouts */
.mobile-card-grid {
    display: none;
    flex-direction: column;
    gap: var(--mobile-margin);
    padding: var(--mobile-padding);
}

.mobile-card {
    background: var(--bg-tertiary);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: var(--mobile-padding);
    margin-bottom: var(--mobile-margin);
}

/* Mobile-optimized tables */
.mobile-table {
    display: none;
    width: 100%;
}

.mobile-table-row {
    background: var(--bg-tertiary);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    margin-bottom: 8px;
    padding: 12px;
}

.mobile-table-cell {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 4px 0;
    border-bottom: 1px solid var(--border-color);
}

.mobile-table-cell:last-child {
    border-bottom: none;
}

.mobile-table-label {
    font-weight: bold;
    color: var(--text-secondary);
    font-size: 14px;
}

.mobile-table-value {
    color: var(--text-primary);
}

/* Mobile progress indicators */
.mobile-progress {
    width: 100%;
    height: 6px;
    background: var(--border-color);
    border-radius: 3px;
    overflow: hidden;
    margin: 8px 0;
}

.mobile-progress-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--primary-green), #00cc6a);
    transition: width 0.5s ease;
}

/* Swipe gestures support */
.swipeable {
    touch-action: pan-y;
    position: relative;
    overflow: hidden;
}

.swipe-actions {
    position: absolute;
    top: 0;
    right: -100px;
    bottom: 0;
    width: 100px;
    background: var(--error-color);
    display: flex;
    align-items: center;
    justify-content: center;
    transition: right 0.3s ease;
}

.swipeable.swiped .swipe-actions {
    right: 0;
}

/* Loading states */
.mobile-loading {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 40px 20px;
    color: var(--text-secondary);
}

.mobile-spinner {
    width: 32px;
    height: 32px;
    border: 3px solid var(--border-color);
    border-top: 3px solid var(--primary-green);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-right: 12px;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Pull-to-refresh */
.pull-to-refresh {
    position: relative;
    overflow-y: auto;
    -webkit-overflow-scrolling: touch;
}

.pull-refresh-indicator {
    position: absolute;
    top: -60px;
    left: 0;
    right: 0;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-secondary);
    font-size: 14px;
    transition: transform 0.3s ease;
}

.pull-refresh-indicator.active {
    transform: translateY(60px);
}

/* Floating action button */
.mobile-fab {
    position: fixed;
    bottom: 80px;
    right: 20px;
    width: 56px;
    height: 56px;
    background: var(--primary-green);
    color: #000;
    border: none;
    border-radius: 50%;
    font-size: 24px;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(0, 255, 136, 0.3);
    z-index: 100;
    display: none;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
}

.mobile-fab:active {
    transform: scale(0.95);
}

/* Toast notifications */
.mobile-toast {
    position: fixed;
    bottom: 20px;
    left: 20px;
    right: 20px;
    background: var(--bg-tertiary);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 16px;
    color: var(--text-primary);
    font-size: 14px;
    z-index: 1001;
    transform: translateY(100px);
    transition: transform 0.3s ease;
}

.mobile-toast.show {
    transform: translateY(0);
}

.mobile-toast.success {
    border-color: var(--success-color);
    background: rgba(0, 255, 136, 0.1);
}

.mobile-toast.error {
    border-color: var(--error-color);
    background: rgba(255, 68, 68, 0.1);
}

/* RESPONSIVE BREAKPOINTS */
/* ===================== */

/* Extra small devices (phones, 320px and up) */
@media (max-width: 575.98px) {
    .dashboard-container,
    .chat-container {
        grid-template-columns: 1fr;
    }
    
    .sidebar,
    .chat-sidebar {
        display: none;
    }
    
    .mobile-nav {
        display: flex;
    }
    
    .main-content,
    .chat-main {
        padding-top: 70px;
        padding-left: var(--mobile-padding);
        padding-right: var(--mobile-padding);
    }
    
    .mobile-chat-input {
        display: block;
    }
    
    .input-area {
        display: none;
    }
    
    .mobile-fab {
        display: flex;
    }
    
    .mobile-card-grid {
        display: flex;
    }
    
    .stats-grid,
    .metrics-grid,
    .component-grid,
    .projects-grid {
        grid-template-columns: 1fr;
        gap: var(--mobile-margin);
    }
    
    .message {
        max-width: 95%;
        margin: 12px 0;
        padding: 12px 16px;
        font-size: 15px;
    }
    
    .header,
    .dashboard-header,
    .chat-header {
        flex-direction: column;
        gap: 12px;
        text-align: center;
        padding: var(--mobile-padding);
    }
    
    .mode-selector {
        justify-content: center;
        flex-wrap: wrap;
        gap: 6px;
    }
    
    .mode-button {
        min-width: auto;
        padding: 6px 12px;
        font-size: 12px;
    }
}

/* Small devices (landscape phones, 576px and up) */
@media (min-width: 576px) and (max-width: 767.98px) {
    .dashboard-container,
    .chat-container {
        grid-template-columns: 1fr;
    }
    
    .sidebar,
    .chat-sidebar {
        display: none;
    }
    
    .mobile-nav {
        display: flex;
    }
    
    .stats-grid,
    .metrics-grid {
        grid-template-columns: repeat(2, 1fr);
    }
    
    .projects-grid {
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    }
}

/* Medium devices (tablets, 768px and up) */
@media (min-width: 768px) and (max-width: 991.98px) {
    .dashboard-container,
    .chat-container {
        grid-template-columns: 250px 1fr;
    }
    
    .sidebar,
    .chat-sidebar {
        width: 250px;
        padding: 16px;
    }
    
    .stats-grid,
    .metrics-grid {
        grid-template-columns: repeat(3, 1fr);
    }
    
    .projects-grid {
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    }
}

/* Large devices (desktops, 992px and up) */
@media (min-width: 992px) and (max-width: 1199.98px) {
    .dashboard-container,
    .chat-container {
        grid-template-columns: 280px 1fr;
    }
    
    .stats-grid,
    .metrics-grid {
        grid-template-columns: repeat(4, 1fr);
    }
}

/* Extra large devices (large desktops, 1200px and up) */
@media (min-width: 1200px) {
    .dashboard-container,
    .chat-container {
        grid-template-columns: 320px 1fr;
    }
    
    .stats-grid,
    .metrics-grid {
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    }
    
    .projects-grid {
        grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    }
}

/* TOUCH AND GESTURE SUPPORT */
/* ========================= */

/* Smooth scrolling for touch devices */
html {
    scroll-behavior: smooth;
    -webkit-overflow-scrolling: touch;
}

/* Prevent zoom on input focus (iOS) */
@media screen and (max-width: 575.98px) {
    input, select, textarea {
        font-size: 16px !important;
    }
}

/* Hover states only for devices that can hover */
@media (hover: hover) and (pointer: fine) {
    .btn:hover,
    .nav-link:hover,
    .project-card:hover,
    .component-card:hover {
        transform: translateY(-2px);
    }
}

/* High DPI displays */
@media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {
    .status-dot,
    .connection-dot {
        border-radius: 1px;
    }
}

/* ACCESSIBILITY ENHANCEMENTS */
/* ========================== */

/* Focus indicators */
*:focus {
    outline: 2px solid var(--primary-green);
    outline-offset: 2px;
}

/* Reduced motion preference */
@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
    }
}

/* High contrast mode */
@media (prefers-contrast: high) {
    :root {
        --border-color: #666;
        --text-secondary: #fff;
    }
    
    .message,
    .card,
    .component-card,
    .project-card {
        border-width: 2px;
    }
}

/* Dark mode preference */
@media (prefers-color-scheme: light) {
    :root {
        --bg-primary: #f8f9fa;
        --bg-secondary: #ffffff;
        --bg-tertiary: #f1f3f4;
        --text-primary: #202124;
        --text-secondary: #5f6368;
        --border-color: #dadce0;
    }
}

/* PRINT STYLES */
/* ============ */

@media print {
    .sidebar,
    .mobile-nav,
    .mobile-fab,
    .input-area,
    .mobile-chat-input {
        display: none !important;
    }
    
    .dashboard-container,
    .chat-container {
        grid-template-columns: 1fr;
    }
    
    .main-content {
        padding: 0;
    }
    
    * {
        color: black !important;
        background: white !important;
    }
}
'''

def create_mobile_javascript():
    """Create mobile-specific JavaScript functionality"""
    return '''
/* ASIS Mobile-Responsive JavaScript */
/* ================================= */

class MobileInterface {
    constructor() {
        this.isMobile = window.innerWidth <= 768;
        this.isTouch = 'ontouchstart' in window;
        this.sidebarOpen = false;
        
        this.init();
    }
    
    init() {
        this.setupMobileNavigation();
        this.setupTouchGestures();
        this.setupPullToRefresh();
        this.setupResizeHandler();
        this.setupKeyboardAdjustment();
        this.setupToastSystem();
        
        // Progressive Web App features
        this.setupPWA();
        
        console.log('Mobile interface initialized', {
            isMobile: this.isMobile,
            isTouch: this.isTouch,
            userAgent: navigator.userAgent
        });
    }
    
    setupMobileNavigation() {
        // Create mobile navigation if it doesn't exist
        if (!document.querySelector('.mobile-nav')) {
            this.createMobileNav();
        }
        
        // Mobile menu toggle
        const toggleBtn = document.querySelector('.mobile-nav-toggle');
        const sidebar = document.querySelector('.mobile-sidebar');
        const overlay = document.querySelector('.mobile-sidebar-overlay');
        
        if (toggleBtn && sidebar && overlay) {
            toggleBtn.addEventListener('click', () => this.toggleMobileSidebar());
            overlay.addEventListener('click', () => this.closeMobileSidebar());
        }
        
        // Handle swipe to close sidebar
        if (sidebar) {
            let startX = 0;
            let currentX = 0;
            
            sidebar.addEventListener('touchstart', (e) => {
                startX = e.touches[0].clientX;
            }, { passive: true });
            
            sidebar.addEventListener('touchmove', (e) => {
                currentX = e.touches[0].clientX;
                const diff = startX - currentX;
                
                if (diff > 50 && startX < 50) {
                    this.closeMobileSidebar();
                }
            }, { passive: true });
        }
    }
    
    createMobileNav() {
        const nav = document.createElement('div');
        nav.className = 'mobile-nav';
        nav.innerHTML = `
            <button class="mobile-nav-toggle">☰</button>
            <div class="mobile-nav-title">ASIS Dashboard</div>
            <button class="mobile-nav-toggle" onclick="location.reload()">⟲</button>
        `;
        
        document.body.insertBefore(nav, document.body.firstChild);
        
        // Create mobile sidebar overlay
        const overlay = document.createElement('div');
        overlay.className = 'mobile-sidebar-overlay';
        document.body.appendChild(overlay);
        
        // Convert existing sidebar to mobile sidebar
        const existingSidebar = document.querySelector('.sidebar') || document.querySelector('.chat-sidebar');
        if (existingSidebar) {
            existingSidebar.classList.add('mobile-sidebar');
        }
    }
    
    toggleMobileSidebar() {
        const sidebar = document.querySelector('.mobile-sidebar');
        const overlay = document.querySelector('.mobile-sidebar-overlay');
        
        if (this.sidebarOpen) {
            this.closeMobileSidebar();
        } else {
            this.openMobileSidebar();
        }
    }
    
    openMobileSidebar() {
        const sidebar = document.querySelector('.mobile-sidebar');
        const overlay = document.querySelector('.mobile-sidebar-overlay');
        
        if (sidebar) sidebar.classList.add('open');
        if (overlay) overlay.style.display = 'block';
        
        this.sidebarOpen = true;
        document.body.style.overflow = 'hidden';
    }
    
    closeMobileSidebar() {
        const sidebar = document.querySelector('.mobile-sidebar');
        const overlay = document.querySelector('.mobile-sidebar-overlay');
        
        if (sidebar) sidebar.classList.remove('open');
        if (overlay) overlay.style.display = 'none';
        
        this.sidebarOpen = false;
        document.body.style.overflow = '';
    }
    
    setupTouchGestures() {
        if (!this.isTouch) return;
        
        // Add touch feedback to buttons
        document.addEventListener('touchstart', (e) => {
            if (e.target.matches('button, .btn, .nav-link, .card')) {
                e.target.style.transform = 'scale(0.98)';
            }
        }, { passive: true });
        
        document.addEventListener('touchend', (e) => {
            if (e.target.matches('button, .btn, .nav-link, .card')) {
                setTimeout(() => {
                    e.target.style.transform = '';
                }, 100);
            }
        }, { passive: true });
        
        // Swipe gestures for cards
        this.setupSwipeGestures();
    }
    
    setupSwipeGestures() {
        const swipeableElements = document.querySelectorAll('.project-card, .message, .swipeable');
        
        swipeableElements.forEach(element => {
            let startX = 0;
            let startY = 0;
            let currentX = 0;
            let currentY = 0;
            
            element.addEventListener('touchstart', (e) => {
                startX = e.touches[0].clientX;
                startY = e.touches[0].clientY;
            }, { passive: true });
            
            element.addEventListener('touchmove', (e) => {
                currentX = e.touches[0].clientX;
                currentY = e.touches[0].clientY;
                
                const diffX = startX - currentX;
                const diffY = startY - currentY;
                
                // Horizontal swipe (left/right)
                if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > 50) {
                    if (diffX > 0) {
                        // Swiped left
                        this.handleSwipeLeft(element);
                    } else {
                        // Swiped right
                        this.handleSwipeRight(element);
                    }
                }
            }, { passive: true });
        });
    }
    
    handleSwipeLeft(element) {
        // Add swipe left functionality (e.g., delete, archive)
        element.classList.add('swiped-left');
        setTimeout(() => element.classList.remove('swiped-left'), 300);
    }
    
    handleSwipeRight(element) {
        // Add swipe right functionality (e.g., favorite, complete)
        element.classList.add('swiped-right');
        setTimeout(() => element.classList.remove('swiped-right'), 300);
    }
    
    setupPullToRefresh() {
        const scrollableElements = document.querySelectorAll('.main-content, .messages-container');
        
        scrollableElements.forEach(element => {
            let startY = 0;
            let pulling = false;
            
            element.addEventListener('touchstart', (e) => {
                if (element.scrollTop === 0) {
                    startY = e.touches[0].clientY;
                    pulling = true;
                }
            }, { passive: true });
            
            element.addEventListener('touchmove', (e) => {
                if (!pulling) return;
                
                const currentY = e.touches[0].clientY;
                const diff = currentY - startY;
                
                if (diff > 100) {
                    this.showPullToRefreshIndicator(element);
                }
            }, { passive: true });
            
            element.addEventListener('touchend', (e) => {
                if (pulling) {
                    this.triggerRefresh(element);
                    pulling = false;
                }
            }, { passive: true });
        });
    }
    
    showPullToRefreshIndicator(element) {
        let indicator = element.querySelector('.pull-refresh-indicator');
        
        if (!indicator) {
            indicator = document.createElement('div');
            indicator.className = 'pull-refresh-indicator';
            indicator.innerHTML = '⟲ Pull to refresh';
            element.insertBefore(indicator, element.firstChild);
        }
        
        indicator.classList.add('active');
    }
    
    triggerRefresh(element) {
        const indicator = element.querySelector('.pull-refresh-indicator');
        
        if (indicator) {
            indicator.innerHTML = '🔄 Refreshing...';
            
            // Simulate refresh
            setTimeout(() => {
                location.reload();
            }, 1000);
        }
    }
    
    setupResizeHandler() {
        let resizeTimeout;
        
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(() => {
                this.isMobile = window.innerWidth <= 768;
                this.handleResize();
            }, 250);
        });
    }
    
    handleResize() {
        if (this.isMobile && this.sidebarOpen) {
            this.closeMobileSidebar();
        }
        
        // Update viewport height for mobile browsers
        document.documentElement.style.setProperty('--vh', `${window.innerHeight * 0.01}px`);
        
        // Adjust chat input position
        this.adjustChatInput();
    }
    
    setupKeyboardAdjustment() {
        if (!this.isMobile) return;
        
        const viewport = window.visualViewport;
        
        if (viewport) {
            viewport.addEventListener('resize', () => {
                this.adjustForKeyboard(viewport.height);
            });
        } else {
            // Fallback for older browsers
            window.addEventListener('resize', () => {
                this.adjustForKeyboard(window.innerHeight);
            });
        }
    }
    
    adjustForKeyboard(viewportHeight) {
        const chatInput = document.querySelector('.mobile-chat-input');
        const initialHeight = window.innerHeight;
        
        if (chatInput) {
            if (viewportHeight < initialHeight * 0.75) {
                // Keyboard is likely open
                chatInput.style.bottom = `${initialHeight - viewportHeight}px`;
            } else {
                // Keyboard is closed
                chatInput.style.bottom = '0';
            }
        }
    }
    
    adjustChatInput() {
        const messagesContainer = document.querySelector('.messages-container');
        const mobileInput = document.querySelector('.mobile-chat-input');
        
        if (messagesContainer && mobileInput && this.isMobile) {
            const inputHeight = mobileInput.offsetHeight;
            messagesContainer.style.paddingBottom = `${inputHeight + 20}px`;
        }
    }
    
    setupToastSystem() {
        this.toastContainer = document.createElement('div');
        this.toastContainer.className = 'toast-container';
        document.body.appendChild(this.toastContainer);
    }
    
    showToast(message, type = 'info', duration = 3000) {
        const toast = document.createElement('div');
        toast.className = `mobile-toast ${type}`;
        toast.textContent = message;
        
        this.toastContainer.appendChild(toast);
        
        // Show toast
        setTimeout(() => toast.classList.add('show'), 100);
        
        // Hide toast
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => {
                if (toast.parentNode) {
                    toast.parentNode.removeChild(toast);
                }
            }, 300);
        }, duration);
    }
    
    setupPWA() {
        // Service Worker registration
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/sw.js')
                .then(registration => {
                    console.log('Service Worker registered:', registration);
                })
                .catch(error => {
                    console.log('Service Worker registration failed:', error);
                });
        }
        
        // Install prompt
        let deferredPrompt;
        
        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            deferredPrompt = e;
            this.showInstallButton();
        });
        
        window.addEventListener('appinstalled', () => {
            console.log('ASIS PWA was installed');
            this.showToast('ASIS installed successfully!', 'success');
        });
    }
    
    showInstallButton() {
        const installBtn = document.createElement('button');
        installBtn.className = 'mobile-fab install-btn';
        installBtn.innerHTML = '📱';
        installBtn.title = 'Install ASIS App';
        
        installBtn.addEventListener('click', async () => {
            if (deferredPrompt) {
                deferredPrompt.prompt();
                const { outcome } = await deferredPrompt.userChoice;
                console.log(`User response to the install prompt: ${outcome}`);
                deferredPrompt = null;
                installBtn.remove();
            }
        });
        
        document.body.appendChild(installBtn);
    }
    
    // Utility methods
    vibrate(pattern = [100]) {
        if ('vibrate' in navigator) {
            navigator.vibrate(pattern);
        }
    }
    
    hapticFeedback(type = 'light') {
        if (window.DeviceMotionEvent && typeof DeviceMotionEvent.requestPermission === 'function') {
            // iOS haptic feedback
            this.vibrate(type === 'light' ? [10] : type === 'medium' ? [50] : [100]);
        } else {
            // Android vibration
            this.vibrate(type === 'light' ? [50] : type === 'medium' ? [100] : [200]);
        }
    }
    
    copyToClipboard(text) {
        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(text)
                .then(() => this.showToast('Copied to clipboard', 'success'))
                .catch(() => this.showToast('Failed to copy', 'error'));
        } else {
            // Fallback
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            this.showToast('Copied to clipboard', 'success');
        }
    }
    
    shareContent(data) {
        if (navigator.share) {
            navigator.share(data)
                .then(() => console.log('Shared successfully'))
                .catch((error) => console.log('Error sharing:', error));
        } else {
            // Fallback
            this.copyToClipboard(data.url || data.text);
        }
    }
}

// Service Worker for PWA
const serviceWorkerCode = `
// ASIS Service Worker
const CACHE_NAME = 'asis-v1';
const urlsToCache = [
    '/',
    '/static/css/mobile.css',
    '/static/js/mobile.js',
    '/chat',
    '/projects'
];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => cache.addAll(urlsToCache))
    );
});

self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request)
            .then((response) => {
                if (response) {
                    return response;
                }
                return fetch(event.request);
            })
    );
});
`;

// PWA Manifest
const pwaManifest = {
    "name": "ASIS Advanced Intelligence System",
    "short_name": "ASIS",
    "description": "Advanced AI Intelligence System Dashboard",
    "start_url": "/",
    "display": "standalone",
    "background_color": "#0a0a0a",
    "theme_color": "#00ff88",
    "orientation": "portrait-primary",
    "icons": [
        {
            "src": "/static/icons/icon-192x192.png",
            "sizes": "192x192",
            "type": "image/png"
        },
        {
            "src": "/static/icons/icon-512x512.png",
            "sizes": "512x512",
            "type": "image/png"
        }
    ],
    "categories": ["productivity", "utilities"],
    "lang": "en",
    "dir": "ltr"
};

// Initialize mobile interface when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.mobileInterface = new MobileInterface();
});

// Export for Node.js if needed
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { MobileInterface, serviceWorkerCode, pwaManifest };
}
'''

def create_pwa_files():
    """Create Progressive Web App files"""
    
    # Service Worker
    sw_js = '''
// ASIS Service Worker
const CACHE_NAME = 'asis-v1.0.0';
const urlsToCache = [
    '/',
    '/chat',
    '/projects',
    '/static/css/mobile.css',
    '/static/js/mobile.js',
    '/static/js/socket.io.min.js',
    '/static/js/chart.js'
];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                console.log('Opened cache');
                return cache.addAll(urlsToCache);
            })
    );
});

self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request)
            .then((response) => {
                // Cache hit - return response
                if (response) {
                    return response;
                }
                
                return fetch(event.request)
                    .then((response) => {
                        // Check if we received a valid response
                        if (!response || response.status !== 200 || response.type !== 'basic') {
                            return response;
                        }
                        
                        // Clone the response
                        var responseToCache = response.clone();
                        
                        caches.open(CACHE_NAME)
                            .then((cache) => {
                                cache.put(event.request, responseToCache);
                            });
                        
                        return response;
                    });
            })
    );
});

self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});
'''
    
    # Manifest
    manifest_json = '''{
    "name": "ASIS Advanced Intelligence System",
    "short_name": "ASIS",
    "description": "Advanced AI Intelligence System Dashboard with Multi-Mode Chat and Project Management",
    "start_url": "/",
    "display": "standalone",
    "background_color": "#0a0a0a",
    "theme_color": "#00ff88",
    "orientation": "portrait-primary",
    "scope": "/",
    "lang": "en",
    "dir": "ltr",
    "categories": ["productivity", "utilities", "education"],
    "icons": [
        {
            "src": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='192' height='192' viewBox='0 0 192 192'%3E%3Cg fill='%2300ff88'%3E%3Ccircle cx='96' cy='96' r='88' fill='%23000'/%3E%3Ctext x='96' y='110' font-family='monospace' font-size='48' text-anchor='middle' fill='%2300ff88'%3E🎯%3C/text%3E%3C/g%3E%3C/svg%3E",
            "sizes": "192x192",
            "type": "image/svg+xml"
        },
        {
            "src": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='512' height='512' viewBox='0 0 512 512'%3E%3Cg fill='%2300ff88'%3E%3Ccircle cx='256' cy='256' r='240' fill='%23000'/%3E%3Ctext x='256' y='300' font-family='monospace' font-size='128' text-anchor='middle' fill='%2300ff88'%3E🎯%3C/text%3E%3C/g%3E%3C/svg%3E",
            "sizes": "512x512",
            "type": "image/svg+xml"
        }
    ],
    "screenshots": [
        {
            "src": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='540' height='720' viewBox='0 0 540 720'%3E%3Crect width='540' height='720' fill='%23000'/%3E%3Ctext x='270' y='360' font-family='sans-serif' font-size='24' text-anchor='middle' fill='%2300ff88'%3EASIS Dashboard%3C/text%3E%3C/svg%3E",
            "sizes": "540x720",
            "type": "image/svg+xml",
            "form_factor": "narrow"
        }
    ]
}'''
    
    return sw_js, manifest_json

def main():
    """Create all mobile-responsive files"""
    print("📱 ASIS Mobile-Responsive Design System")
    print("=" * 50)
    
    # Create CSS file
    with open('static/css/mobile.css', 'w', encoding='utf-8') as f:
        f.write(create_responsive_styles())
    
    # Create JavaScript file
    with open('static/js/mobile.js', 'w', encoding='utf-8') as f:
        f.write(create_mobile_javascript())
    
    # Create PWA files
    sw_js, manifest_json = create_pwa_files()
    
    with open('sw.js', 'w', encoding='utf-8') as f:
        f.write(sw_js)
    
    with open('manifest.json', 'w', encoding='utf-8') as f:
        f.write(manifest_json)
    
    print("✅ Mobile-responsive CSS created")
    print("📱 Touch-optimized JavaScript added")
    print("🔄 Progressive Web App files generated")
    print("👆 Touch gestures and mobile navigation implemented")
    print("📏 Responsive breakpoints configured")
    print("♿ Accessibility enhancements included")
    print("🌐 PWA manifest and service worker ready")

if __name__ == "__main__":
    import os
    
    # Ensure directories exist
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    main()
