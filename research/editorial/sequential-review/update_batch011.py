from pathlib import Path
import json,shutil
from openpyxl import Workbook
from openpyxl.styles import Font,PatternFill,Alignment
r=Path('/home/user/editorial/sequential-review')
def load(n):return json.loads((r/n).read_text())
def save(n,v):(r/n).write_text(json.dumps(v,ensure_ascii=False,indent=2))
for n in ['reading-progress.json','proposal-ledger.json','chronology-register.json','resource-register.json','working-standards-register.json']:
 d=r/'history'/('before-batch011-'+n)
 if not d.exists():shutil.copy2(r/n,d)
cs=sum([load(f'batch-{i:03d}-source.json') for i in range(1,12)],[]);by={c['corpus_chapter']:c for c in cs};batch=cs[220:240]
def src(c,p):return dict(chapter=c,paragraph=p,file=by[c]['file'],text=by[c]['paragraphs'][p-1])
def ss(rr):return [src(*z) for z in rr]
def loc(rr):return [{k:v for k,v in z.items() if k!='text'} for z in ss(rr)]
def refs(z):return '; '.join(f"Ch{x['chapter']} p{x['paragraph']}" for x in z)
def find(c,term):
 hits=[i for i,t in enumerate(by[c]['paragraphs'],1) if term in t];assert len(hits)==1,(c,term,hits);return(c,hits[0])
def reader(c,p,t):
 if (c==151 and (31<=p<=67 or p in [98,99])) or (c,p) in [(201,22),(203,84)]:return '[Restricted passage omitted from reader-facing copy. Original numbering retained; original EPUB unchanged.]'
 return t
ledger=load('history/before-batch011-proposal-ledger.json');new=[]
def pro(i,cat,rr,action,why,conf,dep):
 v=dict(id=f'SR-{i:03d}',category=cat,locations=loc(rr),recommended_action=action,rationale=why,confidence=conf,status='Active provisional proposal; no approval',dependencies=dep,approved=False,applied=False,publication_status='HOLD: full 2334-chapter reading and global reconciliation outstanding');ledger.append(v);new.append(v);return v
pro(104,'incompatible source versions: twins’ fate',[(226,136),(226,137),(228,20),(228,25),(231,79),(231,80),(233,9)],'Quarantine the witness conflict for an edition decision. Preserve the EPUB, label226pp135–137 as compiler paratext, and collate an independently sourced226/231/228/233 sequence before choosing a base version. Do not silently change either deaths to escape or disappearance to death. If a coherent death-branch text is eventually chosen,231pp79–80 require an explicitly documented editorial treatment, not an invented authorial quotation.','226 narrates the deaths;228 and233 affirm them.231 instead says the twins gained an opportunity, disappeared and may be met again. These refer to the same current sequence, not separate rebirth histories. The compiler admits selecting a different226 but its claims about original text, censorship and authorial intent are not authenticated.','Very high internal incompatibility; unresolved canonical provenance.','Independent witnesses, edition/version provenance, later sequential references, user’s eventual base-text decision. Compiler claims are evidence of intervention, not proof of authorial priority.')
pro(105,'missing negation in hostage observation',[(227,23),(228,25),(231,80)],'Preferred227p23 看到百生、百花→没有看到百生、百花, subject to checking a second witness.','The children are no longer in the pair’s hands in either competing fate-version. The subsequent question about their whereabouts fits an absence, not seeing both present.','High contextual missing-negation candidate.','Check immediate scene and alternate witness. This repair does not settle whether the children died or were transported.')
pro(106,'village/caravan interval',[(233,61),(233,62),(233,64),(233,65)],'Conditional preference233p65 第九天→第十天 if all labels count from the same work/agreement start. Alternative: retain day nine and change three days late to two. Keep both held until the counting anchor is established.','Seven workdays followed by arrival three days later yields day ten under a shared day-number anchor, whereas the source says day nine. Inclusive counting or different prediction anchors must first be excluded.','High local numerical tension; moderate repair direction.','Recheck232agreement, inclusive day labels and any later explicit total. Do not manufacture a calendar or assume all intervals additive.')
pro(107,'Ice Muscle effect versus sweat descriptions',[(203,79),(205,38),(223,46),(233,54)],'If the continuing anti-sweat effect is confirmed without exceptions, remove 大汗淋漓 from203p79 and 浑身都被汗水淋湿了 from205p38, with local punctuation adjusted. Preserve breathlessness, fatigue and chill; do not replace sweat with a fabricated secretion or temporary loss of Ice Muscle.','233 explicitly says Ice Muscle stops sweat and blood;203/205 explicitly describe Bai sweating in the same body after the effect was acquired.223 also explains a permanent conflict with Bone Spike. This is separate from whether the original Gu remains in inventory.','High surface inconsistency; conditional physiological scope.','Later effect qualifications and source witnesses. 止血 is not automatic proof that no wound can ever bleed; do not globally delete every bleeding scene. SR060 inventory query remains open.')
pro(108,'Moonlight Gu name at the inheritance comparison',[(222,19),(212,59)],'Preferred222p19 月刃蛊→月光蛊.','The basic Gu of Gu Yue village is Moonlight Gu; moonblade is its attack.212’s 月谷 name already has a separate located candidate. This is not permission to replace every mention of moonblade.','High local name candidate.','Check earliest naming and another witness; keep Gu names distinct from their emitted attacks.')
fixes=[(221,21,'令一个误会','另一个误会'),(221,53,'话赌在','话堵在'),(225,28,'笑肉蛊','肉笑蛊'),(226,58,'骨头团圆蛊','骨肉团圆蛊'),(230,47,'空窍力','空窍里'),(231,2,'拔生','拔升'),(231,22,'骨肉团圆蛊胡','骨肉团圆蛊'),(234,94,'走你','揍你'),(236,27,'骨枪螺旋蛊','螺旋骨枪蛊'),(236,30,'饱受','保守'),(237,6,'一楞','一愣'),(237,33,'卖了死活','卖了私货'),(237,40,'交交他们','教教他们'),(237,53,'踹到','踹倒'),(237,71,'仿佛再问','仿佛在问'),(237,80,'吐沫','唾沫'),(237,93,'楞了一下','愣了一下'),(238,26,'只要抿着嘴','只好抿着嘴'),(238,51,'叫得最唤','叫得最欢'),(238,52,'怎么不就能','怎么就不能'),(238,84,'楞了一下','愣了一下'),(238,109,'只要请来','只好请来'),(239,2,'这只队伍','这支队伍'),(239,2,'这只商队','这支商队'),(239,8,'那就我就会','那我就会'),(239,20,'学银真元','雪银真元'),(239,38,'拈亲带故','沾亲带故'),(239,43,'鼓掌之间','股掌之间'),(239,86,'丑化说在前头','丑话说在前头'),(239,86,'绕不过他','饶不过他'),(240,4,'这只匪猴群','这支匪猴群'),(240,8,'声浪卷席','声浪席卷'),(240,22,'战到猴王面前','站到猴王面前'),(240,28,'吐沫','唾沫'),(240,31,'这型号','这信号'),(240,63,'却不在动手','却不再动手'),(240,70,'度过匪猴山','渡过匪猴山'),(240,75,'这只商队','这支商队'),(240,76,'招受','遭受'),(240,82,'这只队伍','这支队伍')]
# Mountain passage is not a water crossing: prefer a neutral verb, not 渡过.
fixes=[(c,p,a,'通过匪猴山' if (c,p)==(240,70) else b) for c,p,a,b in fixes]
for c,p,a,b in fixes:assert a in src(c,p)['text'],(c,p,a)
v=pro(109,'located copy candidates',sorted(set((c,p) for c,p,a,b in fixes)),'Review each listed substitution individually after approval; no automatic source normalization. Preserve compiler prose as documentary evidence rather than silently correcting its typos.','Located wrong characters, dropped/extra words, Gu-name order, classifiers and a contextual travel verb.','Mostly high local copy confidence; stylistic and classifier items remain editorial preferences.','Second-witness collation where possible; full-novel hold applies even to obvious typos.')
v['copy_items']=[dict(chapter=c,paragraph=p,original=a,replacement=b,confidence='Moderate wording/classifier choice' if (c,p) in [(239,2),(240,4),(240,70),(240,75),(240,82)] else 'High local copy candidate',status='Held; unapproved; unapplied') for c,p,a,b in fixes]
for v in ledger:
 if v['id']=='SR-098':
  v['prior_recommendation_before_batch011']=v['recommended_action'];v['locations']+=loc([(224,11)])
  v['recommended_action']='Reverse the previous preference: preserve214p28 肉骨上师; preferred214p45 骨肉上师→肉骨上师, following the explicit dual-identity statement224p11. Do not reorder the separate healingGu 肉白骨.'
  v['rationale']='224p11 explicitly identifies Grey Bone Scholar’s other title as 肉骨上师. This outweighs the conflicting isolated title in214p45 and reverses the earlier conditional preference.'
  v['confidence']='High current title evidence; still held for global/source reconciliation.'
  v['batch011_update']='Preferred direction reversed on explicit224p11 evidence; old action preserved in history and record. No edit applied.'
 if v['id']=='SR-099':
  v['locations']+=loc([(230,51),(230,60),(231,22)])
  v['batch011_update']='Actual transfer works before RevolutionThree and enables rapid RevolutionOne progression230–231, strengthening the before/after query. Benefits after RevolutionThree remain possible, so not certified.'
  v['confidence']='Moderate conditional scope query after actual operation; later-stage benefit unresolved.'
 if v['id']=='SR-060':v['batch011_update']='223/233 show permanent IceMuscle bodily effect, not proof of where the original Gu went. Keep inventory question separate from SR107 sweating.'
events=load('history/before-batch011-chronology-register.json')['entries'];resources=load('history/before-batch011-resource-register.json')['entries'];ne=[];nr=[]
def ev(timeline,kind,event,constraint,rr,status='Source evidence; provisional global reconciliation'):
 v=dict(id=f'CHR-{len(events)+1:03d}',timeline=timeline,kind=kind,event=event,constraint=constraint,evidence_status=status,dependency='Full sequential reading; preserve explicit anchors and witness status',sources=ss(rr));events.append(v);ne.append(v)
def res(kind,entry,calculation,rr,status='Source evidence; no emendation applied'):
 v=dict(id=f'RES-{len(resources)+1:03d}',kind=kind,entry=entry,calculation=calculation,status=status,sources=ss(rr));resources.append(v);nr.append(v)
ev('Former life information / current action','memory provenance','Entrance known from hearsay','First physical visit; banquet recollection supplies mechanism, not personal prior exploration.',[find(221,'传闻'),find(221,'酒宴上透露')])
ev('Current sequence / conflicting witness','source-version fork','Twins dead versus missing','226 substitution note;228 death,231 disappearance with anticipated reunion,233 death. Not a rebirth interval. Keep both source claims visible.',[(226,136),(228,20),(228,25),(231,79),(231,80),(233,9)],'Incompatible witness; SR104 held')
ev('Mechanics time limit','revival interval','Resurrection Gu','Seven shichen approximately14 conventional hours, notseven hours. Wholebody condition. HistoricalVenerable beneficiaries do not establish cultivationrank whenrevived.',[(224,21)])
ev('Revised current life','flight and shelter','Escape duration','DamagedFootlessBird flies morethanhalfday,crashesatdusk; caveaftermorethanone shichen. Not a full day at undamagedtheoreticalspeed.',[find(228,'半天'),find(228,'时辰')])
ev('Revised current life','travel to village','Detour and arrival','Two-day detour aroundPurpleYou; roadwalk andeveningvillagearrival separatelyanchored. No assumedinstant arrival.',[find(229,'两日后')])
ev('Former-life forecast','future history','Concealment countermeasures','Popularisation about150years later; next50yearswar develops counters, about200years frompresent. Not150/200years elapsed now.',[(239,24),(239,25)])
ev('Revised current life','cultivation','Upper to peak overnight','Cooperative essence supports RevolutionOne peak before workweek; RevolutionTwo subsequently reached daysbefore234notice. NoticeRevolutionOne isstale.',[(231,9),(231,12),(231,15),(231,16),(234,60),(239,20)])
ev('Revised current life','work interval','Seven days and late caravan','Seven-day passage, three-day lateness, ninth-day arrival conflict under a shared anchor. Keep labels pendingSR106.',[(233,61),(233,64),(233,65)],'Held local interval query')
ev('Revised current life','same-day actions','Joining, market and staged complaint','Firstemploymentdaymorning, marketatdusk, thennightfight/self-injury/complaint. Nextmorning releasearranged; notfourdistinctdays.',[(237,106),(237,125),(239,29),(239,30),(239,41)])
ev('Revised current life','travel ellipsis / endpoint','Bandit Monkey Mountain','Ten-plusdays thereafter;half-crocstrength accumulated.240ends beforeFYwrestles: outcome not yetread.',[(239,56),(239,59),(240,89),(240,101)])
res('Inheritance acquisitions','Bone Spear and branches','TwohundredRevolutionOne and20-plusRevolutionTwo spiralrefined,remainingjarGu destroyed. FlyingBoneShieldchosen;otherpillarsleft. Parallelhallsexplainlaterintactskeleton.',[find(222,'两百'),(224,65),(224,66)])
res('Healing / activation','Flesh Bone Gu','FYrefines then lendsBai;RevolutionOnecannotmeetinstantactivationthreshold, whileBaiheals. Ownership doesnotguaranteeusablepower. Rebuildsfleshnotearcartilage.',[find(226,'两成'),find(228,'软骨')])
res('Losses / retained holdings','Escape inventory','EarGrass,Centipede,BackCarapace,IronThorn,HiddenScale,FootlessBird lost. ShieldfailuredoesnotproveCanopyGu died:228retainsit. ClearHeatnowlisted, returnimplicitnotdated.',[(228,53),(228,62)])
res('Ownership transfer','Reunion pair','FYwithdrawsintent;Baiownsredhalf,FYgreen. Notjustrevocableloan. Seriesfivegrades,actualmiddlegrade.',[(230,31),(230,32),(230,35),(230,36),(230,52)])
res('Essence arithmetic','60 percent transfer','10 units→6;6→3.6roundtrip=36%original,64%lost. 20/40/60/80/100gradeefficiencies. Quantitylossnotrank-qualityloss, aura reassigned.',[(230,49),(230,51),(230,56),(230,57),(230,58),(230,59),(230,60)])
res('Consumed body effects','Iron/Jade bone and crocodile strength','Permanentreinforcement allowsFYcrocstrength;BaiIceMuscle/JadeBonecompatibilitydifferentfromBoneSpike/BloodSweat. EndpointFYhalf-crocnotfullcroc.',[(233,54),(239,28),(239,59)])
res('Concealment / cultivation','Hidden practice','RevolutionTwo rediron;FourFlavourretainedbutBaisilverbetter. Internalpracticeconcealed,externalactivation risks cover.',[(239,20),(239,21),(239,22),(239,23),(239,26)])
res('Food / production constraints','Starvation and forgone income','ManyBoneSpearsdieas milkrunsout;exactremainingunknown. Lotuspotentialdozensstones/day notactualincome:cannotuseopenly.',[(239,59),(239,62)])
res('Cash transaction','Two stones recycled as lure','Leafsale2stones. Thrownandpickedup,managerrecovers,entrustedtomanger,stillwithhim239. No netextra2 or3+2revenue.',[(237,2),(237,58),(238,82),(238,83),(239,51)])
res('Strength contest rules','Natural strength versus active Gu','RetainedTurtle/Bearstrengthallowed;activeGucheating. JiaYongloses,JiaPingwins2. Naturalphysicaleffectsnotre-activatedeachbout.',[(240,20),(240,57),(240,59),(240,65),(240,74)])
np=sum(len(c['paragraphs']) for c in batch);nc=sum(sum(map(len,c['paragraphs'])) for c in batch);tp=sum(len(c['paragraphs']) for c in cs);tc=sum(sum(map(len,c['paragraphs'])) for c in cs)
save('proposal-ledger.json',ledger);save('chronology-register.json',dict(scope='Sequential through240; personal/external clocks and conflicting witness versions separately labelled',entries=events));save('resource-register.json',dict(scope='Sequential through240; holdings, ownership, transfer efficiency, consumed effects and losses distinguished',entries=resources))
progress=load('history/before-batch011-reading-progress.json');progress.update(sequential_chapters_completed=list(range(1,241)),paragraphs_read=tp,paragraph_characters_read=tc,next_chapter=241,remaining_chapters=2094,batch_report='Batch-011-Chapters-221-240.md',scope='Full sequential Chinese-source reading through240; not fresh bilingual or live-site audit',whole_novel_chronology_verified=False)
progress['batches'].append(dict(id='011',chapters=[221,240],paragraphs=np,characters=nc,reading_segments='Ten complete untruncated two-chapter outputs'))
progress['chapters'] += [dict(chapter=c['corpus_chapter'],file=c['file'],title=c['title'],paragraphs=len(c['paragraphs']),first_paragraph=1,last_paragraph=len(c['paragraphs'])) for c in batch];save('reading-progress.json',progress)
save('batch-011-reading-log.json',dict(status='Complete',endpoint=240,next_unread=241,segments=[dict(chapters=[a,a+1],status='Full paragraph sequences printed and read; untruncated',paragraphs=sum(len(by[n]['paragraphs']) for n in [a,a+1])) for a in range(221,241,2)],note='Actual reading, not extraction-only coverage. Includes paratext separately identified. No invented timestamps.'))
text=['# Numbered Chinese source: Chapters221–240','Original EPUB wording retained. 226pp135–137 are separator/compiler note;227pp192–193 separator/author-attributed note. Neither is treated as ordinary narrative or independent proof of authorship.']
for c in batch:text += [f"## Corpus chapter {c['corpus_chapter']}: {c['title']}",f"Volume: {c['volume']} | EPUB: {c['file']}"]+[f"{i}. {t}" for i,t in enumerate(c['paragraphs'],1)]
(r/'Batch-011-Numbered-Chinese-Source.md').write_text('\n\n'.join(text))
for name,vs in [('Chronology',ne),('Resources',nr)]:
 out=[f'# Batch011 {name} jotter','All evidence provisional; no source edits.']
 for v in vs:
  out += [f"## {v['id']}: {v.get('event',v.get('entry'))}",v.get('constraint',v.get('calculation')),v.get('evidence_status',v.get('status'))]
  for z in v['sources']:out += [f"Ch{z['chapter']} p{z['paragraph']}",'> '+z['text']]
 (r/f'jotters/Batch-011-{name}.md').write_text('\n\n'.join(out))
out=['# Batch011 continuity and proposed corrections','All held. Earlier SR098 preferred direction reversed; SR099 strengthened but not settled.']
for v in [x for x in ledger if x['id'] in ['SR-098','SR-099']]+new:
 out += [f"## {v['id']}: {v['category']}"]+[f"**{k}:** {v[k]}" for k in ['recommended_action','rationale','confidence','dependencies','status']]
 if 'copy_items' in v:
  for z in v['copy_items']:out += [f"### Ch{z['chapter']} p{z['paragraph']}: {z['original']} → {z['replacement']}",z['confidence'],'> '+src(z['chapter'],z['paragraph'])['text']]
 else:
  for z in v['locations']:out += [f"Ch{z['chapter']} p{z['paragraph']}",'> '+src(z['chapter'],z['paragraph'])['text']]
(r/'jotters/Batch-011-Continuity.md').write_text('\n\n'.join(out))
(r/'jotters/Batch-011-Preserve.md').write_text('''# Batch011 preservation cautions

- Mixed twins versions are a witness problem, not a new rebirth or a licence to invent bridging events.
- Compiler note is not authenticated author testimony. Keep it separate from the author-attributed FootlessBird note.
- Multiple skeleton rooms and BoneSpikeGu are explicitly different branches, not resurrection/duplication errors.
- 肉骨上师 is explicitly confirmed224; do not normalize it to 骨肉上师. 肉白骨 remains a different name.
- 双修 here is cooperative cultivation, not inherently sexual. Villagechief’s misunderstanding is intentional.
- Seven shichen means approximately fourteen conventional hours, not seven.
- 60% transfer means 36% roundtrip; source三分半有余 is consistent with3.6. Do not change it to3.5exact.
- The essence acquires the recipient’s aura, not the recipient’s rank-quality. Silver stays stronger thanbronze.
- RevolutionOne aperture ordinary stonewall is not the consumed StoneApertureGu’s terminal condition.
- Permanent IceMuscle effect does not prove originalGu retained; sweating query is separate.
- Gu ownership, physical placement, borrowed activation and formal refinement transfer differ.
- No claim that every inheritance branch was looted; fullinheritance rhetoric is relative to keyprize.
- StaleRevolutionOnewantednotice does not contradict narratorRevolutionTwo. Bounty is not money received.
- Zhang/Shang surnames and HeiTu/BaiYun aliases are deliberate. 少主 is not identical to designated少族长.
- ShangXinCi’s charity is informed, not proof she cannot recognize fraud. FY’s interest is strategic here.
- Leafsale yields2stones, not3; manager eventually holds same2. No invented netprofit/refund.
- Lotusproduction potential is not availableincome underconcealment; BoneSpearsstarve so200isnotendpointstock.
- Permanentstrengthallowed inarmwrestling; activatingGu forbidden.240endsbeforeFYcompetes.
''')
stand=load('history/before-batch011-working-standards-register.json');stand['coverage_through']=240
su={'WS-01':'226compiler claims and231alternatefate must not be merged with narrator facts. Deception, hearsay and former-life memory remain separately labelled.','WS-02':'230 confirms20/40/60/80/100% transfer tiers; current60%, roundtrip36%. Quantity, pool-capacity fraction and essencequality are different.','WS-03':'Actualcooperativecultivation enablesRevolutionOneupper→peak;RevolutionTwoalreadydaysbefore234. SR099after/before3stillconditional.','WS-04':'Reunionhalf ownershiptransferred230, healingGu borrowed226. Permanentboneeffects consumed;Ear/Centipede lossesexplicit;Canopyretained.','WS-05':'Seven时辰224≈14h.233seven+threelate/ninthdayheld.239150/200yearhistoryforecastsnotelapsedtime.','WS-06':'MilkrunsoutandBoneSpearsstarve;Lotuscannotproduceopenly. Two-stonesaleandmanagerholdingnotadditionalincome.','WS-07':'FootlessBirdhalfdaydamagedflightnot10000lifullratedday. Caravantravelandarmwrestlingtrafficpreserveconditions.','WS-08':'少主(clanleaderchildren) versus少族长(designatedheir) explicit235. Zhang/Shangnamechangeintentional;twinscurrentageremainsunproved.','WS-09':'SR098reversedby224explicitdualidentity;noautomatictitleorder. Names/months andmissingnegation individuallylocated.','WS-10':'Actualcoverage240/2334;2094remain. No source/site edits approved/applied;backupstillunresolved.'}
for v in stand['entries']:v['batch011_update']=su[v['id']]
stand['entries'].append(dict(id='WS-11',topic='Agreed working rendering of 人是万物之灵',status='User-accepted working translation; not manuscript implementation approval',rule='Man is the most intelligent of all living things. Keep the repeated maxim recognisable across synopsis and narrative; do not imply different meanings through inconsistent paraphrase.',evidence='User accepted after discussion of 灵 as intelligence/perceptiveness rather than a universal animating spirit. 人 is collective humanity; 万物 literally all things, living things contextual. Full sourced refrain: 人是万物之灵，蛊是天地真精.',reopen='If a specific later quotation, speaker or taxonomic contrast requires contextual annotation; not a reason to silently replace the agreed refrain.',batch011_update='Recorded user agreement now. Tieba examples discussed previously are fan usage, not consensus or canonical edition authority. No source/site changes.'))
save('working-standards-register.json',stand)
out=['# Working editorial standards','## Evidence checkpoint: Chapters1–240','Working rules do not certify whole-novel factual consistency or authorize manuscript changes.']
for v in stand['entries']:out += [f"## {v['id']}: {v['topic']}"]+[f"**{k}:** {v[k]}" for k in ['status','rule','evidence','reopen','batch011_update']]
(r/'WORKING-STANDARDS.md').write_text('\n\n'.join(out))
def quote(c,p):return f"**Ch{c} p{p}:**\n\n> {src(c,p)['text']}"
report=f'''# Sequential close-reading review: Chapters 221–240
## Batch 011 | The Omniarch

**Actual sequential coverage: 1–240 of 2,334. Next unread: 241. Remaining: 2,094.**

Twenty chapters read in ten complete, untruncated two-chapter sequences: **{np:,} paragraphs / {nc:,} source characters**. Cumulative: **{tp:,} paragraphs / {tc:,} characters**. Counts include attached paratext, which is identified separately from narrative.

The ledger now contains **109 records: 108 active and held, one withdrawn**. Six new records include **{len(fixes)} individually located copy candidates**. Earlier SR-098 is substantially revised. No proposed source, translation or site edits have been applied. This is Chinese-source review, not a fresh bilingual/live-site audit.

## 1. Critical finding: this witness combines incompatible versions

Chapter226 narrates the twins’ deaths in the refinement. Its appended compiler note says a supposedly earlier version was substituted for a later version in which the children were transported away. That is a compiler’s claim, not authenticated authorial testimony. The note also speculates about censorship, authorial intention and hypothetical improvements; none of those claims should be silently promoted into canon.

The contradiction is independently visible in the narrative:

{quote(228,25)}

{quote(231,79)}

{quote(231,80)}

Chapter233p9 again refers to the twins being killed. These are competing accounts of the same post-rebirth events. **This is not an original-life versus revised-life distinction.**

**SR-104 proposes an edition-level hold:** preserve the witness, label226pp135–137 as compiler paratext, and collate independently sourced versions of the affected passages before selecting a coherent base. Neither rewriting231 to make the twins dead nor rewriting226/228/233 to make them escape is currently authorised. A patch invented by us must never be presented as the author’s original wording.

The separate note appended at227p193 is attributed to the author and discusses Footless Bird. It is not the same kind of source as the226 compiler note; that attribution has not been independently authenticated either.

### A related missing negation

{quote(227,23)}

The children are no longer being carried by the pair under either fate-version, and the surrounding dialogue asks where they are. **SR-105: 看到百生、百花 → 没有看到百生、百花** is a strong local candidate. It does not resolve the larger version dispute.

## 2. A previous proposal must change direction

Batch010 tentatively preferred 骨肉上师 over 肉骨上师. The inheritance book now explicitly identifies both titles:

{quote(224,11)}

**Revised SR-098:** preserve214p28 肉骨上师; prefer correcting214p45 骨肉上师 to 肉骨上师. The old recommendation is retained in the audit history. This is precisely why even plausible local corrections remain held until later evidence is read. The healing Gu 肉白骨 is a separate name and must not be mechanically reordered.

## 3. Cooperative cultivation: the arithmetic works

双修 in this sequence means cooperative cultivation. It does not imply sexual activity. The village chief’s later mistaken interpretation is an intentional joke, not the literal mechanism.

The pair refine separate halves of the same linked Gu. Fang Yuan relinquishes his ownership of the red half so Bai can refine it. This is a real transfer of ownership, unlike permission to borrow another Gu.

{quote(230,51)}

| Quality | Essence retained per transfer |
|---|---:|
|骨肉相残|20%|
|骨肉相连|40%|
|情同骨肉, the pair’s result|60%|
|亲如骨肉|80%|
|骨肉至亲|100%|

**10 units → 6 units → 3.6 units.** The round trip retains36% of the original quantity, losing64%. The later wording meaning a little over three and a half is consistent with3.6; it should not be “corrected” to exactly3.5.

Three distinctions matter:

1. The donor’s essence acquires the recipient’s identifying aura. Its cultivation-grade quality does not automatically fall to the recipient’s native grade.
2. A small, carefully controlled amount of snow-silver essence can help a lower-rank aperture. Dumping in too much risks damage. The crowded Gu inventory contributes to the initial strain.
3. Permanent physical effects, a Gu’s ownership, and the ability to activate it at a particular rank are different questions. Fang Yuan can own Flesh Bone Gu while being unable to supply the instant power it needs; he can use Iron Bone under the different conditions created by borrowed stronger essence.

The overnight RevolutionOne upper-to-peak progression strengthens **SR-099**, the query over214’s “after RevolutionThree” rather than “before RevolutionThree”. It does not yet prove that cooperative cultivation has no useful application after RevolutionThree. That correction remains conditional.

Ordinary stone-wall aperture terminology at upper stage must also remain distinct from the earlier terminal Stone Aperture Gu condition.

## 4. Time and progression: separate reliable anchors from tension

| Evidence | Treatment |
|---|---|
|224: Resurrection Gu, 七个时辰|Approximately14 conventional hours, not7; intact-body condition also matters|
|228: damaged Footless Bird flight|More than half a day, ending at dusk; not a full undamaged day at its theoretical range|
|229: detour|Two days around the mountain; subsequent road travel retains its own anchor|
|231: cooperative cultivation|RevolutionOne upper to peak overnight|
|233: work and caravan|Seven days pass, caravan three days late, yet arrives on ninth day: held numerical tension|
|234: wanted notice|RevolutionOne notice is stale; Fang Yuan has already been RevolutionTwo for days|
|237–239: first caravan day|Market, assault and staged complaint occur in the same evening/night; arrangements follow next morning|
|239: mountain approach|Ten-plus days later; not an exact fourteen-day interval|
|239: concealment history|150-year and200-year points belong to former-life forecasts, not elapsed present time|

{quote(233,61)}

{quote(233,64)}

{quote(233,65)}

**SR-106:** if these share one counting anchor, day ten is the natural candidate for day nine. An alternative is changing three days late to two. Inclusive counting and the old chief’s prediction anchor still need reconciliation, so neither has been implemented. The earlier seven-day hunt question, SR-100, also remains open.

## 5. Ice Muscle: effect continuity versus inventory continuity

{quote(203,79)}

{quote(205,38)}

{quote(233,54)}

This is a stronger issue than merely assuming ice-themed skin cannot sweat: the source expressly assigns an anti-sweat effect, yet earlier scenes expressly describe Bai sweating.

**SR-107:** conditionally remove the sweating clauses while preserving breathlessness, fatigue and chill, unless later evidence supplies an exception. Do not invent a temporary failure of the effect. Nor does 止血 establish absolute immunity to every bleeding wound.

This does **not** settle SR-060, the older question of where the original Ice Muscle Gu went. A permanent bodily effect is not proof of continued possession of the Gu that produced it.

## 6. Inheritance and escape: preserve the resource distinctions

- Fang Yuan obtains200 Bone Spear Gu and over20 Spiral Bone Spear Gu. That is an acquisition checkpoint, not the eventual remaining stock.
- Different inheritance branches contain different skeleton halls and Gu. The pursuers’ intact skeleton does not resurrect the one Fang Yuan broke.224 explicitly supplies the branching explanation.
- Flying Bone Shield is selected; the other pillar choices are left. Obtaining the key inheritance is not proof that every branch was looted.
- Flesh Bone restores flesh, not the missing ear cartilage. Fang Yuan deliberately retains the disfiguring burns as part of his cover.
- The escape losses include Ear Grass, Chainsaw Golden Centipede, Back Carapace, Iron Thorn, Hidden Scale and Footless Bird. A broken defensive barrier does not prove the underlying Sky Canopy Gu died:228 lists it as retained.
- Clear Heat appears in the retained inventory. That closes the possession gap from the earlier loan without supplying an exact narrated return scene.
- Iron Bone and Jade Bone produce permanent bodily changes. Fang Yuan can then add crocodile strength; by239 he has accumulated **half a crocodile’s strength**, not a whole crocodile’s.
- Milk supplies run low and many Bone Spear Gu starve. Do not carry the initial200 forward as an exact endpoint inventory.
- The Lotus’s potential daily stone production is not actual spendable income while concealment prevents open use.
- Two stones are received for the leaves, then reused in the staged altercation, recovered by the manager, and entrusted back to him. This is not several independent two-stone gains.

## 7. Names, social roles and viewpoint: do not overcorrect

**少主 and 少族长 are explicitly distinguished in235:** children of a clan leader are not all designated heirs. Keep the English distinction visible rather than translating both mechanically as heir.

Zhang Xin Ci and Shang Xin Ci are deliberate name-context distinctions, not a misspelling. Hei Tu and Bai Yun are deliberate aliases. The source also distinguishes hired helpers from owned household slaves when the transfer to Zhang’s camp is negotiated.

Shang Xin Ci recognises deception and still chooses to help. Rendering her as simply too stupid to notice fraud would erase an explicit character distinction. Fang Yuan’s interest here is strategic; Bai’s suspicion of romantic attraction is a character’s interpretation, not narrator confirmation.

At the arm-wrestling checkpoint, prior permanent strength enhancements are permitted; actively using Gu during the match is cheating. Jia Yong’s loss and Jia Ping’s wins are therefore not explained by cultivation rank alone. **Chapter240 ends before Fang Yuan competes.** No result is claimed in this review.

## 8. New proposals and exact copy candidates

| Record | Proposal | Confidence / dependency |
|---|---|---|
|SR-104|Resolve the mixed twins-fate witness before editing|Very high incompatibility; provenance unresolved|
|SR-105|227p23 add missing negation|High local context; compare witness|
|SR-106|233 ninth/tenth-day or two/three-day tension|Moderate repair direction; counting anchor required|
|SR-107|Remove sweating clauses if Ice Muscle rule is unconditional|High surface tension; later exceptions untested|
|SR-108|222p19 月刃蛊 → 月光蛊|High name candidate; attack versus Gu distinction|
|SR-109|{len(fixes)} individually located copy candidates|Mostly high; wording/classifiers conditional|

SR-098’s title preference is reversed; SR-099 is strengthened but remains open. Every record includes an action, rationale, confidence, dependencies and held status in the ledger and continuity jotter.

'''
report+='| Location | Source fragment | Held candidate |\n|---|---|---|\n'+'\n'.join(f'|{c} p{p}|{a}|{b}|' for c,p,a,b in fixes)
report+=f'''

## 9. Agreed maxim and saved checkpoint

The working standards now record your accepted rendering:

**“Man is the most intelligent of all living things.”**

Man refers collectively to humanity; 灵 here concerns intelligence/perceptiveness, not a universal animating soul. 万物 is literally all things, with living things the agreed contextual English. Keep the recurrent maxim recognisable across synopsis and narrative. This records a working translation decision, not permission to alter the manuscript or site. Earlier Tieba examples were fan usage, not a representative consensus or authority for resolving this batch’s textual variants.

Saved alongside this report: numbered Chinese source, detailed working notes, chronology/resource/continuity/preservation jotters, ten-segment reading log, **109 proposal records, {len(events)} chronology entries, {len(resources)} resource entries**, the cumulative workbook and **11 working standards**. Pre-batch011 register snapshots preserve the earlier recommendations.

**Next unread:241.** Whole-novel consistency is not certified. No original source, manuscript, site or repository edits, uploads or deletions occurred. Remote research backup remains unresolved.
'''
(r/'Batch-011-Chapters-221-240.md').write_text(report)
# Reuse the tested cumulative workbook renderer, not the prior update routines.
old=(r/'update_batch010.py').read_text();wb=old[old.index('# Workbook: cumulative'):old.index("(r/'CURRENT-STATUS.md').write_text")]
wb=wb.replace('1–220 of2334','1–240 of2334').replace("('Next unread',221)","('Next unread',241)").replace('103total;102activeheld;1withdrawn','109total;108activeheld;1withdrawn').replace('range(10,0,-1)','range(11,0,-1)').replace("v['batch010_update']","v['batch011_update']").replace('Batch-010-Chapters-201-220','Batch-011-Chapters-221-240').replace('CHAPTERS201–220','CHAPTERS221–240').replace('Chapters201–220','Chapters221–240').replace('Twenty complete chapters; personal clocks and inventory scope distinguished','Twenty complete chapters; source-version conflicts and transfer mechanics distinguished')
exec(compile(wb,'workbook-and-docx','exec'))
(r/'CURRENT-STATUS.md').write_text(f'''# Sequential review checkpoint

Fully read **1–240 of2334**. Next unread **241**. Remaining **2094**. Suggested next batch241–260, adaptive to density.

Batch011: {np}paragraphs / {nc}characters. Cumulative: {tp}paragraphs / {tc}characters.109proposals:108activeheld,1withdrawn(SR047). SixnewrecordsSR104–109;SR109has{len(fixes)}copycandidates. {len(events)}chronology entries;{len(resources)}resources;11workingstandards. Allapproved/appliedflagsfalse. Whole-novel chronology NOTcertified.

Latest report Batch-011-Chapters-221-240.md/.docx. Source, fivejotters, readinglog,registers,workbook updated. Detailed next-turn handoff is jotters/batch-011-working.md plus011report. Pre011archivesretained;011generatoridempotentfrompre011, do NOT rerunoldergeneratorsovernewstate.

Critical carryforward:
- SR104 EPUBmixedversions:226death/refinement;226135–137compilerclaimsoriginalsubstitution/unverifiedcensorship;22820/25death;23179–80opportunity/disappeared/futurereunion;2339death. Samecurrenttimeline, NOTrebirthresolution. Do notcertifycanon/compilerintent;independentwitnesscollationneeded. Sourceunchanged.
- SR10522723看到→没有看到hostageshighcontextcandidateworksbotheditions.
- SR098 REVERSED:22411explicit肉骨上师/GreyBoneScholaridentity;21428preserve肉骨,21445骨肉→肉骨preferred. Originalcandidateinarchive/history. 肉白骨separateGu.
- SR1062337days+3lateyet9thday;candidate10thconditionalsharedanchor,orlate2. SR100huntcalendarstillopen.
- SR10720379/20538Baisweats vs23354IceMusclestopssweat;effectpermanent223/233, don'tinferoriginalGupossessionSR060. Do noteraseallbleeding.
- SR10822219月刃蛊→月光蛊. SR109copycandidates{len(fixes)};allheld.
- Cooperativecultivation23060%oneway,36%roundtrip(10→6→3.6),tiers20/40/60/80/100. Auraconvertednotessencerank. Separatepowerthreshold/quantity/quality/owner. Revolution1aperturecrowdingGu+silver, spearsmovedBai. SR099before3strongerbutafter3possiblefuturebenefitsunread.
- FYRevolution1upper→peakovernight231;Revolution2daysbefore234staleRevolution1notice.239Revolution2confirmed;FourFlavourstillheldbutinferiortoborrowedsnowSilver. BoneGuconsumed232, FYIron/BaiJade;FYhalfCroc239plusdoubleboar,notfullCroc. BaiIceMuscle/Jadecombo,can'tBoneSpike/BloodSweat.
- 222200BoneSpear+20plusSpiral acquired;239manySpearstarveexactremainingunknown. Milkfood;Lotuspotentialdozensstones/daynotactualproductionundercover. Permanentstrengthallowed240armwrestling,activeGucheat. Multiplefakeparallelhallsskeletonsnotduplication.
- 227lostHiddenScale/Centipede/Ear;228listalsoBackCarapace/IronThorn/Bird;Canopyretained. ClearHeat228inventoryimplicitreturnbutnoscenedate. FYrightEarcartilageunhealablewithFleshBone,scarskeptdeliberately. FootlessBird1usehalfdaydamagedflightnotnominalfullrangecontradiction.224revive7shichen≈14hwholebodycondition;Venerablesrankatbenefitnotestablished.
- 239150/200yearConcealBreathforecastsnotelapsed.2292daysdetour,231firstcultivationnight,232/233workweek/calendarquery,234joinfirstmorning→235–238sameevening/night→239nextmorningcamptransfer→10plusdaysBanditMonkey.240endsBEFORE FYarmwrestles.
- Leafsale2stones(not3),managerholdsafterstagedassault;noadditionalgain. XinCiZhang/Shangintentional;少主vs少族长explicit235;charityawareoffraudnotstupidity;FYstrategicnotromantic. Hiredhelpersnotnecessarilyownedslaves239.
- WS11 recordsaccepted 'Man is the most intelligent of all living things.' Collectivehumanity/intelligence,notcosmicsoul;consistentrefrain,notimplementationapproval.

No source/site/repository edits, uploads or deletions. Backup unresolved. OriginalEPUBunchanged. 226compiler/227author-attributedparatext distinguished. Olderholdsupersededonlywhereexplicitlynoted.
''')
assert len(cs)==240 and len(ledger)==109 and len(new)==6
assert tp==18787+np and tc==671746+nc
assert all(not v['approved'] and not v['applied'] for v in ledger)
assert len({v['id'] for v in events})==len(events)
assert len({v['id'] for v in resources})==len(resources)
assert all(z['text']==src(z['chapter'],z['paragraph'])['text'] for v in events+resources for z in v['sources'])
texts={t for c in cs for t in c['paragraphs']}
for line in report.splitlines():
 if line.startswith('> '):assert line[2:] in texts
print('QA PASSED',dict(chapters=240,new_paragraphs=np,new_characters=nc,paragraphs=tp,characters=tc,proposals=len(ledger),copy_items=len(fixes),chronology=len(events),resources=len(resources),next=241))
