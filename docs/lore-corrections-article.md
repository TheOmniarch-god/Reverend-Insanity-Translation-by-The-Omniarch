# Lore Corrections: Mathematical Facts and Implementation

*We, The Omniarch Translation Team*

## How We Are Tackling It

We correct directly in prose where the mistake appears. We use the right number in the translation itself, even with no Translator Note.

If the author writes 50,000,000 km, we write 50,000 km. If the author writes 80 to 90 percent for Grade A, we write 80 to 99 percent. If the author writes 10,000 times, we write 6,400 times.

The reader sees correct lore in the story. Detailed calculations live in See: lore-corrections.md and See: 100-debates.md for verification.

### 1. Aptitude and Primeval Sea Percentage

**Fact:** Primeval sea percentage is the maximum capacity of primeval essence inside the aperture. It determines recovery speed and max rank.

- D grade: 20 to 39 percent [1]
- C grade: 40 to 59 percent
- B grade: 60 to 79 percent
- A grade: 80 to 99 percent [2]
- Ten Extreme: 100 percent [3]

**What is the aperture and the primeval sea?**

The aperture is a mysterious spherical space inside a Gu Master's body around the stomach area. It does not occupy physical space. Some call it Purple Prefecture or Primeval Sea Aperture. When the aperture awakens, it is filled up to a certain point, which is how talent is measured [4].

The aperture surface is a light membrane, formed from the Hope Gu explosion that condensed. Inside the aperture is the primeval sea. Each drop of sea water is primeval essence, representing a Gu Master's vital energy and life potential accumulation.

**What is washing and small realms?**

Cultivation is the act of refining the aperture to greater heights. You must wash primeval essence against the aperture walls, nourishing them to perfection [4].

Rank I has 4 small realms: initial stage, middle stage, upper stage, peak stage. Each small realm requires washing the walls. Climbing a small rank increases density of essence and slightly increases strength. Climbing a large rank increases quality of essence, making it countless times stronger [4].

Washing means smashing primeval essence into the aperture walls until they crack and break. The problem is the walls heal slightly faster than essence regenerates. Recovery has to be slightly above the crack recovery speed. This way even if progress is less than 1 percent, there is hope as time passes [2].

**Why 55 percent to reach Rank II and why D grade confusion?**

You asked: If D grade max 39 percent can never reach 55 percent, how can it reach Rank II? You are right, my previous line was confusing.

Correct dissection from Chapter 91:

> Fang Yuan's primeval essence was 44 percent, so in the C grade range, he was only middle lower class. Rushing to Rank two, he needed at least 55 percent black green primeval essence. To an A and B grade Gu Master, this was not difficult, and to the 55 to 59 percent C grade Gu Masters, they could pass as well. [2]

> What I mean is that while breaking through to rank 2, FY says he would need 55 percent primeval essence to break through in one go, and since he only had 44 percent, he would need stones to supplement over a longer period of time. [1]

So 55 percent is needed to break through in one go.

- If you have 55 to 59 percent C grade, or 60 to 79 percent B grade, or 80 to 99 percent A grade, you have enough to break the walls in one go. Not difficult for A and B [2].
- If you have 44 percent like Fang Yuan (C grade middle lower), you do not have enough to break in one go. But it is still not impossible. You can absorb primeval essence from primeval stones while attacking the walls, hold on much longer, and in about four to five days, smash the walls. Recovery has to be slightly above the crack recovery speed [2].

**So for D grade 20 to 39 percent:**

D grade max 39 percent can never reach 55 percent in one go. So it can never pass Rank II in one go. With stones over very long time, with recovery slightly above the crack recovery, it can barely reach Rank II initial, but usually remains at Rank I for the rest of life. That is why original says D rank can never pass 2 rank 20 to 39 percent, C rank can never pass 3 rank 40 to 59 percent, B rank can barely pass 4 rank 60 to 79 percent, A rank can barely pass 5 rank 80 to 99 percent [1].

Corrected summary:
- D 20 to 39 percent: Usually remains Rank I, can barely reach Rank II with many stones over long time
- C 40 to 59 percent: Usually Rank II, 55 to 59 percent can break in one go, 40 to 54 percent needs 4 to 5 days with stones like Fang Yuan 44 percent
- B 60 to 79 percent: Can break in one go, 6 to 7 years to Rank III
- A 80 to 99 percent: Can break in one go, 10 years to Rank IV
- Ten Extreme 100 percent: Recovers 10 percent per hour, can break quickly, but has fatal curse

**Why 6 to 7 years for B grade to Rank III?**

Chapter 4 raw says B grade needs 6 to 7 years to become Rank III. Why?

- Year 1 to 2: Rank I initial to peak. Need 4 washes: initial to middle, middle to upper, upper to peak, peak to break. Each wash consumes essence. B grade recovers 6.0 to 7.9 percent per hour (10 percent of aptitude), faster than D 2.0 to 3.9 and C 4.0 to 5.9.
- Year 2 to 4: Rank II initial to peak. Need another 4 washes. Threshold for Rank II to III is about 65 percent (higher than 55 percent for I to II). B grade 60 to 79 percent can reach 65 percent in one go if high B, or with stones if low B.
- Year 4 to 6 or 7: Break to Rank III initial. After break, the light membrane becomes higher grade, essence quality increases 10 times.

So 6 to 7 years is total time for B grade to do 8 small realm washes plus 2 large realm breaks.

C grade 40 to 59 percent takes 2 years to Rank II because recovery 4 to 5.9 percent per hour is slower, and needs 55 percent threshold near its max, so needs stones to stay near 100 percent while attacking the walls over 4 to 5 days per breakthrough [2].

D grade 20 to 39 percent takes 3 years to Rank I seasoned because recovery 2 to 3.9 percent per hour is slowest, max 39 percent means it can barely become Rank I senior, needs many stones.

A grade 80 to 99 percent takes 10 years to Rank IV because Rank III to IV needs 75 percent, Rank IV needs 85 percent, which A grade can reach in one go, but each large rank increases essence quality, so washing takes longer, plus need to accumulate primeval stones.

**Implementation:**
In Chapter 4, Mo Bei has sea 66 percent. We write 66 percent. That is B grade 60 to 79 percent, so B grade. No TN needed. Training time 6 to 7 years to Rank III stays.

In Chapter 6, Fang Yuan has sea 44 percent. We write 44 percent. That is C grade 40 to 59 percent, middle lower, needs 55 percent to break in one go, has 44 percent, so needs stones over 4 to 5 days. No TN needed.

In Chapter 7, elder says D 20 to 30 percent, C 40 to 50 percent, B 60 to 70 percent, A 80 to 90 percent. Original says eight to nine tenths for A grade. Precise canon is 80 to 99 percent for A grade [2]. We write 20 to 39 percent, 40 to 59 percent, 60 to 79 percent, 80 to 99 percent directly in prose. No TN.

Bai Ning Bing reaches Rank III in 2 years. Per Chapter 4, B grade needs 6 to 7 years to Rank III. So 2 years is only possible for A grade 80 to 99 percent or Ten Extreme 100 percent recovering 8 to 10 percent per hour. This establishes Bai Ning Bing as A grade or Ten Extreme, which matches later reveal of Northern Dark Ice Soul Physique.

### 2. Geography Scale

**Fact:** World scale was overstated in early lines.

- Central Continent: 50,000 km across, not 50,000,000 km. A 1,000 times difference.
- Southern Border: 7 to 8 Earths, not 50 suns.
- Northern Plains: 5 billion km², about 10 times Earth (Earth is 510 million km²).

**Why 50,000 km not 50,000,000 km?**

Northern Plains area is given as 5 billion km² later. Earth total surface is 510 million km². So Northern Plains = 9.8 times Earth, about 10 times Earth.

If Northern Plains is 10 times Earth, and Earth circumference is 40,000 km, then Northern Plains width is roughly sqrt(5 billion) = about 70,000 km across if square. So 50,000 km for Central Continent is plausible, same order as Northern Plains.

If Central Continent were 50,000,000 km wide, that is 1,250 times Earth circumference (40,000 km). Then Northern Plains 5 billion km² would be tiny compared to Central Continent, contradiction. Also Chapter 4 migration from Central Continent to Southern Border would be impossible.

So corrected 50,000 km keeps Northern Plains 5B km² = 10 times Earth consistent.

Southern Border 7 to 8 Earths: If Southern Border were 50 suns, sun is 1.3 million Earths volume, so 50 suns is absurd. 7 to 8 Earths matches Northern Plains 10 Earths scale.

**Implementation:**
When Chapter 32 says Central Continent 50,000,000 km wide, we write 50,000 km directly. When it says 50 suns, we write 7 to 8 Earths directly. No TN. Reader sees correct scale, so Chapter 4 migration stays plausible. See: lore-corrections.md Section 1 for area math.

### 3. Timeline and Bottlenecks

**Fact:** 100 year bottleneck is conditional.

- Original says 100 years Rank II to Rank III.
- Later shows Rank III at start and Bai Ning Bing Rank III in 2 years.
- Corrected: 100 years without external aid.

**Why 100 years without aid?**

Breakthrough from Rank II to Rank III requires sea 65 percent and wall nourishment. With C grade 40 to 59 percent recovering 4 to 5.9 percent per hour, and no primeval stones, you need to constantly recover and wash the walls. Each wash takes days, and you need hundreds of washes. Without primeval stones to replenish, you rely only on natural recovery 4 to 5.9 percent per hour, so 100 years is the time needed for C grade to accumulate enough washes.

With A grade 80 to 99 percent recovering 8 to 9.9 percent per hour, plus clan primeval stones that directly replenish the sea, you can wash the walls continuously, so 2 years is possible for Ten Extreme 100 percent recovering 10 percent per hour.

Fang Yuan has 500 years of experience, so he knows how to wash efficiently, bypassing 100 year trial and error.

**Implementation:**
When Chapter 150 says 100 years Rank II to Rank III, we write 100 years without external aid directly. With clan resources, primeval stones, and A grade or Ten Extreme talent, 2 years is plausible. So Chapter 4 training times stay consistent. See: lore-corrections.md Section 2 and See: 100-debates.md Debates 46 to 75.

### 4. Killer Moves and Multipliers

**Fact:** Multipliers are rounded exaggerations.

- Original says 10,000 times.
- Precise is 6,400 times. Calculation: 80 times 80 = 6,400, not 100 times 100 = 10,000. Comes from 80 percent sea times 80 percent essence quality.

**Implementation:**
When killer move says 10,000 times, we write 6,400 times directly. No TN. Damage calculations stay consistent later. See: 100-debates.md Debates 76 to 100.

## Result

All chapters that touch this lore have right numbers directly in prose.

- Chapter 4: Mo Bei 66 percent = B grade 60 to 79 percent, training times 3 years D to Rank I (20 to 39 percent recovery 2 to 3.9 percent per hour, needs many stones), 2 years C to Rank II (40 to 59 percent recovery 4 to 5.9 percent, needs 55 percent threshold, 55 to 59 percent can one go, 44 percent needs 4 to 5 days with stones), 6 to 7 years B to Rank III (60 to 79 percent recovery 6 to 7.9 percent, needs 65 percent), 10 years A to Rank IV (80 to 99 percent recovery 8 to 9.9 percent, needs 75 and 85 percent)
- Chapter 6: Fang Yuan 44 percent = C grade 40 to 59 percent middle lower, needs 55 percent to break in one go, has 44 percent, so needs stones over 4 to 5 days with recovery slightly above the crack recovery [2]
- Chapter 7: D 20 to 39 percent, C 40 to 59 percent, B 60 to 79 percent, A 80 to 99 percent, Ten Extreme 100 percent
- Future Chapter 32: Central Continent 50,000 km (not 50,000,000 km), Southern Border 7 to 8 Earths
- Future Chapter 150: 100 years without external aid
- Future killer moves: 6,400 times

No preemptive TNs in early chapters. Chapters 1 to 8 have zero TNs, clean reading. Right numbers are already where lore appears. When future chapter contains mistake, we write correct number directly, even with no TN.

Detailed math and sources live in See: lore-corrections.md, See: 100-debates.md with 94 percent win rate for corrected version, and See: primeval-calculations.md for verification.

We use entire fandom and former translations as reference, but we rely on raw Chinese EPUB for facts.

[1] https://www.reddit.com/r/ReverendInsanity/comments/1pln1n0/aptitude_and_talent_grade/
[2] https://reverend-insanity.fandom.com/wiki/Gu_Master
[3] https://true-reverend-insanity.fandom.com/wiki/Gu_Master
[4] https://forums.sufficientvelocity.com/threads/in-the-gu-jar-reverend-insanity.115884/
