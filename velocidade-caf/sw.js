/* ===============================
   SERVICE WORKER - Velocidade C.A.F
   Versão: 3.0
   =============================== */

const CACHE_NAME = 'vcaf-cache-v3';
const RUNTIME_CACHE = 'vcaf-runtime-v3';

// Arquivos para pre-cache (instalação)
const PRECACHE_URLS = [
  '/',
  '/index.html',
  '/register.html',
  '/athlete-analises.html',
  '/dashboard2.html',
  '/dashboard3.html',
  '/dash1.html',
  '/coach-dash.html',
  '/coach-testes.html',
  '/coach-config.html',
  '/coach-analise.html',
  '/static/css/style.css',
  '/static/css/dashboard.css',
  '/static/js/auth.js',
  '/static/js/dashboard.js',
  '/static/js/athlete-dashboard.js',
  '/static/js/athlete-perfil.js',
  '/static/js/athlete-marks.js',
  '/static/js/sthletes-stats.js',
  '/static/js/config.js',
  '/static/js/coach-analises.js',
  '/static/js/pwa-register.js',
  '/static/manifest.json'
];

/* === INSTALAÇÃO === */
self.addEventListener('install', event => {
  console.log('[SW] 🔧 Instalando service worker...');
  
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('[SW] 📦 Cache aberto, adicionando arquivos...');
        return cache.addAll(PRECACHE_URLS);
      })
      .then(() => {
        console.log('[SW] ✅ Todos os arquivos em cache!');
        return self.skipWaiting();
      })
      .catch(error => {
        console.error('[SW] ❌ Erro ao instalar:', error);
      })
  );
});

/* === ATIVAÇÃO === */
self.addEventListener('activate', event => {
  console.log('[SW] 🟢 Ativando service worker...');
  
  event.waitUntil(
    caches.keys()
      .then(cacheNames => {
        return Promise.all(
          cacheNames.map(cacheName => {
            if (cacheName !== CACHE_NAME && cacheName !== RUNTIME_CACHE) {
              console.log('[SW] 🗑️ Deletando cache antigo:', cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      })
      .then(() => {
        console.log('[SW] ✅ Service worker ativado!');
        return self.clients.claim();
      })
  );
});

/* === FETCH - ESTRATÉGIA DE CACHE === */
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);
  
  // Ignora requisições de outros domínios (exceto CDN)
  if (url.origin !== location.origin && !url.hostname.includes('cdn')) {
    return;
  }
  
  // Estratégia para chamadas de API
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(networkFirst(request));
    return;
  }
  
  // Estratégia para navegação HTML
  if (request.mode === 'navigate') {
    event.respondWith(networkFirst(request));
    return;
  }
  
  // Estratégia para assets estáticos (CSS, JS, imagens)
  if (request.destination === 'style' || 
      request.destination === 'script' || 
      request.destination === 'image') {
    event.respondWith(cacheFirst(request));
    return;
  }
  
  // Default: Network First
  event.respondWith(networkFirst(request));
});

/* === ESTRATÉGIA: CACHE FIRST === */
async function cacheFirst(request) {
  const cachedResponse = await caches.match(request);
  
  if (cachedResponse) {
    console.log('[SW] 📂 Servindo do cache:', request.url);
    // Atualiza cache em background
    updateCache(request);
    return cachedResponse;
  }
  
  console.log('[SW] 🌐 Não encontrado no cache, buscando na rede:', request.url);
  return fetchAndCache(request);
}

/* === ESTRATÉGIA: NETWORK FIRST === */
async function networkFirst(request) {
  try {
    const networkResponse = await fetch(request, { credentials: 'include' });
    
    // Se sucesso, cacheia para uso offline
    if (networkResponse && networkResponse.status === 200) {
      const cache = await caches.open(RUNTIME_CACHE);
      cache.put(request, networkResponse.clone());
    }
    
    return networkResponse;
  } catch (error) {
    console.log('[SW] 📴 Rede falhou, tentando cache:', request.url);
    
    const cachedResponse = await caches.match(request);
    
    if (cachedResponse) {
      return cachedResponse;
    }
    
    // Se é navegação e não tem cache, retorna página offline
    if (request.mode === 'navigate') {
      return caches.match('/index.html');
    }
    
    // Retorna erro genérico
    return new Response('Offline - Recurso não disponível', {
      status: 503,
      statusText: 'Service Unavailable',
      headers: new Headers({
        'Content-Type': 'text/plain'
      })
    });
  }
}

/* === ATUALIZAR CACHE EM BACKGROUND === */
async function updateCache(request) {
  try {
    const response = await fetch(request);
    if (response && response.status === 200) {
      const cache = await caches.open(CACHE_NAME);
      await cache.put(request, response);
    }
  } catch (error) {
    // Silenciosamente falha se não conseguir atualizar
  }
}

/* === BUSCAR E CACHEAR === */
async function fetchAndCache(request) {
  try {
    const response = await fetch(request);
    
    if (response && response.status === 200) {
      const cache = await caches.open(CACHE_NAME);
      cache.put(request, response.clone());
    }
    
    return response;
  } catch (error) {
    console.error('[SW] ❌ Erro ao buscar:', error);
    throw error;
  }
}

/* === MENSAGENS === */
self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
  
  if (event.data && event.data.type === 'CLEAR_CACHE') {
    event.waitUntil(
      caches.keys().then(cacheNames => {
        return Promise.all(
          cacheNames.map(cacheName => caches.delete(cacheName))
        );
      })
    );
  }
});

/* === SYNC EM BACKGROUND (para quando voltar online) === */
self.addEventListener('sync', event => {
  if (event.tag === 'sync-data') {
    event.waitUntil(syncData());
  }
});

async function syncData() {
  // Implementar sincronização de dados quando voltar online
  console.log('[SW] 🔄 Sincronizando dados...');
}

console.log('[SW] 🚀 Service Worker carregado - Velocidade C.A.F v3.0');

if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/static/sw.js')
    .then(reg => console.log('✅ SW registrado'))
    .catch(err => console.log('❌ Erro SW:', err));
}