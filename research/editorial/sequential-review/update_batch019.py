from pathlib import Path
import json,shutil,hashlib,re
from openpyxl import Workbook,load_workbook
from openpyxl.styles import Font,PatternFill,Alignment
r=Path('/home/user/editorial/sequential-review')
def load(n):return json.loads((r/n).read_text())
def save(n,v):(r/n).write_text(json.dumps(v,ensure_ascii=False,indent=2))
for n in ['reading-progress.json','proposal-ledger.json','chronology-register.json','resource-register.json','working-standards-register.json']:
 p=r/'history'/('before-batch019-'+n)
 if not p.exists():shutil.copy2(r/n,p)
cs=sum([load(f'batch-{i:03d}-source.json') for i in range(1,20)],[]);by={c['corpus_chapter']:c for c in cs};batch=[by[n] for n in range(356,366)]
def src(c,p):return dict(chapter=c,paragraph=p,file=by[c]['file'],text=by[c]['paragraphs'][p-1])
def ss(rr):return [src(*z) for z in rr]
def loc(rr):return [{k:v for k,v in z.items() if k!='text'} for z in ss(rr)]
def refs(z):return '; '.join(f"Ch{x['chapter']} p{x['paragraph']}" for x in z)
# Preserve the established reader-copy omissions. No new omissions in356–365.
old18=(r/'update_batch018.py').read_text();exec(old18[old18.index('def reader('):old18.index("ledger=load(")])
ledger=load('history/before-batch019-proposal-ledger.json');new=[]
def pro(i,cat,rr,action,why,conf,dep):
 v=dict(id=f'SR-{i:03d}',category=cat,locations=loc(rr),recommended_action=action,rationale=why,confidence=conf,status='Provisional proposal or query; no approval',dependencies=dep,approved=False,applied=False,publication_status='HOLD: full2334-chapter reading and global reconciliation outstanding');ledger.append(v);new.append(v);return v
pro(156,'Bone Wings: two pairs versus one pair',[(358,75),(358,77),(361,12)],'Prefer358p75 两对→一对 if the resting Gu shape is intended to represent the deployed wings. English candidate: a pair of folded wings.','358 describes two pairs while the immediately following deployment produces two wings, and361 explicitly names one pair. External358/361 repeat the differing counts.','High confidence in different descriptions; moderate-to-high confidence in one-pair repair.','The resting Gu’s pattern might differ from actual anatomy. Old Footless Bird had four wings227p136, but it is a different creature/form and cannot settle the transformed human anatomy. Do not globally replace two pairs.')
pro(157,'Tie Ba Xiu: peak-stage label versus upper-stage cultivation',[(358,32),(359,4),(361,23),(362,59),(363,63)],'Preferred361p23 四转巅峰→四转高阶. English candidate: this Revolution Four upper-stage strength-path Gu Master.','359 and362 expressly identify upper cultivation;362 separately explains battle strength exceeding ordinary Four peak.361 uses peak as a direct descriptor of the Gu cultivator, not an explicit comparison of fighting power. Checked external passages retain the conflict.','High local support for the cultivation correction; not independently authenticated authorial text.','Keep his Five Earth Overlord Gu and above-ordinary-Four-peak combat power. The requested Four-peak reinforcement356 does not require him to be Four peak himself.')
pro(158,'Reinforcement leader: Li Xian report versus actual command',[(358,32),(359,9),(359,11)],'Retain the quoted report for now and flag the discrepancy. If editorial harmonisation is chosen, replace 首领便是 with 主力便是, identifying Ba Xiu as the principal fighting force rather than commander.','Li Xian calls Ba Xiu leader; the next chapter explicitly gives command to Tie Ruo Nan and makes Ba Xiu her subordinate. Both readings occur in the external repost. Li may have incomplete information or may loosely identify the strongest member.','High confidence in contrasting labels; moderate confidence that a source correction is required.','Do not silently turn mistaken character information into accurate omniscient narration. The 主力 replacement is a proposed clarification, not an attested alternative reading.')
pro(159,'Legendary cauldron: oil and water wording',[(357,26),(357,39),(357,41),(357,44),(357,76)],'Hold a fluid-description query. Preserve oil cauldron and water as quoted; choose no global oil-to-water or water-to-oil substitution. A less specific cauldron/liquid rendering would be an explicit editorial harmonisation, not exact lexical equivalence.','The same cooking/refinement scene is framed by oil cauldron but repeatedly describes water. The repost repeats both. Dictionary油锅 has literal oil-vessel and legendary punishment-cauldron senses, reducing confidence that physical composition alone settles the matter.','High quotation confidence; moderate lexical/material tension; low confidence in selecting the intended fluid.','Magical recipe additions are not evidence of a specified oil-to-water conversion. Do not invent one. No hot/boiling temperature should be added before the text actually heats the contents.')
pro(160,'Yan junior lord: 军 versus 君',[(364,37),(364,42)],'Flag炎军/炎君 as same-person Chinese variants. Use炎军 only as a provisional first-occurrence index form; keep English Yan Jun unchanged.','The same question-and-answer scene alternates the final character. External364 also alternates, so it does not select an authoritative spelling.','High identity and unchanged romanisation; moderate provisional Chinese index preference.','Further occurrences and source collation. Do not infer that a similar name elsewhere must be this junior lord, or globally replace君.')
pro(161,'Fang Zheng mentor: White Crane versus Sky Crane',[(336,51),(365,45)],'Preferred365p45 白鹤上人→天鹤上人. Preserve the established English designation for Tian He rather than introduce a second mentor.','365 identifies the helper within the soul-incubating flea as White Crane;336 explicitly names the continuing teacher Sky Crane. The role and companion are continuous, with no new mentor introduced. External365 repeats白鹤, not a corrected version.','High continuity support for the name correction; authorial priority unestablished.','Keep the original source quotation. Do not conflate a mistaken epithet with proof that every earlier English name is wrong; this is not a new live-chapter audit.')
pro(162,'Fang Yuan age: twenty versus twenty-five',[(332,5),(333,78),(355,12),(356,4),(364,43),(365,41)],'Register20 at332 versus25 in364’s servant report. Hold the age/calendar reconciliation; select no replacement numeral yet.','332 says only twenty;364 gives twenty-five. The surrounding story gives months and short appointments rather than a stated five-year interval. Both ages occur in the checked repost. Their evidential frames differ: narrator statement versus reported information. The earlier figure might also be rounded or stale arena-age information, rather than a precise present birthday.','High confidence in the differing age claims; moderate-to-high chronological tension; low confidence in a precise repaired age before global reconciliation.','The Yan junior lord’s five-year seclusion belongs to him, not FY’s elapsed interval. Do not insert five years, borrow former-life inheritance duration, or replace all ages. Inner/outer clocks, birthdays and unquantified ellipses still require full-novel checking.')
pro(163,'Vanity parable: preserve the red/fame/heat wordplay',[(357,41),(357,50),(357,54)],'Working English candidate: To become red-hot, you must stand the heat. Add a short note if needed: 红 means both red and popular/famous here. This is a translation proposal, not a Chinese correction.','Vanity asks about fame after the liquid has reddened its companion. Its absurd inference couples physical redness and heat to becoming famous. A fame-only paraphrase loses the joke; a redness-only paraphrase loses the motive. HanDian confirms the fame/popularity sense of红.','High confidence in the double meaning; moderate confidence in the best English recreation.','Red-hot can suggest fashionable or sexually attractive in English, so context or a brief note must constrain it. Do not pretend the proposed idiom reproduces every source association or treat it as an already approved line.')
fixes=[tuple(z) for z in load('batch-019-copy-candidates.json')]
moderate={(357,43),(360,9),(364,5),(364,42),(364,75)}
for c,p,a,b in fixes:assert a in src(c,p)['text'],(c,p,a)
v=pro(164,'Nineteen individually held copy candidates',sorted(set((c,p) for c,p,a,b in fixes)),'Review every candidate individually. No blanket application or claim that a faithful English rendering was a translator error.','Located wrong characters, particles, an incomplete expression and contextual reconstructions. All19 original fragments were found in the selected external reposts; repetition demonstrates transmission, not correctness.','High local support for mechanical slips; moderate reconstruction choices marked.','For脚腕,衍伸,收到奇效 and other possible legitimate expressions, no automatic correction was proposed. Recheck plausible counter-readings before publication.')
v['copy_items']=[dict(chapter=c,paragraph=p,original=a,replacement=b,confidence='Moderate: contextual reconstruction; preferred wording not uniquely established' if (c,p) in moderate else 'High local copy support; external repost repeats original',status='HOLD; unapproved/unapplied',external_collation=next(x for x in load('fact-check-019/copy-collation.json') if (x['chapter'],x['paragraph'])==(c,p))) for c,p,a,b in fixes]
for v in ledger:
 if v['id']=='SR-147':v['locations']+=loc([(356,88)]);v['batch019_update']='356p88 again states inside rate3×outside. Local346 conversion repair strengthened; entire calendar still unverified.'
 if v['id']=='SR-150':v['locations']+=loc([(356,82)]);v['batch019_update']='356p82 the elders themselves explicitly describe fourFour-middle members. Stronger support for correcting352’sThree-peak report, while preserving the possibility of informant error.'
 if v['id']=='SR-153':
  v['locations']+=loc([(360,95),(361,55),(361,56),(363,22),(363,34),(363,79)])
  v['recommended_action']='Retain the345 restriction and flag the mechanism for reconciliation. Do not use forging-versus-manifesting alone as a complete solution:363 deploys upgraded phantoms in combat. Check whether guaranteed All-Out activation and occasional spontaneous manifestations differ; do not insert an unreported Four All-Out upgrade.'
  v['confidence']='High evidence that upgraded strength is actually manifested in combat; unresolved which mechanism triggers each intermittent upgraded phantom and whether a textual repair is required.'
  v['batch019_update']='360ThunderBoar and363ThunderBoar/RockCrocodile combat use narrow the earlier possible resolution.361 explicit All-Out volley names five ordinary beasts;363 says upgraded forms appear intermittently. No guarantee-versus-natural-trigger rule certified.'
 if v['id']=='SR-154':v['locations']+=loc([(356,19),(359,7)]);v['batch019_update']='356/359 continue武神通, reinforcing the proposed326 transposition repair.'
 if v['id']=='SR-099':v['locations']+=loc([(365,11),(365,18)]);v['batch019_update']='Remains withdrawn.365 explicitly uses Reunion in the reverse direction: FY’s refined Four-upper essence aids BaiFourinitial.355 personal non-need did not mean destruction or universal uselessness.'
 if 'batch019_update' in v:v['latest_update']=v['batch019_update']
events=load('history/before-batch019-chronology-register.json')['entries'];resources=load('history/before-batch019-resource-register.json')['entries'];ne=[];nr=[]
def ev(t,k,e,c,rr):
 v=dict(id=f'T{len(events)+1:03d}',timeline=t,kind=k,event=e,constraint=c,evidence_status='Source checked; scopes and counter-readings retained',dependency='Full-novel reconciliation outstanding; no dates invented',sources=ss(rr));events.append(v);ne.append(v)
def res(k,e,c,rr):
 v=dict(id=f'R{len(resources)+1:03d}',kind=k,entry=e,calculation=c,status='Reported, observed, consumed and prospective states distinguished',sources=ss(rr));resources.append(v);nr.append(v)
ev('Revised current life','opening recurrence','Five days after final refusal','355 delays3+3+10 days, then3565days:21 days after initial recruitment visit.356 several-month opening interval is not an additional exact number of months.',[(355,50),(355,56),(355,72),(356,1),(356,4)])
ev('Ren Zu legend','intoxication / retrospective','Seven days and nights; earlier Divine Travel','Legend drunken interval not added to present chronology. Divine Travel also explains the previous island episode, not only the current escape from bees.',[(357,18),(357,32),(357,34),(357,35),(357,36)])
ev('Revised current life','checkpoint / unquantified duration','Xin trial32 to exit44','Reaches32, then40-plus, exits at44. This visit longer than Dog visit, exact time unstated. Does not establish44 fully cleared tests or forty-four days.',[(358,7),(358,15),(358,22),(358,23),(358,27)])
ev('Revised current life','overnight breakthrough','Golden Relic advances FY','Overnight Fourinitial→Fourmiddle. Subsequent BoneWings refinement duration not supplied. Two-to-three and five-plus years are generic training requirements, not FY’s elapsed practice.',[(358,52),(358,57),(358,58),(358,72),(358,87)])
ev('Revised current life','itinerary displacement','Reinforcements depart two days early','Relative to planned itinerary, not proof of only two days’ travel or departure before request. Continuous day/night travel unquantified.',[(359,2),(363,37),(363,38)])
ev('Revised current life','battle deaths / rescue','Six dead, one surviving reinforcement','Mu, XianHua, DaoKu, AoKai, unnamedThree member, then BaXiu. RuoNan saved; elders abandon siege to intervene, releasing Bai. No second death/revival for RuoNan.',[(361,88),(362,4),(362,23),(362,43),(362,48),(363,84),(363,88),(364,14)])
ev('Revised current life / backstory','age and reported information','Twenty and twenty-five claims','SR162 tracks divergent age evidence. YanJun’s five-year seclusion is separate; short present intervals do not supply a documented five-year leap.',[(332,5),(364,43)])
ev('Earlier / recent current life','breakthrough distinction','Wei Yang advances from Three peak to Four','364 oldThreepeak and recentFour are explicitly separated. Do not repair either numeral just because both occur in the chapter.',[(364,64),(364,65),(364,66)])
ev('Revised current life','cultivation session / watch rotation','Several shichen; alternating watches','FY helps Bai for several shichen, approximately two hours per shichen. Later first-half/second-half night watches do not give a universal modern12-hour night.',[(365,11),(365,12),(365,22),(365,23)])
ev('Revised current life / forecast','expected retaliation delay','Not a matter of one or two months','Tower intrusions absorb Tie resources. FY’s retaliation timing is expectation, not elapsed calendar evidence. Hundred Battles Gu remains a goal.',[(365,34),(365,36)])
ev('Parallel Central Continent','competition / opening','Several-month contest concludes','Explicit simultaneous cut36539. Several-month contest not added serially to all Southern events. FengJinHuangfirst; FangZheng enters after20–30others, exact placing unstated.',[(365,39),(365,41),(365,42),(365,66),(365,68),(365,72)])
ev('Revised current life','endpoint / unresolved event','True Fang Zheng falls inside inheritance','Aperture suppressed and falling at365end; no death or victory yet. Spirit girl’s winning condition is a forecast/instruction, not completed inheritance transfer.',[(365,75),(365,79),(365,81),(365,82)])
res('Trial inputs / retained materials','First Hairy Man defeated without refining','50stones and two named Gu plus materials supplied. Flattery induces failure; opponent killed by land. Unused inputs kept for later trials.',[(357,78),(357,87),(357,90),(357,91),(358,11),(358,12)])
res('Trial permissions / rewards','Post40 exception and once-per-opening limit','Only one owned refinement Gu permitted after40; FY has none. Rewards include Gu, recipes, stones and GoldenRelic, not necessarily only refinement Gu. One entry per opening as stated.',[(358,16),(358,17),(358,20),(358,21),(358,27),(358,52)])
res('Consumed reward / cultivation / essence','Golden Relic used;90% sea','FourGoldenRelic acquired then consumed overnight. FYFourmiddle, NineEye can refine Fourupper essence; no cultivation jump to upper and no new aptitude increase.',[(358,49),(358,52),(358,54),(358,58),(358,59)])
res('Refinement / replacement / anatomy','Fresh Footless Bird to Bone Wings','Earlierbird destroyed228; newbird trialreward358. Threeinput→FourBoneWings,>180000stones spent. Foldedtwo-pairs vs deployedone-pair querySR156. Ironbone effects colour and strengthen wings.',[(228,44),(358,66),(358,68),(358,72),(358,74),(358,75),(358,77),(358,82),(361,12)])
res('Team census / leadership','Seven reinforcements','TwoFour+fiveThree. RuoNan commands; BaXiu strongest. Four namedThree juniors plus one unnamed, no eighthmember invented.',[(359,1),(359,9),(359,19),(359,20),(359,21),(359,22),(359,71)])
res('Strength mechanics / Gu ownership','Four Tyrant Strength, Five Earth Overlord','BaXiuFourupper can useFiveGu. Earth support increases strength during battle; insufficient long range differs from having no projected attack at all.',[(360,77),(360,89),(360,90),(361,59),(361,62),(362,59)])
res('Summons / attrition','Eighteen to thousands of grass soldiers','RuoNan continually creates soldiers:18, near1000, then thousands. FourGrassSword units combine lower soldiers. Not fixed instantaneous production; no transferredGu inventory.',[(360,55),(360,56),(360,100),(361,6),(362,26)])
res('Gu depletion / attack preparation','Ranged tools targeted','Mosquito stock gone, StarArrow destroyed, FlowerRain2remain. BladeQi/Snowball stillavailable. Not every speaker/owneridentified. Combat consumptions distinct from FYloot.',[(361,33),(361,35),(361,36),(361,39),(361,40)])
res('Combat effects / unresolved mechanism','Upgraded phantoms actually deployed','ThunderBoar360 andThunderBoar/RockCrocodile363 in combat. GuaranteedAllOutversusoccasionalothertrigger unresolved. NoFourAllOutacquisition supplied.',[(360,95),(361,55),(361,56),(363,22),(363,34),(363,79)])
res('Deaths / protection / loot','Iron Cabinet saves Ruo Nan','Sixofsevenkilled. Cabinet preservesRuoNan; BaXiudies. NoexplicitnamedGu loot grantedtoFY. Eldersremainaliveandfresh; FYessencelow.',[(363,82),(363,83),(363,84),(363,88),(364,20)])
res('Status / physical possession','Purple Thorn guest does not restore broken token','YiHuo’s guest-status judgement36472 doesnotproveFY’sphysicaltokenwasreplaced. Keepstatus, knowledge anditempossession separate.',[(332,81),(364,72)])
res('Assisted cultivation / direction','Reunion now helps Bai','FYFourmiddle refinesFourupperfinegold andtransfersit toBaiFourinitial. NoBai advancementnarrated. Reunionstillowned/functioning; SR099withdrawalretained.',[(365,8),(365,9),(365,11),(365,18)])
res('Future acquisition / new land rules','Hundred Battles not owned; Hu aperture suppressed','HundredBattlesGudesired, not acquired. NewHuImmortalentrysuppressesFangZheng’saperture; noinheritancewonatendpoint.',[(365,36),(365,75),(365,81)])
np=sum(len(c['paragraphs']) for c in batch);nc=sum(sum(map(len,c['paragraphs'])) for c in batch);tp=sum(len(c['paragraphs']) for c in cs);tc=sum(sum(map(len,c['paragraphs'])) for c in cs)
save('proposal-ledger.json',ledger);save('chronology-register.json',dict(scope='Sequential through365; present, remembered, legendary, reported and parallel clocks distinguished',entries=events));save('resource-register.json',dict(scope='Sequential through365; current ownership, consumed rewards, power effects and reports distinguished',entries=resources))
progress=load('history/before-batch019-reading-progress.json');progress.update(sequential_chapters_completed=list(range(1,366)),paragraphs_read=tp,paragraph_characters_read=tc,next_chapter=366,remaining_chapters=1969,batch_report='Batch-019-Chapters-356-365.md',scope='Full sequential Chinese reading through365; selected external collation, not fresh bilingual/live chapter audit',whole_novel_chronology_verified=False)
progress['batches'].append(dict(id='019',chapters=[356,365],paragraphs=np,characters=nc,reading_segments='Five complete untruncated two-chapter outputs; ten-chapter installment'))
progress['chapters'] += [dict(chapter=c['corpus_chapter'],file=c['file'],title=c['title'],paragraphs=len(c['paragraphs']),first_paragraph=1,last_paragraph=len(c['paragraphs'])) for c in batch];save('reading-progress.json',progress)
save('batch-019-reading-log.json',dict(status='Complete',endpoint=365,next_unread=366,segments=[dict(chapters=[a,a+1],status='Full paragraph sequences read; untruncated',paragraphs=sum(len(by[n]['paragraphs']) for n in [a,a+1])) for a in range(356,366,2)],note='Ten chapters, not twenty. Actual reading, not extraction-only coverage. Source unchanged.'))
stand=load('history/before-batch019-working-standards-register.json');stand['coverage_through']=365
for v in stand['entries']:v['batch019_update']='Through365, provisional only. Separate cultivation from fighting power, actual commander from informant reports, reported ages from elapsed time, magical lore from current chronology and spontaneous manifestations from guaranteed activation. No whole-novel certification.'
save('working-standards-register.json',stand)
ws=['# Working standards through Chapter365','Twelve working standards, not approval or whole-novel certification.']
for v in stand['entries']:ws += [f"## {v['id']}: {v['topic']}",v['rule'],v['status'],v['batch019_update']]
(r/'WORKING-STANDARDS.md').write_text('\n\n'.join(ws))
text=['# Numbered Chinese source: Chapters356–365','All917 original paragraphs and numbering retained. No reader-facing omissions in this installment. Original EPUB unchanged.']
for c in batch:text += [f"## Corpus chapter {c['corpus_chapter']}: {c['title']}",f"Volume: {c['volume']} | EPUB: {c['file']}"]+[f"{i}. {t}" for i,t in enumerate(c['paragraphs'],1)]
(r/'Batch-019-Numbered-Chinese-Source.md').write_text('\n\n'.join(text))
for name,vs in [('Chronology',ne),('Resources',nr)]:
 out=[f'# Batch019 {name} jotter','All provisional; no substantive source edits.']
 for v in vs:
  out += [f"## {v['id']}: {v.get('event',v.get('entry'))}",v.get('constraint',v.get('calculation'))]
  for z in v['sources']:out += [f"Ch{z['chapter']} p{z['paragraph']}",'> '+reader(z['chapter'],z['paragraph'],z['text'])]
 (r/'jotters'/f'Batch-019-{name}.md').write_text('\n\n'.join(out))
out=['# Batch019 continuity jotter','Detection and repair confidence are separate.']
for v in new:
 out += [f"## {v['id']}: {v['category']}"]+[f"**{k}:** {v[k]}" for k in ['recommended_action','rationale','confidence','dependencies']]
 if v['id']!='SR-164':
  for z in v['locations']:out += [f"Ch{z['chapter']} p{z['paragraph']}",'> '+src(z['chapter'],z['paragraph'])['text']]
 for z in v.get('copy_items',[]):out += [f"Ch{z['chapter']} p{z['paragraph']}: {z['original']} → {z['replacement']}. {z['confidence']}. HOLD."]
(r/'jotters/Batch-019-Continuity.md').write_text('\n\n'.join(out))
preserve='''# Batch019 preservation cautions

-356 Four-middle fighting strength is not the breakthrough; actual Four-middle cultivation arrives358.
- Requesting a Four-peak reinforcement does not make Ba Xiu Four peak. His Four-upper cultivation and exceptional battle power are explicitly separate.
- Ruo Nan’s actual command and Li Xian’s leader report may reflect imperfect information. Do not erase viewpoint automatically.
- Golden Relic is a reward; the post40 rule restricts use of owned refinement Gu, not the categories of all prizes.
- The new Footless Bird is a fresh reward. The old bird’s destruction remains unchanged.
- A four-winged bird does not prove the transformed human should have four wings.
- First20-plus trial wins conserve materials; checkpoint30/40 descriptions are not automatically inconsistent exact counts.
- Seven reinforcements: two Four, five Three. Four named juniors plus one unnamed. Six die, Ruo Nan survives; no extra victim added from loose plural phrasing.
- Ground soldiers obstruct their own team when controlled poorly; this does not prove all teamwork fails.
- Ba Xiu’s insufficient long range does not mean zero ranged techniques or inability to carry a defensive Gu.
- Named Gu used by victims do not become FY’s loot without narrated recovery.
- Wei Yang Three peak then recently Four is an explicit advancement, not a stage mistake.
- Purple Thorn guest status does not restore FY’s destroyed physical token.
- Yan Jun’s five-year seclusion does not add five years to FY’s chronology.
- Correct inference of secret knowledge does not make Li Xian’s entire theory of FY’s flying expertise correct.
- Three-times internal flow is again supported; no global age repair follows automatically.
-355 personal non-need for Reunion is compatible with365 assistance to Bai. SR099 stays withdrawn.
-Several shichen is not the same as several modern hours; no exact session length invented.
- Hu inheritance at365 is only beginning. Fang Zheng is falling, not dead or victorious.
- Hail remains faithful to冰雹; the Batch016 variant qualification remains controlling.
- The separate synopsis correction clarifies the same demon lord with “the ... himself”; it is not an implemented website edit or a chapter-reading advance.
'''
(r/'jotters/Batch-019-Preserve.md').write_text(preserve)
report=[f'# The Omniarch: Sequential Review, Chapters356–365',f'Batch019 | Ten chapters | {np:,} paragraphs | {nc:,} paragraph characters',f'Completed1–365 of2,334. Next unread366. Cumulative{tp:,} paragraphs / {tc:,} characters. All edits held; original EPUB unchanged.',
'## Scope and main findings','Five complete untruncated two-chapter outputs. This is a ten-chapter installment, not a claimed twenty-chapter completion. Eleven selected external captures and a comparison of all19 copy fragments supplement actual Chinese reading. No fresh live-chapter translation audit. No reader-facing source omissions in this installment.',
'1. Bone Wings: two pairs in the resting description versus one deployed pair.\n2. Tie Ba Xiu: narrator peak-stage label conflicts with explicit upper cultivation.\n3. Actual reinforcement commander differs from Li Xian’s report.\n4. Legend switches between oil-cauldron and water wording, requiring a qualified query.\n5. Yan Jun’s Chinese name alternates军/君.\n6. Fang Zheng’s continuing mentor is called白鹤 instead of established天鹤.\n7. FY’s age20 versus reported25 remains a global-clock query, not an approved numerical repair.\n8. Vanity’s red/fame/heat joke merits an explicit translation proposal.\n9. Nineteen individual copy candidates remain held.',
'## Exact evidence and proposed actions']
for v in new[:-1]:
 report += [f"### {v['id']}: {v['category']}",v['recommended_action'],'**Rationale:** '+v['rationale'],'**Confidence:** '+v['confidence'],'**Dependencies / status:** '+v['dependencies']+' HOLD; unapproved and unapplied.']
 for z in v['locations']:report += [f"Ch{z['chapter']} p{z['paragraph']}",'> '+src(z['chapter'],z['paragraph'])['text']]
report += ['## Reopened and strengthened earlier findings']
for v in ledger:
 if 'batch019_update' in v:report += [f"### {v['id']}: {v['category']}",v['batch019_update']]
report += ['SR134–138 retain the controlling Batch016 qualifications unchanged. In particular Hail is a faithful lexical rendering; the separate冰爆 variant does not settle authorial priority. No stale pre-correction generator was rerun.',
'## Research and provenance','Eleven chapter captures from a single external repost tradition. Repetition establishes transmitted wording, not correctness or authorial priority. Every one of the19 copy fragments appears in its checked repost; none of those checks supplies the proposed replacement as a recovered canonical reading. Raw HTML and SHA256 manifests are in fact-check-019/.']
for v in load('fact-check-019/external-witnesses.json'):report += [f"Ch{v['chapter']}: {v['url']}"]
report += ['HanDian红 records the fame/popularity sense alongside colour; this supports the parable’s double meaning, not one compulsory English idiom. [1](https://zdic.net/hans/%E7%BA%A2)',
'HanDian油锅 distinguishes an oil-filled vessel and a legendary punishment cauldron. This limits confidence in a purely physical correction. https://zdic.net/hans/%E6%B2%B9%E9%94%85',
'## Chronology additions']
for v in ne:report += [f"### {v['id']}: {v['event']}",v['constraint'],refs(v['sources'])]
report += ['## Resource additions']
for v in nr:report += [f"### {v['id']}: {v['entry']}",v['calculation'],refs(v['sources'])]
report += [f'## SR164: {len(fixes)} individually held copy candidates','Original fragments checked against the EPUB extraction and reposts. Moderate items are reconstructions, not uniquely recovered originals.','| Chapter / paragraph | Original | Candidate | Confidence |','|---|---|---|---|']
for z in new[-1]['copy_items']:report += [f"| {z['chapter']} / {z['paragraph']} | {z['original']} | {z['replacement']} | {'Moderate; query' if 'Moderate' in z['confidence'] else 'High local; held'} |"]
report += ['## Chapter-by-chapter reading record',(r/'jotters/batch-019-working.md').read_text(),
'## Preserve rather than overcorrect',preserve.replace('# Batch019 preservation cautions',''),
'## Endpoint365','FY is Revolution Four middle, capable of Four-upper essence through Nine Eye. Bai remains Four initial and is now free. New Bone Wings obtained; Golden Relic consumed. Tie Ba Xiu and five juniors are dead, Ruo Nan and the four elders survive. No named Gu loot or exact remaining cash total is established. True Fang Zheng has entered Hu Immortal inheritance and is falling with a suppressed aperture. No366 reading or inheritance outcome claimed.',
'## Separate synopsis clarification','The translator correctly identified that “And a peerless demonic overlord” could introduce a second person after “the demon lord.” The standalone-And recommendation is superseded. Held candidate: “And the peerless demon lord himself, acting as he pleases and roaming the world unfettered!” Definite reference and consistent designation reconnect the same character; “himself” is a clarifying addition. No website edit.',
'## Saved state and backup boundary',f'{len(ledger)} proposal records: {len(ledger)-2} held, two withdrawn. {len(events)} chronology entries, {len(resources)} resource entries, twelve provisional standards. Five jotters, numbered actual source, reading log, report, workbook and QA. Remote verified through355 before this installment;365 backup must be separately verified before claiming upload.']
report_text=re.sub(r'(?m)(^\|[^\n]*\|)\n\n(?=\|)',r'\1\n','\n\n'.join(report));(r/'Batch-019-Chapters-356-365.md').write_text(report_text)
old=(r/'update_batch010.py').read_text();wb=old[old.index('# Workbook: cumulative'):old.index("(r/'CURRENT-STATUS.md').write_text")]
wb=wb.replace('1–220 of2334','1–365 of2334').replace("('Next unread',221)","('Next unread',366)").replace('103total;102activeheld;1withdrawn','164total;162held;2withdrawn').replace('range(10,0,-1)','range(19,0,-1)').replace("v['batch010_update']","v['batch019_update']").replace('Batch-010-Chapters-201-220','Batch-019-Chapters-356-365').replace('CHAPTERS201–220','CHAPTERS356–365').replace('Chapters201–220','Chapters356–365').replace('Twenty complete chapters; personal clocks and inventory scope distinguished','Ten complete chapters; source conflicts researched and repairs explicitly held').replace('Ch151,201p22,203p84 restricted excerpts','Ch151,201,203,250,258,296,303,337,338,344 restricted excerpts')
wb=wb.replace("v['publication_status'],'No','No',latest]","v['publication_status'],'No','No',v.get('latest_update',latest)]")
exec(compile(wb,'workbook-and-docx','exec'))
(r/'CURRENT-STATUS.md').write_text(f'''# Sequential review checkpoint:365

Completed1–365 of2334. Next unread366;1969 remain. Batch019 is ten chapters, five complete untruncated reading outputs;{np} paragraphs/{nc} characters. Cumulative{tp}/{tc}.

{len(ledger)} proposals,{len(ledger)-2} held,two withdrawn. SR156–164 including19copycandidates. {len(events)}chronology/{len(resources)}resources; twelve provisional working standards. Original EPUB unchanged, no source/site edits.

Eleven external captures plus all19 copy-fragment comparisons. Main issues: wing pair count, BaXiu cultivation label, reported/actual leadership, oil/water cauldron, YanJun variant, mentor name,20/25age and red/fame/heat pun. SR153 scope reopened; SR147/SR150 strengthened; SR099 withdrawn; Batch016 corrections preserved.

Endpoint:FYFourmiddle/NineEyeupperessence; BaiFourinitial andfree. Six reinforcement deaths, RuoNan andfour elders alive. TrueFangZheng falling insideHuImmortal; outcome unread. No366coverage.

Remote verified355 data commit238159596ae7dd51592aed5730cfdee16d34e057, cleanup-record commit863ba0edf0623e81f5fc4efd55bef01884d5fd5f. Current365 upload not yet claimed. Workspace remains lean; archived files restorable by backups/restore_archived_file.py. Independent export QA pending after generator.
''')
sha=hashlib.sha256(Path('/home/user/benchmark/sources/Gu-Zhen-Ren.epub').read_bytes()).hexdigest();assert sha==progress['source_sha256'];assert (np,nc,tp,tc)==(917,30865,33025,1136277);assert len(ledger)==164
assert all(not v.get('approved') and not v.get('applied') for v in ledger)
baseline=load('history/before-batch019-proposal-ledger.json')
for id in ['SR-134','SR-135','SR-136','SR-137','SR-138']:assert next(v for v in ledger if v['id']==id)==next(v for v in baseline if v['id']==id)
for v in ne+nr:
 for z in v['sources']:assert z['text']==src(z['chapter'],z['paragraph'])['text']
qa=dict(batch='019',chapters=10,paragraphs=np,characters=nc,cumulative_paragraphs=tp,cumulative_characters=tc,proposal_count=len(ledger),held=len(ledger)-2,copy_candidates=len(fixes),chronology=len(events),resources=len(resources),reading_segments=5,next_unread=366,source_sha256=sha,source_unchanged=True,substantive_changes_applied=False,batch016_factcheck_preserved=True,external_captures=11,remote_uploaded=False)
save('batch-019-qa.json',qa);print(json.dumps(qa,indent=2))
