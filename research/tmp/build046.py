import json, subprocess, sys, re
from collections import Counter
sys.path.insert(0, '/home/user/tmp')
from rows046 import ROWS
from witness_lib import chapter_title
BASE = '/home/user/editorial/sequential-review'
BATCH = '046'
START = 891
CH0, CH1 = 1156, 1205

defs = [{'row': i + 1, 'ch': r[0], 'orig': r[2], 'cand': r[3]} for i, r in enumerate(ROWS)]
json.dump(defs, open('/home/user/tmp/defs-046.json', 'w'), ensure_ascii=False, indent=1)
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
A('# Batch 046 — Chapters 1156–1205 (sequential source review)')
A('')
A('Status: **source reading complete (1156–1205)**. Reading notes: `editorial/sequential-review/batch-046-notes/reading-notes-1156-1205.md`. This report is a candidate list only. Nothing here is approved, applied, or published, and no Chinese source has been changed.')
A('')
A(f'Source check: `batch-046-source.json` ({len(src)} chapters, {para_total:,} paragraphs, {char_total:,} characters). Every row token was found in its stated paragraph ({len(ROWS)} rows, 0 misses).')
A('')
A(f'Produced: proposal-ledger entries SR-{START} to SR-{START+len(ROWS)-1} ({len(ROWS)} rows), this report with a DOCX, a QA file, and witness collation against Hetushu book 7640 (`witness-collation-046.json`) for all 50 chapters. Chapter titles checked against the witness pages: {len(src)-len(title_mismatch)} of {len(src)} match.')
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
A('- **四面八方 (四面八法 → 四面八方)**: 1163 p73 and 1196 p16 are added to the existing set (SR-809, SR-822–825, SR-856). Eight 四面八法 hits in the corpus against 32 四面八方. Decide once.')
A('- **戈登 → 咯噔**: 1196 p40 is added to 982 p44, 1050 p43 and 1055 p104. Decide once.')
A('- **至尊福地 → 至尊仙窍**: 1177 p25 is a fourth hit (with 1113 p110, 1139 p23, 1139 p26). The aperture is 至尊仙窍 in 179 other places. Decide once.')
A('- **异族大联盟 vs 四族大联盟**: the alliance is 四族大联盟 in 11 places (1146–1199). 异族大联盟 appears at 1161 p37, 1172 p65, 1187 p51. 五族大联盟 at 1161 p51 is repaired to 四族 (row). The three 异族 lines need a set-wide decision; they are not repaired here.')
A('- **太古上级天鹰 → 太古上极天鹰 (cross-check done)**: the same token appears at 1143 p48 (batch 045) and 1147 p40 (batch 045). Both are 上级天鹰 (x2), and both should be 上极. Apply to both or neither (batch 045 row).')
A('- **血原 vs 血战平原** (battlefield name, 1190 p78 query row): 血战平原 x5, 血原 x4. Decide one naming rule.')
A('- **权利 vs 权力** (1189 p19 query; 1193 p56): the 最高权利 check at 1049 p44 is still unrun. Decide with it.')
A('- **谈笑宴宴** (1194 p15 query): x3 consistent (919 p2, 1120 p46). Decide with the set-wide form.')
A('')
A('## Dropped during reading (not proposed)')
A('')
A('- 1158 p101 悔池: term (x9 in corpus, 1103–1104 and 1158).')
A('- 1162 p13 八只手臂 (with six listed names): term (x8 in corpus). The earlier query is withdrawn.')
A('- 1164 p78 沙硕: term (x3).')
A('- 1171 p55 人如故: idiom (x48).')
A('- 1173 p99 太丘: place name (x123).')
A('- 1188 p72 不是仙道杀招: phrase x2 (800 p63, 1188 p72), consistent.')
A('- 1190 p73 做过一场: consistent (x4: 813 p15, 1046 p37, 1103 p19).')
A('- 1193 p14 跨域了: 跨域 is consistent (x12).')
A('- 1201 p82 青城纵横: term (x43).')
A('- 1204 p82 剑眉仙蛊: term (x10).')
A('- 1173 p43 六成空间: resource share; user deferred six/eight share (1083 p23). Not a row.')
A('')
A('## Deferred and notes (no row)')
A('')
A('- 1147 p40 (batch 045) 上级天鹰: see set-wide note above.')
A('- 1173 p43 六成: user deferred (six/eight share).')
A('- 1187 p51 异族大联盟: see set-wide note above.')
A('')
A('## Known limits')
A('')
A('- Single-token repairs are local to the stated paragraph. Each row was checked against the batch sources for the same token (see rationale column).')
A('- Queries (no edit proposed): 1156 p51 蝼蚁堕落; 1187 p78 尊重; 1189 p19 权利名声; 1190 p78 血原 naming; 1194 p15 谈笑宴宴.')
A('- Several repairs rest on idiom or sense judgment, not corpus matches (1158 p15, 1165 p62, 1171 p51, 1190 p5, 1201 p42, 1190 p65). Confirm each sentence before applying.')
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
open(f'{BASE}/Batch-046-Chapters-1156-1205.md', 'w', encoding='utf-8').write('\n'.join(L) + '\n')

cc = Counter(r[4].split(' ')[0] for r in ROWS)
qa = {'batch': '046', 'chapters': '1156-1205', 'chapter_count': len(src),
      'source_check': f'batch-046-source.json ({len(src)} chapters, {para_total:,} paragraphs, {char_total:,} characters). Every row token verified present in its stated paragraph (0 misses).',
      'reading_status': 'complete (1156-1205); notes in batch-046-notes/reading-notes-1156-1205.md',
      'report_rows': len(ROWS), 'confidence_counts': dict(cc),
      'approved': 0, 'applied': 0, 'source_edits': 0,
      'witness_collation': f'Hetushu book 7640 automated token-level comparison (witness-collation-046.json); {len(src)} chapter pages fetched and title-checked ({len(src)-len(title_mismatch)} match).',
      'witness_results': dict(cnt),
      'workbook_rows': 'added (chapter completion and paragraph register 1156-1205; ledger sheet SR-891 onward)',
      'ledger_entries': f'SR-{START} to SR-{START+len(ROWS)-1}',
      'docx': 'Batch-046-Chapters-1156-1205.docx',
      'known_limits': [
          '至尊福地 set-wide term decision outstanding (1113 p110, 1139 p23, 1139 p26, 1177 p25).',
          '四面八方 set-wide (1163 p73, 1196 p16 added); 戈登→咯噔 set-wide (1196 p40 added).',
          '异族大联盟 set-wide decision (1161 p37, 1172 p65, 1187 p51).',
          '太古上级天鹰 cross-batch with batch 045 (1143 p48, 1147 p40).',
          '血原 vs 血战平原 naming; 权利 vs 权力; 谈笑宴宴 query.',
          'Queries carry no edit: 1156 p51, 1187 p78, 1189 p19, 1190 p78, 1194 p15.']}
json.dump(qa, open(f'{BASE}/batch-046-qa.json', 'w'), ensure_ascii=False, indent=1)

Lg = json.load(open(f'{BASE}/proposal-ledger.json'))
ids = {e['id'] for e in Lg}
assert f'SR-{START}' not in ids, 'ledger already has batch 046 ids'
new = []
for i, r in enumerate(ROWS):
    ch, pa, orig, cand, conf, cat, action, rat, deps = r
    new.append({'id': f'SR-{START+i}', 'category': cat,
                'locations': [{'chapter': ch, 'paragraph': pa, 'file': '', 'reference_text': f'{ch} p{pa}'}],
                'recommended_action': f'{action} (batch 046, row {i+1}; source token: {orig})',
                'rationale': f'{rat} Confidence {conf}.',
                'confidence': conf, 'status': 'Open; unapproved, unapplied',
                'dependencies': deps,
                'publication_status': 'HOLD: complete-corpus reading and global reconciliation outstanding',
                'witness_collation': f'Hetushu 7640 collation: {wlabel(i+1)}',
                'approved': False, 'applied': False})
Lg.extend(new)
json.dump(Lg, open(f'{BASE}/proposal-ledger.json', 'w'), ensure_ascii=False, indent=1)
json.dump(new, open(f'{BASE}/ledger-new-046.json', 'w'), ensure_ascii=False, indent=1)
print('rows', len(ROWS), 'ledger total', len(Lg), 'last', Lg[-1]['id'])
print(dict(cnt)); print(dict(cc))
print('title mismatches', title_mismatch)
