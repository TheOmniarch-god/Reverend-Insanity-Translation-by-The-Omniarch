import json, sys
b=sys.argv[1]; nums=[int(x) for x in sys.argv[2].split(",")]
d=json.load(open(f"editorial/sequential-review/batch-{b}-source.json"))
for c in d:
    if c["corpus_chapter"] in nums:
        print(f"=== {c['corpus_chapter']} {c['title']} {len(c['paragraphs'])}")
        for i,p in enumerate(c["paragraphs"],1): print(f"{i} {p}")
