import json, re
from pathlib import Path
r = Path(__file__).parent
WM = re.compile(r'https?://\S*|[wｗ][wｗ.\s]*[hｈ][eｅ][tｔ][uｕ][sｓ][hｈ][uｕ][^\u4e00-\u9fff]*|和\W{0,3}图\W{0,3}书|[\*\-_•|.]{0,2}m?\.?hetushu\S*|[a-zA-Zｗｈｅｔｕｓｃｏｍ.•\*\-_]{2,}\.?com\.?', re.I)
S = {c['corpus_chapter']: c for c in json.loads((r/'batch-033-source.json').read_text())}
def wit(ch):
    return WM.sub('', (r/f'fact-check-033/ch{ch}-normalized.txt').read_text(encoding='utf-8'))
checks = [
 ('627p32', 627, 32, '凶宅', '凶灾'),
 ('627p5', 627, 5, '支援援兵', '支援'),
 ('627p52', 627, 52, '悍勇无端', '悍勇无匹'),
 ('629p78', 629, 78, '鸿运蛊', '鸿运齐天蛊'),
 ('631p75', 631, 75, '一只五只无相手', '一只五指无相手'),
 ('634p59', 634, 59, '瓦铄', '瓦砾'),
 ('637p61', 637, 61, '光斓斑点', '光斑斑点'),
 ('642p57', 642, 57, '取名字”', '取名字。”'),
 ('642p66', 642, 66, '大众普通', '大众'),
 ('643p69', 643, 69, '伤口出', '伤口处'),
 ('645p14', 645, 14, '七转招灾仙蛊', '七转水乳交融'),
]
for cid, ch, pn, frm, to in checks:
    e = S[ch]['paragraphs'][pn-1]
    w = wit(ch)
    # locate the witness line that best contains the first 8 chars around the phrase
    ctx = e[max(0, e.find(frm)-6): e.find(frm)+len(frm)+6] if frm in e else e[:12]
    key = frm if frm in e else e[:10]
    wl = [l for l in w.split('\n') if l.strip()]
    best = max(wl, key=lambda l: len(set(l) & set(e)), default='')
    print(cid, '| source has frm:', frm in e, '| witness has frm:', frm in w, '| witness has to:', to in w, '| witness line:', best[:0] or '')
    # show the witness text near the phrase if the phrase is absent
    if frm not in w:
        idx = [i.start() for i in re.finditer(re.escape(to[:2]), w)][:1]
        print('     witness near to-form:', (w[max(0,idx[0]-10):idx[0]+len(to)+8] if idx else 'n/a'))
    else:
        i = w.find(frm); print('     witness context:', w[max(0,i-10):i+len(frm)+8])
