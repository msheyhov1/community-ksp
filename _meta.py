#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Мета-теги, иконка сайта и карточка для соцсетей — на всех страницах.

Правим описание здесь, запускаем `python3 _meta.py` — обновится везде.
При натяжке на Битрикс эти же значения переедут в свойства страниц
и в шаблон (title/description задаются в админке для каждого раздела).
"""

import importlib.util
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('catalog_data', ROOT / '_catalog.py')
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)

SITE = 'Комьюнити'
# Боевой домен заказчика. Пока демо живёт на GitHub Pages, но в микроразметке
# нужен абсолютный адрес — при переезде поменять здесь одну строку.
SITE_URL = 'https://community-store.ru'

# Данные организации для микроразметки. Телефон, почта и адреса — из вёрстки;
# ИНН/ОГРН заказчик ещё не прислал, поэтому их в разметке нет.
ORG = {
    'name': 'Комьюнити',
    'phone': '+7 918 840-37-11',
    'email': 'info@community-ksp.ru',
    'hours': 'Mo-Su 09:00-23:00',
    'shops': [
        {'city': 'Каспийск', 'street': 'ул. Ленина, 39', 'zip': '368300',
         'map': 'https://yandex.ru/maps/org/59448092318/'},
        {'city': 'Махачкала', 'street': 'ул. Ярагского, 65а/1', 'zip': '367000',
         'map': None},
    ],
}
# Пока сайт — черновик на демо-адресе, закрываем его от поисковиков.
# Перед запуском на боевом домене поставить False и перезапустить скрипт.
DRAFT = True
DEFAULT = ('Магазин техники Apple в Каспийске и Махачкале: официальная гарантия, '
           'проверка при выдаче, рассрочка без процентов и Trade-In.')

DESCRIPTIONS = {
    'index.html': DEFAULT,
    'catalog.html': 'Каталог техники Apple: iPhone, Mac, iPad, Apple Watch, AirPods и аксессуары '
                    'с гарантией. Самовывоз в день заказа в Каспийске и Махачкале.',
    'search.html': 'Поиск по каталогу техники Apple в магазине «Комьюнити».',
    'cart.html': 'Корзина: проверьте заказ, примените промокод и оформите доставку или самовывоз.',
    'checkout.html': 'Оформление заказа: самовывоз, курьер по Дагестану или СДЭК по России. '
                     'Оплата при получении, по счёту или в рассрочку.',
    'order-success.html': 'Заказ принят — менеджер перезвонит и подтвердит наличие.',
    'account.html': 'Личный кабинет: профиль, заказы, адреса доставки и избранное.',
    'account-orders.html': 'История заказов и их статусы в личном кабинете.',
    'account-addresses.html': 'Адреса доставки и магазины для самовывоза.',
    'favorites.html': 'Избранные товары — вернитесь к ним, когда будете готовы к покупке.',
    'compare.html': 'Сравнение техники Apple по характеристикам и цене.',
    'sale.html': 'Скидки и акции на технику Apple в Каспийске и Махачкале. '
                 'Скидка суммируется с Trade-In и рассрочкой.',
    'trade-in.html': 'Trade-In: меняем старое устройство на новое с доплатой. Оценка за 15 минут, '
                     'калькулятор стоимости на сайте.',
    'installment.html': 'Рассрочка без процентов через Ляриба-Финанс и Хайр. Решение в день заявки, '
                        'по паспорту, калькулятор платежа на сайте.',
    'delivery.html': 'Доставка и оплата: самовывоз в день заказа, курьер по Каспийску и Махачкале, '
                     'СДЭК по России. Наличные и карта при получении, рассрочка, счёт.',
    'about.html': 'О магазине «Комьюнити»: два магазина в Дагестане, свой сервис, официальная техника '
                  'и проверка при выдаче.',
    'contacts.html': 'Контакты: адреса магазинов в Каспийске и Махачкале, телефон, почта и форма обращения.',
    'privacy.html': 'Политика конфиденциальности магазина «Комьюнити».',
    'offer.html': 'Публичная оферта магазина «Комьюнити».',
    '404.html': 'Страница не найдена. Воспользуйтесь поиском или загляните в каталог.',
}

HEAD_BLOCK = '''  <meta name="description" content="{desc}">
  <meta name="robots" content="{robots}">
  <meta name="theme-color" content="#000000">
  <link rel="icon" href="favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="img/apple-touch-icon.png">
  <meta property="og:type" content="{og_type}">
  <meta property="og:site_name" content="{site}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="{image}">
  <meta name="twitter:card" content="summary_large_image">'''


def describe(name):
    """описание для страницы: своё, категорийное или собранное из данных товара"""
    if name in DESCRIPTIONS:
        return DESCRIPTIONS[name], 'website', 'img/og-cover.png'

    for cat in C.CATS:
        if name == f"catalog-{cat['slug']}.html":
            return cat['seo_text'].replace('\n', ' ').strip(), 'website', 'img/og-cover.png'
        for prod in cat['products']:
            if C.page_name(prod) == name:
                price = f'{prod["price"]:,}'.replace(',', ' ')
                stock = 'В наличии' if prod['avail'] == 'stock' else 'Под заказ'
                desc = (f'{prod["name"]} — {price} ₽. {prod["info"]}. {stock} в Каспийске и Махачкале, '
                        f'гарантия 12 месяцев, рассрочка без процентов.')
                return desc, 'product', f'img/{prod["img"]}'
    return DEFAULT, 'website', 'img/og-cover.png'



# ============================ Микроразметка ============================
# Schema.org в формате JSON-LD: поисковики показывают цену, наличие и рейтинг
# прямо в выдаче. При натяжке на Битрикс эти же данные будет отдавать шаблон
# карточки товара из свойств инфоблока.

def _products_index():
    """slug → (товар, категория). Ручная карточка product.html — тоже здесь."""
    index = {}
    for cat in C.CATS:
        for prod in cat['products']:
            index[prod['slug']] = (prod, cat)
    return index


def _brand(name):
    first = name.split()[0]
    return 'Apple' if first == 'Apple' else first


def _ld(data):
    import json
    return ('  <script type="application/ld+json">'
            + json.dumps(data, ensure_ascii=False, separators=(',', ':'))
            + '</script>')


def _org_node():
    return {
        '@type': 'Store',
        '@id': SITE_URL + '/#org',
        'name': ORG['name'],
        'url': SITE_URL + '/',
        'image': SITE_URL + '/img/og-cover.png',
        'logo': SITE_URL + '/img/logo-black.svg',
        'telephone': ORG['phone'],
        'email': ORG['email'],
        'openingHours': ORG['hours'],
        'priceRange': '₽₽',
        'address': [{
            '@type': 'PostalAddress',
            'addressLocality': s['city'],
            'streetAddress': s['street'],
            'postalCode': s['zip'],
            'addressRegion': 'Республика Дагестан',
            'addressCountry': 'RU',
        } for s in ORG['shops']],
    }


def _crumbs(items):
    return {
        '@type': 'BreadcrumbList',
        'itemListElement': [{
            '@type': 'ListItem', 'position': i + 1, 'name': name,
            **({'item': SITE_URL + '/' + url} if url else {}),
        } for i, (name, url) in enumerate(items)],
    }


def jsonld(page_name):
    """Разметка для конкретной страницы. Пусто — если странице она не нужна."""
    index = _products_index()

    if page_name == 'index.html':
        return _ld({'@context': 'https://schema.org', '@graph': [
            _org_node(),
            {'@type': 'WebSite', 'url': SITE_URL + '/', 'name': SITE,
             'inLanguage': 'ru-RU',
             'potentialAction': {
                 '@type': 'SearchAction',
                 'target': {'@type': 'EntryPoint',
                            'urlTemplate': SITE_URL + '/search.html?q={search_term_string}'},
                 'query-input': 'required name=search_term_string'}},
        ]})

    if page_name == 'contacts.html':
        return _ld({'@context': 'https://schema.org', '@graph': [_org_node()]})

    if page_name.startswith('product'):
        slug = ('iphone-16-pro-max-512-peschanyy-titanovyy' if page_name == 'product.html'
                else page_name[len('product-'):-len('.html')])
        found = index.get(slug)
        if not found:
            # у сгенерированных страниц slug обрезан по длине имени файла
            found = next((v for k, v in index.items() if k.startswith(slug)), None)
        if not found:
            return ''
        prod, cat = found
        has_reviews = prod['pop'] >= 85
        product = {
            '@type': 'Product',
            'name': prod['name'],
            'description': prod['info'],
            'image': SITE_URL + '/img/' + prod['img'],
            'sku': C.sku(prod),
            'brand': {'@type': 'Brand', 'name': _brand(prod['name'])},
            'category': C.CAT_NAMES[cat['slug']],
            'offers': {
                '@type': 'Offer',
                'url': SITE_URL + '/' + page_name,
                'price': prod['price'],
                'priceCurrency': 'RUB',
                'availability': ('https://schema.org/InStock' if prod['avail'] == 'stock'
                                 else 'https://schema.org/PreOrder'),
                'itemCondition': 'https://schema.org/NewCondition',
                'seller': {'@id': SITE_URL + '/#org'},
            },
        }
        if has_reviews:
            product['aggregateRating'] = {'@type': 'AggregateRating',
                                          'ratingValue': '5', 'reviewCount': 3, 'bestRating': '5'}
        return _ld({'@context': 'https://schema.org', '@graph': [
            product,
            _crumbs([('Главная', ''), ('Каталог', 'catalog.html'),
                     (C.CAT_NAMES[cat['slug']], f"catalog-{cat['slug']}.html"),
                     (prod['name'], None)]),
        ]})

    if page_name.startswith('catalog-'):
        slug = page_name[len('catalog-'):-len('.html')]
        cat = next((c for c in C.CATS if c['slug'] == slug), None)
        if not cat:
            return ''
        return _ld({'@context': 'https://schema.org', '@graph': [
            _crumbs([('Главная', ''), ('Каталог', 'catalog.html'),
                     (C.CAT_NAMES[slug], None)]),
            {'@type': 'ItemList', 'numberOfItems': len(cat['products']),
             'itemListElement': [{
                 '@type': 'ListItem', 'position': i + 1,
                 'url': SITE_URL + '/product-' + p['slug'] + '.html',
                 'name': p['name'],
             } for i, p in enumerate(cat['products'][:20])]},
        ]})

    if page_name == 'catalog.html':
        return _ld({'@context': 'https://schema.org', '@graph': [
            _crumbs([('Главная', ''), ('Каталог', None)])]})

    return ''


def main():
    pages = sorted(p for p in ROOT.glob('*.html') if not p.name.startswith('_'))
    changed = 0
    marked = 0
    for page in pages:
        text = page.read_text(encoding='utf-8')
        title_match = re.search(r'<title>(.*?)</title>', text, re.S)
        if not title_match:
            print(f'!! {page.name}: нет <title>')
            continue

        desc, og_type, image = describe(page.name)
        desc = re.sub(r'\s+', ' ', desc).strip()
        block = HEAD_BLOCK.format(desc=desc, title=title_match.group(1), site=SITE,
                                  og_type=og_type, image=image,
                                  robots='noindex, nofollow' if DRAFT else 'index, follow')

        # убираем прошлый блок, чтобы не плодить дубли
        text = re.sub(r'\n?  <meta name="description".*?<meta name="twitter:card"[^>]*>', '', text, flags=re.S)
        text = re.sub(r'\n?  <script type="application/ld\+json">.*?</script>', '', text, flags=re.S)
        ld = jsonld(page.name)
        if ld:
            block = block + '\n' + ld
            marked += 1
        text = text.replace('</title>', '</title>\n' + block, 1)
        page.write_text(text, encoding='utf-8')
        changed += 1
    print(f'мета-теги проставлены: {changed} страниц, микроразметка: {marked}')


if __name__ == '__main__':
    main()
