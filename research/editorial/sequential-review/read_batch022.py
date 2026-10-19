import json,zipfile,sys
from pathlib import Path
from bs4 import BeautifulSoup
r=Path('/home/user/editorial/sequential-review');f=r/'batch-022-source.json'
if not f.exists():
 meta=json.load(open(r.parent/'whole-novel-audit/coverage.json'));z=zipfile.ZipFile('/home/user/benchmark/sources/Gu-Zhen-Ren.epub');cs=[]
 for m in meta[405:425]:
  c={k:m[k] for k in ['corpus_chapter','file','volume','title']};c['paragraphs']=[p.get_text('',strip=True) for p in BeautifulSoup(z.read(m['file']),'html.parser').find_all('p') if p.get_text('',strip=True)];cs.append(c)
 f.write_text(json.dumps(cs,ensure_ascii=False,indent=2))
for c in json.loads(f.read_text()):
 if int(sys.argv[1])<=c['corpus_chapter']<=int(sys.argv[2]):
  print('\nCHAPTER',c['corpus_chapter'],c['title'])
  for i,t in enumerate(c['paragraphs'],1):print(f'{i}: {t}')
