// Community KSP — оформление заказа: пересчёт итога от способа получения,
// связка «оплата при получении ↔ доставка», проверка обязательных полей.

(function () {
  var form = document.querySelector('.co');
  if (!form) return;

  var GOODS = 343970;      // товары по обычной цене
  var DISCOUNT = 10000;    // скидка по акции

  var deliveryList = document.querySelector('[data-group="delivery"]');
  var payList = document.querySelector('[data-group="pay"]');
  var out = {
    name: document.querySelector('[data-co-delivery-name]'),
    price: document.querySelector('[data-co-delivery]'),
    total: document.querySelector('[data-co-total]'),
    installment: document.querySelector('[data-co-installment]')
  };

  function money(v) {
    return Math.round(v).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ') + ' ₽';
  }

  function active(list) {
    return list ? list.querySelector('.radio-card.is-active') || list.querySelector('.radio-card') : null;
  }

  function recalc() {
    var delivery = active(deliveryList);
    var pay = active(payList);
    var cost = delivery ? parseInt(delivery.dataset.price, 10) || 0 : 0;
    var total = GOODS - DISCOUNT + cost;

    if (out.name) out.name.textContent = delivery ? delivery.dataset.label : 'Получение';
    if (out.price) out.price.textContent = cost ? money(cost) : 'бесплатно';
    if (out.total) out.total.textContent = money(total);

    // рассрочку показываем только когда она выбрана
    if (out.installment) {
      var isInstallment = pay && pay.dataset.extra === 'installment';
      out.installment.hidden = !isInstallment;
      if (isInstallment) {
        out.installment.textContent = '12 платежей по ' + money(total / 12) + ' — первый через месяц';
      }
    }

    // СДЭК оплачивается только онлайн: гасим «картой при получении»
    if (payList && delivery) {
      var allowOnsite = delivery.dataset.payonsite === '1';
      payList.querySelectorAll('[data-needs-onsite]').forEach(function (card) {
        card.classList.toggle('is-disabled', !allowOnsite);
        var input = card.querySelector('input');
        if (input) input.disabled = !allowOnsite;
        var note = card.querySelector('.radio-card__note');
        if (!allowOnsite && !note) {
          note = document.createElement('span');
          note.className = 'radio-card__note';
          note.textContent = 'Недоступно для доставки по России — оплата только онлайн';
          card.querySelector('.radio-card__body').appendChild(note);
        } else if (allowOnsite && note) {
          note.remove();
        }
        // если способ был выбран, а стал недоступен — переключаем на онлайн
        if (!allowOnsite && card.classList.contains('is-active')) {
          card.classList.remove('is-active');
          var online = payList.querySelector('[data-extra="online"]');
          if (online) {
            online.classList.add('is-active');
            var radio = online.querySelector('input');
            if (radio) radio.checked = true;
          }
        }
      });
    }
  }

  [deliveryList, payList].forEach(function (list) {
    if (list) list.addEventListener('click', function () { setTimeout(recalc, 0); });
  });

  // проверка обязательных полей перед переходом на «заказ принят»
  var submit = document.querySelector('[data-co-submit]');
  if (submit) {
    submit.addEventListener('click', function (e) {
      var bad = null;
      document.querySelectorAll('[data-required]').forEach(function (input) {
        var field = input.closest('.field');
        var empty = !input.value.trim();
        field.classList.toggle('is-invalid', empty);
        var hint = field.querySelector('.field__error');
        if (empty && !hint) {
          hint = document.createElement('span');
          hint.className = 'field__error';
          hint.textContent = input.dataset.required;
          field.appendChild(hint);
        } else if (!empty && hint) {
          hint.remove();
        }
        if (empty && !bad) bad = input;
      });
      if (bad) {
        e.preventDefault();
        bad.focus();
        bad.closest('.co-block').scrollIntoView({ behavior: 'smooth', block: 'center' });
        if (window.showToast) showToast('Заполните обязательные поля');
      }
    });
  }

  document.querySelectorAll('[data-required]').forEach(function (input) {
    input.addEventListener('input', function () {
      if (input.value.trim()) {
        var field = input.closest('.field');
        field.classList.remove('is-invalid');
        var hint = field.querySelector('.field__error');
        if (hint) hint.remove();
      }
    });
  });

  recalc();
})();
