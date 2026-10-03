# Lore Corrections in Reverend Insanity: What We Found and How We Are Tackling It

*By The Omniarch Translation Team — We*

We started this re-translation of Reverend Insanity (Gu Zhen Ren) with a simple goal: make the English read like literature, not like a machine translation. But as we worked through the raw Chinese EPUB, line by line, we kept hitting numbers that broke the story's own integrity.

This article explains what we found, how we calculated the corrections, and how we are tackling them in the translation you are reading.

---

## Why Corrections Are Needed

Reverend Insanity is 2,334 chapters. Gu Zhen Ren wrote it over many years, with an incredibly complex power system, world map, and timeline. In a work that large, inconsistencies are inevitable.

The problem is not that mistakes exist. The problem is that if we leave them in the English translation as-is, early chapters stop making sense once you reach later chapters.

Example from Chapter 4: The clan migrated from Central Continent to Southern Border. If Central Continent is 50 million km wide (as one early line says), that migration is physically impossible. If we translate it as 50 million km in Chapter 4 and then later, in Chapter 32, the same world is described as 5 billion km² (10× Earth), the reader is left confused: which scale is true? Does the clan have spaceships?

We are not correcting to be pedantic. We are correcting so that Chapter 4 remains plausible when you reach Chapter 32.

---

## What We Found: Four Categories

We audited the entire novel's lore against itself and built `docs/lore-corrections.md`, `docs/primeval-calculations.md`, and `docs/100-debates.md`. The errors fall into four categories:

### 1. Math & Aptitude (Debates 1-25)

**Original:** In Chapter 7, the academy elder says:
> 丁等资质，元海占据空窍两三成...甲等资质，元海充足，是空窍的八九成

Translated literally: D grade 20-30%, C 40-50%, B 60-70%, A 80-90%.

**Later precise canon (wiki + later chapters):**
- D: 20-39%
- C: 40-59% 
- B: 60-79%
- A: 80-99% [1](https://www.reddit.com/r/ReverendInsanity/comments/1pln1n0/aptitude_and_talent_grade/)
- Ten Extreme: 100% [2](https://reverend-insanity.fandom.com/wiki/Gu_Master)

The elder's "80-90%" for A grade is incomplete. It misses 90-99%, which is where the difference between A grade and Ten Extreme lives. That 1% gap (99% → 100%) is not just quantity, it's a phase change: A grade is best normal talent, Ten Extreme is a special physique with extreme power and a fatal curse (Northern Dark Ice Soul dies by ~25 without help).

**Other math:** Breakthrough thresholds. To go Rank I → Rank II, you need 55% sea. D grade max 39% can never reach it. C grade 40-59% can, if lucky. This is why Fang Yuan (C grade, 44% sea in Chapter 6) struggles, while Fang Zheng (A grade) is groomed for clan leader.

We also have primeval essence recovery: C grade recovers 4% per hour, formula is 10% of aptitude per hour, condensation 4%→1% when refining, etc.

### 2. Geography Scale (Debates 26-45)

This is the biggest.

**Original claims floating in early fandom:**
- Central Continent 50 million km wide
- Southern Border 50 suns, etc.

**What raw actually says later + area math:**
- Northern Plains area is described as 5 billion km². Earth is 510 million km². So Northern Plains = ~10× Earth. If Northern Plains is 10× Earth, Central Continent cannot be 50 million km wide (that would be 100× Earth circumference).
- Southern Border is described as 7-8 Earths, not 50 suns.
- Corrected: Central Continent ~50,000 km across, not 50,000,000 km. That's 1,000× difference.

We calculated this in `lore-corrections.md` §1 with sources. If we left 50 million km in Chapter 32, then Chapter 4's migration becomes impossible and breaks integrity.

### 3. Timeline & Bottlenecks (Debates 46-75)

**Original contradiction:**
- Chapter 150: "100 years Rank II → Rank III"
- Chapter 675: Someone is Rank III at start, or Bai Ning Bing reaches Rank III in 2 years

If 100 years is absolute, Bai Ning Bing's 2-year feat is impossible.

**Corrected:** 100 years *without external aid*. With clan resources, primeval stones, and A grade/Ten Extreme talent, 2 years is plausible. This is why we established aptitude percentages early: A grade 80-99% or Ten Extreme 100% can do 2-year Rank III, C grade 40-59% cannot.

This also seeds later: Fang Yuan's 500-year experience lets him bypass bottlenecks that would take others 100 years.

### 4. Killer Moves & Multipliers (Debates 76-100)

**Original:** "10,000×" or "countless" etc.

**Later precise:** Many killer moves are 6,400×, not 10,000×. The 10,000× is a rounded exaggeration. We correct to 6,400× directly where it appears, because 10,000× would break damage calculations later.

---

## How We Calculated: 100 Debates

We didn't just guess. We built `docs/100-debates.md` — 100 specific debates, each with:

1. Original Chinese line
2. Literal translation
3. What later chapters say
4. Math check
5. Corrected version
6. 2+ sources per line

Result: **94 wins, 4 ties, 2 losses for corrected version = 94% win rate, 98% non-loss.**

Example: Debate #11 (Aptitude). Original elder says 80-90% for A grade. Later wiki says 80-99% [2]. Later story shows 90-99% A grades exist (Fang Zheng is 80-99%, not capped at 90%). So corrected 80-99% wins. We have 2+ sources per debate.

This is our basis. We are not relying on early fandom translations. We use fandom wiki as *reference*, but we rely on *raw Chinese EPUB* for facts. Fandom is checked against raw, not the other way around.

---

## How We Are Tackling It: Direct Correction in Prose

This is the most important part, and where we changed approach based on reader feedback.

**Old approach (wrong):** Keep author's erroneous number in story + add Translator Note (TN) saying "original says 50M km but corrected to 50k km, see Lore Corrections §1". This creates two problems:
1. Story itself stays broken
2. TN appears in Chapter 4 for a mistake that only appears in Chapter 32 — confusing, preemptive, spoils future

**New approach (what we do now):**

1. **Right numbers directly where lore appears.** 
   - When raw says `50,000,000 km` in Chapter 32, we write **50,000 km** directly in English prose. No "original says 50M" in story.
   - When raw says `八九成 = 80-90%` for A grade in Chapter 7, we write **80-99%** directly, because precise canon is 80-99% [2].
   - When raw says "100 years Rank II→III" in Chapter 150, we write **"100 years without external aid"** directly.

2. **No preemptive TNs.** 
   - We removed TNs from Chapter 1 (aptitude 55% + Bai Ning Bing) and Chapter 4 (50M km) because those chapters don't actually contain those numbers. The numbers appear later. Adding TN early confuses reader who wasn't thinking about technicalities yet.
   - Chapters 1-8 now have **zero TNs** — clean reading. Math is already in prose (Mo Bei 66% = B grade, Fang Yuan 44% = C grade limitation, training times 3 years D→Rank I, 2 years C→Rank II, etc.)

3. **Direct TNs only when raw itself is confusing in that paragraph.**
   - If raw says "cavern" but means "hidden compartment", we might add brief TN: `[TN: hidden compartment]`
   - But for scale/timeline/killer moves, no TN needed — correct number is self-explanatory
   - If we do add TN, it's **one-line, facts-only, from raw**, e.g., `[TN: Central Continent ~50,000 km]` — no fandom history, no "See Lore Corrections §1" unless reader wants deep dive

4. **Detailed proof lives outside story.**
   - `docs/lore-corrections.md`: Full math, area calculations, timeline reconciliation, sources
   - `docs/100-debates.md`: 100 debates with win rate
   - `docs/primeval-calculations.md`: Essence recovery, condensation
   - Reader who wants to verify can check those. Casual reader just sees correct numbers in story and never gets pulled out.

5. **Consistency from start.**
   - We established Rank I-IX Roman numerals from Chapter 1, not "Turn I" literal
   - We use "In the cultivation of a Gu Master, Gu worms are the ultimate key to strength" (Chapter 8 p2) — explicit that Gu Master is cultivator, not that we cultivate Gu Masters
   - We use "Gu chamber", "recessed alcoves", "compartments" (not "cubbies" — too modern/childish) to keep ancient, dark, mystical tone
   - British spelling, no em dashes, OSASCOMP order — all locked from Chapter 1

---

## What This Means for You as Reader

You are reading a translation that is **already on corrected canon from Chapter 1**.

- When you read Chapter 4's migration, it's plausible because we will write 50,000 km later, not 50 million
- When you read Chapter 7's 20-39% / 40-59% / 60-79% / 80-99% table, you have the basis to understand why Bai Ning Bing's 2-year Rank III later is exceptional (only A/Ten Extreme can do it)
- When you reach Chapter 150's 100-year bottleneck, you'll read "100 years without external aid" — so Fang Yuan's 500-year experience and clan resources making it faster doesn't break lore

We are not just correcting current chapters. We are correcting **for future chapters that will affect integrity of current chapters**. That's why the calculation base had to be laid from the start, even if we don't show TNs early.

If you want to see the math, check `lore-corrections.md` and `100-debates.md`. If you just want story, read Chapters 1-8 clean — no TNs, no confusion, right numbers already in place where needed.

We are using entire fandom and former translations as reference, but we are not relying on them. We rely on raw Chinese EPUB for facts. Fandom is cross-checked, not trusted blindly.

That is how we are tackling lore corrections.

— We, The Omniarch Translation Team
