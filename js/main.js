// Community KSP — базовые интерактивы вёрстки (для натяжки на Битрикс заменяются компонентами)

// Счётчики в шапке: избранное и корзина
function bumpBadge(href, delta) {
  var badge = document.querySelector('.header__icons a[href="' + href + '"] .header__badge');
  if (!badge) return;
  var value = Math.max(0, (parseInt(badge.textContent, 10) || 0) + delta);
  badge.textContent = value;
  badge.hidden = value === 0;
  badge.classList.remove('is-bumped');
  void badge.offsetWidth;
  badge.classList.add('is-bumped');
}

// Избранное на карточке товара
document.querySelectorAll('.p-card__fav').forEach(function (btn) {
  btn.addEventListener('click', function (e) {
    e.preventDefault();
    var on = btn.classList.toggle('is-active');
    btn.setAttribute('aria-label', on ? 'Убрать из избранного' : 'В избранное');
    bumpBadge('favorites.html', on ? 1 : -1);
    if (window.showToast) showToast(on ? 'Добавили в избранное' : 'Убрали из избранного');
  });
});

// Табы на карточке товара: описание / характеристики / отзывы
function showTab(name) {
  document.querySelectorAll('.tabs__item').forEach(function (t) {
    t.classList.toggle('is-active', t.dataset.tab === name);
  });
  ['desc', 'specs', 'reviews'].forEach(function (key) {
    var block = document.getElementById('tab-' + key);
    if (!block) return;
    if (key === name) {
      block.style.display = '';
      block.classList.remove('is-fading');
      void block.offsetWidth;
      block.classList.add('is-fading');
    } else {
      block.style.display = 'none';
      block.classList.remove('is-fading');
    }
  });
}

document.querySelectorAll('.tabs__item').forEach(function (tab) {
  tab.addEventListener('click', function () { showTab(tab.dataset.tab); });
});

// Ссылка «12 отзывов» под заголовком открывает вкладку с отзывами
document.querySelectorAll('[data-tab-link]').forEach(function (link) {
  link.addEventListener('click', function (e) {
    e.preventDefault();
    showTab(link.dataset.tabLink);
    var block = document.getElementById('tab-' + link.dataset.tabLink);
    if (block) block.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
});

// Бургер-меню: на мобильном показываем/прячем меню категорий
var burger = document.querySelector('.burger');
if (burger) {
  burger.addEventListener('click', function () {
    var nav = document.querySelector('.nav');
    if (nav) nav.classList.toggle('is-open');
  });
}

// ================= Плавное раскрытие блоков =================
// Работает без изменения разметки: считаем высоту содержимого и анимируем её.
var CALM = window.matchMedia('(prefers-reduced-motion: reduce)');

function slideToggle(el, open) {
  if (!el) return;
  if (CALM.matches) { el.hidden = !open; return; }

  el.style.overflow = 'hidden';
  if (open) {
    el.hidden = false;
    var target = el.scrollHeight;
    el.style.height = '0px';
    el.style.opacity = '0';
    void el.offsetHeight;
    el.style.transition = 'height .28s ease, opacity .2s ease';
    el.style.height = target + 'px';
    el.style.opacity = '1';
    window.setTimeout(function () {
      el.style.transition = el.style.height = el.style.overflow = el.style.opacity = '';
    }, 300);
  } else {
    el.style.transition = '';
    el.style.height = el.scrollHeight + 'px';
    void el.offsetHeight;
    el.style.transition = 'height .24s ease, opacity .18s ease';
    el.style.height = '0px';
    el.style.opacity = '0';
    window.setTimeout(function () {
      el.hidden = true;
      el.style.transition = el.style.height = el.style.overflow = el.style.opacity = '';
    }, 240);
  }
}

// ================= Модальные окна =================
var lastFocused = null;

function openModal(id) {
  var modal = document.getElementById('modal-' + id);
  if (!modal) return;
  lastFocused = document.activeElement;
  modal.hidden = false;
  modal.classList.remove('is-closing');
  document.body.classList.add('is-locked');
  var input = modal.querySelector('input:not([type="hidden"]), textarea, select') ||
              modal.querySelector('.btn, button:not(.modal__close)');
  if (input) input.focus();
}

function closeModal(modal) {
  if (!modal || modal.hidden) return;
  if (CALM.matches) {
    modal.hidden = true;
  } else {
    modal.classList.add('is-closing');
    window.setTimeout(function () {
      modal.hidden = true;
      modal.classList.remove('is-closing');
    }, 180);
  }
  if (!document.querySelector('.modal:not([hidden]):not(.is-closing), .drawer:not([hidden])')) {
    document.body.classList.remove('is-locked');
  }
}

document.querySelectorAll('[data-modal-open]').forEach(function (el) {
  el.addEventListener('click', function (e) {
    e.preventDefault();
    openModal(el.dataset.modalOpen);
  });
});

document.querySelectorAll('[data-modal-close]').forEach(function (el) {
  el.addEventListener('click', function () {
    closeModal(el.closest('.modal'));
    if (lastFocused) { lastFocused.focus(); lastFocused = null; }
  });
});

// Ловушка фокуса: Tab не уводит за пределы открытого окна
document.addEventListener('keydown', function (e) {
  if (e.key !== 'Tab') return;
  var modal = document.querySelector('.modal:not([hidden])');
  if (!modal) return;
  var items = modal.querySelectorAll('a[href], button:not([disabled]), input, textarea, select');
  if (!items.length) return;
  var first = items[0], last = items[items.length - 1];
  if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
  else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
});

// ================= Мобильное меню =================
var drawer = document.getElementById('drawer');

document.querySelectorAll('[data-drawer-open]').forEach(function (el) {
  el.addEventListener('click', function () {
    if (!drawer) return;
    drawer.hidden = false;
    document.body.classList.add('is-locked');
  });
});

function closeDrawer() {
  if (!drawer || drawer.hidden) return;
  if (CALM.matches) {
    drawer.hidden = true;
  } else {
    drawer.classList.add('is-closing');
    window.setTimeout(function () {
      drawer.hidden = true;
      drawer.classList.remove('is-closing');
    }, 220);
  }
  if (!document.querySelector('.modal:not([hidden])')) {
    document.body.classList.remove('is-locked');
  }
}

document.querySelectorAll('[data-drawer-close]').forEach(function (el) {
  el.addEventListener('click', closeDrawer);
});

// Esc закрывает то, что открыто сверху
document.addEventListener('keydown', function (e) {
  if (e.key !== 'Escape') return;
  if (drawer && !drawer.hidden) {
    closeDrawer();
  } else {
    closeModal(document.querySelector('.modal:not([hidden])'));
    if (lastFocused) { lastFocused.focus(); lastFocused = null; }
  }
});

// ================= Вход: телефон → код =================
function loginStep(name) {
  document.querySelectorAll('#modal-login .modal__step').forEach(function (step) {
    step.hidden = step.dataset.step !== name;
  });
}

document.querySelectorAll('[data-login-next]').forEach(function (btn) {
  btn.addEventListener('click', function () { loginStep('code'); });
});
document.querySelectorAll('[data-login-back]').forEach(function (btn) {
  btn.addEventListener('click', function () { loginStep('phone'); });
});

// Код из SMS: автопереход между полями
document.querySelectorAll('.code-input input').forEach(function (input, i, all) {
  input.addEventListener('input', function () {
    input.value = input.value.replace(/\D/g, '');
    if (input.value && all[i + 1]) all[i + 1].focus();
  });
  input.addEventListener('keydown', function (e) {
    if (e.key === 'Backspace' && !input.value && all[i - 1]) all[i - 1].focus();
  });
});

// ================= Количество товара в корзине =================
document.querySelectorAll('.qty').forEach(function (box) {
  var input = box.querySelector('input');
  box.querySelectorAll('button').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var step = btn.dataset.qty === 'plus' ? 1 : -1;
      var value = Math.max(1, (parseInt(input.value, 10) || 1) + step);
      input.value = value;
      input.dispatchEvent(new Event('change', { bubbles: true }));
    });
  });
});

// Удаление строки корзины: если список опустел — показываем заглушку
document.querySelectorAll('[data-cart-remove]').forEach(function (btn) {
  btn.addEventListener('click', function () {
    var item = btn.closest('.cart-item');
    var list = item.parentElement;
    item.remove();
    if (!list.querySelector('.cart-item')) {
      var cart = document.querySelector('.cart');
      var empty = document.querySelector('.cart-empty');
      if (cart && empty) { cart.hidden = true; empty.hidden = false; }
    }
  });
});

// ================= Переключатели доставки и оплаты =================
// Список вариантов помечен data-group, дополнительные поля — data-extra-group
// с тем же значением; показываем те, что относятся к выбранному варианту.
document.querySelectorAll('.radio-list').forEach(function (list) {
  var group = list.dataset.group;
  list.querySelectorAll('.radio-card').forEach(function (card) {
    card.addEventListener('click', function () {
      list.querySelectorAll('.radio-card').forEach(function (c) { c.classList.remove('is-active'); });
      card.classList.add('is-active');
      if (!group) return;
      document.querySelectorAll('[data-extra-group="' + group + '"]').forEach(function (extra) {
        extra.hidden = extra.dataset.extraFor !== card.dataset.extra;
      });
    });
  });
});

// ================= Аккордеоны (заказы, вопросы) =================
document.querySelectorAll('.order__toggle').forEach(function (btn) {
  btn.addEventListener('click', function () {
    var order = btn.closest('.order');
    var open = order.classList.toggle('is-open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    slideToggle(order.querySelector('.order__body'), open);
  });
});

document.querySelectorAll('.faq__q').forEach(function (btn) {
  btn.addEventListener('click', function () {
    var item = btn.closest('.faq__item');
    var open = item.classList.toggle('is-open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    slideToggle(item.querySelector('.faq__a'), open);
  });
});

// ================= Личный кабинет: подсветка текущего раздела =================
(function () {
  var page = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.acc-nav a').forEach(function (link) {
    if (link.getAttribute('href') === page) link.classList.add('is-active');
  });
})();

// ================= Таблетки-переключатели =================
document.querySelectorAll('.pills').forEach(function (group) {
  group.querySelectorAll('.pill').forEach(function (pill) {
    pill.addEventListener('click', function () {
      group.querySelectorAll('.pill').forEach(function (p) { p.classList.remove('is-active'); });
      pill.classList.add('is-active');
      group.dispatchEvent(new Event('change', { bubbles: true }));
    });
  });
});

// Форматирование цены: 149990 → «149 990 ₽»
function money(value) {
  return Math.round(value).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ') + ' ₽';
}

// ================= Калькулятор рассрочки =================
// Наценка партнёра берётся из data-markup на форме (в процентах).
// Пока заказчик не прислал условия Ляриба/Хайр — там 0, и вместо цифры
// показывается «по договору», чтобы не выдумывать сумму.
(function () {
  var form = document.getElementById('calc-installment');
  if (!form) return;
  var sum = form.querySelector('[data-calc-sum]');
  var sumOut = form.querySelector('[data-calc-sum-out]');
  var down = form.querySelector('[data-calc-down]');
  var downOut = form.querySelector('[data-calc-down-out]');
  var months = form.querySelector('[data-calc-months]');
  var monthly = document.querySelector('[data-calc-monthly]');
  var total = document.querySelector('[data-calc-total]');
  var term = document.querySelector('[data-calc-term]');
  var downSum = document.querySelector('[data-calc-down-sum]');
  var downNote = document.querySelector('[data-calc-down-note]');
  var markupOut = document.querySelector('[data-calc-markup]');
  var markup = parseFloat(form.dataset.markup || '0') || 0;

  function recalc() {
    var value = parseInt(sum.value, 10) || 0;
    var pct = down ? (parseInt(down.value, 10) || 0) : 0;
    var m = parseInt(months.querySelector('.pill.is-active').dataset.months, 10);
    var totalSum = Math.round(value * (1 + markup / 100));
    var downPay = Math.round(totalSum * pct / 100);
    var rest = totalSum - downPay;

    sumOut.textContent = money(value);
    if (downOut) downOut.textContent = pct ? money(downPay) + ' · ' + pct + '%' : '0 ₽';
    monthly.textContent = money(rest / m);
    total.textContent = money(totalSum);
    term.textContent = m + ' мес.';
    if (downSum) downSum.textContent = money(downPay);
    if (downNote) downNote.textContent = pct ? 'после первого взноса' : 'без первого взноса';
    if (markupOut) markupOut.textContent = markup ? money(totalSum - value) : 'по договору';
  }

  sum.addEventListener('input', recalc);
  if (down) down.addEventListener('input', recalc);
  months.addEventListener('change', recalc);
  recalc();
})();

// ================= Калькулятор Trade-In =================
(function () {
  var form = document.getElementById('calc-tradein');
  if (!form) return;
  var model = form.querySelector('[data-trade-model]');
  var state = form.querySelector('[data-trade-state]');
  var out = document.querySelector('[data-trade-out]');
  var bonus = document.querySelector('[data-trade-bonus]');

  function recalc() {
    var base = parseInt(model.value, 10) || 0;
    var k = parseFloat(state.querySelector('.pill.is-active').dataset.k);
    var low = base * k * 0.95;
    var high = base * k * 1.05;
    out.textContent = money(low) + ' – ' + money(high);
    bonus.textContent = money(high * 0.05);
  }

  model.addEventListener('change', recalc);
  state.addEventListener('change', recalc);
  recalc();
})();

// ================= Сравнение: только различия =================
(function () {
  var table = document.querySelector('.compare');
  if (!table) return;

  // Строку считаем «различием», если значения в колонках не совпадают
  table.querySelectorAll('tbody tr:not(.compare__group)').forEach(function (row) {
    var values = [...row.querySelectorAll('td')].map(function (td) { return td.textContent.trim(); });
    if (values.length > 1 && values.some(function (v) { return v !== values[0]; })) {
      row.classList.add('is-diff');
    }
  });

  var toggle = document.getElementById('compare-diff');
  if (!toggle) return;
  toggle.addEventListener('change', function () {
    table.querySelectorAll('tbody tr:not(.compare__group)').forEach(function (row) {
      row.hidden = toggle.checked && !row.classList.contains('is-diff');
    });
  });
})();

// Удаление товара из сравнения
document.querySelectorAll('[data-compare-remove]').forEach(function (btn) {
  btn.addEventListener('click', function () {
    var cell = btn.closest('th, td');
    var index = [].slice.call(btn.closest('tr').children).indexOf(cell);

    document.querySelectorAll('.compare tr').forEach(function (row) {
      var target = row.children[index];
      // строки-заголовки групп занимают всю ширину — их не трогаем
      if (target && !target.hasAttribute('colspan')) target.remove();
    });

    var left = document.querySelectorAll('.compare thead .compare__product').length;
    var chip = document.querySelector('.chips .chip.is-active');
    if (chip) chip.textContent = chip.textContent.replace(/·\s*\d+/, '· ' + left);

    // ширину столбца-заголовка групп подгоняем под остаток
    document.querySelectorAll('.compare__group th').forEach(function (th) {
      th.setAttribute('colspan', left + 1);
    });

    if (left === 0) {
      var wrap = document.querySelector('.compare-wrap');
      var tools = document.querySelector('.compare-tools');
      var empty = document.querySelector('.empty');
      var chips = document.querySelector('.chips');
      if (wrap) wrap.hidden = true;
      if (tools) tools.hidden = true;
      if (chips) chips.hidden = true;
      if (empty) empty.hidden = false;
    }
    if (window.showToast) showToast('Товар убран из сравнения');
  });
});

// ================= Подсказки в поиске =================
document.querySelectorAll('[data-search-input]').forEach(function (input) {
  var drop = input.closest('form').querySelector('[data-search-drop]');
  if (!drop) return;
  var rows = [].slice.call(drop.querySelectorAll('.search-drop__row, .search-drop__product'));
  var titles = [].slice.call(drop.querySelectorAll('.search-drop__title'));
  var emptyRow = document.createElement('div');
  emptyRow.className = 'search-drop__empty';
  emptyRow.hidden = true;
  emptyRow.textContent = 'Ничего не нашли — попробуйте другой запрос';
  drop.insertBefore(emptyRow, drop.firstChild);

  function filterRows() {
    var query = input.value.trim().toLowerCase();
    var shown = 0;
    rows.forEach(function (row) {
      var match = !query || row.textContent.toLowerCase().indexOf(query) !== -1;
      row.hidden = !match;
      if (match) shown++;
    });
    // прячем заголовок группы, если в ней ничего не осталось
    titles.forEach(function (title) {
      var next = title.nextElementSibling, has = false;
      while (next && !next.classList.contains('search-drop__title') && !next.classList.contains('search-drop__all')) {
        if (!next.hidden) has = true;
        next = next.nextElementSibling;
      }
      title.hidden = !has;
    });
    emptyRow.hidden = shown !== 0;
  }

  input.addEventListener('focus', function () { drop.hidden = false; filterRows(); });
  input.addEventListener('input', filterRows);
  document.addEventListener('click', function (e) {
    if (!input.closest('form').contains(e.target)) drop.hidden = true;
  });
  input.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { drop.hidden = true; input.blur(); }
  });
});

// ================= Выбор города =================
document.querySelectorAll('[data-city]').forEach(function (btn) {
  btn.addEventListener('click', function () {
    document.querySelectorAll('[data-city]').forEach(function (b) { b.classList.remove('is-active'); });
    btn.classList.add('is-active');
    document.querySelectorAll('[data-city-name]').forEach(function (out) {
      out.textContent = btn.dataset.city;
    });
    var modal = btn.closest('.modal');
    if (modal) {
      modal.hidden = true;
      document.body.classList.remove('is-locked');
    }
  });
});

// Мегаменю: на тачскрине открываем по тапу, на десктопе работает :hover
document.querySelectorAll('.nav__item > a').forEach(function (link) {
  link.addEventListener('click', function (e) {
    if (!window.matchMedia('(hover: none)').matches) return;
    var item = link.parentElement;
    if (!item.classList.contains('is-open')) {
      e.preventDefault();
      document.querySelectorAll('.nav__item.is-open').forEach(function (i) { i.classList.remove('is-open'); });
      item.classList.add('is-open');
    }
  });
});


// ================= Всплывающие уведомления =================
function showToast(text) {
  var old = document.querySelector('.toast');
  if (old) old.remove();
  var box = document.createElement('div');
  box.className = 'toast';
  box.innerHTML = '<svg class="ico"><use href="#i-check"/></svg> ' + text;
  document.body.appendChild(box);
  setTimeout(function () { box.classList.add('is-hiding'); }, 2900);
  setTimeout(function () { box.remove(); }, 3220);
}

document.addEventListener('click', function (e) {
  var btn = e.target.closest('[data-toast]');
  if (!btn) return;
  if (btn.dataset.toggleActive !== undefined) btn.classList.toggle('is-active');
  showToast(btn.dataset.toast);
  if (btn.dataset.closeModal !== undefined) {
    var modal = btn.closest('.modal');
    if (modal) {
      modal.hidden = true;
      document.body.classList.remove('is-locked');
    }
  }
});

// Оценка звёздами в форме отзыва
document.querySelectorAll('[data-stars]').forEach(function (box) {
  box.querySelectorAll('button').forEach(function (star) {
    star.addEventListener('click', function () {
      var value = parseInt(star.dataset.star, 10);
      box.querySelectorAll('button').forEach(function (s) {
        s.classList.toggle('is-on', parseInt(s.dataset.star, 10) <= value);
      });
    });
  });
});

// ================= Мелкие действия на страницах =================

// Удаление карточки (адрес, товар и т.п.)
document.querySelectorAll('[data-remove-card]').forEach(function (btn) {
  btn.addEventListener('click', function () {
    var card = btn.closest(btn.dataset.removeCard);
    if (card) card.remove();
  });
});

// Сделать адрес основным
document.querySelectorAll('[data-make-main]').forEach(function (btn) {
  btn.addEventListener('click', function () {
    var card = btn.closest('.addr-card');
    document.querySelectorAll('.addr-card').forEach(function (c) { c.classList.remove('addr-card--main'); });
    if (card) card.classList.add('addr-card--main');
    btn.remove();
  });
});

// Очистить корзину целиком
document.querySelectorAll('[data-cart-clear]').forEach(function (btn) {
  btn.addEventListener('click', function () {
    document.querySelectorAll('.cart-item').forEach(function (item) { item.remove(); });
    var cart = document.querySelector('.cart');
    var empty = document.querySelector('.cart-empty');
    if (cart && empty) { cart.hidden = true; empty.hidden = false; }
  });
});

// Очистить список сравнения
document.querySelectorAll('[data-compare-clear]').forEach(function (btn) {
  btn.addEventListener('click', function () {
    ['.compare-wrap', '.compare-tools', '.chips'].forEach(function (sel) {
      var el = document.querySelector(sel);
      if (el) el.hidden = true;
    });
    var empty = document.querySelector('.empty');
    if (empty) empty.hidden = false;
    if (window.showToast) showToast('Список сравнения очищен');
  });
});

// Фильтр заказов по статусу в личном кабинете
document.querySelectorAll('[data-orders]').forEach(function (chip, _, chips) {
  chip.addEventListener('click', function () {
    chips.forEach(function (c) { c.classList.remove('is-active'); });
    chip.classList.add('is-active');
    var mode = chip.dataset.orders;
    var shown = 0;
    document.querySelectorAll('.order').forEach(function (order) {
      var ok = mode === 'all' || order.dataset.status === mode;
      order.hidden = !ok;
      if (ok) shown++;
    });
    var empty = document.querySelector('.acc .empty');
    if (empty) empty.hidden = shown !== 0;
  });
});

// Чипы-переключатели без своей логики (наборы сравнения и т.п.)
document.querySelectorAll('.chips').forEach(function (group) {
  var items = group.querySelectorAll('button.chip:not([data-chip]):not([data-orders])');
  items.forEach(function (chip) {
    chip.addEventListener('click', function () {
      items.forEach(function (c) { c.classList.remove('is-active'); });
      chip.classList.add('is-active');
    });
  });
});

// Кнопка «Добавить в корзину» в карточке товара: счётчик в шапке + уведомление
document.querySelectorAll('button.p-card__btn').forEach(function (btn) {
  btn.addEventListener('click', function () {
    bumpBadge('cart.html', 1);
    showToast('Товар добавлен в корзину');
  });
});


// ================= Дозагрузка товаров на странице скидок =================
(function () {
  var btn = document.querySelector('[data-sale-more-btn]');
  if (!btn) return;
  btn.addEventListener('click', function () {
    var hidden = [].slice.call(document.querySelectorAll('[data-sale-more][hidden]')).slice(0, 4);
    hidden.forEach(function (card, i) {
      card.hidden = false;
      card.classList.add('is-appearing');
      card.style.animationDelay = (i * 60) + 'ms';
    });
    if (!document.querySelector('[data-sale-more][hidden]')) {
      btn.hidden = true;
      if (window.showToast) showToast('Показали все товары со скидкой');
    }
  });
})();

// ================= Избранное: карточка уходит из списка =================
(function () {
  if (!/favorites\.html$/.test(location.pathname)) return;
  document.querySelectorAll('.p-card__fav').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var card = btn.closest('.p-card');
      card.classList.add('is-removing');
      setTimeout(function () {
        card.remove();
        var grid = document.querySelector('.listing__grid');
        var empty = document.querySelector('.empty');
        if (grid && !grid.querySelector('.p-card')) {
          grid.hidden = true;
          if (empty) empty.hidden = false;
        }
      }, 240);
    });
  });
})();


// ================= Кнопка «наверх» =================
(function () {
  var btn = document.querySelector('[data-to-top]');
  if (!btn) return;

  function toggle() {
    var show = window.pageYOffset > 700;
    if (show) {
      btn.hidden = false;
      window.setTimeout(function () { btn.classList.add('is-visible'); }, 10);
    } else {
      btn.classList.remove('is-visible');
      window.setTimeout(function () {
        if (!btn.classList.contains('is-visible')) btn.hidden = true;
      }, 250);
    }
  }

  btn.addEventListener('click', function () {
    try {
      window.scrollTo({ top: 0, behavior: CALM.matches ? 'auto' : 'smooth' });
    } catch (err) {
      window.scrollTo(0, 0);
    }
  });
  window.addEventListener('scroll', toggle, { passive: true });
  window.addEventListener('resize', toggle);
  window.addEventListener('load', toggle);
  toggle();
})();

// ================= Проверка полей перед отправкой формы-заглушки =================
document.querySelectorAll('[data-toast]').forEach(function (btn) {
  btn.addEventListener('click', function (e) {
    var box = btn.closest('form, .co-block, .calc__form, .modal__box, .subscribe, .acc-block');
    if (!box) return;
    var fields = box.querySelectorAll('input[type="tel"], input[type="email"]');
    var bad = null;
    fields.forEach(function (input) {
      var field = input.closest('.field') || input.parentElement;
      var empty = !input.value.trim();
      if (field.classList) field.classList.toggle('is-invalid', empty);
      if (empty && !bad) bad = input;
    });
    if (bad) {
      e.stopImmediatePropagation();
      e.preventDefault();
      bad.focus();
      showToast('Укажите телефон — по нему свяжемся с вами');
    }
  }, true);
});
