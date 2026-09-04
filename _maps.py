#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ссылки на Яндекс.Карты для адресов магазинов.

Все адреса на сайте помечены атрибутом data-map="<магазин>".
Здесь лежат сами ссылки — поменяли строку, запустили скрипт,
и адрес обновился на всех страницах сразу:

    python3 _maps.py

Каспийск — постоянная ссылка на карточку организации (oid 59448092318).
Короткие ссылки вида yandex.ru/maps/-/XXXXXXXX Яндекс выдаёт на каждое
«поделиться» отдельно и со временем может перестать их отдавать,
поэтому используем адрес карточки — он не протухает.
Координаты точки: 42.899783, 47.627239 (широта, долгота).

Махачкала — ПОКА поиск по адресу: карточки организации в Яндексе ещё нет.
Когда магазин добавят — вставьте сюда короткую ссылку вида
https://yandex.ru/maps/-/XXXXXXXX и запустите скрипт.
"""

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent

MAPS = {
    'kaspiysk': 'https://yandex.ru/maps/org/59448092318/',
    'mahachkala': 'https://yandex.ru/maps/?text=Дагестан,%20Махачкала,%20улица%20Ярагского,%2065а/1',
}


def retarget(text):
    """Проставляет href всем ссылкам с data-map, в любом порядке атрибутов."""
    changed = 0

    def fix(m):
        nonlocal changed
        tag, store = m.group(0), m.group('store')
        url = MAPS.get(store)
        if not url:
            sys.exit(f'нет ссылки для магазина: {store}')
        new = re.sub(r'href="[^"]*"', f'href="{url}"', tag)
        if new != tag:
            changed += 1
        return new

    pattern = re.compile(r'<a[^>]*data-map="(?P<store>[^"]+)"[^>]*>')
    return pattern.sub(fix, text), changed


def main():
    pages = sorted(p for p in ROOT.glob('*.html'))
    total = 0
    for page in pages:
        src = page.read_text(encoding='utf-8')
        out, n = retarget(src)
        if n:
            page.write_text(out, encoding='utf-8')
            print(f'✓ {page.name}: обновлено ссылок — {n}')
        total += n
    print(f'\nвсего обновлено: {total}')
    for store, url in MAPS.items():
        print(f'  {store}: {url}')


if __name__ == '__main__':
    main()
