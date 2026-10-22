# Retention at assigned tip

## Result

The sandbox clone was checked out at `8809a3fe1eaa87a0afa177a15263d174378e7462` (`git rev-parse HEAD` output: `8809a3fe1eaa87a0afa177a15263d174378e7462`).

At that revision the retention scan reported **metric 4**, **exit code 1**. The scan's underlying command was:

```text
python3 -I -B tools/mori-retention-gate.py scan --repo <clone> --rev 8809a3fe1eaa87a0afa177a15263d174378e7462 --policy .ufo/waves/round-18/frozen/c1-policy.json --allowlist corpus/evidence/retention-allowlist.json
```

Captured result (only the metric and status were retained):

```text
retention_metric=4
retention_exit_code=1
```

The entering baseline was also metric 4 (`.ufo/waves/round-29/w1/RetentionBase.md:15`), so the measured tip is equal to that baseline. The gate defines the metric as unallowlisted hits and returns 1 when it is nonzero (`tools/mori-retention-gate.py:260-288`). The scanner documents that matched line contents are never emitted (`tools/mori-retention-gate.py:2-6`); no protected line content is included here.

## Requested self-tests

- `python3 -I -B tools/mori-pressure.py --selftest` → `MORI_PRESSURE_SELFTEST: PASS 12/12`; exit 0.
- `TMPDIR=/fast/scratch/hyaku/mori-r29/w2/RetentionAtTip/tmp tools/mori-census.sh --selftest` → `MORI_CENSUS_SELFTEST: PASS (134 cases, 134 passed, 0 failed)`; exit 0. Its temporary directory was placed in this seat's scratch area; census selftest is documented as fixture-only (`tools/mori-census.sh:211-213`).

## Scope and handoff

Only this report was written in the lane; the clone and census temporary directory are under this seat's scratch directory. No tools were installed or updated. No blocker encountered. Risk: retention remains non-clean at metric 4 / exit 1 even though it did not regress against the entering metric-4 baseline. The two requested self-tests passed.