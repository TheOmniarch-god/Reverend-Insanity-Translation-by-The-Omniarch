from pathlib import Path
import json,shutil,hashlib
from openpyxl import Workbook,load_workbook
from openpyxl.styles import Font,PatternFill,Alignment
r=Path('/home/user/editorial/sequential-review')
def load(n):return json.loads((r/n).read_text())
def save(n,v):(r/n).write_text(json.dumps(v,ensure_ascii=False,indent=2))
for n in ['reading-progress.json','proposal-ledger.json','chronology-register.json','resource-register.json','working-standards-register.json']:
 d=r/'history'/('before-batch016-'+n)
 if not d.exists():shutil.copy2(r/n,d)
cs=sum([load(f'batch-{i:03d}-source.json') for i in range(1,17)],[]);by={c['corpus_chapter']:c for c in cs};batch=cs[300:315]
def src(c,p):return dict(chapter=c,paragraph=p,file=by[c]['file'],text=by[c]['paragraphs'][p-1])
def ss(rr):return [src(*z) for z in rr]
def loc(rr):return [{k:v for k,v in z.items() if k!='text'} for z in ss(rr)]
def refs(z):return '; '.join(f"Ch{x['chapter']} p{x['paragraph']}" for x in z)
def reader(c,p,t):
 if (c,p)==(303,16) or (c==296 and 95<=p<=97) or (c==258 and (70<=p<=74 or p==79)) or (c==250 and (24<=p<=31 or p in [33,35,36])) or (c==151 and (31<=p<=67 or p in [98,99])) or (c,p) in [(201,22),(203,84)]:return '[Restricted passage omitted from reader-facing copy. Original numbering retained; original EPUB unchanged.]'
 return t
ledger=load('history/before-batch016-proposal-ledger.json');new=[]
def pro(i,cat,rr,action,why,conf,dep):
 v=dict(id=f'SR-{i:03d}',category=cat,locations=loc(rr),recommended_action=action,rationale=why,confidence=conf,status='Active provisional proposal; no approval',dependencies=dep,approved=False,applied=False,publication_status='HOLD: full2334-chapter reading and global reconciliation outstanding');ledger.append(v);new.append(v);return v
pro(134,'Tie chronology: years, months, and the Qing Mao anchor',[(273,23),(298,104),(301,63),(302,3),(302,14),(302,15),(302,22),(302,35),(304,15),(304,40),(309,30)],'Preferred local302p35 这些年→这段时间, or这几个月 if the recent eye-injury clock is intended. Separately HOLD302pp14–15/22 two-year wording for global reconciliation. If a shorter death-to-arrival interval is confirmed, 一年多前 and相应较短的期间 are candidates; do not assign an exact replacement now.','302 explicitly locates the eye injury a few months earlier but calls the saving period years. The larger two-years-since-death account is in tension with273 nearly one year since Qing Mao plus the subsequently narrated city intervals and301 three-month jump. Unquantified ellipses prevent a certified total.', 'High local months/years scope issue; moderate larger chronology concern; low confidence in an exact global date repair.','Distinguish father’s death, arrival of its news, daughter’s career and Tie Dao Ku’s city residence. Retain later two-plus-year Shang stay after304’s year-plus ellipsis; do not compress that separate period.')
pro(135,'Bai aptitude: ninety-two to ninety-three versus two points',[(275,60),(301,83),(304,80),(304,81)],'Preferred304p80 又回升了两分→又回升了一分. Preserve93% aptitude and seven points remaining to100%.','301 fixes92%;304 gives93% and independently says seven points remain. That supports a one-percentage-point increment, not two. Earlier275’s one-point increase is compatible with91% before301.','Very high local arithmetic and corroborating endpoint.','Source collation; do not reinterpret成/分 as multiplication or change the earlier90%-reserve statement into an aptitude total.')
pro(136,'Shang Bu Li mislabelled clan leader',[(306,52),(306,53),(306,55),(306,56),(306,64)],'Preferred306p53 更是商家族长→更是商家家老. English: he was also a Shang clan elder.','The same scene makes him Shang Yan Fei’s subordinate, first minister and slave-trade administrator. Calling him the clan leader conflicts with the established officeholder.','Very high local office-identity support.','Independent witness; preserve his seniority over ordinary junior lords without making him a co-chief.')
pro(137,'Hail Gu versus Ice Explosion Gu',[(299,25),(312,97),(313,39),(313,40),(313,41)],'Preferred312p97 冰雹蛊→冰爆蛊.','The action proposed is detonating the icicles;299 defines Ice Explosion and313 explicitly names it while performing that action. Hail is the mismatched technical name.','Very high functional and adjacent-name support.','Local technical-name repair only; do not merge every ice-type Gu or automatically equate Frost Spit and Frost Breath.')
pro(138,'Arena promotion: rule scope and eighteen-month window',[(279,58),(301,44),(301,45),(301,46),(301,54),(301,63),(304,35)],'Retain the figures pending scope reconciliation. Clarify the start of the eighteen-month window, carried-in wins, and whether four bouts per month describes only the earlier phase. Only if eighty new fourth-tier wins all fall inside that window under an unchanged four-per-month cap, consider extending the interval (e.g. 两年左右) or explicitly limiting the cap’s duration. No preferred numerical replacement yet.','Eighty wins require at least twenty four-bout monthly allocations, while304 describes advancement over a year and a half. But the preceding three-month phase may supply carried-in wins; the practice cap is not necessarily permanent, and tier-count semantics need confirmation. Likewise8/10/17day fight markers can denote sequential gaps rather than one common zero.','High confidence in the located constraints; low-to-moderate inconsistency diagnosis until their scope is proved.','Later arena rules, promotion counters, calendar/month convention, missing bouts and exact anchor of这一年半. Do not manufacture losses, dates or retroactive wins.')
fixes=[(301,9,'和他队长','和他对战'),(302,25,'年纪岁轻','年纪虽轻'),(302,59,'亲身女儿','亲生女儿'),(302,61,'找到了鹤群','遭到了鹤群'),(302,83,'就那就将','那就将'),(302,86,'却其他人而言','对其他人而言'),(303,27,'急忙分辨','急忙分辩'),(303,44,'莫名其妙的维护','莫名其妙地维护'),(303,67,'好好的活','好好地活'),(303,69,'明显的感觉','明显地感觉'),(303,75,'很干脆的走','很干脆地走'),(304,27,'光轮彪转','光轮飙转'),(304,30,'去的快','去得快'),(304,46,'骏马驰力蛊','驰马骏力蛊'),(304,48,'逢战不殆','逢战不败'),(304,68,'很平静的分析','很平静地分析'),(305,26,'商丘牛','商囚牛'),(305,66,'纯洁无暇','纯洁无瑕'),(305,71,'五成久','五成九分'),(305,85,'和腾灸龙的蛊师交过手','和腾灸龙交过手'),(306,7,'代练司','代炼司'),(306,7,'油钱不多','油水不多'),(306,19,'走的很近','走得很近'),(306,53,'位职','职位'),(306,64,'雄心豹子胆','熊心豹子胆'),(306,75,'一枝箭枝','一支箭矢'),(307,10,'如今已只有','如今也只有'),(307,84,'表现是凛然','表现出凛然'),(307,90,'答应呼之欲出','答案呼之欲出'),(307,98,'得意的大笑','得意地大笑'),(307,100,'觐言','进言'),(308,7,'皆现有怒容','皆现怒容'),(308,78,'众所之知','众所周知'),(308,87,'原比蛊虫','远比蛊虫'),(308,89,'授人鱼','授人以鱼'),(308,93,'诚信为本本','诚信为本'),(309,53,'方源炯炯的目光注视下','在方源炯炯的目光注视下'),(309,59,'一脸骄傲的插嘴','一脸骄傲地插嘴'),(309,79,'笑得道','笑着道'),(309,82,'疑惑重生','疑惑丛生'),(310,6,'无时无刻的不停地','无时无刻不在'),(310,23,'传的有鼻子有眼','传得有鼻子有眼'),(310,28,'来的太快','来得太快'),(310,29,'像父亲大人求亲','向父亲大人求情'),(310,31,'做的很隐秘','做得很隐秘'),(310,32,'一个劲的在','一个劲地在'),(310,38,'点缀期间','点缀其间'),(310,53,'气愤无比的叱问','气愤无比地叱问'),(310,65,'接触毒誓蛊','解除毒誓蛊'),(310,72,'抱住少主之位','保住少主之位'),(311,5,'躲的及时','躲得及时'),(311,6,'把你的皮','扒你的皮'),(311,17,'三番五次的刁难','三番五次地刁难'),(311,23,'寰转','回转'),(311,38,'说的很艰难','说得很艰难'),(311,41,'得意的笑','得意地笑'),(311,83,'吃惊的下巴','吃惊得下巴'),(312,43,'冷冷的回','冷冷地回'),(312,53,'通体白银作色','通体银白色'),(312,63,'回复','恢复'),(312,65,'回复','恢复'),(312,68,'回复','恢复'),(312,78,'迎得了','赢得了'),(312,86,'紧紧的凝视','紧紧地凝视'),(313,2,'想不打','想不到'),(313,4,'做的相当','做得相当'),(313,14,'生出右手','伸出右手'),(313,25,'又不是沉稳','又不失沉稳'),(313,32,'伸指小拇指','伸出小拇指'),(313,39,'一蓬冰锥蛊射出','一蓬冰锥射出'),(313,54,'站在场外','站在远处'),(313,63,'极大的遏制','极大地遏制'),(313,63,'回复威势','恢复威势'),(313,83,'水动成冰','水冻成冰'),(313,85,'挪移一声','揶揄一声'),(313,108,'一点都不没有','一点都没有'),(314,13,'龙眷顾','龙卷蛊'),(314,37,'如今再讲','如今再见'),(314,50,'凭白','平白'),(314,53,'拼劲全力','拼尽全力'),(314,72,'剧烈的呼啸','剧烈地呼啸'),(314,82,'一届新人','一介新人'),(314,86,'卷席天下','席卷天下'),(314,101,'冰刃风波','冰刃风暴'),(314,105,'改良的还不','改良得还不'),(314,111,'心力憔悴','心力交瘁'),(314,118,'冰刃风波','冰刃风暴'),(315,2,'胜的并不','胜得并不'),(315,3,'花的太值','花得太值'),(315,18,'默默的舔舐','默默地舔舐'),(315,19,'倾述','倾诉'),(315,25,'作为考虑到','考虑到'),(315,51,'如是此战','若是此战'),(315,77,'挪揄','揶揄')]
for c,p,a,b in fixes:assert a in src(c,p)['text'],(c,p,a)
v=pro(139,'Located copy and technical-name candidates',sorted(set((c,p) for c,p,a,b in fixes)),'Review each replacement individually. Preserve source quotation and paragraph numbering; do not globally normalise names or staging.','Wrong characters, missing words, technical-name drift, grammatical particles and locally ambiguous diction. The arena场外 candidate is conditional, not proof of an illegal departure.','Mostly high; reconstruction, diction and staging individually qualified.','Independent source witnesses. Preserve legitimate viewpoint, approximation and consciously misleading character speech.')
moderate={(303,27),(304,27),(304,46),(304,48),(305,85),(306,75),(307,10),(309,59),(310,6),(312,53),(313,54),(313,85),(314,111)}
v['copy_items']=[dict(chapter=c,paragraph=p,original=a,replacement=b,confidence='Moderate: contextual reconstruction, diction, name standard or staging; collate first' if (c,p) in moderate else 'High local copy support',status='HOLD; unapproved/unapplied') for c,p,a,b in fixes]
for v in ledger:
 if v['id']=='SR-118':
  v['locations']+=loc([(304,39),(304,40),(304,43),(305,36)])
  v['recommended_action']='Preferred Shang-specific changes:262p65保住少族长的位置→保住少主的位置;304pp39/40/43 use少主 instead of少族长 for Ya Zi.305p36 strongly supports269p72前世差一点成为商家少主→前世差一点成为商家家主. Keep the Bai-twin少族长→少主 component downgraded and unresolved, pending clan-specific succession evidence.'
  v['confidence']='High Shang Ya Zi office correction and strengthened Chao Feng former-life家主 candidate; low-to-moderate Bai title repair.'
  v['batch016_update']='305p36 explicitly says Chao Feng nearly became家主 in the former life, repeating the Xin Ci rival context of269p72.304 repeats Ya Zi少族长 despite311dismissal of one junior-lord office. Tie’s eight junior lords30221 show clan-specific systems again.'
 if v['id']=='SR-099':v['batch016_update']='Remains withdrawn.30173–78 and30478/82 establish accelerated progress within Revolution Three; assistance wanes when both reach Three peak, not when FY first reaches Three.'
 if v['id']=='SR-123':v['batch016_update']='30195 explicitly sells Canopy Gu, not Flying Bone Shield. The missing-shield disposition remains unresolved; do not substitute one defensive Gu’s sale for the other.'
 if v['id']=='SR-120':v['batch016_update']='31023 says precise accounts circulate, but does not reproduce their amounts. The650000 proposed public price versus600000 final clan-funds basis remains unclarified; no numerical reconciliation invented.'
 if v['id']=='SR-090':v['batch016_update']='31260 recalls initial-to-peak by Stone Aperture, but gives no new lifespan or aptitude arithmetic to resolve the earlier mechanism query.'
events=load('history/before-batch016-chronology-register.json')['entries'];resources=load('history/before-batch016-resource-register.json')['entries'];ne=[];nr=[]
def ev(t,k,name,detail,rr,dep='Whole-novel reconciliation, source variants and scope of relative clocks outstanding'):
 v=dict(id=f'T-{len(events)+1:03d}',timeline=t,kind=k,event=name,constraint=detail,evidence_status='Read source; actual, remembered, approximate and forecast clocks distinguished',dependency=dep,sources=ss(rr));events.append(v);ne.append(v)
def res(k,name,detail,rr):
 v=dict(id=f'R-{len(resources)+1:03d}',kind=k,entry=name,calculation=detail,status='Provisional evidence record; no substantive approval or application',sources=ss(rr));resources.append(v);nr.append(v)
ev('Revised current life','arena timing','Eight, ten and seventeen days; rest rule','3018/10/17maybesuccessivegaps,notonezeropoint. FYpractice≤4bouts/month;forcedchallengerulesallow≥8daysrest. Eighty-tierwinsversus18monthwindowheldSR138,carry-inwinspossible.',[(279,58),(301,44),(301,45),(301,46),(301,54),(304,35)])
ev('Revised current life','ellipsis / breakthrough','Three months to Revolution Three middle','301three-monthjump, FYThreeinitial→middle;BaiThreepeakassists. CurrentBai92%afteranother1point. Tiearrivalparallel,notextraelapsedmonths.',[(301,63),(301,73),(301,75),(301,83),(301,96)])
ev('Past report / current residence','year/month query','Tie clocks','302fewmonths-sinceeyefight versusyears-saving35 localquery. Deathnews>2yearsbefore15 versus273nearly1year+cityintervals broaderSR134. TieMu28 is his age,notTieRuoNan’s.',[(273,23),(302,3),(302,14),(302,15),(302,22),(302,30),(302,35)])
ev('Revised current life','visits and departure','Tie Ruo Nan audience','Firstvisit,eveningsecond,nextmorningthird;fourthmeeting303. Actualdeparture304withTieDaoKu. PoisonVowofferednotshownused.',[(302,47),(302,49),(302,55),(302,63),(303,8),(303,34),(303,74),(304,1),(304,2)])
ev('Revised current life / former life','long ellipsis and biographical ages','Year-plus to third city','304yearplusellipsis;1.5yearpromotionwindow;2yearsShangarrival;3092plusyears.305QiuNiu30compatible269near30notprecisely30. XinCiformer-life6yearpromotionforecastnotcurrentelapsed.',[(304,15),(304,35),(304,40),(305,22),(305,56),(309,30)])
ev('Revised current life','refinement and training','Four failures and next auction','Fourfailures30434/46;typicallymonthlyattempt57notproofoneeverymonthsincearrival. Soulrecovery>monthforecast55.2shichenpractice≈4h.7daystonews84,7moretoauction30510.',[(304,34),(304,46),(304,55),(304,57),(304,65),(304,84),(305,10)])
ev('Revised current life / institutional schedule','annual versus exceptional opening','Xin Ci promotion plans','Annualassessmentalreadyover30966,normalonevacancy. FYstillthisyear30976dependsYaZiexceptionaldismissal31166,notcontradictorycalendar. LastXinCimeeting10daysprior30586.',[(305,56),(305,86),(309,66),(309,76),(311,66)])
ev('Revised current life','forecast and elapsed days','Leak, concession and dismissal','3092/3dayforecastversus3103/4dayactualoverlapandnotexactclock. Daysafterconcession31160removaland3yearbanishmentprospective,not3elapsedyears.',[(309,49),(310,1),(311,51),(311,60),(311,66)])
ev('Revised current life','breakthrough / challenge notice','Three upper then peak','312assistedmiddle→upper,SilverRelicthen~2shichen≈4h→peak. Challengesyesterday,Baifighttomorrow:noticeinterval≠eight-dayrestsincepriorbout.',[(312,15),(312,30),(312,42),(312,57),(312,58),(312,69)])
ev('Revised current life / observed history','first defeat and next scheduled fight','Bai loses; FY fight seven days later','314Baisurrenders,315firstlossconfirmation. FYvsJu7dayslaternotyetfought. Baiabsentfromhomebutphysicianlocationknown31535.301Zhuconcessionseparatesunfinished300fromnowwin.',[(301,14),(301,17),(314,149),(315,2),(315,12),(315,14),(315,35)])
ev('Older personal history / future estimate','not present clock','Yan and Ju backstory, FY odds','Oldduelfromdaythroughnighttodawn31566–67separatehistory. FY30%currentwinestimate/60%ifrefinementsucceedsnotobjectiveguaranteeorcompletedoutcome.',[(315,24),(315,26),(315,66),(315,67)])
res('Fight outcomes / unspecified loot','Fourth-tier victories','Zhuconcedesalive,Guprizeunreported. JinBianYuankilled;LiaoHuaDongsparedbyreferee;ZhongDemotionlessnotexplicitdeath. Noinventedlootidentities.',[(301,14),(301,17),(301,44),(301,45),(301,46)])
res('Bodily effects / consumption / sale','Copper Skin and turtle; Canopy sold','ThreeCopperSkinconsumedpermanentdefence,Twoformtemporary. Fullturtleforcereportedafterpriorhalf,completionplausiblenotcertifiedextra1.5turtles. Canopysold30195,GoldenShieldretained;notFlyingBoneShielddisposal.',[(297,87),(301,90),(301,91),(301,92),(301,95)])
res('Loot confirmation / replacement / medical funding','Tie Dao Ku Hand Blade','3024confirmsBaitookHandBlade;Tieboughtreplacement36. PhysicianFivehealingneeded,100000fee;RuoNanfundswithElderGu,exactamountnotshown. Treatmentnotyetshowncomplete.',[(298,113),(302,4),(302,29),(302,33),(302,36)])
res('Inventory / false claims / contingent sale','Blood Moon and Skull','BloodMoonlentforinspection30363,notgivenaway;claimedclanbequest/rescuefabricated. BloodSkullsalediscussedonlycontingency30283–85,notexecuted. NoPoisonVowuseafterTieofferconfirmed.',[(302,83),(302,85),(303,34),(303,63),(303,64),(303,66)])
res('Failed refinement / permanent force','Four strength Gu lost','BrownBear,horse,ox,turtleGuconsumed/lostacross4failedBitterStrengthattempts. TheirDao-markbodilyforcesremain;noautomaticstrengthloss. BitterStrengthnotowneduntil31151.',[(292,36),(292,37),(304,34),(304,46),(311,51)])
res('Aptitude / advancement','Bai92→93 and XinCi20→59','Bai30192;30493with7pointsto100supports+1not+2SR135. XinCiforcedawakeninginitial20GradeD,raised59GradeC,onepointfromGradeB;currentOneupper30968. Noimmortalaptitudeupgradeinferred.',[(301,83),(304,80),(304,81),(305,71),(309,68)])
res('Loans / liquidity / unpriced purchases','Auction funding','FYnear1million+Weinear1millionloan+XinCi100–300kloan=>2millionplusavailableplausible. Borrowedfundsnotnetwealth. ChiWennoloan. WeilaterunpricedlightGu,BaiunpricedTornado,notthreeTornadoGu.',[(304,95),(306,21),(306,24),(306,27),(306,30),(306,33),(307,35),(308,71),(308,72)])
res('Auction payments / ownership','Frost Arrow, Bitter Strength and Feng Qi','BaiFrostArrow150000,40000statedpremium. YaZiBitterStrength810000actual,notFY. FYFengQi500000actual. LostWindWillow/WindChasebidsnotpayments. YaZiatleast1.2mfittingbankruptcyafterextra500kifunder1.31m.',[(306,6),(306,91),(307,15),(307,34),(308,21),(308,54),(308,55)])
res('Proxy purchase / consumed information Gu','Lotus Lord recipe','Wei670000bidonFYbehalf30912,not2payments. FourHeartInscriptionGuconsumedtransfersrecipealreadyrefinedbyWei. FYtotalnamedauctionoutlay500000+670000=1170000. Recipeunappraisedanduntested;noFourLotusowned.',[(308,105),(309,10),(309,12),(309,13),(309,15),(309,20),(309,22),(309,23)])
res('Contract loophole / asymmetric removal / transfer','Bitter Strength finally acquired','Baiwasinformedthirdpartybeforevow;leakdoesnotestablishFYstillbound. YaZivowretaliation3114consistentownrestrictionstillactive. BitterStrengthsurrendered31151,810knotnewFYcost;othercompensationnotitemisedreceived.',[(310,57),(310,66),(310,68),(311,4),(311,5),(311,45),(311,49),(311,51)])
res('Consumed relic / essence stages','Revolution Three peak','301middle;312upperthenSilverRelicconsumed→peak. Threeessencepale/variegated/bright/snowysilver9–11. LotusofferedBai/refused,notloaned. Cicadapressuremanageablebutincreasing.',[(312,9),(312,10),(312,11),(312,15),(312,42),(312,43),(312,57),(312,58),(312,63),(312,68)])
res('Killer move / attention / Gu count','Five active streams, autonomous vitality','BaiIceBlade,IceCrystal,RotatingHeel,Tornado,FrostBreath5active;Vitalityautonomous3146. Upgradedstationarystormnotoldstormmobilityrule. Yan2FourSnakes+4ThreeClaws+FuelOil,combineddragonnotactualFiveGuowned.',[(313,55),(313,56),(314,6),(314,13),(314,20),(314,74),(314,80),(314,108),(314,111)])
res('Destruction / vital transfer / backlash','Bai first defeat','Yanloses1FireSnake+2FireClawGu314146. ReceivesBai’sIceCrystalThreealive,vitaltransfercausesbleeding164. NomandatoryvitalGuownerdeath. FrostDemonreplacementonlyWeihope;notbought.',[(314,146),(314,148),(314,149),(314,161),(314,162),(314,163),(314,164),(314,169)])
res('Vault / orders / future contingency','Lotus stock and Hard Qi','Shangvault2ThreeLotus+1FourLord,notFYholdings/freegifts. JuorderedtakeFYLotusifwin/present,elsemustnotclaimAllOutEffort. HardQialreadyowned,StrengthQiwishonly. FYrefinementoutcomenotshownby315.',[(315,26),(315,43),(315,45),(315,51),(315,84),(315,86),(315,87),(315,88)])
np=sum(len(c['paragraphs']) for c in batch);nc=sum(sum(map(len,c['paragraphs'])) for c in batch);tp=sum(len(c['paragraphs']) for c in cs);tc=sum(sum(map(len,c['paragraphs'])) for c in cs)
save('proposal-ledger.json',ledger);save('chronology-register.json',dict(scope='Sequential through315; current, remembered, hypothetical and approximate clocks distinguished',entries=events));save('resource-register.json',dict(scope='Sequential through315; ownership, loans, proxy purchases, permanent effects and consumption distinguished',entries=resources))
progress=load('history/before-batch016-reading-progress.json');progress.update(sequential_chapters_completed=list(range(1,316)),paragraphs_read=tp,paragraph_characters_read=tc,next_chapter=316,remaining_chapters=2019,batch_report='Batch-016-Chapters-301-315.md',scope='Full sequential Chinese-source reading through315; not a fresh bilingual/live-site audit',whole_novel_chronology_verified=False)
progress['batches'].append(dict(id='016',chapters=[301,315],paragraphs=np,characters=nc,reading_segments='Seven complete untruncated two-chapter outputs and complete315; adaptive15'))
progress['chapters'] += [dict(chapter=c['corpus_chapter'],file=c['file'],title=c['title'],paragraphs=len(c['paragraphs']),first_paragraph=1,last_paragraph=len(c['paragraphs'])) for c in batch];save('reading-progress.json',progress)
save('batch-016-reading-log.json',dict(status='Complete',endpoint=315,next_unread=316,segments=[dict(chapters=[a,a+1],status='Full paragraph sequences read; untruncated',paragraphs=sum(len(by[n]['paragraphs']) for n in [a,a+1])) for a in range(301,315,2)]+[dict(chapters=[315],status='Full paragraph sequence read; untruncated',paragraphs=len(by[315]['paragraphs']))],note='Actual reading, not extraction-only coverage.303p16 explicit reader-facing omission preserves numbering and source. No invented timestamps.'))
text=['# Numbered Chinese source: Chapters301–315','Original wording and paragraph numbering retained, except an explicit reader-facing omission303p16 for a sexualised young-character description. Original EPUB and internal extraction unchanged. All original paragraphs read.']
for c in batch:text += [f"## Corpus chapter {c['corpus_chapter']}: {c['title']}",f"Volume: {c['volume']} | EPUB: {c['file']}"]+[f"{i}. {reader(c['corpus_chapter'],i,t)}" for i,t in enumerate(c['paragraphs'],1)]
(r/'Batch-016-Numbered-Chinese-Source.md').write_text('\n\n'.join(text))
for name,vs in [('Chronology',ne),('Resources',nr)]:
 out=[f'# Batch016 {name} jotter','All provisional; no substantive source edits.']
 for v in vs:
  out += [f"## {v['id']}: {v.get('event',v.get('entry'))}",v.get('constraint',v.get('calculation'))]
  for z in v['sources']:out += [f"Ch{z['chapter']} p{z['paragraph']}",'> '+reader(z['chapter'],z['paragraph'],z['text'])]
 (r/f'jotters/Batch-016-{name}.md').write_text('\n\n'.join(out))
out=['# Batch016 continuity and proposed corrections','All new proposals held. SR118 Shang-title candidates strengthened; Bai component remains downgraded. SR099 remains withdrawn.']
for v in new:
 out += [f"## {v['id']}: {v['category']}"]+[f"**{k}:** {v[k]}" for k in ['recommended_action','rationale','confidence','dependencies','status']]
 if 'copy_items' in v:
  for z in v['copy_items']:out += [f"### Ch{z['chapter']} p{z['paragraph']}: {z['original']} → {z['replacement']}",z['confidence'],'> '+reader(z['chapter'],z['paragraph'],src(z['chapter'],z['paragraph'])['text'])]
 else:
  for z in v['locations']:out += [f"Ch{z['chapter']} p{z['paragraph']}",'> '+reader(z['chapter'],z['paragraph'],src(z['chapter'],z['paragraph'])['text'])]
(r/'jotters/Batch-016-Continuity.md').write_text('\n\n'.join(out))
(r/'jotters/Batch-016-Preserve.md').write_text('''# Batch016 preservation cautions
- Tie Ruo Nan mistakes the alias and Extreme Physique history; FY’s rescue/bequest account is fabricated. These are not corrections to actual Qing Mao events.
- Four failed refinements destroy strength Gu, not already-installed bodily Dao marks. Canopy sale is not Flying Bone Shield disposition. Copper Skin RevolutionThree is consumed; RevolutionTwo form is temporary.
- Own funds, borrowed funds and proxy auction payments are different. FY500000FengQi+670000recipe=1170000. YaZi810000BitterStrength notFYoutflow; later surrender adds no second purchase. Loans not gifts or net wealth.
- XinCi20→59 aptitude is retrospective awakening+upgrades; currentlyOneupper. Bai92→93 supportsonepoint; reserve90 from299isnotaptitudeproof.
- Annualassessmentover doesnotpreventexceptionalvacancyafterYaZidismissal.3yearbanishmentprospective.2/3dayforecastand3/4dayactualnotcertifiedconflict.
- PoisonVow loophole is a cover consistent with pre-informed Bai; FYalreadyremovedhisrestriction,YaZi stillbound. No newTieoath actuallyshownused.
- Near-upper forecasts not exact breakthrough dates.312actualupperthenSilverRelicconsumed→peak. Same-stage assistance wanes; SR099 stayswithdrawn.
- Challenge notice two days is not eight-day rest since previous match.8/10/17days can be successive intervals.18month promotionwindowmaycarryearlierwins;do notforcecalendarrepairbeforecommon-scopeproof.
- Bai upgradedIceStormhas5activecontrols;Vitalityautonomous. Not6activeattentionstreams.7YanGucomponents do notprove7independentcontinuousstreams. Newstormimmobile doesnotinvalidateoldmovingversion.
- FireClawconstructdispersal31341bodyreturns42notdeath;314146explicit1Snake+2Clawsdestroyed. IceCrystaltransferredaliveafterconcession,notdestroyed;vitalbacklashnotmandatoryownerdeath.
- Bai firstdefeat314confirmed315,missingfromhomebutphysicianlocationknown. FrostDemonreplacementnotbought. Yan/Ju stagedrivalry is deliberate reveal.
- VaultLotusstocknotFYproperty/freeaward. SecretorderprotectsAllOutEffortifFYloses; noactualtransfer. JuHardQiowned,StrengthQionlywish. FYvsJu andnewrefinementstillunresolved315.
''')
stand=load('history/before-batch016-working-standards-register.json');stand['coverage_through']=315
su={'WS-01':'303falseExtremePhysique/rescue/bequestexplanations,310loopholecoverand311stagedarenarivalrykeepbeliefseparatefromfact.','WS-02':'Bai92+1=93,7pointsto100. FYauction500k+670kproxy=1.17m; no doublecountYaZi810k.','WS-03':'FY301middle,312upperthenSilverRelic→peak;SR099withdrawalreinforced. Bai93,Threepeak. XinCi59GradeC,Oneupper.','WS-04':'Canopysold;4strengthGuinputsfailednotbodilyforceerasure. IceCrystaltransferredalivewithbacklash. Vitalityautonomousvs5activeGu.','WS-05':'302months/yearsquery;deathnews2yearanchorunreconciled. Arena80/4monthly/18monthscopehold,noforceddate.','WS-06':'Borrowedliquiditynotnetwealth;Wei670kproxyforFYnotsecondpurchase. BitterStrengthreceived311;unpricedcompensationnotinvented.','WS-07':'FireClawfewzhangrangewithcastermovingnotprovencontradiction. NewIceStormimmobileisnewdesignfault.','WS-08':'QiuNiu30vspriornear30notprovedageerror. TieMu28notRuoNanage. Prospective3yearbanishmentnotelapsedtime.','WS-09':'Localcopycandidates;Hail→IceExplosion31297strong. ShangBuLichief→elder30653strong. No blanketFrostSpit/Breathrename.','WS-10':'315/2334actualread;2019remain.139records137held2withdrawn,allsubstantiveapproved/appliedfalse. Backup300verifiedatpackaging;lateruploadreceiptseparate.','WS-11':'Workingmaximunchanged;recognisablerefrainsandviewpointpreserved. No blanketnarrativecertification.','WS-12':'30536confirmsChaoFengformer-lifenear家主,strengthening26972.304YaZi少族长wrongShangoffice;Baitwinscomponentstillunresolved. Tie8juniorlordssystemdiffers.'}
for v in stand['entries']:v['batch016_update']=su[v['id']]
save('working-standards-register.json',stand)
out=['# Working editorial standards','## Evidence checkpoint: Chapters1–315','Working rules are not whole-novel factual certification or manuscript approval. Cultivation terminology: Revolution.']
for v in stand['entries']:out += [f"## {v['id']}: {v['topic']}"]+[f"**{k}:** {v[k]}" for k in ['status','rule','evidence','reopen','batch016_update']]
(r/'WORKING-STANDARDS.md').write_text('\n\n'.join(out))
def quote(c,p):return f"**Ch{c} p{p}:**\n\n> {reader(c,p,src(c,p)['text'])}"
report=f'''# Sequential close-reading review: Chapters 301–315
## Batch 016 | The Omniarch

**Actual sequential coverage: 1–315 of 2,334. Next unread: 316.**

Fifteen chapters fully read in eight complete, untruncated outputs: **{np:,} paragraphs / {nc:,} paragraph characters** this batch. Cumulative: **{tp:,} paragraphs / {tc:,} characters**. This is Chinese-source close reading, not a fresh bilingual or live-site audit.

**Six new records, SR134–139**, including **{len(fixes)} individually held copy candidates** in SR139. Cumulative **139 records:137 held, two withdrawn**. No substantive proposal approved or applied. Cultivation terminology remains **Revolution**. Whole-novel chronology remains uncertified.

## 1. Findings at a glance

| Record | Finding | Proposed treatment | Confidence |
|---|---|---|---|
| SR134 | Tie’s months versus years; larger death-news clock | Prefer local这段时间; hold exact global date | High local, moderate global query |
| SR135 |92% becomes93%, but increase says two points | 两分 → 一分 | Very high |
| SR136 | Shang Bu Li called clan leader | 族长 → 家老 | Very high |
| SR137 | Hail Gu named for an ice-detonation effect | 冰雹蛊 → 冰爆蛊 | Very high |
| SR138 |80 wins, four monthly bouts and18-month window | Reconcile scope/carry-in wins before changing figures | Conditional query |
| SR139 | Located copy faults, names and staging | {len(fixes)} individual candidates | Individually qualified |

## 2. Bai Ning Bing:92%, then93%, not a two-point increase

{quote(301,83)}

{quote(304,80)}

{quote(304,81)}

The endpoints are independently supported:92% in301;93% in304; seven points remaining to100%. The smallest repair is **又回升了两分 → 又回升了一分**. Changing93% to94% would also require changing the following seven to six, with less support.

275’s earlier one-point increase now fits91% before301. This is an aptitude sequence, not a licence to alter299’s90−70=20 reserve statement: current essence level and maximum aptitude capacity are distinct.

Shang Xin Ci’s separate progression is retrospectively confirmed in305p71: forced awakening initially yields20%, Grade D; subsequent costly intervention raises her to59%, Grade C, one percentage point short of Grade B. **五成久 → 五成九分** is the local copy candidate. Her actual cultivation is **Revolution One upper stage** at309p68, not the level of her father or protectors.

## 3. Tie chronology: a local repair and a larger unresolved clock

{quote(302,3)}

{quote(302,35)}

The eye injury is explicitly a few months old, but the saving period is phrased as years. Preferred conservative candidate: **这些年 → 这段时间**. “These past few months” is also possible if the passage is specifically measuring his post-injury saving.

{quote(273,23)}

{quote(302,15)}

The larger timeline is less securely repairable.273 places the return to Revolution Three at nearly one year since leaving Qing Mao. The ensuing city scenes and301’s three-month jump create tension with302’s claim that news of Tie Xue Leng’s death arrived more than two years earlier. Yet unquantified ellipses prevent an exact upper bound.

Accordingly, **do not automatically replace every two-year reference with one year**. Distinguish the death, arrival of its news, Tie Ruo Nan’s career and Tie Dao Ku’s city residence.304 then introduces a further year-plus ellipsis, after which two-plus years in Shang city is repeatedly stated. Those later references belong to a different checkpoint and must not be shortened merely to fix302.

Tie Mu is28; that is not Tie Ruo Nan’s age. Shang Qiu Niu is now30; being “nearly thirty” around two years earlier can be compatible, so no exact-age correction is justified there.

## 4. Two strong identity repairs, and an earlier title query strengthened

{quote(306,53)}

Shang Bu Li is introduced as Shang Yan Fei’s subordinate and senior administrator. **更是商家族长 → 更是商家家老** preserves the role without inventing a second clan chief. His seniority over junior lords does not make him the clan leader.

{quote(312,97)}

{quote(313,40)}

The proposed effect is detonating icicles.299 already defines Ice Explosion Gu, and313 explicitly uses it for this purpose. Preferred **冰雹蛊 → 冰爆蛊** at312p97. This does not license merging all ice-type names: the older Frost Spit and later Frost Breath labels may reflect a replacement or naming drift across the long interval and remain separately tracked.

{quote(269,72)}

{quote(305,36)}

The repeated former-life rivalry now explicitly concerns Shang Chao Feng nearly becoming **family head**, strengthening **SR118’s269p72少主 → 家主** candidate. The new304 references also repeatedly call Ya Zi少族长 even though his office is one of Shang’s competitive junior-lord posts; those join the strong Shang-specific correction cluster.

The **Bai-twin title component remains downgraded**. Evidence about Shang’s offices does not decide Bai succession. Tie’s eight junior lords and explicitly different political arrangements reinforce the need for clan-specific treatment.

## 5. Arena chronology: do not turn an ambiguous window into a certified error

{quote(301,54)}

{quote(304,35)}

The earlier rule279p58 calls for80 net wins in the fourth city before advancement. At no more than four bouts in each monthly allocation,80 new wins require at least twenty such allocations, whereas304 describes the climb over a year and a half.

This is worth recording, but not yet a proved contradiction:
- The preceding three-month phase may supply wins already held at the start of the eighteen-month window.
- Four bouts monthly is Fang Yuan’s stated practice at that earlier stage, not necessarily an unchanging rule for the entire climb.
- The exact scope of the tier counter and of这一年半 needs confirmation.

**SR138 holds these dependencies.** Only if the same window starts at zero, requires80 additional wins and remains capped at four throughout should a longer interval or a clarified temporary cap be proposed. No numerical rewrite is authorised now.

Likewise,301’s eight-, ten- and seventeen-day markers can be successive intervals rather than three dates measured from Zhu Ba’s fight.312’s challenge issued yesterday for a fight tomorrow gives a notice period, not the elapsed rest since the previous bout. It therefore does not itself violate the minimum eight-day rest protection.

## 6. Money: loans, proxy bids and actual transfers

The auction’s financial sequence is coherent when ownership and custody are separated:

- Fang Yuan has accumulated nearly1000000 stones. Wei lends nearly1000000; Xin Ci lends an estimated100000–300000. The later statement of over2000000 available is plausible. **Borrowed liquidity is not net wealth.**
- Bai buys Frost Arrow for150000. The stated40000 premium compares this with her earlier110000 bid, not a guaranteed universal market valuation.
- Shang Ya Zi buys Bitter Strength for810000. Fang Yuan withdraws; this is not his expenditure.
- Fang Yuan buys Feng Qi Gu for500000.
- Wei bids670000 for the Lotus Lord recipe **on Fang Yuan’s behalf**, confirmed309p12. Do not count two670000 payments.
- Thus Fang Yuan’s two named auction purchases cost **1170000**. Loan repayment and exact remaining balance are not supplied.
- Wei also obtains an unpriced light Gu; Bai obtains an unpriced Tornado Gu. “Three bids” does not mean three Tornado Gu.
-311p51 finally puts Bitter Strength in Fang Yuan’s hands as Ya Zi’s concession. No further810000 payment by Fang Yuan occurs. Additional compensation is discussed but not itemised as received.

{quote(309,12)}

The recipe arrives through a Revolution Four Heart Inscription Gu, already refined by Wei and consumed to imprint it on Fang Yuan. This differs from borrowing and returning a reusable bookworm. The recipe remains unappraised and untested, and Fang Yuan does not yet possess a Revolution Four Lotus.

## 7. The oath plot is deliberate, not a forgotten mechanism

310 discloses the actual confidentiality clause: no disclosure to an **uninformed third party**. Bai had already been informed before the oath. Fang Yuan uses that loophole to conceal the more dangerous fact that he had removed his own restriction long ago.

Ya Zi’s restriction remains active.311 shows backlash when he attempts harm with the stone table. This is consistent with asymmetric removal, not proof that Fang Yuan is still bound. Bai’s subsequent fear of textual loopholes does not mean she has learned about the oath-breaker Gu.

The annual junior-lord assessment has already passed, but Ya Zi’s exceptional dismissal creates another opening. His **three-year banishment** is a future sentence, not three elapsed years. The former-life six-year wait for Xin Ci’s promotion is also a different timeline.

Ya Zi’s accounts are said to circulate in precise detail, but the text does not reproduce the disputed public-price figures. **SR120’s650000/600000 basis query remains unresolved.**

## 8. Cultivation and inventory: confirmed changes, not inferred disappearances

Fang Yuan advances to **Revolution Three middle stage** in301, then to upper stage in312. He finally consumes the saved Silver Relic and reaches **Revolution Three peak stage**, after about two 时辰, conventionally four hours.

This further supports **SR099’s withdrawal**. Reunion-assisted cultivation continues to be useful after reaching Revolution Three; its benefit diminishes when donor and recipient reach the same peak stage. Bai advancing to Four would again widen the advantage. Earlier “a few days” breakthrough estimates are forecasts, not guaranteed completion dates.

Other confirmed dispositions:
- **Canopy Gu is sold** at301p95. This does not resolve Flying Bone Shield’s earlier missing disposition, SR123.
- Revolution Three Copper Skin is consumed to leave permanent defence; its Revolution Two counterpart is temporary.
- Four strength Gu are lost across four failed Bitter Strength refinements. Their established bodily Dao marks are not erased merely because the original Gu are lost.
- The previously incomplete turtle force is now described as a full turtle’s force. Completion is a reasonable reading; an extra one-and-a-half turtles is not established.
-302 confirms Bai took Hand Blade Gu after defeating Tie Dao Ku. He buys a replacement. Funding for the100000-stone eye treatment is supplied, but completed treatment is not yet shown.
- Blood Moon is handed over for inspection, not sold or gifted. Fang Yuan’s claimed clan bequest and rescue story is fabricated. The proposed Blood Skull sale remains a contingency.

## 9. The battle’s Gu counts and outcome

Bai’s upgraded Ice Blade Storm has **five actively controlled components**: Ice Blade, Ice Crystal, Rotating Heel, Tornado and Frost Breath. Vitality runs autonomously after activation, explicitly explained314p6. Counting it as a sixth simultaneous active stream would create a false inconsistency.

The new storm’s inability to move is a revealed flaw in the upgraded design, not a retroactive claim that the earlier version could never move. Yan Tu’s two Fire Snake Gu, four Fire Claw Gu and prepared fuel field likewise do not establish seven independently controlled continuous streams. The combined dragon-like attack is not acquisition of an actual Revolution Five Fire Dragon Gu.

313’s dispersed claw effect returns as a Gu; no destruction is established there.314p146 later explicitly destroys **one Fire Snake Gu and two Fire Claw Gu**.

{quote(314,149)}

{quote(314,162)}

{quote(314,164)}

Bai concedes her **first defeat**, transfers Ice Crystal alive and suffers vital-Gu backlash. The transfer does not kill her or destroy the Gu. Yan receives one Revolution Three Gu but loses more valuable components. Frost Demon replacement remains Wei’s suggestion, not an acquisition.

Bai is absent from Nan Qiu Garden, but315 identifies her location at the physician’s premises. “Missing from home” must not become “dead,” “escaped” or “untraceable.”

## 10. Copy evidence and endpoint

The continuity jotter contains all **{len(fixes)} individually qualified candidates**, with source excerpts. Examples:301队长→对战;305商丘牛→商囚牛;310接触毒誓蛊→解除毒誓蛊;314龙眷顾→龙卷蛊. The suggestion to change313p54站在场外 to站在远处 remains conditional:场外 may refer to the immediate melee rather than the arena boundary. It is not proof of an illegal departure.

The numbered source companion supplies the full chapter text, with the sole reader-facing omission303p16 explicitly marked; original numbering, EPUB and internal extraction remain unchanged. All original paragraphs were read. The agreed narrative maxim remains **“Man is the most intelligent of all living things.”**

**Endpoint315:** Fang Yuan is Revolution Three peak, Bai is Revolution Three peak with93% aptitude and has lost Ice Crystal. Fang Yuan versus Ju Kai Bei is scheduled seven days after Bai’s defeat, but has not happened. Fang Yuan has begun a new refinement; its result is not shown. Ju already owns Hard Qi Gu, while Strength Qi is only something he wishes for.

The clan vault’s two Lotus Gu and one Lotus Lord Gu are not Fang Yuan’s property. Shang Yan Fei secretly orders Ju to take Fang Yuan’s Lotus if victorious and present, but not to take All-Out Effort otherwise. This is an intended future selection, not a completed transfer.

Saved: **{len(events)} chronology entries / {len(resources)} resource entries /139 proposals /12 working standards**, cumulative workbook, five jotters and eight-segment reading log. At packaging the verified remote backup reaches300; any subsequent315 upload is separately documented.

**Next unread:316.** All substantive emendations remain unapproved and unapplied. No whole-novel factual certification.
'''
(r/'Batch-016-Chapters-301-315.md').write_text(report)
old=(r/'update_batch010.py').read_text();wb=old[old.index('# Workbook: cumulative'):old.index("(r/'CURRENT-STATUS.md').write_text")]
wb=wb.replace('1–220 of2334','1–315 of2334').replace("('Next unread',221)","('Next unread',316)").replace('103total;102activeheld;1withdrawn','139total;137activeheld;2withdrawn').replace('range(10,0,-1)','range(16,0,-1)').replace("v['batch010_update']","v['batch016_update']").replace('Batch-010-Chapters-201-220','Batch-016-Chapters-301-315').replace('CHAPTERS201–220','CHAPTERS301–315').replace('Chapters201–220','Chapters301–315').replace('Twenty complete chapters; personal clocks and inventory scope distinguished','Fifteen complete chapters; aptitude arithmetic, chronology queries and contractual causality').replace('Ch151,201p22,203p84 restricted excerpts','Ch151,201p22,203p84,250pp24–31/33/35–36,258pp70–74/79,296pp95–97,303p16 restricted excerpts')
exec(compile(wb,'workbook-and-docx','exec'))
(r/'CURRENT-STATUS.md').write_text(f'''# Sequential review checkpoint

Completed1–315/2334; next316;2019remaining. Batch016:{np}paragraphs/{nc}characters. Cumulative{tp}/{tc}.139proposals:137held+SR047/SR099withdrawn. SixnewSR134–139;SR139contains{len(fixes)}copycandidates. {len(events)}chronology/{len(resources)}resources.12standards. Allsubstantiveapproved/appliedfalse. Revolution terminology.

ReportBatch-016-Chapters-301-315.md/.docx; numberedsource30316omittedandmarked, originalsourcefullyreadunchanged. Fivejotters, readinglog, workbook/registers updated. Detailedhandoff jotters/batch-016-working.md.

Carry: SR13430235years-savingvsfewmonthssinceeyefight→这段时间preferred;302deathnews>2yearsversus273near1year+cityintervals+3013monthsglobalquery, noexact1yearrepaircertified.304yearplusnewellipsisand309Shang2plusyearsnotshortened. SR13530192→30493+7remaining supports两分→一分. SR13630653ShangBuLi族长→家老. SR13731297冰雹→冰爆. SR13880tierwins/4monthcap/18monthwindowneedsstart/carry-inwins/policycontinuity;nofixedcorrection. SR139individualcopyitems. SR118304YaZi少族长→少主strong,30536家主supports26972ChaoFengformer-lifeoffice家主;Baitwinscomponentstilldowngraded. SR099withdrawalreinforced301/304,SR120650k/600kpublicbasisunresolved,SR123Canopysale≠FlyingBoneShielddisposal.

FY301ThreeMiddle,312upperthenSilverRelicCONSUMED~2shichen→peak. BaiThreepeak93aptitude;XinCi20D→59Cactualawakening/upgrades,Oneupper309. CopperSkinThreeconsumedpermanent,Two temporary;Canopysold30195. FourfailedstrengthGuinputslostbutbodyforcesremain. Fullturtleafterpriorhalfcompletionplausible,noextra1.5count. TieDaoKucoreHandBladelootconfirmed3024,boughtreplacement,100khealingfundsprovidednotcompletedtreatment. RuoNan4visitsleaveswithTie,offeredoathnotshownused. FYfalsephysique/rescue/bequestclancovernotfacts;Skullsalecontingencynotactual.

AuctionFYownnear1m+Weinear1mloan+XinCi100–300kloan⇒>2mliquidity,notnetwealth. BaiFrostArrow150k+unpricedTornado. YaZi810kBitterboughtthen31151concedesFYwithoutnewcost. FYFengQi500k+LotusLordrecipe670kproxyWei=1.17m;FourHeartInscriptionconsumed,recipeunappraiseduntested,noFourLotusyet. Othercompensationunitemised,loanrepaymentunreported. YaZi3yearbanishmentfuture;annualassessmentpastbutexceptionalvacancyopensforXinCi. Pre-informedBaileakcontractloopholeconcealsFYpriorremoval;YaZistillbound311backlash. Price650k/600knotreproduced310.

BaiIceStorm5active+Vitalityautonomous,not6. Newstormimmobile,newdesignfault. Yan2FourSnakes+4ThreeClawsinitial,loses1Snake+2Claws314146. BaiFIRSTLOSS,concedesIceCrystalalive,vitalbacklashbleeding,notdead. NewFrostDemononlysuggested. Baiatphysician31535notmissingdespiteawayhome. FYvsJu7daysfuture31512notfought;newrefinementoutcomeunknown. JuHardQiowned,StrengthQiwishnotowned. Vault2Lotus+1LordnotFYproperty. ChiefsecretordersJuifwinsrequestLotusifpresent,neverAllOutotherwise;noactualtransfer. Next316.

Remoteverified300atpackagingcommit2dffb2333e88c896ce73379ee3c21a1643cdc4da;any315receiptseparate. Noautomaticbackgroundreading. PreserveoriginalEPUB/uploads/sourcecaptures/sourceJSON. Old22duplicateexportslocallyremovedonlyafterremotehashverification,restoremanifestbackups/Workspace-Cleanup-After-Ch285.json. Remotehistoricfilesretained.016generatoridempotentfrompre016history;earliergeneratorsnotrerun.
''')
assert len(cs)==315 and len(ledger)==139 and len(new)==6
assert all(not v['approved'] and not v['applied'] for v in ledger)
assert all(z['text']==src(z['chapter'],z['paragraph'])['text'] for v in events+resources for z in v['sources'])
texts={t for c in cs for t in c['paragraphs']}
for line in report.splitlines():
 if line.startswith('> '):assert line[2:] in texts
sha=hashlib.sha256((r.parent.parent/'benchmark/sources/Gu-Zhen-Ren.epub').read_bytes()).hexdigest();assert sha=='1ef1c29b6bddd7994f56696e2d091363aa8bbcee4889439465a9e2c51437dd5d'
qa=dict(passed=True,chapters=315,batch_paragraphs=np,batch_characters=nc,paragraphs=tp,characters=tc,proposals=len(ledger),held=137,withdrawn=['SR-047','SR-099'],copy_items=len(fixes),chronology=len(events),resources=len(resources),reading_segments=8,next=316,reader_omissions=[[303,16]],source_sha256_unchanged=sha)
save('batch-016-qa.json',qa);print(json.dumps(qa,indent=2))
