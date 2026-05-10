(function () {
  'use strict';

  const WEEKDAYS = ['Lu', 'Ma', 'Mi', 'Ju', 'Vi', 'Sá', 'Do'];
  const monthFormatter = new Intl.DateTimeFormat('es-ES', {
    month: 'long',
    year: 'numeric',
  });
  const displayFormatter = new Intl.DateTimeFormat('es-ES', {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  });

  function parseIsoDate(iso) {
    if (!iso) return null;
    const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(iso.trim());
    if (!match) return null;
    const year = parseInt(match[1], 10);
    const month = parseInt(match[2], 10);
    const day = parseInt(match[3], 10);
    const date = new Date(year, month - 1, day);
    if (
      date.getFullYear() !== year ||
      date.getMonth() !== month - 1 ||
      date.getDate() !== day
    ) {
      return null;
    }
    return date;
  }

  function formatIso(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return year + '-' + month + '-' + day;
  }

  function formatDisplay(date) {
    return displayFormatter.format(date);
  }

  function formatMonthHeader(year, month) {
    return monthFormatter.format(new Date(year, month, 1));
  }

  function isSameDate(a, b) {
    if (!a || !b) return false;
    return (
      a.getFullYear() === b.getFullYear() &&
      a.getMonth() === b.getMonth() &&
      a.getDate() === b.getDate()
    );
  }

  function leadingBlanksMondayFirst(year, month) {
    return (new Date(year, month, 1).getDay() + 6) % 7;
  }

  function daysInMonth(year, month) {
    return new Date(year, month + 1, 0).getDate();
  }

  function createPopover() {
    const popover = document.createElement('div');
    popover.className = 'date-picker-popover is-hidden';

    const header = document.createElement('div');
    header.className = 'date-picker-header';

    const prev = document.createElement('button');
    prev.type = 'button';
    prev.className = 'date-picker-nav';
    prev.setAttribute('aria-label', 'Mes anterior');
    prev.textContent = '‹';

    const monthLabel = document.createElement('div');
    monthLabel.className = 'date-picker-month';

    const next = document.createElement('button');
    next.type = 'button';
    next.className = 'date-picker-nav';
    next.setAttribute('aria-label', 'Mes siguiente');
    next.textContent = '›';

    header.appendChild(prev);
    header.appendChild(monthLabel);
    header.appendChild(next);

    const grid = document.createElement('div');
    grid.className = 'date-picker-grid';

    WEEKDAYS.forEach(function (label) {
      const cell = document.createElement('div');
      cell.className = 'date-picker-weekday';
      cell.textContent = label;
      grid.appendChild(cell);
    });

    popover.appendChild(header);
    popover.appendChild(grid);

    return { popover: popover, prev: prev, next: next, monthLabel: monthLabel, grid: grid };
  }

  function renderGrid(grid, year, month, selectedDate, today, onSelect) {
    while (grid.children.length > WEEKDAYS.length) {
      grid.removeChild(grid.lastChild);
    }

    const blanks = leadingBlanksMondayFirst(year, month);
    const total = daysInMonth(year, month);

    for (let i = 0; i < blanks; i++) {
      const blank = document.createElement('div');
      blank.className = 'date-picker-day is-blank';
      grid.appendChild(blank);
    }

    for (let day = 1; day <= total; day++) {
      const date = new Date(year, month, day);
      const cell = document.createElement('button');
      cell.type = 'button';
      cell.className = 'date-picker-day';
      cell.textContent = String(day);
      if (isSameDate(date, today)) cell.classList.add('is-today');
      if (isSameDate(date, selectedDate)) cell.classList.add('is-selected');
      cell.addEventListener('click', function () {
        onSelect(date);
      });
      grid.appendChild(cell);
    }
  }

  function attach(input) {
    if (input.dataset.datePickerAttached === '1') return;
    input.dataset.datePickerAttached = '1';
    input.readOnly = true;

    let selectedDate = parseIsoDate(input.value) || new Date();
    let viewYear = selectedDate.getFullYear();
    let viewMonth = selectedDate.getMonth();

    const fieldName = input.getAttribute('name');
    const hidden = document.createElement('input');
    hidden.type = 'hidden';
    if (fieldName) hidden.name = fieldName;
    hidden.value = formatIso(selectedDate);
    input.removeAttribute('name');
    input.parentNode.insertBefore(hidden, input.nextSibling);

    input.value = formatDisplay(selectedDate);

    const parts = createPopover();
    document.body.appendChild(parts.popover);

    function rerender() {
      parts.monthLabel.textContent = formatMonthHeader(viewYear, viewMonth);
      const today = new Date();
      renderGrid(parts.grid, viewYear, viewMonth, selectedDate, today, handleSelect);
    }

    function position() {
      const rect = input.getBoundingClientRect();
      const popWidth = parts.popover.offsetWidth;
      const top = rect.bottom + window.scrollY + 4;
      let left = rect.left + window.scrollX;
      const viewportRight = window.scrollX + document.documentElement.clientWidth - 8;
      const viewportLeft = window.scrollX + 8;
      if (left + popWidth > viewportRight) left = viewportRight - popWidth;
      if (left < viewportLeft) left = viewportLeft;
      parts.popover.style.top = top + 'px';
      parts.popover.style.left = left + 'px';
    }

    function isOpen() {
      return !parts.popover.classList.contains('is-hidden');
    }

    function open() {
      viewYear = selectedDate.getFullYear();
      viewMonth = selectedDate.getMonth();
      rerender();
      parts.popover.classList.remove('is-hidden');
      position();
    }

    function close() {
      parts.popover.classList.add('is-hidden');
    }

    function handleSelect(date) {
      selectedDate = date;
      input.value = formatDisplay(date);
      hidden.value = formatIso(date);
      close();
      input.dispatchEvent(new Event('change', { bubbles: true }));
    }

    input.addEventListener('click', function () {
      if (isOpen()) close();
      else open();
    });

    input.addEventListener('keydown', function (event) {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        if (isOpen()) close();
        else open();
      } else if (event.key === 'Escape') {
        close();
      }
    });

    parts.prev.addEventListener('click', function () {
      viewMonth--;
      if (viewMonth < 0) {
        viewMonth = 11;
        viewYear--;
      }
      rerender();
    });

    parts.next.addEventListener('click', function () {
      viewMonth++;
      if (viewMonth > 11) {
        viewMonth = 0;
        viewYear++;
      }
      rerender();
    });

    document.addEventListener('click', function (event) {
      if (!isOpen()) return;
      if (event.target === input) return;
      if (parts.popover.contains(event.target)) return;
      close();
    });

    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && isOpen()) close();
    });

    window.addEventListener('resize', function () {
      if (isOpen()) position();
    });

    window.addEventListener(
      'scroll',
      function () {
        if (isOpen()) position();
      },
      true,
    );
  }

  function init() {
    const inputs = document.querySelectorAll('input.date-picker');
    inputs.forEach(attach);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
