import subprocess, re, html, json
from pathlib import Path
r = Path('/home/user/editorial/sequential-review')
out = r/'fact-check-029'
b = json.loads((r/'batch-029-source.json').read_text())
res = {}
for c in b:
    n = c['corpus_chapter']
    p = out/f'ch{n}-hetushu.html'
    url = f'https://www.hetushu.com/book/7640/{5345238+n}.html'
    subprocess.run(['curl','-sL','-A','Mozilla/5.0','--max-time','25',url,'-o',str(p)],check=True)
    t = p.read_text(encoding='utf-8', errors='ignore')
    body = re.search(r'<div[^>]*id="content"[^>]*>(.*?)</div>', t, re.S)
    raw = body.group(1) if body else t
    raw = re.sub(r'<br\s*/?>', '\n', raw)
    raw = re.sub(r'</p>', '\n', raw)
    txt = html.unescape(re.sub(r'<[^>]+>', '', raw))
    lines = [l.strip() for l in txt.split('\n') if l.strip()]
    (out/f'ch{n}-normalized.txt').write_text('\n'.join(lines), encoding='utf-8')
    epub = c['paragraphs']
    eset = set(epub)
    matched = sum(1 for l in lines if l in eset)
    res[n] = {'witness_lines': len(lines), 'epub_paras': len(epub), 'exact_matches': matched}
    print(n, res[n], flush=True)
(out/'collation-summary.json').write_text(json.dumps(res, ensure_ascii=False, indent=1))
