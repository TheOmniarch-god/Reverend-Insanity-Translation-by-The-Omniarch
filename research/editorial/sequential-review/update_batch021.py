from pathlib import Path
import json,shutil,hashlib,re
from openpyxl import Workbook,load_workbook
from openpyxl.styles import Font,PatternFill,Alignment
r=Path('/home/user/editorial/sequential-review')
def load(n):return json.loads((r/n).read_text())
def save(n,v):(r/n).write_text(json.dumps(v,ensure_ascii=False,indent=2))
for n in ['reading-progress.json','proposal-ledger.json','chronology-register.json','resource-register.json','working-standards-register.json']:
 p=r/'history'/('before-batch021-'+n)
 if not p.exists():shutil.copy2(r/n,p)
cs=sum([load(f'batch-{i:03d}-source.json') for i in range(1,22)],[]);by={c['corpus_chapter']:c for c in cs};batch=[by[n] for n in range(386,406)]
def src(c,p):return dict(chapter=c,paragraph=p,file=by[c]['file'],text=by[c]['paragraphs'][p-1])
def ss(rr):return [src(*z) for z in rr]
def loc(rr):return [{k:v for k,v in z.items() if k!='text'} for z in ss(rr)]
def refs(z):return '; '.join(f"Ch{x['chapter']} p{x['paragraph']}" for x in z)
s=(r/'update_batch018.py').read_text();exec(s[s.index('def reader('):s.index('ledger=load(')])
oldreader=reader
def reader(c,p,t):
 if (c,p)==(405,173):return '[Restricted passage omitted from reader-facing copy. Original numbering retained; original EPUB unchanged.]'
 return oldreader(c,p,t)
ledger=load('history/before-batch021-proposal-ledger.json');new=[]
def pro(i,cat,rr,action,why,conf,dep):
 v=dict(id=f'SR-{i:03d}',category=cat,locations=loc(rr),recommended_action=action,rationale=why,confidence=conf,status='Provisional proposal or query; no approval',dependencies=dep,approved=False,applied=False,publication_status='HOLD: full2334-chapter reading and global reconciliation outstanding');ledger.append(v);new.append(v);return v
pro(173,'Rewind boundary: Yun Luo Tian aperture appears consumed twice',[(382,56),(382,60),(382,83),(399,37),(399,51),(399,69),(400,38),(400,39)],'Retain the original sequence and flag the reset anchor. Do not book a second Yun aperture into the revised inventory. A possible local repair is400p38 吞噬了他和云落天的空窍→吞噬了他的空窍, if the rewind is fixed at the repeated382p60 speech.','382p56 absorbs Yun before Wang speaks at60.399 returns at that speech.400 then again narrates absorption of both men. The83% result agrees across branches, but the stated order appears to double-count Yun.','High confidence in the sequencing tension; moderate confidence in deleting Yun from400 rather than moving the intended reset point.','The author may have intended a slightly earlier reset or used compressed retrospective wording. No extra aperture, changed percentage, or second Yun death invented. The399 recap alone is not enough to prove the exact order; the repeated speech is the stronger anchor.')
pro(174,'Qiu Jiu trial objective: Second Aperture versus Hundred Battles',[(401,41),(401,43),(401,44),(401,53),(401,54),(401,55),(405,75),(405,77)],'Preferred401p44 斩获第二空窍蛊→斩获百战不殆蛊. English candidate: obtain Invincible Hundred Battles Gu.','The explicit assignment, following delivery and eventual consumption identify Hundred Battles. Second Aperture is being refined separately in the hall and is not a Xin trial reward.','High local correction confidence, additionally supported by the corresponding repost sentence reading百战不殆蛊; authorial priority remains unverified.','Retain Second Aperture everywhere it actually refers to the refinement project. Qiu obtains the reward without clearing the entire inheritance; do not change the two-pillar outcome.')
pro(175,'Five mountain dogs: 恒光 versus 光恒',[(386,74),(386,77),(386,79),(393,57),(394,8)],'Preferred386p79 光恒→恒光 in the five-type list. Preserve the existing English glossary equivalent of Heng Guang rather than introduce another breed.','The same chapter describes恒光 individually, then reverses the characters in the collective list.393/394 return to恒光.','High local referential support; transmitted text is not an authenticated master.','No global reversal of similar names. All five types remain distinct; no extra sixth dog breed.')
pro(176,'Xiao Mang: entering the land versus not entering the inheritance',[(389,7),(389,8),(389,95),(389,96)],'Hold both statements with their different nouns. Do not silently change theOctober21 arrival into an outside-only arrival or invent a narrated exit.','389 says aFive expert entered the blessed land, then later says Xiao Mang came to the mountain without entering the inheritance. This may distinguish land entry from trial participation, or be an actual continuity slip.','High quotation confidence; moderate tension; low confidence in a unique correction.','Unshown exit, difference between福地 and传承, and a loose arrival report are alternatives. None is certified by this installment.')
pro(177,'Xiao Mang title: second clan leader versus second young lord',[(390,23),(392,63),(392,64),(402,82)],'Preferred402p82 萧家二族长→萧家二少主. English candidate: the Xiao clan’s second young lord.','He is addressed as二少主, dislikes that title, and hopes his brother’s death will let him become少族长. The later二族长 appears to omit少 or conflate offices.','High contextual support for the junior-lord reading; no authenticated authorial correction.','Do not promote him to clan chief or presume that every少主 and少族长 elsewhere denotes the same formal office.')
pro(178,'Flower Wine death: compressed ambush causation versus later injury query',[(15,29),(16,32),(156,64),(183,31),(183,32),(183,33),(183,34),(387,29)],'Keep a causation query. If clarification is needed, end the387 historical example after the Fourth leader’s surprise attack and avoid making that alone the proven cause of Flower Wine’s death. Do not replace it with a categorical blood-bat death account.','387 compresses defeat, Slave Gu offer, ambush and death into one history.156 rejects Moon Shadow as the cause of the severe wounds;183 proposes blood bats but explicitly as an inference.','High confidence that the causal accounts require qualification; low-to-moderate confidence that387 demands emendation rather than broad causal compression.','Preserve established attack and eventual death, and separate narrator recap, earlier interpretation, forged public history and later hypothesis. Whole-novel resolution remains pending.')
poem='''Immortals of ages past scatter on the wind;
The Three Kings lie beneath their grassy graves.
Yang Mang fell in sorrow. Who has never failed?
I rise again to reign.
A river hangs from heaven, scouring fish and dragon;
Alone, defying Heaven, I survey the eight horizons.
Today I spread my wings and go;
Tomorrow I ascend immortal, and scourge the phoenix!'''
pro(179,'Closing poem and title: force, imagery and future challenge',[(405,117),(405,118),(405,119),(405,120)],'Held verse draft:\n'+poem+'\nHeld title: Today I Spread My Wings and Go; Tomorrow I Ascend Immortal and Scourge the Phoenix!','Preserve the poem’s movement from dead predecessors through renewed ambition to the challenge aimed at Feng Jin Huang. Avoid flattening笞 into merely surpass or defeat, and retain the deliberate phoenix image.','Moderate literary preference, not a claim of uniquely correct English.','地仙 may carry a technical nuance;龙鱼 may admit different poetic readings. Tomorrow is prospective rhetoric, not proof of a next-day immortal breakthrough. No fresh live translation comparison; all wording remains a proposal.')
fixes=[(386,2,'似的的','似的'),(386,35,'常满尖刺','长满尖刺'),(386,63,'气态威重','气势威重'),(386,85,'白废','白费'),(387,9,'回来过去','回到过去'),(387,34,'在用奴隶蛊','再用奴隶蛊'),(387,43,'电光石闪','电光石火'),(387,47,'能能','能'),(388,4,'勾通外界','沟通外界'),(388,5,'我在以此','我再以此'),(388,20,'太蛊奇毒','太古奇毒'),(388,35,'将加大地加剧','将大大地加剧'),(388,48,'攀等','攀登'),(389,7,'蛊师福地','蛊仙福地'),(389,14,'攻击力也没用','攻击力也没有'),(389,32,'大肚翩翩','大肚便便'),(389,51,'危机空窍','危及空窍'),(390,18,'壮栽','壮哉'),(390,23,'早就想父亲','早就向父亲'),(391,27,'措不及防','猝不及防'),(391,32,'半柱香','半炷香'),(391,63,'吐沫','唾沫'),(391,79,'带西北方向','待西北方向'),(391,80,'接领溃军','接应溃军'),(392,22,'俯看这包同','俯看着包同'),(392,35,'反映过来','反应过来'),(393,2,'统帅权利','统帅权力'),(393,5,'再接再励','再接再厉'),(393,48,'冷不出微吸','禁不住微吸'),(393,73,'受人把柄','授人把柄'),(394,11,'借住孟土','借助孟土'),(394,83,'接下里','接下来'),(395,16,'先前一起的','先前一切的'),(395,16,'白废','白费'),(395,79,'万不得以','万不得已'),(396,34,'阴阳转身蛊','阴阳转生蛊'),(396,50,'背弃对付','背弃对方'),(396,67,'压力重生','压力重重'),(397,12,'真正好听','真是好听'),(397,27,'各占据四个方位','分别占据四个方位'),(397,57,'面对白凝冰','白凝冰'),(397,71,'破空空间','破开空间'),(397,76,'现在还要他','现在只要他'),(397,83,'鹤蚌相争','鹬蚌相争'),(398,3,'浪涛卷席','浪涛席卷'),(398,8,'浑身隆重','浑身笼罩'),(398,27,'锁链迅紧紧','锁链紧紧'),(398,30,'伸直先前','伸直向前'),(398,59,'带这凤金煌','带着凤金煌'),(399,24,'中州五域','中洲五域'),(400,44,'无妨说服','无法说服'),(402,43,'欲火大炙','欲火大炽'),(402,59,'推卸的一干','推卸得一干'),(402,97,'外门的那些','外面的那些'),(403,46,'已经再用','已经在用'),(403,58,'万不得以','万不得已'),(403,81,'已经将冷眼','已经在冷眼'),(404,30,'从他从地上','他从地上'),(404,76,'何况就被','很快就被'),(405,38,'至始至终','自始至终')]
moderate={(386,63),(387,43),(391,80),(393,48),(396,67),(404,76)}
v=pro(180,'Individually held copy candidates',sorted(set((c,p) for c,p,a,b in fixes)),'Review each proposed pair independently; preserve originals and source numbering.','Mechanical duplication, likely miswritten characters, grammatical particles and context-dependent reconstructions.','High local support for simple slips; moderate for specifically marked reconstructions.','No blanket pronoun rewriting across physical transformation, automatic normalisation of楞, or covert alteration of intentional public aliases.')
v['copy_items']=[]
for c,p,a,b in fixes:
 assert a in src(c,p)['text'],(c,p,a)
 v['copy_items'].append(dict(chapter=c,paragraph=p,original=a,replacement=b,confidence='Moderate; reconstruction/query' if (c,p) in moderate else 'High local; held, authorial priority unestablished',status='HOLD; unapproved and unapplied'))
save('batch-021-copy-candidates.json',v['copy_items'])
for v in ledger:
 if v['id']=='SR-167':
  v['history_before_batch021']={k:v.get(k) for k in ['recommended_action','rationale','confidence','status','dependencies','publication_status','latest_update']}
  v.update(status='Withdrawn correction: later knowledge disclosure defeats the earlier alias rationale',recommended_action='Retain370p68 方源. Do not replace it with方正 on the ground that Ruo Nan could not know the true identity.',confidence='High that396 establishes prior knowledge; this removes the earlier basis for correction, without proving every alias alternation intentional.',dependencies='396pp57–64 locates disclosure before the siege and reinforcement episode. Review speaker context individually, not globally.',publication_status='No correction proposed on the superseded rationale; whole-novel review continues')
  v['locations']+=loc([(394,31),(396,57),(396,58),(396,60),(396,61),(396,64)])
  v['batch021_update']='Correction withdrawn.396 explicitly reveals Ruo Nan learned the true identity before the staged siege. Earlier recommended replacement and rationale preserved in history; no source edit had been applied.'
 if v['id']=='SR-137':
  v['locations']+=loc([(396,21)])
  v['batch021_update']='396p21 explicitly names冰爆蛊 in the staged self-destruction plan, reinforcing Ice Explosion as an actual name/effect. This does not turn冰雹→Hail into a mistranslation or establish authorial priority at312. Controlling action, rationale and confidence from the Batch016 addendum remain unchanged.'
 if v['id']=='SR-153':v['batch021_update']='388p11 explicitly says only upgraded phantoms remain and still lacksFourAllOut.397p16 confirms beasts were spent in refinement. No FourAllOut upgrade through405; HundredBattles is ultimately consumed for FixedImmortalTravel, not AllOut.'
 if v['id']=='SR-172':
  for z in v.get('copy_items',[]):
   if (z['chapter'],z['paragraph'])==(373,45):
    z['prior_status_before_batch021']=z['status'];z['status']='SUSPENDED name-normalisation query; repeated魅 readings require wider collation';z['confidence']='High identity; low preference between魅 and媚 without fuller collation'
  v['batch021_update']='373p45狐魅儿→狐媚儿 is suspended as a preferred normalisation.386–405 repeatedly use魅 while370p34 uses媚. Same-person variation remains; frequency alone does not settle authorial spelling. Other copy items stay held.'
 if v['id']=='SR-165':v['batch021_update']='The initial six-person census remains supported. Later XiaoMang, MoWuTian and TieBaiQi are additional arrivals, not retroactive members of the earlier six. At399 rewind, do not merge branch-specific death totals.'
 if v['id']=='SR-156':v['batch021_update']='404p47 again deploys a pair of wings. Further support for one deployed pair, without proving the resting Gu pattern must be anatomically identical.'
 if 'batch021_update' in v:v['latest_update']=v['batch021_update']
events=load('history/before-batch021-chronology-register.json')['entries'];resources=load('history/before-batch021-resource-register.json')['entries'];ne=[];nr=[]
def ev(t,k,e,c,rr):
 v=dict(id=f'T{len(events)+1:03d}',timeline=t,kind=k,event=e,constraint=c,evidence_status='Source checked; branch and viewpoint labelled',dependency='Full-novel reconciliation outstanding; no invented dates',sources=ss(rr));events.append(v);ne.append(v)
def res(k,e,c,rr):
 v=dict(id=f'R{len(resources)+1:03d}',kind=k,entry=e,calculation=c,status='Branch-specific; acquired, consumed and prospective states distinguished',sources=ss(rr));resources.append(v);nr.append(v)
ev('Pre-third-rebirth branch','trial / death','Wu at48; twenty-third opponent','Wu killed before seeingBai. Trial index and human-opponent count differ; neither is a day count.',[(386,1),(386,18),(386,96),(387,2)])
ev('Pre-third-rebirth branch','advancement / elapsed months','ZhangFourupper afterFourmiddle','375 precedes intervening months.387upper need not be a mistake; no precise promotion date supplied.',[(375,71),(375,76),(375,79),(387,16)])
ev('Pre-third-rebirth branch','calendar frame','October19 and eighteen days','388 gives18days sinceLong andOctober19;389 runs20–24. The calendar is requested byFY, but whether it tracks outside dates or local counted days remains unproved. Do not add parallelHu time.',[(388,77),(388,81),(388,82),(388,83),(389,1),(389,6),(389,19),(389,30),(389,58)])
ev('Both branches, separately','sleep schedules','Half shichen versus three shichen','First branch about1hour daily; revised branch at least6hours daily under conventional2hour shichen. These are habits, not totals to add to elapsed plot time.',[(388,39),(388,68),(401,47),(401,48)])
ev('Pre-third-rebirth branch','backstory disclosure','Bai treatment and staged siege','IceCrystal choice, deliberateYanTu loss, death/revival oath escape and priorTie alliance disclosed396. Narrator exposition is not automatically all dialogue heard byFY.',[(396,18),(396,21),(396,43),(396,45),(396,53),(396,54),(396,57),(396,61),(401,40)])
ev('Pre-third-rebirth branch','death / completion / transformation','Spirit dies;SecondAperture completed;Bai male','394BaGui death precedes395 completion. Yang used395;396 confirms malebody. These states are later overwritten, not current405 endpoints.',[(394,75),(394,76),(395,95),(395,98),(396,6)])
ev('Pre-third-rebirth, parallelCentral','inheritance result','Feng wins before rewind','398 explicit summit victory.399biography gives申时两刻;current observation申时三刻, one-ke separation. Conventional gloss15:30/15:45 is not certified global time conversion.',[(398,79),(398,80),(398,81),(399,4),(399,8)])
ev('Third rebirth transition','reset boundary','Cicada third use returns toWang negotiation','Do not add repeatedOctober24 periods as one linear history. SR173 recordsYun absorption-order problem around382p60/399p37/400p38.',[(399,17),(399,30),(399,37),(399,38),(399,51),(400,38)])
ev('Post-third-rebirth branch','changed deaths / enslavement','Wang/Long/Zhang dead;Qiu enslaved','Long killedbeforepoison; Qiu notkilled. Do not import earlierWuShenTong death without current evidence. Feng remainsunenslaved.',[(400,34),(400,53),(400,55),(400,68),(401,17),(405,52)])
ev('Post-third-rebirth branch','repeated calendar date','October24 again','401 repeats the date in a replacement history. Qiu delaysattacks; poisonbreachprevented; originalthreeattackorderscannotbe addedacrossbranches.',[(401,52),(402,7),(402,52),(402,74),(404,39)])
ev('Post-third-rebirth branch','changed outcome','Bai fakeexplosion exposed beforeYanguse','Yangrecalled403p70. Bai remainsfemale; noactual100%aptitude orexplosionproved. Forty-yearembryo preserved, notcompletedSecondAperture.',[(403,69),(403,70),(403,73),(403,78)])
ev('Post-third-rebirth branch, parallelCentral','teleport / inheritance interception','FY reachesHu summitfirst','FixedTravelpoweredbyspirit; clothesleftbehind. FYarrivesbeforeFeng summitcompletion inthisbranch. Landspiritaddressesmaster; no406eventsread.',[(405,103),(405,104),(405,124),(405,125),(405,166),(405,168),(405,177),(405,184),(405,185)])
res('Pre-rebirth acquisition','Wu pack andZhangSlaveGu','Bai receivesWu dogs, force+10%. FYobtainsFiveSlaveGu, usesonFeng. No automaticidenticaltransferafterrewind.',[(387,5),(387,6),(387,27),(387,45),(387,50)])
res('Aptitude / limits','89% andfirst-aperture ceiling','89%reported387/388; next90targetunmetafterLongpoisonscorpse. Secondcapacitycannotexceedfirst90atuse; laterfirstgrowthallowsroom. No90completioninvented.',[(387,11),(387,13),(387,14),(387,15),(388,26)])
res('Suppression / lostloot','One-Gu weakzone andLongpoison','FirstbranchLongdefeatedthensuicide; noapertureorGu recovered. Revisedbranchpreemptivekill allowsBiKongFiveandapertureloot. Notinconsistentlootforonehistory.',[(387,68),(388,14),(388,18),(388,24),(388,25),(400,55),(400,59),(400,62)])
res('Refinement inputs / intermediate lifetimes','300+500Lifespan andtwoforms','LifespanGuconsumedingredients, not800yearspersonalaging. Earlypseudoform7days;goldenshell40years;laterlightform3shichen. Distinctstages, notsameobjectcontradiction.',[(390,78),(390,80),(391,25),(391,36),(395,15),(403,73)])
res('Pre-rebirth trial rewards','Feng clearsXin;BaiDogforce','HundredBattlesreceived;hundredsofHairyMenfollowFeng;near100000dogs. Afterwards9万多surviveinitiallightattack; noexactlossaccount.',[(389,63),(389,64),(389,65),(389,72),(393,47),(393,53)])
res('Military scopes','1600attackers plus400reserve','391300+500+800=1600attackers. LiXian400reserve separate.3921000pluscommittediscompatible; no2000exactcasualtyassertion.',[(391,77),(391,78),(391,79),(391,80),(392,3),(392,7),(392,8)])
res('Immortal exceptions','DreamWings uses soul','Ordinaryneedforimmortalessence has explicitDreamWingsexception. The soulcost canharmmemory; notproofFenghasimmortalessence orcultivationSix.',[(398,62),(398,63),(398,64),(405,149),(405,150)])
res('Pre-rebirth ownership / captivity','SecondAperture heldbyTie,controlledbyFY','FinishedGu physicallyseized butremotelyself-destructiblebyrefiner. CannotstorealongsidepressuringCicada; notactivated. FixedStar+chainssuppressup-toFive,notSixCicada.',[(396,73),(397,76),(397,79),(397,80),(397,81),(398,86),(398,96),(399,13)])
res('Thirdrebirth reset','Cicada weakened;inventorystate reset','Self-explosion fundsrewind. Cicadabecomesweak/dormant again; nofinishedSecondAperture survivesasacquiredGu. Do notcopypriorbranchGoldSouporYangconsumptioninto currentstate.',[(399,19),(399,23),(399,47),(399,48),(399,49),(400,22)])
res('Post-rebirth control / soulburden','Qiuenslaved,notFeng','FiveSlaveGusoulcontestwonusingdistraction. Soulburdenaffectsrefinement. Qiu securesHundredBattles butnotcompleteXin/Hairyfollowers. Two remainingpillars valid.',[(400,74),(400,78),(401,15),(401,17),(401,24),(401,54),(401,55),(401,80),(401,81)])
res('Oath types / viewpoint','Deathandrevival circumventsPoisonOath','396narrator explainsone-thirdrisk;401Qiuconfirmsdoctorhistory. 毒誓without蛊maymeanordinarysolemnoath; preserveinformationalomission. Haillexicalcorrection remainsunchanged.',[(396,50),(396,53),(396,54),(401,25),(401,28),(401,33),(401,35),(401,36)])
res('Post-rebirth defence','Spiritcontrols dogs;Tieapes','BaihandsGu tospirit; notreliableDogcommandremainingwithher. TieBaiQi deployswhiteapes. His laterarrivaldoesnotchangetheoriginalsix-mastercensus.',[(401,60),(401,62),(403,34),(403,36),(403,37),(403,38)])
res('Post-rebirth recipe / consumedparasite','DivineTravel+BiKong+FixedStar+glory','FixedStarconsumed, defeatingchaintrackingwithoutamputation. SpiritprovidesDivineTravel;BiKonghollowbambooconfirmed.Forty-yearintermediateSecondAperturenotusedinthisrecipe.',[(404,60),(404,62),(404,71),(404,74),(404,77),(405,27),(405,29),(405,34),(405,42)])
res('Post-rebirth consumables / damage','FixedTravel completed;HundredBattles spent','TwoThirdWatch→9×cocoonrate; HundredBattlesFiveconsumedforrefinement. AllOutEffortnotupgraded. GoldSoupdestroyed;GoldGlow/wingsdamaged. Localguaranteedrefinementnotyetuniversalrule.',[(405,67),(405,68),(405,69),(405,77),(405,78),(405,81),(405,91)])
res('Post-rebirth endpoint','Teleport andcurrentpossessions','SpiritpowersFixedTravel;clothesexcluded,apertureGuincluded. WeakCicadaallowschangedstoragesituation; noactivatedsecondaperturerequired. Bai stillfemale;Yangretained; Qiu lastaliveenslaved.',[(403,70),(405,103),(405,104),(405,124),(405,125),(405,174),(405,178)])
# Annotate recent historical entries without deleting their branch-specific evidence.
for v in resources:
 if v in nr:continue
 if any(z['chapter'] in range(382,386) for z in v['sources']):v['batch021_update']='At399 the narrative rewinds toWang negotiation. Preserve this earlier evidence as pre-third-rebirth history; use Batch021 branch-specific entries for current405 state.'
np=sum(len(c['paragraphs']) for c in batch);nc=sum(sum(map(len,c['paragraphs'])) for c in batch);tp=sum(len(c['paragraphs']) for c in cs);tc=sum(len(t) for c in cs for t in c['paragraphs'])
save('proposal-ledger.json',ledger);save('chronology-register.json',dict(scope='Sequential through405; third-rebirth branches explicitly separated',entries=events));save('resource-register.json',dict(scope='Sequential through405; overwritten and revised ownership distinguished',entries=resources))
progress=load('history/before-batch021-reading-progress.json');progress.update(sequential_chapters_completed=list(range(1,406)),paragraphs_read=tp,paragraph_characters_read=tc,next_chapter=406,remaining_chapters=1929,batch_report='Batch-021-Chapters-386-405.md',scope='Full sequential Chinese reading through405; selected external collation, not fresh live bilingual audit',whole_novel_chronology_verified=False)
progress['batches'].append(dict(id='021',chapters=[386,405],paragraphs=np,characters=nc,reading_segments='Ten complete untruncated two-chapter outputs'))
progress['chapters'] += [dict(chapter=c['corpus_chapter'],file=c['file'],title=c['title'],paragraphs=len(c['paragraphs']),first_paragraph=1,last_paragraph=len(c['paragraphs'])) for c in batch];save('reading-progress.json',progress)
save('batch-021-reading-log.json',dict(status='Complete',endpoint=405,next_unread=406,segments=[dict(chapters=[a,a+1],status='Full paragraph sequences read; untruncated',paragraphs=sum(len(by[n]['paragraphs']) for n in [a,a+1])) for a in range(386,406,2)],note='Reader-facing405p173omission is not an unread gap; supplied EPUB unchanged. Wrongly mapped external next-chapter capture rejected, not counted as sequential reading.'))
stand=load('history/before-batch021-working-standards-register.json');stand['coverage_through']=405
for v in stand['entries']:v['batch021_update']='Through405 provisional: separate third-rebirth branches, narrator-only explanations from spoken disclosure, physical possession from Gu control, and intermediate forms from final Gu. SR167 correction withdrawn; Hail remains faithful; actual405 endpoint not projected beyond406.'
save('working-standards-register.json',stand)
ws=['# Working standards through Chapter405','Twelve provisional standards; no source or translation edits approved/applied.']
for v in stand['entries']:ws += [f"## {v['id']}: {v['topic']}",v['rule'],v['status'],v['batch021_update']]
(r/'WORKING-STANDARDS.md').write_text('\n\n'.join(ws))
out=['# Batch021 numbered Chinese reading copy, Chapters386–405','Source text and numbering preserved. One restricted passage405p173 marked as omitted; original EPUB unchanged. No editorial emendations applied.']
for c in batch:
 out += [f"## Chapter {c['corpus_chapter']}: {c['title']}",f"EPUB: {c['file']}"]+[f"{p}. {reader(c['corpus_chapter'],p,t)}" for p,t in enumerate(c['paragraphs'],1)]
(r/'Batch-021-Numbered-Chinese-Source.md').write_text('\n\n'.join(out))
for name,vs in [('Chronology',ne),('Resources',nr)]:
 out=[f'# Batch021 {name} jotter','Evidence retains its original timeline; no silent transfer across399 rewind.']
 for v in vs:
  out += [f"## {v['id']}: {v.get('event',v.get('entry'))}",v.get('constraint',v.get('calculation'))]
  for z in v['sources']:out += [f"Ch{z['chapter']} p{z['paragraph']}",'> '+reader(z['chapter'],z['paragraph'],z['text'])]
 (r/'jotters'/f'Batch-021-{name}.md').write_text('\n\n'.join(out))
out=['# Batch021 continuity jotter','All new edits held. EarlierSR167correction explicitly withdrawn.']
for v in new:
 out += [f"## {v['id']}: {v['category']}"]+[f"**{k}:** {v[k]}" for k in ['recommended_action','rationale','confidence','dependencies']]
 for z in v['locations']:out += [f"Ch{z['chapter']} p{z['paragraph']}",'> '+reader(z['chapter'],z['paragraph'],src(z['chapter'],z['paragraph'])['text'])]
 for z in v.get('copy_items',[]):out += [f"Ch{z['chapter']} p{z['paragraph']}: {z['original']} → {z['replacement']}. {z['confidence']}. HOLD."]
(r/'jotters/Batch-021-Continuity.md').write_text('\n\n'.join(out))
preserve='''# Batch021 preservation controls

- No merging of the two October24 histories.399 resets the sequence.
- SR167 correction withdrawn: Ruo Nan already knew the identity. Knowledge revelation does not make every public alias wrong.
- Hail still correctly translates冰雹.396冰爆 confirms an explosion Gu, not authorial priority at312.
- Bai's apparent100%aptitude and self-destruction are staged. Yang is used in the overwritten branch only.
- Qiu is killed in the old branch and enslaved in the new one. Feng is the old enslaved helper, not the new one.
- Narrator explanation of Poison Oath removal need not have been spoken to FY. His401question is not automatically a memory error.
- Nine immortals surprised by Dream Wings and ten by FY are different reactions; no forced9→10 repair.
- Seven-day, forty-year and three-shichen forms are different refinement stages.
- Hundred Battles delivered does not equal entire Xin inheritance cleared. The changed pillar count is explained.
- Immortal Gu ordinarily require immortal essence; Dream Wings has an explicit soul-cost exception.
- Light Gu's harmless standalone effect and damaging combinations are compatible. Three attacks occur in each branch, not six uses in one month.
- Fixed Star removal is by consumption in the final recipe, not actual forearm amputation.
- Returned clothes and carried apertureGu are different transport categories. WeakCicada changes storage pressure after rebirth.
- No all-victims-died claim from landcollapse. No406 aftermath read.
'''
(r/'jotters/Batch-021-Preserve.md').write_text(preserve)
coll=[]
for c,p,a,b in fixes:
 f=r/'fact-check-021'/f'ch{404 if c==405 else c}-normalized.txt';t=f.read_text() if f.exists() else ''
 coll.append(dict(chapter=c,paragraph=p,original=a,replacement=b,original_in_repost=a in t if t else None,replacement_anywhere_in_repost=b in t if t else None,witness_status='Matched chapter; substring test is not same-sentence attestation' if t else 'No matched external chapter; EPUB only'))
save('fact-check-021/copy-collation.json',coll)
checks=[(386,79,'光恒'),(387,29,'被四代族长逆袭暗算'),(388,26,'八成九'),(389,7,'进入了蛊师福地'),(389,95,'没有进入传承'),(396,21,'冰爆蛊'),(396,57,'铁若男这才得知一切真相'),(396,58,'是方源，而并非方正'),(399,37,'我身上就有一只毒誓蛊'),(400,38,'吞噬了他和云落天的空窍'),(401,44,'斩获第二空窍蛊'),(402,82,'萧家二族长'),(405,78,'一次炼蛊必成'),(405,117,'千古地仙随风逝'),(405,120,'明朝登仙笞凤凰'),(405,177,'自己先她一步登顶')]
sub=[]
for c,p,a in checks:
 assert a in src(c,p)['text'];t=(r/'fact-check-021'/f'ch{404 if c==405 else c}-normalized.txt').read_text();sub.append(dict(chapter=c,paragraph=p,fragment=a,in_repost=a in t))
save('fact-check-021/substantive-collation.json',sub)
held=sum(not v['status'].startswith(('Withdrawn','Resolved locally')) for v in ledger)
report=[f'# The Omniarch: Sequential Review, Chapters386–405',f'Batch021 | Twenty chapters | {np:,} paragraphs | {nc:,} paragraph characters',f'Completed1–405 of2,334. Next unread406. Cumulative{tp:,} paragraphs / {tc:,} characters. Original EPUB unchanged. No source/site edits.',
'## Executive findings','Twenty complete chapters read in ten untruncated outputs. The third Cicada use resets history at399. The registers now separate overwritten outcomes from the revised405 endpoint. This is source review, not a fresh live bilingual audit.',
'1. SR167 alias correction withdrawn:396 proves Tie Ruo Nan already knew the true identity.\n2. New strong candidate:401 calls Hundred Battles a Second Aperture trial prize.\n3. Yun’s aperture timing around the rewind needs reconciliation; no double-counting authorised.\n4. Dog-name transposition and Xiao Mang’s title have supported local candidates.\n5. Xiao’s entry wording and Flower Wine’s death causation remain qualified queries.\n6.396 reinforces Ice Explosion Gu as a name without invalidating Hail for冰雹.\n7. A held closing-poem/title draft accompanies the copy candidates.',
'## Earlier findings corrected or qualified']
for v in ledger:
 if 'batch021_update' in v:report += [f"### {v['id']}: {v['category']}",v['batch021_update']]
for c,p in [(396,57),(396,58),(396,61),(396,21)]:report += [f'Ch{c} p{p}','> '+src(c,p)['text']]
report += ['## Exact evidence and proposed actions']
for v in new[:-1]:
 report += [f"### {v['id']}: {v['category']}",v['recommended_action'],'**Rationale:** '+v['rationale'],'**Confidence:** '+v['confidence'],'**Dependencies / status:** '+v['dependencies']+' HOLD; unapproved and unapplied.']
 for z in v['locations']:report += [f"Ch{z['chapter']} p{z['paragraph']}",'> '+reader(z['chapter'],z['paragraph'],src(z['chapter'],z['paragraph'])['text'])]
report += ['## Research and source limits',f'19 distinct external page captures from one Hetushu repost tradition. Pages386–404 are title-matched; the404page also contains appended405material, confirmed by recipe, poem, teleport and summit fragments. The next numeric URL led to Feng Jiu Ge and was rejected as a405mapping. Thus selected evidence from all20chapters is checked across19pages, not20independent witnesses. All{len(sub)} selected substantive fragments were tested; {sum(z["in_repost"] for z in sub)} exactly matched. Raw captures, hashes, rejected-mapping record and copy checks are saved. Repetition is not authorial priority. Replacement substring hits do not alone establish an alternate reading. Contextual checks confirm alternate forms at388p20太古奇毒,396p50背弃对方,398p59带着凤金煌 and404p76很快就被.401p44 directly reads百战不殆蛊 in the repost.402p43 has欲|火大炙, so its failed exact match is a separator artifact, not a corrected炽 reading. Authorial priority remains unknown.']
for z in load('fact-check-021/external-witnesses.json'):report += [f"Ch{z['chapter']}: {z['url']}"]
report += ['## Chronology additions']
for v in ne:report += [f"### {v['id']}: {v['event']}",v['constraint'],refs(v['sources'])]
report += ['## Resources and branch controls']
for v in nr:report += [f"### {v['id']}: {v['entry']}",v['calculation'],refs(v['sources'])]
report += [f'## SR180: {len(fixes)} individually held copy candidates','Moderate rows are reconstructions. The status does not certify an authorial original or a live English error.','| Chapter / paragraph | Original | Candidate | Confidence |','|---|---|---|---|']
for z in new[-1]['copy_items']:report += [f"| {z['chapter']} / {z['paragraph']} | {z['original']} | {z['replacement']} | {z['confidence']} |"]
report += ['## Chapter-by-chapter working notes',(r/'jotters/batch-021-working.md').read_text(),'## Preserve rather than overcorrect',preserve,
'## Endpoint405','FY: Revolution Four upper, at Hu Immortal’s summit, addressed as master. Fixed Immortal Travel completed. Second Aperture: retained40-year intermediate, not completed or activated in this branch. Bai remains female; Yang not consumed. Qiu enslaved and last seen alive; Feng Tian Yu free. Gold Soup destroyed, Gold Glow and wings damaged. No406outcome claimed.',
'## Saved state and backup boundary',f'{len(ledger)} proposal records: {held} held, three withdrawn, one locally resolved without correction. {len(events)} chronology and {len(resources)} resource entries; twelve provisional standards. Five jotters, numbered reading copy, report, workbook and QA. One reader-facing omission405p173, original numbering retained. GitHub backup verified through365 only; no405upload claimed.']
report_text=re.sub(r'(?m)(^\|[^\n]*\|)\n\n(?=\|)',r'\1\n','\n\n'.join(report));(r/'Batch-021-Chapters-386-405.md').write_text(report_text)
old=(r/'update_batch010.py').read_text();wb=old[old.index('# Workbook: cumulative'):old.index("(r/'CURRENT-STATUS.md').write_text")]
wb=wb.replace('1–220 of2334','1–405 of2334').replace("('Next unread',221)","('Next unread',406)").replace('103total;102activeheld;1withdrawn',f'{len(ledger)}total;{held}held;3withdrawn;1locallyresolved').replace('range(10,0,-1)','range(21,0,-1)').replace("v['batch010_update']","v['batch021_update']").replace('Batch-010-Chapters-201-220','Batch-021-Chapters-386-405').replace('CHAPTERS201–220','CHAPTERS386–405').replace('Chapters201–220','Chapters386–405').replace('Twenty complete chapters; personal clocks and inventory scope distinguished','Twenty complete chapters; rebirth branches and later knowledge reconciled').replace('Ch151,201p22,203p84 restricted excerpts','Earlier restricted excerpts and405p173 retain omission markers')
wb=wb.replace("v['publication_status'],'No','No',latest]","v['publication_status'],'No','No',v.get('latest_update',latest)]")
exec(compile(wb,'workbook-and-docx','exec'))
(r/'CURRENT-STATUS.md').write_text(f'''# Sequential review checkpoint:405

Completed1–405 of2334. Next unread406;1929remain. Batch021:20chapters,10untruncated outputs,{np}paragraphs/{nc}characters. Cumulative{tp}/{tc}.

{len(ledger)}proposals:{held}held,3withdrawn,1locallyresolved. SR167correctionwithdrawn after396knowledge disclosure;SR173–180new,including{len(fixes)}copycandidates. {len(events)}chronology/{len(resources)}resources;12standards. Hailfaithfulness retained;396IceExplosion evidence appended transparently.

19distinctexternalpages;404pagealsoincludes405material,confirmedbyselectedrecipe/poem/summitfragments. WrongnextURLcapture rejected. EPUB405readfully. Readercopy/workbook omit405p173onlynewrestrictedpassage,numberingunchanged. No source/site edits.

Endpoint:FYFourupper,HuImmortal summit/master;FixedTravel completed;SecondAperture40yearintermediate only. CurrentBai female/Yangnotused,Qiuenslaved,Fengfree. GoldSoupdestroyed. EarlierbranchmaleBai/deadQiu/finishedSecondAperture notcurrentstates.

IndependentexportQA pending. Remoteverified365only;no405uploadclaim. No localdeletions. Next406.
''')
sha=hashlib.sha256(Path('/home/user/benchmark/sources/Gu-Zhen-Ren.epub').read_bytes()).hexdigest();assert sha==progress['source_sha256'];assert len(cs)==405 and len(ledger)==180 and held==176
assert all(not v.get('approved') and not v.get('applied') for v in ledger)
base=load('history/before-batch021-proposal-ledger.json')
for id in ['SR-134','SR-135','SR-136','SR-138']:assert next(v for v in ledger if v['id']==id)==next(v for v in base if v['id']==id)
for k in ['recommended_action','rationale','confidence','status','fact_check_addendum']:assert next(v for v in ledger if v['id']=='SR-137')[k]==next(v for v in base if v['id']=='SR-137')[k]
texts={t for c in cs for t in c['paragraphs']}
for line in report_text.splitlines():
 if line.startswith('> '):assert line[2:] in texts
qa=dict(batch='021',chapters=20,paragraphs=np,characters=nc,cumulative_paragraphs=tp,cumulative_characters=tc,proposal_count=len(ledger),held=held,withdrawn=3,resolved_local=1,copy_candidates=len(fixes),chronology=len(events),resources=len(resources),reading_segments=10,next_unread=406,source_sha256=sha,source_unchanged=True,substantive_changes_applied=False,batch016_factcheck_controls_preserved=True,external_captures=19,rejected_external_mapping=405,reader_omissions=[[405,173]],remote_uploaded=False,remote_verified_through=365)
save('batch-021-qa.json',qa);print(json.dumps(qa,indent=2))
