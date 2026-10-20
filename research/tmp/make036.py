import json, os
SR='/home/user/editorial/sequential-review'
# (ch, para, source reading, action, rationale, conf_label, conf_num, deps, category, defs_row or None)
R=[
(686,9,"并铺上神猿","Repair 并铺 to 冰瀑 (冰瀑神猿)","冰瀑神猿 is the higher-grade 上古 form (686 p7, 11, 21, 22, 32, 71; 688 p17). 701 p4 separates the lesser 冰刺神猿, so the names are distinct. 并铺 is a typo.","H","0.90","686 p7–71; 688 p17; 701 p4 (distinct 冰刺)","Typo or wording repair candidate",1),
(686,12,"努力告吹","Query: keep unless a clearer idiom is chosen","告吹 means 'fall through'; the phrase is understandable but unusual. No edit proposed.","L–M","0.40","none","Query",25),
(686,61,"应誓而亡","Repair to 违誓而亡","违誓 is the expected idiom (违誓 at 815 p41, 816 p60). 应誓 also appears at 725 p68 and 778 p78; decide those together.","M–H","0.80","725 p68; 778 p78 (应誓 check)","Typo or wording repair candidate",2),
(687,47,"乐意疯狂生产","Repair to 意志疯狂生产","乐意 does not fit 'frenzied production'; 意志 fits. Single-line context. Check 乐意 uses in batch 036–041 before applying.","M–H","0.80","batch-wide 乐意 check","Typo or wording repair candidate",3),
(689,82,"暗牢","Repair to 黑牢","黑牢 is used 51 times in the corpus; 暗牢 once. The cage is 黑牢 elsewhere in 689.","H","0.90","689 p32–47 (黑牢)","Typo or wording repair candidate",4),
(690,18,"守开云雾","Repair to 拨开云雾","The same idiom is 拨开云雾 at 821 p10. 守 is a likely misreading.","M–H","0.85","821 p10","Typo or wording repair candidate",5),
(691,28,"亲身女儿","Query: decide 亲身 vs 亲生 for daughter and father across the novel","亲身 is used for 女儿 at 691 p28, 691 p68, 773 p13, 773 p57; 亲身父亲 at 940 p76 (witness shows candidate 亲生父亲); 亲生女儿 at 943 p111. Whole-novel decision needed.","L–M","0.45","940 p76; 943 p111","Decision / whole-novel reconciliation",26),
(691,31,"怎么半","Repair to 怎么办","怎么办 is the standard phrase (29 hits); 怎么半 reads as a typo.","M–H","0.90","none","Typo or wording repair candidate",7),
(692,15,"力道绝仙","Query: variant form (力绝仙体)","Relevant to the batch 037 query on 力绝仙体 (714 p56). Choose one form before any edit.","L–M","0.40","714 p56 (batch 037 query)","Decision / whole-novel reconciliation",27),
(692,49,"乐山乐意仙蛊","Query: name variant (乐山乐水 vs 乐意)","乐山乐水 is the majority reading in the corpus (58 vs 18). This is already open for batch 037 (709 p55; 748; 749; 754 p84/87).","L–M","0.45","batch 037 open query","Decision / whole-novel reconciliation",28),
(692,54,"再此基础上","Repair to 在此基础上","在此基础上 is the standard phrase (734 p12). 再 reads as a typo.","M–H","0.85","734 p12","Typo or wording repair candidate",6),
(693,27,"仙元石回复道三十六块","Repair 回复道 to 恢复到","恢复到 is the form at 861 p99 and 902 p19. 回复道 is not used elsewhere.","M–H","0.85","861 p99; 902 p19","Typo or wording repair candidate",8),
(694,75,"把我们的家主阁都给撞踏了","Repair 撞踏 to 撞塌","撞塌 is the form at 694 p60 and p63, in the same scene. 撞踏 is unique.","M–H","0.90","694 p60, 63","Typo or wording repair candidate",9),
(695,3,"房屋建筑塌毁倒塌","Repair to 房屋建筑倒塌 (delete one duplicate verb)","Two near-synonyms are stacked (塌毁 and 倒塌). One verb is clearer.","L–M","0.50","none","Typo or wording repair candidate",12),
(695,17,"数百道金色光刀，斩击在的方源身上","Repair to 斩击在方源身上 (delete stray 的)","Stray 的 between 在 and 方源.","M","0.70","none","Typo or wording repair candidate",11),
(695,22,"方源真正要炼蛊什么的，需求量一定很大","Query: sentence reads awkwardly","Possible garble; no edit proposed without a fuller check.","L–M","0.35","none","Query",None),
(695,24,"将这些统统收如囊中","Repair to 收入囊中","收入囊中 is the standard form (6 corpus hits). Batch 040 row 13 applies the same repair.","M–H","0.90","batch 040 row 13","Typo or wording repair candidate",10),
(697,5,"已经持续了大半年","Query: temporal check (大半年)","大半年 appears at 697 p5, 745 p63, 746 p41, 871 p28. Include in the temporal group already open for batch 037.","L","0.30","745 p63; 746 p41; 871 p28","Decision / whole-novel reconciliation",None),
(697,21,"第四位蛊仙点滴啊头","Repair to 点了点头","点了点头 appears 4 times elsewhere; 点滴啊头 is a typo.","H","0.95","none","Typo or wording repair candidate",13),
(697,43,"效果虽然不大，但日积月累，却是可观","Query: 可观 usage (batch-wide)","可观 appears 9 times. Batch 040 row 28 is held M–L pending a batch-wide decision.","M–L","0.30","batch 040 row 28","Decision / whole-novel reconciliation",None),
(698,5,"凤九歌居然主动将我素仙蛊，借给我用","Query: 我素仙蛊 vs 我素蛊","我素仙蛊 appears 3 times; 我素蛊 appears 7 times (696 p35–37; 698 p5–9; 700 p16). Same chapter uses both forms.","L–M","0.40","696 p35; 698 p5–9; 700 p16","Decision / whole-novel reconciliation",32),
(698,26,"面若挑花","Repair to 面若桃花","挑花 appears once; 桃花 is the usual image (698 p47; 757 p72).","M–H","0.80","757 p72","Typo or wording repair candidate",14),
(698,47,"枝条纠缠一起","Repair to 纠缠在一起","纠缠在一起 appears 6 times; 纠缠一起 once.","M–H","0.85","none","Typo or wording repair candidate",15),
(698,60,"这么时间，都感应不到","Repair to 这么长时间","这么长时间 is used at 723 p28; 这么时间 is unique.","M–H","0.85","723 p28","Typo or wording repair candidate",16),
(699,38,"你却仍旧无法那个男人的阴影","Repair to 无法摆脱那个男人的阴影","Missing verb; 无法那个 occurs once.","H","0.90","none","Typo or wording repair candidate",17),
(699,54,"点点会会的魂泪","Repair to 点点滴滴的魂泪","会会 occurs once; 点点 is common (130 hits).","M","0.65","none","Typo or wording repair candidate",18),
(699,63,"走了多少不","Repair to 走了多少步","多少不 occurs once; 多少步 is the intended form.","H","0.90","none","Typo or wording repair candidate",19),
(699,67,"他的嘴张的老大","Repair to 张得老大","张得老大 appears at 859 p66.","M–H","0.85","859 p66","Typo or wording repair candidate",20),
(699,84,"这仙蛊仙鹤门太上二长老之物","Repair to 这仙蛊是仙鹤门太上二长老之物","Missing 是; no other form in the corpus.","M–H","0.85","none","Typo or wording repair candidate",21),
(700,18,"狐仙福地中，最安全的对方，就是荡魂山了","Repair 对方 to 地方","安全的地方 at 806 p75; 安全的对方 occurs once. Witness shows candidate wording.","H","0.90","806 p75","Typo or wording repair candidate",22),
(700,36,"排序先后和仙鹤门当场","Query: unclear phrase","Meaning unclear; needs a fuller check before any edit.","M","0.50","none","Query",29),
(702,3,"红枣仙元","Query: 红枣仙元 vs 青提仙元 (second currency or slip?)","红枣仙元 appears 10 times (702, 703, 729, 732, 790); 青提仙元 appears 55 times. Probably intentional; confirm.","L","0.30","whole-novel currency check","Decision / whole-novel reconciliation",33),
(702,63,"原先晴空万里无语","Repair to 晴空万里无云","无语 is a slip. 703 p71 (湛蓝无云) and 813 p2 (万里无云) confirm the image.","H","0.90","703 p71; 813 p2","Typo or wording repair candidate",23),
(703,44,"魂兽…重新凝绝成新的魂兽","Repair 凝绝 to 凝聚","凝聚成 is used 11 times; 凝绝 once.","H","0.90","none","Typo or wording repair candidate",24),
(703,75,"你们俩个动用了真正手段","Query: 俩个 vs 两个 (batch-wide)","俩个 appears 10 times; 两个人 appears 4 times. Needs a batch-wide decision; no edit proposed here.","L–M","0.40","690 p58; 692 p18; 705 p58 (batch-wide)","Decision / whole-novel reconciliation",34),
(704,69,"经过三百多万的抗争、演变、积累","Query: possible missing 年 (三百多万年?)","三百多万 appears here and at 948 p4; 三百多年 is used 4 times (719 p36, 734 p31, 737 p54, 838 p52). Check the era scale.","M","0.50","948 p4; 719 p36; 734 p31; 737 p54; 838 p52","Decision / whole-novel reconciliation",30),
(704,70,"十大派掌握着中洲八成的修行资源 (also p74)","Query: conflicts with 697 p39 (六成)","697 p39 says six-tenths; 704 p70 and p74 say eight-tenths for the same share. Whole-novel numeric decision.","M","0.50","697 p39 vs 704 p70, 74","Decision / whole-novel reconciliation",None),
(705,38,"一年多前，在宝黄天中暗算他的那个神秘势力","Query: temporal check","The ambush in 宝黄天 'a year-plus ago' should match the timeline in 685–690.","L–M","0.45","685–690 timeline","Decision / whole-novel reconciliation",31),
]
NOCTX_ROW=[i for i,r in enumerate(R,1) if r[0]==699 and r[1]==38][0]
CONF_ROW=[i for i,r in enumerate(R,1) if r[0]==704 and r[1]==70][0]
W={w['row']:w for w in json.load(open(f'{SR}/witness-collation-036.json'))}
defs={d['row']:d for d in json.load(open('/home/user/tmp/defs-036.json'))}
def wit(dr):
    if dr is None: return 'Not collated: no single-token candidate for automated witness check.'
    w=W[dr]; s=f"Hetushu 7640 (ch{w['ch']}): {w['result']}"
    if w['result']=='witness shows candidate wording': s+='; witness differs from source here and matches the proposed wording (web copy, not authoritative)'
    return s
rows=[]
for i,r in enumerate(R,1):
    ch,p,rd,act,rat,lab,num,deps,cat,dr=r
    rows.append(dict(n=i,ch=ch,p=p,reading=rd,action=act,rationale=rat,label=lab,num=num,deps=deps,cat=cat,dr=dr,wit=wit(dr)))
# report
md=[]
md.append("# Batch 036 — Chapters 686–705 (sequential source review)\n")
md.append("Status: **source reading complete (686–705)**. Reading notes: `editorial/sequential-review/batch-036-notes/reading-notes-686-705.md`. This report is a candidate list only. Nothing here is approved, applied, or published, and no Chinese source has been changed.\n")
md.append("Source check: `batch-036-source.json` (20 chapters, 1601 paragraphs, 0 mismatches at build time). Witness collation: `witness-collation-036.json` (Hetushu book 7640; pages for ch686–705 fetched; chapter titles match the reading-note sections, 第三十七章 to 第五十六章). Witness copies the source wording for most candidates, so it neither confirms nor rejects them.\n")
md.append("Confidence labels: H, M–H, M, M–L, L–M, L; numeric values in brackets. \"Action\" is what the editor should decide. Nothing is applied.\n")
md.append("## Proposed review items\n")
md.append("| # | Chapter / para | Source reading | Proposed action | Rationale | Confidence | Dependencies |")
md.append("|---|---|---|---|---|---|---|")
for x in rows:
    md.append(f"| {x['n']} | {x['ch']} p{x['p']} | {x['reading']} | {x['action']} | {x['rationale']} | {x['label']} ({x['num']}) | {x['deps']} |")
md.append("\n## Witness summary\n")
for x in rows:
    if x['dr'] is not None:
        md.append(f"- Row {x['n']} ({x['ch']} p{x['p']}, {x['reading']}): {W[x['dr']]['result']}.")
md.append(f"\nOnly the 700 p18 row shows candidate wording. Row "+str(NOCTX_ROW)+" (699 p38) has no matching witness context. The others copy the source wording, which is not independent confirmation.\n")
md.append("## Cross-batch notes (not rows)\n")
md.append("- 冰瀑神猿 and 冰刺神猿 are distinct beasts (701 p4). Do not unify.")
md.append("- 沙硕 appears at 694 p2 and 906 p36; treat as one consistent term. Batch 041 flag on 906 p36 should be withdrawn.")
md.append("- 乐山乐水 vs 乐意 (692 p49) belongs to the batch 037 open query.")
md.append(f"- 八成 (704) vs 六成 (697) for the ten-sect resource share is a whole-novel conflict (row "+str(CONF_ROW)+").")
md.append("- 挪移, 魅蓝电影, and 这么的 were dropped as recurring usage; not proposed.")
md.append("\nThe batch 036 notes at 686 p12 are recorded as a query only.")
open(f'{SR}/Batch-036-Chapters-686-705.md','w',encoding='utf-8').write("\n".join(md)+"\n")
# ledger
ledger=[e for e in json.load(open(f'{SR}/proposal-ledger.json')) if int(e['id'].split('-')[1])<=672]
last=max(int(e['id'].split('-')[1]) for e in ledger)
assert last==672,last
new=[]
for x in rows:
    sid=f"SR-{last+x['n']:03d}"
    status = 'Held repair candidate; unapproved, unapplied' if x['cat'].startswith('Typo') else ('Open decision; unapproved, unapplied' if x['cat'].startswith('Decision') else 'Query; unapproved, unapplied')
    new.append({'id':sid,'category':x['cat'] if x['cat'].startswith(('Typo','Decision','Query')) else 'Query',
      'locations':[{'chapter':x['ch'],'paragraph':x['p'],'file':'','reference_text':f"{x['ch']} p{x['p']}"}],
      'recommended_action':f"{x['action']} (batch 036, row {x['n']}, source reading: {x['reading']})",
      'rationale':f"{x['rationale']} Confidence {x['label']}.",'confidence':x['label'],'status':status,
      'dependencies':x['deps'],'publication_status':'HOLD: complete-corpus reading and global reconciliation outstanding',
      'witness_collation':x['wit'],'approved':False,'applied':False})
json.dump(new,open(f'{SR}/ledger-new-036.json','w'),ensure_ascii=False,indent=1)
ledger+=new
json.dump(ledger,open(f'{SR}/proposal-ledger.json','w'),ensure_ascii=False,indent=1)
from collections import Counter
conf=Counter(x['label'] for x in rows)
qa={'batch':'036','chapters':'686–705','chapter_count':20,'source_check':'batch-036-source.json; 20 chapters; 1601 paragraphs; 0 mismatches at build time',
 'reading_status':'Complete through ch705 (reading notes 686–705)','report_rows':len(rows),'confidence_counts':dict(conf),
 'approved':0,'applied':0,'source_edits':0,
 'witness_collation':'witness-collation-036.json (Hetushu 7640, ch686–705, 20 pages; chapter titles 第三十七章–第五十六章)',
 'witness_results':dict(Counter(W[r]['result'] for r in W)),'witness_candidates_checked':len(W),
 'ledger_ids':[new[0]['id'],new[-1]['id']],'ledger_count':len(new),'workbook_rows':'pending (appended after ledger)',
 'docx':'Batch-036-Chapters-686-705.docx','known_limits':['Witness copies source wording for most candidates; not independent confirmation.','No line-level bilingual audit; source review only.','Temporal and numeric items are whole-novel decisions, not local repairs.']}
json.dump(qa,open(f'{SR}/batch-036-qa.json','w'),ensure_ascii=False,indent=1)
print(len(rows), new[0]['id'], new[-1]['id'], dict(conf))
