from pathlib import Path
import json,shutil,hashlib
from openpyxl import Workbook,load_workbook
from openpyxl.styles import Font,PatternFill,Alignment
r=Path('/home/user/editorial/sequential-review')
def load(n):return json.loads((r/n).read_text())
def save(n,v):(r/n).write_text(json.dumps(v,ensure_ascii=False,indent=2))
for n in ['reading-progress.json','proposal-ledger.json','chronology-register.json','resource-register.json','working-standards-register.json']:
 d=r/'history'/('before-batch014-'+n)
 if not d.exists():shutil.copy2(r/n,d)
cs=sum([load(f'batch-{i:03d}-source.json') for i in range(1,15)],[]);by={c['corpus_chapter']:c for c in cs};batch=cs[270:285]
def src(c,p):return dict(chapter=c,paragraph=p,file=by[c]['file'],text=by[c]['paragraphs'][p-1])
def ss(rr):return [src(*z) for z in rr]
def loc(rr):return [{k:v for k,v in z.items() if k!='text'} for z in ss(rr)]
def refs(z):return '; '.join(f"Ch{x['chapter']} p{x['paragraph']}" for x in z)
def reader(c,p,t):
 if (c==258 and (70<=p<=74 or p==79)) or (c==250 and (24<=p<=31 or p in [33,35,36])) or (c==151 and (31<=p<=67 or p in [98,99])) or (c,p) in [(201,22),(203,84)]:return '[Restricted passage omitted from reader-facing copy. Original numbering retained; original EPUB unchanged.]'
 return t
ledger=load('history/before-batch014-proposal-ledger.json');new=[]
def pro(i,cat,rr,action,why,conf,dep):
 v=dict(id=f'SR-{i:03d}',category=cat,locations=loc(rr),recommended_action=action,rationale=why,confidence=conf,status='Active provisional proposal; no approval',dependencies=dep,approved=False,applied=False,publication_status='HOLD: full 2334-chapter reading and global reconciliation outstanding');ledger.append(v);new.append(v);return v
pro(123,'Inventory-list scope: Flying Bone Shield',[(266,48),(273,55),(273,56)],'Retain a missing-disposition query for Flying Bone Shield. If later evidence confirms continued ownership, include it in the Ch273 inventory or narrow the list to selected holdings. Do not invent a sale, destruction or loss.','Flying Bone Shield is used in266;273 presents the preceding inventory as all current Gu and explicitly accounts for several other departures, but not this one. Breaking its shield construct did not previously establish destruction of the Gu.','High omission observation; moderate continuity diagnosis; conditional repair.','Later inventory and disposal accounts; independent source witness. Hairy Foot and Crocodile Strength also need disposition tracking, but should not be silently appended as proven holdings.')
pro(124,'Five stone-cutting masters called four',[(277,12),(277,14),(277,16),(277,22),(277,27)],'Preferred277p16 我们四个老家伙→我们五个老家伙.','Five masters are individually named and repeatedly counted before and after the isolated four.','Very high local count support.','Independent witness before implementation; no change to the five-master cast.')
pro(125,'Third strike mistaken for third punch',[(280,4),(280,18),(280,27),(280,84)],'Preferred280p84 你第三拳→你最后一拳. English: your final punch.','The attack sequence is punch, kick, punch. The last is the third strike but only the second punch.','High local staging support.','Preserve all three attacks and the death; do not add an off-page punch.')
pro(126,'Li Ran infiltration: half-year versus eight years',[(283,18),(283,20),(283,21),(283,48),(284,11),(284,19),(284,38)],'Preferred284p19 潜伏了整整半年→潜伏了整整八年. English: had spent eight full years undercover.','Eleven-year mission divides into three years outside and eight in Shang city. Eight is repeated in this very chapter. The separate half-year stakeout concerns preparing the stone swap, not the entire infiltration.','Very high local chronology support.','Independent witness; preserve six-month contact rhythm and stone-shop stakeout. Do not flatten approximate near-ten-year descriptions into exact dates.')
pro(127,'Li Ran first sight versus prior same-shop encounter',[(280,127),(280,142),(280,143),(284,97)],'Hold284p97 第一次见到方源 as an encounter-scope query. If close inspection rather than first physical sight is intended, candidate: 虽然这只是他第一次如此近距离地打量方源. English: Although this was his first close look at Fang Yuan.','Li Ran was present at the earlier stone opening and made a sour comment about the lucky winner. A later absolute first-ever sight is questionable, but earlier attention or recognition may have been limited.','Moderate tension; low-to-moderate replacement confidence.','Later recognition claims and independent versions. Do not claim he knew Fang Yuan personally or had memorised his face at the shop.')
fixes=[(271,25,'以为杵','以为忤'),(271,26,'族人大人','族长大人'),(271,36,'回复原貌','恢复原貌'),(271,48,'芊芊玉指','纤纤玉指'),(271,87,'当上商燕飞','当初商燕飞'),(271,88,'亦数正常','亦属正常'),(271,115,'知无不尽','知无不言'),(271,128,'同时，也这不很好吗','这不也很好吗'),(272,19,'觉的','觉得'),(272,25,'便回','变回'),(272,28,'都像方白','都向方白'),(272,41,'鹤蚌','鹬蚌'),(272,53,'商量出','商家城'),(273,16,'坠落道','坠落到'),(273,16,'多多浪花','朵朵浪花'),(273,44,'解读','解毒'),(273,60,'还有购买','还要购买'),(273,69,'族长之外','族长之位'),(273,82,'泥腿子出生','泥腿子出身'),(274,1,'挪揄','揶揄'),(274,60,'只好像先','只好先'),(275,23,'合练','合炼'),(275,24,'较少真元','减少真元'),(275,35,'几十多万','几十万'),(275,38,'萧燕','萧炎'),(275,62,'终究会还会','终究还会'),(275,70,'忘一些东西','忘了一些东西'),(276,27,'踮脚石','垫脚石'),(276,29,'杂等元石','杂等顽石'),(276,30,'这些元石','这些顽石'),(276,40,'踮脚石','垫脚石'),(276,59,'和空旷','很空旷'),(276,62,'星箭骨','星箭蛊'),(277,3,'用恭敬无比声音','用恭敬无比的声音'),(277,10,'拥有着','拥有者'),(277,42,'磨搓双手','摩搓双手'),(278,70,'照的密室','照得密室'),(278,77,'此后百年后','此后百年'),(279,8,'寰转','回转'),(279,16,'修行越高','修为越高'),(279,58,'第四内场','第四内城'),(279,60,'来的快','来得快'),(280,5,'痛疼','疼痛'),(280,7,'剧烈的摩擦掉','剧烈地摩擦掉'),(280,46,'兔起鹊落','兔起鹘落'),(280,51,'无所谓的耸耸肩','无所谓地耸耸肩'),(280,104,'柜台一脚','柜台一角'),(280,118,'赋有传奇','富有传奇'),(280,141,'搞的这些','搞得这些'),(280,143,'语气酸涩的嘟囔','语气酸涩地嘟囔'),(281,26,'深深的印','深深地印'),(281,83,'当终究','但终究'),(281,88,'配合得发出','配合地发出'),(281,90,'也能只算','也只能算'),(281,98,'第四内场','第四内城'),(282,16,'大搓一顿','大撮一顿'),(282,43,'买吓','买下'),(282,60,'窈窕淑君子','窈窕淑女，君子'),(282,78,'颓废的很有规律','颓废得很有规律'),(283,70,'在加上','再加上'),(283,80,'然而和身体上所受的创伤，完全和他此刻心中的震惊和恐惧相提并论','然而身体上所受的创伤，完全无法和他此刻心中的震惊和恐惧相提并论'),(283,82,'与此同时在，在','与此同时，在'),(284,6,'装做示意','装作失意'),(284,91,'对方源的印象','对方的印象'),(284,91,'或者老年','或者老年人'),(285,33,'一边对望向','一边望向'),(285,44,'这么年纪','这么大年纪'),(285,51,'上升道','上升到'),(285,51,'不会像选中','不会选中'),(285,64,'透漏','透露')]
for c,p,a,b in fixes:assert a in src(c,p)['text'],(c,p,a)
v=pro(128,'Located copy candidates',sorted(set((c,p) for c,p,a,b in fixes)),'Review every substitution separately; do not apply as a global replacement.','Wrong characters, missing words, names and malformed clauses. Reconstruction and diction candidates remain less certain than straightforward character substitutions.','Mostly high; individually qualified.','Independent witnesses, intended idiom and sentence sense; all items unapproved and unapplied.')
moderate={(271,115),(271,128),(272,53),(277,42),(279,16),(280,104),(282,16),(283,80),(284,6)}
v['copy_items']=[dict(chapter=c,paragraph=p,original=a,replacement=b,confidence='Moderate: contextual reconstruction or diction; collate before choosing' if (c,p) in moderate else 'High local copy support',status='HOLD; unapproved/unapplied') for c,p,a,b in fixes]
for v in ledger:
 if v['id']=='SR-099':
  v['superseded_action']=v['recommended_action'];v['recommended_action']='WITHDRAW the proposed after-to-before Revolution Three substitution. Preserve214p51 在三转以后; the forecast has not been disproved.';v['rationale']='273 establishes the Revolution Three breakthrough;282p30 explicitly continues Reunion-assisted cultivation. Continued benefit after reaching Revolution Three undermines the earlier speculative repair.';v['confidence']='High confidence that the proposed correction is not established; not certification of every future rate claim.';v['status']='Withdrawn: later evidence weakens the speculative diagnosis';v['publication_status']='WITHDRAWN; do not apply';v['batch014_update']='273pp21–26 and282p30: benefits continue after reaching Revolution Three. A completed whole-novel rate analysis remains outstanding.'
 if v['id']=='SR-063':v['batch014_update']='275p31 explicitly confirms Frost Demon destruction in the Qing Shu fight, reinforcing retrospective treatment of143; it does not restore the Gu.'
 if v['id']=='SR-104':v['batch014_update']='271p17 Fang Yuan again claims he killed two Bai junior lords. More death-branch evidence; mixed witness and231 disappearance unresolved.'
 if v['id']=='SR-118':v['batch014_update']='271p17 calls Bai twins two少主;272p7 distinguishes ordinary succession from Shang multiple junior lords.273p82 chief’s belief reflects the alias cover story, not authenticated FY biography.'
events=load('history/before-batch014-chronology-register.json')['entries'];resources=load('history/before-batch014-resource-register.json')['entries'];ne=[];nr=[]
def ev(t,k,name,detail,rr,dep='Global reconciliation and later anchors outstanding'):
 v=dict(id=f'T-{len(events)+1:03d}',timeline=t,kind=k,event=name,constraint=detail,evidence_status='Read source; approximate, inferred and hypothetical clocks distinguished',dependency=dep,sources=ss(rr));events.append(v);ne.append(v)
def res(k,name,detail,rr):
 v=dict(id=f'R-{len(resources)+1:03d}',kind=k,entry=name,calculation=detail,status='Provisional evidence register, not approved emendation',sources=ss(rr));resources.append(v);nr.append(v)
ev('Revised current life','scene durations','Banquet, healing and next-day oath','Three shichen wait≈6h; bath half shichen≈1h; healing half cup of tea. Banquet continues half shichen, overnight negotiation, next-morning oath purchase. Do not add parallel scenes as separate days.',[(271,44),(271,91),(271,107),(272,16),(272,73),(272,75)])
ev('Revised current life','relative age of journey','Nearly one year since Qing Mao','273p23 nearly one year, not a precise anniversary. Three shichen breakthrough≈6h; solitary one day/night is counterfactual.',[(273,21),(273,23),(273,24),(273,26)])
ev('Earlier city history','office chronology','Chief met Wei before becoming chief','273p69 explicitly places first meeting while Shang Yan Fei was junior lord; supports earlier age/office distinction.',[(273,69)])
ev('Former-life future / present intentions','forecasts','Stay and oath technology','Two-to-three-year intended stay not elapsed. Oath-breaker discovered200years later in former life, spread decades later, replacement after another decade-plus, countermeasure about century later. Preserve layered anchors.',[(271,13),(278,75),(278,76),(278,77),(278,94)])
ev('Revised current life','scheduled fight and ellipsis','Arena registration to third fight','279 scheduled未时三刻,half刻 until start.280 half-month jump, second win off-page, third pending. Gambling less than month may start before first fight.',[(279,80),(279,81),(280,95),(280,100),(280,116)])
ev('Revised current life','investigation intervals','Tracking Li Ran','Seven/eight investigation days after third win; several tracking days, then another20plus days; three days to restaurant;283 night memory then next-day theft during fight. Keep narrative seams provisional.',[(281,113),(282,11),(282,26),(282,51),(283,57),(283,63)])
ev('Past mission / revised current life','nested durations','Wu Ran mission timeline','11years ago commissioned;3outside+8city=11. Activation announcement1year ago; half-year contacts and half-year stone-shop stakeout distinct.284p19halfyear conflicts8year infiltration, SR126. Near10years city/10years effort remain approximate.',[(282,9),(283,18),(283,20),(283,21),(283,26),(283,27),(283,48),(284,19),(285,64)])
ev('Revised current life / observation','age and recognition','Li Ran family and prior encounter','Target50plus, other registrant60plus; child5/6 given in FYspeech.280same-shop remark versus284first sight queriedSR127; not proven prior acquaintance.',[(282,8),(282,9),(280,143),(284,97),(285,52)])
ev('Revised current life','relative jump','Public legendary Gu discovery','Three days after negotiation scene, public All-Out Effort discovery. Earlier plan for day-after-battle opening superseded by theft/deal. Published collision account staged, not independent history.',[(283,57),(285,69),(285,71),(285,74)])
ev('Scene simile / deliberate manipulation','not a clock error','Summer heat and skipped count','281July/August is terrain simile, not current date.284 counting1,2,5 deliberate pressure, not a missing-three/four copy error.',[(281,7),(284,48),(284,52),(284,55),(284,56)])
res('Rewards / manufacture','Healing and badges','Healing and two Purple Thorn badges accepted; million and bounty removal refused. Token Gu consumed making non-Gu badges; power renewable and temporary, no exact expiry. >200 circulating versus historical hundreds not automatic contradiction.',[(271,143),(271,166),(272,4),(277,25)])
res('Oath / negotiated threshold / division','Yang promise and finances','New threshold Revolution Four peak after explicit reneging on Three and bargaining down from Five peak. Current wealth halves, future loot70/30.3000 oath split1500each;6700 storage charged Bai;9700≈10000. If X pre-division, FY X/2−1500,Bai X/2−8200.',[(272,43),(272,45),(272,57),(272,76),(272,77),(272,84),(272,89)])
res('Cultivation / inventory / disposition','Revolution Three and missing shield','FY Three initial; Bai Three peak. Lotus~50stones/day. Flesh Bone returned; Strong Plunder starved; bone projectiles sold. Flying Bone Shield omissionSR123, no invented loss. Disposal intentions not completed sales.',[(273,21),(273,55),(273,56),(273,57),(273,60),(282,30)])
res('Exchange / refinement','Human Triumph Gu','Chief trades Blood Handprint for Revolution Five Human Triumph, refines rapidly. Intended aptitude awakening not yet carried out; four treasure gifts separate from exchange.',[(274,60),(274,63),(274,65)])
res('Purchases / effects','Ice Crystal and Brown Bear','Ice Crystal28000; Brown Bear4100. Bai deliberately chooses male-suited Gu. Her aptitude rose一分; do not invent exact new total. Brown Bear strength still developing at281, purchase≠complete effect.',[(275,56),(275,57),(275,60),(280,79),(281,42),(281,76)])
res('Refinement / consumed materials / oath scope','Eating One’s Words','Rice Pouch and other ingredients consumed in chain. Three coloured Paper Cranes. Breaker10breaths duration, two existing FY restrictions removed, counterpart restrictions persist.285new oath produced but terms/removal not shown.',[(278,13),(278,27),(278,29),(278,56),(278,62),(278,66),(278,80),(285,69)])
res('Funds / noncash valuation','Gambling and current cash','277cost650,opening free.278cash420000 after unitemised outflows.280gambling aggregate nearly100000, current lot8000,Sword Shadow valued32000 not cash received. Do not subtract aggregate and included expenses twice.',[(277,10),(277,11),(278,83),(280,116),(280,142),(280,148)])
res('Price conventions','Ordinary versus rare Gu','278ordinary price bands explicitly exclude rare Gu; Ice Crystal28000,Sword Shadow32000 and Inspiration29000 need not conform to ordinary Revolution Three1000–10000 range.',[(278,86),(278,87),(278,89),(278,91),(282,34)])
res('Borrowing / arena rules / receipts','Registration and wins','500registration; Vine Gu borrowed Shang property.30net wins to fourth,80there to third; max1fight/day,min1/10days,forced1/month,net5defeats expulsion. Three wins through281. No certified tier cumulative-total reading.',[(279,58),(279,72),(279,75),(279,77),(279,78),(281,102)])
res('Loot / combat effects','Tang brothers','Tang Qing killed:four ordinary Gu≈2000,20–30stones; Vine returned Shang. Tang Xiong surrenders:Bear Grand Gu transferred;2bears permanent+1temporary. Canopy construct damaged, Gu not destroyed.',[(280,52),(280,57),(280,59),(281,42),(281,44),(281,69),(281,102),(281,103)])
res('Consumption / payment','Inspiration and restaurant','Inspiration29000 bought/consumed. Li Ran bill5.5,pays6; separate half-stone reserved-seat fee not automatically the same half-stone.',[(282,34),(282,43),(282,45),(282,53),(282,54),(282,62)])
res('Theft / communication / public cover','Flower Bud and All-Out Effort','Flower Bud stolen/refined with contents30–40stones and fake star stone. Heart Voice paired Revolution Two100pace intentional communication, no ordinary mind-reading. All-Out Effort publicly opened three days later,100% beast phantom activation; staged3stone compensation story not actual acquisition price.',[(283,85),(283,87),(284,31),(284,42),(284,93),(285,71),(285,73),(285,74)])
np=sum(len(c['paragraphs']) for c in batch);nc=sum(sum(map(len,c['paragraphs'])) for c in batch);tp=sum(len(c['paragraphs']) for c in cs);tc=sum(sum(map(len,c['paragraphs'])) for c in cs)
save('proposal-ledger.json',ledger);save('chronology-register.json',dict(scope='Sequential through285; temporal evidence distinguished from inference',entries=events));save('resource-register.json',dict(scope='Sequential through285; ownership, consumption, noncash value and realised transfers separated',entries=resources))
progress=load('history/before-batch014-reading-progress.json');progress.update(sequential_chapters_completed=list(range(1,286)),paragraphs_read=tp,paragraph_characters_read=tc,next_chapter=286,remaining_chapters=2049,batch_report='Batch-014-Chapters-271-285.md',scope='Full sequential Chinese-source reading through285; no fresh bilingual/live-site audit',whole_novel_chronology_verified=False)
progress['batches'].append(dict(id='014',chapters=[271,285],paragraphs=np,characters=nc,reading_segments='Seven complete untruncated pairs and complete285; adaptive15'))
progress['chapters'] += [dict(chapter=c['corpus_chapter'],file=c['file'],title=c['title'],paragraphs=len(c['paragraphs']),first_paragraph=1,last_paragraph=len(c['paragraphs'])) for c in batch];save('reading-progress.json',progress)
save('batch-014-reading-log.json',dict(status='Complete',endpoint=285,next_unread=286,segments=[dict(chapters=[a,a+1],status='Full text read; untruncated',paragraphs=sum(len(by[n]['paragraphs']) for n in [a,a+1])) for a in range(271,285,2)]+[dict(chapters=[285],status='Full text read; untruncated',paragraphs=len(by[285]['paragraphs']))],note='Actual sequential close reading; no fabricated timestamps.'))
text=['# Numbered Chinese source: Chapters271–285','Source wording and paragraph numbering unchanged.']
for c in batch:text += [f"## Corpus chapter {c['corpus_chapter']}: {c['title']}",f"Volume: {c['volume']} | EPUB: {c['file']}"]+[f'{i}. {t}' for i,t in enumerate(c['paragraphs'],1)]
(r/'Batch-014-Numbered-Chinese-Source.md').write_text('\n\n'.join(text))
for name,vs in [('Chronology',ne),('Resources',nr)]:
 out=[f'# Batch014 {name} jotter','All provisional; no source edits.']
 for v in vs:
  out += [f"## {v['id']}: {v.get('event',v.get('entry'))}",v.get('constraint',v.get('calculation'))]
  for z in v['sources']:out += [f"Ch{z['chapter']} p{z['paragraph']}",'> '+z['text']]
 (r/f'jotters/Batch-014-{name}.md').write_text('\n\n'.join(out))
out=['# Batch014 continuity and proposed corrections','All new proposals held. SR099 withdrawn after reassessment.']
for v in new:
 out += [f"## {v['id']}: {v['category']}"]+[f"**{k}:** {v[k]}" for k in ['recommended_action','rationale','confidence','dependencies','status']]
 if 'copy_items' in v:
  for z in v['copy_items']:out += [f"### Ch{z['chapter']} p{z['paragraph']}: {z['original']} → {z['replacement']}",z['confidence'],'> '+src(z['chapter'],z['paragraph'])['text']]
 else:
  for z in v['locations']:out += [f"Ch{z['chapter']} p{z['paragraph']}",'> '+src(z['chapter'],z['paragraph'])['text']]
(r/'jotters/Batch-014-Continuity.md').write_text('\n\n'.join(out))
(r/'jotters/Batch-014-Preserve.md').write_text('''# Batch014 preservation cautions
- False prophetic-Gu inference, FY heir cover story, FY shared-spy identity and staged gambling rumour must not become narrator facts.
- Original counter-support stone empty is explained by an intended stone swap, not repaired by inventing Gu contents.
- One, two, five is intentional coercion. July/August heat is a simile, not current date.
- Ice Crystal is deliberately male-suited; Bai expects eventual bodily reversal. Aptitude increase not a new exact certified total.
- Gu purchase/refinement, temporary effects, permanent bodily strength and actual possession are different events.
- Oath renegotiation is explicit misconduct by FY, not an author forgetting the Revolution Three threshold.
- Two old FY-side oaths removed; others remain bound. No third removal or full new contract is narrated by285.
- Ordinary price bands exclude rare Gu. Sale valuation is not realised cash. Approximate aggregate gambling spending not counted twice.
- First punch, kick, final punch: correct the ordinal wording, not the combat.
- Near-ten-year phrases may be approximate; exact mission11=outside3+city8. Half-year stakeout/contact clocks remain separate.
- Source EPUB unchanged. No substantive edits approved/applied; no remote backup completed.
''')
stand=load('history/before-batch014-working-standards-register.json');stand['coverage_through']=285
su={'WS-01':'Bai predictive-Gu inference, FY shared-spy identity and public stone story are beliefs/cover narratives, not confirmed facts.','WS-02':'Five masters versus four; third attack versus third punch. Counts checked against actual sequence.','WS-03':'FY Three initial273; Reunion still useful282. Withdraw SR099 after/before repair. Bai Three peak, incomplete bear effect tracked.','WS-04':'Plunder starved, Rice Pouch consumed in refinement. Shield inventory omission held. Borrowed Vine Gu remains Shang property.','WS-05':'Nearly1year sinceQingMao; LiRan11=3+8. Halfyear stakeout distinct from8year infiltration. Similes and plans not dates.','WS-06':'Oath3000+storage6700=9700; existing wealth50/50, future70/30.420k cash checkpoint; gambling valuations not receipts.','WS-07':'Heart Voice100pace range applies to communication, moving sender not located. No invented geography correction.','WS-08':'LiRan50plus, other60plus; child5/6 inFYspeech. Chief confirms meetingWei before becoming chief.','WS-09':'70 individually held copy candidates; source quotation unchanged. Revolution adopted for assistant cultivation wording.','WS-10':'285/2334 read;2049remaining.128records,126held,2withdrawn. All substantive approved/applied false.','WS-11':'276p54 preserves full maxim. Working story English unchanged: Man is the most intelligent of all living things.','WS-12':'271Baitwins少主 supportsSR118;272Shangmultipleoffices distinct from ordinary succession. Alias claims not biographical proof.'}
for v in stand['entries']:v['batch014_update']=su[v['id']]
save('working-standards-register.json',stand)
out=['# Working editorial standards','## Evidence checkpoint: Chapters1–285','Working rules are not whole-novel factual certification or manuscript approval. Cultivation wording: Revolution.']
for v in stand['entries']:out += [f"## {v['id']}: {v['topic']}"]+[f"**{k}:** {v[k]}" for k in ['status','rule','evidence','reopen','batch014_update']]
(r/'WORKING-STANDARDS.md').write_text('\n\n'.join(out))
def quote(c,p):return f"**Ch{c} p{p}:**\n\n> {src(c,p)['text']}"
report=f'''# Sequential close-reading review: Chapters 271–285
## Batch 014 | The Omniarch

**Actual sequential coverage: 1–285 of 2,334. Next unread: 286.**

Fifteen complete chapters, {np:,} paragraphs and {nc:,} paragraph characters in this batch. Cumulative: **{tp:,} paragraphs / {tc:,} characters**. All eight reading segments were complete and untruncated. This is Chinese-source close reading, not a fresh bilingual or live-site audit.

**Cultivation terminology: Revolution.** Earlier assistant-authored reports, registers and exports have been migrated, with original source witnesses and pre-change backups preserved. This user-approved terminology change does not approve substantive emendations.

**Six new proposal records: SR123–128.** SR128 contains {len(fixes)} individual copy candidates. **SR099 withdrawn** after later evidence undermined its speculative repair. Totals: **128 records, 126 held and two withdrawn**. No substantive proposal approved or applied. Whole-novel chronology is not certified.

## 1. Principal findings

| Record | Issue | Proposed treatment | Confidence |
|---|---|---|---|
| SR123 | Flying Bone Shield absent from whole-inventory review | Hold missing disposition; add only if continued ownership confirmed | Moderate |
| SR124 | Five stone-cutting masters called four | 四个 → 五个 | Very high |
| SR125 | Third attack called third punch | 第三拳 → 最后一拳 | High |
| SR126 | Eight-year infiltration called half a year | 半年 → 八年 | Very high |
| SR127 | First sight after prior shop encounter | Query first-ever sight versus first close look | Moderate/conditional |
| SR128 | Located copy faults | {len(fixes)} individually held candidates | Individually qualified |

## 2. Inventory: account for disappearance rather than inventing it

{quote(266,48)}

{quote(273,55)}

{quote(273,56)}

Ch273 explicitly accounts for the return of Flesh Bone Gu, the starvation of Strong Plunder Gu and the sale of the bone-projectile Gu. This is useful new information, not a reason to call every earlier unreported disposition an error. However, Flying Bone Shield was still used in266 and is missing from the purported whole-inventory review. Its shield construct being broken is not evidence that the Gu itself died. **SR123** therefore holds the omission for later verification. Hairy Foot and Crocodile Strength also remain disposition questions, not automatic additions.

Rice Pouch Grass is subsequently consumed in278's oath-breaker refinement. Brown Bear Gu being purchased does not mean a full bear's strength is immediately present:280 says it is being used;281 says the bear strength has not yet matured. The arena Vine Information Gu is explicitly borrowed from Shang, not bought with the500-stone registration fee.

## 3. Five masters, not four

{quote(277,12)}

{quote(277,16)}

Five named specialists, five assembled and five repeatedly counted. Preferred local candidate: **我们四个老家伙 → 我们五个老家伙**. No cast reduction or additional master is needed. Independent witness collation remains a prerequisite to implementation.

## 4. Count the attacks, not just the ordinal

{quote(280,18)}

{quote(280,27)}

{quote(280,84)}

The sequence is a punch to the chest, a kick, then a punch to the face. The face punch is the third attack but second punch. Preferred **你第三拳 → 你最后一拳**, English **“your final punch.”** This preserves the choreography without inventing an extra attack. The bell had already sounded before the first attack; Tang Qing's charge of a sneak attack is his evaluation, not proof of a prohibited pre-start strike.

## 5. Li Ran: three outside, eight inside, eleven overall

{quote(283,18)}

{quote(283,20)}

{quote(283,21)}

{quote(284,19)}

The mission began eleven years earlier, with three years building cover outside Shang and eight years in the city. The isolated **half-year infiltration** clashes with repeated eight-year statements in284 itself. Preferred **半年 → 八年**.

Do not change the separate half-year contact rhythm or six-month stone-shop stakeout. The announcement that he would be activated came a year earlier; that is not the start of his infiltration. “Nearly ten years” of city residence and “ten years” of effort may be approximate formulations, while the wider mission includes time outside the city. They do not warrant an automatic exact-date rewrite.

{quote(280,143)}

{quote(284,97)}

The shop scene places Li Ran near Fang Yuan and gives him a sour remark about the winner.284's absolute first-ever sight is therefore questionable. **SR127** offers “his first close look” only conditionally. Limited attention or recognition could explain the wording; prior personal acquaintance is not established.

## 6. A previous proposal withdrawn: SR099

{quote(214,51)}

{quote(282,30)}

The earlier suggestion to replace “after Revolution Three” with “before” was speculative.273 now establishes Fang Yuan's Revolution Three breakthrough;282 explicitly describes his continuing use of Reunion-assisted cultivation. This does not prove every future growth-rate claim, but it does undermine the proposed correction. **Withdraw the after-to-before substitution and retain the source.** Reading must be allowed to reverse our proposals, not merely accumulate support for them.

Separately,275p31 explicitly recalls Frost Demon Gu's destruction during the Qing Shu fight, reinforcing **SR063's retrospective reading**. The Bai twins' deaths are asserted again271p17, and their title is 少主, strengthening SR118. **SR104's mixed-witness problem remains unresolved**: another death assertion is not edition authentication.

## 7. Money, contracts and effects

- **Rewards:** the million-stone reward and bounty removal are refused. Healing and two Purple Thorn badges are accepted. Badges are not Gu: Token Gu is consumed to manufacture them.
- **Yang agreement:** Fang Yuan explicitly reneges on the earlier Revolution Three promise. He demands Five peak; they settle on **Four peak**. This is deliberate misconduct, not a forgotten threshold.
- **Division:** existing wealth50/50, future loot70/30. Poison Vow costs3000 after a1500 reduction from4500, a one-third discount. Bai's storage Gu6700 plus the oath3000 gives9700, reasonably rounded to10000.
- **Allocation:** for actual pre-division funds X, FY receives X/2−1500, Bai X/2−8200. Using the older945000 balance without accounting for intervening income/expenses would give false precision.
- **Cash checkpoint:**278p83 states420000 remaining. Unpriced purchases, accommodation, food and gambling prevent an independently reconstructed exact running balance.
- **Gambling:**277 costs650.280's current lot costs8000 and yields Sword Shadow valued32000. It has not been sold. Nearly100000 cumulative gambling expenditure includes earlier spending; do not subtract aggregate and included items twice.
- **Rare Gu:** ordinary Revolution Three prices of1000–10000 explicitly exclude rarities. Ice Crystal28000, Sword Shadow32000 and Inspiration29000 are not automatically price contradictions.
- **Oaths:**278 removes both existing restrictions on Fang Yuan, not the restrictions on Bai and Shang Ya Zi.285 produces another Poison Vow Gu but does not reproduce its terms or show another removal.
- **Loot:** Tang Qing leaves four ordinary Gu worth about2000 and20–30stones. Tang Xiong yields Bear Grand Gu after surrender. No unnamed loot Gu is arbitrarily assigned a specific identity.

## 8. Chronology and arena rules

{quote(273,23)}

Nearly one year since Qing Mao is a significant approximate anchor, not a dated anniversary. Fang Yuan's breakthrough takes three 时辰, conventionally about six hours; one day and night alone is counterfactual. The two-to-three-year Shang stay is still an intention, not elapsed time.

The later chain includes a half-month jump before the third fight; seven/eight further investigation days; several tracking days followed by another twenty-plus; three days to the restaurant; a night and next-day theft; then three days to public discovery. Preserve the narrative seams rather than pretending every interval is exact or unquestionably additive.

Arena rules:30 net wins to fourth city;80 within that tier to third; maximum one fight per day; at least one every ten days or lose a win; one forced challenge per month; net five defeats cancels qualification. Do not silently certify how tier resets affect a cumulative total. Fang Yuan has three wins by281, with his second occurring off-page.

July/August heat in281 is a terrain simile. **“One, two, five” is deliberate coercion**, not faulty arithmetic. Heart Voice requires intentional transmission; it does not broadcast every private thought. Its100-pace range does not establish a contradiction unless the transmitter's changing position is known.

## 9. Preserve the reveal and the viewpoints

The empty counter-support stone is not a continuity fault. The legendary Gu was held in a counterfeit replacement stone intended for a swap. Fang Yuan's remembered account was a public cover story.283 reveals the mechanism;285 stages a new public explanation about a collision and three compensating stones. Do not promote either rumour to independent omniscient history.

Similarly, Bai's predictive-Gu theory, the chief's belief in Fang Yuan's alias biography, Wei's conviction that the strength path cannot succeed, and Li Ran's belief in a fellow undercover operative are character perspectives. The separated spoken and Heart Voice conversations in285 are intentional narrative layering.

## 10. Copy candidates and complete evidence

The continuity jotter contains **all {len(fixes)} candidates**, each with its exact source paragraph, proposed replacement and confidence. Straightforward examples:273解读→解毒;275萧燕→萧炎;276星箭骨→星箭蛊;282买吓→买下. Lower-confidence reconstructions such as283p80's malformed comparison and284p6's装做示意 are explicitly marked, not silently normalised. Chinese source files are unchanged.

The numbered Chinese source companion supplies all fifteen chapters, not a summary in place of the text. Dedicated chronology, resources, continuity and preservation jotters accompany the full working jotter. The cumulative workbook has been rebuilt through285.

## 11. Endpoint

By285 the All-Out Effort Gu has been publicly opened. Its stated function is100% beast-strength phantom activation. Fang Yuan has reached **Revolution Three initial stage**; Bai remains **Revolution Three peak stage**. Later payments, contractual details and future victories are not supplied at this endpoint.

Saved: **{len(events)} chronology entries, {len(resources)} resource entries,128 proposal records,12 working standards**, full source companion, five jotters, eight-segment reading log and cumulative workbook. The working maxim remains **“Man is the most intelligent of all living things.”**

**Next unread:286.** All substantive edits remain unapproved and unapplied. Original EPUB unchanged; no manuscript/site edits, uploads or deletions. Remote research backup remains unresolved.
'''
(r/'Batch-014-Chapters-271-285.md').write_text(report)
old=(r/'update_batch010.py').read_text();wb=old[old.index('# Workbook: cumulative'):old.index("(r/'CURRENT-STATUS.md').write_text")]
wb=wb.replace('1–220 of2334','1–285 of2334').replace("('Next unread',221)","('Next unread',286)").replace('103total;102activeheld;1withdrawn','128total;126activeheld;2withdrawn').replace('range(10,0,-1)','range(14,0,-1)').replace("v['batch010_update']","v['batch014_update']").replace('Batch-010-Chapters-201-220','Batch-014-Chapters-271-285').replace('CHAPTERS201–220','CHAPTERS271–285').replace('Chapters201–220','Chapters271–285').replace('Twenty complete chapters; personal clocks and inventory scope distinguished','Fifteen complete chapters; chronology, inventory and revised earlier proposals').replace('Ch151,201p22,203p84 restricted excerpts','Ch151,201p22,203p84,250pp24–31/33/35–36,258pp70–74/79 restricted excerpts')
exec(compile(wb,'workbook-and-docx','exec'))
(r/'CURRENT-STATUS.md').write_text(f'''# Sequential review checkpoint

Completed1–285/2334; next286;2049remaining. Batch014:{np}paragraphs/{nc}characters. Cumulative{tp}/{tc}.128proposals:126held+SR047/SR099withdrawn. SixnewSR123–128;SR128contains{len(fixes)}copycandidates. {len(events)}chronology/{len(resources)}resources.12standards. All substantiveapproved/appliedfalse. Cultivation wording Revolution user-approved separately; source witnesses preserved.

Deliverable Batch-014-Chapters-271-285.md/.docx. Fullsourcecompanion, fivejotters, readinglog, workbook and registers updated. Detailed handoff jotters/batch-014-working.md.

Carry: SR123FlyingBoneShield absent273wholeinventory after266active, dispositionquery notinventedloss. SR12427716four→five masters. SR12528084thirdpunch→finalpunch: punch/kick/punch. SR12628419halfyear→eight infiltration, mission11=3outside+8city;halfyearcontacts/stakeoutseparate. SR12728497firstsightvs280same-shopquery conditionalclose-look. SR12870copyitems individualholds. SR099withdraw before/afterrepair:273Threebreakthrough/28230continuedReunionbenefit. SR06327531FrostDemonpriorlossexplicit. SR104sourceversionholdunresolved. SR11827117twins少主strengthens.

Nearly1yearsinceQingMao27323. FYThreeinitial/BaiThreepeak;aptituderise一分noinventedtotal. YangrenegotiatedFourpeak,notThree/Five;currentwealth50/50,future70/30. Oath3000split1500each,Baistorage6700ownshare;Xprebalanceunknown.278cash420k;gamblingnearly100kaggregate,8000lot/SwordShadow32000valuationnotcash. Million/bountyremovalrefused,healing+twoPurplebadgesaccepted. StrongPlunderstarved,FleshBonereturned,RicePouchconsumedbreaker;twoFYprioroathsremoved,counterpartsstillbound.285newoathproduced,terms/removalnotshown.

FirstfightTangQingkilled4Gu≈2000+20–30stones;thirdTangXiongsurrendersBearGrand. FYbearstrengthincomplete;Canopyconstructdamage≠Gudeath. 500registrationVineGuShang-owned.30net/80tierwins,max1/day,min1/10days,forced1/month,net5lossdisqualifies. Thirdwin281;secondoffpage. LiRan50plus,target8city,child5/6FYspeech. HeartVoice100paceintentionalonly;count1,2,5intentional. Originallegendaryrumourstaged,fakestoneswapexplainsmissingGu. FlowerBudstolenwith30–40stones;285publicAllOutEffortopening,3stonecollisioncoverstory. Noinventeddealpayment/futurefights. Backupremoteunresolved;nooriginalsource/siteedits/uploads/deletions.
''')
assert len(cs)==285 and len(ledger)==128 and len(new)==6
assert all(not v['approved'] and not v['applied'] for v in ledger)
assert all(z['text']==src(z['chapter'],z['paragraph'])['text'] for v in events+resources for z in v['sources'])
texts={t for c in cs for t in c['paragraphs']}
for line in report.splitlines():
 if line.startswith('> '):assert line[2:] in texts
sha=hashlib.sha256((r.parent.parent/'benchmark/sources/Gu-Zhen-Ren.epub').read_bytes()).hexdigest();assert sha=='1ef1c29b6bddd7994f56696e2d091363aa8bbcee4889439465a9e2c51437dd5d'
qa=dict(passed=True,chapters=285,batch_paragraphs=np,batch_characters=nc,paragraphs=tp,characters=tc,proposals=len(ledger),held=126,withdrawn=['SR-047','SR-099'],copy_items=len(fixes),chronology=len(events),resources=len(resources),reading_segments=8,next=286,source_sha256_unchanged=sha)
save('batch-014-qa.json',qa);print(json.dumps(qa,indent=2))
