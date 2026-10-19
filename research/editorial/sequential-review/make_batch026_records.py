from pathlib import Path
import json
r = Path(__file__).parent
b = json.loads((r/'batch-026-source.json').read_text())
led = json.loads((r/'proposal-ledger.json').read_text())
p = json.loads((r/'reading-progress.json').read_text())

# guards: run once only, on the expected state
assert [c['corpus_chapter'] for c in b] == list(range(486, 506))
assert sum(len(c['paragraphs']) for c in b) == 1812
assert len(led) == 256 and led[-1]['id'] == 'SR-256'
assert p['next_chapter'] == 486 and p['paragraphs_read'] == 43412
assert not (r/'Batch-026-Numbered-Chinese-Source.md').exists()

PUB = 'HOLD: full2334-chapter reading and global reconciliation outstanding'
DEP = 'Whole-novel reconciliation; witness check for Batch 026 (not yet collated).'
P = 'Provisional proposal or query; no approval'
H = 'Held repair candidate; unapproved.'

def rec(i, cat, locs, action, rat, conf, status, dep=DEP):
    return {'id': f'SR-{i}', 'category': cat,
            'locations': [{'chapter': c, 'paragraph': q, 'file': ''} for c, q in locs],
            'recommended_action': action, 'rationale': rat, 'confidence': conf,
            'status': status, 'dependencies': dep,
            'approved': False, 'applied': False, 'publication_status': PUB}

new = [
rec(257, 'Stray empty quotation marks (486p3)', [(486, 3)],
 'Remove the stray “” after 出乎了方源的意料。', 'Empty quotation pair with no speech; copy-edit artefact.', 'High (0.8).', H),
rec(258, 'Typo 极为广场 for 极为宽广 (486p14)', [(486, 14)],
 'Propose 极为宽广，方圆至少有十里.', '广场 is a noun; the sentence describes a hall, so 宽广 is expected.', 'High (0.85).', H),
rec(259, 'Typo 神智重复清爽 for 恢复 (486p74)', [(486, 74)],
 'Propose 神智恢复清爽.', '重复 does not fit a state of mind; 恢复 fits the sentence.', 'Moderate-high (0.8).', H),
rec(260, 'Typo 就在这是 for 就在这时 (488p65)', [(488, 65)],
 'Propose 就在这时.', 'Slip for 时; the sentence introduces a sound.', 'High (0.85).', H),
rec(261, 'Conflict: 吞并葛家 vs 费家 (488p78)', [(488, 78)],
 'Query. 488p78 says the 马家 captured 暖沼谷 and absorbed 葛家; the rest of the episode concerns 费家 alone.',
 'The 葛家 is an ally of 常山阴 and is not attacked here; 费家 seems intended.', 'Moderate (0.6).', P,
 'External collation of 488; check the target name.'),
rec(262, 'Typo 着一个人 for 派一个人 (489p84)', [(489, 84)],
 'Propose 派一个人，去制止他.', '着 does not fit; 派 is the verb of sending a person.', 'Moderate-high (0.8).', H),
rec(263, 'Name variant 仙屋蛊 vs 仙蛊屋 (490p5 vs 487p89)', [(490, 5), (487, 89)],
 'Query. Check whether the building Gu is 仙蛊屋 or 仙屋蛊 across the batch.',
 'Two forms of one name within three chapters.', 'Moderate (0.6).', P,
 'Name register for the 八十八角真阳楼 Gu.'),
rec(264, 'Typo 模棱两口 for 模棱两可 (490p12)', [(490, 12)],
 'Propose 模棱两可.', 'Fixed phrase; 口 is a slip for 可.', 'High (0.8).', H),
rec(265, 'Chronology: 星宿仙尊 era (490p16 vs 467p57)', [(490, 16), (467, 57)],
 'Query. 490p16 places the founder in 远古 with 三百万年 before the present; 467p57 places the 星宿仙尊 in 太古.',
 'Era labels differ for the same figure.', 'Low (0.3).', P,
 'Chronology register for the 太古 and 远古 eras.'),
rec(266, 'Name variant 瑶光 vs 摇光 (490p76, 474p75 vs 466p74, 467p6)', [(490, 76), (474, 75), (466, 74), (467, 6)],
 'Query. Check whether the star-named fairy is 摇光仙子 or 瑶光仙子; use one form throughout.',
 'Early chapters use 摇光; the later chapters use 瑶光 for the same figure.', 'Moderate-high (0.7).', P,
 'Name register; check first appearance.'),
rec(267, 'Idiom 别出机枢 for 别出机杼 (492p90)', [(492, 90)],
 'Propose 别出机杼，另辟蹊径.', 'Idiom 别出机杼 is the standard form; 枢 is a slip.', 'High (0.8).', H),
rec(268, 'Idiom slip 扮演得敲到好处 for 恰到好处 (493p12)', [(493, 12)],
 'Propose 扮演得恰到好处.', '敲 does not fit the sense; 恰 is expected.', 'Moderate-high (0.7).', H),
rec(269, 'Typo 哪知蛊 for 哪一种蛊 (494p13)', [(494, 13)],
 'Propose 究竟该选择哪一种蛊.', '哪知 does not parse as a noun phrase; 哪一种 is expected.', 'High (0.85).', H),
rec(270, 'Chronology: years of concealment (496p38 vs 470p48)', [(496, 38), (470, 48)],
 'Query. 496p38 says 常山阴 has been missing for more than ten years; 470p48 gives twenty years of sleep.',
 'Two intervals for the same absence.', 'Moderate (0.6).', P,
 'Check the absence interval against 432p80, 440p6 and 470p48.'),
rec(271, 'Name error 珍宝楼 for 真阳楼 (496p51)', [(496, 51)],
 'Propose 八十八角真阳楼.', 'Every other instance of the building name in the corpus uses 真阳楼.', 'High (0.85).', H),
rec(272, 'Typo 一声皮肤 for 一身皮肤 (497p86)', [(497, 86)],
 'Propose 一身皮肤漆黑若墨.', '一声 does not fit; 一身 is expected.', 'High (0.85).', H),
rec(273, 'Grammar: 而是 after a contrast (502p17)', [(502, 17)],
 'Propose 却是立即对外面问道 or restructure the clause.',
 'The contrast clause is not completed; 而是 has no matching 不是.', 'Moderate (0.6).', H),
rec(274, 'Typo 跋涉道天川去 for 跋涉到天川去 (502p49)', [(502, 49)],
 'Propose 跋涉到天川去.', 'Slip for 到; the sense is travel to 天川.', 'Moderate-high (0.8).', H),
rec(275, 'Unclear 纠克 in 异种真元纠克 (504p36)', [(504, 36)],
 'Query. Check the intended term (possibly 冲克); no repair until the wording is confirmed.',
 'The compound is not a standard term in the batch.', 'Low (0.4).', P,
 'Terminology register for true-essence interaction.'),
]
led.extend(new)
assert len(led) == 275 and len({v['id'] for v in led}) == 275
(r/'proposal-ledger.json').write_text(json.dumps(led, ensure_ascii=False, indent=1))
print('ledger', len(led))

chars = sum(len(t) for c in b for t in c['paragraphs'])
p['sequential_chapters_completed'] = list(range(1, 506))
p['paragraphs_read'] = 43412 + 1812
p['paragraph_characters_read'] = 1517163 + chars
p['next_chapter'] = 506
p['remaining_chapters'] = 2334 - 505
p['batch_report'] = 'Batch-026-Chapters-486-505.md'
p['scope'] = 'Full sequential Chinese reading through 505; selected external collation, not fresh live bilingual audit'
p['batches'] = 26
p['chapters'] = 505
(r/'reading-progress.json').write_text(json.dumps(p, ensure_ascii=False, indent=2))
print('progress', p['paragraphs_read'], p['paragraph_characters_read'], p['next_chapter'], p['remaining_chapters'])

out = ['# Batch 026 Numbered Chinese Source (Chapters 486–505)', '',
       'Source: Gu-Zhen-Ren.epub, one line per paragraph. Numbering is chapter.paragraph.', '']
for c in b:
    out.append(f"## Chapter {c['corpus_chapter']} {c['title']}"); out.append('')
    for i, t in enumerate(c['paragraphs'], 1):
        out.append(f"{c['corpus_chapter']}.{i} {t}")
    out.append('')
(r/'Batch-026-Numbered-Chinese-Source.md').write_text('\n'.join(out), encoding='utf-8')
print('numbered written', chars)
