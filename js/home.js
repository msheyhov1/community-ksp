// Community KSP — главная: герой-слайдер и карусель подборки.

// ================= Герой =================
(function () {
  var hero = document.querySelector('.hero');
  var dotsBox = document.querySelector('[data-hero-dots]');
  if (!hero || !dotsBox) return;

  var titleOut = hero.querySelector('[data-hero-title]');
  var subtitleOut = hero.querySelector('[data-hero-subtitle]');
  var btnOut = hero.querySelector('[data-hero-btn]');
  var imgOut = hero.querySelector('[data-hero-img]');
  var dots = [].slice.call(dotsBox.querySelectorAll('i'));

  // Первый слайд повторяет макет — его стили заданы в CSS и не переопределяются.
  var slides = [
    { title: 'iPhone 16', subtitle: 'Привет, Apple&nbsp;Intelligence',
      btn: 'Подробнее', href: 'catalog-iphone.html', img: 'img/p-16pm-desert.png', style: null },
    { title: 'Trade-In', subtitle: 'Меняем старое устройство на новое',
      btn: 'Узнать оценку', href: 'trade-in.html', img: 'img/p-16pm-natural.png', style: null },
    { title: 'Рассрочка 0-0-12', subtitle: 'Без первого взноса и переплаты',
      btn: 'Рассчитать платёж', href: 'installment.html', img: 'img/p-macbook-air.png',
      style: { left: '52%', top: '30%', height: 'auto', width: '46%' } },
    { title: 'Скидки недели', subtitle: 'До −15% на технику Apple',
      btn: 'Смотреть акции', href: 'sale.html', img: 'img/p-ipad-pro-dark.png',
      style: { left: '54%', top: '14%', height: '96%', width: 'auto' } }
  ];

  var current = 0;
  var timer = null;
  var DELAY = 6000;

  function show(index) {
    index = (index + slides.length) % slides.length;
    if (index === current) return;
    current = index;
    var slide = slides[index];

    hero.classList.add('is-changing');
    setTimeout(function () {
      titleOut.innerHTML = slide.title;
      subtitleOut.innerHTML = slide.subtitle;
      btnOut.textContent = slide.btn;
      btnOut.setAttribute('href', slide.href);
      imgOut.src = slide.img;
      imgOut.alt = slide.title;
      imgOut.style.cssText = '';
      if (slide.style) {
        Object.keys(slide.style).forEach(function (key) { imgOut.style[key] = slide.style[key]; });
      }
      hero.classList.remove('is-changing');
    }, 320);

    dots.forEach(function (dot, i) {
      dot.classList.toggle('is-active', i === index);
      dot.setAttribute('aria-current', i === index ? 'true' : 'false');
    });
  }

  function play() {
    stop();
    timer = setInterval(function () { show(current + 1); }, DELAY);
  }
  function stop() {
    if (timer) clearInterval(timer);
    timer = null;
  }

  dots.forEach(function (dot, i) {
    dot.addEventListener('click', function () { show(i); play(); });
    dot.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); show(i); play(); }
      if (e.key === 'ArrowRight') show(current + 1);
      if (e.key === 'ArrowLeft') show(current - 1);
    });
  });

  hero.addEventListener('mouseenter', stop);
  hero.addEventListener('mouseleave', play);
  hero.addEventListener('focusin', stop);

  // свайп на телефоне
  var startX = null;
  hero.addEventListener('touchstart', function (e) { startX = e.touches[0].clientX; stop(); }, { passive: true });
  hero.addEventListener('touchend', function (e) {
    if (startX === null) return;
    var delta = e.changedTouches[0].clientX - startX;
    if (Math.abs(delta) > 40) show(current + (delta < 0 ? 1 : -1));
    startX = null;
    play();
  });

  // не крутим, если вкладка скрыта или пользователь просил меньше анимации
  var calm = window.matchMedia('(prefers-reduced-motion: reduce)');
  document.addEventListener('visibilitychange', function () {
    document.hidden || calm.matches ? stop() : play();
  });
  if (!calm.matches) play();
})();

// ================= Карусель подборки =================
// Сетка не трогается — стрелки перелистывают карточки постранично.
(function () {
  var track = document.querySelector('[data-carousel]');
  if (!track) return;

  var cards = [].slice.call(track.querySelectorAll('.p-card'));
  var prev = document.querySelector('[data-carousel-prev]');
  var next = document.querySelector('[data-carousel-next]');
  var page = 0;

  function perPage() {
    var columns = getComputedStyle(track).gridTemplateColumns.split(' ').filter(Boolean).length;
    return Math.max(1, columns);
  }

  function render(direction) {
    var size = perPage();
    var pages = Math.max(1, Math.ceil(cards.length / size));
    if (page > pages - 1) page = pages - 1;
    if (page < 0) page = 0;

    cards.forEach(function (card, i) {
      var visible = i >= page * size && i < (page + 1) * size;
      card.hidden = !visible;
      if (visible && direction) {
        card.classList.remove('is-slide-left', 'is-slide-right');
        void card.offsetWidth;
        card.classList.add(direction > 0 ? 'is-slide-left' : 'is-slide-right');
      }
    });

    if (prev) prev.disabled = page === 0;
    if (next) next.disabled = page >= pages - 1;
  }

  if (prev) prev.addEventListener('click', function () { page -= 1; render(-1); });
  if (next) next.addEventListener('click', function () { page += 1; render(1); });
  window.addEventListener('resize', function () { render(0); });

  render(0);
})();
