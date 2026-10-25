# ExecOffHostReplay — off-path replay (round 47, wave w1)

Seat: `ExecOffHostReplay` (leaf). Goal: prove the two frozen counters run from a
read-only clone of the lane, independent of the original path, and record their
outputs at the freeze commit.

## Setup

- Scratch: `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47-ExecOffHostReplay`
  (created; used as `TMPDIR` for all lane-tool runs).
- Read-only clone at
  `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47-ExecOffHostReplay/clone`:

```
git clone --no-hardlinks /home/vgpnk/Projects/shokunin/mori-shokunin <dest>
# -> "Cloning into '<dest>'... done."
```

- Toplevel verified:

```
git -C <clone> rev-parse --show-toplevel
# -> /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47-ExecOffHostReplay/clone
#    (equals <dest>, as required)
```

- Clone HEAD: `63eecf2738db96f46b0bd02b1b2dfd66787493d0`
  ("round-47: freeze — contract P-C1/P-C2, mori-pin-check.py, count-c2.py,
  controls, v7.2 OOM source copies, collision/quarantine scratch"). The clone is
  therefore exactly the committed freeze; no working-tree drift.
- Frozen instrument bytes verified in the clone (sha256 match contract §Frozen
  instrument bytes):
  - `tools/mori-pin-check.py` → `e3ef425abde30974faf53a894f96650af11570d2125a5bf621395f6ab0d903e1`
  - `.ufo/waves/round-47/count-c2.py` → `fc77b93338b3f49b9038eaac3832537b1be2e0ff9dff2476fef750153978901e`

## Runs (all from the clone, `TMPDIR` = scratch)

### 1. `python3 tools/mori-pin-check.py --selftest`

Exit code: `0`. Output (verbatim, full):

```
PASS honest  PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS stale_tally  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=1 unparsed=0 no_command=0 dropped=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS stale_in_cell_true_elsewhere  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=1 unparsed=0 no_command=0 dropped=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS pin_moved_out_of_cell  PIN_CHECK=unmet tally_pins=0 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS digest_ok  PIN_CHECK=met tally_pins=1 digest_pins=1 mismatches=0 unparsed=0 no_command=0 dropped=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS digest_stale  PIN_CHECK=unmet tally_pins=1 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS malformed_row  PIN_CHECK=unmet tally_pins=0 digest_pins=0 mismatches=0 unparsed=1 no_command=0 dropped=0 min_tally_pins=0 rev=deadbeef baseline=no
PASS no_command  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=1 dropped=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS digitless_pin  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=1 no_command=0 dropped=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS timeout  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=1 unparsed=0 no_command=0 dropped=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS bare_flag_rev_entry  PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS escaped_pipe_cell  PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS below_floor  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 min_tally_pins=2 rev=deadbeef baseline=no
PASS mutant_pin_bound_to_mutant  PIN_CHECK=met tally_pins=2 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 min_tally_pins=2 rev=deadbeef baseline=no
PASS mutant_pin_wrong  PIN_CHECK=unmet tally_pins=2 digest_pins=0 mismatches=1 unparsed=0 no_command=0 dropped=0 min_tally_pins=2 rev=deadbeef baseline=no
PASS tmpdir_inside_measured_tree  PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS token_boundary_truncated_pin  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=1 unparsed=0 no_command=0 dropped=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS baseline_row_deleted  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=1 min_tally_pins=1 rev=deadbeef baseline=yes
PASS baseline_all_present  PIN_CHECK=met tally_pins=2 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 min_tally_pins=1 rev=deadbeef baseline=yes
PASS nonzero_rc_with_fail0  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=1 unparsed=0 no_command=0 dropped=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS cli_met_rc0  rc=0
PASS cli_bad_rev_rc2  rc=2
PIN_CHECK_SELFTEST pass=22 fail=0
exit=0
```

Wall time: 5.22 s. Selftest fixture-based (`rev=deadbeef`, `baseline=no|yes`); no
repo path needed.

### 2. `python3 .ufo/waves/round-47/count-c2.py --selftest`

Exit code: `0`. Output (verbatim, full):

```
PASS honest  C2=met events=2 rows=2 name_mismatch=0 field_mismatch=0 callsite_mismatch=0 pin_mismatch=0 source_row=ok provenance=ok rev=fixture
PASS missing_event_three_of_eight_class  C2=unmet events=2 rows=1 name_mismatch=1 field_mismatch=0 callsite_mismatch=0 pin_mismatch=0 source_row=ok provenance=ok rev=fixture failed=name_mismatch
PASS invented_event  C2=unmet events=2 rows=3 name_mismatch=1 field_mismatch=0 callsite_mismatch=0 pin_mismatch=0 source_row=ok provenance=ok rev=fixture failed=name_mismatch
PASS missing_field  C2=unmet events=2 rows=2 name_mismatch=0 field_mismatch=1 callsite_mismatch=0 pin_mismatch=0 source_row=ok provenance=ok rev=fixture failed=field_mismatch
PASS wrong_callsite  C2=unmet events=2 rows=2 name_mismatch=0 field_mismatch=0 callsite_mismatch=1 pin_mismatch=0 source_row=ok provenance=ok rev=fixture failed=callsite_mismatch
PASS pin_tamper  C2=unmet events=2 rows=2 name_mismatch=0 field_mismatch=0 callsite_mismatch=0 pin_mismatch=1 source_row=ok provenance=ok rev=fixture failed=pins
PASS no_source_row  C2=unmet events=2 rows=2 name_mismatch=0 field_mismatch=0 callsite_mismatch=0 pin_mismatch=0 source_row=bad provenance=ok rev=fixture failed=source_row
PASS no_provenance  C2=unmet events=2 rows=2 name_mismatch=0 field_mismatch=0 callsite_mismatch=0 pin_mismatch=0 source_row=ok provenance=bad rev=fixture failed=provenance
PASS no_table  C2=unmet events=2 rows=0 name_mismatch=0 field_mismatch=0 callsite_mismatch=0 pin_mismatch=0 source_row=ok provenance=ok rev=fixture failed=table
PASS duplicate_row  C2=unmet events=2 rows=3 name_mismatch=1 field_mismatch=0 callsite_mismatch=0 pin_mismatch=0 source_row=ok provenance=ok rev=fixture failed=name_mismatch
PASS entry_absent_do_nothing  C2=unmet events=2 rows=0 name_mismatch=0 field_mismatch=0 callsite_mismatch=0 pin_mismatch=0 source_row=ok provenance=bad rev=fixture failed=entry_absent
PASS source_row_queued  C2=unmet events=2 rows=2 name_mismatch=0 field_mismatch=0 callsite_mismatch=0 pin_mismatch=0 source_row=bad provenance=ok rev=fixture failed=source_row
PASS cli_not_a_repo_rc2  rc=2
C2_SELFTEST pass=13 fail=0
exit=0
```

Fixture-based; no repo path needed.

### 3. `python3 .ufo/waves/round-47/count-c2.py 63eecf2738db96f46b0bd02b1b2dfd66787493d0 --repo <clone>`

Exit code: `1`. Output (verbatim):

```
C2=unmet events=8 rows=0 name_mismatch=0 field_mismatch=0 callsite_mismatch=0 pin_mismatch=0 source_row=bad provenance=bad rev=63eecf2738db96f46b0bd02b1b2dfd66787493d0 failed=entry_absent,source_row
```

Counter reads the committed v7.2 OOM copies (`events=8` — all eight TRACE_EVENTs
parsed) and reports the pre-build state at the freeze commit: the catalogue entry
does not exist at freeze (`entry_absent`) and there is no S475 source row yet
(`source_row`). This matches the contract's "before" shape (freeze commit has the
source copies but not the entry).

## Path-dependence check

- `grep` for `/home/vgpnk` in `tools/mori-pin-check.py`: **no matches**.
- `grep` for `/home/vgpnk` in `.ufo/waves/round-47/count-c2.py`: **no matches**.
- Widened `grep` for `mori-shokunin|/Projects/|/home/|shokunin` in both: **no
  matches**.

Neither instrument references the original lane path (not even a substring).
`count-c2.py` takes the repo via `--repo` (or defaults to its own working tree,
`git -C`-style); `mori-pin-check.py` runs against its own working tree; selftests
are self-contained fixtures. **Conclusion: neither instrument depends on the
original path** — off-path replay is valid.

## Tooling / hygiene

- No tools installed or upgraded (none needed; `python3` already present).
- No mutation of the fleet repo, lane git/jj state, or host; only read-only git
  ops (`clone`, `rev-parse`, `log`, `cat-file`) plus the scratch tree.
- `/home/vgpnk/Projects/shokuknow` untouched.
- Evidence above is observed output (command + output + exit code); nothing
  inferred.

## Risks / notes

- `count-c2.py 63eecf… --repo <clone>` exit code is 1 (unmet) — expected at the
  freeze commit; the verdict for the landed tip must come from a post-landing run.
- Selftest runs exercised the committed freeze bytes (sha256 verified).
- Clone is a snapshot; the counter's `--repo` points at the clone, so this run is
  fully off-path.
