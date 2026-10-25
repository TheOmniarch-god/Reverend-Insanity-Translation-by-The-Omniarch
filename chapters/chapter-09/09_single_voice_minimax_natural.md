# Chapter 9 — P41 to P77 — Single Voice — NATURAL breathing (fixed)

> **Issue you reported:** `(inhale)` and `(exhale)` sound unnatural / too heavy on MiniMax
> **Fix:** Use only `(breath)` and `(sighs)` + `(chuckle)` + pauses `<#0.5#>`
> **Why:** `(breath)` = subtle natural inhale, `(sighs)` = soft exhale, `(inhale)/(exhale)` = pronounced heavy breathing — unnatural for narration
> **Voice:** One voice only | **Emotion:** Base `Neutral` (your UI), per-line `Happy / Fearful / Disgusted` via highlight

---

### Copy-ready script — NATURAL version

```text
A dense night descended, <#0.5#> the stars, mostly veiled by drifting clouds, filling the sky. <#0.8#> In the stockade, household after household gradually lit their lamps. <#0.8#>

Gu Yue Fang Zheng was led into a room. <#0.6#>

Young Master Fang Zheng, <#0.3#> this room was specially tidied and vacated by this old servant upon Master's personal instruction. (chuckle) <#0.8#>

Granny Shen introduced it obsequiously, stooping, her face wreathed with flattering smiles. <#0.6#>

Fang Zheng looked round, his eyes brightening. This room was more than twice as large as his former room. At its centre was a broad bed; by the window, a desk of sandalwood set with a fine brush, ink, paper and inkstone; the surrounding walls hung with exquisite ornaments. Even beneath his feet was not ordinary flooring, but a layer of soft, hand-made carpet. <#0.8#>

From childhood to now, Fang Zheng had never lived in such a room. At once he nodded repeatedly. (breath) This is very good, really quite fine. Thank you, Granny Shen. <#0.8#>

This Granny Shen was Aunt's most trusted person, managing all the servants in the household, a housekeeper in all but name. Fang Yuan's personal maid Shen Cui was her daughter. <#0.6#>

How could this old servant dare accept young master's thanks, it is as it should be, as it should be. (chuckle) Young master need only eat well and sleep well, if you want anything, shake the bell by the bedside, a servant will come up at once to await your orders. Master has instructed that in these days young master should devote himself wholly to cultivation; other trifling matters should be left to us servants to handle. <#0.8#>

A fresh surge of gratitude rose in Fang Zheng's heart. He said nothing more, only silently resolved within himself: I must seize first place, and not disappoint Uncle and Aunt! <#1.0#>

The clouds above thickened, and with them the night deepened. The stars were all but veiled, save for a few that still glimmered faintly, struggling against the darkness. <#1.0#>

Uncle and Aunt should be plotting how to expel me from the household. In the previous life they secretly instigated servants to provoke me, then framed me, and in the end expelled me. I wonder what change there will be in this life. (chuckle) <#0.8#>

As for the true colours of Uncle and Aunt, he had seen through them long ago. Yet it could be understood. <#0.6#>

Man dies for wealth as birds die for food, whether on Earth or in this world, there are always those who trample upon kinship, friendship and love for the sake of benefit. (sighs) In truth, there was no kinship at all. Uncle and Aunt had taken the brothers in for no other reason than coveting the inheritance. Only the two brothers had repeatedly surprised them. <#0.8#>

All things are difficult at the beginning, and for me doubly so. I possess neither outstanding aptitude nor the guidance of any elder. In truth, I am starting from scratch. My parents' inheritance may yet serve as a great springboard. In the previous life, Uncle and Aunt seized that inheritance, and for that loss I squandered two whole years before I could cultivate to the peak of the First Revolution. In this life, that error shall not be repeated. <#1.0#>

The night sky grew ever more overcast, dark clouds veiling starlight, the mountain wind whistling with a rising howl, ever stronger. Mountain rain was about to break. <#0.8#>

Still, he must explore. His parents' inheritance could only be reclaimed when he is sixteen next year, while Flower-Wine Monk's treasure was something that might be obtained in the near term. <#0.8#>

In the street, few folk were about. From houses by the roadside, dim light shone; some household refuse, leaves, and dust rolled along, blown by the wind, drifting aimlessly. <#0.6#>

Fang Yuan's thin clothes could scarcely hold back this mountain wind. He could not help but feel a chill. (breath) He simply opened one of the jars he carried and took a small sip. Though it was turbid wine, once swallowed, warmth rose within him. (sighs) This was the first time in all these days that he had truly drunk at all. <#0.8#>

The further from the stockade, the sparser the houses by the road, the dimmer the lights. Ahead, gloom lay thicker. Wind pressed upon the mountain forest, branches swaying in the night, whistling as though beasts roared. <#0.8#>

Fang Yuan's steps did not falter. He passed beyond the stockade gate and went on, his figure receding further and further into the dark road. Behind him lay the myriad lights of home, bright and glorious. Amid those lights there was a warm corner. <#0.8#>

There, Fang Zheng sat at his desk, reviewing the notes taken in class. The room was bright with lamplight, solid walls keeping out the cold wind, and at his hand stood a cup of warm ginseng tea, steam curling and rising. <#0.8#>

Young Master Fang Zheng, the hot water for your bath is ready, came Shen Cui's voice softly from outside the door. <#0.5#>

Then bring it in. <#0.5#>

Shen Cui entered, sashaying as she came, her face full of coquettish charm. (chuckle) This servant pays respects to Young Master Fang Zheng. (breath) She gazed upon Fang Zheng with amorous eyes, thinking: "Fang Yuan is only Grade C, but Fang Zheng is of Grade A aptitude. To latch onto him, that would be truly great fortune!" (chuckle)
```

---

### What changed vs previous

| Before (unnatural) | After (natural) | Reason |
|---|---|---|
| `(exhale)` after lamps | removed, just `<#0.8#>` pause | No need to breathe after narration |
| `(inhale)` before rain | removed | Heavy inhale sounds forced |
| `(exhale) (sighs)` stacked | `(sighs)` alone | Stacked tags sound robotic |
| `(breath) (chuckle)` etc kept | kept | `(breath)` = subtle, `(chuckle)` = light, natural |
| All `(inhale)` `(exhale)` | deleted | Use only where character actually breathes from cold/wine |

**Rule of thumb for MiniMax natural:**
- Use `(breath)` max 1 per 3-4 sentences, not every sentence
- Use `(sighs)` only for Fang Yuan's philosophical lines
- Use `(chuckle)` only for Granny Shen / Shen Cui obsequious / coquettish
- Use `<#0.5#>` / `<#0.8#>` for rhythm instead of breathing tags
- Avoid `(inhale)` `(exhale)` `(pant)` `(gasps)` unless scene is exertion/fear

This version should sound much more natural in your UI.

---

### Emotion mapping for this natural version (your UI)

- Narration: `Neutral`
- Granny Shen / Shen Cui: highlight → `Happy`
- Storm / gloom / cold: highlight → `Fearful`
- Fang Yuan sneer / internal: highlight → `Disgusted`
- Warm tea room: highlight → `Happy`
