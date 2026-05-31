(function () {
  const EXT_MARK = '__CHAT_BRIDGE_CONTENT_V2_LOADED__';
  if (window[EXT_MARK]) return;
  window[EXT_MARK] = true;

  const STORAGE_KEY = 'chatBridgeV2Settings';
  const DEFAULTS = {
    recentCount: 3,
    captureMode: 'messages',
    format: 'markdown',
    order: 'recent-first',
    targetTabIds: [],
    autoOpenAfterSend: false
  };

  const state = {
    open: false,
    tabs: [],
    currentSettings: { ...DEFAULTS },
    sending: false
  };

  // Helper functions for scraping & DOM parsing
  function cleanText(text) {
    return String(text || '').replace(/\u00a0/g, ' ').replace(/[ \t]+\n/g, '\n').trim();
  }

  function safeTitle(text, max = 58) {
    const s = cleanText(text || 'Conversa sem título');
    return s.length > max ? s.slice(0, max - 1) + '…' : s;
  }

  function getPageTitle() {
    return document.title || location.href;
  }

  function getConversationKey() {
    const url = new URL(location.href);
    const parts = url.pathname.split('/').filter(Boolean);
    const cIndex = parts.findIndex(p => p === 'c' || p === 'chat');
    const id = cIndex >= 0 && parts[cIndex + 1] ? parts[cIndex + 1] : url.pathname;
    return `${url.hostname}:${id}`;
  }

  async function storageGet(defaults) {
    return await chrome.storage.local.get(defaults);
  }

  async function storageSet(values) {
    return await chrome.storage.local.set(values);
  }

  async function loadSettings() {
    const all = await storageGet({ [STORAGE_KEY]: {} });
    const key = getConversationKey();
    state.currentSettings = { ...DEFAULTS, ...(all[STORAGE_KEY][key] || {}) };
    return state.currentSettings;
  }

  async function saveSettings(patch) {
    const all = await storageGet({ [STORAGE_KEY]: {} });
    const key = getConversationKey();
    const next = { ...DEFAULTS, ...(all[STORAGE_KEY][key] || {}), ...patch };
    await storageSet({ [STORAGE_KEY]: { ...all[STORAGE_KEY], [key]: next } });
    state.currentSettings = next;
    return next;
  }

  function sendRuntime(message) {
    return new Promise(resolve => chrome.runtime.sendMessage(message, res => resolve(res || { ok: false, error: chrome.runtime.lastError?.message || 'Sem resposta.' })));
  }

  function getSelectedOrFocusedText() {
    const selection = cleanText(window.getSelection && window.getSelection().toString());
    if (selection) return selection;

    const active = document.activeElement;
    if (active && (active.tagName === 'TEXTAREA' || active.tagName === 'INPUT')) {
      const start = active.selectionStart || 0;
      const end = active.selectionEnd || 0;
      const value = active.value || '';
      const selected = cleanText(value.slice(start, end));
      if (selected) return selected;
      return cleanText(value);
    }

    const assistant = [...document.querySelectorAll('[data-message-author-role="assistant"], article, .markdown')].pop();
    if (assistant) return cleanText(assistant.innerText || assistant.textContent || '');

    return '';
  }

  function getSelectedTextOnly() {
    return cleanText(window.getSelection && window.getSelection().toString());
  }

  function findComposer() {
    const selectors = [
      '#prompt-textarea',
      '[data-testid="composer"] [contenteditable="true"]',
      '[data-testid="composer"] textarea',
      'form [contenteditable="true"][role="textbox"]',
      'form textarea',
      'textarea[placeholder]',
      'textarea',
      '[contenteditable="true"][role="textbox"]',
      'div[role="textbox"]',
      '[contenteditable="true"]',
      '.ProseMirror',
      'rich-textarea [contenteditable="true"]'
    ];
    for (const selector of selectors) {
      const candidates = [...document.querySelectorAll(selector)]
        .filter(el => el.offsetParent !== null || el.getClientRects().length > 0);
      if (candidates.length) return candidates[candidates.length - 1];
    }
    return null;
  }

  function findStopButton() {
    const selectors = [
      'button[aria-label*="Stop" i]',
      'button[aria-label*="Parar" i]',
      'button[data-testid="stop-button"]'
    ];
    for (const selector of selectors) {
      const buttons = [...document.querySelectorAll(selector)].filter(btn => isVisible(btn) && !btn.disabled);
      if (buttons.length) return buttons[buttons.length - 1];
    }
    const allButtons = [...document.querySelectorAll('button')].filter(btn => isVisible(btn) && !btn.disabled);
    const stopButtons = allButtons.filter(btn => /stop|parar/i.test(`${btn.innerText || ''} ${btn.getAttribute('aria-label') || ''} ${btn.title || ''}`));
    if (stopButtons.length) return stopButtons[stopButtons.length - 1];
    return null;
  }

  async function waitForIdleOrStop() {
    let stopBtn = findStopButton();
    if (stopBtn) {
      try { stopBtn.click(); } catch (_) {}
      await new Promise(r => setTimeout(r, 600));
    }
    stopBtn = findStopButton();
    if (stopBtn) {
      return { ok: false, error: 'Destino ocupado. Aguarde ou pare a geração antes de enviar.' };
    }
    return { ok: true };
  }

  async function insertTextIntoComposer(text) {
    const idle = await waitForIdleOrStop();
    if (!idle.ok) return idle;

    const composer = findComposer();
    if (!composer) return { ok: false, error: 'Campo de texto da conversa não encontrado.' };

    const payload = cleanText(text);
    if (!payload) return { ok: false, error: 'Texto vazio.' };

    composer.scrollIntoView({ block: 'center', behavior: 'smooth' });
    composer.focus();

    if (composer.tagName === 'TEXTAREA' || composer.tagName === 'INPUT') {
      const start = composer.selectionStart ?? composer.value.length;
      const end = composer.selectionEnd ?? composer.value.length;
      const before = composer.value.slice(0, start);
      const after = composer.value.slice(end);
      const glue = before && !before.endsWith('\n') ? '\n\n' : '';
      composer.value = before + glue + payload + after;
      const pos = (before + glue + payload).length;
      composer.setSelectionRange(pos, pos);
      composer.dispatchEvent(new InputEvent('input', { bubbles: true, inputType: 'insertText', data: payload }));
      composer.dispatchEvent(new Event('change', { bubbles: true }));
      showToast('Texto colado no campo da conversa. Confira antes de enviar.');
      return { ok: true };
    }

    const prefix = composer.innerText && composer.innerText.trim() ? '\n\n' : '';
    const textToInsert = prefix + payload;
    let worked = false;

    try {
      const dt = new DataTransfer();
      dt.setData('text/plain', textToInsert);
      worked = composer.dispatchEvent(new ClipboardEvent('paste', { bubbles: true, cancelable: true, clipboardData: dt }));
    } catch (_) {
      worked = false;
    }

    if (!worked || !(composer.innerText || composer.textContent || '').includes(payload.slice(0, 60))) {
      worked = Boolean(document.execCommand && document.execCommand('insertText', false, textToInsert));
    }

    if (!worked || !(composer.innerText || composer.textContent || '').includes(payload.slice(0, 60))) {
      const selection = window.getSelection();
      const range = document.createRange();
      range.selectNodeContents(composer);
      range.collapse(false);
      selection.removeAllRanges();
      selection.addRange(range);
      const node = document.createTextNode(textToInsert);
      range.insertNode(node);
      range.setStartAfter(node);
      range.collapse(true);
      selection.removeAllRanges();
      selection.addRange(range);
    }

    composer.dispatchEvent(new InputEvent('input', { bubbles: true, inputType: 'insertText', data: payload }));
    composer.dispatchEvent(new Event('change', { bubbles: true }));
    showToast('Texto colado no campo da conversa. Confira antes de enviar.');
    return { ok: true };
  }

  function focusComposer() {
    const composer = findComposer();
    if (!composer) return { ok: false, error: 'Campo de texto não encontrado.' };
    composer.scrollIntoView({ block: 'center', behavior: 'smooth' });
    composer.focus();
    showToast('Campo focado. Para print/imagem, pressione Ctrl+V se o navegador bloquear colagem automática.');
    return { ok: true };
  }

  function isVisible(el) {
    return Boolean(el && (el.offsetParent !== null || el.getClientRects().length > 0));
  }

  function dataUrlToFile(dataUrl, name = 'chat-bridge-print.png') {
    const [meta, base64] = String(dataUrl || '').split(',');
    const mime = /data:([^;]+)/.exec(meta || '')?.[1] || 'image/png';
    const binary = atob(base64 || '');
    const bytes = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
    return new File([bytes], name || 'chat-bridge-print.png', { type: mime });
  }

  function dataTransferWithFile(file) {
    const dt = new DataTransfer();
    dt.items.add(file);
    return dt;
  }

  async function attachImageToComposer(dataUrl, name) {
    const idle = await waitForIdleOrStop();
    if (!idle.ok) return idle;

    const composer = findComposer();
    if (!composer) return { ok: false, error: 'Campo de texto da conversa destino não encontrado.' };
    if (!dataUrl) return { ok: false, error: 'Imagem vazia.' };

    composer.scrollIntoView({ block: 'center', behavior: 'smooth' });
    composer.focus();

    const file = dataUrlToFile(dataUrl, name || `chat-bridge-print-${Date.now()}.png`);
    const fileInputs = [...document.querySelectorAll('input[type="file"]')]
      .filter(input => !input.disabled)
      .sort((a, b) => Number(isVisible(b)) - Number(isVisible(a)));

    for (const input of fileInputs) {
      try {
        const dt = dataTransferWithFile(file);
        input.files = dt.files;
        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.dispatchEvent(new Event('change', { bubbles: true }));
        showToast('Print anexado no destino. Confira antes de enviar.');
        return { ok: true, method: 'file-input' };
      } catch (_) {
        // Tenta outras rotas abaixo.
      }
    }

    try {
      const dt = dataTransferWithFile(file);
      composer.dispatchEvent(new ClipboardEvent('paste', { bubbles: true, cancelable: true, clipboardData: dt }));
      showToast('Tentei colar o print no destino. Confira se a imagem anexou.');
      return { ok: true, method: 'paste-event' };
    } catch (_) {
      // Tenta drop abaixo.
    }

    try {
      const dt = dataTransferWithFile(file);
      composer.dispatchEvent(new DragEvent('drop', { bubbles: true, cancelable: true, dataTransfer: dt }));
      showToast('Tentei soltar o print no destino. Confira se a imagem anexou.');
      return { ok: true, method: 'drop-event' };
    } catch (err) {
      return { ok: false, error: err.message || 'O Chrome bloqueou o anexo automático de imagem.' };
    }
  }

  function findSubmitButton() {
    const composer = findComposer();
    const form = composer?.closest?.('form');
    const roots = [form, document].filter(Boolean);
    const selectors = [
      'button[data-testid="send-button"]',
      'button[data-testid="composer-submit-button"]',
      'button[aria-label*="Enviar" i]',
      'button[aria-label*="Send" i]',
      'button[title*="Enviar" i]',
      'button[title*="Send" i]',
      'form button[type="submit"]',
      'button[type="submit"]'
    ];

    for (const root of roots) {
      for (const selector of selectors) {
        const buttons = [...root.querySelectorAll(selector)]
          .filter(btn => isVisible(btn) && !btn.disabled && btn.getAttribute('aria-disabled') !== 'true');
        const safeButtons = buttons.filter(btn => !/stop|parar|cancel/i.test(`${btn.innerText || ''} ${btn.getAttribute('aria-label') || ''} ${btn.title || ''}`));
        if (safeButtons.length) return safeButtons[safeButtons.length - 1];
      }
    }
    return null;
  }

  async function submitComposer() {
    const idle = await waitForIdleOrStop();
    if (!idle.ok) return idle;

    const button = findSubmitButton();
    if (!button) return { ok: false, error: 'Botão de enviar não encontrado ou desativado.' };
    button.click();
    showToast('Mensagem enviada na conversa destino.');
    return { ok: true };
  }

  function normalizeRole(role) {
    const r = String(role || '').toLowerCase();
    if (r.includes('assistant') || r.includes('model') || r.includes('claude') || r.includes('gemini')) return 'assistant';
    if (r.includes('user') || r.includes('human')) return 'user';
    return 'mensagem';
  }

  function compactMessageNodes(nodes) {
    const seen = new Set();
    return nodes
      .map(m => ({ ...m, role: normalizeRole(m.role), text: cleanText(m.text), html: m.html || '' }))
      .filter(m => m.text.length > 0)
      .filter(m => {
        const key = `${m.role}:${m.text.slice(0, 180)}`;
        if (seen.has(key)) return false;
        seen.add(key);
        return true;
      });
  }

  function getMessageNodes() {
    const chatgpt = [...document.querySelectorAll('[data-message-author-role]')]
      .filter(el => cleanText(el.innerText || el.textContent || '').length > 0)
      .map(el => ({
        role: el.getAttribute('data-message-author-role') || 'mensagem',
        text: cleanText(el.innerText || el.textContent || ''),
        html: el.innerHTML || ''
      }));
    if (chatgpt.length) return compactMessageNodes(chatgpt);

    const claude = [...document.querySelectorAll('[data-testid="user-message"], [data-testid="assistant-message"], [data-testid="message-content"], .font-claude-message')]
      .filter(el => cleanText(el.innerText || el.textContent || '').length > 0)
      .map(el => ({
        role: /user|human/i.test(el.getAttribute('data-testid') || el.className || '') ? 'user' : 'assistant',
        text: cleanText(el.innerText || el.textContent || ''),
        html: el.innerHTML || ''
      }));
    if (claude.length) return compactMessageNodes(claude);

    const gemini = [...document.querySelectorAll('user-query, model-response, message-content, .query-text, .model-response-text, .markdown')]
      .filter(el => cleanText(el.innerText || el.textContent || '').length > 0)
      .map(el => ({
        role: /user|query/i.test(el.tagName + ' ' + el.className) ? 'user' : 'assistant',
        text: cleanText(el.innerText || el.textContent || ''),
        html: el.innerHTML || ''
      }));
    if (gemini.length) return compactMessageNodes(gemini);

    const articles = [...document.querySelectorAll('article')]
      .filter(el => cleanText(el.innerText || el.textContent || '').length > 0)
      .map((el, i) => ({ role: i % 2 ? 'assistant' : 'user', text: cleanText(el.innerText || el.textContent || ''), html: el.innerHTML || '' }));
    if (articles.length) return compactMessageNodes(articles);

    const markdowns = [...document.querySelectorAll('.markdown, .prose, [class*="message"]')]
      .filter(el => cleanText(el.innerText || el.textContent || '').length > 20)
      .map(el => ({ role: 'mensagem', text: cleanText(el.innerText || el.textContent || ''), html: el.innerHTML || '' }));
    return compactMessageNodes(markdowns);
  }

  function buildTurns(nodes) {
    const turns = [];
    let current = [];
    for (const node of nodes) {
      if (node.role === 'user' && current.length) {
        turns.push(current);
        current = [];
      }
      current.push(node);
    }
    if (current.length) turns.push(current);
    return turns;
  }

  function selectCapture(count, mode, order, all = false) {
    if (mode === 'selection') {
      const text = getSelectedTextOnly();
      return text ? { kind: 'messages', picked: [{ role: 'selection', text, html: escapeHtml(text).replace(/\n/g, '<br>') }] } : { kind: 'messages', picked: [] };
    }

    const nodes = getMessageNodes();
    const qty = Math.max(1, Number(count || 3));
    const newestFirst = order !== 'oldest-first';

    if (mode === 'turns') {
      let turns = buildTurns(nodes);
      if (!all) turns = turns.slice(-qty);
      if (newestFirst) turns = turns.reverse();
      return { kind: 'turns', picked: turns };
    }

    let filtered = nodes;
    if (mode === 'assistant') filtered = nodes.filter(m => m.role === 'assistant');
    if (mode === 'user') filtered = nodes.filter(m => m.role === 'user');
    let picked = all ? filtered : filtered.slice(-qty);
    if (newestFirst) picked = picked.reverse();
    return { kind: 'messages', picked };
  }

  function captureModeLabel(mode) {
    if (mode === 'selection') return 'texto selecionado';
    if (mode === 'turns') return 'turnos completos';
    if (mode === 'assistant') return 'respostas da IA';
    if (mode === 'user') return 'mensagens do usuário';
    return 'mensagens';
  }

  function formatRecentMessages(count, format, mode = 'messages', order = 'recent-first', all = false) {
    const capture = selectCapture(count, mode, order, all);
    const total = capture.kind === 'turns'
      ? capture.picked.reduce((sum, turn) => sum + turn.length, 0)
      : capture.picked.length;
    if (!total) return '';

    const orderLabel = order === 'oldest-first' ? 'da mais antiga para a mais recente' : 'da mais recente para a mais antiga';
    const amountLabel = all ? 'todas encontradas na página' : (capture.kind === 'turns' ? `${capture.picked.length} turno(s), ${total} mensagem(ns)` : `${total} mensagem(ns)`);
    const header = `Fonte: ${getPageTitle()}\nURL: ${location.href}\nCaptura: ${captureModeLabel(mode)}\nOrdem: ${orderLabel}\nQuantidade: ${amountLabel}\n`;

    if (capture.kind === 'turns') {
      return formatTurns(capture.picked, format, header);
    }

    const picked = capture.picked;

    if (format === 'html') {
      const body = picked.map((m, i) => `<section data-chat-bridge-message="${i + 1}"><h3>${i + 1}. ${escapeHtml(m.role)}</h3><div>${m.html || escapeHtml(m.text).replace(/\n/g, '<br>')}</div></section>`).join('\n');
      return `${header}\n[HTML COPIÁVEL]\n<div class="chat-bridge-export">\n${body}\n</div>`;
    }

    if (format === 'plain') {
      return `${header}\n` + picked.map((m, i) => `${i + 1}. ${roleLabel(m.role)}\n${m.text}`).join('\n\n---\n\n');
    }

    return `${header}\n` + picked.map((m, i) => `### ${i + 1}. ${roleLabel(m.role)}\n\n${m.text}`).join('\n\n---\n\n');
  }

  function formatTurns(turns, format, header) {
    if (format === 'html') {
      const body = turns.map((turn, i) => {
        const messages = turn.map((m, j) => `<section data-chat-bridge-message="${i + 1}-${j + 1}"><h4>${escapeHtml(roleLabel(m.role))}</h4><div>${m.html || escapeHtml(m.text).replace(/\n/g, '<br>')}</div></section>`).join('\n');
        return `<section data-chat-bridge-turn="${i + 1}"><h3>Turno ${i + 1}</h3>${messages}</section>`;
      }).join('\n');
      return `${header}\n[HTML COPIÁVEL]\n<div class="chat-bridge-export">\n${body}\n</div>`;
    }

    if (format === 'plain') {
      return `${header}\n` + turns.map((turn, i) => {
        const content = turn.map(m => `${roleLabel(m.role)}\n${m.text}`).join('\n\n');
        return `Turno ${i + 1}\n\n${content}`;
      }).join('\n\n---\n\n');
    }

    return `${header}\n` + turns.map((turn, i) => {
      const content = turn.map(m => `#### ${roleLabel(m.role)}\n\n${m.text}`).join('\n\n');
      return `### Turno ${i + 1}\n\n${content}`;
    }).join('\n\n---\n\n');
  }

  function roleLabel(role) {
    const r = String(role || '').toLowerCase();
    if (r.includes('selection')) return 'Texto selecionado';
    if (r.includes('assistant') || r.includes('model')) return 'Resposta da IA';
    if (r.includes('user')) return 'Mensagem do usuário';
    return 'Mensagem';
  }

  function escapeHtml(str) {
    return String(str || '').replace(/[&<>"']/g, ch => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' }[ch]));
  }

  async function copyText(text) {
    try {
      await navigator.clipboard.writeText(text);
      return true;
    } catch (_) {
      const ta = document.createElement('textarea');
      ta.value = text;
      ta.style.cssText = 'position:fixed;left:-9999px;top:-9999px';
      document.body.appendChild(ta);
      ta.select();
      const ok = document.execCommand('copy');
      ta.remove();
      return ok;
    }
  }

  async function copyImageDataUrl(dataUrl) {
    const blob = await (await fetch(dataUrl)).blob();
    if (!navigator.clipboard || !window.ClipboardItem) throw new Error('Clipboard de imagem não disponível neste contexto.');
    await navigator.clipboard.write([new ClipboardItem({ [blob.type]: blob })]);
  }

  async function sendRecentToTargets() {
    if (state.sending) return;
    state.sending = true;
    try {
      const settings = await loadSettings();
      const targetIds = await getTargetIds();
      if (!targetIds.length) {
        showToast('Nenhum destino configurado para esta aba.');
        return;
      }

      if (settings.format === 'screenshot') {
        const res = await sendRuntime({ type: 'BG_CAPTURE_VISIBLE_TAB' });
        if (!res?.ok) throw new Error(res?.error || 'Falha ao capturar print.');
        const firstTarget = targetIds[0];
        const attached = await sendRuntime({ type: 'BG_ATTACH_IMAGE_TO_TAB', tabId: firstTarget, dataUrl: res.dataUrl, name: `chat-bridge-print-${Date.now()}.png` });
        if (!attached?.ok) {
          await copyImageDataUrl(res.dataUrl);
          await sendRuntime({ type: 'BG_FOCUS_COMPOSER', tabId: firstTarget });
          showToast('O Chrome bloqueou o anexo direto. Print copiado; pressione Ctrl+V no destino se não aparecer.');
        } else {
          showToast(targetIds.length > 1 ? 'Print enviado ao 1º destino. Para vários destinos, repita por segurança.' : 'Print enviado para o destino. Confira antes de enviar.');
        }
        return;
      }

      const text = formatRecentMessages(settings.recentCount, settings.format, settings.captureMode, settings.order);
      if (!text) {
        showToast(settings.captureMode === 'selection' ? 'Selecione um trecho da conversa antes de enviar.' : 'Não encontrei mensagens para capturar nesta página.');
        return;
      }
      const res = await sendRuntime({ type: 'BG_SEND_TEXT_TO_TABS', tabIds: targetIds, text });
      const okCount = (res?.results || []).filter(r => r.ok).length;
      showToast(okCount ? `Enviado para ${okCount} conversa(s) destino. Confira antes de enviar.` : 'Não consegui colar no destino. Veja se as conversas estão abertas.');
      if (settings.autoOpenAfterSend && targetIds[0]) await sendRuntime({ type: 'BG_ACTIVATE_TAB', tabId: targetIds[0] });
    } catch (err) {
      showToast(err.message || String(err));
    } finally {
      state.sending = false;
    }
  }

  async function copyRecentOnly() {
    const settings = await loadSettings();
    const text = formatRecentMessages(settings.recentCount, settings.format === 'screenshot' ? 'markdown' : settings.format, settings.captureMode, settings.order);
    if (!text) return showToast(settings.captureMode === 'selection' ? 'Selecione um trecho da conversa antes de copiar.' : 'Não encontrei mensagens para copiar.');
    await copyText(text);
    showToast('Mensagens recentes copiadas para a área de transferência.');
  }

  async function refreshTabs() {
    const res = await sendRuntime({ type: 'BG_GET_CONVERSATION_TABS' });
    state.tabs = res?.ok ? res.tabs || [] : [];
    return state.tabs;
  }

  async function getTargetIds() {
    const tabId = (await sendRuntime({ type: 'BG_GET_ACTIVE_TAB_ID' }))?.id;
    if (!tabId) return [];
    const { targetsBySourceTab = {} } = await storageGet({ targetsBySourceTab: {} });
    const targets = targetsBySourceTab[tabId] || [];
    return targets;
  }

  async function sendItemDirectly(item) {
    const targetIds = await getTargetIds();
    if (!targetIds.length) {
      return showToast('Nenhum destino configurado para esta aba.');
    }

    if (item.type === 'text') {
      const res = await sendRuntime({ type: 'BG_SEND_TEXT_TO_TABS', tabIds: targetIds, text: item.text || '' });
      const okCount = (res?.results || []).filter(r => r.ok).length;
      showToast(okCount ? `Texto enviado a ${okCount} destino(s).` : 'Não consegui colar o texto no destino.');
    } else if (item.type === 'image') {
      let successCount = 0;
      let fallback = false;
      for (const targetId of targetIds) {
        const attached = await sendRuntime({ type: 'BG_ATTACH_IMAGE_TO_TAB', tabId: targetId, dataUrl: item.dataUrl, name: item.name || `chat-bridge-print-${Date.now()}.png` });
        if (attached?.ok) {
          successCount++;
        } else {
          fallback = true;
          try {
            await copyImageDataUrl(item.dataUrl);
            await sendRuntime({ type: 'BG_FOCUS_COMPOSER', tabId: targetId });
          } catch (err) {}
        }
      }
      if (fallback) {
        showToast('Print copiado; pressione Ctrl+V no destino se necessário.');
      } else {
        showToast(`Print anexado a ${successCount} destino(s).`);
      }
    }
  }

  async function getStoredItems() {
    const data = await storageGet({ items: [] });
    return data.items || [];
  }

  async function addStoredItem(item) {
    const items = await getStoredItems();
    const next = [...items, { ...item, id: crypto.randomUUID(), createdAt: Date.now() }].slice(-20);
    await storageSet({ items: next });
  }

  // --- CORE v0.3.2 IMPLEMENTATION ---
  let shadow = null;
  const $ = (id) => shadow ? shadow.getElementById(id) : null;

  const css = `
    #cb2-float-root, #cb2-float-root * { box-sizing: border-box; margin: 0; padding: 0; }
    #cb2-float-root {
      position: fixed;
      right: 18px;
      top: 12%;
      z-index: 2147483647;
      font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
      color: #1f2937;
    }
    #cb2-button {
      width: 48px;
      height: 48px;
      border: 0;
      border-radius: 50%;
      cursor: pointer;
      color: white;
      background: linear-gradient(135deg, hsl(156, 72%, 40%), hsl(156, 72%, 30%));
      box-shadow: 0 8px 24px rgba(16, 185, 129, 0.3);
      font-size: 20px;
      display: grid;
      place-items: center;
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    #cb2-button:hover {
      transform: scale(1.08) translateY(-2px);
      box-shadow: 0 12px 28px rgba(16, 185, 129, 0.45);
    }
    #cb2-panel {
      position: fixed;
      right: 80px;
      top: 12%;
      width: 330px;
      max-height: 84vh;
      overflow-y: auto;
      border-radius: 16px;
      background: rgba(255, 255, 255, 0.88);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      color: #1f2937;
      box-shadow: 0 20px 48px rgba(0, 0, 0, 0.15), 0 1px 3px rgba(0, 0, 0, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.4);
      padding: 16px;
      display: none;
      flex-direction: column;
      z-index: 2147483647 !important;
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    #cb2-panel.open {
      display: flex !important;
    }
    #cb2-panel.minimized {
      max-height: 52px;
      overflow: hidden;
      padding-bottom: 4px;
    }
    #cb2-panel.minimized .cb2-body {
      display: none;
    }
    .cb2-drag-handle {
      cursor: grab;
      padding-bottom: 12px;
      margin-bottom: 12px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      user-select: none;
      border-bottom: 1px solid rgba(0, 0, 0, 0.08);
    }
    .cb2-drag-handle:active {
      cursor: grabbing;
    }
    .cb2-drag-handle h3 {
      font-size: 14px;
      font-weight: 700;
      color: #111827;
      letter-spacing: -0.025em;
    }
    .cb2-win-controls {
      display: flex;
      gap: 6px;
    }
    .cb2-win-btn {
      border: 0;
      background: transparent;
      width: 24px;
      height: 24px;
      border-radius: 6px;
      cursor: pointer;
      font-size: 14px;
      display: grid;
      place-items: center;
      color: #6b7280;
      transition: background 0.2s, color 0.2s;
    }
    .cb2-win-btn:hover {
      background: rgba(0, 0, 0, 0.05);
      color: #111827;
    }

    #cb2-state-bar {
      margin-bottom: 12px;
      padding: 10px 12px;
      background: rgba(0, 0, 0, 0.03);
      border: 1px solid rgba(0, 0, 0, 0.05);
      border-radius: 10px;
    }
    .cb2-state-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 6px;
    }
    .cb2-state-row:last-child {
      margin-bottom: 0;
    }
    .cb2-state-label {
      font-size: 11px;
      font-weight: 600;
      color: #6b7280;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .cb2-state-value {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 12px;
      font-weight: 700;
    }
    .cb2-led {
      display: inline-block;
      width: 10px;
      height: 10px;
      border-radius: 50%;
    }
    .cb2-led.IDLE { background-color: hsl(215, 16%, 47%); box-shadow: 0 0 8px hsl(215, 16%, 47%); }
    .cb2-led.COPIADO_PARA_CODEX { background-color: hsl(200, 89%, 48%); box-shadow: 0 0 8px hsl(200, 89%, 48%); }
    .cb2-led.AGUARDANDO_COLAGEM_MANUAL { background-color: hsl(45, 95%, 48%); box-shadow: 0 0 8px hsl(45, 95%, 48%); }
    .cb2-led.AGUARDANDO_RESPOSTA_CODEX {
      background-color: hsl(28, 90%, 50%);
      box-shadow: 0 0 8px hsl(28, 90%, 50%);
      animation: cb2-pulse 1.5s infinite ease-in-out;
    }
    .cb2-led.RESPOSTA_CODEX_COLADA { background-color: hsl(280, 75%, 55%); box-shadow: 0 0 8px hsl(280, 75%, 55%); }
    .cb2-led.AGUARDANDO_AUDITORIA_CHATGPT { background-color: hsl(38, 92%, 50%); box-shadow: 0 0 8px hsl(38, 92%, 50%); }
    .cb2-led.AUDITADO { background-color: hsl(156, 72%, 45%); box-shadow: 0 0 8px hsl(156, 72%, 45%); }
    .cb2-led.BLOQUEADO { background-color: hsl(0, 0%, 20%); box-shadow: 0 0 8px hsl(0, 0%, 20%); }
    .cb2-led.ERRO { background-color: hsl(0, 84%, 60%); box-shadow: 0 0 8px hsl(0, 84%, 60%); }

    @keyframes cb2-pulse {
      0% { transform: scale(1); opacity: 1; }
      50% { transform: scale(1.25); opacity: 0.5; }
      100% { transform: scale(1); opacity: 1; }
    }

    .cb2-roles-info {
      font-size: 11px;
      color: #4b5563;
      margin-top: 6px;
      border-top: 1px dashed rgba(0, 0, 0, 0.08);
      padding-top: 6px;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }
    .cb2-role-item {
      display: flex;
      justify-content: space-between;
    }
    .cb2-role-item span.role-title {
      font-weight: 600;
    }

    .cb2-role-section {
      margin-bottom: 14px;
    }
    .cb2-section-title {
      font-size: 11px;
      font-weight: 700;
      color: #6b7280;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 6px;
    }
    .cb2-role-buttons {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 6px;
    }
    .cb2-role-btn {
      border: 1px solid rgba(0, 0, 0, 0.08);
      background: white;
      border-radius: 8px;
      padding: 6px 2px;
      font-size: 10px;
      font-weight: 600;
      cursor: pointer;
      text-align: center;
      transition: all 0.2s;
      color: #4b5563;
    }
    .cb2-role-btn:hover {
      background: #f9fafb;
      border-color: rgba(0, 0, 0, 0.15);
    }
    .cb2-role-btn.active.chatgpt {
      background: hsl(156, 72%, 95%);
      color: hsl(156, 72%, 25%);
      border-color: hsl(156, 72%, 45%);
      font-weight: bold;
    }
    .cb2-role-btn.active.codex {
      background: hsl(199, 89%, 95%);
      color: hsl(199, 89%, 25%);
      border-color: hsl(199, 89%, 45%);
      font-weight: bold;
    }
    .cb2-role-btn.active.antigravity {
      background: hsl(262, 70%, 95%);
      color: hsl(262, 70%, 30%);
      border-color: hsl(262, 70%, 55%);
      font-weight: bold;
    }

    .cb2-action-group {
      margin-bottom: 12px;
      padding: 10px;
      background: rgba(255, 255, 255, 0.4);
      border: 1px solid rgba(0, 0, 0, 0.04);
      border-radius: 12px;
    }

    .cb2-btn {
      width: 100%;
      border: 0;
      border-radius: 8px;
      padding: 8px 12px;
      margin-bottom: 6px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      background: white;
      color: #374151;
      text-align: left;
      border: 1px solid rgba(0, 0, 0, 0.06);
      display: flex;
      align-items: center;
      justify-content: space-between;
      transition: all 0.25s ease;
    }
    .cb2-btn:hover {
      background: #f9fafb;
      border-color: rgba(0, 0, 0, 0.12);
      transform: translateY(-1px);
    }
    .cb2-btn:disabled {
      opacity: 0.5;
      cursor: not-allowed;
      transform: none !important;
    }
    .cb2-btn.primary {
      background: linear-gradient(135deg, hsl(156, 72%, 40%), hsl(156, 72%, 35%));
      color: white;
      border: 0;
    }
    .cb2-btn.danger {
      background: rgba(239, 68, 68, 0.08);
      color: #b91c1c;
      border: 1px solid rgba(239, 68, 68, 0.15);
    }

    #cb2-toast {
      position: fixed;
      right: 18px;
      bottom: 18px;
      z-index: 2147483647;
      max-width: 350px;
      padding: 12px 16px;
      border-radius: 12px;
      background: #111827;
      color: white;
      font-size: 13px;
      font-weight: 500;
      box-shadow: 0 12px 32px rgba(0, 0, 0, 0.25);
      border: 1px solid rgba(255, 255, 255, 0.08);
      animation: cb2-slide-up 0.3s ease;
    }

    #cb2-modal-container {
      display: none;
      position: fixed;
      left: 0;
      top: 0;
      width: 100vw;
      height: 100vh;
      background: rgba(0, 0, 0, 0.4);
      backdrop-filter: blur(4px);
      z-index: 2147483647;
      align-items: center;
      justify-content: center;
    }
    .cb2-modal-box {
      background: white;
      border-radius: 16px;
      padding: 20px;
      width: 380px;
      box-shadow: 0 24px 64px rgba(0, 0, 0, 0.25);
      border: 1px solid rgba(255, 255, 255, 0.5);
      display: flex;
      flex-direction: column;
      gap: 12px;
    }
    .cb2-modal-textarea {
      width: 100%;
      height: 140px;
      border-radius: 8px;
      border: 1px solid #d1d5db;
      padding: 10px;
      font-family: monospace;
      font-size: 11px;
      resize: vertical;
      background: #f9fafb;
    }
    .cb2-modal-actions {
      display: flex;
      justify-content: flex-end;
      gap: 8px;
    }
    .cb2-modal-btn {
      border: 0;
      padding: 8px 14px;
      border-radius: 8px;
      font-size: 11px;
      font-weight: 700;
      cursor: pointer;
    }
    .cb2-modal-btn.save {
      background: linear-gradient(135deg, hsl(156, 72%, 40%), hsl(156, 72%, 35%));
      color: white;
    }

    @keyframes cb2-slide-up {
      from { transform: translateY(20px); opacity: 0; }
      to { transform: translateY(0); opacity: 1; }
    }

    @media (prefers-color-scheme: dark) {
      #cb2-panel { background: rgba(23, 23, 23, 0.88); color: #f3f4f6; border-color: rgba(255,255,255,0.08); }
      .cb2-modal-box { background: #1f2937; color: #f3f4f6; border-color: rgba(255,255,255,0.08); }
      .cb2-modal-textarea { background: #111827; border-color: rgba(255, 255, 255, 0.08); color: #f3f4f6; }
    }
  `;

  function showToast(message) {
    if (!shadow) return;
    let box = shadow.getElementById('cb2-toast');
    if (!box) {
      box = document.createElement('div');
      box.id = 'cb2-toast';
      shadow.appendChild(box);
    }
    box.textContent = message;
    clearTimeout(box._timer);
    box._timer = setTimeout(() => { if (box && box.parentNode) box.remove(); }, 4200);
  }

  function ensureUi() {
    if (document.getElementById('cb2-float-host')) {
      shadow = document.getElementById('cb2-float-host').shadowRoot;
      return;
    }

    const host = document.createElement('div');
    host.id = 'cb2-float-host';
    host.style.position = 'fixed';
    host.style.right = '0';
    host.style.top = '0';
    host.style.width = '0';
    host.style.height = '0';
    host.style.zIndex = '2147483647';
    document.documentElement.appendChild(host);

    shadow = host.attachShadow({ mode: 'open' });

    const style = document.createElement('style');
    style.textContent = css;
    shadow.appendChild(style);

    const root = document.createElement('div');
    root.id = 'cb2-float-root';
    root.innerHTML = `
      <button id="cb2-button" title="ChatFÁCIL Bridge">🪄</button>
      <div id="cb2-panel">
        <div class="cb2-drag-handle" id="cb2-drag">
          <h3>ChatFÁCIL Bridge v0.3.2</h3>
          <div class="cb2-win-controls">
            <button class="cb2-win-btn" id="cb2-min">_</button>
            <button class="cb2-win-btn" id="cb2-close-panel">×</button>
          </div>
        </div>
        <div class="cb2-body">
          <div id="cb2-state-bar">
            <div class="cb2-state-row">
              <span class="cb2-state-label">Estado Fila</span>
              <div class="cb2-state-value"><span class="cb2-led IDLE" id="cb2-led"></span><span id="cb2-state-text">Livre</span></div>
            </div>
            <div class="cb2-roles-info">
              <div class="cb2-role-item"><span class="role-title">Fonte:</span><span id="cb2-info-source">-</span></div>
              <div class="cb2-role-item"><span class="role-title">Codex:</span><span id="cb2-info-codex">-</span></div>
              <div class="cb2-role-item"><span class="role-title">Antigravity:</span><span id="cb2-info-antigravity">-</span></div>
            </div>
          </div>
          <div class="cb2-role-section">
            <div class="cb2-section-title">Papel desta aba</div>
            <div class="cb2-role-buttons">
              <button class="cb2-role-btn" id="cb2-role-chatgpt">ChatGPT</button>
              <button class="cb2-role-btn" id="cb2-role-codex">Codex Aba</button>
              <button class="cb2-role-btn" id="cb2-role-antigravity">Antigravity</button>
            </div>
          </div>
          
          <!-- Codex Desktop Section (WINDOWS_APP_ASSISTED) -->
          <div class="cb2-action-group" style="border-left: 3px solid hsl(200, 89%, 48%); padding-left: 8px;">
            <div class="cb2-section-title" style="color: hsl(200, 89%, 48%); font-weight: bold; display: flex; justify-content: space-between; align-items: center;">
              <span>🔵 Codex Desktop</span>
              <span style="font-size: 8px; background: rgba(14,165,233,0.15); padding: 1px 4px; border-radius: 4px;">Assistido</span>
            </div>
            <p style="font-size: 10px; color: #6b7280; line-height: 1.35; margin-bottom: 8px;">
              Codex é aplicativo Windows. A extensão copia o prompt; cole no Codex e traga a resposta.
            </p>
            <button class="cb2-btn" id="cb2-action-copy-codex">📋 Copiar para Codex ➔</button>
            <button class="cb2-btn" id="cb2-action-mark-pasted">✓ Marcar como colado</button>
            <button class="cb2-btn" id="cb2-action-paste-response">📥 Colar resposta</button>
            <button class="cb2-btn primary" id="cb2-action-audit-codex" style="display:none">🚀 Enviar p/ Auditoria ChatGPT</button>
            <button class="cb2-btn danger" id="cb2-action-clear-codex">🗑️ Limpar fila Codex</button>
          </div>

          <!-- Web Tabs Section (WEB_TAB) -->
          <div class="cb2-action-group" style="border-left: 3px solid hsl(262, 70%, 58%); padding-left: 8px;">
            <div class="cb2-section-title" style="color: hsl(262, 70%, 58%);">🟣 Antigravity & Abas</div>
            <button class="cb2-btn antigravity-btn" id="cb2-action-send-antigravity">📤 Enviar para Antigravity ➔</button>
            <button class="cb2-btn" id="cb2-action-submit">🚀 Forçar 'Enviar' no destino</button>
            <button class="cb2-btn" id="cb2-action-pull-response">📥 Trazer resposta da aba</button>
          </div>

          <div class="cb2-action-group">
            <div class="cb2-section-title">Auditoria</div>
            <button class="cb2-btn" id="cb2-action-audit">✅ Marcar Auditado</button>
            <button class="cb2-btn danger" id="cb2-action-reset">🗑️ Reset Fila (Livre)</button>
          </div>

          <div style="font-size:9px; color:#9ca3af; text-align:center; margin-top:8px; border-top:1px dashed rgba(0,0,0,0.08); padding-top:6px; line-height: 1.3;">
            🔌 Futuro: LOCAL_BRIDGE_FUTURE (Native Messaging Host & Script Host Integrado)
          </div>
        </div>
      </div>

      <div id="cb2-modal-container">
        <div class="cb2-modal-box">
          <h3>Colar Resposta do Codex Desktop</h3>
          <p>Cole o resultado gerado pelo Codex Desktop abaixo para registrar na fila da extensão:</p>
          <textarea class="cb2-modal-textarea" id="cb2-modal-textarea" placeholder="Pressione Ctrl+V para colar a resposta do Codex aqui..."></textarea>
          <div class="cb2-modal-actions">
            <button class="cb2-modal-btn cancel" id="cb2-modal-cancel">Cancelar</button>
            <button class="cb2-modal-btn save" id="cb2-modal-save">Salvar Resposta</button>
          </div>
        </div>
      </div>
    `;
    shadow.appendChild(root);

    const panel = shadow.getElementById('cb2-panel');
    const dragHandle = shadow.getElementById('cb2-drag');
    let isDragging = false;
    let offset = { x: 0, y: 0 };

    dragHandle.addEventListener('mousedown', (e) => {
      isDragging = true;
      const rect = panel.getBoundingClientRect();
      offset.x = e.clientX - rect.left;
      offset.y = e.clientY - rect.top;
      panel.style.transition = 'none';
      document.body.style.userSelect = 'none';
    });

    window.addEventListener('mousemove', (e) => {
      if (!isDragging) return;
      let left = e.clientX - offset.x;
      let top = e.clientY - offset.y;
      left = Math.max(0, Math.min(left, window.innerWidth - panel.offsetWidth));
      top = Math.max(0, Math.min(top, window.innerHeight - panel.offsetHeight));
      panel.style.left = left + 'px';
      panel.style.top = top + 'px';
      panel.style.right = 'auto';
      panel.style.bottom = 'auto';
    });

    window.addEventListener('mouseup', () => {
      if (isDragging) {
        isDragging = false;
        document.body.style.userSelect = '';
        storageSet({ cb2PanelPos: { left: panel.style.left, top: panel.style.top } });
      }
    });

    storageGet({ cb2PanelPos: null }).then(data => {
      if (data.cb2PanelPos) {
        panel.style.left = data.cb2PanelPos.left;
        panel.style.top = data.cb2PanelPos.top;
        panel.style.right = 'auto';
      }
    });

    shadow.getElementById('cb2-button').addEventListener('click', () => {
      state.open = !state.open;
      panel.classList.toggle('open', state.open);
      panel.classList.remove('minimized');
      if (state.open) {
        updateMiniPanelDestinations().catch(() => {});
      }
    });

    shadow.getElementById('cb2-close-panel').addEventListener('click', () => {
      state.open = false;
      panel.classList.remove('open');
    });

    shadow.getElementById('cb2-min').addEventListener('click', () => {
      panel.classList.toggle('minimized');
    });

    // --- LOGICA DE PAPÉIS DA ABA ---
    shadow.getElementById('cb2-role-chatgpt').addEventListener('click', async () => {
      const myTabId = (await sendRuntime({ type: 'BG_GET_ACTIVE_TAB_ID' }))?.id;
      if (!myTabId) return showToast('Aba atual não identificada.');
      const data = await storageGet(['codexTabId', 'antigravityTabId']);
      const updates = { sourceTabId: myTabId };
      if (data.codexTabId === myTabId) updates.codexTabId = null;
      if (data.antigravityTabId === myTabId) updates.antigravityTabId = null;
      await storageSet(updates);
      showToast('Esta aba foi marcada como Fonte (ChatGPT).');
    });

    shadow.getElementById('cb2-role-codex').addEventListener('click', async () => {
      const myTabId = (await sendRuntime({ type: 'BG_GET_ACTIVE_TAB_ID' }))?.id;
      if (!myTabId) return showToast('Aba atual não identificada.');
      const data = await storageGet(['sourceTabId', 'antigravityTabId']);
      const updates = { codexTabId: myTabId };
      if (data.sourceTabId === myTabId) updates.sourceTabId = null;
      if (data.antigravityTabId === myTabId) updates.antigravityTabId = null;
      await storageSet(updates);
      showToast('Esta aba foi marcada como Destino (Codex Aba).');
    });

    shadow.getElementById('cb2-role-antigravity').addEventListener('click', async () => {
      const myTabId = (await sendRuntime({ type: 'BG_GET_ACTIVE_TAB_ID' }))?.id;
      if (!myTabId) return showToast('Aba atual não identificada.');
      const data = await storageGet(['sourceTabId', 'codexTabId']);
      const updates = { antigravityTabId: myTabId };
      if (data.sourceTabId === myTabId) updates.sourceTabId = null;
      if (data.codexTabId === myTabId) updates.codexTabId = null;
      await storageSet(updates);
      showToast('Esta aba foi marcada como Destino (Antigravity).');
    });

    // --- COPIAR PARA CODEX DESKTOP ASSISTIDO ---
    shadow.getElementById('cb2-action-copy-codex').addEventListener('click', async () => {
      const store = await storageGet(['globalState', 'activePayload']);
      
      // Impedir novo se houver payload ativo
      if (store.globalState && store.globalState !== 'IDLE' && store.globalState !== 'AUDITADO') {
        showToast(`Fila ocupada (${store.globalState}). Libere a fila antes de enviar.`);
        return;
      }

      let content = getSelectedTextOnly();
      let contentType = 'selection';
      if (!content) {
        const composer = findComposer();
        content = composer ? (composer.value || composer.innerText || '').trim() : '';
        contentType = 'composer';
      }
      if (!content) {
        content = formatRecentMessages(1, 'markdown', 'user', 'recent-first');
        contentType = 'last_user_msg';
      }
      if (!content) {
        showToast('Nenhum texto selecionado ou digitado para copiar.');
        return;
      }

      const payload = {
        id: crypto.randomUUID(),
        origem: 'ChatGPT',
        destino: 'Codex Desktop',
        destinationType: 'WINDOWS_APP_ASSISTED',
        conteudo: content,
        horario: new Date().toISOString(),
        status: 'COPIADO_PARA_CODEX',
        proximoPassoEsperado: 'Colar no Codex Desktop (Ctrl+V) e executar.'
      };

      await copyText(content);

      await storageSet({
        globalState: 'COPIADO_PARA_CODEX',
        activePayload: payload
      });

      showToast('Prompt copiado para o Codex. Cole manualmente no aplicativo Codex.');
    });

    // --- MARCAR COMO COLADO NO CODEX ---
    shadow.getElementById('cb2-action-mark-pasted').addEventListener('click', async () => {
      const store = await storageGet(['activePayload']);
      if (!store.activePayload || store.activePayload.destinationType !== 'WINDOWS_APP_ASSISTED') {
        showToast('Nenhum payload ativo para o Codex Desktop.');
        return;
      }
      
      const payload = store.activePayload;
      payload.status = 'AGUARDANDO_RESPOSTA_CODEX';
      payload.proximoPassoEsperado = 'Aguardar processamento no Codex Desktop e copiar resposta.';
      
      await storageSet({
        globalState: 'AGUARDANDO_RESPOSTA_CODEX',
        activePayload: payload
      });
      
      showToast('Fila atualizada. Aguardando processamento no Codex Desktop.');
    });

    // --- ABRIR MODAL PARA COLAR RESPOSTA ---
    shadow.getElementById('cb2-action-paste-response').addEventListener('click', async () => {
      const store = await storageGet(['activePayload']);
      if (!store.activePayload || store.activePayload.destinationType !== 'WINDOWS_APP_ASSISTED') {
        showToast('Nenhum payload ativo para o Codex Desktop.');
        return;
      }
      
      const modal = shadow.getElementById('cb2-modal-container');
      const textarea = shadow.getElementById('cb2-modal-textarea');
      if (modal && textarea) {
        textarea.value = '';
        modal.style.display = 'flex';
        textarea.focus();
      }
    });

    // --- MODAL: CANCELAR E SALVAR ---
    shadow.getElementById('cb2-modal-cancel').addEventListener('click', () => {
      const modal = shadow.getElementById('cb2-modal-container');
      if (modal) modal.style.display = 'none';
    });

    shadow.getElementById('cb2-modal-save').addEventListener('click', async () => {
      const textarea = shadow.getElementById('cb2-modal-textarea');
      const text = textarea ? textarea.value.trim() : '';
      if (!text) {
        showToast('A resposta colada está vazia.');
        return;
      }

      const store = await storageGet(['activePayload']);
      if (!store.activePayload) return;

      const payload = store.activePayload;
      payload.resposta = text;
      payload.status = 'RESPOSTA_CODEX_COLADA';
      payload.proximoPassoEsperado = 'Enviar para auditoria no ChatGPT.';

      await storageSet({
        globalState: 'RESPOSTA_CODEX_COLADA',
        activePayload: payload
      });

      const modal = shadow.getElementById('cb2-modal-container');
      if (modal) modal.style.display = 'none';
      showToast('Resposta do Codex registrada com sucesso!');
    });

    // --- ENVIAR RESPOSTA PARA AUDITORIA NO CHATGPT ---
    shadow.getElementById('cb2-action-audit-codex').addEventListener('click', async () => {
      const store = await storageGet(['activePayload']);
      if (!store.activePayload || !store.activePayload.resposta) {
        showToast('Nenhuma resposta do Codex registrada para auditoria.');
        return;
      }

      const payload = store.activePayload;
      const myTabId = (await sendRuntime({ type: 'BG_GET_ACTIVE_TAB_ID' }))?.id;
      const sourceTabId = store.activePayload.tabIdOrigem || myTabId;

      if (!sourceTabId) {
        showToast('Aba do ChatGPT (Fonte) não identificada.');
        return;
      }

      const auditText = `---
[Auditoria Chat Bridge] Resposta recebida do Codex para auditoria
Origem: Codex Desktop (WINDOWS_APP_ASSISTED)
Horário: ${new Date().toLocaleString('pt-BR')}

${payload.resposta}
---`;

      showToast('Inserindo resposta para auditoria...');

      const insertRes = await sendRuntime({
        type: 'BG_FORWARD_TO_TAB',
        tabId: sourceTabId,
        message: {
          type: 'INSERT_TEXT',
          text: auditText
        }
      });

      if (insertRes?.ok) {
        payload.status = 'AGUARDANDO_AUDITORIA_CHATGPT';
        payload.proximoPassoEsperado = 'Auditar e aprovar a resposta no ChatGPT.';
        
        await storageSet({
          globalState: 'AGUARDANDO_AUDITORIA_CHATGPT',
          activePayload: payload
        });
        
        await sendRuntime({ type: 'BG_FOCUS_COMPOSER', tabId: sourceTabId });
        showToast('Enviado para auditoria no ChatGPT!');
      } else {
        showToast(`Erro ao retornar: ${insertRes?.error || 'Aba fechada?'}`);
      }
    });

    // --- LIMPAR FILA CODEX (COM CONFIRMAÇÃO) ---
    shadow.getElementById('cb2-action-clear-codex').addEventListener('click', async () => {
      if (confirm('Tem certeza que deseja limpar e resetar a fila do Codex?')) {
        await storageSet({
          globalState: 'IDLE',
          activePayload: null
        });
        showToast('Fila do Codex resetada.');
      }
    });

    // --- ENVIAR PARA DESTINOS (ABAS WEB) ---
    async function handleSendToTarget(targetRole) {
      const store = await storageGet(['globalState', 'activePayload', 'sourceTabId', 'codexTabId', 'antigravityTabId']);
      
      if (store.globalState && store.globalState !== 'IDLE' && store.globalState !== 'AUDITADO') {
        showToast(`Fila ocupada (${store.globalState}). Libere ou reset a fila antes.`);
        return;
      }
      
      const myTabId = (await sendRuntime({ type: 'BG_GET_ACTIVE_TAB_ID' }))?.id;
      if (!myTabId) return showToast('Aba atual não identificada.');

      const destTabId = targetRole === 'codex' ? store.codexTabId : store.antigravityTabId;
      if (!destTabId) {
        showToast(`Aba do ${targetRole === 'codex' ? 'Codex' : 'Antigravity'} não configurada.`);
        return;
      }

      if (myTabId === destTabId) {
        showToast('Não é permitido enviar para a própria aba atual.');
        return;
      }

      let content = getSelectedTextOnly();
      let contentType = 'selection';
      if (!content) {
        const composer = findComposer();
        content = composer ? (composer.value || composer.innerText || '').trim() : '';
        contentType = 'composer';
      }
      if (!content) {
        content = formatRecentMessages(1, 'markdown', 'user', 'recent-first');
        contentType = 'last_user_msg';
      }
      if (!content) {
        showToast('Nenhum texto selecionado ou digitado para enviar.');
        return;
      }

      const payload = {
        id: crypto.randomUUID(),
        origem: `Aba ${myTabId} (${getPageTitle().slice(0, 24)})`,
        destino: targetRole === 'codex' ? 'Codex Aba' : 'Antigravity',
        destinationType: 'WEB_TAB',
        horario: new Date().toISOString(),
        tipoContent: contentType,
        conteudo: content,
        status: targetRole === 'codex' ? 'ENVIADO_PARA_CODEX' : 'ENVIADO_PARA_ANTIGRAVITY',
        tabIdOrigem: myTabId,
        tabIdDestino: destTabId
      };

      await storageSet({
        globalState: payload.status,
        activePayload: payload
      });

      showToast(`Pasting prompt into ${payload.destino}...`);

      const pasteRes = await sendRuntime({
        type: 'BG_FORWARD_TO_TAB',
        tabId: destTabId,
        message: {
          type: 'INSERT_TEXT',
          text: content
        }
      });

      if (pasteRes?.ok) {
        showToast(`Colado no ${payload.destino}!`);
        await sendRuntime({ type: 'BG_FOCUS_COMPOSER', tabId: destTabId });
        await storageSet({ globalState: 'EXECUTANDO' });
      } else {
        showToast(`Erro ao colar: ${pasteRes?.error || 'Conexão perdida.'}`);
        await storageSet({ globalState: 'ERRO' });
      }
    }

    shadow.getElementById('cb2-action-send-antigravity').addEventListener('click', () => handleSendToTarget('antigravity'));
    
    // --- LEGACY SUBMIT ---
    shadow.getElementById('cb2-action-submit').addEventListener('click', async () => {
      const store = await storageGet(['activePayload']);
      const targetId = store.activePayload?.tabIdDestino;
      if (!targetId) return showToast('Nenhum destino web configurado no payload ativo.');
      const res = await sendRuntime({ type: 'BG_SUBMIT_COMPOSER', tabId: targetId });
      if (res?.ok) showToast('Envio acionado.');
      else showToast('Falha ao acionar envio.');
    });

    // --- LEGACY PULL ---
    shadow.getElementById('cb2-action-pull-response').addEventListener('click', async () => {
      const store = await storageGet(['activePayload', 'sourceTabId']);
      const targetId = store.activePayload?.tabIdDestino;
      if (!targetId) return showToast('Nenhum destino web configurado no payload.');
      const firstTarget = targetId;
      showToast('Buscando resposta do destino...');
      
      try {
        const res = await sendRuntime({
          type: 'BG_FORWARD_TO_TAB',
          tabId: firstTarget,
          message: {
            type: 'CAPTURE_RECENT_MESSAGES',
            count: 1,
            all: false,
            format: 'plain',
            captureMode: 'assistant',
            order: 'recent-first'
          }
        });
        
        if (!res?.ok || !res.text) {
          return showToast('Não há resposta pronta no destino para trazer.');
        }
        
        const insertRes = await insertTextIntoComposer(res.text);
        if (insertRes?.ok) {
          showToast('Resposta trazida do destino!');
          triggerStateReport();
        } else {
          showToast(insertRes?.error || 'Erro ao inserir resposta.');
        }
      } catch (err) {
        showToast('Erro ao trazer resposta do destino.');
      }
    });

    // --- AUDITORIA & LIBERAR FILA (COM CONTROLES E CONFIRMAÇÕES) ---
    shadow.getElementById('cb2-action-audit').addEventListener('click', async () => {
      const store = await storageGet(['activePayload']);
      if (!store.activePayload || (!store.activePayload.resposta && !store.activePayload.respostaCapturada)) {
        showToast('Não é possível marcar como auditado antes de capturar ou colar a resposta.');
        return;
      }
      await storageSet({
        globalState: 'IDLE',
        activePayload: null
      });
      showToast('Fila liberada e estado marcado como Auditado.');
    });

    shadow.getElementById('cb2-action-reset').addEventListener('click', async () => {
      if (confirm('Deseja forçar o reset da fila de estados para Livre?')) {
        await storageSet({
          globalState: 'IDLE',
          activePayload: null
        });
        showToast('Fila resetada com sucesso.');
      }
    });
  }

  let lastReportedState = null;

  function detectLocalTabState() {
    try {
      const composer = findComposer();
      const stopBtn = findStopButton();
      
      const isGenerating = stopBtn !== null;
      const composerText = composer ? (composer.value || composer.innerText || '').trim() : '';
      const hasText = composerText.length > 0;
      
      let status = 'green';
      let label = 'pronto';
      
      if (isGenerating) {
        status = 'red';
        label = 'respondendo';
      } else if (hasText) {
        status = 'yellow';
        label = 'na caixa';
      } else {
        status = 'green';
        label = 'pronto';
      }
      
      return { status, label };
    } catch (err) {
      return { status: 'gray', label: 'indisponível' };
    }
  }

  function triggerStateReport() {
    const state = detectLocalTabState();
    lastReportedState = state;
    sendRuntime({ type: 'BG_UPDATE_TAB_STATE', state }).catch(() => {});
  }

  async function updateMiniPanelDestinations() {
    if (!shadow) return;

    const led = shadow.getElementById('cb2-led');
    const stateText = shadow.getElementById('cb2-state-text');
    const infoSource = shadow.getElementById('cb2-info-source');
    const infoCodex = shadow.getElementById('cb2-info-codex');
    const infoAntigravity = shadow.getElementById('cb2-info-antigravity');

    const store = await storageGet(['globalState', 'activePayload', 'sourceTabId', 'codexTabId', 'antigravityTabId']);
    const gState = store.globalState || 'IDLE';

    if (led && stateText) {
      led.className = `cb2-led ${gState}`;
      
      const stateLabels = {
        'IDLE': 'Livre',
        'COPIADO_PARA_CODEX': 'Prompt Copiado p/ Codex',
        'AGUARDANDO_COLAGEM_MANUAL': 'Aguardando Colagem',
        'AGUARDANDO_RESPOSTA_CODEX': 'Executando no Codex',
        'RESPOSTA_CODEX_COLADA': 'Resposta do Codex Colada',
        'EXECUTANDO': 'Executando no Destino',
        'RESPOSTA_CAPTURADA': 'Resposta Capturada',
        'AGUARDANDO_AUDITORIA_CHATGPT': 'Auditoria no ChatGPT',
        'AUDITADO': 'Auditado / Livre',
        'BLOQUEADO': 'Bloqueado',
        'ERRO': 'Erro na Fila'
      };
      
      stateText.textContent = stateLabels[gState] || gState;
    }

    const myTabId = (await sendRuntime({ type: 'BG_GET_ACTIVE_TAB_ID' }))?.id;

    const btnGpt = shadow.getElementById('cb2-role-chatgpt');
    const btnCodex = shadow.getElementById('cb2-role-codex');
    const btnAntigravity = shadow.getElementById('cb2-role-antigravity');

    if (btnGpt) btnGpt.classList.toggle('active', store.sourceTabId === myTabId);
    if (btnCodex) btnCodex.classList.toggle('active', store.codexTabId === myTabId);
    if (btnAntigravity) btnAntigravity.classList.toggle('active', store.antigravityTabId === myTabId);

    if (infoSource) infoSource.textContent = store.sourceTabId ? `Aba ${store.sourceTabId}` : '-';
    if (infoCodex) infoCodex.textContent = store.codexTabId ? `Aba ${store.codexTabId}` : '-';
    if (infoAntigravity) infoAntigravity.textContent = store.antigravityTabId ? `Aba ${store.antigravityTabId}` : '-';

    const btnCopyCodex = shadow.getElementById('cb2-action-copy-codex');
    const btnAuditCodex = shadow.getElementById('cb2-action-audit-codex');
    
    if (btnCopyCodex) {
      const hasActivePayload = gState && gState !== 'IDLE' && gState !== 'AUDITADO';
      btnCopyCodex.disabled = hasActivePayload;
    }

    if (btnAuditCodex) {
      const hasResponse = store.activePayload && store.activePayload.resposta && store.activePayload.destinationType === 'WINDOWS_APP_ASSISTED';
      btnAuditCodex.style.display = hasResponse ? 'block' : 'none';
    }
  }

  function initRealtimeSync() {
    setInterval(() => {
      const state = detectLocalTabState();
      if (!lastReportedState || lastReportedState.status !== state.status || lastReportedState.label !== state.label) {
        lastReportedState = state;
        sendRuntime({ type: 'BG_UPDATE_TAB_STATE', state }).catch(() => {});
      }
    }, 1500);
    
    setInterval(() => {
      const panel = shadow ? shadow.getElementById('cb2-panel') : null;
      if (panel && panel.classList.contains('open')) {
        updateMiniPanelDestinations().catch(() => {});
      }
    }, 1500);
    
    chrome.storage.onChanged.addListener((changes, area) => {
      if (area === 'local') {
        if (changes.globalState || changes.activePayload || changes.sourceTabId || changes.codexTabId || changes.antigravityTabId) {
          updateMiniPanelDestinations().catch(() => {});
        }
      }
    });

    triggerStateReport();
    updateMiniPanelDestinations().catch(() => {});
  }

  function renderPanel() {
    ensureUi();
  }

  ensureUi();
  loadSettings();
  initRealtimeSync();

  chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    try {
      if (message?.type === 'PING') {
        sendResponse({ ok: true });
        return true;
      }
      if (message?.type === 'CAPTURE_TEXT') {
        const text = getSelectedOrFocusedText();
        sendResponse({ ok: Boolean(text), text, title: getPageTitle(), url: location.href });
        return true;
      }
      if (message?.type === 'CAPTURE_RECENT_MESSAGES') {
        const text = formatRecentMessages(
          message.count || state.currentSettings.recentCount || 3,
          message.format || state.currentSettings.format || 'markdown',
          message.captureMode || state.currentSettings.captureMode || 'messages',
          message.order || state.currentSettings.order || 'recent-first',
          Boolean(message.all)
        );
        sendResponse({ ok: Boolean(text), text, title: getPageTitle(), url: location.href });
        return true;
      }
      if (message?.type === 'INSERT_TEXT') {
        insertTextIntoComposer(message.text || '')
          .then(res => {
            triggerStateReport();
            sendResponse(res);
          })
          .catch(err => sendResponse({ ok: false, error: err.message || String(err) }));
        return true;
      }
      if (message?.type === 'ATTACH_IMAGE_TO_COMPOSER') {
        attachImageToComposer(message.dataUrl || '', message.name || '')
          .then(res => {
            triggerStateReport();
            sendResponse(res);
          })
          .catch(err => sendResponse({ ok: false, error: err.message || String(err) }));
        return true;
      }
      if (message?.type === 'SUBMIT_COMPOSER') {
        submitComposer()
          .then(res => {
            sendRuntime({ type: 'BG_UPDATE_TAB_STATE', state: { status: 'red', label: 'respondendo' } }).catch(() => {});
            sendResponse(res);
          })
          .catch(err => sendResponse({ ok: false, error: err.message || String(err) }));
        return true;
      }
      if (message?.type === 'FOCUS_COMPOSER') {
        sendResponse(focusComposer());
        return true;
      }
      if (message?.type === 'OPEN_CHAT_BRIDGE') {
        state.open = true;
        renderPanel();
        sendResponse({ ok: true });
        return true;
      }
    } catch (err) {
      sendResponse({ ok: false, error: err.message || String(err) });
      return true;
    }
  });
})();
