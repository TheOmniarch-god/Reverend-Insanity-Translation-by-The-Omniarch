# Chapter 9 P41-P77 — MiniMax OFFICIAL Format (per https://www.minimax.io/audio/text-to-speech + API docs)
# Verified emotion enums from Cloudflare + MiniMax Platform docs:
# emotion = happy, sad, angry, fearful, disgusted, surprised, calm, fluent, neutral, whisper, auto
# - calm DOES exist per https://developers.cloudflare.com/ai/models/minimax/speech-2.8-hd/ and https://platform.minimax.io/docs/guides/mcp-guide
# - Some UIs list neutral instead of calm, but API accepts calm. Use calm for serene narration.
# Sound tags (parentheses, preset only, supported only on speech-2.8-hd / speech-2.8-turbo):
# (laughs) (chuckle) (coughs) (clear-throat) (groans) (breath) (pant) (inhale) (exhale) (gasps) (sniffs) (sighs) (snorts) (burps) (lip-smacking) (humming) (hissing) (emm) (sneezes) (crying) (applause) (yawns) (whistles)
# Pause tags: <#0.5#> = 0.5s silence, range 0.01-99.99
# Do NOT use bracket tags like [calm] in native MiniMax — those are Morphic wrapper only. Use emotion parameter.

## Block 1 — Narration opening — emotion: calm
Text for T2A:
A dense night descended, <#0.5#> the stars, mostly veiled by drifting clouds, filling the sky. <#0.8#> In the stockade, household after household gradually lit their lamps. (exhale)
→ API: model=speech-2.8-hd, emotion=calm, voice_id=Wise_Woman or similar British female calm

## Block 2 — Transition
Text:
Gu Yue Fang Zheng was led into a room. <#0.6#>
→ emotion=calm

## Block 3 — Granny Shen — obsequious fawning — emotion: happy (warm cheerful, but API has happy)
Text:
Young Master Fang Zheng, <#0.3#> this room was specially tidied and vacated by this old servant upon Master's personal instruction. (chuckle)
→ emotion=happy (obsequious cheerful), include (chuckle) sound tag

Narration tag after:
Granny Shen introduced it obsequiously, stooping, her face wreathed with flattering smiles.
→ emotion=calm

## Block 4 — Fang Zheng brightening — emotion: happy
Text:
Fang Zheng looked round, his eyes brightening. <#0.4#> This room was more than twice as large as his former room. At its centre was a broad bed; by the window, a desk of sandalwood set with a fine brush, ink, paper and inkstone; the surrounding walls hung with exquisite ornaments. Even beneath his feet was not ordinary flooring, but a layer of soft, hand-made carpet.
→ emotion=happy

Text:
From childhood to now, Fang Zheng had never lived in such a room. At once he nodded repeatedly. (breath) This is very good, really quite fine. <#0.4#> Thank you, Granny Shen.
→ emotion=happy, (breath) before thanks

## Block 5 — Housekeeper context — emotion: calm
Text:
This Granny Shen was Aunt's most trusted person, managing all the servants in the household, a housekeeper in all but name. <#0.5#> Fang Yuan's personal maid Shen Cui was her daughter.
→ emotion=calm

## Block 6 — Granny Shen chuckle — emotion: happy
Text:
Granny Shen chuckled. (chuckle) How could this old servant dare accept young master's thanks, <#0.3#> it is as it should be, as it should be. <#0.6#> Young master need only eat well and sleep well, <#0.3#> if you want anything, shake the bell by the bedside, <#0.3#> a servant will come up at once to await your orders. <#0.6#> Master has instructed that in these days young master should devote himself wholly to cultivation; <#0.4#> other trifling matters should be left to us servants to handle. (exhale)
→ emotion=happy (warm reassuring), sound tags (chuckle) (exhale)

## Block 7 — Fang Zheng resolve — emotion: excited / happy
Text:
A fresh surge of gratitude rose in Fang Zheng's heart. He said nothing more, only silently resolved within himself: <#0.8#> I must seize first place, and not disappoint Uncle and Aunt! (inhale)
→ emotion=happy for gratitude, then switch to excited for resolve line

## Block 8 — Clouds thicken — emotion: fearful (tense atmosphere)
Text:
The clouds above thickened, and with them the night deepened. <#0.6#> The stars were all but veiled, save for a few that still glimmered faintly, struggling against the darkness. (breath) <#1.0#>
→ emotion=fearful (or calm with tense prosody), (breath)

## Block 9 — Fang Yuan internal — emotion: disgusted / angry (cold sneer)
Text:
Uncle and Aunt should be plotting how to expel me from the household. <#0.5#> In the previous life they secretly instigated servants to provoke me, then framed me, and in the end expelled me. <#0.6#> I wonder what change there will be in this life. (chuckle)
→ emotion=disgusted or angry, (chuckle) cold

Text:
As for the true colours of Uncle and Aunt, he had seen through them long ago. <#0.6#>
→ emotion=calm (deadpan)

Text:
Yet it could be understood. <#0.8#>
→ emotion=neutral

Text:
Man dies for wealth as birds die for food, <#0.4#> whether on Earth or in this world, there are always those who trample upon kinship, friendship and love for the sake of benefit. (sighs)
→ emotion=sad, (sighs)

Text:
In truth, there was no kinship at all. Uncle and Aunt had taken the brothers in for no other reason than coveting the inheritance. <#0.5#> Only the two brothers had repeatedly surprised them.
→ emotion=neutral / calm

Text:
All things are difficult at the beginning, and for me doubly so. <#0.4#> I possess neither outstanding aptitude nor the guidance of any elder. <#0.4#> In truth, I am starting from scratch. <#0.6#> My parents' inheritance may yet serve as a great springboard. <#0.5#> In the previous life, Uncle and Aunt seized that inheritance, and for that loss I squandered two whole years before I could cultivate to the peak of the First Revolution. <#0.6#> In this life, that error shall not be repeated. (exhale)
→ emotion=calm, (exhale) resolve

## Block 10 — Street night — emotion: fearful / calm
Text:
The night sky grew ever more overcast, dark clouds veiling starlight, the mountain wind whistling with a rising howl, ever stronger. (inhale) <#0.6#>
→ emotion=fearful, (inhale)

Text:
Mountain rain was about to break. <#1.0#>
→ emotion=fearful

Text:
Still, he must explore. <#0.4#> His parents' inheritance could only be reclaimed when he is sixteen next year, <#0.4#> while Flower-Wine Monk's treasure was something that might be obtained in the near term. (breath)
→ emotion=calm, (breath)

## Block 11 — Dim street — emotion: sad / calm
Text:
In the street, few folk were about. From houses by the roadside, dim light shone; some household refuse, leaves, and dust rolled along, blown by the wind, drifting aimlessly. (exhale)
→ emotion=sad, (exhale)

Text:
Fang Yuan's thin clothes could scarcely hold back this mountain wind. He could not help but feel a chill. (inhale) <#0.4#>
→ emotion=fearful, (inhale) cold

Text:
He simply opened one of the jars he carried and took a small sip. <#0.5#> Though it was turbid wine, once swallowed, warmth rose within him. (exhale) (sighs)
→ emotion=calm, (exhale) (sighs) warmth

Text:
This was the first time in all these days that he had truly drunk at all. <#0.6#>
→ emotion=calm

Text:
The further from the stockade, the sparser the houses by the road, the dimmer the lights. <#0.6#>
→ emotion=fearful

Text:
Ahead, gloom lay thicker. <#0.4#> Wind pressed upon the mountain forest, branches swaying in the night, whistling as though beasts roared. (breath)
→ emotion=fearful, (breath)

Text:
Fang Yuan's steps did not falter. He passed beyond the stockade gate and went on, his figure receding further and further into the dark road. <#1.0#>
→ emotion=calm (deadpan determination)

## Block 12 — Warm contrast — emotion: happy / calm
Text:
Behind him lay the myriad lights of home, bright and glorious. <#0.6#>
→ emotion=calm

Text:
Amid those lights there was a warm corner. <#0.6#>
→ emotion=happy (warm)

Text:
There, Fang Zheng sat at his desk, reviewing the notes taken in class. The room was bright with lamplight, solid walls keeping out the cold wind, and at his hand stood a cup of warm ginseng tea, steam curling and rising. (breath) <#0.6#>
→ emotion=happy, (breath) cozy

## Block 13 — Shen Cui coquettish — emotion: happy
Text:
Young Master Fang Zheng, the hot water for your bath is ready, (breath) came Shen Cui's voice softly from outside the door.
→ emotion=happy (playful), (breath)

Text:
Fang Zheng's heart stirred. Then bring it in.
→ emotion=calm

Text:
Shen Cui entered, sashaying as she came, her face full of coquettish charm. (chuckle) <#0.4#>
→ emotion=happy, (chuckle)

Text:
This servant pays respects to Young Master Fang Zheng. (breath) She gazed upon Fang Zheng with amorous eyes, thinking: "Fang Yuan is only Grade C, but Fang Zheng is of Grade A aptitude. To latch onto him, that would be truly great fortune!" (chuckle)
→ emotion=happy (playful), (breath) (chuckle) coquettish

---
# Summary for MiniMax API call
# For each block, call:
# {
#   "model": "speech-2.8-hd",
#   "text": ".... with (chuckle) (sighs) (breath) and <#0.5#> pauses",
#   "voice_id": "female-... or male-...",
#   "emotion": "calm" | "happy" | "sad" | "angry" | "fearful" | "disgusted" | "surprised" | "neutral",
#   "speed": 1.0,
#   "format": "mp3"
# }
# calm DOES exist per official docs: https://developers.cloudflare.com/ai/models/minimax/speech-2.8-hd/ lists emotion enum includes calm
# Some frontends show neutral instead, but API accepts calm. If your UI doesn't list calm, use neutral or happy as fallback.
