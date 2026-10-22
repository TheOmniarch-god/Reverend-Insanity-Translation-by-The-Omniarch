import json, subprocess, sys, re, os
from collections import Counter
sys.path.insert(0, '/home/user/tmp')
from rows049 import ROWS
from witness_lib import chapter_title
BASE = '/home/user/editorial/sequential-review'
BATCH = '049'
START = 1056
CH0, CH1 = 1306, 1355

defs = [{'row': i + 1, 'ch': r[0], 'orig': r[2], 'cand': (None if r[5].startswith('Query') else r[3])} for i, r in enumerate(ROWS)]
json.dump(defs, open('/home/user/tmp/defs-049.json', 'w'), ensure_ascii=False, indent=1)
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
A('# Batch 049 — Chapters 1306–1355 (sequential source review)')
A('')
A('Status: **source reading complete (1306–1355)**. Reading flags: `tmp/b049-flags.txt` (working file). This report is a candidate list only. Nothing here is approved, applied, or published, and no Chinese source has been changed.')
A('')
A(f'Source check: `batch-049-source.json` ({len(src)} chapters, {para_total:,} paragraphs, {char_total:,} characters). Every row token was found in its stated paragraph ({len(ROWS)} rows, 0 misses).')
A('')
A(f'Produced: proposal-ledger entries SR-{START} to SR-{START+len(ROWS)-1} ({len(ROWS)} rows), this report with a DOCX, a QA file, and witness collation against Hetushu book 7640 (`witness-collation-049.json`) for all 50 chapters. Chapter titles checked against the witness pages: {len(src)-len(title_mismatch)} of {len(src)} match.')
A('')
A('Confidence: H = high, H–M, M–H, M, L–M, L, with a numeric score in brackets. "Action" is what the editor should decide. Nothing is applied.')
A('')
A('Cross-batch references: 1304 p36 炎黄仙人 (batch 048) is the same error as 1312 p10 and is noted in that row; 1198 p77 (batch 046) and 1237 p18 (batch 047) share 面目前非 with 1339 p42; 1351/1352 黑莬/黑菟 is in the set-wide decision.')
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
A('- **炎黄仙人 → 炎荒仙人**: 1312 p10 (row above) and 1304 p36 (batch 048). 炎荒仙人 x39 in the corpus. Decide once.')
A('- **面目前非 → 面目全非**: 1339 p42 (row above), 1198 p77 (batch 046), 1237 p18 (batch 047). 面目全非 x21. Decide once.')
A('- **太上大家老 → 太上大长老**: 1330 p72 (row above) and 1343 p21, p40, p70 (in this batch, not separately ledgered). 太上大长老 x317. Decide as one set; 1343 p70 also has 太上二长老 in the same paragraph, so the 1343 uses look like a single author habit. Decide before applying any of the four.')
A('- **黑莬 vs 黑菟**: 1349 p36 and 1351 p114 use 黑莬; 1352 body uses 黑菟 (x38 in the corpus) and the 1352 chapter title uses 黑莬. Choose one spelling for the name and apply it to every occurrence (the title included, if the title is treated as the same name).')
A('- **不以为杵 → 不以为忤?**: 1333 p69 (row above), 1194 p48 (batch 046), 1263 p41 (batch 048). 不以为忤 x0 in the corpus; the classical form is the likely intent. Decide once for all three.')
A('- **宴宴 vs 晏晏**: 1320 p87 and 1322 p60 (row above). 宴宴 x5 in the corpus (041 p2, 045, 046 and two in this batch) with 晏晏 x0. The author uses 宴宴 consistently, so this may be intentional. Decide whether to standardise to 晏晏 or keep 宴宴.')
A('- **值得 → 只得**: 1321 p14, 1335 p38, 1352 p77 share one pattern (值得 used for 只得). 只得 x75. Decide once.')
A('- **至尊福地 → 至尊仙窍**: 1312 p61 and 1316 p46 have their own rows above. 1321 p14 also contains 至尊福地 (not changed in its row). Joins the existing set (1113 p110, 1139 p23, 1139 p26, 1177 p25 in batch 045). Decide once.')
A('- **四面八方**: 1316 p56 四面八法 joins the existing set (SR-809, SR-822–825, SR-856; 1163 p73; 1196 p16; 1227 p57; 1246 p33; 1255 p44).')
A('- **通宵 → 通晓**: 1270 p50 (batch 048) and 1242 p17 (batch 047). Not in this batch; listed for completeness.')
A('- **池伤**: name used 261 times in the corpus. Consistent. Not a flag.')
A('')
A('## Dropped during reading (not proposed)')
A('')
A('- 1321 p67 黄龙江: 1326 p14 lists 黄龙江 as a real river. No row.')
A('- 1313 p63 龙鳞湖 → 龙鳞海: the sentence says 从龙鳞湖，到龙鳞海, a deliberate progression. Corpus 龙鳞湖 x8 (earlier batches, a different place) and 龙鳞海 x8 (1313–1314). No row.')
A('- 1320 p78 池伤: x261 corpus, consistent. No row.')
A('- 1327 p23 阴鸠之气: 阴鸠 x5 in the corpus (828 p57, 877 p19, 1215 p35, 1296 p43, 1327 p23), as an appearance term. Consistent. No row.')
A('- 1325 p59 火道: four Dao names in a list; 火道 is a general path term (x9). Kept as a query row (L 0.35) only; no change proposed.')
A('- 1354 p68 大姨妈: 大姨妈 is the established relation (黑楼兰 and 焚天魔女; 041 p942–948, 043 p1031, 1338 p20). No row.')
A('- 1339 p49 缓缓地堕落到血潮天坑: the sense is acceptable (sink into). No row.')
A('')
A('## Known limits')
A('')
A('- Single-token repairs are local to the stated paragraph. Each row was checked against the batch sources for the same token (0 misses; see rationale column).')
A('- Corpus counts use the batch source files for 686–1355 only. Earlier chapters (1–685) are not in the batch sources, so a count of 1 may be a true single occurrence within this range.')
A('- Queries (no edit proposed): 1310 p46, 1319 p11, 1320 p46, 1325 p59, 1331 p19, 1336 p79, 1338 p16, 1347 p69, 1348 p38, 1351 p9, 1354 p84.')
A('- Several repairs rest on sense judgement rather than corpus matches (1306 p32, 1311 p38, 1313 p5, 1318 p32, 1323 p17, 1327 p87, 1342 p42, 1345 p10, 1353 p28). Confirm each sentence before applying.')
A('- Source-level: 1347 p69 contains a × symbol and 1348 p38 is garbled; the witness copy carries the same wording, so these are source issues, not transcription errors.')
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
open(f'{BASE}/Batch-049-Chapters-1306-1355.md', 'w', encoding='utf-8').write('\n'.join(L) + '\n')

cc = Counter(r[4].split(' ')[0] for r in ROWS)
qa = {'batch': '049', 'chapters': '1306-1355', 'chapter_count': len(src),
      'source_check': f'batch-049-source.json ({len(src)} chapters, {para_total:,} paragraphs, {char_total:,} characters). Every row token verified present in its stated paragraph (0 misses).',
      'reading_status': 'complete (1306-1355); flags in tmp/b049-flags.txt',
      'report_rows': len(ROWS), 'confidence_counts': dict(cc),
      'approved': 0, 'applied': 0, 'source_edits': 0,
      'witness_collation': f'Hetushu book 7640 automated token-level comparison (witness-collation-049.json); {len(src)} chapter pages fetched and title-checked ({len(src)-len(title_mismatch)} match).',
      'witness_results': dict(cnt),
      'workbook_rows': 'added (chapter completion and paragraph register 1306-1355; ledger sheet SR-1056 onward)',
      'ledger_entries': f'SR-{START} to SR-{START+len(ROWS)-1}',
      'docx': 'Batch-049-Chapters-1306-1355.docx',
      'cross_batch': ['1304 p36 炎黄仙人 → 炎荒仙人 (batch 048; same as 1312 p10)', '1198 p77 / 1237 p18 面目前非 → 面目全非 (batches 046/047; same as 1339 p42)'],
      'known_limits': [
          'Set-wide decisions: 炎荒仙人; 面目全非; 太上大长老 (1343 p21/p40/p70); 黑莬 vs 黑菟; 不以为杵/忤; 宴宴 vs 晏晏; 值得/只得; 至尊仙窍; 四面八方.',
          'Queries carry no edit: 1310 p46, 1319 p11, 1320 p46, 1325 p59, 1331 p19, 1336 p79, 1338 p16, 1347 p69, 1348 p38, 1351 p9, 1354 p84.',
          'Source-level garbles (1347 p69 ×; 1348 p38) are present in the witness copy too.']}
json.dump(qa, open(f'{BASE}/batch-049-qa.json', 'w'), ensure_ascii=False, indent=1)

Lg = json.load(open(f'{BASE}/proposal-ledger.json'))
ids = {e['id'] for e in Lg}
assert f'SR-{START}' not in ids, 'ledger already has batch 049 ids'
new = []
for i, r in enumerate(ROWS):
    ch, pa, orig, cand, conf, cat, action, rat, deps = r
    new.append({'id': f'SR-{START+i}', 'category': cat,
                'locations': [{'chapter': ch, 'paragraph': pa, 'file': '', 'reference_text': f'{ch} p{pa}'}],
                'recommended_action': f'{action} (batch 049, row {i+1}; source token: {orig})',
                'rationale': f'{rat} Confidence {conf}.',
                'confidence': conf, 'status': 'Open; unapproved, unapplied',
                'dependencies': deps,
                'publication_status': 'HOLD: complete-corpus reading and global reconciliation outstanding',
                'witness_collation': f'Hetushu 7640 collation: {wlabel(i+1)}',
                'approved': False, 'applied': False})
Lg.extend(new)
json.dump(Lg, open(f'{BASE}/proposal-ledger.json', 'w'), ensure_ascii=False, indent=1)
json.dump(new, open(f'{BASE}/ledger-new-049.json', 'w'), ensure_ascii=False, indent=1)
print('rows', len(ROWS), 'ledger total', len(Lg), 'last', Lg[-1]['id'])
print(dict(cnt)); print(dict(cc))
print('title mismatches', title_mismatch)
