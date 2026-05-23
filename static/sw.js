const CACHE_NAME = 'hare-krishna-v1';
const STATIC_ASSETS = [
    '/',
    '/static/css/style.css',
    '/static/js/main.js',
    '/static/js/audio-player.js',
    '/static/manifest.json',
    'https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Inter:wght@300;400;500;600;700&display=swap',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css'
];

// Install - cache static assets
self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open(CACHE_NAME).then(function(cache) {
            return cache.addAll(STATIC_ASSETS);
        }).then(function() {
            return self.skipWaiting();
        })
    );
});

// Activate - clean old caches
self.addEventListener('activate', function(event) {
    event.waitUntil(
        caches.keys().then(function(cacheNames) {
            return Promise.all(
                cacheNames.filter(function(name) {
                    return name !== CACHE_NAME;
                }).map(function(name) {
                    return caches.delete(name);
                })
            );
        }).then(function() {
            return self.clients.claim();
        })
    );
});

// Fetch - cache-first strategy for static, network-first for dynamic
self.addEventListener('fetch', function(event) {
    const request = event.request;
    const url = new URL(request.url);

    // Skip non-GET requests
    if (request.method !== 'GET') return;

    // Skip chrome-extension and other non-http schemes
    if (!url.protocol.startsWith('http')) return;

    // For API calls - network only
    if (url.pathname.startsWith('/api/')) {
        event.respondWith(fetch(request));
        return;
    }

    // For static assets - cache first
    if (STATIC_ASSETS.includes(url.pathname) || 
        url.pathname.startsWith('/static/') ||
        url.pathname.endsWith('.css') ||
        url.pathname.endsWith('.js') ||
        url.pathname.endsWith('.png') ||
        url.pathname.endsWith('.jpg') ||
        url.pathname.endsWith('.svg')) {
        event.respondWith(
            caches.match(request).then(function(response) {
                return response || fetch(request).then(function(networkResponse) {
                    return caches.open(CACHE_NAME).then(function(cache) {
                        cache.put(request, networkResponse.clone());
                        return networkResponse;
                    });
                });
            })
        );
        return;
    }

    // For HTML pages - network first, fallback to cache
    event.respondWith(
        fetch(request).then(function(networkResponse) {
            return caches.open(CACHE_NAME).then(function(cache) {
                cache.put(request, networkResponse.clone());
                return networkResponse;
            });
        }).catch(function() {
            return caches.match(request).then(function(response) {
                if (response) return response;
                return caches.match('/');
            });
        })
    );
});
