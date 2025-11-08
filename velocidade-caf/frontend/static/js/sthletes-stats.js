/* ===============================
   ATLETA PERFIL - Informações Pessoais
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

/* === SIDEBAR TOGGLE === */
document.addEventListener('DOMContentLoaded', () => {
  if (!checkAuth()) return;
  
  const sidebar = document.querySelector('.sidebar');
  const toggleBtn = document.querySelector('#sidebar-toggle');
  
  if (toggleBtn && sidebar) {
    toggleBtn.addEventListener('click', () => {
      sidebar.classList.toggle('expanded');
    });
  }
  
  loadProfile();
  setupForm();
  setupLogout();
});

/* === CARREGAR PERFIL === */
async function loadProfile() {
  try {
    const response = await fetch(`${API_BASE_URL}/athletes/me`, {
      headers: getHeaders()
    });
    
    if (response.ok) {
      const profile = await response.json();
      fillForm(profile);
      updatePreview(profile);
    } else if (response.status === 404) {
      // Perfil ainda não foi criado
      console.log('Perfil não encontrado, crie um novo');
    } else if (response.status === 401) {
      logoutNow();
    }
  } catch (error) {
    console.error('Erro ao carregar perfil:', error);
  }
}

/* === PREENCHER FORMULÁRIO === */
function fillForm(profile) {
  document.getElementById('nome').value = profile.nome_completo || '';
  document.getElementById('dataNascimento').value = profile.data_nascimento || '';
  document.getElementById('altura').value = profile.altura || '';
  document.getElementById('peso').value = profile.peso || '';
  document.getElementById('tamanhoPe').value = profile.tamanho_pe || '';
  document.getElementById('endereco').value = profile.endereco || '';
  document.getElementById('provaPrincipal').value = profile.prova_principal || '';
  document.getElementById('provaSecundaria').value = profile.prova_secundaria || '';
}

/* === ATUALIZAR PRÉ-VISUALIZAÇÃO === */
function updatePreview(profile) {
  document.getElementById('pv-nome').textContent = profile.nome_completo || '—';
  document.getElementById('pv-dataNascimento').textContent = profile.data_nascimento ? formatDate(profile.data_nascimento) : '—';
  document.getElementById('pv-idade').textContent = profile.data_nascimento ? calculateAge(profile.data_nascimento) + ' anos' : '—';
  document.getElementById('pv-altura').textContent = profile.altura ? profile.altura + ' cm' : '—';
  document.getElementById('pv-peso').textContent = profile.peso ? profile.peso + ' kg' : '—';
  document.getElementById('pv-tamanhoPe').textContent = profile.tamanho_pe || '—';
  document.getElementById('pv-endereco').textContent = profile.endereco || '—';
  document.getElementById('pv-provaPrincipal').textContent = translateProva(profile.prova_principal) || '—';
  document.getElementById('pv-provaSecundaria').textContent = translateProva(profile.prova_secundaria) || '—';
}

/* === CALCULAR IDADE === */
function calculateAge(birthDate) {
  const today = new Date();
  const birth = new Date(birthDate + 'T00:00:00');
  let age = today.getFullYear() - birth.getFullYear();
  const monthDiff = today.getMonth() - birth.getMonth();
  
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
    age--;
  }
  
  return age;
}

/* === FORMATAR DATA === */
function formatDate(dateStr) {
  const date = new Date(dateStr + 'T00:00:00');
  return date.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric' });
}

/* === TRADUZIR PROVA === */
function translateProva(prova) {
  const map = {
    '100m': '100m rasos',
    '200m': '200m rasos',
    '400m': '400m rasos',
    '800m': '800m',
    '1500m': '1500m',
    '110m_barreiras': '110m com barreiras',
    '100m_barreiras': '100m com barreiras',
    '400m_barreiras': '400m com barreiras',
    'outro': 'Outro'
  };
  return map[prova] || prova;
}

/* === SETUP DO FORMULÁRIO === */
function setupForm() {
  const form = document.getElementById('athlete-form');
  if (!form) return;
  
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const nome = document.getElementById('nome').value.trim();
    const dataNascimento = document.getElementById('dataNascimento').value;
    const altura = parseFloat(document.getElementById('altura').value) || null;
    const peso = parseFloat(document.getElementById('peso').value) || null;
    const tamanhoPe = parseInt(document.getElementById('tamanhoPe').value) || null;
    const endereco = document.getElementById('endereco').value.trim();
    const provaPrincipal = document.getElementById('provaPrincipal').value;
    const provaSecundaria = document.getElementById('provaSecundaria').value;
    
    if (!nome || !dataNascimento) {
      showFeedback('Preencha pelo menos nome e data de nascimento', 'error');
      return;
    }
    
    const profileData = {
      nome_completo: nome,
      data_nascimento: dataNascimento,
      altura: altura,
      peso: peso,
      tamanho_pe: tamanhoPe,
      endereco: endereco,
      prova_principal: provaPrincipal,
      prova_secundaria: provaSecundaria,
      genero: null,
      nacionalidade: null,
      categoria: null,
      melhor_marca_100m: null,
      melhor_marca_200m: null,
      record_pessoal: null
    };
    
    try {
      // Verifica se perfil já existe
      const checkResponse = await fetch(`${API_BASE_URL}/athletes/me`, {
        headers: getHeaders()
      });
      
      let response;
      if (checkResponse.ok) {
        // Atualiza perfil existente
        response = await fetch(`${API_BASE_URL}/athletes/me`, {
          method: 'PUT',
          headers: getHeaders(),
          body: JSON.stringify(profileData)
        });
      } else {
        // Cria novo perfil
        response = await fetch(`${API_BASE_URL}/athletes/`, {
          method: 'POST',
          headers: getHeaders(),
          body: JSON.stringify(profileData)
        });
      }
      
      if (response.ok) {
        const profile = await response.json();
        showFeedback('Perfil salvo com sucesso!', 'success');
        updatePreview(profile);
      } else if (response.status === 401) {
        logoutNow();
      } else {
        const error = await response.json();
        showFeedback(error.detail || 'Erro ao salvar perfil', 'error');
      }
    } catch (error) {
      console.error('Erro:', error);
      showFeedback('Erro ao conectar com o servidor', 'error');
    }
  });
}

/* === MOSTRAR FEEDBACK === */
function showFeedback(message, type) {
  const feedback = document.getElementById('feedback');
  if (!feedback) return;
  
  feedback.textContent = message;
  feedback.style.display = 'block';
  feedback.style.backgroundColor = type === 'error' ? '#fee2e2' : '#d1fae5';
  feedback.style.color = type === 'error' ? '#991b1b' : '#065f46';
  feedback.style.border = `1px solid ${type === 'error' ? '#fecaca' : '#a7f3d0'}`;
  
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

console.log('[Perfil] Módulo carregado');