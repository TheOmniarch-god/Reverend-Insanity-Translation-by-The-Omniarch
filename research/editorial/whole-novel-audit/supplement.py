from pathlib import Path
import json,re,zipfile
from bs4 import BeautifulSoup
p=Path(__file__).parent;root=p.parent.parent;old=json.loads((p/'hits.json').read_text());seen={(h['file'],h['paragraph']) for h in old};cov=json.loads((p/'coverage.json').read_text());z=zipfile.ZipFile(root/'benchmark/sources/Gu-Zhen-Ren.epub');new=[]
num=re.compile('[一二三四五六七八九十两零〇\\d]+成|百分之|[一二三四五六七八九十两零〇]+分|[一大]半|百分百|\\d+[%％]')
for a in cov:
 s=BeautifulSoup(z.read(a['file']),'html.parser');ps=[q.get_text('',strip=True) for q in s.select('body p')];ps=[q for q in ps if q]
 for i,t in enumerate(ps):
  if (a['file'],i+1) in seen:continue
  ctx=''.join(ps[max(0,i-1):i+2]);cats=[]
  if re.search('空窍|元海|真元|资质',ctx) and (num.search(t) or re.search('球形|球体|体积|容积|高度|水位',t)):
   cats.append('aperture_adjacent_context')
  if re.search('中洲|南疆|天鹤上人|铁喙飞鹤',ctx) and re.search('赶路|行程|路程|里程|时速|飞行速度|迁徙|迁移|跨域|跨越|横跨|辗转|跋涉|赶到|抵达|来到中洲|返回中洲|返回南疆|回中洲',t):cats.append('travel_adjacent_context')
  if not cats:continue
  new.append({k:a[k] for k in ['file','volume','title','corpus_chapter']}|{'paragraph':i+1,'categories':cats,'text':t,'before':ps[max(0,i-1):i],'after':ps[i+1:i+2]})
(p/'supplementary-hits.json').write_text(json.dumps(new,ensure_ascii=False,indent=2));print('Additional unique paragraphs',len(new));print({c:sum(c in h['categories'] for h in new) for c in ['aperture_adjacent_context','travel_adjacent_context']})
