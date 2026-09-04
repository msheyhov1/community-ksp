#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Статический аудит вёрстки: ссылки, кнопки, обработчики, дубли id."""
import pathlib, re, collections, sys

ROOT = pathlib.Path(__file__).resolve().parent
pages = sorted(p for p in ROOT.glob('*.html') if not p.name.startswith('_'))
existing = {p.name for p in ROOT.glob('*.html')}

# селекторы/атрибуты, которые обрабатываются в js/main.js и js/catalog.js
JS = '\n'.join(f.read_text(encoding='utf-8') for f in sorted((ROOT / 'js').glob('*.js')))

def camel_to_dash(name):
    return re.sub(r'([A-Z])', lambda m: '-' + m.group(1).lower(), name)

# атрибуты, по которым в скриптах находят элементы: [data-x] и dataset.x
handled_data = set(re.findall(r'\[data-([a-z-]+)', JS))
handled_data |= {camel_to_dash(n) for n in re.findall(r'dataset\.([a-zA-Z]+)', JS)}
# классы: querySelector('.x'), closest('.x'), classList.toggle('x')
handled_class = set(re.findall(r"querySelector(?:All)?\('\.?([a-z0-9_-]+)", JS))
handled_class |= set(re.findall(r"closest\('\.([a-z0-9_-]+)", JS))
handled_class |= set(re.findall(r"querySelector(?:All)?\('\.([a-z0-9_-]+)\s", JS))

report = collections.defaultdict(list)

for p in pages:
    s = p.read_text(encoding='utf-8')

    # 1. ссылки
    for m in re.finditer(r'<a\b([^>]*)>(.*?)</a>', s, re.S):
        attrs, inner = m.group(1), re.sub(r'<[^>]+>', '', m.group(2)).strip()[:30]
        href = re.search(r'href="([^"]*)"', attrs)
        if not href:
            report['ссылка без href'].append(f'{p.name}: «{inner}»')
            continue
        h = href.group(1)
        if h == '#':
            report['href="#"'].append(f'{p.name}: «{inner or "иконка"}»')
        elif h.startswith(('http', 'tel:', 'mailto:', '#')):
            pass
        else:
            target = h.split('?')[0].split('#')[0]
            if target and target not in existing:
                report['битая ссылка'].append(f'{p.name}: {target} («{inner}»)')

    # 2. кнопки без обработчика
    for m in re.finditer(r'<button\b([^>]*)>(.*?)</button>', s, re.S):
        attrs, inner = m.group(1), re.sub(r'<[^>]+>', '', m.group(2)).strip()[:28]
        if 'type="submit"' in attrs:
            continue
        datas = set(re.findall(r'data-([a-z-]+)', attrs))
        classes = set(re.search(r'class="([^"]*)"', attrs).group(1).split()) if 'class="' in attrs else set()
        ok = bool(datas & handled_data) or bool(classes & handled_class) or any(
            f'.{c}' in JS for c in classes)
        if not ok:
            report['кнопка без обработчика'].append(f'{p.name}: [{" ".join(classes) or "-"}] «{inner or "иконка"}»')

    # 3. дубли id
    ids = re.findall(r'\bid="([^"]+)"', s)
    for i, n in collections.Counter(ids).items():
        if n > 1:
            report['дубль id'].append(f'{p.name}: #{i} × {n}')

    # 4. картинки без alt
    for m in re.finditer(r'<img\b(?![^>]*\balt=)[^>]*>', s):
        report['img без alt'].append(f'{p.name}: {m.group(0)[:60]}')

    # 5. формы, ведущие в никуда
    for m in re.finditer(r'<form\b([^>]*)>', s):
        act = re.search(r'action="([^"]*)"', m.group(1))
        if act and act.group(1) not in ('#',) and act.group(1).split('?')[0] not in existing:
            report['форма → несуществующий адрес'].append(f'{p.name}: {act.group(1)}')

    # 6. пустые ссылки-заглушки в шапке/футере уже посчитаны выше

print(f'страниц: {len(pages)}\n')
for key in sorted(report):
    items = report[key]
    uniq = collections.Counter(items)
    print(f'=== {key}: {len(items)}')
    shown = 0
    for text, n in uniq.most_common():
        # схлопываем одинаковые по всем страницам
        print(f'   {n:>3} × {text}' if n > 1 else f'       {text}')
        shown += 1
        if shown >= 12:
            print(f'   … ещё {len(uniq) - shown} вариантов')
            break
    print()
