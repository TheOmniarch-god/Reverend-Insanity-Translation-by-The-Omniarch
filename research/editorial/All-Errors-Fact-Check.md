# Fact-check: All Errors Tackled Together
## Source-based review for The Omniarch

**Date:** 12 October 2026  
**Status:** editorial recommendations only. No proposed lore change has been applied to the translation or approved on the translator’s behalf.

## Executive conclusion

The document contains many accurately reproduced Chinese passages and several sound decisions to leave the story unchanged. However, its proposed mathematical framework is not ready for adoption. Two negative search conclusions are overturned by explicit passages in the supplied EPUB, and several proposed corrections are unsupported extrapolations rather than recoverable source facts.

**Most consequential findings:**

1. Fang Yuan’s century-long Revolution 2 bottleneck is explicitly present. The source also says an aptitude-raising Gu enabled his eventual advancement.
2. Central Continent explicitly stretches **亿里**, one hundred million li. Under a modern 0.5-km-per-li conversion, this gives fifty million kilometres. That scale is not simply an English invention.
3. Liquor Worm processing expenditure, essence concentration, and combat power were conflated. A specific activation example supports 2:1 initial-to-middle-stage essence expenditure, not a universal 4:1 potency ratio.
4. 6,400% is 64 times, not 6,400 times. The proposed blanket replacement of 10,000 with 6,400 must be stopped.
5. The 55% Revolution 1-to-2 threshold and Fang Yuan’s multi-day stone-assisted breakthrough are supported. The proposed 65/75/85% ladder is not established by the evidence located.
6. The full battlefield passage explicitly discusses exceptions. The later Yama test is a legitimate continuity query, not yet a demonstrated contradiction with only one permissible repair.
7. Xiong Jiao Man has one explicit death in this EPUB; the later barrier scene names Gu Yue Yao Ji. No survival rewrite is needed.

---

## 1. Scope, source, and verification method

### Documents checked

- User-supplied document: `All Errors Tackled Together.docx`, downloaded from the exact link provided in the conversation. The original has been preserved unchanged in `editorial/`.
- Chinese base: the repository EPUB previously supplied by The Omniarch, locally saved as `benchmark/sources/Gu-Zhen-Ren.epub`.
- SHA-256 of that EPUB: `1ef1c29b6bddd7994f56696e2d091363aa8bbcee4889439465a9e2c51437dd5d`.

This review checks what that particular EPUB says. It does not authenticate every statement as the author’s final intention, establish the genealogy of every correction, or certify all 2,334 narrative chapters against an official manuscript.

### What was done

- Read the supplied audit’s extracted paragraph and table text.
- Matched its labelled Chinese quotations against the EPUB text.
- Searched the full extracted EPUB using Chinese number and unit variants, not just Arabic numerals or English-derived search strings.
- Read surrounding passages for the principal mathematical and continuity claims.
- Built a chapter map from the EPUB’s actual spine and headings.
- Recomputed the arithmetic independently.

The referenced companion files `lore-corrections.md` and `primeval-calculations.md` were not supplied or inspected for this pass. Conclusions about the document’s proposed derivations concern what this DOCX actually states, supplemented by the source passages located.

### Status terminology

- **Confirmed:** directly supported by the checked source.
- **Correct conclusion, revise reasoning:** the recommended outcome is defensible but the argument overreaches.
- **Contradicted:** located source or arithmetic conflicts with the claim.
- **Unestablished:** no adequate evidence located; not a proof of absence.
- **Continuity query:** a genuine tension requiring further contextual or edition checking.
- **Adaptation:** a deliberate change to the fictional world, not a translation correction demonstrated by the source.

---

## 2. Source identity and chapter numbering

### File counts: reconcile rather than dismiss

The EPUB contains:

| Measure | Count |
|---|---:|
| ZIP entries | 2,360 |
| HTML documents | 2,345 |
| Spine entries | 2,345 |
| Files named `chapterN.html` | 2,342 |

Therefore, the document’s **2,342 files** count is meaningful if it specifically means the `chapterN.html` set. It is not the count of every file in the EPUB, nor should those files all be called narrative chapters. The initial eight numbered files include front matter and volume-divider material.

My earlier mention of 2,345 HTML documents was not incompatible with that narrower 2,342 count. This is a counting-definition issue, not evidence that either side has a different book.

### Required citation format

Use **volume + printed chapter number + title + EPUB filename**.

Examples:

| Audit label | Actual source location |
|---|---|
| Ch13 | Volume 1, Chapter 5, 人祖三蛊，希望开窍; `chapter13.html` |
| Ch15 | Volume 1, Chapter 7, 蛊师有九转，花酒留遗藏; `chapter15.html` |
| Ch37 | Volume 1, Chapter 29, 不择手段; `chapter37.html` |
| Ch197 | Volume 1, Chapter 189, 惊变; `chapter197.html` |
| Ch202 | Volume 1, Chapter 194, 血幕天华; `chapter202.html` |
| Ch342 | Volume 2, Chapter 135, 仙鹤门，方正; `chapter342.html` |
| Ch754 | Volume 4, Chapter 88, 加入僵盟; `chapter754.html` |
| Ch906 | Volume 4, Chapter 240, 入东海; `chapter906.html` |
| Ch1594 | Volume 5, Chapter 554, 来不及; `chapter1594.html` |

Do not apply a universal numerical offset across the whole novel. The generated `chapter-reference-map.json` preserves the actual mapping.

### Provenance language

The production note says the book uses a 知轩藏书-collated text as its base and describes subsequent multi-version proofreading. It does not certify that every textual error has been removed.

Replace “It has removed all textual errors” with:

> This is our designated base edition. It incorporates a 知轩藏书-collated text and subsequent editorial work. We verify suspected errors against its exact wording and record any further intervention separately.

Also replace the DOCX’s garbled production-note transcription with the EPUB wording. For example, the EPUB has **二次编者**, not “二次编排”, and **大部分劳动**, not “大部分显示”. Its note describes a subsequent editor, not an entity called “Second typesetting”.

**Do not attribute every remaining defect to the author.** A defect in this file can be authorial, inherited, or introduced during transmission or editing.

---

## 3. Aptitude mathematics

### A1. Grade bands

**Verdict: broadly supported; strengthen citations and define precision.**

The Chapter 7 table gives 两三成, 四五成, 六七成, 八九成. More specific passages are available:

- Volume 1, Chapter 91, `chapter99.html`: C-grade storage is explicitly **at least 四成 and at most 五成九**, or 40% to 59%.
- Volume 1, Chapter 135, `chapter143.html`: the best A-grade aptitude reaches **九成九**, and a fully expressed Ten Extreme physique has **十成**, or 100%.

Thus C = 40–59 and A’s upper value = 99 have direct support beyond interpreting the abbreviated early table. The D/B integer endpoints follow the stated band scheme, but the audit should distinguish that reconstruction from an explicit endpoint sentence.

If fractional percentages are to be introduced elsewhere, write a mathematical interval policy separately. Integer ranges such as 20–39 leave ambiguity at 39.5 if the edition later permits decimal precision. Do not quietly invent a measurement resolution.

A qualification is needed for Ten Extreme physiques: Volume 1, Chapter 199 (`chapter207.html`) depicts Bai Ning Bing’s aptitude falling from 100% to 90% after Yin Gu. Do not treat 100% as the instantaneous reading of every suppressed or recovering physique.

**Action:** keep the familiar whole-number grade bands, backed by these later passages. Do not claim that the early shorthand alone demonstrates every exact boundary and decimal rule.

### A2. Natural recovery: the alleged 10%-of-aptitude formula

**Verdict: unestablished. Preserve stated rates; do not install the formula.**

Volume 1, Chapter 10, `chapter18.html`, explicitly gives:

- Fang Yuan: approximately four percentage points per hour; twenty-four over six hours.
- Fang Zheng: eight per hour; forty-eight over six hours.

Volume 1, Chapter 50, `chapter58.html`, also describes Fang Zheng’s recovery as twice Fang Yuan’s.

These support the stated comparative advantage. They do not prove that all individuals recover exactly one tenth of their personal maximum every hour.

The proposed formula changes Fang Yuan’s six-hour recovery from the stated 24 points to 26.4. That may be compatible with a loose approximation, but compatibility is not proof of an exact hidden formula.

**Denominator:** use percentage points of full aperture capacity. Do not confuse this with a percentage of the remaining essence or of a character’s personal maximum.

**Action:** retain “about four” and “eight” where the source gives them. If a linear model is adopted for editorial modelling, label it an assumption and test downstream scenes before changing prose.

### A3. Liquor Worm: expenditure is not potency

**Verdict: the document’s general 4:1 potency inference is unsupported and conflicts with a concrete usage example.**

Volume 1, Chapters 29 and 34 (`chapter37.html`, `chapter42.html`) describe:

1. Ten units of initial-stage essence consumed to create wine mist.
2. Another ten units passed into that mist.
3. Those latter ten units reduced to five units of middle-stage essence.

Therefore:

- **Total input/output expenditure:** (10 + 10) / 5 = 4.
- **Volume ratio of the processed portion:** 10 / 5 = 2.

The first ten units power the process. They are not all retained in the resulting essence.

There is stronger practical evidence in Volume 1, Chapter 62, `chapter70.html`:

> 一转中阶就需要一成真元，换算成初阶，每次使用就得两成真元。

For that Gu’s activation, ten points of middle-stage essence correspond to twenty points of initial-stage essence. That is a **2:1 expenditure equivalence for the stated activation**.

This does not, by itself, prove a universal twofold law across all stages, all Gu, and every type of effect. It does disallow treating the Liquor Worm’s 4:1 total processing cost as the demonstrated potency ratio.

**Action:** keep four separate quantities: processing cost, resulting volume, activation expenditure, and effect. Never substitute one for another without a source-supported relationship.

### A4. 6,400% versus 6,400 times

**Verdict: arithmetic error.**

Even under the unproven fourfold-per-stage assumption:

| Stage | Ratio to initial stage | Expressed as percentage of initial |
|---|---:|---:|
| Initial | 1 | 100% |
| Middle | 4 | 400% |
| Upper | 16 | 1,600% |
| Peak | 64 | 6,400% |

**6,400% = 64 times.**

The separate multiplication 80 × 80 = 6,400 is numerically correct, but the document never demonstrates that those factors represent the quantities in the killer-move passage it proposes to change.

A further reason not to perform a blanket replacement: the EPUB explicitly supports **100 × 100 = 10,000** for a different system, immortal essence. Volume 5, Chapter 627, `chapter1666.html`, says one white-litchi bead can, in the stated sense, be reckoned as a hundred red-date beads and ten thousand green-grape beads. Volume 5, Chapter 185, `chapter1226.html`, also explicitly gives a hundred green-grape beads merging into one red-date bead.

**Action:** reject the blanket 10,000 → 6,400 edit. Locate the exact disputed killer move before ruling on that individual number. Do not import mortal-stage arithmetic into immortal-essence accounting.

### A5. Tenfold mortal revolution relationships

**Verdict: confirmed at the scope actually stated.**

Volume 1, Chapter 26, `chapter34.html`:

> 一份赤铁真元，可比十份的青铜真元。同样的，一份白银真元可比十份的赤铁真元！

The source explicitly gives those broad Revolution 1/2/3 comparisons. It does not specify every pairing of early/peak substages in that sentence.

**Action:** preserve the comparisons. Do not construct a fully stage-resolved conversion matrix without resolving which substages are being compared.

### A6. Breakthrough thresholds

**Verdict: 55% confirmed; 65/75/85% not established in this pass.**

Volume 1, Chapters 90–91 (`chapter98.html`, `chapter99.html`) explicitly give an ordinary minimum of **55% dark-green essence** to break through to Revolution 2, excluding special circumstances.

Full-text literal searches found:

- 五成五: three occurrences, all in the relevant early discussion.
- 六成五: one occurrence, concerning expenditure of Mo Yao’s false will, not a breakthrough threshold.
- 七成五 / 八成五: no exact occurrences.

This is a search result, not proof that no paraphrase or other numerical form exists. However, the document supplies no supporting passage for the higher thresholds either.

**Action:** retain 55% in its stated context. Remove 65/75/85% from the “confirmed canon” table pending evidence.

### A7. Four-to-five-day stone-assisted breakthrough

**Verdict: confirmed for this Revolution 1-to-2 attempt; not a universal cross-revolution rule.**

Volume 1, Chapter 91 explicitly describes Fang Yuan’s plan to keep attacking while absorbing essence from stones, estimating at most four or five days. Chapter 92, `chapter100.html`, depicts success and describes four days and three nights of continuous effort.

Chapter 92 also explains the required willpower, patience, cultivation experience, split attention, and fine control of expenditure and replenishment. It is not merely “own enough stones”.

**Action:** retain this episode and its mechanics. Do not extrapolate its duration to every low-aptitude breakthrough, especially Revolution 2-to-3.

### A8. Six-to-seven-year B-grade schedule

**Verdict: source timeframe supported; invented decomposition not supported.**

The early chapter gives the broad developmental estimate. It does not establish the document’s proposed year-by-year allocations.

Initial → middle → upper → peak has **three within-revolution transitions**, not four. Two completed revolutions have six within-revolution transitions, followed by two major-revolution transitions on the path to Revolution 3. If “wash” means a different operation, it needs its own definition and evidence.

Nor does an exceptional two-year achievement establish that it is *only* possible through the document’s proposed recovery formula. Special Gu, resources, aptitude, experience, and plot-specific aids matter.

**Action:** keep the original estimate; delete the unsupported explanatory schedule from settled lore.

---

## 4. Geography and world scale

### G1. Southern Border compared with Earth

**Verdict: source confirmed, but the audit overstates precision.**

Volume 1, Chapter 29, `chapter37.html`, says Southern Border is **vaster than the combined area of seven or eight Earths**.

“Vaster than” is not “equal to”, and the phrase is approximate. The approximate arithmetic 7–8 × 510 million km² = 3.57–4.08 billion km² is a useful reference calculation, not an exact regional survey derived from the sentence.

### G2. Central Continent’s enormous extent is present in Chinese

**Verdict: the claim that the fifty-million-kilometre figure must be an old-translation error is contradicted.**

Volume 2, Chapter 135, 仙鹤门，方正, `chapter342.html`:

> 中洲幅员辽阔，绵延亿里，元气最为充裕，门派林立。

The relevant phrase is **绵延亿里**, extending for one hundred million li. If the translation uses 1 li = 0.5 km, that converts to fifty million kilometres.

The source does not literally say “diameter”, nor does it provide a cartographic shape in this sentence. A precise geometric interpretation is a separate question. But the enormous linear expression exists in the Chinese.

Searching only `5000万公里` cannot detect this passage. The failed search was too narrow to support its conclusion.

**Action:** do not replace it with 50,000 km as a translation correction. A reduction by a factor of 1,000 would be an explicit scale adaptation requiring a wider audit of distances, travel speeds, territories, and later descriptions.

### G3. Northern Plains

**Verdict: source supports the broad scale; 5 billion km² is rounded.**

Volume 4, Chapter 88, 加入僵盟, `chapter754.html`:

> 北原虽然面积广大，有八万多亿亩，是地球总面积的十倍还多。

This gives over eight trillion mu and says more than ten Earths. Under the modern conversion 1 mu = 1/1,500 km², eight trillion mu is about **5.333 billion km²**, with the source’s 多 indicating more.

Do not call 5 billion the exact source value. Historical/fantasy unit conversion is an editorial convention and should be fixed in the style sheet.

### G4. Circle arithmetic

**Verdict: definite diameter/radius error.**

If width means diameter:

- Diameter 50,000 km: π × 25,000² = **1.9635 billion km²**.
- Radius 50,000 km: π × 50,000² = **7.8540 billion km²**; diameter then equals 100,000 km.
- Diameter 50 million km: π × 25 million² = **1.9635 quadrillion km²**.

The document’s 2.5 quadrillion corresponds to squaring a 50-million-km side, not the circular area formula. Its large-region comparison and smaller replacement do not consistently use the same shape convention.

### G5. Five regions and two heavens totals

**Verdict: unestablished.**

The proposed 45-Earth and 105–120-Earth totals are not derived from a full set of sourced regional and heavenly surface areas. Treating heavens as additional comparable surfaces also requires a definition of what is being measured.

**Action:** remove these totals from confirmed lore. They may remain labelled worldbuilding-model estimates if the project deliberately develops one.

### G6. “Fifty suns”

**Verdict: not established as source text by this pass.**

No specific passage was located supporting the document’s alleged fifty-sun comparison. Absence of that comparison does not invalidate the independently located 亿里 wording. Keep these as separate claims.

---

## 5. Bronze Skin Gu

**Verdict: core distinction confirmed; no continuity repair needed on the evidence cited.**

- Volume 2, Chapter 102, `chapter309.html`, explicitly distinguishes temporary Revolution 2 skin defence from Revolution 3 self-consuming permanent enhancement.
- Volume 2, Chapter 155, `chapter362.html`, explicitly says 铜皮蛊 exists at Revolutions 1–3 and advances to 古铜皮蛊 at Revolution 4.
- The same chapter describes using molten copper to accelerate the latter’s tempering process.
- Volume 1, Chapter 62, `chapter70.html`, describes the instructor’s effect upon activation.

**Scope caution:** the quoted activation passage does not, by itself, establish the instructor’s cultivation revolution or the revolution of his individual Gu. Because the series spans multiple revolutions, those identities need their own support. Preserve “temporary activated effect” without smuggling in an unverified revolution assignment.

**Wording correction:** 铜汁 here is **molten copper**, not plant sap. The same passage says the process is 30% faster. That is not automatically a 30% reduction in duration: under a constant-rate model, time becomes 1/1.3 of the original, about 23.08% shorter.

**Counts:** a literal substring search for 铜皮蛊 in the extracted HTML text yields 31, but this includes 古铜皮蛊 and duplicated title text. Thus the document’s 24-mention claim cannot be compared fairly without knowing its body-only extraction and name-matching rules. Publish counting methods, not just totals.

---

## 6. Revolution 5 numbers and population

**Verdict: both quoted source statements are present; the proposed replacement population is not proved.**

- Volume 2, Chapter 138, `chapter345.html`: a little over a hundred Revolution 5s in Southern Border.
- Volume 3, Chapter 4, `chapter420.html`: only one or two Revolution 5s among a million people, in a discussion comparing the pyramidal distribution of Gu and Gu Masters.

The juxtaposition warrants review. But the document’s population of 56–64 billion is obtained by assigning modern Earth-like average population density to a fantasy region. The source does not provide that demographic premise.

The rarity sentence’s reference population and temporal meaning must also be established. A general rarity description is not automatically a census fraction of all living humans across every region and era.

Even accepting the assumed population, the calculated 56,000–128,000 does not yield the recommended 1,000–10,000. Those are different models.

**Action:** retain the quoted source numbers until the conflict is adequately demonstrated and a correction selected. “Known Revolution 5s” adds a limitation absent from the quoted text; use it only as an acknowledged editorial intervention, not a neutral translation.

The additional tables of immortals per region and the “one in 10,000 Revolution 5s” ascension figure remain unverified in this pass. They cannot be installed as settled numerical rules without supporting passages.

---

## 7. Jia Jin Sheng’s D-grade aptitude

**Verdict: keep D-grade; the central conclusion is confirmed.**

Volume 1, Chapters 45–46, `chapter53.html` and `chapter54.html`, explicitly give his D-grade aptitude and his hope that the inheritance might contain a rare aptitude-improving Gu.

The existence of a wealthy father and aptitude-raising methods does not automatically create a contradiction. Access, price, suitability, information, and requirements can differ.

However, the explanation “his righteous father would not use Blood Skull Gu” is not proved by the cited lines. The later novel’s existence of one such Gu does not show the father possessed it, could obtain it, or considered it.

**Action:** retain the character’s aptitude. Avoid inventing the father’s reasons when the source has not supplied them. Do not generalise the Revolution 1-to-2 four-day example into a guaranteed D-grade advancement schedule.

---

## 8. Battlefield killer moves within blessed lands

**Verdict: genuine continuity query, not yet a justified location rewrite.**

### Earlier rule with its omitted exception

Volume 4, Chapter 240, `chapter906.html`, describes Lang Ya’s fear of using battlefield killer moves inside a blessed land because temporary dao marks can conflict with the aperture’s marks.

But the very same surrounding passage explains that **Yu Lu Fairy overcame this disadvantage**, integrating her battlefield moves with the blessed land. It uses “the overwhelming majority” of immortals, not “all without exception”.

Volume 5, Chapter 33, `chapter1072.html`, adds another scope distinction: the danger discussed there concerns immortal battlefield moves; Fang Yuan’s mortal-level Night Curtain is harmless in that context.

### Later Yama test

Volume 5, Chapter 554, `chapter1594.html`, depicts the test inside Lang Ya’s setting. It begins with an improved defensive formation transporting Fang Yuan to a wilderness, and describes the formation’s silver light reducing damage from a soul explosion. He then tests Yama Battlefield and returns to the ordinary blessed-land environment when it ends.

The formation’s stated transport and defensive functions **do not prove dao-mark isolation**. It would be a mistake to declare that the passage already explains everything. Equally, the earlier rule is not an absolute impossibility.

**Action:** preserve the scene provisionally, mark a high-priority continuity query, and investigate Yama’s construction and compatible-environment exceptions. Do not add an invented isolation formation or relocate the test as though either repair were dictated by the source.

---

## 9. Fang Yuan’s century-long bottleneck

**Verdict: the audit’s negative finding is overturned by an explicit source statement.**

Volume 1, Chapter 105, 我会输得很惨, `chapter113.html`:

> 以他四成四的丙等资质，晋升三转，几乎不可能。前世方源卡在这儿上百年，最终机缘巧合，得到了一只提升资质的蛊虫，这才成了三转蛊师。

Close sense:

> With his 44% C-grade aptitude, advancing to Rank 3 was nearly impossible. In his previous life, he had been stuck at this bottleneck for over a hundred years. Only after a chance encounter brought him a Gu that raised his aptitude did he become a Rank 3 Gu Master.

The decisive search expression is **上百年**, not `100年`.

Volume 1, Chapter 148, `chapter156.html`, reinforces that conventional methods do not offer him a successful Revolution 2-to-3 route in his current situation; he therefore chooses a special Gu-based method.

**Action:** remove “may be translation memory”. Do not insert “without external aid” as the repair. The text identifies a specific eventual remedy: increased aptitude. Simply accumulating stones for four or five days is a different breakthrough episode and cannot replace this explanation.

This finding also limits broad claims that aptitude can always be overcome by ordinary resource expenditure alone.

---

## 10. Early killer moves

**Verdict: retaining early scenes is sensible; the proposed universal cost and small-scale rewrite policy are unsupported.**

### What the early text actually says

Volume 1, Chapter 185, `chapter193.html`, uses 杀招 for Tie Xue Leng’s upcoming technique. The term’s early use may not carry every later technical definition, but the document should not literally say there are no early killing moves.

The one-tenth essence cost cited in early chapters belongs to a **particular Moonlight Gu attack in that context**. It is not a universal price for activating every Gu. Different effects, revolutions, stages, durations, and passive or consumable mechanisms exist.

Volume 3, Chapter 136, `chapter552.html`, explicitly gives **fourteen Gu** for Four-Armed Earth King. This supports the point that combinations are manageable in some mortal contexts, but does not justify reducing every later combination to “a few” Gu.

### Counts are not explanations

Literal searches by EPUB filename range returned:

| EPUB files | DOCX count of 杀招 | This extraction’s count |
|---|---:|---:|
| 100–199 | 1 | 1 |
| 300–399 | 34 | 39 |
| 500–599 | 220 | 263 |
| 700–799 | 394 | 481 |
| 1700–1799 | 822 | 902 |

This extraction includes title text. Different chapter-range definitions and body-only processing can change totals. The increasing prevalence is clear, but these counts do not prove why a character lacked a technique, what inheritance he received, or what he could afford to activate.

**Action:** preserve each source technique’s actual components. Do not reduce the number of Gu to fit a newly imposed budget. Mark the First Generation’s alleged lack of core sect techniques as an unverified explanation unless directly sourced.

---

## 11. Gu Yue First Generation’s aptitude and cultivation

**Verdict: keep the stated facts; do not universalise the proposed explanation.**

Volume 1, Chapter 195, `chapter203.html`, explicitly has him contrast his C-grade aptitude with his fellow disciple’s A-grade aptitude. The surrounding narrative establishes his high cultivation and the Blood Skull Gu scheme.

That is not automatically an error. His existence demonstrates an exceptional trajectory within the story. It does not prove that every C-grade cultivator can reach Revolution 5 merely by purchasing enough ordinary stones.

It also matters that his later use of Blood Skull Gu cannot retroactively explain every earlier cultivation milestone without a chronology showing when each aptitude change occurred.

**Action:** preserve his stated aptitude, achievements, and grievance. Keep resources, unusual inheritance, special methods, and lifespan as possible relevant factors without presenting one unquoted formula as the complete explanation.

---

## 12. Xiong Jiao Man

**Verdict: confirmed for this EPUB. No repair needed.**

- Volume 1, Chapter 189, `chapter197.html`: explicit beheading of 熊骄嫚 by Bai Ning Bing.
- Volume 1, Chapter 193, `chapter201.html`: Gu Yue Yao Ji steps forward to help.
- Volume 1, Chapter 194, `chapter202.html`: Gu Yue Yao Ji is outside the barrier and among those killed.

A full exact-name search of the extracted HTML returns **49 occurrences in nine documents**, ending in `chapter197.html`. The DOCX says 47. The qualitative conclusion is unchanged; the numeric count needs a reproducible method or a specified differing snapshot.

Searching `chapter189.html` and `chapter194.html` is not checking narrative Chapters 189 and 194. The original audit confuses those systems in part of its argument. Replace that explanation with the actual printed chapter/file mapping above.

**Action:** keep the single death and Yao Ji’s later role. Do not change the first death into a near-decapitation in this base edition. Do not state that the editor who fixed the other edition has been identified; that provenance remains unknown.

---

## 13. A new high-confidence error candidate in the base text

Volume 1, Chapter 22, `chapter30.html`, includes a student saying:

> 我只是丙等修为，空窍中能存储三成八的青铜真元。

The sentence combines a C-grade label with **38%**, whereas the same base text’s explicit C-grade range starts at 40%. “修为” also sits awkwardly where aptitude is being discussed.

This is a much stronger local mismatch than inferring a population from land area. Candidate repairs include changing the grade label to D, or checking whether the 38% value is the corrupted element. The student’s wider identity and other editions should be checked before choosing between them.

**Status:** high-confidence inconsistency; exact repair not yet approved. This independently disproves any blanket assurance that the base edition contains no textual errors.

---

## 14. Implementation decision sheet

| Proposal | Recommendation |
|---|---|
| Keep familiar aptitude bands | Keep; improve citations and specify integer-resolution convention. |
| Install exact recovery = 10% of aptitude/hour | Hold. Not established by the cited examples. |
| Treat Liquor Worm’s total 4:1 cost as potency | Reject inference. Separate process cost and output properties. |
| Replace 10,000 with 6,400 throughout | Reject blanket edit. Source explicitly supports 10,000 in immortal-essence accounting. |
| Keep 55% ordinary Revolution 1-to-2 threshold | Keep with source qualifications. |
| Add 65/75/85% higher thresholds | Hold pending direct evidence. |
| Keep Fang Yuan’s multi-day stone-assisted Revolution 2 breakthrough | Keep; preserve the skill and endurance requirements. |
| Explain B-grade timing through eight small transitions | Correct arithmetic and remove unsupported year allocation. |
| Replace Central Continent extent with 50,000 km | Do not apply as a translation fix; optional adaptation only after wider review. |
| Install exact total world area | Hold. Insufficient sourced dimensions. |
| Raise regional Revolution 5 counts to 1,000–10,000 | Hold. Population assumptions and replacement range are unproved. |
| Keep Bronze Skin revolution-dependent distinction | Keep. Verify instructor-specific revolution separately. |
| Keep Jia Jin Sheng D-grade | Keep; do not invent father’s motives. |
| Move Yama test outside Lang Ya | Hold. Genuine query, not a uniquely determined correction. |
| Add “without external aid” to century bottleneck | Reject proposed repair. Translate the located aptitude-raising-Gu explanation. |
| Reduce later mortal killer moves to a few Gu | Reject blanket change. Follow each source construction. |
| Keep First Generation’s stated aptitude and cultivation | Keep; avoid a universal ordinary-resource guarantee. |
| Keep Xiong Jiao Man’s single death | Keep. Correct narrative chapter references. |
| Resolve Chapter 22 C-grade/38% mismatch | Investigate alternate readings; do not silently choose a repair yet. |

## Recommended editorial standard

A correction should be applied directly in prose only after its internal record states:

1. The exact source edition and location.
2. What is actually inconsistent.
3. Whether the problem is textual, mathematical, interpretive, or edition-dependent.
4. The competing candidate repairs.
5. Why the chosen repair is the least speculative.
6. Downstream passages affected.
7. The Omniarch’s approval.

A clean reading experience and an honest editorial record are compatible. Readers need not encounter a footnote every paragraph, but the project should never have to reconstruct later whether a figure came from the author, the base editor, the translator, or the reviewer.

**Bottom line:** preserve the sound source-based decisions, withdraw the two failed negative-search claims, and keep proposed world-model changes out of settled canon until their assumptions and consequences have been tested.
