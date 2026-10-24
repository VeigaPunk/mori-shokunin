# MutModeRead — bounded C2 real-reader mutation probe

## Result

**KILLED by the assigned synthetic mocked-reader detector.** Pristine and restored controls both pass; the one-line mutant attempts a forbidden `qgroups/mode` open after an enabled-first check. The attempt is intercepted entirely in mocked I/O, after a synthetic concurrent disable. No actual kernel mode attribute is opened, and this is not a host-crash reproduction.

Axes: **real-reader safety** (never open mode), **detector sensitivity** (reach and reject the plausible enabled-first regression), and **restoration fidelity** (identical source bytes and restored behavioral controls). This is one mutation, not a round admission or a broader coverage claim.

## Isolation and mutant

- Production pin: `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c`.
- Expectation seal supplied by the assignment: `22772c10f6e3c1d8d3fe1b72083a6194e9f4e687`; no seal ancestry measurement was performed in this seat.
- Actual separate sparse Git clone: `/fast/scratch/hyaku/mori-r23/MutModeRead/repo`.
- Observed clone `HEAD` and unique branch `round23/MutModeRead` both resolved to the production pin before the mutation. The clone has its own working tree/index/refs and read-only object alternates; no lane Git/jj metadata was mutated.
- Subject: `/fast/scratch/hyaku/mori-r23/MutModeRead/repo/tools/mori-quota-surface.py`, function `scan_btrfs_sysfs`.
- Production counterpart, not edited: `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py`.

One inserted statement after original line 611 (`enabled = True`), at mutant line 612:

```python
mode = btrfs_modes(read_sysfs_text(os.path.join(qgroups_path, "mode")))
```

This plausibly reintroduces the rejected informational mode read behind an enabled-first check. It matches the assigned safety invariant and was reached: the mutant's open trace contains the inserted mode request. It is not an inapplicable/nonmatching mutant.

Small exact source fragment: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/falsify/MutModeRead/mutant-source-fragment.py`.

## Expected detector and fixture witness

Detector executed from `/fast/scratch/hyaku/mori-r23/MutModeRead/mode_read_probe.py`; identical archived bytes are at `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/falsify/MutModeRead/mode_read_probe.py`.

It executes exactly the hashed scratch source bytes, calls the actual `scan_btrfs_sysfs` and `read_sysfs_text` implementation, and does not replace either function. Two safety fences apply: `BTRFS_SYSFS` is rebound to `/fast/scratch/hyaku/mori-r23/MutModeRead/synthetic-sysfs`, and `listdir`, `isdir`, `stat`, and `builtins.open` are fully mocked without delegation. Unexpected I/O is rejected. No real mountinfo, device, quota state, or sysfs attribute is queried.

The decisive fixture uses synthetic UUID `11111111-2222-4333-8444-555555555555`, device `dm-synthetic`, and an existing qgroups directory. Its enabled handle returns `1\n`; closing that handle records `synthetic_disable_after_enabled_read` and changes only synthetic state to disabled. Any later mode open records the attempt and raises `ForbiddenModeOpen` before touching a filesystem. Expected pristine/restored record:

```json
{"11111111-2222-4333-8444-555555555555":{"devices":["dm-synthetic"],"qgroups":true,"enabled":true,"mode":null}}
```

The stale `enabled:true` value is deliberately retained: the invariant is not atomic quota-state observation; it is never opening the ASSERT-guarded mode attribute. Independent controls exercise enabled `0`, an unreadable enabled attribute, and an absent qgroups directory. They must preserve their respective `enabled:false/null/null`, `qgroups:true/true/false`, and `mode:null` records. All three controls pass in all phases.

Every invocation used the same unchanged detector and fixture set, Python `3.14.8`, one scanner child at a time, `TMPDIR=/fast/scratch/hyaku/mori-r23/MutModeRead`, a 402653184-byte (384 MiB) address-space limit, a 10-second CPU limit, and a 15-second wall timeout:

```text
env TMPDIR=/fast/scratch/hyaku/mori-r23/MutModeRead timeout --signal=KILL 15s prlimit --as=402653184 --cpu=10 -- python3 -B /fast/scratch/hyaku/mori-r23/MutModeRead/mode_read_probe.py --tool /fast/scratch/hyaku/mori-r23/MutModeRead/repo/tools/mori-quota-surface.py --phase PHASE --result /fast/scratch/hyaku/mori-r23/MutModeRead/PHASE.json
```

`PHASE` was `before`, then `mutant`, then `after`. These are the only three behavioral invocations; no full driver, public selftest, build, lint, formatter, gate, privileged command, mount, or live quota probe was run.

## Actual output

| Source phase | Actual process exit | `cases_passed` / `cases_total` | `mode_open_attempts` | Decisive result |
|---|---:|---:|---:|---|
| Pristine | 0 | 4 / 4 | 0 | Expected record returned, `mode:null` |
| Mutant | 1 | 3 / 4 | 1 | `failure:"ForbiddenModeOpen"`, `observed:null` |
| Restored | 0 | 4 / 4 | 0 | Expected record returned, `mode:null` |

Mutant event order: open enabled → synthetic disable → open mode intercepted. The intercepted path is `/fast/scratch/hyaku/mori-r23/MutModeRead/synthetic-sysfs/11111111-2222-4333-8444-555555555555/qgroups/mode`, with `synthetic_enabled_now:false`. No timeout or unrelated detector failure occurred. A green pristine control, the reached forbidden operation in the mutant, and the green restored control support **killed**, rather than inconclusive.

Archived bounded output projection, exact launch arguments, hashes, and fixture witness: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/falsify/MutModeRead/bounded-results.json`.

Full original JSON outputs remain at:

- `/fast/scratch/hyaku/mori-r23/MutModeRead/before.json`
- `/fast/scratch/hyaku/mori-r23/MutModeRead/mutant.json`
- `/fast/scratch/hyaku/mori-r23/MutModeRead/after.json`

## Hashes and restoration evidence

| Bytes | SHA-256 |
|---|---|
| Pristine source | `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` |
| Mutant source | `799c059e8779775c60020566945de09646bade2d3425673e515f43c2876da7c8` |
| Restored source | `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` |
| Same detector in all three runs | `7d4753b4c5fb7eebad23b8ae5aeb96caa760c5a4263477a1fb131f6e5223df7a` |

The inserted statement was deleted with a surgical edit after the expected mutant exit 1. The restored run hashed the executed source back to the pristine hash and repeated all four controls successfully. No mutated production source remains; the clone is restored, with only the explicitly labelled small mutant fragment retained as evidence.

## Source and contract grounding

Read the original contract, preseal amendment, case decisions, selected `CaseBtrfsQgroup`, quota and rename oracle scope, and round23 lesson. The final preseal safety correction explicitly supersedes the earlier enabled-first/mode-read rule:

- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/preseal-amendment.md`, lines 132–140: real mode never reads `qgroups/mode`; fixture mode metadata remains separate.
- `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-23.md`, lines 79–84: enabled-first can race a quota disable; no host-crash reproduction claimed.
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/evidence/sources/S079-fs_btrfs_sysfs.c`, lines 2355–2395: `qgroup_enabled_show` reads the flag, while `qgroup_mode_show` locks and asserts enabled at line 2378. Recorded source SHA-256 is `ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43`. Upstream: https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/sysfs.c .
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/frozen/case-decisions.json`, lines 25–31, retains the original and selected qgroup-case identities; `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/frozen/quota-cases/CaseBtrfsQgroup.json` remains fixture-only data, not permission to read mode in real mode.

No frozen case, rule, expectation, or oracle was edited. This new detector's kill does **not** establish that the sealed fixture oracle detects real-reader I/O regressions. It does not remeasure C1. The assignment's strict C2 target remains **UNPROVABLE at 29/30**, with frozen `CaseEscapedSpace` unchanged; no special-casing, exclusion, relabelling, or expectation repair was attempted. No privacy clearance, health verdict, admission, or promotion is implied.

Tools installed/updated: **none**. Procedure disclosure: an initial filename-only discovery glob returned `.scratch` path names; no such file contents were opened, and subsequent lesson/source reads used named paths. A documentation-URI range-selector tool inconsistency was reported through the required tool-issue channel; it did not affect any probe or source bytes.

## Authorized followup — per-UUID devices permission loss

**Observed safety counterexample in unchanged pinned production code:** incomplete device membership is classified **disabled**, whereas the followup requires **unknown, never disabled**. This is a source finding, not another mutant, and does not replace or invalidate the preserved mode-read mutant evidence above.

After the original probe completed, L1 explicitly authorized one additional bounded mocked-reader invocation at the same `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c` pin. No subject source was changed. The new detector calls the production `scan_btrfs_sysfs()` and then `classify_btrfs("dm-0", scanned)`, using the same scratch clone and a new fully synthetic root `/fast/scratch/hyaku/mori-r23/MutModeRead/permission-loss-sysfs`. Root rebinding plus nondelegating mocks for `os.listdir`, `os.path.isdir`, `os.stat`, and `builtins.open` prevent actual sysfs I/O.

### Fixture and actual output

Both canonical synthetic UUIDs potentially contain `dm-0`:

- `11111111-2222-4333-8444-555555555555`: the UUID directory is visible, but listing its `devices` directory raises `PermissionError`.
- `aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee`: listing `devices` succeeds and returns `["dm-0"]`.

The qgroups stat reports synthetic absence for both UUIDs. No file open is requested. Actual scanner output:

```json
{
  "11111111-2222-4333-8444-555555555555": {
    "devices": [], "qgroups": false, "enabled": null, "mode": null
  },
  "aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee": {
    "devices": ["dm-0"], "qgroups": false, "enabled": null, "mode": null
  }
}
```

Actual classifier return is `(("disabled", "n/a", "btrfs_qgroups_dir_absent"), None)`. The required safety predicate is `quota_state == "unknown"`; actual `quota_state == "disabled"` fails it. Detector stdout records `pass:false`, `verdict:"safety_counterexample"`, and `exit_code:1`; the child actually exited **1**. That is the detector exit, not a measured quota CLI exit.

The failure-bearing path in `/fast/scratch/hyaku/mori-r23/MutModeRead/repo/tools/mori-quota-surface.py` is:

1. Lines 593–596 catch the per-UUID devices listing `OSError` and replace the unknown membership with `devices=[]`, losing the error.
2. Lines 467–473 of `classify_btrfs` then see exactly one known matching UUID.
3. Lines 478–479 return disabled from that visible UUID's absent qgroups directory, despite the other UUID's unresolved membership.

Thus the observed complete-looking unique match is derived from an incomplete association census. This reproduces ReviewReadFence's specific concern without touching actual sysfs, mode, host quota state, or any frozen fixture.

### Invocation, hashes, and receipts

Exactly one child was run, with no retry:

```text
env TMPDIR=/fast/scratch/hyaku/mori-r23/MutModeRead timeout --signal=KILL 15s prlimit --as=402653184 --cpu=10 -- python3 -B /fast/scratch/hyaku/mori-r23/MutModeRead/permission_loss_probe.py
```

Runtime was Python `3.14.8`; address-space limit 384 MiB, wall timeout 15 seconds, CPU limit 10 seconds. There was no timeout or unexpected I/O. This separately authorized invocation is in addition to the original three mode-mutation invocations.

- Source SHA-256 before **and** after: `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92`.
- New detector SHA-256: `038aac818f1c205e95a4149f18e6dcf582286a142e72afe91b6f3b6f2821fb61`.
- Original new receipt: `/fast/scratch/hyaku/mori-r23/MutModeRead/permission-loss.json`.
- Archived full new receipt: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/falsify/MutModeRead/permission-loss.json`.
- Archived identical new detector: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/falsify/MutModeRead/permission_loss_probe.py`.

No restoration edit was needed: pinned subject bytes stayed unchanged before/after, and the earlier mode mutant remains restored. No production, oracle, case, expectation, or prior evidence file was changed. Only this appended report and the new named synthetic evidence were written in the lane. No tool installation/update, live read, privileged operation, fix, integration, or additional verification was performed. Retain this failure separately from the frozen **29/30** denominator; no expectation or admission rule is changed.
