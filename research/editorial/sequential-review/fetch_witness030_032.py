import subprocess, re, html, json
from pathlib import Path
r = Path(__file__).parent
out = r/'fact-check-030-032'
srcs = [c for n in (30, 31, 32) for c in json.loads((r/f'batch-0{n}-source.json').read_text())]
res = {}
for c in srcs:
    n = c['corpus_chapter']
    p = out/f'ch{n}-hetushu.html'
    if not p.exists() or p.stat().st_size < 1000:
        url = f'https://www.hetushu.com/book/7640/{5345238+n}.html'
        subprocess.run(['curl','-sL','-A','Mozilla/5.0','--max-time','25',url,'-o',str(p)], check=False)
    t = p.read_text(encoding='utf-8', errors='ignore')
    i = t.find('id="content"'); seg = t[i:] if i >= 0 else t
    j = seg.find('</html>'); seg = seg[:j] if j > 0 else seg
    lines = [html.unescape(re.sub(r'<[^>]+>', '', m)).strip() for m in re.findall(r'<div>(.*?)</div>', seg, re.S)]
    lines = [l for l in lines if l]
    (out/f'ch{n}-normalized.txt').write_text('\n'.join(lines), encoding='utf-8')
    eset = set(c['paragraphs'])
    matched = sum(1 for l in lines if l in eset)
    res[n] = {'witness_lines': len(lines), 'epub_paras': len(c['paragraphs']), 'exact_matches': matched,
              'agreement': round(matched / len(c['paragraphs']), 3)}
(out/'collation-summary.json').write_text(json.dumps(res, ensure_ascii=False, indent=1))
print('done', len(res))
