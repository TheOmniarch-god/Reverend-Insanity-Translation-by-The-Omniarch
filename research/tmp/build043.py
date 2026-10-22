import json, subprocess, sys
from collections import Counter
sys.path.insert(0, '/home/user/tmp')
from rows043 import ROWS
BASE = '/home/user/editorial/sequential-review'
BATCH = '043'
START = 773

# 1. defs for collation
defs = [{'row': i + 1, 'ch': r[0], 'orig': r[2], 'cand': r[3]} for i, r in enumerate(ROWS)]
json.dump(defs, open('/home/user/tmp/defs-043.json', 'w'), ensure_ascii=False, indent=1)
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

# source-token check
missing = [w for w in wit if w.get('source_hits', 0) == 0]
if missing:
    print('TOKENS NOT FOUND:', [(m['row'], m['ch'], m['orig']) for m in missing]); sys.exit(1)

# 2. report
L = []
A = L.append
A('# Batch 043 — Chapters 1006–1055 (sequential source review)')
A('')
A('Status: **source reading complete (1006–1055)**. Notes: `editorial/sequential-review/batch-043-notes/reading-notes-1006-1055.md`. This report is a candidate list only. Nothing here is approved, applied, or published, and no Chinese source has been changed.')
A('')
A('Source check: `batch-043-source.json` (50 chapters, 5,057 paragraphs). Every row token was found in its stated paragraph by the collation step (0 misses).')
A('')
A(f'Produced: proposal-ledger entries SR-{START} to SR-{START+len(ROWS)-1} ({len(ROWS)} rows), this report with a DOCX, a QA file, and witness collation against Hetushu book 7640 (`witness-collation-043.json`) for all 50 chapters. Chapter titles were checked against the witness pages. Witness copies the source wording for most candidates, so it neither confirms nor rejects them; any witness difference is web-copy only.')
A('')
A('Not produced in this pass: workbook rows for 043 and the batch 042 rows (still pending). Whole-novel temporal reconciliation and terminology decisions are outstanding and are not resolved here.')
A('')
A('Confidence: H = high, M–H, M = medium, M–L, L–M, L = low. "Action" is what the editor should decide. Nothing is applied.')
A('')
A('## Proposed review items')
A('')
A('| # | Chapter / para | Source reading | Proposed action | Rationale | Confidence | Dependencies | Witness |')
A('|---|---|---|---|---|---|---|---|')
for i, r in enumerate(ROWS, 1):
    ch, pa, orig, cand, conf, cat, action, rat, deps = r
    A(f'| {i} | {ch} p{pa} | {orig} | {action} | {rat} | {conf} | {deps} | {wlabel(i)} |')
A('')
A('## Items withdrawn or dropped during this batch')
A('')
A('- 1006 p99 宇道 (宇道 x160; 宙道 x407): not a typo; dropped.')
A('- 秦百胜 (x103), 本杰孙 (x7), 鬼不觉 (x66), 一届凡人 (x16, consistent), 境地 (common): dropped as consistent usage.')
A('- 1013 p5 优先 (x46) and 1040 p13 优先一礼: common usage; dropped.')
A('- 1036 p93 "你贱": deliberate pun; no flag.')
A('- 1017 p28 紫嫣的气雾 (紫嫣 x5, 紫烟 x5): low; no proposal.')
A('- 1014 p74 兽人拖肠 repeats p73: style; no proposal.')
A('- 1010 p6 待久了: the other 121 usages are legitimate; the fix is local only.')
A('- 1013 p84 总有炼成: precedent at 311; treated as judgment, not a clear error.')
A('- 1051 p51 见面不相识 (x15): the skill name list in that passage; not an error. 见面似相识 remains pending from batch 041.')
A('')
A('## Known limits')
A('')
A('- Single-token repairs are local to the stated paragraph; before applying any of them, check that no other occurrence of the same error exists in the batch sources.')
A('- Systemic items to handle as one set: 四面八法 (row for 1050 p14): five occurrences within 686–1055 (848 p2, 904 p75, 967 p65, 1004 p19, 1050 p14); earlier batches may already have ledger entries for some of them (check before approval). 戈登 (1050 p43, 1055 p104): same pattern as 982 p44 (repaired in batch 042).')
A('- Queries (no edit proposed yet): 1008 p49 建成无悔; 1041 p10 为难着; 1046 p63 七七四百九十; 1049 p95 有两个毛民粗壮; 1050 p15 晃晃乎; 1054 p83 这才地灾 (also 978 p68).')
A('- Unit note: 1024 p35 三丈就是九米 and 1044 p12 数十亿亩 are conversion notes; they need a global unit policy, not an edit here.')
A('- 1046 p21 第三位位: 位位 appears x34 in the batch sources; check each case before applying a global change.')
A('- 1034 p48 毫无阻碍 wording is pending a choice.')
A('- Temporal items: none new in this batch beyond the cross-references in the dependency column; whole-novel reconciliation is still required.')
A('')
A('## Witness summary')
A('')
cnt = Counter(w.get('result', 'not collated') for w in wit)
for k, v in sorted(cnt.items(), key=lambda x: -x[1]):
    A(f'- {k}: {v}')
A('')
open(f'{BASE}/Batch-043-Chapters-1006-1055.md', 'w', encoding='utf-8').write('\n'.join(L) + '\n')

# 3. QA
cc = Counter(r[4] for r in ROWS)
qa = {'batch': '043', 'chapters': '1006-1055', 'chapter_count': 50,
      'source_check': 'batch-043-source.json (50 chapters, 5,057 paragraphs). Every row token verified present in its stated paragraph (0 misses).',
      'reading_status': 'complete (1006-1055); notes in batch-043-notes/reading-notes-1006-1055.md',
      'report_rows': len(ROWS), 'confidence_counts': dict(cc),
      'approved': 0, 'applied': 0, 'source_edits': 0,
      'witness_collation': 'Hetushu book 7640 automated token-level comparison (witness-collation-043.json); 50 chapter pages fetched and title-checked.',
      'witness_results': dict(cnt),
      'workbook_rows': 'NOT ADDED in this pass',
      'ledger_entries': f'SR-{START} to SR-{START+len(ROWS)-1}',
      'docx': 'Batch-043-Chapters-1006-1055.docx',
      'known_limits': ['Workbook rows not added.', 'Whole-novel temporal reconciliation outstanding.',
                       '四面八法 and 戈登 need one set-wide decision; check earlier ledger coverage.',
                       'Queries (建成无悔, 为难着, 七七四百九十, 有两个毛民粗壮, 晃晃乎, 这才地灾) carry no edit.',
                       '1034 p48 wording pending choice.']}
json.dump(qa, open(f'{BASE}/batch-043-qa.json', 'w'), ensure_ascii=False, indent=1)

# 4. ledger
Lg = json.load(open(f'{BASE}/proposal-ledger.json'))
ids = {e['id'] for e in Lg}
assert f'SR-{START}' not in ids, 'ledger already has batch 043 ids'
new = []
for i, r in enumerate(ROWS):
    ch, pa, orig, cand, conf, cat, action, rat, deps = r
    new.append({'id': f'SR-{START+i}', 'category': cat,
                'locations': [{'chapter': ch, 'paragraph': pa, 'file': '', 'reference_text': f'{ch} p{pa}'}],
                'recommended_action': f'{action} (batch 043, row {i+1}; source token: {orig})',
                'rationale': f'{rat} Confidence {conf}.',
                'confidence': conf, 'status': 'Open; unapproved, unapplied',
                'dependencies': deps,
                'publication_status': 'HOLD: complete-corpus reading and global reconciliation outstanding',
                'witness_collation': f'Hetushu 7640 collation: {wlabel(i+1)}',
                'approved': False, 'applied': False})
Lg.extend(new)
json.dump(Lg, open(f'{BASE}/proposal-ledger.json', 'w'), ensure_ascii=False, indent=1)
json.dump(new, open(f'{BASE}/ledger-new-043.json', 'w'), ensure_ascii=False, indent=1)
print('rows', len(ROWS), 'ledger total', len(Lg), 'last', Lg[-1]['id'])
print(dict(cnt))
print(dict(cc))
