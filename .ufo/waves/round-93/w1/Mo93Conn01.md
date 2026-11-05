# Mo93Conn01 — cross-lane overlap scan (mori round 93, wave w1, attempt 1)

Read-only connector seat. Nothing written outside this report file; no sibling lane touched; no scratch clone
needed (no lane edits; all counting ran read-only against the live trees). Tools installed or upgraded: none
(coreutils grep/sed/awk only; pacman untouched per the pause ruling).

## 1. Literal `/home/vgpnk` in sibling `tools/` and `scripts/` (mori excluded)

Command (prescribed shape; `grep -c` counts matching LINES per file):
```
for lane in /home/vgpnk/Projects/shokunin/*-shokunin; do for tree in tools scripts; do
  grep -rl --exclude-dir=.git '/home/vgpnk' "$lane/$tree" | while IFS= read -r f; do
    printf '%s:%s:%s\n' "${lane##*/}" "${f#"$lane"/}" "$(grep -c '/home/vgpnk' "$f")"; done; done; done
```
Totals: 10 of 20 sibling lanes affected; 188 files; 435 matching lines. Zero-hit lanes: audio, game-dev-2d,
game-dev-3d, kagi, kasegi, kengaku, kotoba, lore, mado, revenger.

kaidoku-shokunin: 93 files, 282 lines, ALL inside round-scoped `tools/round-N` dirs, none at tools top level:
```
kaidoku-shokunin:tools/round-49/ (18 files):92
kaidoku-shokunin:tools/round-44/ (17 files):82
kaidoku-shokunin:tools/round-43/ (3 files):19
kaidoku-shokunin:tools/round-41/ (5 files):8
kaidoku-shokunin:tools/round-39/ (4 files):8
kaidoku-shokunin:tools/round-40/ (3 files):6
kaidoku-shokunin:tools/round-78/ (1 file):11
kaidoku-shokunin:tools/round-{27,28,29,32,33,36,37,38,42,50,50-c3,65,66,67,69,71,72,73,79,80,87,88,89,90}/ (24 dirs, 42 files):56
```
Per-file rows (`lane:path:count`; count=1 clusters braced):
```
chousa-shokunin:tools/absent-split.py:2
chousa-shokunin:tools/build-spans.py:1
chousa-shokunin:tools/freeze-check.py:1
chousa-shokunin:tools/quarantine-check.py:3
chousa-shokunin:tools/research-gate.sh:1
kake-shokunin:scripts/freshness-sweep.mjs:9
kama-shokunin:tools/round37-statement-audit.py:3
kama-shokunin:tools/round38-statement-audit.py:2
kama-shokunin:tools/__pycache__/round86-rendered-cells.cpython-314.pyc:1
kama-shokunin:tools/{echo-recheck,round35-statement-audit,round36-statement-audit,round42-capacity-audit,round43-health-audit,round53-cited-path-check,round54-cited-path-check,round56-env-leg-battery,round58-c2-counter,round59-c2-counter,sources-append-only}.py:1 each (11 files, 11 lines)
kotodama-shokunin:tools/gates/frozen/round-22/d4-repin/freeze-receipt.json:2
kotodama-shokunin:tools/gates/frozen/round-3/selftests/costume-era-consistency-gate.out:2
kotodama-shokunin:tools/gates/frozen/round-3/selftests/provenance-audit.out:14
kumitate-shokunin:scripts/control-replay.mjs:3
kumitate-shokunin:scripts/harm-matrix-gates.json:1
kumitate-shokunin:scripts/plan-before-ready.sh:2
souji-shokunin:tools/cand-s16-cert.py:6
souji-shokunin:tools/souji-vault-verify.impl-24.sh:2
souji-shokunin:tools/{cand-census-07.sh,impl-22.sh,impl-40.sh,souji-census.impl-46.sh,souji-vault-verify.impl-22.sh,souji-verify.impl-09.sh}:1 each (6 files, 6 lines)
souji-shokunin:tools/__pycache__/souji-{axis-check,capability-cells,citation-reconcile,coverage-agreement,freeze-check,gate-check,landing-gate,report-contract,seat-audit,worktree-drift}.cpython-314.pyc:1 each (10 files, 10 lines)
tabi-shokunin:scripts/bidi-firefox-loopback-round35.mjs:4
tabi-shokunin:scripts/check-adjacency.mjs:2
tabi-shokunin:scripts/check-freshness.mjs:3
tabi-shokunin:scripts/check-user-round-contract.mjs:2
tabi-shokunin:scripts/measure-c1-round41.mjs:2
tabi-shokunin:scripts/measure-c1-round43.mjs:2
tabi-shokunin:scripts/playwright-firefox-egress-round39.mjs:3
tabi-shokunin:scripts/playwright-firefox-egress-round41.mjs:4
tabi-shokunin:scripts/playwright-firefox-egress-round43.mjs:4
tabi-shokunin:scripts/playwright-firefox-loopback-round38.mjs:3
tabi-shokunin:scripts/round-evidence-audit.mjs:8
tabi-shokunin:scripts/{chrome-cdp-loopback-round56,-round57,-round58,-round59,check-c2-knowledge-round41,count-c1-round40-binding,measure-c1-round40,selftest-measure-c1-round40,webmcp-validation-round19}.mjs:1 each (9 files, 9 lines)
tameshi-shokunin:tools/trace-inputs.py:2
tameshi-shokunin:tools/__pycache__/{capability-census,capability-census-v2,coldread-precheck-portable,defect-bind,selfstate-freshness}.cpython-314.pyc:1 each + cold-read-forecast.cpython-314.pyc:2 + wave-reconcile.cpython-314.pyc:2 (7 files, 9 lines)
tameshi-shokunin:tools/{cold-read-forecast.py,registry.json,wave-reconcile.py}:1 each (3 files, 3 lines)
tsukuroi-shokunin:tools/check-edit-contract.py:2
tsukuroi-shokunin:tools/{check-adjacency-anchors,check-adjacency-overlap,check-adjacency-table-r50,check-adjacency-table-r51,check-path-reconciliation,check-seat-bindings,check-selftest-tally,mutants-adjacency-overlap,score-census-handoff-r32}.py:1 each (9 files, 9 lines)
```

## 2. `verified-at:` form census over sibling `corpus/knowledge/`

Command (20 sibling globs, mori excluded):
```
G='/home/vgpnk/Projects/shokunin/{audio,chousa,game-dev-2d,game-dev-3d,kagi,kaidoku,kake,kama,kasegi,kengaku,kotoba,kotodama,kumitate,lore,mado,revenger,souji,tabi,tameshi,tsukuroi}-shokunin/corpus/knowledge/'
grep -Rh 'verified-at:' $(eval echo $G) | wc -l                                                -> 1808
grep -Rh 'verified-at:' $(eval echo $G) | grep -Ec '(^|[^0-9a-f])[0-9a-f]{7,12}($|[^0-9a-f])'  -> 217
```
commit_form = 217 lines (line contains a 7-12 char lowercase hex token bounded by non-hex chars on both
sides); date_form = 1808 - 217 = 1591. Case-insensitive recount of the same regex = 217 (no uppercase-only
tokens). Boundary rule: a 40-char full SHA never matches (interior adjacency) and an ISO date never matches
(segments 4/2/2 chars); parenthetical tokens like `(clean shared clone at 859ac24f4106)` do match. Lines
carrying both a date and a hex token count as commit form (spec: "contain a hex token").

## 3. Admission-commit / provenance checkers in fleet `scripts/` and `templates/`

None found. `grep -rniE 'admission|provenance' /home/vgpnk/Projects/shokunin/{scripts,templates}` returns 28
prose-only hits, no executable checker: scripts/hyaku/ufo-wave-policy{,-v2}.json:188,192,242 (policy notes);
scripts/hyaku/lane-addendum.md:581,601,607,628,649; scripts/hyaku/closure-prompt.md:89;
templates/agents/ufo-{critic,distiller,revenger,reviewer,scribe,sentinel,simplifier}.md (role prose);
templates/round-prompt.md:37,59,128,129.
Nearest existing facility: scripts/sources-census.sh (806 lines), the SOURCES-CONTRACT-v1 registry-row
validator (census|validate|overdue|shared|selftest); `grep -cE 'admission|provenance|verified-at|diff-filter'`
on it = 0 — it does not check knowledge `verified-at` values against git admission commits. No script in
either directory does (mori's round-93 count-c1.py does; it lives in the lane, not fleet scripts/).

## Adjacency facts (facts only)

- Stale bytecode retention: 24 hitting `.pyc` files (kaidoku 6, souji 10, tameshi 7, kama 1). In 22 of 24 the
  sibling `.py` source has 0 `/home/vgpnk` hits — the literal survives only in `__pycache__` (checked per file:
  source path rebuilt from the pyc, `grep -ac`; exceptions: tameshi tools/cold-read-forecast.py and
  tools/wave-reconcile.py, whose sources also hit). Source-side cleanup without removing stale `__pycache__`
  leaves the literal on disk.
- Frozen vs live: all kaidoku hits sit in per-round `tools/round-N` dirs; kotodama's 3 hits (18 lines) are
  frozen gate receipts under `tools/gates/frozen/`. Live-surface hits concentrate in chousa, kake, kama,
  kumitate, souji, tabi, tameshi, tsukuroi — the same defect class mori's C2 repairs in mori tools/
  (mori entering: home_literals=18, vgpnk_refs=18, per the frozen contract evidence).

## Checks run / not run

Ran: scan 1 with totals cross-check (kaidoku subtree sums = 93 files/282 lines = lane total; per-lane sums =
188 files/435 lines); scan 2 (total, commit-form, case-insensitive recount); scan 3 (fleet grep +
sources-census.sh characterization); pyc-vs-source mapping (24/24 files). Not run: the frozen counters
(count-c1.py / count-c2.py at any revision — not this seat's scope); no mutations anywhere. Unrun checks
within this seat's spec: none.

Report: .ufo/waves/round-93/w1/Mo93Conn01.md
