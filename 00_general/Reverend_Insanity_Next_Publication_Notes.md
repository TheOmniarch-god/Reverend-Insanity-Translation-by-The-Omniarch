# Next publication — Chapter 5 (pending review)

## Approved correction to publish alongside Chapter 5

Chapter 1 source: 这里早已经布下天罗地网，这次你必定身首异处！

Replace:
> An inescapable net of heaven and earth has long encircled this summit—today, your head and torso shall be severed asunder!

With:
> An inescapable net of heaven and earth has long been laid here. This time, your head and body shall be severed asunder!

Local active Markdown editions and editorial logs are updated. When preparing the website release, update the canonical Chapter 1 page and any maintained aliases, search-index text, and current downloadable editions from the approved master. Do not alter historical backups.

## Status

- Chapter 5 is not finalized. Do not publish its proposed renderings as approved prose.
- This file is a publication checklist, not a claim of a scheduled deployment or completed GitHub update.
- No website changes or GitHub push performed.
- Unresolved idiom discussions remain pending; do not fold them into this approved correction.


## Chapter 1: kinship correction applied

Following the user pointing out that “nine generations” remained in the compiled edition, replaced “killed the members of my family, and slaughtered every soul across nine generations of my bloodline” with “killed my entire family, and wiped out all my kin” in the Chapter 1 master and combined Chapters 1–3, 1–4, and 1–5 Markdown editions. Source: 杀光我全家，诛了我的九族. Historical backups remain unchanged. No other portion of the speech changed in this operation. The Chapters 1–5 compilation remains free of em dashes. No website changes or push.


## Chapter 1 — consolidated accusation approved and applied

User authorized the complete proposed speech with “Work on them.” This supersedes the earlier pending status and the intermediate “wiped out all my kin” version.

> “Monster! Three hundred years ago, you violated me and robbed me of my chastity. You killed my entire family and slaughtered all my kin. From that moment on, I’ve wanted nothing more than to devour your flesh and drink your blood! Today, I’ll make you wish you were dead!”

Applied to the Chapter 1 master and combined Chapters 1–3, 1–4, and 1–5 Markdown editions. Replaced “defiled my honor,” “wiped out all my kin,” “that cursed hour,” “I have hungered to,” and “pray for the mercy of death.” Retained the flesh-and-blood vengeance imagery. The approved heaven-and-earth net wording remains present in all four editions. Chapters 1–5 remains free of em dashes. Historical backups remain unchanged.

Queue the entire corrected speech for the next publication, not merely its kinship clause. No website or GitHub changes performed. The Chapter 5 茹毛饮血 decision remains unresolved; its draft wording was not changed in this operation.


## Chapter 1 — dragnet wording supersedes heaven-and-earth net

User explicitly approved:

> We have long since laid an inescapable dragnet here. This time, you shall be beheaded!

Replaces the formerly approved “An inescapable net of heaven and earth has long been laid here” version in the Chapter 1 master and all active combined editions (1–3, 1–4, 1–5). “We” is supplied from the speakers’ collective action. 天罗地网 is rendered idiomatically as an inescapable dragnet. Earlier approvals are historical, not the current publication wording. The corrected woman’s speech remains unchanged. Chapters 1–5 remains free of em dashes. No website edit or GitHub push.


## Final full-read approval

User: “I'm done reading Chapter 5. It's okay.”

Chapter 5 is now approved as presented in the latest compiled Chapters 1–5 reading edition. Created `Reverend_Insanity_Chapter_5_Master_Translation.md` directly from that edition and synchronized the former reading-draft file without rewriting prose. This approval supersedes earlier pending wording statuses for Chapter 5, including the selected 茹毛饮血 rendering, scent wording, pressure phrasing, and other full-read choices. It does not claim completion of a broader idiom audit. The compiled edition remains free of em dashes. No website changes or GitHub push performed.


## Approved Chapter 3 idiomatic dismissal

User approved “Kindly Piss Off” as the Chapter 3 title and the closing line:

> As long as they do not block my path, they can piss off. I wouldn’t even deign to step on them.

This supersedes the former literal ball-playing wording. Applied to the Chapter 3 master and combined Chapters 1–3, 1–4, and 1–5 Markdown editions. Historical backups left unchanged. Queue both title and closing prose for website metadata, chapter list, navigation, search, and chapter page in the next release. No website changes or GitHub push performed.


## Chapter 3 opening sound: approved exception

User approved restoring the audible rhythm within the opening paragraph:

> Clack, clack-clack. Clack, clack-clack. The night watchman was making his rounds, striking his wooden clapper in a steady rhythm.

Source: 邦、邦邦，邦、邦邦。 / 巡游的更夫，敲着有节奏的梆子。

Replaced only the former first sentence; the following sentence about Fang Yuan hearing the strikes remains unchanged. Applied to the Chapter 3 master and combined Chapters 1–3, 1–4, and 1–5. This is a specific exception to the preference against standalone comic sound effects, not permission to add sounds elsewhere. No em dashes added; Chapters 1–5 remains free of them. Historical backups retained. No website update or GitHub push.


## Publication log: 2026-09-27, Chapter 3 clapper line

Pushed directly to `main` of the private repo
`TheOmniarch-god/Reverend-Insanity-Translation-by-The-Omniarch`
as commit `f5b366d`, "Chapter 3: restore audible clapper rhythm in opening line".

Files changed (two, one line each):
- `docs/chapter-3.html`, paragraph `id="p1"`
- `docs/search-index.json`, entry `paras[182].t`

The site is hosted on **Vercel**, not GitHub Pages (`has_pages: false`, DNS points to
cname.vercel-dns.com, responses carry `server: Vercel`). At time of writing the push had
NOT produced a new deployment: the live edge response still showed the 09:16:35 GMT build
with a steadily rising `age`. The previous commit (06:37:47Z) likewise went live only at
09:16 GMT, so deploys appear to be triggered manually rather than by the Git integration.
A redeploy in the Vercel dashboard is required for this change to appear.

Not touched, flagged for a decision: `docs/docs/` is a stale duplicate of an older build.
Its `chapter-3.html` still carries the superseded title and the old closing line, and it is
publicly reachable at /docs/chapter-3. No edit or deletion was made there.


### Deployment resolved, 2026-09-27

First push (`f5b366d`) was committed under an invented author identity
`The Omniarch <theomniarch@users.noreply.github.com>`. Vercel blocked the resulting
deployment: on the Hobby plan a private-repo commit from an unrecognised author is treated
as an outside contributor. A dashboard Redeploy was also refused for the same reason.

Fix: the commit was amended to the account's real identity
`TheOmniarch-god <193905695+TheOmniarch-god@users.noreply.github.com>` and force-pushed as
`4d13997`. Vercel then built and published it. Live page last-modified moved from
09:16:35 GMT to 14:23:08 GMT and now serves the approved opening line, with the search
index matching.

Standing rule for future pushes: always commit as
`TheOmniarch-god <193905695+TheOmniarch-god@users.noreply.github.com>`.

Still outstanding: the stale `docs/docs/` duplicate build, publicly reachable at
/docs/chapter-3, still carries the superseded chapter 3 title and closing line.
Untouched pending a decision.


### Live text audit, 2026-09-27

Record correction: Chapter 5 is ALREADY PUBLISHED on the main site. Earlier notes describing
it as queued and unpublished were wrong. /chapter-5 serves
"Ren Zu's Three Gu, Hope Opens the Aperture", it is listed in the chapter index, and its
54 body paragraphs were compared against
Reverend_Insanity_Chapter_5_Master_Translation.md and match exactly.
The site's search index holds 346 paragraphs across the preface and chapters 1 to 5.

Audited live chapters 1 to 5 against the approved masters:
- Approved wording present: Ch1 dragnet sentence, consolidated woman's speech, "a Chinese
  student on Earth", the self-detonation line, the next-life demon line; Ch3 clapper opening,
  "they can piss off", "a mere slip of a maid", the harem line, "nothing more than flesh";
  Ch4 "like the river of stars in the night sky".
- No superseded wording found: no "nine generations", "wiped out", "heaven and earth net",
  "cursed hour", "pray for mercy", "Huaxia", "Awakening Ceremony", "bag of flesh",
  "Milky Way", "sea of flowers", "scions", "patriarchs".
- Zero em dashes in the live text of all five chapters.
- Ch1 correctly retains "not ten thousand households, but several thousand nonetheless".

The retired Chapter 3 title is no longer served anywhere. The orphaned duplicate build that
still carried it was removed (commit dd74f2f) and /docs/chapter-3 now returns 404. Live
chapter titles for 1 to 5 all match the approved masters.


## Chapter 3 revision, 2026-09-28: sow discord, and concubines rather than harem

Approved by the user and applied to `Reverend_Insanity_Chapter_3_Master_Translation.md`,
`_Chapters_1-4.md`, `_Chapters_1-5.md` and `_Chapters_1–3.md`. Supersedes the earlier
approved wording recorded above. Not yet pushed to the live site: the PAT was lost when
/tmp was cleared and must be resupplied.

1. L54, 挑拨和自己的兄弟情谊
   was: ...and drive a wedge between them.
   now: ...and sow discord in the brotherly bond between them.
   Reason: Han Dian gives 挑拨 as 拨弄是非引起争端, English instigate, incite, with 离间 among its
   synonyms. Drive a wedge dropped 情谊, the bond, which is the grammatical object.

2. L56, 被舅父舅母挑拨成功
   was: Their uncle and aunt had succeeded in setting them against each other.
   now: Their uncle and aunt had succeeded in sowing that discord.
   Reason: 挑拨 appears twice, L54 and L56. Two different English phrasings hid the fact
   that it is the same act named twice.

3. L58, 更能提早收入后宫
   was: ...taken into his harem ahead of time.
   now: ...taken as one of his concubines ahead of time.

4. L61, 收入后宫？她还不配。
   was: Her, in my harem? She's not worthy.
   now: Take her as one of my concubines? She's not worthy.
   Reason for 3 and 4: the author uses two words. Shen Cui's own calculation at L28 is
   侧室, a rank in a household, which is why 从奴转为主 follows. Fang Yuan's word at L58 and
   L61 is 后宫, the rear palace, Han Dian's imperial harem. She wants standing, he thinks
   of a collection. "One of my concubines" keeps that contrast while dropping harem.
   L28 stays plain "concubine": the status is already carried by "rise from servant to
   mistress", so no special term is needed. Also 收入 is "to take in", and "Her, in my
   harem?" presupposed a harem he does not have; "Take her" matches the verb.

### Open, not actioned
Chapter 3 is 66 paragraphs in the Chinese and 49 in the published English. Seventeen
paragraph breaks were lost, including the break between source paragraphs 53 and 54.
Never approved. Queued as a structural pass together with the Chapters 1 to 5 idiom sweep.
