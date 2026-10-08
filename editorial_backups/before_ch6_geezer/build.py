# -*- coding: utf-8 -*-
"""Rebuilds the Chapter 6 draft (docx + html) from persisted data in this folder."""
import json, os
from urllib.parse import quote
HERE = os.path.dirname(os.path.abspath(__file__))

recs = {int(k): v for k, v in json.load(open(f'{HERE}/ch6_lines.json', encoding='utf-8')).items()}
nn = {}; exec(open(f'{HERE}/ch6_notes.py', encoding='utf-8').read(), nn)
NOTES = nn['NOTES']
N = len(recs)

def tidy(t):
    """House style: curly apostrophes, single-character ellipsis, no em dashes."""
    if not t: return t
    return t.replace("...", "\u2026").replace("'", "\u2019")

for k in recs:
    recs[k][1] = tidy(recs[k][1]); recs[k][2] = tidy(recs[k][2])
NOTES = {k: tidy(v) for k, v in NOTES.items()}

def Z(w): return (f"Han Dian, {w}", f"https://www.zdic.net/hans/{quote(w)}")
DANTE = [
 ("Marx, Preface to the First German Edition of Capital, 1867, Marxists Internet Archive",
  "https://www.marxists.org/archive/marx/works/1867-c1/p1.htm"),
 ("Dante, Purgatorio V, lines 13 to 15, with the note on Marx's paraphrase",
  "https://wist.info/dante-alighieri-poet/398/"),
 ("Two Quotations in Marx's Capital Identified",
  "https://www.researchgate.net/publication/283183379_Two_Quotations_in_Marx's_Capital_Identified"),
 ("Chinese attribution of the proverb to Dante, noting Marx's use of it",
  "https://www.kedo.net.cn/c/2018-12-07/960061.shtml"),
]
EXTRA = {
 'baike_zifu': ("Baidu Baike, \u7d2b\u5e9c", "https://baike.baidu.com/item/%E7%B4%AB%E5%BA%9C/10439843"),
 'neidan':     ("Neidan diagram commentary, \u534e\u6c60 at \u8110\u540e\u80be\u524d", "https://www.yzthome.com/thread-1856.htm"),
 'neidan2':    ("Internal alchemy glossary listing \u7d2b\u5e9c among upper-dantian aliases", "https://www.taijizhe.com/topic.php?vid=543"),
 'wiki_bronze':("Chinese Wikipedia, \u9752\u94dc\u65f6\u4ee3, bronze named for its green oxide", "https://zh.wikipedia.org/wiki/%E9%9D%92%E9%93%9C%E6%97%B6%E4%BB%A3"),
 'yue_bronze': ("Cantonese Wikipedia, \u9752\u9285, fresh bronze is not green", "https://zh-yue.wikipedia.org/wiki/%E9%9D%92%E9%8A%85"),
 'ifeng':      ("Ifeng, bronzes named for their green rust, quoting the Shuowen on \u78a7", "https://gs.ifeng.com/c/8qaDXweU6rg"),
 'wiki_laogui':("Chinese Wikipedia, \u8001\u9b3c", "https://zh.wikipedia.org/zh-hans/%E8%80%81%E9%AC%BC"),
}
E_ = EXTRA
SRC = {
 0:[Z('\u7a7a\u7a8d')],
 1:[Z('\u7d2b\u5e9c'), Z('\u534e\u6c60'), E_['baike_zifu'], E_['neidan'], E_['neidan2']],
 2:[Z('\u51dd\u7ed3')],
 5:[Z('\u9752\u94dc'), Z('\u78a7'), E_['wiki_bronze'], E_['yue_bronze'], E_['ifeng']],
 6:[Z('\u771f\u5143')], 8:[Z('\u7cbe\u6c14\u795e')],
 12:[Z('\u6de1\u7136')], 13:[Z('\u5bb6\u8001')], 20:[Z('\u8f69\u7136\u5927\u6ce2')], 25:[Z('\u6ea2\u4e8e\u8a00\u8868')],
 31:[Z('\u4e00\u4ee3\u4e0d\u5982\u4e00\u4ee3')], 35:[Z('\u5e78\u707e\u4e50\u7978')], 37:[Z('\u5931\u9b42\u843d\u9b44')], 38:[Z('\u51cc\u8fdf')],
 47:DANTE, 51:[Z('\u8e49\u8dc4')], 52:[Z('\u54c4\u5802\u5927\u7b11')], 58:[Z('\u96be\u5144\u96be\u5f1f')], 61:[Z('\u73a9\u5473')],
 62:[Z('\u660e\u660e')], 65:[Z('\u4e0a\u6f14')], 72:[Z('\u8109')],
 73:[Z('\u4f55\u5fb7\u4f55\u80fd'), Z('\u8bef\u4eba\u5b50\u5f1f'), E_['wiki_laogui'], Z('\u89e6\u7535')],
 74:[Z('\u683d\u57f9'), Z('\u766b\u72c2')],
}

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.opc.constants import RELATIONSHIP_TYPE as RT

doc = Document()
for s in doc.sections:
    s.left_margin = s.right_margin = Inches(1.0)
    s.top_margin = s.bottom_margin = Inches(0.9)
st = doc.styles['Normal']
st.font.name = 'Calibri'; st.font.size = Pt(11)
st.element.rPr.rFonts.set(qn('w:eastAsia'), 'SimSun')
st.paragraph_format.space_after = Pt(6); st.paragraph_format.line_spacing = 1.15

def hyperlink(p, url, text, size=9):
    rid = p.part.relate_to(url, RT.HYPERLINK, is_external=True)
    h = OxmlElement('w:hyperlink'); h.set(qn('r:id'), rid)
    r = OxmlElement('w:r'); rPr = OxmlElement('w:rPr')
    c = OxmlElement('w:color'); c.set(qn('w:val'),'0563C1'); rPr.append(c)
    u = OxmlElement('w:u'); u.set(qn('w:val'),'single'); rPr.append(u)
    sz = OxmlElement('w:sz'); sz.set(qn('w:val'), str(int(size*2))); rPr.append(sz)
    rPr.append(OxmlElement('w:i')); r.append(rPr)
    t = OxmlElement('w:t'); t.text = text; t.set(qn('xml:space'),'preserve'); r.append(t)
    h.append(r); p._p.append(h)

def field(label, text, size=11):
    p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(0); p.paragraph_format.space_after = Pt(4)
    r = p.add_run(label); r.bold = True; r.font.size = Pt(size)
    r2 = p.add_run(text); r2.font.size = Pt(size)

def cjk(text, size=12.5):
    p = doc.add_paragraph(); pf = p.paragraph_format
    pf.left_indent = Inches(0.25); pf.space_before = Pt(2); pf.space_after = Pt(7)
    r = p.add_run(text); r.font.size = Pt(size); r.font.name = 'SimSun'
    r._element.get_or_add_rPr().rFonts.set(qn('w:eastAsia'), 'SimSun')
    r.font.color.rgb = RGBColor(0x33,0x33,0x33)

def note(text):
    p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(4); p.paragraph_format.space_after = Pt(4)
    r = p.add_run(text); r.font.size = Pt(10); r.font.color.rgb = RGBColor(0x44,0x44,0x44)

def srcline(items):
    p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(2); p.paragraph_format.space_after = Pt(12)
    r = p.add_run("I checked: "); r.bold = True; r.italic = True; r.font.size = Pt(9)
    for k,(l,u) in enumerate(items):
        if k:
            rr = p.add_run("   |   "); rr.font.size = Pt(9)
        hyperlink(p, u, l)

def rule(after=12):
    p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(2); p.paragraph_format.space_after = Pt(after)
    pPr = p._p.get_or_add_pPr(); pbdr = OxmlElement('w:pBdr'); bt = OxmlElement('w:bottom')
    for k,v in (('w:val','single'),('w:sz','6'),('w:space','1'),('w:color','DDDDDD')): bt.set(qn(k), v)
    pbdr.append(bt); pPr.append(pbdr)

for i in range(N):
    zh, lit, dr = recs[i]
    h = doc.add_heading(f'L{i:02d}', level=2)
    h.paragraph_format.space_before = Pt(0 if i == 0 else 14); h.paragraph_format.space_after = Pt(0)
    cjk(zh); field('Literal:  ', lit, 10.5); field('Draft:  ', dr, 11)
    n = NOTES.get(i)
    if n: note(n)
    if i in SRC: srcline(SRC[i])
    else: rule()
doc.save('/home/user/Reverend_Insanity_Chapter_6_Draft.docx')

# ---------------- Markdown, line by line ----------------
md = []
w = md.append
for i in range(N):
    zh, lit, dr = recs[i]
    w(f"### L{i:02d}")
    w("")
    w(f"> {zh}")
    w("")
    w(f"**Literal:** {lit}")
    w("")
    w(f"**Draft:** {dr}")
    w("")
    n = NOTES.get(i)
    if n:
        w(n); w("")
    if i in SRC:
        w("*I checked: " + ", ".join(f"[{l}]({u})" for l, u in SRC[i]) + "*")
        w("")
    w("---")
    w("")
open('/home/user/Reverend_Insanity_Chapter_6_Draft.md', 'w', encoding='utf-8').write("\n".join(md))

# ---------------- Markdown, clean reading text ----------------
rd = []
w = rd.append
w("# Volume 1: Demonic Nature Never Changes")
w("")
w("## Chapter 6: The Road to the Future Will Be Interesting")
w("")
for i in range(N):
    w(recs[i][2])
    w("")
open('/home/user/Reverend_Insanity_Chapter_6_Reading_Draft.md', 'w', encoding='utf-8').write("\n".join(rd).rstrip() + "\n")

print("rebuilt: docx + line-by-line md + reading md")
