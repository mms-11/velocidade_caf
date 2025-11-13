/* ===============================
   PWA Service Worker Registration
   Velocidade C.A.F - v3.0
   =============================== */

// Verifica se o navegador suporta Service Workers
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    registerServiceWorker();
  });
}

/* === REGISTRAR SERVICE WORKER === */
async function registerServiceWorker() {
  try {
    const registration = await navigator.serviceWorker.register('/static/sw.js', {
      scope: '/static/'
    });
    
    console.log('✅ Service Worker registrado com sucesso!');
    console.log('📍 Scope:', registration.scope);
    
    // Verifica se há atualização disponível
    registration.addEventListener('updatefound', () => {
      const newWorker = registration.installing;
      
      newWorker.addEventListener('statechange', () => {
        if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
          // Nova versão disponível
          console.log('🆕 Nova versão disponível!');
          
          // Você pode mostrar uma notificação para o usuário atualizar
          if (confirm('Nova versão disponível! Deseja atualizar agora?')) {
            newWorker.postMessage({ type: 'SKIP_WAITING' });
            window.location.reload();
          }
        }
      });
    });
    
  } catch (error) {
    console.error('❌ Erro ao registrar Service Worker:', error);
  }
}

/* === VERIFICAR STATUS DO SERVICE WORKER === */
navigator.serviceWorker.ready.then(registration => {
  console.log('🟢 Service Worker está ativo e pronto!');
  
  // Verificar atualizações periodicamente (a cada hora)
  setInterval(() => {
    registration.update();
  }, 60 * 60 * 1000);
});

/* === OUVIR MENSAGENS DO SERVICE WORKER === */
navigator.serviceWorker.addEventListener('message', event => {
  if (event.data && event.data.type === 'CACHE_UPDATED') {
    console.log('📦 Cache atualizado:', event.data.url);
  }
});

/* === LIMPAR CACHE (função auxiliar) === */
window.clearAppCache = async function() {
  if ('serviceWorker' in navigator) {
    const registration = await navigator.serviceWorker.ready;
    
    if (registration.active) {
      registration.active.postMessage({ type: 'CLEAR_CACHE' });
      console.log('🗑️ Cache limpo! Recarregue a página.');
    }
  }
};

/* === VERIFICAR SE ESTÁ ONLINE/OFFLINE === */
window.addEventListener('online', () => {
  console.log('🌐 Você está online!');
  document.body.classList.remove('offline');
  
  const indicator = document.getElementById('offlineIndicator');
  if (indicator) indicator.style.display = 'none';
  
  // Sincronizar dados pendentes
  if ('serviceWorker' in navigator && 'sync' in navigator.serviceWorker) {
    navigator.serviceWorker.ready.then(registration => {
      registration.sync.register('sync-data');
    });
  }
});

window.addEventListener('offline', () => {
  console.log('📴 Você está offline! Modo offline ativado.');
  document.body.classList.add('offline');
  
  const indicator = document.getElementById('offlineIndicator');
  if (indicator) {
    indicator.style.display = 'block';
    indicator.textContent = '📴 MODO OFFLINE';
  }
});

/* === PROMPT DE INSTALAÇÃO PWA === */
let deferredPrompt;

window.addEventListener('beforeinstallprompt', (e) => {
  // Previne o prompt automático
  e.preventDefault();
  deferredPrompt = e;
  
  console.log('💾 PWA pode ser instalado!');
  
  // Você pode mostrar um botão customizado de instalação aqui
  showInstallButton();
});

function showInstallButton() {
  // Exemplo: criar um botão de instalação
  const installBtn = document.getElementById('install-btn');
  
  if (installBtn) {
    installBtn.style.display = 'block';
    
    installBtn.addEventListener('click', async () => {
      if (deferredPrompt) {
        deferredPrompt.prompt();
        
        const { outcome } = await deferredPrompt.userChoice;
        
        if (outcome === 'accepted') {
          console.log('✅ PWA instalado!');
        } else {
          console.log('❌ Instalação cancelada');
        }
        
        deferredPrompt = null;
        installBtn.style.display = 'none';
      }
    });
  }
}

/* === DETECTAR SE JÁ ESTÁ INSTALADO === */
window.addEventListener('appinstalled', () => {
  console.log('🎉 PWA instalado com sucesso!');
  deferredPrompt = null;
});

console.log('[PWA] Módulo de registro carregado');
