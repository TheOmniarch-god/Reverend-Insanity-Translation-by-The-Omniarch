import json, subprocess, sys, re
from collections import Counter
sys.path.insert(0, '/home/user/tmp')
from rows047 import ROWS
from witness_lib import chapter_title
BASE = '/home/user/editorial/sequential-review'
BATCH = '047'
START = 942
CH0, CH1 = 1206, 1255

defs = [{'row': i + 1, 'ch': r[0], 'orig': r[2], 'cand': r[3] or None} for i, r in enumerate(ROWS)]
json.dump(defs, open('/home/user/tmp/defs-047.json', 'w'), ensure_ascii=False, indent=1)
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
A('# Batch 047 — Chapters 1206–1255 (sequential source review)')
A('')
A('Status: **source reading complete (1206–1255)**. Reading notes: `editorial/sequential-review/batch-047-notes/reading-notes-1206-1255.md`. This report is a candidate list only. Nothing here is approved, applied, or published, and no Chinese source has been changed.')
A('')
A(f'Source check: `batch-047-source.json` ({len(src)} chapters, {para_total:,} paragraphs, {char_total:,} characters). Every row token was found in its stated paragraph ({len(ROWS)} rows, 0 misses).')
A('')
A(f'Produced: proposal-ledger entries SR-{START} to SR-{START+len(ROWS)-1} ({len(ROWS)} rows), this report with a DOCX, a QA file, and witness collation against Hetushu book 7640 (`witness-collation-047.json`) for all 50 chapters. Chapter titles checked against the witness pages: {len(src)-len(title_mismatch)} of {len(src)} match.')
A('')
A('Confidence: H = high, H–M, M–H, M, L–M, L, with a numeric score in brackets. "Action" is what the editor should decide. Nothing is applied.')
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
A('- **门约 → 盟约**: 1207 p57 is added to 1149 p20 (batch 045). 门约 x2 in the corpus; 盟约 x250. Decide once.')
A('- **四面八方 (四面八法 → 四面八方)**: 1227 p57, 1246 p33 and 1255 p44 are added to the existing set (SR-809, SR-822–825, SR-856, batch 046 1163 p73 and 1196 p16). Decide once.')
A('- **权利 vs 权力**: 1220 p84–85, 1221 p63 and 1238 p70 use 权利 in the power sense. Joins 1189 p19 and 1193 p56 (batch 046). The 最高权利 check at 1049 p44 is still unrun. Decide with it.')
A('- **血战平原 vs 血原**: 1235 p24 (血战平原) adds one count to the batch 046 naming item (1190 p76). Decide once.')
A('- **亲身 vs 亲生**: 1219 p5 is a case-by-case row (user rule). Do not apply the rule across the batch without per-instance review.')
A('')
A('## Dropped during reading (not proposed)')
A('')
A('- 1207 p52 产生过来: x2 (797 p113 and 1207 p52). Consistent.')
A('- 1213 p7 一届散修: x2 (1168 p71 and 1213 p7). Consistent.')
A('- 1215 p35 阴鸠之气: 阴鸠 x3 (828 p57, 877 p19, 1215 p35). Consistent term.')
A('- 1239 p9 烂船还有三磅钉: x2 (1239 p9 and 1249 p51). Consistent; an idiom variant, not a typo.')
A('- 1247 p2 博文广志: x3 (935 p44, 1191 p17, 1247 p2). Consistent.')
A('- 1234 p42 乃是太: x3 (784 p80, 1233 p26, 1234 p42). Legitimate. The unique phrase 乃是太急促 is kept as a query row.')
A('- 1239 p38 产生出来: common phrase; no flag.')
A('')
A('## Known limits')
A('')
A('- Single-token repairs are local to the stated paragraph. Each row was checked against the batch sources for the same token (see rationale column).')
A('- Queries (no edit proposed): 1226 p80, 1234 p59, 1234 p42, 1236 p65, 1237 p27, 1239 p59, 1242 p35, 1250 p50, 1255 p97; 1252 p39 wording (M, query).')
A('- Several repairs rest on sense judgment rather than corpus matches (1213 p8, 1217 p46, 1222 p3, 1229 p3, 1230 p72, 1239 p56, 1239 p83, 1242 p17, 1236 p78, 1247 p59 variant). Confirm each sentence before applying.')
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
open(f'{BASE}/Batch-047-Chapters-1206-1255.md', 'w', encoding='utf-8').write('\n'.join(L) + '\n')

cc = Counter(r[4].split(' ')[0] for r in ROWS)
qa = {'batch': '047', 'chapters': '1206-1255', 'chapter_count': len(src),
      'source_check': f'batch-047-source.json ({len(src)} chapters, {para_total:,} paragraphs, {char_total:,} characters). Every row token verified present in its stated paragraph (0 misses).',
      'reading_status': 'complete (1206-1255); notes in batch-047-notes/reading-notes-1206-1255.md',
      'report_rows': len(ROWS), 'confidence_counts': dict(cc),
      'approved': 0, 'applied': 0, 'source_edits': 0,
      'witness_collation': f'Hetushu book 7640 automated token-level comparison (witness-collation-047.json); {len(src)} chapter pages fetched and title-checked ({len(src)-len(title_mismatch)} match).',
      'witness_results': dict(cnt),
      'workbook_rows': 'added (chapter completion and paragraph register 1206-1255; ledger sheet SR-942 onward)',
      'ledger_entries': f'SR-{START} to SR-{START+len(ROWS)-1}',
      'docx': 'Batch-047-Chapters-1206-1255.docx',
      'known_limits': [
          '门约→盟约 set-wide (1207 p57 with 1149 p20).',
          '四面八方 set-wide (1227 p57, 1246 p33, 1255 p44 added).',
          '权利 vs 权力 set-wide (1220 p84–85, 1221 p63, 1238 p70; plus batch 046 1189 p19, 1193 p56).',
          '亲身 vs 亲生 case-by-case (1219 p5).',
          '血战平原 vs 血原 (1235 p24 added).',
          'Queries carry no edit: 1226 p80, 1234 p59, 1234 p42, 1236 p65, 1237 p27, 1239 p59, 1242 p35, 1250 p50, 1255 p97.']}
json.dump(qa, open(f'{BASE}/batch-047-qa.json', 'w'), ensure_ascii=False, indent=1)

Lg = json.load(open(f'{BASE}/proposal-ledger.json'))
ids = {e['id'] for e in Lg}
assert f'SR-{START}' not in ids, 'ledger already has batch 047 ids'
new = []
for i, r in enumerate(ROWS):
    ch, pa, orig, cand, conf, cat, action, rat, deps = r
    new.append({'id': f'SR-{START+i}', 'category': cat,
                'locations': [{'chapter': ch, 'paragraph': pa, 'file': '', 'reference_text': f'{ch} p{pa}'}],
                'recommended_action': f'{action} (batch 047, row {i+1}; source token: {orig})',
                'rationale': f'{rat} Confidence {conf}.',
                'confidence': conf, 'status': 'Open; unapproved, unapplied',
                'dependencies': deps,
                'publication_status': 'HOLD: complete-corpus reading and global reconciliation outstanding',
                'witness_collation': f'Hetushu 7640 collation: {wlabel(i+1)}',
                'approved': False, 'applied': False})
Lg.extend(new)
json.dump(Lg, open(f'{BASE}/proposal-ledger.json', 'w'), ensure_ascii=False, indent=1)
json.dump(new, open(f'{BASE}/ledger-new-047.json', 'w'), ensure_ascii=False, indent=1)
print('rows', len(ROWS), 'ledger total', len(Lg), 'last', Lg[-1]['id'])
print(dict(cnt)); print(dict(cc))
print('title mismatches', title_mismatch)
