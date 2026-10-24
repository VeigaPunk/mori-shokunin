# CritCollision — attack on the round-42 SOURCES collision check

Seat: CritCollision (critic) · lane: mori round 42 · landed tip `34b926730c30e0251e1aec531863d8355dc491f1`
Claim under attack: `corpus/lessons/round-42.md:59-61` — "Collision check: reg 231 ids (S001–S231) vs staged 115 (S232–S346) → 0 collisions" — and the committed artifacts `.ufo/waves/round-42/assimilation/{reg-ids,staged-ids,collisions}`.

## Re-derivation (independent, not trusting the artifacts)

Extraction anchored to cell 2 of the pipe table, whitespace-normalized, exact `S\d{3}`:

```
awk -F'|' 'NF>2 {c=$2; gsub(/^[ \t]+|[ \t]+$/,"",c); if (c ~ /^S[0-9][0-9][0-9]$/) print c}'
```

- **reg-ids**: `git show 34b92673^:corpus/SOURCES.md` (parent `316f3dcf`) → 231 ids, `diff` vs committed `assimilation/reg-ids` → **identical**.
- **staged-ids**: `/home/vgpnk/Projects/shokuknow/merge/mori/SOURCES.append.md` → 115 ids, `diff` vs committed `assimilation/staged-ids` → **identical**.
- **Past check**: `comm -12 reg staged` → **0 collisions** — claim reproduces. Internal `uniq -d` = 0 on both sets.
- Loose `\bS[0-9]{3}\b` over the whole landed `corpus/SOURCES.md` adds no id outside the 238 cell-2 ids (`comm -23` empty); the anchored pattern loses nothing.
- Guard fixture `assimilation/guard/` verified consistent: `  | S232 | x |` (indented) IS extracted by cell-2 normalization (`guard/reg-ids` = S232, `guard/collisions` = S232); a column-zero-anchored pattern would miss it. Lesson wording is accurate.
- Landed registry re-extracted: 238 ids (`S001`–`S235`, `S241`, `S262`, `S347`), `uniq -d` = 0 — matches the `231->238` commit subject. `tools/mori-sources-appendonly.py --selftest` re-run here: `pass=22 fail=0`; it carries **no** id-uniqueness arm, so today's uniqueness rests on this manual check only.

## Counterexample — NEXT round, proved with comm

Post-append registry vs the remaining staged band:

```
$ comm -12 reg-post <(seq -f 'S%g' 236 346)
S241
S262
```

**2 future collisions, inside the band, created by this round's out-of-order adoption.** Round 42 adopted `S232–S235` (below the remaining band — safe, `comm` gives ∅ for them) but also `S241` and `S262`, which sit inside `S236–S346`. `SOURCES.append.md` is immutable (read-only shokuknow tree): both ids remain staged there. Any next-round re-adoption of the staged remainder verbatim re-emits `S241`/`S262` as rows that **diverge in content** from the landed rows: the staged `S232/S241` teaches are pre-normalization text (the escaped-pipe sweep parenthetical was removed on adoption, `round-42.md:62-63`), and staged `S262` carries the dead `aaron papers fetch -m s2` recheck that lesson M3 recorded as no longer resolving — landed `S262` was re-grounded on the OpenAlex record. A collision-handled-as-overwrite would silently degrade `S241`/`S262` and revive the stale recheck; a collision-handled-as-fatal check blocks the adoption until the ledger is filtered.

**Smallest safe correction**: next adoption computes `comm -23 staged reg-post` first (adoptable set = **109 ids**, verified: `S236–S240`, `S242–S261`, `S263–S346` minus none; `S268` is adoptable-by-id but refused on substance with a recorded flip condition; `S244` quarantined not-cited). The staged ledger needs a recorded disposition for `S241`, `S262`, `S268` (adopted-normalized / adopted-regrounded / refused) — or the merge package must be regenerated against the landed registry — before the band is re-offered.

## Secondary finding — S347 mint-rule identity risk

`S347` = `max(staged)+1`, not `max(reg)+1`. Verified non-colliding today (`comm -12 {S347} staged` = ∅; absent from reg). Conditional hazard: if the campaign-side package ever regenerates staged ids from its own ledger (`max = S346` → next = `S347`) without consulting the landed lane registry, a *different source* gets minted as `S347` and the double-mint is invisible to the ledger-side check (each ledger's `S347` is internally unique). Smallest correction: campaign allocation re-derives next-id from the landed lane registry, and the lesson states the mint rule explicitly.

## Verdict

The claimed check is **correct and reproducible** (0 past collisions, artifacts byte-faithful, guard behavior honest). The counterexample does not falsify it — it bounds it: it is a point-in-time check that neither records ledger dispositions nor owns the allocator. The fixable defects are (1) unstaged-but-ledgered `S241`/`S262` — 2 proved future collisions under verbatim band re-adoption — and (2) the unrecorded `S347` mint rule. Impacted axes: **depth** (ledger lifecycle, allocator identity) primarily; **freshness** secondarily (the S262 stale-recheck revival path). Both are fixable at the next adoption boundary; they are not grounds to reject this round's landing.
