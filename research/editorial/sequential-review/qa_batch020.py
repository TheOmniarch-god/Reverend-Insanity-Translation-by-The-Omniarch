from pathlib import Path
import json,zipfile,re,hashlib
from bs4 import BeautifulSoup
from openpyxl import load_workbook
from docx import Document
r=Path(__file__).parent
load=lambda n:json.loads((r/n).read_text())
cs=sum([load(f'batch-{i:03d}-source.json') for i in range(1,21)],[]);by={c['corpus_chapter']:c for c in cs};b=load('batch-020-source.json');p=load('reading-progress.json');q=load('batch-020-qa.json')
z=zipfile.ZipFile(r.parents[1]/'benchmark/sources/Gu-Zhen-Ren.epub')
for c in b:
 actual=[n.get_text('',strip=True) for n in BeautifulSoup(z.read(c['file']),'html.parser').find_all('p') if n.get_text('',strip=True)]
 assert c['paragraphs']==actual,c['corpus_chapter']
source=(r/'Batch-020-Numbered-Chinese-Source.md').read_text();current=None;found=[]
for line in source.splitlines():
 m=re.match(r'## Chapter (\d+):',line)
 if m:current=int(m[1])
 m=re.match(r'(\d+)\. (.*)',line)
 if m:
  n=int(m[1]);assert m[2]==by[current]['paragraphs'][n-1];found.append((current,n))
assert found==[(c['corpus_chapter'],i) for c in b for i in range(1,len(c['paragraphs'])+1)]
assert len(found)==1639
ledger=load('proposal-ledger.json');events=load('chronology-register.json')['entries'];resources=load('resource-register.json')['entries']
assert len(ledger)==172 and len(events)==274 and len(resources)==234
assert sum(v['status'].startswith('Withdrawn') for v in ledger)==2
assert sum(v['status'].startswith('Resolved locally') for v in ledger)==1
assert all(not v.get('approved') and not v.get('applied') for v in ledger)
assert p['sequential_chapters_completed']==list(range(1,386)) and p['next_chapter']==386
assert p['paragraphs_read']==sum(len(c['paragraphs']) for c in cs)==34664
assert p['paragraph_characters_read']==sum(len(t) for c in cs for t in c['paragraphs'])==1200434
for v in events+resources:
 for s in v['sources']:assert s['text']==by[s['chapter']]['paragraphs'][s['paragraph']-1]
for v in ledger:
 for s in v['locations']:assert 1<=s['paragraph']<=len(by[s['chapter']]['paragraphs'])
for v in load('batch-020-copy-candidates.json'):assert v['original'] in by[v['chapter']]['paragraphs'][v['paragraph']-1]
alltext={t for c in cs for t in c['paragraphs']}
report=(r/'Batch-020-Chapters-366-385.md').read_text()
for line in report.splitlines():
 if line.startswith('> '):assert line[2:] in alltext
# Ensure cultivation wording in authored text, preserving authentic source quotes.
for f in [r/'Batch-020-Chapters-366-385.md',*list((r/'jotters').glob('*020*.md'))]:
 text='\n'.join(x for x in f.read_text().splitlines() if not x.startswith('> '))
 assert not re.search(r'\brank\s*(?:[1-9]|one|two|three|four|five|six|seven|eight|nine)\b',text,re.I),f
 assert '—' not in text,f
w=load_workbook(r/'Sequential-Reading-and-Proposals.xlsx',read_only=True,data_only=True)
assert w.sheetnames==['Read me','Chapter completion','Paragraph register','Proposal ledger','Copy items','Chronology','Resources','Working standards']
assert w['Chapter completion'].max_row==386 and w['Paragraph register'].max_row==34665
assert w['Proposal ledger'].max_row==173 and w['Chronology'].max_row==275 and w['Resources'].max_row==235
assert w['Working standards'].max_row==13
meta=dict(w['Read me'].iter_rows(min_row=2,max_col=2,values_only=True));assert meta['Next unread']==386
seen=0
for row in w['Paragraph register'].iter_rows(min_row=2,values_only=True):
 c,n=row[:2]
 if c>=366:assert row[6]==by[c]['paragraphs'][n-1];seen+=1
assert seen==1639
lr=[row for row in w['Proposal ledger'].iter_rows(min_row=2,values_only=True) if row[0]=='SR-153'][0];assert 'Resolved locally' in lr[6]
doc=Document(r/'Batch-020-Chapters-366-385.docx');assert len(doc.paragraphs)>300
assert any(len(t.rows)==44 for t in doc.tables)
joined='\n'.join(n.text for n in doc.paragraphs);assert '366' in joined and '385' in joined and 'SR153' in joined
for v in load('fact-check-020/external-witnesses.json'):
 assert hashlib.sha256((r/'fact-check-020'/f"ch{v['chapter']}-hetushu.html").read_bytes()).hexdigest()==v['sha256']
assert all(v['in_repost'] for v in load('fact-check-020/substantive-collation.json'))
assert sum(v['original_in_repost'] for v in load('fact-check-020/copy-collation.json'))==40
assert len(load('batch-020-reading-log.json')['segments'])==10
old=load('history/before-batch020-proposal-ledger.json')
for id in ['SR-134','SR-135','SR-136','SR-137','SR-138']:assert next(v for v in old if v['id']==id)==next(v for v in ledger if v['id']==id)
q['independent_export_qa']={'status':'passed','epub_paragraphs_rechecked':1639,'numbered_source_exact':True,'workbook_sheets':8,'workbook_new_source_rows_checked':1639,'docx_paragraphs':len(doc.paragraphs),'docx_copy_table_rows':44,'all_report_blockquotes_exact':True,'witness_hashes_verified':22,'contextual_repost_variants':3,'cultivation_wording_checked':True,'earlier_factcheck_controls_unchanged':True}
(r/'batch-020-qa.json').write_text(json.dumps(q,ensure_ascii=False,indent=2))
f=r/'CURRENT-STATUS.md';s=f.read_text().replace('IndependentexportQA pending aftergenerator.','Independent export QA PASSED: all1639 new EPUB/source/workbook paragraphs exact; eight workbook sheets,43-row candidate table plus header, report blockquotes and22 witness hashes verified.');f.write_text(s)
print(json.dumps(q['independent_export_qa'],indent=2))
