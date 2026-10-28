# Mo59Reviewer05 — C1 real-arm replay (independent re-derivation)

Scope: re-derive the C1 real arm without running the counter's real-arm code —
extract `SCORECARD.md` at freeze `60b3a76ad0524c8978cc51922940be1c8c388915`,
`MANIFEST.json` at fleet `2807c6ab8a9b04dcf256682bcd722c695fdd6e14`, run
`tools/mori-register-check.py` (extracted at freeze, SHA-pinned) with the frozen
`--require` pair, materialize pointers, compare verdict/bound/pointers to the
committed receipt `.ufo/waves/round-59/evidence/c1-at-freeze.txt`.

## Result: no counterexample — replay agrees with the committed receipt

Committed receipt (`.ufo/waves/round-59/evidence/c1-at-freeze.txt`):
`C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=60b3a76a…`, rc 0.
My independent replay of the `real` and `pointers` arms (the only arms in this
seat's scope) reproduces both `ok`; no divergence found.

## Evidence (all commands run from scratch `/fast/scratch/hyaku/mori-r59/Mo59Reviewer05`, TMPDIR set)

1. Input extraction, read-only:
   - `git -C <fleet> rev-parse --verify 2807c6ab…` → commit present;
     `cat-file -e 2807c6ab:MANIFEST.json` → ok. Manifest is 2,439,846 bytes;
     `rounds[832]` → `lane=mori lane_round=56 verdict=admitted
     commit=mori-shokunin@eac193ca…`; `capabilities_added[0]` =
     "dual-shape seat-output vote binding (tools/mori-vote-bind.py, …)",
     `capabilities_added[1]` = "strict per-event driver-liveness probe over
     .ufo/watchdog.log (tools/mori-driver-liveness.py, …)". Both begin with the
     frozen BOUND names (count-c1.py:35-40).
   - `git -C <lane> show 60b3a76a:SCORECARD.md` → 2,937 lines. Three
     `^## Capabilities` heads (lines 596, 637, 1951); exactly one section
     self-declares "current capabilities register" (line 1953, inside the
     1951 section per contract `SCORECARD.md:1951-1953`). `n_decl == 1` holds.
   - `git show 60b3a76a:tools/mori-register-check.py` →
     sha256 `38b733d896f880f5b7ecb464848b80798810ab052fcf0a8afb320918151472b8`
     == counter PIN (count-c1.py:41).
   - Frozen counter bytes unchanged: `sha256sum` of working-tree
     `.ufo/waves/round-59/count-c1.py` == `git show 60b3a76a:…count-c1.py`
     (`2be6fda8…0c9dfd`). Working tree is clean of counter edits at entering
     HEAD `8ff344ff`.

2. Register rows (extracted scorecard, lines 1989–1990, inside the declared
   section 1951–1992): exactly two `rounds[832]` key cells —
   `capabilities_added[0]` name `dual-shape seat-output vote binding`,
   `capabilities_added[1]` name `strict per-event driver-liveness probe`,
   each with `first-working round` cell `56` == `lane_round`, and evidence
   cells carrying backticked pointers `tools/mori-vote-bind.py`;
   `.ufo/waves/round-56/evidence/c2-at-landed.txt` and
   `tools/mori-driver-liveness.py`; `.ufo/waves/round-56/evidence/c1-at-landed.txt`.
   The only other `rounds[832]` text occurrence (line 2915) is a scoring-table
   row outside the declared section whose first cell fails `KEY_CELL` — ignored.

3. Tool pass 1 (learn pointers), cwd=scratch:
   `python3 tool/tool.py --scorecard real/scorecard.md --manifest real/manifest.json
   --root real/_root --require 'rounds[832].capabilities_added[0]'
   --require 'rounds[832].capabilities_added[1]'`
   → rc 1, verdict REGISTER_UNMET, reasons = only `pointers:missing=…` ×4
   (expected: `_root` empty on first pass); `pointers` list = exactly the four
   above; `bound` already maps both REQUIRE keys to the full manifest strings.

4. Pointer resolution at freeze (counter's `git cat-file -e R:path` arm):
   all four pointers `cat-file -e` ok and `cat-file -t` = `blob`
   (not trees — see residual risk). Materialized via `git show` into `_root`.

5. Tool pass 2 (cwd=scratch):
   → rc 0, `{"verdict": "REGISTER_MET", "reasons": [],
   "bound": {rounds[832].capabilities_added[0]: "dual-shape seat-output vote
   binding (tools/mori-vote-bind.py, 16/16 selftest, r55 tally re-bound 78/78
   while the frozen r55 counter reads voted=0 on the same bytes)",
   rounds[832].capabilities_added[1]: "strict per-event driver-liveness probe
   over .ufo/watchdog.log (tools/mori-driver-liveness.py, 13/13 selftest, live
   receipt 1728 log lines / 0 malformed / 23 lanes)"}, "pointers": [the four]}`
   `sorted(bound) == sorted(REQUIRE)` and each bound entry startswith-matches
   its frozen BOUND name → `real_ok = ptr_ok = True`, matching receipt
   `real=ok pointers=ok`.

## Method bounds / adversarial surface checked

- Verified by hand, not by re-running `count-c1.py measure()`: unique-register
  identity (1 declarer of 3 heads), exact key/name/lane_round binding, name
  boundary semantics (`name (` prefix binds; alnum-continuation would not),
  pointer grammar (relative, no `..`/`~`/absolute), and both passes' rc/verdict.
- Receipt `rev=` is an argv echo, not a proof of the freeze commit; the real
  content binding is via `git show R:` reads, which I reproduced at the full
  40-hex freeze sha.
- Residual risk (unexercised by the real arm, not a divergence): a directory
  pointer would pass `git cat-file -e` (trees exist) and counter
  `materialize()` would write `git show`'s text listing as a regular file that
  then satisfies the tool's `is_file()` check — a directory-valued evidence
  pointer could be accepted. All four real pointers are blobs, so no effect
  on this receipt; worth noting for future register rows.
- `bound[want]` is populated even on `manifest:name` mismatch, but the verdict
  gate (`reasons` empty → REGISTER_MET) plus the counter's `startswith` check
  keep that unexploitable here.

## Verdict

`real=ok` and `pointers=ok` re-derived independently; consistent with the
committed receipt at the amended freeze revision. No production edits, no VCS
mutation; scratch cleaned after copying this evidence.
