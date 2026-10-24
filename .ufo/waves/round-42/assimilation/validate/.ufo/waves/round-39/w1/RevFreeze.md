# RevFreeze — round-39 freeze pins and round-38 instrument immutability

Seat: `mori-r39.RevFreeze`. Scored tip `13bfba23b7ca063c76d3504a2ff6eb7b6a294932`; entering tip
`13f3db7e5c7163e7ef300259ff597a42a79f81f1`. All pinned bytes read from git objects, never from the
mutable worktree alone.

## Verdict

- **Freeze (`evidence/freeze-r39.txt`): PASS.** 13/13 sha256 entries match the bytes at `13bfba23`,
  and the same hashes hold at the freeze-landing commit `97b826a`, at the before-receipt commit
  `87ec3d9`, at the later HEADs, and on disk. Zero drift. Nothing in the pinned set was edited after
  the freeze commit.
- **Round-38 instruments: PASS.** The four named files are byte-identical between `13f3db7e` and
  `13bfba23`; the whole 134-file `.ufo/waves/round-38/` tree is byte-identical on disk to its
  `13f3db7e` bytes, and `git diff 13f3db7e..13bfba23 -- .ufo/waves/round-38/` is empty.
- Two frozen-contract declarations disagree with the frozen instruments (F1, F2) and one frozen
  sentence cites a path that exists nowhere (F3). These are claim-text defects, not hash drift.

## Hash comparison table (recomputed `git show 13bfba23:<path> | sha256sum`)

| # | path | expected (freeze) | got | verdict |
|---|---|---|---|---|
| 1 | `.ufo/waves/round-39/contract.md` | `fc36841bff00e46bf3d2ba662c9e4e13e36577da1d1f2fec41d0bea91f8ebcd3` | same | OK |
| 2 | `.ufo/waves/round-39/count-c7.py` | `b92c65f224a6268a901aa6bc5ad66b499048eaca82b493356eb8e1f324ef0520` | same | OK |
| 3 | `.ufo/waves/round-39/conform.py` | `fe0be179aba9df7150f0b6cdb50a5f9bbdb411efb1263b46ffa6b21d46ef7987` | same | OK |
| 4 | `.ufo/waves/round-39/fixtures/run-c7-reds.py` | `061a8cf4f02e5095b0805da1a6cf6ab594bdcb9b99205620937277f4afa37002` | same | OK |
| 5 | `.ufo/waves/round-39/fixtures/run-c8-receipts.py` | `5ecaef10967ae7a698d021c7b8cd7a3e327ce41e279f1920575837ed0cecc65e` | same | OK |
| 6 | `.ufo/waves/round-39/fixtures/run-c9-dags.py` | `d75d774092aac06da9690310782a4e95c83975c7e59282264dc71d04791e59b8` | same | OK |
| 7 | `.ufo/waves/round-39/fixtures/make-m19-bypass.py` | `79a2ee9b089c50932e231ec881ee78fe58c2cb81c38d715579d6cf65168b49c5` | same | OK |
| 8 | `.ufo/waves/round-39/fixtures/witness-comment-anchors.md` | `fc95dc69153f47c2f934a0e9be069764a9da7b606dc0274ffd0f5672f3bd4623` | same | OK |
| 9 | `.ufo/waves/round-39/fixtures/witness-token-entry.md` | `ce4dac65d1dd0ee55f71de1ee5937d474fdfecf32ea599ea3a204395178194f2` | same | OK |
| 10 | `.ufo/waves/round-39/fixtures/witness-dangling-row.md` | `bc62b0b3db38fbf6086eb5dbdff50a90e5901046ab012abb23e89d9c50357ff2` | same | OK |
| 11 | `.ufo/waves/round-39/fixtures/witness-summary-only-live.txt` | `8ac9e82bae369a2e41f4a4377016c3e82d58c8c6de484722f1d85b0bbf7cb4af` | same | OK |
| 12 | `.ufo/waves/round-39/fixtures/hang-after-flush.py` | `647410536bcc6b9ead5456af96056617b78b7945aaacc2c5d3635b1b017a87ca` | same | OK |
| 13 | `tools/mori-sources-appendonly.py` | `62cd4132dbe141538371f79723c3caff66670fab9076494cd9cf65efccfc01e7` | same | OK |

Every row was checked at all four revisions in the command
`for r in 97b826a 87ec3d9 13bfba23 HEAD; do git show $r:<path> | sha256sum; done` — all 13 × 4
equal the frozen value. The manifest file itself is identical at `13bfba23`, at HEAD, and on disk:
`185555b25c81c6d2e53bc317b4a3b504cac0f09732034352a38d27f2bff873c3`.

## Round-38 instrument comparison (`git show` both sides, sha256)

| file | @ `13f3db7e` | @ `13bfba23` | verdict |
|---|---|---|---|
| `.ufo/waves/round-38/count-c4.py` | `8332341c3901ef09e76bbd7f31e8c8e68b4e4ecc5d3002f2d20201c9e7093ba1` | same | SAME |
| `.ufo/waves/round-38/conform.py` | `580a0bf15a815b5a26aed908f67a3d74f29d714b19175cee6057fb694aaeb01e` | same | SAME |
| `.ufo/waves/round-38/count-c1.py` | `5aa51556946a3e5293ba069a12b9e816694ea406bd11f5cb22da5e5ba7c22ea3` | same | SAME |
| `.ufo/waves/round-38/contract.md` | `8cfeed27f0ce715089f18ff5cb20d18d211f2e31ed0f0aecf09105d79fb4eac9` | same | SAME |

These equal the `freeze-r38-v3.txt` pins, so round 38's own v3 pins are still self-consistent at the
entering tip. Full-tree check: 134 tracked files under `.ufo/waves/round-38/` hashed on disk against
`git show 13f3db7e:<path>` — 134 OK, 0 DRIFT; `git diff --stat 13f3db7e 13bfba23 -- .ufo/waves/round-38/`
empty. `git status --porcelain` over round-38/round-39/pinned gate shows only the untracked live
scratch dir `.ufo/waves/round-39/scratch/`, which contains no pinned path.

Independent spot-check that the pinned gate bytes are the ones the receipts describe (copies in
`scratch/RevFreeze/`):
- `git show 13bfba23:tools/mori-sources-appendonly.py` → `--selftest` → `MORI_SOURCES_APPENDONLY_SELFTEST pass=12 fail=0`, exit 0.
- `git show 13f3db7e:tools/mori-sources-appendonly.py` → `--selftest` → `pass=9 fail=0`, exit 0.
- v1 and v2 gate bytes on the lane at `HEAD --round-base f10a320d`: per-id/summary/timing bodies byte-identical (`diff` empty), matching the C3 lane-parity claim.
- v2 bytes at tip vs `.ufo/waves/round-38/evidence/gate-after.txt`: identical apart from the receipt's own `command:`/`P-C6`/`EXIT` lines.
- v2 bytes at `e37dcc6` vs `.ufo/waves/round-38/evidence/gate-after-e37dcc6.txt`: identical body; `stale_supersede=[S069]`, 17 as-of ids — the predicate's "S069 stale at e37dcc6" holds.

## Findings

### F1 — HIGH (claim text): the frozen C3 after-declaration names `S226` in `superseded_as_of`, which the frozen gate cannot emit

`contract.md:147-148` declares, at the landed tip,
`supersede_timing superseded_as_of=[18 ids + S226 once S228 lands] stale_supersede=[]`.

Frozen bytes contradict that:

- `tools/mori-sources-appendonly.py:334-337` builds `ids` only from tip rows absent at first sighting
  **or whose immutable cells differ from their first-sighting commit**; `:343` sets
  `superseded = ids ∩ sup_map`; `:349-359` iterate `superseded` for as-of/stale. An id that is
  superseded but never edited is invisible to `supersede_timing` by construction.
- `S226`'s row text is byte-identical at every walk commit that carries it (first sighting `daa1d4d`,
  then `f920eaf`; one distinct row string across the full-history walk, anchor still `:657-658`).
  The correction rides the separate `S228` row (`contract.md` itself says the anchor cell is
  immutable), so `S226` never enters `ids`.
- Observed with the pinned bytes at the scored tip, `--round-base f10a320d`: 18 as-of ids
  (`S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193`),
  `stale_supersede=[]`, and `S226` appears only as S069's superseder value
  (`changed S069 superseded_by=S226`). No `changed S226` line exists.
- `evidence/c9-after-lane.txt` records the same 18-id line; no receipt anywhere shows `S226` as-of.

So the sentence's bracketed expansion is unobservable under the frozen contract's own append-only
rule. Predicate **P-C9 itself is met** ("no id is stale at the round-39 tip"); the defect is the
declared-after gloss. The wave brief's C3 bullet repeats the same gloss, and the report must not.
Independent convergence: `w1/RevCensus.md` (landed during this review, commit `0662ddb`) files the
same overclaim as MEDIUM. Because the contract is pinned, this needs a recorded correction in the
LOG/lesson, not an edit.

### F2 — LOW (documentation): contract declares gate selftest `pass=11`, frozen gate prints `pass=12`

`contract.md:146` says `MORI_SOURCES_APPENDONLY_SELFTEST pass=11 fail=0`. The pinned gate at
`13bfba23` prints `pass=12 fail=0` (reproduced above and in `evidence/gate-selftest-after.txt:1`).
The brief's C3 bullet and the receipt agree on 12; only the frozen contract text is off by one. The
contract is pinned, so this is a frozen-artifact blemish to record, not a hash drift.

### F3 — MEDIUM (reproducibility): `fixtures/make-ancestry-dags.py`, cited as the C3 red-receipt builder, does not exist

`contract.md:139` says the before control was "measured on committed fixture DAGs built by
`fixtures/make-ancestry-dags.py`". That path exists in no commit of the lane
(`git log --all -- .ufo/waves/round-39/fixtures/make-ancestry-dags.py` empty; not in
`git ls-tree -r 13bfba23 -- .ufo/waves/round-39/fixtures/`; not on disk). The actual DAGs are built
at runtime from gate-embedded bodies (`_selftest_dag_cases()` / `_make_dag_repo()`) and driven by
the pinned `fixtures/run-c9-dags.py`. Reproducibility is not lost — gate and runner are both pinned —
but the frozen sentence's provenance is false as written, and "committed fixture DAGs" overstates
runtime-built repos. Cite `run-c9-dags.py` + the gate's DAG cases instead.

### F4 — LOW (receipt precision): `c9-after-lane.txt` has a prose `command:` line and unlabeled counts

- Line 1 is prose ("gate v2 bytes at f920eaf7 vs the round-38 gate receipts, --round-base f10a320d"),
  not a runnable command, unlike every other receipt.
- "v2 walk commits (full-history): 53 / v1 walk commits (default simplification): 52": the
  full-history walk over `corpus/SOURCES.md` is **54** records (53 non-merge); default simplification
  is **53** (52 non-merge). The receipt's numbers are the non-merge counts, unlabeled.
- The qualitative claim reproduces: `6531ac60` is present once under `--full-history` and zero times
  under default simplification, and it is an ancestor of HEAD.
- The parity claims reproduce exactly (see spot-checks above), so no verdict turns on this.

### F5 — LOW (provenance): the three C9 after receipts lack the runner's command line

`run-c9-dags.py:45-46` always writes a leading `command:` line; the red receipt
`c9-red-a.txt` has it, but `c9-after-fixture-a.txt` / `-c.txt` / `-d.txt` do not — they are
per-fixture excerpts of one run. Regenerating with the pinned runner and pinned gate at the tip
reproduces the three blocks byte-for-byte apart from a trailing blank line, so content fidelity is
intact; only the invocation record is missing and must be reconstructed from `c9-red-a.txt` +
the pinned runner.

## Residual risk

- Lane HEAD advanced during this review (`5561819` → `0662ddb` → `ebc61f4`, adding w1 reports,
  dispatch log, lesson). The scored tip `13bfba23` is still an ancestor and none of the pinned paths
  appear in `git diff --name-only 5561819..HEAD`; all pinned reads were taken from git objects.
- `c9-after-lane.txt`'s walk-count lines came from an uncommitted harness; I reproduced its parity
  diffs and its `6531ac60` claim from the pinned gate, not its numeric labels (F4).
- P-C7/P-C8 counter behavior and the M18/M19 kill demos are other seats' scope; I only verified that
  their bytes are the frozen ones and that the gate selftest counts are the frozen gate's.
- LSP: no language server is available in this seat's toolset, so code locations were established by
  reading `tools/mori-sources-appendonly.py` and by executing the pinned instrument; the decisive
  evidence for F1 is runtime output plus the single-distinct-row-text check, not grep.

## Tooling

No installs or upgrades. Scratch only under `.ufo/waves/round-39/scratch/RevFreeze/` (gate copies,
regen receipts, diff bodies). Lane files were not modified; no git/jj mutating command was run.
