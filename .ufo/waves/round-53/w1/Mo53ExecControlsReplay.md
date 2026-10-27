# Mo53ExecControlsReplay — round 53 w1: independent replay of the ten frozen controls

Seat: Mo53ExecControlsReplay (leaf executor). Assignment: replay all ten controls independently from copies of
`controls/controls.py` and `controls/c1-data.py` in scratch, redirecting only the receipt output directory, and
compare every verdict line with `evidence/control-*.txt`.

Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin` (mori-shokunin). Entering tip measured by the controls:
`20edafa59b38dac1ca358893f0259b1f436372d3`. Data tip re-run: `2a4213bf8da72f7cd78189baa5bb9be825dca1df`.
Lane HEAD during this seat: `95cf78eef71979f9b740ef6bc3c5299b6beff86e`.
Scratch: `/fast/scratch/hyaku/mori-r53/Mo53ExecControlsReplay/` (removed at the end; everything cited here was
copied into this report first). Machine: MACHINE_ID. Disk guard status rc=0 before the run (`/fast` 615 G free
at 24 %). No tool was installed, upgraded or removed for this seat; no pacman transaction was attempted.

## 1. Method — exactly what was copied and changed

```
$ mkdir -p S/ctl S/evidence S/tmp          # S=/fast/scratch/hyaku/mori-r53/Mo53ExecControlsReplay
$ cp .ufo/waves/round-53/controls/controls.py S/src/controls.py
$ cp .ufo/waves/round-53/controls/c1-data.py  S/src/c1-data.py
$ sha256sum S/src/controls.py S/src/c1-data.py
f7ba7ac15592e39fd151b755b2041c138c3ea7454e54394c6dd3133446f1035a  S/src/controls.py
1833309cf072dd96964153a2f2cceffa28c635bb0cefed1d8857a9805c909fd3  S/src/c1-data.py
```

Those two sums equal the frozen list (`evidence/freeze-sha256.txt`) for the same paths, so the copies started as
the frozen bytes. The frozen counters were **not** copied: the copies keep pointing at the lane's
`.ufo/waves/round-53/count-c1.py` and `count-c2.py` (sha256 `ebaff915…` and `5684b69f…`, both equal to the frozen
list), so every control was scored by the frozen counters.

Full diff of my copies against the frozen originals (nothing else was touched):

```diff
--- .ufo/waves/round-53/controls/controls.py
+++ S/src/controls.py
@@ -12,8 +12,12 @@
 HERE = os.path.dirname(os.path.abspath(__file__))
-W = os.path.dirname(HERE)
-LANE = os.path.dirname(os.path.dirname(os.path.dirname(W)))
+# Mo53ExecControlsReplay scratch copy: the only functional edits are (a) W/LANE pinned to the frozen lane
+# locations so the frozen counters and the lane itself are read from the lane (unchanged semantics), and
+# (b) the receipt output directory redirected from the lane's evidence/ to this seat's scratch.
+W = "/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-53"
+LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
+EVIDENCE = "/fast/scratch/hyaku/mori-r53/Mo53ExecControlsReplay/evidence"
@@ -75,7 +79,7 @@
-    out = os.path.join(W, "evidence", "control-%s.txt" % name)
+    out = os.path.join(EVIDENCE, "control-%s.txt" % name)

--- .ufo/waves/round-53/controls/c1-data.py
+++ S/src/c1-data.py
@@ -18,8 +18,10 @@
 HERE = os.path.dirname(os.path.abspath(__file__))
-W = os.path.dirname(HERE)
-LANE = os.path.dirname(os.path.dirname(os.path.dirname(W)))
+# Mo53ExecControlsReplay scratch copy: W pinned to the frozen wave dir (so count-c1.py is imported from the
+# lane, unchanged) and LANE pinned to the lane.
+W = "/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-53"
+LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
```

Why the two path constants had to change: `W`/`LANE` are derived from `dirname(__file__)`, so a copy outside
the lane would have resolved `W` to the scratch directory and `LANE` to `/fast/scratch/hyaku/mori-r53`. The
values written are exactly the values the frozen originals derive in place (`W` = the round-53 wave dir,
`LANE` = the lane). Control logic — the parts maps, `FREEZE_COPY`, the junk-tool `WRAPPER` and its mutations,
the clone/commit helper, the receipt format — is byte-identical.

Run (task-specified invocation, TMPDIR inside the scratch):

```
$ export TMPDIR=S/tmp
$ cd S && python3 S/src/controls.py S/ctl
c1-do-nothing 1 C1=unmet scope=46 rows=0 matched=0 status_ok=0 quote_ok=0 source_rows=bad pins=bad provenance=bad ...
c1-all-held   1 C1=unmet scope=46 rows=46 matched=46 status_ok=44 quote_ok=44 source_rows=ok pins=ok ...
c1-v72-copies 1 C1=unmet ... status_ok=44 quote_ok=44 ... pins=bad ... held=46 absent=0 ...
c1-no-votes   1 C1=unmet ... status_ok=46 quote_ok=46 ... voted=0 dissent=0 failed=votes
c1-witness    0 C1=met ... voted=46 dissent=0
c2-do-nothing 1 C2=unmet tool=absent selftest=error n=0 fixtures=80 agree=0 disagree=0 registry=bad live=error
c2-mode-blind 1 C2=unmet ... agree=60 disagree=20 registry=ok live=ok failed=fixtures
c2-no-band    1 C2=unmet ... agree=73 disagree=7  registry=ok live=ok failed=fixtures
c2-memoriser  1 C2=unmet ... agree=72 disagree=8  registry=ok live=ok failed=fixtures
c2-witness    0 C2=met ... agree=80 disagree=0 registry=ok live=ok
RUN_RC=0
```

Ten receipts were written under `S/evidence/`; the eight controls that need data made a control commit inside a
throwaway `git clone --shared` clone under `S/ctl/` (the two do-nothing controls are scored at the entering tip
itself, so they make none; the script removed every clone). Nothing was committed, staged or checked out in the
lane.

## 2. Verdict-line comparison, all ten controls

Field-by-field (`rev` excluded, as specified; everything else compared literally, exit codes compared exactly,
disagree fixture-name sets compared as sets and split into the 16 frozen fixtures — which do not depend on the
seed — and the 64 seeded ones):

| control | L1 exit | replay exit | fields | disagree L1 → replay (frozen part) |
|---|---|---|---|---|
| c1-do-nothing | 1 | 1 | identical | 0 → 0 (0 → 0) |
| c1-all-held | 1 | 1 | identical | 0 → 0 (—) |
| c1-v72-copies | 1 | 1 | identical | 0 → 0 (—) |
| c1-no-votes | 1 | 1 | identical | 0 → 0 (—) |
| c1-witness | 0 | 0 | identical | 0 → 0 (—) |
| c2-do-nothing | 1 | 1 | identical | 0 → 0 (—) |
| c2-mode-blind | 1 | 1 | **agree/disagree differ** | 27 → 20 (3 → 3, same names, same detail) |
| c2-no-band | 1 | 1 | **agree/disagree differ** | 9 → 7 (1 → 1, same name, same detail) |
| c2-memoriser | 1 | 1 | **agree/disagree differ** | 9 → 8 (0 → 0) |
| c2-witness | 0 | 0 | identical | 0 → 0 (—) |

Replayed receipts verbatim (verdict + exit lines; `$`/header lines differ only by clone path and rev):

```
# control c1-all-held (parts: ledger,allheld,rows,votes); control commit 747f4efbab9f7eeceaa592dde246e25dc9ebb90b
C1=unmet scope=46 rows=46 matched=46 status_ok=44 quote_ok=44 source_rows=ok pins=ok provenance=ok held=44 absent=2 holds=46 changed=0 voted=46 dissent=0 rev=747f4efbab9f7eeceaa592dde246e25dc9ebb90b failed=quote,status
exit=1

# control c1-v72-copies (parts: ledger,rows,votes,v72copies); control commit 70980b1ea16770a669b8ad77a40e30ce7808a4aa
C1=unmet scope=46 rows=46 matched=46 status_ok=44 quote_ok=44 source_rows=ok pins=bad provenance=ok held=46 absent=0 holds=46 changed=0 voted=46 dissent=0 rev=70980b1ea16770a669b8ad77a40e30ce7808a4aa failed=pins,quote,status
exit=1

# control c1-no-votes (parts: ledger,rows); control commit e268e6556ac19b5d0fcbc21f8b92ed73dc7de49e
C1=unmet scope=46 rows=46 matched=46 status_ok=46 quote_ok=46 source_rows=ok pins=ok provenance=ok held=44 absent=2 holds=46 changed=0 voted=0 dissent=0 rev=e268e6556ac19b5d0fcbc21f8b92ed73dc7de49e failed=votes
exit=1

# control c1-witness (parts: ledger,rows,votes); control commit 79e5ac7fe1650e691d9ac280045c5e34a047f4a8
C1=met scope=46 rows=46 matched=46 status_ok=46 quote_ok=46 source_rows=ok pins=ok provenance=ok held=44 absent=2 holds=46 changed=0 voted=46 dissent=0 rev=79e5ac7fe1650e691d9ac280045c5e34a047f4a8
exit=0

# control c2-witness; control commit 27e7cf5ec4dd76bab479a3abaa15a28934922782
C2=met tool=present selftest=pass n=12 fixtures=80 agree=80 disagree=0 registry=ok live=ok rev=27e7cf5ec4dd76bab479a3abaa15a28934922782
exit=0
```

`c1-do-nothing` and `c2-do-nothing` are at the entering tip itself (`rev=20edafa5…`, so their verdict lines
are identical to the L1 receipts **including** `rev=`, because no control commit is made; only the clone path in
the `$`/header lines differs). Frozen-fixture disagreement detail also matched
character for character, e.g. `host-mode0-over: exit want=0 got=1; verdict want='COMMIT_HEURISTIC'
got='COMMIT_LOW'`, `mode1-over: … want='COMMIT_UNLIMITED' got='COMMIT_LOW'`, `mode0-limit-mismatch: verdict
want='COMMIT_HEURISTIC' got='COMMIT_OK'`, `mode2-band-edge-low: exit want=1 got=0; verdict want='COMMIT_LOW'
got='COMMIT_OK'`.

Contract table cross-check (`contract.md` lines 137–146, `…`-elided fragments matched as ordered subsequences):
all ten rows match the L1 receipt and the replay except the three stated `agree=`/`disagree=` pairs:

```
c1-do-nothing  contract table fields match L1 receipt AND replay (exit=1)
c1-all-held    contract table fields match L1 receipt AND replay (exit=1)
c1-v72-copies  contract table fields match L1 receipt AND replay (exit=1)
c1-no-votes    contract table fields match L1 receipt AND replay (exit=1)
c1-witness     contract table fields match L1 receipt AND replay (exit=0)
c2-do-nothing  contract table fields match L1 receipt AND replay (exit=1)
c2-mode-blind  MISMATCH - replay receipt does not contain the contract's stated fields in order
c2-no-band     MISMATCH - replay receipt does not contain the contract's stated fields in order
c2-memoriser   MISMATCH - replay receipt does not contain the contract's stated fields in order
c2-witness     contract table fields match L1 receipt AND replay (exit=0)
```

The three mismatches are the `agree=53/71/71 disagree=27/9/9` cells only; every other field of those rows
(`C2=unmet`, `tool=present`, `selftest=pass`, `n=12`, `fixtures=80`, `registry=ok`, `live=ok`,
`failed=fixtures`, `exit=1`) matches.

## 3. Cause of the three differences, proven

`count-c2.py:397` derives the 64 seeded fixtures from `seed = sha256(<full commit id of R>)`; for a control, `R`
is the control commit. The control commit is created by `controls.py:69-73` (`git add -A` + `git commit`) with
the default author/committer dates, so its hash — and with it the seeded fixture set — changes on every run.
The 16 frozen fixtures (`fixtures = 80` = 16 + 64) are rev-independent.

Proof 1 — recompute each arm from the rev in its own receipt. For each of the four C2 controls that carry a tool
arm, in both its L1 and its replay receipt (8 receipts), regenerating `frozen + seeded(sha256(rev))` and
re-running that control's junk tool against `REF` reproduces that receipt's disagree set **exactly** (names and
count):

```
# recompute each C2 control arm from the seed implied by the rev in its receipt
c2-memoriser   L1      rev=87f557175c27 seed=3a3b782e0d85 agree=71 disagree=9 names_match_receipt=yes
c2-memoriser   REPLAY  rev=a60fc0f19794 seed=6718eae1ebca agree=72 disagree=8 names_match_receipt=yes
c2-mode-blind  L1      rev=55a9d53327ee seed=8274e5c1153d agree=53 disagree=27 names_match_receipt=yes
c2-mode-blind  REPLAY  rev=c2021a4a03ee seed=ff1b858c16d6 agree=60 disagree=20 names_match_receipt=yes
c2-no-band     L1      rev=dcd515560d8d seed=e6beaec6b5e2 agree=71 disagree=9 names_match_receipt=yes
c2-no-band     REPLAY  rev=ff1a38f62604 seed=d8376f35dccf agree=73 disagree=7 names_match_receipt=yes
c2-witness     L1      rev=2890d6c3e09f seed=727f33a617c5 agree=80 disagree=0 names_match_receipt=yes
c2-witness     REPLAY  rev=27e7cf5ec4dd seed=d5db23f9ec39 agree=80 disagree=0 names_match_receipt=yes
```

Proof 2 — pin the commit dates so the rev is reproducible; then the whole verdict line, including the seeded
disagree set, is reproducible, and unpinning it moves again (control `c2-no-band`):

```
pinA      rev=38a5035ca9d744b1da16dfb88550078d2e328b74
          C2=unmet tool=present selftest=pass n=12 fixtures=80 agree=73 disagree=7 registry=ok live=ok failed=fixtures
          disagree=7 mode2-band-edge-low,seeded-04,seeded-14,seeded-18,seeded-22,seeded-24,seeded-47
pinB      rev=38a5035ca9d744b1da16dfb88550078d2e328b74
          (identical line and disagree set)
unpinned  rev=3a35a7085912ae4e834549ffbe3142e34c57c34b
          C2=unmet ... agree=72 disagree=8 ...
          disagree=8 mode2-band-edge-low,seeded-00,seeded-05,seeded-11,seeded-13,seeded-23,seeded-33,seeded-41

pinned runs same rev: True / same verdict line: True / same disagree set: True
unpinned run differs from pinned: rev=True verdict=True disagree_set=True
```

So: no counter or tool behaviour changed between the L1's run and mine; the C2 control `agree`/`disagree`
numbers are a function of the control commit hash and cannot be reproduced from the receipts. The **verdict**
of every control reproduces exactly, which is what the contract's kill rules rest on.

## 4. Independent re-runs at the data tip (read-only, frozen counters, no writes to the lane)

```
$ python3 .ufo/waves/round-53/count-c1.py 2a4213bf8da7 --repo <lane>
C1=unmet scope=46 rows=46 matched=46 status_ok=46 quote_ok=46 source_rows=ok pins=ok provenance=ok held=44 absent=2 holds=46 changed=0 voted=0 dissent=0 rev=2a4213bf8da72f7cd78189baa5bb9be825dca1df failed=votes
rc=1
$ python3 .ufo/waves/round-53/count-c2.py 2a4213bf8da7 --repo <lane> --scratch S/ctl/atdata
C2=met tool=present selftest=pass n=23 fixtures=80 agree=80 disagree=0 registry=ok live=ok rev=2a4213bf8da7…
rc=0
```

Both lines are identical to `evidence/c1-at-data.txt` and `evidence/c2-at-data.txt` (the C1 receipt's
`failed=votes` is the expected pre-vote state; the C1 counter is *not* meant to read met before the RECHECK
arm lands).

## 5. Extra checks on the control set's discriminating power

- **The landed C2 tool is not seed-tuned.** Running `tools/mori-commit-runway.py` as committed at `2a4213bf`
  against `REF` on the 16 frozen + 64 seeded fixtures for 13 different seeds (including the counter's own
  `sha256(2a4213bf…)`) gives `agree=80 disagree=0` on **every** seed — 0 of 13 seeds with a disagreement. A
  tool that had memorised one seed would fail the others.
- **The three junk arms are always detected, but by how much varies.** Over the same 13 seeds:
  `mode_blind` disagree 15–30 (spread 15), `no_band` 3–11 (spread 8), `memoriser` 2–10 (spread 8). Every seed
  keeps `disagree > 0` and `failed=fixtures`, so the qualitative kill is robust; the counts in the contract
  table are not.
- **The C1 control content is deterministic**: all fields, including `status_ok`, `quote_ok`, `held`, `absent`,
  `voted`, `dissent` and the `failed=` list, matched exactly; only `rev` moved. C1 derives every cell from the
  frozen scope and the v7.3 copies with no commit-hash seed (`controls/c1-data.py` reads the scope from the
  clone at `ENTERING`), so only its `rev` can differ between runs.

## 6. Hygiene — lane writes and non-writes

- The lane's ten `evidence/control-*.txt` receipts are **byte-identical** before and after (sha256 recorded
  before the run and diffed after): `control receipts byte-identical (lane untouched)`. The lane HEAD is
  unchanged (`95cf78ee…`), no staged or committed change, no clone/checkout inside the lane.
- **Files my run created inside the lane: none.** The lane holds two ignored bytecode caches,
  `.ufo/waves/round-53/__pycache__/count-c1.cpython-314.pyc` (mtime 22:58:35) and `count-c2.cpython-314.pyc`
  (mtime 22:58:24). Those mtimes are **before** my first receipt (22:59:50) and my controls process ran
  22:59:50–23:00:19, so they were produced by another process importing the frozen counters, not by this seat;
  my run's imports found them fresh (sources unchanged since 22:21/22:24) and did not rewrite them — both
  still carry the same mtimes after my run. They match `.gitignore:3-4` (`__pycache__/`, `*.pyc`), so they are
  invisible to `git status` and touch no tracked file. I left them alone: deleting inside the lane is a lane
  mutation, and other seats are importing the same counters concurrently.
- Everything else I wrote stayed under `/fast/scratch/hyaku/mori-r53/Mo53ExecControlsReplay/` (removed at the
  end, after copying the evidence above into this report). No `/tmp` path is cited as evidence. No host state
  was changed: the only host reads were the tools' own `/proc/meminfo`, five `/proc/sys/vm/*` files and
  `/sys/devices/system/cpu/present`, and the C2 live leg.
- Sibling seats were writing `.ufo/waves/round-53/w1/*.md` concurrently; those files are theirs and were not
  touched. As of my read, the two absent-status rows already carry matching votes in the working tree (Fr08 for
  `0fbd62f51ce8`; Fr10 and Fr12 for `d7a1dc88dcb3`, all with the word `holds`), so no dissent was visible.

## 7. Named limits and items routed to round 54 (counters are frozen — nothing proposed as a fix here)

1. **C2 control readings are not reproducible as written.** Because `count-c2.py:397` seeds the 64 generated
   fixtures from the control commit's own id (created by `controls.py:69-73` without pinned dates), the
   `agree=`/`disagree=` cells in `contract.md:143-145` (53/27, 71/9, 71/9) are artifacts of the L1's particular
   control commit hashes. A replay reproduces the *verdict* of every control (`C2=unmet`, `failed=fixtures`,
   exit 1) but not those numbers. Fix shape for round 54: pin `GIT_AUTHOR_DATE`/`GIT_COMMITTER_DATE` in the
   control builder, or record the seed used next to the count, or state the counts as ranges (measured here:
   mode-blind 15–30, no-band 3–11, memoriser 2–10 over 13 seeds).
2. **The C1 control set does not exercise the vote-arm mutants.** The ten controls contain no `changed`
   disposition anywhere (`c1-data.py:45` leaves `DISPOSITION = {}`), no one-voter arm, no dissent arm, no
   quote-proposing-voter arm, no fenced-vote arm and no tampered-pin arm — all of which `count-c1.py --selftest`
   does cover in memory (`selftest-c1.txt`, 37 checks). Clone-level discrimination of those arms is therefore
   only demonstrated in-process, not against committed control trees.
3. **The C2 control set covers 3 of the 5 mutants its own selftest harness uses.** `no_hugetlb` and
   `string_numbers` (`harness_mutant_no_hugetlb_unmet`, `harness_mutant_string_numbers_unmet` in
   `selftest-c2.txt`) have no control receipt in `evidence/`. Also missing as controls: `harness_registry_unmet`
   and the two `--selftest` floor arms.
4. **The disposition column is uniform `holds` in the landed ledger, including the two `absent`-status rows**
   (`corpus/knowledge/kernel-v7.3-recheck-r53.md` rows for `0fbd62f51ce8` and `d7a1dc88dcb3`). That is
   internally coherent with the entry's prose (the MAP_NORESERVE *rule* survives under the `vma_flags_set`
   spelling; only the quote bytes moved), but it means a RECHECK seat that reads those two rows as `changed`
   produces `dissent=1` and `C1=unmet … failed=votes` at the landed tip. The controls cannot catch that: the
   witness and all-held arms both use all-`holds`, so no committed control exercises a mixed-disposition ledger.
5. **The C2 witness control is tautological by construction** (it wraps the counter's own `REF`), as the
   contract already discloses; it proves feasibility only, not tool correctness. My 13-seed run is the only
   independent evidence I can offer that the authored tool is not seed-tuned, and it is still REF-agreement
   evidence, not kernel evidence.

## Findings

1. **MED** — C2 control verdict counts are not reproducible: the seeded fixture set is keyed to the control
   commit's own id, so `agree=53/71/71 disagree=27/9/9` in `contract.md:143-145` and in
   `evidence/control-c2-mode-blind.txt`, `control-c2-no-band.txt`, `control-c2-memoriser.txt` change on every
   replay (measured 60/20, 73/7, 72/8), while the verdicts and the 16 frozen-fixture disagreements reproduce
   exactly. Cause: `count-c2.py:397` (`seed = sha256(full commit id)`) combined with `controls/controls.py:69-73`
   (unpinned commit dates). Routed to round 54; no counter change proposed this round.
2. **LOW** — The C1 control set never exercises the vote arm: `controls/c1-data.py:45` (`DISPOSITION = {}`) plus
   the absence of one-voter/dissent/author-vote/fenced/tampered-pin controls means those arms are only covered
   in-process by `count-c1.py --selftest` (`evidence/selftest-c1.txt`).
3. **LOW** — The C2 control set omits two of the five mutants its own harness has: `no_hugetlb` and
   `string_numbers` appear only in `count-c2.py --selftest` (`evidence/selftest-c2.txt`), with no
   `evidence/control-c2-*.txt` receipt, so the committed control tree never runs them.
4. **LOW** — `corpus/knowledge/kernel-v7.3-recheck-r53.md` rows `0fbd62f51ce8` and `d7a1dc88dcb3` carry status
   `absent` with disposition `holds`; the counter accepts the pairing, so a RECHECK seat reading those rows as
   `changed` yields `dissent=1` and `C1=unmet … failed=votes`. Current working-tree votes agree with `holds`, so
   the hazard has not fired as of this read.
5. **LOW** — The lane carries `.ufo/waves/round-53/__pycache__/count-c1.cpython-314.pyc` (mtime 22:58:35) and
   `count-c2.cpython-314.pyc` (mtime 22:58:24) from an earlier process importing the frozen counters by
   absolute path. They predate this seat's run (first receipt 22:59:50) and were not created or modified by it;
   both are covered by `.gitignore:3-4`, and no tracked byte or lane index entry changed (`sha256sum` of the ten
   control receipts identical before and after). Reported because any clone-level instrument that imports the
   counters in place leaves such a cache in the lane's wave directory.
