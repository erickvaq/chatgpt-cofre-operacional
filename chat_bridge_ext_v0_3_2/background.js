const SUPPORTED_URLS = [
  'https://chatgpt.com/*',
  'https://chat.openai.com/*',
  'https://gemini.google.com/*',
  'https://claude.ai/*'
];

function isSupportedUrl(url = '') {
  return /^https:\/\/(chatgpt\.com|chat\.openai\.com|gemini\.google\.com|claude\.ai)\//.test(url || '');
}

const tabStates = {};

function isChatGptUrl(url = '') {
  return /^https:\/\/(chatgpt\.com|chat\.openai\.com)\//.test(url || '');
}

async function ensureContent(tabId) {
  try {
    await chrome.tabs.sendMessage(tabId, { type: 'PING' });
    return { ok: true };
  } catch (_) {
    try {
      await chrome.scripting.executeScript({ target: { tabId }, files: ['content.js'] });
      return { ok: true };
    } catch (err) {
      return { ok: false, error: err.message || String(err) };
    }
  }
}

async function sendToTab(tabId, message) {
  const ready = await ensureContent(tabId);
  if (!ready.ok) return ready;
  try {
    return await chrome.tabs.sendMessage(tabId, message);
  } catch (err) {
    return { ok: false, error: err.message || String(err) };
  }
}

async function getConversationTabs() {
  const tabs = await chrome.tabs.query({});
  return tabs
    .filter(tab => tab.id && isSupportedUrl(tab.url))
    .map(tab => ({
      id: tab.id,
      title: tab.title || tab.url || `Aba ${tab.id}`,
      url: tab.url || '',
      active: Boolean(tab.active),
      windowId: tab.windowId,
      platform: isChatGptUrl(tab.url) ? 'ChatGPT' : 'Outro'
    }))
    .sort((a, b) => Number(isChatGptUrl(b.url)) - Number(isChatGptUrl(a.url)) || String(a.title).localeCompare(String(b.title)));
}

async function captureVisible(tabId) {
  const tab = await chrome.tabs.get(tabId);
  const dataUrl = await chrome.tabs.captureVisibleTab(tab.windowId, { format: 'png' });
  return { ok: true, dataUrl, title: tab.title || '', url: tab.url || '' };
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  (async () => {
    try {
      if (message?.type === 'BG_GET_CONVERSATION_TABS') {
        sendResponse({ ok: true, tabs: await getConversationTabs() });
        return;
      }

      if (message?.type === 'BG_UPDATE_TAB_STATE') {
        const tabId = sender?.tab?.id;
        if (tabId) {
          tabStates[tabId] = {
            status: message.state?.status || 'gray',
            label: message.state?.label || 'indisponível',
            lastSeen: Date.now()
          };
        }
        sendResponse({ ok: true });
        return;
      }

      if (message?.type === 'BG_GET_TAB_STATES') {
        try {
          const activeTabs = await chrome.tabs.query({});
          const activeTabIds = new Set(activeTabs.map(t => t.id));
          for (const id in tabStates) {
            if (!activeTabIds.has(Number(id))) {
              delete tabStates[id];
            }
          }
        } catch (_) {}
        sendResponse({ ok: true, states: tabStates });
        return;
      }

      if (message?.type === 'BG_FORWARD_TO_TAB') {
        const res = await sendToTab(message.tabId, message.message);
        sendResponse(res);
        return;
      }

      if (message?.type === 'BG_GET_ACTIVE_TAB_ID') {
        sendResponse({ ok: true, id: sender?.tab?.id });
        return;
      }

      if (message?.type === 'BG_INSERT_TEXT') {
        const res = await sendToTab(message.tabId, { type: 'INSERT_TEXT', text: message.text || '' });
        sendResponse(res);
        return;
      }

      if (message?.type === 'BG_ATTACH_IMAGE_TO_TAB') {
        const res = await sendToTab(message.tabId, { type: 'ATTACH_IMAGE_TO_COMPOSER', dataUrl: message.dataUrl || '', name: message.name || '' });
        sendResponse(res);
        return;
      }

      if (message?.type === 'BG_SUBMIT_COMPOSER') {
        const res = await sendToTab(message.tabId, { type: 'SUBMIT_COMPOSER' });
        sendResponse(res);
        return;
      }

      if (message?.type === 'BG_FOCUS_COMPOSER') {
        const res = await sendToTab(message.tabId, { type: 'FOCUS_COMPOSER' });
        if (res?.ok) await chrome.tabs.update(message.tabId, { active: true });
        sendResponse(res);
        return;
      }

      if (message?.type === 'BG_SEND_TEXT_TO_TABS') {
        const tabIds = Array.isArray(message.tabIds) ? message.tabIds : [];
        const results = [];
        for (const tabId of tabIds) {
          const res = await sendToTab(tabId, { type: 'INSERT_TEXT', text: message.text || '' });
          results.push({ tabId, ...res });
        }
        sendResponse({ ok: results.some(r => r.ok), results });
        return;
      }

      if (message?.type === 'BG_CAPTURE_VISIBLE_TAB') {
        const tabId = message.tabId || sender?.tab?.id;
        if (!tabId) throw new Error('Aba não identificada.');
        sendResponse(await captureVisible(tabId));
        return;
      }

      if (message?.type === 'BG_ACTIVATE_TAB') {
        await chrome.tabs.update(message.tabId, { active: true });
        sendResponse({ ok: true });
        return;
      }

      sendResponse({ ok: false, error: 'Mensagem não reconhecida.' });
    } catch (err) {
      sendResponse({ ok: false, error: err.message || String(err) });
    }
  })();
  return true;
});

// Inicialização do estado global
chrome.runtime.onInstalled.addListener(async () => {
  try {
    const data = await chrome.storage.local.get(['globalState']);
    if (!data.globalState) {
      await chrome.storage.local.set({
        globalState: 'IDLE',
        activePayload: null,
        sourceTabId: null,
        codexTabId: null,
        antigravityTabId: null
      });
    }
  } catch (e) {
    console.error('Erro na inicialização do storage:', e);
  }
});

// Limpeza automática ao fechar abas
chrome.tabs.onRemoved.addListener(async (tabId) => {
  try {
    const data = await chrome.storage.local.get(['sourceTabId', 'codexTabId', 'antigravityTabId', 'globalState', 'activePayload']);
    let updated = false;
    const updates = {};
    
    if (data.sourceTabId === tabId) {
      updates.sourceTabId = null;
      updated = true;
    }
    if (data.codexTabId === tabId) {
      updates.codexTabId = null;
      updated = true;
    }
    if (data.antigravityTabId === tabId) {
      updates.antigravityTabId = null;
      updated = true;
    }
    
    if (data.activePayload) {
      const isSourceClosed = data.activePayload.tabIdOrigem === tabId;
      const isDestClosed = data.activePayload.tabIdDestino === tabId && data.activePayload.destinationType !== 'WINDOWS_APP_ASSISTED';
      
      if (isSourceClosed || isDestClosed) {
        updates.globalState = 'IDLE';
        updates.activePayload = null;
        updated = true;
      }
    }
    
    if (updated) {
      await chrome.storage.local.set(updates);
    }
  } catch (e) {
    console.error('Erro ao processar remoção de aba:', e);
  }
});

