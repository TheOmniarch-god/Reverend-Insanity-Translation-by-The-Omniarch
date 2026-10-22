import json, subprocess, sys, re, os
from collections import Counter
sys.path.insert(0, '/home/user/tmp')
from rows051 import ROWS
from witness_lib import chapter_title
BASE = '/home/user/editorial/sequential-review'
BATCH = '051'
START = 1195
CH0, CH1 = 1406, 1455

defs = [{'row': i + 1, 'ch': r[0], 'orig': r[2], 'cand': (None if r[5].startswith('Query') else r[3])} for i, r in enumerate(ROWS)]
json.dump(defs, open('/home/user/tmp/defs-051.json', 'w'), ensure_ascii=False, indent=1)
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
A('# Batch 051 — Chapters 1406–1455 (sequential source review)')
A('')
A('Status: **source reading complete (1406–1455)**. Reading flags: `tmp/b051-flags.txt` (working file). This report is a candidate list only. Nothing here is approved, applied, or published, and no Chinese source has been changed.')
A('')
A(f'Source check: `batch-051-source.json` ({len(src)} chapters, {para_total:,} paragraphs, {char_total:,} characters). Every row token was found in its stated paragraph ({len(ROWS)} rows, 0 misses).')
A('')
A(f'Produced: proposal-ledger entries SR-{START} to SR-{START+len(ROWS)-1} ({len(ROWS)} rows), this report with a DOCX, a QA file, and witness collation against Hetushu book 7640 (`witness-collation-051.json`) for all 50 chapters. Chapter titles checked against the witness pages: {len(src)-len(title_mismatch)} of {len(src)} match.')
A('')
A('Confidence: H = high, H–M, M–H, M, L–M, L, with a numeric score in brackets. "Action" is what the editor should decide. Nothing is applied.')
A('')
A('Cross-batch references: 1098 p18 (batch 044) and 1435 p81 share 利于不败之地 with 1408 p114. 1313 p5 (batch 049) shares 失踪没有 with 1413 p37. 1339 p42 (batch 049) shares 面目前非 with 1413 p48. 1319 p74 (batch 049) and 1379 p24 (batch 050) share 周翔 with 1430 p48. 771 p49 (batch 038) shares 毫无意识 with 1421 p73. 1330 p72 and 1343 p21, p40, p70 (batch 049) share 太上大家老 with 1449 p83. 1425 p4 and 1426 p69, p71 are set items for 逆流河护身印. SR-809, SR-822–825 and SR-856 (earlier batches) hold the 四面八方/四面八法 record.')
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
A('- **洁身自爱 → 洁身自好**: 1407 p53 (decision row); 1408 p102 (set item). 洁身自好 x36; 洁身自爱 x16 across the corpus. Decide once.')
A('- **利于不败之地 → 立于不败之地**: 1408 p114 (decision row); 1435 p81 (set item); 1098 p18 (batch 044). 立于不败之地 x8; 利于不败 x3. Decide once.')
A('- **逆流河护身印 → 逆流护身印**: 1425 p4 (decision row); 1426 p69, p71 (set items). 逆流护身印 x106; 逆流河护身印 x3. Decide once.')
A('- **四面八法 → 四面八方**: 1451 p25 (decision row). 四面八方 x49; 四面八法 x13. Earlier rows SR-809, SR-822–825, SR-856 already cover the same set; decide once for the whole novel.')
A('- **太上大家老 → 太上大长老**: 1449 p83 (set item); 1330 p72 and 1343 p21, p40, p70 (batch 049). 太上大长老 is the established title across the corpus. Decide with the 武碑 title query (1406 p35).')
A('- **我运真传 → 己运真传**: 1435 p49 (set item). 己运真传 x10 (incl. 1447 p47, p54); 我运真传 x1 here.')
A('- **面目前非 → 面目全非**: 1413 p48 (set item); 1339 p42 (batch 049). Same idiom slip; decide once.')
A('- **周翔 → 周详**: 1430 p48 (row above); 1319 p74 (batch 049); 1379 p24 (batch 050). Name slip in three places; decide once.')
A('- **失踪没有 → 始终没有**: 1413 p37 (row above); 1313 p5 (batch 049). Check 1313 p5 before applying the same fix there.')
A('- **毫无意识**: 1421 p73 (row above, proposed 毫无疑问); 771 p49 (batch 038). Check the sense at 771 p49 before any change.')
A('- **见面曾相识 / 见面似相识**: 1422 p7 (query). 见面曾相识 x137; 见面似相识 x73. Open set item; no edit until decided.')
A('- **Carried-forward set decisions** (not repeated here): 六成/八成 (deferred; no new row); 上古年兽变 vs 上古剑蛟变 (query, 1430 p77).')
A('')
A('## Dropped during reading (not proposed)')
A('')
A('- 1427 p57 大跑了: colloquial sense in a fight scene; not proposed as an error.')
A('- 1414 p31 渡让: x3 consistent (incl. 1273 p40). No row.')
A('- 1418 p80 布置出了六成时: falls in the deferred 六成/八成 set-wide item. No new row.')
A('- 1412 and 1438 flags: none recorded.')
A('')
A('## Known limits')
A('')
A('- Single-token repairs are local to the stated paragraph. Each row was checked against the batch sources for the same token (0 misses; see rationale column).')
A('- Corpus counts use the batch source files for 686–1455 only. Earlier chapters (1–685) are not in the batch sources, so a count of 1 may be a true single occurrence within this range.')
A('- Queries (no edit proposed): 1406 p9, 1406 p35, 1408 p97, 1410 p29, 1422 p7, 1430 p77, 1433 p18, 1435 p34.')
A('- Several repairs rest on sense judgement rather than corpus matches (1411 p64, 1421 p73, 1424 p30, 1429 p63, 1430 p49, 1435 p23, 1440 p64, 1453 p32). Confirm each sentence before applying.')
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
open(f'{BASE}/Batch-051-Chapters-1406-1455.md', 'w', encoding='utf-8').write('\n'.join(L) + '\n')

cc = Counter(r[4].split(' ')[0] for r in ROWS)
qa = {'batch': '051', 'chapters': '1406-1455', 'chapter_count': len(src),
      'source_check': f'batch-051-source.json ({len(src)} chapters, {para_total:,} paragraphs, {char_total:,} characters). Every row token verified present in its stated paragraph (0 misses).',
      'reading_status': 'complete (1406-1455); flags in tmp/b051-flags.txt',
      'report_rows': len(ROWS), 'confidence_counts': dict(cc),
      'approved': 0, 'applied': 0, 'source_edits': 0,
      'witness_collation': f'Hetushu book 7640 automated token-level comparison (witness-collation-051.json); {len(src)} chapter pages fetched and title-checked ({len(src)-len(title_mismatch)} match).',
      'witness_results': dict(cnt),
      'workbook_rows': 'added (chapter completion and paragraph register 1406-1455; ledger sheet SR-1195 onward)',
      'ledger_entries': f'SR-{START} to SR-{START+len(ROWS)-1}',
      'docx': 'Batch-051-Chapters-1406-1455.docx',
      'cross_batch': ['1098 p18 / 1408 p114 / 1435 p81 利于不败之地 (batch 044)', '1313 p5 / 1413 p37 失踪没有 (batch 049)', '1339 p42 / 1413 p48 面目前非 (batch 049)', '1319 p74 / 1379 p24 / 1430 p48 周翔 (batches 049-050)', '771 p49 / 1421 p73 毫无意识 (batch 038)', '1330 p72 / 1343 p21, p40, p70 / 1449 p83 太上大家老 (batch 049)'],
      'known_limits': [
          'Set-wide decisions: 洁身自好/洁身自爱; 立于不败之地; 逆流护身印; 四面八方; 太上大长老; 己运真传; 见面曾相识 (open).',
          'Queries carry no edit: 1406 p9, 1406 p35, 1408 p97, 1410 p29, 1422 p7, 1430 p77, 1433 p18, 1435 p34.',
          'Several repairs rest on sense judgement rather than corpus matches; confirm before applying.']}
json.dump(qa, open(f'{BASE}/batch-051-qa.json', 'w'), ensure_ascii=False, indent=1)

Lg = json.load(open(f'{BASE}/proposal-ledger.json'))
ids = {e['id'] for e in Lg}
assert f'SR-{START}' not in ids, 'ledger already has batch 051 ids'
new = []
for i, r in enumerate(ROWS):
    ch, pa, orig, cand, conf, cat, action, rat, deps = r
    new.append({'id': f'SR-{START+i}', 'category': cat,
                'locations': [{'chapter': ch, 'paragraph': pa, 'file': '', 'reference_text': f'{ch} p{pa}'}],
                'recommended_action': f'{action} (batch 051, row {i+1}; source token: {orig})',
                'rationale': f'{rat} Confidence {conf}.',
                'confidence': conf, 'status': 'Open; unapproved, unapplied',
                'dependencies': deps,
                'publication_status': 'HOLD: complete-corpus reading and global reconciliation outstanding',
                'witness_collation': f'Hetushu 7640 collation: {wlabel(i+1)}',
                'approved': False, 'applied': False})
Lg.extend(new)
json.dump(Lg, open(f'{BASE}/proposal-ledger.json', 'w'), ensure_ascii=False, indent=1)
json.dump(new, open(f'{BASE}/ledger-new-051.json', 'w'), ensure_ascii=False, indent=1)
print('rows', len(ROWS), 'ledger total', len(Lg), 'last', Lg[-1]['id'])
print(dict(cnt)); print(dict(cc))
print('title mismatches', title_mismatch)
