# Mo56MutBinder2 — mutation test of tools/mori-vote-bind.py (round 56, wave w1)

Date: 2026-10-27. Seat: mutation-tester (leaf, no subagents). Scope: falsify the
C2 tool's detector power by mutating scratch copies of
`tools/mori-vote-bind.py` at the freeze tip
`8be2717b0809281d07dffe83dad424a4859e0747` and running the frozen detectors on
pristine, mutated, and restored bytes. The lane repo file was never modified;
all mutants lived in scratch. Machine: MACHINE_ID (host reads were not needed;
no host state touched).

## Godspeed axes

- detection power: share of behavior-bearing mutants killed by the frozen detectors
- coverage breadth: distinct behavior points probed (channel choice, fence state,
  ledger column index, dissent metric, write-wins order, grammar width, overclaim
  guard, bound_voter counting)
- evidence fidelity: verbatim outputs + sha256 before/after for every run
- cost: ~10 s total runtime, one scratch tree, zero repo writes

## Detector (bounded, identical for every run)

- D1 selftest: `python3 <tool> --selftest`; pass requires exit 0 and stdout
  containing `VOTE_BIND_SELFTEST pass=16 fail=0`.
- D2 tally over committed r55 bytes: `python3 <tool> tally --ledger <ledger>
  --results <results> --verb RECHECK --voter Mo55Rc01 .. --voter Mo55Rc16`
  (all 16 voters passed); pass requires exit 0 and stdout containing exactly
  `TALLY rows=78 agree=78 double=68 single=10 zero=0 dissent=0 voters=16 bound_voters=15`.
- Verdict: killed(selftest), killed(tally), killed(selftest+tally), SURVIVED
  (both green), or INCONCLUSIVE (baseline red). A killed verdict records which
  detector fired.

Baseline (pristine copy, before any mutant): D1 `rc=0`, D1 line
`VOTE_BIND_SELFTEST pass=16 fail=0`; D2 `rc=0`, D2 line exactly the frozen
tally. Baseline green, so every verdict below is conclusive.

Inputs were materialized from the freeze revision with `git show <rev>:<path>`
(read-only), sha256:
`462e67c148d66ce1f886d21540474a19bd6244ae56c5fc1c5c8391ba6e7d5e8e`  corpus/knowledge/kernel-v7.3-recheck-r55.md (ledger)
`2e5b0a0f94d1fa5b90b2804d370db87d25d5197fa65bc4f26441d939b8d9763b`  .ufo/waves/round-55/w1-results.json (results)
Pristine tool copy sha256
`8be1acdbb36cd68deba005e21a4a8679534ab5a5099a787aa9335d288dfa6bca` — equals the
PIN frozen in `count-c2.py`; the working-tree file is byte-identical to the
freeze-rev blob (checked). No tool installs were needed (record per operator
directive: none made).

## Mutants and verdicts

Each mutant is a single-site exact-string replacement on the scratch copy
(site uniqueness asserted before applying). Full per-run outputs were captured
to files and are quoted verbatim below.

| id | site (file:line) | mutation | D1 selftest | D2 tally@r55 | verdict |
|----|------------------|----------|-------------|--------------|---------|
| M1 | tools/mori-vote-bind.py:85 | JSON parse skipped (`doc = None`), text channel always | fail=7 | `zero=78 bound_voters=0` | killed(selftest+tally) |
| M2 | :98 | fence state never toggles (`if False and FENCE_RE.match(line)`) | fail=1 | unchanged | killed(selftest) |
| M3 | :153 | read_ledger disposition from cell 5, not 6 | fail=2 | `agree=0` | killed(selftest+tally) |
| M4 | :182 | dissent counted per disagreeing voter pair, not per hash | pass | unchanged | SURVIVED |
| M5 | :115 | last-write-wins inverted to first-write-wins (`setdefault`) | fail=2 | unchanged | killed(selftest) |
| M6 | :34 VOTE_RE | hash12 `{12}` relaxed to `{7,}` | fail=1 | unchanged | killed(selftest) |
| M7 | :91 | `match(s.strip())` → `search(s)` (attempted guard drop) | pass | unchanged | EQUIVALENT (no behavioral effect on any input) |
| M7b | :91 | anchors dropped via `re.search(r"(RECHECK\|ENTAIL)\s+([0-9a-f]{12})\s+([A-Za-z][A-Za-z0-9_-]*)", s)` — group(4) lost | fail=8 (EXC) | rc=1 crash | killed(selftest+tally), mechanical |
| M7c | :91 | anchors dropped, groups preserved: `re.search(r"(RECHECK\|ENTAIL)\s+([0-9a-f]{12})\s+([A-Za-z][A-Za-z0-9_-]*)(?:\s(.*))?", s)` | fail=2 | unchanged | killed(selftest) |
| M8 | :199-200 | `bound_voters` counts any roster output (`if True`) | fail=1 | `bound_voters=16` | killed(selftest+tally) |

Named mutants were M1-M4 as tasked; M5, M6, M7(M7b/M7c), M8 are of my own
devising (5 devised probes, 9 behavioral runs total, one of which — M7 — was
reclassified as an equivalent mutant and superseded by M7c).

### Verbatim detector outputs (killed mutants)

M1 selftest: `rc=1`

    VOTE_BIND_SELFTEST pass=9 fail=7 failed=t_json_array_binds,t_json_nested_binds,t_json_string_doc_binds,t_fenced_scalar_ignored,t_last_wins_json:EXC:('RECHECK', 'a6e5226259c9'),t_last_wins_json,t_entailed_verb_parsed:EXC:('ENTAIL', '7b2d297eec60'),t_entailed_verb_parsed,t_tally_mini

M1 tally: `rc=0`

    TALLY rows=78 agree=0 double=0 single=0 zero=78 dissent=0 voters=16 bound_voters=0

The M1 collapse is exactly the do-nothing control signature (`zero=78`), so the
control arm of P-C2 independently catches channel loss.

M2 selftest: `rc=1` — `VOTE_BIND_SELFTEST pass=15 fail=1 failed=t_fenced_text_ignored`; M2 tally: `rc=0`, frozen line unchanged.
M3 selftest: `rc=1` — `VOTE_BIND_SELFTEST pass=14 fail=2 failed=t_tally_mini,t_roster_and_name_filter`; M3 tally: `rc=0`

    TALLY rows=78 agree=0 double=68 single=10 zero=0 dissent=0 voters=16 bound_voters=15

M5 selftest: `rc=1` — `VOTE_BIND_SELFTEST pass=14 fail=2 failed=t_last_wins_text,t_last_wins_json`; M5 tally: `rc=0`, frozen line unchanged.
M6 selftest: `rc=1` — `VOTE_BIND_SELFTEST pass=15 fail=1 failed=t_hash_len_drift_rejected`; M6 tally: `rc=0`, frozen line unchanged.
M7b selftest: `rc=1` — `VOTE_BIND_SELFTEST pass=8 fail=8` (all JSON-channel cases raise `no such group`); M7b tally: `rc=1`, `IndexError: no such group` at the JSON `m.group(4)` — a mechanically broken probe (my regex dropped group 4), superseded by M7c which preserves the groups.
M7c selftest: `rc=1` — `VOTE_BIND_SELFTEST pass=14 fail=2 failed=t_fenced_scalar_ignored,t_json_prose_substring_rejected`; M7c tally: `rc=0`, frozen line unchanged.
M8 selftest: `rc=1` — `VOTE_BIND_SELFTEST pass=15 fail=1 failed=t_tally_mini`; M8 tally: `rc=0`

    TALLY rows=78 agree=78 double=68 single=10 zero=0 dissent=0 voters=16 bound_voters=16

### Survivor cross-check against the real r55 tally (M4)

M4 (dissent per disagreeing voter pair) passed D1 (`pass=16 fail=0`) and its D2
run over the committed r55 bytes printed, `rc=0`:

    TALLY rows=78 agree=78 double=68 single=10 zero=0 dissent=0 voters=16 bound_voters=15

byte-identical to the frozen tally: the mutant is indistinguishable on the
pinned data. I then proved the mutation site is behavior-bearing (i.e. the
survivor is a real coverage gap, not an equivalent mutant) with a 3-voter
synthetic (one hash; words holds/holds/stale):

    M4-probe pristine: TALLY rows=1 agree=0 double=1 single=0 zero=0 dissent=1 voters=3 bound_voters=3
    M4-probe mutant:   TALLY rows=1 agree=0 double=1 single=0 zero=0 dissent=2 voters=3 bound_voters=3

### M7 equivalence note and M7c behavior-bearing proof

M7 (`match` → `search` with the same anchored pattern) is an EQUIVALENT mutant:
`VOTE_RE` is fully `^...$`-anchored, so `search ≡ match` on every input, not
just on the pinned bytes. The guard semantics live jointly in the anchors and
the `match()` call, so the faithful guard-drop is M7c (anchors dropped, groups
preserved). M7c is behavior-bearing — synthetic one-voter JSON output with the
vote sentence embedded in prose:

    probe pristine: TALLY rows=1 agree=0 double=0 single=0 zero=1 dissent=0 voters=1 bound_voters=0
    probe mutant:   TALLY rows=1 agree=1 double=0 single=1 zero=0 dissent=0 voters=1 bound_voters=1

— yet its D2 run over the real r55 bytes is byte-identical to the frozen tally
(the committed outputs carry no vote sentence embedded in a JSON scalar outside
`vote_lines`), so only the selftest pins the overclaim guard.

## Restoration evidence

- The lane repo file was never opened for writing. Repo tool sha256 before the
  battery and after all runs:
  `8be1acdbb36cd68deba005e21a4a8679534ab5a5099a787aa9335d288dfa6bca` (unchanged, equals PIN).
- Every mutant was a scratch copy under
  `/fast/scratch/hyaku/mori-r56/Mo56MutBinder2/work/`; the battery recorded
  sha256 before and after each detector run (identical — the detectors are
  read-only over the tool) and deleted the mutant copy after its run. Final
  mutant hashes (before==after each run):
  M1 `0fc5a44036b8…`, M2 `a19d8a12d1f2…`, M3 `cf7f0967b641…`,
  M4 `b637cf7c253d…`, M5 `3c64b27f62fe…`, M6 `9637e8285969…`,
  M7 `890dadaa67c2…`, M7b `06a9124a0e2823e203986dfa87165942920c65653bf8280943a0ecaa36bcc0ca`,
  M7c `6c63758e9a1bf23f8ae8bf41f4033ca3c9faff4efc419d4078c0d1990584708f`,
  M8 `54b50923fb08…`.
- No git/jj mutation anywhere; no sysctl/cgroup/process writes; watchdog log
  untouched. Scratch tree removed after this report was written.

## Findings

- MED — Coverage gap (survivor M4): the dissent metric is pinned by neither
  frozen detector. The r55 ledger/results carry zero dissenting rows, so any
  monotone dissent scheme (per-hash, per-voter-pair, 2x, …) prints
  `dissent=0`, and the 16-case selftest has no dissenting tally row
  (`t_dissent_detected` exercises extraction only, not `tally` counting;
  `t_tally_mini` is all-agree). Concern: `tools/mori-vote-bind.py:180-182`
  (dissent increment) vs `.ufo/waves/round-56/count-c2.py` EXPECT_TALLY.
  Named limit of the frozen predicate; counters are not to be changed this
  round — route to round 57: pin one mixed-words tally case (expected
  `dissent=1`) in the tool selftest or a fixture.
- MED — Coverage gap (M7c): the overclaim guard (a JSON scalar binds only if
  the whole stripped scalar is the vote sentence) is pinned only by selftest
  cases; the frozen r55 tally cannot distinguish a guard-dropped binder
  because the committed outputs contain no prose-embedded vote sentences.
  Dropping the anchors also breaks the fenced-scalar guard — both JSON guards
  share the anchored `VOTE_RE` at `tools/mori-vote-bind.py:34,91`. Route to
  round 57 alongside the M4 item if tally-level pinning of guard semantics is
  wanted.
- LOW — Detector shape (M2, M5, M6 killed by selftest only): the r55 bytes
  contain no fenced text-channel votes, no differing duplicate (verb,hash)
  votes per voter, and no hash-length drift, so the TALLY pin alone admits
  fence/last-wins/hash-width mutants. The two-pin structure (selftest AND
  tally) is load-bearing; weakening either arm in a future round would lose
  these kills.
- LOW — Data-level (L1's call; not a fix this round): `--min N`
  (`tools/mori-vote-bind.py:418`) is accepted and echoed in the tally dict but
  never used in classification (dead knob), and the usage line at
  `tools/mori-vote-bind.py:45` documents `--disposition-cols N`, which the
  argparse setup does not implement (passing it exits 2 "unrecognized
  arguments"). Docstring/CLI drift only; both detectors are unaffected.
- LOW — Calibration note: a one-point `match`→`search` edit at
  `tools/mori-vote-bind.py:91` is an equivalent mutant (anchored pattern);
  guard mutations must drop the anchors, and must preserve capture-group
  numbering or the probe dies mechanically (M7b) instead of testing the guard
  (M7c).

All outputs above were produced by commands run under
`/fast/scratch/hyaku/mori-r56/Mo56MutBinder2` with `TMPDIR` pointed there; the
tree was removed after the report was written. Everything reported is
observed; nothing marked UNVERIFIED remains.
