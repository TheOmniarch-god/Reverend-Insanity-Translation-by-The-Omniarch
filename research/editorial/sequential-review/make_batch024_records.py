from pathlib import Path
import json
r = Path(__file__).parent
b = json.loads((r/'batch-024-source.json').read_text())
led = json.loads((r/'proposal-ledger.json').read_text())
p = json.loads((r/'reading-progress.json').read_text())

# guards: run once only, on the expected state
assert [c['corpus_chapter'] for c in b] == list(range(446, 466))
assert sum(len(c['paragraphs']) for c in b) == 1738
assert len(led) == 208 and led[-1]['id'] == 'SR-208'
assert p['next_chapter'] == 446 and p['paragraphs_read'] == 39989
assert not (r/'Batch-024-Numbered-Chinese-Source.md').exists()

PUB = 'HOLD: full2334-chapter reading and global reconciliation outstanding'
DEP = 'Whole-novel reconciliation; witness check for Batch 024 (not yet collated).'
P = 'Provisional proposal or query; no approval'

def rec(i, cat, locs, action, rat, conf, status, dep=DEP):
    return {'id': f'SR-{i}', 'category': cat,
            'locations': [{'chapter': c, 'paragraph': q, 'file': ''} for c, q in locs],
            'recommended_action': action, 'rationale': rat, 'confidence': conf,
            'status': status, 'dependencies': dep,
            'approved': False, 'applied': False, 'publication_status': PUB}

new = [
rec(209, 'Typo 说得痛 for 说得通 (447p67)', [(447, 67)],
 'Propose 说得通.', '痛 does not fit the argument; 通 is the expected word.', 'High (0.9).', 'Held repair candidate; unapproved.'),
rec(210, 'Typo 向要查清楚 for 想要查清楚 (447p72)', [(447, 72)],
 'Propose 想要查清楚.', '向 does not fit before 要; 想 is the expected verb.', 'High (0.9).', 'Held repair candidate; unapproved.'),
rec(211, 'Typo 们 in 但为什么们没有仙蛊 (448p3)', [(448, 3)],
 'Propose 但为什么没有仙蛊.', 'The stray 们 breaks the sentence; no pronoun is needed.', 'High (0.9).', 'Held repair candidate; unapproved.'),
rec(212, 'Typo 又脸抬起来 for 又抬起脸来 (452p36)', [(452, 36)],
 'Propose 又抬起脸来.', 'Word order is inverted; the verb phrase reads 抬起脸来.', 'Moderate-high (0.8).', 'Held repair candidate; unapproved.'),
rec(213, 'Duplicated 是 in 大多是都是 (452p84)', [(452, 84)],
 'Propose 他们大多是二转精英.', 'Two copulas in a row; one is a slip.', 'High (0.85).', 'Held repair candidate; unapproved.'),
rec(214, 'Wording 不愿被奴隶 for 被奴役 (452p27)', [(452, 27)],
 'Propose 不愿被奴役, parallel to SR-186 and the 奴役 usage elsewhere.',
 '奴隶 (slave) is a noun; the sentence needs the verb 奴役 as in the surrounding Gu-master passage.',
 'Moderate (0.7).', 'Held repair candidate; unapproved. Check against SR-186 witness results.'),
rec(215, 'Typo 普通水浪 for 普通水狼 (453p44)', [(453, 44)],
 'Propose 普通水狼.', '水狼 is the lake species named at 459p87 and 461p11; 浪 is a slip.', 'High (0.85).', 'Held repair candidate; unapproved.'),
rec(216, 'Typo 和方源计划的一眼 for 一样 (454p82)', [(454, 82)],
 'Propose 和方源计划的一样.', '一眼 does not parse; 一样 fits the comparison.', 'High (0.85).', 'Held repair candidate; unapproved.'),
rec(217, 'Typo 耳女 for 儿女 (456p19)', [(456, 19)],
 'Propose 我们的儿女.', '耳 is a slip for 儿 in a family-address context.', 'High (0.9).', 'Held repair candidate; unapproved.'),
rec(218, 'Stray 着 in 剩下着两只 (459p34)', [(459, 34)],
 'Propose 剩下两只.', '着 is not needed after 剩下; the count is clear.', 'High (0.85).', 'Held repair candidate; unapproved.'),
rec(219, 'Typo 带会狐仙福地 for 带回狐仙福地 (462p56)', [(462, 56)],
 'Propose 带回狐仙福地.', '会 breaks the verb; 回 is the expected verb complement.', 'Moderate-high (0.8).', 'Held repair candidate; unapproved.'),
rec(220, 'Typo 小脑地 for 小脑袋 (465p95)', [(465, 95)],
 'Propose 小脑袋.', '地 is a slip for 袋 in 脑袋.', 'Moderate-high (0.8).', 'Held repair candidate; unapproved.'),
rec(221, 'Unclear 圆形攻门 (465p88)', [(465, 88)],
 'Query. Possible slip for 圆形星门 or 圆形功门. Do not repair until the witness or the sentence sense is checked.',
 'The star-gate is described as 星门 elsewhere in the same passage; 攻门 does not match.', 'Low to moderate (0.4).', P,
 'External collation of 465; check how 星门 is written across 463–465.'),
rec(222, 'Name consistency 学堂家老 vs 战堂家老 (457p66, 457p78 vs 457p12–13)', [(457, 66), (457, 78), (457, 12), (457, 13)],
 'Propose 战堂家老 for 457p66 and 457p78, matching 457p12–13.',
 'The office is written 战堂家老 at 457p12–13; the two 学堂 entries at 457p66 and 457p78 break that form.', 'High (0.8).',
 'Held repair candidate; unapproved. Check office name in 450–456 first.'),
rec(223, 'Name variant 铁棺蛊 vs 铁柜蛊 (448p8)', [(448, 8)],
 'Query. Check the name against 433, where the same Gu is written 铁柜蛊.', 'Two spellings for one Gu within a short span.', 'Moderate (0.5).', P,
 'Name register for Gu names; 433 collation.'),
rec(224, 'Name variant 鬼炎蛊 vs 鬼焱蛊 (457p43)', [(457, 43)],
 'Query. Check whether 鬼炎蛊 and 鬼焱蛊 are distinct Gu or one Gu written two ways.',
 'Both spellings appear in one paragraph.', 'Moderate (0.5).', P, 'Gu name register.'),
rec(225, 'Idiom 舌战春雷 (456p18)', [(456, 18)],
 'Query. The phrase does not match a known idiom; 舌战群儒 or a different verb may be intended.',
 'Idiom mismatch; no attested witness checked.', 'Low (0.4).', P, 'External collation of 456.'),
rec(226, 'Arithmetic: 千狼王 count (453p13 vs 454p14)', [(453, 13), (454, 14)],
 'Query. Check the running count of 千狼王. 453p13 gives four; 454p14 implies five before three more arrive, for eight.',
 'The count at 453p13 does not match the tally implied by 454p14.', 'Query only (0.5).', P,
 'Recount all 千狼王 acquisitions in 450–454.'),
rec(227, 'Arithmetic: ten-jun Gu count (454p74, 459p34, 459p55 vs 443p30)', [(454, 74), (459, 34), (459, 55), (443, 30)],
 'Query. Reconcile the ten-jun strength Gu count. 443p30 gives twenty jun after its applications; 454p74 says this is the third use; 459p55 gives thirty jun from three uses and 459p34 says two remain.',
 'The later chapters agree with three uses; 443p30 is the outlier and may be the source of SR-203.', 'Query only (0.6 that 443p30 needs revision).', P,
 'Cross-reference with SR-203; whole-novel strength-Gu rules.'),
rec(228, 'Unclear 三王两千头 (458p80)', [(458, 80)],
 'Query. The phrase does not parse as a count; 三王 may refer to three 王-class wolves or be a slip.',
 'A wolf count is normally written as kings plus heads; the phrase as written does not give a clear count.', 'Low (0.4).', P,
 'External collation of 458; wolf-count register.'),
rec(229, 'Chronology: 五百年前世 and 距今十几年后 (461p35–38, 461p71)', [(461, 35), (461, 37), (461, 71)],
 'Query. Check whether the 三尊说 and Ma Hongyun passages use the same time frame as 441p50, where Ma Hongyun is about thirteen.',
 'The passage mixes a past-life frame (五百年前世) with a 距今 anchor; the two need to be reconciled.', 'Query only (0.5).', P,
 'Whole-novel chronology; Fang Yuan\'s previous-life frame.'),
rec(230, 'Death of 凤九歌 at 琅琊福地 (463p14)', [(463, 14)],
 'Query. Confirm the claim against the whole-novel record of Feng Jiu Ge before any repair.',
 'The sentence states Feng Jiu Ge died at 琅琊福地; the claim is strong and needs a whole-novel check.', 'Query only (0.5).', P,
 'Whole-novel check of 凤九歌 death and later appearances.'),
rec(231, 'Possible conflation 地灵小狐仙 (462p55)', [(462, 55)],
 'Query. The phrase reads as if 地灵 and 小狐仙 are one entity; the intended referent may be 小狐仙 alone.',
 '小狐仙 is the fox immortal; 地灵 is the Gu spirit; the sentence contrasts them.', 'Low to moderate (0.5).', P,
 'Check naming of 小狐仙 across 459–465.'),
rec(232, 'Soul-strength description (450p65)', [(450, 65)],
 'Query. Cross-check the soul-strength description with 437–443 and 458p7.',
 'Soul-strength figures appear in several forms (百人魂, 千人魂) across the arc.', 'Low (0.3).', P,
 'Whole-novel soul-strength register.'),
]
led.extend(new)
assert len(led) == 232 and len({v["id"] for v in led}) == 232
(r/'proposal-ledger.json').write_text(json.dumps(led, ensure_ascii=False, indent=1))
print('ledger', len(led))

# progress
chars = sum(len(t) for c in b for t in c['paragraphs'])
p['sequential_chapters_completed'] = list(range(1, 466))
p['paragraphs_read'] = 39989 + 1738
p['paragraph_characters_read'] = 1391431 + chars
p['next_chapter'] = 466
p['remaining_chapters'] = 2334 - 465
p['batch_report'] = 'Batch-024-Chapters-446-465.md'
p['scope'] = 'Full sequential Chinese reading through 465; selected external collation, not fresh live bilingual audit'
p['batches'] = 24
p['chapters'] = 465
(r/'reading-progress.json').write_text(json.dumps(p, ensure_ascii=False, indent=2))
print('progress', p['paragraphs_read'], p['paragraph_characters_read'], p['next_chapter'], p['remaining_chapters'])

# numbered source, format: chapter.paragraph text
out = ['# Batch 024 Numbered Chinese Source (Chapters 446–465)', '',
       'Source: Gu-Zhen-Ren.epub, one line per paragraph. Numbering is chapter.paragraph.', '']
for c in b:
    out.append(f"## Chapter {c['corpus_chapter']} {c['title']}"); out.append('')
    for i, t in enumerate(c['paragraphs'], 1):
        out.append(f"{c['corpus_chapter']}.{i} {t}")
    out.append('')
(r/'Batch-024-Numbered-Chinese-Source.md').write_text('\n'.join(out), encoding='utf-8')
print('numbered written', chars)
