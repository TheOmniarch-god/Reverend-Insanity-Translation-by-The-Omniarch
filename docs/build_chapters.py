#!/usr/bin/env python3
"""
The Omniarch Translation — Reverend Insanity Chapter Compiler
Parses .md manuscripts into atelier-styled HTML chapters with:
- Playfair Display poem blocks
- Semantic <em> and <strong> detection
- Scene-break formatting
- Capitalized title formatting
- Genre tags in chapter header
- Clickable top navigation buttons + keyboard arrow navigation
- Word counts & estimated reading times
- Reader font size switcher
- Automatic index.html squircle ledger updating
- Deployment zip packaging
"""

import re
import os
import shutil
import zipfile

WORKSPACE = '/home/user/reverend-insanity'
DOCS_DIR = '/home/user/gh-deploy/docs'
DEPLOY_DIR = '/home/user/gh-deploy'
MD_PATH = '/home/user/uploads/Reverend_Insanity_Chapters_1–3 (3).md'

with open(MD_PATH, 'r', encoding='utf-8') as f:
    full_text = f.read()

def capitalize_title(title_str):
    # Capitalize every single word per user request ("Capitalize each word for the title")
    words = title_str.split()
    capitalized = []
    for w in words:
        if w.startswith('“') or w.startswith('"'):
            # handle leading quote
            w = w[0] + w[1:].capitalize()
        else:
            w = w.capitalize()
        capitalized.append(w)
    return " ".join(capitalized)

def parse_markdown_prose(text):
    paragraphs = text.strip().split('\n\n')
    html_paragraphs = []
    
    for p in paragraphs:
        p_str = p.strip()
        if not p_str:
            continue
            
        # Check for poem block
        if p_str.startswith('*“Green mountains') or p_str.startswith('“Green mountains'):
            lines = [l.strip().strip('*').rstrip('\\').strip() for l in p_str.split('\n') if l.strip()]
            poem_content = "<br>\n      ".join(lines)
            html_paragraphs.append(f'<blockquote class="prose-poem">\n      <p><em>{poem_content}</em></p>\n    </blockquote>')
            continue
            
        # Check for scene break
        if p_str in ['……', '…', '---', '***']:
            html_paragraphs.append('<p class="scene-break">……</p>')
            continue
            
        # Process inline markdown
        # 1. Bold: **text**
        p_formatted = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', p_str)
        # 2. Italic: *text*
        p_formatted = re.sub(r'\*(.+?)\*', r'<em>\1</em>', p_formatted)
        
        # Replace intra-paragraph single newlines with space
        p_formatted = p_formatted.replace('\n', ' ')
        
        html_paragraphs.append(f'<p>{p_formatted}</p>')
        
    return "\n    ".join(html_paragraphs)

# Extract chapters
c_splits = re.split(r'\n## (Chapter \d+:[^\n]+)\n', full_text)

chapters = []
for i in range(1, len(c_splits), 2):
    header = c_splits[i] # e.g. "Chapter 1: Though the Flesh..."
    body = c_splits[i+1]
    
    num_match = re.match(r'Chapter (\d+):\s*(.+)', header)
    num = int(num_match.group(1))
    raw_title = num_match.group(2).strip()
    title = capitalize_title(raw_title)
    
    words = len(body.split())
    mins = max(1, round(words / 220))
    
    chapters.append({
        "num": num,
        "title": title,
        "body": body,
        "words": words,
        "mins": mins,
        "file": f"/home/user/reverend-insanity/chapter-{num}.html"
    })

total_chapters = len(chapters)

def make_chapter_html(ch, idx):
    prose_html = parse_markdown_prose(ch["body"])
    
    # Previous Button (Bottom and Top)
    if idx == 0:
        prev_btn_bottom = '<a class="btn btn-ghost" href="index.html#chapters">← Chapters</a>'
        top_prev_btn = '<span class="gamepad-btn prev disabled" aria-disabled="true" title="First Chapter">←</span>'
    else:
        prev_num = chapters[idx - 1]["num"]
        prev_btn_bottom = f'<a class="btn btn-ghost" href="chapter-{prev_num}">← Chapter {prev_num}</a>'
        top_prev_btn = f'<a class="gamepad-btn prev" href="chapter-{prev_num}" title="Previous Chapter: Chapter {prev_num}">←</a>'
        
    # Next Button (Bottom and Top)
    if idx < total_chapters - 1:
        next_num = chapters[idx + 1]["num"]
        next_btn_bottom = f'<a class="btn btn-primary" href="chapter-{next_num}">Chapter {next_num} →</a>'
        top_next_btn = f'<a class="gamepad-btn next" href="chapter-{next_num}" title="Next Chapter: Chapter {next_num}">→</a>'
    else:
        upcoming_num = ch["num"] + 1
        next_btn_bottom = f'<a class="btn btn-primary" aria-disabled="true" style="pointer-events:none;opacity:.45">Chapter {upcoming_num} · In Progress</a>'
        top_next_btn = '<span class="gamepad-btn next disabled" aria-disabled="true" title="No later chapter published yet">→</span>'
        
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Chapter {ch["num"]}: {ch["title"]} — Reverend Insanity | The Omniarch Translation</title>
<meta name="description" content="Chapter {ch["num"]} of Reverend Insanity, translated by The Omniarch. {ch['words']} words · ~{ch['mins']} min read.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,500;1,600&family=Newsreader:ital,opsz,wght@0,6..72,400..600;1,6..72,400..500&family=Noto+Sans+SC:wght@400;500;700;900&family=Playfair+Display:ital,wght@0,700;0,800;1,500;1,700&family=Spectral:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css?v=20260923Q">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" href="logo-circle.png" type="image/png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<script>
  (function() {{
    var saved = localStorage.getItem('theme');
    if (saved === 'obsidian' || (!saved && window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches)) {{
      document.documentElement.setAttribute('data-theme', 'obsidian');
    }}
    var f = localStorage.getItem('readerFont');
    if (f === 'opendyslexic' || f === 'cormorant' || f === 'newsreader' || f === 'spectral') {{
      document.documentElement.className = (document.documentElement.className + ' rf-' + f).trim();
    }}
  }})();
</script>
</head>
<body>

<div class="progress"></div>

<nav class="nav">
  <div class="nav-inner">
    <a class="nav-logo" href="index.html">
      <img class="nav-logo-img" src="logo-circle.png" width="32" height="32" alt="The Omniarch Translation logo">
      <span class="wordmark"><span class="brand-name">The Omniarch</span><span class="brand-sub"> Translation</span></span>
    </a>
    <div class="nav-actions">
      <button class="theme-toggle" id="themeToggle" aria-label="Toggle theme" title="Toggle theme">
        <svg class="icon-moon" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
        <svg class="icon-sun" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>
        <span class="toggle-text" id="themeToggleText">Dark theme</span>
      </button>
      <button class="nav-burger" aria-label="Menu">☰</button>
    </div>
    <ul class="nav-links">
      <li><a href="index.html">Home</a></li>
      <li><a href="index.html#chapters">Chapters</a></li>
      <li><a href="about">About</a></li>
      <li><a href="support">Support</a></li>
      <li><a href="https://discord.gg/UgwTKn4sQf" target="_blank" rel="noopener">Discord</a></li>
    </ul>
  </div>
</nav>

<header class="reader-head">
  <h1>Chapter {ch["num"]}</h1>
  <p class="ch-title">{ch["title"]}</p>
  <div class="ch-meta-row">
    <span class="ch-meta-item">Volume 1 · Demonic Nature Never Changes</span>
    <span class="ch-meta-sep">·</span>
    <span class="ch-meta-item">Translator: <strong>The Omniarch</strong></span>
    <span class="ch-meta-sep">·</span>
    <span class="ch-meta-item">{ch["words"]:,} words</span>
    <span class="ch-meta-sep">·</span>
    <span class="ch-meta-item">~{ch["mins"]} min read</span>
  </div>
  <div class="reader-toolbar">
    <div class="font-ctrls" aria-label="Reading controls">
      <button class="font-btn" id="fontDec" title="Decrease font size" aria-label="Decrease font size">A−</button>
      <button class="font-btn" id="fontInc" title="Increase font size" aria-label="Increase font size">A+</button>
      <span class="font-picker-wrap">
        <button class="font-btn" id="fontPickerBtn" title="Choose typeface" aria-label="Choose typeface" aria-haspopup="true" aria-expanded="false">Aa</button>
        <div class="font-panel" id="fontPanel" role="menu" aria-label="Reader typeface">
          <div class="fp-label">Typeface</div>
          <button class="font-option" data-font="opendyslexic" role="menuitem" type="button">
            <span class="fo-name fo-opendyslexic">OpenDyslexic</span>
            <span class="fo-desc">Friend's pick · dyslexia-friendly</span>
            <span class="fo-sample fo-opendyslexic">The Spring Autumn Cicada stirred.</span>
          </button>
          <button class="font-option" data-font="inter" role="menuitem" type="button">
            <span class="fo-name fo-inter">Inter</span>
            <span class="fo-desc">Clean modern sans</span>
            <span class="fo-sample fo-inter">The Spring Autumn Cicada stirred.</span>
          </button>
          <button class="font-option" data-font="cormorant" role="menuitem" type="button">
            <span class="fo-name fo-cormorant">Cormorant Garamond</span>
            <span class="fo-desc">Elegant high-contrast serif</span>
            <span class="fo-sample fo-cormorant">The Spring Autumn Cicada stirred.</span>
          </button>
          <button class="font-option" data-font="newsreader" role="menuitem" type="button">
            <span class="fo-name fo-newsreader">Newsreader</span>
            <span class="fo-desc">Crisp editorial serif</span>
            <span class="fo-sample fo-newsreader">The Spring Autumn Cicada stirred.</span>
          </button>
          <button class="font-option" data-font="spectral" role="menuitem" type="button">
            <span class="fo-name fo-spectral">Spectral</span>
            <span class="fo-desc">Warm literary serif</span>
            <span class="fo-sample fo-spectral">The Spring Autumn Cicada stirred.</span>
          </button>
        </div>
      </span>
    </div>
    <div class="reader-gamepad" aria-label="Chapter navigation">
      {top_prev_btn}
      {top_next_btn}
    </div>
  </div>
</header>

<main class="chapter-body">
  <div class="prose">
    {prose_html}
  </div>
  <div class="end-mark" aria-hidden="true">◆</div>
</main>

<nav class="chapter-nav">
  {prev_btn_bottom}
  {next_btn_bottom}
</nav>

<footer>
  <div class="footer-inner">
    <span><img class="f-logo" src="logo-circle.png" width="18" height="18" alt="">The Omniarch Translation</span>
    <div class="footer-socials">
      <a href="support.html">Support Us</a>
      <span class="sep">·</span>
      <a href="https://discord.gg/UgwTKn4sQf" target="_blank" rel="noopener">Discord</a>
      <span class="sep">·</span>
      <a href="https://www.youtube.com/@GodofPeakFiction" target="_blank" rel="noopener">YouTube</a>
      <span class="sep">·</span>
      <a href="https://www.tiktok.com/@GodOfPeakFiction" target="_blank" rel="noopener">TikTok</a>
    </div>
    <span>© <span class="year">2026</span></span>
  </div>
</footer>

<script src="app.js?v=20260923Q"></script>
</body>
</html>
"""

for idx, ch in enumerate(chapters):
    html = make_chapter_html(ch, idx)
    with open(ch["file"], 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Generated {ch['file']} (Chapter {ch['num']}: {ch['title']})")

# Update chapter-001 and chapter-002 for legacy compatibility
shutil.copy2('/home/user/reverend-insanity/chapter-1.html', '/home/user/reverend-insanity/chapter-001.html')
shutil.copy2('/home/user/reverend-insanity/chapter-2.html', '/home/user/reverend-insanity/chapter-002.html')

print("Build complete!")
