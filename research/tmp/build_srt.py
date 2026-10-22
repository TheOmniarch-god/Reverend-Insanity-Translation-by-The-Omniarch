import json
a = json.load(open("tmp/aligned.json"))
def ts(x):
    h=int(x//3600); m=int((x%3600)//60); s=x%60
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".",",")
caps=[]; cur=[]
def flush():
    global cur
    if not cur: return
    text=" ".join(w["t"] for w in cur)
    start=cur[0]["s"]; end=cur[-1]["e"]
    caps.append([start,end,text]); cur=[]
for k,w in enumerate(a):
    if cur and w["p"]!=cur[-1]["p"]:
        flush()
    cur.append(w)
    txt=" ".join(x["t"] for x in cur)
    dur=cur[-1]["e"]-cur[0]["s"]
    ends_sentence = w["t"][-1] in ".?!\""
    if len(txt)>=90 or dur>=6.5 or (ends_sentence and len(txt)>=55):
        flush()
flush()
# split long captions into two lines, fix timings/overlaps
out=[]; idx=1
for s,e,t in caps:
    if len(t)>84:
        words=t.split(); half=len(words)//2
        t=" ".join(words[:half])+"\n"+" ".join(words[half:])
    else:
        pass
    out.append((s,e,t))
lines=[]
for i,(s,e,t) in enumerate(out):
    e=e+0.15
    if i+1<len(out) and e>out[i+1][0]: e=out[i+1][0]-0.05
    lines.append(f"{i+1}\n{ts(s)} --> {ts(max(e,s+0.8))}\n{t}\n")
open("Test v3.srt","w",encoding="utf-8").write("\n".join(lines))
print(len(out),"captions")
