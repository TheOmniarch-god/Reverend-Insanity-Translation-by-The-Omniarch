from pathlib import Path
import json,shutil
from openpyxl import Workbook
from openpyxl.styles import Font,PatternFill,Alignment
r=Path('/home/user/editorial/sequential-review')
def load(n):return json.loads((r/n).read_text())
def save(n,v):(r/n).write_text(json.dumps(v,ensure_ascii=False,indent=2))
for n in ['reading-progress.json','proposal-ledger.json','chronology-register.json','resource-register.json','working-standards-register.json']:
 d=r/'history'/('before-batch013-'+n)
 if not d.exists():shutil.copy2(r/n,d)
cs=sum([load(f'batch-{i:03d}-source.json') for i in range(1,14)],[]);by={c['corpus_chapter']:c for c in cs};batch=cs[255:270]
def src(c,p):return dict(chapter=c,paragraph=p,file=by[c]['file'],text=by[c]['paragraphs'][p-1])
def ss(rr):return [src(*z) for z in rr]
def loc(rr):return [{k:v for k,v in z.items() if k!='text'} for z in ss(rr)]
def refs(z):return '; '.join(f"Ch{x['chapter']} p{x['paragraph']}" for x in z)
def find(c,term):
 hits=[i for i,t in enumerate(by[c]['paragraphs'],1) if term in t];assert len(hits)==1,(c,term,hits);return(c,hits[0])
def reader(c,p,t):
 if (c==258 and (70<=p<=74 or p==79)) or (c==250 and (24<=p<=31 or p in [33,35,36])) or (c==151 and (31<=p<=67 or p in [98,99])) or (c,p) in [(201,22),(203,84)]:return '[Restricted passage omitted from reader-facing copy. Original numbering retained; original EPUB unchanged.]'
 return t
ledger=load('history/before-batch013-proposal-ledger.json');new=[]
def pro(i,cat,rr,action,why,conf,dep):
 v=dict(id=f'SR-{i:03d}',category=cat,locations=loc(rr),recommended_action=action,rationale=why,confidence=conf,status='Active provisional proposal; no approval',dependencies=dep,approved=False,applied=False,publication_status='HOLD: full 2334-chapter reading and global reconciliation outstanding');ledger.append(v);new.append(v);return v
pro(114,'Ding Hao’s Green Zombie count',[(255,85),(255,86),(256,54),(257,98)],'Preferred255p86 replace 丁浩这么多年来，也就攒了这么两具 with 丁浩这次随身带来的青毛僵尸，也就这么两具. Preserve three total in256, one guarding the cave and two deployed.','255 describes only two accumulated over the years;256 explicitly says three owned, one at home. The later destruction concerns one of the two deployed, not all holdings.','High scope inconsistency; strong two-deployed clarification.','Independent witness and later army references. Do not turn the cave guard into a fourth zombie or subtract the same combat loss twice.')
pro(115,'Ding Hao’s elapsed years',[(254,11),(254,23),(256,54),(256,64),(257,124)],'If 近十年 means less than ten rather than loosely around a decade, prefer 十来年 in256p54/p64 and257p124. Do not replace the biography with an exact eleven years.','Over eight years of cultivation followed by nearly three more years of army-building approaches/exceeds eleven, whereas repeated near-ten wording is narrower under a strict reading. Approximate colloquial usage may explain it.','Moderate numerical wording query, not a certified chronological contradiction.','Meaning of 近 in context, approximate source intervals, independent versions and later explicit dates.')
pro(116,'restaurant floor and discount',[(259,101),(259,102),(260,2),(260,44)],'Preferred260p2 三层→四层;260p44 半折→五折, or English half price. Preserve the fifteen-stone payment.','259 assigns RevolutionThree guests to floor four at50% price and explicitly selects that floor.260 calls it floor three and half a 折, literally5% price rather than50%.','High two local inconsistencies; no need to alter the paid amount.','Source collation. A thirty-stone undiscounted bill is inferred only under the intended50% rate, not independently itemised.')
pro(117,'arena dimensions and movement distance',[(265,60),(266,23),(266,54)],'Conditional preference266p54 近六百米→近百米 if 方圆三十丈 specifies the arena’s roughly hundred-metre span. Conservative alternative: remove the exact metre clause pending collation, retaining the rapid movement from side to side. Do not automatically substitute sixty metres: the eighteen-zhang leap is a different move.','Thirty zhang at the conventional scale is about100m, and an eighteen-zhang leap is said to cross more than half the arena. A later side-to-side600m movement clashes with that local staging. This is not evidence that fantasy geography generally needs reduction.','High local spatial tension; moderate repair direction because 方圆 is imprecise.','Source variants, arena shape, unit convention and whether the later figure describes traversed path rather than direct extent. Keep timing and geometry separate.')
pro(118,'clan-specific junior-lord and heir titles',[(235,93),(262,65),(262,76),(263,52),(263,75),(267,60),(269,72)],'Prefer262p65 保住少族长的位置→保住少主的位置, and263p75 两个少族长→两个少主. Separately hold269p72 少主 as a lower-confidence title query: 族长 is a plausible intended future office, but do not apply it without later evidence.','Ya Zi is competing to retain one of ten junior-lord offices, while Tuo Hai is the designated heir. The Bai twins are earlier called junior lords. Chao Feng’s former-life almost-junior-lord statement is suspicious beside his present office, but different timelines prevent a categorical repair.','High first two title candidates; low-to-moderate former-life Chao Feng query.','Clan-specific rules, former versus revised histories and independent witnesses. Do not call all clan-leader children designated heirs or assume Shang’s ten offices apply to every clan.')
pro(119,'outstanding payment: thirty versus fifty thousand',[(268,26),(268,58),(268,72),(268,75),(268,85),(268,89)],'Preferred268p75 剩下的五万块元石→剩下的三万块元石. Preserve900000 total and870000 first instalment.','900000−870000=30000; thirty thousand is repeated before and after the isolated fifty-thousand line, including the actual final payment.','Very high local arithmetic and repeated-attestation support.','Check another witness and any omitted additional transaction before implementation. The6600 storage-Gu purchase is explicitly separate, not a netting adjustment.')
pro(120,'public price and private-funds basis',[(267,77),(268,23),(268,58),(268,59),(268,73),(268,94)],'Retain the final900000 cash price and934020 net transaction gain. Hold the change from a proposed650000 public price to600000 clan funds, and the400000-plus savings versus270000 near-entire assets, for documentary clarification. If later evidence fixes650000 as the final public price,600000/270000 would become650000/220000; do not apply that linked alternative now.','The final oath’s wording is not reproduced, so its public-price basis could have been renegotiated. Personal savings may have had unreported outflows. Both are scope/accounting queries, unlike the demonstrable thirty/fifty-thousand error.','High location of changes; low confidence in a specific numerical emendation.','Final contractual text, intervening expenditure and independent witnesses. Do not invent an expenditure to reconcile the savings or rewrite an unquoted contract.')
pro(121,'negotiation two-day/three-day wording',[(267,37),(268,7),(268,17)],'If the narrator’s two-day interval and Fang Yuan’s elapsed-time statement share one exclusive anchor, prefer268p17 已经过去两天了. Less precise candidate: 这几天价格自然要涨的. Retain the source pending inclusive-count and dialogue checks.','The narrator says two days later; Fang Yuan says three days have passed. Inclusive day numbering, a different quote anchor or deliberate bargaining rhetoric could explain the difference.','Moderate tension; low-to-moderate replacement confidence.','Do not convert character bargaining language into an exact narrator clock without establishing its anchor.')
fixes=[(256,4,'漏出马脚','露出马脚'),(256,6,'楞了一楞','愣了一愣'),(256,43,'楞了一下','愣了一下'),(256,61,'然而你得碰运气','然后你得碰运气'),(256,61,'这尸体身前','这尸体生前'),(257,13,'我们往退后','我们往后退'),(257,126,'头昏脑涨','头昏脑胀'),(257,143,'化为交谈','化为焦炭'),(257,147,'带着身上','带在身上'),(258,4,'一颗枯树','一棵枯树'),(258,6,'半柱香','半炷香'),(258,22,'已经渡过','已经度过'),(258,61,'没有理睬他','没有理睬她'),(258,63,'再搞清楚真相','在搞清楚真相'),(258,69,'在和商心慈相见','再和商心慈相见'),(259,3,'传入耳帘','传入耳中'),(259,8,'没有这些目光放在心上','没有把这些目光放在心上'),(259,60,'压入监牢','押入监牢'),(259,62,'白家寨发布','百家寨发布'),(259,90,'捐客','掮客'),(259,103,'出显真元','显露真元'),(260,15,'寰转','回转'),(260,20,'碎石因为','虽是因为'),(260,64,'温纯平和','温驯平和'),(261,17,'把手的蛊师','把守的蛊师'),(261,26,'分外五区','分为五区'),(261,36,'采光在不用','采光再不用'),(261,54,'勾引了泉水','引来了泉水'),(261,72,'笔力刚虬','笔力遒劲'),(261,82,'纺棰','纺锤'),(261,106,'只看了地一眼','只看了一眼'),(261,111,'一族蛊虫','一转蛊虫'),(262,27,'让他老者察觉','让老者察觉'),(262,64,'亢奋阴鸠','亢奋阴鸷'),(262,84,'商心慈闻言不语','商燕飞闻言不语'),(263,18,'好好修行','好好休息'),(263,19,'商燕飞看得出商燕飞','商燕飞看得出商心慈'),(263,46,'他们俩个','他们两个'),(263,75,'有一只铁家队伍','有一支铁家队伍'),(264,2,'他可以压价','他刻意压价'),(264,8,'真正的权利来源','真正的权力来源'),(264,11,'忽然将被父亲','忽然间被父亲'),(264,71,'感观','观感'),(264,84,'不能打到','不能达到'),(265,18,'教白凝冰','叫白凝冰'),(265,32,'还有谢谢','还要谢谢'),(265,66,'家老的权利','家老的权力'),(266,9,'没有接收过','没有接受过'),(266,34,'在使用光虹蛊就难了','再使用光虹蛊就难了'),(266,49,'先一步看中','先一步砍中'),(266,51,'就要集中他的胸膛','就要击中他的胸膛'),(266,57,'不过硬抗','不敢硬抗'),(266,69,'不由顾及太多','不用顾及太多'),(267,32,'脱胎骨','脱胎蛊'),(267,40,'六十五元石','六十五万元石'),(267,76,'你的打的好算盘','你打的好算盘'),(267,79,'轻佻眉头','轻挑眉头'),(267,81,'低谷了','低估了'),(268,52,'水晶所致','水晶所制'),(268,54,'白发垂髫','白发垂髻'),(269,25,'居然做的位置','居然坐的位置'),(269,32,'少主有理','少主有礼'),(269,36,'代练司','代炼司'),(269,66,'就杯中酒','将杯中酒'),(269,70,'二人贵客','二位贵客'),(269,72,'好斗狠争胜','好勇斗狠，争强好胜'),(269,81,'但比力气','单比力气'),(270,6,'你们俩个','你们两个'),(270,37,'不甚唏嘘','不胜唏嘘'),(270,41,'一楞','一愣'),(270,70,'惨烈的斗志','惨烈的斗争'),(270,77,'小兰、小蝶','小蓝、小蝶'),(270,87,'反映过来','反应过来')]
# Hair arrangement is not specified: prefer deleting the erroneous child-hairstyle term rather than inventing a bun.
fixes=[(c,p,a,'白发垂落' if (c,p)==(268,54) else b) for c,p,a,b in fixes]
for c,p,a,b in fixes:assert a in src(c,p)['text'],(c,p,a)
v=pro(122,'located copy candidates',sorted(set((c,p) for c,p,a,b in fixes)),'Review each substitution individually. Bigger number, title and staging issues have separate records. Local pronouns are scene-specific, not a global identity policy.','Wrong characters, missing words, names, measure-word usage and contextual phrasing. Some diction and nickname candidates require witness confirmation.','Mostly high local confidence; contextual replacements remain moderate.','Full-novel hold; source collation; do not mechanically replace every 白/百, name, pronoun or unit.')
moderate={(258,22),(258,61),(259,3),(259,103),(260,15),(260,64),(261,54),(261,72),(263,18),(264,11),(265,18),(268,54),(269,72),(270,77)}
v['copy_items']=[dict(chapter=c,paragraph=p,original=a,replacement=b,confidence='Moderate contextual candidate' if (c,p) in moderate else 'High local copy candidate',status='Held; unapproved; unapplied') for c,p,a,b in fixes]
for v in ledger:
 if v['id']=='SR-104':
  v['locations']+=loc([(263,75),(270,53)]);v['batch013_update']='263 repeats deaths as rumour;270 repeats them in the investigation account. More death-branch evidence does not authenticate compiler claims or reconcile231 disappearance. Edition-level hold continues.'
 if v['id']=='SR-110':
  v['locations']+=loc([(257,83)]);v['batch013_update']='257p83 again uses陈双全, explicitly reporting his andChenXin’sdeaths. Strengthenspreferred双全, not implementation approval.'
 if v['id']=='SR-099':v['batch013_update']='258FangreachesRevolutionTwopeak;260RevolutionThreepromiseboundarystillfuture. BeforeRevolutionThreeadvantagefurtherconfirmed, afterRevolutionThreebenefitnotyetread.'
events=load('history/before-batch013-chronology-register.json')['entries'];resources=load('history/before-batch013-resource-register.json')['entries'];ne=[];nr=[]
def ev(timeline,kind,event,constraint,rr,status='Source evidence; provisional global reconciliation'):
 v=dict(id=f'CHR-{len(events)+1:03d}',timeline=timeline,kind=kind,event=event,constraint=constraint,evidence_status=status,dependency='Full sequential reading; preserve anchors, viewpoint and version status',sources=ss(rr));events.append(v);ne.append(v)
def res(kind,entry,calculation,rr,status='Source evidence; no emendation applied'):
 v=dict(id=f'RES-{len(resources)+1:03d}',kind=kind,entry=entry,calculation=calculation,status=status,sources=ss(rr));resources.append(v);nr.append(v)
ev('Revised current life','battle completion','Caravan and Ding deaths','After>1shichenrenewedattack,4escape;last3caravanmemberskilled;Dingreportsnoneescaped,thenFYkillsDing. No longer merely a futureplan.',[(257,3),(257,83),(257,109),(257,110),(257,134),(257,151)])
ev('Revised-life future narration','prolepsis','Xin Ci remembers this night','Years-laterreflection25773–75 is narrativeflashforward, not currenttimejump orFYformer-life recall.',[(257,73),(257,74),(257,75)])
ev('Ding’s earlier biography','approximate interval','Near ten versus8plus+nearly3','Near-decade wording may be approximate; SR115held, noexact11calendarassertion.',[(254,11),(254,23),(256,54),(256,64),(257,124)])
ev('Revised current life','travel / cultivation','Arrival at Shang','TwinGenerals→BloodTears→6moremountains, briefvillagestops. FYRevolutionTwopeak25824;fulljourneydurationunstated.',[(258,17),(258,20),(258,23),(258,24),(258,25),(258,27)])
ev('Former life / revised comparison','investigation and historical encounter','Distinct histories','Former-life merchantsdetained/compensatedtwice258notcurrentreceipt. YiTianbanquet269rememberedfewyearslater;thislifeearlyencounter.',[(258,62),(258,63),(269,57),(269,58),(269,60)])
ev('Revised current life / older intelligence','dated report','Qing Mao information','267callsQingMao intelligence overhalfyearold. Supportsmonths-longtravel, not an exactnewyear/calendar date.',[(267,3),(267,4),(267,6)])
ev('Revised current life','city intervals','Investigation, waiting and tours','Three-dayTianLanreport andthree-daylodgingparallel. Audiencewait3shichen≈6h,meal>2shichen≈4h; nextdaytour,third-daytour+duel.',[(263,45),(263,49),(264,50),(264,85),(264,90),(265,1),(265,21)])
ev('Revised current life / bargaining dialogue','contract intervals','Negotiation to family banquet','Three-dayjump267;two-dayreturn268narratorvsdialoguethreedays(SR121);then3daybalanceandanother3daybanquetinvitation. Do not double-count overlapping anchors.',[(267,37),(268,7),(268,17),(268,89),(268,100),(268,101)])
ev('Conflicting textual witness','new death-branch evidence','Twins again reported dead','263rumour/270investigationsupportdeathaccount;231missingversionnotresolved.',[(263,75),(270,53)],'SR104 edition-level hold remains')
res('Army holdings / deployment','Ding’s zombies','3Green=2deployed+1home;onefieldGreendestroyed.120plusBlack/~4000White approximate reporting checkpoint;FY2Blueclaimfabricated.',[(255,86),(256,54),(256,56),(257,98)])
res('Loot / storage / deliberate destruction','Ding assets','~13000stonesreceivedandpackedTushita,within30000absolute/15000workinglimit. NoZombieHeartacquisition:allDingGuburned.',[(161,82),(257,118),(257,143),(257,147)])
res('Healing / activation','Clear Heat and simulated injury','FYdeliberatelydropsCanopyandgetsclawed;ClearHeatdetoxexplicit25765. Addedwounds258staged. No permanentnewGuacquisition.',[(257,40),(257,41),(257,65),(258,14)])
res('City charges','Entry, dining and lodging','Outer10each=20;fifth100each=200;fourth200each=400;third600quotedforpair,per-personreadingnotexplicit. Meal15;lodging30/day,10days300,monthnearly1000approx.',[(259,66),(259,101),(260,44),(261,1),(261,22),(261,47),(263,66)])
res('Cancelled versus completed sales','Bone Gu','56*320=17920;20*800=16000;Spike6700=>40620.262withdrawalmeansnoactualsaleuntil26892;Spiraluse265/266valid. Bai’sseparateholdingnotautomaticallyincluded.',[(262,12),(262,16),(262,22),(262,23),(262,26),(262,28),(262,54),(268,92),(268,93)])
res('Borrowed information Gu','Bookworms','Twoownedbyshopkeeper,temporarilyborrowednotacquired;FYreturnsexplicit. White-lightentrydoesnotdestroythem.',[(261,79),(261,88),(261,90),(261,98)])
res('Movement constraints / efficiency','Wei Yang’s Gu set','LightRainbowfastbutreaction+essence+physicalmodificationconstraints;LightSourcehalveslight-typeGu costs only. BrokenFlyingBoneShieldconstructnotGu-loss, reused26648.',[(265,93),(266,29),(266,31),(266,34),(266,48),(266,62)])
res('Contract / instalments / purchase','Recipe and storage Gu','900000=870000+30000,not50000balance. StorageGu6600separatepaidpurchase,1millionmaxcapacity. PoisonVowconsumed;Reunionrecipeexplicitlyexcluded.',[(268,26),(268,32),(268,42),(268,57),(268,58),(268,66),(268,68),(268,85),(268,87),(268,89),(268,90)])
res('Net transaction / endpoint wealth','934020 net,945000 stated total','900000+40620−6600=934020;945000−934020=10980impliedearliernetfundsifexact. No inventedexpensesreconciliation;mostfundsinPrimevalElder,someseparatelyheld.',[(268,92),(268,93),(268,94),(268,95)])
res('Offered not received','Million-stone reward','270offers1million,rejected. Alternativeoffernotdescribeduntilunread271;do notaddmillionto945000.',[(270,91),(270,95),(270,101),(270,103)])
np=sum(len(c['paragraphs']) for c in batch);nc=sum(sum(map(len,c['paragraphs'])) for c in batch);tp=sum(len(c['paragraphs']) for c in cs);tc=sum(sum(map(len,c['paragraphs'])) for c in cs)
save('proposal-ledger.json',ledger);save('chronology-register.json',dict(scope='Sequential through270; current, remembered and proleptic clocks distinguished',entries=events));save('resource-register.json',dict(scope='Sequential through270; deployment, custody, offers, cancellations and realised transactions distinguished',entries=resources))
progress=load('history/before-batch013-reading-progress.json');progress.update(sequential_chapters_completed=list(range(1,271)),paragraphs_read=tp,paragraph_characters_read=tc,next_chapter=271,remaining_chapters=2064,batch_report='Batch-013-Chapters-256-270.md',scope='Full sequential Chinese-source reading through270; no fresh bilingual/live-site audit',whole_novel_chronology_verified=False)
progress['batches'].append(dict(id='013',chapters=[256,270],paragraphs=np,characters=nc,reading_segments='Seven complete untruncated two-chapter outputs and complete270; adaptive15'))
progress['chapters'] += [dict(chapter=c['corpus_chapter'],file=c['file'],title=c['title'],paragraphs=len(c['paragraphs']),first_paragraph=1,last_paragraph=len(c['paragraphs'])) for c in batch];save('reading-progress.json',progress)
save('batch-013-reading-log.json',dict(status='Complete',endpoint=270,next_unread=271,segments=[dict(chapters=[a,a+1],status='Full paragraph sequences printed and read; untruncated',paragraphs=sum(len(by[n]['paragraphs']) for n in [a,a+1])) for a in range(256,270,2)]+[dict(chapters=[270],status='Complete untruncated chapter read',paragraphs=len(by[270]['paragraphs']))],note='Adaptive15, actual reading. Reader258pp70–74/79 omissions marked, original numbering and EPUB unchanged. No invented timestamps.'))
text=['# Numbered Chinese source: Chapters256–270','Original wording retained except explicit reader-facing omission markers258pp70–74/79 for sexualised minor content. Original numbering and EPUB unchanged. All original paragraphs read.']
for c in batch:text += [f"## Corpus chapter {c['corpus_chapter']}: {c['title']}",f"Volume: {c['volume']} | EPUB: {c['file']}"]+[f"{i}. {reader(c['corpus_chapter'],i,t)}" for i,t in enumerate(c['paragraphs'],1)]
(r/'Batch-013-Numbered-Chinese-Source.md').write_text('\n\n'.join(text))
for name,vs in [('Chronology',ne),('Resources',nr)]:
 out=[f'# Batch013 {name} jotter','All provisional; no source edits.']
 for v in vs:
  out += [f"## {v['id']}: {v.get('event',v.get('entry'))}",v.get('constraint',v.get('calculation')),v.get('evidence_status',v.get('status'))]
  for z in v['sources']:out += [f"Ch{z['chapter']} p{z['paragraph']}",'> '+reader(z['chapter'],z['paragraph'],z['text'])]
 (r/f'jotters/Batch-013-{name}.md').write_text('\n\n'.join(out))
out=['# Batch013 continuity and proposed corrections','All held, unapproved and unapplied. SR104 andSR110 receive new evidence.']
for v in new:
 out += [f"## {v['id']}: {v['category']}"]+[f"**{k}:** {v[k]}" for k in ['recommended_action','rationale','confidence','dependencies','status']]
 if 'copy_items' in v:
  for z in v['copy_items']:out += [f"### Ch{z['chapter']} p{z['paragraph']}: {z['original']} → {z['replacement']}",z['confidence'],'> '+reader(z['chapter'],z['paragraph'],src(z['chapter'],z['paragraph'])['text'])]
 else:
  for z in v['locations']:out += [f"Ch{z['chapter']} p{z['paragraph']}",'> '+reader(z['chapter'],z['paragraph'],src(z['chapter'],z['paragraph'])['text'])]
(r/'jotters/Batch-013-Continuity.md').write_text('\n\n'.join(out))
(r/'jotters/Batch-013-Preserve.md').write_text('''# Batch013 preservation cautions

- Ding’s stone tablet is ordinary; FY uses remembered biography, not a hidden surveillance Gu.
- FY claiming twoBlueZombies andseniorbrotherstatusisfalse. NoZombieHeartacquired;DingGuallburned.
- ThreeGreenowned,twofielded,onefieldloss. Donotdoublecountlossorignorehomeguard.
- Near-decadewordingandnegotiationtwo/three-dayclaimmayberough/inclusive;do notcertifyexactdates.
-257years-laterXinCirecollectionisprolepsis,notelapsedsceneorformerlife.
-13000lootfitsTushita’s30000absolute/15000practicalallocation. Fundsownedarenotallinsideflower.
-258RevolutionTwopeak;noRevolutionThreebreakthroughorYanghandoveryet. PerformanceandstoredsilvermisleadWei.
-Former-lifecaravancompensation2xnotcurrentcash. Currentmillionrewardofferedthenrefused.
-Innercityfiveradialzonesnotfiveverticalfloors. Thirdentry600forpairwordingnotexplicit600each.
-Bookwormsborrowednotbought;FlyingBoneShieldconstructsbrokennotconfirmedGudead.
-262salescancelled;268salesactual. Thus265/266Spiraluseisnotuseafterdisposal.
-56BoneSpearsafterfurtherstarvationfits242approximate2/3loss;initialdemonstrationnotnecessarilyextra57th.
-40620Gusaleand934020netgainarecorrect. 30000balanceversus50000isdistinctfromunquotedpubliccontractprice.
-Agreementtextnotfullygiven;270publicacknowledgmentsoldrecipeisnotproveddisclosureofsecretfraud.
-15Shangofficesreducedby1/3=10. Oneheirplus10juniorlordsnot11heirs;allchildrennotnecessarilyofficeholders.
-269banquettenofficeholders=9sons+ChiWen. Chief’syoungappearanceisnotactualage;nearly30oldestsonnotparadox.
-Wei25atappointmentbythen-youngShangYanFei,notnecessarilyalreadyclanhead. XiaoYan27fits27/28earlier.
-Newtwinsdeathreportsdonotresolvemixedwitness. Noindependentcollationperformed.
-270endsbeforealternativerewarddetails;do notinventreceiptsofGu,badge,healingormoney.
''')
stand=load('history/before-batch013-working-standards-register.json');stand['coverage_through']=270
su={'WS-01':'Dingfalsebrotherhood,ordinarytablet,RevolutionThreebluffandFangZhengaliasmustnotbeadoptedasfacts. Newdeath-branchreportdoesnotresolveSR104.','WS-02':'56*320+20*800+6700=40620;900000+40620−6600=934020. Actual30kbalance,50kisolatedcandidate.','WS-03':'FY2peak258,not3;Wei’sbothRevolution3/GradeAassessmentinference. Yangpromiseunfulfilledbutnotyetatthreshold.','WS-04':'DingGuallburned. Bookwormsborrowed;262salescancelledbeforeduel,268actuallysold. Most945kfundsinnewstorageGu.','WS-05':'257futureXinCirecollectionisprolepsis. Audience3时辰≈6h,meal>2≈4h. Near-decadeandtwo/three-daywordingheld.','WS-06':'13klootsfitsTushitalimits. Millionrewardrefused. Publicprice/privateassetsqueriesmustnotcorruptcorrectnetgain.','WS-07':'Arena30丈/18丈vs600mheldlocalquery,notblanketshrinkage. Cityfivezonesandverticallevelsaredifferentaxes.','WS-08':'Wei25recruitedbeforeYanFeibecamechief;XiaoYan27. Chiefyoungappearance≠birthage.15juniorofficesminus1/3=10.','WS-09':'Floor4vs3/半折vs五折locallyheld. Wrongsubjectnames26284/26319located;noall-name-normalisation.','WS-10':'Actualcoverage270/2334;2064remain. Allapproved/appliedfalse;backupunresolved.','WS-11':'Agreedmaximunchanged;noimplementationapproval.'}
for v in stand['entries']:v['batch013_update']=su[v['id']]
stand['entries'].append(dict(id='WS-12',topic='Clan-specific titles and competitive offices',status='Working distinction strengthened; clan rules still require whole-novel review',rule='Keep 少主 distinct from 少族长. Do not equate every leader’s child with a designated heir. In Shang clan, separate ordinary children, ten selected junior-lord officeholders and one designated heir.',evidence='235p93 gives a broad child/heir distinction;262p76 and263pp35/53–55 establish Shang’s restricted competitive offices.267p60 identifiesShangTuoHai asheir. The earlier general formulation needs this clan-specific qualification.',reopen='Any explicit clan-specific succession rule, nominal versus functional title, or different historical arrangement.',batch013_update='SR118holdswrongtitles26265/26375 andlower-confidence26972futuretitle. Stabilising vocabularydoesnotauthorisemanuscriptedits.'))
save('working-standards-register.json',stand)
out=['# Working editorial standards','## Evidence checkpoint: Chapters1–270','Working rules are not whole-novel factual certification or manuscript approval.']
for v in stand['entries']:out += [f"## {v['id']}: {v['topic']}"]+[f"**{k}:** {v[k]}" for k in ['status','rule','evidence','reopen','batch013_update']]
(r/'WORKING-STANDARDS.md').write_text('\n\n'.join(out))
def quote(c,p):return f"**Ch{c} p{p}:**\n\n> {reader(c,p,src(c,p)['text'])}"
report=f'''# Sequential close-reading review: Chapters 256–270
## Batch 013 | The Omniarch

**Actual sequential coverage: 1–270 of 2,334. Next unread:271. Remaining:2,064.**

Fifteen complete chapters read in seven untruncated pairs and one complete final chapter: **{np:,} paragraphs / {nc:,} source characters**. Cumulative: **{tp:,} paragraphs / {tc:,} characters**. No extraction-only coverage is counted.

The ledger now contains **122 records:121 active and held, one withdrawn**. Nine new records include **{len(fixes)} located copy candidates**. Every proposal retains an action, rationale, confidence, dependencies and held status. No manuscript or site emendations have been applied. This is Chinese-source review, not a fresh bilingual/live-site audit.

## 1. A definite balance error inside an otherwise correct transaction

{quote(268,58)}

{quote(268,75)}

{quote(268,89)}

The agreed total is900,000, the first instalment870,000, and the balance30,000. The repeated thirty-thousand references agree with the actual final payment. **SR-119: 五万 → 三万 at268p75** is a very strong local candidate.

The larger transaction should otherwise be preserved:

| Component | Amount in stones |
|---|---:|
|56 Bone Spear Gu ×320|17,920|
|20 Spiral Bone Spear Gu ×800|16,000|
|Bone Spike Gu|6,700|
|Gu sale subtotal|40,620|
|Recipe price actually agreed|900,000|
|Primeval Elder storage Gu purchased separately|−6,600|
|Net gain from these transactions|**934,020**|
|Stated resulting funds|**945,000**|

The subtotal and net gain are correct. If945,000 is exact, the implied earlier net funds are10,980. We do not have a complete itemised expenditure history, so I have not invented food, rent or transport costs to force that balance.

The storage Gu can hold up to one million stones. Most funds are put there, with some kept elsewhere. There is no need to force almost a million stones into the Tushita Flower.

### Two accounting questions are less certain

**SR-120** keeps these separate from the proven balance typo:

-267 proposes a650,000 public sale figure;268 instead identifies600,000 clan funds within the870,000 payment. The final oath’s full text is not reproduced, so the public price may have been renegotiated.
-268 first describes over400,000 in accumulated personal savings, then calls270,000 almost all of Ya Zi’s private assets. Unreported outflows are possible, but not established.

Neither warrants silently changing600,000/270,000 to650,000/220,000, or inserting a fictional expense. Those are held documentary/accounting queries.

## 2. The Gu are not sold before the duel

The seemingly completed sale negotiations in262 are subsequently cancelled:

{quote(262,54)}

Thus the Spiral Bone Spear Gu used against Wei Yang in265–266 have not yet been sold. The actual sale occurs in268p92, after the duel. The final56 Bone Spear Gu also fit progressive starvation after the earlier approximate two-thirds loss; the count need not remain frozen at that earlier checkpoint.

The Bone Flesh Reunion recipe is expressly withheld. The record does not treat the entire inheritance as sold merely because a bundle of related recipes is transferred. Bai’s possible separately held Spiral Gu also should not automatically be included in Fang Yuan’s twenty offered specimens.

The shop’s Bookworms are borrowed, not acquired. Their conversion into light when information is transmitted is not their destruction. Similarly, broken Flying Bone Shield constructs do not establish that the underlying Gu died; it is used again during the duel.

## 3. Ding Hao: owned inventory is not deployed inventory

{quote(255,86)}

{quote(256,54)}

**SR-114:** change255’s statement that he accumulated only two into a statement that he brought only two.256 gives three total:two deployed and one guarding the cave. Later, one of the deployed Green Zombies is destroyed. The home guard must not disappear from the ledger.

Fang Yuan’s claim to possess two Blue Zombies is a lie. His alleged senior-disciple status is also a lie. The tablet is explicitly ordinary: he knows Ding’s private habit through remembered biography, not a secret surveillance mechanism.

Ding’s Gu are deliberately burned after his death. Fang Yuan does not acquire Zombie Heart Gu. The roughly13,000 stones he does obtain fit the Flower’s previously stated30,000 absolute capacity and15,000 working allocation, without proving that every other owned stone is inside it too.

**SR-115** separately holds the near-ten-year wording:254 gives over eight years of cultivation plus nearly three more of army-building. 十来年 is a possible less restrictive wording if近十年 is intended strictly, but approximate colloquial usage prevents a categorical error finding.

The caravan’s destruction is now narrated, rather than merely planned: the remaining three are killed, Ding reports no escapees, and Fang Yuan then kills Ding. This is the present witness’s account, not a guarantee against any later revelation.

## 4. Restaurant: floor and discount drift

{quote(259,101)}

{quote(259,102)}

{quote(260,2)}

{quote(260,44)}

**SR-116 has two linked local candidates:**

-260p2 三层 → 四层, matching the explicitly chosen floor.
-260p44 半折 → 五折, matching the advertised half-price rate.

In ordinary discount notation, one折 means paying10% of the price, so半折 is5%, not50%. The fifteen-stone payment need not change. A full-price thirty-stone bill is an inference under the intended half-price rate, not an independently itemised sum.

## 5. Arena geometry: a local problem, not a general scale policy

{quote(265,60)}

{quote(266,23)}

{quote(266,54)}

At the conventional scale, thirty丈 is roughly100 metres and eighteen丈 roughly60. The latter being more than half the arena fits that local description. A later movement from one side to the other covering nearly600 metres is difficult to reconcile with it.

**SR-117:** conditional preference for近百米 if the thirty丈 description establishes the arena’s span. Another held option is removing the exact metre clause until a second witness establishes the intended figure. 方圆 is imprecise, and a travelled path is not always a straight-line extent, so the repair is not final.

Do **not** automatically replace600 with60: the eighteen丈 leap and the later movement are separate actions. Nor does this justify shrinking mountains, city walls, travel distances or Gu ranges throughout the novel.

Wei Yang’s speed itself has stated limits: reaction support, substantial essence consumption and incompatibility with certain bodily strength modifications. His Light Source Gu halves light-type Gu costs, not all Gu costs universally.

## 6. Titles: the distinction becomes more precise

Shang has **ten selected junior-lord offices and one designated heir**, not ten heirs and not necessarily one office for every child. The earlier broad explanation in235 must be qualified by these clan-specific rules. Fifteen offices reduced by one-third correctly yields ten.

**SR-118:**

-262p65: Ya Zi wants to retain a少主 position, not the少族长 position already associated with Shang Tuo Hai.
-263p75: the two Bai children should provisionally be少主, not two designated heirs.
-269p72: Chao Feng’s former-life almost becoming少主 is a weaker query. 族长 may be intended, but the different timeline prevents a confident automatic substitution.

The banquet itself names ten officeholders:nine sons and Chi Wen. The heir need not be an eleventh named attendee. Wei Yang being the third-ranked general among five is also consistent.

A twelfth working standard now records this vocabulary distinction while explicitly preserving clan-specific exceptions. It does not authorise applying the candidates.

## 7. Chronology and staged appearances

The new chronology retains the following distinctions:

-258: Fang Yuan reaches **RevolutionTwo peak**, not RevolutionThree. The Yang Gu handover threshold has not yet been reached.
-257’s account of Shang Xin Ci remembering this night years later is a **narrative flashforward**, not a present time jump or Fang Yuan’s former-life memory.
-258’s detained merchants and double compensation belong to the former life, not a current receipt.
-263’s three-day investigation and three-day lodging descriptions are parallel anchors, not automatically six days.
-264’s wait lasts three时辰, about six conventional hours; the meal lasts over two, about four. These are not silently translated as three and two hours.
-265 moves to the next day’s tour and then the third day’s tour and duel.
-267 describes the Qing Mao intelligence as more than half a year old, supporting a months-long journey without supplying an exact date.

**SR-121:**268’s narrator says Ya Zi returns two days later, while Fang Yuan says three days have passed. Inclusive day counting, a different quoted-price anchor or bargaining rhetoric may explain it. The candidate“两天” or a nonnumerical“这几天” remains held.

Wei Yang’s impression that both guests are at leastRevolutionThree is an inference based on the performance and borrowed essence. It is not a new narrator-certified promotion. “My true name is Gu Yue Fang Zheng” is another deliberate cover story, not a name correction for Fang Yuan.

## 8. Earlier proposals: new evidence, not automatic closure

-**SR-104, twins-version fork:**263 repeats their deaths as a report;270 repeats them in the investigation account. This strengthens the death branch’s attestation but does not reconcile231’s missing-twins version or authenticate the compiler’s provenance claims.
-**SR-110, Chen leader:**257p83 again uses陈双全, strengthening the current preference over陈双金. The emendation remains held.
-**SR-099, before/after RevolutionThree cultivation:** further lower-rank progression supports the query; benefits afterRevolutionThree remain unread.

The poison oath’s complete terms are not quoted. Fang Yuan publicly mentioning that he sold recipes in270 does not by itself prove that he disclosed the secret inflated-payment arrangement. I have not labelled that a poison-oath contradiction without establishing the actual scope of the prohibited disclosure.

## 9. Located copy candidates

The continuity jotter contains the full source paragraphs, confidence labels and proposal dependencies. These include several strong wrong-subject repairs, not just typographical preferences:262p84 substitutes Shang Xin Ci for the father thinking about his daughter, and263p19 repeats Shang Yan Fei where the daughter is meant.

| Location | Source fragment | Held candidate |
|---|---|---|
'''
report+='\n'.join(f'|{c} p{p}|{a}|{b}|' for c,p,a,b in fixes)
report+=f'''

## 10. Exact endpoint

At270, Fang Yuan is stillRevolutionTwo peak; Bai isRevolutionThree peak. The sale has been completed and the stated funds are945,000. **The offered one-million-stone reward is refused**, so it must not be added to those funds.

The chapter ends as Shang Yan Fei begins another reward proposal. Its details are not given in the material read so far. No new badge, healing, Gu or monetary reward is claimed here.

Saved: this report, numbered Chinese source, five jotter files, eight-segment reading log, **122 proposal records, {len(events)} chronology entries, {len(resources)} resource entries**, cumulative workbook and12 working standards. Reader258pp70–74/79 use explicit omission markers for sexualised minor content; numbering and original EPUB remain unchanged and all original paragraphs were read.

Your agreed maxim remains **“Man is the most intelligent of all living things.”**

**Next unread:271.** All edits remain held. No original-source, manuscript, site or repository changes, uploads or deletions occurred. Remote research backup remains unresolved. Whole-novel consistency is not certified.
'''
(r/'Batch-013-Chapters-256-270.md').write_text(report)
old=(r/'update_batch010.py').read_text();wb=old[old.index('# Workbook: cumulative'):old.index("(r/'CURRENT-STATUS.md').write_text")]
wb=wb.replace('1–220 of2334','1–270 of2334').replace("('Next unread',221)","('Next unread',271)").replace('103total;102activeheld;1withdrawn','122total;121activeheld;1withdrawn').replace('range(10,0,-1)','range(13,0,-1)').replace("v['batch010_update']","v['batch013_update']").replace('Batch-010-Chapters-201-220','Batch-013-Chapters-256-270').replace('CHAPTERS201–220','CHAPTERS256–270').replace('Chapters201–220','Chapters256–270').replace('Twenty complete chapters; personal clocks and inventory scope distinguished','Fifteen complete chapters; instalment arithmetic, source variants and local staging').replace('Ch151,201p22,203p84 restricted excerpts','Ch151,201p22,203p84,250pp24–31/33/35–36,258pp70–74/79 restricted excerpts')
exec(compile(wb,'workbook-and-docx','exec'))
(r/'CURRENT-STATUS.md').write_text(f'''# Sequential review checkpoint

Fullyread1–270/2334,next271,remaining2064. Batch01315chapters:{np}paragraphs/{nc}characters. Cumulative{tp}/{tc}.122proposals121activeheld+SR047withdrawn.9newSR114–122,SR122has{len(fixes)}copyitems. {len(events)}chronology/{len(resources)}resources,12workingstandards. Allapproved/appliedfalse. Detailedhandoff jotters/batch-013-working.md andBatch-013-Chapters-256-270.md/.docx. Originalsourceunchanged;pre013archivespreserved.

Criticalcarry:
-SR114255only2Green vs2563total(onehome2field),preferredqualify2deployed. OnefieldGreenlost257,noBlueFYfalseclaim. DingGuallburnednoZombieHeartloot,~13000stonesTushitafits30k/15kcapacity. Caravanlast3dead/Dingdead257;4travelpartysurvivorssourcecurrentaccount.
-SR115Ding8plusyears+nearly3vs近10wordingapproxquerycandidate十来年notexact11. SR116259floor4selectedvs260floor3;半折5%vs五折50%preferred,15paidunchanged. SR117arena30zhang/18zhangoverhalfvs266600m,conditionalnear100mnotautomatic60(globalshrinkforbidden).
-SR118YaZi26265保少族长→少主,26375Baitwinstwoheirs→少主.26972ChaoFengformerlifealmost少主lowquerypossibly族长,don'tconflatebranches. WS12Shang10competitivejuniorlords+1heir/ordinarychildrenqualifies235generaldescription.15minus1/3=10correct.
-SR11926875五万→三万,900k−870k=30k repeated58/72/85/89. SR120publicpriceproposed650kbut600kclanfundsfinalunquotedcontract;400kprivateearlier270knearalllaterunreportedoutflowspossible. Noautomaticlinked650/220kfix. SR121narratortwodaysvsFYthreedaysinclusive/rhetoricpossible.
-56BoneSpear*320=17920,20Spiral*800=16000,Spike6700 total40620.262recallsALLgoodsnosaleuntil26892afterduel,notuseafterdisposal. Bai separateSpiralnotautomaticincluded. Recipe900k excludesReunion;PrimevalElderGu6600boughtseparate,1millioncapacity. Net900000+40620−6600=934020correct,total945000impliesprior10980ifexactnoinventedspends.270millionrewardREFUSED;alternativeofferundetaileduntilunread271.
-FY2peak258through270,noRevolution3/Yanghandover. WeiBgrade3peak,guessFY3publicbluff. LightRainbowconstraintsreaction/essence/bodystrength;LightSourcehalvesonlylightGu;shieldconstructbreaknotGu-loss. Bookwormsborrowedshopownedreturned.
-258routeTwinGenerals→BloodTears→6mountainsvillagestopsdurationunknown. 257years-laterXinCiflashforwardnotcurrenttimejump. Formerlife2xcompensationnotcurrentfunds.267QingMaointelligence>halfyearold. City3dayparallelspy/lodging,264wait3shichen≈6h,meal>2≈4h,nextdaytour,thirdtourduel,3dayjump267,2dayreturn268,3daybalance,3daybanquet. Noexactdateinvented.
-Outer20pair,fifth200pair,fourth400pair,third600wordedpairnotexplicitperhead;rent30/day. City5zonesnot5verticalfloors.258Revolution6ShangelderthreatCicadasearch;avoidguilt-motivatedmarriagecontentreaderomissions25870–74/79.
-SR104new263rumour/270investigationtwinsdeadstilldoesNOTresolve231missing/compilerprovenance. SR11025783陈双全furtherstrengthenscandidate. SR099stillheldfutureRevolution3benefitsunknown. Poisonvowfulltextabsent;270acknowledgespublicrecipesale≠provenfrauddisclosure. Olderholdscontinue.
-Endpointfamilybanquet:ShangXinCirecognised,tenofficeholders9sons+ChiWen;TuoHaiheirnotnamedattendee. Noalternativeawardknown. OriginalEPUBhashchecknextQA.

No source/site/repo changes,uploads,deletions. Backupunresolved. Do notrerunoldgeneratorsafter013;013idempotentfrompre013archives. Source/notes/log/registers/workbook/reportupdated. Readeroriginalnumberingretained. Agreedmaximunchanged.
''')
assert len(cs)==270 and len(ledger)==122 and len(new)==9
assert tp==22365+np and tc==784942+nc
assert all(not v['approved'] and not v['applied'] for v in ledger)
assert all(z['text']==src(z['chapter'],z['paragraph'])['text'] for v in events+resources for z in v['sources'])
assert len({v['id'] for v in events})==len(events) and len({v['id'] for v in resources})==len(resources)
texts={t for c in cs for t in c['paragraphs']}
for line in report.splitlines():
 if line.startswith('> '):assert line[2:] in texts
print('QA PASSED',dict(chapters=270,new_paragraphs=np,new_characters=nc,paragraphs=tp,characters=tc,proposals=len(ledger),copy_items=len(fixes),chronology=len(events),resources=len(resources),next=271))
