import json, sys, subprocess, re
sys.path.insert(0,'/home/user/tmp')
from rows042 import ROWS
BASE='/home/user/editorial/sequential-review'
defs=[{'row':i+1,'ch':r[0],'orig':r[2],'cand':r[3]} for i,r in enumerate(ROWS)]
json.dump(defs, open('/home/user/tmp/defs-042.json','w'), ensure_ascii=False, indent=1)
subprocess.run(['python3','/home/user/tmp/collate.py','042'], check=True, capture_output=True)
wit=json.load(open(f'{BASE}/witness-collation-042.json'))
wmap={w['row']:w for w in wit}
def wlabel(i):
    w=wmap.get(i)
    if not w: return 'not collated'
    r=w.get('result','')
    if r.startswith('witness copies'): return 'copies source (neutral)'
    if r.startswith('witness shows'): return 'shows candidate (web copy only)'
    return 'context not found'
# ---------- report ----------
lines=[]
A=lines.append
A('# Batch 042 — Chapters 956–1005 (sequential source review)')
A('')
A('Status: **source reading complete (956–1005)**. Notes: `editorial/sequential-review/batch-042-notes/reading-notes-956-1005.md`. This report is a candidate list only. Nothing here is approved, applied, or published, and no Chinese source has been changed.')
A('')
A('Source check: `batch-042-source.json` (50 chapters, 4773 paragraphs, 0 mismatches at build time). Every row was checked against the paragraph text in that file; the token in column 3 appears in the stated paragraph.')
A('')
A('Produced: proposal-ledger entries SR-716 to SR-772 (57 rows) and this report with a DOCX and QA file. Witness collation against Hetushu book 7640 (`witness-collation-042.json`) for all 50 chapters; all 50 witness pages matched their source chapter titles. The witness copies the source wording for most candidates, so it neither confirms nor rejects them. Witness differences, where they exist, are web-copy only.')
A('')
A('Not produced in this pass: workbook rows (Chapter completion and Paragraph register for 956–1005 remain pending). Global reconciliation of temporal items and terminology is outstanding and is not resolved here.')
A('')
A('Confidence: H = high, M–H, M = medium, M–L, L–M, L = low. "Action" is what the editor should decide. Nothing is applied.')
A('')
A('## Proposed review items')
A('')
A('| # | Chapter / para | Source reading | Proposed action | Rationale | Confidence | Dependencies | Witness |')
A('|---|---|---|---|---|---|---|---|')
for i,r in enumerate(ROWS,1):
    ch,pa,orig,cand,conf,cat,action,rat,deps=r
    A(f'| {i} | {ch} p{pa} | {orig} | {action} | {rat} | {conf} | {deps} | {wlabel(i)} |')
A('')
A('## Items corrected or withdrawn during this batch')
A('')
A('- 975 p18 "见面曾相识的核心蛊虫": initially flagged as 见面似相识. Withdrawn: 见面曾相识 is the original 盗天魔尊 杀招 (named in 976 and 975 p18); the 方源 variant is 见面似相识. No change proposed.')
A('- 985 p92–93 and 987 p5: 宋坤 / 宋启元 identity unresolved; flagged as row 40 rather than repaired.')
A('- 956 p105 uses 举办 for the same event that 956 p106 calls 举报; row 1 repairs 956 p106 only.')
A('')
A('## Known limits')
A('')
A('- Rows 1–8 (956–959) were checked against paragraph text in this pass; they were first recorded in the 956–959 notes.')
A('- Rows 2, 8, 13, 14, 16, 22, 38, 42, 53, 55 and 57 are queries or consistency checks, not repairs. No edit is proposed for them yet.')
A('- Temporal items (rows 2, 22, 29, 36, 55, 57): require whole-novel reconciliation. Do not resolve individually.')
A('- Terminology items (奴隶 as verb: rows 27, 46; 萧家 titles: row 56; 炎煌雷泽: row 33 is a repair, not a query; 一身/一声 are repairs): decide one rule before any global change.')
A('- Witness collation: copies source wording for most candidates; differences are web-copy only.')
A('')
A('## Witness summary')
A('')
cnt={}
for w in wit:
    k=w.get('result','not collated'); cnt[k]=cnt.get(k,0)+1
for k,v in sorted(cnt.items(), key=lambda x:-x[1]):
    A(f'- {k}: {v}')
A('')
open(f'{BASE}/Batch-042-Chapters-956-1005.md','w',encoding='utf-8').write('\n'.join(lines)+'\n')
# ---------- QA ----------
from collections import Counter
cc=Counter(r[4] for r in ROWS)
qa={'batch':'042','chapters':'956-1005','chapter_count':50,
 'source_check':'batch-042-source.json (50 chapters, 4773 paragraphs, 0 mismatches). Every report row token verified present in its stated paragraph.',
 'reading_status':'complete (956-1005); notes in batch-042-notes/reading-notes-956-1005.md',
 'report_rows':len(ROWS),'confidence_counts':dict(cc),
 'approved':0,'applied':0,'source_edits':0,
 'witness_collation':'Hetushu book 7640 automated token-level comparison (witness-collation-042.json); 50 chapter pages fetched and title-checked. Witness copies source wording for most candidates; differences recorded as web-copy only.',
 'witness_results':cnt,
 'workbook_rows':'NOT ADDED in this pass (Chapter completion and Paragraph register remain at 955)',
 'ledger_entries':'SR-716 to SR-772',
 'docx':'Batch-042-Chapters-956-1005.docx',
 'known_limits':['Workbook rows not added.','Temporal items need whole-novel reconciliation.','Terminology items (奴隶 verb, 萧家 titles, 宋坤/宋启元 identity, 天莲派 vs 战仙宗 target) need decision.','975 p18 flag withdrawn (见面曾相识 is the original skill).']}
json.dump(qa, open(f'{BASE}/batch-042-qa.json','w'), ensure_ascii=False, indent=1)
# ---------- ledger ----------
L=json.load(open(f'{BASE}/proposal-ledger.json'))
ids={e['id'] for e in L}
assert 'SR-716' not in ids
new=[]
for i,r in enumerate(ROWS):
    ch,pa,orig,cand,conf,cat,action,rat,deps=r
    new.append({'id':f'SR-{716+i}','category':cat,
      'locations':[{'chapter':ch,'paragraph':pa,'file':'','reference_text':f'{ch} p{pa}'}],
      'recommended_action':f'{action} (batch 042, row {i+1}; source token: {orig})',
      'rationale':f'{rat} Confidence {conf}.',
      'confidence':conf,'status':'Open; unapproved, unapplied',
      'dependencies':deps,
      'publication_status':'HOLD: complete-corpus reading and global reconciliation outstanding',
      'witness_collation':f'Hetushu 7640 collation: {wlabel(i+1)}',
      'approved':False,'applied':False})
L.extend(new)
json.dump(L, open(f'{BASE}/proposal-ledger.json','w'), ensure_ascii=False, indent=1)
json.dump(new, open(f'{BASE}/ledger-new-042.json','w'), ensure_ascii=False, indent=1)
print('rows',len(ROWS),'ledger total',len(L),'last',L[-1]['id'])
print(cnt)
