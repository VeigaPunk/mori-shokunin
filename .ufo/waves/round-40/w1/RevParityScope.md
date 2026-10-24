# RevParityScope — round 40 wave 1 (reviewer)

Date: 2026-10-24. Target: `.ufo/waves/round-40/evidence/c10-parity.txt` and every
landed statement that cites it. No production edits. No `lsp` device exists in this
session's tool inventory, so the static side below is `diff`/`git show`/execution
evidence, not name resolution.

## Verdict

**The parity claim is true in the scope the evidence file records, and false if that
scope is dropped.**

- True as recorded: at rev `bb1f2457`, seed `20261024`, the round-39 counter bytes and
  `count-c8.py` print **byte-identical receipts** (stdout), exit 0 both. I reproduced
  this independently and byte-matched both parked receipts.
- Not claimed, and false: that the two **counters** are identical. They differ:
  `b92c65f2…` vs `4e4d50eb…`, 568 vs 563 lines, exactly five deleted lines.
- Not valid unqualified: the receipt is **seed-dependent**. `count-c8.py` (and
  `count-c7.py`) draws `DRAWN_STATES` with `random.Random(--seed)` and prints
  `drawn=<state>` plus the mutated got-row in the `drift_kill_v2` line, so the same
  counter prints different bytes at a seed that draws a different state. The claim
  must carry `(rev, seed)`.
- No measurement defect found. All five defects below are wording/evidence-pointer/
  replayability defects, not false receipts.

## Measured facts (exact commands and outputs)

### Instrument identity and the real diff

```
sha256sum .ufo/waves/round-40/count-c8.py .ufo/waves/round-40/fixtures/extracted/count-c7-r39.py
4e4d50eb1e96d947f0e9d2ab25a13b2b8c33963f216f3be43060a3348702f6da  count-c8.py
b92c65f224a6268a901aa6bc5ad66b499048eaca82b493356eb8e1f324ef0520  count-c7-r39.py

git -C <lane> show bb1f2457:.ufo/waves/round-39/count-c7.py | sha256sum
b92c65f224a6268a901aa6bc5ad66b499048eaca82b493356eb8e1f324ef0520  -
git -C <lane> show 265a955cc:.ufo/waves/round-39/count-c7.py | sha256sum
b92c65f224a6268a901aa6bc5ad66b499048eaca82b493356eb8e1f324ef0520  -
```

`diff --unified=0 fixtures/extracted/count-c7-r39.py count-c8.py` is two hunks,
**five deletions, zero insertions**:

```
@@ -98 +97,0 @@        -ROWSTATES_RE = re.compile(r"^selftest row_states (PASS|FAIL) (\(.*\))$")
@@ -441,4 +439,0 @@   -table = None
                     -    if arm and arm[0] == "FAIL":
                     -        parsed = parse_got_want(arm[1])
                     -        table = parsed[0] if parsed else None
```

`wc -l` → `568` vs `563`. `ROWSTATES_RE` has zero references after deletion; the
`table` block was in the `--arms selftest` branch and assigned a name never read
(`parse_got_want` itself returns `None` on malformed input — no removed exit-2 path).
The 16-line SimpCounters total is `1+4` in count-c7 **plus** `5+6` in conform
(`.ufo/waves/round-39/w1/SimpCounters.md`, D1–D4). So "count-c8 = count-c7 minus the
sixteen dead lines" is wrong; the counter pair differs by **five**.

### Independent parity reproduction

Both counters were run from byte copies staged in `/tmp/mori-parity-review/{c7,c8}/`
with a real `fixtures/` neighbor (witness files copied from
`.ufo/waves/round-40/fixtures/`), through a loader that overrode only
`SCRATCH_ROOT` to `/tmp` (so the lane's `.ufo/waves/round-39/scratch` was not
written) and called `main([rev, "--repo", <lane>, "--seed", seed])`. The in-place
`count-c8.py` produced the same bytes as the staged c8 copy at seed `20261024`
(`c03e05ce…`), so staging did not alter the receipt.

`python3 driver.py <counter> <scratch> <rev> <seed> <lane>`, results:

| rev | seed | drawn state | c7 exit | c8 exit | c7 == c8 stdout | stdout sha256 |
|---|---|---|---|---|---|---|
| bb1f2457 | 20261024 | fresh | 0 | 0 | yes | `c03e05ce2bf08664148c0d9d15be4d93c986d4ee77448cbb129c14a435861eff` |
| bb1f2457 | 1 | fresh | 0 | 0 | yes | same `c03e05ce…` (same drawn state) |
| bb1f2457 | 2 | excerpt | 0 | 0 | yes | `cab903572ff7567637168aa3e6cab1c31bdee4524c0d3f474e1e66dacbee487e` |
| bb1f2457 | 5 | unavailable | 0 | 0 | yes | `c5a20ffea60b3206dc4befc5f888925059fcb0ece8f8f1bcdb00fe9a055136b4` |
| bb1f2457 | 0 | no-copy | 0 | 0 | yes | `80a700e74439761253f09fb015f094a9162468427a98aff3e07ee150c6f25882` |
| 265a955 | 20261024 | fresh | 0 | 0 | yes | `c03e05ce…` |
| 265a955 | 2 | excerpt | 0 | 0 | yes | `cab90357…` |

stderr was empty in every run. Across seeds the receipts differ in exactly **one
line**, `check drift_kill_v2`, whose `drawn=` token and mutated `got` row carry the
drawn state (e.g. seed 2 changes `('S103','fresh')` to `('S103','excerpt')`).
Seed 20261024 and seed 1 draw `fresh` and are byte-identical, which is the concrete
demonstration that "byte-identical" is a per-(rev,seed) property.

The parked raw receipts were matched byte-for-byte, not just by digest:

```
sha256sum evidence/.parity-c7.txt evidence/.parity-c8.txt evidence/c10-parity.txt
c03e05ce2bf08664148c0d9d15be4d93c986d4ee77448cbb129c14a435861eff  .parity-c7.txt
c03e05ce2bf08664148c0d9d15be4d93c986d4ee77448cbb129c14a435861eff  .parity-c8.txt
aa2b8a6b23f049061bbde3fd7510d95b93a668da4c86353c1cf51c35f9820e9d  c10-parity.txt

cmp /tmp/repro-c7.txt evidence/.parity-c7.txt   → equal
cmp /tmp/repro-c8.txt evidence/.parity-c8.txt   → equal
cmp /tmp/repro-c7.txt /tmp/repro-c8.txt         → equal
```

The round-39 instrument path is also runnable and yields the same bytes:
`driver.py <lane>/.ufo/waves/round-39/count-c7.py … bb1f2457 20261024` → exit 0,
sha `c03e05ce…`, equal to the parked receipt. Inputs were comparable: the r39 and r40
witness files hash identically (`witness-token-entry ce4dac65…`, `dangling-row
bc62b0b3…`, `summary-only-live 8ac9e82b…`, `comment-anchors fc95dc69…`).

### The recorded command is not replayable as written

```
python3 fixtures/extracted/count-c7-r39.py bb1f2457… --seed 20261024 --repo <lane>
exit=2
stderr: counter setup error: [Errno 2] No such file or directory:
        '.../fixtures/extracted/fixtures/witness-token-entry.md'
```

The counter resolves witnesses relative to `__file__`; `fixtures/extracted/` has no
`fixtures/` neighbor, so the extracted copy cannot print the receipt that
`c10-parity.txt` records. `c7_exit=0` was produced by the r39 working-tree instrument
path or by undocumented staging. `ExeParity.md` hit the same failure and switched to
`.ufo/waves/round-39/count-c7.py`; the parity summary should say so.

### Counter `--arms selftest` (the branch that held D2)

```
driver_arms.py c7/count.py … --tool <lane>/tools/mori-source-drift.py --arms selftest
stdout: tool selftest: fail exit=0 row_states=None
        C7=unmet                                     (exit 1)
(same stdout for count-c8; byte-identical)
```

Both counters agree (parity holds there too), but the arm is **unmet**: the tool prints
`selftest row_states           PASS` (padded), and the branch parses it with
`parse_rowstates`' single-space regex `^selftest row_states (PASS|FAIL)…`, which
returns `None`; the main path's `selftest_arms` uses `\s+` and matches. This is
pre-existing in both counters, not introduced by the deletions.

## Findings

### F1 (medium, wording) — `contract.md:70-72` states byte-identity without rev/seed

> "…printed receipts byte-identical, proven in `evidence/c10-parity.txt`"

The receipts are seed-dependent (table above). Unqualified, the clause is false for the
same counter at another seed (seed 2 vs 20261024: one line different). It also
contradicts the contract's own admission rule at `contract.md:157` ("no universal
clauses"). The adjacent `c10-parity.txt` does name `seed 20261024`, so the measurement
is honest; the prose is not scoped to it.

**Fix (no re-freeze; this is not the frozen predicate):** write "receipts byte-identical
at `(rev, seed)`; verified at `bb1f2457`, seed `20261024`" in the report/scorecard, or
use the stronger measured form: "byte-identical per (rev,seed), re-derived at
`bb1f2457` and `265a955` for seeds 20261024/1 (`fresh`), 2 (`excerpt`), 5
(`unavailable`), 0 (`no-copy`)".

### F2 (medium, factual wording) — "the sixteen dead lines" is attributed to the wrong file

`contract.md:70-71` says count-c8 is "round-39 `count-c7.py` bytes minus the sixteen
dead lines of SimpCounters D1–D4". Measured: count-c7 loses **5** lines (D1 `1` +
D2 `4`), zero insertions; the other 11 (D3 `5` + D4 `6`) are in conform. Any report
sentence of the form "the counters differ by the 16 dead lines" or "count-c8 =
count-c7 minus 16 lines" is false. Correct form: "count-c8 = count-c7 − D1 − D2
(5 lines); the 16-line deletion spans count-c7 and conform."

### F3 (medium, evidence pointer) — `c10-parity.txt` alone does not prove byte-identity

The cited 306-byte file records the rev, seed, count-c7 sha, both exits, and the
assertion `PARITY: receipts byte-identical`; it records **no digest or byte count of
either receipt** and does not name the raw receipts. The receipts are parked as hidden
dotfiles `evidence/.parity-c{7,8}.txt` (sha `c03e05ce…`, identical), which
`c10-parity.txt` does not mention and which the contract's "P-C10/P-C11 evidence paths"
list (`contract.md:151-153`: `freeze-r40`, `census-*`, `c10-red-*`, `c10-after*`,
`c11-*`) does not include. So "proven in `evidence/c10-parity.txt`" overstates the
visible file; the proof is in files the citation does not name. My re-run confirms the
identity, so this is a pointer/recording defect, not a false result.

**Fix:** have the report cite `.parity-c7.txt` / `.parity-c8.txt` with sha `c03e05ce…`,
or add both digests plus the raw-receipt paths to `c10-parity.txt`; add the parity files
(including the dotfiles) to the evidence-path list / erratum.

### F4 (low, replayability) — the receipt's "command:" line names no runnable path

`command: parity count-c7-r39 (disk == bb1f2457 bytes) vs count-c8 on rev bb1f2457,
seed 20261024` reads as the extracted copy, but the extracted copy exits 2 (missing
`fixtures/` neighbor; measured above). A reviewer replaying literally gets a spurious
failure. Name the actual instrument path (`.ufo/waves/round-39/count-c7.py`, sha
`b92c65f2…` at both `bb1f2457` and `265a955`) or the staged layout with a `fixtures/`
neighbor; the identical r39/r40 witness hashes mean either run compares equal inputs.

### F5 (low, ambiguous clause) — "behavior byte-identical including both selftests"

`contract.md:42-44`. `c10-parity.txt` covers only the main-path receipt. The counter's
`--arms selftest` path — precisely the branch where D2's four dead lines lived — is not
receipted, and my run shows it prints `C7=unmet` (identically for both counters, due to
the single-space `parse_rowstates` vs padded tool output above). If "both selftests"
means the conform/gate selftests, the parity file is the wrong evidence pointer and the
counter has no `--selftest`; if it means the counter's arms path, "byte-identical" is
true but any implication of "passes" is false. Drop the clause or name the two
selftests and their own receipts (`c10-after-selftest.txt`, `c11-after-selftest.txt`).

## Residual risk and verification gaps

- **Evidence not at the scored tip.** The whole evidence directory is absent from the
  265a955 tree: `git cat-file -e 265a955:.ufo/waves/round-40/evidence` → exit 128
  (`exists on disk, but not in '265a955…'`); `git ls-tree 265a955 -- .ufo/waves/round-40/`
  lists only `conform.py`, `contract.md`, `count-c8.py`, `fixtures`. `c10-parity.txt` and
  the two dotfiles are staged in the lane index (`git ls-files .ufo/waves/round-40/evidence/`
  lists all three) but are not in the scored tree, so the claim's proof lives only in the
  pending evidence commit. If that commit drops the dotfiles (easy to miss, and unlisted
  in the contract), the cited evidence becomes unreachable from the scored tree. Nothing
  in my evidence changes that; the L1 must ensure the pending commit contains all three
  files.
- The contract is frozen; F1/F2/F5 are prose corrections for the report/scorecard (and
  an erratum if the L1 keeps one). They do not require touching the predicate or
  instruments.
- Seed coverage: I sampled five seeds covering all four `DRAWN_STATES` values, not
  "all seeds"; the general statement belongs to the code path (only `drawn=` and its
  got-row can vary), not to a finite receipt set. The single-seed recorded evidence is
  sufficient for the scoped claim and insufficient for an unqualified one.
- I did not run the r39 counter file in place (scratch redirected to `/tmp`); its
  loaded run is byte-identical to the parked receipt, so the in-place scratch side
  effect would not change the answer.
- The `--arms selftest` parser mismatch is pre-existing and outside this seat's claim;
  it is reported only because F5's wording touches that path. Not fixed here.

## Wording guidance for the report / SCORECARD rows

Safe:

- "`count-c8.py` is `count-c7.py` with D1–D2 removed (5 lines; `diff --unified=0`
  shows nothing else, 568 → 563); the full 16-line SimpCounters deletion spans
  count-c7 and conform."
- "At `bb1f2457`, seed `20261024`, count-c7 and count-c8 print byte-identical
  receipts, exit 0 both (`c10-parity.txt`; raw receipts `.parity-c7.txt`/`.parity-c8.txt`,
  sha256 `c03e05ce…`). I independently re-confirmed the pair at seeds 1/2/5/0 (all four
  drawn states) and at `265a955`."
- "Receipts are byte-identical per (rev, seed) — independently re-derived at
  `bb1f2457` and `265a955` across seeds 0/1/2/5/20261024 (all four drawn states)."

Must not appear:

- "the counters are identical" / "byte-identical counters" (shas and line counts differ).
- "receipts byte-identical" with no rev and seed.
- "count-c8 is count-c7 minus sixteen lines".
- "proven by `c10-parity.txt`" without the raw-receipt paths or digests.
- "the counter selftest passes" / "both selftests pass" for the counter's
  `--arms selftest` path.

## Bounds / tooling

No persistent lane or fleet writes except this report; no git/jj mutation (only
`git show`, `git ls-tree`, `git ls-files`, `git status` reads). Every parity run
redirected `SCRATCH_ROOT` to `/tmp/mori-parity-review/`; the one direct
extracted-path replay (recorded under F4) used the counter's own
`mkdtemp`/`rmtree` in `.ufo/waves/round-39/scratch`, leaving no directory behind
(`ls .ufo/waves/round-39/scratch/ | wc -l` → `0`; `git status --porcelain
--untracked-files=all` shows no residue from this seat). No tool installs or
upgrades were needed.
