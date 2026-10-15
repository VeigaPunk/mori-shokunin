# Round 9 — scribe measurement ledger (working record)

Seat: scribe (round-9 goal wave) · lane mori-shokunin · writes only under
`.ufo/round-9/goal-wave/`. Detection and report only; fixtures `/tmp` only; no fleet writes.
This ledger carries the raw first-hand measurements the three drafts cite; it is a working
record, not a deliverable. Status: **complete at scribe clock 2026-10-15T21:31Z** —
before-side at `390ab9cd…`, after-side at the landed `1c49238a…` (both first-hand);
sibling-seat artifacts unlanded at this clock are marked `[PENDING]`.

## Pinned bytes at scribe clock

| Artifact | sha256 | Version/label |
|---|---|---|
| `tools/mori-census.sh` (r8 bytes, entering r9) | `390ab9cd2db17b9d71508639f4f61cc61646ae090b61bf48243cda3e7211cae1` | `VERSION=census-r5`, 2380 lines |
| `tools/mori-silence-cases.sh` (ORACLE — byte-frozen this round) | `448f77238c73a5c929a898dad0f0c495fd2a66cc4b90a00ae84ede69a86beeb5` | r7 oracle, 1090 lines |

Baseline commit entering the wave: `c47c888` (round-8 records; evidence `9738f1a`).

## The round-9 claim (registered)

Before: the selftest harness false-fails at 1/8–25% on a random case via a live-pipe-grep
race (r8 admission defect, `SCORECARD.md:413-422`). After: the race class is eliminated at
**every** occurrence; two independent ≥20-run batteries (one under artificial load) show
0 flakes; the production census is byte-behavior-identical (fix touches only the
`--selftest` path); selftest stays 56 cases; no new bare pipelines; the ORACLE file is
byte-frozen.

## Race class in the entering bytes (`390ab9cd…`) — sites

Harness: `run_selftest()` (`:1577`…), top-level `set -euo pipefail` (`:194`). The
`check()` helper runs the census into `$out`, then asserts with `printf '%s\n' "$out" |
grep -qE …` pipelines. Under `pipefail`, if the `printf` producer takes SIGPIPE (the
`grep -q` consumer exits on its first match and closes the pipe while `printf` still has
bytes to write), the pipeline rc becomes 141 and the assertion reads as a failed match —
a false-FAIL, randomly on whichever case hits the scheduling window.

Four occurrences in the entering bytes (grep `printf .* | grep`, selftest path):

| Site | Shape | Measured false-FAIL observed |
|---|---|---|
| `tools/mori-census.sh:1771` | `elif ! printf '%s\n' "$out" \| grep -qE "^MORI_CENSUS: ${wverdict} "; then` (verdict check) | — (class member; r8 measurements named :1783/:1809) |
| `tools/mori-census.sh:1773` | `elif printf '%s\n' "$out" \| grep -qE 'integer expected\|line [0-9]+: \[: '; then` (diagnostic-noise check) | — (class member) |
| `tools/mori-census.sh:1783` | `for re in "$@"; do printf '%s\n' "$out" \| grep -qE -- "$re" \|\| miss=…` (per-case want checks) | yes — r8: `FAIL drift: CGROUP_OOM_KILL: missing match \|FINDING CGROUP_OOM_KILL\|` (55/56) |
| `tools/mori-census.sh:1809` | same shape in `check_cli()` | yes — r8 parent battery 1/8 "missing match" on a silence case |

Note: the oracle's own `fx_hash` pipeline (`tools/mori-silence-cases.sh` — frozen) has a
`{ … || true; }` producer with a draining consumer chain (`sort`/`sha256sum`), not this
class; not in scope, not touched.

## Before-side race battery (scribe, first-hand)

Frozen `/tmp` copy of the entering bytes: `/tmp/mori-scribe-r9/before/mori-census-r8.sh`
(sha256 `390ab9cd…`, re-verified). Battery: 16 × `bash <frozen> --selftest`.

```
[started 21:08Z; completed 21:16Z]
01 rc=0 MORI_CENSUS_SELFTEST: PASS (56 cases, 56 passed, 0 failed)
02..16 rc=0 MORI_CENSUS_SELFTEST: PASS (56 cases, 56 passed, 0 failed)
BATTERY_DONE fails=0 runs=16
```

First-hand result: **0/16 false-FAILs at the entering bytes under this clock's load**
(the class is the r8-measured one — parent battery 1/8, admission seat ~25%; this
battery's 0/16 at lower scheduling pressure is below its resolving power, stated as
measured, not as evidence against the class). Raw log:
`~/.kimi-code/sessions/…/agents/agent-301/tasks/bash-87fnck57/output.log` (16 lines, all
`rc=0`) and `/tmp/mori-scribe-r9/before/` (frozen copy; no failure files written).

## After-side — the landed fix (`1c49238a`)

Landed at 21:16Z (first change seen), stable from ~21:17Z; scribe re-verified the sha
unchanged at 21:22Z / 21:23Z (multiple checks). Bytes: `tools/mori-census.sh` sha256
`1c49238a7fd87277151ff5776acfb4d62fadd9d69764a02f0ede03ef0d3902d2`, 2394 lines,
`git diff --stat` = +21/−7 vs HEAD (`390ab9cd…`). Oracle `448f7723…` byte-unchanged
(`git diff` empty at every check).

**The fix (as measured in the diff):** one capture file `OUT_FILE="$work/.last-out"`
(fixture work dir, `/tmp`), written once per case (`printf '%s\n' "$out" > "$OUT_FILE"`)
and then ALL match checks grep the FILE, never a live pipe. Every harness site from the
lesson's classification table transformed (old r5 numbering → new):

| r5 site (HEAD) | shape before | after (`1c49238a`) |
|---|---|---|
| `:1771` | `elif ! printf…\|grep -qE "^MORI_CENSUS: …"` | `:1784` `elif ! grep -qE … "$OUT_FILE"` |
| `:1772` | `got=$(printf…\|grep '^MORI_CENSUS:'\|head -n1)` — message text, `head` early-exit | `:1785` `got=$(grep -m1 '^MORI_CENSUS:' "$OUT_FILE" \|\| true)` |
| `:1773` | `elif printf…\|grep -qE 'integer expected…'` | `:1786` `grep -qE … "$OUT_FILE"` |
| `:1779` | `$( printf…\|grep -m1 -E … )` — message text | `:1792` `$( grep -m1 -E … "$OUT_FILE" \|\| true )` |
| `:1783` | `for re: printf…\|grep -qE -- "$re" \|\| miss=…` | `:1796` `grep -qE -- "$re" "$OUT_FILE" \|\| miss=…` |
| `:1809` | same shape in `check_cli` | `:1823` `grep -qE -- "$re" "$OUT_FILE" \|\| miss=…` |

(Six harness class sites, not five: the lesson's classification table groups the message
shape into one `:1779` row and misses `:1772`'s `head -n1` — my sweep found it at HEAD
`grep -n 'printf .*| *head'`. The fix converts it too; the round's "every occurrence"
mandate is met at all six.)

**Scope proof (fix touches only the `--selftest` path):**
- All 8 diff hunks have old-line starts `1572 1583 1768 1771 1779 1783 1803 1809` —
  inside `run_selftest()` (HEAD span `1571`…`2361`).
- Prefix `lines 1–1570` (everything before `run_selftest()`, i.e. the whole production
  path) byte-identical: sha256 `19772ee21887437aad3d97f1b52584d1efbfa5c1119d5cf9d027e06cc912cc8b` both sides.
- Suffix from `# ---- main` to EOF byte-identical (diff empty).
- The diff adds **no** pipeline (`|`); it removes three live pipes and file-izes two
  more; the only remaining pipe in the touched region is the pre-existing message-path
  `printf '%s' "$out" | tail -n3 | tr '\n' '|'` (consumers read to EOF — not the class).

**Race-site sweep at `1c49238a`:** `grep -n 'grep -q'` → harness: `:1786`, `:1788`,
`:1796`, `:1823` (all file-based, no writer process), production: `:636` (file-based,
safe). No `printf … | grep -q` remains anywhere in the file. Same-shaped **production**
site `:1322` (`printf | sed | grep -Fxq` inside an `if` — fail-toward-wrong-grade, the
lesson measured 88/3000 pipeline-nonzero-despite-match on its shape) is OUT of the
round's fix scope (byte-freeze); named debt, per the lesson `§classification` and its
"Limits".

**After-side battery** (frozen `/tmp` copy of `1c49238a`,
`/tmp/mori-scribe-r9/after/mori-census-r9.sh`; pinned.txt re-verified oracle unchanged):
16 × `--selftest`, then oracle ×2 (lane-root invocation), then live ×1 — plus an 8-run
extension battery (total 24).

| Check | Verbatim tail | Exit |
|---|---|---|
| selftest ×24 (16 + 8) | `MORI_CENSUS_SELFTEST: PASS (56 cases, 56 passed, 0 failed)` — all 24 runs | 0, 0 failure files |
| oracle ×2 | `MORI_SILENCE_CASES: matched=28 total=28` both (28 `PASS` case-lines each) | 0 |
| live (correct root, `live2.log`) | `MORI_CENSUS: DRIFT (findings=15 drift=14 unavailable=1 surfaces=7)`; stderr 0 B; 16/16 surface rows' key-sets identical to r8 receipt run1; finding-id set identical | 1 |

Notes: the first battery's live arm ran the frozen copy from `/tmp`, so its `LANE_ROOT`
resolved to `/tmp/mori-scribe-r9` — that run is superseded by `live2.log` (lane-root
invocation `bash tools/mori-census.sh`), and the drafts bind only `live2.log`. Census sha
re-verified `1c49238a…` before and after every arm; oracle sha `448f7723…` unchanged
throughout.

**Negative control (fail-path proof).** On a `/tmp` mutant that renames ONLY the
production-side `TMUX_SESSION_IDLE` emission (mutated lines all < 1571: comments
`:103/:142/:191` + the emission `:1516`; the harness's own expected string `:2310`
untouched): selftest `FAIL (56 cases, 55 passed, 1 failed)` rc=1 with exactly
`FAIL tmux: idle fleet session -> INFO finding, foreign session not probed: missing match
|FINDING TMUX_SESSION_IDLE .*session=fx_session idle_s=100000 threshold_s=3600 threshold_label=local|`
— deterministic (not a race), exactly the case whose want referenced the renamed token.
The fixed harness's `missing match` path still fires on genuine misses. Raw:
`/tmp/mori-scribe-r9/mut/mutant2-selftest.out` (ephemeral).

## Ledger status (final at scribe clock, 21:31Z)

After-side complete. Battery results above are first-hand at the frozen `1c49238a…`
bytes; drafts v1 (`scorecard-verdict-draft.md`, `log-entry-draft.md`, `report-draft.md`)
are built from the sections above. **Named gap:** the note-writer's `corpus/knowledge/selftest-flake-r9.md` **landed at
21:35:48Z** (its §5 carries the two ≥20-run post-fix batteries: 20 unloaded + 20 under 4
CPU hogs, 40/40 PASS, lane sha re-verified before/after — 64 post-fix runs combined with
this seat's 24; its §3 records the race as old as the harness's first commit; its §6 is
the determinism-gate recipe); `corpus/README.md` r9 index rows + the r8 known-gaps
disposition landed; `corpus/knowledge/surfaces-r8.md` defect-2 disposition landed; the r9
receipt set landed 21:40:35Z
(`flake-r9-20261015T2119Z-{selftest,selftest-battery-a,selftest-battery-b,oracle,live}.log` —
battery-a 20/20 unloaded, battery-b 20/20 under 12 owned CPU hogs all killed, oracle 28/28
with frozen re-check, live 3-run identity); still unlanded at scribe clock: SKILL.md r9
rows. The drafts mark that `[PENDING]` and the parent's acceptance must bind or
re-check it. If the census SHA moves past `1c49238a…` after this clock, the drafts'
scope proof must be re-run against the final bytes.