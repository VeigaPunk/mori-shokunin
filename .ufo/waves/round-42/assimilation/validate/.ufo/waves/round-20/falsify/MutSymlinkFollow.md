HOLDS — scoped detector-strength probe: the assigned symlink-follow mutant was KILLED by both selftest and independent oracle. This is evidence for this one mutation, not a judgment of C2 as a whole.

## Mutant and expected detector

Seat: `MoriR20.MutSymlinkFollow`. Axes: C2 detector sensitivity, scratch isolation, exact-byte restoration.

Production source was copied to `.ufo/waves/round-20/falsify/MutSymlinkFollow/mori-wave-settlement.py`. Exactly one behavior-bearing statement at line 68 was changed, then restored:

```diff
-    return os.lstat(path)
+    return os.stat(path)
```

This is the existing `_lstat` helper; report inspection calls it at `tools/mori-wave-settlement.py:178,188`. The helper is also shared by root/discovery checks; no other statement or detector was changed.

Expected rejection: `.ufo/waves/round-20/frozen/c2-expected.json:16` requires the `symlink-report` fixture to have scan exit 1, present 0, and `not_followed: true`. The independent fixture creates a report symlink to a nonempty external target at `.ufo/waves/round-20/build/OracleHarness/c2-oracle.py:124-130`; selftest checks non-presence and missing status at `tools/mori-wave-settlement.py:575-579`.

## Commands and actual outputs

All three phases ran the same detector implementation and frozen expectations, against the same scratch tool path. Only the oracle output artifact filename differed. Commands were bounded to 180 seconds each; none timed out. Full absolute argv, stdout, stderr and exit codes are retained in:

- `.ufo/waves/round-20/falsify/MutSymlinkFollow/pristine-run.json`
- `.ufo/waves/round-20/falsify/MutSymlinkFollow/mutated-run.json`
- `.ufo/waves/round-20/falsify/MutSymlinkFollow/restored-run.json`

### Selftest: unmutated control, mutant, restored

Exact command in every phase:

```sh
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/MutSymlinkFollow/mori-wave-settlement.py --selftest
```

| Phase | Exact stdout (one line, terminated by LF) | Exit |
|---|---|---:|
| Pristine control | `MORI_WAVE_SETTLEMENT_SELFTEST: PASS (21 cases, 21 passed, 0 failed)` | 0 |
| Mutated | `MORI_WAVE_SETTLEMENT_SELFTEST: FAIL (21 cases, 20 passed, 1 failed)` | 1 |
| Restored | `MORI_WAVE_SETTLEMENT_SELFTEST: PASS (21 cases, 21 passed, 0 failed)` | 0 |

Stderr was empty in all three runs.

### Independent oracle: unmutated control

```sh
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/build/OracleHarness/c2-oracle.py --tool /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/MutSymlinkFollow/mori-wave-settlement.py --out /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/MutSymlinkFollow/control-oracle.json
```

Exit 0; stdout and stderr empty.

```sh
/usr/bin/jq .counts /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/MutSymlinkFollow/control-oracle.json
```

Exit 0; stderr empty; exact stdout:

```json
{
  "capability_absent": 0,
  "matched": 14,
  "mismatched": 0
}
```

### Independent oracle: mutant

```sh
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/build/OracleHarness/c2-oracle.py --tool /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/MutSymlinkFollow/mori-wave-settlement.py --out /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/MutSymlinkFollow/oracle.json
```

Exit 1; stdout and stderr empty.

```sh
/usr/bin/jq .counts /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/MutSymlinkFollow/oracle.json
```

Exit 0; stderr empty; exact stdout:

```json
{
  "capability_absent": 0,
  "matched": 13,
  "mismatched": 1
}
```

The following command exited 0 with empty stderr and emitted exactly one mismatched case, `symlink-report`:

```sh
/usr/bin/jq '.results[] | select(.status != "matched")' /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/MutSymlinkFollow/oracle.json
```

Its reported mismatches were:

| Key | Expected | Observed |
|---|---|---|
| `exit` | 1 | 0 |
| `present` | 0 | 1 |
| `not_followed` | true | false |

The case's observed wave state was `settled`, with one member and zero missing reports. Full case output remains in `oracle.json`; this file retains the mutated result after tool restoration.

### Independent oracle: restored

```sh
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/build/OracleHarness/c2-oracle.py --tool /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/MutSymlinkFollow/mori-wave-settlement.py --out /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/MutSymlinkFollow/restored-oracle.json
```

Exit 0; stdout and stderr empty.

```sh
/usr/bin/jq .counts /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/MutSymlinkFollow/restored-oracle.json
```

Exit 0; stderr empty; exact stdout:

```json
{
  "capability_absent": 0,
  "matched": 14,
  "mismatched": 0
}
```

## Restoration evidence

Observed SHA-256 values from `sha256sum`:

| Bytes | SHA-256 |
|---|---|
| Production source before copying | `c6e6091937e4bcb02775cea81ce33990924c6e27487a6ce255d2959d94f4e795` |
| Pristine scratch copy | `c6e6091937e4bcb02775cea81ce33990924c6e27487a6ce255d2959d94f4e795` |
| Mutated scratch copy | `9e22a9aeb0f9a6f46abbcfaef02eb6b7143590bfa3ff34e57a392990582e5aed` |
| Restored scratch copy | `c6e6091937e4bcb02775cea81ce33990924c6e27487a6ce255d2959d94f4e795` |
| Production source after restoration | `c6e6091937e4bcb02775cea81ce33990924c6e27487a6ce255d2959d94f4e795` |

Post-restoration exact commands:

```sh
sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-wave-settlement.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/MutSymlinkFollow/mori-wave-settlement.py
cmp -- /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-wave-settlement.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/MutSymlinkFollow/mori-wave-settlement.py
```

Both exited 0. `sha256sum` emitted the identical production/restored hashes shown above with their absolute filenames; `cmp` emitted no stdout or stderr. Full outputs are retained in `.ufo/waves/round-20/falsify/MutSymlinkFollow/restoration-evidence.json`.

## Disposition and bounds

**KILLED**, not inconclusive: both pristine controls passed, both mutated detectors failed, and both restored controls passed. Exact scratch bytes were restored. No production file, sibling source, fleet state, Git index, or jj state was edited. No census, host service operation, tool install, subagent dispatch, integration, or shipping action was performed.
