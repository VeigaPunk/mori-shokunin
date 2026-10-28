# Mo59Reviewer04 — C1 manifest-arm attack: type/shape mutations of rounds[832]

Seat: `Mo59Reviewer04` (reviewer). Round 59, wave `w1`.
Scope: build manifest fixtures where `rounds[832].capabilities_added[0]` is a
non-string, `capabilities_added` is a dict, `lane_round` is the string `"56"`,
or the two capability strings swap indexes; run the frozen tool
`tools/mori-register-check.py` against each over the real SCORECARD register
and real materialized pointers; report exact reason tokens. Adversarial
finding or explicit no-counterexample result.

Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`
Freeze rev: `60b3a76ad0524c8978cc51922940be1c8c388915`
Entering rev: `2b9f03975bfb6e508f35074ac8181ec8bf54e805`
Scratch: `/fast/scratch/hyaku/mori-r59/Mo59Reviewer04/` (created; TMPDIR set
there; cleaned before yield).
No commits, no lane VCS mutation, no production/corpus/SCORECARD/LOG edits.
Only file written outside scratch: this report.

---

## 0. Frozen-input integrity

```
$ git -C <lane> show 60b3a76:tools/mori-register-check.py | sha256sum
38b733d896f880f5b7ecb464848b80798810ab052fcf0a8afb320918151472b8  -   # == frozen PIN (count-c1.py:46)
$ git -C <lane> show HEAD:tools/mori-register-check.py | sha256sum
38b733d896f880f5b7ecb464848b80798810ab052fcf0a8afb320918151472b8  -   # identical at HEAD (8ff344ff)
$ git -C <lane> show 60b3a76:.ufo/waves/round-59/count-c1.py | sha256sum
2be6fda8c54633fd96f9d447e8e78ff4ba4a6d6136670f79a9d622003f0c9dfd  -
$ sha256sum <lane>/.ufo/waves/round-59/count-c1.py
2be6fda8c54633fd96f9d447e8e78ff4ba4a6d6136670f79a9d622003f0c9dfd    # counter bytes frozen, unchanged
```

The tool exercised below is byte-identical to the frozen PIN, so results apply
to the claimed capability, not to a post-freeze drift.

## 1. Method (bounded)

- Real inputs: `SCORECARD.md` @ HEAD (active register, rows 1989–1990 —
  keys `rounds[832].capabilities_added[0|1]`, names `dual-shape seat-output
  vote binding` / `strict per-event driver-liveness probe`,
  first-working-round cell `56`) and `MANIFEST.json` @ fleet
  `2807c6ab8a9b04dcf256682bcd722c695fdd6e14` (`rounds[832].lane_round` =
  int `56`, `capabilities_added` = 2-string list), extracted via `git show`
  into scratch — exactly the counter's real-arm inputs (count-c1.py:168–195).
- Pointer root materialized for all four evidence pointers
  (`tools/mori-vote-bind.py`, `tools/mori-driver-liveness.py`,
  `.ufo/waves/round-56/evidence/c1-at-landed.txt`,
  `.ufo/waves/round-56/evidence/c2-at-landed.txt`), mirroring
  `materialize()` at count-c1.py:77–88.
- Driver invocation identical to the counter's `run_tool()`
  (count-c1.py:64–74):
  `python3 tool.py --scorecard S --manifest M --root R --require
  'rounds[832].capabilities_added[0]' --require 'rounds[832].capabilities_added[1]'`
- Each mutation is a JSON edit to `rounds[832]` only; scorecard and pointer
  root are held at the known-good baseline.

Baseline (unmutated): `REGISTER_MET`, exit 0, `reasons=[]`, `bound` = both
frozen capability strings — reproduces the counter's real arm.

## 2. Results — assigned mutations

| # | mutation on `rounds[832]` | verdict | exit | reason tokens (verbatim) |
|---|---|---|---|---|
| M1 | `capabilities_added[0]` = `{"name": <entry0>}` (non-string object) | UNMET | 1 | `manifest:entry_missing=rounds[832].capabilities_added[0]` |
| M1b | `capabilities_added[0]` = `null` | UNMET | 1 | `manifest:entry_missing=rounds[832].capabilities_added[0]` |
| M2 | `capabilities_added` = `{"0": e0, "1": e1}` (dict) | UNMET | 1 | `manifest:entry_missing=rounds[832].capabilities_added[0]`, `manifest:entry_missing=rounds[832].capabilities_added[1]` |
| M2b | `capabilities_added` = bare string `e0` | UNMET | 1 | `manifest:entry_missing=rounds[832].capabilities_added[0]`, `manifest:entry_missing=rounds[832].capabilities_added[1]` |
| **M3** | **`lane_round` = `"56"` (string, same text)** | **MET** | **0** | **`reasons=[]` — REGISTER_MET, `bound` identical to baseline** |
| M3b | `lane_round` = `56.0` (float) | UNMET | 1 | `manifest:lane_round=rounds[832].capabilities_added[0]`, `manifest:lane_round=rounds[832].capabilities_added[1]` |
| M3c | `lane_round` = `true` (bool) | UNMET | 1 | `manifest:lane_round=rounds[832].capabilities_added[0]`, `manifest:lane_round=rounds[832].capabilities_added[1]` |
| M3d | `lane_round` = `" 56"` (padded string) | UNMET | 1 | `manifest:lane_round=rounds[832].capabilities_added[0]`, `manifest:lane_round=rounds[832].capabilities_added[1]` |
| M4 | `capabilities_added` = `[e1, e0]` (indexes swapped) | UNMET | 1 | `manifest:name=rounds[832].capabilities_added[0]`, `manifest:name=rounds[832].capabilities_added[1]` |

Verbatim M3 output:

```
{"bound": {"rounds[832].capabilities_added[0]": "dual-shape seat-output vote binding (tools/mori-vote-bind.py, 16/16 selftest, r55 tally re-bound 78/78 while the frozen r55 counter reads voted=0 on the same bytes)", "rounds[832].capabilities_added[1]": "strict per-event driver-liveness probe over .ufo/watchdog.log (tools/mori-driver-liveness.py, 13/13 selftest, live receipt 1728 log lines / 0 malformed / 23 lanes)"}, "pointers": [...4 pointers...], "reasons": [], "schema": "mori-register-check-v1", "verdict": "REGISTER_MET"}
exit=0
```

## 3. Adversarial finding (one counterexample)

**F1 (medium) — `lane_round` binding is type-blind: string `"56"` scores
REGISTER_MET where the contract promises an integer binding.**

- Tool docstring (mori-register-check.py:19): *"`first-working round` cell
  equals rounds[i].lane_round (integer)"*.
- Implementation (mori-register-check.py:173–175):

  ```python
  lr = obj.get("lane_round")
  if cells[4] != str(lr):
      reasons.append("manifest:lane_round=%s" % want)
  ```

  The check coerces the manifest value with `str()` and compares **text**.
  `str(56) == str("56") == "56"`, so a manifest carrying the JSON string
  `"56"` is indistinguishable from integer `56`. The boundary scan (M3b–M3d)
  shows the hole is *exactly* the string whose `str()` rendering matches the
  cell: `56.0` → `"56.0"`, `true` → `"True"`, `" 56"` → `" 56"` all fail
  correctly. The type axis is enforced for `capabilities_added`
  (lines 163–165: `not isinstance(cap, list) … or not isinstance(cap[cai],
  str)` → `manifest:entry_missing`) but **asymmetrically absent** for
  `lane_round`.

- Consequence for the claimed capability: `VERIFIES … (b) exact key/name/
  pointer binding` (contract.md §C1) holds on the real manifest, but the
  checker cannot detect a type-corrupted `lane_round` in a manifest writer —
  `"56"` binds silently, `bound` output byte-identical to the honest run.
  A `manifest:lane_round_type` (or `not isinstance(lr, int)`) check is the
  missing token class; there is currently **no reason token** that can name
  this defect — the tool emits `reasons=[]`.
- Fixture-corpus gap: the 13 committed fixtures cover *value* drift
  (f12 uses `lane_round: 55`, wrong int), name drift (f08/f09), index drift
  (f11) and lane drift (f10), but no fixture exercises a *type* mutation on
  `lane_round`. M3 is therefore uncovered attack surface, not a re-run of a
  committed case.
- Does **not** falsify the frozen C1 claim: the real `MANIFEST.json` @
  `2807c6ab…` carries integer `56`, and every frozen arm (tool sha, selftest,
  13 fixtures, real, pointers) still passes. The finding is a
  binding-strength defect in the landed capability — the checker under-
  verifies what its own docstring and the contract's "exact binding"
  language promise — plus a coverage gap in the hostile-fixture corpus.

**F2 (low, informational) — `bound` cross-maps on the swap mutation.** In M4,
`bound` maps `capabilities_added[0]` → the probe string and `[1]` → the
binding string (entries are recorded before the name check rejects the row,
mori-register-check.py:166–167 vs 184). Harmless because `verdict` is UNMET
and count-c1.py:197–200 requires `REGISTER_MET`, but a consumer reading only
`bound` would inherit a swapped mapping.

## 4. Non-findings (mutations the checker resists)

- All `capabilities_added` shape attacks fail closed: non-string element
  (object, null), dict container, and bare-string container each yield
  `manifest:entry_missing` per required key and `REGISTER_UNMET` exit 1.
  No partial-binding escape: M1/M1b still bind `[1]` honestly while failing
  `[0]` (verdict UNMET overall).
- Index swap (M4) fails via `manifest:name` on both rows — name binding is
  positional, not substring (contract defect #3 fix confirmed on this axis).

## 5. Risks / residual

- C1 is not invalidated by F1, but if any future manifest writer emits
  `lane_round` as a string, the checker will call it bound. Recommend
  (detection only, no remediation performed): `isinstance(lr, int)` in the
  tool and a `lane_round: "56"` fixture in the corpus.
- Method bound: only `rounds[832]` fields mutated; scorecard held fixed.
  The type-hole conclusion does not extend to scorecard-cell attacks, which
  other seats own.

## 6. Tooling

No installs or updates; `pacman` not invoked (paused host-wide). Used:
`git` (read-only `show`/`ls-tree`/`cat-file`), `python3` (stdlib only),
`sha256sum`, `grep`. `disk-guard.sh status` checked before work — green.

## 7. Cleanup

`/fast/scratch/hyaku/mori-r59/Mo59Reviewer04/` (baseline + 9 mutated manifest
dirs, tool copy, pointer root) removed after the outputs above were captured
into §2. Lane tree left clean apart from this report.
