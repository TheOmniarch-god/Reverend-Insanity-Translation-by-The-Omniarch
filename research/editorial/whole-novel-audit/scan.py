from pathlib import Path
import json,re,zipfile,hashlib,csv
from collections import Counter
from bs4 import BeautifulSoup
root=Path('/home/user');out=Path(__file__).parent
source=root/'benchmark/sources/Gu-Zhen-Ren.epub'
m=json.loads((root/'editorial/chapter-reference-map.json').read_text())
narr=[x for x in m if re.match(r'^第[零〇一二三四五六七八九十百千万两\d]+[节章]',x['title'])]
assert len(narr)==2334
z=zipfile.ZipFile(source);hits=[];coverage=[];counts=Counter()
num=re.compile(r'[一二三四五六七八九十两零〇\d]+成|百分之|\d+[%％]')
for ordinal,item in enumerate(narr,1):
 soup=BeautifulSoup(z.read(item['file']),'html.parser');ps=[p.get_text('',strip=True) for p in soup.select('body p')];ps=[p for p in ps if p]
 if not ps:raise ValueError(item['file'])
 chapter_counts=Counter();both=any('中洲' in p for p in ps) and any('南疆' in p for p in ps)
 for i,p in enumerate(ps):
  cats=[]
  aperture=bool(re.search('空窍|元海|真元|资质',p))
  if aperture and re.search('高度|体积|容积|球形|球体|海面|海平面|水位',p):cats.append('aperture_geometry')
  if aperture and num.search(p):cats.append('aperture_percentages')
  if '中洲' in p and '南疆' in p:cats.append('central_southern_link')
  if both and re.search('赶路|行程|路程|赶到|到达|抵达|辗转|迁徙|迁移|跨越|横跨|跋涉|飞行|回中洲|来到南疆',p):cats.append('regional_journey_context')
  if re.search('中洲|南疆|北原|西漠|东海|五域',p) and re.search('亿里|万里|亿亩|万亩|面积|幅员|广袤|地球|直径|方圆',p):cats.append('regional_scale')
  if '界壁' in p and re.search('蛊师|蛊仙|凡人|修为|越强|五转|跨越|穿越|通过|消失|耗费|消耗|代价|压制',p):cats.append('regional_barriers')
  if re.search('定仙游|星门|洞地|通天|传送|宇道',p) and re.search('五域|跨域|南疆|中洲|距离|路程|时间',p):cats.append('travel_methods')
  if not cats:continue
  rec={**item,'corpus_chapter':ordinal,'paragraph':i+1,'categories':cats,'text':p,'before':ps[max(0,i-1):i],'after':ps[i+1:i+2]}
  hits.append(rec);chapter_counts.update(cats);counts.update(cats)
 coverage.append({**item,'corpus_chapter':ordinal,'paragraph_count':len(ps),'characters':sum(map(len,ps)),'hits':dict(chapter_counts),'status':'automated_screen_complete'})
(out/'hits.json').write_text(json.dumps(hits,ensure_ascii=False,indent=2))
(out/'coverage.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2))
with (out/'chapter-coverage.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['corpus_chapter','volume','title','epub_file','paragraphs','characters','matched_paragraphs','screen_status'])
 for a in coverage:w.writerow([a['corpus_chapter'],a['volume'],a['title'],a['file'],a['paragraph_count'],a['characters'],len([h for h in hits if h['file']==a['file']]),a['status']])
summary={'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'narrative_chapters_screened':len(coverage),'paragraphs_screened':sum(a['paragraph_count'] for a in coverage),'characters_screened':sum(a['characters'] for a in coverage),'unique_hit_paragraphs':len(hits),'category_counts':dict(counts),'method':'Automated paragraph-level Chinese expression screen, not full contextual reading of every chapter. Context is one paragraph on either side. Ordinals follow actual EPUB spine; cite volume/title/file as authoritative.'}
(out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2));print(json.dumps(summary,ensure_ascii=False,indent=2))
for cat in counts:
 lines=[f'# {cat}','']
 for h in hits:
  if cat not in h['categories']:continue
  lines.extend([f"## Corpus {h['corpus_chapter']} | {h['volume']} {h['title']} | {h['file']} | paragraph {h['paragraph']}",*h['before'],'**'+h['text']+'**',*h['after'],''])
 (out/f'{cat}.md').write_text('\n'.join(lines))
