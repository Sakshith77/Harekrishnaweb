// ===== Sidebar =====
function openSidebar() {
    document.getElementById('sidebar').classList.add('open');
    document.getElementById('sidebar-overlay').classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeSidebar() {
    document.getElementById('sidebar').classList.remove('open');
    document.getElementById('sidebar-overlay').classList.remove('active');
    document.body.style.overflow = '';
}

// ===== Loading Screen =====
document.addEventListener('DOMContentLoaded', function() {
    const loader = document.getElementById('loading-screen');
    if (loader) {
        setTimeout(function() {
            loader.classList.add('hidden');
        }, 1200);
    }
});

// ===== PWA Install =====
let deferredPrompt;
const installBtn = document.getElementById('install-btn');

window.addEventListener('beforeinstallprompt', function(e) {
    e.preventDefault();
    deferredPrompt = e;
    if (installBtn) installBtn.style.display = 'flex';
});

if (installBtn) {
    installBtn.addEventListener('click', async function() {
        if (!deferredPrompt) return;
        deferredPrompt.prompt();
        const { outcome } = await deferredPrompt.userChoice;
        if (outcome === 'accepted') {
            installBtn.style.display = 'none';
        }
        deferredPrompt = null;
    });
}

// ===== Service Worker Registration =====
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/sw.js')
            .then(function(registration) {
                console.log('SW registered:', registration.scope);
            })
            .catch(function(error) {
                console.log('SW registration failed:', error);
            });
    });
}

// ===== Auto-hide flash messages =====
document.addEventListener('DOMContentLoaded', function() {
    const flashes = document.querySelectorAll('.flash');
    flashes.forEach(function(flash) {
        setTimeout(function() {
            flash.style.opacity = '0';
            flash.style.transform = 'translateX(30px)';
            setTimeout(function() { flash.remove(); }, 400);
        }, 4000);
    });
});
