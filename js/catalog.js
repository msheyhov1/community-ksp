// Community KSP — витрина каталога: фильтры, сортировка, вид, догрузка.
// Работает по data-атрибутам карточек, при натяжке на Битрикс заменяется
// компонентами catalog.section / catalog.filter, разметка остаётся той же.

(function () {
  var grid = document.querySelector('[data-grid]');
  if (!grid) return;

  var cards = [].slice.call(grid.querySelectorAll('.p-card'));
  var filtersBox = document.getElementById('filters');
  var boxes = [].slice.call(document.querySelectorAll('.filters input[type="checkbox"][data-key]'));
  var priceMin = document.querySelector('[data-price-min]');
  var priceMax = document.querySelector('[data-price-max]');
  var sortSelect = document.querySelector('[data-sort]');
  var foundOut = document.querySelector('[data-found]');
  var emptyBox = document.querySelector('[data-empty]');
  var activeBox = document.querySelector('[data-active-filters]');
  var moreBtn = document.querySelector('[data-more]');
  var chips = [].slice.call(document.querySelectorAll('[data-chip]'));
  var STEP = parseInt(grid.dataset.step || '9', 10);
  var page = 1;            // текущая страница
  var accumulated = false; // true — показываем всё до текущей страницы («Показать ещё»)
  var pagesBox = document.querySelector('.pagination__pages');

  // ---------- вспомогательное ----------

  function values(input) {
    return (input.dataset.value || input.value || '').split(',');
  }

  function cardValues(card, key) {
    return (card.dataset[key] || '').split(',').filter(Boolean);
  }

  function checkedByKey() {
    var map = {};
    boxes.forEach(function (b) {
      if (!b.checked) return;
      map[b.dataset.key] = map[b.dataset.key] || [];
      map[b.dataset.key].push(b.value);
    });
    return map;
  }

  function priceRange() {
    return {
      min: parseInt((priceMin && priceMin.value) || '', 10) || 0,
      max: parseInt((priceMax && priceMax.value) || '', 10) || Infinity
    };
  }

  // Карточка проходит фильтр: внутри группы — ИЛИ, между группами — И
  function matches(card, map, range) {
    var price = parseInt(card.dataset.price, 10) || 0;
    if (price < range.min || price > range.max) return false;
    return Object.keys(map).every(function (key) {
      var mine = cardValues(card, key);
      return map[key].some(function (v) { return mine.indexOf(v) !== -1; });
    });
  }

  // ---------- счётчики у пунктов фильтра ----------

  function updateCounts(map, range) {
    boxes.forEach(function (box) {
      var probe = {};
      Object.keys(map).forEach(function (k) { if (k !== box.dataset.key) probe[k] = map[k]; });
      probe[box.dataset.key] = [box.value];
      var n = cards.filter(function (c) { return matches(c, probe, range); }).length;
      var out = box.parentElement.querySelector('.filters__count');
      if (out) out.textContent = n;
      box.parentElement.classList.toggle('is-empty', n === 0 && !box.checked);
    });
  }

  // ---------- чипы выбранных фильтров ----------

  function renderActive(map) {
    if (!activeBox) return;
    var chips = [];
    boxes.forEach(function (box) {
      if (!box.checked) return;
      var label = box.parentElement.textContent.replace(/\d+$/, '').trim();
      chips.push('<button class="active-filters__chip" type="button" data-drop="' + box.dataset.key + ':' + box.value + '">' +
        label + ' <svg class="ico"><use href="#i-close"/></svg></button>');
    });
    var range = priceRange();
    if (range.min || range.max !== Infinity) {
      chips.push('<button class="active-filters__chip" type="button" data-drop="price">' +
        (range.min ? 'от ' + range.min.toLocaleString('ru-RU') + ' ₽' : '') +
        (range.max !== Infinity ? ' до ' + range.max.toLocaleString('ru-RU') + ' ₽' : '') +
        ' <svg class="ico"><use href="#i-close"/></svg></button>');
    }
    activeBox.hidden = chips.length === 0;
    activeBox.innerHTML = chips.join('') +
      (chips.length ? '<button class="link" type="button" data-filters-reset>Сбросить всё</button>' : '');
  }

  // ---------- сортировка ----------

  function sortCards(list) {
    var mode = sortSelect ? sortSelect.value : 'pop';
    var num = function (card, key) { return parseFloat(card.dataset[key] || '0'); };
    var sorted = list.slice();
    if (mode === 'price-asc') sorted.sort(function (a, b) { return num(a, 'price') - num(b, 'price'); });
    else if (mode === 'price-desc') sorted.sort(function (a, b) { return num(b, 'price') - num(a, 'price'); });
    else if (mode === 'new') sorted.sort(function (a, b) { return num(b, 'new') - num(a, 'new'); });
    else if (mode === 'discount') sorted.sort(function (a, b) { return num(b, 'discount') - num(a, 'discount'); });
    else sorted.sort(function (a, b) { return num(b, 'pop') - num(a, 'pop'); });
    sorted.forEach(function (card) { grid.appendChild(card); });
    return sorted;
  }

  // ---------- чипы подкатегорий (те же фильтры, только крупно) ----------

  function boxOfChip(chip) {
    var parts = chip.dataset.chip.split(':');
    return boxes.filter(function (b) {
      return b.dataset.key === parts[0] && b.value === parts[1];
    })[0];
  }

  function syncChips() {
    chips.forEach(function (chip) {
      var box = boxOfChip(chip);
      chip.classList.toggle('is-active', !!box && box.checked);
    });
  }

  // ---------- перерисовка ----------

  // Номера страниц рисуем от количества найденного
  function renderPages(total) {
    if (!pagesBox) return;
    var count = Math.max(1, Math.ceil(total / STEP));
    if (count < 2) { pagesBox.hidden = true; return; }
    pagesBox.hidden = false;

    var html = '';
    if (page > 1) {
      html += '<button type="button" data-page="' + (page - 1) + '" aria-label="Предыдущая страница"><svg class="ico"><use href="#i-chev-l"/></svg></button>';
    }
    for (var i = 1; i <= count; i++) {
      html += '<button type="button" data-page="' + i + '"' + (i === page ? ' class="is-active"' : '') + '>' + i + '</button>';
    }
    if (page < count) {
      html += '<button type="button" data-page="' + (page + 1) + '" aria-label="Следующая страница"><svg class="ico"><use href="#i-chev-r"/></svg></button>';
    }
    pagesBox.innerHTML = html;
  }

  function apply(resetPaging) {
    var map = checkedByKey();
    var range = priceRange();
    var passed = cards.filter(function (c) { return matches(c, map, range); });

    if (resetPaging !== false) { page = 1; accumulated = false; }

    var pageCount = Math.max(1, Math.ceil(passed.length / STEP));
    if (page > pageCount) page = pageCount;
    var from = accumulated ? 0 : (page - 1) * STEP;
    var to = page * STEP;

    cards.forEach(function (c) { c.hidden = true; });
    var sorted = sortCards(passed);
    sorted.slice(from, to).forEach(function (c) {
      c.hidden = false;
      c.classList.remove('is-appearing');
      void c.offsetWidth;              // перезапуск анимации появления
      c.classList.add('is-appearing');
    });

    if (foundOut) foundOut.textContent = passed.length;
    if (emptyBox) emptyBox.hidden = passed.length !== 0;
    if (moreBtn) moreBtn.hidden = page >= pageCount;
    renderPages(passed.length);
    updateCounts(map, range);
    renderActive(map);
    syncChips();
  }

  // ---------- события ----------

  boxes.forEach(function (box) { box.addEventListener('change', function () { apply(); }); });
  [priceMin, priceMax].forEach(function (input) {
    if (input) input.addEventListener('input', function () { apply(); });
  });
  if (sortSelect) sortSelect.addEventListener('change', function () { apply(false); });

  if (moreBtn) {
    moreBtn.addEventListener('click', function (e) {
      e.preventDefault();
      page += 1;
      accumulated = true;
      apply(false);
    });
  }

  if (pagesBox) {
    pagesBox.addEventListener('click', function (e) {
      var btn = e.target.closest('[data-page]');
      if (!btn) return;
      page = parseInt(btn.dataset.page, 10);
      accumulated = false;
      apply(false);
      var top = document.querySelector('.listing').getBoundingClientRect().top + window.pageYOffset - 90;
      window.scrollTo({ top: top, behavior: 'smooth' });
    });
  }

  document.addEventListener('click', function (e) {
    var drop = e.target.closest('[data-drop]');
    if (drop) {
      var key = drop.dataset.drop;
      if (key === 'price') {
        if (priceMin) priceMin.value = '';
        if (priceMax) priceMax.value = '';
      } else {
        var parts = key.split(':');
        boxes.forEach(function (b) {
          if (b.dataset.key === parts[0] && b.value === parts[1]) b.checked = false;
        });
      }
      apply();
    }
    if (e.target.closest('[data-filters-reset]')) {
      boxes.forEach(function (b) { b.checked = false; });
      if (priceMin) priceMin.value = '';
      if (priceMax) priceMax.value = '';
      apply();
    }
  });

  // Вид: плитка / список — с короткой сменой, чтобы перестроение не «прыгало»
  document.querySelectorAll('[data-view]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      if (btn.classList.contains('is-active')) return;
      document.querySelectorAll('[data-view]').forEach(function (b) { b.classList.remove('is-active'); });
      btn.classList.add('is-active');

      grid.classList.add('is-switching');
      window.setTimeout(function () {
        grid.classList.toggle('listing__grid--list', btn.dataset.view === 'list');
        grid.classList.remove('is-switching');
        grid.querySelectorAll('.p-card:not([hidden])').forEach(function (card, i) {
          card.classList.remove('is-appearing');
          void card.offsetWidth;
          card.style.animationDelay = (i * 35) + 'ms';
          card.classList.add('is-appearing');
        });
      }, 130);
    });
  });

  // «Показать все» внутри группы фильтров
  document.querySelectorAll('[data-filters-expand]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      btn.parentElement.querySelectorAll('.filters__item[hidden]').forEach(function (item) { item.hidden = false; });
      btn.remove();
    });
  });

  // Шторка фильтров на мобильном
  var overlay = document.querySelector('.filters-overlay');
  function closeFilters() {
    filtersBox.classList.remove('is-open');
    if (overlay) overlay.hidden = true;
    document.body.classList.remove('is-locked');
  }
  document.querySelectorAll('[data-filters-open]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      filtersBox.classList.add('is-open');
      if (overlay) overlay.hidden = false;
      document.body.classList.add('is-locked');
    });
  });
  document.querySelectorAll('[data-filters-close], [data-filters-apply]').forEach(function (btn) {
    btn.addEventListener('click', closeFilters);
  });
  if (overlay) overlay.addEventListener('click', closeFilters);

  chips.forEach(function (chip) {
    chip.addEventListener('click', function () {
      var box = boxOfChip(chip);
      if (!box) return;
      box.checked = !box.checked;
      apply();
    });
  });

  // Предвыбор фильтров из ссылки: catalog-iphone.html?f=model:16pm,memory:512
  (function preselect() {
    var q = new URLSearchParams(location.search).get('f');
    if (!q) return;
    q.split(',').forEach(function (pair) {
      var parts = pair.split(':');
      boxes.forEach(function (b) {
        if (b.dataset.key === parts[0] && b.value === parts[1]) b.checked = true;
      });
    });
  })();

  apply();
})();

// Кнопка «Сравнить» на карточке товара
document.querySelectorAll('.p-card__compare').forEach(function (btn) {
  btn.addEventListener('click', function (e) {
    e.preventDefault();
    var on = btn.classList.toggle('is-active');
    btn.setAttribute('aria-label', on ? 'Убрать из сравнения' : 'Добавить к сравнению');
    if (window.showToast) {
      showToast(on ? 'Товар добавлен к сравнению' : 'Товар убран из сравнения');
    }
  });
});
