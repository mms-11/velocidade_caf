/* ===============================
   CONFIGURAÇÕES - Preferências do Sistema
   Velocidade C.A.F - Integrado com FastAPI
   =============================== */

const API_BASE_URL = 'http://localhost:8000/api/v1';
let authToken = localStorage.getItem('authToken');

/* === VERIFICAR AUTENTICAÇÃO === */
function checkAuth() {
  if (!authToken) {
    window.location.href = '/login.html';
    return false;
  }
  return true;
}

/* === HEADERS COM AUTENTICAÇÃO === */
function getHeaders() {
  return {
    'Authorization': `Bearer ${authToken}`,
    'Content-Type': 'application/json'
  };
}

/* === INICIALIZAÇÃO === */
document.addEventListener('DOMContentLoaded', () => {
  if (!checkAuth()) return;
  
  const sidebar = document.querySelector('.sidebar');
  const toggleBtn = document.querySelector('#sidebar-toggle');
  
  if (toggleBtn && sidebar) {
    toggleBtn.addEventListener('click', () => {
      sidebar.classList.toggle('expanded');
    });
  }
  
  loadUserInfo();
  loadPreferences();
  setupForms();
  setupLogout();
});

/* === CARREGAR INFORMAÇÕES DO USUÁRIO === */
async function loadUserInfo() {
  try {
    const response = await fetch(`${API_BASE_URL}/users/me`, {
      headers: getHeaders()
    });
    
    if (response.ok) {
      const user = await response.json();
      
      document.getElementById('user-email').textContent = user.email;
      document.getElementById('user-role').textContent = user.role === 'atleta' ? 'Atleta' : 'Treinador';
      document.getElementById('user-created').textContent = formatDate(user.created_at);
      document.getElementById('user-last-login').textContent = user.last_login ? formatDate(user.last_login) : 'Nunca';
    } else if (response.status === 401) {
      logoutNow();
    }
  } catch (error) {
    console.error('Erro ao carregar informações:', error);
  }
}

/* === CARREGAR PREFERÊNCIAS === */
function loadPreferences() {
  // Theme
  const savedTheme = localStorage.getItem('theme') || 'light';
  document.getElementById('theme-select').value = savedTheme;
  applyTheme(savedTheme);
  
  // Notificações
  const notificationsEnabled = localStorage.getItem('notifications') !== 'false';
  document.getElementById('notifications-toggle').checked = notificationsEnabled;
  
  // Sidebar
  const sidebarExpanded = localStorage.getItem('sidebar-expanded') === 'true';
  document.getElementById('sidebar-toggle-pref').checked = sidebarExpanded;
}

/* === APLICAR TEMA === */
function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('theme', theme);
}

/* === SETUP DOS FORMULÁRIOS === */
function setupForms() {
  // Alterar senha
  const passwordForm = document.getElementById('password-form');
  if (passwordForm) {
    passwordForm.addEventListener('submit', handlePasswordChange);
  }
  
  // Preferências
  const preferencesForm = document.getElementById('preferences-form');
  if (preferencesForm) {
    preferencesForm.addEventListener('submit', handlePreferencesChange);
  }
  
  // Theme select
  const themeSelect = document.getElementById('theme-select');
  if (themeSelect) {
    themeSelect.addEventListener('change', (e) => {
      applyTheme(e.target.value);
    });
  }
}

/* === ALTERAR SENHA === */
async function handlePasswordChange(e) {
  e.preventDefault();
  
  const currentPassword = document.getElementById('current-password').value;
  const newPassword = document.getElementById('new-password').value;
  const confirmPassword = document.getElementById('confirm-password').value;
  
  if (newPassword !== confirmPassword) {
    showFeedback('password-feedback', 'As senhas não coincidem', 'error');
    return;
  }
  
  if (newPassword.length < 8) {
    showFeedback('password-feedback', 'A senha deve ter no mínimo 8 caracteres', 'error');
    return;
  }
  
  try {
    // Primeiro verificar senha atual fazendo login
    const loginResponse = await fetch(`${API_BASE_URL}/users/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: localStorage.getItem('userEmail'),
        password: currentPassword
      })
    });
    
    if (!loginResponse.ok) {
      showFeedback('password-feedback', 'Senha atual incorreta', 'error');
      return;
    }
    
    // Atualizar senha
    const userId = localStorage.getItem('userId');
    const updateResponse = await fetch(`${API_BASE_URL}/users/${userId}`, {
      method: 'PUT',
      headers: getHeaders(),
      body: JSON.stringify({
        password: newPassword
      })
    });
    
    if (updateResponse.ok) {
      showFeedback('password-feedback', 'Senha alterada com sucesso!', 'success');
      document.getElementById('password-form').reset();
    } else {
      const error = await updateResponse.json();
      showFeedback('password-feedback', error.detail || 'Erro ao alterar senha', 'error');
    }
  } catch (error) {
    console.error('Erro:', error);
    showFeedback('password-feedback', 'Erro ao conectar com o servidor', 'error');
  }
}

/* === SALVAR PREFERÊNCIAS === */
function handlePreferencesChange(e) {
  e.preventDefault();
  
  const theme = document.getElementById('theme-select').value;
  const notifications = document.getElementById('notifications-toggle').checked;
  const sidebarExpanded = document.getElementById('sidebar-toggle-pref').checked;
  
  localStorage.setItem('theme', theme);
  localStorage.setItem('notifications', notifications);
  localStorage.setItem('sidebar-expanded', sidebarExpanded);
  
  applyTheme(theme);
  
  showFeedback('preferences-feedback', 'Preferências salvas com sucesso!', 'success');
}

/* === DELETAR CONTA === */
async function deleteAccount() {
  if (!confirm('⚠️ ATENÇÃO: Esta ação é irreversível!\n\nTem certeza que deseja deletar sua conta?\n\nTodos os seus dados serão permanentemente excluídos.')) {
    return;
  }
  
  if (!confirm('Última confirmação: Deletar minha conta permanentemente?')) {
    return;
  }
  
  try {
    const userId = localStorage.getItem('userId');
    const response = await fetch(`${API_BASE_URL}/users/${userId}`, {
      method: 'DELETE',
      headers: getHeaders()
    });
    
    if (response.ok || response.status === 204) {
      alert('Conta deletada com sucesso. Você será redirecionado para a página de login.');
      logoutNow();
    } else {
      alert('Erro ao deletar conta. Tente novamente mais tarde.');
    }
  } catch (error) {
    console.error('Erro:', error);
    alert('Erro ao conectar com o servidor');
  }
}

/* === EXPORTAR DADOS === */
async function exportData() {
  try {
    const userRole = localStorage.getItem('userRole');
    
    let data = {
      user: null,
      profile: null,
      jumps: null,
      marks: null
    };
    
    // User info
    const userResponse = await fetch(`${API_BASE_URL}/users/me`, {
      headers: getHeaders()
    });
    if (userResponse.ok) {
      data.user = await userResponse.json();
    }
    
    if (userRole === 'atleta') {
      // Profile
      const profileResponse = await fetch(`${API_BASE_URL}/athletes/me`, {
        headers: getHeaders()
      });
      if (profileResponse.ok) {
        data.profile = await profileResponse.json();
      }
      
      // Jumps
      const jumpsResponse = await fetch(`${API_BASE_URL}/jumps/me?limit=1000`, {
        headers: getHeaders()
      });
      if (jumpsResponse.ok) {
        data.jumps = await jumpsResponse.json();
      }
      
      // Marks
      const marksResponse = await fetch(`${API_BASE_URL}/marks/me?limit=1000`, {
        headers: getHeaders()
      });
      if (marksResponse.ok) {
        data.marks = await marksResponse.json();
      }
    } else {
      // Coach profile
      const profileResponse = await fetch(`${API_BASE_URL}/coaches/me`, {
        headers: getHeaders()
      });
      if (profileResponse.ok) {
        data.profile = await profileResponse.json();
      }
      
      // Athletes
      const athletesResponse = await fetch(`${API_BASE_URL}/coaches/me/athletes`, {
        headers: getHeaders()
      });
      if (athletesResponse.ok) {
        data.athletes = await athletesResponse.json();
      }
    }
    
    // Download JSON
    const dataStr = JSON.stringify(data, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `velocidade-caf-backup-${new Date().toISOString().split('T')[0]}.json`;
    link.click();
    
    showFeedback('preferences-feedback', 'Dados exportados com sucesso!', 'success');
  } catch (error) {
    console.error('Erro ao exportar dados:', error);
    showFeedback('preferences-feedback', 'Erro ao exportar dados', 'error');
  }
}

/* === FORMATAR DATA === */
function formatDate(dateStr) {
  const date = new Date(dateStr);
  return date.toLocaleDateString('pt-BR', { 
    day: '2-digit', 
    month: '2-digit', 
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}

/* === MOSTRAR FEEDBACK === */
function showFeedback(elementId, message, type) {
  const feedback = document.getElementById(elementId);
  if (!feedback) return;
  
  feedback.textContent = message;
  feedback.style.display = 'block';
  feedback.className = `feedback ${type}`;
  
  setTimeout(() => {
    feedback.style.display = 'none';
  }, 5000);
}

/* === LOGOUT === */
function logoutNow() {
  localStorage.clear();
  window.location.href = '/login.html';
}

function setupLogout() {
  const logoutBtn = document.getElementById('logoutBtn');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', (e) => { 
      e.preventDefault(); 
      logoutNow();
    });
  }
}

console.log('[Configurações] Módulo carregado');