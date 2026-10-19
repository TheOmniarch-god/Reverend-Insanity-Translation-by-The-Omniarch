from pathlib import Path
import json
r = Path(__file__).parent
b = json.loads((r/'batch-025-source.json').read_text())
led = json.loads((r/'proposal-ledger.json').read_text())
p = json.loads((r/'reading-progress.json').read_text())

# guards: run once only, on the expected state
assert [c['corpus_chapter'] for c in b] == list(range(466, 486))
assert sum(len(c['paragraphs']) for c in b) == 1685
assert len(led) == 232 and led[-1]['id'] == 'SR-232'
assert p['next_chapter'] == 466 and p['paragraphs_read'] == 41727
assert not (r/'Batch-025-Numbered-Chinese-Source.md').exists()

PUB = 'HOLD: full2334-chapter reading and global reconciliation outstanding'
DEP = 'Whole-novel reconciliation; witness check for Batch 025 (not yet collated).'
P = 'Provisional proposal or query; no approval'

def rec(i, cat, locs, action, rat, conf, status, dep=DEP):
    return {'id': f'SR-{i}', 'category': cat,
            'locations': [{'chapter': c, 'paragraph': q, 'file': ''} for c, q in locs],
            'recommended_action': action, 'rationale': rat, 'confidence': conf,
            'status': status, 'dependencies': dep,
            'approved': False, 'applied': False, 'publication_status': PUB}

H = 'Held repair candidate; unapproved.'
new = [
rec(233, 'Typo 他说中 for 其中 (469p9)', [(469, 9)],
 'Propose 其中血神子仙蛊残方中，也需要大量的舍利蛊.', '他说中 does not parse; 其中 fits the list of Gu.', 'Moderate-high (0.7).', H),
rec(234, 'Typo 呢电射 for 纷纷电射 (470p88)', [(470, 88)],
 'Propose 一众家老纷纷电射.', '呢 breaks the verb phrase; 纷纷 is expected.', 'Moderate-high (0.75).', H),
rec(235, 'Typo 存储顾 for 存储蛊 (470p89)', [(470, 89)],
 'Propose 拿捏着存储蛊.', '顾 is a slip for 蛊; the object is the storage Gu named in 470p84.', 'High (0.9).', H),
rec(236, 'Name slip 月亮湖 for 月牙湖 (472p12)', [(472, 12)],
 'Propose 月牙湖上.', 'The lake is 月牙湖 throughout the batch and earlier chapters.', 'High (0.8).', H),
rec(237, 'Typo 眼睁睁地着 for 眼睁睁地看着 (474p14)', [(474, 14)],
 'Propose 眼睁睁地看着千狼王张开血盆大口.', 'The verb 看 is missing before 着.', 'Moderate-high (0.8).', H),
rec(238, 'Typo 运超 for 远超 (475p17)', [(475, 17)],
 'Propose 气息强盛，远超四转巅峰晶膜.', '运 does not fit the comparison; 远超 is the expected comparative.', 'High (0.8).', H),
rec(239, 'Typo 敷衍率 for 繁衍率 (476p63)', [(476, 63)],
 'Propose 会减少繁衍率.', 'The passage is about breeding and survival of 气泡鱼; 敷衍 does not fit.', 'Moderate-high (0.75).', H),
rec(240, 'Typo 如次 for 如此 (477p65)', [(477, 65)],
 'Propose 葛家达到如此境地.', '次 is a slip for 此.', 'High (0.85).', H),
rec(241, 'Typo 一百都只 for 一百多只 (481p74)', [(481, 74)],
 'Propose 其中三转蛊，就有一百多只.', '都只 does not parse as a count.', 'Moderate-high (0.8).', H),
rec(242, 'Unclear 离开贤弟 (481p64)', [(481, 64)],
 'Query. 贤弟 (worthy younger brother) does not fit the sense; the intended referent may be the 灵犀 herd or the beast.',
 'The sentence describes leaving the herd after taking the wild Gu, not leaving a person.', 'Moderate (0.6).', P,
 'External collation of 481; check the wording of 481p57–64.'),
rec(243, 'Typo 蓝天蛞蝓蛊 for 蓝田蛞蝓蛊 (484p36)', [(484, 36)],
 'Propose 蓝田蛞蝓蛊.', '484p18–24 uses 蓝田蛞蝓蛊 for the same transport Gu.', 'High (0.85).', H),
rec(244, 'Unclear 一番把设计 (485p17)', [(485, 17)],
 'Propose 一番布设，来到水巢附近.', '把设计 does not parse; 布设 fits the sense of setting a route.', 'Moderate (0.6).', H),
rec(245, 'Name variant 杨破樱 vs 杨破缨 (472p42 vs 482p34)', [(472, 42), (482, 34)],
 'Query. Check the full name of the 奴道 master across the novel; the two spellings differ.',
 'The same master is named as 杨破樱 in 472p42 and 杨破缨 in 482p34.', 'Moderate (0.6).', P,
 'Name register for 奴道 masters; check the first appearance.'),
rec(246, 'Name consistency 学堂家老 (471p22) with SR-222', [(471, 22), (473, 18), (473, 22)],
 'Query. 471p22 gives 学堂家老 for a 严家 elder; 473p18 and 473p22 give 战堂家老 for a 严家 elder in the same battle. Confirm whether 学堂 is an error here as well as in 457.',
 'Three 学堂 uses across 457 and 471 against many 战堂 uses. The office name needs one form across both families.', 'Moderate-high (0.6).', P,
 'Cross-reference SR-222; check the office name across 450–480.'),
rec(247, 'Chronology: time-flow ratio of 狐仙福地 (466p2 vs 474p62)', [(466, 2), (474, 62)],
 'Query. 466p2 gives five times the outside rate; 474p62 gives six times. Check which ratio the novel uses.',
 'The same fox-fortune time rate is stated as 五倍 and as 六倍 in two chapters; 469p63 uses five.', 'Moderate-high (0.8).', P,
 'Whole-novel check of the 狐仙福地 time ratio.'),
rec(248, 'Arithmetic: 紫晶舍利蛊 uses (475p43 vs 475p48–51)', [(475, 43), (475, 48), (475, 50), (475, 51)],
 'Query. 475p43 says three 紫晶舍利蛊 reach peak; the passage uses four (two to reach 五转高阶, two more to reach 五转巅峰).',
 'The text gives three as sufficient, then describes four.', 'Query only (0.5).', P,
 'Check the rule for how many 紫晶舍利蛊 a five-level master needs to reach the next sub-realm.'),
rec(249, 'Contradiction: tampered 紫晶舍利蛊 used (475p44, 475p46, 475p50)', [(475, 44), (475, 46), (475, 48), (475, 50)],
 'Query. 475p44 says two jars have fuzz and were tampered; 475p48 says only the two clear ones are usable; 475p50 then uses the two fuzzed ones.',
 'The sequence contradicts itself on which two Gu were used.', 'Moderate-high (0.7).', P,
 'External check of 475; this is a narrative inconsistency to resolve in the text.'),
rec(250, 'Arithmetic: 龟背狼 count (476p27 vs 476p29)', [(476, 27), (476, 29)],
 'Query. 476p27 says the seller has two wolf-thousands of 龟背狼 for sale; 476p29 says Fang Yuan bought three wolf-thousands.',
 'The two numbers for the same transaction differ.', 'Moderate-high (0.8).', P,
 'External collation of 476; check the number in the Chinese source.'),
rec(251, 'Arithmetic: total wolves (476p7–8, 476p29–30, 477p17, 484p50)', [(476, 7), (476, 8), (476, 30), (477, 17), (484, 50)],
 'Query. Reconcile the wolf count. 476p7 says near 30,000; 476p8 says 27,000; purchases in 476p29–30 total about 79,000; 477p17 says 60,000; 484p50 says six thousand before losses.',
 'The purchase totals cannot be reconciled with the stated post-purchase count.', 'Query only (0.6).', P,
 'Recount the wolf totals across 474–485.'),
rec(252, 'Realm inconsistency after 敛息蛊 (477p25 vs 477p26)', [(477, 25), (477, 26)],
 'Query. 477p25 says the cultivation was suppressed to 四转中阶; 477p26 says the aura left is 五转初阶.',
 'Both statements describe the same suppression and give different realms.', 'Moderate (0.6).', P,
 'Check the 敛息蛊 effect against 477p19–27.'),
rec(253, 'Conflicting source of wolf-accelerating Gu (479p33 vs 484p43)', [(479, 33), (484, 43)],
 'Query. 479p33 says 宙道蛊虫 accelerated the white-eyed wolf; 484p43 says 三更蛊.',
 'Two different Gu are named for the same accelerated growth.', 'Moderate-high (0.7).', P,
 'Check the 白眼狼 growth passage across 479–484.'),
rec(254, 'Back-reference to an earlier 金银电蛟 contest (480p71)', [(480, 71)],
 'Query. 480p71 says 夜狼万兽王 was earlier stopped by this move; the earlier text shown in the batch does not show that exchange.',
 'Possible missing earlier passage or loose back-reference.', 'Low (0.4).', P,
 'Check 479–480 for the earlier 金银电蛟 contact.'),
rec(255, 'Term variant 夜狼万狼王 vs 夜狼万兽王 (472p21 vs 473p1)', [(472, 21), (473, 1)],
 'Query. Check whether 万狼王 and 万兽王 are used interchangeably in the source before correcting.',
 'The same class of wolf is called 万狼王 and 万兽王 in nearby passages.', 'Low (0.4).', P,
 'Term register for wolf-king grades.'),
rec(256, 'Repeated colour 血狼 in one list (476p15)', [(476, 15)],
 'Query. 血狼 appears under both 南疆 and 中土 in one list. Check whether a second species name was intended.',
 'Repeated name in a catalogue of wolf species.', 'Low (0.4).', P,
 'Species list check.'),
]
led.extend(new)
assert len(led) == 256 and len({v['id'] for v in led}) == 256
(r/'proposal-ledger.json').write_text(json.dumps(led, ensure_ascii=False, indent=1))
print('ledger', len(led))

chars = sum(len(t) for c in b for t in c['paragraphs'])
p['sequential_chapters_completed'] = list(range(1, 486))
p['paragraphs_read'] = 41727 + 1685
p['paragraph_characters_read'] = 1454484 + chars
p['next_chapter'] = 486
p['remaining_chapters'] = 2334 - 485
p['batch_report'] = 'Batch-025-Chapters-466-485.md'
p['scope'] = 'Full sequential Chinese reading through 485; selected external collation, not fresh live bilingual audit'
p['batches'] = 25
p['chapters'] = 485
(r/'reading-progress.json').write_text(json.dumps(p, ensure_ascii=False, indent=2))
print('progress', p['paragraphs_read'], p['paragraph_characters_read'], p['next_chapter'], p['remaining_chapters'])

out = ['# Batch 025 Numbered Chinese Source (Chapters 466–485)', '',
       'Source: Gu-Zhen-Ren.epub, one line per paragraph. Numbering is chapter.paragraph.', '']
for c in b:
    out.append(f"## Chapter {c['corpus_chapter']} {c['title']}"); out.append('')
    for i, t in enumerate(c['paragraphs'], 1):
        out.append(f"{c['corpus_chapter']}.{i} {t}")
    out.append('')
(r/'Batch-025-Numbered-Chinese-Source.md').write_text('\n'.join(out), encoding='utf-8')
print('numbered written', chars)
