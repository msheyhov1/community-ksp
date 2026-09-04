#!/usr/bin/env python3
"""Сборка страниц вёрстки из общих частей.

В каждой странице общие куски обёрнуты маркерами:

    <!--@part:header--> ... <!--/@part:header-->

Скрипт подставляет в эти блоки актуальное содержимое файлов
`_parts_<имя>.html`. Запускать после правки любой общей части:

    python3 _build.py
"""

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
    pages = sorted(p for p in ROOT.glob("*.html") if not p.name.startswith("_"))
    for page in pages:
        src = page.read_text(encoding="utf-8")
        out, n = sync(src, parts)
        if n == 0:
            print(f"  {page.name}: маркеров нет — пропуск")
            continue
        if out != src:
            page.write_text(out, encoding="utf-8")
            print(f"✓ {page.name}: обновлено блоков — {n}")
        else:
            print(f"· {page.name}: без изменений ({n} блока)")


if __name__ == "__main__":
    main()
