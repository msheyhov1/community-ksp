// Community KSP — корзина: пересчёт сумм при изменении количества,
// удалении позиций и вводе промокода.

(function () {
  var list = document.querySelector('.cart__list');
  if (!list) return;

  var PROMO = { 'community': 3, 'дагестан': 5, 'apple': 3 };   // код → скидка, %
  var promoPercent = 0;
  var promoCode = '';

  var out = {
    count: document.querySelector('[data-cart-count]'),
    subtotal: document.querySelector('[data-cart-subtotal]'),
    discount: document.querySelector('[data-cart-discount]'),
    discountRow: document.querySelector('[data-cart-discount-row]'),
    promo: document.querySelector('[data-cart-promo]'),
    promoRow: document.querySelector('[data-cart-promo-row]'),
    promoCode: document.querySelector('[data-cart-promo-code]'),
    total: document.querySelector('[data-cart-total]'),
    installment: document.querySelector('[data-cart-installment]')
  };

  function money(value) {
    return Math.round(value).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ') + ' ₽';
  }

  function plural(n) {
    return n + ' ' + (n % 10 === 1 && n % 100 !== 11 ? 'шт.' : 'шт.');
  }

  function recalc() {
    var items = [].slice.call(list.querySelectorAll('.cart-item'));
    var count = 0, subtotal = 0, discount = 0, total = 0;

    items.forEach(function (item) {
      var qty = parseInt(item.querySelector('.qty input').value, 10) || 1;
      var price = parseInt(item.dataset.price, 10) || 0;
      var old = parseInt(item.dataset.old, 10) || price;

      count += qty;
      subtotal += old * qty;
      discount += (old - price) * qty;
      total += price * qty;

      var priceOut = item.querySelector('[data-item-price]');
      var oldOut = item.querySelector('[data-item-old]');
      if (priceOut) priceOut.textContent = money(price * qty);
      if (oldOut) oldOut.textContent = money(old * qty);
    });

    var promo = Math.round(total * promoPercent / 100);
    total -= promo;

    if (out.count) out.count.textContent = plural(count);
    if (out.subtotal) out.subtotal.textContent = money(subtotal);
    if (out.discount) out.discount.textContent = '−' + money(discount);
    if (out.discountRow) out.discountRow.hidden = discount === 0;
    if (out.promoRow) out.promoRow.hidden = promo === 0;
    if (out.promo) out.promo.textContent = '−' + money(promo);
    if (out.promoCode) out.promoCode.textContent = promoCode ? '«' + promoCode.toUpperCase() + '»' : '';
    if (out.total) out.total.textContent = money(total);
    if (out.installment) out.installment.textContent = money(total / 12);

    // счётчик в шапке
    var badge = document.querySelector('.header__icons a[href="cart.html"] .header__badge');
    if (badge) {
      badge.textContent = count;
      badge.hidden = count === 0;
    }

    // корзина опустела
    if (!items.length) {
      var cart = document.querySelector('.cart');
      var empty = document.querySelector('.cart-empty');
      if (cart && empty) { cart.hidden = true; empty.hidden = false; }
    }
  }

  // количество и удаление уже обрабатываются в main.js — здесь только пересчёт
  list.addEventListener('change', recalc);
  list.addEventListener('input', recalc);
  list.addEventListener('click', function (e) {
    if (e.target.closest('[data-qty], [data-cart-remove]')) setTimeout(recalc, 0);
  });
  document.querySelectorAll('[data-cart-clear]').forEach(function (btn) {
    btn.addEventListener('click', function () { setTimeout(recalc, 0); });
  });

  // промокод
  var form = document.querySelector('[data-promo-form]');
  if (form) {
    var input = form.querySelector('[data-promo-input]');
    var hint = document.querySelector('[data-promo-hint]');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var code = input.value.trim().toLowerCase();
      if (!code) {
        hint.hidden = false;
        hint.className = 'promo-hint is-error';
        hint.textContent = 'Введите промокод';
        return;
      }
      if (PROMO[code]) {
        promoPercent = PROMO[code];
        promoCode = code;
        hint.hidden = false;
        hint.className = 'promo-hint is-ok';
        hint.textContent = 'Промокод применён: скидка ' + promoPercent + '%';
        input.value = '';
        recalc();
        if (window.showToast) showToast('Промокод применён: скидка ' + promoPercent + '%');
      } else {
        hint.hidden = false;
        hint.className = 'promo-hint is-error';
        hint.textContent = 'Такого промокода нет. Попробуйте COMMUNITY';
      }
    });
  }

  recalc();
})();
