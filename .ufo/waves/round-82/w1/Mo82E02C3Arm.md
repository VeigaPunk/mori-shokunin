# Mo82E02C3Arm — revision-precision arm

## Scope and behavior

Axes: depth, operability, freshness, coverage, calibration, adjacency. Detection/report only; no remediation or scalar score claim.

Changed `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-record-sweep.py` and produced this exclusive report at `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-82/w1/Mo82E02C3Arm.md`.

- Added revision bindings: first matching table row must contain the exact numeric token; then resolve the named commit, read the named path at that immutable commit, and require the same token. Each binding is graded; each contributes its first failure as `REVISION_MISMATCH carrier:line row-value|rev-unresolvable|path-absent|rev-bytes`. Missing rows report line 1.
- Added `--git DIR`, defaulting to `--root`. Git operations are argv-only `rev-parse --verify --end-of-options REV^{commit}` and `show COMMIT:PATH`, with captured stdout/stderr and no writes. Resolving to a commit hash prevents a moving revision name from changing between reads.
- Preserved all 26 r81 selftest arms and added ten revision arms, including all six frozen scenarios, first-row strictness, evaluation order, exact token boundaries and revisions-only pins.
- Accepted revisions-only JSON without schema/bindings, matching the frozen counter's independent fixture. Existing command bindings retain their parsing and grading behavior.
- Following L1's explicit interpretation, `bindings=` counts both binding lists. `revisions=` counts revision mismatches and is appended only when pins contains the revisions key, preserving the old summary bytes for r81 pins.
- Updated usage/behavior documentation in the tool header. Pins, SCORECARD, LOG, SKILL, PROVINCE and all external substrates untouched by this seat. No tools installed, no scratch directories created, no git mutations, commits, or subagents.

LSP definitions/references/refactoring were unavailable: no LSP tool is mounted in this seat. Used direct source reads and anchored surgical edits.

## Commands and exact retained output

Commands ran with cwd `/home/vgpnk/Projects/shokunin/mori-shokunin`; both were explicitly requested (the second by L1).

```text
$ python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-record-sweep.py --selftest
case pending-in-round pass
case pending-outside-round pass
case pending-prose pass
case pending-trimmed pass
case pending-exact pass
case round-end pass
case round-subsection pass
case escaped-pipe pass
case first-stating-row pass
case missing-stated pass
case live-single pass
case live-repeated-agreement pass
case live-conflict pass
case live-absent pass
case malformed-json pass
case malformed-schema pass
case malformed-bindings pass
case valid-pins pass
case command-not-shell pass
case clean-totals pass
case dirty-totals pass
case tool-absent pass
case failed-command pass
case missing-live pass
case conflicting-live pass
case missing-stated-mismatch pass
case revision-conformant pass
case revision-D81-1 pass
case revision-unresolvable pass
case revision-path-absent pass
case revision-missing-row pass
case revision-second-stale pass
case revision-first-row pass
case revision-row-before-git pass
case revision-token-boundaries pass
case revision-only-pins pass
RECORD_SWEEP_SELFTEST pass=36 fail=0
rc=0

$ python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-record-sweep.py --root /home/vgpnk/Projects/shokunin/mori-shokunin --pins /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-81/record-pins.json
RECORD_SWEEP_MISMATCH pinned SCORECARD.md:4038 pointers stated=240 live=241 command_rc=1
RECORD_SWEEP pending=0 pinned=1 carriers=1 bindings=1
rc=1
```

The old grammar is retained, but a clean r81 numeric result was NOT verified: the concurrent worktree's pinned command returned 241 and exit 1 against the carrier's 240 at `/home/vgpnk/Projects/shokunin/mori-shokunin/SCORECARD.md:4038`. This integration mismatch was sent to L1; it is not evidence that the new revision arm failed, and no sibling bytes were changed to suppress it.

## Limits and integration gates

Verified: requested in-memory selftest passes all 36 arms under `python3 -I`; the real r81 pins run exercises the existing pending/pinned output paths and honestly reports the live mismatch above.

Not verified: frozen C3 independent Git fixture, full landed-revision C3 keeper, real round-82 pins, pristine r81 lane snapshot, broader build/lint/format/battery. These remain L1 post-integration gates; no passing result is inferred. The selftest stubs read responses in memory and does not exercise an actual Git subprocess.

Known frozen limit: a token occurring anywhere in the named committed path satisfies the revision-byte requirement; the arm does not establish that a historical command produced it or that it belongs to the same historical row. It grades only registered bindings. Token boundaries reject larger identifiers, larger integers, decimals and exponent suffixes.

No new independently established defect in another seat's implementation. The measured carrier mismatch above is an integration observation during concurrent edits, not an ownership attribution.

## Self-evaluation

Accuracy 4/5: exact observed stdout and return codes retained; actual Git-path integration remains unrun. Completeness 4/5: all frozen arm cases implemented, but pristine r81 green cannot be asserted from the current changing carriers. Clarity 4/5: summary compatibility convention is explicitly documented; the frozen interface's binding-count ambiguity required L1 interpretation. Actionability 4/5: files and integration blocker are named; L1 must run the landed keeper. Conciseness 4/5: full requested stdout makes this report longer but preserves evidence. Overall 4.0/5. Highest-impact improvement: exercise the independent fixture and real pins once landed; remeasure the r81 command after carrier integration. User-agreement self-check: no unrun gate is represented as passed.
