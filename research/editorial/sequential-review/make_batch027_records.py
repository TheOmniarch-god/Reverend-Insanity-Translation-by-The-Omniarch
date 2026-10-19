from pathlib import Path
import json
r = Path(__file__).parent
b = json.loads((r/'batch-027-source.json').read_text())
led = json.loads((r/'proposal-ledger.json').read_text())
p = json.loads((r/'reading-progress.json').read_text())

# guards: run once, on the expected Batch 026 end state
assert [c['corpus_chapter'] for c in b] == list(range(506, 526))
assert sum(len(c['paragraphs']) for c in b) == 1696
assert len(led) == 275 and led[-1]['id'] == 'SR-275'
assert p['next_chapter'] == 506 and p['paragraphs_read'] == 45224
assert not (r/'Batch-027-Numbered-Chinese-Source.md').exists()

def para(ch, n):
    return b[ch-506]['paragraphs'][n-1]

# fragment checks: each cited fragment must appear in the cited paragraph
frag = [
 (510,22,'狐群、战蟹、狐群、蝙蝠'),(517,44,'她十分，冒然打听'),(516,38,'但在之类'),
 (516,66,'微微光滑'),(518,32,'更深寂的沉默'),(506,32,'万人之上的权利'),(525,30,'着权利'),
 (508,29,'五转巅峰修为'),(517,21,'他现在是五转修为'),(515,69,'只是四转巅峰'),(525,82,'四转蛊师，拿得出手的'),
 (509,9,'只用一只百兽群'),(509,34,'只带了一支千兽群'),(519,63,'至少再壮大五成'),
 (520,19,'战力将上涨五倍左右'),(511,13,'一千四百人魂'),(511,51,'千人魂的级数'),
]
for c,n,f in frag:
    assert f in para(c,n), (c,n,f)

PUB = 'HOLD: full2334-chapter reading and global reconciliation outstanding'
DEP = 'Whole-novel reconciliation; Hetushu witness for Batch 027 not yet collated.'
P = 'Provisional proposal or query; no approval'
H = 'Held repair candidate; unapproved.'

def rec(i, cat, locs, action, rat, conf, status, dep=DEP):
    return {'id': f'SR-{i}', 'category': cat,
            'locations': [{'chapter': c, 'paragraph': q, 'file': ''} for c, q in locs],
            'recommended_action': action, 'rationale': rat, 'confidence': conf,
            'status': status, 'dependencies': dep,
            'approved': False, 'applied': False, 'publication_status': PUB}

new = [
rec(276, 'Duplicated 狐群 (510p22)', [(510,22)],
 'Remove the second 狐群: 还有狐群、战蟹、蝙蝠等等.',
 'The same noun is listed twice in one series; a copy-edit slip.', 'Moderate (0.6).', H),
rec(277, 'Broken clause 她十分，冒然打听 (517p44)', [(517,44)],
 'Propose 她十分明白，不敢冒然打听这些秘密 or a similar completed verb.',
 'The comma after 十分 leaves the adverb without a predicate; a verb such as 明白 or 清楚 is missing.',
 'Moderate (0.6).', H),
rec(278, 'Garbled phrase 但在之类 (516p38)', [(516,38)],
 'Propose 但在此界, or 但在这里, to match 这个世界 in the preceding sentence.',
 '之类 does not fit the sense of a place; the surrounding text is about this world.', 'Low-moderate (0.5).', H),
rec(279, 'Wording 微微光滑 (516p66)', [(516,66)],
 'Propose 微微光华 or 微微发光; the reading needs confirmation.',
 'Gu light is described as luminous, not smooth; 光滑 is a surface term.', 'Low-moderate (0.4).', H),
rec(280, 'Wording 更深寂的沉默 (518p32)', [(518,32)],
 'Propose 更深的寂静 or 更加沉默; low priority.',
 '更深寂 is not a standard compound; the sense is clear but the phrasing is awkward.', 'Low (0.3).', H),
rec(281, 'Possible 权利 for 权力 (506p32 and 525p30)', [(506,32),(525,30)],
 'Propose 权力 at both points, where power over others is meant. Confirm first, because 权利 is used for rights elsewhere.',
 'Both uses describe power of authority, not entitlement. Repeated use suggests a possible author habit, so this is held as a query-repair.',
 'Low-moderate (0.5).', H),
rec(282, 'Realm of 常山阴: five-level or four-level (508p29, 517p21 vs 515p69, 525p82)', [(508,29),(517,21),(515,69),(525,82)],
 'Query. Establish whether 常山阴 is 五转巅峰 (508p29, 517p21) or 四转巅峰 (515p69, 525p82) before any change. The 515p69 and 525p82 statements may be in a rival character\'s perspective.',
 'Two sets of statements disagree on the same figure\'s level. 525p82 places him in a list of four-level figures.',
 'Moderate (0.6).', P,
 'Realm register for 常山阴; check 500–505 and 524 for realm statements.'),
rec(283, 'Army size 百兽群 vs 千兽群 (509p9 vs 509p34, 509p58)', [(509,9),(509,34)],
 'Query. Check whether 509p9 should read 千兽群, matching her own force at 509p34 and 509p58.',
 'Tang Miaoming plans for him to use a 百兽群 to match her 狐群, but her force is a 千兽群 in the same scene.',
 'Low-moderate (0.4).', P),
rec(284, 'Strength gain from the indemnity: 五成 vs 五倍 (519p63 vs 520p19)', [(519,63),(520,19)],
 'Query. Clarify whether the increase is in 军力 (+50%) or 战力 (五倍). No change until the measure is confirmed.',
 'Both statements describe the same windfall with different scale; they may measure different things.',
 'Low-moderate (0.4).', P),
rec(285, 'Soul level of the three-mind technique (511p13 vs 511p51)', [(511,13),(511,51)],
 'Query. 511p13 gives 一千四百人魂; 511p51 gives 千人魂的级数. Check whether the second is a lower bound.',
 'The two figures differ for the same technique in the same chapter.',
 'Low (0.3).', P),
]
led.extend(new)
assert len(led) == 285 and len({v['id'] for v in led}) == 285
(r/'proposal-ledger.json').write_text(json.dumps(led, ensure_ascii=False, indent=1))
print('ledger', len(led))

chars = sum(len(t) for c in b for t in c['paragraphs'])
p['sequential_chapters_completed'] = list(range(1, 526))
p['paragraphs_read'] = 45224 + 1696
p['paragraph_characters_read'] = 1582593 + chars
p['next_chapter'] = 526
p['remaining_chapters'] = 2334 - 525
p['batch_report'] = 'Batch-027-Chapters-506-525.md'
p['batches'] = 27
p['chapters'] = 525
(r/'reading-progress.json').write_text(json.dumps(p, ensure_ascii=False, indent=2))
print('progress', p['paragraphs_read'], p['paragraph_characters_read'], p['next_chapter'], p['remaining_chapters'])

out = ['# Batch 027 Numbered Chinese Source (Chapters 506–525)', '',
       'Source: Gu-Zhen-Ren.epub, one line per paragraph. Numbering is chapter.paragraph.', '']
for c in b:
    out.append(f"## Chapter {c['corpus_chapter']} {c['title']}"); out.append('')
    for i, t in enumerate(c['paragraphs'], 1):
        out.append(f"{c['corpus_chapter']}.{i} {t}")
    out.append('')
(r/'Batch-027-Numbered-Chinese-Source.md').write_text('\n'.join(out), encoding='utf-8')
print('numbered written', chars)
