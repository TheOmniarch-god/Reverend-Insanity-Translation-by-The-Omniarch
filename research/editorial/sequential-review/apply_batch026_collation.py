import json, re
from pathlib import Path
from openpyxl import load_workbook
r = Path('/home/user/editorial/sequential-review')
led = json.loads((r/'proposal-ledger.json').read_text())
R = {
'SR-257':'Witness repeats the same stray “” at the same point. Copied text; no independent support.',
'SR-258':'Witness repeats 极为广场. Copied; no independent support.',
'SR-259':'Witness repeats 神智重复清爽. Copied; no independent support.',
'SR-260':'Witness repeats 就在这是. Copied; no independent support.',
'SR-261':'Witness repeats 吞并葛家 in the same speech. Copied; no independent support. The speech may intend 葛家 as a second target, so the query stays open.',
'SR-262':'Witness repeats 着一个人. Copied; no independent support.',
'SR-264':'Witness has 模棱两可 and not 模棱两口. Supports the proposed correction.',
'SR-267':'Witness repeats 别出机枢. Copied; no independent support.',
'SR-268':'Witness has 恰到好处 and not the EPUB wording. Supports the proposed correction.',
'SR-269':'Witness repeats 哪知蛊. Copied; no independent support. Location corrected to 494p14.',
'SR-270':'Witness has both 二十年 (470p48) and 十几年 (496p38), matching the EPUB. Sleep and absence may be different intervals, so this may not be a true conflict. Confidence lowered.',
'SR-271':'Witness repeats 八十八角珍宝楼 once, but every other mention in 486–505 is 真阳楼. Internal evidence is strong; the witness adds nothing new.',
'SR-272':'Witness repeats 一声皮肤. Copied; no independent support.',
'SR-273':'Witness repeats 而是立即. Copied; no independent support.',
'SR-274':'Witness has 跋涉到天川去 and not the EPUB wording. Supports the proposed correction.',
'SR-275':'Witness repeats 纠克. Copied; no independent support.',
'SR-263':'Witness has both 仙屋蛊 (490p5) and 仙蛊屋 (487p89), matching the EPUB. No independent evidence on the variant.',
'SR-265':'Witness matches the EPUB: 远古 at 490p16 and 太古 at 467p57. No independent evidence.',
'SR-266':'Witness matches the EPUB: 摇光 at 466p74 and 467p6; 瑶光 at 474p75 and 490p76. No independent evidence on the variant.',
}
for v in led:
    if v['id'] in R:
        v['witness_collation'] = R[v['id']]
        v['dependencies'] = 'Hetushu witness (fact-check-026, 486–505 plus 466, 467, 470, 474) checked: ' + R[v['id']] + ' Whole-novel reconciliation outstanding.'
    if v['id']=='SR-269':
        v['locations']=[{'chapter':494,'paragraph':14,'file':''}]
        v['category']='Typo 哪知蛊 for 哪一种蛊 (494p14)'
    if v['id']=='SR-261': v['confidence']='Low-moderate (0.4).'
    if v['id']=='SR-270':
        v['confidence']='Low-moderate (0.4).'
        v['recommended_action']='Query. Check whether 496p38 (more than ten years absent) and 470p48 (twenty years of sleep) describe different intervals before any change.'
(r/'proposal-ledger.json').write_text(json.dumps(led,ensure_ascii=False,indent=2))
# workbook
wb = load_workbook(r/'Sequential-Reading-and-Proposals.xlsx')
ws = wb['Proposal ledger']
hdr = [c.value for c in ws[1]]
ci = {h:i for i,h in enumerate(hdr)}
n=0
for row in ws.iter_rows(min_row=2):
    sid = row[0].value
    if sid in R:
        row[ci['Dependencies']].value = led[[v['id'] for v in led].index(sid)]['dependencies']; n+=1
    if sid=='SR-269':
        row[ci['Category']].value='Typo 哪知蛊 for 哪一种蛊 (494p14)'; row[ci['References']].value='Ch494 p14'
    if sid in ('SR-261','SR-270'):
        row[ci['Confidence']].value='Low-moderate (0.4).'
    if sid=='SR-270':
        row[ci['Action']].value=led[[v['id'] for v in led].index('SR-270')]['recommended_action']
wb.save(r/'Sequential-Reading-and-Proposals.xlsx')
print('workbook rows updated', n)
# report
p=r/'Batch-026-Chapters-486-505.md'; s=p.read_text(encoding='utf-8')
s=s.replace('| SR-269 | 494p13 |','| SR-269 | 494p14 |')
s=s.replace('| SR-261 | 488p78 | 吞并葛家 vs 费家: the target of the 马家 takeover is likely 费家, not the 葛家 ally. Moderate (0.6). |',
            '| SR-261 | 488p78 | 吞并葛家 vs 费家: the target of the 马家 takeover is likely 费家, not the 葛家 ally. Low-moderate (0.4). |')
s=s.replace('| SR-270 | 496p38 vs 470p48 | Absence of 常山阴: more than ten years vs twenty years. Moderate (0.6). |',
            '| SR-270 | 496p38 vs 470p48 | Absence of 常山阴: more than ten years vs twenty years of sleep. These may be different intervals. Low-moderate (0.4). |')
start=s.index('## 5. External collation'); end=s.index('## 6. Status')
s=s[:start]+'''## 5. External collation

- Witness: Hetushu (single repost tradition, not an authorial master). Pages fetched for 486–505, plus 466, 467, 470 and 474 for the cross-batch queries.
- Method: fragment-level check of each proposal's current and proposed wording in the normalized witness text. No whole-chapter comparison.
- Result summary (detail per proposal in the ledger field witness_collation):
  - Supports the correction: SR-264, SR-268, SR-274 (witness already has the proposed form).
  - Witness repeats the EPUB wording (copied, no independent support): SR-257 to SR-262, SR-267, SR-269, SR-272, SR-273, SR-275.
  - Internal evidence is strong, witness adds nothing: SR-271 (珍宝楼 occurs once in the batch; all other mentions are 真阳楼).
  - Witness matches the EPUB in cases where the variant itself is the question: SR-261, SR-263, SR-265, SR-266, SR-270. No resolution from the witness.
- Correction: SR-269 location is 494p14, not 494p13. The earlier 494p13 reference was an off-by-one error.
- Caveat: the witness copies the EPUB in most cases, so the witness cannot confirm an authorial reading for those. Witness support is treated as weak for the copied items.
- Do not use 5345239+n: it fetches chapter n+1.

'''+s[end:]
s=s.replace('- Deliverables: this report, Batch-026-Numbered-Chinese-Source.md, proposal-ledger.json, reading-progress.json. DOCX, workbook rows and QA follow.',
            '- Deliverables: this report, Batch-026-Numbered-Chinese-Source.md, proposal-ledger.json, reading-progress.json, the DOCX and the workbook.')
p.write_text(s,encoding='utf-8')
print('report updated', '494p14' in s, 'Low-moderate' in s)
