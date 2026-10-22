import json, subprocess, sys, re
from collections import Counter
sys.path.insert(0, '/home/user/tmp')
from rows045 import ROWS
from witness_lib import chapter_title
BASE = '/home/user/editorial/sequential-review'
BATCH = '045'
START = 857
CH0, CH1 = 1106, 1155

defs = [{'row': i + 1, 'ch': r[0], 'orig': r[2], 'cand': r[3]} for i, r in enumerate(ROWS)]
json.dump(defs, open('/home/user/tmp/defs-045.json', 'w'), ensure_ascii=False, indent=1)
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
A('# Batch 045 — Chapters 1106–1155 (sequential source review)')
A('')
A('Status: **source reading complete (1106–1155)**. Reading notes: `editorial/sequential-review/batch-045-notes/reading-notes-1106-1155.md`. This report is a candidate list only. Nothing here is approved, applied, or published, and no Chinese source has been changed.')
A('')
A(f'Source check: `batch-045-source.json` ({len(src)} chapters, {para_total:,} paragraphs, {char_total:,} characters). Every row token was found in its stated paragraph ({len(ROWS)} rows, 0 misses).')
A('')
A(f'Produced: proposal-ledger entries SR-{START} to SR-{START+len(ROWS)-1} ({len(ROWS)} rows), this report with a DOCX, a QA file, and witness collation against Hetushu book 7640 (`witness-collation-045.json`) for all 50 chapters. Chapter titles checked against the witness pages: {len(src)-len(title_mismatch)} of {len(src)} match.')
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
A('- **至尊福地 → 至尊仙窍** (1113 p110, 1139 p23, 1139 p26): three hits; the aperture is 至尊仙窍 in 126 other places. Decide once.')
A('- **阴长阳错 → 阴差阳错** (1133 p29; 755 p54 in batch 037): same token, same fix. Decide once.')
A('- **Ancient Supreme Pole Eagle (太古上极天鹰)**: 1143 p48 is a repair (上级 → 上极). The same token appears at 1147 p40 (batch 046), which is not yet read. Cross-check when batch 046 is read.')
A('- **炎煌 vs 炎黄 (雷泽/天坑)**: 1155 p24 炎煌天坑 is consistent with 炎煌雷泽 (x76). The five 炎黄雷泽 hits (925 p100/106/108, 945 p29, 989 p16) are an existing item from batches 041–042, not new here.')
A('- **Term query 黄金部族** (1140 p19): term-list decision; no edit now.')
A('')
A('## Dropped during reading (not proposed)')
A('')
A('- 1119 p52 相差仿佛: idiom (x6 in corpus).')
A('- 1120 p69 双发髻: consistent with 1122 p60 (x2).')
A('- 1118 p36 亲生父母: correct (case of 亲生 is reviewed separately under the 亲身/亲生 rule, which is not a repair here).')
A('- 1142 p31 区区一个福地: speaker\'s view; consistent with narration.')
A('- 1149 p8 有五百年重生过来: matches the idiom at 990 p11 (x2 in corpus); not proposed.')
A('- 1152 p59 红枣仙元: term (x12 in corpus, 702–790).')
A('')
A('## Deferred and notes (no row)')
A('')
A('- 1155 p24 炎煌天坑: see set-wide note above; no row.')
A('- 1139 p58 这么的: dropped earlier (policy).')
A('')
A('## Known limits')
A('')
A('- Single-token repairs are local to the stated paragraph. Each row was checked against the batch sources for the same token (see rationale column).')
A('- Queries (no edit proposed): 1112 p84 效果脱俗; 1120 p46 谈笑宴宴; 1124 p10 催促进步; 1136 p94 上古皇室; 1143 p102 有眼不识天梯山; 1140 p19 黄金部族 (term).')
A('- Temporal items: none new in this batch.')
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
open(f'{BASE}/Batch-045-Chapters-1106-1155.md', 'w', encoding='utf-8').write('\n'.join(L) + '\n')

cc = Counter(r[4].split(' ')[0] for r in ROWS)
qa = {'batch': '045', 'chapters': '1106-1155', 'chapter_count': len(src),
      'source_check': f'batch-045-source.json ({len(src)} chapters, {para_total:,} paragraphs, {char_total:,} characters). Every row token verified present in its stated paragraph (0 misses).',
      'reading_status': 'complete (1106-1155); notes in batch-045-notes/reading-notes-1106-1155.md',
      'report_rows': len(ROWS), 'confidence_counts': dict(cc),
      'approved': 0, 'applied': 0, 'source_edits': 0,
      'witness_collation': f'Hetushu book 7640 automated token-level comparison (witness-collation-045.json); {len(src)} chapter pages fetched and title-checked ({len(src)-len(title_mismatch)} match).',
      'witness_results': dict(cnt),
      'workbook_rows': 'added (chapter completion and paragraph register 1106-1155; ledger sheet SR-857 to SR-890)',
      'ledger_entries': f'SR-{START} to SR-{START+len(ROWS)-1}',
      'docx': 'Batch-045-Chapters-1106-1155.docx',
      'known_limits': [
          '至尊福地 (1113 p110, 1139 p23, 1139 p26) term decision outstanding.',
          '阴差阳错 set-wide with 755 p54 (batch 037).',
          '太古上极天鹰 cross-check with 1147 p40 (batch 046) pending.',
          'Queries carry no edit: 1112 p84, 1120 p46, 1124 p10, 1136 p94, 1143 p102, 1140 p19.']}
json.dump(qa, open(f'{BASE}/batch-045-qa.json', 'w'), ensure_ascii=False, indent=1)

Lg = json.load(open(f'{BASE}/proposal-ledger.json'))
ids = {e['id'] for e in Lg}
assert f'SR-{START}' not in ids, 'ledger already has batch 045 ids'
new = []
for i, r in enumerate(ROWS):
    ch, pa, orig, cand, conf, cat, action, rat, deps = r
    new.append({'id': f'SR-{START+i}', 'category': cat,
                'locations': [{'chapter': ch, 'paragraph': pa, 'file': '', 'reference_text': f'{ch} p{pa}'}],
                'recommended_action': f'{action} (batch 045, row {i+1}; source token: {orig})',
                'rationale': f'{rat} Confidence {conf}.',
                'confidence': conf, 'status': 'Open; unapproved, unapplied',
                'dependencies': deps,
                'publication_status': 'HOLD: complete-corpus reading and global reconciliation outstanding',
                'witness_collation': f'Hetushu 7640 collation: {wlabel(i+1)}',
                'approved': False, 'applied': False})
Lg.extend(new)
json.dump(Lg, open(f'{BASE}/proposal-ledger.json', 'w'), ensure_ascii=False, indent=1)
json.dump(new, open(f'{BASE}/ledger-new-045.json', 'w'), ensure_ascii=False, indent=1)
print('rows', len(ROWS), 'ledger total', len(Lg), 'last', Lg[-1]['id'])
print(dict(cnt)); print(dict(cc))
print('title mismatches', title_mismatch)
