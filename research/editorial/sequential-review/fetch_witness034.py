import subprocess, re, html, json
from pathlib import Path
r = Path(__file__).parent
out = r/'fact-check-034'
WM = re.compile(r'https?://\S*|[wｗ][wｗ.\s]*[hｈ][eｅ][tｔ][uｕ][sｓ][hｈ][uｕ][^\u4e00-\u9fff]*|和\W{0,3}图\W{0,3}书|[\*\-_•|.]{0,2}m?\.?hetushu\S*|[a-zA-Zｗｈｅｔｕｓｃｏｍ.•\*\-_]{2,}\.?com\.?', re.I)
srcs = json.loads((r/'batch-034-source.json').read_text())
res = {}
for c in srcs:
    n = c['corpus_chapter']
    p = out/f'ch{n}-hetushu.html'
    if not p.exists() or p.stat().st_size < 1000:
        subprocess.run(['curl','-sL','-A','Mozilla/5.0','--max-time','25',f'https://www.hetushu.com/book/7640/{5345238+n}.html','-o',str(p)], check=False)
    t = p.read_text(encoding='utf-8', errors='ignore')
    i = t.find('id="content"'); seg = t[i:] if i >= 0 else t
    j = seg.find('</html>'); seg = seg[:j] if j > 0 else seg
    lines = [html.unescape(re.sub(r'<[^>]+>', '', m)).strip() for m in re.findall(r'<div>(.*?)</div>', seg, re.S)]
    lines = [l for l in lines if l]
    (out/f'ch{n}-normalized.txt').write_text('\n'.join(lines), encoding='utf-8')
    clean = [WM.sub('', l) for l in lines]; clean = [l for l in clean if l]
    eset = set(c['paragraphs'])
    matched_clean = sum(1 for l in clean if l in eset)
    res[n] = {'witness_lines': len(lines), 'epub_paras': len(c['paragraphs']), 'exact_matches_after_watermark_strip': matched_clean,
              'agreement_after_watermark_strip': round(matched_clean/len(c['paragraphs']),3)}
(out/'collation-summary.json').write_text(json.dumps(res, ensure_ascii=False, indent=1))
ag = [v['agreement_after_watermark_strip'] for v in res.values()]
print('chapters', len(res), 'min', min(ag), 'mean', round(sum(ag)/len(ag),3), 'lowest', sorted(res.items(), key=lambda kv: kv[1]['agreement_after_watermark_strip'])[:3])
