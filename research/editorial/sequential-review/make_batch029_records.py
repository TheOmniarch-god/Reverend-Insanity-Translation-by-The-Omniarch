from pathlib import Path
import json
r = Path(__file__).parent
b = json.loads((r/'batch-029-source.json').read_text())
led = json.loads((r/'proposal-ledger.json').read_text())
p = json.loads((r/'reading-progress.json').read_text())

# guards: run once, on the expected Batch 028 end state
assert [c['corpus_chapter'] for c in b] == list(range(546, 566))
N = sum(len(c['paragraphs']) for c in b); CH = sum(len(t) for c in b for t in c['paragraphs'])
assert len(led) == 306 and led[-1]['id'] == 'SR-306'
assert p['next_chapter'] == 546 and p['paragraphs_read'] == 48681
assert not (r/'Batch-029-Numbered-Chinese-Source.md').exists()

def para(ch, n):
    return b[ch-546]['paragraphs'][n-1]

frag = [(546,6,'蓝天蛞蝓蛊'),(546,16,'生出在大蜥屋'),(546,46,'拒绝蛊仙进入'),(547,47,'好变天'),
 (547,52,'长出六个脑袋'),(547,56,'七张嘴'),(548,57,'价值相当的高'),(550,15,'既潘平'),(550,18,'天青万狼皇'),
 (550,65,'居然向鼓动'),(550,85,'攻倍蛊'),(552,22,'捷足先登的可能”'),(552,64,'狼人常山阴'),(553,15,'壮栽'),
 (554,22,'是可以惊骇天下了'),(556,10,'展漏无疑'),(556,20,'第十二光'),(558,8,'脸盆大笑'),(558,51,'相差仿佛'),
 (559,58,'也是认知场景'),(559,87,'这并代表'),(560,3,'上蛊力道'),(561,47,'发成本质'),(563,21,'小光谷'),
 (563,31,'光栅蛊接连一起'),(563,60,'明拜暗访'),(564,55,'火道仙蛊'),(565,6,'一彻底成形'),(565,17,'历代王庭胜主'),
 (565,47,'推进到五十三层'),(565,62,'常山阴的亲身儿子')]
for c,n,f in frag:
    assert f in para(c,n), (c,n,f)
assert '夜狼狼皇' in json.loads((r/'batch-028-source.json').read_text())[543-526]['paragraphs'][35]

PUB = 'HOLD: full2334-chapter reading and global reconciliation outstanding'
DEP = 'Whole-novel reconciliation; Hetushu witness for Batch 029 collated (fact-check-029/).'
P = 'Provisional query; no approval'
H = 'Held repair candidate; unapproved.'

def rec(i, cat, locs, action, rat, conf, status, wit, dep=DEP):
    return {'id': f'SR-{i}', 'category': cat,
            'locations': [{'chapter': c, 'paragraph': q, 'file': ''} for c, q in locs],
            'recommended_action': action, 'rationale': rat, 'confidence': conf,
            'status': status, 'dependencies': dep, 'witness_collation': wit,
            'approved': False, 'applied': False, 'publication_status': PUB}

new = [
rec(307,'Inconsistent name 蓝天 for 蓝田蛞蝓蛊 (546p6)',[(546,6),(546,5),(484,36)],
 'Change 跟在蓝天蛞蝓蛊的身后 to 跟在蓝田蛞蝓蛊的身后. Cross-note only for 484p36 (Batch 025, not re-proposed here).',
 'The same creature is 蓝田蛞蝓蛊 at 546p5 and four times in 484 (484p18, 21, 23, 24). 蓝天 appears at 546p6 and 484p36 only. 蓝天 is the outlier.',
 'Moderate-high (0.6).',H,
 'Hetushu line for 546p6 also reads 蓝天 (copied); no independent support. Witness and EPUB agree on the internal inconsistency.'),
rec(308,'Verb slip 生出在 for 身处 (546p16)',[(546,16)],
 'Change 方源生出在大蜥屋蛊中 to 方源身处大蜥屋蛊中.',
 'The sentence describes Fang Yuan being inside the lizard-house gu and hearing the wind outside. 生出 (born out of) does not fit; 身处 (be situated in) does.',
 'Moderate (0.6).',H,
 'Witness repeats 生出在大蜥屋蛊中 (copied); no independent support.'),
rec(309,'Cross-link: 王庭福地拒绝蛊仙进入 (546p46) vs entry rules',[(546,46),(528,53),(524,47)],
 'Query, no text change. Record 546p46 with SR-289 as a further datum on whether 王庭福地 admits 蛊仙. Decide at whole-novel reconciliation.',
 '546p46 states that 王庭福地 refuses 蛊仙 entry, which supports the 528p53 rule and conflicts with 524p47.',
 'Low (0.3).',P,
 'Witness repeats 王庭福地拒绝蛊仙进入 (copied); no independent support.'),
rec(310,'Wrong adverb 好变天 for 好半天 (547p47)',[(547,47)],
 'Change 好变天，她尽了最大可能 to 好半天，她尽了最大可能.',
 '好半天 (a long while) is the expected idiom. 变天 (weather turns) does not fit a surgical or cosmetic effort on a nose.',
 'High (0.75).',H,
 'Witness repeats 好变天 (copied); no independent support.'),
rec(311,'Head count vs mouth count for the seven-mouthed figure (547p52 vs 547p56, 547p68)',[(547,52),(547,56),(547,68)],
 'Query. 547p52 says the figure grows six heads; 547p56 and 547p68 give seven mouths. Check whether the head count or the mouth count should be changed, or whether the text intends one extra mouth.',
 'Six heads and seven mouths can co-exist, but the chapter does not say so. The mismatch is not resolved by the text read.',
 'Low (0.4).',P,
 'Witness repeats 长出六个脑袋 and 七张嘴 (copied); no independent support.'),
rec(312,'Grammar: 价值相当的高 (548p57)',[(548,57)],
 'Change 其中几只价值相当的高 to 其中几只价值相当高.',
 'The predicate 价值相当高 (fairly high in value) is the expected form. 的 after 高 makes the phrase ungrammatical in this position.',
 'Low (0.25).',H,
 'Witness repeats 价值相当的高 (copied); no independent support.'),
rec(313,'Typo 既 for 继 (550p15)',[(550,15)],
 'Change 既潘平、朱宰之后 to 继潘平、朱宰之后.',
 '继 (following) is the expected verb for the sequence of 潘平 and 朱宰 greeting the wolf king. 既 does not fit this position.',
 'Moderate (0.5).',H,
 'Witness repeats 既潘平、朱宰之后 (copied); no independent support.'),
rec(314,'Name slip 天青万狼皇 for 天青万狼王 (550p18)',[(550,18),(549,78),(549,82),(550,61),(555,61)],
 'Change 方源坐在一头天青万狼皇的背上 to 方源坐在一头天青万狼王的背上.',
 'The tier used elsewhere for this wolf is 万狼王 (549, 550p61, 555p61). 狼皇 is a separate, higher tier (Batch 026 uses it for the 夜狼皇). Only 550p18 uses 万狼皇.',
 'Moderate (0.5).',H,
 'Witness repeats 天青万狼皇 (copied); no independent support.'),
rec(315,'Word slip 向 for 想 (550p65)',[(550,65)],
 'Change 居然向鼓动我和他联手 to 居然想鼓动我和他联手.',
 '向 (toward) does not govern 鼓动 here. 想 (intend) gives the sense that 潘平 wants to persuade Fang Yuan to join him.',
 'High (0.75). Witness-supported.',H,
 'Hetushu reads 居然想鼓动我和他联手 where the EPUB reads 居然向鼓动. Witness supports the correction.'),
rec(316,'Cross-link: 攻倍蛊 at 550p85 vs SR-299 (功倍蛊 name)',[(550,85),(533,27),(534,24),(534,89),(539,95)],
 'Query, no text change. Record 550p85 as a further site for SR-299 and as counter-evidence. 550p85 uses 攻倍蛊 as a generic category ("偏门的攻倍蛊", "炼制成本可比攻倍蛊"). Decide at whole-novel reconciliation whether 攻倍 and 功倍 are two names or one.',
 'Earlier batches use 五转攻倍蛊 only in batch 028 (533p27, 534p24, 534p89, 539p95). Batch 029 uses the term generically, so it cannot be dismissed as a simple slip.',
 'Low (0.3).',P,
 'Witness repeats 攻倍蛊 (copied); no independent support. SR-299 confidence lowered to moderate (0.6) on this basis (see report section 4).'),
rec(317,'Punctuation: missing 。 and stray ” (552p22)',[(552,22)],
 'Query. 552p22 ends with a closing quote and no full stop. Check the opening quote and the end of the quotation before any change.',
 'The quoted passage has a closing mark but no visible opening mark in this paragraph, and no full stop before the closing mark.',
 'Low (0.3).',P,
 'Witness repeats the same ending (copied); no independent support.'),
rec(318,'Name slip 狼人 for 狼王 (552p64)',[(552,64)],
 'Change 狼人常山阴的确立下功劳 to 狼王常山阴的确立下功劳.',
 '狼王 is the title used for 常山阴 throughout (552p64 later, and 552p16 context). 狼人 does not fit a wolf king who is a stated 盟军 member.',
 'Moderate-high (0.75). Witness-supported.',H,
 'Hetushu reads 狼王常山阴的确立下功劳; the EPUB reads 狼人常山阴. Witness supports the correction.'),
rec(319,'Typo 壮栽 for 壮哉 (553p15)',[(553,15)],
 'Change 壮栽，圣宫！ to 壮哉，圣宫！.',
 '壮哉 (How magnificent) is the exclamation intended. 壮栽 is not a word that fits an exclamation.',
 'High (0.7).',H,
 'Witness repeats 壮栽，圣宫！ (copied); no independent support.'),
rec(320,'Grammar: 是可以惊骇天下了 (554p22)',[(554,22)],
 'Query. Check whether 是可以惊骇天下了 should read 可以惊骇天下了 or 足以惊骇天下了. No change proposed without a further check.',
 'The predicate has a stray 是 before 可以, which reads as a copy-edit slip, but the sense is clear.',
 'Low (0.25).',P,
 'Witness repeats 是可以惊骇天下了 (copied); no independent support.'),
rec(321,'Typo 展漏 for 展露 (556p10)',[(556,10)],
 'Change 他暴躁的脾气，残酷的秉性，彻底展漏无疑 to 彻底展露无疑.',
 '展露 (revealed) is the expected verb with 无疑. 展漏 is a character slip.',
 'High (0.7).',H,
 'Witness repeats 彻底展漏无疑 (copied); no independent support.'),
rec(322,'Numeral unit: 第十二光 for 第十二关 (556p20)',[(556,20)],
 'Change 乃是之前闯第十二光，四十六关时的真阳楼奖励 to 乃是之前闯第十二关，四十六关时的真阳楼奖励.',
 '关 is the unit used for trial gates throughout this section (for example 第五十四关, 第六十一关). 光 does not fit.',
 'High (0.75). Witness-supported.',H,
 'Hetushu reads 第十二关; the EPUB reads 第十二光. Witness supports the correction.'),
rec(323,'Typo 脸盆大笑 for 脸盆大小 (558p8)',[(558,8)],
 'Change 此蛊乃是一朵蓝白相间的盛放莲花，脸盆大笑 to 脸盆大小.',
 '脸盆大小 (the size of a basin) is the description intended. 大笑 does not describe a plant.',
 'High (0.85).',H,
 'Witness repeats 脸盆大笑 (copied); no independent support. Local slip; high confidence without witness support.'),
rec(324,'Idiom: 相差仿佛 (558p51)',[(558,51)],
 'Query. The sense is that the four lights are roughly equal. Consider 相差无几 or 不相上下. No change without a check of the surrounding light-level passage.',
 '相差仿佛 is not a standard idiom. The sense needs the wording for "about the same".',
 'Low (0.4).',P,
 'Witness repeats 相差仿佛 (copied); no independent support.'),
rec(325,'Garbled phrase: 也是认知场景 (559p58)',[(559,58)],
 'Query. 认知场景 does not parse here. The sense is that trimming dull material is ordinary, so consider 也是人之常情 or similar.',
 'The phrase after 删减无趣冗长的部分 does not make sense as written. The probable intended sense is "also ordinary".',
 'Low-moderate (0.4).',P,
 'Witness repeats 也是认知场景 (copied); no independent support.'),
rec(326,'Missing 不 in 但这并代表 (559p87)',[(559,87)],
 'Change 但这并代表，他就能安然进入当中 to 但这并不代表，他就能安然进入当中.',
 '并不代表 (does not mean) is required. 并代表 reverses the sense.',
 'Moderate-high (0.6). Witness-supported.',H,
 'Hetushu reads 但这并不代表; the EPUB reads 但这并代表. Witness supports the correction. The Hetushu line carries a watermark artifact in the same paragraph; the wording itself is unaffected.'),
rec(327,'Unclear phrase 上蛊力道 (560p3)',[(560,3)],
 'Query. 这只上蛊力道的五转蛊 does not parse. The probable intent is a 借力 gu (借力蛊); confirm before any change.',
 'The sentence is about the 借力蛊 named in the same paragraph, so the phrase is probably garbled.',
 'Low (0.3).',P,
 'Witness repeats 这只上蛊力道的五转蛊 (copied); no independent support.'),
rec(328,'Wrong verb 发成 for 发生 (561p47)',[(561,47)],
 'Change 使得生命发成本质上的进化 to 使得生命发生本质上的进化.',
 '发生 (occur) is the expected verb. 发成 is a character slip.',
 'High (0.7).',H,
 'Witness repeats 使得生命发成本质上的进化 (copied); no independent support.'),
rec(329,'Typo 小光谷 for 小光蛊 (563p21)',[(563,21),(563,18),(563,20)],
 'Change 这些小光谷纷纷飞入土丘的地洞当中 to 这些小光蛊纷纷飞入土丘的地洞当中.',
 '小光蛊 is the Gu named at 563p18 and 563p20 in the same passage. 小光谷 is a character slip.',
 'High (0.8).',H,
 'Witness repeats 小光谷 (copied); no independent support.'),
rec(330,'Verb slip 接连一起 (563p31)',[(563,31)],
 'Query. 光栅蛊接连一起 is awkward. Probable intent: 光栅蛊连成一起 or 光栅蛊接连成一片. Confirm before any change.',
 'The sentence is about the grille formed by several 光栅蛊 linking together; the verb does not carry that sense.',
 'Low (0.3).',P,
 'Witness repeats 光栅蛊接连一起 (copied); no independent support.'),
rec(331,'Idiom slip 明拜暗访 (563p60)',[(563,60)],
 'Query. Probable intent: 明访暗拜 or 明来暗访. Confirm the sense from the next sentence before any change.',
 '明拜暗访 is not a standard idiom. The sense needs the verb pair for open and covert visits.',
 'Low (0.3).',P,
 'Witness repeats 明拜暗访 (copied); no independent support. Hetushu line carries a watermark artifact in the same paragraph.'),
rec(332,'Naming: 火道仙蛊 vs 炎道仙蛊 (564p55)',[(564,55),(565,29),(565,30),(550,16)],
 'Change 寄托着火道仙蛊 to 寄托着炎道仙蛊 (564p55), so that the Gu name matches 550p16, 565p29 and 565p30.',
 'Three uses of 炎道仙蛊 for the same Gu against one use of 火道仙蛊. The naming is inconsistent within the chapters.',
 'Moderate (0.6).',H,
 'Witness repeats 火道仙蛊 (copied); no independent support.'),
rec(333,'Word slip 一彻底成形 (565p6)',[(565,6)],
 'Query. Probable intent: 一旦彻底成形 (once fully formed). Confirm before any change.',
 '一 followed by 彻底 is not a standard construction here. The sense is "once", which 一旦 gives.',
 'Low-moderate (0.45).',P,
 'Witness repeats 一彻底成形 (copied); no independent support.'),
rec(334,'Typo 王庭胜主 for 王庭之主 (565p17)',[(565,17),(546,13),(556,16)],
 'Change 历代王庭胜主通关的层数屈指可数 to 历代王庭之主通关的层数屈指可数.',
 '王庭之主 is the term used at 546p13 and 556p16. 王庭胜主 is not used elsewhere.',
 'Moderate (0.5).',H,
 'Witness repeats 历代王庭胜主 (copied); no independent support.'),
rec(335,'Unit slip: 推进到五十三层 for 五十三关 (565p47)',[(565,47),(555,85),(556,20)],
 'Change 将关卡推进到五十三层 to 将关卡推进到五十三关.',
 'The unit for barrier gates in this section is 关 (556p20, 557p, 560p). 层 is the unit for the storeys of the tower (555p85). 五十三层 mixes the two.',
 'Moderate (0.5).',H,
 'Witness repeats 推进到五十三层 (copied); no independent support.'),
rec(336,'Identity conflict: 常山阴的亲身儿子 (565p62) vs 常极右 as 义子 (530p8, 530p17)',[(565,62),(565,67),(530,8),(530,17)],
 'Query, not a text change. Check whether 565p62 should read 义子 (adopted son) to match 530, or whether the chapter intends the biological-son claim. Decide at whole-novel reconciliation.',
 '530 names 常山阴 as 义父 and says 常极右 was adopted under his name. 565p62 says 常极右 is 常山阴的亲身儿子, which conflicts with 530. 565p67 says 常飚 is the real father, which fits 530.',
 'Low-moderate (0.55).',P,
 'Hetushu reads 常山阴的亲生儿子 at 565p62 and 亲生父亲 at 565p67, where the EPUB reads 亲身. The witness agrees with the EPUB on the claim, so the conflict is in the source, not a transcription slip.'),
rec(337,'Doubled 狼 in 夜狼狼皇 (543p36, Batch 028 chapter)',[(543,36)],
 'Query. 方源坐于老迈的夜狼狼皇背上 probably reads 夜狼皇 (as used at 526-545). Confirm before any change; this is a Batch 028 chapter.',
 'The doubled 狼 is not a standard form. 夜狼皇 is the term used in Batch 026 and elsewhere.',
 'Low-moderate (0.4).',P,
 'Batch 028 Hetushu witness (fact-check-028) repeats 夜狼狼皇 (copied); no independent support.'),
]
led.extend(new)
assert len(led) == 337 and len({v['id'] for v in led}) == 337
(r/'proposal-ledger.json').write_text(json.dumps(led, ensure_ascii=False, indent=1))
print('ledger', len(led))

chars = CH
p['sequential_chapters_completed'] = list(range(1, 566))
p['paragraphs_read'] = 48681 + N
p['paragraph_characters_read'] = 1711344 + CH
p['next_chapter'] = 566
p['remaining_chapters'] = 2334 - 565
p['batch_report'] = 'Batch-029-Chapters-546-565.md'
p['batches'] = 29
p['chapters'] = 565
(r/'reading-progress.json').write_text(json.dumps(p, ensure_ascii=False, indent=2))
print('progress', p['paragraphs_read'], p['paragraph_characters_read'], p['next_chapter'], p['remaining_chapters'])

out = ['# Batch 029 Numbered Chinese Source (Chapters 546–565)', '',
       'Source: Gu-Zhen-Ren.epub, one line per paragraph. Numbering is chapter.paragraph.', '']
for c in b:
    out.append(f"## Chapter {c['corpus_chapter']} {c['title']}"); out.append('')
    for i, t in enumerate(c['paragraphs'], 1):
        out.append(f"{c['corpus_chapter']}.{i} {t}")
    out.append('')
(r/'Batch-029-Numbered-Chinese-Source.md').write_text('\n'.join(out), encoding='utf-8')
print('numbered written', N, CH)
