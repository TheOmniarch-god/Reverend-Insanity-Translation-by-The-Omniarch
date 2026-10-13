from pathlib import Path
import json,shutil
from openpyxl import Workbook
from openpyxl.styles import Font,PatternFill,Alignment
r=Path('/home/user/editorial/sequential-review')
def load(n):return json.loads((r/n).read_text())
def save(n,v):(r/n).write_text(json.dumps(v,ensure_ascii=False,indent=2))
for n in ['reading-progress.json','proposal-ledger.json','chronology-register.json','resource-register.json','working-standards-register.json']:
 d=r/'history'/('before-batch012-'+n)
 if not d.exists():shutil.copy2(r/n,d)
cs=sum([load(f'batch-{i:03d}-source.json') for i in range(1,13)],[]);by={c['corpus_chapter']:c for c in cs};batch=cs[240:255]
def src(c,p):return dict(chapter=c,paragraph=p,file=by[c]['file'],text=by[c]['paragraphs'][p-1])
def ss(rr):return [src(*z) for z in rr]
def loc(rr):return [{k:v for k,v in z.items() if k!='text'} for z in ss(rr)]
def refs(z):return '; '.join(f"Ch{x['chapter']} p{x['paragraph']}" for x in z)
def find(c,term):
 hits=[i for i,t in enumerate(by[c]['paragraphs'],1) if term in t];assert len(hits)==1,(c,term,hits);return(c,hits[0])
def reader(c,p,t):
 if (c==250 and (24<=p<=31 or p in [33,35,36])) or (c==151 and (31<=p<=67 or p in [98,99])) or (c,p) in [(201,22),(203,84)]:return '[Restricted passage omitted from reader-facing copy. Original numbering retained; original EPUB unchanged.]'
 return t
ledger=load('history/before-batch012-proposal-ledger.json');new=[]
def pro(i,cat,rr,action,why,conf,dep):
 v=dict(id=f'SR-{i:03d}',category=cat,locations=loc(rr),recommended_action=action,rationale=why,confidence=conf,status='Active provisional proposal; no approval',dependencies=dep,approved=False,applied=False,publication_status='HOLD: full 2334-chapter reading and global reconciliation outstanding');ledger.append(v);new.append(v);return v
pro(110,'Chen deputy leader’s name',[(247,37),(247,38),(249,16),(252,75),(252,76),(252,78),(255,39),(255,40),(255,41)],'Provisional preference: normalize the earlier 陈双金 references to 陈双全 if subsequent attestations and an independent witness support the latter. Preserve both forms in the research register until then; do not invent two deputy leaders.','The same Chen leader associated with Chen Xin is called Shuang Jin in247/249 and Shuang Quan repeatedly in252/255. No replacement or introduction of another deputy is narrated.','High name inconsistency; moderate choice of preferred form.','Later name attestations and independent Chinese witnesses; repetition alone does not establish original authorial priority.')
pro(111,'caravan headcount after identities revealed',[(249,1),(249,5),(250,73),(251,113),(252,7)],'Preferred scope clarification252p7: add 不计方白二人 after 商队. Retain11/27/38 as the old registered Gu-Master roster after the two Ou deaths. If a complete actual-rank roster is intended instead, use12/28/38, subject to confirming initial inclusion of the pair among the59 apparent mortals.','The subtraction12−1=11 and28−1=27 is correct, but it does not reclassify Fang/Bai after their reveal. Fang is actuallyRevolutionTwo upper, BaiRevolutionThree peak; the public believes bothRevolutionThree peak. Those three counting scopes yield different rank distributions.','High scope problem; conditional complete-population reconstruction.','Confirm who was included in249’s roll. Do not automatically use13RevolutionThree, which incorporates the false impression of Fang’s rank. No new people are acquired merely by revealing an identity.')
pro(112,'gold-grass proceeds versus profit and principal',[(242,65),(243,17),(244,58),(244,63),(249,71),(249,74)],'Clarifying candidate244p58: 八千块元石的收益→八千块元石的售款. Preserve the stated8000 proceeds and4000/4000 distribution. Track the less-than500 barter principal separately as unsettled rather than silently deducting500 or revising the split.','Revenue is8000, barter cost is less than500, and profit before other costs is therefore greater than7500. The earlier lending/profit-sharing language does not supply a complete capital-repayment schedule. 收益 can denote returns broadly; this is an accounting/translation precision proposal, not a proven arithmetic error.','High arithmetic; moderate lexical clarification; unresolved principal treatment.','Later settlement, exact acquisition cost and whether division concerns proceeds or net profit. Do not manufacture an exact7500 profit or3750 share.')
fixes=[(241,24,'楞了','愣了'),(241,27,'惊叹声迭传','惊叹声迭传'),(241,89,'这只混并起来的商队','这支混并起来的商队'),(242,15,'笑魇如花','笑靥如花'),(242,19,'被大劫','被打劫'),(242,19,'却到商家城','去到商家城'),(242,75,'楞了一下','愣了一下'),(243,12,'砰然而动','怦然而动'),(243,48,'启程的前天晚上','启程的前一天晚上'),(244,54,'想买到一万块','想卖到一万块'),(244,54,'坐不了主','做不了主'),(244,62,'不要在这么弄险','不要再这么弄险'),(245,21,'都表示纷纷点头','都纷纷点头'),(245,87,'小蝶有催促','小蝶又催促'),(246,8,'啸月山抵挡','啸月山地带'),(246,20,'损失一大步','损失一大半'),(246,36,'瘦减','缩减'),(246,61,'一磨搓','一摩挲'),(246,74,'一直走过她身边的驼鸡','一只走过她身边的驼鸡'),(247,16,'众价值','总价值'),(247,35,'如今家同舟共济','如今大家同舟共济'),(247,38,'大家伙心理都清楚','大家伙心里都清楚'),(247,93,'头昏脑涨','头昏脑胀'),(247,101,'看到这幅清晰','看到这情形'),(247,104,'白羽飞雪','白羽飞象'),(248,15,'白羽飞雪','白羽飞象'),(248,19,'枪尖定死','枪尖钉死'),(249,1,'一百三七人','一百三十七人'),(249,28,'命运栓在','命运拴在'),(249,89,'送个黑土你','送给黑土你'),(250,4,'须于你明说','须与你明说'),(250,8,'自热而然','自然而然'),(250,9,'私生子出生','私生子出身'),(250,14,'阁下随是','阁下虽是'),(250,23,'阴鸠','阴鸷'),(250,39,'双耳闻名','双耳嗡鸣'),(250,41,'绝然','决然'),(250,55,'帐篷周围的人。无不','帐篷周围的人，无不'),(250,62,'楞了','愣了'),(251,22,'这人真是','这人正是'),(251,24,'眼泪滚滚留下','眼泪滚滚流下'),(251,25,'嘶声力竭','声嘶力竭'),(251,34,'那个没有眼力','哪个没有眼力'),(251,40,'就像欧羊公撞来','就向欧羊公撞来'),(251,86,'皆楞','皆愣'),(252,60,'在外门跑的','在外面跑的'),(252,60,'心灵清楚','心里清楚'),(253,28,'他再杀了张柱之后','他在杀了张柱之后'),(253,31,'在运作几番','再运作几番'),(253,57,'出不多','差不多'),(254,3,'一只路过村子的商队','一支路过村子的商队'),(254,7,'还在此时留下','还在此地留下'),(254,9,'一步步渡过考验','一步步通过考验'),(254,13,'一只僵尸大军','一支僵尸大军'),(254,13,'直需一个','只需一个'),(254,24,'这只商队','这支商队'),(254,29,'这只商队','这支商队'),(254,47,'解读的蛊','解毒的蛊'),(254,67,'我如果墓碑山','我路过墓碑山'),(255,37,'吐沫星子','唾沫星子'),(255,53,'这只小队','这支小队'),(255,55,'勉力了一句','勉励了一句'),(255,60,'三只突围小队','三支突围小队'),(255,72,'在加上之前','再加上之前')]
fixes=[z for z in fixes if z[2]!=z[3]]
for c,p,a,b in fixes:assert a in src(c,p)['text'],(c,p,a)
v=pro(113,'located copy candidates',sorted(set((c,p) for c,p,a,b in fixes)),'Review and approve each substitution separately. Preserve original source and paragraph numbering; no global replacement.','Wrong characters, omitted words, classifiers and a few contextual wording candidates. The137 correction restores a missing十, not a change to the sum. The shrinkage wording does not decide whether the original describes loss or remaining population.','Mostly high local copy confidence; classifiers and contextual diction moderate.','Second-witness checks and full-novel hold. Do not turn246p36 into a different remaining fraction without evidence.')
v['copy_items']=[dict(chapter=c,paragraph=p,original=a,replacement=b,confidence='Moderate contextual/classifier candidate' if (c,p) in [(241,89),(243,48),(246,36),(246,61),(247,101),(250,9),(254,3),(254,7),(254,9),(254,13),(254,24),(254,29),(255,53),(255,60)] else 'High local copy candidate',status='Held; unapproved; unapplied') for c,p,a,b in fixes]
for v in ledger:
 if v['id']=='SR-104':v['batch012_update']='No resolution of the twins-version fork in241–255. Silence is not evidence choosing either version; no canonical decision made.'
 if v['id']=='SR-099':v['batch012_update']='241/245 show rapid RevolutionTwo middle/upper growth with Bai’s essence;250/251 show higher-quality stored essence usable in combat. BeforeRevolutionThree advantage supported; afterRevolutionThree benefit still unread.'
events=load('history/before-batch012-chronology-register.json')['entries'];resources=load('history/before-batch012-resource-register.json')['entries'];ne=[];nr=[]
def ev(timeline,kind,event,constraint,rr,status='Source evidence; provisional global reconciliation'):
 v=dict(id=f'CHR-{len(events)+1:03d}',timeline=timeline,kind=kind,event=event,constraint=constraint,evidence_status=status,dependency='Full sequential reading; preserve anchors, viewpoints and overlapping intervals',sources=ss(rr));events.append(v);ne.append(v)
def res(kind,entry,calculation,rr,status='Source evidence; no emendation applied'):
 v=dict(id=f'RES-{len(resources)+1:03d}',kind=kind,entry=entry,calculation=calculation,status=status,sources=ss(rr));resources.append(v);nr.append(v)
ev('Revised current life','travel and advancement','Monkey Mountain to Golden Mountain','Morethan20dayscrossing; departure-nightRevolutionTwo middle;Goldenarrivalfullcrocstrength. Interveningtravelnotdated.',[(241,64),(241,78),(241,79)])
ev('Revised current life','stay and trade','Jin village','Three-daywaitforinvestigation followedbytrade;grassboughtnightbeforedeparture.243前天candidateclarifies243明天/244昨晚.',[(242,52),(243,48),(243,64),(244,9)])
ev('Former-life memory / present age','age and history','Xin Ci and Jin forecast','XinCi16;FYnear100yearscommerce,then400plusmemoryspan approximate. Fouryeargrassmaturation;rememberedJinattackoneyearto come,notelapsednow.',[(243,28),(243,29),(243,39),(243,73),(243,74)])
ev('Revised current life','route intervals','Golden to Howling Moon','HalfmonthtoSoulWood,20plusdaystoGiantRain;SquareBrickandfourfurthervillages. Do not assignexactdurationtostops. FirstHowlingMoonnightRevolutionTwo upper.',[(245,2),(245,3),(245,9),(245,18),(245,94)])
ev('Revised current life','successive attacks','Howling Moon and White Tiger','Fewdayssecondwolf;3dayslaterlightning;>halfmonthrepeated. WhiteTigerattackseparated5+7+10days=22daysbetweenfirst/final listed attacks,notwholejourney.',[(246,4),(246,6),(246,9),(246,12),(246,23),(246,25),(246,27)])
ev('Revised current life','battle interval / death','Ivory Mountain massacre','Elephantattack>oneshichen(~2h). ZhangkilledbyFY;ChenXinsurvivesburied.100plussurvivorslatercounted137. 十不存一doesnotforceinitialexact1000.',[(248,21),(248,34),(248,38),(248,45),(248,46),(249,1)])
ev('Revised current life','onward interval','Ou deaths to Tombstone','7/8daysafterOu deaths;crocelephants;fewdaysleaveIvory;halfmonthattacks;fewmoreenterTombstone. Noexactcalendarassigned.',[(253,15),(253,69),(253,72),(253,73),(253,80)])
ev('Earlier current-life biography / former-life forecast','personal history','Ding Hao','8plusyears cultivation thennearly3yearsarmybuilding. About11yearstotalnot8. Futureloyaldeath255memorynotpresentdeath.',[(254,11),(254,15),(254,23),(255,5)])
ev('Revised current life','endpoint','Ding Hao called out','Finalbreakout8inclFY,5fall,3escape,FYkills2companions;at255endDinghasnotyetresponded. Baiinremainingcamp;caravanattackongoing.',[(255,68),(255,70),(255,76),(255,92),(255,93),(255,97)])
res('Strength / declined reward','Monkey contest','Domain-specificpower,notuniversalconversion.2winsdeliberate3rdloss.150rewardrefused,nocashreceipt;100/1000rhetoricalnotrewardmiscount.',[(241,9),(241,13),(241,19),(241,48),(241,52),(241,54),(241,57)])
res('Food and attrition','Bone Spears','Abouttwo-thirdsdead242;milkacquiredunknowncost. Do notinferexact67leftfrom200initial orcarryallSpiralGuasdead.',[(242,37),(242,38)])
res('Trade / accounting','Grass proceeds','Cost<500bartergoods,8000cashreceived,4000allocatedeach,FYshareheldXinCi. Profit>7500beforeothercosts;principalrepaymentnotfullyspecified.',[(244,45),(244,58),(244,63)])
res('Cargo versus value','Engineered losses','245~1000valuefirstnightloss;246lessthanhalfcargoquantity;247retainsmostvaluablegoodsoverhalftotalvalue. Differentdenominators,notcontradiction.',[(245,28),(245,92),(246,15),(247,15),(247,16)])
res('Population / categories','Caravan roster','24978knownGu+59apparentmortals=137. Ou2deaths=>135total;oldGuroll76. Withpairreclassifiedactual78Gu+57mortals,conditionalonoriginalinclusion. Actualranks12/28/38;publicmistakenranks13/27/38.',[(249,1),(249,5),(250,73),(251,113),(252,7)],'SR111 held scope clarification; complete-population reconstruction conditional')
res('Title / custody / allocation','Donated and reassigned goods','XinCidonatesloanedgoodswithoutpermission,offerssavingsFYdeclines. Laterleadersallocatecargoagain. Noexactnewvalueandnotrepeatedsame2boxesasadditionalmoney.',[(249,30),(249,71),(249,72),(249,74),(249,83),(252,68),(253,5),(253,6)])
res('Essence / rank / Gu','RevolutionTwo combat and RevolutionThree bluff','FYactualRevolutionTwo upper,storedBaisilver,Canopy/Spiral/Moon/JumpingGrassused. Finalsilverdisplaynotnativeessenceempty. Bai3peakactual;FY3peakpublicerror.',[(250,73),(250,74),(250,75),(250,99),(251,57),(251,59),(251,61),(251,116)])
res('Reconnaissance / contingency','Missing Ear and Jia Fu token','Earstilllost,noGu-recon;usesotherscoutstolocateDing. JiaFutokenbackupconsidered253,notactuallyshownoraccepted.',[(253,25),(253,31),(255,13),(255,60)])
res('Controlled army / rank comparisons','Ding’s zombies','Black~hundredking,50plusattacking;twoGreen~thousandkingatnight. Blue~ten-thousandking,noneownedconfirmed. 1000killrequirementseparatefromarmytierquotas.',[(254,13),(254,89),(254,90),(254,102),(255,85),(255,86)])
np=sum(len(c['paragraphs']) for c in batch);nc=sum(sum(map(len,c['paragraphs'])) for c in batch);tp=sum(len(c['paragraphs']) for c in cs);tc=sum(sum(map(len,c['paragraphs'])) for c in cs)
save('proposal-ledger.json',ledger);save('chronology-register.json',dict(scope='Sequential through255; separate biographies, forecasts, current intervals and conflicting witnesses',entries=events));save('resource-register.json',dict(scope='Sequential through255; roster categories, title/custody, gross/net and combat-quality distinctions',entries=resources))
progress=load('history/before-batch012-reading-progress.json');progress.update(sequential_chapters_completed=list(range(1,256)),paragraphs_read=tp,paragraph_characters_read=tc,next_chapter=256,remaining_chapters=2079,batch_report='Batch-012-Chapters-241-255.md',scope='Full sequential Chinese-source reading through255; no fresh bilingual/live-site audit',whole_novel_chronology_verified=False)
progress['batches'].append(dict(id='012',chapters=[241,255],paragraphs=np,characters=nc,reading_segments='Seven complete untruncated two-chapter outputs and complete255; adaptive15'))
progress['chapters'] += [dict(chapter=c['corpus_chapter'],file=c['file'],title=c['title'],paragraphs=len(c['paragraphs']),first_paragraph=1,last_paragraph=len(c['paragraphs'])) for c in batch];save('reading-progress.json',progress)
save('batch-012-reading-log.json',dict(status='Complete',endpoint=255,next_unread=256,segments=[dict(chapters=[a,a+1],status='Full paragraph sequences printed and read; untruncated',paragraphs=sum(len(by[n]['paragraphs']) for n in [a,a+1])) for a in range(241,255,2)]+[dict(chapters=[255],status='Complete untruncated chapter read',paragraphs=len(by[255]['paragraphs']))],note='Adaptive15, actualreading. Reader-facing250pp24–31/33/35–36 omissionmarkers preserve numbering; originalEPUB unchanged. No invented timestamps.'))
text=['# Numbered Chinese source: Chapters241–255','Original wording retained except explicit reader-facing omission markers250pp24–31,33,35–36 for sexualised descriptions of a minor character. Original EPUB unchanged; all original paragraphs read.']
for c in batch:text += [f"## Corpus chapter {c['corpus_chapter']}: {c['title']}",f"Volume: {c['volume']} | EPUB: {c['file']}"]+[f"{i}. {reader(c['corpus_chapter'],i,t)}" for i,t in enumerate(c['paragraphs'],1)]
(r/'Batch-012-Numbered-Chinese-Source.md').write_text('\n\n'.join(text))
for name,vs in [('Chronology',ne),('Resources',nr)]:
 out=[f'# Batch012 {name} jotter','All provisional. No source edits.']
 for v in vs:
  out += [f"## {v['id']}: {v.get('event',v.get('entry'))}",v.get('constraint',v.get('calculation')),v.get('evidence_status',v.get('status'))]
  for z in v['sources']:out += [f"Ch{z['chapter']} p{z['paragraph']}",'> '+reader(z['chapter'],z['paragraph'],z['text'])]
 (r/f'jotters/Batch-012-{name}.md').write_text('\n\n'.join(out))
out=['# Batch012 continuity and proposed corrections','All held, unapproved and unapplied.']
for v in new:
 out += [f"## {v['id']}: {v['category']}"]+[f"**{k}:** {v[k]}" for k in ['recommended_action','rationale','confidence','dependencies','status']]
 if 'copy_items' in v:
  for z in v['copy_items']:out += [f"### Ch{z['chapter']} p{z['paragraph']}: {z['original']} → {z['replacement']}",z['confidence'],'> '+reader(z['chapter'],z['paragraph'],src(z['chapter'],z['paragraph'])['text'])]
 else:
  for z in v['locations']:out += [f"Ch{z['chapter']} p{z['paragraph']}",'> '+reader(z['chapter'],z['paragraph'],src(z['chapter'],z['paragraph'])['text'])]
(r/'jotters/Batch-012-Continuity.md').write_text('\n\n'.join(out))
(r/'jotters/Batch-012-Preserve.md').write_text('''# Batch012 preservation cautions

-150rewardrefused;100/1000rhetoricalrefusalnotactualrewardamounts.
-Bear/boar/crocstrengthspecialisationsnotuniversalnumericalconversion. Ordinaryattackmentioningallcomponentsdoesnotprovefull100%aggregationcontradiction.
-CrocGuusecompleted241meansenhancementcomplete;notnecessarilyGuconsumedordestroyed.
-Two-thirdsBoneSpeardeadapproximation;don'tinventexact67remaining.
-Grass8000grossproceeds,cost<500,profit>7500beforeothercosts;principalunsettled. Donotdeductexact500orresplit7500automatically.
-Cargovolumeandcargo-value lossesdifferent;247revealsFYprotectedvaluableportion.
-137rosterpublicclassification;FYactualRevolution2despiteRevolution3peakbluff. Reclassifyingdoesnotcreatetwopeople.
-十不存一versus137notcontradictionwhenoriginalmerely1000plus.
-XinCi16, charityandjudgmentnotomniscience;herbeliefFYgoodisfalsePOV,notnarratorendorsement.
-GuMasterrolecoverandhiddenelderstorynotactualZhangclanappointments.
-Chenuncle'stheoryFYalreadyknewwitnessisconjecture;253clarifiesFYuncertain.
-JiaFu tokenplannedfallback,notshown. LostEarstilllost;FYusesotherscoutsnotnewGu.
-ZombieKing~centuryrevengebackstory,Ding8plus+3yearbiography,andfutureloyaldeathnotcurrentelapsedtime.
-8breakoutmembersincludeFY;5fallthenFYkillstwoleavesFYonly. CaravanNOTyetdestroyedby255.
-Twins-versionforkSR104unresolved;silenceinthisbatchselectsneitherversion.
''')
stand=load('history/before-batch012-working-standards-register.json');stand['coverage_through']=255
su={'WS-01':'XinCi’sbeliefFYbenevolent,publicRevolution3bluff,hiddeneldercover,andChenuncle’stheoryareviewpointsnotomniscientfacts.','WS-02':'Roster137=78+59,butrevealedidentitiesmustbereclassifiednotadded. Proceeds8000,cost<500,profit>7500;denominatorsdistinct.','WS-03':'FYRevolutionTwo middle241,upper245;storedsilvercombat250/251doesnotpromotehimtoRevolutionThree. SR099held.','WS-04':'CompletedCrocstrengthdoesnotbyitselfmeandestroyedGu. Donatedloanedgoods,reallocatedcargo,andcustodyofcashseparate.','WS-05':'TwentyplusMonkeydays;HowlingMoonandWhiteTigerintervals;Ding8plus+nearly3years. Forecastsnotelapsedtime.','WS-06':'2/3BoneSpearsstarvedapproximate;valueandvolumeoflostcargoaredifferent;declined150notincome.','WS-07':'Strengthspecieshavedifferentdomains;noone-dimensionalbeaststrengthconversion. Routewaypointforecastsnotexhaustivemountainlists.','WS-08':'XinCiexplicit16. Chenleadername双金/双全heldSR110;noinventedseconduncleorleader.','WS-09':'Locatedcopycandidates;reader250omissionsmarked.246shrinkagewordingnotlicensetochangeproportion.','WS-10':'Actualcoverage255/2334;2079remain. Noauthorised/appliedsourceedits;backupunresolved.','WS-11':'Agreedmaximunchanged: Man is the most intelligent of all living things. No new manuscript implementation approval.'}
for v in stand['entries']:v['batch012_update']=su[v['id']]
save('working-standards-register.json',stand)
out=['# Working editorial standards','## Evidence checkpoint: Chapters1–255','Working rules are not whole-novel certification or manuscript approval.']
for v in stand['entries']:out += [f"## {v['id']}: {v['topic']}"]+[f"**{k}:** {v[k]}" for k in ['status','rule','evidence','reopen','batch012_update']]
(r/'WORKING-STANDARDS.md').write_text('\n\n'.join(out))
def quote(c,p):return f"**Ch{c} p{p}:**\n\n> {reader(c,p,src(c,p)['text'])}"
report=f'''# Sequential close-reading review: Chapters 241–255
## Batch 012 | The Omniarch

**Actual sequential coverage: 1–255 of 2,334. Next unread: 256. Remaining: 2,079.**

This adaptive fifteen-chapter batch was fully read in seven complete, untruncated pairs and one complete final chapter: **{np:,} paragraphs / {nc:,} source characters**. Cumulative coverage: **{tp:,} paragraphs / {tc:,} characters**. The shorter batch accommodates the caravan’s changing population, property arrangements, concealed identities and multiple travel intervals. Extraction alone is not counted as reading.

The ledger now contains **113 records: 112 active and held, one withdrawn**. Four records are new, including **{len(fixes)} individually located copy candidates**. All emendations remain unapproved and unapplied. This is Chinese-source review, not fresh bilingual or live-site verification.

## 1. A deputy leader changes names

{quote(247,37)}

{quote(252,75)}

The Chen leader is 陈双金 in247 and249, then 陈双全 repeatedly in252 and255. The same office and connection to Chen Xin continue; no new deputy or replacement is introduced.

**SR-110:** provisional preference for 陈双全, supported by the repeated later uses, with earlier 陈双金 locations flagged for possible normalization. Confidence is high that the witness is inconsistent, but only moderate about which name should prevail. Later sequential evidence and an independent witness may reverse this preference, just as224 reversed our earlier inheritance-title preference. We should not solve this by inventing two people.

## 2. Population totals: subtraction is correct, classification is not explicit

{quote(249,1)}

The missing 十 in 一百三七 is a straightforward copy candidate: **137 = 78 + 59**. The detailed Gu-Master roll also checks out:

{quote(249,5)}

**12 RevolutionThree + 28 RevolutionTwo + 38 RevolutionOne = 78.** At this point, Fang Yuan and Bai Ning Bing are publicly treated as ordinary workers.

After the two Ou deaths and the pair’s reveal:

{quote(252,7)}

The two deaths correctly subtract one RevolutionThree and one RevolutionTwo: **11 + 27 + 38 = 76**. The issue is that this retains the old registered Gu-Master population without expressly excluding the newly revealed pair.

| Counting scope after the two deaths | RevolutionThree | RevolutionTwo | RevolutionOne | Gu-Master total |
|---|---:|---:|---:|---:|
|Old registered roster, excluding Fang/Bai|11|27|38|76|
|Actual ranks, including Fang/Bai|12|28|38|78|
|Public belief that both are RevolutionThree peak|13|27|38|78|

The complete-population reconstruction assumes the pair were included among249’s59 apparent mortals: initial actual population would then be80 Gu Masters plus57 ordinary people. After the Ou deaths, it becomes78 plus57, totalling135. **Reclassification does not add two new people to the caravan.**

**SR-111 preferred repair:** qualify252p7 with **不计方白二人**, preserving its existing11/27/38 subtotal. If the author intended a complete actual-rank roll,12/28/38 is the alternative. A mechanical11→13 change would incorrectly promote Fang Yuan according to the public’s mistaken belief.

The earlier phrase 十不存一 is not yet a proved conflict with137 survivors. The original caravan was described as over a thousand, not exactly1,000. An original total above1,370 could satisfy both descriptions.

## 3. Gold-grass trade: do not confuse proceeds with profit

{quote(244,58)}

{quote(244,63)}

The transaction is:

| Item | Supported amount |
|---|---:|
|Barter goods exchanged for the grass|Less than500 stones in value|
|Cash sale proceeds|8,000 stones|
|Profit before other costs|Greater than7,500 stones|
|Stated allocation to each party|4,000 stones|
|Fang Yuan’s allocated portion|Left in Shang Xin Ci’s custody|

The offers of3,000,5,000 and7,000 are rejected negotiating positions, not separate receipts. The desired10,000 is not received. Fang Yuan deliberately buys most of the grass, not all of it, leaving other buyers involved.

**SR-112:** consider clarifying 收益 as **售款**, sale proceeds, at244p58. This is an accounting and translation-precision proposal, not a certified numerical error. The earlier loan and sharing agreement does not fully state how the original capital is repaid. We must not silently deduct exactly500, change the proceeds to7,500, or invent3,750-stone shares.

The subsequent donation is also explicit about ownership: Shang Xin Ci gives away the loaned cargo without Fang Yuan’s permission and apologises for doing so. Her offer of savings is declined. Later the caravan leaders allocate cargo back to her for political reasons. These are different transactions, not continuous undisturbed possession of the same goods.

## 4. Cultivation and combat: Fang Yuan remains RevolutionTwo

| Checkpoint | Confirmed state |
|---|---|
|241, departure from Bandit Monkey Mountain|RevolutionTwo middle stage|
|241, arrival at Golden Mountain|Full crocodile-strength enhancement completed|
|245, first night in Howling Moon territory|RevolutionTwo upper stage|
|250–251, Ou fights|RevolutionTwo upper using stored snow-silver essence|
|251, intimidation display|Public mistakes him for RevolutionThree peak|
|255, endpoint|No further promotion narrated|

{quote(250,73)}

{quote(250,75)}

The essence is stronger than his native cultivation grade. That does not make his aperture RevolutionThree. Chapter251’s last displayed trace of silver is the last of that reserve, not necessarily the last of all his native essence.

His RevolutionTwo aperture can store a reserve. Earlier RevolutionOne assisted use does not automatically contradict this: immediately controlled transfer during cultivation and retaining a combat reserve are different conditions.

The two-stage separation between RevolutionTwo upper and RevolutionThree initial is also sensible: upper → peak → the next rank’s initial stage. There is no need to “correct”251’s one minor-stage plus one major-rank description.

This batch strengthens SR-099’s evidence for accelerated cultivation **before RevolutionThree**, but still does not establish that benefits **after RevolutionThree** are impossible. That proposal remains conditional.

## 5. Physical strength does not form a universal conversion table

{quote(241,13)}

Chapter241 explicitly distinguishes both the amount of strength and the action in which it is best expressed. Arm-wrestling does not necessarily draw the complete sum of every permanent enhancement. This prevents a simplistic inference that a turtle, bear, boar and crocodile can always be assigned fixed interchangeable combat values.

Later descriptions of Fang Yuan’s boar and crocodile strength erupting together are not precise statements that100% of every enhancement has been concentrated into one action. They do not by themselves prove he secretly acquired the legendary Gu mentioned in241. Keep that possible future mechanical distinction open rather than supplying an unacquired Gu.

Other resource cautions:

- The150-stone reward is offered and refused. His rhetorical refusal of100 or even1,000 does not redefine the actual offer.
- Completion of Crocodile Strength Gu’s bodily enhancement does not by itself prove that the Gu is consumed or destroyed.
- Chapter242 says roughly two-thirds of the Bone Spear Gu have starved. Starting from200 does not justify an exact remaining inventory of67.
- Lost cargo quantity and lost cargo value have different denominators.247 reveals that Fang Yuan preserved the most valuable goods despite large apparent losses.
- Ear Grass remains lost. Fang Yuan uses other people’s scouts to locate Ding Hao; he has not acquired a new personal reconnaissance Gu.
- The Jia Fu token is a contemplated fallback, not something he actually displays or has accepted in this batch.

## 6. Chronology: preserve the travel intervals without inventing dates

| Sequence | Explicit constraint |
|---|---|
|Bandit Monkey crossing|More than20 days|
|Golden Mountain waiting|Three days waiting for an investigation that does not come|
|Grass transaction|Night before departure, sold the following morning|
|Golden → Soul Wood|Half a month|
|Onward → Giant Rain|Over20 days; retain the narrative anchor rather than impose a calendar date|
|Square Brick and four further villages|Stops mentioned without complete durations|
|Howling Moon attacks|First night; another after a few days; lightning wolves three days later; repeated attacks over a further half-month-plus|
|White Tiger sequence|Five days, then seven, then ten between the listed attacks:22 days between first and last, not the whole journey|
|White-feathered elephant attack|Over one 时辰, approximately two conventional hours|
|After the Ou deaths|Seven or eight days before the next described scene|
|Toward Tombstone Mountain|Further days, a half-month of attacks, then more days before entry|
|Ding Hao’s biography|Over eight years’ cultivation, then nearly three more years building the army|

Ding Hao’s roughly eleven-year personal history is not an eight-year total, and his remembered future death is not a present event. The old Zombie King’s long revenge history is another separate clock.

## 7. False beliefs, concealment and characterisation

The caravan’s apparently extraordinary bad luck is explained: Fang Yuan has been attracting the attacks. This is a delayed revelation, not an unexplained ecological contradiction.

Shang Xin Ci is explicitly **sixteen** in243. Her perceptiveness is real, but her favourable judgment of Fang Yuan is based on incomplete and manipulated evidence. Passages describing her belief that the pair are good people are her viewpoint, not an omniscient moral certification. The text can credit her intelligence while showing her deceived.

Likewise:

- The “hidden Zhang elders” explanation is a cover story, not an actual appointment.
- Jia Long’s public praise of the killings is political reframing, not evidence that he secretly commissioned them.
- Chen Xin’s uncle speculates that Fang Yuan may already know about the witness.253 instead shows Fang Yuan uncertain. A character’s guess is not a narrator contradiction.
- Zhang Zhu’s death is explicit. Chen Xin survives through his own burial Gu, and the lack of reconnaissance helps explain why Fang Yuan misses him.

The twins’ incompatible fate-versions from Batch011 remain unresolved. **Silence about them here chooses neither version.**

## 8. Proposals and copy candidates

| Record | Action | Confidence and dependency |
|---|---|---|
|SR-110|Resolve 陈双金 / 陈双全|High variation; preferred form awaits later and independent evidence|
|SR-111|Clarify roster excludes Fang/Bai, or reclassify explicitly|High scope issue; initial inclusion assumption must remain visible|
|SR-112|Distinguish sale proceeds from profit|Arithmetic secure; principal and sharing basis unresolved|
|SR-113|{len(fixes)} individually located copy candidates|Mostly high; classifiers/contextual wording separately qualified|

Every record includes action, rationale, dependencies, confidence and held status. The continuity jotter includes exact source paragraphs.

| Location | Source fragment | Held candidate |
|---|---|---|
'''
report+='\n'.join(f'|{c} p{p}|{a}|{b}|' for c,p,a,b in fixes)
report+=f'''

## 9. Exact endpoint and saved checkpoint

In255, the final breakout team contains **eight people including Fang Yuan**. Five fall, three escape, then Fang Yuan kills his two remaining companions. He is the sole survivor of that particular team. That is not eight people plus Fang Yuan.

At the chapter’s final line he calls for Ding Hao to come out. Ding Hao has not yet responded. Bai remains with the camp, and the caravan’s destruction is a plan, **not an accomplished event at this reading endpoint**.

Saved: this report, numbered Chinese source, five jotter files, eight-segment reading log, **113 proposal records, {len(events)} chronology entries, {len(resources)} resource entries**, the cumulative workbook and11 working standards. Reader-facing250pp24–31/33/35–36 have explicit omission markers for sexualised descriptions of a minor character; original paragraph numbering and the EPUB are unchanged, and all original paragraphs were read.

The agreed maxim remains **“Man is the most intelligent of all living things.”** No manuscript implementation approval is inferred.

**Next unread:256.** No original-source, manuscript, site or repository edits, uploads or deletions occurred. Remote backup remains unresolved. Whole-novel consistency is not certified.
'''
(r/'Batch-012-Chapters-241-255.md').write_text(report)
old=(r/'update_batch010.py').read_text();wb=old[old.index('# Workbook: cumulative'):old.index("(r/'CURRENT-STATUS.md').write_text")]
wb=wb.replace('1–220 of2334','1–255 of2334').replace("('Next unread',221)","('Next unread',256)").replace('103total;102activeheld;1withdrawn','113total;112activeheld;1withdrawn').replace('range(10,0,-1)','range(12,0,-1)').replace("v['batch010_update']","v['batch012_update']").replace('Batch-010-Chapters-201-220','Batch-012-Chapters-241-255').replace('CHAPTERS201–220','CHAPTERS241–255').replace('Chapters201–220','Chapters241–255').replace('Twenty complete chapters; personal clocks and inventory scope distinguished','Fifteen complete chapters; roster categories, trade accounts and concealed identities').replace('Ch151,201p22,203p84 restricted excerpts','Ch151,201p22,203p84,250pp24–31/33/35–36 restricted excerpts')
exec(compile(wb,'workbook-and-docx','exec'))
(r/'CURRENT-STATUS.md').write_text(f'''# Sequential review checkpoint

Fully read **1–255 of2334**. Next unread **256**. Remaining **2079**. Next adaptive batch256onward,15–20ifdense.

Batch01215chapters: {np}paragraphs/{nc}characters. Cumulative{tp}/{tc}.113proposals:112activeheld,SR047withdrawn.4newSR110–113,SR113has{len(fixes)}copyitems. {len(events)}chronology/{len(resources)}resources,11workingstandards. Allapproved/appliedfalse,whole-novelcertificationfalse. Pre012archivespreserved.

Latest Batch-012-Chapters-241-255.md/.docx; numberedsource;5jotters;8segmentlog;registers;workbook. Main detailedhandoff jotters/batch-012-working.md.

Carryforward:
-SR110Chenleader陈双金247/249vs陈双全252/255sameoffice/nephewChenXin;preferlater双全conditionalnotsettled. Noinventsecondleader.
-SR111249137=78registeredGu+59apparentmortals,12/28/38ranks.252Oufather3initial/son2initialdeaths=>oldregistered11/27/38=76 excludesFY/Bai. Preferredclarify不计方白二人. ActualincludingFY2upper/Bai3peak=>12/28/38=78Gu;publicfalseboth3peak=>13/27/38. Ifpairamong59initialmortals,actualtotalafter2deaths135=78Gu+57mortals. Do notadd2people. 十不存一notconflict137whenoriginal>1000notexact1000.
-SR1128000grassgrosscash,<500bartercost=>profit>7500beforecosts;explicit4000/4000,FYshareheldXinCi. Principalrepayunclear,noexact7500or3750edits. Candidate收益→售款.243majoritygrassnotall,3cartsnotnecessarilyall3mu. Declined150rewardnotincome. Subsequentdonationloanedgoodsacknowledged;FYdeclinesnewcash;leadersreallocatecargo,noexactvalue.
-24120plusdaysMonkeycrossingFY2middledeparture;GoldenarrivalfullCrocstrengthnotnecessarilyGuconsumed.2452upperfirstHowlingMoonnight,250/251silverreservecombatnotFYRevolution3. Lastsilvertracebluffnotallnativeessencezero. SR099before3strongerafter3unknown.
-Strengthspeciesdifferentdomains241,notuniversalbear/boar/crocconversion. Laterpowerburstnotexplicit100percentallcomponentproofcontradiction.
-2422/3BoneSpeardeadapprox;noexact67. Cargoquantity246<halfvs247valuable>halfkeptdifferentdenominator. EarGrassstilllost253/255,noreconGu,reasons/scoutslocateDing. JiaFutokenonlycontingency253notshown.
-Time245halfmonthSoulWood,20plusGiantRain,SquareBrick+4villages;246fewdayswolf/3dayslightning/>halfmonthattacks;WhiteTiger5+7+10=22daysbetweenfirst/finalattacksnotwholetotal.247severaldaysIvorythenfewdaysinside;248elephants>1shichen≈2h.2537/8daysafterOu,thenfewdays+halfmonth+fewdaysTombstoneentry. Ding8plusyears+nearly3more≈11not8total;1000killrequirementseparatearmycomposition.
-XinCi16explicit243. FYengineersattacks,hergoodmanbeliefPOVnotfact;concealedelderscovernotrealappointments. ZhangZhukilled248;ChenXinsurvivesburied,uncletheoryFYknewnotfact253uncertainty. JiaPingdeadreported247.
-255endpoint:8inclFYbreakout,5fall,3escape,FYkills2companions=>FYalone;Ding2Green~1000kingnight;50plusBlack~100king. DingnotyetrespondedtoFYcall. Baiguardscamp,XinCi/XiaoDiestillalive,caravanattackongoingNOTfinishedextermination.
-SR104twinsversionforkunchanged:226/228/233deadvs231missing,futuremeeting. Compilerclaimsunauthenticated. Noresolutionbysilence. SR098reversedpreviousbatch肉骨上师correctcandidate21445骨肉→肉骨;preserve224evidence. SR106caravanday7+3vs9stillheld;SR107BaisweatvsIceMuscleheld,246generalslavesweatnotexplicitBai. Olderholdscontinue.
-WS11agreedmaximunchanged 'Man is the most intelligent of all living things.' Noimplementationapproval.

No originalsource/site/repo edits,uploads,deletions. Backupunresolved. Reader250sexualisedminor-descriptionomissionsmarked;originalEPUBunchanged. Do notrerunoldergeneratorsafter012.012idempotentfrompre012.
''')
assert len(cs)==255 and len(ledger)==113 and len(new)==4
assert tp==20908+np and tc==737306+nc
assert all(not v['approved'] and not v['applied'] for v in ledger)
assert all(z['text']==src(z['chapter'],z['paragraph'])['text'] for v in events+resources for z in v['sources'])
assert len({v['id'] for v in events})==len(events) and len({v['id'] for v in resources})==len(resources)
texts={t for c in cs for t in c['paragraphs']}
for line in report.splitlines():
 if line.startswith('> '):assert line[2:] in texts
print('QA PASSED',dict(chapters=255,new_paragraphs=np,new_characters=nc,paragraphs=tp,characters=tc,proposals=len(ledger),copy_items=len(fixes),chronology=len(events),resources=len(resources),next=256))
