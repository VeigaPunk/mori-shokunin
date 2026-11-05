# DigestExec (round 96 w1) — claim C2 pinned-copy work

Full per-row table, receipts and scratch tool output: `.ufo/waves/round-96/w1/digest/DigestExec.md`.
Pinned set for the L1 to copy into `corpus/evidence/`: `.ufo/waves/round-96/w1/digest/pinned/`.

## Verdict

- C2 is **not met** at this seat's candidate. `unpinned` 6 → 3; `ok` 86 → 89; `mismatch=0`; `prefix_only=31` unchanged.
- Pinned (live bytes match recorded): S125 (both sibling receipts, via commit 157ee255 raw fetch), S612, S622.
- Stale, not pinned (live bytes ≠ recorded digest): S615, S616, S623. Repeat fetches byte-identical.
- Sibling path S125 is resolved by the sibling receipts; the entry bytes match the exempt entry digest.

## Commands and outputs supporting the verdicts

```
$ python3 tools/mori-source-digest.py corpus/SOURCES.md corpus/evidence      (baseline)
DIGEST_CHECK rows=124 ok=86 mismatch=0 superseded=1 prefix_only=31 unpinned=6      EXIT=1
$ curl -sSL <6 URLs> ; sha256sum fetched/*.bin
S612 200 357953 0889867a…=recorded; S622 200 375834 f206647f…=recorded
S615 200 362493 5e531ef0… ≠ 7891c588…; S616 200 53982 91bea7a6… ≠ 6842ed0f…; S623 200 171073 f0a03369… ≠ 90ac3b25…
S125 entry 200 27828 ecafdcdd… (exempt entry digest); receipts raw@157ee255: e60f1bbc…, 7adbe069… (= recorded)
$ python3 tools/mori-source-digest.py <scratch SOURCES.md> <scratch corpus/evidence>   (candidate)
DIGEST S125 ok … S612 ok … S622 ok … S615 unpinned … S616 unpinned … S623 unpinned
DIGEST_CHECK rows=124 ok=89 mismatch=0 superseded=1 prefix_only=31 unpinned=3      EXIT=1
$ python3 tools/mori-source-digest.py --selftest
DIGEST_SELFTEST pass=11 fail=0
```

Predicate P2 is not met (unpinned must be 0 and ok 92). Kill rule: C2 unmet.

## Risks for the L1

- S619 (`ast (pinned copy)`, round-90 bytes sha `7891c588…94b0f83b`) carries "supersedes S615". If a live S615 copy were ever pinned and mismatched, the tool would report `superseded-by S619` and drop S615 from `mismatch=`. The registry's rule, not changed here. Diagnostic receipt: `digest/tool-run-diag-stale-live-NOT-PINNED.txt`.
- S615's recorded digest (`…94b8f1a6`) matches neither the round-90 copy (`…94b0f83b`) nor the live bytes. Not edited.
- S623 live page content differs from the recorded copy in the same byte count (171073). S615 and S616 differ from live in 4 bytes each at 253 bytes before EOF; the cause is not identified [INFERENCE].

## Not run

- Census, CORPUS checks and any commit/integration: not run (not assigned to this seat).
- No installs or upgrades this seat.
