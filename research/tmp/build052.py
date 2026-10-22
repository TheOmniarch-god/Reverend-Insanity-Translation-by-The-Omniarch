import json, subprocess, sys, re, os
from collections import Counter
sys.path.insert(0, '/home/user/tmp')
from rows052 import ROWS
from witness_lib import chapter_title
BASE = '/home/user/editorial/sequential-review'
BATCH = '052'
START = 1261
CH0, CH1 = 1456, 1505

defs = [{'row': i + 1, 'ch': r[0], 'orig': r[2], 'cand': (None if r[5].startswith(('Query', 'Decision')) else r[3])} for i, r in enumerate(ROWS)]
json.dump(defs, open('/home/user/tmp/defs-052.json', 'w'), ensure_ascii=False, indent=1)
res = subprocess.run(['python3', '/home/user/tmp/collate.py', BATCH], capture_output=True, text=True)
if res.returncode != 0:
    print(res.stderr); sys.exit(1)
wit = json.load(open(f'{BASE}/witness-collation-{BATCH}.json'))
wmap = {w['row']: w for w in wit}

def wlabel(i):
    w = wmap.get(i)
    if not w: return 'not collated'
    r = w.get('result', '')
    if r.startswith('witness copies'): return 'copies source (neutral)'
    if r.startswith('witness shows'): return 'shows candidate (web copy only)'
    return 'context not found'

missing = [w for w in wit if w.get('source_hits', 0) == 0]
if missing:
    print('TOKENS NOT FOUND:', [(m['row'], m['ch'], m['orig']) for m in missing]); sys.exit(1)

src = json.load(open(f'{BASE}/batch-{BATCH}-source.json'))
assert [c['corpus_chapter'] for c in src] == list(range(CH0, CH1 + 1))
def tkey(t):
    t = re.sub(r'^第[^节章]+[节章][：:\s]*', '', t or '')
    return re.sub(r'\s', '', t)
title_mismatch = []
for c in src:
    wt = chapter_title(c['corpus_chapter']) or ''
    if tkey(wt) != tkey(c['title']):
        title_mismatch.append((c['corpus_chapter'], c['title'], wt))
para_total = sum(len(c['paragraphs']) for c in src)
char_total = sum(len(p) for c in src for p in c['paragraphs'])

L = []; A = L.append
A('# Batch 052 — Chapters 1456–1505 (sequential source review)')
A('')
A('Status: **source reading complete (1456–1505)**. Reading flags: `tmp/b052-flags.txt` (working file). This report is a candidate list only. Nothing here is approved, applied, or published, and no Chinese source has been changed.')
A('')
A(f'Source check: `batch-052-source.json` ({len(src)} chapters, {para_total:,} paragraphs, {char_total:,} characters). Every row token was found in its stated paragraph ({len(ROWS)} rows, 0 misses).')
A('')
A(f'Produced: proposal-ledger entries SR-{START} to SR-{START+len(ROWS)-1} ({len(ROWS)} rows), this report with a DOCX, a QA file, and witness collation against Hetushu book 7640 (`witness-collation-052.json`) for all 50 chapters. Chapter titles checked against the witness pages: {len(src)-len(title_mismatch)} of {len(src)} match.')
A('')
A('Confidence: H = high, H–M, M–H, M, L–M, L, with a numeric score in brackets. "Action" is what the editor should decide. Nothing is applied.')
A('')
A('**Correction to batch 051 (row 46, 1435 p49):** the earlier proposal to change 我运真传 to 己运真传 is withdrawn. 巨阳真传 names 我运真传 in the same paragraph, and 1482 p22 in this batch names it again. Status is now Query (ledger SR-1240 updated). See the batch 051 report correction note.')
A('')
A('## Proposed review items')
A('')
A('| # | Chapter / para | Source reading | Proposed action | Rationale | Confidence | Dependencies | Witness |')
A('|---|---|---|---|---|---|---|---|')
for i, r in enumerate(ROWS, 1):
    ch, pa, orig, cand, conf, cat, action, rat, deps = r
    A(f'| {i} | {ch} p{pa} | {orig} | {action} | {rat} | {conf} | {deps} | {wlabel(i)} |')
A('')
A('## Set-wide and term decisions (one decision each, not per line)')
A('')
A('- **惨白亏输 / 惨败亏输**: 1456 p4 (decision row, query). 惨白亏 x2 (1369 p21, 1456 p4); 惨败亏 x1 (1334 p72). Check 1334 p72 before deciding.')
A('- **至尊仙躯 → 至尊仙体**: 1479 p4 (decision row, proposed). 至尊仙躯 x5 (1371 p19 batch 050; 1448 p2, p23, p24 batch 051; 1479 p4); 至尊仙体 x82. Decide once; batch 051 entries cover 1448.')
A('- **不以为杵 / 不以为忤**: 1496 p29 (decision row, query). 不以为杵 x4 (1194 p48, 1263 p41, 1333 p69, 1496 p29); 不以为忤 x0. Corpus form is consistent; idiom check for the set decision.')
A('- **得走 → 拿走**: 1461 p46 (row above); 1130 p47 (batch 045). 得走 x2. Decide with 1130 p47 before editing either.')
A('- **石宗 / 石忠**: 1475 p13 (row above) covers the scene. 石宗 is a real different character (太上大长老) in 1143, 1146, 1149 and 1459; do not change those.')
A('- **秦百胜 / 秦百合**: 1483 p54 (row above). 秦百胜 x630 is a different established name; do not change those occurrences.')
A('- **我运真传**: 1435 p49 (batch 051, now query) and 1482 p22 (this batch, note). Both name the Ju-Yang inheritance. 己运真传 x10 is a separate name; confirm both before any change.')
A('- **特意** (1462 p52 is a new instance; 特意 x102; set items 1052 p50, 1075 p24, 1079 p82 from batch 044). No new row; keep decision with the batch 044 set item.')
A('- **黑菟** (1464 p53; 黑菟 x70 in 1352). Consistent; no row.')
A('- **Carried-forward set decisions** (not repeated here): 六成/八成 (deferred); 逆流河/逆流护身印 (1486 p36 quoted speech, set item); 见面曾相识/见面似相识 (1485 p72 use of 见面曾相识 with no proposal).')
A('')
A('## Dropped during reading (not proposed)')
A('')
A('- 1466–1470 毛民蛊仙: 毛民 x774, established term.')
A('- 1470 p49 百八十奴杀招: 百八十奴 x26, established.')
A('- 1468 p7 如厦 (高耸如厦): plausible image; no row.')
A('- 1481 p38 估料 (×8 across corpus) and 1480 p31 estimates: 估料 is established; not a row.')
A('- 1502 p55 准大师一级: 准大师 x17, established term.')
A('- 1462 p34 毛民蛊仙: term, no row.')
A('- 1476 p17, 1483 p9, 1479 p50 etc. were kept as rows where the corpus shows a single slip.')
A('')
A('## Known limits')
A('')
A('- Single-token repairs are local to the stated paragraph. Each row was checked against the batch sources for the same token (0 misses; see rationale column).')
A('- Corpus counts use the batch source files; earlier chapters (1–685) are not in the batch sources, so a count of 1 may be a true single occurrence within this range.')
A('- Queries (no edit proposed): 1457 p54, 1460 p40, 1464 p42, 1471 p63, 1471 p64, 1480 p53, 1481 p38, plus decisions 1456 p4 and 1496 p29.')
A('- Several repairs rest on sense judgement (1465 p18, 1468 p50, 1476 p50, 1478 p63, 1487 p15, 1504 p17). Confirm each sentence before applying.')
A('- 1475 p13 is a multi-paragraph name change; the row verifies p13 only. Other paragraphs (p16–p44) are listed in the row action.')
A('- Witness copy is for reference only. A witness difference is web-copy only, not authority.')
A('')
A('## Witness summary')
A('')
cnt = Counter(w.get('result', 'not collated') for w in wit)
for k, v in sorted(cnt.items(), key=lambda x: -x[1]):
    A(f'- {k}: {v}')
A('')
A(f'Chapter title check: {len(src)-len(title_mismatch)} of {len(src)} match' + ('' if not title_mismatch else f'; mismatches: {title_mismatch}'))
A('')
open(f'{BASE}/Batch-052-Chapters-1456-1505.md', 'w', encoding='utf-8').write('\n'.join(L) + '\n')

cc = Counter(r[4].split(' ')[0] for r in ROWS)
qa = {'batch': '052', 'chapters': '1456-1505', 'chapter_count': len(src),
      'source_check': f'batch-052-source.json ({len(src)} chapters, {para_total:,} paragraphs, {char_total:,} characters). Every row token verified present in its stated paragraph (0 misses).',
      'reading_status': 'complete (1456-1505); flags in tmp/b052-flags.txt',
      'report_rows': len(ROWS), 'confidence_counts': dict(cc),
      'approved': 0, 'applied': 0, 'source_edits': 0,
      'witness_collation': f'Hetushu book 7640 automated token-level comparison (witness-collation-052.json); {len(src)} chapter pages fetched and title-checked ({len(src)-len(title_mismatch)} match).',
      'witness_results': dict(cnt),
      'workbook_rows': 'added (chapter completion and paragraph register 1456-1505; ledger sheet SR-1261 onward)',
      'ledger_entries': f'SR-{START} to SR-{START+len(ROWS)-1}',
      'docx': 'Batch-052-Chapters-1456-1505.docx',
      'corrections': ['Batch 051 row 46 (1435 p49, 我运真传 -> 己运真传) withdrawn; now Query (SR-1240).'],
      'known_limits': ['Set-wide decisions: 惨白亏输; 至尊仙躯; 不以为杵; 得走; 我运真传; 特意; 黑菟.',
                       'Queries carry no edit: 1457 p54, 1460 p40, 1464 p42, 1471 p63, 1471 p64, 1480 p53, 1481 p38.']}
json.dump(qa, open(f'{BASE}/batch-052-qa.json', 'w'), ensure_ascii=False, indent=1)

Lg = json.load(open(f'{BASE}/proposal-ledger.json'))
ids = {e['id'] for e in Lg}
assert f'SR-{START}' not in ids, 'ledger already has batch 052 ids'
new = []
for i, r in enumerate(ROWS):
    ch, pa, orig, cand, conf, cat, action, rat, deps = r
    new.append({'id': f'SR-{START+i}', 'category': cat,
                'locations': [{'chapter': ch, 'paragraph': pa, 'file': '', 'reference_text': f'{ch} p{pa}'}],
                'recommended_action': f'{action} (batch 052, row {i+1}; source token: {orig})',
                'rationale': f'{rat} Confidence {conf}.',
                'confidence': conf, 'status': 'Open; unapproved, unapplied',
                'dependencies': deps,
                'publication_status': 'HOLD: complete-corpus reading and global reconciliation outstanding',
                'witness_collation': f'Hetushu 7640 collation: {wlabel(i+1)}',
                'approved': False, 'applied': False})
Lg.extend(new)
json.dump(Lg, open(f'{BASE}/proposal-ledger.json', 'w'), ensure_ascii=False, indent=1)
json.dump(new, open(f'{BASE}/ledger-new-052.json', 'w'), ensure_ascii=False, indent=1)
print('rows', len(ROWS), 'ledger total', len(Lg), 'last', Lg[-1]['id'])
print(dict(cnt)); print(dict(cc))
print('title mismatches', title_mismatch)
