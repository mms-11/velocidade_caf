/* ===============================
   TREINADOR DASHBOARD - Visão Geral
   Velocidade C.A.F - Integrado com FastAPI
   =============================== */

const API_BASE_URL = 'http://localhost:8000/api/v1';
let authToken = localStorage.getItem('authToken');

/* === VERIFICAR AUTENTICAÇÃO === */
function checkAuth() {
  const userRole = localStorage.getItem('userRole');
  
  if (!authToken) {
    window.location.href = '/login.html';
    return false;
  }
  
  if (userRole !== 'treinador') {
    window.location.href = '/atleta-dash.html';
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
  
  loadCoachName();
  loadDashboardStats();
  loadMyAthletes();
  setupLogout();
});

/* === CARREGAR NOME DO TREINADOR === */
async function loadCoachName() {
  const nameElement = document.getElementById('coachName');
  if (!nameElement) return;
  
  try {
    const response = await fetch(`${API_BASE_URL}/users/me`, {
      headers: getHeaders()
    });
    
    if (response.ok) {
      const data = await response.json();
      nameElement.textContent = data.email.split('@')[0].toUpperCase();
    } else if (response.status === 401) {
      logoutNow();
    }
  } catch (error) {
    console.error('Erro ao carregar nome:', error);
  }
}

/* === CARREGAR ESTATÍSTICAS DO DASHBOARD === */
async function loadDashboardStats() {
  try {
    // Buscar atletas do treinador
    const athletesResponse = await fetch(`${API_BASE_URL}/coaches/me/athletes`, {
      headers: getHeaders()
    });
    
    if (athletesResponse.ok) {
      const athletes = await athletesResponse.json();
      
      document.getElementById('total-atletas').textContent = athletes.length;
      
      // Buscar estatísticas de cada atleta
      let totalTreinos = 0;
      let totalProvas = 0;
      
      for (const athlete of athletes) {
        // Saltos
        const jumpsResponse = await fetch(`${API_BASE_URL}/jumps/athlete/${athlete.id}`, {
          headers: getHeaders()
        });
        if (jumpsResponse.ok) {
          const jumps = await jumpsResponse.json();
          totalTreinos += jumps.length;
        }
        
        // Marcas
        const marksResponse = await fetch(`${API_BASE_URL}/marks/athlete/${athlete.id}`, {
          headers: getHeaders()
        });
        if (marksResponse.ok) {
          const marks = await marksResponse.json();
          totalProvas += marks.length;
        }
      }
      
      document.getElementById('total-treinos').textContent = totalTreinos;
      document.getElementById('total-provas').textContent = totalProvas;
      
      // Atividade recente (última semana)
      const weekAgo = new Date();
      weekAgo.setDate(weekAgo.getDate() - 7);
      document.getElementById('atividade-semana').textContent = '-- ativ.';
    }
  } catch (error) {
    console.error('Erro ao carregar estatísticas:', error);
  }
}

/* === CARREGAR MEUS ATLETAS === */
async function loadMyAthletes() {
  const container = document.getElementById('athletes-list');
  if (!container) return;
  
  container.innerHTML = '<p class="muted">Carregando atletas...</p>';
  
  try {
    const response = await fetch(`${API_BASE_URL}/coaches/me/athletes`, {
      headers: getHeaders()
    });
    
    if (response.ok) {
      const athletes = await response.json();
      
      if (athletes.length === 0) {
        container.innerHTML = '<p class="muted">Você ainda não tem atletas cadastrados.</p>';
        return;
      }
      
      displayAthletes(athletes);
    } else if (response.status === 401) {
      logoutNow();
    } else {
      container.innerHTML = '<p class="muted">Erro ao carregar atletas</p>';
    }
  } catch (error) {
    console.error('Erro ao carregar atletas:', error);
    container.innerHTML = '<p class="muted">Erro de conexão. Tente novamente.</p>';
  }
}

/* === EXIBIR ATLETAS === */
async function displayAthletes(athletes) {
  const container = document.getElementById('athletes-list');
  if (!container) return;
  
  const athletesWithStats = await Promise.all(athletes.map(async (athlete) => {
    // Buscar última atividade
    const jumpsResponse = await fetch(`${API_BASE_URL}/jumps/athlete/${athlete.id}?limit=1`, {
      headers: getHeaders()
    });
    
    let lastActivity = 'Sem atividade';
    if (jumpsResponse.ok) {
      const jumps = await jumpsResponse.json();
      if (jumps.length > 0) {
        lastActivity = formatDate(jumps[0].date);
      }
    }
    
    return { ...athlete, lastActivity };
  }));
  
  container.innerHTML = athletesWithStats.map(athlete => `
    <div class="athlete-card">
      <div class="athlete-avatar">
        ${athlete.nome_completo ? athlete.nome_completo.charAt(0).toUpperCase() : 'A'}
      </div>
      <div class="athlete-info">
        <h4>${athlete.nome_completo || 'Atleta'}</h4>
        <p class="muted">Última atividade: ${athlete.lastActivity}</p>
        <p class="muted">Categoria: ${athlete.categoria || 'Não definida'}</p>
      </div>
      <div class="athlete-actions">
        <button onclick="viewAthleteDetails('${athlete.id}')" class="btn btn-sm">Ver Detalhes</button>
      </div>
    </div>
  `).join('');
}

/* === VER DETALHES DO ATLETA === */
function viewAthleteDetails(athleteId) {
  window.location.href = `/treinador-analise.html?athlete=${athleteId}`;
}

/* === FORMATAR DATA === */
function formatDate(dateStr) {
  const date = new Date(dateStr + 'T00:00:00');
  return date.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric' });
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

console.log('[Treinador Dashboard] Módulo carregado');