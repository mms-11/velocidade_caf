/* ===============================
   ATLETA DASHBOARD - Sistema de Saltos
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
      
      try {
        localStorage.setItem('sidebar-expanded', sidebar.classList.contains('expanded'));
      } catch (e) {
        console.warn('Não foi possível salvar preferência da sidebar');
      }
    });
    
    // Restaura preferência
    try {
      const savedState = localStorage.getItem('sidebar-expanded');
      if (savedState === 'true') {
        sidebar.classList.add('expanded');
      }
    } catch (e) {
      console.warn('Não foi possível restaurar preferência da sidebar');
    }
  }
  
  const dateInput = document.getElementById('selectedDate');
  if (dateInput) {
    const today = new Date().toISOString().split('T')[0];
    dateInput.value = today;
    dateInput.addEventListener('change', loadDayData);
    
    loadDayData();
    loadWeekStats();
    loadRecordJump();
    loadAthleteName();
  }
  
  setupForm();
  setupLogout();
});

/* === CARREGAR NOME DO ATLETA === */
async function loadAthleteName() {
  const nameElement = document.getElementById('athleteName');
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

/* === CARREGAR DADOS DO DIA === */
async function loadDayData() {
  const dateInput = document.getElementById('selectedDate');
  if (!dateInput) return;
  
  const selectedDate = dateInput.value;
  if (!selectedDate) return;
  
  try {
    const response = await fetch(`${API_BASE_URL}/jumps/me`, {
      headers: getHeaders()
    });
    
    if (response.ok) {
      const jumps = await response.json();
      const jumpOfDay = jumps.find(j => j.date === selectedDate);
      
      if (jumpOfDay) {
        displayJumpData(jumpOfDay);
        fillFormForEdit(jumpOfDay);
      } else {
        resetDisplayAndForm();
      }
    } else if (response.status === 401) {
      logoutNow();
    } else {
      resetDisplayAndForm();
    }
  } catch (error) {
    console.error('Erro ao carregar dados:', error);
    if (!navigator.onLine) {
      showFeedback('Você está offline. Conecte-se à internet para sincronizar dados.', 'warning');
    }
    resetDisplayAndForm();
  }
}

/* === EXIBIR DADOS DOS SALTOS === */
function displayJumpData(data) {
  document.getElementById('salto1Display').textContent = data.jump1 + ' cm';
  document.getElementById('salto2Display').textContent = data.jump2 + ' cm';
  document.getElementById('salto3Display').textContent = (data.jump3 || 0) + ' cm';
  
  const media = data.average || ((data.jump1 + data.jump2 + (data.jump3 || 0)) / 3).toFixed(1);
  document.getElementById('mediaDia').textContent = media + ' cm';
}

/* === PREENCHER FORMULÁRIO PARA EDIÇÃO === */
function fillFormForEdit(data) {
  document.getElementById('recordId').value = data.id;
  document.getElementById('alturaS1').value = data.jump1;
  document.getElementById('alturaS2').value = data.jump2;
  document.getElementById('alturaS3').value = data.jump3 || '';
  document.getElementById('notes').value = data.observacoes || '';
  
  document.getElementById('formTitle').textContent = 'Editar Saltos do Dia';
  document.getElementById('submitBtn').textContent = 'Atualizar';
  document.getElementById('cancelBtn').style.display = 'inline-block';
  document.getElementById('deleteBtn').style.display = 'inline-block';
}

/* === CARREGAR RECORDE === */
async function loadRecordJump() {
  const recordElement = document.getElementById('maiorSalto');
  if (!recordElement) return;
  
  try {
    const response = await fetch(`${API_BASE_URL}/jumps/me/statistics`, {
      headers: getHeaders()
    });
    
    if (response.ok) {
      const data = await response.json();
      recordElement.textContent = data.melhor_salto ? data.melhor_salto + ' cm' : '-- cm';
    }
  } catch (error) {
    console.error('Erro ao carregar recorde:', error);
  }
}

/* === CARREGAR ESTATÍSTICAS DA SEMANA === */
async function loadWeekStats() {
  const weekElement = document.getElementById('treinosSemana');
  if (!weekElement) return;
  
  try {
    const response = await fetch(`${API_BASE_URL}/jumps/me/statistics`, {
      headers: getHeaders()
    });
    
    if (response.ok) {
      const data = await response.json();
      weekElement.textContent = (data.total_registros || 0) + '/7';
    }
  } catch (error) {
    console.error('Erro ao carregar estatísticas:', error);
  }
}

/* === RESETAR DISPLAY E FORMULÁRIO === */
function resetDisplayAndForm() {
  document.getElementById('salto1Display').textContent = '-- cm';
  document.getElementById('salto2Display').textContent = '-- cm';
  document.getElementById('salto3Display').textContent = '-- cm';
  document.getElementById('mediaDia').textContent = '-- cm';
  resetForm();
}

/* === RESETAR FORMULÁRIO === */
function resetForm() {
  const form = document.getElementById('dailyForm');
  if (form) form.reset();
  
  const dateInput = document.getElementById('selectedDate');
  if (dateInput) {
    dateInput.value = new Date().toISOString().split('T')[0];
  }
  
  document.getElementById('recordId').value = '';
  document.getElementById('formTitle').textContent = 'Registrar Saltos';
  document.getElementById('submitBtn').textContent = 'Registrar';
  document.getElementById('cancelBtn').style.display = 'none';
  document.getElementById('deleteBtn').style.display = 'none';
}

/* === SETUP DO FORMULÁRIO === */
function setupForm() {
  const dailyForm = document.getElementById('dailyForm');
  if (!dailyForm) return;
  
  dailyForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const recordId = document.getElementById('recordId').value;
    const selectedDate = document.getElementById('selectedDate').value;
    const jump1 = parseFloat(document.getElementById('alturaS1').value);
    const jump2 = parseFloat(document.getElementById('alturaS2').value);
    const jump3 = parseFloat(document.getElementById('alturaS3').value) || null;
    const notes = document.getElementById('notes').value;
    
    if (!jump1 || !jump2) {
      showFeedback('Preencha pelo menos os dois primeiros saltos', 'error');
      return;
    }
    
    if (jump1 < 0 || jump2 < 0 || (jump3 && jump3 < 0)) {
      showFeedback('Os valores dos saltos devem ser positivos', 'error');
      return;
    }
    
    const data = {
      date: selectedDate,
      jump1: jump1,
      jump2: jump2,
      jump3: jump3,
      observacoes: notes
    };
    
    try {
      let response;
      if (recordId) {
        response = await fetch(`${API_BASE_URL}/jumps/${recordId}`, {
          method: 'PUT',
          headers: getHeaders(),
          body: JSON.stringify(data)
        });
      } else {
        response = await fetch(`${API_BASE_URL}/jumps/`, {
          method: 'POST',
          headers: getHeaders(),
          body: JSON.stringify(data)
        });
      }
      
      if (response.ok) {
        showFeedback('Dados salvos com sucesso!', 'success');
        loadDayData();
        loadWeekStats();
        loadRecordJump();
      } else if (response.status === 401) {
        logoutNow();
      } else {
        const error = await response.json();
        showFeedback(error.detail || 'Erro ao salvar dados', 'error');
      }
    } catch (error) {
      console.error('Erro:', error);
      showFeedback('Erro ao conectar com o servidor', 'error');
    }
  });
  
  const cancelBtn = document.getElementById('cancelBtn');
  if (cancelBtn) {
    cancelBtn.addEventListener('click', resetForm);
  }
  
  const deleteBtn = document.getElementById('deleteBtn');
  if (deleteBtn) {
    deleteBtn.addEventListener('click', deleteRecord);
  }
}

/* === EXCLUIR REGISTRO === */
async function deleteRecord() {
  const recordId = document.getElementById('recordId').value;
  if (!recordId) return;
  
  if (!confirm('Tem certeza que deseja excluir este registro?')) return;
  
  try {
    const response = await fetch(`${API_BASE_URL}/jumps/${recordId}`, {
      method: 'DELETE',
      headers: getHeaders()
    });
    
    if (response.ok || response.status === 204) {
      showFeedback('Registro excluído com sucesso!', 'success');
      resetDisplayAndForm();
      loadWeekStats();
      loadRecordJump();
    } else {
      showFeedback('Erro ao excluir registro', 'error');
    }
  } catch (error) {
    console.error('Erro:', error);
    showFeedback('Erro ao conectar com o servidor', 'error');
  }
}

/* === MOSTRAR FEEDBACK === */
function showFeedback(message, type) {
  if (typeof showToast === 'function') {
    showToast(message, type);
    return;
  }
  
  const feedback = document.getElementById('feedback');
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

console.log('[Dashboard] Módulo carregado');
