# PackExactAnchor — round-16 advisory report

## Files changed

- `.ufo/waves/round-16/fixtures/ExactAnchor.json` (new): 4 shared-schema cases.

## Scope delivered

Topic: retained anchor alone and anchor followed by benign record — the rc0
exact-continuity baseline for `tools/mori-journal-window.py`. Every case is a
success (the pack's topic-specific success set); every case pins
`want_rc=0`, `want_id=MORI_JOURNAL_WINDOW_OK`, and `want` selects
`records_after_anchor`, all four `positive_*` counters (all 0), and
`evidence_basis=validated-record-subsets`.

| id | scope | stream | want |
|---|---|---|---|
| `anchor-only-user-empty-window` | user | anchor record only (MESSAGE_ID = kernel-OOM id as a drop-detector canary) | `records_after_anchor=0`, all positives 0 |
| `anchor-then-one-benign-user` | user | anchor + benign coredump-notice record | `records_after_anchor=1`, all positives 0 |
| `anchor-realistic-cursor-then-benign-unit-result-system` | system | realistic journalctl cursor shape (`s=…;i=…;b=<boot>;m=…;t=…;x=…`) + benign unit-failure record with `UNIT_RESULT="resources"` (exact catalog id, non-positive result) | `records_after_anchor=1`, all positives 0 |
| `anchor-then-two-benign-ordered-system` | system | anchor + two benign records (oomd-notice, coredump-notice), unique cursors, ordered | `records_after_anchor=2`, all positives 0 |

## Source bytes verified before writing

- Catalog ids byte-read at `tools/mori-census.sh:1032-1036` (grep output):
  `JOURNAL_ID_KERNEL_OOM=fe6faa94e7774663a0da52717891d8ef`,
  `JOURNAL_ID_OOMD=d989611b15e44c9dbf31e3c81256e4ed`,
  `JOURNAL_ID_COREDUMP=fc2e22bc6ee647b6b90729ab34a250b1`,
  `JOURNAL_ID_UNIT_SIGKILL=98e322203f7a4ed290d09fe03c09fe15`,
  `JOURNAL_ID_UNIT_FAILURE=d9b373ed55a64feb8242e02dbe79a49c`.
- r15 predicates read at `corpus/knowledge/journal-positive-evidence-r15.md:106-113`:
  kernel-OOM positive = identity only; unit positives require exact string
  `oom-kill` / `signal`; process SIGKILL requires `killed` + scalar `9`. All
  benign records satisfy no predicate (`resources` is neither unit-positive
  vocabulary value; coredump/oomd notice ids match no positive predicate).
- **Correction noted for the wave:** the `PackUnitOom` dispatch prompt prints a
  wrong unit-failure id (`d9b373ed55a64e6c8e2e7d70a0fce472`). The census source
  constant `d9b373ed55a64feb8242e02dbe79a49c` is authority; my pack uses it.

## Design notes

- Anchor record carries the kernel-OOM catalog id in 3 of 4 cases: it is the
  exact-continuity canary — a producer that fails to drop the anchor record
  would report `positive_kernel_oom=1`, and the pack fails loudly.
- Self-check performed at write time (structural only, no tool run): first
  JSONL record's `__CURSOR`/`_BOOT_ID` exactly match the anchor in all 4 cases;
  all later records are objects, same boot, unique scalar cursors; no record
  satisfies any positive predicate; `records_after_anchor` equals
  post-anchor line count. JSONL strings produced by `json.dumps` — exact
  escaping guaranteed; no `MESSAGE` field present in any record.
- No timeout/overflow/negative arms: those topics are assigned to
  PackBounds / PackMissingAnchor / PackBootBoundary / PackCursorShape /
  PackProducerFailure / PackStderr — no overlap introduced.

## Risks / blockers

- None blocking. `want.evidence_basis` assumes the harness compares `want` keys
  against the tool's stdout object; if `want` is restricted to numeric fields,
  that one key can be dropped without weakening the pack.
- No runs executed (per contract); harness `tools/mori-round16-regressions.py`
  and tool `tools/mori-journal-window.py` do not exist yet — normal for the
  baseline stage (`capability_absent`).

## Tooling

- No installs. `python3` (host, already present) used only to emit the pack
  with exact JSON escaping.
