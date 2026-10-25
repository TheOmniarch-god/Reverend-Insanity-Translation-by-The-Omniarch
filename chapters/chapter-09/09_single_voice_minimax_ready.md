# Chapter 9 — P41 to P77 — Single Voice MiniMax Ready

> **Paste into:** https://www.minimax.io/audio/text-to-speech
> **Model:** `speech-2.8-hd` or `speech-2.8-turbo`
> **Voice:** One voice only (e.g. Wise_Woman, Calm Male, etc)
> **Emotion param:** Your screenshot shows UI has `Happy, Sad, Angry, Fearful, Disgusted, Surprised, Neutral, Fluent` — **no Calm button**. API docs list `calm` as enum, but web UI uses **Neutral** for calm/serene. Use **Neutral** for narration base.
> **Tags supported natively:** `(chuckle) (sighs) (breath) (inhale) (exhale) (gasps)` + pause `<#0.5#>`

---

### How to use (matches your screenshot)

1. Select **one voice**
2. Set base emotion to **Neutral** — this is your Calm/serene in this UI
3. Paste the block below — it's ~3.5k chars, under 5k limit
4. **Highlight** text to set per-line emotion as you showed in screenshot:
   - Granny Shen / Shen Cui coquettish → `Happy`
   - Storm / cold wind / gloom → `Fearful`
   - Fang Yuan cold sneer → `Disgusted`
   - Warm tea room → `Happy`
   - Narration → leave as `Neutral` (or `Fluent` for clean broadcast style)
5. Click Generate

---

### Full Script — Ready to Copy

```text
A dense night descended, <#0.5#> the stars, mostly veiled by drifting clouds, filling the sky. <#0.8#> In the stockade, household after household gradually lit their lamps. (exhale)

Gu Yue Fang Zheng was led into a room. <#0.6#>

Young Master Fang Zheng, <#0.3#> this room was specially tidied and vacated by this old servant upon Master's personal instruction. (chuckle)

Granny Shen introduced it obsequiously, stooping, her face wreathed with flattering smiles. <#0.6#>

Fang Zheng looked round, his eyes brightening. This room was more than twice as large as his former room. At its centre was a broad bed; by the window, a desk of sandalwood set with a fine brush, ink, paper and inkstone; the surrounding walls hung with exquisite ornaments. Even beneath his feet was not ordinary flooring, but a layer of soft, hand-made carpet. <#0.8#>

From childhood to now, Fang Zheng had never lived in such a room. At once he nodded repeatedly. (breath) This is very good, really quite fine. Thank you, Granny Shen. <#0.8#>

This Granny Shen was Aunt's most trusted person, managing all the servants in the household, a housekeeper in all but name. Fang Yuan's personal maid Shen Cui was her daughter. <#0.6#>

How could this old servant dare accept young master's thanks, it is as it should be, as it should be. (chuckle) Young master need only eat well and sleep well, if you want anything, shake the bell by the bedside, a servant will come up at once to await your orders. Master has instructed that in these days young master should devote himself wholly to cultivation; other trifling matters should be left to us servants to handle. (exhale) <#0.8#>

A fresh surge of gratitude rose in Fang Zheng's heart. He said nothing more, only silently resolved within himself: I must seize first place, and not disappoint Uncle and Aunt! (inhale) <#1.0#>

The clouds above thickened, and with them the night deepened. The stars were all but veiled, save for a few that still glimmered faintly, struggling against the darkness. (breath) <#1.0#>

Uncle and Aunt should be plotting how to expel me from the household. In the previous life they secretly instigated servants to provoke me, then framed me, and in the end expelled me. I wonder what change there will be in this life. (chuckle) <#0.8#>

As for the true colours of Uncle and Aunt, he had seen through them long ago. Yet it could be understood. <#0.6#>

Man dies for wealth as birds die for food, whether on Earth or in this world, there are always those who trample upon kinship, friendship and love for the sake of benefit. (sighs) In truth, there was no kinship at all. Uncle and Aunt had taken the brothers in for no other reason than coveting the inheritance. Only the two brothers had repeatedly surprised them. <#0.8#>

All things are difficult at the beginning, and for me doubly so. I possess neither outstanding aptitude nor the guidance of any elder. In truth, I am starting from scratch. My parents' inheritance may yet serve as a great springboard. In the previous life, Uncle and Aunt seized that inheritance, and for that loss I squandered two whole years before I could cultivate to the peak of the First Revolution. In this life, that error shall not be repeated. (exhale) <#1.0#>

The night sky grew ever more overcast, dark clouds veiling starlight, the mountain wind whistling with a rising howl, ever stronger. (inhale) Mountain rain was about to break. <#0.8#>

Still, he must explore. His parents' inheritance could only be reclaimed when he is sixteen next year, while Flower-Wine Monk's treasure was something that might be obtained in the near term. (breath) <#0.8#>

In the street, few folk were about. From houses by the roadside, dim light shone; some household refuse, leaves, and dust rolled along, blown by the wind, drifting aimlessly. (exhale) <#0.6#>

Fang Yuan's thin clothes could scarcely hold back this mountain wind. He could not help but feel a chill. (inhale) He simply opened one of the jars he carried and took a small sip. Though it was turbid wine, once swallowed, warmth rose within him. (exhale) (sighs) This was the first time in all these days that he had truly drunk at all. <#0.8#>

The further from the stockade, the sparser the houses by the road, the dimmer the lights. Ahead, gloom lay thicker. Wind pressed upon the mountain forest, branches swaying in the night, whistling as though beasts roared. (breath) <#0.8#>

Fang Yuan's steps did not falter. He passed beyond the stockade gate and went on, his figure receding further and further into the dark road. Behind him lay the myriad lights of home, bright and glorious. Amid those lights there was a warm corner. <#0.8#>

There, Fang Zheng sat at his desk, reviewing the notes taken in class. The room was bright with lamplight, solid walls keeping out the cold wind, and at his hand stood a cup of warm ginseng tea, steam curling and rising. (breath) <#0.8#>

Young Master Fang Zheng, the hot water for your bath is ready, came Shen Cui's voice softly from outside the door. <#0.5#>

Then bring it in. <#0.5#>

Shen Cui entered, sashaying as she came, her face full of coquettish charm. (chuckle) This servant pays respects to Young Master Fang Zheng. (breath) She gazed upon Fang Zheng with amorous eyes, thinking: "Fang Yuan is only Grade C, but Fang Zheng is of Grade A aptitude. To latch onto him, that would be truly great fortune!" (chuckle)
```

---

### Split by Emotion (if you call API with one voice but varying emotion) — mapped to YOUR UI

| Part | Emotion in YOUR UI | Original intent | Text Start |
|------|-------------------|-----------------|------------|
| P41-P44 | `Neutral` | calm serene | A dense night descended... |
| P45-P48 | `Happy` | warm obsequious | Young Master Fang Zheng, this room... |
| P49-P52 | `Happy` | gratitude/excited | A fresh surge of gratitude... |
| P53-P65 | `Disgusted` + `Neutral` | cold sneer + deadpan | Uncle and Aunt should be plotting... |
| P66-P73 | `Fearful` → `Neutral` | tense storm → calm resolve | The night sky grew ever more overcast... |
| P74-P77 | `Happy` | coquettish | Young Master Fang Zheng, the hot water... |

Use same `voice_id` for all, just change `emotion` param per block. API also accepts `calm`, but your web UI shows `Neutral` — they are equivalent for serene narration.

---

### Our plain TTS preview (same voice, no tags spoken)

Generated with `voice-01` (masculine narrator):

- `audio/ch9_single_voice_part1_clean.mp3`
- `audio/ch9_single_voice_part2_clean.mp3`
- `audio/ch9_single_voice_part3_clean.mp3`
- `audio/ch9_single_voice_part4_clean.mp3`
- `audio/ch9_single_voice_part5_clean.mp3`

These are clean (no parentheses) so our player doesn't speak `(chuckle)` literally. For MiniMax, use the tagged version above — MiniMax will render them as actual chuckles/breaths.
