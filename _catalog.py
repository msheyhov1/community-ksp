#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генератор страниц каталога.

Данные разделов и товаров лежат здесь же — из них собираются
catalog.html (витрина разделов) и catalog-<раздел>.html (листинги).
Разметка карточек и фильтров та же, что руками; data-атрибуты нужны
скрипту js/catalog.js, при натяжке на Битрикс их отдаёт компонент.

    python3 _catalog.py && python3 _build.py
"""

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent


import unicodedata

TRANSLIT = {'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ё':'e','ж':'zh','з':'z','и':'i','й':'y',
            'к':'k','л':'l','м':'m','н':'n','о':'o','п':'p','р':'r','с':'s','т':'t','у':'u','ф':'f',
            'х':'h','ц':'c','ч':'ch','ш':'sh','щ':'sch','ъ':'','ы':'y','ь':'','э':'e','ю':'yu','я':'ya'}


def slugify(text):
    out = []
    for ch in text.lower():
        if ch in TRANSLIT:
            out.append(TRANSLIT[ch])
        elif ch.isalnum():
            out.append(ch)
        elif ch in ' -/':
            out.append('-')
    slug = re.sub(r'-+', '-', ''.join(out)).strip('-')
    for extra in ('apple-', '-gb', '-tb'):
        slug = slug.replace(extra, '-' if extra.startswith('-') else '')
    return re.sub(r'-+', '-', slug).strip('-')[:48]


def p(name, img, price, attrs, pop, info, old=None, new=0, avail='stock', badge=None):
    return dict(name=name, img=img, price=price, old=old, attrs=attrs, pop=pop,
                info=info, new=new, avail=avail, badge=badge, slug=slugify(name))


CATS = [
    dict(
        slug='iphone', h1='iPhone',
        title='iPhone — купить в Каспийске и Махачкале | Комьюнити',
        chips=[('iPhone 16 Pro Max', 'model:16pm'), ('iPhone 16 Pro', 'model:16p'),
               ('iPhone 16', 'model:16'), ('iPhone 15', 'model:15'), ('iPhone 14', 'model:14')],
        filters=[
            dict(title='Модель', key='model', items=[
                ('iPhone 16 Pro Max', '16pm'), ('iPhone 16 Pro', '16p'), ('iPhone 16', '16'),
                ('iPhone 15', '15'), ('iPhone 14', '14')]),
            dict(title='Память', key='memory', items=[
                ('512 ГБ', '512'), ('256 ГБ', '256'), ('128 ГБ', '128')]),
            dict(title='Цвет', key='color', items=[
                ('Чёрный', 'black'), ('Белый', 'white'), ('Титановый', 'natural'),
                ('Песчаный', 'beige'), ('Бирюзовый', 'teal'), ('Ультрамарин', 'blue'),
                ('Розовый', 'pink')]),
            dict(title='SIM-карта', key='sim', items=[
                ('nano-SIM + eSIM', 'esim'), ('Две nano-SIM', 'dual')]),
            dict(title='Наличие', key='avail', items=[
                ('В наличии', 'stock'), ('Под заказ', 'order')]),
        ],
        seo_title='iPhone в Каспийске и Махачкале',
        seo_text='Официальные iPhone с гарантией 12 месяцев. Проверяем каждое устройство при вас, '
                 'помогаем перенести данные и оформляем рассрочку 0-0-12 без переплаты. '
                 'Забрать можно в день заказа в Каспийске или Махачкале.',
        products=[
            p('Apple iPhone 16 Pro Max 512 ГБ, песчаный титановый', 'p-16pm-desert.png', 149990,
              dict(model='16pm', memory='512', color='beige', sim='esim'), 98,
              '6,9" · A18 Pro · 3 камеры 48 Мп · титан', old=159990, new=9),
            p('Apple iPhone 16 Pro Max 256 ГБ, натуральный титановый', 'p-16pm-natural.png', 139990,
              dict(model='16pm', memory='256', color='natural', sim='esim'), 95,
              '6,9" · A18 Pro · 3 камеры 48 Мп · титан', new=9),
            p('Apple iPhone 16 Pro Max 256 ГБ, чёрный титановый', 'p-16pm-black.png', 139990,
              dict(model='16pm', memory='256', color='black', sim='esim'), 93,
              '6,9" · A18 Pro · 3 камеры 48 Мп · титан', new=9),
            p('Apple iPhone 16 Pro Max 512 ГБ, белый титановый', 'p-16pm-white.png', 149990,
              dict(model='16pm', memory='512', color='white', sim='dual'), 88,
              '6,9" · A18 Pro · 3 камеры 48 Мп · титан', new=8, avail='order'),
            p('Apple iPhone 16 Pro 256 ГБ, натуральный титановый', 'p-15pro-natural.png', 129990,
              dict(model='16p', memory='256', color='natural', sim='esim'), 90,
              '6,3" · A18 Pro · 3 камеры 48 Мп · титан', new=8),
            p('Apple iPhone 16 128 ГБ, бирюзовый', 'p-16-teal.png', 79990,
              dict(model='16', memory='128', color='teal', sim='esim'), 86,
              '6,1" · A18 · 2 камеры 48 Мп · алюминий', new=7),
            p('Apple iPhone 16 256 ГБ, ультрамарин', 'p-16-ultramarine.png', 89990,
              dict(model='16', memory='256', color='blue', sim='esim'), 84,
              '6,1" · A18 · 2 камеры 48 Мп · алюминий', new=7),
            p('Apple iPhone 16 128 ГБ, розовый', 'p-16-pink.png', 79990,
              dict(model='16', memory='128', color='pink', sim='dual'), 78,
              '6,1" · A18 · 2 камеры 48 Мп · алюминий', new=7),
            p('Apple iPhone 16 256 ГБ, белый', 'p-16-white.png', 89990,
              dict(model='16', memory='256', color='white', sim='esim'), 80,
              '6,1" · A18 · 2 камеры 48 Мп · алюминий', new=7),
            p('Apple iPhone 15 128 ГБ, чёрный', 'p-15-black.png', 69990,
              dict(model='15', memory='128', color='black', sim='esim'), 72,
              '6,1" · A16 Bionic · 2 камеры 48 Мп', old=74990, new=5),
            p('Apple iPhone 14 128 ГБ, синий', 'p-14-blue.png', 56990,
              dict(model='14', memory='128', color='blue', sim='dual'), 60,
              '6,1" · A15 Bionic · 2 камеры 12 Мп', new=3, avail='order'),
            p('Apple iPhone 14 128 ГБ, белый', 'p-14-white.png', 56990,
              dict(model='14', memory='128', color='white', sim='esim'), 58,
              '6,1" · A15 Bionic · 2 камеры 12 Мп', new=3),
        ]),

    dict(
        slug='mac', h1='Mac',
        title='MacBook и Mac — купить в Каспийске и Махачкале | Комьюнити',
        chips=[('MacBook Air', 'line:air'), ('MacBook Pro', 'line:pro'),
               ('iMac', 'line:imac'), ('Mac mini', 'line:mini')],
        filters=[
            dict(title='Линейка', key='line', items=[
                ('MacBook Air', 'air'), ('MacBook Pro', 'pro'), ('iMac', 'imac'), ('Mac mini', 'mini')]),
            dict(title='Процессор', key='chip', items=[
                ('M4', 'm4'), ('M4 Pro', 'm4pro'), ('M3', 'm3')]),
            dict(title='Оперативная память', key='ram', items=[
                ('16 ГБ', '16'), ('24 ГБ', '24'), ('32 ГБ', '32')]),
            dict(title='Накопитель', key='ssd', items=[
                ('256 ГБ', '256'), ('512 ГБ', '512'), ('1 ТБ', '1024')]),
            dict(title='Диагональ', key='size', items=[
                ('13"', '13'), ('14"', '14'), ('15"', '15'), ('16"', '16'), ('24"', '24')]),
            dict(title='Наличие', key='avail', items=[
                ('В наличии', 'stock'), ('Под заказ', 'order')]),
        ],
        seo_title='Mac для работы и учёбы',
        seo_text='MacBook Air и Pro, iMac и Mac mini — с гарантией и настройкой при вас. '
                 'Поможем выбрать конфигурацию под задачи: монтаж, разработку, учёбу или офис. '
                 'Для организаций выставляем счёт и отгружаем с полным пакетом документов.',
        products=[
            p('Apple MacBook Air 13" M4, 16 / 256 ГБ, сияющая звезда', 'p-macbook-air.png', 119990,
              dict(line='air', chip='m4', ram='16', ssd='256', size='13'), 96,
              'M4 · 10 ядер GPU · до 18 часов работы', new=9),
            p('Apple MacBook Air 13" M4, 16 / 512 ГБ, полуночный', 'p-macbook-air.png', 134990,
              dict(line='air', chip='m4', ram='16', ssd='512', size='13'), 90,
              'M4 · 10 ядер GPU · до 18 часов работы', new=9),
            p('Apple MacBook Air 15" M4, 16 / 512 ГБ, серебристый', 'tile-mac.png', 154990,
              dict(line='air', chip='m4', ram='16', ssd='512', size='15'), 85,
              'M4 · 15,3" Liquid Retina · 6 динамиков', new=8),
            p('Apple MacBook Pro 14" M4, 16 / 512 ГБ, космический чёрный', 'promo-macbook.png', 189990,
              dict(line='pro', chip='m4', ram='16', ssd='512', size='14'), 92,
              'M4 · Liquid Retina XDR · 120 Гц', new=9),
            p('Apple MacBook Pro 14" M4 Pro, 24 / 512 ГБ', 'promo-macbook.png', 229990,
              dict(line='pro', chip='m4pro', ram='24', ssd='512', size='14'), 80,
              'M4 Pro · 14 ядер CPU · 3 порта Thunderbolt', new=8, avail='order'),
            p('Apple MacBook Pro 16" M4 Pro, 24 / 1 ТБ', 'promo-macbook.png', 279990,
              dict(line='pro', chip='m4pro', ram='24', ssd='1024', size='16'), 76,
              'M4 Pro · 16,2" XDR · до 24 часов работы', new=8, avail='order'),
            p('Apple iMac 24" M4, 16 / 256 ГБ, серебристый', 'tile-mac.png', 159990,
              dict(line='imac', chip='m4', ram='16', ssd='256', size='24'), 68,
              '4,5K Retina · камера 12 Мп · Touch ID', new=7),
            p('Apple Mac mini M4, 16 / 256 ГБ', 'tile-mac.png', 74990,
              dict(line='mini', chip='m4', ram='16', ssd='256'), 74,
              'M4 · компактный корпус · 5 портов', old=79990, new=7),
        ]),

    dict(
        slug='ipad', h1='iPad',
        title='iPad — купить в Каспийске и Махачкале | Комьюнити',
        chips=[('iPad Pro', 'line:pro'), ('iPad Air', 'line:air'),
               ('iPad', 'line:ipad'), ('iPad mini', 'line:mini')],
        filters=[
            dict(title='Линейка', key='line', items=[
                ('iPad Pro', 'pro'), ('iPad Air', 'air'), ('iPad', 'ipad'), ('iPad mini', 'mini')]),
            dict(title='Диагональ', key='size', items=[
                ('13"', '13'), ('11"', '11'), ('8,3"', '8')]),
            dict(title='Память', key='memory', items=[
                ('512 ГБ', '512'), ('256 ГБ', '256'), ('128 ГБ', '128')]),
            dict(title='Связь', key='conn', items=[
                ('Wi-Fi', 'wifi'), ('Wi-Fi + Cellular', 'cellular')]),
            dict(title='Наличие', key='avail', items=[
                ('В наличии', 'stock'), ('Под заказ', 'order')]),
        ],
        seo_title='iPad для работы, учёбы и рисования',
        seo_text='iPad Pro, Air, mini и базовый iPad — подберём диагональ и объём памяти под задачи. '
                 'В наличии аксессуары: Apple Pencil, клавиатуры и чехлы.',
        products=[
            p('Apple iPad Pro 11" M4, 256 ГБ, Wi-Fi', 'p-ipad-pro-dark.png', 104990,
              dict(line='pro', size='11', memory='256', conn='wifi'), 94,
              'M4 · Ultra Retina XDR · 120 Гц', new=9),
            p('Apple iPad Pro 13" M4, 512 ГБ, Wi-Fi', 'p-ipad-pro-dark.png', 149990,
              dict(line='pro', size='13', memory='512', conn='wifi'), 86,
              'M4 · Ultra Retina XDR · 120 Гц', new=9),
            p('Apple iPad Pro 11" M4, 256 ГБ, Wi-Fi + Cellular', 'p-ipad-pro-dark.png', 124990,
              dict(line='pro', size='11', memory='256', conn='cellular'), 78,
              'M4 · eSIM · Ultra Retina XDR', new=8, avail='order'),
            p('Apple iPad Air 11" M3, 128 ГБ, Wi-Fi', 'tile-ipad.png', 69990,
              dict(line='air', size='11', memory='128', conn='wifi'), 88,
              'M3 · Liquid Retina · Touch ID', new=7),
            p('Apple iPad Air 13" M3, 256 ГБ, Wi-Fi + Cellular', 'tile-ipad.png', 99990,
              dict(line='air', size='13', memory='256', conn='cellular'), 72,
              'M3 · eSIM · Liquid Retina', new=7),
            p('Apple iPad 11" A16, 128 ГБ, Wi-Fi', 'tile-ipad.png', 44990,
              dict(line='ipad', size='11', memory='128', conn='wifi'), 82,
              'A16 · Liquid Retina · Apple Pencil', old=49990, new=6),
            p('Apple iPad mini 8,3" A17 Pro, 128 ГБ, Wi-Fi', 'tile-ipad.png', 54990,
              dict(line='mini', size='8', memory='128', conn='wifi'), 70,
              'A17 Pro · компактный · Apple Pencil Pro', new=6),
        ]),

    dict(
        slug='watch', h1='Apple Watch',
        title='Apple Watch — купить в Каспийске и Махачкале | Комьюнити',
        chips=[('Series 10', 'series:s10'), ('SE', 'series:se'), ('Ultra 2', 'series:ultra')],
        filters=[
            dict(title='Серия', key='series', items=[
                ('Series 10', 's10'), ('SE', 'se'), ('Ultra 2', 'ultra')]),
            dict(title='Размер корпуса', key='size', items=[
                ('49 мм', '49'), ('46 мм', '46'), ('44 мм', '44'), ('42 мм', '42'), ('40 мм', '40')]),
            dict(title='Материал корпуса', key='material', items=[
                ('Алюминий', 'alu'), ('Титан', 'titan')]),
            dict(title='Связь', key='conn', items=[
                ('GPS', 'gps'), ('GPS + Cellular', 'cellular')]),
            dict(title='Наличие', key='avail', items=[
                ('В наличии', 'stock'), ('Под заказ', 'order')]),
        ],
        seo_title='Apple Watch для спорта и здоровья',
        seo_text='Series 10, SE и Ultra 2 — с ремешками на выбор. Поможем подобрать размер корпуса '
                 'и настроить часы при покупке.',
        products=[
            p('Apple Watch Series 10 46 мм, титан, чёрный ремешок', 'p-watch10-dark.png', 63990,
              dict(series='s10', size='46', material='titan', conn='cellular'), 92,
              'Титан · Cellular · всегда включённый экран', new=9),
            p('Apple Watch Series 10 46 мм, алюминий, GPS', 'p-watch10-dark.png', 49990,
              dict(series='s10', size='46', material='alu', conn='gps'), 95,
              'Алюминий · GPS · до 18 часов', new=9),
            p('Apple Watch Series 10 42 мм, алюминий, GPS', 'tile-watch.png', 44990,
              dict(series='s10', size='42', material='alu', conn='gps'), 90,
              'Алюминий · GPS · до 18 часов', new=9),
            p('Apple Watch Series 10 42 мм, титан, Cellular', 'tile-watch.png', 59990,
              dict(series='s10', size='42', material='titan', conn='cellular'), 74,
              'Титан · Cellular · сапфировое стекло', new=8, avail='order'),
            p('Apple Watch SE 40 мм, алюминий, GPS', 'tile-watch.png', 24990,
              dict(series='se', size='40', material='alu', conn='gps'), 84,
              'Алюминий · GPS · датчик падения', old=27990, new=5),
            p('Apple Watch SE 44 мм, алюминий, Cellular', 'tile-watch.png', 32990,
              dict(series='se', size='44', material='alu', conn='cellular'), 76,
              'Алюминий · Cellular · датчик падения', new=5),
            p('Apple Watch Ultra 2 49 мм, титан, Cellular', 'p-watch10-dark.png', 99990,
              dict(series='ultra', size='49', material='titan', conn='cellular'), 80,
              'Титан · до 36 часов · глубина 100 м', new=8),
        ]),

    dict(
        slug='airpods', h1='AirPods',
        title='AirPods — купить в Каспийске и Махачкале | Комьюнити',
        chips=[('AirPods 4', 'model:a4'), ('AirPods Pro', 'model:pro'), ('AirPods Max', 'model:max')],
        filters=[
            dict(title='Модель', key='model', items=[
                ('AirPods 4', 'a4'), ('AirPods Pro 2', 'pro'), ('AirPods Max', 'max')]),
            dict(title='Тип', key='type', items=[
                ('Вкладыши', 'in'), ('Полноразмерные', 'over')]),
            dict(title='Шумоподавление', key='anc', items=[
                ('Есть', 'yes'), ('Нет', 'no')]),
            dict(title='Наличие', key='avail', items=[
                ('В наличии', 'stock'), ('Под заказ', 'order')]),
        ],
        seo_title='AirPods с гарантией',
        seo_text='Оригинальные наушники Apple: AirPods 4, Pro 2 и Max. Проверяем комплектацию '
                 'и подключение при вас, меняем по гарантии в наших магазинах.',
        products=[
            p('Apple AirPods Pro 2, USB-C', 'tile-airpods.png', 24990,
              dict(model='pro', type='in', anc='yes'), 96,
              'Активное шумоподавление · адаптивный звук', new=8),
            p('Apple AirPods Pro 2 с зарядным кейсом MagSafe', 'tile-airpods.png', 26990,
              dict(model='pro', type='in', anc='yes'), 88,
              'MagSafe · до 30 часов с кейсом', new=8),
            p('Apple AirPods 4 с шумоподавлением', 'tile-airpods.png', 22990,
              dict(model='a4', type='in', anc='yes'), 84,
              'Шумоподавление · пространственное аудио', new=7),
            p('Apple AirPods 4', 'tile-airpods.png', 17990,
              dict(model='a4', type='in', anc='no'), 80,
              'Пространственное аудио · до 30 часов', old=19990, new=7),
            p('Apple AirPods Max, USB-C', 'tile-airpods.png', 59990,
              dict(model='max', type='over', anc='yes'), 70,
              'Полноразмерные · память формы · Hi-Fi', new=6, avail='order'),
        ]),

    dict(
        slug='accessories', h1='Аксессуары',
        title='Аксессуары для техники Apple | Комьюнити',
        chips=[('Чехлы', 'type:case'), ('Защитные стёкла', 'type:glass'),
               ('Зарядки', 'type:charger'), ('Кабели', 'type:cable')],
        filters=[
            dict(title='Тип', key='type', items=[
                ('Чехлы', 'case'), ('Защитные стёкла', 'glass'), ('Зарядные устройства', 'charger'),
                ('Кабели', 'cable'), ('Подставки', 'stand'), ('Стилусы', 'stylus')]),
            dict(title='Для устройства', key='compat', items=[
                ('iPhone', 'iphone'), ('iPad', 'ipad'), ('Mac', 'mac'), ('Apple Watch', 'watch')]),
            dict(title='Бренд', key='brand', items=[
                ('Apple', 'apple'), ('Spigen', 'spigen'), ('Baseus', 'baseus'), ('Ubear', 'ubear')]),
            dict(title='Наличие', key='avail', items=[
                ('В наличии', 'stock'), ('Под заказ', 'order')]),
        ],
        seo_title='Аксессуары к технике Apple',
        seo_text='Чехлы, стёкла, зарядки и кабели — оригинальные и от проверенных брендов. '
                 'Наклеим стекло бесплатно при покупке в магазине.',
        products=[
            p('Чехол Apple Silicone Case с MagSafe для iPhone 16 Pro Max', 'tile-accessories.png', 5990,
              dict(type='case', compat='iphone', brand='apple'), 92, 'Силикон · MagSafe · оригинал'),
            p('Чехол Apple FineWoven с MagSafe для iPhone 16', 'tile-accessories.png', 6990,
              dict(type='case', compat='iphone', brand='apple'), 74, 'Микротвил · MagSafe · оригинал', avail='order'),
            p('Чехол Spigen Ultra Hybrid для iPhone 16 Pro', 'tile-accessories.png', 2490,
              dict(type='case', compat='iphone', brand='spigen'), 86, 'Прозрачный · защита углов'),
            p('Защитное стекло Ubear Extreme 3D для iPhone 16 Pro Max', 'tile-accessories.png', 1490,
              dict(type='glass', compat='iphone', brand='ubear'), 90, 'Полная проклейка · наклеим бесплатно'),
            p('Адаптер питания Apple USB-C, 20 Вт', 'tile-accessories.png', 2490,
              dict(type='charger', compat='iphone', brand='apple'), 88, 'Быстрая зарядка · оригинал'),
            p('Кабель Apple USB-C / USB-C, 1 м', 'tile-accessories.png', 1990,
              dict(type='cable', compat='iphone', brand='apple'), 82, '60 Вт · оригинал'),
            p('Подставка Baseus для iPhone с MagSafe', 'tile-accessories.png', 1990,
              dict(type='stand', compat='iphone', brand='baseus'), 66, 'Алюминий · регулировка угла'),
            p('Apple Pencil Pro', 'tile-accessories.png', 16990,
              dict(type='stylus', compat='ipad', brand='apple'), 78, 'Нажим · сжатие · поиск через «Локатор»'),
        ]),

    dict(
        slug='powerbanks', h1='Павербанки',
        title='Внешние аккумуляторы и павербанки | Комьюнити',
        chips=[('С MagSafe', 'magsafe:yes'), ('10 000 мА·ч', 'capacity:10000'),
               ('20 000 мА·ч', 'capacity:20000')],
        filters=[
            dict(title='Ёмкость', key='capacity', items=[
                ('20 000 мА·ч', '20000'), ('10 000 мА·ч', '10000'), ('5 000 мА·ч', '5000')]),
            dict(title='Мощность', key='power', items=[
                ('65 Вт', '65'), ('30 Вт', '30'), ('20 Вт', '20')]),
            dict(title='MagSafe', key='magsafe', items=[
                ('Есть', 'yes'), ('Нет', 'no')]),
            dict(title='Бренд', key='brand', items=[
                ('Anker', 'anker'), ('Baseus', 'baseus'), ('Ubear', 'ubear')]),
            dict(title='Наличие', key='avail', items=[
                ('В наличии', 'stock'), ('Под заказ', 'order')]),
        ],
        seo_title='Павербанки для iPhone и iPad',
        seo_text='Внешние аккумуляторы с быстрой зарядкой и магнитным креплением. '
                 'Подскажем, какой мощности хватит для вашего устройства.',
        products=[
            p('Anker MagGo 10 000 мА·ч, MagSafe', 'tile-accessories.png', 7990,
              dict(capacity='10000', power='30', magsafe='yes', brand='anker'), 90, 'Магнитное крепление · подставка'),
            p('Anker 737 Power Bank 20 000 мА·ч, 65 Вт', 'tile-accessories.png', 8990,
              dict(capacity='20000', power='65', magsafe='no', brand='anker'), 84, 'Зарядит MacBook · дисплей'),
            p('Baseus Magnetic 10 000 мА·ч, 20 Вт', 'tile-accessories.png', 4990,
              dict(capacity='10000', power='20', magsafe='yes', brand='baseus'), 86, 'MagSafe-совместимый'),
            p('Baseus Bipow 10 000 мА·ч, 30 Вт', 'tile-accessories.png', 3990,
              dict(capacity='10000', power='30', magsafe='no', brand='baseus'), 72, 'Два порта · компактный'),
            p('Ubear Magnetic 5 000 мА·ч', 'tile-accessories.png', 2990,
              dict(capacity='5000', power='20', magsafe='yes', brand='ubear'), 64, 'Тонкий · магнитный', avail='order'),
        ]),

    dict(
        slug='docks', h1='Док-станции',
        title='Док-станции и хабы для Apple | Комьюнити',
        chips=[('3-в-1 с MagSafe', 'type:dock3'), ('USB-C хабы', 'type:hub')],
        filters=[
            dict(title='Тип', key='type', items=[
                ('Док-станция 3-в-1', 'dock3'), ('USB-C хаб', 'hub'), ('Зарядная станция', 'charger')]),
            dict(title='Портов', key='ports', items=[
                ('8 портов', '8'), ('6 портов', '6'), ('без портов', '0')]),
            dict(title='Бренд', key='brand', items=[
                ('Belkin', 'belkin'), ('Anker', 'anker'), ('Satechi', 'satechi'), ('Baseus', 'baseus')]),
            dict(title='Наличие', key='avail', items=[
                ('В наличии', 'stock'), ('Под заказ', 'order')]),
        ],
        seo_title='Док-станции и хабы',
        seo_text='Зарядные станции 3-в-1 для iPhone, Apple Watch и AirPods, USB-C хабы для MacBook. '
                 'Подберём под ваш набор устройств.',
        products=[
            p('Belkin BoostCharge Pro 3-в-1 с MagSafe', 'tile-accessories.png', 12990,
              dict(type='dock3', ports='0', brand='belkin'), 90, 'iPhone + Watch + AirPods · 15 Вт'),
            p('Anker 3-в-1 Cube с MagSafe', 'tile-accessories.png', 14990,
              dict(type='dock3', ports='0', brand='anker'), 82, 'Складная · сертификат Apple', avail='order'),
            p('Satechi USB-C Hub, 8 портов', 'tile-accessories.png', 9990,
              dict(type='hub', ports='8', brand='satechi'), 78, 'HDMI 4K · SD · Ethernet'),
            p('Baseus USB-C Hub, 6 портов', 'tile-accessories.png', 4990,
              dict(type='hub', ports='6', brand='baseus'), 70, 'HDMI · USB-A · картридер'),
        ]),
]

HEAD = '''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/styles.css">
</head>
<body>

<!--@part:sprite-->
<!--/@part:sprite-->

<!--@part:header-->
<!--/@part:header-->

<!-- Страница собрана скриптом _catalog.py — правьте данные там и пересоберите:
     python3 _catalog.py && python3 _build.py -->
'''

FOOT = '''
<!--@part:footer-->
<!--/@part:footer-->

<!--@part:modals-->
<!--/@part:modals-->

<script src="js/main.js"></script>
<script src="js/catalog.js"></script>
</body>
</html>
'''


def money(v):
    return f'{v:,}'.replace(',', ' ') + ' ₽'


# У флагмана карточка сделана вручную: там показаны торговые предложения
# (цвет и память меняют фото, цену и артикул) — образец для натяжки на Битрикс.
HAND_MADE = {'iphone-16-pro-max-512-peschanyy-titanovyy': 'product.html'}


def page_name(prod):
    return HAND_MADE.get(prod['slug'], f"product-{prod['slug']}.html")


def card(prod, cat):
    href = page_name(prod)
    attrs = ' '.join(f'data-{k}="{v}"' for k, v in prod['attrs'].items())
    discount = (prod['old'] - prod['price']) if prod['old'] else 0
    old = f'<s>{money(prod["old"])}</s>' if prod['old'] else ''
    badge = ''
    if prod['badge']:
        badge = f'<span class="p-card__badge">{prod["badge"]}</span>'
    elif discount:
        badge = f'<span class="p-card__badge">−{money(discount)}</span>'
    stock = ('<div class="p-card__stock"><svg class="ico"><use href="#i-check"/></svg> В наличии</div>'
             if prod['avail'] == 'stock' else
             '<div class="p-card__stock p-card__stock--order"><svg class="ico"><use href="#i-clock"/></svg> Под заказ, 2–3 дня</div>')
    return f'''          <article class="p-card" data-price="{prod['price']}" data-pop="{prod['pop']}" data-new="{prod['new']}" data-discount="{discount}" data-avail="{prod['avail']}" {attrs}>
            <div class="p-card__photo">
              {badge}
              <a href="{href}"><img src="img/{prod['img']}" alt="{prod['name']}"></a>
              <button class="p-card__fav" type="button" aria-label="В избранное"><svg class="ico"><use href="#i-heart"/></svg></button>
              <button class="p-card__compare" type="button" aria-label="Добавить к сравнению"><svg class="ico"><use href="#i-compare"/></svg></button>
            </div>
            <a class="p-card__name" href="{href}">{prod['name']}</a>
            <div class="p-card__list-info">{prod['info']}</div>
            {stock}
            <div class="p-card__price">{money(prod['price'])}{old}</div>
            <div class="p-card__installment"><b>{money(round(prod['price'] / 12))}</b> В рассрочку х 12 мес.</div>
            <a href="cart.html" class="btn btn--secondary p-card__btn">Добавить в корзину</a>
          </article>'''


def filters_html(cat):
    prices = [p['price'] for p in cat['products']]
    out = ['''      <aside class="filters" id="filters">
        <div class="filters__head">
          <span>Фильтры</span>
          <button type="button" aria-label="Закрыть" data-filters-close><svg class="ico"><use href="#i-close"/></svg></button>
        </div>
        <div class="filters__group">
          <div class="filters__title">Цена, ₽</div>
          <div class="price-fields">
            <input type="number" data-price-min placeholder="{}" aria-label="Цена от">
            <span>—</span>
            <input type="number" data-price-max placeholder="{}" aria-label="Цена до">
          </div>
        </div>'''.format(money(min(prices)).replace(' ₽', ''), money(max(prices)).replace(' ₽', ''))]

    for group in cat['filters']:
        out.append('        <div class="filters__group">')
        out.append(f'          <div class="filters__title">{group["title"]}</div>')
        for i, (label, value) in enumerate(group['items']):
            hidden = ' hidden' if i >= 5 else ''
            out.append(f'          <label class="filters__item"{hidden}><input type="checkbox" data-key="{group["key"]}" value="{value}"> {label} <i class="filters__count">0</i></label>')
        if len(group['items']) > 5:
            out.append('          <button class="filters__more" type="button" data-filters-expand>Показать все</button>')
        out.append('        </div>')

    out.append('''        <div class="filters__actions">
          <button class="btn btn--primary btn--block" type="button" data-filters-apply>Показать товары</button>
          <button class="link" type="button" data-filters-reset>Сбросить фильтры</button>
        </div>
      </aside>''')
    return '\n'.join(out)


def listing_page(cat):
    chips = '\n'.join(
        f'      <button class="chip" type="button" data-chip="{value}">{label}</button>'
        for label, value in cat['chips'])
    cards = '\n'.join(card(p, cat) for p in cat['products'])

    body = f'''<main>
  <div class="container">
    <nav class="breadcrumbs">
      <a href="index.html"><svg class="ico"><use href="#i-home"/></svg></a>
      <span class="breadcrumbs__sep">›</span>
      <a href="catalog.html">Каталог</a>
      <span class="breadcrumbs__sep">›</span>
      <span>{cat['h1']}</span>
    </nav>

    <h1 class="page-title">{cat['h1']}</h1>

    <div class="chips">
{chips}
    </div>

    <div class="listing-top">
      <div class="listing-top__count">Найдено <b data-found>{len(cat['products'])}</b> товаров</div>
      <div class="listing-top__tools">
        <button class="btn btn--outline listing-top__filters" type="button" data-filters-open>
          <svg class="ico"><use href="#i-filter"/></svg> Фильтры
        </button>
        <label class="sort">
          <span>Сортировать:</span>
          <select data-sort aria-label="Сортировка">
            <option value="pop">по популярности</option>
            <option value="price-asc">сначала дешёвые</option>
            <option value="price-desc">сначала дорогие</option>
            <option value="new">сначала новинки</option>
            <option value="discount">по размеру скидки</option>
          </select>
        </label>
        <div class="view-toggle">
          <button type="button" class="is-active" data-view="grid" aria-label="Плиткой"><svg class="ico"><use href="#i-grid"/></svg></button>
          <button type="button" data-view="list" aria-label="Списком"><svg class="ico"><use href="#i-list"/></svg></button>
        </div>
      </div>
    </div>

    <div class="active-filters" data-active-filters hidden></div>

    <div class="listing">
      <div class="filters-overlay" hidden></div>
{filters_html(cat)}

      <div>
        <div class="listing__grid" data-grid data-step="9">
{cards}
        </div>

        <div class="empty" data-empty hidden>
          <svg class="ico"><use href="#i-search"/></svg>
          <div class="empty__title">Ничего не нашлось</div>
          <div class="empty__text">Попробуйте убрать часть фильтров или позвоните — подберём вручную и привезём под заказ</div>
          <button class="btn btn--primary" type="button" data-filters-reset>Сбросить фильтры</button>
        </div>

        <div class="pagination">
          <button class="btn btn--outline pagination__more" type="button" data-more>Показать ещё</button>
          <div class="pagination__pages"></div>
        </div>
      </div>
    </div>

    <section class="prose" style="margin:48px 0 64px">
      <h2>{cat['seo_title']}</h2>
      <p>{cat['seo_text']}</p>
    </section>
  </div>
</main>
'''
    return HEAD.format(title=cat['title']) + body + FOOT


def index_page():
    tiles = {
        'iphone': ('tile-iphone.png', 'iPhone'),
        'mac': ('tile-mac.png', 'Mac'),
        'ipad': ('tile-ipad.png', 'iPad'),
        'watch': ('tile-watch.png', 'Apple Watch'),
        'airpods': ('tile-airpods.png', 'AirPods'),
        'accessories': ('tile-accessories.png', 'Аксессуары'),
        'powerbanks': ('tile-accessories.png', 'Павербанки'),
        'docks': ('tile-accessories.png', 'Док-станции'),
    }
    cards = []
    for cat in CATS:
        img, name = tiles[cat['slug']]
        cards.append(f'''      <a class="section-card" href="catalog-{cat['slug']}.html">
        <div>
          <div class="section-card__name">{name}</div>
          <div class="section-card__count">{len(cat['products'])} товаров в наличии</div>
        </div>
        <span class="section-card__link">Смотреть <svg class="ico"><use href="#i-arrow-r"/></svg></span>
        <img class="section-card__img" src="img/{img}" alt="">
      </a>''')

    hits = []
    for cat in CATS[:4]:
        prod = max(cat['products'], key=lambda x: x['pop'])
        hits.append(card(prod, cat))

    body = f'''<main>
  <div class="container">
    <nav class="breadcrumbs">
      <a href="index.html"><svg class="ico"><use href="#i-home"/></svg></a>
      <span class="breadcrumbs__sep">›</span>
      <span>Каталог</span>
    </nav>

    <h1 class="page-title">Каталог</h1>

    <div class="sections-grid">
{chr(10).join(cards)}
    </div>

    <h2 class="section-title">Хиты продаж</h2>
    <div class="products">
{chr(10).join(hits)}
    </div>

    <section class="prose" style="margin:48px 0 64px">
      <h2>Техника Apple в Каспийске и Махачкале</h2>
      <p>В каталоге — официальные устройства с гарантией: iPhone, Mac, iPad, Apple Watch, AirPods
        и аксессуары. Проверяем каждое устройство при выдаче, помогаем перенести данные,
        оформляем рассрочку 0-0-12 и принимаем старую технику по Trade-In.</p>
    </section>
  </div>
</main>
'''
    return HEAD.format(title='Каталог техники Apple | Комьюнити') + body + FOOT


CAT_NAMES = {'iphone': 'iPhone', 'mac': 'Mac', 'ipad': 'iPad', 'watch': 'Apple Watch',
             'airpods': 'AirPods', 'accessories': 'Аксессуары', 'powerbanks': 'Павербанки',
             'docks': 'Док-станции'}


def search_page():
    """Результаты поиска: те же карточки, фильтр по разделу и цене."""
    picked = []
    for cat in CATS:
        for prod in sorted(cat['products'], key=lambda x: -x['pop'])[:3]:
            item = dict(prod)
            item['attrs'] = dict(cat=cat['slug'])
            picked.append(item)

    cards = '\n'.join(card(prod, None) for prod in picked)
    cat_items = '\n'.join(
        f'          <label class="filters__item"><input type="checkbox" data-key="cat" value="{cat["slug"]}"> {CAT_NAMES[cat["slug"]]} <i class="filters__count">0</i></label>'
        for cat in CATS)
    chips = '\n'.join(
        f'      <button class="chip" type="button" data-chip="cat:{cat["slug"]}">{CAT_NAMES[cat["slug"]]}</button>'
        for cat in CATS[:5])
    prices = [p['price'] for p in picked]

    body = f'''<main>
  <div class="container">
    <nav class="breadcrumbs">
      <a href="index.html"><svg class="ico"><use href="#i-home"/></svg></a>
      <span class="breadcrumbs__sep">›</span>
      <span>Поиск</span>
    </nav>

    <h1 class="page-title">Результаты поиска</h1>

    <form class="search search--light search--page" action="search.html">
      <input type="text" name="q" value="iPhone 16" placeholder="Что ищем?">
      <button type="submit" aria-label="Найти"><svg class="ico"><use href="#i-search"/></svg></button>
    </form>

    <div class="chips">
{chips}
    </div>

    <div class="listing-top">
      <div class="listing-top__count">Найдено <b data-found>{len(picked)}</b> товаров по запросу «iPhone 16»</div>
      <div class="listing-top__tools">
        <button class="btn btn--outline listing-top__filters" type="button" data-filters-open>
          <svg class="ico"><use href="#i-filter"/></svg> Фильтры
        </button>
        <label class="sort">
          <span>Сортировать:</span>
          <select data-sort aria-label="Сортировка">
            <option value="pop">по релевантности</option>
            <option value="price-asc">сначала дешёвые</option>
            <option value="price-desc">сначала дорогие</option>
            <option value="new">сначала новинки</option>
          </select>
        </label>
        <div class="view-toggle">
          <button type="button" class="is-active" data-view="grid" aria-label="Плиткой"><svg class="ico"><use href="#i-grid"/></svg></button>
          <button type="button" data-view="list" aria-label="Списком"><svg class="ico"><use href="#i-list"/></svg></button>
        </div>
      </div>
    </div>

    <div class="active-filters" data-active-filters hidden></div>

    <div class="listing">
      <div class="filters-overlay" hidden></div>
      <aside class="filters" id="filters">
        <div class="filters__head">
          <span>Фильтры</span>
          <button type="button" aria-label="Закрыть" data-filters-close><svg class="ico"><use href="#i-close"/></svg></button>
        </div>
        <div class="filters__group">
          <div class="filters__title">Цена, ₽</div>
          <div class="price-fields">
            <input type="number" data-price-min placeholder="{money(min(prices)).replace(' ₽', '')}" aria-label="Цена от">
            <span>—</span>
            <input type="number" data-price-max placeholder="{money(max(prices)).replace(' ₽', '')}" aria-label="Цена до">
          </div>
        </div>
        <div class="filters__group">
          <div class="filters__title">Раздел</div>
{cat_items}
        </div>
        <div class="filters__group">
          <div class="filters__title">Наличие</div>
          <label class="filters__item"><input type="checkbox" data-key="avail" value="stock"> В наличии <i class="filters__count">0</i></label>
          <label class="filters__item"><input type="checkbox" data-key="avail" value="order"> Под заказ <i class="filters__count">0</i></label>
        </div>
        <div class="filters__actions">
          <button class="btn btn--primary btn--block" type="button" data-filters-apply>Показать товары</button>
          <button class="link" type="button" data-filters-reset>Сбросить фильтры</button>
        </div>
      </aside>

      <div>
        <div class="listing__grid" data-grid data-step="9">
{cards}
        </div>

        <div class="empty" data-empty hidden>
          <svg class="ico"><use href="#i-search"/></svg>
          <div class="empty__title">По запросу ничего не нашлось</div>
          <div class="empty__text">Проверьте написание или позвоните — подберём модель и привезём под заказ за 2–3 дня</div>
          <a class="btn btn--primary" href="catalog.html">Открыть каталог</a>
        </div>

        <div class="pagination">
          <button class="btn btn--outline pagination__more" type="button" data-more>Показать ещё</button>
        </div>
      </div>
    </div>

    <section class="prose" style="margin:48px 0 20px">
      <h2>Часто ищут</h2>
    </section>
    <div class="chips" style="margin-bottom:64px">
      <a class="chip" href="search.html">iPhone 16 Pro Max</a>
      <a class="chip" href="search.html">MacBook Air M4</a>
      <a class="chip" href="search.html">AirPods Pro 2</a>
      <a class="chip" href="search.html">Apple Watch Series 10</a>
      <a class="chip" href="search.html">iPad Air</a>
      <a class="chip" href="search.html">Чехол для iPhone 16</a>
    </div>
  </div>
</main>
'''
    return HEAD.format(title='Поиск | Комьюнити') + body + FOOT


def main():
    (ROOT / 'catalog.html').write_text(index_page(), encoding='utf-8')
    print('✓ catalog.html (витрина разделов)')
    (ROOT / 'search.html').write_text(search_page(), encoding='utf-8')
    print('✓ search.html (результаты поиска)')
    for cat in CATS:
        name = f"catalog-{cat['slug']}.html"
        (ROOT / name).write_text(listing_page(cat), encoding='utf-8')
        print(f"✓ {name} — товаров: {len(cat['products'])}, групп фильтров: {len(cat['filters'])}")


if __name__ == '__main__':
    main()
