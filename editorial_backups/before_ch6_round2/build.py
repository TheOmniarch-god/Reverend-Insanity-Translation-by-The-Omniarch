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
SRC = {
 0:[Z('空窍')], 1:[Z('紫府'),Z('华池')], 2:[Z('凝结')], 6:[Z('真元')], 8:[Z('精气神')],
 12:[Z('淡然')], 13:[Z('家老')], 20:[Z('轩然大波')], 25:[Z('溢于言表')],
 31:[Z('一代不如一代')], 35:[Z('幸灾乐祸')], 37:[Z('失魂落魄')], 38:[Z('凌迟')],
 47:DANTE, 51:[Z('踉跄')], 52:[Z('哄堂大笑')], 58:[Z('难兄难弟')], 61:[Z('玩味')],
 73:[Z('何德何能'),Z('误人子弟'),Z('老鬼')], 74:[Z('栽培'),Z('癫狂')],
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
