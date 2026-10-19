import re, html, json
from pathlib import Path
r = Path('/home/user/editorial/sequential-review'); out = r/'fact-check-029'
b = json.loads((r/'batch-029-source.json').read_text())
res = {}
for c in b:
    n = c['corpus_chapter']
    t = (out/f'ch{n}-hetushu.html').read_text(encoding='utf-8', errors='ignore')
    i = t.find('id="content"'); seg = t[i:]
    j = seg.find('</html>'); seg = seg[:j] if j > 0 else seg
    lines = [html.unescape(re.sub(r'<[^>]+>', '', m)).strip() for m in re.findall(r'<div>(.*?)</div>', seg, re.S)]
    lines = [l for l in lines if l]
    (out/f'ch{n}-normalized.txt').write_text('\n'.join(lines), encoding='utf-8')
    eset = set(c['paragraphs'])
    matched = sum(1 for l in lines if l in eset)
    res[n] = {'witness_lines': len(lines), 'epub_paras': len(c['paragraphs']), 'exact_matches': matched,
              'agreement': round(matched / len(c['paragraphs']), 3)}
(out/'collation-summary.json').write_text(json.dumps(res, ensure_ascii=False, indent=1))
print(json.dumps(res))
