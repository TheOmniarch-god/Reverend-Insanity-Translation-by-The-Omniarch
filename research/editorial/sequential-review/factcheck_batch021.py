from pathlib import Path
import json,hashlib,concurrent.futures,re
import requests
from bs4 import BeautifulSoup
from opencc import OpenCC
r=Path(__file__).parent;d=r/'fact-check-021';d.mkdir(exist_ok=True);cc=OpenCC('t2s')
cs=sum([json.loads((r/f'batch-{i:03d}-source.json').read_text()) for i in range(1,22)],[]);by={c['corpus_chapter']:c for c in cs}
def get(n):
 url=f'https://www.hetushu.com/book/7640/{5345239+n}.html';p=d/f'ch{n}-hetushu.html'
 if not p.exists():
  resp=requests.get(url,timeout=45);resp.raise_for_status();p.write_bytes(resp.content)
 raw=p.read_bytes();s=BeautifulSoup(raw,'html.parser');title=cc.convert(s.title.get_text());body=s.select_one('#content');assert body is not None,(n,title)
 text=cc.convert(body.get_text('',strip=True));(d/f'ch{n}-normalized.txt').write_text(text)
 return dict(chapter=n,url=url,title=title,sha256=hashlib.sha256(raw).hexdigest(),limitation='Single repost tradition, not an authorial master; HTML order scrambled, checked fragments only. Traditional-to-simplified normalisation used for comparison.')
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex: out=list(ex.map(get,list(range(386,405))))
out[-1]['coverage_chapters']=[404,405]
out[-1]['coverage_note']='Page404also contains appended405material, verified by recipe,poem,teleport andsummit fragments.'
(d/'external-witnesses.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print(json.dumps(out,ensure_ascii=False,indent=2))
