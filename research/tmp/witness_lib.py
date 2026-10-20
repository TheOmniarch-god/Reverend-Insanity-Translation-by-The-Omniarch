import re, json, os
W = '/tmp/witness'
WM = re.compile(r'[A-Za-z0-9ａ-ｚＡ-Ｚ０-９•·．.~`:/_\-\\\s＼]+')
def chapter_title(ch):
    s = open(f'{W}/ch{ch}.html', encoding='utf-8', errors='ignore').read()
    m = re.search(r'<h2 class="h2">(第[^<]*)</h2>', s)
    return m.group(1) if m else None
def paragraphs(ch):
    s = open(f'{W}/ch{ch}.html', encoding='utf-8', errors='ignore').read()
    i = s.find('id="content"')
    j = s.find('</div>\n', i) if i >= 0 else -1
    body = s[i:] if i >= 0 else s
    out = []
    for m in re.finditer(r'<div>(.*?)</div>', body, re.S):
        t = re.sub(r'<[^>]+>', '', m.group(1))
        t = t.replace('&nbsp;', ' ').replace('&quot;', '"').replace('&amp;', '&')
        out.append(t)
    return out
def norm(t):
    t = WM.sub('', t)
    return re.sub(r'[\s“”"‘’\'…\.。，,、！!？?：:；;《》（）()\-—]', '', t)
