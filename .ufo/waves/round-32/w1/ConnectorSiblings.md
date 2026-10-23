# Connector — sibling-overlap scan for C1 (round 32, wave 1)

Read-only scan of every `*-shokunin` lane for rows carrying the same URL as a round-32 population row.
No sibling file was written, no lane git/jj state touched, no URL fetched; the only writes are this
report and scratch under `/fast/scratch/hyaku/mori-r32/ConnectorSiblings/`. No tool was installed or upgraded.

Method. Population read from `.ufo/waves/round-32/c1-population.json` (34 rows, 29 distinct URLs).
For each of the 21 lanes with a `corpus/`, I parsed `corpus/SOURCES.md` header-aware (column index from the
header row, not from cell position) and matched each row against the population URLs both as an exact
substring and by canonical `host+path` (lower-case, `www.` stripped, trailing slash stripped). The substring
pass also caught two rows citing the version-pinned `/2.56.0` variant (`tsukuroi-shokunin/corpus/SOURCES.md:83,88`);
the canonical pass treats those as a different path, so they count as page overlap, not URL overlap.

Result: 8 distinct population URLs appear in 7 sibling lanes, 22 sibling rows, covering 9 of the 34
population ids (S044 S045 S046 S047 S049 S058 S064 S069 S073). The other 25 ids have no sibling row.

## 1. Shared URLs, sibling rows, status, opened, recorded recheck

| population URL | mori ids | lane:line | row | status | opened | recheck cell |
|---|---|---|---|---|---|---|
| docs.jj-vcs.dev/latest/git-compatibility/ | S044 | souji:71 | S051 | mined | 2026-10-20 | on-release |
| | | tameshi:70 | S061 | mined | 2026-10-20 | 180d |
| | | tameshi:85 | S076 | mined | 2026-10-20 | 180d |
| docs.jj-vcs.dev/latest/cli-reference/ | S045 | kama:84 | S072 | mined | 2026-10-21 | on-release |
| | | kama:96 | S084 | mined | 2026-10-21 | on-release |
| git-scm.com/docs/git-rev-list | S058 | kama:114 | S102 | mined | 2026-10-21 | on-release |
| | | souji:80 | S060 | mined | 2026-10-20 | on-release |
| git-scm.com/docs/git-merge-base | S046 | kaidoku:79 | S073 | mined | 2026-10-21 | on-release |
| | | tsukuroi:67 | S061 | mined | 2026-10-20 | on-release |
| git-scm.com/docs/git-symbolic-ref | S047 | tabi:65 | S051 | queued | 2026-10-20 | 180d |
| | | tameshi:83 | S074 | mined | 2026-10-20 | on-release |
| docs.python.org/3/library/pathlib.html | S069 S073 | souji:60 | S040 | mined | 2026-10-20 | on-release |
| cheatsheetseries.owasp.org/.../Logging_Cheat_Sheet.html | S049 | souji:121 | S101 | mined | 2026-10-21 | 90d |
| git-scm.com/docs/git-rev-parse | S064 | kumitate:44 | S031 | mined | 2026-10-21 | on-release |
| | | souji:99 | S079 | mined | 2026-10-21 | on-release |
| | | souji:111 | S091 | mined | 2026-10-21 | on-release |
| | | souji:119 | S099 | mined | 2026-10-21 | on-release |
| | | tabi:66 | S052 | queued | 2026-10-20 | 180d |
| | | tabi:79 | S065 | mined | 2026-10-20 | 180d |
| | | tameshi:71 | S062 | mined | 2026-10-20 | on-release |
| | | tsukuroi:83 | S077 | mined | 2026-10-21 | on-release (URL is `/2.56.0`) |
| | | tsukuroi:88 | S082 | mined | 2026-10-21 | on-release (URL is `/2.56.0`) |

The `recheck` cell is a cadence, not a result; no sibling row of these 22 carries a "rechecked on" cell.
Recorded results exist only where a lane wrote a superseding row, a receipt or a lesson:

- `git-rev-parse`, tabi S052: receipt `tabi-shokunin/corpus/evidence/round-18/source-recheck/S052.json`
  — `fetchedAt 2026-10-20T20:49:06.283Z`, `httpStatus 200`, `bytes 122459`, `sha256 1e84fc20…585f19da`,
  `teachesVerdict drift`, `quoteFound true`. Corrected by tabi S065 (`tabi-shokunin/corpus/SOURCES.md:79`,
  "reopened 2026-10-20"; note table `corpus/knowledge/source-recheck-round-18.md:166`): "HEAD names a base
  commit but may be attached via a symbolic branch reference; 'not a branch' was overbroad."
- `git-symbolic-ref`, tabi S051: receipt `…/source-recheck/S051.json` — same second,
  `bytes 28804`, `sha256 d706904473082a0ef07ed8eedd2c4d94be25dac852e58ff3b017048828c38872`,
  `teachesVerdict held`.
- `git-rev-parse`, souji S079→S091→S099 (`SOURCES.md:99,111,119`): reopened 2026-10-21 and narrowed twice;
  `souji-shokunin/corpus/lessons/round-20.md:160` states "reopen and narrow the old teaches claims; no
  immutable row rewrite".
- `git-compatibility`, tameshi S061→S076 (`SOURCES.md:85`): "re-opened 2026-10-20", anchor ¶2→¶3; the page
  did not change, the earlier paragraph anchor was wrong (`corpus/lessons/round-18.md:50,109`).
- `cli-reference`, kama S072→S084 (`SOURCES.md:96`): S084 labels the page "automatically generated latest
  reference … not an installed-version pin" — a scope correction, not a page change.
- `git-merge-base`, tsukuroi S061 anchor records the version panel "2.43.1–2.56.0 no changes";
  mori's own S046 anchor records the same panel. Two lanes read the same marker, no digest.
- `git-rev-list`, kama S102 and souji S060 both record "last updated 2.56.0"; no digest.
- `pathlib`, souji S040 records "Python 3.15.0 online documentation"; no digest.
- `Logging Cheat Sheet`, souji S101 records "unversioned page" and a 90d cadence; no digest.

## 2. Prior art

Closest method — **tabi round 18** (`tabi-shokunin/corpus/knowledge/source-recheck-round-18.md`):
one producer script, one normaliser, one receipt per row binding body bytes, sha256, excerpt and quote
(:13, :19, :21); URL class split pinned/live/own-work (:110); drift handling "no superseding row is opened
by this note", "moving anchors are not drift" (:123, :127); limits "quote presence is not claim truth",
"dynamic pages … a digest pins one response's bytes" (:140, :143); final counts `held=41
drift_superseded=9` (:209). Bodies and receipts are committed (verified: `git -C tabi-shokunin ls-files`
lists `S051.body.gz`, `S051.json` and the note; `git status --porcelain` on them is empty).

tabi's rule the mori method should cite verbatim — `tabi-shokunin/corpus/lessons/round-12.md:35`:
"Dynamic full-page hashes are fetch identities, not semantic drift."

Adjacent tools, none of which re-checks a live URL (this confirms the contract's "no lane tool re-checks
these rows"):
- `tabi-shokunin/scripts/check-sources.mjs` — registry shape only; its URL matches are fixtures (:387-459)
  and `spawnSync` calls only `awk` and the selftest (:467, :510). No network.
- `tabi-shokunin/scripts/check-freshness.mjs` — three local plugin files (:13-17), not web sources.
- `kotodama-shokunin/tools/check-source-access.py:2` — flags bypass markers; adjacent rule mori already obeys.
- `tsukuroi-shokunin/tools/check-recheck-commands.py:2` — gates `recheck:` *procedure lines* in knowledge
  entries for forbidden binaries. Different meaning of "recheck"; do not cite as prior art for freshness.

Design alternative to differ from: `tsukuroi-shokunin/corpus/SOURCES.md:83,88` repinned the same mutable page
to `/2.56.0`. That is the cheap fix the round's frozen population forbids (pinning removes a row from C1),
so mori must recheck in place, and should say so once in the README.

Rules that constrain reuse: `mori-shokunin/corpus/QUALITY.md:104` (#41) "A green fixture or sibling gate
never establishes drift freshness"; mori's own precedent for citing without absorbing is
`corpus/knowledge/userspace-oom-killers-r26.md:153` ("cited here and **not absorbed**").

## 3. Evidence: the fleet already holds a two-date witness for 2 of the 9 overlapped ids

mori's copies in `corpus/evidence/recheck-r32/` were written at `2026-10-22 22:35:55 -0300`, i.e.
`2026-10-23T01:35:55Z` (`stat`; `date -u` at scan `2026-10-23T01:38:16Z`), so a fetch instant at or after
the contract's `2026-10-23T01:00:00Z` floor can be recorded honestly. Comparing them with tabi's committed
bodies, whose gunzip digest equals its receipt digest:

| id | mori copy | mori bytes / sha256 | tabi fetch | tabi bytes / sha256 | normalised text |
|---|---|---|---|---|---|
| S047 | `recheck-r32/S047.src` | 28808 / `0d2ea49c…bea20791c` | `S051.json` 2026-10-20T20:49:06Z | 28804 / `d7069044…828c38872` | identical: 4232 B, sha256 `b9c0c595…` |
| S064 | `recheck-r32/S064.src` | 122463 / `64c60354…09b83421` | `S052.json` 2026-10-20T20:49:06Z | 122459 / `1e84fc20…585f19da` | identical: 34023 B, sha256 `01e80bf0…` |

Commands (all read-only):
`gunzip -c tabi-shokunin/corpus/evidence/round-18/source-recheck/S051.body.gz | sha256sum`
→ `d7069044…`; `python3 .ufo/waves/round-32/seat-check.py text <file> | sha256sum` on mori's copy and on
tabi's body → the same `b9c0c595…` (S047) and `01e80bf0…` (S064). The same pair on
`S052.body.gz` and `recheck-r32/S064.src` gives `1e84fc20…` for the raw body and `01e80bf0…` for the text.

The raw difference is 4 bytes in the page-head asset fingerprint: first difference at byte 901 (S047) and
898 (S064), inside `application.min.<64-hex>`, which the counter's tag-stripping normaliser removes.
tabi's own quotes are present in mori's normalised copies: "This will error out if $REV is empty or not a
valid revision." (1 occurrence in `S064`) and "Typically you would give HEAD" (1 in `S047`). So for these
two ids the fleet holds a *measured* no-change interval of 2 d 4 h 46 m, and the digest inequality that a
naive cross-run comparison would report is not drift.

For the other 7 shared URLs there is no second date: every sibling row was opened 2026-10-20 or 2026-10-21,
the same days mori opened them, and none stores bytes. What they add is version-marker agreement
(v0.46.0 latest, git 2.56.0, Python 3.15.0, unversioned OWASP page) — a textual reading, not an interval.

## 4. Contradictions, stated not smoothed

1. tabi's note says both "No drift in this round. All 51 receipts are `held`" (:123) and, in its own wave-2
   section, `held=41 drift_superseded=9` (:209) plus `S065 supersedes S052 … 'not a branch' was overbroad`
   (:166). Reading only :123 would make a connector call S064 `drifted`; the bytes prove the page did not
   move. The label was a teaches-scope supersession.
2. tabi's `S052.json` is internally inconsistent: `teachesVerdict drift` while its `note` opens "Held: body
   keeps …". A sibling verdict field therefore cannot be consumed as a page-drift signal.
3. Same-day opens are not independence: all 22 sibling rows were opened on 2026-10-20 or 2026-10-21, the
   same two days mori opened all 9 of its overlapped ids. Only tabi's 2026-10-20T20:49:06Z fetch is a
   genuinely earlier date.
4. `tsukuroi-shokunin/corpus/SOURCES.md:83,88` carry the *pinned* `/2.56.0` URL, so they are not in the
   population and their rows do not witness the population URL's continuity; counting them as shared rows
   would inflate the overlap from 20 to 22 without adding freshness evidence.

## 5. Proposed move (one, bounded)

**Move.** In `corpus/evidence/recheck-r32/README.md` — already contract-required and already in the counter's
new-source check — add a nine-line "cross-lane continuity" block: for S047 and S064 record sibling lane, row,
`fetchedAt`, raw sha256 and the *equal normalised-text sha256* with both reproduction commands; for S044 S045
S046 S049 S058 S069 S073 record only the sibling row line and the version marker it names, labelled
`version-marker agreement, not a date interval`; then one rule sentence: raw-digest inequality across fetches
is not drift (cite `tabi-shokunin/corpus/lessons/round-12.md:35` and
`source-recheck-round-18.md:143`), and no sibling verdict sets mori's verdict (`QUALITY.md:104`). Nothing in
the `## Recheck` table changes.

**Axes.** Freshness (AXES.md:14, "drift detection — claims re-verified against live surfaces; stale items
flagged") improves: two rows move from a single snapshot to a measured two-date no-change interval, seven get
a second lane's independent version or mutability-marker reading, and the README names the exact
false-positive mode (raw digest across runs) that would otherwise manufacture a `drifted` verdict and
needless `Round32` corrections under R5.
Depth, coverage, adjacency, calibration and operability are untouched; calibration is if anything improved by
stating the limit. Cost: zero fetches, zero row edits, no counter edit.

**Why non-obvious.** The round treats each row as one fetch. The only other lane that archives source bytes
(tabi — the sole lane with `rowUrl` receipts, 51 of them) happens to hold the same two pages from 2 d 5 h
earlier, and the counter's own normaliser is what turns "different digests" into "same text". Neither fact is
visible from the population file, and the one label a naive reader would copy (`drift`) is wrong.

**Risks.** (a) A judge may read the block as claim inflation; mitigate by the explicit "corroboration only,
verdict stays quote-driven" sentence and by citing QUALITY #41. (b) The tabi files must be cited at content,
not at a moving tip: they are tracked and clean today, so cite path + digest; a later tabi revision could
rewrite the note, and the digest is what a reviewer can still check. (c) It must not be generalised: the
identity holds for two pages, not the 29.
(d) If L1 prefers the README minimal, the same four digests fit in the wave evidence file, but README is the
only contract-named document, so leaving them out loses them.

**Verification.** (1) The frozen predicate must be unmoved: `count-c1.py <rev>` still prints `rows_ok=34/34`,
`new_ok>=1`, `C1=met exit=0`. (2) The interval claim reproduces read-only:
`gunzip -c tabi-shokunin/corpus/evidence/round-18/source-recheck/S051.body.gz | sha256sum` = `d7069044…`,
`python3 .ufo/waves/round-32/seat-check.py text corpus/evidence/recheck-r32/S047.src | sha256sum` =
`b9c0c595…`, and the same commands on `S052.body.gz` with `recheck-r32/S064.src` give `1e84fc20…` and
`01e80bf0…`. (3) A non-author reviewer can rerun (2) at the tip without network.

## 6. Routed observations (not part of the move)

- S056 (PNAS) already has a six-try transcript `corpus/evidence/recheck-r32/S056.fetch.txt`: every try
  `exit=22 http=403`, `cf-mitigated: challenge`, and the seat's counter cross-check yielded 0 bodies. The
  `unreachable` branch is being handled per contract; no bot challenge was attempted.
- Duplicate-URL pairs already saved identical bytes for both ids (S015=S037, S069=S073, S128=S149 —
  `sha256sum` equal), which is what the binding rule permits; the counter still fetches each row's URL, so a
  quote valid for one twin must exist in the page (it does, same bytes).
- `corpus/lessons/round-32.md` does not exist yet at scan time; only copies were present. Row drafting is
  still open, so this proposal is pre-row, not retroactive.
