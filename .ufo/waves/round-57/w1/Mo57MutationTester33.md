# Mo57MutationTester33 — C1 capability-table probe

## Routed defect and exact surface

`corpus/lessons/round-56-verifier-spotcheck.md:81-86` routes item 4: no capability row entered in the round-56 SCORECARD section; fix is to enter vote-binding (and driver-liveness if claimed) per AXES.md §Capabilities. AXES.md §Capabilities says the SCORECARD carries a separate repertoire table (name, description, evidence pointer, first-working round), and rows enter only through a round that demonstrates the capability running.

The frozen detector at `.ufo/waves/round-57/count-c1.py:9-11` selects the text between the **first** `## Capabilities` and following `## Saturation`, then accepts exactly two matching pipe rows if each contains the round-56 directory substring and `| 56 |`. At freeze `618562c72a03dc4d17386b715357f863fd327274`, that section is SCORECARD.md:596-604: the `— none yet —` placeholder and its note. The actual register is a later `## Capabilities` at SCORECARD.md:1951; its own description says it supersedes the first placeholder, which is left as filed. Thus a convention-following register/per-round capability entry is invisible to the frozen C1 detector. The routed correction is underspecified as to placement; C1's operative surface is the historical first section, not the current register.

The second exact gap is resolvability: the contract says “resolvable round-56 evidence pointer,” but the detector checks only for `.ufo/waves/round-56/` in row text. It does not resolve a file/path or check artifact contents.

## Bounded mutation probe

Scratch fixture was built from `git archive` of the freeze tree under `/fast/scratch/hyaku/mori-r57/Mo57MutationTester33/fixture`; `git rev-parse --show-toplevel` returned that fixture path before its commits. Detector copy differed from frozen bytes only in the hardcoded `repo` path, redirected to the scratch fixture; predicate code was unchanged. Frozen counter SHA-256: `7156fb4bb29f27881091b22dfa7ef3d661b1e955a1ec9a4d13e48013f1b368ec`.

- Pristine fixture: `C1=unmet rows=0 evidence=bad rev=eaea9c73df6c70d0caa0528dc781f930362838fb`, exit 1. The lane counter at entering tip likewise returned `C1=unmet rows=0 evidence=bad rev=53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2`, exit 1; at freeze it returned the same shape with freeze rev, exit 1. Expected before-state; baseline is usable.
- Mutant: replaced the placeholder with two rows named `driver-liveness` and `vote-binding`, each with first-working `56`, but each evidence pointer was `.ufo/waves/round-56/does-not-exist.md`. Fixture counter output: `C1=met rows=2 evidence=ok rev=fdd9fecf7ccdbd9b5f1abaa09ef022de3ee196ef`, exit 0. `git cat-file -e <mutant>:.ufo/waves/round-56/does-not-exist.md` failed (128). **Survived**: the frozen predicate accepts unresolvable pointers. This is a coverage finding, not grounds to alter the frozen contract/counter.
- Restoration: restored SCORECARD.md bytes from the pristine fixture commit. Restored SHA-256 `c2c40693c30987e27e1ff9bcd92d50c430ff5fbd6ec46e7c655ceeaa1abe452f` equals pristine SHA-256 exactly; restored detector output returned to `C1=unmet rows=0 evidence=bad`, exit 1. Scratch directory was removed before report completion. No lane production bytes or commits were changed.

## Falsifiable correction recommendation

At the scored revision, place the two demonstrated rows on the detector's first-section surface (SCORECARD.md:596-604) if C1 is to be satisfiable under its frozen code; use real round-56 paths. At freeze, `git cat-file -e <freeze>:.ufo/waves/round-56/evidence/driver-liveness-live.txt`, `.../evidence/selftest-vote-bind.txt`, `.../corpus/knowledge/driver-liveness-r56.md`, and `.../corpus/knowledge/vote-binding-r56.md` all resolve. Replacing either row with a missing pointer currently leaves the detector green, as the mutant demonstrates; the independent resolution check is therefore required to substantiate the contract's “resolvable” wording. Because placing rows in the first section conflicts with SCORECARD's stated “left as filed”/superseded status, record an explicit append-only correction to that convention alongside the rows, rather than silently treating the historical placeholder as the current register. A future re-frozen counter could instead bind to the actual register, but do not alter the frozen predicate in this wave.

No tools installed.