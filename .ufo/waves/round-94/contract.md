# Round 94 — frozen contract (mori, L1 MoriR94, attempt 1)

Entering revision `84b152308fa6c2f224ad75dff68e525dab9057ac` (lane `master` = origin, `jj-lane.sh state`
clean except three orchestrator markers, not lane work). This contract, the two round-94 counters
(`count-c1v2.py`, `count-c2v2.py`), the controls script (`controls-r94.py`), the premise and entering
receipts under `evidence/`, and the wave spec are committed before any wave dispatch. Axes:
**calibration** (C1, score 5, tied lowest non-retired with depth and freshness) and **operability**
(C2, score 7). Two claims, distinct axes. No score is moved by this contract; each claim is admitted only
if its frozen predicate is met at the landing revision, the kill rule does not fire, and no axis is harmed.

Shape: ONE v1 wave, `w1`, 12 seats (band 8–16), attack seats 6/12 (reviewer 2, critic 2, mutation-tester 2),
connector 1, executor 3, scribe 1, scout 1. Planner is the L1 (the validator rejects `planner` as a swarm
role; the L1 holds the §3 planner seat). No residual call.

## Premises (QUALITY 196 — grepped and committed before the freeze; `evidence/premises-r94.txt`)

- P1 (R02, round-93 routed defect): the frozen round-93 counter `count-c1.py:141` tests
  `ac[:7] in va`, a plain substring with no token boundary, so a 7-character admission prefix embedded
  in a longer token passes.
- P2 (counter host path, round-93 routed defect): `/home/vgpnk` appears in `.ufo/waves/round-93/count-c1.py:39`,
  `count-c2.py:39` and `controls-r93.sh:81` (the last twice). These are frozen history and are not edited.
- P3 (token shape, measured): all 19 round-92 trio files carry an 8-character `%h` admission prefix as the
  first token of `verified-at:` and it is a prefix of the admission `%h` (19/19 `token_prefix=True`). So the
  v2 rule reads live data as the v1 rule does; the controls, not the live data, separate them.
- P4 (carried, not claimed): the digest-gate debt (31 prefix-only rows, S125 unpinned; round-93 contract P3)
  and the round-90 nonce guard (QUALITY 191) are carried. Completing a recorded digest in place edits an
  anchor cell, which CORPUS.md rule 2 forbids.
- P5 (sourced claim, frontier step): the v2 rule is `str.startswith`, prefix equality, not `in`. Source
  S624 (Python str.startswith, opened this round; access 2026-11-05; sha256
  `2397d83204d8901b852e5dcb72cb1b5cbf311e9db1f15116089b85ab21d22b68`, 815447 bytes; located quote
  "Return True if string starts with the prefix , otherwise return False ." at the `str.startswith` anchor
  of https://docs.python.org/3/library/stdtypes.html). Row S624 is appended at landing; its used-by is the
  lesson of this round and the knowledge entry that cites it.

## Claims

### C1 — calibration (score 5, tied lowest non-retired): the round-92 trio admission self-check cannot pass an embedded hash

- **Teaching target.** The round-93 closure found the admission check accepts a hash embedded inside a longer
  token (P1). The check is the counter that certifies the round-92 lesson's sentence "each verified-at names
  the admission commit of its file". A self-check that accepts a forged admission is an overreach the counter
  fails to catch, which is a calibration defect of the lane's self-description.
- **Predicate P-C1 (one sentence, same in `count-c1v2.py`, `controls-r94.py` and this line).** On the
  frozen battery of three embedded-hash fixtures (left, right, middle; `controls-r94.py`), the frozen v1
  counter reads `C1=met` on all three (false pass 3/3) and the round-94 v2 counter reads
  `C1=unmet checks_failed=admission` on all three (0/3 false passes), while v2 on the unmodified base and on
  the landing revision reads `C1=met … adm_ok=19 adm_fail=0 patched12=12 seven_same=7 census=ok` (live data
  still passes). Counting command: `python3 -I .ufo/waves/round-94/controls-r94.py <lane> <fleet>` prints
  `EMBED_FALSE_PASS v1=3/3 v2=0/3 live_v2=met …` and exits 0; the landing check is
  `SHOKUNIN_ROOT=<fleet> python3 -I .ufo/waves/round-94/count-c1v2.py <landing> --repo <lane>` exits 0.
- **Before** (entering `84b15230`; `evidence/controls-r94.txt` and `evidence/entering-c1-r94.txt`):
  v1 `EMBED_FALSE_PASS v1=3/3`; v2 on the battery is not the claim's before (it is the candidate).
- **After.** Measured at the landing revision; the battery is re-run there with the same controls.
- **Do-nothing control.** Keeping the frozen v1 counter reaches `v1=3/3` (false passes) on the battery, so the
  predicate is unmet by doing nothing. The text-only control is not separate: the predicate reads the counter's
  verdicts on committed fixture bytes, not any sentence.
- **Kill rule (C1).** Any of: v2 false-passes any battery fixture (`v2` count > 0); v2 reads any live trio file
  as `adm_fail` at the landing; the v1 battery expectation fails (v1 reads an embedded fixture as unmet, so the
  battery does not discriminate v1 and the claim is unprovable, not met); census fails.
- **Named limits (C1).** The rule checks that the first token of `verified-at:` is a prefix (≥7 chars) of the
  admission `%h`. It does not check that the admission commit introduced the file's current content (round-93
  named limit). A future `%h` shortening to 7 characters would fail the 8-character tokens; that is a
  repository-growth limit to re-measure, not a hidden pass.
- **Sourced (frontier step).** The prefix semantics rest on S624 (P5).

### C2 — operability (score 7): the round-94 counters carry no host home path and run with HOME unset

- **Predicate P-C2 (one sentence, same in `count-c2v2.py` and this line).** At revision R,
  `SHOKUNIN_ROOT=<fleet> python3 -I .ufo/waves/round-94/count-c2v2.py R --repo <lane> --root <fleet>` prints
  `C2=met literal_r94=0 files_r94=3 frozen_r93=unchanged env_i=met env_unset=rc2 rev=<12>` and exits 0, where
  `literal_r94` counts `/home/<user>` occurrences in every `.py`/`.sh` under `.ufo/waves/round-94/`
  (must be 0), `frozen_r93=unchanged` pins the three round-93 counter blob hashes (`count-c1.py`
  45a9d07d…, `count-c2.py` 7d0a003c…, `controls-r93.sh` be60882e…), `env_i=met` runs `count-c1v2.py` from the
  extracted tree with `HOME=/nonexistent` and `SHOKUNIN_ROOT` set and gets `C1=met`, and `env_unset=rc2`
  runs it with `SHOKUNIN_ROOT` unset and no `--census` and gets exit 2 (fails closed).
- **Before** (entering; `evidence/entering-c2-r94.txt`): the round-93 counters carry `literal=6` over
  `.ufo/waves/round-93` (5 `.py`/`.sh` files, diagnostic scan `count-c2v2.py … --report --scan
  .ufo/waves/round-93`), and the round-94 counters do not exist at the entering revision, so the full check reads
  `C2=unmet literal_r94=0 files_r94=0 … checks_failed=files,env_i`.
- **After.** Measured at the landing revision.
- **Do-nothing control.** The entering tree reads `C2=unmet`, so the predicate is unmet by doing nothing.
- **Kill rule (C2).** Any of: a `/home/<user>` literal in any round-94 `.py`/`.sh` (`literal_r94` > 0); fewer than
  3 round-94 counter files; any round-93 counter blob hash changed; `env_i` unmet (the counter needs HOME or a
  host path); `env_unset` not rc 2 (a silent fallback exists).
- **Named limits (C2).** The scan matches `/home/<user>` only; `~user`, `/Users/`, `C:\Users` and `$HOME`
  expansions are outside the literal regex (attacked by a reviewer seat in the wave). The round-93 counters
  keep their literals as frozen history (named debt, not edited). `env_i` runs one counter, not the whole
  counter family.

## Controls and receipts (committed with the freeze)

- `controls-r94.py` — do-nothing (v1 and v2 on base), three embedded-hash fixtures, each one commit in a
  scratch clone (identity `mori-r94-controls`, toplevel checked before commit). Pre-freeze run at the base:
  `EMBED_FALSE_PASS v1=3/3 v2=0/3 live_v2=met do_nothing_v1=C1=met do_nothing_v2=C1=met`, exit 0
  (`evidence/controls-r94.txt`).
- `count-c2v2.py` — pre-freeze runs: at the base `C2=unmet` (no round-94 counters at the base);
  diagnostic `literal=6` over the round-93 counters (`evidence/entering-c2-r94.txt`).
- Mutation kill (wave seat `Mo94M01Mut`, `Mo94M02Mut`): frozen controls must kill each named v2/C2 mutant or the
  survivor is recorded as a control-battery gap for the lesson.

## Learning and frontier step (CORPUS.md; protocol §2b)

- SOURCES: rows before→after by `scripts/sources-census.sh validate --root <fleet> mori` (entering: `mori ok`, exit 0;
  S624 added at landing). Census entering: exit 0.
- Mistake mined (lesson `## Mistakes`): `untracked-orchestrator-marker` — the round-92 and round-93 orchestrator
  dispatch markers (`*.ready.dispatched`) sit untracked in the lane porcelain (round-93 spot-check D3; `jj-lane.sh
  state` shows `untracked=3` at entering). Captured-by: none. Fix: a `.gitignore` rule; red-before `git check-ignore`
  exit 1, green exit 0 (shown able to fail).
- Routed, not claimed: digest debt P4 (round-93 contract P3 carried); round-93 spot-check D1 (no planner seat in
  the L2 floor) is answered by the Shape line above (the L1 holds the planner seat; the validator refuses
  `planner`).

## Frozen order (the ordering is the proof)

1. This contract, `count-c1v2.py`, `count-c2v2.py`, `controls-r94.py`, `evidence/*` — one `jj-lane.sh commit` (freeze).
2. `w1-spec.json`, `w1-dispatch.json`, `w1/swarm-registry.json` — second commit, before the `.ready` file.
3. `w1.ready` — written by the L1 after validation, never rewritten.
4. Wave results and seat outputs under `w1/`; attacks cite the frozen artifacts.
5. Landing: S624 row, round-94 lesson, `.gitignore` rule, QUALITY criteria, SCORECARD and LOG entries,
   measured at the landing revision by the frozen commands above.
