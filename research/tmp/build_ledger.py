import json, re, os
SR = '/home/user/editorial/sequential-review'
LEDGER = f'{SR}/proposal-ledger.json'
ledger = json.load(open(LEDGER))
last = max(int(e['id'].split('-')[1]) for e in ledger)
assert last == 442, last
BATCHES = {'039': 'Batch-039-Chapters-806-855.md', '040': 'Batch-040-Chapters-856-905.md', '041': 'Batch-041-Chapters-906-955.md'}
def rows(md):
    out = []
    for line in open(f'{SR}/{md}', encoding='utf-8'):
        if not line.startswith('| '): continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) != 7 or not re.match(r'^\d+$', cells[0]): continue
        out.append(cells)
    return out
def witness_for(batch, row):
    p = f'{SR}/witness-collation-{batch}.json'
    if not os.path.exists(p): return None
    for r in json.load(open(p)):
        if str(r['row']) == row: return r
    return None
new = []
n = last
for b, md in BATCHES.items():
    for cells in rows(md):
        num, ref, reading, action, rationale, conf, deps = cells
        if action.startswith(('No action', '—', 'No conflict')) or conf in ('—',):
            continue
        n += 1
        sid = f'SR-{n:03d}'
        m = re.match(r'(\d{3})', ref)
        ch = int(m.group(1)) if m else None
        pm = re.search(r'p(\d+)', ref)
        low = action.lower()
        if action.startswith(('Repair', 'Standardise')):
            cat = 'Typo or wording repair candidate'; status = 'Held repair candidate; unapproved, unapplied'
        elif action.startswith('Check') or 'check' in low[:12]:
            cat = 'Query (check against source line)'; status = 'Query; unapproved, unapplied'
        elif 'decision' in low or 'decide' in low or 'whole-novel' in low or 'reconcile' in low or 'canonical' in low or 'timeline' in low or 'Whole-novel' in action:
            cat = 'Decision / whole-novel reconciliation'; status = 'Open decision; unapproved, unapplied'
        else:
            cat = 'Query'; status = 'Query; unapproved, unapplied'
        w = witness_for(b, num)
        if w:
            wit = f"Hetushu 7640 (ch{w['ch']}): {w['result']}"
            if w.get('cand') and w['result'].startswith('witness shows candidate'):
                wit += '; witness differs from source here and matches the proposed wording (web copy, not authoritative)'
        else:
            wit = 'Not collated: no single-token candidate for automated witness check.'
        new.append({
            'id': sid, 'category': cat,
            'locations': [{'chapter': ch, 'paragraph': int(pm.group(1)) if pm else None, 'file': '', 'reference_text': ref}],
            'recommended_action': f'{action} (batch {b}, row {num}, source reading: {reading})',
            'rationale': f'{rationale} Confidence {conf}.',
            'confidence': conf,
            'status': status,
            'dependencies': deps,
            'publication_status': 'HOLD: complete-corpus reading and global reconciliation outstanding',
            'witness_collation': wit,
            'approved': False, 'applied': False,
        })
print(len(new), new[0]['id'], new[-1]['id'])
json.dump(new, open(f'{SR}/ledger-new-039-041.json','w'), ensure_ascii=False, indent=1)
