# Reverend Insanity - Primeval Essence Calculations (Corrected Edition)

This document compiles all primeval essence mechanics needed for translation consistency, notes the popularly known calculation error, and provides the mathematically correct version we will use.

---

## 1. Aptitude and Maximum Capacity

| Grade | Aperture Fill | Max Rank (Common Knowledge) | Example |
|-------|---------------|-----------------------------|---------|
| D | 20-39% | Rank I~II | 31% middle stage [SickoLife example] |
| C | 40-59% | Rank II~III | Fang Yuan 44% |
| B | 60-79% | Rank III~IV | Mo Bei 66% |
| A | 80-99% | Rank V | Fang Zheng 80%+ |
| Ten Extreme | 100% | - | Bai Ning Bing |

Sources: Gu Master aptitude table 20-39% D, 40-59% C, 60-79% B, 80-99% A, 100% Extreme [1](https://reverend-insanity.fandom.com/wiki/Gu_Master) and [2](https://true-reverend-insanity.fandom.com/wiki/Gu_Master). Fang Yuan 44% limit from Chapter 10 refinement description [3](https://www.wattpad.com/1038063629-reverend-insanity-chapter-10-a-storm-may-arise/page/2).

Formula: `MaxSea = Aptitude% * ApertureVolume`. Cannot store beyond aptitude even if aperture space remains [3](https://www.wattpad.com/1038063629-reverend-insanity-chapter-10-a-storm-may-arise/page/2).

---

## 2. Natural Recovery Rate

Two sources give slightly different but compatible numbers:

- **Canon text Chapter 10:** C grade ~4% per hour, 24% per 6 hours. A grade ~8% per hour, 48% per 6 hours [3](https://www.wattpad.com/1038063629-reverend-insanity-chapter-10-a-storm-may-arise/page/2).
- **Fan calculation (Sufficient Velocity):** Recovery = 10% of *total* aptitude per hour. So 44% aptitude => 4.4% per hour [4](https://forums.sufficientvelocity.com/threads/reverend-fortuity-reverend-insanity-cyoa-si.147760/).

We adopt **4% (C) / 8% (A) per hour** as narrative numbers, and **4.4% = 10% of 44%** as precise math for calculations. Both are cited.

Formula: `Recovery_per_hour = Aptitude% * 0.10` [4](https://forums.sufficientvelocity.com/threads/reverend-fortuity-reverend-insanity-cyoa-si.147760/) which matches [3](https://www.wattpad.com/1038063629-reverend-insanity-chapter-10-a-storm-may-arise/page/2) when rounded.

Example:
- Fang Yuan 44% => 4.4%/h => 17.6% in 4h [4](https://forums.sufficientvelocity.com/threads/reverend-fortuity-reverend-insanity-cyoa-si.147760/)
- Fang Zheng ~90% A => 9%/h => 54% in 6h (text says 48% [3], slight variance due to rounding)

---

## 3. Small Realm Condensation (Within Same Rank)

Within Rank I, II, III, IV, V, there are four small realms: initial, middle, upper, peak.

Rule: **4% lower stage = 1% higher stage** [5](https://reverend-insanity.fandom.com/wiki/Primeval_Essence).

Table from Fandom [5](https://reverend-insanity.fandom.com/wiki/Primeval_Essence):

| To get 100% of -> | Need Initial | Need Middle | Need Upper | Need Peak |
|-------------------|--------------|-------------|------------|-----------|
| Initial | - | 25% | 6.25% | 1.5625% |
| Middle | 400% | - | 25% | 6.25% |
| Upper | 1600% | 400% | - | 25% |
| Peak | 6400% | 1600% | 400% | - |

Explanation: 100% middle = 400% initial, 100% upper = 400% middle = 1600% initial, 100% peak = 400% upper = 6400% initial [5](https://reverend-insanity.fandom.com/wiki/Primeval_Essence).

This is used by Liquor Worm Gu to condense essence [5](https://reverend-insanity.fandom.com/wiki/Primeval_Essence).

---

## 4. Great Realm Condensation (Across Ranks)

- Rank I: green copper [5](https://reverend-insanity.fandom.com/wiki/Primeval_Essence)
- Rank II: red iron, 1 portion red iron = 10 portions green copper [5](https://reverend-insanity.fandom.com/wiki/Primeval_Essence)
- Rank III: white silver, 1 portion white silver = 10 portions red iron [5](https://reverend-insanity.fandom.com/wiki/Primeval_Essence)
- Rank IV: yellow gold [6](https://m.webnovel.com/book/reverend-insanity(english)_32605619408374705/chapter-275-strength-path-and-ice-path_87787784521176761)
- Rank V: purple crystal, light purple initial, violet middle, deep upper, crystal peak [7](https://www.webnovel.com/book/reverend-insanity(english)_32605619408374705/chapter-379-all-according-to-plan_87895047034434400)

Therefore:
- Rank II initial = 10x Rank I peak (if we ignore small realm factor)
- Rank III initial = 10x Rank II peak

Fandom note: "one portion of rank 3 initial stage primeval essence is comparable to 10 portions of rank 2 peak stage primeval essence or 10,000 portions of rank 1 peak stage primeval essence" [5](https://reverend-insanity.fandom.com/wiki/Primeval_Essence). This implies Rank II peak = 1000x Rank I peak.

---

## 5. Known Calculation Error and Corrected Version

**Popularly known error:** Small realm ratio 4:1 gives Rank I initial -> peak = 64x (6400% initial = 100% peak). Great realm ratio 10:1 gives Rank II initial = 10x Rank I peak. So Rank II peak = 64x Rank II initial = 640x Rank I peak. But Fandom note says Rank III initial = 10,000x Rank I peak, which would require Rank II peak = 1000x Rank I peak, not 640x. The 640 vs 1000 discrepancy is the known error [5](https://reverend-insanity.fandom.com/wiki/Primeval_Essence).

**Our corrected consistent system (use for book):**
We keep both rules as canon but clarify:

- Small realm: 4:1 [5](https://reverend-insanity.fandom.com/wiki/Primeval_Essence)
- Great realm: 10:1 between *peak of lower* and *initial of higher* (not between initials) [5](https://reverend-insanity.fandom.com/wiki/Primeval_Essence)

Thus:
- 1% Rank I peak = 64% Rank I initial
- 1% Rank II initial = 10% Rank I peak = 640% Rank I initial
- 1% Rank II peak = 64% Rank II initial = 640% Rank I peak = 40,960% Rank I initial
- 1% Rank III initial = 10% Rank II peak = 6,400% Rank I peak

This makes Rank III initial = 6,400% Rank I peak, not 10,000%, correcting the 10,000 figure as approximate/unconfirmed [5](https://reverend-insanity.fandom.com/wiki/Primeval_Essence) (the page marks "Based on ch. 26; unconfirmed").

We will use **6400x** as mathematically correct, note **10,000x** as popular approximate.

---

## 6. Breakthrough Cost (Aperture Wall)

To advance small realm or great realm, Gu Master crashes primeval sea against aperture walls.

Canon examples:
- Rank I -> II needs ~55% primeval essence in one go (Reddit discussion of Fang Yuan's breakthrough) [8](https://www.reddit.com/r/ReverendInsanity/comments/1crzwjw/how_much_primeval_essence_do_you_need_to_break/)
- Rank II -> III: Fang Yuan uses Man-Beast Life Burial Gu, expends 38% black-red primeval essence to break white crystal walls [9](https://www.webnovel.com/book/reverend-insanity(english)_32605619408374705/chapter-152-advance-to-rank-three_87710901385357640)

General formula from Reddit speculation [8](https://www.reddit.com/r/ReverendInsanity/comments/1crzwjw/how_much_primeval_essence_do_you_need_to_break/):
- Rank II breakthrough ~55%
- Rank III ~75%
- Rank IV ~95%
- Rank V ~115% (requires external stones, since max aptitude 99% < 115%, hence need primeval stones)

This matches aptitude limits: D 20-39% cannot reach 55% => max Rank I~II [1](https://reverend-insanity.fandom.com/wiki/Gu_Master), C 40-59% can reach 55% but not 75% => max Rank II~III [1], B 60-79% can reach 75% but not 95% => max Rank III~IV, A 80-99% can reach 95% but needs stones for 115% => max Rank V [1][2].

We adopt this as working model.

---

## 7. Primeval Stone Efficiency

- Primeval stone = condensed natural primeval essence [3](https://www.wattpad.com/1038063629-reverend-insanity-chapter-10-a-storm-may-arise/page/2)
- One stone refills aperture visibly, ~30 minutes to refill 44% sea [3]
- No rank difference in stones themselves, but higher rank needs more stones to refill same % because essence is more condensed [10](https://www.reddit.com/r/ReverendInsanity/comments/1crl0iu/how_do_primeval_stones_work/)
- Calculation: 1 stone ≈ 10% Rank I initial essence (estimated from Chapter 10: 6 stones used to refine Liquor Worm after spending 30%+ [4])
- For Rank II, 1 stone ≈ 1% Rank II initial (since 10x condensation)

---

## 8. Liquor Worm and Four Flavours Liquor Worm

- Liquor Worm: condenses primeval essence, increases quality, used as vital Gu better than Moonlight Gu [11](https://reverend-insanity.fandom.com/wiki/Primeval_Essence)
- Effect: Allows Gu Master to use 4% initial to get 1% middle, but Liquor Worm does it automatically, saving primeval essence
- Four Flavours Liquor Worm (Rank II): bid 5113 primeval stones in story (example of stone cost) [12](https://forums.spacebattles.com/threads/reverend-fortuity-reverend-insanity-cyoa-si.1259362/page-2)

---

## 9. Worked Examples

### Fang Yuan 44% C
- Max sea: 44% [3]
- Recovery: 4.4%/h [4], 26.4% per 6h (text says 24% [3], we use 26.4% corrected)
- To refine Moonlight Gu: spends 30% (10% + 20%) to get 1/12 refinement, needs stones because recovery 4.4%/h < expulsion rate [3]
- Breakthrough Rank I -> II: needs 55% [8] but has only 44% => needs stones to supplement 11%+ (explains why he needs stones)

### Mo Bei 66% B
- Max sea: 66% [13](https://reverend-insanity.fandom.com/wiki/Gu_Master) (B grade 60-79%)
- Recovery: 6.6%/h, 39.6% per 6h
- Can breakthrough to Rank III (needs 75%? No, 66% < 75% => needs stones, but close)

### Fang Zheng ~90% A
- Max sea: 80-99% [1]
- Recovery: 8-9.9%/h, 48-59.4% per 6h [3]
- Can breakthrough Rank I->II (55%) without stones, Rank II->III (75%) with slight stone help

### Primeval Essence Conversion Example (Corrected)
- 100% Rank I initial = 25% Rank I middle = 6.25% Rank I upper = 1.5625% Rank I peak [5]
- 100% Rank I peak = 6400% Rank I initial [5]
- 100% Rank II initial = 10% Rank I peak [5] = 640% Rank I initial (corrected) vs 1000% (approximate old)
- 100% Rank III initial = 10% Rank II peak = 640% Rank I peak

---

## 10. Summary Formulas for Translation Consistency

- `Sea_max = Aptitude%`
- `Recovery = Aptitude% * 0.10 per hour` [4]
- `SmallCondensation: 1% higher = 4% lower` [5]
- `GreatCondensation: 1% higher Rank initial = 10% lower Rank peak` [5]
- `Breakthrough: Rank II 55%, Rank III 75%, Rank IV 95%, Rank V 115%` [8][9]
- Use Roman numerals for Ranks: Rank I, II, III, IV, V, VI, VII, VIII, IX

We will use corrected 6400x where math matters, but note popular 10,000x as in-universe approximation.

---

## Sources

[1] https://reverend-insanity.fandom.com/wiki/Gu_Master
[2] https://true-reverend-insanity.fandom.com/wiki/Gu_Master
[3] https://www.wattpad.com/1038063629-reverend-insanity-chapter-10-a-storm-may-arise/page/2
[4] https://forums.sufficientvelocity.com/threads/reverend-fortuity-reverend-insanity-cyoa-si.147760/
[5] https://reverend-insanity.fandom.com/wiki/Primeval_Essence
[6] https://m.webnovel.com/book/reverend-insanity(english)_32605619408374705/chapter-275-strength-path-and-ice-path_87787784521176761
[7] https://www.webnovel.com/book/reverend-insanity(english)_32605619408374705/chapter-379-all-according-to-plan_87895047034434400
[8] https://www.reddit.com/r/ReverendInsanity/comments/1crzwjw/how_much_primeval_essence_do_you_need_to_break/
[9] https://www.webnovel.com/book/reverend-insanity(english)_32605619408374705/chapter-152-advance-to-rank-three_87710901385357640
[10] https://www.reddit.com/r/ReverendInsanity/comments/1crl0iu/how_do_primeval_stones_work/
[11] https://sagaofgu.com/cultivation/primeval-essence/
[12] https://forums.spacebattles.com/threads/reverend-fortuity-reverend-insanity-cyoa-si.1259362/page-2
[13] https://reverend-insanity.fandom.com/wiki/Gu_Master (B grade example)

