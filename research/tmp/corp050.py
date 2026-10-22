import json,glob,sys,re
SR='/home/user/editorial/sequential-review'
chs=[]
for f in sorted(glob.glob(f'{SR}/batch-0*-source.json')):
    chs+=json.load(open(f))
seen={}
for c in chs: seen[c['corpus_chapter']]=c
toks=sys.argv[1:]
for t in toks:
    hits=[]
    for n in sorted(seen):
        for i,p in enumerate(seen[n]['paragraphs'],1):
            if t in p: hits.append(f'{n}p{i}')
    print(f'{t}: {len(hits)} {hits[:12]}')
