# Mo61ScribeReg5253 — round-61 gate-registry rows for rounds 52 and 53

Seat: draft four SKILL.md gate-registry rows (rounds 52–53) for
`.ufo/waves/round-61/gate-manifest.json`. Read-only; no production file, registry,
VCS state, fleet or sibling repo was touched. Frozen revision
`7370a731abcafc4c803111de7c22cd6264d63be1`; entering revision
`325f7e639916fcbc77fa2ec7475951a1b86bb1cb`.

## Scoped paths (manifest entries 1–4)

| manifest path | round | landing commit | landing subject | counter sha256 (at landing) |
|---|---|---|---|---|
| `.ufo/waves/round-52/count-c1.py` | 52 | `d3a8ea5957b73bddbde750a8c0af2fba8da8b7c2` | round-52: freeze — contract, C1/C2 counters with selftests, C1 controls and receipts, census-start, sweep, five v7.2 source copies | `e864922790451b4026be784d5344d9a06827b251ed3c81bfe26b1c559ee3c300` |
| `.ufo/waves/round-52/count-c2.py` | 52 | `d3a8ea5957b73bddbde750a8c0af2fba8da8b7c2` | (same commit) | `0a9ec2ffdd85dd1a2be13f359ad82c0f45f99b781d73f9bcf3fa098d7f3bb74a` |
| `.ufo/waves/round-53/count-c1.py` | 53 | `f4da3fd400fa88a6db8ea544a4f7045c15d2410e` | round-53: freeze — contract, C1/C2 counters with selftests, controls and receipts, census-start, sweeps, v7.3 and band source copies | `ebaff9158362b905961e9c23b2e91790df135e3b344327030c6f67a2db27005d` |
| `.ufo/waves/round-53/count-c2.py` | 53 | `f4da3fd400fa88a6db8ea544a4f7045c15d2410e` | (same commit) | `5684b69f7ae9030b33195490f10c650c3c123909f0d61e182b6c1cadfbb168c5` |

All four sha256s are byte-identical at the landing commit and at lane HEAD
(`git show <rev>:<path> | sha256sum`, both revs) and all four paths resolve at the
freeze revision (`git cat-file -e 7370a731…:<path>` → exit 0).

## Commands run (exact)

Materialize the artifact at its landing commit into scratch (no lane write):

```
S=/fast/scratch/hyaku/mori-r61/Mo61ScribeReg5253
cd /home/vgpnk/Projects/shokunin/mori-shokunin
git show d3a8ea5957b73bddbde750a8c0af2fba8da8b7c2:.ufo/waves/round-52/count-c1.py > $S/art/.ufo_waves_round-52_count-c1.py
git show d3a8ea5957b73bddbde750a8c0af2fba8da8b7c2:.ufo/waves/round-52/count-c2.py > $S/art/.ufo_waves_round-52_count-c2.py
git show f4da3fd400fa88a6db8ea544a4f7045c15d2410e:.ufo/waves/round-53/count-c1.py > $S/art/.ufo_waves_round-53_count-c1.py
git show f4da3fd400fa88a6db8ea544a4f7045c15d2410e:.ufo/waves/round-53/count-c2.py > $S/art/.ufo_waves_round-53_count-c2.py
```

Whole-tree materialization at each landing commit (`git archive <landing> | tar -x -C $S/tree-r52`,
`…tree-r53`) so that each counter's `--selftest` can read its sibling committed source
copies from `corpus/evidence/sources-r52/` and `corpus/evidence/sources-r53/`.

Selftest run once per artifact, at its landing commit, materialized to scratch, `TMPDIR`
inside my scratch:

```
export TMPDIR=$S/tmp
cd $S/tree-r52 && python3 -I -B .ufo/waves/round-52/count-c1.py --selftest   # rc 0
cd $S/tree-r52 && python3 -I -B .ufo/waves/round-52/count-c2.py --selftest   # rc 0
cd $S/tree-r53 && python3 -I -B .ufo/waves/round-53/count-c1.py --selftest   # rc 0
cd $S/tree-r53 && python3 -I -B .ufo/waves/round-53/count-c2.py --selftest   # rc 0
```

## Measured selftest output lines (last line of each run, rc 0 each)

```
r52 count-c1: C1_SELFTEST pass=42 fail=0
r52 count-c2: C2_SELFTEST pass=45 fail=0
r53 count-c1: C1_SELFTEST pass=37 fail=0
r53 count-c2: C2_SELFTEST pass=30 fail=0
```

These match the committed round receipts byte for byte
(`.ufo/waves/round-52/evidence/selftest-c1.txt` → `C1_SELFTEST pass=42 fail=0`,
`…/round-52/evidence/selftest-c2.txt` → `C2_SELFTEST pass=45 fail=0`,
`…/round-53/evidence/selftest-c1.txt` → `C1_SELFTEST pass=37 fail=0`,
`…/round-53/evidence/selftest-c2.txt` → `C2_SELFTEST pass=30 fail=0`, each followed by
`exit=0`) and the LOG.md tallies at `LOG.md:2826-2827` and `LOG.md:2863-2864`.
Re-running the same four selftests at lane HEAD reproduces the same four lines and rc 0
(so the landing-commit numbers are not stale).

## Live (non-selftest) runs at the freeze revision `7370a731…` (extra evidence)

```
python3 -I -B .ufo/waves/round-52/count-c2.py 7370a731… --repo <lane>          → rc 0
  C2=met claims=28 located=28 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=28 dissent=0 rev=7370a731…
python3 -I -B .ufo/waves/round-53/count-c1.py 7370a731… --repo <lane>          → rc 0
  C1=met scope=46 rows=46 matched=46 status_ok=46 quote_ok=46 source_rows=ok pins=ok provenance=ok held=44 absent=2 holds=46 changed=0 voted=46 dissent=0 rev=7370a731…
python3 -I -B .ufo/waves/round-53/count-c2.py 7370a731… --repo <lane> --scratch <scratch>  → rc 0
  C2=met tool=present selftest=pass n=31 fixtures=80 agree=80 disagree=0 registry=ok live=ok rev=7370a731…
python3 -I -B .ufo/waves/round-52/count-c1.py 7370a731… --repo <lane> --fleet-repo /home/vgpnk/Projects/shokunin --scratch <scratch> → rc 1
  C1=unmet items=41 axes=6 pins=4 boxes=4 living=7 superseded=4 locators=24 mismatches=3 errors=1 hidden=0 lane_writes=2 manifest=6209bdb8e400 rev=7370a731… failed=errors,lane_writes,mismatch
```

The r52 C1 live `unmet` is **not** a property of the artifact: its three mismatches are
`receipt_missing` for three living pins whose receipts live in a later round's directory
(`mori-register-check.py` 12/12, `mori-settlement-scan.py` 10/10, `mori-vote-bind.py` 16/16 —
receipts at `.ufo/waves/round-52/evidence/selftests/` hold only the round-50 pair), and its
`lane_writes=2` counts two untracked files that other round-61 seats wrote into
`.ufo/waves/round-61/w1/` **during** the run (the receipt shows
`lane_write ?? .ufo/waves/round-61/w1/Mo61RevPoc.md` and
`lane_write ?? .ufo/waves/round-61/w1/Mo61ScoutFloor.md`). Both are ambient-state effects of
running a round-52 gate inside a live round-61 wave, not defects in the frozen r52 artifact.
Reported as a finding, not fixed (no remediation in this lane).

## Where LOG.md names rounds 52 and 53

`LOG.md` names both rounds' counters by **bare filename only**, never by repo-relative path:

- round 52 section (`LOG.md:2808`): "`count-c1.py`, arms A-D" (`LOG.md:2813`),
  "`count-c2.py` with the two-voter non-author entailment arm" (`LOG.md:2815`),
  selftest tallies `C1_SELFTEST pass=42 fail=0`, `C2_SELFTEST pass=45 fail=0`
  (`LOG.md:2826-2827`).
- round 53 section (`LOG.md:2841`): "counter `count-c1.py`" (`LOG.md:2849`),
  "counter `count-c2.py`" (`LOG.md:2854`), selftest tallies `C1_SELFTEST pass=37 fail=0`,
  `C2_SELFTEST pass=30 fail=0` (`LOG.md:2863-2864`).

`grep -c "round-52/count-c" LOG.md` → **0**; `grep -c "round-53/count-c" LOG.md` → **0**.
The full repo-relative paths appear only in the corpus, not the log:
`corpus/QUALITY.md:1363,1374,1379,1390,1423`, `corpus/README.md:733,755`,
`corpus/lessons/round-52.md:56`, `corpus/lessons/round-53.md:130`,
`corpus/knowledge/kernel-v7.3-recheck-r53.md:13`, and `SKILL.md:1203` / `SKILL.md:1242`
(prose only — the existing SKILL.md has **no** registry row for any of the four paths).

## Draft rows (one line each, exact 8 cells; the L1 appends them)

Cell order is the counter's own header (`count-c1.py:22-24`, `HEADER_CELLS`):
name | kind | entry | verdict map | self-test | pinned values | write scope | owner.
The entry cell names the artifact path verbatim (backticked, as the counter's
`row_hits` requires); the self-test cell names the runnable `--selftest` command and the
measured output line; the owner cell names the landing round's L1.

```
| r52 calibration counter (C1) | gate | `python3 .ufo/waves/round-52/count-c1.py <rev> [--repo DIR] [--fleet-repo DIR] [--fleet-rev REV] [--scratch DIR] [--timeout S]` | 0 → `C1=met items=N axes=6 pins=P boxes=B living=L superseded=S locators=O mismatches=0 errors=0 hidden=0 lane_writes=0 manifest=<sha12> rev=R` · 1 → `C1=unmet … failed=<reasons>` (one `item <axis> <name> expect=… got=… state=…` line per mismatch, one `lane_write <path>` line per lane write) · 2 → `C1_SETUP <reason>` (usage, missing option value, unresolvable revision, scratch inside the lane) | `python3 .ufo/waves/round-52/count-c1.py --selftest` → `C1_SELFTEST pass=42 fail=0` (measured 2026-10-30 at landing `d3a8ea59`, file materialized to scratch, `TMPDIR` in scratch, rc 0) | `FLEET_REV` `f0b61b4ad192bcd95d7a76613a626f71285996ed` (the fleet repo's `MANIFEST.json` is read at it; `--fleet-repo` defaults to the lane's parent), `THROUGH` 51, `RECEIPT_DIR` `.ufo/waves/round-52/evidence/selftests/`, `TOOL_TIMEOUT` 900; counter sha256 `e864922790451b4026be784d5344d9a06827b251ed3c81bfe26b1c559ee3c300` at `d3a8ea59` | scratch only — read-only `git show` / `git cat-file` / `git ls-tree` / `git archive` on the lane and the fleet repo; the archive is extracted under `--scratch` (default a fresh dir under `$TMPDIR`, refused when it lies inside the lane) and removed on exit (the default dir wholly; with an explicit `--scratch` only its `tree/` and `tmp/` subtrees); `lane_writes` counts any lane-repo write and a nonzero value is an error | MoriR52 |
| r52 overcommit-ledger entry counter (C2) | gate | `python3 .ufo/waves/round-52/count-c2.py <rev> [--repo DIR] [--entry PATH]` (also `--hashes <rev>`, which prints each row's 12-hex claim handle) | 0 → `C2=met claims=N located=N quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=N dissent=0 rev=R` · 1 → `C2=unmet … failed=<checks>` (entry absent, table, claims floor, bad rows, quote missing, sources floor, pins, provenance, entailment) · 2 → `C2_SETUP <reason>` (usage, unresolvable revision, entry absent for `--hashes`) | `python3 .ufo/waves/round-52/count-c2.py --selftest` → `C2_SELFTEST pass=45 fail=0` (measured 2026-10-30 at landing `d3a8ea59`, file materialized to scratch, `TMPDIR` in scratch, rc 0) | in-script `COPIES` sha256 of the five v7.2 copies under `corpus/evidence/sources-r52/` (`767ab881…` overcommit-accounting.rst, `bf8ca026…` vm.rst, `e702754c…` util.c, `d7bf787c…` mman.h, `449b8583…` mmap.c); `ENTRY` `corpus/knowledge/overcommit-commit-limit-r52.md`; `ENTAIL_DIR` `.ufo/waves/round-52/w1/`; `VOTERS` `Mo52Ent01`–`Mo52Ent12`, `MIN_VOTES` 2; counter sha256 `0a9ec2ffdd85dd1a2be13f359ad82c0f45f99b781d73f9bcf3fa098d7f3bb74a` at `d3a8ea59` | none — read-only `git show` / `git ls-tree` / `git rev-parse`; the selftest reads the committed v7.2 copies under `corpus/evidence/sources-r52/` (lane root resolved by path arithmetic from the counter file, not by `--repo`) and writes nothing | MoriR52 |
| r53 v7.3-recheck ledger counter (C1) | gate | `python3 .ufo/waves/round-53/count-c1.py <rev> [--repo DIR]` (also `--scope`, which prints the frozen scope set read at the entering tip) | 0 → `C1=met scope=N rows=N matched=N status_ok=N quote_ok=N source_rows=ok pins=ok provenance=ok held=N absent=N holds=N changed=N voted=N dissent=0 rev=R` · 1 → `C1=unmet … failed=<checks>` (ledger absent, scope mismatch, status, quote, source rows, pins, provenance, votes) · 2 → `C1_SETUP <reason>` (usage, unresolvable revision, empty scope at the entering tip) | `python3 .ufo/waves/round-53/count-c1.py --selftest` → `C1_SELFTEST pass=37 fail=0` (measured 2026-10-30 at landing `f4da3fd4`, file materialized to scratch, `TMPDIR` in scratch, rc 0) | in-script `V73` sha256 of the nine v7.3 copies under `corpus/evidence/sources-r53/` (`bc178ff5…` proc.rst, `c50205bc…` show_mem.c, `d6c58074…` meminfo.c, `277e99e2…` mm_inline.h, `767ab881…` overcommit-accounting.rst, `f81feb3d…` vm.rst, `4dfcce2b…` util.c, `d7bf787c…` mman.h, `8e51fb1c…` mmap.c); `ENTERING` `20edafa59b38dac1ca358893f0259b1f436372d3`, `LEDGER` `corpus/knowledge/kernel-v7.3-recheck-r53.md`, `ENTRIES` memavailable-estimate-r51.md + overcommit-commit-limit-r52.md, `VOTE_DIR` `.ufo/waves/round-53/w1/`, `VOTERS` `Mo53Fr01`–`Mo53Fr12`, `MIN_VOTES` 2, `OPENED` 2026-10-26; counter sha256 `ebaff9158362b905961e9c23b2e91790df135e3b344327030c6f67a2db27005d` at `f4da3fd4` | none — read-only `git show` / `git ls-tree` / `git rev-parse`; the selftest reads the committed v7.3 copies under `corpus/evidence/sources-r53/` (lane root resolved by path arithmetic from the counter file, not by `--repo`) and writes nothing | MoriR53 |
| r53 commit-runway fixture counter (C2) | gate | `python3 .ufo/waves/round-53/count-c2.py <rev> [--repo DIR] [--scratch DIR]` (also `--fixtures <rev>`, which prints the reference reading per fixture) | 0 → `C2=met tool=present selftest=pass n=N fixtures=N agree=N disagree=0 registry=ok live=ok rev=R` · 1 → `C2=unmet … failed=<checks>` (tool absent, tool selftest fail, fixture disagreement — one `disagree` line each — registry row missing, live leg error) · 2 → `C2_SETUP <reason>` (usage, unresolvable revision, archive failure) | `python3 .ufo/waves/round-53/count-c2.py --selftest` → `C2_SELFTEST pass=30 fail=0` (measured 2026-10-30 at landing `f4da3fd4`, file materialized to scratch, `TMPDIR` in scratch, rc 0) | in-script `TOOL` `tools/mori-commit-runway.py`, `SCHEMA` `mori-commit-runway-v1`, `MIN_SELFTEST` 12, `N_SEEDED` 64 plus the 16 frozen edge fixtures, 15 checked `FIELDS`, exit `CODES`; the seeded-fixture seed is `sha256(<full commit id of R>)`; counter sha256 `5684b69f7ae9030b33195490f10c650c3c123909f0d61e182b6c1cadfbb168c5` at `f4da3fd4` | scratch only — the lane is read with `git archive` / `git ls-tree` / `git show`; fixtures and the live leg run under `--scratch` (default a fresh dir under `$TMPDIR`), removed on exit; the live leg reads this host's `/proc/meminfo`, `/proc/sys/vm` and `/sys/devices/system/cpu/present` and writes nothing | MoriR53 |
```

## Conformance check of the drafted rows (scratch fixture, no lane write)

Built a throwaway fixture repo at `$S/fixture` (`git -C "$D" init -q`, throwaway identity
`t <t@t>`, every later call named `git -C "$D"`), containing lane `SKILL.md` + the four
drafted rows in an 8-cell registry table, plus the four counter files materialized at their
landing commits. Ran the frozen round-61 C1 counter against it:

```
python3 .ufo/waves/round-61/count-c1.py <fixture-rev> --repo $S/fixture --manifest $S/manifest-4.json --scratch $S/tmp
→ C1=met gates=4 registered=4 missing=0 thin=0 dup=0 unres=0 noselftest=0 noowner=0 failed=none rev=5f4b73ec11ce2f08aa06c6834244a4b6545ea732
```

Baseline on the real lane at the freeze revision (25-path manifest, unchanged lane):

```
python3 .ufo/waves/round-61/count-c1.py 7370a731… --repo <lane> --manifest .ufo/waves/round-61/gate-manifest.json --scratch $S/tmp
→ C1=unmet gates=25 registered=0 missing=25 … failed=missing:.ufo/waves/round-52/count-c1.py,… (rc 1)
```

All four scoped paths appear in the baseline `missing=` list, confirming the four rows are
the delta this seat owes. Counter-side checks on the drafts:
each row's entry cell resolves via `row_hits` (`count-c1.py:66-72`) — verified
`hits=1` per path, no `dup`; every cell non-empty (`thin=0`); every self-test cell contains
`--selftest` (`noselftest=0`); owner cells non-empty (`noowner=0`).

## Findings (report only — no fix applied; frozen claims/counters/predicates untouched)

**F1 (r53 C2 registry arm is a bare-substring scan, and my row-4 draft would satisfy it).**
The r53 C2 counter's registry arm is `for line in skill_text.split("\n"): if
line.lstrip().startswith("|") and TOOL in line and "--selftest" in line: registry = "ok"`
(`count-c2.py` of round 53, `evaluate_tree`, ~line 351-353). It looks for the **tool**
`tools/mori-commit-runway.py` plus `--selftest` anywhere on one `|`-prefixed line — it does
not require that line to be the tool's own registry row, nor that the entry cell hold the
path. Demonstrated on the scratch fixture:
 - real tool row removed, only my draft rows 1–3 present → `C2=unmet … failed=registry`
   (`registry=bad`);
 - real tool row removed, my draft rows 1–4 present → `C2=met … registry=ok` — because my
   **row 4** draft names `tools/mori-commit-runway.py` in its pinned-values cell and
   `--selftest` in its self-test cell on the same `|` line.
Consequence for the L1: appending row 4 as drafted would make the r53 C2 counter's
registry arm green **even if the tool's own registry row were absent**, so the r53 C2
"registry" check would no longer prove the tool is registered. This does not affect the
four manifest paths (row 4's *entry* cell is `.ufo/waves/round-53/count-c2.py`, not the
tool), and it does not change any frozen counter. If the L1 wants the tool's row to remain
the sole satisfier, row 4's pinned-values cell should name the tool by `TOOL` constant
without the literal path string. Left as drafted (the path is the truthful pinned value);
the L1 decides.

**F2 (round-52 C1's live arm is not evaluable inside a live round-61 wave).**
The r52 C1 counter's `lane_writes` arm diffs `git status --porcelain --ignored
--untracked-files=all` before and after it runs the pinned commands, and treats any
new line as an error. In this wave, sibling seats write into `.ufo/waves/round-61/w1/`
concurrently, so the r52 C1 live run at the freeze revision reports `lane_writes=2` and
`errors=1` (`errors` from the three `receipt_missing` pins whose receipts belong to
round-56/59 rounds, not to round 52). Both are ambient; the r52 C1 artifact itself is
sound (selftest 42/0, and its own committed receipt agrees). If the L1 needs a live r52 C1
verdict for the C1 claim's evidence, it must be run in a quiesced lane; a row that claims
"this gate reads `C1=met`" would be false today.

**F3 (LOG.md never names these four artifacts by path).** `grep -c "round-52/count-c"
LOG.md` → 0 and `grep -c "round-53/count-c" LOG.md` → 0: the round-52/53 LOG sections name
the counters by bare filename (`LOG.md:2813,2815,2849,2854`), so the path→row mapping
cannot be reconstructed from LOG.md alone; the corpus (`corpus/QUALITY.md`,
`corpus/README.md`, `corpus/lessons/round-52.md:56`, `corpus/lessons/round-53.md:130`) and
the frozen manifest are the only path-bearing records. The four drafted rows are therefore
the first path-bearing registry entries for these artifacts.

**F4 (SKILL.md prose mentions two of the four paths but no row does).** `SKILL.md:1203`
cites `.ufo/waves/round-53/count-c1.py` in the release-recheck rule and `SKILL.md:1242`
cites `.ufo/waves/round-54/count-c1.py`; the counter's parser only reads 8-cell table rows,
so the prose citations do not register. Confirmed: parsing lane `SKILL.md` with the frozen
counter's own `parse_tables`/`row_hits` gives `hits=0` for each of the four scoped paths
(62 rows parsed in total).

## Out of scope

The other 21 manifest paths (rounds 54–60 wave counters, r57 `verify-c2-source.py`, the
five lane tools) are other seats' rows; the r53 tool registry row already at `SKILL.md:1209`
(`commit runway (r53, C2)`) is a different artifact and was left untouched. No file in
`SKILL.md`, `LOG.md`, `SCORECARD.md`, `corpus/`, `tools/`, the registry or any VCS state was
modified; the only file written by this seat is this report.

## Tooling

No tool was installed or upgraded by this seat (nothing in the task needed one beyond the
pre-installed `python3` 3.14.8 and `git` 2.56.0, both already on PATH). Per the operator's
paused-pacman rule nothing was installed through pacman.

## Scratch and receipts

Scratch root `$HYAKU_SCRATCH/mori-r61/Mo61ScribeReg5253` (`/fast/scratch/hyaku/…`); disk
guard was green before the work (`/fast/scratch/hyaku` 47% used, 434 G free). Small
receipts copied into this report: the four measured selftest lines, the four live verdict
lines, and the counter's own output above. The scratch tree (materialized artifacts,
`tree-r52`, `tree-r53`, the fixture repo, `tmp*`) was removed after the report was written.
