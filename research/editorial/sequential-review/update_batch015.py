from pathlib import Path
import json,shutil,hashlib
from openpyxl import Workbook,load_workbook
from openpyxl.styles import Font,PatternFill,Alignment
r=Path('/home/user/editorial/sequential-review')
def load(n):return json.loads((r/n).read_text())
def save(n,v):(r/n).write_text(json.dumps(v,ensure_ascii=False,indent=2))
for n in ['reading-progress.json','proposal-ledger.json','chronology-register.json','resource-register.json','working-standards-register.json']:
 d=r/'history'/('before-batch015-'+n)
 if not d.exists():shutil.copy2(r/n,d)
cs=sum([load(f'batch-{i:03d}-source.json') for i in range(1,16)],[]);by={c['corpus_chapter']:c for c in cs};batch=cs[285:300]
def src(c,p):return dict(chapter=c,paragraph=p,file=by[c]['file'],text=by[c]['paragraphs'][p-1])
def ss(rr):return [src(*z) for z in rr]
def loc(rr):return [{k:v for k,v in z.items() if k!='text'} for z in ss(rr)]
def refs(z):return '; '.join(f"Ch{x['chapter']} p{x['paragraph']}" for x in z)
def reader(c,p,t):
 if (c==296 and 95<=p<=97) or (c==258 and (70<=p<=74 or p==79)) or (c==250 and (24<=p<=31 or p in [33,35,36])) or (c==151 and (31<=p<=67 or p in [98,99])) or (c,p) in [(201,22),(203,84)]:return '[Restricted passage omitted from reader-facing copy. Original numbering retained; original EPUB unchanged.]'
 return t
ledger=load('history/before-batch015-proposal-ledger.json');new=[]
def pro(i,cat,rr,action,why,conf,dep):
 v=dict(id=f'SR-{i:03d}',category=cat,locations=loc(rr),recommended_action=action,rationale=why,confidence=conf,status='Active provisional proposal; no approval',dependencies=dep,approved=False,applied=False,publication_status='HOLD: full 2334-chapter reading and global reconciliation outstanding');ledger.append(v);new.append(v);return v
pro(129,'Li Ran instalment precision: over eighty thousand versus exact balances',[(287,40),(287,42),(288,55),(288,57),(289,14),(289,16),(292,69),(293,52),(293,55)],'If the later balances are exact, prefer287p42 八万多块→八万块 and288p55 八万多块→八万块. Otherwise retain the approximate instalment and explicitly treat the later totals as rounded. Do not silently increase the200000 agreement or invent a refund.','The first payment is twice over80000, but subsequent arithmetic repeatedly uses80000:120000 owed, then50000 paid gives130000 total/70000 owed, then40000 gives170000 total/30000 owed.','High precision tension; moderate repair direction because rounded accounting may be intended.','Source variants and later settlement. Distinguish promised total, amount actually paid, remaining liability and spoken approximation.')
pro(130,'Six-month training compressed to one: total versus additional multiplier',[(289,39),(289,40),(289,41),(293,92)],'Preferred289p41 比常人多出六倍→是常人的六倍; if preserving the source’s 至少半年 literally, candidate 至少是常人的六倍. English: roughly six times the usual daily training time, or at least six times if the lower bound is intended.','A six-month workload compressed to one month requires six times the daily work, not six additional multiples, which literally gives seven times. The source already treats time and workload approximately.','High multiplier-language issue; moderate choice between approximate and lower-bound wording.','Assumes the narrative’s intended proportional workload. Do not turn pain tolerance or all cultivation into a universal linear-rate law.')
pro(131,'Li Hao fight misnames the combatant as Li Ran',[(290,7),(291,65),(291,66),(291,67)],'Preferred291pp65–66 李然→李好 in both places.','The active combatant using Position Swap throughout this fight is Li Hao. Li Ran is the separate undercover ally.','Very high local identity support.','Local substitution only, not a global replacement of either name; preserve the distinct characters.')
pro(132,'Instant Success: suppressing light versus stopping the consumable',[(297,39),(297,49),(297,50),(297,54),(297,55),(297,62),(297,81)],'Prefer297p50 催停一蹴而就蛊→收敛一蹴而就蛊的光辉, or translate as suppressing its light. Retain continued consumption and eventual expiry.','The next explanation explicitly says activation cannot be stopped; light can be suppressed only to prolong the remaining lifetime. 催停 alone risks implying a true pause/reset which the scene denies.','Moderate local precision issue; high confidence in the distinction between suppressing output and cancelling consumption.','Independent witness and later time-Gu mechanics. Do not alter the multiple applications, remaining wings or personal lifespan cost.')
fixes=[(286,30,'一切其他的蛊','一些其他的蛊'),(286,45,'才能希望','才有希望'),(286,51,'喧嚣尘上','甚嚣尘上'),(286,64,'洒杀下去','洒下去'),(286,73,'我都被你逼的','我都是被你逼的'),(287,82,'大声的呼喊','大声地呼喊'),(287,83,'陡荡','震荡'),(288,25,'这两根断裂的石柱','这根断成两截的石柱'),(288,31,'膘肥体状','膘肥体壮'),(288,42,'充足主要支点','充作主要支点'),(288,110,'为了对付我','为了对付你'),(288,110,'得意的大笑','得意地大笑'),(289,60,'被气浪很推一把','被气浪狠狠推了一把'),(289,63,'它的比猛犸','它比猛犸'),(289,78,'在尝一次','再尝一次'),(290,48,'捂住轻笑','捂嘴轻笑'),(290,49,'清楚的很','清楚得很'),(290,50,'安全的很','安全得很'),(291,4,'闪避的很轻松','闪避得很轻松'),(291,33,'用的如此','用得如此'),(291,91,'直觉抡起','直接抡起'),(291,125,'它日狂歌','他日狂歌'),(292,19,'需要修养','需要休养'),(292,27,'锻炼置身','锻炼自身'),(292,45,'就会知道导致','就会导致'),(292,49,'它日狂歌','他日狂歌'),(292,67,'绞动天下','搅动天下'),(292,81,'渡过一段','度过一段'),(293,24,'收纳起架子','收起架子'),(293,40,'半柱香','半炷香'),(293,76,'他们俩个','他们两个'),(294,8,'近世人','近十人'),(294,8,'是必取','誓必取'),(294,13,'好的很','好得很'),(294,14,'死的好','死得好'),(294,14,'死的妙','死得妙'),(294,47,'两位族长','两位少族长'),(294,64,'淡淡的说','淡淡地说'),(294,71,'无疑中','无意中'),(294,80,'压力重生','压力重重'),(295,2,'查的出来','查得出来'),(295,13,'渡过此难关','度过此难关'),(295,38,'不同戴天','不共戴天'),(295,48,'拱着你','供着你'),(296,3,'至始至终','自始至终'),(296,25,'一席人','一行人'),(296,41,'皆有我承担','皆由我承担'),(296,61,'价格太高了','价格抬高了'),(296,91,'二十二余','二十二万余'),(296,95,'供十八位','共十八位'),(296,100,'羞燥','羞臊'),(297,12,'一朵在被','一朵被'),(297,13,'雷光暂起','雷光乍起'),(297,37,'要去了这','要去掉这'),(297,43,'天然元泉','天然真元'),(297,46,'虚影的之上','虚影之上'),(297,88,'折腾的起','折腾得起'),(298,7,'深深的记在','深深地记在'),(298,25,'顺着惯势','顺着惯性'),(298,32,'一道残留','一道残影'),(298,48,'但铁刀苦同时是运转的三转蛊','但铁刀苦运转的同样是三转蛊'),(298,50,'一口不停歇','一口气不停歇'),(298,58,'一捅冰水','一桶冰水'),(298,80,'狠狠的撞','狠狠地撞'),(298,89,'更多的专注','更多地专注'),(298,91,'白凝冰白凝冰','白凝冰'),(298,100,'心中抖沉','心中陡沉'),(298,102,'大不服','大部分'),(298,112,'呼呼的喘','呼呼地喘'),(299,12,'不要动心','不用担心'),(299,33,'慢慢的对','慢慢地对'),(299,33,'一些的阴险','一些阴险'),(299,64,'没事人一眼','没事人一样'),(299,82,'然后在一举','然后再一举'),(299,86,'方源在这些','方源对这些'),(299,88,'笑出身来','笑出声来'),(300,40,'不屑的嗤笑','不屑地嗤笑'),(300,43,'带了给他','带给了他'),(300,50,'虚弱的闪了闪','虚弱地闪了闪'),(300,60,'对于他方源','对于方源'),(300,66,'很好的掩饰','很好地掩饰'),(300,90,'更区区一个','更何况区区一个'),(300,92,'直冲蛊','直撞蛊'),(300,96,'感到了','赶到了'),(300,99,'后座力','后坐力')]
for c,p,a,b in fixes:assert a in src(c,p)['text'],(c,p,a)
v=pro(133,'Located copy and terminology candidates',sorted(set((c,p) for c,p,a,b in fixes)),'Review each listed replacement separately, retaining exact source and paragraph numbering. Do not globally replace names or titles.','Typographical faults, missing words, corrupted subject/object references and local technical names. Missing 少 at294p47 is a narrow local repair, not approval to rewrite every Bai succession title.','Mostly high; individually qualified.','Witness collation; the近十人 candidate repairs a corrupted phrase without certifying Tie Dao Ku’s casualty attribution.')
moderate={(286,30),(286,51),(286,73),(287,83),(289,60),(291,125),(292,49),(294,8),(294,80),(297,13),(298,25),(298,48)}
v['copy_items']=[dict(chapter=c,paragraph=p,original=a,replacement=b,confidence='Moderate: reconstruction, idiom or scope-sensitive wording; collate first' if (c,p) in moderate else 'High local copy support',status='HOLD; unapproved/unapplied') for c,p,a,b in fixes]
for v in ledger:
 if v['id']=='SR-101':v['batch015_update']='294p8 corrupt近世人 likely近十人, but the speech attributes near-ten losses to the trap while earlier9−2−3 leaves4 at blast. Character blame may encompass all8 pursuit deaths. Do not automatically replace this speech with an objective three-death count; earlier220local casualty proposal remains held.'
 if v['id']=='SR-104':v['batch015_update']='294p28 survival suggestion is deliberate bait, followed by55death admission;69 narrator says fabricated pleading account and死无对证.295p44 repeats death-branch account. This reinforces incompatibility with231 but does not authenticate the compiler’s chosen version.'
 if v['id']=='SR-118':
  v['superseded_action_before_batch015']=v['recommended_action'];v['recommended_action']='Retain strong262p65 Shang candidate 保住少族长的位置→保住少主的位置. DOWNGRADE263p75 Bai twins 少族长→少主 to an unresolved clan-specific title query; preserve current wording pending proof of Bai succession rules. Continue holding269p72 former-life Chao Feng future-office query without a settled replacement.';v['confidence']='High Shang office distinction; low-to-moderate Bai twin-title repair and former-life Chao Feng query.';v['batch015_update']='293p70 and294–295 repeatedly call the twins少族长, including their own clansmen. Repetition does not prove correctness, but undermines the earlier high-confidence isolated-title diagnosis. Do not impose Shang’s succession structure on Bai.294p47族长 missing少 can be corrected locally without deciding少主 versus少族长 globally.'
 if v['id']=='SR-123':v['batch015_update']='286 broad inventory reconfiguration and288explicit JumpingGrass sale do not establish the earlier FlyingBoneShield disposition.300 Canopy/GoldenShield fight still supplies no explicit shield disposal; retain query without inventing loss.'
 if v['id']=='SR-060':v['batch015_update']='292 permanent Dao-mark effects and298IceMuscle bleeding control again establish body effects, not the old Gu’s survival or consumption. Still unresolved.'
 if v['id']=='SR-099':v['batch015_update']='Remains withdrawn.296p90 explicitly delays SilverRelic because Bai’s cultivation assistance continues, rather than restoring the speculative before/after substitution.'
events=load('history/before-batch015-chronology-register.json')['entries'];resources=load('history/before-batch015-resource-register.json')['entries'];ne=[];nr=[]
def ev(t,k,name,detail,rr,dep='Global reconciliation, source collation and later anchors outstanding'):
 v=dict(id=f'T-{len(events)+1:03d}',timeline=t,kind=k,event=name,constraint=detail,evidence_status='Read source; narrative clocks separated from inference, plans and approximation',dependency=dep,sources=ss(rr));events.append(v);ne.append(v)
def res(k,name,detail,rr):
 v=dict(id=f'R-{len(resources)+1:03d}',kind=k,entry=name,calculation=detail,status='Provisional evidence register; no substantive emendations approved/applied',sources=ss(rr));resources.append(v);nr.append(v)
ev('Current-life plan / future recollection','not elapsed','Strength-path development plan','Two-to-three-year Shang stay, then Three Kings, then Yi Tian. Infallible inheritance distant; remembered refinement protection not yet acquired.',[(286,26),(286,31),(286,32),(286,34),(286,47)])
ev('Revised current life','purchase and fight intervals','Reconfiguration to Li Ran fight','Negotiations1.5shichen≈3h, Gu arrive2days later, fight another day later. No exact dated starting day.',[(286,61),(286,62),(286,65)])
ev('Ren Zu legend','separate narrative clock','Reputation Gu story','Several days starvation in legendary Ordinary Abyss, not extra Shang days. Abyss/bridge imagery not a measured current-life travel problem.',[(287,61),(287,62),(287,67),(287,93)])
ev('Revised current life','relative days / retrospective actions','Training and third-oath removal','Eight days after Li Ran fight; oath removed a few days earlier; Wu emergency contact three days earlier. Another3days to Wang Han bout. SteelTendon starts28898.',[(288,1),(288,55),(288,59),(288,63),(288,98),(288,99)])
ev('Revised current life','fight counts and forecasts','Seventeen wins, then Li Hao','17wins/0losses2899; LiHao forcedchallenge5days later, confirmed2901. LiRan fight never explicitly fourth, so no proved13wins-in11days error. LiHao29net before encounter.',[(289,9),(289,19),(289,26),(289,90),(290,1)])
ev('Revised current life','workload / elapsed healing','Steel Tendon and recovery','Normal≥6months versus intended1month; sixfold total not sixfold extraSR130.292healingin fifthshichen≈10h in progress;293tendoncompleted, earnings over1month anchor not exactly fixed.',[(289,36),(289,39),(289,40),(289,41),(292,26),(293,89),(293,92)])
ev('Revised current life','arena progression','Eighteenth through twenty-ninth wins','LiHao fight follows17;292 lists19/20/21;29329th and40000payment. Off-page bouts and non-fighting days not reconstructed as exact calendar.',[(289,9),(292,91),(293,52),(293,58)])
ev('Revised current life','negotiation and deadline','Bai extortion contract','30breath deadline intentionally overruns to tea-cup pause. Tie outside>halfshichen.500000 due1day; auction3days after negotiation. Do not treat deadlines as elapsed receipts.',[(295,70),(295,76),(295,77),(295,84),(296,1),(296,12),(296,50)])
ev('Personal versus external clock','targeted acceleration','Instant Success session','3days afterauction; normalboar removal≥19days becomes10plusbreaths; horse2–3months in halfcuptea,oxanotherhalf,turtlehalfcompleted. FYlosesoverhalfyearlife; targetedboar-removalexposure notautomatically19daysFYlife.',[(297,26),(297,31),(297,49),(297,60),(297,64),(297,68),(297,75),(297,81),(297,87)])
ev('Revised current life / unspecified transition','tier promotion and later fights','Thirtieth win; fourth-tier debut','One day aftertimeGu session,30thwin promotesFY. Ellipsis beforeTie registration/Baifight can conceal daygap.299todayFYfirstfourthtierfight does not prove twoFYfights same day.300fight ongoing.',[(297,90),(297,95),(297,98),(297,103),(299,41),(300,121)])
ev('Combat internal timing','cooldown / attention','Five breaths, alternating Gu and maintained states','DirectChargefive-breathreuse limit; alternatingmoveswiththree-breathinterval plus travel does not replace per-Gu cooldown. Changingcontrols demandsattention, maintainingstates differs.',[(290,49),(290,52),(291,26),(298,74),(298,76)])
ev('Conflicting witness / character claim','twins and casualty evidence','Later death account, clan titles and blame','294survivalhint bait;55deathadmission,69narrator死无对证. Ownclanrepeated少族长 weakenssimpleBaititleemendation. Tieaccusationnear10casualties remains attribution/scopetension.',[(293,70),(294,8),(294,28),(294,32),(294,55),(294,69),(295,44)])
res('Recipe / ownership / protection','All-Out Effort recipe and vital Gu','Three-to-Four recipe already obtainedfromLiRan;Five recipe notowned. Cicadavital unchanged. Wei’s suggestion toreplacevitalGu notexecuted. HundredBattlesUndefeatedandGreenMountain protectiondifferent, unacquired.',[(286,15),(286,24),(286,26),(286,36),(286,44),(286,45)])
res('Instalments / liability','Li Ran200000 compensation','Secretdealforrecipe+acting28755. Firstover80000versuslater80000exactquerySR129. +50000=>130000,+40000=>170000;30000remaining. Notfull200000paid.',[(287,40),(287,42),(287,55),(288,57),(289,14),(289,16),(292,69),(293,52),(293,55)])
res('Bodily effects / acquired Gu / sale','Bear completed, charge Gu and tendons','Bearstrengthcompleted28837;2boars+bear+croc atcapacity. JumpingGrassactuallysold;Sideways/DirectChargeowned. DirectChargehalf成=5%standardcapacity, max50pacesunobstructed. SteelTendonowned,continuoususe,IronBoneconsumable.',[(288,37),(288,67),(288,74),(288,81),(288,93),(288,94),(288,96)])
res('Consumption / oath scope','Li Ran and Bai agreements removed','28859 confirmsLiRanrestrictionremoved;29727 laterBai-extortionrestrictionremovedafteronefailedbreakerrefinement. Samecounterpartyrestrictionsnotautomaticallyremoved. Costsunspecified;donotdoublechargepastrecipes.',[(288,59),(296,12),(297,27)])
res('Healing / prices / permanent marks','Self-Reliance and Dao-mark effects','RevolutionThreeSelfReliance45000, boughtduringreconfiguration,selfonly,healsmorestronglywithbodystrength. Tendonmarkscomplicatehealing;durableeffectnotproofGuconsumed. AllOutEffortsmallessencecost;phantomsthemselveszero,wholebuildnotzero.',[(291,105),(291,107),(292,5),(292,9),(292,11),(292,13),(292,26),(292,33),(292,34)])
res('Loot / deaths / reward','Li Hao fight','MountainBackToaddestroyed;PositionSwapvitaldieswithLiHao.3otherGuunnamedlooted. Arena reward6000plus. NoSwapacquisition; 横冲直撞291132doesnotprovecombinedRevolutionFourGuowned.',[(291,131),(291,132),(291,136),(293,86),(293,87),(293,88)])
res('Charges / loans / extortion','Bai party and first500000','6enter,3badgeexempt,3×10=30. BaiFengplanned300000loan+200000pawnshortfall,severalGuoffered.500000cashconfirmed29680/2984;3millionpledged,remaining2.5millionnotreceived. Tieowesdinnerthenfriendloan,amountunreported.',[(293,15),(293,16),(295,23),(295,82),(296,32),(296,36),(296,80),(297,99),(298,4)])
res('Auction arithmetic / acquisitions','Instant Success, Silver Relic, Golden Shield','500000available;InstantSuccess180000plus;Relic+Shield83000combined.270000plusspent,220000plusremainingcanfitfirstprice187000–under190000. No27→26repair. Relicheldunused, BitterStrengthunacquired. Otherbids38000/42000/250000notFYexpenses.',[(296,55),(296,66),(296,77),(296,80),(296,82),(296,83),(296,85),(296,90),(296,91)])
res('Time Gu / continuous consumption / return option','Instant Success and Cloud pair','RevolutionFourtimeGuconsumed;lightcanbesuppressednottruepausedSR132. Yin/YangCloudsordinaryThreebought,3dayfullpricereturnOPTIONnotactualsale. RepeatedLotusrefillsfundactivationwithoutclaimoneapertureholds>100%.',[(297,27),(297,39),(297,41),(297,43),(297,45),(297,50),(297,51),(297,55),(297,81)])
res('Body strength transition','One boar removed; horse,ox,half-turtle added','Before2boars+bear+croc;after1boar+bear+croc+horse+ox+half-turtle. Nofullturtle. Overhalfyearpersonallifespanexpended. Horsecharge30%fasterthanboar30093, not30%greatermaxdistance.',[(297,25),(297,65),(297,76),(297,81),(297,87),(299,77),(300,93)])
res('Bai Gu set / reserve / decision versus sale','Ice Crystal vital and Snowball decision','IceCrystalnowvital,Vitalitysupport,IceBladeThree/IcicleTwo/SnowballThree/IceExplosionThree;FrostSpitname notautomaticallyFrostBreathauctionGu. Reserve90−70=20%,notaptituderecalculation. Snowballdiscarddecisionnotactualsale;oldIronThorntransitionunreportedbutvitalconversionpossible28615.',[(297,105),(298,47),(298,54),(298,68),(299,1),(299,19),(299,24),(299,25),(299,38)])
res('Injuries / defeat / unreported loot','Tie Dao Ku survives','Baiwins;Tieleftblind,rightinjured;hishealingcannotrepairleft,notuniversalirreversibility. Refereeseparatesfighters. Bai’sselectedlootunreported. IcebladeconstructexplosionnotproofGuconsumed.',[(298,97),(298,104),(298,105),(298,108),(298,113)])
res('Defence / deductions / ongoing fight','Zhu Ba and Golden Shield','80%reflectionconditionalonactivecoordinateddefence. Canopyheavilyinjured30050,notexplicitdead. GoldenShieldfirstused,cannotcombinewithCanopy. ZhuBa3metrebodymodified;number8fourthtiernotRevolutionEight. Battleunfinishedat300,nowin/loot/deathregistered.',[(299,51),(299,59),(299,61),(299,69),(300,6),(300,18),(300,50),(300,56),(300,59),(300,107),(300,121)])
np=sum(len(c['paragraphs']) for c in batch);nc=sum(sum(map(len,c['paragraphs'])) for c in batch);tp=sum(len(c['paragraphs']) for c in cs);tc=sum(sum(map(len,c['paragraphs'])) for c in cs)
save('proposal-ledger.json',ledger);save('chronology-register.json',dict(scope='Sequential through300; current, retrospective, legendary, personal and external clocks distinguished',entries=events));save('resource-register.json',dict(scope='Sequential through300; actual receipts, promises, conditional returns, bodily effects and Gu ownership distinguished',entries=resources))
progress=load('history/before-batch015-reading-progress.json');progress.pop('in_progress_batch',None);progress.update(sequential_chapters_completed=list(range(1,301)),paragraphs_read=tp,paragraph_characters_read=tc,next_chapter=301,remaining_chapters=2034,batch_report='Batch-015-Chapters-286-300.md',scope='Full sequential Chinese-source reading through300; no fresh bilingual/live-site audit',whole_novel_chronology_verified=False)
progress['batches'].append(dict(id='015',chapters=[286,300],paragraphs=np,characters=nc,reading_segments='Seven complete untruncated two-chapter outputs and complete300; adaptive15'))
progress['chapters'] += [dict(chapter=c['corpus_chapter'],file=c['file'],title=c['title'],paragraphs=len(c['paragraphs']),first_paragraph=1,last_paragraph=len(c['paragraphs'])) for c in batch];save('reading-progress.json',progress)
save('batch-015-reading-log.json',dict(status='Complete',endpoint=300,next_unread=301,segments=[dict(chapters=[a,a+1],status='Full paragraph sequences read; untruncated',paragraphs=sum(len(by[n]['paragraphs']) for n in [a,a+1])) for a in range(286,300,2)]+[dict(chapters=[300],status='Full paragraph sequence read; untruncated',paragraphs=len(by[300]['paragraphs']))],note='Actual reading, not extraction-only coverage;296pp95–97 reader-facing omission markers preserve original numbering and EPUB. No invented timestamps.'))
text=['# Numbered Chinese source: Chapters286–300','Source wording and paragraph numbering retained. Reader-facing omissions296pp95–97 for sexualised descriptions of young girls; original EPUB and internal extraction unchanged. All original paragraphs read.']
for c in batch:text += [f"## Corpus chapter {c['corpus_chapter']}: {c['title']}",f"Volume: {c['volume']} | EPUB: {c['file']}"]+[f"{i}. {reader(c['corpus_chapter'],i,t)}" for i,t in enumerate(c['paragraphs'],1)]
(r/'Batch-015-Numbered-Chinese-Source.md').write_text('\n\n'.join(text))
for name,vs in [('Chronology',ne),('Resources',nr)]:
 out=[f'# Batch015 {name} jotter','All provisional; no substantive source edits.']
 for v in vs:
  out += [f"## {v['id']}: {v.get('event',v.get('entry'))}",v.get('constraint',v.get('calculation'))]
  for z in v['sources']:out += [f"Ch{z['chapter']} p{z['paragraph']}",'> '+reader(z['chapter'],z['paragraph'],z['text'])]
 (r/f'jotters/Batch-015-{name}.md').write_text('\n\n'.join(out))
out=['# Batch015 continuity and proposed corrections','All new proposals held. SR118 Bai-title component downgraded, not silently applied. SR099 remains withdrawn.']
for v in new:
 out += [f"## {v['id']}: {v['category']}"]+[f"**{k}:** {v[k]}" for k in ['recommended_action','rationale','confidence','dependencies','status']]
 if 'copy_items' in v:
  for z in v['copy_items']:out += [f"### Ch{z['chapter']} p{z['paragraph']}: {z['original']} → {z['replacement']}",z['confidence'],'> '+reader(z['chapter'],z['paragraph'],src(z['chapter'],z['paragraph'])['text'])]
 else:
  for z in v['locations']:out += [f"Ch{z['chapter']} p{z['paragraph']}",'> '+reader(z['chapter'],z['paragraph'],src(z['chapter'],z['paragraph'])['text'])]
(r/'jotters/Batch-015-Continuity.md').write_text('\n\n'.join(out))
(r/'jotters/Batch-015-Preserve.md').write_text('''# Batch015 preservation cautions
- Li Ran receives instalments, not200000 in full;30000 remains owed at latest explicit checkpoint. Bai500000 received versus3000000 promised leaves2500000 not yet received.
- Auction rounded amounts can agree; no automatic270000→260000 repair.83000 is two Gu combined, not each. Other auction buyers’ spending not FY’s.
- Steel Tendon continuous-use Gu differs from consumed Iron Bone. Repeated Lotus refill supports activation, not enlarged aperture capacity.
- Instant Success burns continuously after activation, output can be suppressed. Personal lifespan expenditure is not months passing outside. Yin/Yang Cloud return option not completed sale.
- One boar removed, horse+ox+half-turtle added. Half turtle not complete. Only one beast phantom at a time. Fifty-pace max remains; horse gives30%more speed notrange.
- Fifth-tier17wins need not mean13wins sinceLiRan; LiRan fight not explicitly fourth. Possible ellipsis before fourth-tier debut prevents proved two-fights-one-day contradiction.
- Three-breath alternate-move intervals plus travel not same as five-breath per-Gu cooldown. Changing control distinct from maintaining effects.
- LiHao dead;MountainBackToad dead;vitalPositionSwap dieswithowner;3otherGu looted. NoSwapacquisition. TieDaoKu survivesBai;hisownhealinginadequateforleft-eye injury, not universal permanence.
- Bai reserve90−70=20 doesnotfixheraptitudeat90afterearlierrise. Snowball relinquishment decision not completed sale. Ice Crystal now vital; prior Iron Thorn disposition unreported, changing vital Gu possible.
- Bai twins alive hint is coercive bait, followed by death account. Mixed source witness still unresolved. RepeatedBai少族长weakens simplistic title correction; Shang rules not universal.
- Ren Zu legend and characterprophecy/motivesnotnarratorcalendar/fact. Repeatpoem andmaximpreserved.
- ZhuBa fourth-tiernumber8notRevolutionEight.300endsmidfight,not31stwin/death/loot. Canopyheavilyinjurednotexplicitlydead;GoldenShieldcannotstackwithit.
''')
stand=load('history/before-batch015-working-standards-register.json');stand['coverage_through']=300
su={'WS-01':'294survivalhintbait,69fabricatedpleadingstory;SR104versionholdcontinues. Chief’sfaithinFYprinciplesandBai’spredictiveGuinference notnarratorfacts.','WS-02':'Sixfoldtotalnotadditionalmultiples;80kprecisionquery;auctionapproximatebandscohere. MatchnameLiHao,notLiRan.','WS-03':'FYThreeinitial;SilverRelicheldunused. BaiThreepeak,90reservebeforefightnotautomatic90aptitude. Onephantomatime;half-turtleunfinished.','WS-04':'JumpingGrasssold;SelfReliancebought;PositionSwapvitaldieswithLiHao. Canopydamage≠death. PermanentmarksnotproofGuconsumption.','WS-05':'TimeGuconsumesoverhalfyearpersonal life inminutesexternal. Legendarydaysseparate. Off-pagebouts/ellipsesnotfabricateddateproof.','WS-06':'LiRan170kpaid/30kowed onlaterroundedledger. Bai500kreceived/2.5millionunreceived. Auction180kplus+83kconsistent270kplusunder187–190kfirstprice.','WS-07':'50pacesunobstructedcharge,mud45,cooldownsperGu. Horse30%fasternotfarther. Largepillarsandlegendaryabyssnotautomaticallyreduced.','WS-08':'SteelTendoncompleted293afterone-monthplan,relativeanchoruncertain. Lifespanspentnotbirthcalendaradvance. Six-personparty=5Bai+Tie.','WS-09':'Individualcopycandidates;29447missing少localrepairnotglobalBaititlepolicy.30092DirectChargetechnicalnamecandidate.','WS-10':'300/2334actualread,2034remaining.133records,131held,2withdrawn. Substantiveapproved/appliedfalse. Remote285verified atpackaging; laterbackupreceiptseparate.','WS-11':'29231fullmaximrepeated. Poem291125/29249keptrecognisable;noem-dashrequirementinEnglishprose.','WS-12':'SR118Baitwinscomponentdowngradedafterownclanrepeated少族长293–295. Shang262officecorrectionremainsstrong. Do not universaliseclanrules.'}
for v in stand['entries']:v['batch015_update']=su[v['id']]
save('working-standards-register.json',stand)
out=['# Working editorial standards','## Evidence checkpoint: Chapters1–300','Working rules are not whole-novel factual certification or manuscript approval. Cultivation terminology: Revolution.']
for v in stand['entries']:out += [f"## {v['id']}: {v['topic']}"]+[f"**{k}:** {v[k]}" for k in ['status','rule','evidence','reopen','batch015_update']]
(r/'WORKING-STANDARDS.md').write_text('\n\n'.join(out))
def quote(c,p):return f"**Ch{c} p{p}:**\n\n> {reader(c,p,src(c,p)['text'])}"
report=f'''# Sequential close-reading review: Chapters 286–300
## Batch 015 | The Omniarch

**Actual sequential coverage: 1–300 of 2,334. Next unread: 301.**

Fifteen complete chapters, **{np:,} paragraphs / {nc:,} paragraph characters** in this batch. Cumulative: **{tp:,} paragraphs / {tc:,} characters**. Eight full, untruncated reading segments. Chinese-source close reading, not a fresh bilingual or live-site audit.

**Five new records, SR129–133.** SR133 contains **{len(fixes)} individually held copy candidates**. The Bai-twin component of SR118 has been downgraded after contrary contextual evidence. SR047 and SR099 remain withdrawn. **133 total records: 131 held, two withdrawn.** No substantive proposal approved or applied. Cultivation wording remains **Revolution**.

## 1. Findings and confidence

| Record | Finding | Proposed treatment | Confidence |
|---|---|---|---|
| SR129 | First instalment over80000 versus later exact80000 arithmetic | Conditional removal of 多, or explicitly rounded ledger | Moderate repair |
| SR130 | Six times total versus six times more | 是常人的六倍, with approximate/lower-bound qualification | High distinction |
| SR131 | Li Ran named inside Li Hao’s fight | 李然 → 李好 at291pp65–66 | Very high |
| SR132 | Time Gu stopped versus its light suppressed | Clarify output suppression, not cancellation | Moderate wording issue |
| SR133 | Located copy faults and technical names | {len(fixes)} individual candidates, not global replacement | Individually qualified |

## 2. Six times as much is not six times more

{quote(289,39)}

{quote(289,40)}

{quote(289,41)}

The intended comparison compresses an approximately six-month workload into one month. That requires six times the usual daily training, not six additional multiples. Preferred **比常人多出六倍 → 是常人的六倍**. Because the ordinary duration says at least half a year, **至少是常人的六倍** is an alternative if that lower bound is intended literally.

Suggested English: **“He would have to use Steel Tendon Gu for roughly six times as long each day as an ordinary Gu Master.”** This expresses the workload relation without claiming an exact universal cultivation law. The effect is complete by293p92; the intervening chronology is compatible with a month but does not supply a precise dated schedule.

## 3. Li Hao, not Li Ran

{quote(291,65)}

{quote(291,66)}

These two lines describe the active opponent operating Position Swap Gu. That is **Li Hao**. Li Ran is the undercover ally. Preferred local replacement: **李然 → 李好** in both paragraphs. No replacement elsewhere is authorised.

Li Hao and Mountain Back Toad die at the fight’s end.293pp86–88 then supply the disposition: three other Gu are looted, Position Swap dies because it is his vital Gu, and the arena reward exceeds6000 stones. Do not add Position Swap or the dead toad to Fang Yuan’s inventory.

## 4. Instalments: the total is clear, the first payment’s precision is not

{quote(287,42)}

{quote(288,57)}

{quote(289,16)}

{quote(293,55)}

The secret agreement is **200000** for the recipe and staged cooperation. The first payment is twice described as **over80000**, but the subsequent ledger uses precisely80000:120000 owed, then50000 paid gives130000 total and70000 owed, then40000 gives170000 total and30000 owed.

If the later figures are exact, the smallest candidate is to remove **多** from287p42 and288p55. If they are rounded running totals, preserve the original wording and label the approximation. We should not manufacture a refund or increase the agreed compensation. **The200000 has not been fully paid by this batch’s latest explicit settlement.**

The Bai clan transaction is separate: **3000000 demanded and agreed,500000 first instalment received,2500000 not yet received.** A demand, a pledge and a receipt are different ledger entries. The plan is300000 borrowed plus200000 raised through pledged Gu; the text does not itemise every completed pawn transaction.

## 5. The auction arithmetic can reconcile

{quote(296,82)}

{quote(296,83)}

{quote(296,91)}

Do not automatically change270000-plus to260000-plus. If Instant Success costs between187000 and190000, then adding83000 produces between270000 and273000. From500000, that leaves between227000 and230000. These intervals fit the source’s approximate eighteen-, twenty-seven- and twenty-two-ten-thousand descriptions, with endpoint strictness governed by 多/余.

The actual local copy candidate is **二十二余 → 二十二万余**, restoring the missing unit.83000 is the combined cost of Silver Relic and Golden Shield, not the price of each. The other auction bids,38000,42000 and250000, belong to other buyers. Silver Relic is acquired but deliberately left unused; Bitter Strength is still not obtained.

## 6. A time Gu can keep burning while its light is restrained

{quote(297,50)}

{quote(297,55)}

The first line’s 催停 can suggest stopping the Gu. The explanation immediately denies that interpretation: once activated it keeps consuming itself, and restraining its light merely stretches the remaining duration. Preferred precision candidate: **收敛一蹴而就蛊的光辉**, or English **“suppressed Instant Success Gu’s light.”** Do not give it a true pause/reset mechanism.

The sequence is:
- Remove one stored boar’s strength: normally at least nineteen days, here a little over ten breaths under accelerated effect.
- Add horse strength: normally two or three months, compressed into half a cup of tea.
- Add ox strength in another half-cup-of-tea interval.
- Begin turtle strength, but stop halfway when the time Gu expires.

Fang Yuan loses **over half a year of personal lifespan**, not half a year on the external calendar. The light during boar removal is directed at the clouds/phantom; do not automatically charge him nineteen extra days without establishing his exposure. The rounded month intervals can accommodate the reported lifespan cost. The resulting body has **one boar, one bear, one crocodile, one horse, one ox and half a turtle**, not two boars or a completed turtle.

Repeated Lotus refills finance the expensive activation. This is not a claim that one aperture contains more than100% essence simultaneously. The Yin/Yang Cloud Gu can be returned at full price within three days under the badge privilege; the text offers that option without yet showing the actual return.

## 7. Earlier proposals must remain revisable

### SR118: downgrade the Bai-twin title correction

{quote(293,70)}

{quote(294,35)}

The Bai twins are repeatedly called 少族长, including by their own clansmen. That does not prove the title faultless, but it weakens the earlier high-confidence reading of263p75 as an isolated error. **Retain the Bai wording pending clan-specific succession evidence.** The strong Shang correction remains: Ya Zi’s competitive junior-lord office is not the designated heirship. Shang rules must not be imposed universally.

294p47 has a narrower defect, **两位族长**, in a scene about the two children. Inserting **少** follows the scene’s repeated wording without deciding the wider 少主 versus 少族长 issue.

### SR104: more death-branch evidence, still no edition verdict

{quote(294,55)}

{quote(294,69)}

The survival suggestion is bait. Fang Yuan then says the children are dead, and the narrator explicitly labels the alleged pleading/source-of-information story a fabrication with no living witness to contradict it.295p44 repeats the death account. This sharpens the inconsistency with231’s disappearance branch; it does not authenticate the compiler’s editorial intervention or settle which edition to adopt.

### SR101: casualty attribution is not an objective count

294p8’s malformed **近世人** likely means **近十人**. But the earlier pursuit starts with nine, loses five before the trap, and leaves four at the explosion. Tie Dao Ku’s emotional accusation may attribute all eight pursuit deaths to Fang Yuan. Correcting the characters does not certify that nearly ten people died in the blast. Keep the objective casualty sequence separate from blame in dialogue.

SR123’s Flying Bone Shield disposition remains unreported. SR060’s Ice Muscle inventory question is not resolved merely by the persistence of bodily effects. **SR099 remains withdrawn**;296p90 continues to treat Bai’s cultivation assistance as useful.

## 8. Chronology: actual anchors and avoided false alarms

-286: one-and-a-half 时辰 negotiating, conventionally about three hours; deliveries two days later; Li Ran fight another day later.
-288: eight-day jump, then three more days to the next narrated fight. The Li Ran oath had been removed a few days earlier; the emergency Wu contact happened three days earlier.
-289: seventeen wins, zero losses. Li Hao’s challenge is five days away, confirmed by290’s opening.
-292: healing is in its fifth 时辰, roughly the tenth hour in progress, not a precisely completed ten-hour course.
-293: twenty-nine wins; earnings described over more than a month; Steel Tendon complete.
-295–296: a thirty-breath ultimatum deliberately overruns; the500000 payment is due within a day; the auction is three days later.
-297: three days after the auction, the accelerated session; one day later the thirtieth win promotes Fang Yuan.

**Do not claim thirteen wins in eleven days as a proven error.** That depends on treating the Li Ran fight as the fourth bout, which the source does not explicitly establish. The long investigation period can contain off-page bouts.

Similarly, the ellipsis after the thirtieth victory can contain a day transition before Bai’s fight and Fang Yuan’s fourth-tier debut. The current evidence does not prove two Fang Yuan fights on one day. Retain the one-bout-per-day rule without inventing a contradiction or a precise hidden date.

## 9. Mechanics and inventory that should be preserved

**Movement:** Direct Charge’s maximum is fifty unobstructed paces, fewer through obstacles or mud. Alternating two movement Gu with three-breath intervals plus travel time is not a three-breath reuse cooldown for one Gu. Horse strength later gives30% more speed, not30% greater maximum distance.

**Essence:** All-Out Effort costs little; stored beast-force phantoms themselves consume no essence. Defence, movement and healing still cost essence. Bai’s90−70=20 reserve statement is not90×30%=27, and it does not prove her aptitude has reverted to exactly90% after the earlier increase.

**Body and Gu:** Brown Bear’s effect is completed; Steel Tendon requires repeated use; Iron Bone was consumable. Jumping Grass is explicitly sold. Self-Reliance, Revolution Three and45000 stones, heals only the user and improves as bodily force grows. Permanent Dao marks do not prove the original Gu is still held or was consumed.

**Bai:** Ice Crystal is now vital, supported by Vitality Gu. The earlier Iron Thorn transition is unreported, but286 explicitly establishes that vital Gu can be changed with assistance. Snowball is selected for removal, not yet shown sold. Frost Spit’s name should not automatically be changed to the auction’s Frost Breath. Her ice-blade explosion is not proof that the blade-producing Gu itself died.

**Tie Dao Ku:** he survives and concedes. His own healing cannot repair the left eye; that does not establish universal irreversible blindness. The referee’s intervention stops Bai’s attempted continuation. Her selected loot is not narrated here.

**Zhu Ba:** the fourth tier’s number-eight fighter is not a Revolution Eight cultivator. His80% reflection depends on coordinated active defence, not unconditional invulnerability. Canopy suffers heavy damage, not explicitly death. Golden Shield first appears in300, and the two defence Gu cannot operate together.

## 10. Copy evidence, refrain and endpoint

All **{len(fixes)} copy candidates** appear in the continuity jotter with exact locations, source excerpts, confidence and held status. Examples include the two broken sections of one pillar, 为了对付我→为了对付你 at288p110, repeated白凝冰 at298p91, and **直冲蛊→直撞蛊** at300p92.297p43天然元泉→天然真元 is supported by187pp62–68’s explicit Lotus explanation, not an invented change to the mechanism.

The poem repeated in291–292 should remain recognisable. The maxim reappears at292p31; the working narrative rendering remains **“Man is the most intelligent of all living things.”** No em-dash requirement has been introduced into proposed English prose.

**Chapter300 ends during Fang Yuan versus Zhu Ba.** Fang Yuan has broken through the defence and holds the advantage, but the result has not been narrated. Do not register a thirty-first victory, Zhu Ba’s death or any loot.

Saved: this report, full numbered Chinese companion, five evidence jotters, eight-segment reading log, cumulative workbook, **{len(events)} chronology entries / {len(resources)} resource entries /133 proposal records /12 working standards**. Reader-facing296pp95–97 omissions are explicitly marked; source numbering, original EPUB and internal extraction remain unchanged, and all original paragraphs were read.

At packaging, the verified remote backup covers285; any subsequent300 upload is recorded separately in a backup receipt. The22 older exports removed locally were individually remote-verified, with restoration URLs retained. No unique source evidence was deleted.

**Next unread:301.** Whole-novel chronology remains uncertified; all substantive emendations are unapproved and unapplied.
'''
(r/'Batch-015-Chapters-286-300.md').write_text(report)
old=(r/'update_batch010.py').read_text();wb=old[old.index('# Workbook: cumulative'):old.index("(r/'CURRENT-STATUS.md').write_text")]
wb=wb.replace('1–220 of2334','1–300 of2334').replace("('Next unread',221)","('Next unread',301)").replace('103total;102activeheld;1withdrawn','133total;131activeheld;2withdrawn').replace('range(10,0,-1)','range(15,0,-1)').replace("v['batch010_update']","v['batch015_update']").replace('Batch-010-Chapters-201-220','Batch-015-Chapters-286-300').replace('CHAPTERS201–220','CHAPTERS286–300').replace('Chapters201–220','Chapters286–300').replace('Twenty complete chapters; personal clocks and inventory scope distinguished','Fifteen complete chapters; temporal mechanics, exact versus approximate figures, revisable proposals').replace('Ch151,201p22,203p84 restricted excerpts','Ch151,201p22,203p84,250pp24–31/33/35–36,258pp70–74/79,296pp95–97 restricted excerpts')
exec(compile(wb,'workbook-and-docx','exec'))
(r/'CURRENT-STATUS.md').write_text(f'''# Sequential review checkpoint

Completed1–300/2334; next301;2034remaining. Batch015:{np}paragraphs/{nc}characters. Cumulative{tp}/{tc}.133proposals:131held+SR047/SR099withdrawn. Five newSR129–133;SR133contains{len(fixes)}copycandidates. {len(events)}chronology/{len(resources)}resources.12standards. All substantiveapproved/appliedfalse. Cultivation wording Revolution.

Deliverable Batch-015-Chapters-286-300.md/.docx. Fullsourcecompanion(reader29695–97omittedandmarked), fivejotters, readinglog, workbook/registers. Detailedhandoff jotters/batch-015-working.md. Alloriginalparagraphsread,EPUBunchanged.

Carry:SR129over80kfirstpaymentvs120kowed/later80+50+40=170,30owed;conditionaldelete多orroundedaccounting,noinventedrefund. SR130sixmonths→one daily6×totalnot6×extra. SR13129165/66李然→李好. SR13229750催停→suppresslight,consumablecannottrulystop55. SR133locatedcopyitemsincludes29447missing少,29743天然元泉→天然真元,30092直冲→直撞. SR118BaitwinscomponentDOWNGRADED:ownclanrepeated少族长293–295;Shang262strongstill. SR104294survivalbaitthen55death69死无对证 reinforcesforkunresolved231. SR101294near10blamevs3blastdeaths/8totalpursuitdifferentattribution. SR123FlyingBoneShielddispositionstillunknown,SR060IceMuscleeffectnotownershipproof;SR099stillwithdrawn.

FYThreeinitial,SilverRelicboughtunused. Bodyoneboar+bear+croc+horse+ox+halfturtleaftertimeGu. SteelTendoncomplete293,IronBoneconsumed,JumpingGrasssold,SelfReliance45000acquired. AllOutEffort3→4recipefromLiRan,5unknown,Cicadavitalunchanged. LiHao/Toaddead,PositionSwapvitaldieswithowner,3unnamedlooted+6000plusreward. LiRan170kpaid/30kowedperlaterledger. Bai3millionpromise500kreceived/2.5millionunreceived. Auction500kstart180kplus+83kcombined=270kpluspossibleiffirst187–190k;balance220kplus,missing万copyonly. BitterStrengthunowned. CloudGu3dayreturnoptionnotcompletedreturn. LiRanoathremoved28859,Baioathremoved29727afteronefailedbreakerattempt. TimeGuexhaustedafterhalf-turtle,overhalfyearFYlifespanpersonalclock,notoutsidecalendar.

Arena17wins289,LiHao18th,19–21then29in293,30win297promotes4thtier. LiRanfightnotexplicit4th;17countdoesnotproveimpossible13wins11days. 297ellipsisallowsdaygapbefore299first4thtierfight,noprovedsame-dayrulebreak. Fifty-pacemaxcharge,mud45,fivebreathreuseversus3breathalternationplustravel. Bai90−70=20reserve≠exactaptitude,newIceCrystalvitalchangepossible28615(oldIronThorntransitionunknown),Snowballdiscarddecisionnotsale. Tiesurvives,leftblind/rightinjured,refereestopsBai,selectedlootunreported. Endpoint300FYadvantageoverZhuBa,fightUNFINISHED,no31stwin/death/loot. Canopyheavilyinjurednotexplicitdead,GoldenShieldfirstusedcannotstack. Fourthtiernumber8notRevolutionEight.

Remote verifiedthrough285atpackaging:commit9a1c8a25509d54c50754498ea4b0e5e1520a1ce1. Subsequentuploadreceiptseparate. Cleanup22oldduplicateexports2,944,436bytesfreedafterindividualremoteSHAverification,restoreURLs backups/Workspace-Cleanup-After-Ch285.json. Originaluploads/captures/EPUB/sourceJSON/jotters/Markdownretained. No automaticbackgroundreading. Do not rerunearliergenerators;015idempotentfrompre015history.
''')
assert len(cs)==300 and len(ledger)==133 and len(new)==5
assert all(not v['approved'] and not v['applied'] for v in ledger)
assert all(z['text']==src(z['chapter'],z['paragraph'])['text'] for v in events+resources for z in v['sources'])
texts={t for c in cs for t in c['paragraphs']}
for line in report.splitlines():
 if line.startswith('> '):assert line[2:] in texts
sha=hashlib.sha256((r.parent.parent/'benchmark/sources/Gu-Zhen-Ren.epub').read_bytes()).hexdigest();assert sha=='1ef1c29b6bddd7994f56696e2d091363aa8bbcee4889439465a9e2c51437dd5d'
qa=dict(passed=True,chapters=300,batch_paragraphs=np,batch_characters=nc,paragraphs=tp,characters=tc,proposals=len(ledger),held=131,withdrawn=['SR-047','SR-099'],copy_items=len(fixes),chronology=len(events),resources=len(resources),reading_segments=8,next=301,reader_omissions=[[296,95],[296,96],[296,97]],source_sha256_unchanged=sha)
save('batch-015-qa.json',qa);print(json.dumps(qa,indent=2))
