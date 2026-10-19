import json
from pathlib import Path
r = Path('/home/user/editorial/sequential-review')
led = json.loads((r/'proposal-ledger.json').read_text())
W = {
'SR-276':'Witness repeats the duplicated 狐群 (copied); no independent support.',
'SR-277':'Witness repeats 她十分，冒然打听 (copied); no independent support.',
'SR-278':'Witness has 但在这里, not 但在之类, at 516p38. Independent support for the proposed correction (repost, so partial).',
'SR-279':'Witness repeats 微微光滑 (copied); no independent support.',
'SR-280':'Witness repeats 更深寂的沉默 (copied); no independent support.',
'SR-281':'Witness repeats 万人之上的权利 and 着权利 (copied); no independent support.',
'SR-282':'Witness matches the EPUB at 508p29, 515p69, 517p21 and 525p82. The contradiction is in the text, not a transcription error. Query stays open.',
'SR-283':'Witness repeats 只用一只百兽群 and the two 千兽群 mentions (copied); no independent support.',
'SR-284':'Witness has 战力将上涨五成左右 at 520p19, where the EPUB reads 五倍. Supports the 五成 reading, consistent with 519p63 (至少再壮大五成).',
'SR-285':'Witness repeats 一千四百人魂 and 千人魂的级数 (copied); no independent support.',
}
for v in led:
    if v['id'] in W:
        v['witness_collation'] = W[v['id']]
        v['dependencies'] = 'Hetushu witness (fact-check-026, 506–525) checked: ' + W[v['id']] + ' Whole-novel reconciliation outstanding.'
    if v['id'] == 'SR-278':
        v['confidence'] = 'Moderate-high (0.7).'
        v['status'] = 'Held repair candidate; unapproved.'
    if v['id'] == 'SR-284':
        v['category'] = 'Numeric: 五倍 vs 五成 (520p19)'
        v['locations'] = [{'chapter': 520, 'paragraph': 19, 'file': ''}]
        v['recommended_action'] = 'Propose 战力将上涨五成左右 at 520p19, matching 519p63 and the witness.'
        v['rationale'] = 'The same windfall is described as +50% (519p63). The witness reads 五成 at 520p19 where the EPUB reads 五倍.'
        v['confidence'] = 'Moderate (0.6).'
        v['status'] = 'Held repair candidate; unapproved.'
(r/'proposal-ledger.json').write_text(json.dumps(led, ensure_ascii=False, indent=1))
print('ledger', len(led), 'witness fields', sum(1 for v in led if 'witness_collation' in v))
