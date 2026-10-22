import json, re, difflib
from difflib import SequenceMatcher
asr = json.load(open("tmp/words.json"))
hint_raw = open("tmp/hint.txt", encoding="utf-8").read()
# hint tokens: keep original text, split on whitespace, keep paragraph breaks
hint = []
for para_i, para in enumerate(hint_raw.strip().split("\n")):
    for tok in para.split():
        hint.append({"t": tok, "p": para_i})
def norm(s): return re.sub(r"[^a-z0-9]", "", s.lower())
H = [norm(h["t"]) for h in hint]
A = [norm(a["w"]) for a in asr]
n, m = len(H), len(A)
def sc(i, j):
    if H[i] == A[j]: return 2
    if H[i] and A[j] and SequenceMatcher(None, H[i], A[j]).ratio() >= 0.6: return 1
    return -1
GAP = -1
import array
D = [[0]*(m+1) for _ in range(n+1)]
B = [[0]*(m+1) for _ in range(n+1)]
for i in range(1, n+1): D[i][0] = i*GAP; B[i][0] = 1
for j in range(1, m+1): D[0][j] = j*GAP; B[0][j] = 2
for i in range(1, n+1):
    for j in range(1, m+1):
        diag = D[i-1][j-1] + sc(i-1, j-1)
        up = D[i-1][j] + GAP
        left = D[i][j-1] + GAP
        best = max(diag, up, left)
        D[i][j] = best
        B[i][j] = 0 if best == diag else (1 if best == up else 2)
i, j = n, m
pairs = {}
while i > 0 or j > 0:
    b = B[i][j]
    if i>0 and j>0 and b == 0:
        pairs[i-1] = j-1; i -= 1; j -= 1
    elif i>0 and (j==0 or b == 1):
        i -= 1
    else:
        j -= 1
# assign times
times = [None]*n
for hi, aj in pairs.items():
    if H[hi] and sc(hi, aj) >= 1:
        times[hi] = (asr[aj]["s"], asr[aj]["e"])
matched = sum(1 for t in times if t)
print("hint words", n, "matched", matched)
# interpolate unmatched
last_end = 0.0
for k in range(n):
    if times[k] is None:
        # find next matched
        nxt = next((q for q in range(k+1, n) if times[q]), None)
        start = last_end
        end = times[nxt][0] if nxt is not None else (asr[-1]["e"])
        cnt = sum(1 for q in range(k, (nxt if nxt is not None else n)) if times[q] is None)
        idx = k - (max([q for q in range(k) if times[q]] , default=-1)+1)
        seg = (end - start)/max(cnt,1)
        s = start + idx*seg
        times[k] = (s, s+seg)
    last_end = times[k][1]
json.dump([{"t":hint[k]["t"],"p":hint[k]["p"],"s":times[k][0],"e":times[k][1],"m":bool(H[k]) and any(pp==k for pp in pairs)} for k in range(n)], open("tmp/aligned.json","w"), indent=0)
# print unmatched words
print("UNMATCHED:", [hint[k]["t"] for k in range(n) if not any(pp==k for pp in pairs)])
