from pathlib import Path
import json,shutil,hashlib
from openpyxl import Workbook,load_workbook
from openpyxl.styles import Font,PatternFill,Alignment
r=Path('/home/user/editorial/sequential-review')
def load(n):return json.loads((r/n).read_text())
def save(n,v):(r/n).write_text(json.dumps(v,ensure_ascii=False,indent=2))
for n in ['reading-progress.json','proposal-ledger.json','chronology-register.json','resource-register.json','working-standards-register.json']:
 p=r/'history'/('before-batch017-'+n)
 if not p.exists():shutil.copy2(r/n,p)
cs=sum([load(f'batch-{i:03d}-source.json') for i in range(1,18)],[]);by={c['corpus_chapter']:c for c in cs};batch=[by[n] for n in range(316,336)]
def src(c,p):return dict(chapter=c,paragraph=p,file=by[c]['file'],text=by[c]['paragraphs'][p-1])
def ss(rr):return [src(*z) for z in rr]
def loc(rr):return [{k:v for k,v in z.items() if k!='text'} for z in ss(rr)]
def refs(z):return '; '.join(f"Ch{x['chapter']} p{x['paragraph']}" for x in z)
def reader(c,p,t):
 if (c,p)==(303,16) or (c==296 and 95<=p<=97) or (c==258 and (70<=p<=74 or p==79)) or (c==250 and (24<=p<=31 or p in [33,35,36])) or (c==151 and (31<=p<=67 or p in [98,99])) or (c,p) in [(201,22),(203,84)]:return '[Restricted passage omitted from reader-facing copy. Original numbering retained; original EPUB unchanged.]'
 return t
ledger=load('history/before-batch017-proposal-ledger.json');new=[]
def pro(i,cat,rr,action,why,conf,dep):
 v=dict(id=f'SR-{i:03d}',category=cat,locations=loc(rr),recommended_action=action,rationale=why,confidence=conf,status='Provisional proposal or query; no approval',dependencies=dep,approved=False,applied=False,publication_status='HOLD: full2334-chapter reading and global reconciliation outstanding');ledger.append(v);new.append(v);return v
pro(140,'Liquor Worm retrospective scope',[(121,62),(122,11),(145,28),(239,20),(326,22),(326,23)],'Prefer narrowing326p22 to 自从有了骨肉团圆蛊，四味酒虫就一直没有再动用，只是白白养着。 English candidate: Since obtaining Flesh-Bone Reunion Gu, he had left the Four-Flavour Liquor Worm unused, merely keeping it fed. Preserve its earlier Qing Mao use.','326p22 literally anchors non-use to initial refinement;121/122/145 explicitly show use.239p20 and326p23 instead support redundancy after Reunion and access to Bai’s superior essence. External repost repeats both326 and121/145 evidence.','High confidence in literal retrospective conflict; moderate-to-high confidence in narrower replacement scope.','Exact onset of disuse remains unquantified; independent authorial witness unavailable. Do not claim it was never useful or that Four-Flavour refines Revolution Three essence.')
pro(141,'Xin Ci festival-stage inconsistency',[(309,68),(327,33),(328,9),(329,29)],'Provisionally prefer327p33 两转→一转 if no new advancement is established. Keep as a query until the possibility of an outdated brothers’ assessment at329p29 is excluded. Do not silently alter either source quotation.','327 describes Two;329 describes One during the same festival outing, with no narrated change.309 One upper supports One. External repost repeats both readings.329 is embedded in the brothers’ evaluation and could be outdated knowledge rather than authoritative stage reporting.','High confidence in located conflicting readings; moderate confidence in correcting327 rather than329.','Later stage statements; viewpoint and any unshown advancement. Source inconsistency is not proof of a mistranslation.')
pro(142,'Sun Yuan Hua: Chinese character variants',[(334,22),(334,26),(334,28),(334,30),(334,38),(334,43),(334,44),(334,46),(334,96),(335,18),(335,27)],'Provisional Chinese index spelling 孙元化; flag 孙元华 in334pp26/28/30/43/44/46 as variants. Keep English Sun Yuan Hua unchanged.','Both names identify the same opponent in one uninterrupted duel.335 repeats化. External334 repost also alternates, so it does not establish an uncontested original spelling.','High same-character identity and unchanged romanisation; moderate preferred Chinese standard.','Further name occurrences and source collation; no blanket replacement of unrelated华 characters.')
pro(143,'Tripling versus three doublings: commercial wording',[(322,65),(323,15),(324,36),(324,38),(325,1),(325,2),(326,67),(327,41),(333,72)],'Render the stated result as tripled, or grew from100000 to300000. If Chinese emendation is chosen, use增至原来的三倍 for the relevant三番 wording. Distinguish200000 net profit from300000 closing capital; do not inflate holdings to800000.','325p1 explicitly gives100000+10×20000=300000.324p38 says三倍. Standard three doublings would produce800000, but those are not the narrated accounts.327’s赚到三十万 is best kept as accumulated capital in this context, not an added300000 net profit.','High arithmetic and intended commercial result; Chinese lexical repair remains editorial.','Dictionary meaning researched; contextual numerical statements control. Do not globally replace番/倍 or treat every赚 as net profit.')
v=pro(144,'Xiaodie Grade B aptitude, not cultivation',[(325,21)],'Prefer乙等修为→乙等资质. English: she had Grade B aptitude.','The sentence discusses资质; A/B/C/D grades classify aptitude, not cultivation. External Chinese witness reads乙等资质 in the same sentence.','High category distinction and attested alternate reading; authorial priority unestablished.','Preserve EPUB reading in source companion and record variant provenance.')
v['external_variant']='https://www.hetushu.com/book/7640/5345564.html'
pro(145,'Zhou Quan upper versus peak: unshown restoration query',[(325,29),(327,87),(332,5),(332,65)],'Retain both readings for now. Track325 Three upper versus332 Three peak; select no numerical replacement.','XinCi reports a fall fromFour toThreeupper; later narration says stillThreepeak. Time passes and recovery/advancement may be unshown. The first statement is character information, not automatically infallible narration. External332 witness corroboratespeak as transmitted wording only.','High quotation accuracy; low-to-moderate inconsistency diagnosis.','More evidence of restoration or earlier stage; do not confuse current100-plus age with his40–50 age at reachingFour.')
fixes=[
(316,3,'在吃之前','在此之前'),(316,89,'没用动用','没有动用'),(316,100,'能继续力气','能积蓄力气'),(316,104,'手掌着劈砍','手掌则劈砍'),
(317,4,'一根接着一根石林','一根接着一根石柱'),(317,14,'野兽石嘶吼','野兽嘶吼'),(317,42,'局面板回来','局面扳回来'),(317,50,'抓住稍纵即逝','抓住稍纵即逝的战机'),(317,77,'方源战在','方源站在'),(317,87,'不堪回事','不堪回首'),(317,88,'倾述','倾诉'),
(318,38,'连续撞到数根','连续撞倒数根'),(318,47,'咬牙巨臂','咬牙举臂'),(318,56,'兼并灵活','兼具灵活'),(318,85,'被剥削了少主之位','被剥夺了少主之位'),(318,88,'现在有是','现在又是'),
(319,18,'毫无疑外','毫无意外'),(319,39,'龙形虎步蛊','龙行虎步蛊'),(319,48,'坚固卓绝','艰苦卓绝'),(319,94,'有开始','又开始'),
(320,24,'伸手向着轻轻一指','伸手向前轻轻一指'),(320,95,'还有使用','还要使用'),
(321,28,'从另个方面','从另一个方面'),(321,44,'许多人心起伏不定','许多人人心起伏不定'),(321,60,'茶钱饭后','茶余饭后'),
(322,15,'脸色有阴沉','脸色又阴沉'),(322,29,'一只商队','一支商队'),(322,38,'考研一个','考验一个'),(322,57,'我还有特别关照','我还要特别关照'),
(323,6,'瓢盆满钵','盆满钵满'),(323,41,'心中不禁没有喜感','心中不仅没有喜感'),(323,66,'忽然发出异变','忽然发生异变'),
(324,13,'自然不能对待寻常属下一样对待他','自然不能像对待寻常属下一样对待他'),(324,18,'要什么做','要怎么做'),(324,24,'大量收购这三只蛊','大量收购这三种蛊'),(324,65,'彻底拔出','彻底拔除'),
(325,3,'瓢盆满钵','盆满钵满'),(325,39,'南疆地域山','南疆地域多山'),(325,55,'被三王得益','被三王利用'),
(326,1,'三叉山一代','三叉山一带'),(326,22,'没有在动用','没有再动用'),(326,49,'时间一天天，','时间一天天过去，'),
(327,66,'笑魇如花','笑靥如花'),(327,69,'茁长成长','茁壮成长'),(327,90,'他的死心','他的私心'),
(328,5,'我在来出手','我再来出手'),(328,22,'离开商心慈','离开商家城'),(328,26,'坐上起去','坐上去'),(328,47,'他有流露出','他又流露出'),(328,58,'触及道','触及到'),(328,75,'俯下身之','俯下身子'),
(329,25,'兄弟有长眼','兄弟不长眼'),(329,31,'就说话的人','将说话的人'),(329,54,'生出手来','伸出手来'),
(330,18,'方源本来','方源本人'),(330,22,'凶煞恶煞','凶神恶煞'),(330,27,'商家城；里','商家城里'),(330,35,'无暇的陶瓷','无瑕的陶瓷'),(330,39,'才能解读','才能解毒'),(330,52,'手续有都','手续又都'),(330,69,'扇飞取出','扇飞出去'),(330,77,'咬了咬，','咬了咬牙，'),
(331,11,'震摄','震慑'),(331,26,'震摄','震慑'),(331,35,'卷席而去','席卷而去'),(331,67,'中原','中洲'),(331,71,'重生一来','重生以来'),(331,78,'负责的家','的家'),
(332,23,'惊魂失措','惊慌失措'),(332,24,'给他再一个胆子','再给他一个胆子'),(332,35,'竭力竭声','竭力嘶声'),(332,84,'紫金令牌','紫荆令牌'),
(333,14,'相反设法','想方设法'),(333,40,'倾述','倾诉'),(333,42,'不再现场','不在现场'),(333,73,'严密周瑾','严密周谨'),
(334,21,'众人对紧紧地','众人都紧紧地'),(334,27,'狼背蜂腰','狼背蜂腰'),(334,35,'天资纵横','天资卓绝'),(334,69,'两只鹤群','两支鹤群'),(334,84,'勾勒起了','勾起了'),
(335,9,'不问出生','不问出身'),(335,52,'必经之力','必经之路'),(335,54,'壮年成为','壮年称为')]
# No correction is warranted solely because an unusual idiom looks unfamiliar.
fixes=[z for z in fixes if z[2]!=z[3]]
for c,p,a,b in fixes:assert a in src(c,p)['text'],(c,p,a)
moderate={(316,100),(317,50),(318,38),(318,56),(320,24),(321,44),(323,6),(324,24),(325,3),(325,39),(325,55),(327,69),(328,22),(330,52),(330,77),(331,67),(331,78),(332,23),(332,35),(333,73),(334,35),(334,84)}
v=pro(146,'Individual copy and naming candidates',sorted(set((c,p) for c,p,a,b in fixes)),'Review each candidate separately; preserve quotations and numbering. These are not approved edits or claims of live English mistranslation.','Located wrong characters, missing words, local naming variants and contextual reconstructions. Literary diction, word order and the person-versus-place reference remain conditional.','High local support for mechanical slips; moderate reconstruction and terminology items explicitly marked.','Independent witnesses for each candidate not yet exhaustively collated; do not treat the bundle as certified. Reopen any plausible literary or viewpoint reading.')
v['copy_items']=[dict(chapter=c,paragraph=p,original=a,replacement=b,confidence='Moderate: contextual reconstruction or diction; collate and test counter-reading' if (c,p) in moderate else 'High local copy support; external collation still pending',status='HOLD; unapproved/unapplied') for c,p,a,b in fixes]
for v in ledger:
 if v['id']=='SR-136':
  v['locations']+=loc([(329,77)]);v['confidence']='High source-office inconsistency; elder repair now strongly supported by explicit329p77, not an independently recovered306 variant.';v['recommended_action']='Preferred306p53 商家族长→商家家老.329p77 explicitly names Shang Bu Li as家老. Treat as source emendation, not proof that a faithful clan-leader translation was wrong.';v['batch017_update']='329p77 explicit五大家老之首的商不离家老 strengthens exact elder repair. Earlier external306 repost still reads族长; authorial variant not established.'
 if v['id']=='SR-118':v['locations']+=loc([(326,84)]);v['batch017_update']='326p84 again explicitly frames former-life ChaoFeng/XinCi competition as商家族长.322p27 distinguishes TuoHai少族长 above ten少主. Generic少主 forTuoHai322p29 does not justify a blanket title rule.'
 if v['id']=='SR-099':v['batch017_update']='Remains withdrawn.326p24–25 same-stage future assistance reduced,331 actualBaiFour→FYThreepeak assistance completesFour breakthrough. No contradiction with continuingReunionutility.'
 if v['id']=='SR-135':v['batch017_update']='326p46 now96% aptitude. Does not establish baseline of304 two-point retrospective; retain Batch016 fact-check downgrade.'
 if v['id']=='SR-139':v['batch017_update']='Horse-strength name骏马驰力蛊 recurs317p18. Earlier304p46 alternative name candidate remains moderate, not a proved universal standard.'
 if v['id'] in ['SR-136','SR-118','SR-099','SR-135','SR-139']:v['latest_update']=v['batch017_update']
events=load('history/before-batch017-chronology-register.json')['entries'];resources=load('history/before-batch017-resource-register.json')['entries'];ne=[];nr=[]
def ev(t,k,e,c,rr):
 v=dict(id=f'T{len(events)+1:03d}',timeline=t,kind=k,event=e,constraint=c,evidence_status='Source wording checked; interpretation provisional and scoped',dependency='Whole-novel reconciliation outstanding; no exact dates invented',sources=ss(rr));events.append(v);ne.append(v)
def res(k,e,c,rr):
 v=dict(id=f'R{len(resources)+1:03d}',kind=k,entry=e,calculation=c,status='Observed, reported and contingent states distinguished; not a complete balance sheet',sources=ss(rr));resources.append(v);nr.append(v)
ev('Revised current life','appointment / elapsed battle','Seven-day fight and two-hour bout','316 seven-day appointment fulfilled.317 halfshichen≈1h;319 one shichen≈2h elapsed, not another2h added. Juconcedes320.',[(316,1),(317,59),(319,49),(320,85)])
ev('Revised current life / public belief','concealment and breakthrough','PublicThree middle versus trueThreepeak','316p38 explicitConcealedBreath reconciles public316p11 andtruepeak316p81. BaiFourinitial by321; FYFourinitial331, notFourmiddle335.',[(316,11),(316,38),(316,81),(321,34),(321,68),(331,60),(335,70)])
ev('Revised current life / former life','refinement / future rediscovery','Strength Qi completed before Ju battle','Severalday/night refinement completedbefore316. Twohundredyearformula rediscovery is former-life future, not currentelapsed time.',[(316,41),(320,76),(320,80),(320,82),(320,83),(320,84)])
ev('Revised current life','politics / forecast','Arena exits and competition','FYwithdraws, supportannounceddayslater, Baisubsequentwithdrawal. Competition3months with100000capital; YaZi3yearsentence stillfuture.',[(321,36),(321,52),(321,61),(322,1),(322,39)])
ev('Current opening / older kings','news / elapsed','Three Kings opens, news and investment','Three-days-to-news thenfive-daypurchases. Twentydaypromise metwithin10reportedcompetitiondays, notinconsistentdeadline. Kingsorigins300yearsago andnear100yeartraining not currentclock.',[(323,15),(323,72),(323,79),(323,98),(324,44),(324,55),(325,1)])
ev('Revised current life','ongoing opening / refinement','Half-month-plus opening, Nine Eye, rival arrival','326openingoverhalfmonth; finalrecipe3daymarker, notcertifiedtotalchain. WuTongShentwodaysafterLongQingTian. Annualfestivaldateunnamed.',[(326,11),(326,36),(326,50),(326,51),(326,56),(326,57)])
ev('Current evening / previous life','festival and service','Token acquired one year earlier','328festival→329recruitment sameouting. Historicaltokenorigin300yearsago, capturewithin50years. Former-lifepurchasewouldbenextyear, service20years, sellerdeathwithinhalfmonthafterterm. Currentservice20yearsprospective.',[(328,9),(328,78),(328,83),(329,6),(329,10),(329,11),(329,13),(329,69)])
ev('Revised current life','short intervals / administrative obstruction','Wei sale and breakthrough','Clerkclaims1daypaperwork, replacementfinisheswithinquarterhour. Followingmorningcontroltransferred; fewdayslaternightbreakthroughlasting1shichen≈2h. Latermiddayraid separatedbyellipsis.',[(330,8),(330,33),(330,54),(331,32),(331,56),(331,76),(331,82)])
ev('Revised current life / character reports','age and stage','FY20, Zhou100plus and stage query','FY20reported332; ZhoureachedFourage40–50butisnow100plus. ZhouThreeupper325versuspeak332remainsrestoration/viewpointquery. XinCiTwo327versusOne329samefestivalrequiresreconciliation.',[(325,29),(327,33),(327,87),(329,29),(332,5),(332,65)])
ev('Revised current life','business and departure','Seven-day growth then months to victory','Informationbusiness300000→440000after7days; severalmonthsellipsis toXinCi appointment. Noexactwinningtotal ordate. Two–three-yearcitystayapproximate, nottotalreborntime.',[(328,15),(331,61),(333,69),(333,72),(333,78),(333,79),(333,81)])
ev('Parallel Central Continent thread','institutional cycles / recovery','True Fang Zheng promotion and sleep','3/8/15yearexamsareinstitutionalcycles, notyearsserved. Fourmiddlewinseliteplace;2days2nightssleep; WhiteFoxinheritanceappearedmonthsago. ThreadcutdoesnotproveexactsynchronywithFY20statement.',[(334,20),(334,35),(334,56),(334,96),(335,5),(335,12),(335,20),(335,31)])
ev('Revised current journey','unquantified travel / unfinished fight','Fire Charcoal mountain encounter','Severaldaystraversingthismountain, notexacttotaltimefromShang. Assassinssettrapbutnotyetpersonallyengaged. LavaCrocodilefightabouttobegin; resultunknown.',[(335,43),(335,44),(335,59),(335,65),(335,73),(335,76)])
res('Permanent strength / present limit','Eight beasts, three Dragon-Elephants','FY8phantoms nowexplicit, addedwhiteelephantandpython; currentbodylimit8notuniversal. Ju3DragonElephantGuused. StrengthGu lostinrefinementdoesnoteraseembodiedpower.',[(317,18),(317,19),(317,37),(317,38),(317,39)])
res('Combat mechanics / healing','Injury-controlled strength and armour','BitterStrengthFour enables2then3then8phantoms; injuriesriskdeath. SelfRelianceusedselectively. Inertiaresetafterburst. Ivoryarmourcannotstretch; HardQicoversapparentopening. GiantTransformation3×notnew9beastsowned.',[(316,87),(317,42),(318,77),(318,81),(319,10),(319,23),(319,29),(319,79),(319,100),(319,109)])
res('Refinement / permanent carrier','Strength Qi replaces Feng Qi','FourFengQi reverse-refined toThreeStrengthQi;20plusauxiliaries/30plussteps/80%estimate. Actualsuccessconfirmed. Beastphantomsreturnafterqiexpires; notconsumed.',[(320,74),(320,75),(320,76),(320,77),(320,80),(320,81),(320,82)])
res('Essence / attention','Forty-percent volley, seventy-percent replenishment','8×5%=40percentagepoints;90%reservepermits2theoreticalvolleyswithoutothercosts. Refilled70%includesLotus+2stones; absorptiontakesattention. Noextraaptitudeinferred.',[(320,25),(320,44),(320,45),(320,57),(320,91),(320,92),(320,93),(320,95)])
res('Loot / cultivation / withdrawal','Giant Spirit Will claimed; BaiFour','FYtakesGiantSpiritWill,notcompleteJuGuinventory. BaireachesFourinitial andlaterleavesarena. HerlostIceCrystalnotautomaticallyrestored. FYwithdrawswithoutYanvictoryor18defences.',[(321,12),(321,32),(321,34),(321,36),(321,61),(321,68)])
res('Entrusted assets / rules','YiFan capital and competition comparisons','YaZisecretholdingsentrustedfor3years,notgiftorfutureconfirmedreturn.100000competitioncapital; figures300000/600000/700000–800000andrecords890000/920000/1110000areclosingtotals.',[(322,3),(322,5),(322,12),(322,39),(322,43),(322,53),(322,54)])
res('Pooled capital / partial receipts','Gu speculation and Bai instalment','DogOne/CraneTwo/EggOne bought. XinCi100000+newBaiinstalment300000+otherfunds. Baihaspaidmorethanhalf3m demand; exactcumulativebalanceunknown. Competitionprofitproportionalto100000investment.',[(323,98),(323,99),(323,100),(324,21),(324,35),(324,36)])
res('Realised capital / assets / fees','Tripling and information income','XinCi100000+200000profit=300000. FYassets>2.4m,3ElderGucontainers,notdebt-freecashcertification. Intelligence400000agreedandlateradditionalunpricedpayment; Wuofferuncompleted.',[(325,1),(325,2),(325,3),(325,62),(325,63),(325,66),(325,70)])
res('Refinement recipe / stock','Nine Eye Liquor Worm','TwoOne→Two;twoTwo→Three;twoThree→Four. ExistingTwoinput,failuresinTwoandThree stages,near200000totalcost. FinalNineEyeFourobtainedbutFYThreecannotuseyet. Exactreplacementinputcountunreported.',[(326,17),(326,22),(326,29),(326,30),(326,32),(326,35),(326,36),(326,39),(326,44)])
res('Aptitude / stage distinction','Bai96%, XinCiquery, XiaodieGradeB','BaiFourinitial96%aptitude; NineEyeacceleratingadvancementundesirable. XinCiTwo327versusOne329query. XiaodieGradeBaptitudevariantnotcultivation. Noexactbirthdayorpercentageclockrepair.',[(325,21),(326,46),(327,33),(329,29)])
res('Purchase / bounded service','Ten-stone stall, Xiong three brothers','10stonesbuysstallincludinghalftoken. XiongTuThreeupper/HuoThreemiddle/FengThreeinitial,allGradeB;20yearservicetoXinCiagreed. NofamilyidentitywithQingMaoXiongassumed.',[(328,45),(329,21),(329,22),(329,23),(329,29),(329,69),(329,72)])
res('Purchase / fine / control','Wei captives and Poison Scorpion','Morethan30Weicaptivesbought,priceunreported. Assaultfine49paid50. ThreePoisonScorpionproducesTwoDung;weeklystingantidoteconsumesnoessence. AssistedtransfernextdaytoXinCi. Trainingpromisednotalreadycomplete.',[(330,23),(330,25),(330,34),(330,37),(330,39),(330,42),(330,55),(330,57),(330,58),(330,82)])
res('Breakthrough / plan','FYFourinitial and Charge fusion pending','BaiFourinitialassistsFYtoFourinitial. NineEyecanthenproduceFourmiddleessence,notadvancementtoFourmiddle. CombinedHorizontalVerticalChargeonlyplanned33175; outcomeunreportedby335.',[(331,48),(331,49),(331,56),(331,60),(331,75),(335,70)])
res('Fine / token destruction / recruitment','Zhou submits alive','Bai500prepaidfine/damage;notexactfinalbill. FYownPurpleThorntokendestroyed33281. Zhoubeatenbutnotkilled,submits33356. Baitokennotshownlost.',[(332,37),(332,66),(332,81),(333,54),(333,56)])
res('Business growth / office','XinCi junior lord appointed','300000→440000after7days=140000increase. Months laterwinsvacancy;finalwealthunreported. Noassumed300000additionalprofitortwoappointments.',[(333,69),(333,72),(333,78),(333,79)])
res('Parallel ownership / mission','True Fang Zheng cranes and bookworm','Fourmiddle;>10000IronBeakcranesincludingmyriadking. Sunhundredsoflightningcranes,3hundredkingsand1injuredthousandking. Elitepromotion;bookwormreceivedunreadbefore2dayssleep. WhiteFoxinheritancenotwon.',[(334,35),(334,45),(334,75),(334,96),(335,14),(335,20),(335,30),(335,33)])
res('Future rewards / present encounter','Assassins and lava crocodiles','JiaoHuang/MengTuThreepeak;>10000andYellowPeartokenspromisednotpaid. FY/BaibothFourinitial, FYessenceFourmiddle.1000pluscrocsandthousandking; noresultorlootby335.',[(335,55),(335,56),(335,57),(335,66),(335,70),(335,72),(335,73)])
# Carry the Batch016 second-pass qualifications into the current resource register.
for v in resources:
 if any(z['chapter']==304 and z['paragraph']==80 for z in v['sources']):
  v['status']='Batch016 fact-check controls: 92→93 endpoints verified, but the two-point retrospective baseline remains unresolved; no numerical emendation selected.'
np=sum(len(c['paragraphs']) for c in batch);nc=sum(sum(map(len,c['paragraphs'])) for c in batch);tp=sum(len(c['paragraphs']) for c in cs);tc=sum(sum(map(len,c['paragraphs'])) for c in cs)
save('proposal-ledger.json',ledger);save('chronology-register.json',dict(scope='Sequential through335; personal, external, remembered and institutional clocks distinguished',entries=events));save('resource-register.json',dict(scope='Sequential through335; inventories, assets, loans, provenance and pending transfers distinguished',entries=resources))
progress=load('history/before-batch017-reading-progress.json');progress.update(sequential_chapters_completed=list(range(1,336)),paragraphs_read=tp,paragraph_characters_read=tc,next_chapter=336,remaining_chapters=1999,batch_report='Batch-017-Chapters-316-335.md',scope='Full sequential Chinese-source reading through335; selected external fact-checks, not fresh bilingual/live-site audit',whole_novel_chronology_verified=False)
progress['batches'].append(dict(id='017',chapters=[316,335],paragraphs=np,characters=nc,reading_segments='Ten complete untruncated two-chapter outputs; expanded20'))
progress['chapters'] += [dict(chapter=c['corpus_chapter'],file=c['file'],title=c['title'],paragraphs=len(c['paragraphs']),first_paragraph=1,last_paragraph=len(c['paragraphs'])) for c in batch];save('reading-progress.json',progress)
save('batch-017-reading-log.json',dict(status='Complete',endpoint=335,next_unread=336,segments=[dict(chapters=[a,a+1],status='Full paragraph sequences read; untruncated',paragraphs=sum(len(by[n]['paragraphs']) for n in [a,a+1])) for a in range(316,336,2)],note='Actual sequential reading, not extraction-only coverage. Selected older passages reread for fact-checking. No original source changes or invented timestamps.'))
stand=load('history/before-batch017-working-standards-register.json');stand['coverage_through']=335
for v in stand['entries']:v['batch017_update']='Through335, retain provisional status. Distinguish source reading, translation equivalence, suspected inconsistency and chosen emendation. Batch016 fact-check addendum remains authoritative, with329p77 strengtheningSR136.'
# The verification protocol is a review method, not a thirteenth certified story standard.
save('working-standards-register.json',stand)
ws=['# Working standards through Chapter335','Twelve working standards, not whole-novel certification or approval to edit.']
for v in stand['entries']:ws += [f"## {v['id']}: {v['topic']}",v['rule'],v['status'],v['batch017_update']]
(r/'WORKING-STANDARDS.md').write_text('\n\n'.join(ws))
text=['# Numbered Chinese source: Chapters316–335','All original paragraph text and numbering retained. No reader-facing omissions in this batch. Original EPUB unchanged.']
for c in batch:text += [f"## Corpus chapter {c['corpus_chapter']}: {c['title']}",f"Volume: {c['volume']} | EPUB: {c['file']}"]+[f"{i}. {reader(c['corpus_chapter'],i,t)}" for i,t in enumerate(c['paragraphs'],1)]
(r/'Batch-017-Numbered-Chinese-Source.md').write_text('\n\n'.join(text))
for name,vs in [('Chronology',ne),('Resources',nr)]:
 out=[f'# Batch017 {name} jotter','All provisional; no substantive source edits.']
 for v in vs:
  out += [f"## {v['id']}: {v.get('event',v.get('entry'))}",v.get('constraint',v.get('calculation'))]
  for z in v['sources']:out += [f"Ch{z['chapter']} p{z['paragraph']}",'> '+z['text']]
 (r/'jotters'/f'Batch-017-{name}.md').write_text('\n\n'.join(out))
out=['# Batch017 continuity and proposal jotter','All candidates held; confidence in an issue differs from confidence in its repair.']
for v in new:
 out += [f"## {v['id']}: {v['category']}"]+[f"**{k}:** {v[k]}" for k in ['recommended_action','rationale','confidence','dependencies']]
 if v['id']!='SR-146':
  for z in v['locations']:out += [f"Ch{z['chapter']} p{z['paragraph']}",'> '+src(z['chapter'],z['paragraph'])['text']]
 for z in v.get('copy_items',[]):out += [f"Ch{z['chapter']} p{z['paragraph']}: {z['original']} → {z['replacement']}. {z['confidence']}. HOLD."]
(r/'jotters/Batch-017-Continuity.md').write_text('\n\n'.join(out))
(r/'jotters/Batch-017-Preserve.md').write_text('''# Batch017 preservation cautions

-316 public Three-middle is concealed actual Three-peak; no correction.
-319 peak fighting condition is not a cultivation substage. Eight beasts is current body capacity, not a universal fixed rule.
-Hard Qi deliberately invalidates Wei’s apparent armour-opening analysis. Strength Qi is a separate Gu, reverse-refined from Feng Qi; Bitter Strength was acquired311.
-Strength Qi reserve percentages are aperture-capacity points, not percentages repeatedly taken from a shrinking balance.
-321 family-origin rumour, relationship gossip,325 Grey Bone letter and333 dying-wife story are false or staged, not narrator facts to harmonise.
-326 Nine Eye has no head eyes, but nine body eyes. Do not invent a contradiction.
-327 Two/329 One is a real source query, but329 may reflect character knowledge.325 upper/332 peak allows unshown recovery. Neither automatically licenses a repair.
-328 token backstory,329 alternate seller’s20years,322 exile3years and334 exam3/8/15yearcycles are not added to current elapsed time.
-乌 clan of Three Kings revenge is not automatically武 great clan. Shared Xiong surname does not establish QingMao ancestry.
-2.4m assets is not debt-free cash; loan repayments still unitemised. XinCi profit200000 and capital300000 are distinct.
-331 combined Charge Gu is only a plan;335 Fourmiddle essence is not Fourmiddle cultivation.
-FY destroys ownPurpleThorn token, Zhou survives. Bai’s token not lost. WhiteFox inheritance not won; finalcrocodilebattleunfinished.
-Historical geography and fantasy dimensions are not automatically shrunk. Institutional exam timing does not date enrolment.
-Source and live English translation are separate objects; this is not a fresh live-site audit.
''')
# Assemble an evidence-rich report, including exact source anchors and qualified candidate list.
report=[f'# The Omniarch: Sequential Review, Chapters316–335',f'Batch017 | Expanded20-chapter batch | {np:,} paragraphs | {nc:,} paragraph characters',f'Coverage now1–335 of2,334. Next unread336. Cumulative{tp:,} paragraphs / {tc:,} characters. All substantive edits held. Original EPUB unchanged.','## Scope and verification','Ten complete untruncated two-chapter reading segments. Eight selected external Chinese captures and dictionary research supplement, not replace, reading. No claim that every copy candidate has been independently collated. Batch016 second-pass corrections remain in the current ledger; no historical generator was rerun to restore superseded confidence.','## Main decisions',
'1. SR140: narrow the Four-Flavour Liquor Worm non-use retrospective rather than erase its earlier use.\n2. SR141: XinCi Two/One within one festival is a qualified source-stage query.\n3. SR142: Sun Yuan Hua has two Chinese spellings in one duel; English romanisation need not change.\n4. SR143: preserve the explicit tripling100000→300000, not three doublings.\n5. SR144: Xiaodie GradeB aptitude has an attested Chinese variant supporting the correction.\n6. SR145: Zhouupper/peak remains a restoration/viewpoint query.\n7. SR146: individual copy candidates, not blanket approval.',
'## Earlier findings revisited','SR136 is strengthened:329p77 explicitly calls ShangBuLi家老. Preferred306 elder repair now has direct later-source office evidence, though the checked306 repost still reads族长. SR118 former-lifeChaoFeng clan-head correction reinforced326p84. SR099 remains withdrawn. SR135 baseline query remains unresolved despite Bai now96%. SR137 Hail/IceExplosion variant remains as documented in Batch016 addendum; no source selection made. Earlier94copyitems not collectively certified.',
'## Exact evidence and proposed actions']
for v in new[:-1]:
 report += [f"### {v['id']}: {v['category']}",v['recommended_action'],'**Reason:** '+v['rationale'],'**Confidence:** '+v['confidence'],'**Dependencies / status:** '+v['dependencies']+' HOLD; unapproved and unapplied.']
 for z in v['locations']:
  if v['id']=='SR-142' and z['paragraph'] not in [22,26,96,18]:continue
  if v['id']=='SR-143' and z['chapter'] not in [323,325,333]:continue
  report += [f"Ch{z['chapter']} p{z['paragraph']}",'> '+src(z['chapter'],z['paragraph'])['text']]
report += ['## Fact-check sources and provenance','These pages are external repost witnesses, not authenticated authorial editions. Different chapters on one site are not independent transmission traditions. Exact sentence presence was checked; the site’s scrambled/duplicated presentation was not used for paragraph order. HTML and SHA256 records saved underfact-check-017/.']
for v in load('fact-check-017/external-witnesses.json'):
 report += [f"Ch{v['chapter']}: {v['url']}"]
 if v['chapter']==325:report += ['External Xiaodie reading: 有乙等资质; supplied EPUB: 有乙等修为.']
report += ['Dictionary: https://www.zdic.net/hans/翻番 and https://zdic.net/hans/翻一番. Standard翻番 concerns doubling; the explicit narrative accounts establish tripling here. Do not convert this source imprecision into an800000 balance.','## Chronology and resource findings']
for v in ne:report += [f"### {v['id']}: {v['event']}",v['constraint'],refs(v['sources'])]
for v in nr:report += [f"### {v['id']}: {v['entry']}",v['calculation'],refs(v['sources'])]
report += [f'## SR146: {len(fixes)} individually held copy candidates','These source-side candidates have been checked against the supplied EPUB paragraphs. They have not all been externally verified; moderate items are reconstructions, not proven errors. Original quotations remain unchanged.','| Chapter / paragraph | Original | Candidate | Confidence |','|---|---|---|---|']
for z in new[-1]['copy_items']:report += [f"| {z['chapter']} / {z['paragraph']} | {z['original']} | {z['replacement']} | {'Moderate; query' if 'Moderate' in z['confidence'] else 'High local; collate'} |"]
report += ['## Chapter-by-chapter close-reading record',(r/'jotters/batch-017-working.md').read_text().split('## 316:')[1].join(['## 316:','']) if False else (r/'jotters/batch-017-working.md').read_text(),
'## Endpoint335','FY and Bai are both RevolutionFourinitial. FY can useNineEye to produceFourmiddle essence. Bai’s last explicit aptitude is96%. XinCi has won the junior-lord vacancy; finalcompetitioncashunreported. FY’sPurpleThorntokenisdestroyed;Bai’sisnot. GiantSpiritWillacquired; FengQiconsumedintoStrengthQi; NineEyeobtained. CombinedChargefusionnotconfirmed. TrueFangZhengFourmiddle,elitepromotionandWhiteFoxmission,notinheritancevictory. FY/Baifaceathousand-kingLavaCrocodilepack;fightoutcomeunknown.',
'## Saved state and backup boundary',f'{len(ledger)} proposals; {len(ledger)-2} held, SR047/SR099 withdrawn. {len(events)} chronology entries / {len(resources)} resource entries /12 working standards. Fivejotters, numberedsource, readinglog, workbook andfact-checkcaptures saved. RemoteverifiedsnapshotremainsChapter315 andpredatesBatch016fact-checkcorrections. ThisChapter335packagehasnotbeenremotelyuploaded. No manuscript or site changes applied.']
report_text='\n\n'.join(report)
import re
report_text=re.sub(r'(?m)(^\|[^\n]*\|)\n\n(?=\|)',r'\1\n',report_text)
(r/'Batch-017-Chapters-316-335.md').write_text(report_text)
# Reuse cumulative export formatting, while preserving later fact-check qualifications.
old=(r/'update_batch010.py').read_text();wb=old[old.index('# Workbook: cumulative'):old.index("(r/'CURRENT-STATUS.md').write_text")]
wb=wb.replace('1–220 of2334','1–335 of2334').replace("('Next unread',221)","('Next unread',336)").replace('103total;102activeheld;1withdrawn','146total;144held;2withdrawn').replace('range(10,0,-1)','range(17,0,-1)').replace("v['batch010_update']","v['batch017_update']").replace('Batch-010-Chapters-201-220','Batch-017-Chapters-316-335').replace('CHAPTERS201–220','CHAPTERS316–335').replace('Chapters201–220','Chapters316–335').replace('Twenty complete chapters; personal clocks and inventory scope distinguished','Twenty complete chapters; selected external fact-checks and qualified proposals').replace('Ch151,201p22,203p84 restricted excerpts','Ch151,201p22,203p84,250,258,296,303 restricted excerpts')
wb=wb.replace("v['publication_status'],'No','No',latest]","v['publication_status'],'No','No',v.get('latest_update',latest)]")
exec(compile(wb,'workbook-and-docx','exec'))
(r/'CURRENT-STATUS.md').write_text(f'''# Sequential review checkpoint:335

Batch017 Chapters316–335 fully read in10 untruncated segments;{np}paragraphs/{nc}characters. Cumulative{tp}/{tc};next336;1999chaptersremain. Larger20-chapterbatchcompletedwithoutskimming.

{len(ledger)}proposals,{len(ledger)-2}heldandSR047/SR099withdrawn. {len(events)}chronology/{len(resources)}resources.12workingstandards. NewSR140–146 include{len(fixes)}copycandidates. Fact-checkwitnesses121/145/325/326/327/329/332/334anddictionarychecks. Sourcequotationsvalidated;originalEPUBunchanged.

Batch016fact-checkcorrectionsretained.329p77strengthensSR136elderrepair. SR137stillvariantquery;SR135baselineunresolved;SR099withdrawn. Do not rerun pre-fact-check generators over current state.

ReportBatch-017-Chapters-316-335.md/.docx;numberedChinesesource;fivejotters;readinglog;fact-check-017/. Endpoint:FY/BaiFourinitial,FYFourmiddleessence;Bailast96%.XinCijuniorlordappointed;FYtokenbroken;Zhoualive. TrueFangZhengFourmiddleandelite. Crocodilefightnotresolved,combinedChargefusionnotconfirmed.

Remoteverified315commit8d542c76b5adddfeaf62a192c2b3ea1936e97767predatesBatch016fact-checkupdatesandall017work. No335backupclaimed. No manuscript/site edits. IndependentexportQAandpresentationpendingaftergenerator.
''')
sha=hashlib.sha256(Path('/home/user/benchmark/sources/Gu-Zhen-Ren.epub').read_bytes()).hexdigest();assert sha==progress['source_sha256'];assert len(ledger)==146
assert all(not v.get('approved') and not v.get('applied') for v in ledger)
for v in ne+nr:
 for z in v['sources']:assert z['text']==src(z['chapter'],z['paragraph'])['text']
assert next(v for v in ledger if v['id']=='SR-137')['category'].startswith('Chinese textual variant')
assert 'baseline' in next(v for v in ledger if v['id']=='SR-135')['recommended_action']
qa=dict(batch='017',chapters=20,paragraphs=np,characters=nc,cumulative_paragraphs=tp,cumulative_characters=tc,proposal_count=len(ledger),held=len(ledger)-2,copy_candidates=len(fixes),chronology=len(events),resources=len(resources),reading_segments=10,next_unread=336,source_sha256=sha,source_unchanged=True,substantive_changes_applied=False,batch016_factcheck_preserved=True,external_captures=8,remote_uploaded=False)
save('batch-017-qa.json',qa);print(json.dumps(qa,indent=2))
