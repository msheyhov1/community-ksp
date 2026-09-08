#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генератор карточек товара: по странице на каждую позицию каталога.

Данные берутся из _catalog.py, поэтому цены и характеристики на листинге
и в карточке всегда совпадают.

    python3 _product.py && python3 _build.py
"""

import importlib.util
import html
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('catalog_data', ROOT / '_catalog.py')
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)

CAT_NAMES = {'iphone': 'iPhone', 'mac': 'Mac', 'ipad': 'iPad', 'watch': 'Apple Watch',
             'airpods': 'AirPods', 'accessories': 'Аксессуары', 'powerbanks': 'Павербанки',
             'docks': 'Док-станции'}

# ракурсы для смартфонов — других фото у нас пока нет
IPHONE_VIEWS = ['g-side.png', 'g-camera.png', 'g-back.png']

INTRO = {
    'iphone': 'Смартфон с гарантией производителя. Перед выдачей вскрываем коробку при вас, проверяем '
              'серийный номер и комплектацию, активируем и помогаем перенести данные со старого телефона.',
    'mac': 'Ноутбук с гарантией производителя. Настроим при выдаче, перенесём данные и поможем выбрать '
           'конфигурацию под ваши задачи — от учёбы до монтажа.',
    'ipad': 'Планшет с гарантией производителя. Проверяем и активируем при вас, подберём чехол, '
            'клавиатуру и Apple Pencil.',
    'watch': 'Часы с гарантией производителя. Подберём размер корпуса и ремешок, настроим и свяжем '
             'с вашим iPhone прямо в магазине.',
    'airpods': 'Оригинальные наушники Apple. Проверяем комплектацию и подключение при выдаче, '
               'меняем по гарантии в наших магазинах.',
    'accessories': 'Аксессуар с гарантией. Защитное стекло наклеиваем бесплатно при покупке в магазине.',
    'powerbanks': 'Внешний аккумулятор с гарантией. Подскажем, на сколько зарядов хватит для вашего устройства.',
    'docks': 'Док-станция с гарантией. Поможем подобрать под ваш набор устройств и проверим совместимость.',
}

COMMON_SPECS = [
    ('Гарантия и документы', 'Гарантия', '12 месяцев, официальная'),
    ('', 'Документы', 'Чек и гарантийный талон'),
    ('', 'Страна производителя', 'Китай'),
    ('Покупка', 'Способы оплаты', 'Наличными или картой при получении, рассрочка Ляриба/Хайр, счёт на оплату'),
    ('', 'Получение', 'Самовывоз в Каспийске и Махачкале, курьер, СДЭК по России'),
]

REVIEWS = [
    ('Магомед', '28 августа 2026', 5, 'Брал в Каспийске, при мне вскрыли коробку и проверили комплектацию. '
     'Всё работает как надо, с настройкой помогли на месте.'),
    ('Патимат', '14 августа 2026', 5, 'Оформила в рассрочку, одобрили в тот же день. Консультант подробно '
     'ответил на все вопросы, ничего лишнего не навязывал.'),
]


def money(v):
    return f'{v:,}'.replace(',', ' ') + ' ₽'


def stars(n):
    return ''.join(f'<svg class="ico{" is-on" if i < n else ""}"><use href="#i-star"/></svg>' for i in range(5))


def labels(cat):
    """ключ атрибута → (заголовок группы, {значение: подпись})"""
    out = {}
    for group in cat['filters']:
        out[group['key']] = (group['title'], {v: label for label, v in group['items']})
    return out


def specs_rows(prod, cat):
    rows, names = [], labels(cat)
    first = True
    for key, value in prod['attrs'].items():
        title, values = names.get(key, (key.title(), {}))
        rows.append((cat['h1'] if first else '', title, values.get(value, value)))
        first = False
    rows.append(('', 'Наличие', 'В наличии' if prod['avail'] == 'stock' else 'Под заказ, 2–3 дня'))
    return rows + COMMON_SPECS


def variants(prod, cat):
    """Другие конфигурации той же модели — реальные ссылки на соседние товары."""
    key = list(prod['attrs'].keys())[0]
    base = prod['attrs'][key]
    same = [x for x in cat['products'] if x['attrs'].get(key) == base and x is not prod]
    if not same:
        return ''
    items = '\n'.join(
        f'''            <a class="opt-chip" href="{C.page_name(x)}">{x['name'].replace('Apple ', '')} — {money(x['price'])}</a>'''
        for x in same[:4])
    title = labels(cat).get(key, ('Конфигурация', {}))[0]
    return f'''        <div class="opt-group">
          <div class="opt-group__title">Другие варианты — {title.lower()} «{labels(cat)[key][1].get(base, base)}»</div>
          <div class="opt-group__row opt-group__row--links">
{items}
          </div>
        </div>
'''


def gallery(prod):
    safe_alt = html.escape(prod['name'], quote=True)
    safe_name = prod['img']
    photos = [prod['img']] + (IPHONE_VIEWS if prod['img'].startswith('p-1') and 'macbook' not in prod['img'] else [])
    if len(photos) == 1:
        return '', f'''      <div class="product__photo">
        <img src="img/{safe_name}" alt="{safe_alt}" id="product-photo">
      </div>'''
    thumbs = '\n'.join(
        f'''        <img src="img/{src}" class="{'is-active' if i == 0 else ''}" alt="{safe_alt}, фото {i + 1}">'''
        for i, src in enumerate(photos))
    box = f'''      <div class="product__thumbs">
        <button class="product__thumbs-arrow" type="button" aria-label="Предыдущее фото" data-gallery="prev"><svg class="ico"><use href="#i-chev-l"/></svg></button>
{thumbs}
        <button class="product__thumbs-arrow" type="button" aria-label="Следующее фото" data-gallery="next"><svg class="ico"><use href="#i-chev-r"/></svg></button>
      </div>'''
    photo = f'''      <div class="product__photo">
        <img src="img/{safe_name}" alt="{safe_alt}" id="product-photo">
      </div>'''
    return box, photo


def reviews_block(prod):
    if prod['pop'] < 85:
        return '4,9', 0, '''      <div class="empty" style="padding:40px 20px 20px">
        <svg class="ico"><use href="#i-star"/></svg>
        <div class="empty__title">Отзывов пока нет</div>
        <div class="empty__text">Купили этот товар у нас? Расскажите, как он вам — это поможет другим выбрать</div>
        <button class="btn btn--primary" type="button" data-modal-open="review">Написать отзыв</button>
      </div>'''
    items = '\n'.join(f'''      <article class="review">
        <div class="review__head">
          <span class="rating">{stars(rate)}</span>
          <span class="review__name">{name}</span>
          <span class="review__date">{date}</span>
          <span class="review__badge">Покупка в «Комьюнити»</span>
        </div>
        <div class="review__text">{text}</div>
      </article>''' for name, date, rate, text in REVIEWS)
    head = f'''      <div class="reviews__head">
        <div class="reviews__score">
          <div class="reviews__num">5,0</div>
          <span class="rating">{stars(5)}</span>
          <div class="reviews__count">{len(REVIEWS)} отзыва</div>
        </div>
        <div class="reviews__bars">
          <div class="reviews__bar"><span>5 звёзд</span> <i><span style="width:100%"></span></i> <span>{len(REVIEWS)}</span></div>
          <div class="reviews__bar"><span>4 звезды</span> <i><span style="width:0"></span></i> <span>0</span></div>
        </div>
        <button class="btn btn--primary" type="button" data-modal-open="review">Написать отзыв</button>
      </div>'''
    return '5,0', len(REVIEWS), head + '\n' + items


def similar(prod, cat):
    others = [x for x in cat['products'] if x is not prod][:4]
    return '\n'.join(C.card(x, cat) for x in others)


def page(prod, cat):
    thumbs, photo = gallery(prod)
    rating, review_count = reviews_block(prod)[:2]
    reviews_html = reviews_block(prod)[2]
    price = prod['price']
    old = f'<s>{money(prod["old"])}</s>' if prod['old'] else ''
    stock = ('<svg class="ico"><use href="#i-check"/></svg> В наличии в Каспийске и Махачкале'
             if prod['avail'] == 'stock'
             else '<svg class="ico"><use href="#i-clock"/></svg> Под заказ — привезём за 2–3 дня')

    specs = '\n'.join(f'''      <div class="specs__group">
        <div class="specs__cat">{cat_name}</div>
        <div class="specs__key">{key}</div>
        <div>{value}</div>
      </div>''' for cat_name, key, value in specs_rows(prod, cat))

    tab_count = f' <span class="product-head__code">{review_count}</span>' if review_count else ''
    head_rating = (f'''      <span class="rating">{stars(5)}</span>
      <a class="product-head__link" href="#tab-reviews" data-tab-link="reviews">{rating} · {review_count} отзыва</a>'''
                   if review_count else
                   '''      <a class="product-head__link" href="#tab-reviews" data-tab-link="reviews">Отзывов пока нет</a>''')

    single = ' product--single' if not thumbs else ''
    body = f'''<main>
  <div class="container">
    <nav class="breadcrumbs">
      <a href="index.html"><svg class="ico"><use href="#i-home"/></svg></a>
      <span class="breadcrumbs__sep">›</span>
      <a href="catalog.html">Каталог</a>
      <span class="breadcrumbs__sep">›</span>
      <a href="catalog-{cat['slug']}.html">{CAT_NAMES[cat['slug']]}</a>
      <span class="breadcrumbs__sep">›</span>
      <span>{prod['name']}</span>
    </nav>

    <h1 class="page-title">{prod['name']}</h1>

    <div class="product-head">
{head_rating}
      <span class="product-head__code">Артикул: {prod['slug'][:14].upper()}</span>
    </div>

    <div class="product{single}">
{thumbs}
{photo}
      <div class="product__opts">
        <div class="opt-group">
          <div class="opt-group__title">Коротко о товаре</div>
          <div class="product__summary">{prod['info']}</div>
        </div>
{variants(prod, cat)}
        <div class="product__price">{money(price)} {old}</div>
        <div class="product__stock{'' if prod['avail'] == 'stock' else ' product__stock--order'}">{stock}</div>

        <div class="product__installment-row">
          <svg class="ico"><use href="#i-percent"/></svg>
          <span>Рассрочка без процентов — <b>{money(round(price / 12))}</b> в месяц на 12 месяцев</span>
        </div>

        <div class="product__actions">
          <a href="cart.html" class="btn btn--primary">Добавить в корзину</a>
          <button class="btn btn--outline" type="button" data-modal-open="oneclick">Купить в один клик</button>
        </div>

        <div class="product__extra">
          <button type="button" data-toggle-active data-toast="Добавили в избранное">
            <svg class="ico"><use href="#i-heart"/></svg> В избранное
          </button>
          <button type="button" data-toggle-active data-toast="Товар добавлен к сравнению">
            <svg class="ico"><use href="#i-compare"/></svg> Сравнить
          </button>
          <button type="button" data-toast="Ссылка на товар скопирована">
            <svg class="ico"><use href="#i-send"/></svg> Поделиться
          </button>
        </div>

        <div class="delivery-list">
          <div class="delivery-row">
            <svg class="ico"><use href="#i-store"/></svg>
            <span class="delivery-row__text"><b>Самовывоз сегодня</b> Каспийск, ул. Ленина, 39 · после 14:00</span>
            <span class="delivery-row__price">бесплатно</span>
          </div>
          <div class="delivery-row">
            <svg class="ico"><use href="#i-truck"/></svg>
            <span class="delivery-row__text"><b>Курьером сегодня</b> Каспийск и Махачкала, интервал 2 часа</span>
            <span class="delivery-row__price">300 ₽</span>
          </div>
          <div class="delivery-row">
            <svg class="ico"><use href="#i-box"/></svg>
            <span class="delivery-row__text"><b>СДЭК по России</b> 2–5 дней, оплата по счёту</span>
            <span class="delivery-row__price">от 490 ₽</span>
          </div>
          <div class="delivery-row">
            <svg class="ico"><use href="#i-refresh"/></svg>
            <span class="delivery-row__text"><b>Trade-In</b> сдайте старое устройство и получите скидку</span>
            <span class="delivery-row__price"><a class="link" href="trade-in.html">оценить</a></span>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="tabs">
    <div class="container">
      <div class="tabs__list">
        <div class="tabs__item is-active" data-tab="desc">Описание</div>
        <div class="tabs__item" data-tab="specs">Характеристики</div>
        <div class="tabs__item" data-tab="reviews">Отзывы{tab_count}</div>
      </div>
    </div>
  </div>

  <div class="container">
    <div class="desc" id="tab-desc">
      <h2 style="margin-top:0">{prod['name']}</h2>
      <p>{prod['info']}.</p>
      <p>{INTRO[cat['slug']]}</p>
      <h2>Покупка и гарантия</h2>
      <p>Товар официальный, с гарантией производителя 12 месяцев. Гарантийные случаи принимаем в наших
        магазинах в Каспийске и Махачкале. В течение 14 дней товар надлежащего качества можно вернуть,
        если сохранены упаковка и товарный вид — подробности в <a href="offer.html">договоре оферты</a>.</p>
    </div>

    <div class="specs" id="tab-specs" style="display:none">
{specs}
    </div>

    <div class="reviews" id="tab-reviews" style="display:none">
{reviews_html}
    </div>
  </div>

  <section class="section section--grey">
    <div class="container">
      <div class="section__head">
        <h2 class="section__title">Похожие товары</h2>
        <a class="section__link" href="catalog-{cat['slug']}.html">Все {CAT_NAMES[cat['slug']]} <svg class="ico"><use href="#i-chev-r"/></svg></a>
      </div>
      <div class="products">
{similar(prod, cat)}
      </div>
    </div>
  </section>
</main>

<!-- Купить в один клик -->
<div class="modal" id="modal-oneclick" hidden>
  <div class="modal__overlay" data-modal-close></div>
  <div class="modal__box" role="dialog" aria-modal="true" aria-labelledby="modal-oneclick-title">
    <button class="modal__close" type="button" aria-label="Закрыть" data-modal-close><svg class="ico"><use href="#i-close"/></svg></button>
    <h2 class="modal__title" id="modal-oneclick-title">Купить в один клик</h2>
    <p class="modal__text">Оставьте номер — перезвоним в течение 15 минут, подтвердим наличие и оформим заказ</p>
    <div class="mini-item" style="margin-top:20px">
      <div class="mini-item__photo"><img src="img/{prod['img']}" alt=""></div>
      <div>
        <div class="mini-item__name">{prod['name']}</div>
        <div class="mini-item__meta">{prod['info']}</div>
      </div>
      <div class="mini-item__price">{money(price)}</div>
    </div>
    <label class="field">
      <span class="field__label">Телефон</span>
      <input type="tel" placeholder="+7 (___) ___-__-__">
    </label>
    <button class="btn btn--primary btn--block" type="button" data-toast="Заявка отправлена, перезвоним в течение 15 минут" data-close-modal>Жду звонка</button>
    <p class="modal__note">Нажимая кнопку, вы соглашаетесь с <a href="privacy.html">политикой конфиденциальности</a></p>
  </div>
</div>

<!-- Написать отзыв -->
<div class="modal" id="modal-review" hidden>
  <div class="modal__overlay" data-modal-close></div>
  <div class="modal__box" role="dialog" aria-modal="true" aria-labelledby="modal-review-title">
    <button class="modal__close" type="button" aria-label="Закрыть" data-modal-close><svg class="ico"><use href="#i-close"/></svg></button>
    <h2 class="modal__title" id="modal-review-title">Ваш отзыв</h2>
    <p class="modal__text">Расскажите, как вам устройство и покупка — это помогает другим выбрать</p>
    <div class="field">
      <span class="field__label">Оценка</span>
      <div class="stars-input" data-stars>
        <button type="button" class="is-on" data-star="1"><svg class="ico"><use href="#i-star"/></svg></button>
        <button type="button" class="is-on" data-star="2"><svg class="ico"><use href="#i-star"/></svg></button>
        <button type="button" class="is-on" data-star="3"><svg class="ico"><use href="#i-star"/></svg></button>
        <button type="button" class="is-on" data-star="4"><svg class="ico"><use href="#i-star"/></svg></button>
        <button type="button" class="is-on" data-star="5"><svg class="ico"><use href="#i-star"/></svg></button>
      </div>
    </div>
    <label class="field">
      <span class="field__label">Имя</span>
      <input type="text" placeholder="Как вас зовут">
    </label>
    <label class="field">
      <span class="field__label">Отзыв</span>
      <textarea placeholder="Что понравилось, что нет"></textarea>
    </label>
    <button class="btn btn--primary btn--block" type="button" data-toast="Спасибо! Отзыв появится после модерации" data-close-modal>Отправить отзыв</button>
  </div>
</div>
'''
    title = html.escape(f"{prod['name']} — купить в Каспийске и Махачкале | Комьюнити", quote=True)
    return C.HEAD.format(title=title) + body + C.FOOT.replace(
        '<script src="js/main.js"></script>',
        '<script src="js/main.js"></script>\n<script src="js/product.js"></script>')


def main():
    made = 0
    for cat in C.CATS:
        for prod in cat['products']:
            if prod['slug'] in C.HAND_MADE:
                continue          # карточка собрана вручную, не трогаем
            (ROOT / C.page_name(prod)).write_text(page(prod, cat), encoding='utf-8')
            made += 1
    print(f'карточек товара собрано: {made}')


if __name__ == '__main__':
    main()
