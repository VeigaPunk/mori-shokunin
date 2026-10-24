# MutHeadingCheck — mutation test of `.ufo/waves/round-28/check-heading-time.py` @ `f2de0e`

**Verdict: `breaks`** — the QUALITY 83 checker has one real fail-open (a heading whose file is
**renamed** is bound to the rename commit, not the commit that wrote the line, so a future-dated
heading passes); 8 of 23 mutants survive the assigned detector — 7 are killed only by scenarios
outside the task's named families, and 1 (`M17`) is a **Python-version-dependent crash**, equivalent
on 3.11+ and fatal on ≤3.10.

- Target `f2de0eedcd60d2e354da75265ea6122bc3896073:.ufo/waves/round-28/check-heading-time.py`;
  pristine committed bytes sha256 `2ef80ed1fc546364c30fbc4ccc8de8375dba542cae45ec5126770795f0eeb040`;
  harness-adapted pristine sha256 `db5cb98e47da6ae42548f72a93ac84d6013073f89776cdb6230b2c1638d15706`.
- Lane file **unchanged**: `sha256sum .ufo/waves/round-28/check-heading-time.py` = `2ef80ed1…` =
  `git show f2de0e:…`; `git diff --stat f2de0e -- <file>` prints nothing. Scratch:
  `/fast/scratch/hyaku/mori-r28-w2/MutHeadingCheck/` (clone `--no-hardlinks`, fixture clone,
  harness). Lane tree, jj state and git index untouched (`git status` shows only pre-existing
  untracked `.scratch/`, `w1/FixR1Runway.md`, `wave1-run.err`).

- **The task's two named runs.** round-27 W1 must fail: `python3 -I -B
  .ufo/waves/round-28/check-heading-time.py f2de0e .ufo/waves/round-27/contract.md` → exit **1**,
  `stated=2026-10-22T15:55Z granularity=instant added_by=dd4dbb20a601 cI=2026-10-22T12:50:10-03:00
  verdict=FUTURE-DATED`, `headings=2 future_dated=1` (the second heading, the appended correction, is
  `day`/`ok`); at `df886be1` (criterion 83's reference rev) exit **1**, `headings=1 future_dated=1`.
  Round-28 must pass: the same script on `.ufo/waves/round-28/contract.md` @ `f2de0e` → exit **0**,
  `headings=1 future_dated=0`; its one dated heading (`## Correction to round-27 amendment W1
  (appended 2026-10-22, …)`) is `granularity=day verdict=ok`, `added_by=079a47c61691`,
  `cI=2026-10-22T14:56:06-03:00`. **No failing heading to name.**

## Method, baseline, and how kills are counted

One harness adaptation, applied **identically** to pristine and every mutant, so it is never a
mutation: `LANE = "/home/vgpnk/..."` → `LANE = os.environ.get("MORI_LANE", "/home/vgpnk/...")`
(plus `import os`). It only redirects which repo the script reads; every behavioural byte is
untouched. Per mutant: pristine bytes → mutate → run the **same** bounded detector → restore →
assert the restored sha256 equals the pristine-adapted sha256. All 23 mutants restored cleanly
(`RESTORE final sha256 db5cb98e… equals pristine-adapted: True`).

Expected values come from an **independent oracle** — the checker's own documented method
`git log --reverse -S<line> -- <path>` run directly through git, plus criterion 83's stated
granularity and bound rules (`corpus/QUALITY.md:383-401`); the oracle never calls the script under
test. Kill accounting is baseline-aware: only a scenario that **passes on pristine bytes** can kill
a mutant; one already failing on pristine bytes is a **finding about the checker**, never a kill.
**Tier A** = the families the task names (date-only, zone-less, full instant; a line moved between
commits; a heading added in a merge; round-27 W1 must fail; round-28 must pass). **Tier B** = the
remainder of criterion 83 (exit codes, level-1 scope, `--bound`/`--heading` options, UTC-offset
commits). Baseline: tier A **20/20 PASS**, tier B **10/10 PASS**; one scenario fails on pristine —
a finding, not a kill (F1).

## F1 — fail-open: a renamed file rebinds a future-dated heading (baseline failure)

Contract-derived expectation: `## Moved (2026-10-20 ~14:00)` was written at `2026-10-20T09:00:00-03:00`
(A7) and the file renamed at `2026-10-21T09:00:00-03:00` (A8). The heading claims 14:00 on
2026-10-20 — **later than the commit that wrote the line** — so the check must bind to A7 and report
`FUTURE-DATED`. It does not; it prints `heading mut/move-dst.md:3 stated=2026-10-20 ~14:00
granularity=local-minute added_by=ea70081d2eea aI=2026-10-21T09:00:00-03:00
cI=2026-10-21T09:00:00-03:00 bound=2026-10-21T09:00:00-03:00 delta_s=68400 verdict=ok` and
`headings=1 future_dated=0` (exit 0).

Cause: `adding_commit` (`:77`) runs `git log --reverse -S<line> rev -- path`. The `-- path` filter
plus git's rename detection makes the rename commit A8 the only hit on the destination path; the
same pickaxe **without** the path filter returns A7 (`7b8252be3275`, cI `2026-10-20T09:00:00-03:00`),
the true adding commit. Verified: `-S<line> <A8> -- mut/move-dst.md` → `ea70081d2eea` (the rename);
`-S<line> <A8>` (no path filter) → `7b8252be3275` (the authoring commit);
`git log --name-status -1 <A8>` → `R100 mut/move-src.md mut/move-dst.md`. Consequence:
**renaming or moving a contract file makes any future-dated heading in it pass.** `git log --follow`
does not help (`-S` + `--follow` returns nothing: `--follow` needs a single path and the pickaxe
count is per-blob). M07 further shows the ordering is load-bearing: the same `-S` mechanism binds a
heading to the commit that **last** added it in that path, not the first.

## F2 — M17 is a Python-version-dependent crash (equivalent mutant on 3.11+)

`parse_iso` (`:43-46`) rewrites a trailing `Z` to `+00:00` before `fromisoformat`. Git emits `Z`
for UTC-offset commits (`%aI`/`%cI` → `2026-10-30T10:00:00Z`, confirmed on fixture commits A27/A28
and upstream commit `5b576560c2bf`). On Python ≥ 3.11 `fromisoformat` accepts `Z` natively, so
deleting the branch is **behaviourally equivalent** there (hence the survivor); on Python ≤ 3.10 it
is **fatal** — `uv run --python 3.10 --no-project python -I -B /tmp/m17.py <A27> mut/utc.md` →
`ValueError: Invalid isoformat string: '2026-10-30T10:00:00Z'` (exit 1), while pristine on the
same fixture under 3.10 succeeds (`verdict=FUTURE-DATED`, exit 1). The check is invoked as
`python3 -I -B` (criterion 83) and the lane pins no interpreter version. Equivalent mutant, not a
live defect at this host's 3.14.8 — reported because the surviving branch is the only thing between
a UTC commit and a crash.

## Mutants and verdicts

Before = `db5cb98e47da` (pristine adapted) in every row; 23 mutants, one single-token edit each.
K = killed by that tier, **S** = survived it; `/B:` = tier-B-only kill.

| id | edit (line) | after sha256 | tierA(/B) | killed by |
|---|---|---|---|---|
| M01 | `<=`→`<` on date (`:145`) | `8695acc72905` | K | lane-r28-must-pass, date-only-same-day |
| M02 | date compared to UTC date (`:145`) | `1a561124b517` | K | ext-date-local-vs-utc |
| M03 | zone-less vs UTC wall clock (`:141`) | `60a8cd60a333` | K | zoneless-after-commit, merge-side-branch |
| M04 | `<=`→`<` on instant (`:138`) | `aa676247aac3` | K | instant-equal-to-commit |
| M05 | zone sign ignored (`:63`) | `3f881ebc0262` | K | instant-one-second-later |
| M06 | `Z` not UTC (`:60`) | `850b137971ce` | K | lane-r27-W1-must-fail |
| M07 | pickaxe latest-not-first (`:77`) | `e960063e20e8` | K | readded-line |
| M08 | bound = author time (`:134`) | `be157b9eb3eb` | K | ext-bound-committer-not-author, ext-r17-honest-text |
| M09 | `no_adding_commit` passes (`:130`) | `ff6f428087ea` | K | merge-resolution-only |
| M10 | level-1 headings counted (`:34`) | `498aecbc80cf` | **S** / B:K | ext-level1-heading-ignored |
| M11 | level-2 headings dropped (`:34`) | `e396c7f1b6a8` | K | 20 tier-A scenarios |
| M12 | bad rev → exit 0 (`:110-111`) | `b04fac241139` | **S** / B:K | ext-bad-rev-exit-2 |
| M13 | missing file → exit 0 (`:115-116`) | `cc09cbd30f44` | **S** / B:K | ext-missing-file-exit-2 |
| M14 | `--bound aI` ignored (`:134`) | `c62f25806a2e` | **S** / B:K | ext-bound-aI-option |
| M15 | `--heading` filter ignored (`:119-120`) | `d3820b01bee5` | **S** / B:K | ext-heading-filter |
| M16 | path filter dropped (`:77`) | `cd3fb10fc732` | K | duplicate-text-later-file |
| M17 | `Z` parse branch deleted (`:44`) | `fadfe630501c` | **S** / **S** | equivalent on 3.11+; fatal ≤3.10 (F2) |
| M18 | date-only → local-minute (`:57`) | `5d28f8c3c839` | K | lane-r28-must-pass, date-only-same-day |
| M19 | local-minute → instant (`:69`) | `1fa0f090bc15` | K | zoneless-after-commit, ext-r17-honest-text |
| M20 | `~` dropped from stamp regex (`:32`) | `367816de3ac2` | K | zoneless-after-commit, merge-side-branch |
| M21 | usage error → exit 0 (`:88-89`) | `32a2c5e03aa5` | **S** / B:K | ext-usage-no-args-exit-2 |
| M22 | bad arg → exit 0 (`:106-107`) | `8c1f27c79a7c` | **S** / B:K | ext-usage-error-exit-2 |
| M23 | `<rev>` ignored, HEAD used (`:108`) | `62b7505d7412` | K | moved-within-file, merge-resolution-only |

## Survivors (assigned detector) — 8, and what to do about them

The task-named families cannot kill these; each is killed only by a scenario outside them, so each
is a **coverage gap in the assigned detector**, not proof the checker is wrong. Two are
behaviour-relevant, not CLI-relevant: **M10** (level-1 headings unchecked in the lane) and
**M17** (portability).

- **M10** level-1 dated headings — `HEAD = re.compile(r"^#{2,6} .*$")` (`:34`) skips `#` headings.
  The lane has one today: `# mori round 17 — shared seat contract (L1-authored, 2026-10-20)`
  (`273aa74`, cI `2026-10-20T16:31:56-03:00`) — the exact case criterion 83 uses as its honest-text
  example — and it is **not** checked. Killed by ext-level1-heading-ignored.
- **M12 / M13 / M21 / M22** exit codes — bad rev (`:110`), missing file (`:115`), usage (`:88`), bad
  arg (`:106`). Criterion 83 requires exit 2 in all four; the task-named families exercise only
  exit 0 and 1. Killed by the four ext exit-code scenarios.
- **M14** `--bound aI` — a documented CLI flag (`:99-103`) no named family uses. Killed by
  ext-bound-aI-option. **M15** `--heading` filter — documented (`:96-98`, `:119-120`), likewise
  unused. Killed by ext-heading-filter.
- **M17** `Z` parse branch — the one survivor no scenario kills, because it is **equivalent** on
  Python ≥ 3.11. See F2; fatal on ≤ 3.10, and the lane pins no interpreter version.

Recommendations (findings only; the contract is not changed here):

1. **F1** is a genuine fail-open: bind the pickaxe to the commit that **first** added the line,
   across renames. A tree-wide `-S` (no `-- path`) finds A7 correctly but must then be
   disambiguated per file — M16 shows the path filter is load-bearing, since without it two files
   sharing a heading text bind to the wrong commit. The fix needs both halves; not implemented here.
2. Add the level-1 heading case (M10) and the four exit-code cases (M12/M13/M21/M22) to whatever
   exercises criterion 83, so the assigned detector can see them.
3. Pin the interpreter (criterion 83 invokes `python3`): `fromisoformat` gained `Z` support in
   3.11, and the checker's own `Z` branch is the only thing protecting ≤ 3.10.

**Reproduction and tools.** `cd /fast/scratch/hyaku/mori-r28-w2/MutHeadingCheck &&
python3 build_fixture.py && python3 harness.py` (rebuild fixture; baseline, verdicts, restore
proof). `final_run.txt` holds the recorded run. The harness reads the lane read-only via
`git -C … show`; it never writes into the lane. No installs were needed; nothing was added or
upgraded on this host. Python 3.14.8 (host `python3`); 3.10.22 via pre-existing `uv` at
`~/.local/bin/uv` (`uv run --python 3.10`, ephemeral interpreter, no system change) — used only to
confirm F2; git 2.56.0; `bash`, `sha256sum`, `grep`/`sed` for the lane read-only queries.
