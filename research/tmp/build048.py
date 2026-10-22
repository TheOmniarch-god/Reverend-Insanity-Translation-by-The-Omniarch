import json, subprocess, sys, re, os
from collections import Counter
sys.path.insert(0, '/home/user/tmp')
from rows048 import ROWS
from witness_lib import chapter_title
BASE = '/home/user/editorial/sequential-review'
BATCH = '048'
START = 986
CH0, CH1 = 1256, 1305

defs = [{'row': i + 1, 'ch': r[0], 'orig': r[2], 'cand': (None if r[5].startswith('Query') else r[3])} for i, r in enumerate(ROWS)]
json.dump(defs, open('/home/user/tmp/defs-048.json', 'w'), ensure_ascii=False, indent=1)
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
A('# Batch 048 — Chapters 1256–1305 (sequential source review)')
A('')
A('Status: **source reading complete (1256–1305)**. Reading notes: `editorial/sequential-review/batch-048-notes/reading-notes-1256-1305.md`. This report is a candidate list only. Nothing here is approved, applied, or published, and no Chinese source has been changed.')
A('')
A(f'Source check: `batch-048-source.json` ({len(src)} chapters, {para_total:,} paragraphs, {char_total:,} characters). Every row token was found in its stated paragraph ({len(ROWS)} rows, 0 misses).')
A('')
A(f'Produced: proposal-ledger entries SR-{START} to SR-{START+len(ROWS)-1} ({len(ROWS)} rows), this report with a DOCX, a QA file, and witness collation against Hetushu book 7640 (`witness-collation-048.json`) for all 50 chapters. Chapter titles checked against the witness pages: {len(src)-len(title_mismatch)} of {len(src)} match.')
A('')
A('Confidence: H = high, H–M, M–H, M, L–M, L, with a numeric score in brackets. "Action" is what the editor should decide. Nothing is applied.')
A('')
A('Cross-batch rows: two rows point at batch 047 (1242 p17 通宵; 1247 p59 黒豕蛊). They come from corpus checks in this batch and are listed here so each decision is made once.')
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
A('- **权利 vs 权力**: 1263 p49 生存下来的权力 joins the existing set (1189 p19, 1193 p56 in batch 046; 1220 p84–85, 1221 p63, 1238 p70 in batch 047; 最高权利 at 1049 p44 still unrun). Decide once with the set.')
A('- **特意**: 1266 p81 巨阳特意不管马鸿运 joins the 特意 non-ordinary-term set (1052 p50, 1075 p24, 1079 p82 in batch 044). 特意 x82 in the corpus. Decide once; no row here.')
A('- **不以为杵 → 不以为忤**: 1263 p41 (row above) and 1194 p48 (batch 046) share the string. Decide with the 1194 p48 row.')
A('- **传到到了**: 1268 p24 (row above) and 1167 p45 (batch 040) share the string. Decide as a pair.')
A('- **通宵 → 通晓**: 1270 p50 (row above) and 1242 p17 (batch 047 cross-batch row). Decide as a pair.')
A('- **黑豕蛊**: 1272 p58–59 use 黑豕蛊, which supports the batch 047 row at 1247 p59 (黒豕蛊 → 黑豕蛊). Raised to H (0.90).')
A('- **雪山老祖 (alias check)**: 1278 p80 and p87 (query row above) and six earlier uses (903, 945, 1100, 1177). Decide as a set.')
A('- **黑城 vs 黑凡**: 1299 p87 (row above). 黑城 x526 elsewhere; decide with a name check.')
A('')
A('## Dropped during reading (not proposed)')
A('')
A('- 1257 p81 所然→所以: the string 所然 does not occur anywhere in the corpus, and 1257 has no paragraph containing it. The earlier note was a paragraph error and is withdrawn. No row.')
A('- 1271 p45 大同风: x46 in the corpus; a set term. No row.')
A('- 1271 p62 / 1262 p61 心中一吐: x2 (1262 p61 uses 一吐 for a flame; 1271 p62 uses 心中一吐). Consistent. No row.')
A('- 1294 p43 资辈不小: 资辈 x3 (691 p19, 918 p45, 1294 p44). Consistent term. No row.')
A('- 1296 p52 宋甲丹: prose name 宋甲丹 x47 (899 and others); the poem line uses 盘甲丹 (1296 p50, 899 p30, 903 p40, 982 p43). Consistent. No row.')
A('- 1298 p75 感且佩: 感且佩 x2 (1133 p5, 1298 p75). Consistent idiom variant. No row.')
A('- 1280 p94 这么的人: 这么的 is a recurrent colloquial form (x14). No row.')
A('- 1260 p12 力道仙僵 and 撤走 (from earlier checks): x87 and x14. No row.')
A('')
A('## Known limits')
A('')
A('- Single-token repairs are local to the stated paragraph. Each row was checked against the batch sources for the same token (see rationale column).')
A('- Queries (no edit proposed): 1264 p61, 1278 p80, 1287 p63, 1289 p36, 1304 p36 (扩张疆域半途). Query rows carry no candidate in the ledger.')
A('- Several repairs rest on sense judgment rather than corpus matches (1257 p17, 1258 p3 pronoun, 1266 p79, 1270 p21, 1294 p68, 1299 p87, 1268 p40, 1272 p46). Confirm each sentence before applying.')
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
open(f'{BASE}/Batch-048-Chapters-1256-1305.md', 'w', encoding='utf-8').write('\n'.join(L) + '\n')

cc = Counter(r[4].split(' ')[0] for r in ROWS)
qa = {'batch': '048', 'chapters': '1256-1305', 'chapter_count': len(src),
      'source_check': f'batch-048-source.json ({len(src)} chapters, {para_total:,} paragraphs, {char_total:,} characters). Every row token verified present in its stated paragraph (0 misses).',
      'reading_status': 'complete (1256-1305); notes in batch-048-notes/reading-notes-1256-1305.md',
      'report_rows': len(ROWS), 'confidence_counts': dict(cc),
      'approved': 0, 'applied': 0, 'source_edits': 0,
      'witness_collation': f'Hetushu book 7640 automated token-level comparison (witness-collation-048.json); {len(src)} chapter pages fetched and title-checked ({len(src)-len(title_mismatch)} match).',
      'witness_results': dict(cnt),
      'workbook_rows': 'added (chapter completion and paragraph register 1256-1305; ledger sheet SR-986 onward)',
      'ledger_entries': f'SR-{START} to SR-{START+len(ROWS)-1}',
      'docx': 'Batch-048-Chapters-1256-1305.docx',
      'cross_batch': ['1242 p17 通宵 → 通晓 (batch 047; decide with 1270 p50)', '1247 p59 黒豕蛊 → 黑豕蛊 (batch 047; raised to H 0.90)'],
      'known_limits': [
          '权利 vs 权力 set-wide (1263 p49 added).',
          '特意 set-wide (1266 p81 added).',
          '不以为杵 (1263 p41 with 1194 p48).',
          '传到到了 (1268 p24 with 1167 p45).',
          '通宵/通晓 (1270 p50 with 1242 p17).',
          '雪山老祖 alias query (1278 p80, p87).',
          '黑城/黑凡 name check (1299 p87).',
          'Queries carry no edit: 1264 p61, 1278 p80, 1287 p63, 1289 p36, 1304 p36.']}
json.dump(qa, open(f'{BASE}/batch-048-qa.json', 'w'), ensure_ascii=False, indent=1)

Lg = json.load(open(f'{BASE}/proposal-ledger.json'))
ids = {e['id'] for e in Lg}
assert f'SR-{START}' not in ids, 'ledger already has batch 048 ids'
new = []
for i, r in enumerate(ROWS):
    ch, pa, orig, cand, conf, cat, action, rat, deps = r
    new.append({'id': f'SR-{START+i}', 'category': cat,
                'locations': [{'chapter': ch, 'paragraph': pa, 'file': '', 'reference_text': f'{ch} p{pa}'}],
                'recommended_action': f'{action} (batch 048, row {i+1}; source token: {orig})',
                'rationale': f'{rat} Confidence {conf}.',
                'confidence': conf, 'status': 'Open; unapproved, unapplied',
                'dependencies': deps,
                'publication_status': 'HOLD: complete-corpus reading and global reconciliation outstanding',
                'witness_collation': f'Hetushu 7640 collation: {wlabel(i+1)}',
                'approved': False, 'applied': False})
Lg.extend(new)
json.dump(Lg, open(f'{BASE}/proposal-ledger.json', 'w'), ensure_ascii=False, indent=1)
json.dump(new, open(f'{BASE}/ledger-new-048.json', 'w'), ensure_ascii=False, indent=1)
print('rows', len(ROWS), 'ledger total', len(Lg), 'last', Lg[-1]['id'])
print(dict(cnt)); print(dict(cc))
print('title mismatches', title_mismatch)
