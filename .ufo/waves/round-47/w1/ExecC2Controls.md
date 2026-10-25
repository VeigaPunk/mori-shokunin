# ExecC2Controls — w1 C2 control re-runs (round 47)

Seat: ExecC2Controls (fleet wave w1, mori-shokunin lane). Skill: godspeed.
Scoped assignment: re-run the C2 counter at the freeze commit `63eecf2738db96f46b0bd02b1b2dfd66787493d0`
(do-nothing, staged control, three control, `--selftest`), compare with the
at-freeze receipts, and verify the four sha256 pins in `count-c2.py` against the
committed freeze blobs. All runs used `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47-ExecC2Controls`
(created). No tools installed (none needed; rule RULES.md).
No host/lane state touched; read-only `git show`/`rev-parse` only.

## Instrument integrity

- Working-tree `count-c2.py` sha256 = `fc77b93338b3f49b9038eaac3832537b1be2e0ff9dff2476fef750153978901e` — matches frozen instrument hash in contract.md, so the working-tree bytes are the frozen bytes (measurement at measured revision).
- Freeze commit resolves: `git rev-parse --verify 63eecf2738db96f46b0bd02b1b2dfd66787493d0^{commit}` → `63eecf2738db96f46b0bd02b1b2dfd66787493d0` (rc=0).

## C2 re-runs at freeze commit 63eecf (each: command, output, rc)

### 1. Do-nothing (P-C2 at freeze, no entry)
```
$ TMPDIR=… python3 .ufo/waves/round-47/count-c2.py 63eecf2738db96f46b0bd02b1b2dfd66787493d0
C2=unmet events=8 rows=0 name_mismatch=0 field_mismatch=0 callsite_mismatch=0 pin_mismatch=0 source_row=bad provenance=bad rev=63eecf2738db96f46b0bd02b1b2dfd66787493d0 failed=entry_absent,source_row
rc=1
```
Matches `evidence/control-c2-donothing-at-freeze.txt` byte-for-byte (same line, rc=1).
Control stays unmet as required by the frozen contract.

### 2. Staged control (`--entry controls/control-c2-staged.md`)
```
$ TMPDIR=… python3 .ufo/waves/round-47/count-c2.py 63eecf2738db96f46b0bd02b1b2dfd66787493d0 --entry .ufo/waves/round-47/controls/control-c2-staged.md
C2=unmet events=8 rows=0 name_mismatch=0 field_mismatch=0 callsite_mismatch=0 pin_mismatch=0 source_row=bad provenance=bad rev=63eecf2738db96f46b0bd02b1b2dfd66787493d0 failed=provenance,source_row,table
rc=1
```
Matches `evidence/control-c2-staged-at-freeze.txt` byte-for-byte (rc=1). The
staged entry (byte-exact, no catalogue table) stays unmet — its "exactly three
named tracepoints" claim is falsified by `events=8`.

### 3. Three control (`--entry controls/control-c2-three.md`)
```
$ TMPDIR=… python3 .ufo/waves/round-47/count-c2.py 63eecf2738db96f46b0bd02b1b2dfd66787493d0 --entry .ufo/waves/round-47/controls/control-c2-three.md
C2=unmet events=8 rows=3 name_mismatch=5 field_mismatch=0 callsite_mismatch=0 pin_mismatch=0 source_row=bad provenance=ok rev=63eecf2738db96f46b0bd02b1b2dfd66787493d0 failed=name_mismatch,source_row
rc=1
```
Matches `evidence/control-c2-three-at-freeze.txt` byte-for-byte (rc=1). Three-row
"staged claim as a table" stays unmet: 8 events committed, 3 rows seen →
`name_mismatch=5`; the "exactly three" claim is falsified.

### 4. Selftest
```
$ TMPDIR=… python3 .ufo/waves/round-47/count-c2.py --selftest
PASS honest …
PASS missing_event_three_of_eight_class …
PASS invented_event …
PASS missing_field …
PASS wrong_callsite …
PASS pin_tamper …
PASS no_source_row …
PASS no_provenance …
PASS no_table …
PASS duplicate_row …
PASS entry_absent_do_nothing …
PASS source_row_queued …
PASS cli_not_a_repo_rc2  rc=2
C2_SELFTEST pass=13 fail=0
rc=0
```
Matches `evidence/selftest-c2.txt` (13 PASS lines, `pass=13 fail=0`, rc=0).

## Pin verification (4 sha256 pins in count-c2.py `PINS` vs committed freeze blobs)

`git -C <lane> show 63eecf…:corpus/evidence/sources-r47/<file> | sha256sum`:

| file | pin in count-c2.py | committed blob sha256 | match |
|---|---|---|---|
| `include_trace_events_oom.h` | `82f04ad4108ba9499b638fe298967f124269c0a2feb6ddbb14b1ade59c974e0d` | `82f04ad4108ba9499b638fe298967f124269c0a2feb6ddbb14b1ade59c974e0d` | YES |
| `mm_oom_kill.c` | `452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e` | `452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e` | YES |
| `mm_page_alloc.c` | `439ae8ec1e47cbf38770865e53e98bf2229e32a20c4b0f8178e6f19f34edbc50` | `439ae8ec1e47cbf38770865e53e98bf2229e32a20c4b0f8178e6f19f34edbc50` | YES |
| `fs_proc_base.c` | `cef1a2cf3f34f683e69d623c4df563d5c0dc6bd71dcb3d42f40dadb0084915c6` | `cef1a2cf3f34f683e69d623c4df563d5c0dc6bd71dcb3d42f40dadb0084915c6` | YES |

All four pins match (`pin_mismatch=0` in every run above is consistent).

## Findings

- All three controls stay **unmet** at the freeze commit, exactly as the frozen
  contract requires; each re-run matches its at-freeze receipt byte-for-byte.
  The failure isolates to the entry (do-nothing: `entry_absent,source_row`;
  staged: `provenance,source_row,table`; three: `name_mismatch,source_row`).
- The staged entry's "exactly three named tracepoints" claim is falsified: the
  committed Linux v7.2 `include/trace/events/oom.h` copy defines `events=8`
  TRACE_EVENTs.
- Counter selftest passes 13/13 and matches the committed receipt.
- The four frozen pins all reproduce from the committed freeze blobs.

## Risks / notes

- Evidence is `git show <freeze>`-based (the counter's own `git_reader`); all
  runs were at the freeze commit. Entering-revision receipts
  (`evidence/control-c2-*.txt`, rev `2d85e33`) show `events=0 pin_mismatch=4`
  because the sources-r47 copies were not committed at entering — expected, not
  a regression.
- No host reads, no tracing, no lane/lane-repo mutations performed. UNVERIFIED:
  nothing (all assignment checks ran).

Report: `.ufo/waves/round-47/w1/ExecC2Controls.md`
