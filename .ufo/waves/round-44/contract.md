# mori round 44 — frozen contract (declared before any data seat)

Entering tip: `1429c791db5891c484684feef893799909d2d6a8` (round-43 closure admitted;
`corpus/lessons/round-43-verifier-spotcheck.md`, verdict **Admit**).

Lowest non-retired axes at the entering tip: calibration 5 tied with depth 5 and
freshness 5. C1 works calibration (the tied-lowest axis); C2 works operability;
C3 works coverage. Three claims, three distinct axes, causally separable: C1
measures a self-assessment ledger, C2 measures registry conformance of runnable
counters, C3 measures corpus registry/coverage ground. No claim's verification
depends on another claim having landed.

Routed defects this round answers (`corpus/lessons/round-43-verifier-spotcheck.md`
§"Routed defects"): item 3 (count slips: "15 checks" observed 14; "34 seat logs"
observed 8), item 4 (no `SKILL.md` registry row; no `--selftest` mode on the two
new counters), item 5 (receipt measured at `dde525ea` while the verdict claims the
landed tip). Items 1, 2, 6 are durable-record or operator-side and are reported,
not fixed. Item 2 binds this round's own filing: no filed byte is rewritten.

## P-C1 — figure reconciliation (calibration 5)

**Predicate (frozen sentence).** A committed figure ledger
`.ufo/waves/round-44/figures.tsv` carries one row per numeric assertion the round
report makes about a committed artifact class; each row's command is a single
`git` pipeline over `@REV@`; the frozen counter executes every row at the measured
revision and prints `C1=met mismatches=0` only when every row's recomputed value
equals its asserted value, the ledger holds at least 12 rows, and those rows cover
at least 4 of the declared classes {registry, evidence, wave, corpus, checks}.

**Before.** `python3 .ufo/waves/round-44/count-c1.py 1429c791…` →
`check ledger_present FAIL (absent)` → `C1=unmet`, exit 1: nothing reconciles the
lane's reported counts.

**After.** `python3 .ufo/waves/round-44/count-c1.py <landed tip>` →
`C1=met mismatches=0`, exit 0.

**Witness (the class the round-43 closure routed).** The same counter over
`fixtures/figures-r43.tsv`, which reproduces the two superseded figures exactly as
the round-43 report and lesson assert them (14 checks reported as 15; 8 rate-limited
seat logs reported as 34), prints `C1=unmet mismatches=2` and names both rows.

**Kill rules.** A do-nothing control cannot print `C1=met` (no ledger at the
entering tip). A ledger whose commands do not read committed bytes (grammar: the
command must be one `git` pipeline naming `@REV@`, no `echo`/`printf`/`true`
producer) is rejected, not scored. A ledger below the row floor is rejected. An
off-by-one row is a mismatch, not a pass — that is the witness.

## P-C2 — gate-standard conformance (operability 7)

**Predicate (frozen sentence).** Each of the round's counters is a registered gate:
`SKILL.md`'s gate table carries a row whose entry cell names its repo-relative
path and whose eight standard cells (name, kind, entry, verdict map, self-test,
pinned values, write scope, owner) are non-empty; the named path resolves at the
measured revision; the counter's `--selftest` runs over isolated fixtures and
prints a `pass=/fail=` tally with fail 0; a committed mutant of each counter, whose
one check is disabled, is caught by that counter's own selftest (fail ≥ 1); and
`tools/mori-gate-registry.py --selftest` prints a `pass=/fail=` tally with fail 0.
The counter prints `C2=met` only when every one of those holds.

**Before.** `python3 .ufo/waves/round-44/count-c2.py 1429c791…` →
`check counters_present FAIL (absent)` → `C2=unmet`, exit 1.

**After.** `python3 .ufo/waves/round-44/count-c2.py <landed tip>` → `C2=met`,
exit 0.

**Witness (round-43 routed defect 4).**
`python3 tools/mori-gate-registry.py --rev <tip> --audit .ufo/waves/round-43/count-c1s.py .ufo/waves/round-43/count-c2.py`
→ `REGISTRY=unmet` naming both round-43 counters as unregistered and without a
selftest mode.

**Kill rules.** A registry row missing any of the eight cells fails `registry_cells`.
A row naming a path that does not resolve at the revision fails `entry_resolves`.
A counter with no `--selftest` fails `selftest_tally`. A mutant the counter's own
selftest cannot catch fails `mutant_kill`. A counter that prints `C2=met` from a
registry row alone fails `selftest_tally` and `mutant_kill`.

## P-C3 — pid-probe conclusion ground (coverage 6)

**Predicate (frozen sentence).** The lane's corpus gains one admitted knowledge
entry on FR5 ground it did not hold — the `Z`/`X` process-state alphabet and the
three worlds a zero-character `/proc/<pid>/cmdline` read is consistent with — with
its `source:` ids present as `mined` registry rows whose `used-by` names that
entry, a `coverage-map:` naming FR5, a `verified-at:` and a `recheck:`; the registry
census validates at the measured revision with exit 0; and `corpus/README.md`
carries a frontier-map row naming the entry.

**Before.** `git -C . grep -l 'Z ゾンビ' 1429c791… -- corpus/` → 0 files; registry
243 rows.

**After.** the same sweep at the landed tip → 1 file; registry 245 rows (S471,
S472) with census exit 0.

**Kill rules.** A token that is quoted by no opened source fails the Gate. A row
whose source this round did not open is refused (CORPUS.md rule 1). A registry
append that fails the census is not an append. A `used-by` naming an entry that
does not cite the row fails `rows_present`.

## Freeze

The counters, `tools/mori-gate-registry.py`, their fixtures and this contract are
pinned by sha256 in `evidence/freeze-r44.txt` before the first data seat is
dispatched. Their bytes are not amended after any seat scores them; a defect found
post-freeze is recorded as a lesson and routed to round 45, never patched in place.
