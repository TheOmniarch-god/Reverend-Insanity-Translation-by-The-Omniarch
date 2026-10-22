import json, subprocess, sys, re
from collections import Counter
sys.path.insert(0, '/home/user/tmp')
from rows044 import ROWS
from witness_lib import chapter_title
BASE = '/home/user/editorial/sequential-review'
BATCH = '044'
START = 826
CH0, CH1 = 1056, 1105

# 1. defs for collation
defs = [{'row': i + 1, 'ch': r[0], 'orig': r[2], 'cand': r[3]} for i, r in enumerate(ROWS)]
json.dump(defs, open('/home/user/tmp/defs-044.json', 'w'), ensure_ascii=False, indent=1)
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

# 2. chapter title check against witness
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
print('title mismatches:', title_mismatch)
para_total = sum(len(c['paragraphs']) for c in src)

# 3. report
L = []
A = L.append
A('# Batch 044 — Chapters 1056–1105 (sequential source review)')
A('')
A('Status: **source reading complete (1056–1105)**. Notes: `editorial/sequential-review/batch-044-notes/reading-notes-1056-1105.md`. This report is a candidate list only. Nothing here is approved, applied, or published, and no Chinese source has been changed.')
A('')
A(f'Source check: `batch-044-source.json` ({len(src)} chapters, {para_total:,} paragraphs). Every row token was found in its stated paragraph by the collation step ({len(ROWS)} rows, 0 misses).')
A('')
A(f'Produced: proposal-ledger entries SR-{START} to SR-{START+len(ROWS)-1} ({len(ROWS)} rows), this report with a DOCX, a QA file, and witness collation against Hetushu book 7640 (`witness-collation-044.json`) for all 50 chapters. Chapter titles checked against the witness pages: {len(src)-len(title_mismatch)} of {len(src)} match.')
A('')
A('Confidence: H = high, H–M, M–H, M, L–M, L. "Action" is what the editor should decide. Nothing is applied.')
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
A('- **调教方源 → 调教方正** (1066 p16, 1084 p53, 1088 p49): three hits, same pattern (the training is aimed at 方正). Decide once; the three rows depend on each other.')
A('- **四面八法 → 四面八方**: now six occurrences (848 p2, 904 p75, 967 p65, 1004 p19, 1050 p14, 1096 p55). 1096 p55 is added in this batch as SR-856 and linked to SR-809 and SR-822–825; apply as one set.')
A('- **特意 (non-ordinary sense)**: 1075 p24, 1079 p82 (this batch) and 1052 p50 (batch 043). 特意 is common in its normal sense (x59), so these are not typos to fix one by one. One whole-novel rule is needed (term, or error to repair in each place).')
A('- **五百年前世 vs 五百年前前世** (1058 p53; 1004 p110 in batch 042): same token, same fix.')
A('')
A('## Items withdrawn or dropped during this batch')
A('')
A('- 1072 p17 眉如淡柳龙烟: unusual but readable; no proposal.')
A('- 1089 p72 眼界却有: awkward but readable; no proposal.')
A('- 1100 p69 目标之我: read as deliberate phrasing; no proposal.')
A('- 1080 p4 态度可掬: normal idiom; no proposal.')
A('- 1099 p40 前世五百年 and 1093 p5 五百年前世: consistent usage (supports 五百年前世); no proposal.')
A('- 1105 p1–109: no proposal beyond the rows above.')
A('')
A('## Deferred and notes (no row)')
A('')
A('- 1083 p23 八成 (the "two of eight" resource share): belongs to the deferred 六成/八成 group the user chose to defer. No decision here.')
A('')
A('## Known limits')
A('')
A('- Single-token repairs are local to the stated paragraph. Before applying any repair, check the same token across the batch sources (done for each row in the rationale column).')
A('- Queries (no edit proposed): 1057 p51 开口握紧; 1068 p60 反映在外面; 1075 p24 and 1079 p82 特意; 1093 p8 全身的肉身就是优秀; 1098 p78 半年前.')
A('- Temporal items: 1098 p78 半年前 (also 915 p51). Whole-novel temporal reconciliation is still required.')
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
open(f'{BASE}/Batch-044-Chapters-1056-1105.md', 'w', encoding='utf-8').write('\n'.join(L) + '\n')

# 4. QA
cc = Counter(r[4] for r in ROWS)
qa = {'batch': '044', 'chapters': '1056-1105', 'chapter_count': len(src),
      'source_check': f'batch-044-source.json ({len(src)} chapters, {para_total:,} paragraphs). Every row token verified present in its stated paragraph (0 misses).',
      'reading_status': 'complete (1056-1105); notes in batch-044-notes/reading-notes-1056-1105.md',
      'report_rows': len(ROWS), 'confidence_counts': dict(cc),
      'approved': 0, 'applied': 0, 'source_edits': 0,
      'witness_collation': f'Hetushu book 7640 automated token-level comparison (witness-collation-044.json); {len(src)} chapter pages fetched and title-checked ({len(src)-len(title_mismatch)} match).',
      'witness_results': dict(cnt),
      'workbook_rows': 'added (chapter completion and paragraph register 1056-1105; ledger sheet SR-826 to SR-856)',
      'ledger_entries': f'SR-{START} to SR-{START+len(ROWS)-1}',
      'docx': 'Batch-044-Chapters-1056-1105.docx',
      'known_limits': [
          'Set-wide 调教方正 (1066 p16, 1084 p53, 1088 p49) and 四面八方 (SR-809, SR-822–825, SR-856) decisions outstanding.',
          '特意 non-ordinary usage (1052 p50, 1075 p24, 1079 p82): one whole-novel rule needed.',
          '1083 p23 八成 belongs to the deferred 六成/八成 group; no row.',
          'Queries carry no edit: 1057 p51, 1068 p60, 1075 p24, 1079 p82, 1093 p8, 1098 p78.',
          'Whole-novel temporal reconciliation outstanding (1098 p78 半年前).']}
json.dump(qa, open(f'{BASE}/batch-044-qa.json', 'w'), ensure_ascii=False, indent=1)

# 5. ledger
Lg = json.load(open(f'{BASE}/proposal-ledger.json'))
ids = {e['id'] for e in Lg}
assert f'SR-{START}' not in ids, 'ledger already has batch 044 ids'
new = []
for i, r in enumerate(ROWS):
    ch, pa, orig, cand, conf, cat, action, rat, deps = r
    new.append({'id': f'SR-{START+i}', 'category': cat,
                'locations': [{'chapter': ch, 'paragraph': pa, 'file': '', 'reference_text': f'{ch} p{pa}'}],
                'recommended_action': f'{action} (batch 044, row {i+1}; source token: {orig})',
                'rationale': f'{rat} Confidence {conf}.',
                'confidence': conf, 'status': 'Open; unapproved, unapplied',
                'dependencies': deps,
                'publication_status': 'HOLD: complete-corpus reading and global reconciliation outstanding',
                'witness_collation': f'Hetushu 7640 collation: {wlabel(i+1)}',
                'approved': False, 'applied': False})
Lg.extend(new)
json.dump(Lg, open(f'{BASE}/proposal-ledger.json', 'w'), ensure_ascii=False, indent=1)
json.dump(new, open(f'{BASE}/ledger-new-044.json', 'w'), ensure_ascii=False, indent=1)
print('rows', len(ROWS), 'ledger total', len(Lg), 'last', Lg[-1]['id'])
print(dict(cnt))
print(dict(cc))
