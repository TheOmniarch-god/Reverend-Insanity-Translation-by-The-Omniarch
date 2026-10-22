import openpyxl, json
SR = '/home/user/editorial/sequential-review'
srcs = []
for b in ['052']:
    srcs += json.load(open(f'{SR}/batch-{b}-source.json'))
srcs = sorted(srcs, key=lambda c: c['corpus_chapter'])
assert [c['corpus_chapter'] for c in srcs] == list(range(1456, 1506)), 'range mismatch'

ledger = json.load(open(f'{SR}/proposal-ledger.json'))
pmap = {}
for e in ledger:
    for loc in e['locations']:
        if loc.get('chapter') and loc.get('paragraph'):
            pmap.setdefault((loc['chapter'], loc['paragraph']), []).append(e['id'])

wb = openpyxl.load_workbook(f'{SR}/Sequential-Reading-and-Proposals.xlsx')
cc = wb['Chapter completion']; pr = wb['Paragraph register']; rm = wb['Read me']; pl = wb['Proposal ledger']

# --- 1. Proposal ledger sheet: add SR-716..SR-821 (not yet in sheet) ---
existing_ids = {r[0] for r in pl.iter_rows(min_row=2, values_only=True) if r[0]}
added_ledger = 0
for e in ledger:
    if e['id'] in existing_ids:
        continue
    n = int(e['id'].split('-')[1])
    if n < 1131:
        raise SystemExit(f'unexpected missing id {e["id"]}')
    refs = '; '.join(l.get('reference_text', '') for l in e['locations'])
    pl.append([e['id'], e['category'], refs, e['recommended_action'], e['rationale'],
               e['confidence'], e['status'], e['dependencies'], e['publication_status'],
               'No', 'No', e.get('witness_collation', '')])
    added_ledger += 1

# --- 1b. Correct SR-1240 (batch 051 row 46, withdrawn repair) if present in sheet ---
corr = {e['id']: e for e in ledger}.get('SR-1240')
fixed = 0
if corr:
    for row in pl.iter_rows(min_row=2):
        if row[0].value == 'SR-1240':
            row[1].value = corr['category']; row[3].value = corr['recommended_action']
            row[4].value = corr['rationale']; fixed += 1
print('SR-1240 sheet rows corrected:', fixed)

# --- 2. Chapter completion ---
existing_ch = {r[0] for r in cc.iter_rows(min_row=2, values_only=True)}
assert 1455 in existing_ch and 1456 not in existing_ch
for c in srcs:
    cc.append([c['corpus_chapter'], c['file'], c['title'], len(c['paragraphs']), 'Full sequential read'])

# --- 3. Paragraph register ---
newchars = 0; newparas = 0
for c in srcs:
    ch = c['corpus_chapter']
    for i, p in enumerate(c['paragraphs'], 1):
        ids = pmap.get((ch, i))
        pr.append([ch, i, 'Read; not certified error-free',
                   ', '.join(sorted(set(ids))) if ids else None, None, None, p])
        newchars += len(p); newparas += 1

# --- 4. Read me ---
old = {}
for row in rm.iter_rows(min_row=1, max_row=rm.max_row):
    old[row[0].value] = row[1].value
prev_paras = int(old['Paragraphs']); prev_chars = int(old['Characters'])
total_ledger = len(ledger)
for row in rm.iter_rows(min_row=1, max_row=rm.max_row):
    k = row[0].value
    if k == 'Completed': row[1].value = '1–1505 of 2334'
    elif k == 'Next unread': row[1].value = '1506'
    elif k == 'Paragraphs': row[1].value = str(prev_paras + newparas)
    elif k == 'Characters': row[1].value = str(prev_chars + newchars)
    elif k == 'Proposals':
        row[1].value = f'{total_ledger} total (SR-001 to SR-{total_ledger:03d}); batches 036–052 added; nothing approved or applied'

wb.save(f'{SR}/Sequential-Reading-and-Proposals.xlsx')
print('ledger rows added', added_ledger, 'sheet last id', pl.cell(pl.max_row, 1).value)
print('sheet ids seen before:', len(existing_ids))
print('chapters added', len(srcs), 'paragraphs added', newparas, 'chars added', newchars)
print('linked paragraphs in 1456-1505:', sum(1 for k in pmap if 1456 <= k[0] <= 1505))
print('Read me before', prev_paras, prev_chars)
