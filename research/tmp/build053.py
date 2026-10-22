import json, subprocess, sys, re, os
from collections import Counter
sys.path.insert(0, '/home/user/tmp')
from rows053 import ROWS
from witness_lib import chapter_title
BASE = '/home/user/editorial/sequential-review'
BATCH = '053'
START = 1309
CH0, CH1 = 1506, 1555

defs = [{'row': i + 1, 'ch': r[0], 'orig': r[2], 'cand': (None if r[5].startswith(('Query', 'Decision')) else r[3])} for i, r in enumerate(ROWS)]
json.dump(defs, open('/home/user/tmp/defs-053.json', 'w'), ensure_ascii=False, indent=1)
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
A('# Batch 053 — Chapters 1506–1555 (sequential source review)')
A('')
A('Status: **source reading complete (1506–1555)**. Reading flags: `tmp/b053-flags.txt` (working file). This report is a candidate list only. Nothing here is approved, applied, or published, and no Chinese source has been changed.')
A('')
A(f'Source check: `batch-053-source.json` ({len(src)} chapters, {para_total:,} paragraphs, {char_total:,} characters). Every row token was found in its stated paragraph ({len(ROWS)} rows, 0 misses).')
A('')
A(f'Produced: proposal-ledger entries SR-{START} to SR-{START+len(ROWS)-1} ({len(ROWS)} rows), this report with a DOCX, a QA file, and witness collation against Hetushu book 7640 (`witness-collation-053.json`) for all 50 chapters. Chapter titles checked against the witness pages: {len(src)-len(title_mismatch)} of {len(src)} match.')
A('')
A('Confidence: H = high, H–M, M–H, M, L–M, L, with a numeric score in brackets. "Action" is what the editor should decide. Nothing is applied.')
A('')
A('## Summary')
A('')
A('- Chapters 1506–1555 are a Nine-Revolution mid-arc run: the 因果神树 / 豆神宫 fight (1516–1526), the 房家 alliance and the 青甲菜园 and 桃花迷林 battle (1521–1530), the 烟罗暖玉田 and 地底寒心湖 scene with 叶凡 and 铁若男 (1531–1535), the 胎土迷宫 interlude (1538–1541), the 大风歌 and 定真树 battle at 琅琊福地 (1542–1547), and the 荡魂山 compensation negotiation (1550–1552).')
A('- Most rows are typo or idiom slips (single occurrences). Several are set-wide or whole-novel decisions and are recorded as Decision or Query rows, not edits.')
A('- The largest open point is the sect name for 陈衣 (元莲派 vs 天莲派). It is a Decision row, not a line fix.')
A('')
A('## Rows (38)')
A('')
A('| # | SR | Ch | Para | Token | Proposed | Confidence | Category |')
A('|---|---|---|---|---|---|---|---|')
for i, r in enumerate(ROWS):
    ch, pa, orig, cand, conf, cat, action, rat, deps = r
    c = '' if cand is None else cand
    A(f'| {i+1} | SR-{START+i} | {ch} | {pa} | {orig} | {c or "(delete)" if cand is not None else "—"} | {conf} | {cat} |')
A('')
A('### Row notes')
A('')
for i, r in enumerate(ROWS):
    ch, pa, orig, cand, conf, cat, action, rat, deps = r
    A(f'- **SR-{START+i} ({ch} p{pa})** {action} Rationale: {rat} Dependencies: {deps}')
A('')
A('## Set-wide and whole-novel items')
A('')
A('- **陈衣 sect name (元莲派 / 天莲派)**: 1526 p35 (decision row). 元莲派 is used in 1516 p3 and 1522 (about eight times). 天莲派 is used in 1526 p35, 1527 p11 and p16, 1530 p3 and p12. 天莲派 x42 in earlier chapters is a separate, established sect with its seat at 天池. The switch inside 1516–1530 needs one whole-novel decision before any line edit.')
A('- **见面曾相识 / 见面不相识 / 见面似相识**: 1530 p48 and 1555 p67 (query, row above). 见面曾相识 x160; 见面不相识 x26 (also a skill name, 1540 p44); 见面似相识 x73 earlier. Decide once.')
A('- **至尊仙躯 / 至尊仙体**: 1535 p57 uses 仙躯; 1535 p4 and 1539 use 仙体 in the same chapter. 至尊仙体 x82; 至尊仙躯 x5 before this batch. Carry with the batch 052 set decision.')
A('- **权利 / 权力**: 1522 p12 (饱尝权利滋味) and 1525 p61 (这部分权利). Carry with the set item from batch 043.')
A('- **六成 / 八成**: 1522 and 1529 use 六成 in the sense of six tenths of ability (1527 p73). Deferred by the user; not proposed.')
A('- **凤金煌 / 凤九歌**: 1541 p25 (row above). 凤金煌 x510 is an established separate character name. Check the subject before editing.')
A('- **沟动 / 勾动**: 1539 p35 (row above) repeats the 774 p80 form (batch 038). Decide once with batch 038.')
A('- **但蛊师**: 1552 p6 (query). 但蛊师 x4 across 823, 830, 1025 and 1552; 但凡蛊师 x1 (828). Decide as a set.')
A('- **眉如淡柳龙烟**: 1531 p13 (query). Same wording at 1072 p17 (batch 044). Decide as a set.')
A('- **Carried-forward set decisions** (not repeated here): 惨白亏输; 不以为杵; 得走 → 拿走; 石宗 / 石忠; 秦百胜 / 秦百合; 逆流河 / 逆流护身印; 己运真传 / 我运真传.')
A('')
A('## Dropped during reading (not proposed)')
A('')
A('- 1506–1555 毛民 and 蛊仙 terms: established terms, no row.')
A('- 1516 p20 九转仙道杀招 and 1524 p33 鬼不觉: established terms.')
A('- 1518 p41 百八十奴: established (百八十奴 x26 in earlier batches).')
A('- 1523 p76 and 1525 p80 松柏 and 桃林 passages: no anomaly.')
A('- 1538 p31 and 1544 p2: long sentences truncated by the source window; left as read.')
A('- 1544 p85 耸搭: 耸搭 x8 in corpus (established). Not flagged.')
A('- 1546 p61 砖们: source phrasing, not flagged at confidence above L.')
A('- 1555 p28 见面曾相识么: covered by the set item above.')
A('')
A('## Known limits')
A('')
A('- Single-token repairs are local to the stated paragraph. Each row was checked against the batch sources for the same token (0 misses; see rationale column).')
A('- Corpus counts use the batch source files; earlier chapters (1–685) are not in the batch sources, so a count of 1 may be a true single occurrence within this range.')
A('- Queries (no edit proposed): 1506 p47, 1506 p19, 1520 p30, 1530 p48, 1531 p13, 1551 p60, 1552 p6.')
A('- Decisions: 1526 p35 (陈衣 sect name).')
A('- Several repairs rest on sense judgement (1510 p52, 1527 p66, 1531 p45, 1541 p25). Confirm each sentence before applying.')
A('- 1527 p16 is a deletion of a stray fragment; confirm against the live text before applying.')
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
open(f'{BASE}/Batch-053-Chapters-1506-1555.md', 'w', encoding='utf-8').write('\n'.join(L) + '\n')

cc = Counter(r[4].split(' ')[0] for r in ROWS)
qa = {'batch': '053', 'chapters': '1506-1555', 'chapter_count': len(src),
      'source_check': f'batch-053-source.json ({len(src)} chapters, {para_total:,} paragraphs, {char_total:,} characters). Every row token verified present in its stated paragraph (0 misses).',
      'reading_status': 'complete (1506-1555); flags in tmp/b053-flags.txt',
      'report_rows': len(ROWS), 'confidence_counts': dict(cc),
      'approved': 0, 'applied': 0, 'source_edits': 0,
      'witness_collation': f'Hetushu book 7640 automated token-level comparison (witness-collation-053.json); {len(src)} chapter pages fetched and title-checked ({len(src)-len(title_mismatch)} match).',
      'witness_results': dict(cnt),
      'workbook_rows': 'added (chapter completion and paragraph register 1506-1555; ledger sheet SR-1309 onward)',
      'ledger_entries': f'SR-{START} to SR-{START+len(ROWS)-1}',
      'docx': 'Batch-053-Chapters-1506-1555.docx',
      'corrections': [],
      'known_limits': ['Decision: 陈衣 sect name (元莲派 / 天莲派), 1526 p35.',
                       'Queries carry no edit: 1506 p47, 1506 p19, 1520 p30, 1530 p48, 1531 p13, 1551 p60, 1552 p6.']}
json.dump(qa, open(f'{BASE}/batch-053-qa.json', 'w'), ensure_ascii=False, indent=1)

Lg = json.load(open(f'{BASE}/proposal-ledger.json'))
ids = {e['id'] for e in Lg}
assert f'SR-{START}' not in ids, 'ledger already has batch 053 ids'
new = []
for i, r in enumerate(ROWS):
    ch, pa, orig, cand, conf, cat, action, rat, deps = r
    new.append({'id': f'SR-{START+i}', 'category': cat,
                'locations': [{'chapter': ch, 'paragraph': pa, 'file': '', 'reference_text': f'{ch} p{pa}'}],
                'recommended_action': f'{action} (batch 053, row {i+1}; source token: {orig})',
                'rationale': f'{rat} Confidence {conf}.',
                'confidence': conf, 'status': 'Open; unapproved, unapplied',
                'dependencies': deps,
                'publication_status': 'HOLD: complete-corpus reading and global reconciliation outstanding',
                'witness_collation': f'Hetushu 7640 collation: {wlabel(i+1)}',
                'approved': False, 'applied': False})
Lg.extend(new)
json.dump(Lg, open(f'{BASE}/proposal-ledger.json', 'w'), ensure_ascii=False, indent=1)
json.dump(new, open(f'{BASE}/ledger-new-053.json', 'w'), ensure_ascii=False, indent=1)
print('rows', len(ROWS), 'ledger total', len(Lg), 'last', Lg[-1]['id'])
print(dict(cnt)); print(dict(cc))
print('title mismatches', title_mismatch)
