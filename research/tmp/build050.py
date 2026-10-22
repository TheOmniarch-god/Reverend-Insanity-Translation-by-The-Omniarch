import json, subprocess, sys, re, os
from collections import Counter
sys.path.insert(0, '/home/user/tmp')
from rows050 import ROWS
from witness_lib import chapter_title
BASE = '/home/user/editorial/sequential-review'
BATCH = '050'
START = 1131
CH0, CH1 = 1356, 1405

defs = [{'row': i + 1, 'ch': r[0], 'orig': r[2], 'cand': (None if r[5].startswith('Query') else r[3])} for i, r in enumerate(ROWS)]
json.dump(defs, open('/home/user/tmp/defs-050.json', 'w'), ensure_ascii=False, indent=1)
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
A('# Batch 050 — Chapters 1356–1405 (sequential source review)')
A('')
A('Status: **source reading complete (1356–1405)**. Reading flags: `tmp/b050-flags.txt` (working file). This report is a candidate list only. Nothing here is approved, applied, or published, and no Chinese source has been changed.')
A('')
A(f'Source check: `batch-050-source.json` ({len(src)} chapters, {para_total:,} paragraphs, {char_total:,} characters). Every row token was found in its stated paragraph ({len(ROWS)} rows, 0 misses).')
A('')
A(f'Produced: proposal-ledger entries SR-{START} to SR-{START+len(ROWS)-1} ({len(ROWS)} rows), this report with a DOCX, a QA file, and witness collation against Hetushu book 7640 (`witness-collation-050.json`) for all 50 chapters. Chapter titles checked against the witness pages: {len(src)-len(title_mismatch)} of {len(src)} match.')
A('')
A('Confidence: H = high, H–M, M–H, M, L–M, L, with a numeric score in brackets. "Action" is what the editor should decide. Nothing is applied.')
A('')
A('Cross-batch references: 1354 p93 灰夜 (batch 049) is the first of the 灰夜 → 夜灰 set, with 1356 p73 and 1366 p56 here. 1044 p12 and 1117 p52–53 (batches 044–045) share the 在一切 pattern with 1358 p77. 1143 p48 and 1147 p40 (batch 045) share the 上级天鹰 variant with 1379 p52. 735 p54 and 1148 p12 (batches 037, 045) share 宝皇天 with 1370 p31. 1246 p53 (batch 047) shares 难以附加 with 1387 p78. 1319 p74 (batch 049) shares 周翔 with 1379 p24. 732 p56 (batch 040) shares 点了点 with 1405 p44.')
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
A('- **灰夜 → 夜灰**: 1354 p93 (batch 049), 1356 p73 and 1366 p56 (rows above). 夜灰 x123; 灰夜 x3. Decide once.')
A('- **在一切 → 在一起**: 1358 p77 (row above), 1044 p12 (batch 044), 1117 p52 and p53 (batch 045). Four uses, all with 堆砌/结合 in this sense. Likely an author habit rather than a single slip; decide once before changing any of the four.')
A('- **上级天鹰 → 上极天鹰**: 1379 p52 (row above), 1143 p48 and 1147 p40 (batch 045). 上极天鹰 x317; 上级天鹰 x3.')
A('- **宝皇天 → 宝黄天**: 1370 p31 (row above), 735 p54 (batch 037), 1148 p12 (batch 045). 宝黄天 x351; 宝皇天 x3.')
A('- **难以附加 → 难以复加**: 1387 p78 (row above) and 1246 p53 (batch 047). 难以复加 x1 (1127 p82).')
A('- **通宵 → 通晓**: 1385 p64 (row above), 1242 p17 (batch 047), 1270 p50 (batch 048). 通晓 x6.')
A('- **纯梦求真仙**: 1376 p49 and p57 (decision row). 纯梦求真体 x87; the short form appears only in this chapter.')
A('- **点了点**: 1405 p44 (query row) and 732 p56 (batch 040). 点了点头 x14. Decide whether the short form is deliberate.')
A('- **黑菟/黑莬**: 1376 p62 uses 黑菟. The set decision from batch 049 applies; no new row.')
A('- **Carried-forward set decisions** (not repeated here): 炎荒仙人; 面目全非; 太上大长老; 不以为杵/忤; 宴宴/晏晏; 值得/只得; 至尊仙窍; 四面八方; 八成/六成 (deferred).')
A('- **池伤, 白天中**: consistent term usage (1366 p7, 1375 p102, 1379 p9). Not flags.')
A('')
A('## Dropped during reading (not proposed)')
A('')
A('- 1359 p30 也在白天中有所布置: 白天中 is a consistent location term. No row.')
A('- 1361 p80 狗尾续命貂毛里球: 狗尾续命 x37 across the novel; the name is established. No row.')
A('- 1374 p3 修行宇道的盗天魔尊: 宇道 is a valid space Dao (see 1383 p5, p59). No row.')
A('- 1370 p42 青城纵横: established term. No row.')
A('- 1386 p27 黑凡真传: 黑凡 is established (many hits). No row.')
A('- 1392 p79 偷道仙蛊: 偷道 is established (x14). No row.')
A('- 1394 p42 八成: falls in the deferred 六成/八成 set-wide item. No new row.')
A('- 1363 p29 and 1403 p71: kept only as optional queries, not repairs.')
A('')
A('## Known limits')
A('')
A('- Single-token repairs are local to the stated paragraph. Each row was checked against the batch sources for the same token (0 misses; see rationale column).')
A('- Corpus counts use the batch source files for 686–1405 only. Earlier chapters (1–685) are not in the batch sources, so a count of 1 may be a true single occurrence within this range.')
A('- Queries (no edit proposed): 1357 p13, 1358 p82, 1361 p20, 1362 p9, 1363 p29, 1376 p24, 1383 p2, 1384 p31, 1391 p60, 1403 p71, 1405 p44, 1405 p61.')
A('- Several repairs rest on sense judgement rather than corpus matches (1356 p44, 1361 p34, 1369 p34, 1375 p21, 1380 p11, 1383 p38, 1383 p49, 1387 p59, 1399 p67). Confirm each sentence before applying.')
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
open(f'{BASE}/Batch-050-Chapters-1356-1405.md', 'w', encoding='utf-8').write('\n'.join(L) + '\n')

cc = Counter(r[4].split(' ')[0] for r in ROWS)
qa = {'batch': '050', 'chapters': '1356-1405', 'chapter_count': len(src),
      'source_check': f'batch-050-source.json ({len(src)} chapters, {para_total:,} paragraphs, {char_total:,} characters). Every row token verified present in its stated paragraph (0 misses).',
      'reading_status': 'complete (1356-1405); flags in tmp/b050-flags.txt',
      'report_rows': len(ROWS), 'confidence_counts': dict(cc),
      'approved': 0, 'applied': 0, 'source_edits': 0,
      'witness_collation': f'Hetushu book 7640 automated token-level comparison (witness-collation-050.json); {len(src)} chapter pages fetched and title-checked ({len(src)-len(title_mismatch)} match).',
      'witness_results': dict(cnt),
      'workbook_rows': 'added (chapter completion and paragraph register 1356-1405; ledger sheet SR-1131 onward)',
      'ledger_entries': f'SR-{START} to SR-{START+len(ROWS)-1}',
      'docx': 'Batch-050-Chapters-1356-1405.docx',
      'cross_batch': ['1354 p93 / 1356 p73 / 1366 p56 灰夜 → 夜灰 (batch 049 row for 1354 p93)', '1044 p12 / 1117 p52–53 / 1358 p77 在一切 (batches 044–045)', '1143 p48 / 1147 p40 / 1379 p52 上级天鹰 (batch 045)', '735 p54 / 1148 p12 / 1370 p31 宝皇天 (batches 037, 045)', '1246 p53 / 1387 p78 难以附加 (batch 047)'],
      'known_limits': [
          'Set-wide decisions: 夜灰; 在一起 (在一切); 上极天鹰; 宝黄天; 难以复加; 通晓; 纯梦求真体 (纯梦求真仙); 点了点头.',
          'Queries carry no edit: 1357 p13, 1358 p82, 1361 p20, 1362 p9, 1363 p29, 1376 p24, 1383 p2, 1384 p31, 1391 p60, 1403 p71, 1405 p44, 1405 p61.',
          'Several repairs rest on sense judgement rather than corpus matches; confirm before applying.']}
json.dump(qa, open(f'{BASE}/batch-050-qa.json', 'w'), ensure_ascii=False, indent=1)

Lg = json.load(open(f'{BASE}/proposal-ledger.json'))
ids = {e['id'] for e in Lg}
assert f'SR-{START}' not in ids, 'ledger already has batch 050 ids'
new = []
for i, r in enumerate(ROWS):
    ch, pa, orig, cand, conf, cat, action, rat, deps = r
    new.append({'id': f'SR-{START+i}', 'category': cat,
                'locations': [{'chapter': ch, 'paragraph': pa, 'file': '', 'reference_text': f'{ch} p{pa}'}],
                'recommended_action': f'{action} (batch 050, row {i+1}; source token: {orig})',
                'rationale': f'{rat} Confidence {conf}.',
                'confidence': conf, 'status': 'Open; unapproved, unapplied',
                'dependencies': deps,
                'publication_status': 'HOLD: complete-corpus reading and global reconciliation outstanding',
                'witness_collation': f'Hetushu 7640 collation: {wlabel(i+1)}',
                'approved': False, 'applied': False})
Lg.extend(new)
json.dump(Lg, open(f'{BASE}/proposal-ledger.json', 'w'), ensure_ascii=False, indent=1)
json.dump(new, open(f'{BASE}/ledger-new-050.json', 'w'), ensure_ascii=False, indent=1)
print('rows', len(ROWS), 'ledger total', len(Lg), 'last', Lg[-1]['id'])
print(dict(cnt)); print(dict(cc))
print('title mismatches', title_mismatch)
