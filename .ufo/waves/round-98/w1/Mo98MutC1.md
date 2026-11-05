# Mo98MutC1 — mutation test: `tools/mori-userns-runway.py` vs frozen counter `count-c1.py`

Lane: mori, round 98 wave w1, seat Mo98MutC1 (role: mutation-tester). Date: 2026-11-05.
Landing revision under test: `600deb7ed2695f54b289cf5b6c3931e0fa9c8bb3`. Counter bytes: `.ufo/waves/round-98/count-c1.py` (frozen, never edited). Scratch: `/fast/scratch/hyaku/mori-r98/Mo98MutC1` (removed at finish; `TMPDIR=$S` throughout).

## Method

1. `git -C /home/vgpnk/Projects/shokunin/mori-shokunin archive 600deb7e… | tar -x -C $S/base` — pristine landing tree.
2. Baseline: frozen counter `--root $S/base --work $S` + `--selftest` (a baseline failure would make everything inconclusive; it did not happen).
3. 14 isolated copies `cp -a $S/base $S/mNN`; exactly ONE single-change replacement each in `tools/mori-userns-runway.py` (applied and confirmed at the intended line by the edit tool diff).
4. Detector per mutant: `python3 $S/mNN/tools/mori-userns-runway.py --selftest` then `python3 count-c1.py --root $S/mNN --work $S`. Tool file sha256 recorded before and after each run (no run modified bytes — all pairs equal).
5. No lane/fleet file outside my report was written; git used read-only only (`archive`, `rev-parse`, `hash-object`); no sudo, no sysctl or namespace changes, no user namespace created (none needed).

## Baseline (pristine landing bytes) — green, so all verdicts below are conclusive

```
base tool sha256: 5ab134ee036f83851eb98a9027db699a5800130c5c13598cb37aeb2abe452db2
base_selftest_rc=0
MORI_USERNS_RUNWAY_SELFTEST: PASS (11 cases)
base_counter_rc=0
C1=met cases_ok=15/15 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) registry=met sourced=met(S629,S630,S631,S632) province=met checks_failed=- root=/fast/scratch/hyaku/mori-r98/Mo98MutC1/base
```

Pristine-copy proof after all runs: `git rev-parse 600deb7e:tools/mori-userns-runway.py` = `89335d913ddb317f1b78e156444a91b68c958b90` = `git hash-object $S/base/tools/mori-userns-runway.py`; working sha256 unchanged (`5ab134ee…`).

## Results table

| Mutant | Single change (line) | Counter verdict | Selftest | Killed by |
|---|---|---|---|---|
| m01 | `INIT_USER_INO` 4026531837→…836 (off by one) | `C1=unmet cases_ok=8/15` (F1,F2,F3,F4,F5,F8,F9) | FAIL 4/11 (ok-distinct, limit-zero, full, low) | both |
| m02 | `LINK_RE` `^user:` → `^(?:user\|net):` (accepts `net:[…]`) | `C1=unmet cases_ok=15/15 checks_failed=selftest` | FAIL 1/11 (ok-distinct used 3≠2) | selftest only |
| m03 | `runway = max(limit-used,0)` → `runway = limit-used` | **`C1=met cases_ok=15/15 checks_failed=-`** | PASS (11 cases) | **SURVIVED** |
| m04 | low boundary `runway < low` → `runway <= low` | `C1=unmet cases_ok=14/15` (F5-boundary) | PASS | counter F5 only |
| m05 | `if runway == 0:` → `if limit != 0 and runway == 0:` (limit 0 no longer exhausted) | `C1=unmet cases_ok=14/15` (F2-limit-zero) | FAIL 1/11 (limit-zero state low≠exhausted) | both |
| m06 | `used = len(seen)` → `len(seen) + unreadable` | `C1=unmet cases_ok=14/15` (F1-mixed) | FAIL 1/11 (ok-distinct) | both |
| m07 | `pids = [e for e in entries if e.isdigit()]` → `list(entries)` (non-digit counted) | `C1=unmet cases_ok=8/15` (F1,F2,F3,F4,F5,F8,F9) | FAIL 5/11 (incl. no-pids wants setup, got low) | both |
| m08 | `ECHO_RE` `>{1,2}` → `>` (`>>` append missed) | `C1=unmet cases_ok=14/15` (J2-forms) | PASS | counter J2 only |
| m09 | `TEE_RE` drops `(?:-a\s+)?` (`tee -a` missed) | `C1=unmet cases_ok=14/15` (J2-forms) | PASS | counter J2 only |
| m10 | `-p/--load` branch → `if False:` (`sysctl -p` not counted) | `C1=unmet cases_ok=15/15 checks_failed=selftest` | FAIL 1/11 (journal-forms n=3≠4) | selftest only |
| m11 | userns_zero `e["value"] == "0"` → `!= ""` (any value) | `C1=unmet cases_ok=14/15` (J1-incident) | FAIL 1/11 (journal-incident zero 2≠1) | both |
| m12 | `clean_value` → `return v` (no `?` masking) | `C1=unmet cases_ok=15/15 checks_failed=selftest` | FAIL 1/11 (redaction: `value=MARKERX$(id)` leaked) | selftest only |
| m13 | journal setup `return 2` → `return 0` | `C1=unmet cases_ok=14/15` (J5-unreadable) | PASS | counter J5 only |
| m14 | `elif a == "--system":` → `"--system-disabled"` (not counted) | `C1=unmet cases_ok=14/15` (J2-forms) | PASS | counter J2 only |

13/14 killed. 1 survivor. Per-mutant tool-file sha256 identical before and after the detector runs (no self-modification): m01 `d64982be8fb67180…` m02 `98ddf8fffa007c7c` m03 `53bf4333364f4af7` m04 `6baa0bb7b608e587` m05 `6bded0ccc0871890` m06 `d83e41b0659394a3` m07 `4f7e767103eb05f5` m08 `5a0c7b4976615c18` m09 `0a223b3fa28432be` m10 `2a8e8ec4990ffc41` m11 `01236f58de009851` m12 `531244bcaae4ec4f` m13 `e35a5f9747c70a3f` m14 `9a866e8a3d3a5084`.

## Survivor m03 — coverage finding, not equivalence

`C1=met cases_ok=15/15 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) registry=met sourced=met(S629,S630,S631,S632) province=met checks_failed=-` — byte-for-byte the landing verdict (modulo `root=` path).

Not equivalent in general: when used > limit the pristine tool clamps `runway` to 0 → `state=exhausted` (rc 1); the mutant reports a negative runway and `state=low` (rc 1, so exit code happens to match). **No frozen fixture exercises used > limit**: all 9 counter runway cases and all 4 non-setup selftest runway cases have used ≤ limit (F2/F3 sit exactly at 0), and the live host at run time had used_lb=6 ≪ 122865. What would kill it (report-only suggestion, no contract change implied): one more fixture with used > limit, e.g. limit `"2\n"`, three distinct non-initial links → pristine `runway=0 state=exhausted`, mutant `runway=-1 state=low`.

## Coverage findings from selftest-only and battery-only kills

Five mutants (m02, m08, m09, m10, m12) leave the frozen 15-case fixture battery at 15/15 and are caught only by the tool's own selftest conjunct (a). In detail: the counter battery has no `net:[…]` link (F1 uses `mnt:[…]`, correctly still unmatched), no `>>` append echo, no `tee -a`, no `sysctl -p/--load` line (verified: `grep -cE 'sysctl (-p|--load)|--load'` on the pinned incident capture = 0; its 6 writes are two `sysctl -w` plus echo/tee forms), and its J6 redaction case plants markers in PWD/username (never parsed) rather than in a hostile value — a raw `$(id)` value would pass J6. m13 (setup rc) and m04 (boundary) and m14 (`sysctl --system`) are caught by exactly one counter case each (J5, F5, J2) with selftest blind. This is a detection-and-report observation only; the frozen instrument is not mine to amend.

## Verdict

`VERDICT C1 holds: 13/14 single-change mutants of tools/mori-userns-runway.py are killed by the frozen counter (survivor m3 is a battery-coverage gap on used>limit, documented above); baseline and all runs reproducible, bytes pinned.`

## Hygiene, tooling, unrun checks

- Restoration: base tree verified pristine post-run (sha256 + git blob id above); mutant copies were disposable per tasking and deleted with the scratch dir at finish; the lane working tree was never written (archive/rev-parse/hash-object only).
- Tool installs: none (stdlib python3 sufficient; pacman untouched).
- Unrun checks: C2 calibration (out of my scope); `--journal-live` path (needs journalctl, not exercised); no unshare/user-namespace created (task authorized it but the mutation battery needs none); the frozen counter's own sha256 pin of the incident capture was not independently recomputed beyond the counter enforcing `INCIDENT_SHA` on every run (15 runs, all passed setup).
