NEGATIVE CONTROLS PRINTED C1=met: one-five-word-span, one-uncited-copy-span; the frozen counter violates P-C1.

# CtlJudgeShapes — judge receipt and dispatch mutation probe

## Result

- Positive synthetic control: `C1=met`, exit 0, before any mutation.
- Negative controls: 10 killed, 2 survived, 0 inconclusive.
- Whitespace-only R-J rewrapping: `C1=met`, exit 0, as required.
- Every one of the 13 controls was measured as a pristine → mutated → restored triple. All 13 pristine and all 13 restored measurements printed `C1=met`, exit 0.
- Axes: predicate discrimination; whitespace parity; exact-byte restoration; sandbox containment.

## Counter defect observed

The five-word-span mutant changes only row 1's supported span to `The Linux kernel is the`. The uncited-copy-span mutant changes only row 1's supported span to `All contributions to the Linux Kernel are subject to this COPYING file.`; row 1 cites only S180, while that replacement is located in S181 and not S180. Both receipts still name all 12 rows `supported`. Both measurements print:

```text
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=11 supported_new=11 spans_bad=[1] unsupported=[]
skill_rows=4
C1=met
```

At `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py:275-285`, a bad supported-row span is added to `spans_bad` and excluded from the supported count, but nonempty `spans_bad` is not itself a failure. Eleven other rows exceed the ten-row support threshold, so the invalid supported row is tolerated. P-C1 instead requires every supported row to carry a located six-or-more-word span in a new source that row cites. These are surviving mutants and a coverage finding, not permission to weaken that contract. The frozen counter and contract were not changed.

## Sandbox and fixture

- Sandbox clone: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo`.
- Frozen clone start: `27969134d51ea15982db4f36c77e2decd2a22b07`.
- Entering-tip URL novelty reference: `7d382043016e8854e3be2ee523a095b409c3d8a1`.
- Positive commit: `f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc`.
- Positive Git tree: `aeb3187dd02a9e7cbbb24e1c6689fd38b63c7a7b`.
- This is a deliberately synthetic shape-valid control, not actual lane data or a real judge decision. No judge runtime was invoked.
- The entry has 12 distinct rows, each citing one new source, with two rows per S180–S185; six unique upstream URLs, six distinct SHA-256 values, six admit Gate rows with located quotes, committed source copies, six mined source rows, four qualifying Round33 skill lines, a rule-bearing dispatch and receipt, and an entry-matching judged SHA-256.
- Each selected URL was absent from every entering-tip source-registry line; builder assertions establish that condition. Every detector measurement independently fetched all six URLs and reported `fetch_ok=6/6`.
- Each mutant is an immutable commit derived directly from the positive tree, changing only one target blob or deleting the dispatch. These immutable revisions allow concurrent read-only measurements without shared worktree mutations. The index was restored after creating each mutant; each separately committed restoration has the entire original positive tree. The worktree stayed byte-identical to the positive fixture throughout.
- All Git writes were confined to this clone with GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE unset. No fleet/lane Git writes were used, and the only lane file written is this assigned report.

### Real tag-pinned sources

| ID | URL | Committed copy and locator | SHA-256 | Span words |
|---|---|---|---|---:|
| S180 | https://raw.githubusercontent.com/torvalds/linux/v7.2/README | `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo/corpus/evidence/sources-r33/S180.src:4` | `2844b0b2cafe22741724c4fdda79b1259de48743f12ad40ce408adb1ef00ceda` | 11 |
| S181 | https://raw.githubusercontent.com/torvalds/linux/v7.2/COPYING | `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo/corpus/evidence/sources-r33/S181.src:20` | `fb5a425bd3b3cd6071a3a9aff9909a859e7c1158d54d32e07658398cd67eb6a0` | 12 |
| S182 | https://raw.githubusercontent.com/torvalds/linux/v7.2/.clang-format | `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo/corpus/evidence/sources-r33/S182.src:3` | `127fc850fd74996410163972eb3e2fb9af428ada97d2403b149f8d16c2d674f5` | 8 |
| S183 | https://raw.githubusercontent.com/torvalds/linux/v7.2/.clippy.toml | `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo/corpus/evidence/sources-r33/S183.src:8` | `84f65a530a18dbccc5867b1a66b13604905b60df46f87ce45904d99b55150249` | 10 |
| S184 | https://raw.githubusercontent.com/torvalds/linux/v7.2/.gitignore | `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo/corpus/evidence/sources-r33/S184.src:3` | `b850d6169d68eab9b78b1e67a37a784dba7538955e904df7437a22ff3cd4dd4c` | 9 |
| S185 | https://raw.githubusercontent.com/torvalds/linux/v7.2/.rustfmt.toml | `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo/corpus/evidence/sources-r33/S185.src:7` | `b2aaa0727b5c31d2caed8a6865347de1def4b99bb95f844e158351b07cdc7974` | 14 |

## Mutation table

| Mutation | Expected | Observed | Exit | Verdict |
|---|---|---|---:|---|
| R-J removed from receipt | C1=unmet | C1=unmet | 1 | killed |
| R-J removed from dispatch | C1=unmet | C1=unmet | 1 | killed |
| Receipt R-J: every -> the main | C1=unmet | C1=unmet | 1 | killed |
| Receipt R-J rewrapped at 53 columns | C1=met | C1=met | 0 | whitespace parity preserved |
| Entry edited after receipt; judged-sha256 stale | C1=unmet | C1=unmet | 1 | killed |
| Spans removed from all 12 supported rows | C1=unmet | C1=unmet | 1 | killed |
| Only row 1 span shortened to five words | C1=unmet | C1=met | 0 | survived |
| Only row 1 span copied from uncited S181; row cites S180 | C1=unmet | C1=met | 0 | survived |
| Row 12 omitted from receipt | C1=unmet | C1=unmet | 1 | killed |
| Row 1 named twice in receipt | C1=unmet | C1=unmet | 1 | killed |
| All 12 receipt verdicts unsupported | C1=unmet | C1=unmet | 1 | killed |
| Rows 1-3 unsupported; nine remain supported | C1=unmet | C1=unmet | 1 | killed |
| Committed dispatch.json absent | C1=unmet | C1=unmet | 1 | killed |

## Exact commands and full outputs

The shared positive commit was first measured directly, producing the same pristine output reproduced in each triple below. The following are the captured, unabridged stdout streams from every triple; no output is inferred or substituted. Every command is bounded by `timeout 600` and uses the same frozen counter. All captured stderr streams are empty.

### receipt-no-rule

Mutation: R-J removed from receipt.
Expected detector: `C1=unmet`; observed verdict: **killed**.
Sandbox: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo`.
Changed path: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo/.ufo/waves/round-33/judge/JudgeC1Rows.md`.
Pristine commit: `f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc`.
Mutated commit: `6df7fa4135812abbb8dfc642d6ad7788a42c814e`; tree: `a14956d3e2aa3210ec9075fe0f9bb5e7c1f063a7`.
Restored commit: `d7413cd89220a33b968379b57e1668c052bc8ef7`; tree: `aeb3187dd02a9e7cbbb24e1c6689fd38b63c7a7b`.

| Byte state | SHA-256 of changed path |
|---|---|
| Before | `e3862859d0496b5e9f0837e69338b1c9724ab7e827b7fc2f912cb2302765f7ce` |
| Mutated | `6e3abab4f445811156347b0f603ecfc637cd9c89a48018c674680fe4cf9e73be` |
| Restored | `e3862859d0496b5e9f0837e69338b1c9724ab7e827b7fc2f912cb2302765f7ce` |

All other fixture bytes are unchanged; every restored fixture byte equals its pristine byte.

#### pristine

Commit: `f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc`. Printed `C1=met`; exit `0`. Stderr: empty.
Captured receipt: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/results/receipt-no-rule-pristine.json`.

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc --repo /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
```

Full stdout:

```text
rev=f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc repo=/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
entry=present entry_sha256=8797f82b679990de7be866cc2cc514894f4e5c38b8a723e70ee723e8b034c2db head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=12 rows_ok=12 distinct_rows=12 short_readings=0
new_id_rows=12 new_ids=6 (S180,S181,S182,S183,S184,S185)
S180 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/README
S181 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/COPYING
S182 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clang-format
S183 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clippy.toml
S184 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.gitignore
S185 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.rustfmt.toml
gates_ok=6/6 copies_ok=6/6 fetch_ok=6/6 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=12 supported_new=12 spans_bad=[] unsupported=[]
skill_rows=4
C1=met
```

#### mutated

Commit: `6df7fa4135812abbb8dfc642d6ad7788a42c814e`. Printed `C1=unmet`; exit `1`. Stderr: empty.
Captured receipt: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/results/receipt-no-rule-mutated.json`.

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py 6df7fa4135812abbb8dfc642d6ad7788a42c814e --repo /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
```

Full stdout:

```text
rev=6df7fa4135812abbb8dfc642d6ad7788a42c814e repo=/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
entry=present entry_sha256=8797f82b679990de7be866cc2cc514894f4e5c38b8a723e70ee723e8b034c2db head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=12 rows_ok=12 distinct_rows=12 short_readings=0
new_id_rows=12 new_ids=6 (S180,S181,S182,S183,S184,S185)
S180 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/README
S181 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/COPYING
S182 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clang-format
S183 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clippy.toml
S184 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.gitignore
S185 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.rustfmt.toml
gates_ok=6/6 copies_ok=6/6 fetch_ok=6/6 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=no judged_sha=ok covered=yes supported=12 supported_new=12 spans_bad=[] unsupported=[]
skill_rows=4
unmet_conditions=judge
C1=unmet
```

#### restored

Commit: `d7413cd89220a33b968379b57e1668c052bc8ef7`. Printed `C1=met`; exit `0`. Stderr: empty.
Captured receipt: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/results/receipt-no-rule-restored.json`.

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py d7413cd89220a33b968379b57e1668c052bc8ef7 --repo /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
```

Full stdout:

```text
rev=d7413cd89220a33b968379b57e1668c052bc8ef7 repo=/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
entry=present entry_sha256=8797f82b679990de7be866cc2cc514894f4e5c38b8a723e70ee723e8b034c2db head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=12 rows_ok=12 distinct_rows=12 short_readings=0
new_id_rows=12 new_ids=6 (S180,S181,S182,S183,S184,S185)
S180 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/README
S181 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/COPYING
S182 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clang-format
S183 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clippy.toml
S184 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.gitignore
S185 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.rustfmt.toml
gates_ok=6/6 copies_ok=6/6 fetch_ok=6/6 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=12 supported_new=12 spans_bad=[] unsupported=[]
skill_rows=4
C1=met
```

### dispatch-no-rule

Mutation: R-J removed from dispatch.
Expected detector: `C1=unmet`; observed verdict: **killed**.
Sandbox: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo`.
Changed path: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo/.ufo/waves/round-33/judge/dispatch.json`.
Pristine commit: `f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc`.
Mutated commit: `3f343cb393ac428d139ad25fe7baddda20495c50`; tree: `bf98c9ab4572cccb4833496e158ea12076b6438b`.
Restored commit: `7c58401ec5ecf188b841afffac11649a692f4e49`; tree: `aeb3187dd02a9e7cbbb24e1c6689fd38b63c7a7b`.

| Byte state | SHA-256 of changed path |
|---|---|
| Before | `ad4a922a96a8b5349398c6bc8421749aded5b5f9f6fa992519bca8dcfb3f9a12` |
| Mutated | `9efde9f6c378b4739b5e2697ec7b3a76ccbf7cd341a068acd8f871da62f68803` |
| Restored | `ad4a922a96a8b5349398c6bc8421749aded5b5f9f6fa992519bca8dcfb3f9a12` |

All other fixture bytes are unchanged; every restored fixture byte equals its pristine byte.

#### pristine

Commit: `f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc`. Printed `C1=met`; exit `0`. Stderr: empty.
Captured receipt: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/results/dispatch-no-rule-pristine.json`.

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc --repo /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
```

Full stdout:

```text
rev=f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc repo=/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
entry=present entry_sha256=8797f82b679990de7be866cc2cc514894f4e5c38b8a723e70ee723e8b034c2db head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=12 rows_ok=12 distinct_rows=12 short_readings=0
new_id_rows=12 new_ids=6 (S180,S181,S182,S183,S184,S185)
S180 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/README
S181 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/COPYING
S182 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clang-format
S183 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clippy.toml
S184 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.gitignore
S185 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.rustfmt.toml
gates_ok=6/6 copies_ok=6/6 fetch_ok=6/6 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=12 supported_new=12 spans_bad=[] unsupported=[]
skill_rows=4
C1=met
```

#### mutated

Commit: `3f343cb393ac428d139ad25fe7baddda20495c50`. Printed `C1=unmet`; exit `1`. Stderr: empty.
Captured receipt: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/results/dispatch-no-rule-mutated.json`.

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py 3f343cb393ac428d139ad25fe7baddda20495c50 --repo /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
```

Full stdout:

```text
rev=3f343cb393ac428d139ad25fe7baddda20495c50 repo=/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
entry=present entry_sha256=8797f82b679990de7be866cc2cc514894f4e5c38b8a723e70ee723e8b034c2db head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=12 rows_ok=12 distinct_rows=12 short_readings=0
new_id_rows=12 new_ids=6 (S180,S181,S182,S183,S184,S185)
S180 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/README
S181 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/COPYING
S182 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clang-format
S183 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clippy.toml
S184 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.gitignore
S185 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.rustfmt.toml
gates_ok=6/6 copies_ok=6/6 fetch_ok=6/6 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=no receipt_rule=yes judged_sha=ok covered=yes supported=12 supported_new=12 spans_bad=[] unsupported=[]
skill_rows=4
unmet_conditions=judge
C1=unmet
```

#### restored

Commit: `7c58401ec5ecf188b841afffac11649a692f4e49`. Printed `C1=met`; exit `0`. Stderr: empty.
Captured receipt: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/results/dispatch-no-rule-restored.json`.

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py 7c58401ec5ecf188b841afffac11649a692f4e49 --repo /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
```

Full stdout:

```text
rev=7c58401ec5ecf188b841afffac11649a692f4e49 repo=/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
entry=present entry_sha256=8797f82b679990de7be866cc2cc514894f4e5c38b8a723e70ee723e8b034c2db head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=12 rows_ok=12 distinct_rows=12 short_readings=0
new_id_rows=12 new_ids=6 (S180,S181,S182,S183,S184,S185)
S180 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/README
S181 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/COPYING
S182 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clang-format
S183 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clippy.toml
S184 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.gitignore
S185 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.rustfmt.toml
gates_ok=6/6 copies_ok=6/6 fetch_ok=6/6 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=12 supported_new=12 spans_bad=[] unsupported=[]
skill_rows=4
C1=met
```

### receipt-rule-word-change

Mutation: Receipt R-J: every -> the main.
Expected detector: `C1=unmet`; observed verdict: **killed**.
Sandbox: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo`.
Changed path: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo/.ufo/waves/round-33/judge/JudgeC1Rows.md`.
Pristine commit: `f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc`.
Mutated commit: `80499a7a0a0183987b83253ac52d9c7bcab8b7bb`; tree: `5e83db2c8434318d35d6f80d7d4e6d121f8dc024`.
Restored commit: `afad9b7b6d4d2f6572ad7cbf58c8ee859381dbef`; tree: `aeb3187dd02a9e7cbbb24e1c6689fd38b63c7a7b`.

| Byte state | SHA-256 of changed path |
|---|---|
| Before | `e3862859d0496b5e9f0837e69338b1c9724ab7e827b7fc2f912cb2302765f7ce` |
| Mutated | `9a1311b101af2f63749fe20139c94f276417ac64f31708a6180334d333eb2e1b` |
| Restored | `e3862859d0496b5e9f0837e69338b1c9724ab7e827b7fc2f912cb2302765f7ce` |

All other fixture bytes are unchanged; every restored fixture byte equals its pristine byte.

#### pristine

Commit: `f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc`. Printed `C1=met`; exit `0`. Stderr: empty.
Captured receipt: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/results/receipt-rule-word-change-pristine.json`.

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc --repo /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
```

Full stdout:

```text
rev=f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc repo=/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
entry=present entry_sha256=8797f82b679990de7be866cc2cc514894f4e5c38b8a723e70ee723e8b034c2db head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=12 rows_ok=12 distinct_rows=12 short_readings=0
new_id_rows=12 new_ids=6 (S180,S181,S182,S183,S184,S185)
S180 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/README
S181 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/COPYING
S182 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clang-format
S183 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clippy.toml
S184 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.gitignore
S185 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.rustfmt.toml
gates_ok=6/6 copies_ok=6/6 fetch_ok=6/6 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=12 supported_new=12 spans_bad=[] unsupported=[]
skill_rows=4
C1=met
```

#### mutated

Commit: `80499a7a0a0183987b83253ac52d9c7bcab8b7bb`. Printed `C1=unmet`; exit `1`. Stderr: empty.
Captured receipt: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/results/receipt-rule-word-change-mutated.json`.

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py 80499a7a0a0183987b83253ac52d9c7bcab8b7bb --repo /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
```

Full stdout:

```text
rev=80499a7a0a0183987b83253ac52d9c7bcab8b7bb repo=/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
entry=present entry_sha256=8797f82b679990de7be866cc2cc514894f4e5c38b8a723e70ee723e8b034c2db head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=12 rows_ok=12 distinct_rows=12 short_readings=0
new_id_rows=12 new_ids=6 (S180,S181,S182,S183,S184,S185)
S180 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/README
S181 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/COPYING
S182 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clang-format
S183 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clippy.toml
S184 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.gitignore
S185 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.rustfmt.toml
gates_ok=6/6 copies_ok=6/6 fetch_ok=6/6 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=no judged_sha=ok covered=yes supported=12 supported_new=12 spans_bad=[] unsupported=[]
skill_rows=4
unmet_conditions=judge
C1=unmet
```

#### restored

Commit: `afad9b7b6d4d2f6572ad7cbf58c8ee859381dbef`. Printed `C1=met`; exit `0`. Stderr: empty.
Captured receipt: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/results/receipt-rule-word-change-restored.json`.

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py afad9b7b6d4d2f6572ad7cbf58c8ee859381dbef --repo /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
```

Full stdout:

```text
rev=afad9b7b6d4d2f6572ad7cbf58c8ee859381dbef repo=/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
entry=present entry_sha256=8797f82b679990de7be866cc2cc514894f4e5c38b8a723e70ee723e8b034c2db head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=12 rows_ok=12 distinct_rows=12 short_readings=0
new_id_rows=12 new_ids=6 (S180,S181,S182,S183,S184,S185)
S180 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/README
S181 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/COPYING
S182 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clang-format
S183 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clippy.toml
S184 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.gitignore
S185 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.rustfmt.toml
gates_ok=6/6 copies_ok=6/6 fetch_ok=6/6 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=12 supported_new=12 spans_bad=[] unsupported=[]
skill_rows=4
C1=met
```

### receipt-rule-rewrap

Mutation: Receipt R-J rewrapped at 53 columns.
Expected detector: `C1=met`; observed verdict: **whitespace parity preserved**.
Sandbox: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo`.
Changed path: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo/.ufo/waves/round-33/judge/JudgeC1Rows.md`.
Pristine commit: `f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc`.
Mutated commit: `f6781170cf916d138880d1cc92e62a400da02add`; tree: `7cd96a5dcb219d8a558dd4c8ae0706f94f2bc1c3`.
Restored commit: `734736b136b64b93f5d7104673617cbc22b15b62`; tree: `aeb3187dd02a9e7cbbb24e1c6689fd38b63c7a7b`.

| Byte state | SHA-256 of changed path |
|---|---|
| Before | `e3862859d0496b5e9f0837e69338b1c9724ab7e827b7fc2f912cb2302765f7ce` |
| Mutated | `7cceb5de89fabbcdea5aae374df9e3f8ad7c243c22d24faf6d124e45409c89e7` |
| Restored | `e3862859d0496b5e9f0837e69338b1c9724ab7e827b7fc2f912cb2302765f7ce` |

All other fixture bytes are unchanged; every restored fixture byte equals its pristine byte.

#### pristine

Commit: `f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc`. Printed `C1=met`; exit `0`. Stderr: empty.
Captured receipt: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/results/receipt-rule-rewrap-pristine.json`.

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc --repo /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
```

Full stdout:

```text
rev=f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc repo=/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
entry=present entry_sha256=8797f82b679990de7be866cc2cc514894f4e5c38b8a723e70ee723e8b034c2db head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=12 rows_ok=12 distinct_rows=12 short_readings=0
new_id_rows=12 new_ids=6 (S180,S181,S182,S183,S184,S185)
S180 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/README
S181 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/COPYING
S182 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clang-format
S183 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clippy.toml
S184 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.gitignore
S185 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.rustfmt.toml
gates_ok=6/6 copies_ok=6/6 fetch_ok=6/6 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=12 supported_new=12 spans_bad=[] unsupported=[]
skill_rows=4
C1=met
```

#### mutated

Commit: `f6781170cf916d138880d1cc92e62a400da02add`. Printed `C1=met`; exit `0`. Stderr: empty.
Captured receipt: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/results/receipt-rule-rewrap-mutated.json`.

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py f6781170cf916d138880d1cc92e62a400da02add --repo /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
```

Full stdout:

```text
rev=f6781170cf916d138880d1cc92e62a400da02add repo=/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
entry=present entry_sha256=8797f82b679990de7be866cc2cc514894f4e5c38b8a723e70ee723e8b034c2db head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=12 rows_ok=12 distinct_rows=12 short_readings=0
new_id_rows=12 new_ids=6 (S180,S181,S182,S183,S184,S185)
S180 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/README
S181 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/COPYING
S182 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clang-format
S183 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clippy.toml
S184 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.gitignore
S185 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.rustfmt.toml
gates_ok=6/6 copies_ok=6/6 fetch_ok=6/6 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=12 supported_new=12 spans_bad=[] unsupported=[]
skill_rows=4
C1=met
```

#### restored

Commit: `734736b136b64b93f5d7104673617cbc22b15b62`. Printed `C1=met`; exit `0`. Stderr: empty.
Captured receipt: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/results/receipt-rule-rewrap-restored.json`.

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py 734736b136b64b93f5d7104673617cbc22b15b62 --repo /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
```

Full stdout:

```text
rev=734736b136b64b93f5d7104673617cbc22b15b62 repo=/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
entry=present entry_sha256=8797f82b679990de7be866cc2cc514894f4e5c38b8a723e70ee723e8b034c2db head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=12 rows_ok=12 distinct_rows=12 short_readings=0
new_id_rows=12 new_ids=6 (S180,S181,S182,S183,S184,S185)
S180 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/README
S181 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/COPYING
S182 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clang-format
S183 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clippy.toml
S184 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.gitignore
S185 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.rustfmt.toml
gates_ok=6/6 copies_ok=6/6 fetch_ok=6/6 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=12 supported_new=12 spans_bad=[] unsupported=[]
skill_rows=4
C1=met
```

### stale-judged-sha

Mutation: Entry edited after receipt; judged-sha256 stale.
Expected detector: `C1=unmet`; observed verdict: **killed**.
Sandbox: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo`.
Changed path: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo/corpus/knowledge/disk-write-rate-r33.md`.
Pristine commit: `f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc`.
Mutated commit: `5ecb2520a25f22cd488501629c0767b54b5ebdc5`; tree: `1a4c1ae8823a0f39a918420624fc9a080c75ac11`.
Restored commit: `2b48cb04845d9505d8a7a2fb3c8b3e2f56e423e6`; tree: `aeb3187dd02a9e7cbbb24e1c6689fd38b63c7a7b`.

| Byte state | SHA-256 of changed path |
|---|---|
| Before | `8797f82b679990de7be866cc2cc514894f4e5c38b8a723e70ee723e8b034c2db` |
| Mutated | `aaf8aa75fb9051a08eb63906508ae50e098187b260b6fd62d7f0eeef4f767022` |
| Restored | `8797f82b679990de7be866cc2cc514894f4e5c38b8a723e70ee723e8b034c2db` |

All other fixture bytes are unchanged; every restored fixture byte equals its pristine byte.

#### pristine

Commit: `f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc`. Printed `C1=met`; exit `0`. Stderr: empty.
Captured receipt: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/results/stale-judged-sha-pristine.json`.

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc --repo /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
```

Full stdout:

```text
rev=f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc repo=/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
entry=present entry_sha256=8797f82b679990de7be866cc2cc514894f4e5c38b8a723e70ee723e8b034c2db head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=12 rows_ok=12 distinct_rows=12 short_readings=0
new_id_rows=12 new_ids=6 (S180,S181,S182,S183,S184,S185)
S180 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/README
S181 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/COPYING
S182 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clang-format
S183 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clippy.toml
S184 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.gitignore
S185 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.rustfmt.toml
gates_ok=6/6 copies_ok=6/6 fetch_ok=6/6 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=12 supported_new=12 spans_bad=[] unsupported=[]
skill_rows=4
C1=met
```

#### mutated

Commit: `5ecb2520a25f22cd488501629c0767b54b5ebdc5`. Printed `C1=unmet`; exit `1`. Stderr: empty.
Captured receipt: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/results/stale-judged-sha-mutated.json`.

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py 5ecb2520a25f22cd488501629c0767b54b5ebdc5 --repo /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
```

Full stdout:

```text
rev=5ecb2520a25f22cd488501629c0767b54b5ebdc5 repo=/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
entry=present entry_sha256=aaf8aa75fb9051a08eb63906508ae50e098187b260b6fd62d7f0eeef4f767022 head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=12 rows_ok=12 distinct_rows=12 short_readings=0
new_id_rows=12 new_ids=6 (S180,S181,S182,S183,S184,S185)
S180 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/README
S181 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/COPYING
S182 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clang-format
S183 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clippy.toml
S184 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.gitignore
S185 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.rustfmt.toml
gates_ok=6/6 copies_ok=6/6 fetch_ok=6/6 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=bad covered=yes supported=12 supported_new=12 spans_bad=[] unsupported=[]
skill_rows=4
unmet_conditions=judge
C1=unmet
```

#### restored

Commit: `2b48cb04845d9505d8a7a2fb3c8b3e2f56e423e6`. Printed `C1=met`; exit `0`. Stderr: empty.
Captured receipt: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/results/stale-judged-sha-restored.json`.

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py 2b48cb04845d9505d8a7a2fb3c8b3e2f56e423e6 --repo /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
```

Full stdout:

```text
rev=2b48cb04845d9505d8a7a2fb3c8b3e2f56e423e6 repo=/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
entry=present entry_sha256=8797f82b679990de7be866cc2cc514894f4e5c38b8a723e70ee723e8b034c2db head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=12 rows_ok=12 distinct_rows=12 short_readings=0
new_id_rows=12 new_ids=6 (S180,S181,S182,S183,S184,S185)
S180 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/README
S181 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/COPYING
S182 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clang-format
S183 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clippy.toml
S184 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.gitignore
S185 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.rustfmt.toml
gates_ok=6/6 copies_ok=6/6 fetch_ok=6/6 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=12 supported_new=12 spans_bad=[] unsupported=[]
skill_rows=4
C1=met
```

### all-spans-removed

Mutation: Spans removed from all 12 supported rows.
Expected detector: `C1=unmet`; observed verdict: **killed**.
Sandbox: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo`.
Changed path: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo/.ufo/waves/round-33/judge/JudgeC1Rows.md`.
Pristine commit: `f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc`.
Mutated commit: `509c636ce25de1ee2eaceac9aff28277bb1ff4ea`; tree: `6bf62e67c7874fa88cee45aba52939bd54daaeb6`.
Restored commit: `d5b86af69b492ea9f504cc056fd1b6346f11ab40`; tree: `aeb3187dd02a9e7cbbb24e1c6689fd38b63c7a7b`.

| Byte state | SHA-256 of changed path |
|---|---|
| Before | `e3862859d0496b5e9f0837e69338b1c9724ab7e827b7fc2f912cb2302765f7ce` |
| Mutated | `5b247d5fa1416dd4d830d406fd0eb4ce6fbd547fdf5cc3d69f6c30aa96f46183` |
| Restored | `e3862859d0496b5e9f0837e69338b1c9724ab7e827b7fc2f912cb2302765f7ce` |

All other fixture bytes are unchanged; every restored fixture byte equals its pristine byte.

#### pristine

Commit: `f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc`. Printed `C1=met`; exit `0`. Stderr: empty.
Captured receipt: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/results/all-spans-removed-pristine.json`.

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc --repo /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
```

Full stdout:

```text
rev=f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc repo=/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
entry=present entry_sha256=8797f82b679990de7be866cc2cc514894f4e5c38b8a723e70ee723e8b034c2db head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=12 rows_ok=12 distinct_rows=12 short_readings=0
new_id_rows=12 new_ids=6 (S180,S181,S182,S183,S184,S185)
S180 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/README
S181 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/COPYING
S182 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clang-format
S183 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clippy.toml
S184 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.gitignore
S185 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.rustfmt.toml
gates_ok=6/6 copies_ok=6/6 fetch_ok=6/6 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=12 supported_new=12 spans_bad=[] unsupported=[]
skill_rows=4
C1=met
```

#### mutated

Commit: `509c636ce25de1ee2eaceac9aff28277bb1ff4ea`. Printed `C1=unmet`; exit `1`. Stderr: empty.
Captured receipt: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/results/all-spans-removed-mutated.json`.

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py 509c636ce25de1ee2eaceac9aff28277bb1ff4ea --repo /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
```

Full stdout:

```text
rev=509c636ce25de1ee2eaceac9aff28277bb1ff4ea repo=/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
entry=present entry_sha256=8797f82b679990de7be866cc2cc514894f4e5c38b8a723e70ee723e8b034c2db head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=12 rows_ok=12 distinct_rows=12 short_readings=0
new_id_rows=12 new_ids=6 (S180,S181,S182,S183,S184,S185)
S180 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/README
S181 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/COPYING
S182 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clang-format
S183 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clippy.toml
S184 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.gitignore
S185 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.rustfmt.toml
gates_ok=6/6 copies_ok=6/6 fetch_ok=6/6 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=0 supported_new=0 spans_bad=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] unsupported=[]
skill_rows=4
unmet_conditions=judge
C1=unmet
```

#### restored

Commit: `d5b86af69b492ea9f504cc056fd1b6346f11ab40`. Printed `C1=met`; exit `0`. Stderr: empty.
Captured receipt: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/results/all-spans-removed-restored.json`.

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py d5b86af69b492ea9f504cc056fd1b6346f11ab40 --repo /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
```

Full stdout:

```text
rev=d5b86af69b492ea9f504cc056fd1b6346f11ab40 repo=/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
entry=present entry_sha256=8797f82b679990de7be866cc2cc514894f4e5c38b8a723e70ee723e8b034c2db head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=12 rows_ok=12 distinct_rows=12 short_readings=0
new_id_rows=12 new_ids=6 (S180,S181,S182,S183,S184,S185)
S180 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/README
S181 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/COPYING
S182 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clang-format
S183 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clippy.toml
S184 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.gitignore
S185 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.rustfmt.toml
gates_ok=6/6 copies_ok=6/6 fetch_ok=6/6 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=12 supported_new=12 spans_bad=[] unsupported=[]
skill_rows=4
C1=met
```

### one-five-word-span

Mutation: Only row 1 span shortened to five words.
Expected detector: `C1=unmet`; observed verdict: **survived**.
Sandbox: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo`.
Changed path: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo/.ufo/waves/round-33/judge/JudgeC1Rows.md`.
Pristine commit: `f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc`.
Mutated commit: `24aea096e5f698f4d22c40c88c1dbb45a2ad5245`; tree: `3f39b174da3dddd159ee5603cd400ccd5d07b210`.
Restored commit: `19f95e0c7251022ff359e8e71c80b43142f0b3d2`; tree: `aeb3187dd02a9e7cbbb24e1c6689fd38b63c7a7b`.

| Byte state | SHA-256 of changed path |
|---|---|
| Before | `e3862859d0496b5e9f0837e69338b1c9724ab7e827b7fc2f912cb2302765f7ce` |
| Mutated | `1ea728c07558207d713fa9b0cb78348a1cdfbf424d32a70628148ebcc2e1219e` |
| Restored | `e3862859d0496b5e9f0837e69338b1c9724ab7e827b7fc2f912cb2302765f7ce` |

All other fixture bytes are unchanged; every restored fixture byte equals its pristine byte.

#### pristine

Commit: `f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc`. Printed `C1=met`; exit `0`. Stderr: empty.
Captured receipt: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/results/one-five-word-span-pristine.json`.

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc --repo /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
```

Full stdout:

```text
rev=f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc repo=/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
entry=present entry_sha256=8797f82b679990de7be866cc2cc514894f4e5c38b8a723e70ee723e8b034c2db head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=12 rows_ok=12 distinct_rows=12 short_readings=0
new_id_rows=12 new_ids=6 (S180,S181,S182,S183,S184,S185)
S180 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/README
S181 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/COPYING
S182 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clang-format
S183 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clippy.toml
S184 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.gitignore
S185 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.rustfmt.toml
gates_ok=6/6 copies_ok=6/6 fetch_ok=6/6 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=12 supported_new=12 spans_bad=[] unsupported=[]
skill_rows=4
C1=met
```

#### mutated

Commit: `24aea096e5f698f4d22c40c88c1dbb45a2ad5245`. Printed `C1=met`; exit `0`. Stderr: empty.
Captured receipt: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/results/one-five-word-span-mutated.json`.

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py 24aea096e5f698f4d22c40c88c1dbb45a2ad5245 --repo /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
```

Full stdout:

```text
rev=24aea096e5f698f4d22c40c88c1dbb45a2ad5245 repo=/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
entry=present entry_sha256=8797f82b679990de7be866cc2cc514894f4e5c38b8a723e70ee723e8b034c2db head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=12 rows_ok=12 distinct_rows=12 short_readings=0
new_id_rows=12 new_ids=6 (S180,S181,S182,S183,S184,S185)
S180 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/README
S181 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/COPYING
S182 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clang-format
S183 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clippy.toml
S184 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.gitignore
S185 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.rustfmt.toml
gates_ok=6/6 copies_ok=6/6 fetch_ok=6/6 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=11 supported_new=11 spans_bad=[1] unsupported=[]
skill_rows=4
C1=met
```

#### restored

Commit: `19f95e0c7251022ff359e8e71c80b43142f0b3d2`. Printed `C1=met`; exit `0`. Stderr: empty.
Captured receipt: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/results/one-five-word-span-restored.json`.

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py 19f95e0c7251022ff359e8e71c80b43142f0b3d2 --repo /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
```

Full stdout:

```text
rev=19f95e0c7251022ff359e8e71c80b43142f0b3d2 repo=/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
entry=present entry_sha256=8797f82b679990de7be866cc2cc514894f4e5c38b8a723e70ee723e8b034c2db head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=12 rows_ok=12 distinct_rows=12 short_readings=0
new_id_rows=12 new_ids=6 (S180,S181,S182,S183,S184,S185)
S180 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/README
S181 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/COPYING
S182 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clang-format
S183 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clippy.toml
S184 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.gitignore
S185 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.rustfmt.toml
gates_ok=6/6 copies_ok=6/6 fetch_ok=6/6 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=12 supported_new=12 spans_bad=[] unsupported=[]
skill_rows=4
C1=met
```

### one-uncited-copy-span

Mutation: Only row 1 span copied from uncited S181; row cites S180.
Expected detector: `C1=unmet`; observed verdict: **survived**.
Sandbox: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo`.
Changed path: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo/.ufo/waves/round-33/judge/JudgeC1Rows.md`.
Pristine commit: `f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc`.
Mutated commit: `c126ffcd124286106049b99f4b16a025b38b5fef`; tree: `236068fb20b221a054e21cdfbfe9b794885e4463`.
Restored commit: `8ec1669d1523135a314b7aa68788f7fd8ba8c571`; tree: `aeb3187dd02a9e7cbbb24e1c6689fd38b63c7a7b`.

| Byte state | SHA-256 of changed path |
|---|---|
| Before | `e3862859d0496b5e9f0837e69338b1c9724ab7e827b7fc2f912cb2302765f7ce` |
| Mutated | `81544d8a7259fc82480ba958d0494d8d7f95d24c705e44ca05a2737481c1294a` |
| Restored | `e3862859d0496b5e9f0837e69338b1c9724ab7e827b7fc2f912cb2302765f7ce` |

All other fixture bytes are unchanged; every restored fixture byte equals its pristine byte.

#### pristine

Commit: `f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc`. Printed `C1=met`; exit `0`. Stderr: empty.
Captured receipt: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/results/one-uncited-copy-span-pristine.json`.

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc --repo /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
```

Full stdout:

```text
rev=f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc repo=/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
entry=present entry_sha256=8797f82b679990de7be866cc2cc514894f4e5c38b8a723e70ee723e8b034c2db head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=12 rows_ok=12 distinct_rows=12 short_readings=0
new_id_rows=12 new_ids=6 (S180,S181,S182,S183,S184,S185)
S180 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/README
S181 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/COPYING
S182 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clang-format
S183 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clippy.toml
S184 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.gitignore
S185 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.rustfmt.toml
gates_ok=6/6 copies_ok=6/6 fetch_ok=6/6 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=12 supported_new=12 spans_bad=[] unsupported=[]
skill_rows=4
C1=met
```

#### mutated

Commit: `c126ffcd124286106049b99f4b16a025b38b5fef`. Printed `C1=met`; exit `0`. Stderr: empty.
Captured receipt: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/results/one-uncited-copy-span-mutated.json`.

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py c126ffcd124286106049b99f4b16a025b38b5fef --repo /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
```

Full stdout:

```text
rev=c126ffcd124286106049b99f4b16a025b38b5fef repo=/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
entry=present entry_sha256=8797f82b679990de7be866cc2cc514894f4e5c38b8a723e70ee723e8b034c2db head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=12 rows_ok=12 distinct_rows=12 short_readings=0
new_id_rows=12 new_ids=6 (S180,S181,S182,S183,S184,S185)
S180 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/README
S181 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/COPYING
S182 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clang-format
S183 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clippy.toml
S184 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.gitignore
S185 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.rustfmt.toml
gates_ok=6/6 copies_ok=6/6 fetch_ok=6/6 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=11 supported_new=11 spans_bad=[1] unsupported=[]
skill_rows=4
C1=met
```

#### restored

Commit: `8ec1669d1523135a314b7aa68788f7fd8ba8c571`. Printed `C1=met`; exit `0`. Stderr: empty.
Captured receipt: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/results/one-uncited-copy-span-restored.json`.

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py 8ec1669d1523135a314b7aa68788f7fd8ba8c571 --repo /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
```

Full stdout:

```text
rev=8ec1669d1523135a314b7aa68788f7fd8ba8c571 repo=/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
entry=present entry_sha256=8797f82b679990de7be866cc2cc514894f4e5c38b8a723e70ee723e8b034c2db head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=12 rows_ok=12 distinct_rows=12 short_readings=0
new_id_rows=12 new_ids=6 (S180,S181,S182,S183,S184,S185)
S180 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/README
S181 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/COPYING
S182 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clang-format
S183 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clippy.toml
S184 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.gitignore
S185 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.rustfmt.toml
gates_ok=6/6 copies_ok=6/6 fetch_ok=6/6 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=12 supported_new=12 spans_bad=[] unsupported=[]
skill_rows=4
C1=met
```

### one-row-missing

Mutation: Row 12 omitted from receipt.
Expected detector: `C1=unmet`; observed verdict: **killed**.
Sandbox: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo`.
Changed path: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo/.ufo/waves/round-33/judge/JudgeC1Rows.md`.
Pristine commit: `f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc`.
Mutated commit: `3a8355ebe585c7d3b083242884b2ce992556dfca`; tree: `90afb76c4b40722284eefa27ac55e6841ce089ee`.
Restored commit: `eb3c4e0810800ae9d6dc5aaa551a3bb56ec1ba67`; tree: `aeb3187dd02a9e7cbbb24e1c6689fd38b63c7a7b`.

| Byte state | SHA-256 of changed path |
|---|---|
| Before | `e3862859d0496b5e9f0837e69338b1c9724ab7e827b7fc2f912cb2302765f7ce` |
| Mutated | `7db30baa96b5101706280733966934d58efc6c5d2c4cb063d94292e7d2993909` |
| Restored | `e3862859d0496b5e9f0837e69338b1c9724ab7e827b7fc2f912cb2302765f7ce` |

All other fixture bytes are unchanged; every restored fixture byte equals its pristine byte.

#### pristine

Commit: `f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc`. Printed `C1=met`; exit `0`. Stderr: empty.
Captured receipt: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/results/one-row-missing-pristine.json`.

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc --repo /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
```

Full stdout:

```text
rev=f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc repo=/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
entry=present entry_sha256=8797f82b679990de7be866cc2cc514894f4e5c38b8a723e70ee723e8b034c2db head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=12 rows_ok=12 distinct_rows=12 short_readings=0
new_id_rows=12 new_ids=6 (S180,S181,S182,S183,S184,S185)
S180 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/README
S181 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/COPYING
S182 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clang-format
S183 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clippy.toml
S184 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.gitignore
S185 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.rustfmt.toml
gates_ok=6/6 copies_ok=6/6 fetch_ok=6/6 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=12 supported_new=12 spans_bad=[] unsupported=[]
skill_rows=4
C1=met
```

#### mutated

Commit: `3a8355ebe585c7d3b083242884b2ce992556dfca`. Printed `C1=unmet`; exit `1`. Stderr: empty.
Captured receipt: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/results/one-row-missing-mutated.json`.

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py 3a8355ebe585c7d3b083242884b2ce992556dfca --repo /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
```

Full stdout:

```text
rev=3a8355ebe585c7d3b083242884b2ce992556dfca repo=/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
entry=present entry_sha256=8797f82b679990de7be866cc2cc514894f4e5c38b8a723e70ee723e8b034c2db head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=12 rows_ok=12 distinct_rows=12 short_readings=0
new_id_rows=12 new_ids=6 (S180,S181,S182,S183,S184,S185)
S180 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/README
S181 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/COPYING
S182 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clang-format
S183 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clippy.toml
S184 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.gitignore
S185 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.rustfmt.toml
gates_ok=6/6 copies_ok=6/6 fetch_ok=6/6 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=no supported=11 supported_new=11 spans_bad=[] unsupported=[]
skill_rows=4
unmet_conditions=judge
C1=unmet
```

#### restored

Commit: `eb3c4e0810800ae9d6dc5aaa551a3bb56ec1ba67`. Printed `C1=met`; exit `0`. Stderr: empty.
Captured receipt: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/results/one-row-missing-restored.json`.

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py eb3c4e0810800ae9d6dc5aaa551a3bb56ec1ba67 --repo /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
```

Full stdout:

```text
rev=eb3c4e0810800ae9d6dc5aaa551a3bb56ec1ba67 repo=/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
entry=present entry_sha256=8797f82b679990de7be866cc2cc514894f4e5c38b8a723e70ee723e8b034c2db head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=12 rows_ok=12 distinct_rows=12 short_readings=0
new_id_rows=12 new_ids=6 (S180,S181,S182,S183,S184,S185)
S180 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/README
S181 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/COPYING
S182 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clang-format
S183 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clippy.toml
S184 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.gitignore
S185 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.rustfmt.toml
gates_ok=6/6 copies_ok=6/6 fetch_ok=6/6 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=12 supported_new=12 spans_bad=[] unsupported=[]
skill_rows=4
C1=met
```

### one-row-duplicated

Mutation: Row 1 named twice in receipt.
Expected detector: `C1=unmet`; observed verdict: **killed**.
Sandbox: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo`.
Changed path: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo/.ufo/waves/round-33/judge/JudgeC1Rows.md`.
Pristine commit: `f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc`.
Mutated commit: `6e26310e3b4d077d40df9df4909a5854c7151e6d`; tree: `bf090bb4aee4ba693f5c6347e9528fd368e70bf1`.
Restored commit: `52b5c79ee64735e0847c024ad12915b49beae09e`; tree: `aeb3187dd02a9e7cbbb24e1c6689fd38b63c7a7b`.

| Byte state | SHA-256 of changed path |
|---|---|
| Before | `e3862859d0496b5e9f0837e69338b1c9724ab7e827b7fc2f912cb2302765f7ce` |
| Mutated | `5ba9bb35854b5d34aa150ad40b1d9eb9fff117a2acae12b3169be1d8aed6dc27` |
| Restored | `e3862859d0496b5e9f0837e69338b1c9724ab7e827b7fc2f912cb2302765f7ce` |

All other fixture bytes are unchanged; every restored fixture byte equals its pristine byte.

#### pristine

Commit: `f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc`. Printed `C1=met`; exit `0`. Stderr: empty.
Captured receipt: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/results/one-row-duplicated-pristine.json`.

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc --repo /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
```

Full stdout:

```text
rev=f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc repo=/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
entry=present entry_sha256=8797f82b679990de7be866cc2cc514894f4e5c38b8a723e70ee723e8b034c2db head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=12 rows_ok=12 distinct_rows=12 short_readings=0
new_id_rows=12 new_ids=6 (S180,S181,S182,S183,S184,S185)
S180 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/README
S181 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/COPYING
S182 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clang-format
S183 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clippy.toml
S184 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.gitignore
S185 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.rustfmt.toml
gates_ok=6/6 copies_ok=6/6 fetch_ok=6/6 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=12 supported_new=12 spans_bad=[] unsupported=[]
skill_rows=4
C1=met
```

#### mutated

Commit: `6e26310e3b4d077d40df9df4909a5854c7151e6d`. Printed `C1=unmet`; exit `1`. Stderr: empty.
Captured receipt: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/results/one-row-duplicated-mutated.json`.

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py 6e26310e3b4d077d40df9df4909a5854c7151e6d --repo /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
```

Full stdout:

```text
rev=6e26310e3b4d077d40df9df4909a5854c7151e6d repo=/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
entry=present entry_sha256=8797f82b679990de7be866cc2cc514894f4e5c38b8a723e70ee723e8b034c2db head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=12 rows_ok=12 distinct_rows=12 short_readings=0
new_id_rows=12 new_ids=6 (S180,S181,S182,S183,S184,S185)
S180 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/README
S181 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/COPYING
S182 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clang-format
S183 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clippy.toml
S184 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.gitignore
S185 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.rustfmt.toml
gates_ok=6/6 copies_ok=6/6 fetch_ok=6/6 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=no supported=12 supported_new=12 spans_bad=[] unsupported=[]
skill_rows=4
unmet_conditions=judge
C1=unmet
```

#### restored

Commit: `52b5c79ee64735e0847c024ad12915b49beae09e`. Printed `C1=met`; exit `0`. Stderr: empty.
Captured receipt: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/results/one-row-duplicated-restored.json`.

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py 52b5c79ee64735e0847c024ad12915b49beae09e --repo /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
```

Full stdout:

```text
rev=52b5c79ee64735e0847c024ad12915b49beae09e repo=/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
entry=present entry_sha256=8797f82b679990de7be866cc2cc514894f4e5c38b8a723e70ee723e8b034c2db head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=12 rows_ok=12 distinct_rows=12 short_readings=0
new_id_rows=12 new_ids=6 (S180,S181,S182,S183,S184,S185)
S180 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/README
S181 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/COPYING
S182 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clang-format
S183 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clippy.toml
S184 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.gitignore
S185 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.rustfmt.toml
gates_ok=6/6 copies_ok=6/6 fetch_ok=6/6 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=12 supported_new=12 spans_bad=[] unsupported=[]
skill_rows=4
C1=met
```

### all-unsupported

Mutation: All 12 receipt verdicts unsupported.
Expected detector: `C1=unmet`; observed verdict: **killed**.
Sandbox: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo`.
Changed path: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo/.ufo/waves/round-33/judge/JudgeC1Rows.md`.
Pristine commit: `f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc`.
Mutated commit: `7904723ce0240fd44b1c639b91819ae6460f1e31`; tree: `78d1d840a362db7e41e55db9a91cccc4e20c1252`.
Restored commit: `f8fc1a4ccdad7321ff4fdd6b4fb875826ca8da7a`; tree: `aeb3187dd02a9e7cbbb24e1c6689fd38b63c7a7b`.

| Byte state | SHA-256 of changed path |
|---|---|
| Before | `e3862859d0496b5e9f0837e69338b1c9724ab7e827b7fc2f912cb2302765f7ce` |
| Mutated | `3a17b2ffb817c6ee82a05cb3709a12b52d8cede207e8ea9a400b1b096c20d2e3` |
| Restored | `e3862859d0496b5e9f0837e69338b1c9724ab7e827b7fc2f912cb2302765f7ce` |

All other fixture bytes are unchanged; every restored fixture byte equals its pristine byte.

#### pristine

Commit: `f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc`. Printed `C1=met`; exit `0`. Stderr: empty.
Captured receipt: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/results/all-unsupported-pristine.json`.

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc --repo /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
```

Full stdout:

```text
rev=f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc repo=/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
entry=present entry_sha256=8797f82b679990de7be866cc2cc514894f4e5c38b8a723e70ee723e8b034c2db head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=12 rows_ok=12 distinct_rows=12 short_readings=0
new_id_rows=12 new_ids=6 (S180,S181,S182,S183,S184,S185)
S180 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/README
S181 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/COPYING
S182 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clang-format
S183 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clippy.toml
S184 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.gitignore
S185 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.rustfmt.toml
gates_ok=6/6 copies_ok=6/6 fetch_ok=6/6 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=12 supported_new=12 spans_bad=[] unsupported=[]
skill_rows=4
C1=met
```

#### mutated

Commit: `7904723ce0240fd44b1c639b91819ae6460f1e31`. Printed `C1=unmet`; exit `1`. Stderr: empty.
Captured receipt: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/results/all-unsupported-mutated.json`.

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py 7904723ce0240fd44b1c639b91819ae6460f1e31 --repo /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
```

Full stdout:

```text
rev=7904723ce0240fd44b1c639b91819ae6460f1e31 repo=/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
entry=present entry_sha256=8797f82b679990de7be866cc2cc514894f4e5c38b8a723e70ee723e8b034c2db head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=12 rows_ok=12 distinct_rows=12 short_readings=0
new_id_rows=12 new_ids=6 (S180,S181,S182,S183,S184,S185)
S180 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/README
S181 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/COPYING
S182 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clang-format
S183 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clippy.toml
S184 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.gitignore
S185 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.rustfmt.toml
gates_ok=6/6 copies_ok=6/6 fetch_ok=6/6 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=0 supported_new=0 spans_bad=[] unsupported=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
skill_rows=4
unmet_conditions=judge
C1=unmet
```

#### restored

Commit: `f8fc1a4ccdad7321ff4fdd6b4fb875826ca8da7a`. Printed `C1=met`; exit `0`. Stderr: empty.
Captured receipt: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/results/all-unsupported-restored.json`.

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py f8fc1a4ccdad7321ff4fdd6b4fb875826ca8da7a --repo /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
```

Full stdout:

```text
rev=f8fc1a4ccdad7321ff4fdd6b4fb875826ca8da7a repo=/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
entry=present entry_sha256=8797f82b679990de7be866cc2cc514894f4e5c38b8a723e70ee723e8b034c2db head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=12 rows_ok=12 distinct_rows=12 short_readings=0
new_id_rows=12 new_ids=6 (S180,S181,S182,S183,S184,S185)
S180 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/README
S181 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/COPYING
S182 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clang-format
S183 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clippy.toml
S184 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.gitignore
S185 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.rustfmt.toml
gates_ok=6/6 copies_ok=6/6 fetch_ok=6/6 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=12 supported_new=12 spans_bad=[] unsupported=[]
skill_rows=4
C1=met
```

### three-unsupported

Mutation: Rows 1-3 unsupported; nine remain supported.
Expected detector: `C1=unmet`; observed verdict: **killed**.
Sandbox: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo`.
Changed path: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo/.ufo/waves/round-33/judge/JudgeC1Rows.md`.
Pristine commit: `f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc`.
Mutated commit: `ddb9b31e83e44fd6dc9b9f05bca3c247834b655c`; tree: `3a8d70ae0438a581c555a381bd487898bdd140c9`.
Restored commit: `d3fcd7a1f0a62bb21378ba040d0945883a16f8b5`; tree: `aeb3187dd02a9e7cbbb24e1c6689fd38b63c7a7b`.

| Byte state | SHA-256 of changed path |
|---|---|
| Before | `e3862859d0496b5e9f0837e69338b1c9724ab7e827b7fc2f912cb2302765f7ce` |
| Mutated | `f85989f119f3d1e44e3fa1234f09c2441375f4ea80d10f5b8ebd1acd326ce549` |
| Restored | `e3862859d0496b5e9f0837e69338b1c9724ab7e827b7fc2f912cb2302765f7ce` |

All other fixture bytes are unchanged; every restored fixture byte equals its pristine byte.

#### pristine

Commit: `f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc`. Printed `C1=met`; exit `0`. Stderr: empty.
Captured receipt: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/results/three-unsupported-pristine.json`.

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc --repo /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
```

Full stdout:

```text
rev=f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc repo=/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
entry=present entry_sha256=8797f82b679990de7be866cc2cc514894f4e5c38b8a723e70ee723e8b034c2db head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=12 rows_ok=12 distinct_rows=12 short_readings=0
new_id_rows=12 new_ids=6 (S180,S181,S182,S183,S184,S185)
S180 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/README
S181 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/COPYING
S182 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clang-format
S183 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clippy.toml
S184 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.gitignore
S185 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.rustfmt.toml
gates_ok=6/6 copies_ok=6/6 fetch_ok=6/6 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=12 supported_new=12 spans_bad=[] unsupported=[]
skill_rows=4
C1=met
```

#### mutated

Commit: `ddb9b31e83e44fd6dc9b9f05bca3c247834b655c`. Printed `C1=unmet`; exit `1`. Stderr: empty.
Captured receipt: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/results/three-unsupported-mutated.json`.

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py ddb9b31e83e44fd6dc9b9f05bca3c247834b655c --repo /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
```

Full stdout:

```text
rev=ddb9b31e83e44fd6dc9b9f05bca3c247834b655c repo=/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
entry=present entry_sha256=8797f82b679990de7be866cc2cc514894f4e5c38b8a723e70ee723e8b034c2db head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=12 rows_ok=12 distinct_rows=12 short_readings=0
new_id_rows=12 new_ids=6 (S180,S181,S182,S183,S184,S185)
S180 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/README
S181 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/COPYING
S182 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clang-format
S183 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clippy.toml
S184 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.gitignore
S185 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.rustfmt.toml
gates_ok=6/6 copies_ok=6/6 fetch_ok=6/6 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=9 supported_new=9 spans_bad=[] unsupported=[1, 2, 3]
skill_rows=4
unmet_conditions=judge
C1=unmet
```

#### restored

Commit: `d3fcd7a1f0a62bb21378ba040d0945883a16f8b5`. Printed `C1=met`; exit `0`. Stderr: empty.
Captured receipt: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/results/three-unsupported-restored.json`.

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py d3fcd7a1f0a62bb21378ba040d0945883a16f8b5 --repo /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
```

Full stdout:

```text
rev=d3fcd7a1f0a62bb21378ba040d0945883a16f8b5 repo=/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
entry=present entry_sha256=8797f82b679990de7be866cc2cc514894f4e5c38b8a723e70ee723e8b034c2db head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=12 rows_ok=12 distinct_rows=12 short_readings=0
new_id_rows=12 new_ids=6 (S180,S181,S182,S183,S184,S185)
S180 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/README
S181 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/COPYING
S182 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clang-format
S183 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clippy.toml
S184 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.gitignore
S185 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.rustfmt.toml
gates_ok=6/6 copies_ok=6/6 fetch_ok=6/6 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=12 supported_new=12 spans_bad=[] unsupported=[]
skill_rows=4
C1=met
```

### dispatch-absent

Mutation: Committed dispatch.json absent.
Expected detector: `C1=unmet`; observed verdict: **killed**.
Sandbox: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo`.
Changed path: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo/.ufo/waves/round-33/judge/dispatch.json`.
Pristine commit: `f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc`.
Mutated commit: `a190ef16bf56225a651c80f16953afb7893f6a6d`; tree: `c59346223f4531440175de8c5a238b75555a3d98`.
Restored commit: `cc1f329f47b930cf87bdd2cc3a8194934e4dd894`; tree: `aeb3187dd02a9e7cbbb24e1c6689fd38b63c7a7b`.

| Byte state | SHA-256 of changed path |
|---|---|
| Before | `ad4a922a96a8b5349398c6bc8421749aded5b5f9f6fa992519bca8dcfb3f9a12` |
| Mutated | absent |
| Restored | `ad4a922a96a8b5349398c6bc8421749aded5b5f9f6fa992519bca8dcfb3f9a12` |

All other fixture bytes are unchanged; every restored fixture byte equals its pristine byte.

#### pristine

Commit: `f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc`. Printed `C1=met`; exit `0`. Stderr: empty.
Captured receipt: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/results/dispatch-absent-pristine.json`.

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc --repo /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
```

Full stdout:

```text
rev=f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc repo=/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
entry=present entry_sha256=8797f82b679990de7be866cc2cc514894f4e5c38b8a723e70ee723e8b034c2db head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=12 rows_ok=12 distinct_rows=12 short_readings=0
new_id_rows=12 new_ids=6 (S180,S181,S182,S183,S184,S185)
S180 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/README
S181 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/COPYING
S182 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clang-format
S183 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clippy.toml
S184 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.gitignore
S185 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.rustfmt.toml
gates_ok=6/6 copies_ok=6/6 fetch_ok=6/6 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=12 supported_new=12 spans_bad=[] unsupported=[]
skill_rows=4
C1=met
```

#### mutated

Commit: `a190ef16bf56225a651c80f16953afb7893f6a6d`. Printed `C1=unmet`; exit `1`. Stderr: empty.
Captured receipt: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/results/dispatch-absent-mutated.json`.

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py a190ef16bf56225a651c80f16953afb7893f6a6d --repo /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
```

Full stdout:

```text
rev=a190ef16bf56225a651c80f16953afb7893f6a6d repo=/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
entry=present entry_sha256=8797f82b679990de7be866cc2cc514894f4e5c38b8a723e70ee723e8b034c2db head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=12 rows_ok=12 distinct_rows=12 short_readings=0
new_id_rows=12 new_ids=6 (S180,S181,S182,S183,S184,S185)
S180 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/README
S181 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/COPYING
S182 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clang-format
S183 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clippy.toml
S184 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.gitignore
S185 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.rustfmt.toml
gates_ok=6/6 copies_ok=6/6 fetch_ok=6/6 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=no receipt_rule=yes judged_sha=ok covered=yes supported=12 supported_new=12 spans_bad=[] unsupported=[]
skill_rows=4
unmet_conditions=judge
C1=unmet
```

#### restored

Commit: `cc1f329f47b930cf87bdd2cc3a8194934e4dd894`. Printed `C1=met`; exit `0`. Stderr: empty.
Captured receipt: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/results/dispatch-absent-restored.json`.

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py cc1f329f47b930cf87bdd2cc3a8194934e4dd894 --repo /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
```

Full stdout:

```text
rev=cc1f329f47b930cf87bdd2cc3a8194934e4dd894 repo=/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
entry=present entry_sha256=8797f82b679990de7be866cc2cc514894f4e5c38b8a723e70ee723e8b034c2db head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=12 rows_ok=12 distinct_rows=12 short_readings=0
new_id_rows=12 new_ids=6 (S180,S181,S182,S183,S184,S185)
S180 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/README
S181 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/COPYING
S182 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clang-format
S183 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.clippy.toml
S184 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.gitignore
S185 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/.rustfmt.toml
gates_ok=6/6 copies_ok=6/6 fetch_ok=6/6 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=12 supported_new=12 spans_bad=[] unsupported=[]
skill_rows=4
C1=met
```

## Restoration and containment evidence

- HEAD remains `f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc`.
- Original positive tree: `aeb3187dd02a9e7cbbb24e1c6689fd38b63c7a7b`.
- Restored index tree: `aeb3187dd02a9e7cbbb24e1c6689fd38b63c7a7b` (exact match: `true`).
- All 12 worktree fixture SHA-256 values match the pre-mutation manifest: `true`.
- Counter before SHA-256: `7361f3e31f4a88afc7a50a907d9c2d5b66ca98306a633760ecc40ca53fa3d942`.
- Counter after SHA-256: `7361f3e31f4a88afc7a50a907d9c2d5b66ca98306a633760ecc40ca53fa3d942`.
- Active detector child processes after cleanup: `0`. Each detector process group is explicitly terminated after collection; all command trees have completed.
- Machine-readable restoration receipt: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/restoration.json`.

| Absolute fixture path | Before and final SHA-256 |
|---|---|
| `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo/corpus/SOURCES.md` | `13599cbc66cae8a02598924c27943e79d2db27fc96bc3e465f5003d5d26af365` |
| `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo/SKILL.md` | `940f7fc150e8628e2e4a8070687db5adc680f131ea584a9fa8a905003a2f8ca3` |
| `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo/corpus/knowledge/disk-write-rate-r33.md` | `8797f82b679990de7be866cc2cc514894f4e5c38b8a723e70ee723e8b034c2db` |
| `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo/corpus/lessons/round-33.md` | `6e41aedb28261ddd631c866c26df0ca73662e1ad4dcd683e593dbccf53c88b36` |
| `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo/.ufo/waves/round-33/judge/JudgeC1Rows.md` | `e3862859d0496b5e9f0837e69338b1c9724ab7e827b7fc2f912cb2302765f7ce` |
| `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo/.ufo/waves/round-33/judge/dispatch.json` | `ad4a922a96a8b5349398c6bc8421749aded5b5f9f6fa992519bca8dcfb3f9a12` |
| `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo/corpus/evidence/sources-r33/S180.src` | `2844b0b2cafe22741724c4fdda79b1259de48743f12ad40ce408adb1ef00ceda` |
| `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo/corpus/evidence/sources-r33/S181.src` | `fb5a425bd3b3cd6071a3a9aff9909a859e7c1158d54d32e07658398cd67eb6a0` |
| `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo/corpus/evidence/sources-r33/S182.src` | `127fc850fd74996410163972eb3e2fb9af428ada97d2403b149f8d16c2d674f5` |
| `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo/corpus/evidence/sources-r33/S183.src` | `84f65a530a18dbccc5867b1a66b13604905b60df46f87ce45904d99b55150249` |
| `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo/corpus/evidence/sources-r33/S184.src` | `b850d6169d68eab9b78b1e67a37a784dba7538955e904df7437a22ff3cd4dd4c` |
| `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo/corpus/evidence/sources-r33/S185.src` | `b2aaa0727b5c31d2caed8a6865347de1def4b99bb95f844e158351b07cdc7974` |

## Preserved scripts and machine-readable receipts

| Script | SHA-256 | Purpose |
|---|---|---|
| `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/build-control.py` | `08462ccb924b9dcd427804f505caa19b3d010ef5b10f64b6834b833232a19f72` | Build and commit the new positive fixture files; source-registry and skill insertions were made surgically in the sandbox before this script ran. |
| `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/probe-shapes.py` | `cfe85435afab7b72cc3d607d362309a81011d9da844a6cb741e598ee70e8554a` | Prepare isolated mutant and restored Git trees; run 13 independent bounded detector triples with six workers; restore the index and record bytes. |
| `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/render-report.py` | `0d54621e87924853f7746ac0918cf8dbf4560e1277f12e269c58a2edb277d222` | Render this report from captured outputs without rerunning the detector. |

- Positive fixture metadata: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/positive-manifest.json`.
- Mutant and restoration revisions/hashes: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/controls-manifest.json`.
- Complete combined measurement receipts: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/probe-results.json`.
- Per-command captured stdout/stderr/exit receipts: `/fast/scratch/hyaku/mori-r33/CtlJudgeShapes/results`.

### Commands actually used to create and exercise the sandbox

```sh
timeout 180 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q /home/vgpnk/Projects/shokunin/mori-shokunin /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
timeout 15 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo config user.name ctl
timeout 15 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo config user.email ctl@local
timeout 65 curl -sSL --fail -m 60 https://raw.githubusercontent.com/torvalds/linux/v7.2/README -o /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/S180.src
timeout 65 curl -sSL --fail -m 60 https://raw.githubusercontent.com/torvalds/linux/v7.2/COPYING -o /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/S181.src
timeout 65 curl -sSL --fail -m 60 https://raw.githubusercontent.com/torvalds/linux/v7.2/.clang-format -o /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/S182.src
timeout 65 curl -sSL --fail -m 60 https://raw.githubusercontent.com/torvalds/linux/v7.2/.clippy.toml -o /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/S183.src
timeout 65 curl -sSL --fail -m 60 https://raw.githubusercontent.com/torvalds/linux/v7.2/.gitignore -o /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/S184.src
timeout 65 curl -sSL --fail -m 60 https://raw.githubusercontent.com/torvalds/linux/v7.2/.rustfmt.toml -o /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/S185.src
timeout 180 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE python3 /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/build-control.py
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py f145ac70cf600c2eb6d44be6cd63d2ae7a41e9fc --repo /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/repo
timeout 600 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE python3 /fast/scratch/hyaku/mori-r33/CtlJudgeShapes/probe-shapes.py
```

Tool installs or updates: none. Only the assigned mutation probe and evidence rendering were performed; no build, lint, formatter, integration, shipment, or contract change was performed.
