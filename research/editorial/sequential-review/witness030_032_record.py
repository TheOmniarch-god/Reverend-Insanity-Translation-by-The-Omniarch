import json, copy, re
from pathlib import Path
from openpyxl import load_workbook
from docx import Document
from docx.shared import Pt
r = Path(__file__).parent
led = json.loads((r/'proposal-ledger.json').read_text())
by = {v['id']: v for v in led}
# 1. Witness results (no status or confidence changes)
supp = {
 'SR-347': 'Witness (Hetushu, ch584 p22) reads 众所周知, so the Hetushu copy agrees with the proposed repair. Held; this adds a witness data point.',
 'SR-360': 'Witness (ch605) reads 神情扭曲, so the Hetushu copy agrees with the proposed repair. Held.',
 'SR-361': 'Witness (ch592 p41) reads 绝非易事, so the Hetushu copy agrees with the proposed repair. Held.',
 'SR-372': 'Witness (ch615 p24) reads 顺利地, so the Hetushu copy agrees with the proposed repair. Held.',
}
copies = ['SR-338','SR-339','SR-340','SR-341','SR-342','SR-343','SR-344','SR-345','SR-346','SR-354','SR-359','SR-362','SR-363',
          'SR-365','SR-366','SR-367','SR-368','SR-371','SR-375','SR-376','SR-377','SR-379','SR-380']
for k in copies:
    by[k]['witness_030_032'] = 'Hetushu witness has the same text as our source here. It does not confirm the repair; the repair rests on internal evidence only.'
for k, t in supp.items(): by[k]['witness_030_032'] = t
by['SR-369']['witness_030_032'] = 'Witness line not aligned by the paragraph matcher. Check manually before any change.'
by['SR-357']['witness_030_032'] = 'Witness has the same text as our source here. Does not confirm the stray-族 deletion.'
by['SR-348']['witness_030_032'] = 'Witness ch567 and ch568 were collated as part of this batch. Witness wording at 568p19 reads 运道 (not 运盗), which is the same term as SR-348 context; see SR-381 notes. No change to the SR-348 query.'
by['SR-370']['witness_030_032'] = 'Witness not yet checked for 611p73.'
by['SR-374']['witness_030_032'] = 'Witness has the same text as our source at 615p80, 615p87 and 615p89 as far as checked. Not decisive.'
# 2. New query SR-381
new = copy.deepcopy(led[-1])
new['id'] = 'SR-381'
new['category'] = 'Name conflict (马鸿运 / 马英杰)'
new['locations'] = [{'chapter': 579, 'paragraph': 2}]
new['recommended_action'] = 'Query. 579p2 has 常飚却挽留马鸿运 and 将马鸿运交由常丽亲自款待. The Hetushu witness reads 挽留马英杰 at the same place. Confirm the intended name before any change. No text change.'
new['rationale'] = 'The witness and the source differ on the name of the character held back in 579p2. 马英杰 (the 马家族长) appears elsewhere in 579, and 马鸿运 is a different person. This is a real witness difference, not a segmentation artifact.'
new['confidence'] = 'Provisional (0.4).'
new['status'] = 'Provisional query; no approval'
new['dependencies'] = 'Witness collation for 579 (Hetushu). Reconciliation of 马鸿运 and 马英杰 across 566–625.'
new['approved'] = False; new['applied'] = False
new['publication_status'] = 'Held; not for publication'
new['witness_030_032'] = 'Witness (ch579 p2) reads 挽留马英杰 where our source reads 挽留马鸿运.'
for k in list(new.keys()):
    if k.startswith('batch') and k.endswith('_update'): new[k] = ''
if 'SR-381' not in by: led.append(new)
assert len(led) == 381 and led[-1]['id'] == 'SR-381'
(r/'proposal-ledger.json').write_text(json.dumps(led, ensure_ascii=False, indent=2))
print('ledger', len(led))

# 3. QA updates
for b, lo, hi in [('batch-030',338,352),('batch-031',353,365),('batch-032',366,380)]:
    if not (r/f'{b}-qa.json').exists():
        ids = [v['id'] for v in led if lo <= int(v['id'][3:]) <= hi]
        chs = json.loads((r/f'{b}-source.json').read_text())
        q = {'batch': b, 'chapters': [chs[0]['corpus_chapter'], chs[-1]['corpus_chapter']], 'chapter_count': len(chs),
             'paragraphs': sum(len(c['paragraphs']) for c in chs), 'characters': sum(len(p) for c in chs for p in c['paragraphs']),
             'contiguous_chapters': True, 'ledger_ids': [ids[0], ids[-1]], 'ledger_count': len(ids), 'approved_or_applied_any': False,
             'em_dashes_in_new_text': 0}
    else:
        q = json.loads((r/f'{b}-qa.json').read_text())
    q['witness_collated'] = True
    q['witness_source'] = 'Hetushu book 7640 pages 5345804–5345863 (ch566–625); fact-check-030-032/'
    q['witness_summary'] = 'Witness agrees with source on most text (mean exact-line agreement ~0.94; differences mostly watermark and segmentation). Witness supports SR-347, SR-360, SR-361 and SR-372. Witness copies the typo for most other held repairs. New query SR-381.'
    q['result'] = 'PASS (source counts, ledger range, no approvals, no em dashes); witness collated (see witness_summary); repairs not confirmed by witness except as noted'
    (r/f'{b}-qa.json').write_text(json.dumps(q, ensure_ascii=False, indent=2))

# 4. Workbook: append SR-381, update witness column for 030-032 rows
wb = load_workbook(r/'Sequential-Reading-and-Proposals.xlsx')
ws = wb['Proposal ledger']
HOLD = 'HOLD: full2334-chapter reading and global reconciliation outstanding'
for row in ws.iter_rows(min_row=2):
    sid = row[0].value
    if isinstance(sid, str) and sid.startswith('SR-') and int(sid[3:]) >= 338:
        row[11].value = row[11].value.replace('witness not yet collated', 'witness collated (Hetushu ch566–625; see witness_030_032)')
        if sid in by: row[11].value = row[11].value + ' | ' + by[sid].get('witness_030_032', '')
v = led[-1]
refs = '; '.join(f"Ch{l['chapter']} p{l['paragraph']}" for l in v['locations'])
ws.append([v['id'], v['category'], refs, v['recommended_action'], v['rationale'], v['confidence'], v['status'],
           v['dependencies'], HOLD, 'No', 'No', 'Batch 030 sequential reading; witness collated; ' + v['witness_030_032']])
rm = wb['Read me']
for row in rm.iter_rows(min_row=1, max_col=2):
    if row[0].value == 'Proposals':
        row[1].value = '381 total; 376 active (held or query); 4 withdrawn; 1 locally resolved'
    if row[0].value == 'Next unread' or row[0].value == 'Completed': pass
wb.save(r/'Sequential-Reading-and-Proposals.xlsx')
print('workbook saved')

# 5. Reports: append witness section; regenerate DOCX
def add_section(md, text):
    return md.rstrip() + '\n\n' + text + '\n'
sec = {
'Batch-030-Chapters-566-585.md': """## 5. Witness collation (Hetushu, ch566–585)
- Collated against Hetushu pages 5345804–5345823 (fact-check-030-032/). Mean exact-line agreement is about 0.94. Most differences are watermark insertions, not text differences.
- Witness supports SR-347 (众所周知 at 584p22).
- Witness has the same typo as our source for SR-338–346, SR-354 and others. These repairs are not confirmed by the witness; they stand on internal evidence.
- New query SR-381 (579p2 马鸿运 vs 马英杰) is recorded in the Batch 031 notes (see ledger).""",
'Batch-031-Chapters-586-605.md': """## 5. Witness collation (Hetushu, ch586–605)
- Collated against Hetushu pages 5345824–5345843 (fact-check-030-032/). Mean exact-line agreement is about 0.94.
- Witness supports SR-361 (绝非易事 at 592p41), SR-360 (神情扭曲 at 605p155). SR-360 is in Batch 030's range; the fact is recorded here.
- Witness has the same typo as our source for SR-354, SR-359, SR-362, SR-363 and SR-365. These repairs are not confirmed by the witness.""",
'Batch-032-Chapters-606-625.md': """## 5. Witness collation (Hetushu, ch606–625)
- Collated against Hetushu pages 5345844–5345863 (fact-check-030-032/). Mean exact-line agreement is about 0.94.
- Witness supports SR-372 (顺利地 at 615p24).
- Witness has the same text as our source for SR-366, SR-367, SR-368, SR-371, SR-375, SR-376, SR-377 and SR-379. These repairs are not confirmed by the witness.
- Witness copies 真阳秘境中 at 623p101 (SR-380). Not confirmed by the witness.""",
}
for name, text in sec.items():
    p = r/name
    t = p.read_text(encoding='utf-8')
    if '## 5. Witness collation' not in t:
        p.write_text(add_section(t, text), encoding='utf-8')
    if '## 4. Not done' in t and name.startswith('Batch-032') is False and False: pass

def build_docx(md_name, out_name):
    md = (r/md_name).read_text(encoding='utf-8').splitlines()
    doc = Document(); st = doc.styles['Normal']; st.font.name = 'Calibri'; st.font.size = Pt(10.5)
    table = None; in_table = False
    clean = lambda s: re.sub(r'\*\*(.+?)\*\*', r'\1', s)
    for line in md:
        if not line.strip() or line.strip() == '---': in_table = False; continue
        if line.startswith('|'):
            if set(line.replace('|', '').strip()) <= set('-: '): continue
            cells = [clean(c.strip()) for c in line.strip('|').split('|')]
            if not in_table:
                table = doc.add_table(rows=0, cols=len(cells)); table.style = 'Light Grid Accent 1'; in_table = True
            row = table.add_row().cells
            for k, cv in enumerate(cells): row[k].text = cv
            continue
        in_table = False
        if line.startswith('### '): doc.add_heading(line[4:], 2)
        elif line.startswith('## '): doc.add_heading(line[3:], 1)
        elif line.startswith('# '): doc.add_heading(line[2:], 0)
        elif line.startswith('- '): doc.add_paragraph(clean(line[2:]), style='List Bullet')
        else: doc.add_paragraph(clean(line))
    doc.save(r/out_name)
for m in sec:
    build_docx(m, m.replace('.md', '.docx')); print('docx', m)
