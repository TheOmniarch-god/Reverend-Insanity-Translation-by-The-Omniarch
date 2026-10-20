import json, sys, re
sys.path.insert(0,'/home/user/tmp')
from witness_lib import paragraphs, norm, W
BATCH = sys.argv[1]
DEFS = json.load(open(f'/home/user/tmp/defs-{BATCH}.json'))
src = {c['corpus_chapter']: c['paragraphs'] for c in json.load(open(f'/home/user/editorial/sequential-review/batch-{BATCH}-source.json'))}
out = []
for d in DEFS:
    ch, orig, cand, row = d['ch'], d['orig'], d.get('cand'), d['row']
    paras = src[ch]
    hits = [i for i,p in enumerate(paras) if orig in p]
    rec = {'row': row, 'ch': ch, 'orig': orig, 'cand': cand, 'source_hits': len(hits)}
    if not hits:
        rec['status'] = 'SOURCE TOKEN NOT FOUND'; out.append(rec); continue
    p = paras[hits[0]]
    k = p.index(orig)
    win_o = p[max(0,k-6):k+len(orig)+6]
    if cand:
        pc = p[:k] + cand + p[k+len(orig):]
        win_c = pc[max(0,k-6):k+len(cand)+6]
    else:
        win_c = None
    wit = ''.join(norm(t) for t in paragraphs(ch))
    no, nc = norm(win_o), (norm(win_c) if win_c else None)
    rec['witness_has_original'] = no in wit
    rec['witness_has_candidate'] = (nc in wit) if nc else None
    if rec['witness_has_original']: rec['result'] = 'witness copies source wording'
    elif nc and rec['witness_has_candidate']: rec['result'] = 'witness shows candidate wording'
    else: rec['result'] = 'context not found in witness (variant, segmentation, or watermark)'
    out.append(rec)
json.dump(out, open(f'/home/user/editorial/sequential-review/witness-collation-{BATCH}.json','w'), ensure_ascii=False, indent=1)
for r in out: print(r['row'], r['ch'], r['orig'], '|', r.get('source_hits'), '|', r.get('result', r.get('status')))
