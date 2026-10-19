import json, re, difflib
from pathlib import Path
r = Path(__file__).parent
WM = re.compile(r'https?://\S*|[wｗ][wｗ.\s]*[hｈ][eｅ][tｔ][uｕ][sｓ][hｈ][uｕ][^\u4e00-\u9fff]*|和\W{0,3}图\W{0,3}书|[\*\-_•|.]{0,2}m?\.?hetushu\S*|[a-zA-Zｗｈｅｔｕｓｃｏｍ.•\*\-_]{2,}\.?com\.?', re.I)
srcs = {c['corpus_chapter']: c for n in (23,24,25) for c in json.loads((r/f'batch-0{n}-source.json').read_text())}
led = json.loads((r/'proposal-ledger.json').read_text())
out = []
for v in led:
    locs = [l for l in v['locations'] if 426 <= l['chapter'] <= 485]
    if not locs or v['status'].startswith('Withdrawn'): continue
    pass
    for l in locs[:1]:
        ch, pn = l['chapter'], l['paragraph']
        e = srcs[ch]['paragraphs'][pn-1]
        w = [WM.sub('', x) for x in (r/f'fact-check-023-025/ch{ch}-normalized.txt').read_text(encoding='utf-8').split('\n')]
        w = [x for x in w if x]
        best = difflib.get_close_matches(e, w, n=1, cutoff=0.5)
        if best and best[0] == e: st = 'WITNESS EXACT (same as source)'
        elif best:
            sm = difflib.SequenceMatcher(None, e, best[0])
            ops = [(t, e[a1:a2], best[0][b1:b2]) for t,a1,a2,b1,b2 in sm.get_opcodes() if t!='equal']
            st = 'DIFF ' + '; '.join(f"{t} {a!r}->{b!r}" for t,a,b in ops[:3])
        else: st = 'NO WITNESS LINE'
        out.append((v['id'], f'{ch}p{pn}', v['status'][:25], v['recommended_action'][:60], st))
for o in out: print(*o, sep=' | ')
print('total', len(out))
