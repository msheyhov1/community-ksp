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
# Пока сайт — черновик на демо-адресе, закрываем его от поисковиков.
# Перед запуском на боевом домене поставить False и перезапустить скрипт.
DRAFT = True
DEFAULT = ('Магазин техники Apple в Каспийске и Махачкале: официальная гарантия, '
           'проверка при выдаче, рассрочка 0-0-12 и Trade-In.')

DESCRIPTIONS = {
    'index.html': DEFAULT,
    'catalog.html': 'Каталог техники Apple: iPhone, Mac, iPad, Apple Watch, AirPods и аксессуары '
                    'с гарантией. Самовывоз в день заказа в Каспийске и Махачкале.',
    'search.html': 'Поиск по каталогу техники Apple в магазине «Комьюнити».',
    'cart.html': 'Корзина: проверьте заказ, примените промокод и оформите доставку или самовывоз.',
    'checkout.html': 'Оформление заказа: самовывоз, курьер по Дагестану или СДЭК по России. '
                     'Оплата картой, наличными или в рассрочку.',
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
    'installment.html': 'Рассрочка 0-0-12 без первого взноса и переплаты. Решение банка за 2 минуты '
                        'по паспорту, калькулятор платежа на сайте.',
    'delivery.html': 'Доставка и оплата: самовывоз в день заказа, курьер по Каспийску и Махачкале, '
                     'СДЭК по России. Карта, наличные, рассрочка и кредит.',
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
                        f'гарантия 12 месяцев, рассрочка 0-0-12.')
                return desc, 'product', f'img/{prod["img"]}'
    return DEFAULT, 'website', 'img/og-cover.png'


def main():
    pages = sorted(p for p in ROOT.glob('*.html') if not p.name.startswith('_'))
    changed = 0
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
        text = text.replace('</title>', '</title>\n' + block, 1)
        page.write_text(text, encoding='utf-8')
        changed += 1
    print(f'мета-теги проставлены: {changed} страниц')


if __name__ == '__main__':
    main()
