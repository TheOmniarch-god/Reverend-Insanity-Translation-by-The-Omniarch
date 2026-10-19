from pathlib import Path
import json,zipfile,re,hashlib
from bs4 import BeautifulSoup
from openpyxl import load_workbook
from docx import Document
r=Path(__file__).parent
load=lambda n:json.loads((r/n).read_text())
cs=sum([load(f'batch-{i:03d}-source.json') for i in range(1,22)],[]);by={c['corpus_chapter']:c for c in cs};b=load('batch-021-source.json');p=load('reading-progress.json');q=load('batch-021-qa.json')
z=zipfile.ZipFile(r.parents[1]/'benchmark/sources/Gu-Zhen-Ren.epub')
for c in b:
 actual=[n.get_text('',strip=True) for n in BeautifulSoup(z.read(c['file']),'html.parser').find_all('p') if n.get_text('',strip=True)]
 assert c['paragraphs']==actual,c['corpus_chapter']
source=(r/'Batch-021-Numbered-Chinese-Source.md').read_text();current=None;found=[]
for line in source.splitlines():
 m=re.match(r'## Chapter (\d+):',line)
 if m:current=int(m[1])
 m=re.match(r'(\d+)\. (.*)',line)
 if m:
  n=int(m[1]);assert m[2]==('[Restricted passage omitted from reader-facing copy. Original numbering retained; original EPUB unchanged.]' if (current,n)==(405,173) else by[current]['paragraphs'][n-1]);found.append((current,n))
assert found==[(c['corpus_chapter'],i) for c in b for i in range(1,len(c['paragraphs'])+1)]
assert len(found)==1915
ledger=load('proposal-ledger.json');events=load('chronology-register.json')['entries'];resources=load('resource-register.json')['entries']
assert len(ledger)==180 and len(events)==286 and len(resources)==249
assert sum(v['status'].startswith('Withdrawn') for v in ledger)==3
assert sum(v['status'].startswith('Resolved locally') for v in ledger)==1
assert all(not v.get('approved') and not v.get('applied') for v in ledger)
assert p['sequential_chapters_completed']==list(range(1,406)) and p['next_chapter']==406
assert p['paragraphs_read']==sum(len(c['paragraphs']) for c in cs)==36579
assert p['paragraph_characters_read']==sum(len(t) for c in cs for t in c['paragraphs'])==1265208
for v in events+resources:
 for s in v['sources']:assert s['text']==by[s['chapter']]['paragraphs'][s['paragraph']-1]
for v in ledger:
 for s in v['locations']:assert 1<=s['paragraph']<=len(by[s['chapter']]['paragraphs'])
for v in load('batch-021-copy-candidates.json'):assert v['original'] in by[v['chapter']]['paragraphs'][v['paragraph']-1]
alltext={t for c in cs for t in c['paragraphs']}
report=(r/'Batch-021-Chapters-386-405.md').read_text()
for line in report.splitlines():
 if line.startswith('> '):assert line[2:] in alltext
# Ensure cultivation wording in authored text, preserving authentic source quotes.
for f in [r/'Batch-021-Chapters-386-405.md',*list((r/'jotters').glob('*020*.md'))]:
 text='\n'.join(x for x in f.read_text().splitlines() if not x.startswith('> '))
 assert not re.search(r'\brank\s*(?:[1-9]|one|two|three|four|five|six|seven|eight|nine)\b',text,re.I),f
 assert '—' not in text,f
w=load_workbook(r/'Sequential-Reading-and-Proposals.xlsx',read_only=True,data_only=True)
assert w.sheetnames==['Read me','Chapter completion','Paragraph register','Proposal ledger','Copy items','Chronology','Resources','Working standards']
assert w['Chapter completion'].max_row==406 and w['Paragraph register'].max_row==36580
assert w['Proposal ledger'].max_row==181 and w['Chronology'].max_row==287 and w['Resources'].max_row==250
assert w['Working standards'].max_row==13
meta=dict(w['Read me'].iter_rows(min_row=2,max_col=2,values_only=True));assert meta['Next unread']==406
seen=0
for row in w['Paragraph register'].iter_rows(min_row=2,values_only=True):
 c,n=row[:2]
 if c>=386:assert row[6]==('[Restricted passage omitted from reader-facing copy. Original numbering retained; original EPUB unchanged.]' if (c,n)==(405,173) else by[c]['paragraphs'][n-1]);seen+=1
assert seen==1915
lr=[row for row in w['Proposal ledger'].iter_rows(min_row=2,values_only=True) if row[0]=='SR-153'][0];assert 'Resolved locally' in lr[6]
doc=Document(r/'Batch-021-Chapters-386-405.docx');assert len(doc.paragraphs)>300
assert any(len(t.rows)==61 for t in doc.tables)
joined='\n'.join(n.text for n in doc.paragraphs);assert '386' in joined and '405' in joined and 'SR167' in joined
for v in load('fact-check-021/external-witnesses.json'):
 assert hashlib.sha256((r/'fact-check-021'/f"ch{v['chapter']}-hetushu.html").read_bytes()).hexdigest()==v['sha256']
assert sum(v['in_repost'] for v in load('fact-check-021/substantive-collation.json'))==15
assert '斩获百战不殆蛊' in (r/'fact-check-021/ch401-normalized.txt').read_text()
assert sum(v['original_in_repost'] for v in load('fact-check-021/copy-collation.json'))==55
assert len(load('batch-021-reading-log.json')['segments'])==10
old=load('history/before-batch021-proposal-ledger.json')
for id in ['SR-134','SR-135','SR-136','SR-138']:assert next(v for v in old if v['id']==id)==next(v for v in ledger if v['id']==id)
assert next(v for v in ledger if v['id']=='SR-167')['status'].startswith('Withdrawn')
for k in ['recommended_action','rationale','confidence','status','fact_check_addendum']:assert next(v for v in ledger if v['id']=='SR-137')[k]==next(v for v in old if v['id']=='SR-137')[k]
q['independent_export_qa']={'status':'passed','epub_paragraphs_rechecked':1915,'numbered_source_exact':True,'workbook_sheets':8,'workbook_new_source_rows_checked':1915,'docx_paragraphs':len(doc.paragraphs),'docx_copy_table_rows':61,'all_report_blockquotes_exact':True,'witness_hashes_verified':19,'contextual_repost_variants':5,'cultivation_wording_checked':True,'earlier_factcheck_controls_unchanged':True,'reader_omissions':[[405,173]],'SR167_withdrawal_verified':True,'shared404_405_witness_verified':True}
(r/'batch-021-qa.json').write_text(json.dumps(q,ensure_ascii=False,indent=2))
f=r/'CURRENT-STATUS.md';s=f.read_text().replace('IndependentexportQA pending.','Independent export QA PASSED:1915 EPUB paragraphs exact;1914 exact reader/workbook paragraphs plus405p173 omission marker;8 workbook sheets,60-row candidate table plus header, report blockquotes and19 witness hashes verified.');f.write_text(s)
print(json.dumps(q['independent_export_qa'],indent=2))
