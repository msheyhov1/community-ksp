#!/usr/bin/env python3
"""Сборка страниц вёрстки из общих частей.

В каждой странице общие куски обёрнуты маркерами:

    <!--@part:header--> ... <!--/@part:header-->

Скрипт подставляет в эти блоки актуальное содержимое файлов
`_parts_<имя>.html`. Запускать после правки любой общей части:

    python3 _build.py
"""

import hashlib
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
PART_NAMES = ("sprite", "header", "footer", "modals", "accnav")


def load_parts():
    parts = {}
    for name in PART_NAMES:
        path = ROOT / f"_parts_{name}.html"
        if not path.exists():
            sys.exit(f"нет файла части: {path.name}")
        parts[name] = path.read_text(encoding="utf-8").strip()
    return parts


def asset_versions():
    """К ссылкам на стили и скрипты добавляем версию-хеш.

    Без этого браузер держит старый CSS из кеша и правки «не видны»,
    пока пользователь не нажмёт Cmd+Shift+R. С хешем адрес файла меняется
    при каждой правке, и обновление подхватывается само.
    """
    versions = {}
    for path in sorted(ROOT.glob('css/*.css')) + sorted(ROOT.glob('js/*.js')):
        digest = hashlib.md5(path.read_bytes()).hexdigest()[:8]
        versions[f'{path.parent.name}/{path.name}'] = digest
    return versions


def stamp_assets(text, versions):
    for name, digest in versions.items():
        text = re.sub(rf'(["\'])({re.escape(name)})(\?v=[0-9a-f]+)?\1',
                      lambda m: f'{m.group(1)}{name}?v={digest}{m.group(1)}', text)
    return text


def sync(text, parts):
    changed = 0
    for name, body in parts.items():
        pattern = re.compile(
            rf"(<!--@part:{name}-->).*?(<!--/@part:{name}-->)", re.S
        )
        text, n = pattern.subn(
            lambda m: f"{m.group(1)}\n{body}\n{m.group(2)}", text
        )
        changed += n
    return text, changed


def main():
    parts = load_parts()
    versions = asset_versions()
    pages = sorted(p for p in ROOT.glob("*.html") if not p.name.startswith("_"))
    for page in pages:
        src = page.read_text(encoding="utf-8")
        out, n = sync(src, parts)
        out = stamp_assets(out, versions)
        if n == 0 and out == src:
            print(f"  {page.name}: маркеров нет — пропуск")
            continue
        if out != src:
            page.write_text(out, encoding="utf-8")
            print(f"✓ {page.name}: обновлено блоков — {n}")
        else:
            print(f"· {page.name}: без изменений ({n} блока)")


if __name__ == "__main__":
    main()
