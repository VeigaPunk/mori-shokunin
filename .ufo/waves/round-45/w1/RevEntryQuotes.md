# RevEntryQuotes — quote, line, scope and recheck review of `census-cgroup-levels-r45.md`

Seat: reviewer (leaf; no dispatch). Reviewed artifact:
`/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/knowledge/census-cgroup-levels-r45.md`
**final bytes** `sha256 b066d2dd1361c6cdd953186d58ac364366751ae9d0b89cbb8911e5d14c9e8483`,
66 lines, mtime 2026-10-25 07:51:12, stable (sampled every 10 s: nine consecutive equal
hashes, and unchanged through the whole verification run below). The scribe rewrote the file three times while I worked
(`1f28dd38` → `f94b8326` → `b066d2dd`); **all findings below are against `b066d2dd`**, and an
earlier defect in `1f28dd38` ("the unreadable case … so both branches fail") is already gone.

Sources, both read-only:
- `cgroup-v2.rst.src` sha256 `a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad`
  (3524 lines; re-fetched this seat from the entry's URL, `curl -fsSL --max-time 40` rc 0,
  digest identical);
- `tools/mori-census.sh` sha256 `87b8d680b9b2572e89977a10ff9b91630fbaf689f23f4892e06be427b977ab28`
  (4744 lines) — identical at `554ff416`, at HEAD `3ad8faaa`, and in the worktree
  (`git status --porcelain tools/mori-census.sh` → empty).

No tool installed or upgraded. Scratch: `.ufo/waves/round-45/tmp/RevEntryQuotes/`.

`wc` below = whitespace tokens of the quoted text after whitespace normalisation — the
entry's own convention; it reproduces every "(N words)" it prints.

## 1. Quote table (every quoted unit in the file)

| # | entry line | quote (abridged) | located | cited → actual | wc | stated | verdict |
|---|---|---|---|---|---|---|---|
| 1 | L7 | `a PSI trigger watcher is resident, … full=0 is not evidence of no stall` | `PROVINCE.md` | `:55` → 55 | 20 | — | verbatim |
| 2 | L19-25 | fenced `service_oom_kill='' … fi` | `mori-census.sh` | `:1707-1712` → 1707-1712 | 20 | 20 (L17) | byte-exact, whole block |
| 3 | L28 | `LOCAL_EVENTS` default `<CGROUP_EVENTS%.events>.events.local` | census | `:1705` → 1705 | 1 | — | exact code, not a quote |
| 4 | L28 | `SERVICE_EVENTS` default `user@<uid>.service/memory.events` | census | `:1706` → 1706 | 1 | — | **abbreviated** (finding F5) |
| 5 | L36 | `field must not claim the file does not exist` | census | `:1748` (block `:1747-1749`) → 1748 | 9 | 9 | verbatim, span correct |
| 6 | L38 | `local_oom_kill=$service_oom_kill path=${LOCAL_EVENTS} (local counter: …)` | census | `:1844` → 1844 | 9 | 9 | verbatim, exact |
| 7 | L40 | `MORI_CGROUP_SERVICE_EVENTS="$FX/cgroup/memory.events"` | census | `:3253` → 3253 | 1 | 1 | verbatim, exact |
| 8 | L40 | `check 'drift: CGROUP_OOM_KILL' 1 DRIFT` | census | `:3907` → 3907 | 5 | 5 | verbatim, exact |
| 9 | L40 | `'FINDING CGROUP_OOM_KILL'` | census | `:3908` → 3908 | 2 | 2 | verbatim, exact |
| 10 | L40 | `PASS (134 cases, 134 passed, 0 failed)` | run output | from my run, see §2 | 7 | 7 | matches my receipt |
| 11 | L42 | `ledger_round local_oom_kill max mem_fill_pct mem_peak not_open` | census | `:2747` → 2747 | 6 | 6 | verbatim, exact |
| 12 | L42 | `-e "s/\\b(${cre})=[0-9]+/\\1=<V>/g"` | census | `:2791` → 2791 | 2 | 2 | byte-exact incl. `-e` and doubled backslashes |
| 13 | L42 | `MORI_DRIFT: +FINDING:DISK_LOW -FINDING:DISK_CRITICAL` | their run | not reproducible byte-for-byte (live churn); same shape reproduced | 3 | 3 | see §gaps |
| 14 | L46 | `all fields in this file are hierarchical … down the hierarchy` | rst | `:1474-1476` → 1474-1476 | 22 | 22 | verbatim substring (leading `Note that` dropped, no ellipsis — cosmetic) |
| 15 | L46 | `For the local events at the cgroup level see memory.events.local.` | rst | `:1476-1477` → 1476-1477 | 10 | 10 | verbatim, exact |
| 16 | L46 | `Similar to memory.events but the fields … not hierarchical.` | rst | `:1518-1519` → 1518-1519 | 17 | 17 | verbatim, exact |
| 17 | L52 | `the parent slice's 1 is a propagated count, and memory.events.local reads 0` | `observability-census-r1.md` | `:135` → 135 | 12 | 12 | verbatim; companion fact is on `:136` (F4) |
| 18 | L54 | `the bare oom_kill= is still the parent cumulative counter … as local_oom_kill=` | `surfaces-r7.md` | `:88-90` → 88-90 | 20 | 20 | verbatim across the line break |
| 19 | L55 | `the read alone separates none of these` | `pid-probe-conclusion-r44.md` | `:53` → 53 | 7 | 7 | verbatim |

Every quote is ≤25 words; every stated count matches `wc`; no paraphrase is presented as a
quote. Code quotes are byte-exact, including the fenced block and the doubled backslashes of
the sed rule.

## 2. Census claims at the tip (`3ad8faaa`; worktree identical)

| claim | cited | actual line at tip | holds |
|---|---|---|---|
| silent preference order | `:1707-1712` | `service_oom_kill=''` … `if [ -r "$LOCAL_EVENTS" ]` … `elif [ -r "$SERVICE_EVENTS" ]` … `fi` | yes, byte-exact |
| `LOCAL_EVENTS` default | `:1705` | `  LOCAL_EVENTS=${MORI_CGROUP_LOCAL_EVENTS:-${CGROUP_EVENTS%.events}.events.local}` | yes |
| `SERVICE_EVENTS` default | `:1706` | `  SERVICE_EVENTS=${MORI_CGROUP_SERVICE_EVENTS:-/sys/fs/cgroup/user.slice/user-$(id -u).slice/user@$(id -u).service/memory.events}` | yes; entry abbreviates it (F5) |
| absent ≠ unreadable rule | `:1747-1749` | `  elif [ -e "$CGROUP_PRESSURE" ]; then` / `    # Present but not readable is a DIFFERENT fact from absent, and the state` / `    # field must not claim the file does not exist (measured: a mode-000` / `    # MORI_CGROUP_PRESSURE was reported 'absent' before this branch existed).` | yes, and it is the pressure branch |
| hard-wired `path=` | `:1844` | `    emit_finding CGROUP_OOM_KILL crit "local_oom_kill=$service_oom_kill path=${LOCAL_EVENTS} (local counter: kills in this cgroup only)"` | yes |
| pins to one file | `:3253`,`:3254` | `      MORI_CGROUP_SERVICE_EVENTS="$FX/cgroup/memory.events"` / `      MORI_CGROUP_LOCAL_EVENTS="$FX/cgroup/memory.events"` (and `:3252` `MORI_CGROUP_EVENTS=…` same file) | yes |
| only OOM assertion | `:3907-3908` | `  check 'drift: CGROUP_OOM_KILL' 1 DRIFT \` / `    'FINDING CGROUP_OOM_KILL'` | yes for `CGROUP_OOM`; "only cgroup assertion" is over-wide (F2) |
| volatile list | `:2747` | `  ledger_round local_oom_kill max mem_fill_pct mem_peak not_open` | yes |
| normalize rule | `:2791` | `    -e "s/\\b(${cre})=[0-9]+/\\1=<V>/g"` | yes, byte-exact |

### Reproduced measurements (my runs; fixture overrides only, census unmodified)

- **B** (the entry's provenance case): local `local7.events` mode 000 holding `oom_kill 7`,
  service `svc3.events` holding `3` → `EXIT=1`,
  `FINDING CGROUP_OOM_KILL severity=crit obs=local_oom_kill=3 path=…/local7.events (local counter: kills in this cgroup only)`.
- **A**: local path absent, service `3` → `EXIT=1`, `obs=local_oom_kill=3 path=…/absent-memory.events.local`,
  and `test -e` on that path → rc 1 (the printed path does not exist).
- **C**: local and service absent, `memory.events` present → `EXIT=1`,
  `SURFACE cgroup: ok`, `local_oom_kill=unavailable`, `FINDING CGROUP_OOM_KILL` count **0**.
- **Selftest baseline**: `TMPDIR=<scratch> ./tools/mori-census.sh --selftest` → `EXIT=0`,
  `MORI_CENSUS_SELFTEST: PASS (134 cases, 134 passed, 0 failed)` (14 s).
- **Three mutants** (private copies, `bash -n` clean):
  `elif` fallback deleted → `EXIT=0`, PASS 134/134 (live: `local_oom_kill=unavailable`, 0 findings);
  `path=${LOCAL_EVENTS}` → `${SERVICE_EVENTS}` → `EXIT=0`, PASS 134/134 (live: `path=…/svc3.events`);
  finding value forced to `0` → `EXIT=0`, PASS 134/134.
- **Drift mask**: with the script's own `DRIFT_COUNTER_KEYS` and `drift_normalize` sourced from
  its bytes, `local_oom_kill=1` and `=2` rows both normalise to
  `SURFACE cgroup: ok local_oom_kill=<V> path=/x` (`diff` empty → `NORMALIZED-EQUAL`).
  A real `--pin` then `--drift` over one fixture tree whose only change was that counter
  printed `DRIFT EXIT=1` and `MORI_DRIFT: +FINDING:DISK_LOW SURFACE:disk` — **no cgroup token**
  (the exact 3-word line in the entry depends on live disk churn; see gaps).

## Findings (severity order)

**F1 — moderate (title scope wider than the measurement; the parent's refutation condition).**
L1: "**The cgroup row's level is silent**". The row does name one level: `mem_fill_scope=` is
set on every arm (`fill_field="… mem_fill_scope=cgroup"` `:1856`, `…=host-ram` `:1858`,
`…=unavailable` `:1860`) and is embedded in the row at `:1862`. The body is about the OOM
counters' provenance only, never claims the whole row is level-blind, and never contradicts
`mem_fill_scope=`. As written the title is a general "the row names no level" claim and is
refuted by the same line the entry quotes. Fix:
`# The cgroup row's OOM provenance is silent: a preferred fallback, a hard-wired path=, and a selftest that cannot see the switch`.

**F2 — moderate ("only" over-wide).** L40: "The only cgroup assertion is `check 'drift:
CGROUP_OOM_KILL' 1 DRIFT`". The selftest has other cgroup assertions: `:4372`
`check 'clean: CGROUP_UNAVAILABLE is not DRIFT' 0 CLEAN`; `:4437`
`check 'drift: MEM_FILL_HIGH vs numeric cgroup limit' 1 DRIFT`; `:4444`
`check 'clean: cgroup fill under threshold does not fire' 0 CLEAN`; `:4621`
`check 'cgroup: scope high-watermark read with its instance anchor' 0 CLEAN`; `:4629`
`check 'cgroup: non-integer peak refused, bytes never echoed' 0 CLEAN`.
The only **`CGROUP_OOM_KILL`** assertion is indeed `:3907`. Fix: "The only
`CGROUP_OOM_KILL` assertion …".

**F3 — minor (grep label does not match its cited hit).** L40: "`memory.events.local` is never
created (`grep -c` of the name in the census: comments at `:1698,:1701` and the default at
`:1705`, no fixture)". Measured: `grep -c 'memory\.events\.local'` → **2** (1698, 1701);
line 1705 contains only `events.local` (derived `${CGROUP_EVENTS%.events}.events.local`), so
the literal name has no match there. With the shorter pattern `grep -c 'events\.local'` → **3**
(1698, 1701, 1705). The substantive claim (no fixture creates it) holds. Fix: name the
pattern, e.g. "`grep -c 'events\.local'` → 3".

**F4 — minor (under-citation).** L52 cites `observability-census-r1.md:135` for two facts. The
quote is exact at `:135`; "the probe prefers the local file" is `:136`
(`The probe now prefers \`memory.events.local\`, which is immune to both traps the`).
Cite `:134-136` (or `:135-136`), as both halves are part of the cited claim.

**F5 — minor (abbreviated default presented as the default).** L28: "`SERVICE_EVENTS` to
`user@<uid>.service/memory.events` (`:1706`)". The actual default begins
`/sys/fs/cgroup/user.slice/user-<uid>.slice/…`; as written it reads as a relative path. Use the
full prefix or write "…`/user@<uid>.service/memory.events`".

**F6 — minor (overstates what r12 cites).** L48: "`oom-kill-counter-kernel-only-r12.md:12`
cites the same local-vs-hierarchical sentence … as `1505–1509`". `:12` of that entry cites
`memory.events.local:1505–1509` as *making the distinction* (no sentence is quoted there) and
quotes the `oom_kill` phrase at `memory.events:1448–1458,1491–1494`. The conclusion — the two
renders differ, so a line number travels with its copy — holds. Fix: "cites the same
distinction as `memory.events.local:1505–1509`".

**Cosmetic.** L46's 22-word quote starts after the source's `Note that ` without an ellipsis;
text is verbatim.

## 3. Scope sentences (wider than the source?)

`What this does not license` (L61-66) is narrower than the sources throughout: no census change
(verified: `mori-census.sh` unchanged at tip), no cgroup v1, no remediation, no live-host
claim (A/B/C are fixture overrides — true), no general selftest weakness, no FR1 closure or
FR12 advance. No `proves`; the only `all` is inside the verbatim rst quote. The title (F1) and
"the only cgroup assertion" (F2) are the two over-wide statements; both are fixable without
touching the claim. The entry does **not** assert a general "the census names no level" claim,
and it does not contradict `mem_fill_scope=` in its body.

## 4. Metadata and recheck

| line | present | check |
|---|---|---|
| `source:` | L3 | `S473` + jsDelivr URL (`torvalds/linux@v7.2/Documentation/admin-guide/cgroup-v2.rst`) + opened-copy digest `a9433bb0…` + `fetched 2026-10-25`. Digests match; `S473` is the next free id (prior max `S472`; `renumber-map.tsv` "S473 reserved") |
| `verified-at:` | L4 | `2026-10-25` |
| `recheck:` | L5 | ran both arms: `curl … \| sha256sum` rc 0 → `a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad` (exact); `sha256sum …/tools/mori-census.sh` rc 0 → `87b8d680…b977ab28` (exact). Both are byte-sensitive: one appended byte changes each digest (`186f13db…` measured for the rst copy), so a changed fact fails the recheck. Earlier revision pinned only a selftest line; the current census-digest pin closes that hole |
| `coverage-map:` | L6 | names FR1 and FR12 with a rationale each |
| `ground:` | L7 | names **FR12** and quotes `PROVINCE.md:55`'s boundary verbatim (20 words) |

## Residual risk / verification gaps

- The entry's exact 3-word `MORI_DRIFT` line was not reproduced byte-for-byte: my pin/drift
  printed `+FINDING:DISK_LOW SURFACE:disk` (rc 1) because the drift is live disk churn, which
  the entry itself says. The substantive claim (no cgroup field/line in the drift verdict) is
  reproduced.
- `--selftest` mutants were run on private copies under my scratch, not against the committed
  file; the committed digest was verified unchanged before and after.
- I did not re-run the *whole* lane gate suite; the scope here is this entry's quotes, lines,
  scope and recheck.
- The file was edited under me three times. If the scribe lands another revision, F1-F6 and
  every line number above must be re-checked against the new hash; the source-side facts
  (census and rst line numbers) are invariant across them.

## What the L1 should run before admitting

1. `grep -n 'level is silent\|only cgroup assertion\|grep -c.*of the name' ` on the entry →
   after F1-F3, the title must name the OOM provenance, the assertion must be
   `CGROUP_OOM_KILL`, and the grep pattern must be named.
2. Re-run both `recheck` commands (expected `a9433bb0…` and `87b8d680…`).
3. Confirm the file hash changed only for the F1-F6 wording edits and that no cited line moved.
