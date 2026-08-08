(function () {
  'use strict';

  const BUTTON_ID = 'copy-orders-btn';
  const DATE_PICKER_SELECTOR = 'input.date-picker';
  const TABLE_BODY_SELECTOR = '.table tbody';
  const TOAST_DURATION_MS = 3500;

  function showToast(message, variant) {
    const toast = document.createElement('div');
    toast.className = 'toast';
    if (variant === 'error') {
      toast.style.borderColor = 'var(--red)';
      toast.style.color = 'var(--red)';
    }
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(function () {
      toast.remove();
    }, TOAST_DURATION_MS);
  }

  function getDateLabel() {
    const input = document.querySelector(DATE_PICKER_SELECTOR);
    if (!input) return '';
    return (input.value || '').trim();
  }

  function readRows(tbody) {
    const rows = [];
    const trs = tbody.querySelectorAll('tr');
    trs.forEach(function (tr) {
      const nameCell = tr.querySelector('th[scope="row"]');
      const numberCell = tr.querySelector('.col-right');
      if (!nameCell || !numberCell) return;
      const name = (nameCell.textContent || '').trim();
      const numberText = (numberCell.textContent || '').trim();
      const number = parseInt(numberText, 10);
      if (!name) return;
      if (!Number.isFinite(number)) return;
      rows.push({ name: name, number: number });
    });
    return rows;
  }

  function buildMessage(rows, dateLabel) {
    const visibleRows = rows.filter(function (r) {
      return r.number > 0;
    });
    const heading = '*Pedidos — ' + (dateLabel || '') + '*';
    if (visibleRows.length === 0) {
      return heading + '\n\n(Sin pedidos)';
    }
    const lines = visibleRows.map(function (r) {
      return '• *' + r.name + '*: ' + r.number;
    });
    return heading + '\n\n' + lines.join('\n');
  }

  function fallbackCopy(text) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.setAttribute('readonly', '');
    textarea.style.position = 'fixed';
    textarea.style.top = '0';
    textarea.style.left = '0';
    textarea.style.opacity = '0';
    textarea.style.pointerEvents = 'none';
    document.body.appendChild(textarea);
    textarea.focus();
    textarea.select();
    let ok = false;
    try {
      ok = document.execCommand('copy');
    } catch (_) {
      ok = false;
    }
    document.body.removeChild(textarea);
    return ok;
  }

  async function copyToClipboard(text) {
    if (navigator.clipboard && typeof navigator.clipboard.writeText === 'function') {
      try {
        await navigator.clipboard.writeText(text);
        return true;
      } catch (_) {
      }
    }
    return fallbackCopy(text);
  }

  async function handleClick() {
    const tbody = document.querySelector(TABLE_BODY_SELECTOR);
    if (!tbody) return;
    const rows = readRows(tbody);
    const message = buildMessage(rows, getDateLabel());
    const ok = await copyToClipboard(message);
    if (ok) {
      showToast('Pedido copiado');
    } else {
      showToast('No se pudo copiar', 'error');
    }
  }

  function init() {
    const button = document.getElementById(BUTTON_ID);
    if (!button) return;
    button.addEventListener('click', handleClick);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
