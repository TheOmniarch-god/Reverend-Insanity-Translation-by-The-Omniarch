import json, zipfile, re, sys, html
from html.parser import HTMLParser
start, end = int(sys.argv[1]), int(sys.argv[2])
cov = json.load(open("editorial/whole-novel-audit/coverage.json"))
bychap = {c["corpus_chapter"]: c for c in cov}
z = zipfile.ZipFile("benchmark/sources/Gu-Zhen-Ren.epub")
class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.paras=[]; s.cur=None; s.depth=0
    def handle_starttag(s, tag, attrs):
        if tag=="p": s.cur=[]
    def handle_endtag(s, tag):
        if tag=="p" and s.cur is not None:
            t="".join(s.cur).strip()
            if t: s.paras.append(t)
            s.cur=None
    def handle_data(s, d):
        if s.cur is not None: s.cur.append(d)
out=[]; mism=0
for n in range(start, end+1):
    c=bychap[n]
    raw=z.read(c["file"]).decode("utf-8")
    p=P(); p.feed(raw)
    paras=[html.unescape(x) for x in p.paras]
    if len(paras)!=c["paragraph_count"]: mism+=1
    out.append({"corpus_chapter":n,"file":c["file"],"volume":c["volume"],"title":c["title"],"paragraphs":paras})
json.dump(out, open(f"editorial/sequential-review/batch-040-source.json","w"), ensure_ascii=False, indent=1)
print("chapters",len(out),"mismatches",mism)
