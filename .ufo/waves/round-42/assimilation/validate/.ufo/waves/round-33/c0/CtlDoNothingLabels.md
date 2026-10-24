All six negative controls printed `C1=unmet` and exited 1; none printed `C1=met`.

# CtlDoNothingLabels — P-C1 adversarial controls

## Axes and containment

- **Depth:** a plausible diskstats table must not count as the claimed new, supported knowledge merely because its shape is right.
- **Calibration:** Round33 labels and high-numbered source ids must not substitute for source novelty or an independent R-J receipt.
- **Freshness:** genuinely fetched copies of already-registered URLs must remain distinguishable from new sources.
- **Operability:** only the required visible decision table should satisfy the table requirement; exact committed-revision receipts must be reproducible.

These are review concerns, not claimed axis moves or an admission decision. No judge was invoked or impersonated. No lane/fleet git or jj writes were performed. The only lane write is this report; all synthetic commits are in `/fast/scratch/hyaku/mori-r33/CtlDoNothingLabels/repo`.

Read in full before construction: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/contract.md` and `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py`, including P-C1 and R-J. The frozen counter was not edited. Its observed SHA-256 is `7361f3e31f4a88afc7a50a907d9c2d5b66ca98306a633760ecc40ca53fa3d942`; the contract's is `6edaf25fb830522d029479f88901e72497161c249afa8ddb58d73459766d273a`.

All shell commands were timeout-capped at at most 600 seconds. Git commands ran with GIT_DIR, GIT_WORK_TREE, and GIT_INDEX_FILE unset. All launched jobs returned; the scoring runner additionally kills its subprocess group in a finally block. No installations or tool updates were needed.

## Summary

Every row below uses sandbox clone `/fast/scratch/hyaku/mori-r33/CtlDoNothingLabels/repo`.

| Control | Commit | Printed unmet_conditions | Result |
|---|---|---|---|
| Entering tip, unchanged | `7d382043016e8854e3be2ee523a095b409c3d8a1` | Not emitted: early return at `entry=absent` | `C1=unmet`, exit 1 |
| Freeze, unchanged | `27969134d51ea15982db4f36c77e2decd2a22b07` | Not emitted: early return at `entry=absent` | `C1=unmet`, exit 1 |
| Sourceless table | `fee620cb24517fece510c52195df2f6b640a957e` | `new_ids,sources,judge` | `C1=unmet`, exit 1 |
| Relabel shortcut | `7b646aaebc5cc5e1e767a2cf5cd32c0e129492a2` | `new_ids,sources,quote_overlap,judge` | `C1=unmet`, exit 1 |
| Fenced table | `bcf9f45a0c46ab8ff8783641bc16f9e59c67dd6b` | `decision_table_count,rows,new_ids,sources,judge` | `C1=unmet`, exit 1 |
| HTML-commented table | `01af423b178bff54f86fc55cfc7d7f379e5a65da` | `html_comment,new_ids,sources,judge` | `C1=unmet`, exit 1 |

The synthetic chain starts at the freeze, then sourceless → fenced → commented → relabel. The relabel commit removes the comment wrapper. Counters measured each named immutable commit, not the current worktree. Full counter stdout follows; stderr was empty for every control. The runner's successful wrapper exit is not the counter's exit code: the counter exited 1 in every case.

## 1. Do nothing — entering tip

What: the entering tip as committed, with no synthetic changes.

Sandbox: `/fast/scratch/hyaku/mori-r33/CtlDoNothingLabels/repo`.
Commit: `7d382043016e8854e3be2ee523a095b409c3d8a1`.
Receipt: `/fast/scratch/hyaku/mori-r33/CtlDoNothingLabels/entering.json`.

Exact counter command:

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py 7d382043 --repo /fast/scratch/hyaku/mori-r33/CtlDoNothingLabels/repo
```

Full stdout:

```text
rev=7d382043016e8854e3be2ee523a095b409c3d8a1 repo=/fast/scratch/hyaku/mori-r33/CtlDoNothingLabels/repo
entry=absent
C1=unmet
```

Exit code: **1**. Printed `C1=unmet`: **yes**. No `unmet_conditions` line is emitted on this early-return path; the observed failure is the absent entry, not an invented condition label.

## 2. Do nothing — freeze

What: the frozen contract/counter revision as committed, with no synthetic changes at that revision.

Sandbox: `/fast/scratch/hyaku/mori-r33/CtlDoNothingLabels/repo`.
Commit: `27969134d51ea15982db4f36c77e2decd2a22b07`.
Receipt: `/fast/scratch/hyaku/mori-r33/CtlDoNothingLabels/freeze.json`.

Exact counter command:

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py 27969134 --repo /fast/scratch/hyaku/mori-r33/CtlDoNothingLabels/repo
```

Full stdout:

```text
rev=27969134d51ea15982db4f36c77e2decd2a22b07 repo=/fast/scratch/hyaku/mori-r33/CtlDoNothingLabels/repo
entry=absent
C1=unmet
```

Exit code: **1**. Printed `C1=unmet`: **yes**. Again, `unmet_conditions` is not emitted because the entry is absent.

## 3. Sourceless table

What: added `/fast/scratch/hyaku/mori-r33/CtlDoNothingLabels/repo/corpus/knowledge/disk-write-rate-r33.md` with source:, verified-at:, and recheck: lines and one visible observation/reading/verdict/sources table. Its 12 distinct plausible diskstats cases cover interval arithmetic, missing/zero intervals, reset/wrap, 512-byte sectors, device identity, partition and stacked-device overlap, zero deltas, completion accounting, versioned field layouts, and pressure versus throughput. Every citation is an entering-tip id: S033, S001, or S090. No new source ids or Gate rows were added. Four distinct qualifying Round33/entry-path lines were added to `/fast/scratch/hyaku/mori-r33/CtlDoNothingLabels/repo/SKILL.md`. No judge artifacts were added.

Sandbox: `/fast/scratch/hyaku/mori-r33/CtlDoNothingLabels/repo`.
Commit: `fee620cb24517fece510c52195df2f6b640a957e`.
Receipt: `/fast/scratch/hyaku/mori-r33/CtlDoNothingLabels/sourceless.json`.

Exact counter command:

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py fee620c --repo /fast/scratch/hyaku/mori-r33/CtlDoNothingLabels/repo
```

Full stdout:

```text
rev=fee620cb24517fece510c52195df2f6b640a957e repo=/fast/scratch/hyaku/mori-r33/CtlDoNothingLabels/repo
entry=present entry_sha256=1dfc257e85d0291d697bacaa290b9eb1dd1b50e9326241685ffd6e807eee1aa1 head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=12 rows_ok=12 distinct_rows=12 short_readings=0
new_id_rows=0 new_ids=0 ()
gates_ok=0/0 copies_ok=0/0 fetch_ok=0/0 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=no judge=absent
skill_rows=4
unmet_conditions=new_ids,sources,judge
C1=unmet
```

Exit code: **1**. Printed `C1=unmet`: **yes**. Shape, row count, reading length, citation existence, and skill links pass their printed checks; they do not overcome absent new-source support and judge evidence.

## 4. Relabel shortcut

What: restored the same visible 12-row table and four skill links, but cycled its citations through S180–S182. Renamed three already-existing mined registry rows in place, copying every non-id cell unchanged: **S001→S180**, **S090→S181**, **S092→S182**. Thus the registry ids change, not the source identities or URLs. The old references elsewhere in this intentionally synthetic clone are not migrated. Added one admit Gate row per relabeled id and actual upstream copies under `/fast/scratch/hyaku/mori-r33/CtlDoNothingLabels/repo/corpus/evidence/sources-r33/`. The Gate includes distinct copy hashes and located quotes of 13, 13, and 24 words. No judge artifacts were fabricated.

Sandbox: `/fast/scratch/hyaku/mori-r33/CtlDoNothingLabels/repo`.
Commit: `7b646aaebc5cc5e1e767a2cf5cd32c0e129492a2`.
Receipt: `/fast/scratch/hyaku/mori-r33/CtlDoNothingLabels/relabel.json`.

Exact counter command:

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py 7b646aa --repo /fast/scratch/hyaku/mori-r33/CtlDoNothingLabels/repo
```

Full stdout:

```text
rev=7b646aaebc5cc5e1e767a2cf5cd32c0e129492a2 repo=/fast/scratch/hyaku/mori-r33/CtlDoNothingLabels/repo
entry=present entry_sha256=69a54aa00794d01d99a44c916a6d1f4d463566b32a173b8a35a2a3f11a3a6bdc head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=12 rows_ok=12 distinct_rows=12 short_readings=0
new_id_rows=12 new_ids=3 (S180,S181,S182)
S180 gate=bad url_registered_at_entering_tip
S181 gate=bad url_registered_at_entering_tip
S182 gate=bad url_registered_at_entering_tip
gates_ok=0/3 copies_ok=0/3 fetch_ok=0/3 distinct_sources=yes
rows_without_quote_overlap=12 [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
dispatch_rule=no judge=absent
skill_rows=4
unmet_conditions=new_ids,sources,quote_overlap,judge
C1=unmet
```

Exit code: **1**. Printed `C1=unmet`: **yes**. All three relabeled ids are explicitly rejected for URLs registered at the entering tip. Three ids also remain below the frozen five-id minimum. The counter skips copy checking, live fetching, and quote-word collection after a bad Gate; therefore its `copies_ok=0/3`, `fetch_ok=0/3`, and 12 overlap failures are not evidence that the downloaded bytes were counterfeit or that it actually performed three measurement-time fetches.

### Real-source capture receipts

These commands were executed individually in concurrent timeout-bounded calls; all completed successfully with empty stdout. The exact retained fetch recipe is also available in `/fast/scratch/hyaku/mori-r33/CtlDoNothingLabels/fetch_copies.sh` (recorded recipe, not separately re-executed).

```sh
timeout 70 curl -sSL --fail -m 60 --output /fast/scratch/hyaku/mori-r33/CtlDoNothingLabels/repo/corpus/evidence/sources-r33/S180.src https://docs.kernel.org/accounting/psi.html
timeout 70 curl -sSL --fail -m 60 --output /fast/scratch/hyaku/mori-r33/CtlDoNothingLabels/repo/corpus/evidence/sources-r33/S181.src https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst
timeout 70 curl -sSL --fail -m 60 --output /fast/scratch/hyaku/mori-r33/CtlDoNothingLabels/repo/corpus/evidence/sources-r33/S182.src https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/cgroup-v2.rst
```

Observed SHA-256 output from `timeout 60 sha256sum` over those three files:

```text
f752c8d5447760a315048037eb8f53007f8e4862d58617264f587cccd8798258  /fast/scratch/hyaku/mori-r33/CtlDoNothingLabels/repo/corpus/evidence/sources-r33/S180.src
11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692  /fast/scratch/hyaku/mori-r33/CtlDoNothingLabels/repo/corpus/evidence/sources-r33/S181.src
a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad  /fast/scratch/hyaku/mori-r33/CtlDoNothingLabels/repo/corpus/evidence/sources-r33/S182.src
```

The copies are committed at the relabel revision above. Entering-tip source registration can be reproduced without any worktree changes:

```sh
timeout 600 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mori-r33/CtlDoNothingLabels/repo show 7d382043016e8854e3be2ee523a095b409c3d8a1:corpus/SOURCES.md
```

That command was executed; its S001, S090, and S092 rows carry the same three URLs, all with status mined. This avoids the separate queued-status failure that copying S033 unchanged would have introduced.

## 5. Fenced table

What: the sourceless table, byte-for-byte between its wrapper lines, enclosed in a Markdown code fence. Metadata and all four skill lines remain outside the fence. No new sources or Gate rows.

Sandbox: `/fast/scratch/hyaku/mori-r33/CtlDoNothingLabels/repo`.
Commit: `bcf9f45a0c46ab8ff8783641bc16f9e59c67dd6b`.
Receipt: `/fast/scratch/hyaku/mori-r33/CtlDoNothingLabels/fenced.json`.

Exact counter command:

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py bcf9f45 --repo /fast/scratch/hyaku/mori-r33/CtlDoNothingLabels/repo
```

Full stdout:

```text
rev=bcf9f45a0c46ab8ff8783641bc16f9e59c67dd6b repo=/fast/scratch/hyaku/mori-r33/CtlDoNothingLabels/repo
entry=present entry_sha256=99c5570b509e78552a4b887e8526a7cadafdde35a5cd830f85f0bc34e8cd85d8 head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=0
new_id_rows=0 new_ids=0 ()
gates_ok=0/0 copies_ok=0/0 fetch_ok=0/0 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=no judge=absent
skill_rows=4
unmet_conditions=decision_table_count,rows,new_ids,sources,judge
C1=unmet
```

Exit code: **1**. Printed `C1=unmet`: **yes**. The table is recognized syntactically but supplies no unfenced decision table; consequently its rows are not credited.

## 6. HTML-commented table

What: the same sourceless table enclosed in one HTML comment rather than a code fence. Metadata and four skill lines remain outside the comment. No new sources or Gate rows.

Sandbox: `/fast/scratch/hyaku/mori-r33/CtlDoNothingLabels/repo`.
Commit: `01af423b178bff54f86fc55cfc7d7f379e5a65da`.
Receipt: `/fast/scratch/hyaku/mori-r33/CtlDoNothingLabels/commented.json`.

Exact counter command:

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py 01af423 --repo /fast/scratch/hyaku/mori-r33/CtlDoNothingLabels/repo
```

Full stdout:

```text
rev=01af423b178bff54f86fc55cfc7d7f379e5a65da repo=/fast/scratch/hyaku/mori-r33/CtlDoNothingLabels/repo
entry=present entry_sha256=3351b47a21b8c8e67ff86ee6aa835a0ba980dc984341334e1772fe4019859418 head_lines=yes html_comments=1
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=12 rows_ok=12 distinct_rows=12 short_readings=0
new_id_rows=0 new_ids=0 ()
gates_ok=0/0 copies_ok=0/0 fetch_ok=0/0 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=no judge=absent
skill_rows=4
unmet_conditions=html_comment,new_ids,sources,judge
C1=unmet
```

Exit code: **1**. Printed `C1=unmet`: **yes**. The parser still counts the hidden table and its rows, but the separate global `html_comment` condition rejects this entry as the frozen predicate requires.

## Retained scripts

Observed `timeout 60 sha256sum` output:

```text
2b19b8e2d1b033a88625b2732d929058d1994d89ab7ddd525060a1d4e145fdec  /fast/scratch/hyaku/mori-r33/CtlDoNothingLabels/score_control.py
a8a169b8c44fc39d8dce785715e2cf4e7d00dabc33ab7348b2963aa20bae32a2  /fast/scratch/hyaku/mori-r33/CtlDoNothingLabels/fetch_copies.sh
```

The scoring script was exercised once per control with arguments `entering 7d382043`, `freeze 27969134`, `sourceless fee620c`, `fenced bcf9f45`, `commented 01af423`, and `relabel 7b646aa`. It preserves each command, full stdout/stderr, counter exit, timeout status, and printed C1 labels in the corresponding absolute JSON receipt paths named above. No builds, linters, native judges, or unrelated tests were run.

## Counterexample, evidence, impacted axes, smallest safe correction

**Strongest assigned counterexample:** relabeling three real, already-mined sources to S180–S182 while supplying genuine upstream copies, valid-looking Gate rows, a 12-row visible table, and four Round33 skill links. Its receipt explicitly reports `url_registered_at_entering_tip` for every relabeled id and `C1=unmet`. High ids did not manufacture source novelty. The sourceless table independently shows that valid table shape and labels do not suffice. The fence and comment variants were also rejected.

**Impacted axes:** depth and calibration are the main false-positive risks; freshness concerns source identity versus merely refetched bytes, and operability concerns visible content and exact measurement receipts. No axis score or closure verdict is assigned here.

**Smallest safe correction:** none to the frozen counter is justified by these six results. Keep the URL-registration and HTML-comment conditions intact. The reporting correction to avoid is premature saturation: these are combined negative controls, not a single-fault proof of every check. In particular, the relabel control also has only three new ids and no independent judge, while fence/comment controls retain the sourceless/judge failures. Their rejection does not validate R-J semantic judgment, authenticate a future receipt, or establish a no-trade admission. Those decisions remain with the canonical judge and the integration owner.
