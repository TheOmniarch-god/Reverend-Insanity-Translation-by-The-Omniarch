import json, copy, re
from pathlib import Path
from openpyxl import load_workbook
from docx import Document
from docx.shared import Pt
r = Path(__file__).parent
led = json.loads((r/'proposal-ledger.json').read_text())
by = {v['id']: v for v in led}
WIT = 'Hetushu copy has the same text as our source here. The witness does not confirm or reject this candidate.'
new = [
 ('SR-384','Typo (character)', 627, 32, 'Repair 凶宅 to 凶灾, giving 乃是十大凶灾之一. Held.', 'Held repair candidate; unapproved.', 'Held (0.9).',
  '凶宅 is unique in the corpus. 十大凶灾 is used at 623p67, 626p46, 627p50, 128p17, 129p53 and 162p19. 627p32 is the only 凶宅.'),
 ('SR-385','Query (duplicated 援)', 627, 5, 'Query. 支援援兵 probably reads 支援，援兵 or 支援的援兵. Confirm the intended phrasing before any change. No text change.', 'Provisional query; no approval', 'Provisional (0.4).',
  '支援援 is unique in the corpus. The likely repair is punctuation or a missing 的. Do not change without a context check.'),
 ('SR-386','Query (word choice)', 627, 52, 'Query. 悍勇无端 may be intended as 悍勇无匹. Decide at reconciliation. No text change.', 'Provisional query; no approval', 'Provisional (0.3).',
  '悍勇无端 is unique in the corpus. 无匹 is the usual collocation for 悍勇. No change without a witness reading.'),
 ('SR-387','Query (shorthand)', 629, 78, 'Query. 受到鸿运蛊的反噬 may be shorthand for 鸿运齐天蛊 (as at 629p80). Decide at reconciliation. No text change.', 'Provisional query; no approval', 'Provisional (0.25).',
  '鸿运蛊 is unique in the corpus. The full name 鸿运齐天蛊 is used at 629p80 and elsewhere. The speaker may be using shorthand.'),
 ('SR-388','Typo (character)', 631, 75, 'Repair 一只五只无相手 to 一只五指无相手. Held.', 'Held repair candidate; unapproved.', 'Held (0.8).',
  '一只五只 is unique in the corpus. 五指无相手 is used at 629p86 and 631p78. 五只无相 appears at 630p74 and 631p60 as a plural form.'),
 ('SR-389','Query (uncommon character)', 634, 59, 'Query. 一片瓦铄 may be intended as 瓦砾 or another word. Decide at reconciliation. No text change.', 'Provisional query; no approval', 'Provisional (0.35).',
  '瓦铄 is unique in the corpus. 瓦砾 has no hits in the corpus. The character 铄 is uncommon in this context.'),
 ('SR-390','Query (possible word variant)', 637, 61, 'Query. 十数道光斓斑点 may be intended as 光斑斑点 or 斑斓 wording. Decide at reconciliation. No text change.', 'Provisional query; no approval', 'Provisional (0.35).',
  '斓斑 is unique in the corpus. 光斑 is used at 62p14 and 145p29. The next sentence uses 光斑.'),
 ('SR-391','Punctuation (missing 。)', 642, 57, 'Repair the closing quote to …取名字。” by adding 。 before ”. Held.', 'Held repair candidate; unapproved.', 'Held (0.5).',
  '巨阳意志 speech at 642p57 closes with 字” and no full stop. Check house style for closing quotes before change.'),
 ('SR-392','Query (word choice)', 642, 66, 'Query. 组成的蛊虫大众普通 may be intended as 大众 or 普通 alone. Decide at reconciliation. No text change.', 'Provisional query; no approval', 'Provisional (0.25).',
  '大众普通 is unique in the corpus. The phrase is redundant but grammatical.'),
 ('SR-393','Typo (character)', 643, 69, 'Repair 伤口出还缠绕 to 伤口处还缠绕. Held.', 'Held repair candidate; unapproved.', 'Held (0.85).',
  '伤口出 also appears at 137p89 (earlier batch). 伤口处 is used 18 times in the corpus. Consider 137p89 in the same repair list.'),
 ('SR-394','Query (Gu identity; cross-check SR-348)', 645, 14, 'Query. 645p14 says 近水楼台中的七转招灾仙蛊. 641p59–62 lists the components of 近水楼台 without 招灾仙蛊, and gives 水乳交融 as the core. Confirm before any change. No text change.', 'Provisional query; no approval', 'Provisional (0.5).',
  '七转招灾 is unique in the corpus. 招灾仙蛊 is the lure at 645p1. Ties to the SR-348 招灾蛊 ownership query. Do not change without context.'),
]
for sid, cat, ch, pn, action, status, conf, rat in new:
    if sid in by: continue
    e = copy.deepcopy(led[-1])
    e.update({'id': sid, 'category': cat, 'locations': [{'chapter': ch, 'paragraph': pn}], 'recommended_action': action,
              'status': status, 'confidence': conf, 'rationale': rat,
              'dependencies': 'Hetushu witness for 626–645 collated (copy matches source). Whole-novel reconciliation.',
              'approved': False, 'applied': False, 'publication_status': 'Held; not for publication',
              'witness_033': WIT})
    for k in list(e.keys()):
        if k.startswith('batch') and k.endswith('_update'): e[k] = ''
    led.append(e)
# Context notes (no status or confidence change)
ctx = {
 'SR-336': '626–645: 629p3, 635p16 and 639p78 are consistent with the impersonation (603p66). 635p16 states the real 常山阴 is dead. Query kept.',
 'SR-332': '633p34, 633p46 and 633p49 use 炎道仙蛊. No 火道 instance in 626–645. Query kept.',
 'SR-348': '645p1 and 645p14 use 招灾仙蛊 as a lure and then as part of 近水楼台 (see SR-394). Query kept.',
 'SR-378': '639p72 数万年前 and 639p79 数万年之久 add to the timeline scale. Compare 622p4 and 602p42. Query kept.',
 'SR-377': '637p84 uses 原理 correctly in the sense of the Gu principle. Held repair stands.',
}
for sid, t in ctx.items():
    if sid in by: by[sid]['context_033'] = t
assert len(led) == 394 and led[-1]['id'] == 'SR-394', len(led)
(r/'proposal-ledger.json').write_text(json.dumps(led, ensure_ascii=False, indent=2))
print('ledger', len(led))
