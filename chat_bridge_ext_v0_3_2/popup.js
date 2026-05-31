// ============================================================
// ChatFÁCIL / Chat Bridge v0.3.2 — popup.js
// P0: filtro ChatGPT no dropdown
// P1: [Colar | Enviar | Auto] grupo verde
// P2: [Trazer | Enviar | Auto] grupo azul
// P3: padrão recentCount = 1
// P4: atalhos de teclado sob cada botão (click-to-capture, auto-save, persist)
// P5: botão "Manter no topo" (visual + aviso se não suportado)
// P6: preserva print, itens capturados, janela fixa
// ============================================================

const $ = (id) => document.getElementById(id);

// ─── REFS ───────────────────────────────────────────────────
const sourceStatusEl       = $('sourceStatus');
const selectedDestStatusEl = $('selectedDestStatus');
const connectedDestListEl  = $('connectedDestList');
const availableTabsListEl  = $('availableTabsList');
const addDestDropdownEl    = $('addDestDropdown');
const recentCountEl        = $('recentCount');
const captureAllToggle     = $('captureAllToggle');
const itemsEl              = $('items');
const statusMessageEl      = $('statusMessage');
const roleIndicatorsEl     = $('roleIndicators');

// ─── ESTADO ─────────────────────────────────────────────────
let state = {
  sourceTabId:    null,
  sourceTitle:    '',
  connectedDests: [],
  selectedDestId: null,
  availableTabs:  [],
  captureAll:     false,
  recentCount:    1,        // P3: padrão = 1
  items:          [],
  globalState:    'IDLE',
  alwaysOnTop:    false,    // P5
  shortcuts:      {},       // P4: { actionId: keyCombo }
};

// ─── HELPERS ────────────────────────────────────────────────
function showStatus(msg) {
  if (statusMessageEl) statusMessageEl.textContent = msg || '';
}

function isChatGptUrl(url = '') {
  // P0: somente ChatGPT
  return /^https:\/\/(chatgpt\.com|chat\.openai\.com)(\/|$)/.test(url || '');
}

function short(text, max = 80) {
  const s = String(text || '').replace(/\s+/g, ' ').trim();
  return s.length > max ? s.slice(0, max - 1) + '…' : s;
}

function safeCount(value) {
  const parsed = Number.parseInt(value, 10);
  if (!Number.isFinite(parsed)) return 1;
  return Math.min(999, Math.max(1, parsed));
}

function escapeHtml(str) {
  return String(str || '').replace(/[&<>"']/g, ch =>
    ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' }[ch])
  );
}

function sendRuntime(message) {
  return new Promise(resolve => {
    chrome.runtime.sendMessage(message, res => {
      resolve(res || { ok: false, error: chrome.runtime.lastError?.message || 'Sem resposta.' });
    });
  });
}

async function sendToTab(tabId, message) {
  try {
    return await chrome.tabs.sendMessage(tabId, message);
  } catch (err) {
    try {
      await chrome.scripting.executeScript({ target: { tabId }, files: ['content.js'] });
      return await chrome.tabs.sendMessage(tabId, message);
    } catch (err2) {
      return { ok: false, error: err2.message || err.message || String(err2) };
    }
  }
}

// ─── STORAGE: DESTINOS ──────────────────────────────────────
async function loadConnectedDests() {
  const { connectedDestIds = [] } = await chrome.storage.local.get({ connectedDestIds: [] });
  const valid = [];
  for (const tabId of connectedDestIds) {
    try {
      const tab = await chrome.tabs.get(tabId);
      valid.push({ tabId: tab.id, title: tab.title || tab.url || `Aba ${tab.id}`, url: tab.url || '' });
    } catch (_) { /* aba fechada */ }
  }
  return valid;
}

async function saveConnectedDests(dests) {
  await chrome.storage.local.set({ connectedDestIds: dests.map(d => d.tabId) });
}

async function loadSelectedDestId() {
  const { selectedDestId = null } = await chrome.storage.local.get({ selectedDestId: null });
  return selectedDestId;
}

async function saveSelectedDestId(id) {
  await chrome.storage.local.set({ selectedDestId: id });
}

// ─── STORAGE: ATALHOS ───────────────────────────────────────
async function loadShortcuts() {
  const { shortcuts = {} } = await chrome.storage.local.get({ shortcuts: {} });
  return shortcuts;
}

async function saveShortcuts(sc) {
  await chrome.storage.local.set({ shortcuts: sc });
}

// ─── CARREGAR ESTADO INICIAL ────────────────────────────────
async function loadState() {
  const [activeTab] = await chrome.tabs.query({ active: true, currentWindow: true });
  state.sourceTabId = activeTab?.id || null;
  state.sourceTitle = activeTab?.title || activeTab?.url || 'Aba atual';

  state.connectedDests = await loadConnectedDests();

  const savedSel = await loadSelectedDestId();
  const isValid  = savedSel &&
    state.connectedDests.some(d => d.tabId === savedSel) &&
    savedSel !== state.sourceTabId;
  state.selectedDestId = isValid ? savedSel : null;
  if (!isValid) await saveSelectedDestId(null);

  state.availableTabs = await chrome.tabs.query({});

  const stored = await chrome.storage.local.get({ recentCount: 1, captureAll: false, items: [], alwaysOnTop: false });
  state.recentCount  = safeCount(stored.recentCount);
  state.captureAll   = Boolean(stored.captureAll);
  state.items        = stored.items || [];
  state.alwaysOnTop  = Boolean(stored.alwaysOnTop);

  const { globalState = 'IDLE' } = await chrome.storage.local.get({ globalState: 'IDLE' });
  state.globalState = globalState;

  state.shortcuts = await loadShortcuts();

  renderAll();
}

// ─── RENDERIZAÇÃO ───────────────────────────────────────────
function renderAll() {
  renderGlobalState();
  renderSourceStatus();
  renderConnectedDests();
  renderCaptureControls();
  renderItems(state.items);
  renderRoleIndicators();
  renderAlwaysOnTopBtn();
  renderShortcutInputs();
}

function renderGlobalState() {
  const led = $('popup-led');
  const txt = $('popup-state-text');
  if (!led || !txt) return;
  const labels = {
    IDLE: 'Livre', COPIADO_PARA_CODEX: 'Copiado p/ Codex',
    AGUARDANDO_COLAGEM_MANUAL: 'Aguardando Colagem',
    AGUARDANDO_RESPOSTA_CODEX: 'Executando no Codex',
    RESPOSTA_CODEX_COLADA: 'Resposta do Codex Colada',
    ENVIADO_PARA_CODEX: 'Enviado p/ Codex Aba',
    ENVIADO_PARA_ANTIGRAVITY: 'Enviado p/ Antigravity',
    EXECUTANDO: 'Executando na Aba', RESPOSTA_CAPTURADA: 'Resposta Capturada',
    AGUARDANDO_AUDITORIA_CHATGPT: 'Auditoria no ChatGPT',
    AUDITADO: 'Auditado / Livre', BLOQUEADO: 'Bloqueado', ERRO: 'Erro na Fila',
  };
  led.className = `led-dot ${state.globalState}`;
  txt.textContent = labels[state.globalState] || state.globalState;
}

function renderSourceStatus() {
  if (sourceStatusEl)
    sourceStatusEl.textContent = `🟢 Fonte: ${short(state.sourceTitle || 'Aba atual', 40)}`;

  const dest = state.connectedDests.find(d => d.tabId === state.selectedDestId);
  if (selectedDestStatusEl) {
    selectedDestStatusEl.textContent = dest
      ? `🎯 Destino: ${short(dest.title, 36)}`
      : '🎯 Destino: nenhum selecionado';
  }
}

function renderConnectedDests() {
  if (!connectedDestListEl) return;
  connectedDestListEl.innerHTML = '';

  if (!state.connectedDests.length) {
    connectedDestListEl.innerHTML = '<div class="empty">Nenhum destino. Clique em "+ Adicionar".</div>';
    return;
  }

  for (const dest of state.connectedDests) {
    const isSelected = dest.tabId === state.selectedDestId;
    const isSource   = dest.tabId === state.sourceTabId;

    const row = document.createElement('div');
    row.className = 'dest-row' +
      (isSelected ? ' selected' : '') +
      (isSource   ? ' unavailable' : '');
    row.dataset.tabId = dest.tabId;
    row.title = isSource
      ? 'Aba ativa (fonte atual — não pode ser destino)'
      : 'Clique para selecionar como destino';

    const led = document.createElement('span');
    led.className = 'led-dot ' + (isSource ? 'yellow' : 'green');

    const info = document.createElement('div');
    info.className = 'dest-info';
    info.innerHTML = `<span class="dest-title">${escapeHtml(short(dest.title, 26))}</span>`
      + `<span class="dest-url">${escapeHtml(short(dest.url, 34))}</span>`;

    const badge = document.createElement('span');
    if (isSource) {
      badge.style.cssText = 'font-size:9px; color:#fbbf24; white-space:nowrap;';
      badge.textContent = '(fonte)';
    }

    row.appendChild(led);
    row.appendChild(info);
    row.appendChild(badge);

    if (!isSource) {
      row.addEventListener('click', () => selectDest(dest.tabId));
    }

    connectedDestListEl.appendChild(row);
  }
}

function selectDest(tabId) {
  if (tabId === state.sourceTabId) {
    showStatus('⚠️ Esta aba é a fonte — escolha um destino diferente.');
    return;
  }
  state.selectedDestId = tabId;
  saveSelectedDestId(tabId);
  renderSourceStatus();
  renderConnectedDests();
}

function renderCaptureControls() {
  if (recentCountEl) {
    recentCountEl.value    = String(state.recentCount);
    recentCountEl.disabled = state.captureAll;
  }
  if (captureAllToggle) {
    captureAllToggle.classList.toggle('active', state.captureAll);
    captureAllToggle.setAttribute('aria-pressed', String(state.captureAll));
    captureAllToggle.textContent = state.captureAll ? 'Todas: on' : 'Todas';
  }
}

function renderItems(items) {
  if (!itemsEl) return;
  itemsEl.innerHTML = '';
  if (!items.length) {
    itemsEl.innerHTML = '<div class="empty">Nenhum item capturado ainda.</div>';
    return;
  }
  for (const item of items.slice().reverse()) {
    const card = document.createElement('div');
    card.className = 'item';

    const head = document.createElement('div');
    head.className = 'item-head';
    head.innerHTML = `<span>${item.type === 'image' ? 'Print' : 'Texto'}</span>`
      + `<span>${new Date(item.createdAt).toLocaleTimeString('pt-BR')}</span>`;
    card.appendChild(head);

    const preview = document.createElement('div');
    preview.className = 'preview';
    if (item.type === 'image') {
      const img = document.createElement('img');
      img.src = item.dataUrl;
      preview.appendChild(img);
    } else {
      preview.textContent = short(item.text, 240);
    }
    card.appendChild(preview);

    const acts = document.createElement('div');
    acts.className = 'actions';
    const btn = document.createElement('button');
    btn.textContent = 'Colar no destino';
    btn.addEventListener('click', () => sendItem(item));
    acts.appendChild(btn);
    card.appendChild(acts);

    itemsEl.appendChild(card);
  }
}

function renderRoleIndicators() {
  if (!roleIndicatorsEl) return;
  roleIndicatorsEl.innerHTML = '';
  const list = [
    ['F = Fonte automática', 'fonte',    'Aba ativa no momento'],
    ['D = Destino Web',      'dest-web', 'Aba ChatGPT conectada'],
    ['C = Codex Assistido',  'codex',    'Codex Desktop — clipboard'],
    ['A = Antigravity',      'antigrav', 'Antigravity Desktop — clipboard'],
  ];
  for (const [label, cls, title] of list) {
    const el = document.createElement('span');
    el.className = `role-indicator ${cls}`;
    el.title = title;
    el.textContent = label;
    roleIndicatorsEl.appendChild(el);
  }
}

// ─── P5: MANTER NO TOPO ─────────────────────────────────────
function renderAlwaysOnTopBtn() {
  const btn = $('btn-always-top');
  if (!btn) return;
  if (state.alwaysOnTop) {
    btn.textContent = '📌 Topo: on';
    btn.classList.add('active');
    btn.title = 'Clique para desativar';
  } else {
    btn.textContent = '📌 Topo';
    btn.classList.remove('active');
    btn.title = 'Manter janela sempre no topo';
  }
}

async function toggleAlwaysOnTop() {
  // chrome.windows.update com alwaysOnTop só funciona em janelas "normal" criadas pela extensão.
  // O popup padrão NÃO suporta alwaysOnTop. Para a janela criada pelo botão Fixar, sim.
  const urlParams = new URLSearchParams(window.location.search);
  const isWindowMode = urlParams.get('mode') === 'window';

  if (!isWindowMode) {
    showStatus(
      '⚠️ "Manter no topo" só funciona na janela fixada (clique em ⧉ Fixar primeiro).\n' +
      'Alternativas externas: PowerToys "Always on Top" ou app auxiliar com Native Messaging.'
    );
    return;
  }

  // Tentar via chrome.windows.update
  const windowId = await new Promise(resolve => chrome.windows.getCurrent(w => resolve(w?.id)));
  if (!windowId) {
    showStatus('❌ Não foi possível identificar a janela atual.');
    return;
  }

  state.alwaysOnTop = !state.alwaysOnTop;
  await chrome.storage.local.set({ alwaysOnTop: state.alwaysOnTop });

  try {
    // A API alwaysOnTop existe mas é limitada — funciona apenas em janelas normais
    await new Promise((resolve, reject) =>
      chrome.windows.update(windowId, { alwaysOnTop: state.alwaysOnTop }, (w) => {
        if (chrome.runtime.lastError) reject(chrome.runtime.lastError);
        else resolve(w);
      })
    );
    showStatus(state.alwaysOnTop ? '📌 Janela fixada no topo.' : '📍 Janela destravada do topo.');
  } catch (err) {
    // Fallback: aviso detalhado
    const msg = state.alwaysOnTop
      ? '⚠️ Topo ativado visualmente, mas requer PowerToys / Native Messaging para garantir o always-on-top real.'
      : '📍 Topo desativado.';
    showStatus(msg);
  }

  renderAlwaysOnTopBtn();
}

// ─── P4: ATALHOS DE TECLADO ─────────────────────────────────
// Mapeamento: id do botão → função a executar
const SHORTCUT_ACTIONS = {
  'pasteToDestBtn':         () => pasteToDest(),
  'submitDestination':      () => submitDestination(),
  'autoSendBtn':            () => autoSend(),
  'pullDestinationResponse':() => pullDestinationResponse(),
  'submitSourceBtn':        () => submitSource(),
  'autoReturnBtn':          () => autoReturn(),
};

// Converte evento de teclado em string de combo (ex: "Ctrl+Alt+C", "Alt+Enter")
function comboFromEvent(e) {
  const parts = [];
  if (e.ctrlKey)  parts.push('Ctrl');
  if (e.altKey)   parts.push('Alt');
  if (e.shiftKey) parts.push('Shift');
  const key = e.key === ' ' ? 'Space' : e.key;
  if (!['Control','Alt','Shift','Meta'].includes(key)) parts.push(key);
  return parts.join('+');
}

function renderShortcutInputs() {
  document.querySelectorAll('.sc-input').forEach(input => {
    const action = input.dataset.action;
    input.value = state.shortcuts[action] || '';
  });
}

function initShortcutInputs() {
  let captureTarget = null;  // input que está capturando tecla

  document.querySelectorAll('.sc-input').forEach(input => {
    const action = input.dataset.action;

    // Clique na caixinha = entrar em modo captura
    input.addEventListener('click', () => {
      if (captureTarget && captureTarget !== input) {
        captureTarget.classList.remove('capturing');
        captureTarget.placeholder = 'atalho';
      }
      captureTarget = input;
      input.classList.add('capturing');
      input.placeholder = '▶ tecle...';
      input.focus();
    });

    // Blur = sai do modo captura sem gravar
    input.addEventListener('blur', () => {
      if (captureTarget === input) {
        captureTarget = null;
        input.classList.remove('capturing');
        input.placeholder = 'atalho';
      }
    });
  });

  // Captura global de teclado quando algum input está em modo captura
  document.addEventListener('keydown', async (e) => {
    if (!captureTarget) return;

    // Esc = cancela captura
    if (e.key === 'Escape') {
      captureTarget.blur();
      return;
    }

    // Teclas solitárias de controle não gravam
    if (['Control','Alt','Shift','Meta'].includes(e.key)) return;

    e.preventDefault();
    e.stopPropagation();

    const combo  = comboFromEvent(e);
    const action = captureTarget.dataset.action;

    // Verificar colisão com outro atalho
    const collision = Object.entries(state.shortcuts)
      .find(([k, v]) => v === combo && k !== action);
    if (collision) {
      showStatus(`⚠️ Atalho "${combo}" já está em uso por outro botão.`);
      captureTarget.blur();
      return;
    }

    state.shortcuts[action] = combo;
    await saveShortcuts(state.shortcuts);
    captureTarget.value = combo;
    captureTarget.blur();
    showStatus(`✅ Atalho "${combo}" salvo para o botão.`);
  });

  // Execução de atalhos globais (quando nenhum input está capturando)
  document.addEventListener('keydown', (e) => {
    if (captureTarget) return;  // não executar durante captura
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

    const combo = comboFromEvent(e);
    if (!combo) return;

    for (const [action, fn] of Object.entries(SHORTCUT_ACTIONS)) {
      if (state.shortcuts[action] === combo) {
        e.preventDefault();
        fn();
        return;
      }
    }
  });
}

// ─── P0: DROPDOWN — APENAS CHATGPT ──────────────────────────
async function openAddDestDropdown() {
  state.availableTabs = await chrome.tabs.query({});
  renderAvailableTabs();
  if (addDestDropdownEl) addDestDropdownEl.style.display = 'block';
}

function closeAddDestDropdown() {
  if (addDestDropdownEl) addDestDropdownEl.style.display = 'none';
}

function renderAvailableTabs() {
  if (!availableTabsListEl) return;
  availableTabsListEl.innerHTML = '';

  // P0: filtrar apenas abas ChatGPT
  const chatGptTabs = state.availableTabs.filter(t => t.id && isChatGptUrl(t.url || ''));

  if (!chatGptTabs.length) {
    availableTabsListEl.innerHTML =
      '<div class="empty" style="font-size:10px;">Nenhuma aba ChatGPT aberta.<br>Abra chatgpt.com e recarregue.</div>';
    return;
  }

  for (const tab of chatGptTabs) {
    const isSource  = tab.id === state.sourceTabId;
    const isAlready = state.connectedDests.some(d => d.tabId === tab.id);

    const row = document.createElement('div');
    row.className = 'avail-tab-row' +
      (isSource  ? ' is-source'   : '') +
      (isAlready ? ' already-added' : '');

    const title = document.createElement('span');
    title.className = 'avail-tab-title';
    title.title     = tab.url || '';
    title.textContent = short(tab.title || tab.url || `Aba ${tab.id}`, 30);
    row.appendChild(title);

    const badge = document.createElement('span');
    badge.className = 'avail-tab-badge';
    if (isSource) {
      badge.classList.add('badge-source');
      badge.textContent = 'Fonte';
    } else if (isAlready) {
      badge.classList.add('badge-added');
      badge.textContent = 'Adicionado';
    } else {
      badge.style.cssText = 'background:#1e3a5f; color:#7dd3fc; cursor:pointer;';
      badge.textContent = '+ Adicionar';
    }
    row.appendChild(badge);

    if (!isSource && !isAlready) {
      row.addEventListener('click', () => addDestination(tab));
    }

    availableTabsListEl.appendChild(row);
  }
}

function addDestination(tab) {
  if (tab.id === state.sourceTabId) {
    showStatus('⚠️ A aba ativa é a fonte — não pode ser destino.');
    return;
  }
  if (state.connectedDests.some(d => d.tabId === tab.id)) {
    showStatus('Essa aba já está na lista.');
    return;
  }
  state.connectedDests.push({ tabId: tab.id, title: tab.title || tab.url || `Aba ${tab.id}`, url: tab.url || '' });
  saveConnectedDests(state.connectedDests);
  if (!state.selectedDestId) {
    state.selectedDestId = tab.id;
    saveSelectedDestId(tab.id);
  }
  showStatus(`✅ Destino adicionado: ${short(tab.title || tab.url, 38)}`);
  closeAddDestDropdown();
  renderSourceStatus();
  renderConnectedDests();
}

function removeSelectedDest() {
  if (!state.selectedDestId) { showStatus('Nenhum destino selecionado para remover.'); return; }
  const dest = state.connectedDests.find(d => d.tabId === state.selectedDestId);
  if (!dest) { showStatus('Destino não encontrado.'); return; }
  state.connectedDests  = state.connectedDests.filter(d => d.tabId !== state.selectedDestId);
  state.selectedDestId  = state.connectedDests[0]?.tabId || null;
  saveConnectedDests(state.connectedDests);
  saveSelectedDestId(state.selectedDestId);
  showStatus('🗑️ Destino removido da lista (a aba não foi fechada).');
  renderSourceStatus();
  renderConnectedDests();
}

// ─── VALIDAÇÃO ──────────────────────────────────────────────
function validateSendTarget() {
  if (!state.selectedDestId) {
    showStatus('⚠️ Nenhum destino selecionado. Clique em "+ Adicionar" e selecione um destino.');
    return null;
  }
  if (state.selectedDestId === state.sourceTabId) {
    showStatus('🚫 Bloqueado: origem e destino são a mesma aba.');
    return null;
  }
  return state.selectedDestId;
}

async function getSourceTabId() {
  const [activeTab] = await chrome.tabs.query({ active: true, currentWindow: true });
  state.sourceTabId = activeTab?.id || state.sourceTabId;
  state.sourceTitle = activeTab?.title || state.sourceTitle;
  return state.sourceTabId;
}

// ─── P1: COLAR NO DESTINO (sem enviar) ──────────────────────
async function pasteToDest() {
  const sourceId = await getSourceTabId();
  const destId   = validateSendTarget();
  if (!destId) return;

  const count = safeCount(recentCountEl?.value || state.recentCount);
  const all   = Boolean(state.captureAll);

  showStatus('Capturando mensagens da fonte…');
  const captureRes = await sendToTab(sourceId, {
    type: 'CAPTURE_RECENT_MESSAGES', count, all,
    format: 'markdown', captureMode: 'messages', order: 'recent-first',
  });

  if (!captureRes?.ok || !captureRes.text) {
    showStatus(captureRes?.error || '❌ Nenhuma mensagem encontrada na aba fonte.');
    return;
  }

  await addItem({ type: 'text', text: captureRes.text, sourceTitle: captureRes.title, sourceUrl: captureRes.url });

  showStatus('Colando no destino (sem enviar)…');
  const pasteRes = await sendToTab(destId, { type: 'INSERT_TEXT', text: captureRes.text });

  showStatus(pasteRes?.ok
    ? `✅ Colado no destino. Revise e clique "Enviar" quando quiser disparar.`
    : `❌ Falha ao colar: ${pasteRes?.error || 'Destino não alcançável.'}`);
}

// ─── P1: ENVIAR (conteúdo já no campo do destino) ───────────
async function submitDestination() {
  const destId = validateSendTarget();
  if (!destId) return;
  showStatus('Acionando envio no destino…');
  const res = await sendRuntime({ type: 'BG_SUBMIT_COMPOSER', tabId: destId });
  showStatus(res?.ok
    ? '🚀 Envio acionado no destino.'
    : `❌ Falha: ${res?.error || 'Botão de envio não encontrado no destino.'}`);
}

// ─── P1: AUTO (colar + enviar no destino) ───────────────────
async function autoSend() {
  const sourceId = await getSourceTabId();
  const destId   = validateSendTarget();
  if (!destId) return;

  const count = safeCount(recentCountEl?.value || state.recentCount);
  const all   = Boolean(state.captureAll);

  showStatus('Auto: capturando da fonte…');
  const captureRes = await sendToTab(sourceId, {
    type: 'CAPTURE_RECENT_MESSAGES', count, all,
    format: 'markdown', captureMode: 'messages', order: 'recent-first',
  });

  if (!captureRes?.ok || !captureRes.text) {
    showStatus(captureRes?.error || '❌ Nenhuma mensagem para capturar.');
    return;
  }

  await addItem({ type: 'text', text: captureRes.text, sourceTitle: captureRes.title, sourceUrl: captureRes.url });

  showStatus('Auto: colando no destino…');
  const pasteRes = await sendToTab(destId, { type: 'INSERT_TEXT', text: captureRes.text });
  if (!pasteRes?.ok) {
    showStatus(`❌ Falha ao colar: ${pasteRes?.error || ''}`);
    return;
  }

  // Pequena pausa para o DOM do destino reagir
  await new Promise(r => setTimeout(r, 400));

  showStatus('Auto: enviando no destino…');
  const sendRes = await sendRuntime({ type: 'BG_SUBMIT_COMPOSER', tabId: destId });
  showStatus(sendRes?.ok
    ? '⚡ Auto concluído: capturado, colado e enviado para o destino.'
    : `⚠️ Colado, mas falha ao enviar: ${sendRes?.error || ''}`);
}

// ─── P2: TRAZER RESPOSTA DO DESTINO ─────────────────────────
async function pullDestinationResponse() {
  const sourceId = await getSourceTabId();
  const destId   = validateSendTarget();
  if (!destId) return;

  showStatus('Buscando resposta no destino…');
  const count = safeCount(recentCountEl?.value || state.recentCount);
  const res = await sendToTab(destId, {
    type: 'CAPTURE_RECENT_MESSAGES', count,
    all: false, format: 'plain', captureMode: 'assistant', order: 'recent-first',
  });

  if (!res?.ok || !res.text) {
    showStatus('Nenhuma resposta disponível no destino.');
    return;
  }

  showStatus('Colando resposta na aba ativa…');
  const insertRes = await sendToTab(sourceId, { type: 'INSERT_TEXT', text: res.text });
  showStatus(insertRes?.ok
    ? '📥 Resposta trazida do destino e colada aqui. Revise antes de enviar.'
    : `❌ Não foi possível colar na fonte: ${insertRes?.error || ''}`);
}

// ─── P2: ENVIAR NA FONTE (conteúdo já colado) ───────────────
async function submitSource() {
  const sourceId = await getSourceTabId();
  showStatus('Acionando envio na aba ativa (fonte)…');
  const res = await sendRuntime({ type: 'BG_SUBMIT_COMPOSER', tabId: sourceId });
  showStatus(res?.ok
    ? '🚀 Envio acionado na aba fonte.'
    : `❌ Falha: ${res?.error || 'Botão de envio não encontrado na fonte.'}`);
}

// ─── P2: AUTO RETURN (trazer + colar + enviar na fonte) ─────
async function autoReturn() {
  const sourceId = await getSourceTabId();
  const destId   = validateSendTarget();
  if (!destId) return;

  showStatus('Auto Retorno: buscando resposta no destino…');
  const count = safeCount(recentCountEl?.value || state.recentCount);
  const res = await sendToTab(destId, {
    type: 'CAPTURE_RECENT_MESSAGES', count,
    all: false, format: 'plain', captureMode: 'assistant', order: 'recent-first',
  });

  if (!res?.ok || !res.text) {
    showStatus('Nenhuma resposta no destino para trazer.');
    return;
  }

  showStatus('Auto Retorno: colando na fonte…');
  const pasteRes = await sendToTab(sourceId, { type: 'INSERT_TEXT', text: res.text });
  if (!pasteRes?.ok) {
    showStatus(`❌ Falha ao colar na fonte: ${pasteRes?.error || ''}`);
    return;
  }

  await new Promise(r => setTimeout(r, 400));

  showStatus('Auto Retorno: enviando na fonte…');
  const sendRes = await sendRuntime({ type: 'BG_SUBMIT_COMPOSER', tabId: sourceId });
  showStatus(sendRes?.ok
    ? '⚡ Auto Retorno concluído: resposta trazida, colada e enviada na fonte.'
    : `⚠️ Resposta colada, mas falha ao enviar na fonte: ${sendRes?.error || ''}`);
}

// ─── PRINT + ITENS ──────────────────────────────────────────
async function capturePrintAndSend() {
  const [activeTab] = await chrome.tabs.query({ active: true, currentWindow: true });
  state.sourceTabId = activeTab?.id || state.sourceTabId;

  const destId = validateSendTarget();
  if (!destId) return;

  if (!activeTab?.windowId) { showStatus('Não foi possível capturar o print.'); return; }

  const dataUrl = await chrome.tabs.captureVisibleTab(activeTab.windowId, { format: 'png' });
  const name    = `chat-bridge-print-${Date.now()}.png`;
  const item    = { type: 'image', dataUrl, name, sourceTitle: activeTab.title || '', sourceUrl: activeTab.url || '' };
  await addItem(item);
  await sendItem(item);
}

async function addItem(item) {
  const { items = [] } = await chrome.storage.local.get({ items: [] });
  const next = [...items, { ...item, id: crypto.randomUUID(), createdAt: Date.now() }].slice(-20);
  await chrome.storage.local.set({ items: next });
  state.items = next;
  renderItems(next);
}

async function copyImageToClipboard(dataUrl) {
  const blob = await (await fetch(dataUrl)).blob();
  if (!navigator.clipboard || !window.ClipboardItem) throw new Error('Clipboard de imagem não disponível.');
  await navigator.clipboard.write([new ClipboardItem({ [blob.type]: blob })]);
}

async function sendItem(item) {
  const destId = validateSendTarget();
  if (!destId) return;

  if (item.type === 'text') {
    const res = await sendToTab(destId, { type: 'INSERT_TEXT', text: item.text || '' });
    showStatus(res?.ok
      ? '✅ Texto colado no destino.'
      : `❌ Falha: ${res?.error || ''}`);
    return res;
  }

  if (item.type === 'image') {
    const attached = await sendRuntime({ type: 'BG_ATTACH_IMAGE_TO_TAB', tabId: destId, dataUrl: item.dataUrl, name: item.name || `print-${Date.now()}.png` });
    if (attached?.ok) { showStatus('✅ Print anexado no destino.'); return { ok: true }; }
    try {
      await copyImageToClipboard(item.dataUrl);
      await sendRuntime({ type: 'BG_FOCUS_COMPOSER', tabId: destId });
      showStatus('Print copiado — pressione Ctrl+V no destino se não aparecer.');
    } catch {
      showStatus('❌ Não foi possível enviar o print.');
    }
    return { ok: false };
  }
}

// ─── MODO ASSISTIDO ──────────────────────────────────────────
async function copyForAssisted(target) {
  const [activeTab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const tabId = activeTab?.id;
  if (!tabId) { showStatus('Aba fonte não identificada.'); return; }

  const count = safeCount(recentCountEl?.value || state.recentCount);
  const res = await sendToTab(tabId, {
    type: 'CAPTURE_RECENT_MESSAGES', count, all: Boolean(state.captureAll),
    format: 'markdown', captureMode: 'messages', order: 'recent-first',
  });

  const text = res?.text || '';
  if (!text) { showStatus('Nenhum texto encontrado para copiar.'); return; }

  try {
    await navigator.clipboard.writeText(text);
    showStatus(`✅ Copiado. Cole no ${target} (Ctrl+V) e execute.`);
  } catch {
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.style.cssText = 'position:fixed;left:-9999px;top:-9999px';
    document.body.appendChild(ta);
    ta.select();
    document.execCommand('copy');
    ta.remove();
    showStatus(`✅ Copiado (fallback). Cole no ${target}.`);
  }
}

async function pasteAssistedResponse(target) {
  const text = prompt(`Cole aqui a resposta do ${target}:`);
  if (!text?.trim()) { showStatus('Nenhuma resposta colada.'); return; }

  const [activeTab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const tabId = activeTab?.id;
  if (!tabId) { showStatus('Aba fonte não identificada.'); return; }

  const block = `---\n[Resposta de ${target}] ${new Date().toLocaleString('pt-BR')}\n\n${text.trim()}\n---`;
  const res = await sendToTab(tabId, { type: 'INSERT_TEXT', text: block });
  showStatus(res?.ok
    ? `✅ Resposta do ${target} colada para auditoria.`
    : `❌ Falha: ${res?.error || ''}`);
}

// ─── LISTENERS ──────────────────────────────────────────────
$('btnAddDest')?.addEventListener('click', openAddDestDropdown);
$('btnCloseDropdown')?.addEventListener('click', closeAddDestDropdown);
$('btnRemoveDest')?.addEventListener('click', removeSelectedDest);
$('refreshTabs')?.addEventListener('click', async () => { await loadState(); showStatus('Atualizado.'); });

recentCountEl?.addEventListener('input', async () => {
  const count = safeCount(recentCountEl.value);
  recentCountEl.value = String(count);
  state.recentCount = count;
  await chrome.storage.local.set({ recentCount: count });
});

captureAllToggle?.addEventListener('click', async () => {
  state.captureAll = !state.captureAll;
  await chrome.storage.local.set({ captureAll: state.captureAll });
  renderCaptureControls();
});

// Grupo verde — Para o Destino
$('pasteToDestBtn')?.addEventListener('click', pasteToDest);
$('submitDestination')?.addEventListener('click', submitDestination);
$('autoSendBtn')?.addEventListener('click', autoSend);

// Grupo azul — Trazer do Destino
$('pullDestinationResponse')?.addEventListener('click', pullDestinationResponse);
$('submitSourceBtn')?.addEventListener('click', submitSource);
$('autoReturnBtn')?.addEventListener('click', autoReturn);

// Print
$('capturePrintAndSend')?.addEventListener('click', capturePrintAndSend);

// Itens capturados
$('captureSelection')?.addEventListener('click', async () => {
  const [activeTab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (!activeTab?.id) { showStatus('Aba não identificada.'); return; }
  const res = await sendToTab(activeTab.id, { type: 'CAPTURE_TEXT' });
  if (!res?.ok || !res.text) { showStatus('Selecione um trecho primeiro.'); return; }
  await addItem({ type: 'text', text: res.text, sourceTitle: res.title, sourceUrl: res.url });
  showStatus('✅ Seleção capturada.');
});

$('sendSelection')?.addEventListener('click', async () => {
  const [activeTab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (!activeTab?.id) { showStatus('Aba não identificada.'); return; }
  const res = await sendToTab(activeTab.id, { type: 'CAPTURE_TEXT' });
  if (!res?.ok || !res.text) { showStatus('Selecione um trecho primeiro.'); return; }
  const item = { type: 'text', text: res.text, sourceTitle: res.title, sourceUrl: res.url };
  await addItem(item);
  await sendItem(item);
});

$('captureScreenshot')?.addEventListener('click', async () => {
  const [activeTab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (!activeTab?.id) { showStatus('Aba não identificada.'); return; }
  const dataUrl = await chrome.tabs.captureVisibleTab(activeTab.windowId, { format: 'png' });
  await addItem({ type: 'image', dataUrl, name: `print-${Date.now()}.png`, sourceTitle: activeTab.title || '', sourceUrl: activeTab.url || '' });
  showStatus('✅ Print capturado.');
});

$('sendLast')?.addEventListener('click', async () => {
  const { items = [] } = await chrome.storage.local.get({ items: [] });
  const last = items[items.length - 1];
  if (!last) { showStatus('Nenhum item capturado ainda.'); return; }
  await sendItem(last);
});

$('clearItems')?.addEventListener('click', async () => {
  if (confirm('Limpar todos os itens capturados?')) {
    await chrome.storage.local.set({ items: [] });
    state.items = [];
    renderItems([]);
    showStatus('✅ Itens limpos.');
  }
});

// Modo assistido
$('btnCopyForCodex')?.addEventListener('click', () => copyForAssisted('Codex Desktop'));
$('btnPasteCodexResponse')?.addEventListener('click', () => pasteAssistedResponse('Codex'));
$('btnCopyForAntigravity')?.addEventListener('click', () => copyForAssisted('Antigravity'));
$('btnPasteAntigravityResponse')?.addEventListener('click', () => pasteAssistedResponse('Antigravity'));

// P5: Manter no topo
$('btn-always-top')?.addEventListener('click', toggleAlwaysOnTop);

// ─── INIT ───────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', async () => {
  const urlParams    = new URLSearchParams(window.location.search);
  const isWindowMode = urlParams.get('mode') === 'window';
  if (isWindowMode) document.body.classList.add('window-mode');

  const fixBtn = $('btn-fix-window');
  if (fixBtn) {
    if (isWindowMode) {
      fixBtn.style.display = 'none';
    } else {
      fixBtn.addEventListener('click', () => {
        chrome.windows.create({ url: 'popup.html?mode=window', type: 'popup', width: 440, height: 700 });
        window.close();
      });
    }
  }

  await loadState();
  initShortcutInputs();

  // LEDs + estado global a cada 2 segundos
  setInterval(updateTabLeds, 2000);
});

// ─── ATUALIZAÇÃO PERIÓDICA ───────────────────────────────────
async function updateTabLeds() {
  const stillAlive = [];
  let changed = false;
  for (const dest of state.connectedDests) {
    try {
      const tab = await chrome.tabs.get(dest.tabId);
      stillAlive.push({ ...dest, title: tab.title || dest.title, url: tab.url || dest.url });
    } catch (_) {
      changed = true;
    }
  }
  if (changed) {
    state.connectedDests = stillAlive;
    if (!stillAlive.some(d => d.tabId === state.selectedDestId)) {
      state.selectedDestId = stillAlive[0]?.tabId || null;
      await saveSelectedDestId(state.selectedDestId);
    }
    saveConnectedDests(stillAlive);
    renderSourceStatus();
    renderConnectedDests();
  }

  const { globalState = 'IDLE' } = await chrome.storage.local.get({ globalState: 'IDLE' });
  if (globalState !== state.globalState) {
    state.globalState = globalState;
    renderGlobalState();
  }
}
