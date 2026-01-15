
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
