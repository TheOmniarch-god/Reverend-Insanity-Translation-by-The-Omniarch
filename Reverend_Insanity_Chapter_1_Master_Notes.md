# Chapter 1 — Translation and Reading Notes
## First-Person In-Depth Thought

### Why I translated the title this way
**Though the Flesh Perish, the Demonic Heart Knows No Regret**

The Chinese is 肉身虽陨魔心不悔. 肉身 = flesh/body, 陨 = perish/fall, 魔心 = demonic heart, 不悔 = no regret. I wanted to keep the parallel structure: Though X, Y. "Perish" is stronger than "die" — it carries the weight of a cultivator's body falling in battle, not just dying. "Knows No Regret" instead of "has no regret" because 魔心 is personified — the demonic heart *knows*, it is aware, it chooses.

### What I learned in this session that changed Chapter 1

**1. Grade phrasing — "of" vs "a"**

This was the biggest find. I had been writing:
> *would be a Grade A aptitude*
> *only a Grade C?*
> *Only a Grade C!*

User pointed out: "He is of grade A aptitude" is better. Research confirmed:

- `aptitude` is uncountable quality, not a person. You can't *be* an aptitude.
- `be of + quality` is standard English: *of poor quality*, *of very high quality* [Cambridge], *craftsmanship of very high quality* [Merriam-Webster], *a man of quality*.
- `a Grade A` is unnatural — WordReference: *"a grade A is not natural. It is saying the same thing twice."*

Fixed in Ch1:
- *possessing Grade A aptitude was exceptionally high* — kept as possession (okay)
- No `a Grade` left in Ch1 after audit

But for **person**, `a` is correct:
- `a Rank 1 Gu Master`, `a Rank 3 Gu Master` — Gu Master is countable person, Rank modifies the person. You *are* a Gu Master.
- `a Grade A genius` — genius is person, so `a` is correct.

So house rule now:
- **Quality → of**: `of Grade A aptitude`, `merely of Grade C`, `genius of Grade A aptitude`
- **Person → a**: `a Rank 1 Gu Master`, `a Grade A genius`

**2. Rank numerals — Arabic vs Roman**

We currently use `Rank 1`, `Rank 3`, `Rank 4` (Arabic). User asked: should we use Roman `Rank I`?

I kept Arabic because:
- It's standard in 90% of RI translations, more readable on mobile
- `Rank IV` vs `Rank VI` is harder to scan than `Rank 4` vs `Rank 6`
- Matches `Grade A` (letter, not Roman) style
- Our new justified container (680px) reads better with Arabic

If we want classical feel, we can switch to Roman in one push, but I recommend keeping Arabic.

**3. Scene breaks — …… vs * * ***

Original Chinese uses `……` (six dots) as scene break. In Ch1 I found 3 places:
- After opening siege dialogue
- After Fang Yuan self-detonates
- After clan elders disperse, before Fang Yuan at window

House style says scene break `* * *`. I had left `……` in Ch1 flow, which slipped back live after grade fix. Now converted all 3 to `* * *` — same as Ch6. User confirmed we should use `***` at demarcations, not follow Chinese `……`.

**4. Paragraphing — the basics**

User: "Paragraphing is the basics of writing NGL"

Original Chinese is one sentence per paragraph — very gappy on web. I had reflowed Ch1 73 → 45 paras (too aggressive, merged different speakers), then fixed to proper dialogue rule: new speaker = new paragraph, narration merged to 50-120w.

Final Ch1: **55 paras**, avg 49w, 3 scene breaks. Example of fix:
- Before (wrong): Chi Lian + Mo Chen + Bo in one 153w paragraph
- After (correct): 3 separate paras, each speaker alone

**5. Punctuation house style — zero tolerance**

Audit found live Ch1 had:
- 14 em dashes `—` — e.g., `summit—today`, `atrocities—unpardonable`, `abyssal—like an ancient well`, `breath— With a thunderous blast`
- All replaced with commas/periods per house style: 0 em dashes allowed
- `……` left as scene break — replaced with `* * *`
- Curly `’ “ ”` and ellipsis `…` enforced, zero straight `'` `"` and zero `...`

**6. Clack sound — Chapter 3 find that affected Chapter 1 audit**

In Ch3 we had two versions:
- Old: `The patrolling night watchman struck his wooden clapper in a repeating rhythm—one beat, then two.`
- Approved: `Clack, clack-clack. Clack, clack-clack. The night watchman was making his rounds...`

The approved version with onomatopoeia was lost when I overwrote masters with flow versions. Restored from `before_ch3_discord_concubine` backup. This taught me to save masters after every approved change — I now save both Flow.md and Master_Translation.md in workspace.

**7. Reading container — mobile felt broad**

User screenshot showed large blank space before "Chapter..." and broad reading area on mobile Brave.

Fixes pushed:
- `chapter-body` max-width 700px → 680px (better 65-75 chars per line)
- Added prose container: white card, border `#e7e5de`, radius 12px, padding 36px 32px, shadow
- Mobile ≤700px: padding 8px 12px 60px, font-size 16px, line-height 1.8, prose 22px 18px, radius 10px
- Mobile ≤480px: 8px 8px 50px, 15.5px, 1.75 line-height, 18px 14px, no border
- Header gap: `reader-head` 122px top/20px bottom → 100px/12px (web), 72px/8px on mobile. Total gap header→text from ~88px to ~16px on mobile.

**8. Justification**

User asked my take. I recommended:
- Web: `text-align: justify; hyphens: auto; text-justify: inter-word;` — book-like clean edge
- Mobile: `text-align: left; hyphens: none;` — no rivers, better for OpenDyslexic mode

Pushed live. Web now justified, mobile left.

**9. Confusing files audit**

Live audit found:
- Homepage meta said `Chapters 1–5 available` but we have 6 live — fixed to `1–6`
- Old redirect pages `/chapter-001`, `/chapter-002` existed with em dash in title `Redirecting —` — deleted, now 404
- Search-index had glossary leak `* Refine... * Demonic Path...` in Ch2 — removed
- Ch3 had `*suffocation*!` markdown emphasis — fixed to `suffocation!`

Workspace has 35 md/docx in root + 19 backup folders + `ch6_build/`. Per user, stored all drafts in new branch `archive/drafts` (96 files) on GitHub, main stays clean.

### Chapter 1 specific translation choices I kept

- **Old Demon Fang** — keeping Fang as name, Old Demon as epithet
- **Spring Autumn Cicada** — not Spring and Autumn Cicada, keeping compact
- **towering atrocities—unpardonable** → `towering atrocities, unpardonable` — em dash removed, comma keeps flow
- **eyes were abyssal—like an ancient well** → `abyssal, like an ancient well` — appositive
- **And in that very breath— With a thunderous blast** → `breath. With a thunderous blast` — strong break needs period, not comma
- **stilt houses—not ten thousand** → `houses, not ten thousand` — parenthetical
- **Bai Ning Bing of the Bai clan—his natural talent** → `clan, his natural talent` — appositive

All same wording, only breaks and punctuation moved per house style.

### What I would do next for Chapter 1 if you want

- Add `* * *` is now 3 places, but check if Ch1 needs a 4th break between green mountains poem and "Countless memories..." — currently merged, could be separate for breath
- Consider whether `……` as ellipsis inside dialogue should stay `……` (Chinese style) or become `…` (house style) — I kept `……` for dramatic pause in siege, but house says `…` single char. We have 4 `……` left in Ch1 as ellipsis, not scene breaks — should we convert those to `…` or keep `……` as stylistic?

Let me know if you want those last `……` inside prose converted to `…` as well.
