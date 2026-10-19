import json
LP='proposal-ledger.json'
led=json.load(open(LP))
ids={r['id'] for r in led}
assert 'SR-337' in ids and 'SR-338' not in ids
def rec(i,cat,loc,action,rat,conf,status,dep,wit):
    return {"id":i,"category":cat,"locations":[{"chapter":c,"paragraph":p,"file":""} for c,p in loc],
            "recommended_action":action,"rationale":rat,"confidence":conf,"status":status,
            "dependencies":dep,"witness_collation":wit,"approved":False,"applied":False,
            "publication_status":"HOLD: full2334-chapter reading and global reconciliation outstanding"}
HELD="Held repair candidate; no approval"
Q="Provisional query; no approval"
WIT="Not yet collated (Batch 030 witness pending; fact-check-030 not created)."
new=[
rec("SR-338","Transposed fixed phrase (566p16)",[(566,16)],
 "Repair 梅咏雪香 to 咏梅雪香 (cf. 552p7 and 561p58 密语). Held.",
 "The four-step 密语 is 咏梅雪香 in the other passages cited. The 566 form reverses the 梅/咏 order.",
 "Moderate-high (0.6).",HELD,"Whole-novel reconciliation; witness collation for 566.",WIT),
rec("SR-339","Typo: 一翻 for 一遍 (569p57)",[(569,57)],
 "Repair 先实践一翻 to 先实践一遍. Held.",
 "一翻 is not a standard form here; 一遍 (one round) fits the sense of trying the method once first.",
 "Moderate (0.55).",HELD,"Witness collation for 569.",WIT),
rec("SR-340","Typo: 点一边头 for 点头哈腰 (570p75)",[(570,75)],
 "Repair 点一边头哈腰 to 点头哈腰. Held.",
 "Idiom 点头哈腰 is standard; the 一边 insertion looks like a stray character.",
 "Moderate-high (0.7).",HELD,"Witness collation for 570.",WIT),
rec("SR-341","Duplicated word 目光目光 (571p55)",[(571,55)],
 "Repair 目光目光猛地闪烁 to 目光猛地闪烁. Held.",
 "Duplicated 目光 with no stylistic reason; the sentence reads cleanly with one.",
 "Moderate-high (0.7).",HELD,"Witness collation for 571.",WIT),
rec("SR-342","Idiom: 眨眼睛 for 眨眼间 (571p82)",[(571,82)],
 "Repair 眨眼睛就将 to 眨眼间就将. Held.",
 "眨眼间 is the standard expression for 'in a blink'. 眨眼睛 is not standard.",
 "Moderate (0.6).",HELD,"Witness collation for 571.",WIT),
rec("SR-343","Character error: 股 for 蛊 (578p64)",[(578,64)],
 "Repair 赤铁舍利股献上去 to 赤铁舍利蛊献上去. Held.",
 "The object is a Gu throughout 578 (赤铁舍利蛊, 578p41, 578p61). 股 is a clear substitution.",
 "High (0.85).",HELD,"Witness collation for 578.",WIT),
rec("SR-344","Character error: 另 for 令 (580p101)",[(580,101)],
 "Repair 一面另其不断思考 to 一面令其不断思考. Held.",
 "令其 is the standard causative form. 另其 is not a usable form in context.",
 "High-moderate (0.75).",HELD,"Witness collation for 580.",WIT),
rec("SR-345","Idiom error: 刚则易则 for 刚则易折 (580p88)",[(580,88)],
 "Repair 然刚则易则 to 然刚则易折. Held.",
 "The parallel construction and the sense (rigid, so easily broken) point to 易折. 易则 is not idiomatic.",
 "Moderate (0.55).",HELD,"Witness collation for 580.",WIT),
rec("SR-346","Character error: 毕竟 for 逼近 (583p136)",[(583,136)],
 "Repair 他迅速向飞熊毕竟 to 他迅速向飞熊逼近. Held.",
 "The sentence describes Liu Jinglin moving toward the beast (137 counts down distance). 毕竟 does not fit; 逼近 does.",
 "High (0.85).",HELD,"Witness collation for 583.",WIT),
rec("SR-347","Character error: 众所之知 for 众所周知 (584p22)",[(584,22)],
 "Repair 这点众所之知 to 这点众所周知. Held.",
 "众所周知 is the standard idiom; 之 is a substitution.",
 "High (0.85).",HELD,"Witness collation for 584.",WIT),
rec("SR-348","Ownership contradiction: 招灾蛊 (567p171 vs 568p23-29)",[(567,171),(568,23),(568,29)],
 "Query. Decide which reading the text intends: 567p171 says the 招灾蛊 became Fang Yuan's property (成为方源之物) without difficulty; 568p23-29 says he cannot yet refine it and must leave it in the bowl. Do not change either text until resolved.",
 "A reader cannot take ownership and also be unable to refine. Either the 567 line means 'bound/recognised' rather than 'refined', or 568 intends a later reversal. Needs a fuller context check before a repair is proposed.",
 "Moderate (0.5).",Q,"Whole-novel reconciliation of 招灾蛊 timeline (see 566-568, 575p8, 575p14-15).",WIT),
rec("SR-349","Count and role mismatch: 六臂天尸王 composition (569p74 vs 574p60 vs 579p61)",[(569,74),(574,60),(574,62),(579,61),(581,5)],
 "Query. The Gu count and role disagree: 569p74 says six 飞僵蛊 are 辅 and 36 other Gu are included; 574p60 says six 飞僵蛊 are 基石 and 18 Gu are 辅; 579p61 says 支柱. Decide the intended composition before any repair. Do not change any text now.",
 "The count (36 vs 18) and the role label (辅 / 基石 / 支柱) differ across three passages describing the same Gu. The 574p62 line (three 增添生机之蛊) and 581p5 (删减了不少辅助蛊虫) suggest 18 may be the later figure, but that is not decided.",
 "Moderate (0.6).",Q,"Whole-novel reconciliation; check 569-581 for every later count of supporting Gu.",WIT),
rec("SR-350","Possible verb error: 欺的 (572p13)",[(572,13)],
 "Query. 墨瑶意志也就欺的方源智道造诣不深 probably needs a verb; the likely reading is 只能欺负/欺骗方源 or the phrase is a slip. Do not change without a context check.",
 "The phrase is grammatically incomplete as written; the meaning (the intrusion could only deceive Fang Yuan about the depth of his 智道) is inferable, but the verb is missing.",
 "Low-moderate (0.4).",Q,"Witness collation for 572.",WIT),
rec("SR-351","Subject mismatch: 令其 for 令他 (574p40)",[(574,40)],
 "Query. 令其殚精竭虑了 may refer to Fang Yuan, who is the one exhausted; 其 could be read as 墨瑶意志. Check before any change.",
 "The sentence describes Fang Yuan's burden, so 其 should probably be 他. The surrounding text is ambiguous enough to hold it as a query.",
 "Low (0.35).",Q,"Witness collation for 574.",WIT),
rec("SR-352","Doubtful phrase: 前番时间 (582p2)",[(582,2)],
 "Query. 再加上他前番时间 probably needs 前番/前段时间 or 这段时间. Do not change without a context check.",
 "The phrase is awkward; the meaning (Huang Lanshou's recent free opening of the tower) is clear, but the wording is not standard.",
 "Low (0.3).",Q,"Witness collation for 582.",WIT),
]
for r in new: assert r['id'] not in ids
led.extend(new)
# context notes (keep existing status, confidence, and rationale wording)
for r in led:
    if r['id']=='SR-336':
        r['rationale']+=" Batch 030 context (576p52, 580p72): narrator states 常极右 is 常飚's biological son (亲生儿子) and that 常飚 would not acknowledge him; 573p26 is a belief statement and is not counted as narrator truth (corrected in Batch 031); 580p72 has 常极右 addressing him as 义父 publicly. This supports the reading that 565p62 reports the public belief while the narrator's truth is 亲生. Status unchanged; still a query for reconciliation."
    if r['id']=='SR-332':
        r['rationale']+=" Batch 030 context: 584p14 uses 炎道仙蛊 again for 耶律桑's inherited Gu, adding a fourth 炎道 instance with no change of fire-Gu naming. Status unchanged."
json.dump(led,open(LP,'w'),ensure_ascii=False,indent=2)
print('ledger',len(led),'last',led[-1]['id'])
