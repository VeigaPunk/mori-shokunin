# Round 93 — frozen contract (mori, L1 MoriR93, attempt 1)

Entering revision `7b3fe9d540c98b8b0390a0f9bbe78de4341092a5` (lane `master`, local = remote at
round start; `jj-lane.sh state` clean, one untracked orchestrator marker `w1.ready.dispatched`
under round-92 which is not lane work and is not committed). This contract, the two counters,
the controls script and the receipts under `evidence/` are committed in one `jj-lane.sh commit`
**before** any wave dispatch. Axes: **calibration** (C1, score 5, tied lowest non-retired with
freshness and depth) and **operability** (C2, score 7). Two claims, both on distinct axes.
No score is moved by this contract; each claim is admitted only if its frozen predicate is met
at the landing revision and no axis is harmed.

## Premises (QUALITY 196 — grepped and committed before the freeze)

- P1 (C1): the round-92 lesson's sentence "Each `verified-at` names the admission commit of its
  file" is at `corpus/lessons/round-92.md:51-52` (a wrapped sentence). Evaluated at the entering
  revision by `count-c1.py`: `adm_ok=7 adm_fail=12` over the 19-file trio landing; the 12 failing
  files are listed with their values in `evidence/measure-c1-entering.txt`.
- P2 (C2): `git grep -n vgpnk 7b3fe9d5 -- tools` → 12 lines in three files; the counter's byte
  count of `vgpnk` over `tools/` is 18; `(?<![>\w])/home/[a-z_][a-z0-9_-]*` matches 18 (the
  fourth file `tools/mori-round17-jj-regressions.py` has `<case>/home/gitconfig`-style
  case-relative paths, not host paths, and is excluded by the `>` lookbehind).
  Measured in `evidence/measure-c2-entering.txt`.
- P3 (rule 2, found this round): the digest-gate debt (31 prefix-only rows, S125 unpinned) cannot
  be closed honestly this round. Completing a recorded digest in place edits the anchor cell,
  which CORPUS.md rule 2 forbids (only `status`, `recheck`, `used-by` change in place); the
  supersession path (`supersedes S<id>`) is honoured only for `mismatch` targets, and
  `tools/mori-source-digest.py --selftest` case "prefix-only row is not superseded" pins that
  by design (QUALITY 193/195). The digest-gate claim is therefore **not** taken this round and is
  routed (see Mistakes M1 in the lesson). No registry rows are edited in place.
- P4 (freshness, considered and dropped): `recheck` cadences are all measured against `opened`
  dates from 2026-10; `grep` over `recheck-col` shows 0 cadence rows due at 2026-11-05 (98
  `Nd` rows, earliest due 2027-01). A freshness claim on recheck would be met by doing nothing,
  so it is not declared.

## Claims

### C1 — calibration: the round-92 lesson's self-description is true of the repo it describes

- **Predicate P-C1 (one sentence, same in `count-c1.py`, the receipt and this line):** at revision
  R `python3 -I .ufo/waves/round-93/count-c1.py R --repo <clone>` prints
  `C1=met trio=98 claim_r92_true=1 files=19 adm_ok=19 adm_fail=0 patched12=12 seven_same=7
  census=ok rev=<12>` and exits 0, where: `trio` counts knowledge entries with the three
  provenance keys in their first 12 lines (>= 98); each of the 19 round-92 trio files' `verified-at:`
  line at R contains the file's admission commit (`git log --diff-filter=A --format=%h
  7b3fe9d5 -- <file> | tail -1`, first 7 characters); each of the 12 entering-mismatch files
  changes exactly one line between the entering revision and R, which is its `verified-at:` line;
  each of the other seven is byte-identical; `sources-census.sh validate --file` exits 0.
  Otherwise `C1=unmet ...` with `checks_failed=`; exit 1.
- **Before** (measured at `7b3fe9d5`; receipt `evidence/measure-c1-entering.txt`): `C1=unmet
  trio=98 claim_r92_true=0 adm_ok=7 adm_fail=12 patched12=0`. Counting command:
  `python3 -I .ufo/waves/round-93/count-c1.py 7b3fe9d5 --repo <lane> --report`.
- **Repair shape (bounded):** for each of the 12 files, replace only the `verified-at:` value by
  `verified-at: <admission-short-hash> (<the original value, unchanged>)`. No other line changes.
  The original date/round text is kept, so the information is not lost and the value gains the
  admission commit the round-92 lesson said it had.
- **Do-nothing and text-only controls** (`evidence/controls-r93.txt`): at the entering revision
  `C1=unmet adm_fail=12`; with only the lesson sentence reworded (a fixture commit) the counter
  still reads `C1=unmet adm_fail=12` — the claim measures the data, not the sentence.
- **Deletion control:** `verified-at` stripped from the 12 files → `C1=unmet trio=86 adm_fail=12`.
- **Forgery control:** correct admission hashes written into all 12 `verified-at` lines plus one
  body edit in one file → `C1=unmet patched12=11`; the no-body-change rule is enforced.
- **Sourced claim (frontier step, CORPUS.md rule 1):** the admission-commit derivation rests on
  `git log --diff-filter=A` semantics; the source row `S622` (git-log documentation, opened this
  round) is cited by the lesson Gate and the SCORECARD row.
- **Named limit:** the counter checks presence of the admission short hash inside `verified-at:`,
  not that the hash is the commit that introduced the file's *current content*; a later rewrite
  would be invisible to it (accepted, named).

### C2 — operability: no tool under `tools/` hardcodes a host home path (QUALITY 197)

- **Predicate P-C2 (one sentence, same in `count-c2.py`, the receipt and this line):** at revision
  R `python3 -I .ufo/waves/round-93/count-c2.py R --repo <clone>` prints
  `C2=met home_literals=0 vgpnk_refs=0 tools=3 selftests=3/3 census=ok rev=<12>` and exits 0,
  where `home_literals` counts `(?<![>\w])/home/[a-z_][a-z0-9_-]*(?![a-zA-Z0-9_.-])` over every
  file under `tools/` at R, `vgpnk_refs` counts the byte `vgpnk` there, `tools=3` is the presence
  of the three named tools, `selftests=3/3` is each tool's declared self-test exiting 0 in the
  extracted tree, and `census=ok` is the registry validator at R. Otherwise `C2=unmet ...`; exit 1.
- **Before** (measured at `7b3fe9d5`; receipt `evidence/measure-c2-entering.txt`): `C2=unmet
  home_literals=18 vgpnk_refs=18 tools=3 selftests=3/3 census=ok`.
- **Repair shape (bounded):** each functional literal becomes a value derived at run time from
  `SHOKUNIN_ROOT` when set, else `$HOME/Projects/shokunin` (python: `os.path.expanduser`; bash:
  `${SHOKUNIN_ROOT:-$HOME/Projects/shokunin}`). Each prose or comment mention becomes a
  placeholder (`<fleet-root>`, `<lane-root>`). The rendered seat-context text in
  `mori-round17-context-check.py` must stay byte-identical on this host (the derived value equals
  the old literal here). Equivalence receipt: each tool's `--selftest` stdout and `--help`
  stdout identical between `7b3fe9d5` and R, committed as `evidence/equivalence-c2.txt`.
- **Do-nothing and deletion controls** (`evidence/controls-r93.txt`): entering `C2=unmet
  home_literals=18`; three tools deleted `C2=unmet tools=0 selftests=0/3`.
- **Rename control:** `vgpnk` replaced by `someone` in the three tools → `C2=unmet
  home_literals=18 vgpnk_refs=0`. The byte-count-only predicate would have accepted it; the
  regex clause is what refuses it.
- **Named limit:** a host path written as a relative `../../<user>` form or assembled at run
  time by concatenation is not caught; the counter reads static bytes only.

## Ordering

1. This contract, `count-c1.py`, `count-c2.py`, `controls-r93.sh`, `evidence/`, and the wave
   spec `w1-spec.json` are committed together **before** the wave is dispatched.
2. The wave runs; seats return patches and findings into `.ufo/waves/round-93/w1/`. Only the L1
   edits the lane tree; seats never commit.
3. The L1 integrates the patches, re-runs every counting command at the landing revision, and
   commits the landing with after-receipts under `evidence/after-r93.txt`.
4. The report cites the landed hash, after `git ls-remote` shows it.

## Kill rule

A claim whose predicate is unmet at integration is reported unmet; it is not narrowed after
landing. A repair patch that breaks a no-harm conjunct (census exit, selftest, the seven
unchanged files, a byte change in a seat-context render) is rejected and that claim reports
unmet. A trade anywhere is not an improvement.

## Frontier (declared, not claimed)

Digest-gate debt (31 prefix-only rows, S125 unpinned), the nonce guard for the round-90 gate
(QUALITY 191), and the round-87 arm-pin supersession record stay carried, as recorded in the
round-92 lesson; this round does not take them (P3).
