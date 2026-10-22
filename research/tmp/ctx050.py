import json,glob,sys,re
SR='/home/user/editorial/sequential-review'
seen={}
for f in sorted(glob.glob(f'{SR}/batch-0*-source.json')):
    for c in json.load(open(f)): seen[c['corpus_chapter']]=c
pat=sys.argv[1]; w=int(sys.argv[2]) if len(sys.argv)>2 else 14
only=sys.argv[3].split(',') if len(sys.argv)>3 else None
for n in sorted(seen):
    for i,p in enumerate(seen[n]['paragraphs'],1):
        for m in re.finditer(pat,p):
            tag=f'{n}p{i}'
            if only and tag not in only: continue
            print(tag, '|', p[max(0,m.start()-w):m.end()+w])
