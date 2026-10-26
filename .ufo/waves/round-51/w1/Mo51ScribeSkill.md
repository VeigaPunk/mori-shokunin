# Mo51ScribeSkill — round 51 w1 (scribe)

Seat: Mo51ScribeSkill, leaf, no subagent dispatch. Scope: draft (fenced) the `## Round51` section for
`SKILL.md` in the style of `## Round50`, with gate-table rows for the round's two counters (the `self-test` header
cell and the eight columns as Round50 has them), the `C1` row carrying the note that
`.ufo/waves/round-51/count-c1.py` has no selftest and is exercised by controls instead; a
`### Decision row — runway reading (round 51)` table (situation | do | do not | source) built from
`corpus/knowledge/memavailable-estimate-r51.md`'s Reading rules; and a `### Pin mismatch classes (round 51)` table
(class env / stale → what it means → what the lane does).

SKILL.md was **not** edited. The section below is a draft for the L1 to append after the Round50 decision-row table
(the file currently ends at `SKILL.md:1067`; `grep -n 'Round51' SKILL.md` returns nothing).

## Behavior

1. Read the frozen contract and the receipts it names, then the two counters at the frozen bytes, then
   `tools/mori-pin-check.py` v5 to get the class rule right.
2. Built the draft from observed strings only: the C1 summary line is the one in
   `.ufo/waves/round-51/evidence/c1-at-data.txt`, the C2 summary line the one in `evidence/c2-at-data.txt`, the
   `C2_SELFTEST pass=34 fail=0` pin text from a run I made myself, and the class semantics from the tool's v5
   docstring and its code (not from prose about it).
3. Verified that the draft's two registry rows do not break the lane's own reconciler: a throwaway probe tree in
   scratch holding only the draft as `SKILL.md`, a copy of `count-c2.py`, and the five committed source copies reads
   `PIN_CHECK=met … tally_pins=1 … hidden=0 unparsed=0 no_command=0`, exit 0. The probe's first attempt (without the
   copies) read the pin as `class=env` with a `FileNotFoundError` — recorded below as a limit, not a defect of the
   draft.
4. Drafted the decision rows from the entry's five Reading rules (rows 1, 2, 3, 4, 5 of that section, each citing
   its S-ids and claim-row numbers); drafted the class table from `tools/mori-pin-check.py`'s `env`/`stale`
   definition and from what the counter's arm C requires (`env=2 stale=2`).

## Commands, exit codes, output

All commands ran with `TMPDIR=/fast/scratch/hyaku/mori-r51/Mo51ScribeSkill/tmp` and cwd
`/fast/scratch/hyaku/mori-r51/Mo51ScribeSkill` unless the line says otherwise.

### 1. The C2 selftest (the pin text the draft pins)

```
$ python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-51/count-c2.py --selftest
PASS honest_met
PASS entry_absent_unmet
PASS no_table_unmet
PASS altered_quote_unmet
PASS quote_from_wrong_copy_unmet
PASS short_quote_unmet
PASS long_quote_unmet
PASS duplicate_quote_unmet
PASS claims_floor_unmet
PASS sources_floor_unmet
PASS row_not_mined_unmet
PASS row_opened_other_day_unmet
PASS used_by_missing_unmet
PASS indented_row_ok
PASS code_indented_row_unmet
PASS pin_mismatch_unmet
PASS table_id_uncited_in_source_unmet
PASS verified_at_missing_unmet
PASS header_wrong_unmet
PASS claim_cell_short_unmet
PASS breadcrumb_identical_claims_unmet
PASS claim_echoes_quote_unmet
PASS table_inside_fence_unseen_unmet
PASS other_entry_path_unmet
PASS entail_no_votes_unmet
PASS entail_one_row_unreviewed_unmet
PASS entail_dissent_unmet
PASS entail_l1_file_ignored_unmet
PASS entail_other_dir_ignored_unmet
PASS entail_hash_of_other_text_unmet
PASS entail_hash_whitespace_folded_met
PASS entail_non_md_ignored_unmet
PASS words_beyond_counts
PASS text_copy_keeps_angle_brackets
C2_SELFTEST pass=34 fail=0
EXIT=0
```

34 lines, `fail=0`, exit 0 — the draft's pinned text `C2_SELFTEST pass=34 fail=0` is the observed last line, and it
is the same text as the frozen receipt `.ufo/waves/round-51/evidence/selftest-c2.txt` (`tail`: `C2_SELFTEST pass=34
fail=0`, `exit=0`). Eight of the 34 are the entailment arm's (`entail_*`).

### 2. count-c1.py has no selftest (the draft says so)

```
$ python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-51/count-c1.py --selftest
usage: count-c1.py [-h] [--repo REPO] [--hide HIDE] [--scratch SCRATCH]
                   [--keep]
                   rev
count-c1.py: error: the following arguments are required: rev
EXIT=2
```

`grep -n 'selftest' .ufo/waves/round-51/count-c1.py` finds the flag only as arm D's reference to R's
`tools/mori-pin-check.py --selftest` and as the fixture registry's tally texts; the counter's own `main()` takes
`rev` plus the five options above (`.ufo/waves/round-51/count-c1.py:211-217`). Its arms are exercised by
`.ufo/waves/round-51/controls/c1-controls.py` and the five receipts `evidence/control-c1-<name>.txt`.

### 3. The frozen bytes are the working-tree bytes I quoted

```
$ for f in .ufo/waves/round-51/count-c1.py .ufo/waves/round-51/count-c2.py; do
    a=$(git show 4677910eae6df3dabd38fe9a0daf1945146a1110:$f | sha256sum | cut -d' ' -f1)
    b=$(sha256sum $f | cut -d' ' -f1); echo "$f same=$([ "$a" = "$b" ] && echo yes || echo no)"; done
.ufo/waves/round-51/count-c1.py same=yes
.ufo/waves/round-51/count-c2.py same=yes
```

(`git -C /home/vgpnk/Projects/shokunin/mori-shokunin`; read-only. The two sha256 values:
`622f650c1ade984d8c9abed20e7a7fd08930861a698398f36d4c3a770aff355c` and
`19553792d74d8f3ca9c09e6a018b9c66f61a58e8ad78e72b524a69ec892cfb26`.)

### 4. The data commit carries what the draft's rows point at

```
$ git ls-tree 87e0c374537557754bf71dd68036ded3ddc6699c -- .ufo/waves/round-51/count-c1.py \
    .ufo/waves/round-51/count-c2.py corpus/evidence/sources-r51/ corpus/knowledge/memavailable-estimate-r51.md
100755 blob 0151b4bde71a613d49fd0103df4c04a7f726b933  .ufo/waves/round-51/count-c1.py
100644 blob e8843753105f83adc0516d15119192960187a4b9  .ufo/waves/round-51/count-c2.py
100644 blob c5d641d92dae3cce4d26bdf4778a77c192b7930d  corpus/evidence/sources-r51/34e431b0.patch
100644 blob b2813ff13cb23bb26985bd6cfd6cd6a46cdb49ca  corpus/evidence/sources-r51/meminfo.c.v7.2
100644 blob a8430a7ae05447ab69233e427366c4e40e8dddb9  corpus/evidence/sources-r51/mm_inline.h.v7.2
100644 blob 2ccd5b2dfdd33a98f4491b0b9f48c6877370c309  corpus/evidence/sources-r51/proc.rst.v7.2
100644 blob 43aca5a2ac990ab338e99e57f7fc4e36789fb52e  corpus/evidence/sources-r51/show_mem.c.v7.2
100644 blob b34adda32cc581ca58fdf7de449181592a17336c  corpus/knowledge/memavailable-estimate-r51.md
```

### 5. The draft's registry rows, measured by the lane's own reconciler (probe tree, scratch only)

```
$ cp draft-section.md probe/SKILL.md
$ cp .ufo/waves/round-51/count-c2.py probe/.ufo/waves/round-51/count-c2.py
$ cp -r corpus/evidence/sources-r51 probe/corpus/evidence/
$ python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-pin-check.py --root probe
pin line=44 kind=tally prefix=C2_SELFTEST state=match pinned='pass=34 fail=0' observed='pass=34 fail=0' rc=0 cmd='python3 .ufo/waves/round-51/count-c2.py --selftest'
PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=- baseline=no env=0 stale=0
EXIT=0
```

What this establishes for the draft, and nothing more: the two new `gate` rows parse as registry rows with the
Round50 header; the C2 row yields exactly one tally pin, bound to `python3 .ufo/waves/round-51/count-c2.py
--selftest`, matching `pass=34 fail=0` with rc 0; the C1 row yields no pin and no `no_command`/`unparsed`
finding (its self-test cell deliberately carries no `*_SELFTEST` token); and the two prose-style tables
(`situation|do|do not|source`, `class|what it means|what the lane does`) add no `hidden` row — none of their cells
carry an uppercase `*SELFTEST` token or the text of the selftest flag.

The same probe before the copies were present is the reason the draft's C2 row names the copies:

```
$ python3 … /tools/mori-pin-check.py --root probe        # probe without corpus/evidence/sources-r51/
pin line=43 kind=tally prefix=C2_SELFTEST state=mismatch pinned='pass=34 fail=0' observed=None rc=1 cmd='… --selftest' class=env
PIN_CHECK=unmet tally_pins=1 … mismatches=1 … env=1 stale=0
EXIT=1
$ python3 probe/.ufo/waves/round-51/count-c2.py --selftest
  File "…/count-c2.py", line 306, in selftest
    with open(os.path.join(lane, path), "rb") as f:
FileNotFoundError: [Errno 2] No such file or directory: '…/probe/corpus/evidence/sources-r51/proc.rst.v7.2'
EXIT=1
```

That is the class rule working as the draft describes it (no tally line → `env`, not `stale`), and it is a limit of
the C2 pin rather than a defect: the selftest reads the committed copies through the counter's own lane path
(`.ufo/waves/round-51/count-c2.py:306`), so the pin is green only in a tree that carries
`corpus/evidence/sources-r51/` — true of the lane and of a `--rev` clone at or after the data commit.

### 6. Guard read before the heavy-ish runs

```
$ scripts/hyaku/disk-guard.sh status
root                             use%     free
/tmp                               4%   124.0G
/var/tmp                          35%   584.8G
/fast/scratch/hyaku               26%   601.8G
```

## Gates

| gate | how it was met | state |
|---|---|---|
| section shape as `## Round50` | draft carries an H2 heading, opening prose, a registry table with the header row `| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |` copied from `SKILL.md:1007` and from the counter's own `HDR`, and two `###` sub-sections | met |
| gate rows for both counters, `self-test` cell carrying the right thing | C2 row pins `C2_SELFTEST pass=34 fail=0` (observed last line, exit 0); C1 row states there is no selftest mode and names the controls and their receipts | met |
| note that count-c1.py has no selftest (controls instead) | in prose (second paragraph) and in the C1 row's `self-test` cell | met |
| the draft does not break the reconciler | probe above: `PIN_CHECK=met`, `tally_pins=1`, all finding counters zero | met in the probe tree |
| decision table built from the entry's Reading rules | five rows, one per Reading rule, each citing the entry and its S-ids/claim rows; the "do not" side is the rule's own warning | met |
| class table: env / stale → meaning → what the lane does | two rows; semantics from `tools/mori-pin-check.py:138-143` (v5 docstring) and its code at `:816-830` (tally), `:713-741` (digest, line-count), and arm C's expected ` env=2 stale=2` | met |
| no ENTAIL votes from this seat | this seat's item is not an entailment item; no line of this report starts with that token, and no vote is claimed anywhere | met (not applicable) |

Not run, and not claimed: a full `tools/mori-pin-check.py --rev <integration tip>` over the whole 1067-line
`SKILL.md`. The probe measures only the draft's rows in isolation. **UNVERIFIED at the live tip** — the L1 should run
it after appending.

## Draft (fenced) — append after the Round50 decision-row table

````markdown
## Round51 — the operability counter, the MemAvailable entry and the pin mismatch classes

Round 50's spot-check routed two defects into round 51: §5 item 1 / D-d — `tools/mori-pin-check.py` exported its
`--rev` tree under `<repo>/.scratch`, so a SIGKILLed run left 12547 paths in the repo it reads, and
`.ufo/waves/round-40/conform.py:69` hardcoded the lane path, so a re-execution off-host died as a setup error — and
§5 item 4 — a depth counter that scored where a quote sits and not what it says. Round 51 works operability and
depth on both, freezes its counters at `4677910e…` and lands the data at `87e0c374…`. Pin-check v5 measures a
`git clone --shared` checked out at the revision under `--scratch`/TMPDIR instead of a `git archive` under the repo
(the scratch-only control reads `reloc_mismatch=3` in `evidence/control-c1-scratch-only.txt`: the export cannot
simply leave the tree — the lane's relocation witness found two pinned instruments and `conform.py` read git
objects from the tree they run in), and it tags every mismatch line `class=env` or `class=stale`; `conform.py`
derives the lane from its own path and takes its selftest scratch from TMPDIR. At the landed tip
`.ufo/waves/round-51/count-c1.py` reads `C1=met kill_residue=0 relocated=met reloc_mismatch=0 classified=ok
selftest=pass=119,fail=0 failed=-`; entering `aa3af1ec` the same counter read `C1=unmet kill_residue=12547
relocated=unmet reloc_mismatch=1 classified=bad selftest=pass=114,fail=0
failed=kill_residue,relocated,classified`. The counters, predicates, controls and kill rules stay frozen: a
counter weakness found after scoring is a named limit, never a repair.

`.ufo/waves/round-51/count-c1.py` (operability) runs four arms at R. A: a `--rev` run in a fresh `--no-local` clone
is SIGKILLed 3 s after that run starts writing, and the clone it read must show 0 lines in
`git status --porcelain --ignored --untracked-files=all`. B: a second fresh clone runs pin-check under bubblewrap
with the lane working-tree path on a `--tmpfs`, and the run must exit 0 with a last line starting `PIN_CHECK=met`.
C: R's pin-check over a frozen five-row fixture registry must class the two no-tally pins `env`, the different-tally
pin and the rc-contradicting pin `stale`, leave the matching pin unclassed, and end ` env=2 stale=2`. D: R's own
pin-check selftest must exit 0 with at least 114 arms. The counter has no selftest of its own — `--selftest` is an
argparse usage error (exit 2) — so its controls carry that job: the five under `.ufo/waves/round-51/controls/`
(receipts `evidence/control-c1-<name>.txt`). The always-env control is the one that keeps the classifier honest:
a tool that says env for everything reads `failed=relocated,classified,selftest`.

`.ufo/waves/round-51/count-c2.py` (depth) scores `corpus/knowledge/memavailable-estimate-r51.md` against the five
frozen copies under `corpus/evidence/sources-r51/`: at least 12 claim rows, each claim cell 6+ words, unique, and
carrying 3 words its own quote does not; one mined `SOURCES.md` row per claim, opened 2026-10-26, naming its URL
among the five copies and citing the entry; one backticked 6–25-word quote per row located in that row's copy; all
five copies drawn on and sha256-pinned; and — the entailment arm that closes §5 item 4 — for every row a non-L1
wave report under `.ufo/waves/round-51/w1/` records the judgment for that exact claim text, with no dissent. At the
data commit it reads `C2=unmet claims=21 located=21 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok
provenance=ok entailed=0 dissent=0 failed=entailment`: every quote is located and no seat has judged them yet. Its
selftest carries the entry-level controls plus the arm's eight (no votes, one row unreviewed, dissent, L1-authored
vote, vote in another directory, vote on other text, non-markdown file, whitespace folding).

| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| r51 operability counter (C1) | gate | `python3 .ufo/waves/round-51/count-c1.py <rev> [--repo DIR] [--hide PATH] [--scratch DIR] [--keep]` (`--hide` is the path bubblewrap hides, default the lane; `--scratch` must lie outside the source repo) | 0 → `C1=met kill_residue=0 relocated=met reloc_mismatch=0 classified=ok selftest=pass=N,fail=0 rev=<full> failed=-` · 1 → `C1=unmet … failed=<arms>` (kill_residue, relocated, classified, selftest), plus a `kill_residue_first:` line and the classifier's `prefix=` lines and summary echoed as `classified:` lines · 2 → argparse usage error, or `C1_SETUP <reason>` (unresolvable revision, scratch inside the source repo) | no mode of its own: `--selftest` is an argparse usage error (exit 2); the arms are exercised by the five controls in `.ufo/waves/round-51/controls/` (receipts `evidence/control-c1-<name>.txt`), and arm D pins R's pin-check selftest at ≥ 114 arms | `ENTERING_SELFTEST` 114; the five-row fixture registry (`enva`/`envb` → env, `stla`/`stlb` → stale, `okay` → match) and the ` env=2 stale=2` summary are in-script; the kill lands 3 s after the first write; limits: one kill moment, one hidden path (the lane), five fixture rows, and a tool that prints a tally then fails for an environmental reason is classed stale | scratch only: `--scratch DIR` (default a `mkdtemp` under TMPDIR) is refused inside the source repo and removed on exit unless `--keep`; each arm clones the repo fresh with `--no-local` and writes nothing into the tree it reads | mori |
| r51 MemAvailable entry counter (C2) | gate | `python3 .ufo/waves/round-51/count-c2.py <rev> [--repo DIR] [--entry PATH]`; `--hashes <rev>` prints each row's 12-hex claim handle | 0 → `C2=met claims=N located=N quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=N dissent=0 rev=R` · 1 → `C2=unmet … failed=<checks>` (entry absent, table, claims floor, bad rows, quote missing, sources floor, pins, provenance, entailment) · 2 → `C2_SETUP` (usage, unresolvable revision) | `python3 .ufo/waves/round-51/count-c2.py --selftest` → `C2_SELFTEST pass=34 fail=0` (re-run 2026-10-26; receipt `evidence/selftest-c2.txt`) | sha256 of the five copies under `corpus/evidence/sources-r51/` (in-script `COPIES`); `ENTRY` `corpus/knowledge/memavailable-estimate-r51.md`; `OPENED` 2026-10-26; claims floor 12; quote 6–25 words with 3 words beyond it; the entailment arm reads `.ufo/waves/round-51/w1/` reports whose names do not start `MoriR51` and needs one `ENTAIL <h> entailed` line per row and no dissent; limits: a located quote proves the words occur, a vote proves a wave seat recorded that judgment — neither proves the judgment right — and v7.2 says nothing about other kernels | none (read-only `git show` / `git ls-tree` / `git rev-parse`) | mori |

### Decision row — runway reading (round 51)

| situation | do | do not | source |
|---|---|---|---|
| a seat spawn, a census or a pressure probe wants the host's runway | read the `MemAvailable` line itself and compare it with the dispatcher's floor; read a `MemAvailable/MemTotal` ratio as unit-free | rebuild the figure as `MemFree + Cached`: that sum counts tmpfs and shmem pages, which sit on anon LRU lists and which the estimate does not add | `corpus/knowledge/memavailable-estimate-r51.md` (S492–S495, rows 4, 7, 17, 20) |
| a meminfo figure is converted, or compared with a figure from another surface | read the figures through row 14's helper: a page count shifted by `PAGE_SHIFT - 10` prints kB, and a ratio is unit-free | mix a kB line with a cgroup block's byte amounts or a `Tasks state` page count (the round-50 conversion rule) | `corpus/knowledge/memavailable-estimate-r51.md` (S494, row 14; S489–S491) |
| `MemAvailable` reads 0, or small, while swap is free | read 0 as the formula's clamp, and the figure as excluding swap by construction: a host with free swap can keep running past 0 | read 0 as an exact zero or as proof a kill is imminent; read free swap as counted in the estimate | `corpus/knowledge/memavailable-estimate-r51.md` (S493, rows 1, 12) |
| `Cached` is large while `MemAvailable` is small | compare `Shmem`: tmpfs and shared memory raise `Cached` without raising the estimate | read the gap as cache the host can hand to a new seat, or as headroom the estimate has already counted | `corpus/knowledge/memavailable-estimate-r51.md` (S492–S496, rows 4, 5, 7, 17) |
| a runway threshold goes into a receipt, a report or a gate | report it as local: the estimate withholds min(half the term, the summed low watermarks) from both the file cache and the reclaimable kernel term, and the proc document says its accuracy varies from system to system | state the threshold as a property of `MemAvailable` in general, or recompute the estimate from `/proc/meminfo` alone (`totalreserve_pages` is not exported) | `corpus/knowledge/memavailable-estimate-r51.md` (S492–S493, rows 3, 8, 10, 13; Boundaries) |

### Pin mismatch classes (round 51)

`tools/mori-pin-check.py` v5 (round 51) tags a mismatch with why the pin failed, so an off-host re-execution reads
as what it is: "can't run here" or "the row and the instrument disagree". The rule is the tool docstring's (v5) and
the shape arm C of the round-51 operability counter scores over its fixture registry. The summary line ends
`env=N stale=N`, env + stale = mismatches, and any mismatch leaves `PIN_CHECK=unmet`. The class is a property of
the run, not of the registry: `unparsed`, `no_command`, `dropped`, `rebound`, `duplicate`, `hidden`,
`misattributed` and `env_unexpanded` findings carry no class.

| class | what it means | what the lane does |
|---|---|---|
| `class=env` | the pinned command printed no line starting with its prefix at all — a setup error, a missing path, a timeout, an OS error — so the instrument could not run here and the pin says nothing about the measured revision | read it as "can't run here": fix the environment or the instrument's own lane assumption (path, TMPDIR, interpreter, git objects) and rerun there; leave the row's pinned tally as it is — an env mismatch never justifies a re-pin, and rewriting the row to silence env is the false green the class exists to prevent |
| `class=stale` | the command ran and printed a different tally for its prefix, printed the pinned tally with an exit code that contradicts it, or a digest or line-count pin does not match the file — the row and the instrument disagree at the measured revision | read it as a disagreement to settle, not a run to retry: either the pin is out of date, and the row and its receipt are edited in the same commit as the tool change (reconcile before landing a round), or the tool regressed, and the tool is fixed; say which in the receipt |

Named limits of the classes, frozen with the counter: a tool that prints a tally and then fails for an
environmental reason is classed stale; a row that binds no command is a `no_command` registry defect rather than
either class; and the class says why the pin failed, never whether the revision is good.
````

## Sources the draft's cells rest on

| cell | evidence |
|---|---|
| C1 summary line, at data / entering | `.ufo/waves/round-51/evidence/c1-at-data.txt` and `evidence/control-c1-do-nothing.txt` (both read in full) |
| `kill_residue_first:` and `classified:` echo lines | `evidence/c1-at-data.txt`, `evidence/control-c1-do-nothing.txt`, `evidence/control-c1-scratch-only.txt` (they show the echo shape and, in do-nothing, `kill_residue_first: !! .scratch/pin-check-uphozg94/tree/.gitignore`) |
| `reloc_mismatch=3` for the scratch-only control | `evidence/control-c1-scratch-only.txt` |
| always-env reading `failed=relocated,classified,selftest` | `evidence/control-c1-always-env.txt` (`C1=unmet … selftest=pass=118,fail=1`, `env=4 stale=0`) |
| C1 arm mechanics, `ENTERING_SELFTEST` 114, fixture names, 3 s kill | `.ufo/waves/round-51/count-c1.py` docstring lines 4-27, `:40-65` (fixtures and rows), `:106-121` (kill), `:131-150` (relocated), `:236-262` (output) |
| C2 predicate, floors, copy sha256 list, `--hashes` | `.ufo/waves/round-51/count-c2.py:1-30` (docstring), `:42-70` (constants and `COPIES`), `:269-300` (modes) |
| C2 data-commit reading | `evidence/c2-at-data.txt` |
| pin class semantics | `tools/mori-pin-check.py:126-143` (output line and v5 paragraph), `:816-830` (tally class), `:713-741` (digest/line-count), `:773-780` (`no_command`) |
| pin-check v5 clone, not archive, under scratch | `tools/mori-pin-check.py:869-881`; `tools/mori-pin-check.py:938` in `SKILL.md` describes the same v5 |
| `conform.py` lane from its own path, scratch from TMPDIR | `.ufo/waves/round-40/conform.py:72` (`LANE = … os.path.abspath(__file__)`) and `:73` (`SCRATCH_ROOT = tempfile.gettempdir()`), `:746` (`mkdtemp(..., dir=SCRATCH_ROOT)`) |
| the five Reading rules the decision rows paraphrase | `corpus/knowledge/memavailable-estimate-r51.md` §Reading rules |
| S-ids | `corpus/SOURCES.md:271-275` (S492–S496) |

## Touched surfaces

- Wrote: `.ufo/waves/round-51/w1/Mo51ScribeSkill.md` (this file). Nothing else in the lane.
- Scratch only: `/fast/scratch/hyaku/mori-r51/Mo51ScribeSkill/` (`draft-section.md`, `probe/`, `tmp/`), removed at
  the end — `ls` of that path after cleanup returns nothing.
- Read-only, no writes: `SKILL.md`, `.ufo/waves/round-51/contract.md`, both counters, `evidence/*` receipts,
  `tools/mori-pin-check.py`, `.ufo/waves/round-40/conform.py`, `corpus/knowledge/memavailable-estimate-r51.md`,
  `corpus/SOURCES.md`, `corpus/lessons/round-50-verifier-spotcheck.md`, `considerthese/2026-10-26.md`, and
  `git show` / `git ls-tree` in the lane.
- No `git add/commit/stash/checkout/reset/pull/push`, no jj command, no pacman, no tool install or upgrade (nothing
  was needed), nothing written into a PATH directory, `/home/vgpnk/Projects/shokuknow` untouched, no host setting
  read or changed beyond the disk-guard status line, no kernel log read.

## Out of scope, and deviations

- No votes of any kind were recorded: this seat is not an entailment item, and no line of this report starts with
  the vote keyword. The draft quotes the keyword only inside a table cell and inside prose.
- The counters, predicates, controls and kill rules were not proposed for change and were not edited.
- No full-lane reconciler run at the integration tip (see Gates). No rerun of the C1 arms: their receipts are the
  evidence and the contract freezes them.
- The sentence "two pinned instruments and `conform.py` read git objects from the tree they run in" is attributed in
  the draft to the lane's relocation witness; I read that attribution in the contract (§C1 witness paragraph) and
  the `reloc_mismatch=3` reading in the scratch-only receipt, and did not re-run the witness myself.

## Findings

- **MED — a pinless C1 gate row is one token away from a red registry.**
  `.ufo/waves/round-51/w1/Mo51ScribeSkill.md` C1 row / `tools/mori-pin-check.py:442-459` and `:773-780`: the C1
  row's `self-test` cell must carry no `[A-Z][A-Z0-9_]*SELFTEST` token. `pin_commands()` binds every such span to
  the nearest preceding command span (or to `None`), so adding e.g. a made-up `C1_SELFTEST` tally to that cell makes
  the reconciler either emit a fatal `no_command` (no preceding command span) or run `count-c1.py --selftest`,
  which exits 2 by argparse — a `class=env` mismatch either way. The draft keeps the cell token-free on purpose; the
  L1 should not "improve" it into a tally.
- **LOW — the C2 selftest pin is green only in a tree that carries the copies.**
  `.ufo/waves/round-51/count-c2.py:300-310`: `selftest()` opens `corpus/evidence/sources-r51/<copy>` through the
  counter's own lane path, so a `--rev` pin at a revision before the data commit (e.g. `aa3af1ec`) reads
  `class=env` with a `FileNotFoundError`, not `class=stale`. Measured: probe without the copies →
  `PIN_CHECK=unmet … env=1`; with them → `PIN_CHECK=met`. This is the class rule behaving correctly and the pin
  being tree-dependent; it is a named limit, not a reason to change the counter.
- **LOW — `reloc_mismatch` and pin-check's own `mismatches` count different things.**
  `.ufo/waves/round-51/count-c1.py:149` sums `state=mismatch` and `state=no_command` lines from the relocated run,
  while pin-check's summary counts `no_command` outside `mismatches` (`tools/mori-pin-check.py:852-860`). On a run
  with a `no_command` finding the counter's `reloc_mismatch` and the tool's `mismatches` disagree by that count.
  Frozen; recorded as a named limit only.
- **LOW — the draft repeats volatile counts in prose.** `SKILL.md` (draft): `12547`, `119`, `34` and the two rev
  prefixes are quoted in the section body; the same numbers live in `evidence/control-c1-do-nothing.txt`,
  `evidence/c1-at-data.txt` and `evidence/selftest-c2.txt`. If a later round re-runs the do-nothing control, the
  residue number there drifts (the contract itself notes 12475–12547), so the prose number is a reading of one run —
  the C2 selftest count and the C1 landed-tip count are exact and re-derivable.
- **LOW — the decision-row table cites round-50 S-ids for the conversion rule.** `SKILL.md` (draft), Decision row
  row 2 cites `S489–S491` beside `S494`; S489–S491 belong to `corpus/knowledge/oom-memcg-stat-r50.md`, not to the
  round-51 entry. It is deliberate (the "do not" is cross-surface) but an S-id outside the entry can read as a
  provenance drift; the L1 may prefer to drop the parenthetical and keep the pointer to the round-50 entry.
- **LOW — the class table's "env + stale = mismatches" is a property of one counter run.** `SKILL.md` (draft),
  Pin mismatch classes paragraph: true of the tool's summary line (`tools/mori-pin-check.py:816-830`, `:707-711`,
  `:839-844` all increment exactly one of the two on each mismatch), but the sentence is prose and not pinned, so it
  will not be caught if a later version reclassifies. Named here so a future round re-reads the docstring.
