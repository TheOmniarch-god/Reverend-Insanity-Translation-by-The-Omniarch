from pathlib import Path
import json,hashlib,concurrent.futures
import requests
from bs4 import BeautifulSoup
from opencc import OpenCC
r=Path(__file__).parent;d=r/'fact-check-022';d.mkdir(exist_ok=True);cc=OpenCC('t2s')
def get(n):
    url=f'https://www.hetushu.com/book/7640/{5345238+n}.html';p=d/f'ch{n}-hetushu.html'
    if not p.exists():
        resp=requests.get(url,timeout=45);resp.raise_for_status();p.write_bytes(resp.content)
    raw=p.read_bytes();s=BeautifulSoup(raw,'html.parser');title=cc.convert(s.title.get_text());body=s.select_one('#content');assert body is not None,(n,title)
    text=cc.convert(body.get_text('',strip=True));(d/f'ch{n}-normalized.txt').write_text(text)
    return dict(chapter=n,url=url,title=title,sha256=hashlib.sha256(raw).hexdigest(),text_chars=len(text),limitation='Single repost tradition, not an authorial master; scrambled order possible; fragment checks only.')
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex: out=list(ex.map(get,list(range(406,426))))
(d/'external-witnesses.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
for o in out: print(o['chapter'],o['title'][:40],o['text_chars'])
