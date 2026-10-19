import json, copy, re
from pathlib import Path
from openpyxl import load_workbook
from docx import Document
from docx.shared import Pt
r = Path(__file__).parent
led = json.loads((r/'proposal-ledger.json').read_text())
by = {v['id']: v for v in led}
by['SR-348']['witness_030_032'] = 'Witness collation of 567–568 was checked. The witness has a different word at 568p19 (see SR-382), which does not change the SR-348 query. SR-348 stays a query.'
if 'SR-382' not in by:
    new = copy.deepcopy(led[-1]); new['id'] = 'SR-382'
    new['category'] = 'Word variant (运盗 / 运道), 568p19'
    new['locations'] = [{'chapter': 568, 'paragraph': 19}]
    new['recommended_action'] = 'Query. 568p19 reads 巨阳仙尊即运气大盗，巨阳一死，运盗才消. The Hetushu witness reads 运道才消. Keep 运盗 unless the pun is shown to be an error. No text change.'
    new['rationale'] = 'The witness reading 运道 would match the 运道 used elsewhere for the same fragment, but 运盗 may be a deliberate pun on 运气大盗. The text does not decide this.'
    new['confidence'] = 'Provisional (0.35).'
    new['status'] = 'Provisional query; no approval'
    new['dependencies'] = 'Witness collation for 568 (Hetushu). SR-348 context.'
    new['approved'] = False; new['applied'] = False
    new['publication_status'] = 'Held; not for publication'
    new['witness_030_032'] = 'Witness (ch568 p19) reads 运道才消 where our source reads 运盗才消.'
    for k in list(new.keys()):
        if k.startswith('batch') and k.endswith('_update'): new[k] = ''
    led.append(new)
assert len(led) == 382 and led[-1]['id'] == 'SR-382'
(r/'proposal-ledger.json').write_text(json.dumps(led, ensure_ascii=False, indent=2))
by = {v['id']: v for v in led}

# Report corrections
p = r/'Batch-030-Chapters-566-585.md'; t = p.read_text(encoding='utf-8')
t = t.replace("- Witness has the same typo as our source for SR-338–346, SR-354 and others. These repairs are not confirmed by the witness; they stand on internal evidence only.",
              "- Witness has the same typo as our source for SR-338–346 and others in this batch. These repairs are not confirmed by the witness; they stand on internal evidence only.")
t = t.replace("- New query SR-381 (579p2 马鸿运 vs 马英杰) is recorded in the Batch 031 notes (see ledger).",
              "- New query SR-381 (579p2: 马鸿运 in our source, 马英杰 on the witness page). No text change.\n- New query SR-382 (568p19: 运盗 in our source, 运道 on the witness page). No text change.")
t = t.replace("- Witness supports SR-347 (众所周知 at 584p22).", "- Witness supports SR-347 (众所周知 at 584p22).\n- Witness differs from our source at 568p19 (SR-382) and 579p2 (SR-381).")
p.write_text(t, encoding='utf-8')
p = r/'Batch-031-Chapters-586-605.md'; t = p.read_text(encoding='utf-8')
t = t.replace("- Witness supports SR-361 (绝非易事 at 592p41), SR-360 (神情扭曲 at 605p155). SR-360 is in Batch 030's range; the fact is recorded here.",
              "- Witness supports SR-361 (绝非易事 at 592p41) and SR-360 (神情扭曲 at 605p155).")
p.write_text(t, encoding='utf-8')

# QA
for b in ['batch-030','batch-031','batch-032']:
    q = json.loads((r/f'{b}-qa.json').read_text())
    q['ledger_ids'] = ['SR-338', 'SR-352'] if b=='batch-030' else (['SR-353','SR-365'] if b=='batch-031' else ['SR-366','SR-380'])
    q['ledger_count'] = {'batch-030':15,'batch-031':13,'batch-032':15}[b]
    if b=='batch-030':
        q['witness_collated']=True
    (r/f'{b}-qa.json').write_text(json.dumps(q, ensure_ascii=False, indent=2))
# Workbook
wb = load_workbook(r/'Sequential-Reading-and-Proposals.xlsx')
ws = wb['Proposal ledger']
HOLD = 'HOLD: full2334-chapter reading and global reconciliation outstanding'
v = led[-1]
refs = '; '.join(f"Ch{l['chapter']} p{l['paragraph']}" for l in v['locations'])
ws.append([v['id'], v['category'], refs, v['recommended_action'], v['rationale'], v['confidence'], v['status'],
           v['dependencies'], HOLD, 'No', 'No', 'Batch 030 sequential reading; witness collated; ' + v['witness_030_032']])
for row in wb['Read me'].iter_rows(min_row=1, max_col=2):
    if row[0].value == 'Proposals':
        row[1].value = '382 total; 377 active (held or query); 4 withdrawn; 1 locally resolved'
wb.save(r/'Sequential-Reading-and-Proposals.xlsx')
print('ok ledger', len(led))

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
for m in ['Batch-030-Chapters-566-585','Batch-031-Chapters-586-605','Batch-032-Chapters-606-625']:
    build_docx(m+'.md', m+'.docx'); print('docx', m)
