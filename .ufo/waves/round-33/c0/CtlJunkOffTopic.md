Declared fabricated-receipt negative variant: `C1=met`, exit 0; honest junk/off-topic negative control: `C1=unmet`, exit 1. The former exposes the explicitly declared receipt-integrity residual, not genuine semantic support.

# CtlJunkOffTopic — C0 sandbox findings

## Scope, axes and identities

- Seat: `MoriR33.CtlJunkOffTopic`; advisory synthetic-control review only. No canonical runtime judgment, admission, integration or shipping performed.
- Axes: **depth** (the claimed diskstats knowledge), **calibration** (unsupported claims and false receipt provenance), **freshness** (measurement-time upstream byte identity), **operability** (reproducible committed controls). No coverage or adjacency improvement is claimed. Review dimensions also include containment and receipt integrity.
- Frozen base: `27969134d51ea15982db4f36c77e2decd2a22b07`.
- Frozen contract read: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/contract.md`, including P-C1, R-J and the declared residual at lines 73–75.
- Frozen counter read, including its complete docstring: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py`.
- Counter SHA256: `7361f3e31f4a88afc7a50a907d9c2d5b66ca98306a633760ecc40ca53fa3d942`.
- Sandbox clone for both states: `/fast/scratch/hyaku/mori-r33/CtlJunkOffTopic/repo`.
- Honest commit: `be0bad2a9a0ffba62585a3ca99e7b8f7e710f40f`.
- Forged-receipt child commit: `5ae82bab403743ac65ff420802b28fd9212e8f5b`. Its commit operation changed exactly one file: `/fast/scratch/hyaku/mori-r33/CtlJunkOffTopic/repo/.ufo/waves/round-33/judge/JudgeC1Rows.md`.
- Both counter runs report the identical entry SHA256: `fc3e0086367fd2f20b0c3c18bbc6d80699b81e182a58c33810de4fc802a97a0d`.

All git writes were confined to the sandbox clone, with `GIT_DIR`, `GIT_WORK_TREE` and `GIT_INDEX_FILE` unset. Sandbox author identity is `ctl <ctl@local>`. The only lane write is this report; no fleet write occurred. No counter or contract edits occurred.

## Constructed counterexample and real source evidence

The sandbox contains five new mined registry rows, five unchanged curl-fetched copies, five Gate rows with decision `admit, A, mined`, twelve distinct junk diskstats rows, four qualifying Round33 skill lines, a dispatch quoting R-J verbatim, and an entry-hash-bound receipt quoting R-J verbatim.

Artifacts:

- `/fast/scratch/hyaku/mori-r33/CtlJunkOffTopic/repo/corpus/SOURCES.md`
- `/fast/scratch/hyaku/mori-r33/CtlJunkOffTopic/repo/corpus/lessons/round-33.md`
- `/fast/scratch/hyaku/mori-r33/CtlJunkOffTopic/repo/corpus/knowledge/disk-write-rate-r33.md`
- `/fast/scratch/hyaku/mori-r33/CtlJunkOffTopic/repo/SKILL.md`
- `/fast/scratch/hyaku/mori-r33/CtlJunkOffTopic/repo/.ufo/waves/round-33/judge/dispatch.json`
- `/fast/scratch/hyaku/mori-r33/CtlJunkOffTopic/repo/.ufo/waves/round-33/judge/JudgeC1Rows.md`

Accessed: `2026-10-22`. Every URL is tag-pinned to Linux v7.2. Both counter measurements independently fetched all five URLs and reported matching copy/Gate/upstream hashes, distinct sources and zero rows without quote overlap.

| id | URL | Absolute copy locator | SHA256 | Gate quotation |
|---|---|---|---|---|
| S180 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/process/coding-style.rst | `/fast/scratch/hyaku/mori-r33/CtlJunkOffTopic/repo/corpus/evidence/sources-r33/S180.src:21` | `332454d2ab9a0462dd9f292c52291cf3b5e1afcd638aa06df15f557c47a126f5` | 11 words: “Tabs are 8 characters, and thus indentations are also 8 characters.” |
| S181 | https://raw.githubusercontent.com/torvalds/linux/v7.2/README | `/fast/scratch/hyaku/mori-r33/CtlJunkOffTopic/repo/corpus/evidence/sources-r33/S181.src:4` | `2844b0b2cafe22741724c4fdda79b1259de48743f12ad40ce408adb1ef00ceda` | 11 words: “The Linux kernel is the core of any Linux operating system.” |
| S182 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/process/submitting-patches.rst | `/fast/scratch/hyaku/mori-r33/CtlJunkOffTopic/repo/corpus/evidence/sources-r33/S182.src:19` | `d9c5f7c9c849751d49208b537da9766dd6e1527a4eab0fec3baaf087ce7f2f23` | 11 words: “This documentation assumes that you're using ``git`` to prepare your patches.” |
| S183 | https://raw.githubusercontent.com/torvalds/linux/v7.2/COPYING | `/fast/scratch/hyaku/mori-r33/CtlJunkOffTopic/repo/corpus/evidence/sources-r33/S183.src:20` | `fb5a425bd3b3cd6071a3a9aff9909a859e7c1158d54d32e07658398cd67eb6a0` | 12 words: “All contributions to the Linux Kernel are subject to this COPYING file.” |
| S184 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/README.rst | `/fast/scratch/hyaku/mori-r33/CtlJunkOffTopic/repo/corpus/evidence/sources-r33/S184.src:6` | `f23b47d66a6bea64044743276b9f94c2d83dc3e4c95fea65cd539cc08e98ebc4` | 9 words: “These are the release notes for Linux version 6.” |

Deliberate overlap pairs are characters/indentations, kernel/core, documentation/patches, contributions/Kernel and release/notes. These satisfy the lexical check without stating the diskstats claims.

Strongest concrete counterexample: row 11 claims that coding-style “characters and indentations” permit division by a zero-duration interval while preserving finite disk write rates. Its only cited Gate quotation specifies tab/indentation width. No part of that quote states the denominator or finite-rate assertions. Source genuineness, located spans, matching hashes and lexical overlap cannot bridge that semantic gap.

## Honest R-J application, every row

Frozen R-J, preserved verbatim in dispatch and both receipts:

> A row is supported only when the quotes located in the committed copies of the sources it cites state every fact its observation and reading cells assert, and its verdict cell follows from that reading without any further fact; a row any part of which is not so stated is unsupported, including a row the judge would accept only with a caveat or through a source the row does not cite.

The honest committed receipt contains exactly one `row N: unsupported` line per row and an individual reason for each:

| Row | Cited id | Unsupported assertion; the located quote supplies no such fact |
|---|---|---|
| 1 | S180 | Every diskstats written sector is 4096 bytes; coding indentation width does not state sector units. |
| 2 | S181 | Future writes are completed before submission and charged when devices appear; a kernel introduction does not state this. |
| 3 | S182 | Every kernel requires ninety seven diskstats fields; git patch preparation does not specify any field count. |
| 4 | S183 | Counters wrap every minute and need modulo-sixty correction; contribution licensing states no counter behavior. |
| 5 | S184 | Partition counters are independent of parent disks and must be added; a release-notes introduction states neither. |
| 6 | S180 | Stacked-device writes are disjoint and safe to sum; coding indentation states neither. |
| 7 | S181 | All queued writes become complete whenever diskstats is sampled; a kernel introduction does not state queue/completion semantics. |
| 8 | S182 | All deltas are normalized to ten seconds irrespective of elapsed time; patch preparation supplies no interval rule. |
| 9 | S183 | Device replacement cannot reset counters, making every negative delta corruption; licensing supplies no continuity or reset rule. |
| 10 | S184 | Written sectors equal elapsed write milliseconds and are interchangeable; release-note identification supplies no unit equivalence. |
| 11 | S180 | Zero elapsed time gives a valid denominator and finite rate; indentation width supplies no rate arithmetic. |
| 12 | S181 | Device logical block size always equals the diskstats sector unit; a kernel introduction supplies no unit conversion rule. |

No caveat, uncited source or outside knowledge was used to rescue a row. All twelve are unsupported.

## Control A — honest junk/off-topic receipt

What: all structural evidence is real and well-shaped, but the honest receipt marks all twelve claims unsupported.

Clone: `/fast/scratch/hyaku/mori-r33/CtlJunkOffTopic/repo`

Commit: `be0bad2a9a0ffba62585a3ca99e7b8f7e710f40f`

Exact counter command:

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py be0bad2a9a0ffba62585a3ca99e7b8f7e710f40f --repo /fast/scratch/hyaku/mori-r33/CtlJunkOffTopic/repo
```

Full stdout:

```text
rev=be0bad2a9a0ffba62585a3ca99e7b8f7e710f40f repo=/fast/scratch/hyaku/mori-r33/CtlJunkOffTopic/repo
entry=present entry_sha256=fc3e0086367fd2f20b0c3c18bbc6d80699b81e182a58c33810de4fc802a97a0d head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=12 rows_ok=12 distinct_rows=12 short_readings=0
new_id_rows=12 new_ids=5 (S180,S181,S182,S183,S184)
S180 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/process/coding-style.rst
S181 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/README
S182 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/process/submitting-patches.rst
S183 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/COPYING
S184 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/README.rst
gates_ok=5/5 copies_ok=5/5 fetch_ok=5/5 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=0 supported_new=0 spans_bad=[] unsupported=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
skill_rows=4
unmet_conditions=judge
C1=unmet
```

Exit code: **1**. Stderr: empty. Printed `C1=unmet`: **yes**. Printed `C1=met`: **no**. The sole reported unmet condition is `judge`, as expected.

Saved stdout: `/fast/scratch/hyaku/mori-r33/CtlJunkOffTopic/honest-counter.stdout`.

## Control B — declared fabricated-receipt residual

What: the same entry, sources, copies, Gate rows, dispatch and skill lines, with only the receipt changed. All twelve labels are forged to `supported` with located six-word spans. The forged receipt explicitly identifies its labels as false and preserves every honest reason. It still quotes the unchanged R-J and binds to the unchanged entry hash.

Six-word spans, reused for the appropriate cited rows:

- S180, rows 1/6/11: `Tabs are 8 characters, and thus`
- S181, rows 2/7/12: `The Linux kernel is the core`
- S182, rows 3/8: `This documentation assumes that you're using`
- S183, rows 4/9: `All contributions to the Linux Kernel`
- S184, rows 5/10: `These are the release notes for`

Each is located at the absolute copy locator in the source-evidence table. None states its row's diskstats assertions.

Clone: `/fast/scratch/hyaku/mori-r33/CtlJunkOffTopic/repo`

Commit: `5ae82bab403743ac65ff420802b28fd9212e8f5b`

Exact counter command:

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py 5ae82bab403743ac65ff420802b28fd9212e8f5b --repo /fast/scratch/hyaku/mori-r33/CtlJunkOffTopic/repo
```

Full stdout:

```text
rev=5ae82bab403743ac65ff420802b28fd9212e8f5b repo=/fast/scratch/hyaku/mori-r33/CtlJunkOffTopic/repo
entry=present entry_sha256=fc3e0086367fd2f20b0c3c18bbc6d80699b81e182a58c33810de4fc802a97a0d head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=12 rows_ok=12 distinct_rows=12 short_readings=0
new_id_rows=12 new_ids=5 (S180,S181,S182,S183,S184)
S180 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/process/coding-style.rst
S181 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/README
S182 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/process/submitting-patches.rst
S183 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/COPYING
S184 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/README.rst
gates_ok=5/5 copies_ok=5/5 fetch_ok=5/5 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=12 supported_new=12 spans_bad=[] unsupported=[]
skill_rows=4
C1=met
```

Exit code: **0**. Stderr: empty. Printed `C1=unmet`: **no**. Printed `C1=met`: **yes**.

Saved stdout: `/fast/scratch/hyaku/mori-r33/CtlJunkOffTopic/forged-counter.stdout`.

## Finding and smallest safe correction

**Observed:** honest junk is rejected solely by the receipt's honest unsupported labels. Changing those labels and inserting irrelevant located spans makes the frozen counter print `C1=met`, even while the forged receipt retains explicit unsupported reasons. The structural checks prove receipt shape and byte identity, not semantic entailment or authentic judging.

**Evidence:** `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py:243-250` checks token overlap; lines 264–285 accept supported labels when a six-word span occurs in a cited copy. Neither operation checks whether the span states the observation/reading facts. The declared trust boundary is `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/contract.md:73-75`.

**Classification:** the honest negative control meets its expected rejection. The forged variant is the contract's declared fabricated-receipt residual. It is a real false positive if `C1=met` is treated as semantic support; the counter/target would be wrong for that interpretation. It is not an honest-control miss, a depth improvement, an admission or evidence of saturation. Treating forged shape as knowledge would sacrifice calibration without adding depth; the canonical judgment must not accept that trade.

**Smallest safe correction:** leave the frozen counter untouched. Keep the honest twelve unsupported decisions, and require the independent closure's actual R-J re-judgement plus the real judge transcript/receipt provenance before any depth claim is admitted. For real data, replace off-topic support and unsupported assertions with quoted facts that fully state each row, not with more overlap words. No id/label shortcut or source-keyword blocklist corrects this semantic defect. A different automated integrity promise requires a separately declared future design, never a post-data amendment of this frozen claim.

## Control scripts, execution and tooling

| Script | SHA256 | Purpose |
|---|---|---|
| `/fast/scratch/hyaku/mori-r33/CtlJunkOffTopic/fetch-sources.sh` | `bbd06fb5abcc23f9774c292740f53f6dfa6c5614f9b87b54c15a7ff8f448427d` | Fetch all five unchanged tag-pinned source copies concurrently with bounded curl commands; wait and clean child process groups. |
| `/fast/scratch/hyaku/mori-r33/CtlJunkOffTopic/score-controls.py` | `4cbc11f241f50b6127c83d506edfc9ba665df84ea1dcce9877820b8e623fdac2` | Execute the exact two frozen counter commands concurrently, preserve full stdout/stderr and exit codes, and clean isolated subprocess groups. |

Observed scoring-driver invocation:

```sh
timeout --kill-after=5s 600 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE python3 /fast/scratch/hyaku/mori-r33/CtlJunkOffTopic/score-controls.py be0bad2a9a0ffba62585a3ca99e7b8f7e710f40f 5ae82bab403743ac65ff420802b28fd9212e8f5b
```

The driver itself exited 0; the two independently captured counter exits were 1 and 0 as reported above. Each counter was run once. No build, formatter, linter or unrelated test was run. All shell commands were timeout-bounded, network fetches used `curl -sSL --fail -m 60`, and started process groups were waited for/cleaned before return. No long-running service was started.

Two independent read-only advisory audit tasks were requested in one batch; the task tool refused both because spawning is disabled for this agent. No additional runtime was invoked. Tool installs/updates: **none**; no package-manager transaction occurred.
