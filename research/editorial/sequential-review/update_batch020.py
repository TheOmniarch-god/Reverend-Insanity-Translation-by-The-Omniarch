from pathlib import Path
import json,shutil,hashlib,re
from openpyxl import Workbook,load_workbook
from openpyxl.styles import Font,PatternFill,Alignment
r=Path('/home/user/editorial/sequential-review')
def load(n):return json.loads((r/n).read_text())
def save(n,v):(r/n).write_text(json.dumps(v,ensure_ascii=False,indent=2))
for n in ['reading-progress.json','proposal-ledger.json','chronology-register.json','resource-register.json','working-standards-register.json']:
 p=r/'history'/('before-batch020-'+n)
 if not p.exists():shutil.copy2(r/n,p)
cs=sum([load(f'batch-{i:03d}-source.json') for i in range(1,21)],[]);by={c['corpus_chapter']:c for c in cs};batch=[by[n] for n in range(366,386)]
def src(c,p):return dict(chapter=c,paragraph=p,file=by[c]['file'],text=by[c]['paragraphs'][p-1])
def ss(rr):return [src(*z) for z in rr]
def loc(rr):return [{k:v for k,v in z.items() if k!='text'} for z in ss(rr)]
def refs(z):return '; '.join(f"Ch{x['chapter']} p{x['paragraph']}" for x in z)
old18=(r/'update_batch018.py').read_text();exec(old18[old18.index('def reader('):old18.index('ledger=load(')])
ledger=load('history/before-batch020-proposal-ledger.json');new=[]
def pro(i,cat,rr,action,why,conf,dep):
 v=dict(id=f'SR-{i:03d}',category=cat,locations=loc(rr),recommended_action=action,rationale=why,confidence=conf,status='Provisional proposal or query; no approval',dependencies=dep,approved=False,applied=False,publication_status='HOLD: full2334-chapter reading and global reconciliation outstanding');ledger.append(v);new.append(v);return v
pro(165,'Six Five-Revolution cultivators: three inconsistent summaries',[(375,76),(375,79),(375,82),(376,27),(378,119),(380,31),(380,66),(381,49),(381,61),(382,81),(383,13),(384,6),(385,25),(385,30),(385,31)],'Preferred381p61 共有五位→共有六位;384p6 杀了四位→杀了五位. If385p31 intends the exhaustive summary implied by p30, add王逍 to the list and change这五个人→这六个人. English: six Revolution Five Gu Masters; had already killed five Revolution Five Gu Masters.','The arrival sequence and376 explicitly establish six. Five die before the encounter with Qiu Jiu. The381 sentence itself enumerates six people after saying five. The385 list contains only five actual names and omits Wang, so it is an omission/scope problem rather than a five-name arithmetic failure.','High confidence in six-person census and first two numeral repairs; moderate-to-high confidence in expanding385’s summary.','Single repost repeats the discrepancies, not an authenticated corrected edition. Qiu kills himself before FY destroys the remains; do not force every death verb to mean FY personally delivered the fatal blow. Preserve all six distinct identities.')
pro(166,'Dang Hun Mountain: 魄 versus 魂',[(366,14),(366,41),(366,42),(372,3)],'Preferred366p14 荡魄山→荡魂山. English: Dang Hun Mountain, using the established name rather than introducing Dang Po Mountain.','The same mentor and climb refer to one mountain; the subsequent explicit identification and later usage give荡魂山.','High local referential support; authorial priority unestablished.','Do not globally replace魄 with魂. Other soul terminology may deliberately distinguish them. Checked repost contains the same initial variant.')
pro(167,'Tie Ruo Nan dialogue: Fang Yuan amid the Fang Zheng alias',[(370,67),(370,68),(374,62),(374,63),(376,36)],'Preferred370p68 唯有方源察觉→唯有方正察觉. English candidate: Only Fang Zheng detected it.','She uses方正 immediately before and again within the same speech, and continues to address him that way later. The isolated方源 appears to be an alias slip.','High local alias-pattern support; moderate-to-high correction confidence.','Do not alter narrator references to Fang Yuan. If later evidence proves she knowingly alternates identities here, reassess. This installment does not establish such a disclosure; the repost repeats方源.')
pro(168,'望其项背: idiom polarity versus inability to compete',[(370,48)],'Preferred contextual English: Even Yi Huo could not hope to match this veteran, much less contend with him. Chinese candidate: 他易火也难以望其项背，根本不能和他争锋.','HanDian defines望其项背 as being able to approach or match another’s level. The affirmative只能 phrase therefore jars with the immediately stated inability to compete. The candidate follows the explicit surrounding sense.','High confidence in standard idiom sense and intended inferiority; moderate-to-high confidence in a source-level polarity repair.','A literal trailing-behind image may have been intended instead of the standard idiom. Rewording is an editorial interpretation, not recovered authorial text. Keep quoted source and do not present this as an observed live-English mistake.')
pro(169,'Yun Luo Tian: wind path versus cloud path',[(375,73),(382,37)],'Retain both labels in the evidence register. Translate风道 as wind path and云道 as cloud path; select no replacement yet.','His introduction labels him wind path, while the looting account identifies cloud path. Both occur in the checked repost.','High quotation confidence; moderate continuity tension; low confidence in which label, if either, requires correction.','Mixed cultivation or related disciplines remain possible. Names and Gu possession do not prove mutually exclusive path membership. Do not collapse cloud into wind merely to hide the distinction.')
pro(170,'Nine million mu and the Brunei comparison',[(383,44),(383,45),(383,47),(383,48)],'Optional precision clarification: On Earth, that would be roughly the size of Brunei. Retain nine million mu; do not change it to an exact modern-country equivalent.','At the modern conversion of1500mu perkm²,9000000mu=6000km². Britannica gives Brunei5765km², a difference of235km² or about4.1%. This is a reasonable rough comparison, not exact equality.','High conditional arithmetic confidence; moderate need for editing, since narrative comparisons may already be approximate.','Modern-mu conversion is explicit as an assumption, not a universal claim about all fictional land units. No systematic geographical rescaling. Original full area and reduced current area are different states.')
pro(171,'Immortal essence reserve mislabelled as primeval essence',[(377,65),(377,66),(379,66),(379,69),(379,70),(379,71),(383,7),(383,10)],'Preferred local substitutions:379p66 鼎底的真元→鼎底的仙元;379p70 十份真元→十份仙元;383p10 八份真元→八份仙元. English: immortal essence in these three budget references.','The cauldron, sixteen-part division and refinement costs all refer to immortal essence. The surrounding lines consistently use仙元. Primeval stones are a substitute for part of the cost, not proof that the cauldron suddenly contains ordinary primeval essence.','High local referential and terminology support; no claim of an authenticated corrected witness.','Preserve genuine真元 elsewhere, including mortal aperture seas. Do not globally replace the term. Budget quantities are conserved; the proposal only repairs the resource label.')
fixes=[(367,12,'郊游广阔','交游广阔'),(367,66,'在做的各位','在座的各位'),(368,4,'干女儿一样','干女儿一眼'),(368,31,'压力重生','压力重重'),(368,38,'一但','一旦'),(368,57,'似的的','似的'),(368,60,'扳不会来','扳不回来'),(368,81,'压力重生','压力重重'),(369,48,'寒风陡峭','寒风料峭'),(370,67,'过人此处','过人之处'),(371,38,'星辰银色','形成银色'),(372,8,'雪白无暇','雪白无瑕'),(373,36,'肉沫','肉末'),(373,45,'狐魅儿','狐媚儿'),(373,59,'变向延长','变相延长'),(373,61,'源自中州','源自中洲'),(374,11,'若在配合','若再配合'),(374,51,'单打独头','单打独斗'),(374,61,'但老人欣慰','老人欣慰'),(374,63,'授首之','斩杀之'),(374,72,'地宅','地灾'),(375,2,'成沙石变成','从沙石变成'),(375,13,'已经再为','已经在为'),(376,19,'忽然将骚动','忽然骚动'),(376,54,'真是云家的','正是云家的'),(376,64,'代表这云家','代表着云家'),(377,5,'方源就要杀死','方源就要被杀死'),(377,21,'平衡的声音','平静的声音'),(377,41,'力道蛊是','力道蛊师'),(378,32,'宝云中空','宝玉中空'),(378,79,'沙硕','沙砾'),(379,25,'冒然使用','贸然使用'),(380,45,'散修出生','散修出身'),(380,88,'勾通外界','沟通外界'),(381,53,'方源也不例外','方源也不意外'),(382,9,'我到愿意','我倒愿意'),(382,59,'变得如光滑','变得光滑'),(383,32,'稳着稳打','稳扎稳打'),(383,34,'尤可活','犹可活'),(384,47,'毅然绝然','毅然决然'),(384,53,'费劲心机','费尽心机'),(385,31,'若真打独斗','若单打独斗'),(385,38,'都要想打量','都要先打量')]
moderate={(368,31),(368,81),(369,48),(374,61),(374,63),(377,21)}
v=pro(172,'Individually held copy candidates',sorted(set((c,p) for c,p,a,b in fixes)),'Review each candidate independently. Simple duplication, miswritten particles and name/collocation repairs are not collective manuscript approval.','Every original fragment is checked against its actual paragraph. Repost agreement cannot establish authorial correctness. Ambiguous pressure, wind, connective and voice wording remain reconstructions.','High local support for mechanical items; moderate for explicitly marked reconstructions.','No automatic楞→愣,金钢→金刚,乌七→乌漆 or stylistic overhaul of unusual language. First determine whether a passage is erroneous, then whether a unique repair is supported.')
v['copy_items']=[]
for c,p,a,b in fixes:
 assert a in src(c,p)['text'],(c,p,a)
 v['copy_items'].append(dict(chapter=c,paragraph=p,original=a,replacement=b,confidence='Moderate; reconstruction/query' if (c,p) in moderate else 'High local; not authenticated authorial wording',status='HOLD; unapproved and unapplied'))
for z in v['copy_items']:
  if (z['chapter'],z['paragraph']) in [(374,51),(374,72),(382,9)]:z['external_variant']='Proposed replacement attested in corresponding repost sentence; authorial priority unknown.'
save('batch-020-copy-candidates.json',v['copy_items'])
for v in ledger:
 if v['id']=='SR-153':
  v['history_before_batch020']={k:v.get(k) for k in ['recommended_action','confidence','status','dependencies','publication_status','latest_update']}
  v['locations']+=loc([(368,41),(368,43),(368,44),(368,45),(368,69),(378,117)])
  v.update(status='Resolved locally by later explicit evidence; no correction required',recommended_action='Preserve the source. Three-Revolution All-Out Effort cannot deliberately trigger the upgraded Four phantoms; they can still manifest by chance. Do not invent an upgrade.',confidence='High: explicit narration368p44 plus contextual explanation41–45, lucky activation69 and378p117.',dependencies='Local mechanics resolved; whole-novel terminology and later changes remain to be read.',publication_status='No emendation proposed for this resolved issue; not global certification')
  v['batch020_update']='Resolved by368pp41–45: guaranteed invocation differs from chance activation. Earlier018/019 doubts preserved as history, not silently erased. No source correction or unreported upgrade needed.'
 if v['id']=='SR-004':
  v['locations']+=loc([(379,39)])
  v['dependencies']='379p39, previously cited topically, now fully sequentially rechecked in context and externally collated. Global reconciliation through2334 remains outstanding.'
  v['confidence']='High evidence for the ten-million branch; conditional preferred harmonisation, not proof of authorial priority.'
  v['batch020_update']='379p39, already cited in the earlier topical check, is now sequentially rechecked. It supplies Fang Yuan’s own recollection of slaughtering ten million while refining Spring Autumn Cicada, strengthening the ten-million branch beyond the hostile accusation at1p3.2p11 still says several hundred thousand. Hold the proposed2 repair until global reconciliation; distinct subsets or exaggeration remain alternatives, not established explanations.'
 if v['id']=='SR-147':
  v['locations']+=loc([(366,23),(380,86),(383,44),(383,47),(383,48)])
  v['batch020_update']='380/383 explicitly confirm current Three Kings3×;383 distinguishes former6×;366 HuImmortal5× is a different land. Supports local346 inversion repair without imposing a universal rate.'
 if v['id']=='SR-150':
  v['locations']+=loc([(369,64),(369,71)])
  v['batch020_update']='TieXuanZhi isFourupper369, after months. This can be later advancement and does not automatically contradict earlierFourmiddle or reverse the held352 repair.'
 if v['id']=='SR-161':
  v['locations']+=loc([(366,14),(366,23),(375,29)])
  v['batch020_update']='366/375 return to天鹤上人 for the continuing SoulFlea mentor, strengthening the held365白鹤 correction.'
 if v['id']=='SR-162':v['batch020_update']='367 onward supplies later multi-month skips, but these do not retroactively explain a five-year gap before the364 report. No blanket age correction.368p60 says twenty-something, not an exact new birthday.'
 if 'batch020_update' in v:v['latest_update']=v['batch020_update']
events=load('history/before-batch020-chronology-register.json')['entries'];resources=load('history/before-batch020-resource-register.json')['entries'];ne=[];nr=[]
def ev(t,k,e,c,rr):
 v=dict(id=f'T{len(events)+1:03d}',timeline=t,kind=k,event=e,constraint=c,evidence_status='Source checked; chronological scopes distinguished',dependency='Full-novel reconciliation outstanding; no invented dates',sources=ss(rr));events.append(v);ne.append(v)
def res(k,e,c,rr):
 v=dict(id=f'R{len(resources)+1:03d}',kind=k,entry=e,calculation=c,status='Acquired, consumed, observed, reported and prospective states distinguished',sources=ss(rr));resources.append(v);nr.append(v)
ev('Parallel Central Continent','rate / forecast','HuImmortal fivefold clock','Outside1day=inside5days. Year-or-half-year climb estimate is prospective/colloquial, not an elapsed eighteen months.',[(366,23),(366,56)])
ev('Revised current life','ellipsis / age','Several months; HundredYearChild over180','Physical8–9 from rejuvenation, not chronological age. Four strength cultivators killed this month; no exact month length or birthdate supplied.',[(367,1),(367,11),(367,21)])
ev('Revised current life','session / later advancement','Feast and Tie elder stage','One shichen feast. Months after previous battle makeFourmiddle→upper advancement possible; do not invent the precise breakthrough date.',[(369,38),(369,64),(369,71)])
ev('Revised current life','opening / report','MuBai inheritance visit','Eight days to opening; news reported three days later; opening more than half a month. Avoid treating reported events as repeated events.',[(370,10),(370,24),(370,38)])
ev('Revised current life','overlapping recap','Hidden cultivation and mountain control','Several months/two openings, warning one month earlier, mountain held over half a year. Different anchors overlap; not an additive calendar sum.',[(371,71),(372,38),(373,2)])
ev('Ren Zu legend','death / separate history','TaiRiYangMang dies','Legendary episode not current elapsed time. Do not convert fantasy wings into ordinary aeronautics.',[(371,63),(371,64)])
ev('Character backstory','career milestones','MuBai ages and rivalry','After42 and before50 atFourpeak are compatible. Earlier50/80/100-plus rivalry intervals need anchor analysis, not blind addition.',[(372,69),(374,44),(374,45),(374,48)])
ev('Revised current life','training / aftermath','Half month after Five battle','Needle tactics take7–8days; lecture more than half a shichen. Neither equals whole mentorship length.',[(374,1),(374,12),(374,22),(374,66)])
ev('Parallel Central Continent','actual assistance / historic use','Soul support begins halfway','375 actual halfway intervention. First immortalGu use80years earlier, secondnow; no calendar date for final climb success.',[(375,18),(375,23),(375,44),(375,58)])
ev('Revised current life','arrival anchors','AdditionalFive arrivals','One-month, more-than-one-month and two-month transitions may share anchors. Further8days afterWu explicit. Do not certify an exact grand total. SixFive present at376.',[(375,70),(375,76),(375,79),(375,82),(376,27)])
ev('Former life / current life','selection comparison','Earlier rescue than remembered failed inheritance','Former applicants and destruction are not current events. Present spirit rescue followsnear-death, not confirmed death/revival.',[(377,7),(377,19),(377,70),(377,71),(377,81)])
ev('Revised current life','internal work / sleep','Five days refining plus one day sleeping','6inside days=2outside days at current3×. This does not date all later killings exactly.',[(378,107),(378,108),(380,86)])
ev('Revised current life','ordered deaths','Six Five-master census','MuBai→KuMo→WuGui→WuLanShan→WangXiao→QiuJiu. Yun isFour and killedbyBai. Qiu suicide then remainsdestroyed. SR165 records discrepant summaries.',[(378,119),(380,31),(380,66),(381,49),(382,81),(385,25),(385,59),(385,60)])
ev('Revised current life','cultivation / offpage progress','FY nowFourupper','379 comparison and383 explicit selfassessment establish actualFourupper. Interveningmonths allowprogress; not justNineEyeessence and notaFivebreakthrough.',[(379,5),(383,31)])
ev('Character habit / former life','recurrence not elapsed','Wang sleep and altered future','Threeshichen≈sixhours daily; notthreehours orpresentwait. His laterYitian role belongs topreviouslife, nowchanged.',[(382,75),(382,76),(382,78),(382,81)])
ev('Blessed-land history','rate change','Originalsixfold/currentthreefold','383 expressly separates former6× fromcurrent3×. Landareaalsoeroded. NoapplyHu5× here.',[(383,44),(383,47),(383,48)])
ev('Former life / current life','revival histories','Qiu earlier resurrection and present destruction','FormerYitian throatkill/revival precedes finalexecution. Currentdeath/remainsdestruction isdifferent branch; noactualrevivalby385.',[(383,27),(385,53),(385,55),(385,56),(385,59),(385,60)])
res('Mechanics / resolved query','Upgraded phantoms andAllOutEffort','ThreeAllOutcannotdeliberatelyinvokeFourforms; randommanifestationpossible. KunlunBullreplacesGreenBull. SR153resolvedwithoutupgrade.',[(368,41),(368,43),(368,44),(368,45),(368,69)])
res('Body upgrades','Ironbones andtendons','Ironbonerefinementcompletedaftermonths. TendonGuspelling金钢筋retained. Noforced金刚normalisation.',[(368,56),(368,57),(368,58),(368,59)])
res('Land rules / mistaken testimony','Spirit notabsent','MuBai374believesnospirit;377BaGuisurvives. Landspiritcannotleaveitsland; One–FiveordinaryrestrictionsandSixexceptiondistinguished.',[(372,20),(372,22),(372,27),(374,71),(377,20),(381,54),(381,55)])
res('Immortal Gu / consumption','我素蛊 threeuses','Oneuse80yearsago, secondnow toprotectSoulFlea; oneleft. FactionownedSixGu, notFangZhengSixcultivation.',[(375,41),(375,42),(375,43),(375,44),(375,58)])
res('Cultivation / census','SixFive stageallocation','MuBai/WuGui/KuMoFivepeak;WangXiao/WuLanShanFiveupper;QiuFiveinitial.375Yunage35 approachingFourpeak. SR165countdiscrepancy.',[(375,73),(376,27),(381,61),(382,40)])
res('Land ownership / prerequisites','BaGui test notcompleted','Sufficientstrength+neardeathadmission. Spiritassistance isnotfullownership. OriginalThreeKingsremainedFive; ancientlandstrengthpath.',[(377,36),(377,37),(377,49),(377,50),(383,11),(384,17)])
res('Prospective capacity','Two90aperturesforecast','377180% meanssumoftwo90reservoirs, notone180aperture. Finalsecondaptitudedependsonplacentarefinement andisnotfixedatthisforecast.',[(377,83),(379,38),(381,59),(382,83),(383,2)])
res('Guarded supplies / probability','Recipe stock notfreepersonalGu','Atleast5000Gu,>600Four,>80Five;>10goldrelics/8purple. Spiritrestrictsuse.Refinementestimate50%→about30%afterfullrecipe. NotnarratedFivepeakadvancement.',[(377,94),(378,15),(378,20),(378,22),(378,25)])
res('Immortal ingredient / intermediate','DivineTravel andplacenta','DivineTravelSixsealed, notconsumedby385. FourbeastphantomsrefinedintoFiveBeastStrengthPlacenta; SecondApertureSixnotfinished. Exactremainingbodystrengthnotcertified.',[(378,36),(378,49),(378,80),(378,83),(378,85),(378,105)])
res('Loot / aptitude','MuBai sevenGu and40%','FiveTouchGold,GoldSoup,VajraGlare;FourGoldDragon,GoldWind,GoldClothes,GoldGlow.98%belongstoMuBai;placenta40afterabsorption. GoldEyemodificationsnotextraunconsumedloot.',[(379,5),(379,7),(379,14),(379,17),(379,25),(379,28),(379,38)])
res('Suppression / ownership transfer','FiveGu refinablethroughlandspirit','CicadapressurealonecurrentlymaxFour; spiritrestrainsFiveenablingrefinement. NoindependentFiveconqueringpowerorordinaryescape-tokenexception.',[(379,58),(379,61),(379,62),(380,32)])
res('Budget / prospective expenditure','Sixteenpartimmortalessencereserve','8refinement+4maintaininginheritance+morethan3killing+lessthan1reserve=16withcomplementaryremainders. FirstMuoperation0.5. Spiritcounterproposal10+2 notsimultaneousactualcost. SR171terminologyquery.',[(379,63),(379,66),(379,69),(379,70),(379,71),(383,7),(383,10)])
res('Currency / substitutable resources','30millionstonesneeded','Atleast30000000topartlyreplaceimmortalessence;FYownsmillionplus, insufficient. Plannedlootingnotconfirmedtotalpayment. Noexactcashbalanceinvented.',[(379,76),(379,78)])
res('Loot / approximate quantities','KuMo/WuGuicollection','KuMo1Five+7Four;WuGui1Five+8or9Four. FiveFiveGuintheseizedset/aperturedoesnoteraseFiveplacentafromoverallinventory. Dogarmiesnotautomaticallyacquired.',[(380,36),(380,39),(380,47),(380,76),(380,79),(380,83),(380,84)])
res('Promise / deployment','Bai protection andYangGu','YangGupromisedonsuccess,nottransferred. BaiDogrouteguidedbyspirit; oathinvocationnotproofagainstunreadloopholes.',[(380,93),(381,8),(381,34),(381,40),(381,41)])
res('Recovered enemy Gu / aptitude','WuLanShan threeFiveescape','Wuclanimmortalrecovers3Five;FYtakesremainingFour. FourFiveaperturesyield75%, not160%. Nonlinear35pointgainafterfirst40.',[(381,51),(381,52),(381,53),(381,56),(381,59),(381,60)])
res('Separate ownership / failed acquisition','YunlootBai;Wumountainnotwon','BaitakesYunGu,sendsbodyforabsorption. FYfailsgetWangpath;killsandlootsWang. CombinedYun/Wangplacenta83%.Killingcost>2parts.',[(382,36),(382,37),(382,38),(382,53),(382,81),(382,82),(382,83)])
res('Geography / historicalextent','Ninemillionmuoriginalarea','Modern1500mu/km²assumptiongives6000km²;Brunei5765km²;roughcomparisonreasonable. Under1%landnow,not9millioncurrentmu. Noshrinkingallfantasyranges.',[(377,43),(383,44),(383,45),(383,48)])
res('Knowledge / historical belief','Cicadadisclosed;venerablelore','FYrevealsCicadaandformerSixexperience. TwoactualCicadausesrecalled. RedLotus/fate/venerableclaimsretainhistoricalspeakerandtimeframes.',[(383,36),(383,42),(383,50),(383,54),(383,60)])
res('Oath types / reportedsect','SeaOath versusPoisonOath','SixSeaOathreusable;PoisonOathconsumable. Destructionoflinkedsea/mountainstatedloophole,nothappened. LoversPoisonOathatsea385notautomaticallysameas384secrecySeaOath.',[(384,25),(384,27),(384,32),(384,38),(384,42),(385,5),(385,6),(385,9)])
res('Final loot / revival prevention','QiumovementGuandremains','OneFiveMovementGu;noFivehealingGu. ConsumedFiveRevivalGueffectcouldreactivateaslandweakens;bodydestroyed/burned/ashesdispersed. Apertureabsorbedwithoutnewstatedpercentage;83lastmeasured,90target.',[(385,44),(385,47),(385,50),(385,54),(385,55),(385,56),(385,59),(385,60),(385,61)])
# Preserve historical entries while explicitly superseding now-resolved mechanics notes.
for v in resources:
 if v not in nr and any(z['chapter'] in [345,353,360,363] for z in v['sources']) and any(s in str(v).lower() for s in ['all-out','allout','guaranteed']):
  v['batch020_update']='See368pp41–45 and SR153: chance activation remains possible; deliberate Three-AllOut invocation of upgradedFour forms is not. Earlier unresolved wording is historical.'
  v['status']='Historical entry; mechanics query locally resolved in Batch020'
  if 'Updated by Batch020' not in v['calculation']:v['calculation']+=' Updated by Batch020:368 explicitly distinguishes chance activation from deliberate invocation; SR153 locally resolved.'
np=sum(len(c['paragraphs']) for c in batch);nc=sum(sum(map(len,c['paragraphs'])) for c in batch);tp=sum(len(c['paragraphs']) for c in cs);tc=sum(sum(map(len,c['paragraphs'])) for c in cs)
save('proposal-ledger.json',ledger);save('chronology-register.json',dict(scope='Sequential through385; overlapping, parallel and former-life clocks distinguished',entries=events));save('resource-register.json',dict(scope='Sequential through385; ownership, observations and forecasts distinguished',entries=resources))
progress=load('history/before-batch020-reading-progress.json');progress.update(sequential_chapters_completed=list(range(1,386)),paragraphs_read=tp,paragraph_characters_read=tc,next_chapter=386,remaining_chapters=1949,batch_report='Batch-020-Chapters-366-385.md',scope='Full sequential Chinese reading through385; selected external collation, not a fresh live bilingual audit',whole_novel_chronology_verified=False)
progress['batches'].append(dict(id='020',chapters=[366,385],paragraphs=np,characters=nc,reading_segments='Ten complete untruncated two-chapter outputs; twenty chapters'))
progress['chapters'] += [dict(chapter=c['corpus_chapter'],file=c['file'],title=c['title'],paragraphs=len(c['paragraphs']),first_paragraph=1,last_paragraph=len(c['paragraphs'])) for c in batch];save('reading-progress.json',progress)
save('batch-020-reading-log.json',dict(status='Complete',endpoint=385,next_unread=386,segments=[dict(chapters=[a,a+1],status='Full paragraph sequences read; untruncated',paragraphs=sum(len(by[n]['paragraphs']) for n in [a,a+1])) for a in range(366,386,2)],note='Actual sequential reading; extraction alone not counted. No invented timestamps.'))
stand=load('history/before-batch020-working-standards-register.json');stand['coverage_through']=385
for v in stand['entries']:v['batch020_update']='Through385 provisional. Explicit368 mechanics resolves SR153 without emendation. Distinguish land-specific/historical rates, counterfactual resources, incomplete inventories, character claims and actual acquisitions. Hail correction and Batch016 qualifications remain controlling.'
save('working-standards-register.json',stand)
ws=['# Working standards through Chapter385','Twelve provisional standards. No source or website edits approved or applied.']
for v in stand['entries']:ws += [f"## {v['id']}: {v['topic']}",v['rule'],v['status'],v['batch020_update']]
(r/'WORKING-STANDARDS.md').write_text('\n\n'.join(ws))
out=['# Batch020: actual numbered Chinese source, Chapters366–385','All paragraphs reproduced from the supplied EPUB with original numbering; no emendations. Full sequential reading complete.']
for c in batch:
 out += [f"## Chapter {c['corpus_chapter']}: {c['title']}",f"EPUB: {c['file']}"]
 out += [f'{p}. {t}' for p,t in enumerate(c['paragraphs'],1)]
(r/'Batch-020-Numbered-Chinese-Source.md').write_text('\n\n'.join(out))
for name,vs in [('Chronology',ne),('Resources',nr)]:
 out=[f'# Batch020 {name} jotter','Held editorial interpretation; exact source follows each entry.']
 for v in vs:
  out += [f"## {v['id']}: {v.get('event',v.get('entry'))}",v.get('constraint',v.get('calculation'))]
  for z in v['sources']:out += [f"Ch{z['chapter']} p{z['paragraph']}",'> '+reader(z['chapter'],z['paragraph'],z['text'])]
 (r/'jotters'/f'Batch-020-{name}.md').write_text('\n\n'.join(out))
out=['# Batch020 continuity jotter','All proposals unapproved and unapplied.']
for v in new:
 out += [f"## {v['id']}: {v['category']}"]+[f"**{k}:** {v[k]}" for k in ['recommended_action','rationale','confidence','dependencies']]
 for z in v['locations']:out += [f"Ch{z['chapter']} p{z['paragraph']}",'> '+src(z['chapter'],z['paragraph'])['text']]
 for z in v.get('copy_items',[]):out += [f"Ch{z['chapter']} p{z['paragraph']}: {z['original']} → {z['replacement']}. {z['confidence']}. HOLD."]
(r/'jotters/Batch-020-Continuity.md').write_text('\n\n'.join(out))
preserve='''# Batch020 preservation controls

- SR153 is locally resolved, not still an active correction query. Preserve its earlier reasoning in history.
- Hail faithfully renders冰雹. The controlling Batch016 research remains unchanged.
- Third-Revolution All-Out Effort need not have been upgraded merely because an upgraded phantom appears.
- Hundred Year Child's appearance, name and actual age are different quantities. Wood and strength need not be mutually exclusive.
- Tie Xuan Zhi can advance across the intervening months. Fang Yuan'sFourupper is now explicit, not merely NineEye-enhanced essence.
- CurrentThreeKings3×, formerThreeKings6×, and HuImmortal5× are distinct rates. Do not merge parallel calendars or mechanically add recap intervals.
- Mu Bai's claim that the spirit is absent is wrong character knowledge, not a narrator error to fix before the reveal.
- 我素蛊 three uses are a special item rule, not a universal consumable-Gu rule.
- The proposed second aperture's180% aggregate does not make one180%-capacity aperture.90%remains a target, not a completed new aperture.
- Stored recipe Gu are guarded inputs. The EightPurpleRelic fantasy does not narrate an actual Five-peak breakthrough.
- GoldEyes body modifications are not demonstrably two additional loot Gu. Soulstrength and bodilystrength need different accounting.
- WuLanShan's threeFive Gu escape via immortal recovery. Bai's Yunloot is not automatically FangYuan's property. Wang's mountain is not acquired.
- Five lootedFive Gu in an aperture list does not erase the separateFive placenta from possessions. No false total based on one storage location.
-16-part budget allocations, counterproposals and overruns are different states; no fabricated final cash total or exact remaining essence.
- Qiu's ShadowSect story is testimony. LoversPoisonOath and secrecySeaOath are not interchangeable just because both mention a sea.
- Qiu's tongue-biting death remains fictional narration, not a medical claim or an invitation to rewrite the scene.
- 乌七 has seven-white-marking support. 金钢 repeated spelling and楞 variants are not mechanically corrected.
- The Brunei comparison is approximately sound under a modern-mu assumption. No mass shrinking of fictional geography.
-385ends afterQiu's remains are destroyed. NoSecondAperture success, Hu inheritance winner,90%placenta measurement or subsequent betrayal claimed.
'''
(r/'jotters/Batch-020-Preserve.md').write_text(preserve)
# Collate every proposed original fragment and substantive key readings against saved witnesses.
d=r/'fact-check-020';coll=[]
for c,p,a,b in fixes:
 text=(d/f'ch{c}-normalized.txt').read_text();coll.append(dict(chapter=c,paragraph=p,original=a,replacement=b,original_in_repost=a in text,replacement_in_repost=b in text))
save('fact-check-020/copy-collation.json',coll)
checks=[(1,3,'杀了千万人的性命'),(2,11,'屠杀了数十万人'),(366,14,'荡魄山'),(366,41,'荡魂山'),(368,44,'还不能随心所欲地催动'),(370,48,'只能望其项背'),(370,68,'唯有方源察觉'),(375,73,'风道蛊师'),(376,27,'五转蛊师就有六位'),(379,39,'屠杀千万人'),(379,66,'鼎底的真元'),(379,70,'十份真元'),(381,61,'共有五位'),(382,37,'走的是云道'),(383,10,'八份真元'),(383,44,'九百万亩'),(384,6,'杀了四位五转蛊师'),(385,31,'这五个人')]
sub=[]
for c,p,a in checks:
 assert a in src(c,p)['text'];text=(d/f'ch{c}-normalized.txt').read_text();sub.append(dict(chapter=c,paragraph=p,fragment=a,in_repost=a in text))
save('fact-check-020/substantive-collation.json',sub)
held=len(ledger)-3
report=[f'# The Omniarch: Sequential Review, Chapters366–385',f'Batch020 | Twenty chapters | {np:,} paragraphs | {nc:,} paragraph characters',f'Completed1–385 of2,334. Next unread386. Cumulative{tp:,} paragraphs / {tc:,} characters. Original EPUB unchanged. No source/site edits.',
'## Executive findings','This installment doubles the preceding ten-chapter batch. All twenty chapters were read in ten complete untruncated outputs. Source extraction and external fragment searches are not substituted for sequential reading. This is a Chinese-source continuity and editorial review, not a new live bilingual audit.',
'1. SR153 is locally resolved: upgraded phantoms may appear by chance, although Three-Revolution All-Out Effort cannot deliberately invoke them. No correction needed.\n2. Six Five-Revolution cultivators are established, but later summaries lose Wang Xiao and miscount prior killings.\n3. Dang Hun Mountain, the Fang Zheng alias, and immortal-essence terminology have strongly supported local correction candidates.\n4. The wind/cloud label discrepancy remains a query, not an automatic path replacement.\n5. The idiom望其项背 requires contextual polarity care. The Brunei comparison needs at most an explicit approximation.\n6. Fang Yuan’s own ten-million recollection strengthens SR004.\n7. Forty-three individual copy candidates are held separately; ambiguous reconstructions are marked.',
'## A previous query resolved without changing the text']
v=next(v for v in ledger if v['id']=='SR-153');report += [v['batch020_update'],v['recommended_action']]
for c,p in [(368,41),(368,44),(368,45),(368,69),(378,117)]:report += [f'Ch{c} p{p}','> '+src(c,p)['text']]
report += ['**Editorial consequence:** update the register, not the novel. SR153 now has resolved-local status. Its prior hypotheses and pre020 ledger remain preserved. All other new substantive proposals remain held.','## Exact evidence and proposed actions']
for v in new[:-1]:
 report += [f"### {v['id']}: {v['category']}",v['recommended_action'],'**Rationale:** '+v['rationale'],'**Confidence:** '+v['confidence'],'**Dependencies / status:** '+v['dependencies']+' HOLD; unapproved and unapplied.']
 for z in v['locations']:report += [f"Ch{z['chapter']} p{z['paragraph']}",'> '+src(z['chapter'],z['paragraph'])['text']]
report += ['## Earlier findings revisited']
for v in ledger:
 if 'batch020_update' in v and v['id']!='SR-153':
  report += [f"### {v['id']}: {v['category']}",v['batch020_update']]
  if v['id']=='SR-004':
   for c,p in [(1,3),(2,11),(379,39)]:report += [f'Ch{c} p{p}','> '+src(c,p)['text']]
report += ['SR134–138 retain the controlling Batch016 fact-check qualifications unchanged. In particular冰雹→Hail remains faithful. New numbers or mechanics have not been made corrections simply because they looked surprising.',
'## External reconfirmation and limitations',f'22 saved Hetushu chapter captures:366–385 plus1–2. Raw HTML SHA256 manifests and normalised text are saved. All{len(sub)} selected substantive fragments checked; {sum(z["in_repost"] for z in sub)} found exactly. Of{len(coll)} copy originals,{sum(z["original_in_repost"] for z in coll)} found exactly; {sum(z["replacement_in_repost"] for z in coll)} proposed replacements found. These are whole-page substring checks, not proof of a variant at the corresponding sentence. Contextual review finds three same-sentence alternatives:374p51单打独斗 against EPUB单打独头,374p72地灾 against地宅,382p9我倒愿意 against我到愿意. The other replacement hits are substrings or usages elsewhere, not corrected witnesses. None establishes authorial priority. This is one repost tradition, not22 independent authorities. Scrambled display order is not used to infer narrative order.']
for z in load('fact-check-020/external-witnesses.json'):report += [f"Ch{z['chapter']}: {z['url']}"]
report += ['HanDian望其项背: 能够看到别人的颈项和脊背。比喻有能力赶上或达到对方的水平。 Supports the idiom analysis, not a uniquely recovered sentence. https://www.zdic.net/hans/%E6%9C%9B%E5%85%B6%E9%A1%B9%E8%83%8C',
'Britannica, Brunei main article, Quick Facts: Total Area (Sq Km):5,765. The editorial comparison uses a stated modern-mu assumption and arithmetic, not a new universal in-world unit law. https://www.britannica.com/place/Brunei',
'## Chronology additions']
for v in ne:report += [f"### {v['id']}: {v['event']}",v['constraint'],refs(v['sources'])]
report += ['## Resources and mechanics additions']
for v in nr:report += [f"### {v['id']}: {v['entry']}",v['calculation'],refs(v['sources'])]
report += [f'## SR172: {len(fixes)} individually held copy candidates','Original source remains unchanged. Moderate rows are optional reconstructions or queries, not recovered canonical readings.','| Chapter / paragraph | Original | Candidate | Confidence |','|---|---|---|---|']
for z in new[-1]['copy_items']:report += [f"| {z['chapter']} / {z['paragraph']} | {z['original']} | {z['replacement']} | {z['confidence']} |"]
report += ['## Chapter-by-chapter working notes',(r/'jotters/batch-020-working.md').read_text(),'## Preserve rather than overcorrect',preserve,
'## Endpoint385','FY is explicitly Revolution Four upper. Second Aperture Gu is unfinished; the Five-Revolution placenta exists.83%is the last measured aptitude before Qiu’s absorption; no final90%asserted. AllsixFive opponents are dead; Qiu’s remains are destroyed. Bai owns Yun’s Gu and is building the dog force. YangGu remains only promised. HuImmortal contest remains unresolved. Nextunread386.',
'## Saved state and backup boundary',f'{len(ledger)} proposal records: {held} held, two withdrawn, one locally resolved without correction. {len(events)} chronology and {len(resources)} resource entries; twelve provisional standards. Full actual source, five jotters, report, workbook and QA. GitHub backup remains verified through365 only unless a separate385 upload receipt is generated. No credential was recovered or invented to claim a new upload.']
report_text=re.sub(r'(?m)(^\|[^\n]*\|)\n\n(?=\|)',r'\1\n','\n\n'.join(report));(r/'Batch-020-Chapters-366-385.md').write_text(report_text)
old=(r/'update_batch010.py').read_text();wb=old[old.index('# Workbook: cumulative'):old.index("(r/'CURRENT-STATUS.md').write_text")]
wb=wb.replace('1–220 of2334','1–385 of2334').replace("('Next unread',221)","('Next unread',386)").replace('103total;102activeheld;1withdrawn',f'{len(ledger)}total;{held}held;2withdrawn;1locallyresolved').replace('range(10,0,-1)','range(20,0,-1)').replace("v['batch010_update']","v['batch020_update']").replace('Batch-010-Chapters-201-220','Batch-020-Chapters-366-385').replace('CHAPTERS201–220','CHAPTERS366–385').replace('Chapters201–220','Chapters366–385').replace('Twenty complete chapters; personal clocks and inventory scope distinguished','Twenty complete chapters; explicit mechanics resolution and held source corrections').replace('Ch151,201p22,203p84 restricted excerpts','Earlier restricted excerpts retain original omission markers; none newly omitted in366–385')
wb=wb.replace("v['publication_status'],'No','No',latest]","v['publication_status'],'No','No',v.get('latest_update',latest)]")
exec(compile(wb,'workbook-and-docx','exec'))
(r/'CURRENT-STATUS.md').write_text(f'''# Sequential review checkpoint:385

Completed1–385 of2334. Next unread386;1949remain. Batch020 is20chapters,10complete untruncated reading outputs: {np}paragraphs/{nc}characters. Cumulative{tp}/{tc}.

{len(ledger)}proposal records: {held}held,2withdrawn,1locally resolved. SR153resolvedby368 without source correction; SR165–172new, including{len(fixes)}copycandidates. {len(events)}chronology/{len(resources)}resources;12provisional standards. OriginalEPUBunchanged; no source/site edits.

22external chapter captures; individualcopyandsubstantivecollation. DictionaryidiomandBruneiarea factchecks. Batch016Hailqualificationspreserved. IndependentexportQA pending aftergenerator.

Endpoint:FYFourupper,SecondApertureunfinished,83%lastmeasuredbeforeQiuabsorption,90targetnotachievedoncamera. SixFiveopponentsdead;Qiuashesdispersed. BaiDogforce/Yunloot;YangGupromisedonly. Huinheritanceunfinished.

Remote verifiedthrough365: data9bc0ee614fb53c335a7278159f8a41814c542582;metadata8618c5ad1878efb1de91096d9e1d0f23e9b475f7.385notuploaded orclaimed. No localdeletions. Nextbatch386onward.
''')
sha=hashlib.sha256(Path('/home/user/benchmark/sources/Gu-Zhen-Ren.epub').read_bytes()).hexdigest();assert sha==progress['source_sha256'];assert len(cs)==385 and len(ledger)==172 and len(fixes)==43
assert all(not v.get('approved') and not v.get('applied') for v in ledger)
baseline=load('history/before-batch020-proposal-ledger.json')
for id in ['SR-134','SR-135','SR-136','SR-137','SR-138']:assert next(v for v in ledger if v['id']==id)==next(v for v in baseline if v['id']==id)
for v in ne+nr:
 for z in v['sources']:assert z['text']==src(z['chapter'],z['paragraph'])['text']
texts={t for c in cs for t in c['paragraphs']}
for line in report_text.splitlines():
 if line.startswith('> '):assert line[2:] in texts
qa=dict(batch='020',chapters=20,paragraphs=np,characters=nc,cumulative_paragraphs=tp,cumulative_characters=tc,proposal_count=len(ledger),held=held,withdrawn=2,resolved_local=1,copy_candidates=len(fixes),chronology=len(events),resources=len(resources),reading_segments=10,next_unread=386,source_sha256=sha,source_unchanged=True,substantive_changes_applied=False,batch016_factcheck_preserved=True,external_captures=22,remote_uploaded=False,remote_verified_through=365)
save('batch-020-qa.json',qa);print(json.dumps(qa,indent=2))
