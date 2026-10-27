# Mo54ScoutRecheckDebt — recheck trigger inventory (2026-10-27)

Scope: every `corpus/knowledge/*.md` entry with a `recheck:` line at round-54 landed data revision `78295c764093ff1f6cee08d7246679900bde7265`; 56 files found. Trigger labels: **date cadence**, **on-release**, **tool change**, **none** (command-only/manual, no explicit event trigger). Fired means its stated event occurred by 2026-10-27; `answered` means a later round/ledger/source record visibly covers it, not that I reran the referenced procedure. Where `on-release` does not identify a product, I mark the result UNVERIFIED rather than infer an event.

| Entry | Trigger | Fired by 2026-10-27? | Answered by / status |
|---|---|---|---|
| c1s-cwd-r43 | date cadence (90d) | No; verified 2026-10-24 | Open; not due |
| census-cgroup-levels-r45 | date cadence (90d), plus pinned v7.2 copy | v7.3 exists, but no explicit on-release trigger; cadence not due | Open for v7.3; no ledger found |
| commit-runway-read-r53 | on-release (Linux tag) | Yes: v7.3 | Round-54 C1 ledger (`kernel-v7.3-recheck-r54.md`), disposition/votes settlement pending |
| conform-bindings-r41 | none (explicit command recipe) | No explicit trigger | Open/manual procedure |
| conform-scope-r40 | on-release (product unspecified) | UNVERIFIED; Python release target not named | Open/ambiguous |
| conform-source-order-r42 | date cadence (90d) | No; verified 2026-10-24 | Open; not due |
| containment-timed-supersede-r38 | tool change + S226 canonical-path paragraph move | Yes: S226 paragraph was corrected in r39; append-only tool changed in r40/r41 | Partially answered by r39 source correction; no complete recheck receipt located for subsequent tool changes |
| disk-write-rate-r33 | on-release, with host kernel >7.2 or sysstat >12.8.0 conditions | No: host kernel 7.2.11, sysstat 12.8.0 | Open; strict “past” conditions not met |
| dispatch-ledger-r18 | none (verification/selftest recipe) | No explicit trigger | Open/manual procedure |
| drift-repin-r20 | none; recipe explicitly superseded/inactive in entry | No active trigger | Superseded; entry itself names round-21 active acceptance audit |
| earlyoom-invocation-scope-r30 | earlyoom release, systemd release, or tool change | No observed release/tool change: latest tags queried were earlyoom v1.9.0 and systemd v262; tool last change 2026-10-22 | Not fired |
| evidence-minimization-r18 | none (selftest/scan recipe) | No explicit trigger | Open/manual procedure |
| freeze-order-r18 | none (check/selftest recipe) | No explicit trigger | Open/manual procedure |
| gate-ancestry-r39 | tool change (append-only gate walk/edit/timing) + S227 cadence | Yes: `mori-sources-appendonly.py` changed in r40/r41 after r39 | Open/UNVERIFIED S227 cadence; no later recheck receipt located |
| harness-job-capacity-r25 | omp release | Yes: installed `omp --version` reports 18.13.1 vs entry’s v18.12.6 | Open; no newer-release recheck located |
| inheritance-d72ac16-r42 | none (fixed-commit count recipe) | No explicit trigger | Open/manual procedure |
| jj-branch-anchor-r17 | none (regression recipe) | No explicit trigger | Open/manual procedure |
| journal-alarm-routing-r14 | none (pinned/manual source and query recipe) | No explicit trigger | Open/manual procedure |
| journal-cursor-window-r16 | none (pinned/manual source recipe) | No explicit trigger | Open/manual procedure |
| journal-disk-usage-total-r51 | date cadence (180d) | No; verified 2026-10-24 | Open; not due |
| journal-positive-evidence-r15 | none (manual source/query recipe) | No explicit trigger | Open/manual procedure |
| journal-reach-r49 | date cadence (180d) | No; verified 2026-10-25 | Open; not due |
| kernel-oom-line-attribution-r12 | none (commands pin v7.2/commit and live journal; no cadence/release rule) | No explicit trigger | Open/manual procedure; v7.2 pin remains |
| kernel-v7.3-recheck-r53 | on-release (next Linux tag after v7.3) | No later tag established; v7.4 API query yielded no output, UNVERIFIED | Open for next release |
| kill-classes-by-message-id-r12 | none (pinned source/manual journal recipe) | No explicit trigger | Open/manual procedure |
| lane-silence-r2 | none (live census recipe) | No explicit trigger | Open/manual procedure |
| memavailable-estimate-r51 | on-release (Linux tag) | Yes: v7.3 | Answered by r53 ledger; v7.3 sources also used in r54 |
| memory-failure-kills-r54 | on-release (Linux tag), plus host-kernel-past-7.2 observation | v7.3 was the tag used to create it; no newer tag established (UNVERIFIED); host remains 7.2.11 | Newly answered at v7.3 in this entry; no host firing observed |
| observability-census-r1 | none (live census/selftest recipe) | No explicit trigger | Open/manual procedure |
| observability-surfaces-r2 | none (live census/selftest recipe) | No explicit trigger | Open/manual procedure |
| oom-evidence-loss-r38 | date cadence (180d) | No; verified 2026-10-24 | Open; not due |
| oom-kill-counter-kernel-only-r12 | none (v7.2 source/live counter recipe) | No explicit trigger | Open/manual procedure; v7.2 pin remains |
| oom-memcg-stat-r50 | date cadence (90d) | No; verified 2026-10-26 | Rechecked separately by r54 C1 because its v7.2-pinned claim rows were in scope; cadence itself not due |
| oom-tracepoints-r47 | on-release (Linux tag) | Yes: v7.3 | Open; r53 README explicitly says this entry is unrechecked; r54 C1 does not cover catalogue |
| oom-victim-context-r41 | date cadence (180d) | No; verified 2026-10-25 | Open; not due |
| oom-victim-selection-r27 | kernel, earlyoom, or systemd release | Kernel v7.3 fired; no earlyoom/systemd newer tag observed | Open for kernel arm; r54 C1 scope excludes prose/other entries |
| overcommit-commit-limit-r52 | on-release (Linux tag) | Yes: v7.3 | Answered by r53 ledger |
| pid-probe-conclusion-r44 | date cadence (180d) | No; verified 2026-10-25 | Open; not due |
| quota-observability-r48 | mixed: date cadence (180d) and Linux on-release | Linux v7.3 fired; 180d arms not due (verified 2026-10-25) | v7.3 errno row answered in r54 C1; other cadence arms open/not due |
| retention-reconciliation-r22 | none (selftest/check recipe) | No explicit trigger | Open/manual procedure |
| roster-truth-r12 | none (census recipe) | No explicit trigger | Open/manual procedure |
| s235-sha-correction-r43 | date cadence (180d) | No; verified 2026-10-24 | Open; not due |
| seat-terminal-status-r17 | none (selftest/regression recipe) | No explicit trigger | Open/manual procedure |
| source-drift-content-anchor-r38 | tool change (classify path or live receipt) | No tool change found after r37; no live-receipt change established | Not fired / live-receipt arm UNVERIFIED |
| source-drift-hardening-r37 | tool change (fetch path), plus S221/S222/S223 180d, S225 90d, S224 on-release | v7.3 fired S224’s on-release arm; no later tool change found; date arms not due | S224/Yama arm open; no recheck receipt located |
| source-drift-r36 | on-release (target unspecified) | UNVERIFIED; generic trigger does not name product | Open/ambiguous |
| structured-journal-scopes-r13 | none (pinned source/query recipe) | No explicit trigger | Open/manual procedure |
| surfaces-r7 | none (census/selftest recipe) | No explicit trigger | Open/manual procedure |
| surfaces-r8 | none (census/selftest recipe) | No explicit trigger | Open/manual procedure |
| system-pressure-r24 | on-release (Linux tag) | Yes: v7.3 | Open; no r54 ledger coverage found for S090/S091 pressure surfaces |
| userspace-oom-killers-r12 | none (pinned systemd v261/earlyoom commit and live checks) | No explicit trigger | Open/manual procedure; pinned versions do not themselves state on-release |
| userspace-oom-killers-r26 | earlyoom or systemd release | No observed release: queried latest tags v1.9.0 and v262, matching entry pins | Not fired |
| verdict-contract-r13 | none (regression/source archaeology recipe) | No explicit trigger | Open/manual procedure |
| watchdog-identity-r31 | procps-ng, kernel, man-pages release or watchdog lines 1, 380–382 change | Kernel v7.3 fired; script changed 2026-10-25 but inserted disk-guard code at line 65; pinned lock block appears moved, not substantively changed; procps is 4.0.7 and pgrep binary 4.0.7 | Kernel arm fired; recheck status open (no receipt located) |
| wave-settlement-r20 | none (selftest/oracle/live scan recipe) | No explicit trigger | Open/manual procedure |

## Commands and observed outputs

Commands run (all repository reads were against absolute lane/fleet paths; no repo mutation):

```sh
# Count and enumerate all knowledge entries with a recheck key
cd /home/vgpnk/Projects/shokunin/mori-shokunin
 grep -rlE '^[-* ]*recheck *:' corpus/knowledge | sort | wc -l
# 56

# Extract provenance/recheck headers
for f in $(grep -rlE '^[-* ]*recheck *:' corpus/knowledge | sort); do
  grep -nE '^(source|verified-at|recheck|author|coverage-map|superseded|status)[: ]' "$f"
done

# Host facts
uname -r                                      # 7.2.11-arch1-1
systemctl --version | head -1                 # systemd 262 (262-1-arch)
pacman -Q sysstat man-pages earlyoom systemd procps-ng linux
# sysstat 12.8.0-1; man-pages 6.19-1; earlyoom 1.9.0-1; systemd 262-1;
# procps-ng 4.0.7-1; linux 7.2.11.arch1-1
/usr/bin/pgrep -V                              # pgrep from procps-ng 4.0.7
omp --version                                  # omp/18.13.1

# Upstream tag checks
curl -fsSL --max-time 12 'https://api.github.com/repos/systemd/systemd/tags?per_page=3'
# first returned tag name v262
curl -fsSL --max-time 12 'https://api.github.com/repos/rfjakob/earlyoom/tags?per_page=3'
# returned v1.9.0, v1.8.2, v1.8.1
curl -fsSL --max-time 12 'https://api.github.com/repos/torvalds/linux/tags?per_page=6'
# no output; UNVERIFIED

git ls-remote --tags https://github.com/torvalds/linux 'refs/tags/v7.4*' 'refs/tags/v7.3*'
# timed out (15s); UNVERIFIED

# Tool-change evidence
git -C /home/vgpnk/Projects/shokunin/mori-shokunin log --format='%h %cs %s' -- tools/mori-sources-appendonly.py
# changes include 265a955c (r40) and d72ac167 (r41), after gate-ancestry-r39 verification
git -C /home/vgpnk/Projects/shokunin/mori-shokunin log --format='%h %cs %s' -- tools/mori-source-drift.py
# last listed change e57c58b5 (r37 freeze), no later change observed

git -C /home/vgpnk/Projects/shokunin show 5f4fa8d8 --stat -- scripts/shokunin-watchdog.sh
# 2026-10-25 insertion, disk-guard; diff hunk starts at old line 65
```

Disk-guard check: `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status`; result showed `/fast/scratch/hyaku` 26% used, 596.8G free. Scratch created at `/fast/scratch/hyaku/mori-r54/Mo54ScoutRecheckDebt/` and removed at completion. No tools installed/updated.

## Findings

- **MED — OPEN:** several fired on-release triggers remain unverified/open: `oom-tracepoints-r47.md`, `system-pressure-r24.md`, `oom-victim-selection-r27.md`, `watchdog-identity-r31.md`, and `source-drift-hardening-r37.md` (S224 arm). Their triggers were met by Linux v7.3, but the r54 freshness ledger scope is claim tables only and does not answer these entries/catalogues.
- **MED — OPEN:** `harness-job-capacity-r25.md` names an omp release trigger; installed `omp/18.13.1` differs from pinned v18.12.6; no release recheck receipt was located.
- **LOW — OPEN:** tool-change entries `gate-ancestry-r39.md` and `containment-timed-supersede-r38.md` have subsequent append-only-gate changes and/or S226 correction; complete subsequent recheck receipt not located.
- **LOW — UNVERIFIED:** `conform-scope-r40.md` and `source-drift-r36.md` say only `on-release` without naming the product; target and fired state cannot be grounded from the entry.
- **LOW — UNVERIFIED:** Linux v7.4 availability check failed (API returned no output; `git ls-remote` timed out). The r53 ledger’s next-tag trigger state is not established.
- **LOW — ANSWERED:** C1-relevant v7.2-pinned table rows in `oom-memcg-stat-r50.md`, `commit-runway-read-r53.md`, and `quota-observability-r48.md` have v7.3 recheck data in `kernel-v7.3-recheck-r54.md`; the frozen counter and voter settlement are outside this reconnaissance and were not rerun.
