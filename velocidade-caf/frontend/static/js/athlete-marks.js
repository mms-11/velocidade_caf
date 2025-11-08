/* ===============================
   ATLETA MARCAS - Resultados e Competições
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
  
  setupForm();
  loadMarks();
  setupLogout();
  
  // Event listeners para filtros
  document.getElementById('filterProva')?.addEventListener('change', loadMarks);
  document.getElementById('filterTipo')?.addEventListener('change', loadMarks);
});

/* === CARREGAR MARCAS === */
async function loadMarks() {
  const marcasList = document.getElementById('marcas-list');
  if (!marcasList) return;
  
  const filterProva = document.getElementById('filterProva')?.value || '';
  const filterTipo = document.getElementById('filterTipo')?.value || '';
  
  marcasList.innerHTML = '<p class="muted">Carregando marcas...</p>';
  
  try {
    let url = `${API_BASE_URL}/marks/me`;
    const params = new URLSearchParams();
    
    if (filterProva) params.append('evento', filterProva);
    if (filterTipo) params.append('tipo', filterTipo);
    
    if (params.toString()) url += '?' + params.toString();
    
    const response = await fetch(url, {
      headers: getHeaders()
    });
    
    if (response.ok) {
      const marks = await response.json();
      displayMarks(marks);
    } else if (response.status === 401) {
      logoutNow();
    } else {
      marcasList.innerHTML = '<p class="muted">Erro ao carregar marcas</p>';
    }
  } catch (error) {
    console.error('Erro ao carregar marcas:', error);
    marcasList.innerHTML = '<p class="muted">Erro de conexão. Tente novamente.</p>';
  }
}

/* === EXIBIR MARCAS === */
function displayMarks(marks) {
  const marcasList = document.getElementById('marcas-list');
  if (!marcasList) return;
  
  if (marks.length === 0) {
    marcasList.innerHTML = '<p class="muted">Nenhuma marca registrada ainda.</p>';
    return;
  }
  
  marcasList.innerHTML = marks.map(mark => {
    const isInvalidWind = mark.vento > 2.0;
    const windClass = isInvalidWind ? 'wind-invalid' : 'wind-valid';
    const windLabel = isInvalidWind ? '⚠️ Vento irregular' : '✓ Vento válido';
    
    return `
      <div class="mark-card ${isInvalidWind ? 'invalid-wind' : ''}">
        <div class="mark-date">${formatDate(mark.data)}</div>
        <h4>${mark.evento}</h4>
        <div class="mark-result">${mark.resultado}s</div>
        <p><strong>Local:</strong> ${mark.local}</p>
        <p><strong>Vento:</strong> ${mark.vento > 0 ? '+' : ''}${mark.vento} m/s 
          <span class="wind-badge ${windClass}">${windLabel}</span>
        </p>
        <p><strong>Tipo:</strong> ${mark.tipo === 'competicao' ? 'Competição' : 'Teste'}</p>
        ${mark.observacoes ? `<p><strong>Obs:</strong> ${mark.observacoes}</p>` : ''}
        <div style="display: flex; gap: 8px; margin-top: 10px;">
          <button onclick="editMark('${mark.id}')" class="btn btn-primary" style="font-size: 13px; padding: 6px 10px;">Editar</button>
          <button onclick="deleteMark('${mark.id}')" class="delete-btn">Excluir</button>
        </div>
      </div>
    `;
  }).join('');
}

/* === FORMATAR DATA === */
function formatDate(dateStr) {
  const date = new Date(dateStr + 'T00:00:00');
  return date.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric' });
}

/* === SETUP DO FORMULÁRIO === */
function setupForm() {
  const form = document.getElementById('marca-form');
  if (!form) return;
  
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const markId = document.getElementById('markId').value;
    const prova = document.getElementById('prova').value;
    const marca = parseFloat(document.getElementById('marca').value);
    const vento = parseFloat(document.getElementById('vento').value);
    const data = document.getElementById('data').value;
    const local = document.getElementById('local').value;
    const tipo = document.getElementById('tipo').value;
    
    if (!prova || !marca || !vento || !data || !local || !tipo) {
      showFeedback('Preencha todos os campos', 'error');
      return;
    }
    
    const markData = {
      evento: prova,
      resultado: marca,
      vento: vento,
      data: data,
      local: local,
      tipo: tipo,
      observacoes: null
    };
    
    try {
      let response;
      if (markId) {
        response = await fetch(`${API_BASE_URL}/marks/${markId}`, {
          method: 'PUT',
          headers: getHeaders(),
          body: JSON.stringify(markData)
        });
      } else {
        response = await fetch(`${API_BASE_URL}/marks/`, {
          method: 'POST',
          headers: getHeaders(),
          body: JSON.stringify(markData)
        });
      }
      
      if (response.ok) {
        showFeedback(markId ? 'Marca atualizada com sucesso!' : 'Marca adicionada com sucesso!', 'success');
        resetForm();
        loadMarks();
      } else if (response.status === 401) {
        logoutNow();
      } else {
        const error = await response.json();
        showFeedback(error.detail || 'Erro ao salvar marca', 'error');
      }
    } catch (error) {
      console.error('Erro:', error);
      showFeedback('Erro ao conectar com o servidor', 'error');
    }
  });
}

/* === EDITAR MARCA === */
async function editMark(markId) {
  try {
    const response = await fetch(`${API_BASE_URL}/marks/${markId}`, {
      headers: getHeaders()
    });
    
    if (response.ok) {
      const mark = await response.json();
      
      document.getElementById('markId').value = mark.id;
      document.getElementById('prova').value = mark.evento;
      document.getElementById('marca').value = mark.resultado;
      document.getElementById('vento').value = mark.vento;
      document.getElementById('data').value = mark.data;
      document.getElementById('local').value = mark.local;
      document.getElementById('tipo').value = mark.tipo;
      
      document.getElementById('submitBtn').textContent = 'Atualizar Marca';
      document.getElementById('cancelBtn').style.display = 'inline-block';
      
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  } catch (error) {
    console.error('Erro ao carregar marca:', error);
    showFeedback('Erro ao carregar marca', 'error');
  }
}

/* === DELETAR MARCA === */
async function deleteMark(markId) {
  if (!confirm('Tem certeza que deseja excluir esta marca?')) return;
  
  try {
    const response = await fetch(`${API_BASE_URL}/marks/${markId}`, {
      method: 'DELETE',
      headers: getHeaders()
    });
    
    if (response.ok || response.status === 204) {
      showFeedback('Marca excluída com sucesso!', 'success');
      loadMarks();
    } else {
      showFeedback('Erro ao excluir marca', 'error');
    }
  } catch (error) {
    console.error('Erro:', error);
    showFeedback('Erro ao conectar com o servidor', 'error');
  }
}

/* === RESETAR FORMULÁRIO === */
function resetForm() {
  const form = document.getElementById('marca-form');
  if (form) form.reset();
  
  document.getElementById('markId').value = '';
  document.getElementById('submitBtn').textContent = 'Adicionar Marca';
  document.getElementById('cancelBtn').style.display = 'none';
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

console.log('[Marcas] Módulo carregado');