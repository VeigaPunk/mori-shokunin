# MisrootBaseline — fleet-root working-tree baseline for the round-25 end sweep

Seat: MoriR25.MisrootBaseline (leaf; read-only). Instant of record: **2026-10-22T10:01:22Z**.
Fleet root: `/home/vgpnk/Projects/shokunin`, branch `main`, HEAD
**`31ba19ee06278abe5f6cfd5f9a4c07dbc9d1363e`** (committed 2026-10-22T07:00:02-03:00).
First read at 09:58:58Z saw HEAD `7c19c9e`; the fleet repo is live (see §7).

No file was moved, deleted, or written outside this report. No tool was installed.

## 1. Command and result

```
$ git -C /home/vgpnk/Projects/shokunin status --porcelain ; echo exit=$?
exit=0
```

There are **no `??` lines at 09:58:58Z**. Exactly one appears later, when a sibling seat writes
its report `.ufo/waves/round-51/falsify/ReopenS113.md` at 10:00:43Z. Snapshot bytes:

| Snapshot | Taken (UTC) | Lines | SHA-256 of porcelain bytes |
|---|---|---|---|
| S1 | 2026-10-22T09:58:58Z | 17 | `3ee62a15426661a518f2bfd17ae4955291226cc65dfaead4a48ce70443578c84` |
| S2 | 2026-10-22T10:00:44Z | 18 | `732dd5878f5cc60ec6bb330a8358e1ea409936926bdabafcd835203448f731d7` |
| S3 | 2026-10-22T10:01:22Z | 18 | same `732dd5…` (S2→S3 delta empty) |

S1→S2 delta is one line: `?? .ufo/waves/round-51/`. S3 verbatim:

```
 A .scratch/goal-20261022-hyaku-12h.md
 M .ufo/state/chousa.report-baseline
 M .ufo/state/kagi.report-baseline
 M .ufo/state/kaidoku.report-baseline
 M .ufo/state/kake.report-baseline
 M .ufo/state/kama.report-baseline
 M .ufo/state/kengaku.report-baseline
 A .ufo/state/kotoba.report-baseline
 A .ufo/state/kotodama.report-baseline
 M .ufo/state/kumitate.report-baseline
 M .ufo/state/mori.report-baseline
 A .ufo/state/revenger.report-baseline
 M .ufo/state/tameshi.report-baseline
 M .ufo/state/tsukuroi.report-baseline
 M .ufo/watchdog.log
 A scripts/hyaku/__pycache__/append-closure.cpython-314.pyc
 A write
?? .ufo/waves/round-51/
```

## 2. Untracked (`??`) paths, with mtime

| Path | Kind | mtime local (-0300) | mtime UTC | Size (B) | mori / round 25 in content |
|---|---|---|---|---|---|
| `.ufo/waves/round-51/falsify/ReopenS113.md` (dir collapsed as `.ufo/waves/round-51/`) | file | 2026-10-22 07:00:43.844 | 2026-10-22T10:00:43Z | 26,024 (25,718 at 10:00:19Z, still being written) | none |

`grep -aoF` counts over its bytes: `mori` 0, `Mori` 0, `round 25` 0, `round-25` 0, `R25` 0,
`r25` 0. It is KotodamaR51a3.ReopenS113's seat report ("# ReopenS113: re-open of SOURCES rows
S113 to S118 (round 51, attempt 3, falsify)", line 1) — another lane's artifact, recorded only.

## 3. Paths not in HEAD but not reported as `??` (staged adds, `A`)

All six fail `git cat-file -e HEAD:<path>` (exit nonzero ⇒ absent from HEAD).
Marker counts from `grep -aoF` per token.

| Path | mtime local | mtime UTC | Size | mori | round 25 / round-25 / R25 | Notes |
|---|---|---|---|---|---|---|
| `.scratch/goal-20261022-hyaku-12h.md` | 2026-10-22 04:54:00.451 | 2026-10-22T07:54:00Z | 17,367 | **2** | 0 / 0 / 0 (but `r25` **6**) | Only non-HEAD path naming mori or a round-25 lane id; lines 86–87, 99, 102, 104, 106 of a 12h goal/strategy table (e.g. line 102 `\| B4 \| mori (r24) \| …`, line 99 `\| A1 \| tameshi (r25) \| …`). |
| `.ufo/state/kotoba.report-baseline` | 2026-10-22 06:30:26.994 | 2026-10-22T09:30:26Z | 68 | 0 | 0 / 0 / 0 | `25 e3b0c442…` (sha256 of empty string) |
| `.ufo/state/kotodama.report-baseline` | 2026-10-22 06:19:48.257 | 2026-10-22T09:19:48Z | 68 | 0 | 0 / 0 / 0 | same 68-byte shape |
| `.ufo/state/revenger.report-baseline` | 2026-10-21 14:54:50.930 | 2026-10-21T17:54:50Z | 68 | 0 | 0 / 0 / 0 | same 68-byte shape |
| `scripts/hyaku/__pycache__/append-closure.cpython-314.pyc` | 2026-10-22 05:01:42.512 | 2026-10-22T08:01:42Z | 10,738 | 0 | 0 / 0 / 0 | byte-level `grep -a`; committed-byproduct class (cf. contract D4) |
| `write` | 2026-10-21 19:52:50.857 | 2026-10-21T22:52:50Z | 25 | 0 | 0 / 0 / 0 | **misroot**: literal filename `write` whose content is `agent://U100N079H334f935b`, no trailing newline — a `write` call that received an agent URI as its path. |

## 4. Empty directories at the fleet root (invisible to git, hence never in `status`)

| Path | Files | mtime local | mtime UTC | Observation |
|---|---|---|---|---|
| `bash: ` (name has a **trailing space**) | 1 | 2026-10-18 14:01:47.326 | 2026-10-18T17:01:47Z | **misroot**: nested tree `bash: /home/vgpnk/Projects/shokunin/souji-shokunin/tests/tools/` holding one 10,139-byte file named `souji-verify.sh: No such file or directory` — a shell command captured as a path. Ignored because a path component matches `.gitignore:1` `*-shokunin/` (`git check-ignore -v` agrees). No mori/round-25 content. |
| `local/` (`local/fleet-analysis/`) | 0 | 2026-10-19 18:12:36 | 2026-10-19T21:12:36Z | empty |
| `reports/` | 0 | 2026-10-18 13:05:53 | 2026-10-18T16:05:53Z | empty |
| `mori-shokukin/` (misspelled) | 0 | 2026-10-21 09:53:32 | 2026-10-21T12:53:32Z | empty chain `mori-shokukin/.ufo/waves/round-21/` |
| `tameshi-shokukin/` (misspelled) | 0 | 2026-10-21 02:50:33 | 2026-10-21T05:50:33Z | empty chain incl. nested `tameshi-shokunin/.ufo/waves/` |
| `.ufo/waves/round-25/` (fleet root) | 0 | 2026-10-22 06:46 | 2026-10-22T09:46Z | empty (plus empty `build/`); `git ls-files .ufo/waves/round-25` = 0. Distinct from the lane's contract dir. |

`.ufo/reports/round-25/` is **tracked** (6 files: chousa, kagi, kake, kengaku, kotodama,
tameshi `.md`) and unmodified, so it is not part of this baseline.

## 5. Ignored-but-present trees (diff target, not `??`)

`git ls-files --others` (no exclusions) = **321** paths; `--exclude-standard` = 0 at 09:58:58Z.
Grouped by first segment:

| Segment | Paths | Ignore source |
|---|---|---|
| `.tower/` | 139 | `.git/info/exclude:8` `.tower/` |
| `.jj/` | 120 | repo internals |
| `.ufo/` | 37 | `.gitignore:5` `.ufo/waves/*/*-scratch/` (36 files dated 2026-10-13/14) + the round-51 report |
| `.ruff_cache/` | 3 | `.ruff_cache/.gitignore:2` `*` |
| `*-shokunin/` lane repos | 21 | `.gitignore:1` `*-shokunin/` (each is its own git/jj repo) |
| `bash: ` | 1 | via the `*-shokunin/` component inside its embedded path |

## 6. Content-marker sweep (`grep -l` semantics)

Marker set: `mori`, `Mori`, `MORI`, `round 25`, `round-25`, `Round 25`, `R25`, `r25`.

* Only non-HEAD path with a semantic mori / round-25 hit: `.scratch/goal-20261022-hyaku-12h.md`
  (`mori` ×2, `r25` ×6 — both exact-case).
* Incidental hits in old ignored scratch/path listings, not prose claims:
  `.ufo/waves/shokunin-train-20261013-w5/xsentinel-scratch/new-w5-files.txt` (4 lines),
  `.ufo/waves/shokunin-train-20261101-w10/xsentinel-scratch/audio-5415115-swept-files.txt`
  (7 lines), `.tower/quarantine/kaika-fleetroot-20261019/aggregate-README.md` (2 lines).
  [INFERENCE] these are path inventories from 2026-10-13/14, not round-25 artifacts.
* No hit in: `write`, the `bash: ` misroot file, the pyc, the three untracked baselines,
  `ReopenS113.md`, or any empty directory (no content).

## 7. Volatility and what moved during the run

* HEAD moved `7c19c9e` → `31ba19e` (author `protocol-shokunin`, "hyaku phase3: kake r28 landed to
  closure; tsukuroi r25 dispatched"); `git show --stat 31ba19e` = `.ufo/waves/hyaku/PHASE3.md` +8 only.
* `.ufo/watchdog.log` was 54,927 B at 06:58:58.444 local (09:58:58Z) and 55,021 B at 06:59:30
  (09:59:30Z) — live writer; any size/hash of it is instant-bound.
* `.ufo/waves/round-51/falsify/ReopenS113.md` grew 25,718 → 26,024 B between 10:00:19Z and 10:00:43Z.
* `.ufo/state/mori.report-baseline` mtime **09:42:02.194Z** exactly matches the contract's L1
  dispatch stamp, so the state-baseline cluster 09:19–09:59Z is this round's dispatch traffic.
* Tracked-modified paths and mtimes (UTC): chousa 2026-10-21T23:38:09Z; kagi 2026-10-21T17:32:03Z;
  kaidoku 2026-10-22T09:19:46Z; kake 09:26:14Z; kama 09:19:50Z; kengaku 2026-10-21T17:32:03Z;
  kumitate 09:43:13Z; mori 09:42:02Z; tameshi 09:52:10Z; tsukuroi 09:59:28Z; watchdog.log 09:58:58Z.

## 8. Suggested end-of-round diff

1. `git -C /home/vgpnk/Projects/shokunin status --porcelain` versus S3 (17→18 lines, hash
   `732dd5…`); the only expected new `??` from this round is `.ufo/waves/round-51/`.
2. Re-run the grouping `git ls-files --others | awk -F/ '{print $1}' | sort | uniq -c` and compare
   with 139/120/37/3 (plus 21 lane repos + `bash: `).
3. Re-stat the six §3 paths and the six §4 dirs; a new empty dir or a new literal `write`-like file
   is the misroot signature this baseline is meant to catch.

## 9. Confidence and gaps

* High confidence: every git-classified fact (§1–§3, §5), because it comes from `git status`,
  `git ls-files`, `git cat-file -e HEAD:<path>` and `git check-ignore -v`.
* High confidence: §4 mtimes and emptiness (`find -type f | wc -l` = 0 for all four).
* Gaps: lane repos are separate repositories and are deliberately not content-swept (they appear
  only as single ignored entries); `.jj` internals were not content-read; content markers were
  tested as fixed byte strings, so synonyms ("round twenty-five", "MORI-r25-dispatch") would not
  match. The snapshot is instant-bound; use S3's hash as the anchor, not bare re-runs.
