#!/usr/bin/env python3
"""
ri_extract.py — extract chapters from https://ri.theomniarch.com.ng into clean
Markdown / plain text / JSON files.

The site serves fully server-rendered pages: the chapter lives in
    <div class="prose"> ... <p id="pN">paragraph</p> ...
with scene breaks marked as <p class="scene-break">• • •</p>.
This script pulls exactly that block and drops the nav / toolbar / footer chrome.

Usage
-----
    python3 ri_extract.py 7                        # chapter 7 -> chapters/*.md
    python3 ri_extract.py 7 --format txt           # plain text instead
    python3 ri_extract.py 7 --format json          # structured records
    python3 ri_extract.py 1-8                      # a range
    python3 ri_extract.py --all                    # walk 1,2,3... until it 404s
    python3 ri_extract.py https://ri.theomniarch.com.ng/chapter-7
    python3 ri_extract.py 7 --dry-run              # parse + report stats, write nothing

Options
-------
    --out DIR       output directory (default: ./chapters)
    --format FMT    md (default) | txt | json
    --delay SECS    pause between requests in range/--all mode (default 1.5)
    --dry-run       don't write files; print title, word/paragraph counts, checksum
    --force         overwrite existing files (default: skip existing)

Notes
-----
* Uses the site's own <meta name="description"> / header block for metadata
  (chapter title, volume, translator, word count).
* Only ONE request per chapter, with a normal User-Agent and a polite delay in
  batch mode. Please respect the site's terms and the translator's work: use
  this for personal, offline reading.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from dataclasses import dataclass, field, asdict
from datetime import date
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

BASE = "https://ri.theomniarch.com.ng"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/125.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml",
}


# --------------------------------------------------------------------------- #
# data model
# --------------------------------------------------------------------------- #
@dataclass
class Chapter:
    number: int | None
    title: str
    volume: str = ""
    translator: str = ""
    url: str = ""
    prev_url: str = ""
    next_url: str = ""
    paragraphs: list[str] = field(default_factory=list)  # rendered lines, incl. "* * *"
    fetched: str = field(default_factory=lambda: date.today().isoformat())

    @property
    def word_count(self) -> int:
        text = " ".join(p for p in self.paragraphs if p != "* * *")
        return len(re.findall(r"[\w’'\-]+", text))

    @property
    def body_words_only(self) -> str:
        return "\n\n".join(self.paragraphs)


# --------------------------------------------------------------------------- #
# fetching / parsing
# --------------------------------------------------------------------------- #
def fetch(url: str, timeout: int = 30) -> str:
    r = requests.get(url, headers=HEADERS, timeout=timeout)
    r.raise_for_status()
    r.encoding = r.apparent_encoding or "utf-8"
    return r.text


def _clean(line: str) -> str:
    line = line.replace("\u00a0", " ")
    line = re.sub(r"[ \t]+", " ", line)
    return line.strip()


def parse_chapter(html: str, url: str) -> Chapter:
    soup = BeautifulSoup(html, "html.parser")

    # --- header block -----------------------------------------------------
    h1 = soup.select_one("header.reader-head h1")
    ch_title_el = soup.select_one("header.reader-head .ch-title")
    number = None
    if h1:
        m = re.search(r"\d+", h1.get_text())
        if m:
            number = int(m.group())

    title = ch_title_el.get_text(strip=True) if ch_title_el else (
        h1.get_text(strip=True) if h1 else "Untitled"
    )

    volume = translator = ""
    for item in soup.select("header.reader-head .ch-meta-item"):
        t = item.get_text(" ", strip=True)
        if t.lower().startswith("volume"):
            volume = t
        elif t.lower().startswith("translator"):
            translator = t.split(":", 1)[-1].strip()

    prev_url = next_url = ""
    p = soup.select_one("a.gamepad-btn.prev")
    n = soup.select_one("a.gamepad-btn.next")
    if p and p.get("href"):
        prev_url = urljoin(url, p["href"])
    if n and n.get("href"):
        next_url = urljoin(url, n["href"])

    # --- body -------------------------------------------------------------
    prose = soup.select_one("div.prose")
    if prose is None:
        raise ValueError(f"no <div class='prose'> found at {url}")

    # Drop inline encyclopedia cross-reference markers: the site links terms to
    # /notes with <a class="note-ref" data-note="1">1</a>, styled as a superscript.
    # Left in, they leak into the text as a bare digit ("Spring Autumn Cicada 1").
    notes = [
        (ref.get("data-note"), ref.get("href"))
        for ref in prose.select("a.note-ref")
    ]
    for ref in prose.select("a.note-ref, sup"):
        ref.decompose()

    paragraphs: list[str] = []
    for el in prose.find_all(["p", "h2", "h3", "blockquote"], recursive=True):
        classes = el.get("class") or []
        if "scene-break" in classes:
            paragraphs.append("* * *")
            continue
        text = _clean(el.get_text(" ", strip=True))
        if text:
            paragraphs.append(text)

    if not paragraphs:
        raise ValueError(f"chapter body at {url} parsed to zero paragraphs")

    return Chapter(
        number=number, title=title, volume=volume, translator=translator,
        url=url, prev_url=prev_url, next_url=next_url, paragraphs=paragraphs,
    )


# --------------------------------------------------------------------------- #
# rendering
# --------------------------------------------------------------------------- #
def slugify(text: str, maxlen: int = 60) -> str:
    s = text.lower()
    s = re.sub(r"[\u2018\u2019']", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:maxlen].rstrip("-")


def render_md(ch: Chapter) -> str:
    n = ch.number if ch.number is not None else "?"
    label = f"Chapter {n}" if ch.number is not None else "Chapter"
    out = [
        f"# {label}: {ch.title}",
        "",
    ]
    meta = []
    if ch.volume:
        meta.append(ch.volume)
    if ch.translator:
        meta.append(f"Translator: {ch.translator}")
    meta.append(f"{ch.word_count:,} words")
    out.append(f"*{' · '.join(meta)}*")
    out.append("")
    out.append(f"Source: {ch.url}  ")
    out.append(f"Extracted: {ch.fetched}")
    out.append("")
    out.append("---")
    out.append("")
    out.extend(ch.paragraphs)
    out.append("")
    if ch.next_url:
        out.append(f"*Next: {ch.next_url}*")
        out.append("")
    return "\n".join(out)


def render_txt(ch: Chapter) -> str:
    n = ch.number if ch.number is not None else "?"
    head = [
        f"CHAPTER {n}: {ch.title}",
        "=" * (10 + len(str(n)) + 2 + len(ch.title)),
        "",
    ]
    if ch.volume:
        head.append(ch.volume)
    if ch.translator:
        head.append(f"Translator: {ch.translator}")
    head += [f"Source: {ch.url}", f"Extracted: {ch.fetched}", f"Words: {ch.word_count:,}", "", ""]
    body = [("" if p == "* * *" else p) for p in ch.paragraphs]
    body = ["        * * *" if p == "" else p for p in body]
    return "\n".join(head + body) + "\n"


def render_json(ch: Chapter) -> str:
    d = asdict(ch)
    d["word_count"] = ch.word_count
    return json.dumps(d, ensure_ascii=False, indent=2)


RENDERERS = {"md": (render_md, "md"), "txt": (render_txt, "txt"), "json": (render_json, "json")}


# --------------------------------------------------------------------------- #
# targets
# --------------------------------------------------------------------------- #
def url_for(spec: str) -> str:
    """Accept '7', 'ch7', 'chapter-7', or a full URL."""
    if spec.startswith("http"):
        return spec
    m = re.search(r"(\d+)\s*$", spec.strip())
    if not m:
        raise ValueError(f"can't read a chapter number out of {spec!r}")
    return f"{BASE}/chapter-{int(m.group(1))}"


def discover_last_chapter(delay: float, cap: int = 4000) -> int:
    """Walk forward until a chapter URL stops resolving."""
    n = 1
    last = 0
    while n <= cap:
        try:
            fetch(url_for(str(n)), timeout=15)
            last = n
            n += 1
            time.sleep(delay)
        except requests.HTTPError as e:
            if e.response is not None and e.response.status_code == 404:
                break
            raise
    return last


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Extract chapters from ri.theomniarch.com.ng")
    ap.add_argument("target", nargs="?",
                    help="chapter number, range like 1-8, or full URL")
    ap.add_argument("--all", action="store_true", help="extract every chapter found")
    ap.add_argument("--out", default="chapters", help="output directory")
    ap.add_argument("--format", choices=sorted(RENDERERS), default="md")
    ap.add_argument("--delay", type=float, default=1.5, help="pause between requests")
    ap.add_argument("--dry-run", action="store_true", help="report stats, write nothing")
    ap.add_argument("--force", action="store_true", help="overwrite existing files")
    args = ap.parse_args(argv)

    render, ext = RENDERERS[args.format]
    outdir = Path(args.out)

    # build the list of chapter specs
    specs: list[str] = []
    if args.all:
        last = discover_last_chapter(args.delay)
        specs = [str(i) for i in range(1, last + 1)]
        print(f"discovered {last} chapter(s)")
    elif args.target:
        t = args.target.strip()
        m = re.fullmatch(r"(\d+)\s*-\s*(\d+)", t)
        if m and not t.startswith("http"):
            a, b = int(m.group(1)), int(m.group(2))
            specs = [str(i) for i in range(min(a, b), max(a, b) + 1)]
        else:
            specs = [t]
    else:
        ap.error("give a chapter number/range/URL, or --all")

    if not args.dry_run:
        outdir.mkdir(parents=True, exist_ok=True)

    ok = failed = 0
    for i, spec in enumerate(specs):
        url = url_for(spec)
        try:
            ch = parse_chapter(fetch(url), url)
        except Exception as e:  # noqa: BLE001
            print(f"  ✗ {url}: {e}")
            failed += 1
            continue

        label = f"Chapter {ch.number if ch.number is not None else '?'}"
        digest = hashlib.sha256(
            "\n".join(ch.paragraphs).encode("utf-8")
        ).hexdigest()[:12]
        print(
            f"  ✓ {label}: {ch.title[:70]} — "
            f"{len(ch.paragraphs)} para · {ch.word_count:,} words · sha256:{digest}"
        )
        if args.dry_run:
            ok += 1
            continue

        if args.format == "json":
            name = f"chapter-{ch.number:03d}.json" if ch.number is not None else "chapter.json"
        else:
            num = f"{ch.number:03d}" if ch.number is not None else "000"
            name = f"chapter-{num}-{slugify(ch.title)}.{ext}" if ch.title else f"chapter-{num}.{ext}"

        path = outdir / name
        if path.exists() and not args.force:
            print(f"      skip (exists): {path}")
            ok += 1
            continue
        path.write_text(render(ch), encoding="utf-8")
        print(f"      → {path}")
        ok += 1
        if i < len(specs) - 1:
            time.sleep(args.delay)

    print(f"\n{'parsed' if args.dry_run else 'written'}: {ok} · failed: {failed}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
