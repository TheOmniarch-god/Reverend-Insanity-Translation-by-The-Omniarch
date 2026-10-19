import json, re, difflib
from pathlib import Path
exec(open('diff030_032.py').read().split('srcs =')[0])  # reuse WM regex
r = Path(__file__).parent
srcs = {c['corpus_chapter']: c for n in (30,31,32) for c in json.loads((r/f'batch-0{n}-source.json').read_text())}
led = json.loads((r/'proposal-ledger.json').read_text())
rows = []
for v in led:
    n = int(v['id'][3:])
    if n < 338 or v['status'].startswith('Withdrawn'): continue
    if not v['recommended_action'].startswith(('Repair','Replace','Delete','Insert','Query')): continue
    if v['recommended_action'].startswith('Query'): continue
    for l in v['locations'][:1]:
        ch, pn = l['chapter'], l['paragraph']
        e = srcs[ch]['paragraphs'][pn-1]
        w = [WM.sub('', x) for x in (r/f'fact-check-030-032/ch{ch}-normalized.txt').read_text(encoding='utf-8').split('\n')]
        w = [x for x in w if x]
        best = difflib.get_close_matches(e, w, n=1, cutoff=0.5)
        if best and best[0] == e: st = 'WITNESS EXACT MATCH (same text as source)'
        elif best:
            sm = difflib.SequenceMatcher(None, e, best[0])
            ops = [(t, e[a1:a2], best[0][b1:b2]) for t,a1,a2,b1,b2 in sm.get_opcodes() if t!='equal']
            st = 'DIFF: ' + '; '.join(f"{t} {a!r}->{b!r}" for t,a,b in ops[:3])
        else: st = 'NO WITNESS LINE'
        rows.append((v['id'], f'{ch}p{pn}', v['recommended_action'][:45], st))
for x in rows: print(*x, sep=' | ')
