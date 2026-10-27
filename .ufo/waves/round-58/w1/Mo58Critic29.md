# Mo58Critic29 — C1 active-register identity

## Finding

**The requested real-layout fixture passes; an ambiguity counterexample remains.** The freeze counter correctly skips the actual superseded first `## Capabilities` section and binds to the round-35 register when both appear in the real order. However, `_find_register` returns the *first* section matching three textual tests (the current-register sentence in the first 12 body lines, absence of ASCII `-- none yet --`, and `| key | capability |`). A first register-shaped decoy retaining the canonical em-dash stub marker can therefore shadow the real register and score `C1=met`.

The counter’s `STUB_MARK` does not match the canonical superseded stub in the freeze revision: `SCORECARD.md:600` is `| — none yet — | | | |`, and the stub table header at line 598 starts `| Capability |`, not `| key | capability |`. Thus the ASCII-marker branch is not exercised by the actual stub. The selftest’s `stub_only_binding_refused` fixture instead uses `-- none yet --`; it does not test the canonical stub bytes.

## Evidence and bounded method

- Read the frozen contract and both frozen counters first; inspected frozen revision `fe8801120a67c1a6b8899d7d0423839caa09e7d0` only. The working-tree counter and freeze-object counter have identical SHA-256: `6ecdb627bb55522c258dc484ed5c530cfd6f7c57c6a89b4c38179df4c0f84e4b`.
- At freeze, the superseded exact heading is `SCORECARD.md:596`; the active round-35 heading is `:1951`, its self-description is at `:1953`, and its table header is `:1970`. It contains 20 `rounds[...]` rows; the two target keys are at `:1989-1990`. The round-12 demonstrations heading is `## Capabilities (round 12 demonstrations)`, so it does not match `_find_register`’s exact heading test.
- Ran the unchanged frozen counter on the freeze revision: `C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none`, exit 0. Its selftest reported `C1_SELFTEST pass=4 fail=0`, exit 0. The entering revision lacks the counter path (`git cat-file -e b783d0b892637ce8d20f188cad20e4d8913ca635:.ufo/waves/round-58/count-c1.py` failed, as the contract says).
- Built isolated scratch git fixtures using a byte-identical copy of the frozen counter, fixture-local `MANIFEST.json`, and valid target pointer objects. Before fixture commits, asserted each fixture’s `git rev-parse --show-toplevel` equaled its explicit fixture lane path. No production files or lane VCS were changed.
  - **Canonical stub first + exact frozen active register second:** `C1=met rows=2 pointers=ok manifest=ok binding=ok`, exit 0. No counterexample to the requested real-layout walk.
  - **Canonical stub alone:** `C1=unmet rows=0 ... binding=bad`, exit 1. This satisfies the refusal outcome; the stub is rejected by missing active preamble/header, not by `STUB_MARK`.
  - **First decoy + real active register second:** made the first section register-shaped, included the canonical `— none yet —` marker, ten padding keyed rows and both round-56 keys with valid pointers; left the genuine active register second. The unchanged counter returned `C1=met rows=2 pointers=ok manifest=ok binding=ok`, exit 0. Since `_find_register` returns the first matching section, this is a false-green bound to the decoy, not the genuine second section.

Fixture receipt (recorded from `/fast/scratch/hyaku/mori-r58/Mo58Critic29/fixture-results.json` before cleanup):

```json
{
  "freeze": "fe8801120a67c1a6b8899d7d0423839caa09e7d0",
  "counter_sha256": "6ecdb627bb55522c258dc484ed5c530cfd6f7c57c6a89b4c38179df4c0f84e4b",
  "stub_first_active_second": {"rc": 0, "output": "C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none"},
  "canonical_stub_only": {"rc": 1, "output": "C1=unmet rows=0 pointers=ok manifest=bad binding=bad failed=binding"},
  "canonical_marker_decoy_then_real_active": {"rc": 0, "output": "C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none"},
  "stub_marker_present_in_freeze_stub": true,
  "ascii_stub_marker_present_in_freeze_stub": false,
  "canonical_stub_header": true,
  "real_active_count_key_rows": 20
}
```

**Correction to scope note:** the compact fixture receipt is preserved above; temporary fixture repositories and scratch receipt files are removed after this report is saved.

## Impacted axis and smallest safe correction

- **C1 calibration — active table identity / counter false-green resistance.** The frozen target revision is correctly identified under the actual SCORECARD layout; the defect is ambiguity handling and the ineffective canonical-stub marker, not a demonstrated failure on the real freeze tree.
- Smallest safe correction for a future counter: recognize the canonical em-dash stub form (and use those exact bytes in selftest), and reject zero or multiple qualifying active-register sections rather than silently taking the first. Add the decoy-first-plus-real-register fixture as a required negative arm. Do not change the frozen counter or claim retroactively.

## Scope

No production edits, corpus/scorecard/log edits, commits, or writes outside this seat’s report and scratch were made. No tool installations. Scratch fixtures and receipts were removed before yielding.
