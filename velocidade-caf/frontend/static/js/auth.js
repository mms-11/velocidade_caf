/* ===============================
   AUTH - Autenticação FastAPI
   Velocidade C.A.F - v3.0 Integrado
   =============================== */

const API_BASE_URL = 'http://localhost:8000/api/v1';

/* === HELPER PARA POST JSON === */
async function postJSON(url, data) { 
  return fetch(url, { 
    method: 'POST', 
    headers: { 'Content-Type': 'application/json' }, 
    body: JSON.stringify(data) 
  }); 
}

/* === VALIDAÇÃO DE EMAIL === */
function isValidEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
}

/* === MOSTRAR FEEDBACK === */
function showFeedback(elementId, message, isError = false) {
  const feedbackEl = document.getElementById(elementId);
  if (!feedbackEl) {
    // Fallback para toast
    if (typeof showToast === 'function') {
      showToast(message, isError ? 'error' : 'success');
    }
    return;
  }
  
  feedbackEl.textContent = message;
  feedbackEl.style.display = 'block';
  feedbackEl.style.color = isError ? '#dc2626' : '#16a34a';
  feedbackEl.style.fontWeight = '500';
  feedbackEl.style.marginTop = '12px';
}

/* === INICIALIZAÇÃO === */
document.addEventListener('DOMContentLoaded', () => {
  setupLoginForm();
  setupRegisterForm();
  checkExistingAuth();
});

/* === VERIFICAR AUTENTICAÇÃO EXISTENTE === */
function checkExistingAuth() {
  const token = localStorage.getItem('authToken');
  const userRole = localStorage.getItem('userRole');
  
  // Se já está autenticado e está na página de login/register, redireciona
  if (token && (window.location.pathname === '/' || window.location.pathname === '/login.html' || window.location.pathname === '/register.html')) {
    if (userRole === 'treinador') {
      window.location.href = '/treinador-dash.html';
    } else {
      window.location.href = '/atleta-dash.html';
    }
  }
}

/* === LOGIN FORM === */
function setupLoginForm() {
  const loginForm = document.getElementById('loginForm');
  if (!loginForm) return;
  
  loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    
    // Validações
    if (!email || !password) {
      showFeedback('feedback', 'Preencha todos os campos', true);
      return;
    }
    
    if (!isValidEmail(email)) {
      showFeedback('feedback', 'Email inválido', true);
      return;
    }
    
    if (password.length < 8) {
      showFeedback('feedback', 'Senha deve ter no mínimo 8 caracteres', true);
      return;
    }
    
    // Desabilita o botão durante o processo
    const submitBtn = loginForm.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.disabled = true;
    submitBtn.textContent = 'Entrando...';
    
    try {
      const res = await postJSON(`${API_BASE_URL}/users/login`, { 
        email, 
        password 
      });
      
      const data = await res.json();
      
      if (!res.ok) { 
        showFeedback('feedback', data.detail || 'Erro ao fazer login', true);
        submitBtn.disabled = false;
        submitBtn.textContent = originalText;
        return;
      }
      
      // Salva token e informações do usuário
      localStorage.setItem('authToken', data.access_token);
      localStorage.setItem('userRole', data.user.role);
      localStorage.setItem('userId', data.user.id);
      localStorage.setItem('userEmail', data.user.email);
      
      // Redireciona baseado no role
      if (data.user.role === 'treinador') {
        window.location.href = '/treinador-dash.html';
      } else {
        window.location.href = '/atleta-dash.html';
      }
    } catch (error) {
      showFeedback('feedback', 'Erro de conexão. Tente novamente.', true);
      console.error('Login error:', error);
      submitBtn.disabled = false;
      submitBtn.textContent = originalText;
    }
  });
}

/* === REGISTER FORM === */
function setupRegisterForm() {
  const registerForm = document.getElementById('registerForm');
  if (!registerForm) return;
  
  registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword')?.value;
    const role = document.getElementById('role')?.value || 'atleta';
    
    // Validações
    if (!email || !password) {
      showFeedback('feedback', 'Preencha todos os campos', true);
      return;
    }
    
    if (!isValidEmail(email)) {
      showFeedback('feedback', 'Email inválido', true);
      return;
    }
    
    if (password.length < 8) {
      showFeedback('feedback', 'Senha deve ter no mínimo 8 caracteres', true);
      return;
    }
    
    if (confirmPassword && password !== confirmPassword) {
      showFeedback('feedback', 'As senhas não coincidem', true);
      return;
    }
    
    // Desabilita o botão durante o processo
    const submitBtn = registerForm.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.disabled = true;
    submitBtn.textContent = 'Criando conta...';
    
    try {
      const res = await postJSON(`${API_BASE_URL}/users/register`, { 
        email, 
        password, 
        role 
      });
      
      if (!res.ok) { 
        const d = await res.json();
        showFeedback('feedback', d.detail || 'Erro ao criar conta', true);
        submitBtn.disabled = false;
        submitBtn.textContent = originalText;
        return;
      }
      
      // Sucesso
      showFeedback('feedback', 'Conta criada! Faça login para continuar...', false);
      setTimeout(() => {
        window.location.href = '/login.html';
      }, 1500);
    } catch (error) {
      showFeedback('feedback', 'Erro de conexão. Tente novamente.', true);
      console.error('Register error:', error);
      submitBtn.disabled = false;
      submitBtn.textContent = originalText;
    }
  });
}

/* === LOGOUT GLOBAL === */
window.logoutNow = function() {
  localStorage.removeItem('authToken');
  localStorage.removeItem('userRole');
  localStorage.removeItem('userId');
  localStorage.removeItem('userEmail');
  window.location.href = '/login.html';
};

console.log('[Auth] Módulo de autenticação carregado');