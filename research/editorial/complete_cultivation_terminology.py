from pathlib import Path
import re,json,zipfile,io,hashlib
from lxml import etree
root=Path('/home/user');base=root/'editorial';backup=base/'terminology-backups'/'before-revolution-terminology.zip';backup.parent.mkdir(exist_ok=True)
pat=re.compile(r'Rank(?=[A-Z0-9])|\bRANKS?\b|\bRanks?\b|\branks?\b')
def repl(m):
 s=m.group();return {'Rank':'Revolution','Ranks':'Revolutions','rank':'revolution','ranks':'revolutions','RANK':'REVOLUTION','RANKS':'REVOLUTIONS'}[s]
def sub(s):return pat.sub(repl,s)
def markdown(s):return ''.join(line if line.lstrip().startswith('>') else sub(line) for line in s.splitlines(keepends=True))
def jwalk(v,key=''):
 if isinstance(v,dict):return {k:jwalk(x,k) for k,x in v.items()}
 if isinstance(v,list):return [jwalk(x,key) for x in v]
 if isinstance(v,str):return v if key in {'text','original','source_text','source_quote','english','chinese','first_paragraph','last_paragraph'} else sub(v)
 return v
files=[]
for p in base.rglob('*'):
 if not p.is_file() or 'terminology-backups' in p.parts or p.name in {'change_cultivation_terminology.py','complete_cultivation_terminology.py','terminology-revolution-change-log.json','terminology-revolution-followup-log.json'}:continue
 if p.name in {'All Errors Tackled Together.docx','errors-plan-extracted.txt'}:continue
 if p.parent==base or 'sequential-review' in p.parts or 'whole-novel-audit' in p.parts or p.suffix=='.md':files.append(p)
files += list((root/'benchmark').glob('*.md'))+list((root/'benchmark').glob('*.docx'))+list((root/'qa').glob('*.md'))
changes=[];source_hash=hashlib.sha256((root/'benchmark/sources/Gu-Zhen-Ren.epub').read_bytes()).hexdigest()
with zipfile.ZipFile(backup,'a',zipfile.ZIP_DEFLATED) as bak:
 names=set(bak.namelist())
 for p in sorted(set(files)):
  old=p.read_bytes();new=old
  if p.suffix in {'.md','.txt','.py','.json'}:
   s=old.decode('utf-8')
   if p.suffix=='.json':t=json.dumps(jwalk(json.loads(s)),ensure_ascii=False,indent=2) if pat.search(s) else s
   elif p.suffix=='.md':t=markdown(s)
   elif p.suffix=='.py':t=re.sub(r'Rank(?=[A-Z0-9])|\bRanks?\b|\bRANKS?\b',repl,s)
   else:t=sub(s)
   new=t.encode('utf-8')
  elif p.suffix in {'.docx','.xlsx','.pptx'}:
   zin=zipfile.ZipFile(io.BytesIO(old));buf=io.BytesIO();changed=False
   with zipfile.ZipFile(buf,'w',zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
     data=zin.read(item.filename)
     if item.filename.endswith('.xml') and item.filename.startswith(('word/','xl/','ppt/')):
      tree=etree.fromstring(data)
      for node in tree.xpath('//*[local-name()="t"]'):
       if not node.text or not pat.search(node.text):continue
       # Preserve actual quoted source passages in Word's quotation paragraphs.
       ps=node.xpath('ancestor::*[local-name()="p"]')
       if ps and any('quote' in str(x).lower() for x in ps[-1].xpath('.//*[local-name()="pStyle"]/@*[local-name()="val"]')):continue
       node.text=sub(node.text);changed=True
      data=etree.tostring(tree,xml_declaration=True,encoding='UTF-8',standalone=True)
     zout.writestr(item,data)
   if changed:new=buf.getvalue()
  if new!=old:
   rel=str(p.relative_to(root))
   if rel not in names:bak.writestr(rel,old);names.add(rel)
   p.write_bytes(new);changes.append(rel)
assert hashlib.sha256((root/'benchmark/sources/Gu-Zhen-Ren.epub').read_bytes()).hexdigest()==source_hash
manifest={'instruction':'Use Revolution instead of Rank for cultivation levels in assistant-authored editorial materials. User-approved terminology only; held substantive emendations remain held.','changed_files':changes,'count':len(changes),'backup':str(backup.relative_to(root)),'preserved':'Original EPUB, uploads, captured live/source snapshots, quoted-source fields and original-fragment fields. Immutable pre-change backup retained.','source_sha256_unchanged':source_hash}
(base/'terminology-revolution-followup-log.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
print(json.dumps({'changed_files':len(changes),'backup':str(backup),'source_unchanged':True}))
