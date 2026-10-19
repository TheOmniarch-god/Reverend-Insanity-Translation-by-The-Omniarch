import json, re, difflib
from pathlib import Path
r = Path(__file__).parent
WM = re.compile(r'https?://\S*|[wｗ][wｗ.\s]*[hｈ][eｅ][tｔ][uｕ][sｓ][hｈ][uｕ][^\u4e00-\u9fff]*|和\W{0,3}图\W{0,3}书|[\*\-_•|.]{0,2}m?\.?hetushu\S*|[a-zA-Zｗｈｅｔｕｓｃｏｍ.•\*\-_]{2,}\.?com\.?', re.I)
srcs = [c for n in (30, 31, 32) for c in json.loads((r/f'batch-0{n}-source.json').read_text())]
out = {}
for c in srcs:
    n = c['corpus_chapter']
    w = (r/f'fact-check-030-032/ch{n}-normalized.txt').read_text(encoding='utf-8').split('\n')
    w = [WM.sub('', l) for l in w]
    w = [l for l in w if l]
    e = c['paragraphs']
    wset = set(w)
    diffs = []
    for i, p in enumerate(e, 1):
        if p in wset: continue
        cand = difflib.get_close_matches(p, w, n=1, cutoff=0.6)
        if not cand:
            diffs.append((i, 'NO-MATCH', p[:60], '')); continue
        sm = difflib.SequenceMatcher(None, p, cand[0])
        ops = [(t, p[a1:a2], cand[0][b1:b2]) for t, a1, a2, b1, b2 in sm.get_opcodes() if t != 'equal']
        diffs.append((i, 'DIFF', ops, ''))
    out[n] = diffs
    print(n, 'epub', len(e), 'witness', len(w), 'unmatched', len(diffs))
    for d in diffs:
        print('   ', d[0], d[1], (d[2] if d[1]=='NO-MATCH' else d[2][:6]))
Path(r/'fact-check-030-032/unmatched-after-watermark-strip.json').write_text(json.dumps({k: [list(map(str, x)) for x in v] for k, v in out.items()}, ensure_ascii=False, indent=1))
