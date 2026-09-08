// Community KSP — карточка товара: галерея и выбор конфигурации.
// При натяжке на Битрикс данные о вариантах отдаёт компонент catalog.element,
// разметка и классы остаются теми же.

(function () {
  var photo = document.getElementById('product-photo');
  if (!photo) return;

  var thumbs = [].slice.call(document.querySelectorAll('.product__thumbs img'));
  var colors = [].slice.call(document.querySelectorAll('.opt-color'));
  var memories = [].slice.call(document.querySelectorAll('[data-memory]'));
  var sims = [].slice.call(document.querySelectorAll('[data-sim]'));

  var priceOut = document.querySelector('[data-product-price]');
  var oldOut = document.querySelector('[data-product-old]');
  var payOut = document.querySelector('[data-product-installment]');
  var skuOut = document.querySelector('[data-product-sku]');
  var titleOuts = [].slice.call(document.querySelectorAll('[data-product-title]'));

  function money(value) {
    return Math.round(value).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ') + ' ₽';
  }

  function active(list) {
    return list.filter(function (el) { return el.classList.contains('is-active'); })[0] || list[0];
  }

  // ---------- галерея ----------

  function setPhoto(src, thumb) {
    if (photo.getAttribute('src') === src) return;
    photo.classList.add('is-swapping');
    setTimeout(function () {
      photo.src = src;
      photo.classList.remove('is-swapping');
    }, 140);
    thumbs.forEach(function (t) { t.classList.toggle('is-active', t === thumb); });
  }

  thumbs.forEach(function (thumb) {
    thumb.addEventListener('click', function () { setPhoto(thumb.src, thumb); });
  });

  document.querySelectorAll('[data-gallery]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var current = thumbs.indexOf(active(thumbs));
      var step = btn.dataset.gallery === 'next' ? 1 : -1;
      var next = (current + step + thumbs.length) % thumbs.length;
      setPhoto(thumbs[next].src, thumbs[next]);
    });
  });

  // ---------- выбор конфигурации ----------

  function refresh() {
    var color = active(colors);
    var memory = active(memories);
    var sim = active(sims);

    var price = parseInt(memory.dataset.price, 10);
    var old = parseInt(memory.dataset.old, 10);

    if (priceOut) priceOut.textContent = money(price);
    if (oldOut) oldOut.textContent = money(old);
    if (payOut) payOut.textContent = money(price / 12);

    var name = memory.dataset.memory + ', ' + color.dataset.color;
    titleOuts.forEach(function (out) { out.textContent = name; });

    if (skuOut) {
      var colorCode = { 'песчаный титановый': 'DT', 'натуральный титановый': 'NT',
                        'чёрный титановый': 'BT', 'белый титановый': 'WT' }[color.dataset.color] || 'XX';
      var sizeCode = { '1 ТБ': '1024', '512 ГБ': '512', '256 ГБ': '256', '128 ГБ': '128' }[memory.dataset.memory] || '';
      // формат тот же, что у остальных карточек (см. sku() в _catalog.py)
      skuOut.textContent = 'CK-IPM-16-' + sizeCode + '-' + colorCode;
    }

    document.title = 'Apple iPhone 16 Pro Max ' + name + ' — купить | Комьюнити';
    if (sim) document.querySelectorAll('[data-product-sim]').forEach(function (out) {
      out.textContent = sim.dataset.sim;
    });
  }

  [colors, memories, sims].forEach(function (group) {
    group.forEach(function (option) {
      option.addEventListener('click', function () {
        group.forEach(function (o) { o.classList.remove('is-active'); });
        option.classList.add('is-active');
        if (option.dataset.photo) {
          thumbs[0].src = option.dataset.photo;
          setPhoto(option.dataset.photo, thumbs[0]);
        }
        refresh();
      });
    });
  });

  refresh();
})();
