# Wave settlement by report presence (C2 knowledge note, round 20) — DRAFT

Status: DRAFT by DraftSettlementNote for L1 integration. Frozen rules come from
`.ufo/waves/round-20/contract.md` (C2) and `.ufo/waves/round-20/frozen/c2-expected.json`.
Final numbers are marked `TODO-L1`. The tool `tools/mori-wave-settlement.py` does not exist
in this lane tree at the time of drafting (`ls tools/mori-wave-settlement.py` → no such file),
so every tool-behaviour statement below is the frozen contract, not observed output.

## 1. What the tool measures

`scan` answers one question: for each dispatch file the lane has written under `.ufo/waves/`,
which of its declared members left a non-empty report file at the path their task named.
It is a filesystem-shape reading. It is not a judgement of whether a seat ran, failed, died,
or produced a good report, and it does not read report bytes.

Inputs (contract C2, Discovery and Members):

- Discovery: every regular `*.json` under `<lane-root>/.ufo/waves/` (recursive, symlinks not
  followed) whose top-level `schema` equals `ufo-swarm-wave-dispatch-v1`. Other parseable JSON
  → `ignored_json`. Unparseable JSON → `unreadable_json`.
- Members: `taskCall.tasks[*]` (`name`, `agent`). `taskCall: null` → wave state `no-spawn`.
- Expected report path: the LAST line of each task matching
  `^Report: write your scoped findings to (\S+)$`. The path must be relative, contain no `..`
  component and resolve inside the lane root; otherwise the member is `unsafe` and never read.
  No trailer → `unparsed`.

Shape of a dispatch file the tool expects (from the frozen fixture note):
`{"schema":"ufo-swarm-wave-dispatch-v1","wave":W,"taskCall":{"context":…,"tasks":[…]}}`.

Live shape on disk, checked read-only with `jq` (not the tool):
`.ufo/waves/round-20/wave1-run.json` has `schema` `ufo-swarm-wave-dispatch-v1`,
`counts.total` 76, `taskCall.tasks` length 76, and every task's last line is a
`Report: write your scoped findings to .ufo/waves/round-20/build/<Name>.md` trailer.
`.ufo/waves/round-19/wave1-run.json` has `counts.total` 64 and 64 tasks, every trailer in the
same form. Both files are in the same schema, so both are in scope for `scan`.

## 2. Member statuses

| status | rule | counted as present? |
|---|---|---|
| `present` | regular, non-symlink file at the lane-root path, size > 0 | yes |
| `empty` | regular, non-symlink file, size 0 | no |
| `missing` | nothing at the lane-root path and no misroot candidate (§5) | no |
| `misrooted` | nothing at the lane-root path, but a regular file exists at the same relative path under `--fleet-root` | no |
| `unsafe` | trailer path absolute, containing `..`, or resolving outside the lane root; never read | no |
| `unparsed` | task has no valid trailer as its last line | no |

Symlinks are never followed (oracle case `symlink-report`: a symlink to a non-empty file
→ `present: 0`). Report bytes are never emitted; output carries statuses and counts only
(oracle case `content-not-emitted`).

## 3. Wave states

| state | rule (contract C2) | oracle case |
|---|---|---|
| `settled` | every member `present` | `all-present` |
| `partial` | ≥1 `present` and ≥1 not present | `one-missing`, `empty-report`, `misrooted`, `no-trailer` |
| `unsettled` | 0 `present` and ≥1 member | `none-present` |
| `no-spawn` | `taskCall: null` (0 members) | `no-spawn` |
| `unavailable` | no member had a parseable safe path | `traversal`, `absolute-path` |

Precedence when cases overlap (`[INFERENCE]`, derived from the wording above; the frozen
oracle does not name a mixed case, so L1 must confirm against the built tool):

1. `taskCall: null` → `no-spawn`.
2. No member with a parseable safe trailer path (all `unsafe` / `unparsed`) → `unavailable`.
3. Otherwise count `present`: all → `settled`; some → `partial`; none → `unsettled`.

Consequence to note: a wave where one member is `unsafe` and the other `missing` is `unsettled`,
not `unavailable`, because one member did have a parseable safe path. `TODO-L1`: confirm.

Two different "settled" words exist in this lane. The census `SURFACE waves` token
(`tools/mori-census.sh:865-931`) calls a directory settled when a settlement-type file exists
(`results.json`, `closeout.json`, `mission-result.json`, `closeout.md`, or a `"closed"`/`"settled"`
true marker). The new tool's `settled` means every dispatched member left a non-empty report.
The two are not comparable, and the note must not present one as the other.

## 4. Exit codes

| tool | exit 0 | exit 1 | exit 2 / 64 |
|---|---|---|---|
| `mori-wave-settlement.py scan` (contract) | every discovered wave `settled` or `no-spawn` | any other state | 2: usage error or unreadable lane root |
| `ufo-swarm-collect.mjs collect` (kumitate, `ufo-fsd-alpha` HEAD `31c465f1`) | success | typed `SwarmCollectError` (`scripts/ufo-swarm-collect.mjs:805`); internal fault also 1 (`:808`) | 64 usage (`:641`, `:805`) |
| `ufo-swarm-wave.mjs` (kumitate, same HEAD) | ok | 1 invalid spec/plan (`scripts/ufo-swarm-wave.mjs:102`) | 64 usage |
| `mori-misroot-sweep.py` (mori, `RC_*` constants) | 0 clean | 1 candidate | 2 setup |

Collision warning: in kumitate's tools, exit 1 is an error. In mori's `scan`, exit 1 means
"not every wave settled" and is a successful observation. A pipeline that treats `$? != 0` as
failure will misread a healthy-but-incomplete scan as a crash. Read the JSON state, not only
the exit code.

Exit 0 does not mean every report is complete or readable. Oracle case `malformed-dispatch`
expects exit 0 with `unreadable_json: 1`: an unreadable dispatch file is counted, not
escalated. Any non-zero `unreadable_json` must be read alongside the exit code.

## 5. Why missing is not dead, and why present is not complete

Missing is not dead. The tool's output never uses `dead`, `failed` or `killed`
(oracle case `deterministic`, `no_vocab`). The frozen reason is that a report missing on disk
can have many causes that the filesystem cannot separate.

The round-19 closure is the evidence. `MANIFEST.json:10171` (fleet root) records for W1:
`64 returned IDs, 16 reports, 8 known provider failures, 1 cancellation, 39 unknown no-report
causes (not successful reviews/deaths inferred)`. That is 8 + 1 + 39 = 48 non-reports: 8 with a
known provider failure, 1 with a cancellation, and 39 with no recorded cause. The closure itself
declined to call them deaths.

Manual shell reproduction, same rule as `scan` (`TODO-L1`: replace with the tool's output):
`.ufo/waves/round-19/wave1-run.json` → 64 members, `present_nonempty` 16, `empty` 0,
`missing` 48, `misrooted_candidates` 0, start-stub-only 0. This matches the MANIFEST figures
(16 reports, 48 without). The scan reproduces the count; it does not explain the 48.

Present is not complete. The `present` rule is size > 0. A report that a seat began and never
finished still passes it. At the time of drafting, round-20 `wave1-run.json` (76 members, 76
trailer paths, all of them under `.ufo/waves/round-20/build/`) had 76 non-empty files by that rule.
Of those, 57 had size ≤ 32 bytes and began with the line `STATUS: started`, which is the
first-tool-call stub each seat writes before its work. So 57 of 76 would count `present` while
holding no findings. This is a counting observation at one instant, not a stable figure.

Caveat for L1 (decision, not changed here): the frozen contract's `present` admits start stubs.
Either (a) the tool keeps the size>0 rule and the note says `present` means "file exists and is
non-empty", or (b) the tool adds a `started`-only sub-status (first line `STATUS: started` and
size below a fixed bound). Option (b) reads report content, which C2 currently forbids for
output but not for classification. `TODO-L1`: decide, and record the choice in the C2 expected
file before the after-run.

## 6. Misrooted detection

A seat told to write `.ufo/waves/round-N/build/<Name>.md` under the lane root sometimes writes
the same relative path under the fleet root (`/home/vgpnk/Projects/shokunin`). The contract
classifies that as `misrooted`: not present, but reported separately so it cannot be mistaken
for a missing report with no output at all.

Precedent in this fleet: `mori-misroot-sweep.py` documents a round-16 seat report written at
the fleet root (`MoriR16.Lesson`), later relocated to `.ufo/waves/hyaku/misroots/`. That tool
uses a different query (`git status` over the fleet root with no pathspec, untracked files,
name-based candidates). `scan` uses the report path the dispatch named.

Limits, to be carried into the output doc:
- A fleet-root file at the same relative path is a lead, not proof that it is this seat's report.
  The fleet root also holds fleet-level `.ufo/waves/*` directories. The tool checks existence only;
  it must not open the file for ownership.
- `misrooted` never moves, copies or deletes. Relocation is operator/L1 work.
- The manual pass above found 0 misroot candidates for round-19 W1 and 0 for round-20 W1
  (every round-20 trailer resolved in the lane root). `TODO-L1`: tool-run counts.

## 7. Undispatched-file caveat

A dispatch file on disk records what was planned, not what was sent. The tool reads the file,
so a wave whose dispatch was never sent looks the same as a wave whose seats went silent:
members `missing`, state `unsettled`.

Observed in this lane:
- `.ufo/waves/round-20/wave1-run.json`: `registry.members.*.agentId` is `null` for all 76
  members (checked with jq). A null agentId means the registry holds no spawn handle. It is
  not evidence that any seat ran.
- Dispatch receipt: `.ufo/waves/round-20/wave1-dispatch-receipt.json` (schema
  `mori-r20-dispatch-receipt-v1`) records a single task call, a `taskcall_sha256` and 76
  returned IDs. That receipt, not the dispatch file, is the evidence that the call happened.
- Round-18 `tools/mori-dispatch-ledger.py` binds each attempt to a payload digest, and states
  its own limit: it "cannot prove that an unlogged attempt never happened"
  (`corpus/knowledge/dispatch-ledger-r18.md`, Limits).

Rule for readers: an `unsettled` or `partial` wave with no dispatch receipt or ledger row
means dispatch is unverified. It does not mean seats were silent. Pair `scan` output with the
receipt before drawing a conclusion. The tool's output should say so in its limits, not
imply dispatch.

Coverage note: the census `SURFACE waves` loop skips children named `round-*`
(`tools/mori-census.sh:876-879`), so round-N wave files like `.ufo/waves/round-20/wave1-run.json`
are invisible to the census waves surface. The new tool recurses and will see them. This is
why the two surfaces can disagree about the same lane.

## 8. FR3 boundary with kumitate

Frontier FR3 (`corpus/README.md:334`): "Authoritative wave settlement and emptied-by-hygiene
versus never-written". Its boundary text: "Mori reports filesystem shape; kumitate owns
orchestration/result semantics; `empty` alone does not prove never-written, and receipt review
stays offline."

What C2 advances, and what it does not:

- Advances: a per-seat, read-only count of which dispatched members left a non-empty report
  at the path their own task named. This is filesystem shape. It is capability acquisition
  for mori, not settlement authority.
- Does not advance: authoritative settlement. Kumitate's contract is that settlement is the
  `collect` join of dispatch members to a results file (`ufo-swarm-collect.mjs collect`), with
  unmapped and unexpected members refused (`unmapped_member`, `unexpected_member`; collect
  source at `scripts/ufo-swarm-collect.mjs:549-555`). Kumitate's own note says there is no
  `settle` CLI verb (`swarm-wave-lifecycle.md:28-36`). The live `ufo-swarm-wave.mjs` contains no
  `settle` token (grep at `31c465f1`, empty result), so mori must never advise running `settle`.
- Does not advance: emptied-by-hygiene versus never-written. `scan` returns `missing` for both;
  the difference needs souji's receipts, which mori reads offline only. A `missing` output is
  not evidence of "never written" and not evidence of "removed by cleanup".
- Routing: when `scan` shows `unsettled` or `partial`, the owner of result semantics is
  kumitate (run collect with its results input). Mori reports the count and stops there.
  Mori never runs collect, never writes a results file, never edits a registry.

Anchor caveat: `swarm-wave-lifecycle.md` carries a round-35 fidelity notice that 24 of its line
anchors no longer land on their claims at `31c465f1`. Cite the file, and re-check line
numbers before using them as proof (`TODO-L1`).

## 9. Oracle map (14 cases, `frozen/c2-expected.json`)

| case | rule exercised |
|---|---|
| all-present | §3 `settled`, exit 0 |
| one-missing | §3 `partial`, `missing_names` sorted |
| none-present | §3 `unsettled`, exit 1 |
| empty-report | §2 `empty` is not present |
| misrooted | §2 `misrooted` is not present |
| malformed-dispatch | §4 `unreadable_json` counted, exit 0 |
| no-trailer | §2 `unparsed` |
| traversal | §2 `unsafe`, §3 `unavailable` |
| absolute-path | §2 `unsafe`, §3 `unavailable` |
| symlink-report | symlinks not followed |
| other-schema-ignored | §1 `ignored_json` |
| no-spawn | §3 `no-spawn`, exit 0 |
| content-not-emitted | §5 no report bytes in output |
| deterministic | byte-identical output, waves sorted, no `dead`/`failed`/`killed` |

Counts for the L1 integration (all `TODO-L1`): C2 `before` `capability_absent` 14; `after`
`matched` 14 (`jq '.counts.matched'`); live round-19 W1 scan expected to reproduce
`reports_present = 16` of 64; fleet-wide totals to be recorded from the run.

## 10. Limits

- Presence is a size check and a path check. It is not report validity, completeness or
  quality (§5).
- The tool reads only the dispatch files it finds. A dispatch that was never written to
  `.ufo/waves/` is invisible to it (§7).
- A lane tree that has been moved or re-rooted changes the result. `--fleet-root` is needed to
  see misroots.
- Reports deleted or moved after settlement will flip a wave back to `partial` on the next
  scan. The output records the point in time only.
- The tool does not check that a report's round or lane matches its name.
