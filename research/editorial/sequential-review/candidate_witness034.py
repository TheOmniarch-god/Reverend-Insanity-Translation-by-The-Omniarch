import json, re
from pathlib import Path
r = Path(__file__).parent
WM = re.compile(r'https?://\S*|[wｗ][wｗ.\s]*[hｈ][eｅ][tｔ][uｕ][sｓ][hｈ][uｕ][^\u4e00-\u9fff]*|和\W{0,3}图\W{0,3}书|[\*\-_•|.]{0,2}m?\.?hetushu\S*|[a-zA-Zｗｈｅｔｕｓｃｏｍ.•\*\-_]{2,}\.?com\.?', re.I)
S = {c['corpus_chapter']: c for c in json.loads((r/'batch-034-source.json').read_text())}
def wit(ch): return WM.sub('', (r/f'fact-check-034/ch{ch}-normalized.txt').read_text(encoding='utf-8'))
# (id, chapter, paragraph, source-as-printed, proposed-to)
C = [
 ('647p57',647,57,'将计将计','将计就计'),
 ('648p31',648,31,'展漏','展露'),
 ('652p11',652,11,'却却','却'),
 ('652p42',652,42,'干涉的声音','干涩的声音'),
 ('653p57',653,57,'据早','据考'),
 ('654p25',654,25,'不世枭魔','不世枭雄'),
 ('657p30',657,30,'大同风同化','大同风幕同化'),
 ('657p38',657,38,'在前领悟','在旁领悟'),
 ('656p72',656,72,'沈翠儿','沈翠儿'),
 ('658p20',658,20,'并不没有','并没有'),
 ('658p24',658,24,'暴漏','暴露'),
 ('660p6',660,6,'但正茶几上','但茶几上'),
 ('660p12',660,12,'骊山仙子','黎山仙子'),
 ('660p50',660,50,'签订的盟约','签订了盟约'),
 ('661p9',661,9,'被与运道真传','被运道真传'),
 ('661p27',661,27,'八座完好无缺，剩余三座','八座完好无缺，剩余四座'),
 ('662p20',662,20,'来未他','来为他'),
 ('662p42',662,42,'有用城池','有城池'),
 ('663p32',663,32,'远超同济','远超同级'),
 ('664p5',664,5,'云道仙蛊','运道仙蛊'),
 ('664p31',664,31,'连云','连运'),
 ('650p59',650,59,'微微一步','一步'),
 ('651p66',651,66,'有很多细微','有很多办法'),
]
for cid,ch,pn,frm,to in C:
    e=S[ch]['paragraphs'][pn-1]; w=wit(ch)
    print(f"{cid} | src has: {frm in e} | witness has source form: {frm in w} | witness has proposed form: {(to in w) and to!=frm}")
