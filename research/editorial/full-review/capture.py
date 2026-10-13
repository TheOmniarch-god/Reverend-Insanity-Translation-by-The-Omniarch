import requests,json,hashlib,concurrent.futures
from pathlib import Path
from bs4 import BeautifulSoup
p=Path(__file__).parent
base='https://ri.theomniarch.com.ng'
def get(n):
 u=base+(f'/chapter-{n}' if n else '/');r=requests.get(u,timeout=30);r.raise_for_status();r.encoding='utf-8';(p/f'live-{n}.html').write_text(r.text)
 s=BeautifulSoup(r.text,'html.parser');b=s.select_one('.prose') if n else s
 if b is None:raise ValueError(f'No prose {u}')
 for a in b.select('a.note-ref'):a.decompose()
 rows=[{'id':x.get('id'),'text':x.get_text(' ',strip=True),'html':str(x)} for x in b.select('p')];(p/f'en-{n}.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));(p/f'en-{n}.txt').write_text('\n\n'.join(f"{x['id']}: {x['text']}" for x in rows))
 return {'url':u,'sha256':hashlib.sha256(r.content).hexdigest(),'paragraphs':len(rows),'date_header':r.headers.get('Date'),'etag':r.headers.get('ETag')}
with concurrent.futures.ThreadPoolExecutor(max_workers=9) as e:r=list(e.map(get,range(9)))
(p/'manifest.json').write_text(json.dumps({'review_date':'2026-10-13','captures':r},indent=2));print(json.dumps(r,indent=2))
