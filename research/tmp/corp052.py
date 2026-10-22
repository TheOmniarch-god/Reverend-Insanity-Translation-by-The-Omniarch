import json, glob, sys, re
from collections import defaultdict
hits = defaultdict(list)
for f in sorted(glob.glob('editorial/sequential-review/batch-*-source.json')):
    for c in json.load(open(f)):
        for i, p in enumerate(c['paragraphs'], 1):
            for t in sys.argv[1:]:
                for m in re.finditer(re.escape(t), p):
                    hits[t].append(f"{c['corpus_chapter']}p{i}")
for t in sys.argv[1:]:
    h = hits[t]
    print(t, len(h), h[:14])
