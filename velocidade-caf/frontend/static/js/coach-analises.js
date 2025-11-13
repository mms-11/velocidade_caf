/* ===============================
   TREINADOR ANÁLISE - Estatísticas Avançadas
   Velocidade C.A.F - Integrado com FastAPI
   =============================== */

const API_BASE_URL = 'http://localhost:8000/api/v1';
let authToken = localStorage.getItem('authToken');
let selectedAthleteId = null;

/* === VERIFICAR AUTENTICAÇÃO === */
function checkAuth() {
  const userRole = localStorage.getItem('userRole');
  
  if (!authToken) {
    window.location.href = '/login.html';
    return false;
  }
  
  if (userRole !== 'treinador') {
    window.location.href = '/athlete-analises.html';
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
  
  loadMyAthletes();
  setupLogout();
  
  // Event listener para seleção de atleta
  document.getElementById('athleteSelect')?.addEventListener('change', (e) => {
    selectedAthleteId = e.target.value;
    if (selectedAthleteId) {
      loadAthleteAnalysis(selectedAthleteId);
    }
  });
});

/* === CARREGAR MEUS ATLETAS === */
async function loadMyAthletes() {
  const select = document.getElementById('athleteSelect');
  if (!select) return;
  
  try {
    const response = await fetch(`${API_BASE_URL}/coaches/me/athletes`, {
      headers: getHeaders()
    });
    
    if (response.ok) {
      const athletes = await response.json();
      
      select.innerHTML = '<option value="">Selecione um atleta</option>';
      athletes.forEach(athlete => {
        const option = document.createElement('option');
        option.value = athlete.id;
        option.textContent = athlete.nome_completo;
        select.appendChild(option);
      });
    } else if (response.status === 401) {
      logoutNow();
    }
  } catch (error) {
    console.error('Erro ao carregar atletas:', error);
  }
}

/* === CARREGAR ANÁLISE DO ATLETA === */
async function loadAthleteAnalysis(athleteId) {
  await Promise.all([
    loadAthleteProfile(athleteId),
    loadAthleteJumpStats(athleteId),
    loadAthleteMarkStats(athleteId),
    loadAthleteRecords(athleteId)
  ]);
}

/* === CARREGAR PERFIL DO ATLETA === */
async function loadAthleteProfile(athleteId) {
  try {
    const response = await fetch(`${API_BASE_URL}/athletes/${athleteId}`, {
      headers: getHeaders()
    });
    
    if (response.ok) {
      const profile = await response.json();
      displayAthleteProfile(profile);
    }
  } catch (error) {
    console.error('Erro ao carregar perfil:', error);
  }
}

/* === EXIBIR PERFIL DO ATLETA === */
function displayAthleteProfile(profile) {
  const container = document.getElementById('athlete-profile');
  if (!container) return;
  
  container.innerHTML = `
    <div class="profile-card">
      <h3>${profile.nome_completo}</h3>
      <div class="profile-details">
        <p><strong>Idade:</strong> ${calculateAge(profile.data_nascimento)} anos</p>
        <p><strong>Categoria:</strong> ${profile.categoria || 'Não definida'}</p>
        <p><strong>Altura:</strong> ${profile.altura || '--'} cm</p>
        <p><strong>Peso:</strong> ${profile.peso || '--'} kg</p>
      </div>
    </div>
  `;
}

/* === CARREGAR ESTATÍSTICAS DE SALTOS === */
async function loadAthleteJumpStats(athleteId) {
  try {
    const response = await fetch(`${API_BASE_URL}/jumps/athlete/${athleteId}`, {
      headers: getHeaders()
    });
    
    if (response.ok) {
      const jumps = await response.json();
      displayJumpStats(jumps);
    }
  } catch (error) {
    console.error('Erro ao carregar estatísticas de saltos:', error);
  }
}

/* === EXIBIR ESTATÍSTICAS DE SALTOS === */
function displayJumpStats(jumps) {
  const container = document.getElementById('jump-stats');
  if (!container) return;
  
  if (jumps.length === 0) {
    container.innerHTML = '<p class="muted">Nenhum salto registrado ainda.</p>';
    return;
  }
  
  const maxJumps = jumps.map(j => Math.max(j.jump1, j.jump2, j.jump3 || 0));
  const bestJump = Math.max(...maxJumps);
  const avgJump = (maxJumps.reduce((a, b) => a + b, 0) / maxJumps.length).toFixed(1);
  const lastJump = jumps[0];
  
  container.innerHTML = `
    <div class="stats-grid">
      <div class="stat-card">
        <h4>Melhor Salto</h4>
        <div class="stat-value">${bestJump} cm</div>
      </div>
      <div class="stat-card">
        <h4>Média Geral</h4>
        <div class="stat-value">${avgJump} cm</div>
      </div>
      <div class="stat-card">
        <h4>Total de Treinos</h4>
        <div class="stat-value">${jumps.length}</div>
      </div>
      <div class="stat-card">
        <h4>Último Treino</h4>
        <div class="stat-value">${formatDate(lastJump.date)}</div>
      </div>
    </div>
  `;
}

/* === CARREGAR ESTATÍSTICAS DE MARCAS === */
async function loadAthleteMarkStats(athleteId) {
  try {
    const response = await fetch(`${API_BASE_URL}/marks/athlete/${athleteId}`, {
      headers: getHeaders()
    });
    
    if (response.ok) {
      const marks = await response.json();
      displayMarkStats(marks);
    }
  } catch (error) {
    console.error('Erro ao carregar estatísticas de marcas:', error);
  }
}

/* === EXIBIR ESTATÍSTICAS DE MARCAS === */
function displayMarkStats(marks) {
  const container = document.getElementById('mark-stats');
  if (!container) return;
  
  if (marks.length === 0) {
    container.innerHTML = '<p class="muted">Nenhuma marca registrada ainda.</p>';
    return;
  }
  
  // Agrupa por evento
  const eventosMap = {};
  marks.forEach(mark => {
    if (!eventosMap[mark.evento]) {
      eventosMap[mark.evento] = [];
    }
    eventosMap[mark.evento].push(mark.resultado);
  });
  
  const eventos = Object.keys(eventosMap);
  const lastMark = marks[0];
  
  container.innerHTML = `
    <div class="stats-grid">
      <div class="stat-card">
        <h4>Eventos Praticados</h4>
        <div class="stat-value">${eventos.length}</div>
      </div>
      <div class="stat-card">
        <h4>Total de Marcas</h4>
        <div class="stat-value">${marks.length}</div>
      </div>
      <div class="stat-card">
        <h4>Última Competição</h4>
        <div class="stat-value">${formatDate(lastMark.data)}</div>
      </div>
      <div class="stat-card">
        <h4>Último Resultado</h4>
        <div class="stat-value">${lastMark.resultado}s</div>
      </div>
    </div>
  `;
}

/* === CARREGAR RECORDES === */
async function loadAthleteRecords(athleteId) {
  try {
    const response = await fetch(`${API_BASE_URL}/marks/athlete/${athleteId}`, {
      headers: getHeaders()
    });
    
    if (response.ok) {
      const marks = await response.json();
      
      // Agrupa por evento e pega o melhor
      const records = {};
      marks.forEach(mark => {
        if (!records[mark.evento] || mark.resultado < records[mark.evento].resultado) {
          records[mark.evento] = mark;
        }
      });
      
      displayRecords(Object.values(records));
    }
  } catch (error) {
    console.error('Erro ao carregar recordes:', error);
  }
}

/* === EXIBIR RECORDES === */
function displayRecords(records) {
  const container = document.getElementById('athlete-records');
  if (!container) return;
  
  if (records.length === 0) {
    container.innerHTML = '<p class="muted">Nenhum recorde pessoal ainda.</p>';
    return;
  }
  
  container.innerHTML = `
    <h4>Recordes Pessoais</h4>
    <div class="records-grid">
      ${records.map(record => `
        <div class="record-card">
          <h5>${translateEvento(record.evento)}</h5>
          <div class="record-time">${record.resultado}s</div>
          <p class="muted">${formatDate(record.data)} · ${record.local}</p>
        </div>
      `).join('')}
    </div>
  `;
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

/* === TRADUZIR EVENTO === */
function translateEvento(evento) {
  const map = {
    '100m': '100m',
    '200m': '200m',
    '400m': '400m',
    '800m': '800m',
    '1500m': '1500m',
    '110m_barreiras': '110m Barreiras',
    '100m_barreiras': '100m Barreiras',
    '400m_barreiras': '400m Barreiras'
  };
  return map[evento] || evento;
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

console.log('[Treinador Análise] Módulo carregado');