import json, openpyxl, subprocess
SR='/home/user/editorial/sequential-review'
rows=[
(48,"850 p6","能能看出","Repair 能能 to 能","能能看出 is a doubled-character slip; 能看出 appears 4 times.","H","0.95","none","Typo or wording repair candidate",850,6),
(49,"850 p9","只是表现现象","Repair 表现现象 to 表面现象","The phrase means the surface appearance of the damage; 表现现象 occurs once, and the surrounding sentence describes the outward effect.","M–H","0.80","none","Typo or wording repair candidate",850,9),
(50,"842 p4","从中中阶出出题者的用意","Repair to 从中阶出题者的用意 (delete the doubled 中 and 出); confirm whether 看 is missing","Doubled characters in the source; the intended sense is studying the setter's intent from the intermediate-level questions. Two possible repairs; editor to choose.","M","0.60","none","Typo or wording repair candidate",842,4),
(51,"841 p16","仙蛊唯一，太太太难炼制成功了","Repair 太太太 to 太太 (or 太)","Triple 太 is an unlikely stutter in narration; 太太 is the common form.","M","0.65","none","Typo or wording repair candidate",841,16),
(52,"841 p67","但，这这这方源，怎么一上来就炼蛊了？","Query: 这这这 (dialogue stutter or slip)","Triple 这 also appears at 831 p51. Decide one rule for dialogue stutter before any edit; do not change individually.","L–M","0.40","831 p51 (same form)","Decision / whole-novel reconciliation",841,67),
]
md=open(f'{SR}/Batch-039-Chapters-806-855.md',encoding='utf-8').read().split('\n')
idx=[i for i,l in enumerate(md) if l.startswith('| 47 |')][0]
new=[f"| {n} | {ref} | {rd} | {act} | {rat} | {lab} ({num}) | {deps} |" for n,ref,rd,act,rat,lab,num,deps,cat,c,p in rows]
md[idx+1:idx+1]=new
txt='\n'.join(md)
txt=txt.replace('Status: **source reading complete (806–855)','Status: **source reading complete (806–855); line-level recheck of 838–855 added rows 48–52 (automated rare-pattern scan plus targeted reading)**. Status (earlier)',1) if 'line-level recheck' not in txt else txt
open(f'{SR}/Batch-039-Chapters-806-855.md','w',encoding='utf-8').write(txt)
subprocess.run(['python3','/home/user/tmp/md2docx.py','Batch-039-Chapters-806-855.md','Batch-039-Chapters-806-855.docx'],cwd=SR,check=True)
L=json.load(open(f'{SR}/proposal-ledger.json'))
last=max(int(e['id'].split('-')[1]) for e in L); assert last==710,last
ent=[]
for n,ref,rd,act,rat,lab,num,deps,cat,c,p in rows:
    sid=f'SR-{last+n-47:03d}'
    status='Held repair candidate; unapproved, unapplied' if cat.startswith('Typo') else ('Open decision; unapproved, unapplied' if cat.startswith('Decision') else 'Query; unapproved, unapplied')
    ent.append({'id':sid,'category':cat,'locations':[{'chapter':c,'paragraph':p,'file':'','reference_text':ref}],
      'recommended_action':f"{act} (batch 039, row {n}, source reading: {rd})",'rationale':f"{rat} Confidence {lab}.",
      'confidence':lab,'status':status,'dependencies':deps,'publication_status':'HOLD: complete-corpus reading and global reconciliation outstanding',
      'witness_collation':'Not collated: no single-token candidate for automated witness check.','approved':False,'applied':False})
json.dump(ent,open(f'{SR}/ledger-new-039-recheck.json','w'),ensure_ascii=False,indent=1)
L+=ent; json.dump(L,open(f'{SR}/proposal-ledger.json','w'),ensure_ascii=False,indent=1)
wb=openpyxl.load_workbook(f'{SR}/Sequential-Reading-and-Proposals.xlsx')
ws=wb['Proposal ledger']
for e in ent:
    ws.append([e['id'],e['category'],e['locations'][0]['reference_text'],e['recommended_action'],e['rationale'],e['confidence'],e['status'],e['dependencies'],e['publication_status'],'No','No',e['witness_collation']])
pr=wb['Paragraph register']
key={(e['locations'][0]['chapter'],e['locations'][0]['paragraph']):e['id'] for e in ent}
hit=0
for row in pr.iter_rows(min_row=2):
    k=(row[0].value,row[1].value)
    if k in key:
        cur=row[3].value
        row[3].value=key[k] if not cur else cur+', '+key[k]
        hit+=1
wb['Read me'].cell  # ensure sheet
for r in wb['Read me'].iter_rows():
    if r[0].value=='Proposals': r[1].value='715 total (SR-001 to SR-715); batches 036–041 and 039 recheck added; nothing approved or applied'
wb.save(f'{SR}/Sequential-Reading-and-Proposals.xlsx')
print('added',len(ent),ent[0]['id'],ent[-1]['id'],'register links',hit)
