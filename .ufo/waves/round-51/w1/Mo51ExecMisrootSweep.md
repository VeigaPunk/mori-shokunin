# Mo51ExecMisrootSweep — fleet-root misroot pre-sweep (round-51 wave w1, read-only)

Item: `git -C /home/vgpnk/Projects/shokunin status --porcelain` (no pathspec), list every untracked file at the
fleet root or under `/home/vgpnk/Projects/shokunin/.ufo` that could belong to mori round 51, and
`git -C /home/vgpnk/Projects/shokunin/mori-shokunin status --porcelain --ignored` for stray files outside
`.ufo/waves/round-51/`. Read-only: no fleet repo, lane, sibling-lane, jj or git-index mutation was made by this seat.
Nothing under `.ufo/state/`, `.scratch/` or another lane was opened, changed or removed (only path names were read
from `git status` output, which is why `.ufo/state/mori.*` appears below as an excluded category).

MACHINE_ID: MACHINE_ID (redacted). Date of observation: 2026-10-26, 19:46–19:52 -03.
Scratch: `/fast/scratch/hyaku/mori-r51/Mo51ExecMisrootSweep/` (`mkdir -p`, only `cd` into it; removed before finish).
Disk guard before the run: `/tmp` 4 % / 124.0 GiB free, `/var/tmp` 35 % / 584.8 GiB free, `/fast/scratch/hyaku`
25→26 % / ~597 GiB free. No tool install or upgrade was needed.

## 1. Fleet-root status (exact readings)

At the start of the sweep the fleet root was **dirty**:

```
$ git -C /home/vgpnk/Projects/shokunin status --porcelain          # no pathspec
?? .ufo/waves/round-51/
$ echo $?
0
$ git -C /home/vgpnk/Projects/shokunin status --porcelain --untracked-files=all
?? .ufo/waves/round-51/w1/Mo51ConnSiblings.md
?? .ufo/waves/round-51/w1/Mo51CritEntail12.md
$ echo $?
0
```

The plain form collapses the new directory to one line; with `-uall` the two files are visible. Both were created by
this wave today (`Mo51CritEntail12.md` mtime 19:45:05, `Mo51ConnSiblings.md` mtime 19:46:19) and
`git check-ignore -v` on both returned rc 1 (no ignore rule matches), i.e. they were real untracked repo content,
not caches: any `git add -A` at the fleet root would have staged them.

At 19:51:26 the fleet root was **clean**, and `/home/vgpnk/Projects/shokunin/.ufo/waves/round-51/` no longer
existed:

```
$ git -C /home/vgpnk/Projects/shokunin status --porcelain ; echo $?          # 0 lines
$ git -C /home/vgpnk/Projects/shokunin status --porcelain -uall ; echo $?    # 0 lines
$ ls -d /home/vgpnk/Projects/shokunin/.ufo/waves/round-51
ls: cannot access '.../.ufo/waves/round-51': No such file or directory
```

The bytes were **moved into the lane, not lost**: at 19:51:30 the destination files existed with the same size,
the same original mtimes and the same sha256 as the fleet-root copies I hashed minutes earlier (mtimes preserved
⇒ a move, not a rewrite). Who moved them is UNVERIFIED (no seat reported it to me; the L1's integrator is the
plausible actor). Net result: no copy is outstanding, but the event is a real wave-time misroot and is recorded
below with the copy command that both uncovers and verifies that class.

## 2. The two files — evidence they are mori round-51 wave w1 reports

Destination (lane) paths, verified present at 19:52:20:

| file | size | mtime | sha256 |
|---|---|---|---|
| `mori-shokunin/.ufo/waves/round-51/w1/Mo51ConnSiblings.md` | 13717 | 19:46:19 | `c85e3277fcc0150c38b4df16d0391045829459b8195d1183aa5ac3775e72f720` |
| `mori-shokunin/.ufo/waves/round-51/w1/Mo51CritEntail12.md` | 8318 | 19:45:05 | `351684a681c198007bbc1dd84889aa8f7fd909fd9e1bde92ae5d5b3012797b13` |

Evidence of ownership (all read from the bytes, not inferred):

1. **Dispatch spec names the seats and the lane-relative output.** `mori-shokunin/.ufo/waves/round-51/w1-spec.json`
   has `items[9].name = Mo51CritEntail12` (role critic, "ENTAILMENT item (adversarial second vote) … rows 12-16 of the
   `## Claims` table of /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/knowledge/memavailable-estimate-r51.md at
   87e0c374…") and `items[26].name = Mo51ConnSiblings` (role connector, "Sibling-overlap scan … MemAvailable /
   meminfo / memory runway knowledge"). `w1-dispatch.json` carries both spawn entries and, in the task text,
   `Report: write your scoped findings to .ufo/waves/round-51/w1/Mo51ConnSiblings.md` and
   `Report: write your scoped findings to .ufo/waves/round-51/w1/Mo51CritEntail12.md` — lane-relative, i.e. the
   fleet-root paths were never intended.
2. **File bodies cite the lane and the round's data commit.** `Mo51CritEntail12.md:1-10` names
   `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/knowledge/memavailable-estimate-r51.md` at
   `87e0c374537557754bf71dd68036ded3ddc6699c`, quotes `evidence/c2-hashes-at-data.txt`, and names scratch
   `/fast/scratch/hyaku/mori-r51/Mo51CritEntail12/`. `Mo51ConnSiblings.md:1-8` names "round-51 wave w1", mori's
   `corpus/knowledge/memavailable-estimate-r51.md` and scratch `/fast/scratch/hyaku/mori-r51/Mo51ConnSiblings/`.
3. **No other copy exists anywhere.** `find /home/vgpnk/Projects/shokunin … -name 'Mo51*'` (pruning `.jj`, `.git`,
   `node_modules`) reported only these two fleet-root files plus the lane's own `w1/Mo51*.md` set;
   `grep -rIl 'Mo51ConnSiblings|Mo51CritEntail12'` reported only the two files plus
   `w1-spec.json`, `w1-dispatch.json`, `w1/swarm-registry.json`, `w1.ready.dispatched`.

Copy-and-verify command for this class (idempotent; `--no-clobber` so a complete lane copy is never replaced by a
partial one, `cmp` proves the bytes):

```
SRC=/home/vgpnk/Projects/shokunin/.ufo/waves/round-51/w1
DST=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-51/w1
for f in Mo51ConnSiblings.md Mo51CritEntail12.md; do
  cp -p --no-clobber "$SRC/$f" "$DST/$f" && cmp "$SRC/$f" "$DST/$f" && echo "ok $f"
done
```

Observed resolution instead: `cmp` of the (now absent) fleet-root source returned rc 2 ("No such file or
directory") and the destination sha256 equals the recorded source sha256 — the files are in place.

## 3. Fleet root and `.ufo` — full untracked/ignored census

`git -C /home/vgpnk/Projects/shokunin status --porcelain --ignored --untracked-files=all` produced 8724 lines
(snapshot taken 19:49:16, while the fleet-root copies still existed; by 19:52:13 the same command returned 0 lines).
Grouped by leading components:

| group | lines | mori-51 relevance |
|---|---|---|
| `.jj/repo/**` (jj store internals) | 8426 | none — jj's own store, not work files |
| `.tower/comms/**` | 111 | none (coordination substrate, not read) |
| `.ufo/state/**` (`mori.mission`, `mori.out`, `mori.report-baseline`, `mori.round`, …) | 82 | fleet dispatcher state — **excluded by rule**, never touched |
| `.tower/quarantine/**` | 41 | none (not read) |
| `.ufo/waves/shokunin-train-2026*/x*-scratch/**` | 36 | none — every one is an older `shokunin-train` wave scratch file; no line names mori, round 51 or Mo51 |
| `.jj/working_copy/*`, `.jj/.gitignore` | 4 | none |
| nested lane repos (`mori-shokunin/`, `kasegi-shokunin/`, … 21 entries) | 21 | nested-repo markers only; each lane's own status was out of scope except mori's |
| `.ufo/watchdog.log` | 1 | none |

Targeted filters: `grep -iE 'mori|round-51|Mo51'` over the same list returned only the two untracked files above,
the four `.ufo/state/mori.*` entries (excluded) and the `mori-shokunin/` nested-repo marker. There is **no other**
untracked or ignored file at the fleet root or under `.ufo` that belongs to mori round 51. `.ufo/prompts/mori-round-51.md`
and `.ufo/prompts/closure/*` are tracked (`git ls-files` shows them), i.e. not strays.

## 4. Lane `status --porcelain --ignored` — strays outside `.ufo/waves/round-51/`

`git -C /home/vgpnk/Projects/shokunin/mori-shokunin status --porcelain --ignored` = 13 lines (the plain form collapses
`.jj/` to one line and rounds the wave files up to their directories); with `-uall` at 19:53:20 it is 10185 lines,
of which 10109 are `.jj/**` internals; the remaining 76 are 57 `??`/`!!` entries under `.ufo/waves/round-*`
(the wave's own reports, `w1.ready*`, `swarm-registry.json`, per-round `__pycache__` and the transient selftest
scratch of (b)), 15 `!!` per-round `__pycache__` entries and 4 `!! tools/__pycache__` entries. After removing the
`.jj/` store, the round-51 wave directory and Python byte-code caches, the lane has these entries outside
`.ufo/waves/round-51/`:

**(a) Ignored tool caches — 4 files, benign**

```
!! tools/__pycache__/mori-gate-registry.cpython-314.pyc   49199  2026-10-25 07:55:55
!! tools/__pycache__/mori-pin-check.cpython-314.pyc       70114  2026-10-25 19:36:37
!! tools/__pycache__/mori-round19-regressions.cpython-314.pyc 80266 2026-10-25 07:45:25
!! tools/__pycache__/mori-source-drift.cpython-314.pyc    26369  2026-10-26 19:45:46
```

All match `.gitignore:2-3` (`__pycache__/`, `*.pyc`); they are import caches from running the lane's tools during
this wave (the `mori-source-drift` cache is from today 19:45:46). No counter reads them.

**(b) Live in-lane conform-selftest scratch — transient, observed while running**

Two selftest working directories appeared inside the lane during the sweep. They are produced by the registered
conformance pins (`SKILL.md:910` round-39 `conform.py --selftest`, `SKILL.md:911` round-40), whose selftest does
`tempfile.mkdtemp(prefix="mori-conform-selftest-", dir=SCRATCH_ROOT)`:

- `.ufo/waves/round-39/scratch/mori-conform-selftest-4m82s7b4/` — 7 files `counter-{predicate,head_pin,
  tool_resolve,bounded_reads,timeout_state,timeout_value,drain_shape}.py`, 22498–22536 bytes, mtimes
  19:50:13–19:50:32; **gone by 19:51:13** (the selftest's `finally` cleanup). The empty parent
  `.ufo/waves/round-39/scratch/` (mtime 19:51) remains; git does not track empty dirs, so it is invisible to
  `status`.
- `.ufo/waves/round-40/scratch/mori-conform-selftest-ux20v9vq/` (mode 0700) — 9 files `counter-*.py`
  (`predicate`, `head_pin`, `tool_resolve`, `bounded_reads`, `timeout_scope`, `timeout_scope_shadow`, `drain_bind`,
  `drain_bind_decoy`, `timeout_state`), still being written at 19:52:03 and still present at 19:52:20. These show as
  `??` (untracked, not ignored: `git check-ignore` rc 1) for as long as the run lasts.

Provenance, by code (not by attribution):

- `mori-shokunin/.ufo/waves/round-39/conform.py:54` — `SCRATCH_ROOT = os.path.join(LANE, ".ufo", "waves",
  "round-39", "scratch")`; `:491-492` `os.makedirs(SCRATCH_ROOT, exist_ok=True)` then the `mkdtemp`. Round-39 was
  **not** touched by C1, so its selftest still writes inside the lane whenever it runs there.
- entering `aa3af1ec:.ufo/waves/round-40/conform.py:69-70` — `LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"`,
  `SCRATCH_ROOT = os.path.join(LANE, ".ufo", "waves", "round-40", "scratch")`; landed
  `87e0c374:.ufo/waves/round-40/conform.py:71-72` — `LANE` derived from `__file__`, `SCRATCH_ROOT =
  tempfile.gettempdir()`. A lane-side `round-40/scratch/mori-conform-selftest-*` therefore means a **pre-data
  (entering) copy of round-40 `conform.py`, or a run whose TMPDIR was not set, was executed in the lane** — the
  exact residue class C1 arm A measures in a clone, observed live here in the working tree.
- The pre-existing contents of `.ufo/waves/round-40/scratch/` (`mutconform-arms2/`, `selftest-v3-draft.txt`,
  `selftest-v3-draft2.txt`, 09:07 today) are **tracked** (`git ls-files -s` shows them in the index), i.e. round-40
  wave artifacts, not strays.

These directories self-clean, so they are not residue that needs removal; they are reported because (i) a SIGKILL
mid-run leaves them as untracked lane content (the C1 arm-A hazard, reproduced in the working tree), and (ii) a
concurrent census or `status`-based sweep sees them as stray files. Attribution to a specific seat is UNVERIFIED;
several w1 seats re-run pins/controls.

Nothing else in the lane is untracked or ignored outside `.ufo/waves/round-51/`; no stray file was found in
`corpus/`, `tools/`, `.ufo/waves/round-39/` (tracked content only), `considerthese/` or the lane root.

## 5. Consequences the L1 should fold in

- **Misrooted votes are now live lane data.** `Mo51CritEntail12.md` contributes five `entailed` lines for rows
  12/13/15/16 and the replacement hash `56b7a3309d66`, plus one `overclaim` line for row 14's hash `a06f1037d952`
  (line 63 of the file, inside the fenced "Assigned verdict lines" block — the lines start at column 0, so
  `count-c2.py` counts them). P-C2 requires *no* overclaim line for a row hash: while row 14's claim cell still
  hashes to `a06f1037d952`, C2's entailment arm stays blocked on that row until the L1 replaces the claim text with
  the proposed replacement (hash `56b7a3309d66`), whose own `entailed` line is already in the same report. This is
  the seat doing its job, not a defect; it is flagged because the vote only became visible after the move.
- **Neither moved report carries a `Report:` trailer.** In fact 0 of the 35 `w1/*.md` reports present at 19:52 has
  a line beginning `Report:` (`grep -L '^Report:'` lists all 35), so path intent is recorded only in
  `w1-dispatch.json`, not in the reports. If the L1 wants the trailer rule enforced, it is a wave-wide gap, not a
  property of these two seats.
- **Fleet root is clean as of 19:52:13**; the two files are byte-identical at their lane destinations. No copy
  action is outstanding. If the fleet-root directory reappears, the `cp -p --no-clobber … && cmp` loop in §2 is the
  whole remedy.

## Findings

- **HIGH** — fleet-root misroot (observed, then resolved during the sweep): `Mo51ConnSiblings.md` (sha256
  `c85e3277…72f720`) and `Mo51CritEntail12.md` (sha256 `351684a6…2797b13`) were written to
  `/home/vgpnk/Projects/shokunin/.ufo/waves/round-51/w1/`, not to the lane path named by `w1-dispatch.json`. Plain
  `git status --porcelain` showed `?? .ufo/waves/round-51/` while the wave was running; both files are untracked,
  non-ignored content of the fleet repo. By 19:51:26 the fleet copy was gone and the lane copies were present with
  identical bytes and mtimes. Any fleet-root `git add -A` during that window would have staged wave reports into
  the fleet repo.
- **MED** — live in-lane conform-selftest scratch: `.ufo/waves/round-40/scratch/mori-conform-selftest-ux20v9vq/`
  (9 untracked `counter-*.py`, present 19:51–19:52+) and the earlier, already-cleaned
  `.ufo/waves/round-39/scratch/mori-conform-selftest-4m82s7b4/` (7 files, 19:50:13–19:50:32). Root cause in code:
  entering `aa3af1ec:.ufo/waves/round-40/conform.py:69-70` and unchanged
  `mori-shokunin/.ufo/waves/round-39/conform.py:54` put `SCRATCH_ROOT` inside the lane. A kill mid-run leaves them
  as repo-visible residue; a concurrent census sees them.
- **MED** — `mori-shokunin/tools/__pycache__/{mori-gate-registry,mori-pin-check,mori-round19-regressions,
  mori-source-drift}.cpython-314.pyc`: four ignored byte-code caches outside `.ufo/waves/round-51/`, the newest
  (mori-source-drift, 26369 bytes) written 2026-10-26 19:45:46 by this wave's tool runs. Harmless, `.gitignore`d;
  listed because the seat's second command asks for everything outside the wave directory.
- **LOW** — `mori-shokunin/.ufo/waves/round-39/scratch/` is an empty untracked directory left by the round-39
  selftest run; invisible to git and to any status-based sweep, removed only by hand.
- **LOW** — No w1 report (all 35 present at 19:52) ends with a `Report:` trailer line, including the two moved
  reports; the output path exists only in `w1-dispatch.json`. A wave-wide integration note for the L1, not a
  misroot.
