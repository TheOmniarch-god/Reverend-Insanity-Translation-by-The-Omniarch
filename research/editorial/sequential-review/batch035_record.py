import json
from pathlib import Path
r = Path(__file__).parent
p = r/'proposal-ledger.json'
led = json.loads(p.read_text())
ids = {v['id'] for v in led}
HELD = 'Held repair candidate; unapproved.'
QRY = 'Provisional query; no approval'
PUB = 'HOLD: complete-corpus reading and global reconciliation outstanding'
W35 = 'Not yet collated (batch 035 Hetushu pages not fetched). No witness evidence either way.'
NA = 'Not applicable (outside this batch).'
# (id, category, chapter, para, action, status, confidence, rationale, dependencies)
ITEMS = [
 ('SR-419','Typo (word choice)',667,19,'Repair 这鞋杀招 to 这种杀招 at 667p19. Held.',HELD,'Held (0.9).','这鞋杀招 is unique (520p42 and 521p35 use 这鞋 in other senses). 这种杀招 is the expected phrase.','Batch 035 reading. Corpus grep.'),
 ('SR-420','Typo (character)',668,30,'Repair 载种海量的抖抖树 to 栽种海量的抖抖树 at 668p30. Held.',HELD,'Held (0.85).','载种 is unique. The same paragraph uses 栽种抖抖树.','Batch 035 reading.'),
 ('SR-421','Typo (word choice)',669,52,'Repair 越家温和 to 越发温和 at 669p52. Held.',HELD,'Held (0.9).','越家温和 is unique. 越发温和 is the expected phrase.','Batch 035 reading.'),
 ('SR-422','Typo (word order)',670,58,'Repair 墨人王卖你了一个人情 to 墨人王卖了你一个人情 at 670p58. Held.',HELD,'Held (0.75).','卖你了 is unique. Verb-complement order (卖了你) is the expected form.','Batch 035 reading. Corpus grep.'),
 ('SR-423','Typo (proper name)',670,69,'Repair 星罗小新 to 星罗小仙 at 670p69. Held.',HELD,'Held (0.9).','星罗小新 is unique. 星罗小仙 appears 16 times, including 668p9–16.','Batch 035 reading. Corpus grep.'),
 ('SR-424','Typo (character)',670,70,'Repair 花去半空仙元石 to 花去半块仙元石 at 670p70. Held.',HELD,'Held (0.8).','Same error at 683p25 (SR-438). Handle the pair together at reconciliation. 半块仙元石 is used 10 times.','Batch 035 reading. SR-438.'),
 ('SR-425','Query (numeric consistency)',672,10,'Query. 672p10–12 says 60 blocks earned from 琅琊地灵 and 20 spent, but the stated remaining balance is 30.5. 60 minus 20 is 40. The itemised purchases in 667–671 sum to about 11. The gap may be an unstated opening balance. No text change.',QRY,'Provisional (0.5).','Source: 672p10 (60 earned), 672p11 (20 spent), 672p12 (30.5 remaining). The opening balance is not stated in batch 035.','Whole-novel reconciliation. Check the balance chain from 665 onward.'),
 ('SR-426','Typo (word choice)',673,16,'Repair 我喜欢你尽量的五转起来 to 我希望你尽量的五转起来 at 673p16. Held.',HELD,'Held (0.6).','The next sentence has 希望 (我希望你能够理解). 我喜欢你 occurs 3 times (146p63, 412p91, 673p16) and none fits this sentence.','Batch 035 reading.'),
 ('SR-427','Typo (proper name)',673,67,'Repair 星落小仙 to 星罗小仙 at 673p67. Held.',HELD,'Held (0.9).','星落小仙 is unique. 星罗小仙 is the established name (16 hits).','Batch 035 reading. Corpus grep.'),
 ('SR-428','Typo (repeated character)',675,52,'Repair 四百年多年 to 四百多年 at 675p52. Held.',HELD,'Held (0.85).','四百年多年 is unique. 675p55 uses 四百多年 for the same span.','Batch 035 reading.'),
 ('SR-429','Typo (omitted character)',675,70,'Repair 躲藏着沙土深处 to 躲藏在沙土深处 at 675p70. Held.',HELD,'Held (0.5).','Missing 在. Low priority.','Batch 035 reading.'),
 ('SR-430','Query (meaning unclear)',675,74,'Query. 令狐虚 刚想钻出杀敌 at 675p74 may be missing a word (钻出来杀敌?). No text change.',QRY,'Provisional (0.4).','The phrase is unclear. No parallel in the corpus.','Batch 035 reading.'),
 ('SR-431','Typo (character)',676,57,'Repair 泛善可陈 to 乏善可陈 at 676p57. Held.',HELD,'Held (0.9).','泛善 is unique. 乏善可陈 appears at 82p74 and 211p17.','Batch 035 reading. Corpus grep.'),
 ('SR-432','Query (numeric or title consistency)',677,17,'Query. 677p17 calls 黑楼兰 a 六转 蛊仙 (in the speech of 黑城). 679p31 gives 黑楼兰 as 五转巅峰. Decide whether 677p17 is loose speech or a numeric slip. No text change.',QRY,'Provisional (0.5).','Source: 677p17 and 679p31. Both are within the same arc.','Batch 035 reading. Check the 黑楼兰 level chain at reconciliation.'),
 ('SR-433','Typo (repeated word)',678,37,'Repair 借机可以掺和 to 借机掺和 at 678p37 (remove the second 可以). Held.',HELD,'Held (0.7).','借机可以掺和 is unique. The doubled 可以 reads as a slip.','Batch 035 reading.'),
 ('SR-434','Typo (punctuation or character)',680,14,'Repair 穷人子，弟寒酸书生 to 穷人子弟，寒酸书生 at 680p14. Held.',HELD,'Held (0.55).','穷人子弟 (poor family) is the likely phrase. The comma and 弟 look misplaced.','Batch 035 reading.'),
 ('SR-435','Query (title consistency)',680,22,'Query. The titles for 袁白 (谷主 at 680p23, 680p32; 掌门 at 680p38) and 范医 (掌门 at 680p22, 680p32; 谷主 at 680p39) alternate. May be deliberate. No text change.',QRY,'Provisional (0.4).','The alternation may reflect either character’s standing in the scene.','Batch 035 reading. Check the titles used in 645–660 for these two.'),
 ('SR-436','Numeric consistency (price pattern)',682,32,'Query. 682p32 gives 九成 残方 as 10 blocks and 八成 残方 as 20 blocks. Completeness and price rise in opposite directions. 665p35 gives 10 blocks for a 九成 six-turn 残方. No text change until the pricing basis is checked.',QRY,'Provisional (0.6).','The earlier pricing ("之前的定价") is not stated in batch 035. Check its basis at reconciliation.','Batch 035 reading. SR-424 context.'),
 ('SR-437','Typo (character)',682,36,'Repair 宝皇天 to 宝黄天 at 682p36. Held.',HELD,'Held (0.9).','宝皇天 is unique. 宝黄天 is the standard name in the batch.','Batch 035 reading. Corpus grep.'),
 ('SR-438','Typo (character)',683,25,'Repair 只留下半空仙元石 to 只留下半块仙元石 at 683p25. Held.',HELD,'Held (0.8).','Same error as SR-424 (670p70). 半块仙元石 is used 10 times. Handle the pair together.','Batch 035 reading. SR-424.'),
 ('SR-439','Query (term)',684,20,'Query. 音劫灌儿 at 684p20 is unique. It may be a nonstandard term or a slip. No text change.',QRY,'Provisional (0.4).','The phrase appears once in the corpus. 惊心音劫 is the named calamity in the sentence.','Batch 035 reading.'),
 ('SR-440','Typo (word choice)',685,14,'Repair 从眼角出留下两股鲜血 to 从眼角流出两股鲜血 at 685p14. Held.',HELD,'Held (0.6).','出 alone does not fit the verb. 流出 or 渗出 is expected.','Batch 035 reading.'),
 ('SR-441','Typo (word choice)',685,16,'Repair 最后两道音斗 to 最后两道音磬 at 685p16. Held.',HELD,'Held (0.9).','音斗 is unique. 音磬 is used throughout 684–685 for the same calamity.','Batch 035 reading. Corpus grep.'),
 ('SR-442','Typo (Gu name)',685,71,'Repair 乐山乐意仙蛊 to 乐山乐水仙蛊 at 685p71. Held.',HELD,'Held (0.85).','乐山乐意 is unique. 乐山乐水 appears 18 times, including 684p60 and 682p30.','Batch 035 reading. Corpus grep.'),
]
added = 0
for sid, cat, ch, pn, action, status, conf, rat, dep in ITEMS:
    if sid in ids: continue
    led.append({
      'id': sid, 'category': cat,
      'locations': [{'chapter': ch, 'paragraph': pn, 'file': ''}],
      'recommended_action': action,
      'rationale': rat + ' ' + conf,
      'confidence': conf,
      'status': status,
      'dependencies': dep,
      'witness_collation': W35,
      'approved': False, 'applied': False,
      'publication_status': PUB,
      'witness_030_032': NA, 'witness_023_025': NA, 'witness_033': NA, 'witness_034': NA,
      'witness_035': W35,
    })
    added += 1
# Context notes on existing entries (no withdrawal, no change of status)
CTX = {
 'SR-414': ' Batch 035 context (2026-10-14): 663p30 and 664p5 use 运道; 云道 is also a genuine class term (670p11, 670p21, 673p7, 382p37, 610p84, 618p60). Reassessed to 0.5. Still held; needs confirmation.',
 'SR-418': ' Batch 035 context: 666p47 says nine 青提 remain. 650p40 gives 19. The explicit costs in 655–666 total about eight, which leaves about eleven. 672p14 and 679p39 agree with the nine-to-six-to-two chain from 666 onward. Gap of two still unresolved.',
 'SR-394': ' Batch 035 context: 672p40 names 乐山乐水 and 浪迹天涯 as components of 近水楼台 and does not mention 招灾. Supports the existing reading but does not settle 650p49 or 645p14. Context only.',
}
for v in led:
    if v['id'] in CTX and 'Batch 035 context' not in v.get('rationale',''):
        v['rationale'] += CTX[v['id']]
p.write_text(json.dumps(led, ensure_ascii=False, indent=2))
print('added', added, 'total', len(led), 'last', led[-1]['id'])
