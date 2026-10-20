# PackKernelUser — user-scope kernel OOM retained against a wrong-MESSAGE_ID record

Status: COMPLETE. Owned artifact written: `.ufo/waves/round-15/fixtures/KernelUser.json` (4 cases). No production, harness, fleet, sibling, verifier or aggregator file was touched. No census/gate execution, no builds/tests/formatters (L1 verifies once), no installs or upgrades.

## Axes named (godspeed)

- **Coverage (judged)**: does the fixture set actually exercise C1 — a valid user kernel-OOM record surviving an adjacent nonmatching record that invalidates the aggregate class?
- **Non-fabrication (guardrail)**: every case must keep the aggregate raw count unavailable and must not imply completeness, authenticated ids, unique victims, or a numeric-zero total.

Moves kept: four cases whose only difference is the poison shape and multiplicity; each is cheap, none harms the guardrail axis.

## Cases (file content)

All records are objects; every valid record is a scalar matching `MESSAGE_ID` with the current scalar `_BOOT_ID=11111111111111111111111111111111`. No `MESSAGE` field and no canary text anywhere.

| case id | user records | want_oom | want_signal | invalid_class |
|---|---|---|---|---|
| `kernuser_wrong_oomd_id_retains_valid_oom` | valid kernel OOM `fe6faa94…`, then oomd-notice id `d989611b…` (current boot) | true | false | `kernel_oom_notice` |
| `kernuser_two_valid_coredump_id_single_oom` | valid kernel OOM, coredump id `fc2e22bc…`, valid kernel OOM | true | false | `kernel_oom_notice` |
| `kernuser_sigkill_id_without_status_retains_valid_oom` | `98e32220…` record with no `EXIT_CODE`/`EXIT_STATUS`, then valid kernel OOM | true | false | `kernel_oom_notice` |
| `kernuser_missing_message_id_retains_valid_oom` | valid kernel OOM, then object with `_BOOT_ID` only (no `MESSAGE_ID`) | true | false | `kernel_oom_notice` |

Concrete distinctions: case 1 is the minimal wrong-scalar-id adjacency; case 2 raises multiplicity to two independently valid positives and puts the poison between them (one alarm, not two); case 3 uses a record-class id adjacent to the signal path but without the mandatory process fields, proving it is neither OOM nor signal evidence; case 4 drops the field entirely instead of mismatching it. Poison-before-valid ordering in case 3 shows the positive scan is not position-gated (order fanout remains PackOrderMixed's edge; this is only adjacency).

Structural checks performed on the authored file (static only): JSON parses; 4 case objects; exact key set `{id,user,system,want_oom,want_signal,invalid_class}`; booleans are booleans; every `_BOOT_ID` is the 32-hex fixed current boot; every `MESSAGE_ID` is a scalar string; no `MESSAGE` key; ids unique within the pack and no collision with `KernelSystem.json` (the only other pack present when checked).

## Required harness setting (central finding)

`journal_stub_body` (tools/mori-round14-regressions.py:404-580) filters records against the census's exact argv filters in its default `honor` mode (`:518-527`). A wrong-`MESSAGE_ID` record therefore **never reaches the census** in that mode; the kernel aggregate stays valid (`count=1`) and `invalid_class: kernel_oom_notice` can never be observed. The cases would pass `want_oom` for the wrong reason and silently skip C1.

The harness must build these cases with stub mode **`dup-kernel`**: `:511-513` sets `ignore=True` only for the kernel `MESSAGE_ID` query, returning the scope's whole record set (mixed valid + wrong-id) while every other class query stays honor-filtered. Two conditions:

1. Mode is per case, not per pack: choose `dup-kernel` whenever a case carries records intended to be adjacent-but-nonmatching; `honor` otherwise. The pack schema has no mode field, so this mapping must live in `tools/mori-round15-regressions.py`.
2. `dup-kernel` triggers only when the census kernel query still passes an exact `MESSAGE_ID=fe6faa94e7774663a0da52717891d8ef` argv token (r14 shape, tools/mori-census.sh:1219). If the r15 census changes that argv, the stub will honor-filter the poison away.

`ignore-filters` (`:510`) also delivers the poison but additionally returns every user record for the unit and process queries, poisoning aggregates this pack does not declare invalid. It satisfies the alarm booleans here but is not the intended stream; prefer `dup-kernel`.

Coordination: this requirement was sent to `MoriR15.HarnessBuild` (dotted id; bare `HarnessBuild` is not a registered agent).

## Expected observable behavior (to be judged by HarnessBuild, not run here)

With `dup-kernel`, the kernel query capture is rc 0, stderr-free, valid NDJSON. The aggregate jq predicate sees one nonmatching record, `JOURNAL_JQ_TAIL` classifies `record-invalid` (tools/mori-census.sh:973-974,1104), so:

- raw `user.kernel_oom_notice` stays `unavailable:record-invalid` — never a repaired count and never `0`;
- per the r15 production interface, `positive_kernel_oom=1` (case 2: 2) from the same captured stream, no extra journal query;
- exactly one `OOM_KILL_JOURNAL` crit fires because an independently valid positive exists;
- no `KILL_SIGNAL_JOURNAL` warn: case 3's `98e32220…` record lacks `EXIT_CODE=killed`/`EXIT_STATUS=9`, and no `UNIT_RESULT` string `oom-kill`/`signal` exists in any case;
- `positive_unit_oom`, `positive_unit_signal`, `positive_process_sigkill` are 0 for these cases; positive fields remain *available* here because the capture itself succeeded (the contract makes them unavailable only on capture/parser failure).

## Non-claims

- No claim of complete journal coverage, authenticated `MESSAGE_ID`, or a unique-victim/kill total; the raw aggregate stays unavailable in all four cases.
- No claim that the current census implements `positive_kernel_oom`; these fixtures encode the contract for CensusPositive + HarnessBuild.
- No claim that `want_oom`/`invalid_class` assertions pass until the harness runs.

## Risks / blockers

- Schema lacks a mode discriminator; if HarnessBuild's pack→`Case` builder cannot set `dup-kernel` per case, every KernelUser case degrades to `honor` and the C1 edge is untested while still green on `want_oom`. Message sent; a follow-up note in the harness report is warranted.
- `dup-kernel` depends on the r14 kernel-query argv shape; an r15 argv refactor silently disables the poison.
- Not verified by execution, per assignment (L1 owns the single post-integration gate).

## Tooling

No installs or updates. Host-safety notice received; any future pacman use would follow the `pacman -Sp` all-not-installed gate.
