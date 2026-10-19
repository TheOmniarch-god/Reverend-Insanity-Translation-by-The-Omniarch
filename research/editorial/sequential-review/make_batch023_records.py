from pathlib import Path
import json
r=Path(__file__).parent
b=json.loads((r/'batch-023-source.json').read_text())
led=json.loads((r/'proposal-ledger.json').read_text())
assert len(led)==193 and led[-1]['id']=='SR-193'
PUB='HOLD: full2334-chapter reading and global reconciliation outstanding'
DEP='Whole-novel reconciliation; witness check for Batch 023 (not yet collated).'
def rec(i,cat,locs,action,rat,conf,status,dep=DEP):
    return {'id':f'SR-{i}','category':cat,'locations':[{'chapter':c,'paragraph':p,'file':''} for c,p in locs],
            'recommended_action':action,'rationale':rat,'confidence':conf,'status':status,'dependencies':dep,
            'approved':False,'applied':False,'publication_status':PUB}
P='Provisional proposal or query; no approval'
new=[
rec(194,'Huang Lou Lan reign length (427p19 vs 427p22)',[(427,19),(427,22)],
 'Query. Do not alter. Either the ten-year figure or the two-year figure is an error, or they refer to different intervals.',
 'Source-internal conflict within one chapter. Not yet checked against earlier chronology.','Query only (0.4 that an error exists).',P,'Whole-novel chronology for the Huang Lou Lan and Ma Hongyun succession.'),
rec(195,'Unclear word 冤枉 (437p22)',[(437,22)],
 'Query. Possible garbling of an adverb or phrase. No repair until a witness is checked.',
 '冤枉 does not fit the sunlit grassland description.','Low (0.3) for any specific reading.',P,'External collation of 437.'),
rec(196,'Typo 旦 for 但 (436p89)',[(436,89)],
 'Propose 但有飘渺至极的可能.','旦 is probably a slip for 但 in this context.','Moderate-high (0.8).','Held repair candidate; unapproved.'),
rec(197,'Typo 和起 for 和他 (443p27)',[(443,27)],
 'Propose 和他相比.','和起 does not parse; 和他 fits the comparison with the wolf-king figure.','High (0.85).','Held repair candidate; unapproved.'),
rec(198,'Typo 燃烧这 for 燃烧着 (445p26)',[(445,26)],
 'Propose 静静地燃烧着.','这 is probably 着 in this aspect construction.','High (0.85).','Held repair candidate; unapproved.'),
rec(199,'Stray 地 before 方源 (439p4)',[(439,4)],
 'Propose 方源有意接近，有所图谋.','The 地 has no grammatical role.','Moderate-high (0.8).','Held repair candidate; unapproved.'),
rec(200,'Repeated 当 (436p30)',[(436,30)],
 'Propose 当时，当这头驼狼.','The repeated 当 is probably a slip; a comma clarifies the time clause.','Moderate (0.7).','Held repair candidate; unapproved.'),
rec(201,'Stray 着 in 男人们着蹲在 (441p9)',[(441,9)],
 'Propose 男人们蹲在买铁器的摊子前.','着 breaks the verb phrase.','Moderate-high (0.8).','Held repair candidate; unapproved.'),
rec(202,'Possible 重地 for 重点 (442p58)',[(442,58)],
 'Propose 重点是二转、三转的驭狼蛊.','重地 does not parse in this sentence; 重点 fits the list of focus items.','Moderate (0.7).','Held repair candidate; unapproved.'),
rec(203,'Arithmetic: ten-jun strength Gu stacking (443p30–33)',[(443,30),(443,31),(443,33)],
 'Query. Confirm the stacking rule and the applied count against the stated total of twenty jun.',
 'Three ten-jun applications would give thirty jun under stacking; the text gives twenty and states the stacking limit without a figure.',
 'Query only.',P,'Whole-novel reconciliation of strength-Gu stacking rules.'),
rec(204,'Unclear 嫉妒 in 真元嫉妒匮乏 (438p76)',[(438,76)],
 'Propose 他们真元早已匮乏.','嫉妒 (envy) does not fit the sentence about depleted spirit power.','Moderate (0.7).','Held repair candidate; unapproved.'),
rec(205,'Unclear 正值 in 德行和正值 (440p10)',[(440,10)],
 'Propose 你的德行和正直广为传颂.','正值 does not fit; 正直 matches the praise of conduct.','Moderate (0.6).','Held repair candidate; unapproved.'),
rec(206,'Possible 远出 for 远超 (438p43)',[(438,43)],
 'Propose 风狼王智慧要远超其他野狼.','远出 does not parse in the comparison; 远超 fits.','Moderate (0.7).','Held repair candidate; unapproved.'),
rec(207,'Narrative knowledge of future biography (431p48)',[(431,48)],
 'Query. Check how Fang Yuan knows the later biography of Chang Shanyin.',
 'The biography is written after the death described in 431, yet the narrator attributes Fang Yuan\'s knowledge to it.',
 'Query only.',P,'Earlier batches on Fang Yuan\'s knowledge sources; whole-novel chronology.'),
rec(208,'Chronology: rescue and Ma Hongyun age (431p23, 431p44, 431p66, 441p50, 432p80, 440p6)',[(431,23),(431,44),(431,66),(441,50),(432,80),(440,6)],
 'Query. Hold for whole-novel chronology. The present year is not stated.',
 'The battle is "二十几年前"; Ma Hongyun finds Chang Shanyin "三十多年后"; rescue about ten years away; Ma Hongyun about thirteen now; Fang Yuan floated about twenty years. These are roughly consistent only if the battle was about twenty-two years ago.',
 'Query only.',P,'Whole-novel timeline anchors for the Chang Shanyin death, the Ma Hongyun rescue, and Ma Hongyun\'s birth.'),
]
led.extend(new)
(r/'proposal-ledger.json').write_text(json.dumps(led,ensure_ascii=False,indent=1))
print('ledger',len(led))
p=json.loads((r/'reading-progress.json').read_text())
p['sequential_chapters_completed']=list(range(1,446))
p['paragraphs_read']=38245+sum(len(c['paragraphs']) for c in b)
p['paragraph_characters_read']=1328051+sum(sum(len(t) for t in c['paragraphs']) for c in b)
p['next_chapter']=446; p['remaining_chapters']=2334-445
p['batch_report']='Batch-023-Chapters-426-445.md'
p['scope']='Full sequential Chinese reading through445; selected external collation, not fresh live bilingual audit'
p['batches']=23; p['chapters']=445
(r/'reading-progress.json').write_text(json.dumps(p,ensure_ascii=False,indent=2))
print(p['paragraphs_read'],p['paragraph_characters_read'],p['next_chapter'],p['remaining_chapters'])
# numbered source
out=['# Batch 023 Numbered Chinese Source (Chapters 426–445)','','Source: Gu-Zhen-Ren.epub, one line per paragraph. Numbering is paragraph within chapter.','']
for c in b:
    out.append(f"## Chapter {c['corpus_chapter']} {c['title']}"); out.append('')
    for i,t in enumerate(c['paragraphs'],1): out.append(f"{c['corpus_chapter']}.{i} {t}".replace(f"{c['corpus_chapter']}.","",1) if False else f"{i}. {t}" if False else f"{i} {t}")
    out.append('')
(r/'Batch-023-Numbered-Chinese-Source.md').write_text('\n'.join(out),encoding='utf-8')
print('numbered written')
