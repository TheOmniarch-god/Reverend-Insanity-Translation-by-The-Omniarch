from pathlib import Path
import json
r = Path(__file__).parent
b = json.loads((r/'batch-028-source.json').read_text())
led = json.loads((r/'proposal-ledger.json').read_text())
p = json.loads((r/'reading-progress.json').read_text())

# guards: run once, on the expected Batch 027 end state
assert [c['corpus_chapter'] for c in b] == list(range(526, 546))
assert sum(len(c['paragraphs']) for c in b) == 1761
assert len(led) == 285 and led[-1]['id'] == 'SR-285'
assert p['next_chapter'] == 526 and p['paragraphs_read'] == 46920
assert not (r/'Batch-028-Numbered-Chinese-Source.md').exists()

def para(ch, n):
    return b[ch-526]['paragraphs'][n-1]

frag = [
 (526,82,'都在寻常方源'),(526,73,'悍猛至厮'),(527,8,'屠杀了五位四转蛊师'),(528,53,'除非是达到九转'),
 (530,74,'还未刷完'),(531,14,'就有在下先出马吧'),(531,18,'直接向冲去'),(532,28,'毒发身份'),
 (532,32,'白毫精兵'),(532,41,'八百多头'),(533,32,'一只五转蛊人如故'),(533,27,'五转攻倍蛊'),
 (533,24,'五转功倍蛊'),(534,16,'一臂倒在高扬'),(534,51,'脸酱成紫红色'),(534,24,'五转攻倍蛊'),
 (534,89,'五转攻倍蛊'),(539,95,'五转攻倍蛊'),(540,13,'不足二十万'),(540,19,'只有二十万'),
 (538,36,'和他耶律盟军'),(544,44,'和和马家'),(542,102,'同时奴道大师'),(545,57,'吱呀咧嘴'),
 (545,37,'只剩下三成的底气'),(535,58,'便于今日'),
]
for c,n,f in frag:
    assert f in para(c,n), (c,n,f)

PUB = 'HOLD: full2334-chapter reading and global reconciliation outstanding'
DEP = 'Whole-novel reconciliation; Hetushu witness for Batch 028 collated (fact-check-028/).'
P = 'Provisional query; no approval'
H = 'Held repair candidate; unapproved.'

def rec(i, cat, locs, action, rat, conf, status, wit, dep=DEP):
    return {'id': f'SR-{i}', 'category': cat,
            'locations': [{'chapter': c, 'paragraph': q, 'file': ''} for c, q in locs],
            'recommended_action': action, 'rationale': rat, 'confidence': conf,
            'status': status, 'dependencies': dep, 'witness_collation': wit,
            'approved': False, 'applied': False, 'publication_status': PUB}

new = [
rec(286,'Wrong verb 寻常 for 寻找 (526p82)',[(526,82)],
 'Change 寻常方源的身影 to 寻找方源的身影.',
 'The sentence describes the Liu side searching for 方源. 寻常 (ordinary) does not fit the verb position; 寻找 is the intended verb.',
 'High (0.85).',H,
 'Witness repeats 都在寻常方源的身影 (copied); no independent support.'),
rec(287,'Idiom slip 悍猛至厮 (526p73)',[(526,73)],
 'Change 悍猛至厮 to 悍猛至斯.',
 'The four-character idiom is 悍猛至斯 (to this extreme). 厮 is a different character with no fit here. Copy-edit slip.',
 'Moderate (0.5).',H,
 'Witness repeats 悍猛至厮 (copied); no independent support.'),
rec(288,'Count check: 欧阳碧桑 kills (527p8 vs 526)',[(527,8),(526,70)],
 'Query. 527p8 credits 欧阳碧桑 with five 四转 kills and twelve 三转 家老 in the day\'s battle. Chapter 526 itemises only some kills. Check whether 527 counts the wider day before any change.',
 'The text read does not contradict the 527p8 tally. 526 does not itemise every kill, so the figure cannot be checked from 526 alone.',
 'Low (0.2).',P,
 'Witness repeats 屠杀了五位四转蛊师 (copied); no independent support.'),
rec(289,'Entry rule for 王庭福地: 九转 (528p53) vs 524p47',[(528,53),(524,47)],
 'Query. Reconcile 528p53 (only 九转 may enter 王庭福地) with 524p47 (太白云生 enters and advances to 蛊仙 inside it). Hold until the entry rule is checked across the novel.',
 '524p47 describes entry before advancement, which conflicts with a 九转 entry requirement unless 528p53 is read as a rule about advancement or about lodging. Cross-check only; no text change proposed.',
 'Low (0.3).',P,
 'Witness repeats 除非是达到九转 at 528p53 (copied); no independent support.'),
rec(290,'Verb slip 刷完 (530p74)',[(530,74)],
 'Query for the verb. The sentence reads 他还未刷完, then 方源 steps on his head. Probable candidates are 喊完 or 说完; confirm from context before any change.',
 'The verb does not fit the sense of an unfinished utterance, but no single replacement is certain from the text.',
 'Moderate (0.5).',P,
 'Witness repeats 他还未刷完 (copied); no independent support.'),
rec(291,'Wrong pronoun/verb 就有在下 (531p14)',[(531,14)],
 'Change 就有在下先出马吧 to 就由在下先出马吧.',
 'The speaker is proposing to go first. 由 (let/leave to) fits the sense; 有 does not. Likely copy-edit slip.',
 'Moderate (0.5).',H,
 'Witness repeats 就有在下先出马吧 (copied); no independent support.'),
rec(292,'Missing object: 直接向冲去 (531p18)',[(531,18)],
 'Query. Supply the target in 直接向[target]冲去 after confirming the target from the immediately preceding action.',
 'The verb 冲去 needs a goal (the target of the charge). The clause as printed has none.',
 'Moderate (0.5).',P,
 'Witness repeats 直接向冲去 (copied); no independent support.'),
rec(293,'Typo 毒发身份 for 毒发身亡 (532p28)',[(532,28)],
 'Change 有的毒发身份 to 有的毒发身亡.',
 'The list describes deaths (冻成冰棍, 烧成焦炭, 碎尸断肢). 身份 is a copy-edit slip for 身亡.',
 'High (0.9).',H,
 'Witness has 毒发身亡 at 532p28, where the EPUB reads 毒发身份. Independent support for the correction (repost, so partial).'),
rec(294,'Faction of 白毫精兵 for 黑家 (532p32)',[(532,32),(533,76),(534,70)],
 'Query. 532p32 gives 黑家 corps as 黑旗精兵 and 白毫精兵. 白毫 belongs to 刘家 (533p76), and 534p70 names both 黑旗军 and 白毫军 as suppressors across both sides. Confirm the 黑家 corps before any change.',
 'A 黑家 corps is named with a 刘家 corps. The 黑家 counterpart is not identified in the text read, so no replacement is proposed.',
 'Moderate (0.6).',P,
 'Witness repeats 白毫精兵 (copied); no independent support.'),
rec(295,'Wolf count: 八百多头 (532p41) vs 上百 (528) and 三百 (537p52)',[(532,41),(528,55),(537,52)],
 'Query. Check the 异兽狼 count at 532p41 against 528 (狐仙 holds 上百 异兽狼) and 537p52 (三百头 异兽狼 handed to 黑楼兰). The 532 figure may include other stock; confirm before any change.',
 'Three figures for the same asset class are not reconciled in the text read.',
 'Moderate (0.5).',P,
 'Witness repeats 八百多头 (copied); no independent support.'),
rec(296,'Wording 一只五转蛊人如故 (533p32)',[(533,32),(533,59)],
 'Consider 一只五转人如故蛊, matching 533p59 (五转——人如故). Low priority.',
 'The name of the Gu is written inconsistently with 533p59. The sense is clear.',
 'Low (0.3).',H,
 'Witness repeats 一只五转蛊人如故 (copied); no independent support.'),
rec(297,'Verb 倒 for striking (534p16)',[(534,16)],
 'Query. The verb 倒在 for the arm striking the head may be 拍在 or 劈在. Confirm from the wider description before any change.',
 'The arm strikes the head, so 倒 (to fall) is an unexpected verb here. The verb is a candidate, not a certainty.',
 'Low-moderate (0.4).',P,
 'Witness repeats 一臂倒在高扬 (copied); no independent support.'),
rec(298,'Typo 酱 for 涨 (534p51)',[(534,51)],
 'Change 黑楼兰的脸酱成紫红色 to 黑楼兰的脸涨成紫红色.',
 'The face turns purple-red from effort. 涨 (swell, flush) is the expected verb; 酱 is a copy-edit slip.',
 'Moderate-high (0.7).',H,
 'Witness repeats 脸酱成紫红色 (copied); no independent support.'),
rec(299,'Gu name 攻倍蛊 for 功倍蛊 (533p27, 534p24, 534p89, 539p95)',[(533,27),(534,24),(534,89),(539,95)],
 'Change 五转攻倍蛊 to 五转功倍蛊 at the four sites, after confirming against the canonical name.',
 'The same Gu is named 五转功倍蛊 at 533p24 and 533p68 in the same fight, and in 536p37 and 541p48. 功倍蛊 is the established name across the corpus. The 攻倍 spellings are the outliers, and they occur only in Batch 028.',
 'Moderate-high (0.75).',H,
 'Witness repeats 攻倍蛊 at 533p27, 534p24, 534p89 and 539p95 (copied); witness has 功倍 at 533p24. No independent support for the change.'),
rec(300,'Figure for 鼠群: 不足二十万 (540p13) vs 只有二十万 (540p19)',[(540,13),(540,19)],
 'Query. Check whether 540p13 (江暴牙, speech) should read 不足 or the figure should match 540p19 exactly. No change proposed until confirmed.',
 'The two statements give the same figure in different forms. The 540p20 arithmetic (74万 against 78万) is consistent either way.',
 'Low-moderate (0.35).',P,
 'Witness repeats both figures (copied); no independent support.'),
rec(301,'Stray 他 in 和他耶律盟军 (538p36)',[(538,36)],
 'Change 和他耶律盟军之战 to 和耶律盟军之战.',
 'The 他 has no clear antecedent: the sentence contrasts 马家 with 耶律盟军. Probable stray character.',
 'Low (0.3).',H,
 'Witness repeats 和他耶律盟军 (copied); no independent support.'),
rec(302,'Doubled 和和 (544p44)',[(544,44)],
 'Change 经过和和马家的第三场大战后 to 经过和马家的第三场大战后.',
 'Doubled character; copy-edit slip with no alternative reading.',
 'High (0.9).',H,
 'Witness repeats 和和马家 (copied); no independent support. Local slip, high confidence without witness support.'),
rec(303,'Wrong word 同时 for 同为 (542p102)',[(542,102)],
 'Change 马王居然被同时奴道大师的狼王 to 马王居然被同为奴道大师的狼王.',
 'The sense is that both men are 奴道大师, not that the events were simultaneous. 同为 fits; 同时 does not.',
 'High (0.8).',H,
 'Witness repeats 同时奴道大师 (copied); no independent support.'),
rec(304,'Onomatopoeia 吱呀咧嘴 (545p57)',[(545,57)],
 'Change 费才吱呀咧嘴地赶上来 to 费才龇牙咧嘴地赶上来.',
 '龇牙咧嘴 (grimacing from effort) is the expected idiom. 吱呀 is a creaking sound word that does not fit a person running.',
 'Moderate (0.55).',H,
 'Witness repeats 吱呀咧嘴 (copied); no independent support.'),
rec(305,'Figures for 底气 pillars (545p37)',[(545,37)],
 'Query. The text gives three pillars with one broken, then 只剩下三成的底气, and says the loss took away 一成. Check whether the figures should read 二成 or 三成 before any change.',
 'If one of three pillars is lost, the remaining share is not simply 三成 and the loss is not simply 一成. The figures do not reconcile as written.',
 'Low (0.3).',P,
 'Witness repeats 只剩下三成的底气 (copied); no independent support.'),
rec(306,'Wording 便于今日 (535p58)',[(535,58)],
 'Consider 方源就在今日召见 for 方源便于今日召见. Low priority; may be authorial phrasing.',
 '便于 (convenient for) does not carry the sense of choosing a day. Probable slip for 就在今日, but the phrasing may be deliberate.',
 'Low (0.25).',H,
 'Witness repeats 便于今日 (copied); no independent support.'),
]
led.extend(new)
assert len(led) == 306 and len({v['id'] for v in led}) == 306
(r/'proposal-ledger.json').write_text(json.dumps(led, ensure_ascii=False, indent=1))
print('ledger', len(led))

chars = sum(len(t) for c in b for t in c['paragraphs'])
p['sequential_chapters_completed'] = list(range(1, 546))
p['paragraphs_read'] = 46920 + 1761
p['paragraph_characters_read'] = 1645947 + chars
p['next_chapter'] = 546
p['remaining_chapters'] = 2334 - 545
p['batch_report'] = 'Batch-028-Chapters-526-545.md'
p['batches'] = 28
p['chapters'] = 545
(r/'reading-progress.json').write_text(json.dumps(p, ensure_ascii=False, indent=2))
print('progress', p['paragraphs_read'], p['paragraph_characters_read'], p['next_chapter'], p['remaining_chapters'])

out = ['# Batch 028 Numbered Chinese Source (Chapters 526–545)', '',
       'Source: Gu-Zhen-Ren.epub, one line per paragraph. Numbering is chapter.paragraph.', '']
for c in b:
    out.append(f"## Chapter {c['corpus_chapter']} {c['title']}"); out.append('')
    for i, t in enumerate(c['paragraphs'], 1):
        out.append(f"{c['corpus_chapter']}.{i} {t}")
    out.append('')
(r/'Batch-028-Numbered-Chinese-Source.md').write_text('\n'.join(out), encoding='utf-8')
print('numbered written', chars)
