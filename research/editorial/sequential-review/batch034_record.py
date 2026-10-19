import json
from pathlib import Path
r = Path(__file__).parent
led = json.loads((r/'proposal-ledger.json').read_text())
ids = {v['id'] for v in led}
WIT = 'Hetushu 646–665 collated (fact-check-034/). Witness copies the source wording here; it neither confirms nor rejects this item.'
HELD = 'Held repair candidate; unapproved.'
QRY = 'Provisional query; no approval'
PUB = 'HOLD: complete-corpus reading and global reconciliation outstanding'
ITEMS = [
 ('SR-395','Typo (repeated character)',647,57,'Repair 将计将计 to 将计就计 at 647p57. Held.',HELD,'Held (0.9).',
  '将计将计 is unique in the corpus. 将计就计 is used seven times (77p13, 271p77, 294p3, 322p12, 400p8, 507p52, 645p5).'),
 ('SR-396','Typo (character)',648,31,'Repair 展漏无疑 to 展露无疑 at 648p31. Held.',HELD,'Held (0.85).',
  '展漏 also occurs at 556p10 (earlier batch). 展露 has 24 hits. Review 556p10 and 648p31 together.'),
 ('SR-397','Typo (repeated character)',652,11,'Repair 却却 to 却 at 652p11 (但太白云生却偏偏选择了). Held.',HELD,'Held (0.9).',
  '却却 is unique in the corpus. The sentence reads cleanly with one 却.'),
 ('SR-398','Typo (word choice)',652,42,'Repair 干涉的声音 to 干涩的声音 at 652p42. Held.',HELD,'Held (0.6).',
  '干涉的声音 is unique. 干涩 is used five times (3p3, 185p90, 499p20, 632p46, 650p13). The voice is described as hoarse at 650p13.'),
 ('SR-399','Query (repair target unclear)',653,57,'Query. 据早出现 at 653p57. The repair target is unclear (据考 has no corpus hits). Decide the wording at reconciliation. No text change.',QRY,'Provisional (0.5).',
  '据早 is unique. A repair is probable but the replacement wording is not settled.'),
 ('SR-400','Typo (character)',654,25,'Repair 乃不世枭魔 to 乃不世枭雄 at 654p25. Held.',HELD,'Held (0.5).',
  '不世枭魔 is unique. 不世枭雄 is used at 653p15 for the same idea.'),
 ('SR-401','Typo (omitted character)',657,30,'Repair 大同风同化一切 to 大同风幕同化一切 at 657p30. Held.',HELD,'Held (0.55).',
  '大同风同化 is unique. 大同风幕 has 58 hits. The sentence needs the full name.'),
 ('SR-402','Query (word choice)',657,38,'Query. 在前领悟的蛊仙东方一空 at 657p38. 在旁 may be intended (the speaker stands beside the group at 657p73). Decide at reconciliation. No text change.',QRY,'Provisional (0.35).',
  '在前领悟 is unique in the corpus.'),
 ('SR-403','Query (name)',656,72,'Query. 沈翠儿 at 656p72 appears once in the corpus. Check the name against any other reference to 方正 family or the 亲族 before any change. No text change.',QRY,'Provisional (0.3).',
  'The name appears only here. It may be a valid new character name.'),
 ('SR-404','Typo (character)',658,20,'Repair 并不没有 to 并没有 at 658p20. Held.',HELD,'Held (0.85).',
  '并不没有 is unique. 并没有 has 131 hits.'),
 ('SR-405','Typo (character)',658,24,'Repair 暴漏出 to 暴露出 at 658p24 (暴漏了一个毛病). Held.',HELD,'Held (0.85).',
  '暴漏 is unique. 暴露 has 148 hits.'),
 ('SR-406','Query (wording)',660,6,'Query. 但正茶几上 at 660p6 may be intended as 但茶几上 or kept as 正. No change without a context check.',QRY,'Provisional (0.2).',
  '正茶几 is unique. The phrase reads awkwardly but is not clearly wrong.'),
 ('SR-407','Typo (proper name)',660,12,'Repair 骊山仙子 to 黎山仙子 at 660p12. Held.',HELD,'Held (0.9).',
  '骊山仙子 is unique. 黎山仙子 has 19 hits and is used for the same character in the same chapter (660p11, 660p16).'),
 ('SR-408','Query (grammar)',660,50,'Query. 虽然东方一族和其他正道部族都签订的盟约 at 660p50 may need 已 or 了. Decide at reconciliation. No text change.',QRY,'Provisional (0.3).',
  '签订的盟约 is unique. 签订了盟约 occurs at 139p14.'),
 ('SR-409','Typo (extra character)',661,9,'Repair 被与运道真传带出大同风幕 to 被运道真传带出大同风幕 at 661p9 (delete 与). Held.',HELD,'Held (0.6).',
  '被与运道真传 is unique. The 与 appears to be a stray character.'),
 ('SR-410','Query (numeric consistency)',661,27,'Query. 661p27 says eight of the twelve 云阁 are intact and three are damaged (8+3=11). Check whether it should read four damaged, or nine intact. Decide at reconciliation. No text change.',QRY,'Provisional (0.6).',
  'Chapter 661p21 says twelve 云阁. 460p81 mentions three 云阁 under attack, which does not settle the count.'),
 ('SR-411','Typo (character)',662,20,'Repair 来未他解除封印 to 来为他解除封印 at 662p20. Held.',HELD,'Held (0.85).',
  '来未他 is unique. 来为他 occurs at 52p105.'),
 ('SR-412','Query (wording)',662,42,'Query. 已经有用城池数百座 at 662p42 may have a stray 有用. Consider 已经有城池数百座 or 拥有. Decide at reconciliation. No text change.',QRY,'Provisional (0.5).',
  '有用城池 is unique in the corpus.'),
 ('SR-413','Query (same pattern as SR-371)',663,32,'Query. 远超同济 at 663p32 has the same pattern as SR-371 (612p41, 同济 for 同级). Decide with SR-371 at reconciliation. No text change.',QRY,'Provisional (0.5).',
  '同济 occurs in five places (514p10, 514p21, 522p40, 612p41, 663p32). Some uses may be correct. 同级 has 11 hits.'),
 ('SR-414','Typo (Gu name)',664,5,'Repair 将云道仙蛊平步青云 to 运道仙蛊平步青云 at 664p5. Held.',HELD,'Held (0.8).',
  '云道仙蛊 is unique. The same Gu is 运道仙蛊平步青云 at 663p30.'),
 ('SR-415','Typo (Gu name)',664,31,'Repair 连云 to 连运 at 664p31 (净魂、平步青云、妇人心以及连运). Held.',HELD,'Held (0.8).',
  '连云 is unique. 连运仙蛊 has seven hits, including 663p61 and 664p39.'),
 ('SR-416','Query (idiom)',650,59,'Query. 无法晋升微微一步 at 650p59 may be intended as 一步 or 半步. Decide at reconciliation. No text change.',QRY,'Provisional (0.25).',
  '微微一步 also occurs at 151p95. The phrase may be an idiom in the author\'s style.'),
 ('SR-417','Query (wording)',651,66,'Query. 我有很多细微 at 651p66 may be intended as 办法 or 手段. Decide at reconciliation. No text change.',QRY,'Provisional (0.3).',
  '有很多细微 is unique in the corpus.'),
 ('SR-418','Query (count gap)',650,40,'Query. 650p40 gives 方源 19 青提仙元. 636p62 leaves 21. 655p74 gives 18 after one use at 655p18. No recorded consumption in 637–649 accounts for the gap of two. Confirm at reconciliation. No text change.',QRY,'Provisional (0.5).',
  'Counts: 650p40 (19), 652p25 (19), 653p26 (19), 655p74 (18), 665p26 (three used). Two unexplained units between 636 and 650.'),
]
for sid, cat, ch, pn, action, status, conf, rat in ITEMS:
    if sid in ids: continue
    led.append({'id': sid, 'category': cat, 'locations': [{'chapter': ch, 'paragraph': pn, 'file': ''}],
        'recommended_action': action, 'rationale': rat, 'confidence': conf, 'status': status,
        'dependencies': 'Hetushu 646–665 collated. Whole-novel reconciliation.',
        'witness_collation': WIT, 'approved': False, 'applied': False, 'publication_status': PUB,
        'witness_030_032': 'Not applicable (outside batches 030–032).',
        'witness_023_025': 'Not applicable (outside batches 023–025).',
        'witness_033': 'Not applicable (outside batch 033).',
        'witness_034': WIT})
# Context notes (no status or confidence change) recorded on existing entries
by = {v['id']: v for v in led}
ctx = {
 'SR-394': '650p49 lists 招灾仙蛊 among the three 近水楼台 Gu (浪迹天涯, 乐山乐水, 招灾仙蛊). 650p49 is not consistent with 641p60–62, which names 水乳交融 as the core and two auxiliaries. This supports holding SR-394 open.',
 'SR-348': '663p7 gives 招灾 as created by 墨瑶 (灵缘斋某代仙子), consistent with 644p52. 645p1 and 645p14 remain under SR-394.',
 'SR-247': '650p19 gives the 狐仙福地 ratio as five days to one (consistent with 409p20, 423p9, 466p2 and 494p28). 474p62 remains the single 六倍 reference.',
 'SR-371': '663p32 repeats the 同济 pattern (SR-413). Review SR-371 and SR-413 together.',
 'SR-336': '664p7 and 665p2 keep the 常山阴 impersonation thread consistent. No new conflict.',
}
for sid, t in ctx.items():
    if sid in by: by[sid]['context_034'] = t
led_sorted = led
(r/'proposal-ledger.json').write_text(json.dumps(led_sorted, ensure_ascii=False, indent=2))
print('ledger', len(led), led[-1]['id'])
