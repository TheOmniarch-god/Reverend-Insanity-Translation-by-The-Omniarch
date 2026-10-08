# Reverend Insanity — The Omniarch Translation — Project Memory

This file is the persistent memory so I don't have amnesia. GitHub is the source of truth.
Last updated: 2026-10-08 19:24 UTC after workspace cleanup.

## Golden Repo
- **Repo:** `TheOmniarch-god/Reverend-Insanity-Translation-by-The-Omniarch` (private)
- **Live site:** https://ri.theomniarch.com.ng/ (Vercel)
- **Vercel:** Auto-deploys on push to main when author is `TheOmniarch-god <193905695+TheOmniarch-god@users.noreply.github.com>`
- **PAT:** saved in `~/.github_token` (600) and `~/.netrc` — use `TOKEN=$(cat ~/.github_token)` to clone
- **Clone cmd:** `git clone https://oauth2:${TOKEN}@github.com/TheOmniarch-god/Reverend-Insanity-Translation-by-The-Omniarch.git`

## Current Live State (as of 2026-10-08)

### Chapter 8 — Complete and Locked (86 lines)
- File: `docs/chapter-8.html` — 1908 words ~9 min, 43 paras, scene-break * * *, end-mark ◆
- Title: `Chapter 8: Things Remain, People Have Changed — Reverend Insanity`
- Meta fixed in commit 5408bd3: og:title clean (was broken missing quote merging og:description), twitter:title, ld+json position 8 wordCount 1908
- Nav: gamepad prev /chapter-7 + next disabled bench (span disabled, title="Chapter 9 at the bench") — safer than red primary 404
- Bottom nav: ← Chapter 7 + disabled Chapter 9 bench
- Ch8 master: `Reverend_Insanity_Chapter_8_Master_Translation.md`

**Ch8 fixes live (13 total, main 5408bd3):**
1. 境界 vs 层次 — nine ranks / nine major realms (Gu Masters = realm, Gu worms = tier)
2. Grammar + literary both — largest was... smallest was... (was in both clauses)
3. Fix C-grade → Grade C (Ch1-7 style Grade D/C/B/A)
4. Demarcator …… → * * * scene-break (matches Ch1 3x, Ch6 1x)
5. 迟迟不现身 = show itself (not manifest/show up)
6. Avoid repetition: toll/toll → cost, devastating/devastating → grievous
7. for → within (感到 = felt inside)
8. Internal monologue grammar: Don't I even have the courage...? split for punch
9. Punctuation audit, Rank I consistency, etc.
10. Design parity rebuild from Ch7 template — fixed broken meta
11. Prev/next buttons
12. Mobile container improvements

**Live verified:** `curl -s https://ri.theomniarch.com.ng/chapter-8.html | grep og:title` clean

### Mobile Fix — Live c86a23b (2026-10-08 19:15:08 GMT)
- **Issue:** Index chapter list very long (84px padding), reading container very long on mobile (screenshot)
- **Fix:**
  - Index 640px: wrap 28→14px, chapters 84→32px 0 48px, vol-band tighter 14x16 radius 8, ch-list gap 8px, ch-row 40px→32px 1fr auto 12x14px gap 10px radius 10px, num 13px name 14.5px/1.3 small 11.5px/1.35 pill 10px
  - Reading 700px: prose 22x18→20x16, p margin 1em line-height 1.75 (was 1.8/1.9 very long), scene-break 1.2em, end-mark 1.5em, reader-head 72→68px h1 24px ch-title 18px
  - 480px: 6x8x48px 15px/1.7 prose 16x12 p 0.95em
  - Bump style.css?v=20261008-mobile-fix2 to bust Vercel edge
- **Verified live:** `style.css?v=20261008-mobile-fix2` contains new rules

### Workspace Cleanup — Live f1d06a1 + 612ffa4
- **Problem:** Workspace 168 MB (23 MB + 145 MB repo_push) >128 MB snapshot cap → .git/config excluded, PAT lost, amnesia
- **Solution:**
  - f1d06a1: 21 files (10k lines) — editorial notes, idioms, literary notes, lore, Ch6-8 line-by-line, combined editions
  - 612ffa4: 89 files (25k lines) — remaining md + editorial_backups full history
  - Deleted: repo_push (145M), site_preview (9.8M), uploads (3.8M), docx, mp3, webp, pdf, etc.
  - After: 797 KB, ~60 files — well under cap
- **Token preserved:** `~/.github_token` and `~/.netrc` (600) — survives cleanup

## User Constraints & Corrections (Standing Rules)

- **British spelling:** towards (not toward) — preface Either Towards Success or Towards Destruction, all chapters towards
- **Author identity:** Must be `TheOmniarch-god <193905695+TheOmniarch-god@users.noreply.github.com>` — Vercel Hobby private repo blocks outside contributor
- **Tolkien style:** peak Tolkien narration + natural earnest internal dialogue, modernism not too archaic, no em dashes, no drift for flat voice, lowered not bowed, upon for elevated poetic, on for simple
- **They varied in size:** must have was in both clauses — largest was... smallest was... (grammar + literary)
- **GU major:** Major/Minor belongs to Gu Masters (境界=realm, 大境界 major, 小境界 minor), Gu worms = 层次=tier, 转=Rank long-term. Must be nine ranks / nine major realms
- **Keep densely packed**
- **Grade style:** Ch1-7 uses Grade D/C/B/A aptitude (Grade + letter), not C-grade
- **damage vs damages:** damage uncountable no article, damages = legal compensation, keep grievous damage
- **piece vs fragments:** 一块蓝水晶 = a piece of blue crystal (measure word), 元石碎块 = fragments of primeval stone (poverty broken bits)
- **迟迟不现身 = show itself** best — manifest too mystical formal, show up too colloquial, show itself literal 现身=show body
- **Avoid repetition:** toll/toll and devastating/devastating back-to-back — use cost + grievous
- **I accumulated** correct — not accumulates, not have accumulated, matches 原先积攒的
- **After these past days had already come to remember** — wordy but literary gradual (7 days recognition), keep despite Google business-concise flag
- **Demarcator:** * * * with scene-break class same as Ch1/Ch6 live, not …… plain
- **Thrill within vs for:** 伴随着这种理解，方正隐隐地感到一阵难以言表的痛快 — 感到 = felt inside, within more literal/internal than for
- **Internal monologue grammar:** 自己这是怎么了？连和哥哥对视的勇气都没有么？ 我已经变了，我已经彻底改变了！ — Must be Don't I even have the courage to look my brother in the eye? I have changed! I have completely changed! — adds subject/article/possessive, splits for punch, keeps unquoted
- **Quoting rule:** direct speech spoken aloud = quoted " ", indirect monologue / inner thought = NOT quoted free indirect
- **face flush** (verb bare infinitive) = feel becoming red active immediate matches 发烫, vs face flushed (adjective result state) needs was/grow — keep flush

## Recent Commits (main)
- 612ffa4 chore: save remaining workspace md + editorial_backups to GitHub
- f1d06a1 chore: save editorial notes + line-by-line sources to GitHub — workspace cleanup
- c86a23b fix(mobile): normal design — index + reading container less long
- 5408bd3 fix(ch8): design parity with Ch7 — rebuild meta + structure clean
- 6b91cb2 fix(ch8): rebuild nav properly — prev/next same as other chapters
- a9996fa fix(ch8): prev/next buttons — was Ch6/Ch8 self, now Ch7 + All Chapters
- ... (see git log)

## Workspace Current (after cleanup)
- `/home/user/` — 797 KB, ~60 files, mostly master translations Ch2-8, raw Chinese, preface, official synopsis, etc.
- `~/.github_token` — PAT for cloning
- `~/.netrc` — netrc for github.com
- `~/.ssh/known_hosts` — ssh known host
- No `site_preview/` — deleted, can re-clone to /tmp when needed: `git clone --depth 1 https://oauth2:${TOKEN}@github.com/... /tmp/mem_clone`
- No `repo_push/` — deleted to stay under 128MB cap, re-clone on demand

## How to Restore Memory
1. Check this file `MEMORY.md`
2. Clone shallow to /tmp: `TOKEN=$(cat ~/.github_token); git clone --depth 20 https://oauth2:${TOKEN}@github.com/TheOmniarch-god/Reverend-Insanity-Translation-by-The-Omniarch.git /tmp/mem_clone`
3. `cd /tmp/mem_clone && git log --oneline -20 && ls docs/`
4. Fetch live site: `curl -s https://ri.theomniarch.com.ng/ | grep style.css`

## Next Planned Work
- After Ch8 locked: Ch9 bench line-by-line or Ch1-7 consistency audit
- Mobile container very long fix is now live, but user may want further tweaks
- Keep workspace under 128MB — always delete repo clones after push, keep only essentials in /home/user

## External Sources
- https://en.wikipedia.org/wiki/Three_teachings: Three teachings = Confucianism, Buddhism, Taoism
- https://zhuanlan.zhihu.com/p/654059306: 三观 = worldview, life view, values

## Errors & Dead Ends to Avoid
- Duplicate shopkeeper line after v2 rebuild (fatty vs greasy)
- Greasy and shining with oil tautology
- chapter-8.html not auto-generated from master md — must edit HTML directly
- Index chapter 8 hidden as bench — need edit docs/index.html chapters list
- .git/config excluded from snapshot — always save PAT to ~/.github_token and ~/.netrc
- Vercel blocks deploy if author != TheOmniarch-god — always set git config user.name/email
- Workspace snapshot cap 128MB/10000 files — repo_push 145MB causes loss, delete after push
