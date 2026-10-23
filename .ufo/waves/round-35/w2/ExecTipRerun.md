measured 2026-10-23T09:14:36Z
# ExecTipRerun — frozen C1 counter re-run at tip, register commit and base

Seat MoriR35.ExecTipRerun, wave 2 (falsify). Attacked: the frozen counter `.ufo/waves/round-35/count-c1.py` — its
outputs, exits, sha256 and determinism at landed tip cedb0ec, register commit 721040a9 and base dd76eb79.

## Frozen inputs
- Counter sha256 27b82d71f2f591df1833c8de793201475d8f01735b5ed4edd7b74e389ee18167 — measured on the lane file and on
  the scratch copy; matches `evidence/c1-freeze.txt:2`.
- Contract sha256 94b7f90a352c96a0b8be17cef62f95647aad06fa84c83d4540751d888d65ba40 (`evidence/c1-freeze.txt:3`) and
  MANIFEST.json@37b51a24 sha256 0b414b8a926f44b54f11fedbbc4f9a00ef2075659dcf1e52db5ff57395ae9952 (`:6`) both remeasured
  unchanged.
- Clone: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone --no-hardlinks <lane> lane-clone` under
  /fast/scratch/hyaku/mori-r35/ExecTipRerun. HEAD cedb0ec4f3a4f672804deac388b7191258f01fcd; no
  .git/objects/info/alternates (independent objects). Lane HEAD read-only: same sha.
- Revs in clone: 721040a9 -> 721040a908103817fe2025b5edd4614f96d791d2; dd76eb79 -> dd76eb79ef4f6d39c9c26647a56d3fb607308f8f.

## Runs — two per revision in the fresh clone
Command shape: `timeout 300 python3 ./count-c1.py <rev> --repo ./lane-clone`

cedb0ec tip, run1 and run2, exit 0 both:
label=P-C1 rev=cedb0ec4f3a4f672804deac388b7191258f01fcd manifest_rev=37b51a243302 register='## Capabilities' oracle=18 rows=18 matched=18 missing=0 bad=0 extra=0 mismatches=0 C1=met

721040a9 register commit, run1 and run2, exit 0 both:
label=P-C1 rev=721040a908103817fe2025b5edd4614f96d791d2 manifest_rev=37b51a243302 register='## Capabilities' oracle=18 rows=18 matched=18 missing=0 bad=0 extra=0 mismatches=0 C1=met

dd76eb79 base, run1 and run2, exit 1 both:
label=P-C1 rev=dd76eb79ef4f6d39c9c26647a56d3fb607308f8f manifest_rev=37b51a243302 register='## Capabilities (round 12 demonstrations)' oracle=18 rows=5 matched=0 missing=18 bad=0 extra=5 mismatches=23 C1=unmet

- `diff run-<rev>-1.out run-<rev>-2.out` empty for all three revisions; stderr 0 bytes in all six.
- Output sha256: tip aa3bc02bbef4471ca208c8ed08a0d081802770363a61849f38650140c1af962f; register
  38a3ec4dd39d89507a4cea7621978a0f1dcac92cd21ca3c00564e46a22b8388d; base
  8633ae8ff78040f225c24eb753c1af608244c4300b56c67dd2efe271e168aa86.

## Determinism beyond the two repeats
- Lane-default form (no --repo): same three summary lines, exits 0/0/1; outputs byte-identical to the clone runs.
- PYTHONHASHSEED 0, 12345, 999983 at tip and 0, 12345 at base: output hashes unchanged (tip aa3bc02b…, base 8633ae8f…).
- Run from cwd /tmp with absolute --repo: identical.
- Second fresh clone (lane-clone2): tip and base reproduce aa3bc02b… and 8633ae8f… exactly.
- Error arm: unknown rev prints one line `count-c1: error: git rev-parse --verify deadbeefdeadbeef^{commit} failed:
  fatal: Needed a single revision` and exits 2, matching the exit contract at contract.md:54-55.

## Agreement with the frozen contract
- Base line matches contract.md:69-70 word for word: rows=5 matched=0 missing=18 bad=0 extra=5 mismatches=23 C1=unmet.
- Tip line matches contract.md:74 word for word: matched=18 missing=0 bad=0 extra=0 mismatches=0 C1=met.
- SCORECARD.md final `## Capabilities` section is byte-identical at 721040a9 and tip (section diff empty), so the
  register-commit rerun and the tip rerun score the same register.
- Heading selection: three headings begin `## Capabilities` at tip (SCORECARD.md:586, :627, :1941); the counter takes
  the last (SCORECARD.md:1941), and no later `## ` heading exists.

## Independent check, not the counter
- MANIFEST.json@37b51a24: 23 mori entries, 13 admitted, 12 admitted with capabilities_added, 18 keys; rounds
  12,14,15,16,18,19,22,24,25,26,28,31 — matches contract.md:23-24.
- Register table at SCORECARD.md:1959-1978: 1 header plus 18 data rows; every row has 5 cells; key set equals the 18
  MANIFEST keys and is unique; every round cell equals the MANIFEST round; 0 empty capability or what cells.

## Sensitivity mutants (sandbox clone, detached commits from tip)
Five one-row mutants of the landed register, each scored by the same frozen counter file:
- mutA row rounds[313] evidence -> `tools/nonexistent-xyz.py`: exit 1, matched=17 bad=1, why absent-at-rev.
- mutD row rounds[313] evidence -> `corpus/knowledge/watchdog-identity-r31.md`: exit 1, bad=1, why weak-path (exists
  at tip but was not landed or named by round 12).
- mutB row rounds[313] round cell 12 -> 999: exit 1, bad=1, why round=999!=12.
- mutE row rounds[313] evidence carrying three backticked paths: exit 1, bad=1, why evidence-paths=3.
- mutG row rounds[313] key -> rounds[999].capabilities_added[0]: exit 1, missing=1 extra=1.
- Restored tip baseline after the series: exit 0, C1=met, output sha256 aa3bc02b….
- Method note: the first mutation pass used unscoped whole-file replaces; two of them (mutA, mutB) hit earlier lines,
  changed no register row and scored met. That is a construction no-op, re-run line-scoped and killed above; it is
  not counter behaviour.

## Hygiene and limits
- Installs or updates: none. No background jobs; every command bounded by timeout; no process left running.
- Writes: this report plus scratch only under /fast/scratch/hyaku/mori-r35/ExecTipRerun/. Lane read-only; the lane
  round-35 directory contains no __pycache__.
- Residual: the counter reads MANIFEST.json from the fleet path at the frozen rev, so runs depend on the fleet repo
  carrying 37b51a24 (it does). P-C1 does not judge cells 2-3 (contract residual, control 10c); the independent check
  found them non-empty, reported beside P-C1 only.
- [INFERENCE] nothing reported as measured depends on an inference; all summary lines above are pasted command output.

## Verdicts
VERDICT: no defect found — frozen counter at cedb0ec, 721040a9 and dd76eb79: outputs, exits 0/0/1, sha256 and repeat runs all match contract.md:69-70 and :74.
VERDICT: holds — rerun claim that the frozen counter prints C1=met exit 0 at tip and register commit and C1=unmet exit 1 at base.
VERDICT: holds — determinism claim: byte-identical across two runs, two fresh clones, lane and clone paths, cwd change and three hash seeds.
VERDICT: killed — mutA absent-at-rev mutation of row rounds[313].
VERDICT: killed — mutD weak-path mutation of row rounds[313].
VERDICT: killed — mutB wrong-round mutation of row rounds[313].
VERDICT: killed — mutE three-evidence-path mutation of row rounds[313].
VERDICT: killed — mutG extra-key mutation of row rounds[313].
