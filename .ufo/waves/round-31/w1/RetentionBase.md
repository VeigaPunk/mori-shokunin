# Retention baseline at round-31 entry and freeze commits

## Task and method

Measure the lane retention scan metric at the entering tip `a12c68ae81257fb6f918bb165bcb39c73f82d212` and at the freeze commits `2124cbcddd676102b3d59f0765cb42e8f05090ee` (contract freeze) and `8baccf4ac9c44a38848d90c34df52392e804c168` (receipts freeze), the same way round 30 did. Method source: `.ufo/waves/round-30/w1/RetentionBase.md:7-11` (command shape) and `.ufo/waves/round-30/evidence/tip-retention.txt:2-4` (summary format and the note that exit 1 is structural while the inherited hits exist). Tool: `tools/mori-retention-gate.py`, subcommand `scan`. All runs were in a sandbox clone, never in the lane.

## Sandbox setup

```sh
mkdir -p /fast/scratch/hyaku/mori-r31/RetentionBase && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone --no-hardlinks /home/vgpnk/Projects/shokunin/mori-shokunin /fast/scratch/hyaku/mori-r31/RetentionBase/repo
```

Output: `Cloning into '/fast/scratch/hyaku/mori-r31/RetentionBase/repo'... done.`

All three revisions verified present in the lane before cloning (read-only `git rev-parse --verify <sha>^{commit}`; each printed its own sha).

## Scans

For each revision the sandbox clone was detached at that revision, and the tool copy of that same revision was run from inside the clone (round-30 pattern):

```sh
cd /fast/scratch/hyaku/mori-r31/RetentionBase/repo && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git checkout --detach --quiet <sha> && timeout 120 python3 -I -B tools/mori-retention-gate.py scan --repo /fast/scratch/hyaku/mori-r31/RetentionBase/repo --rev <sha> --policy .ufo/waves/round-18/frozen/c1-policy.json --allowlist corpus/evidence/retention-allowlist.json > /fast/scratch/hyaku/mori-r31/RetentionBase/scan-<shortsha>.json; echo "EXIT=$?"
```

Each run emitted one compact JSON line (full stdout saved under `/fast/scratch/hyaku/mori-r31/RetentionBase/`). The complete top-level summary fields, verbatim per revision:

`2124cbcd` (exit=1):

```text
{"commit":"2124cbcddd676102b3d59f0765cb42e8f05090ee","finding_id":"RETENTION_FINDINGS","metric":4,"non_author":5,"policy_sha256":"db06e9810bbfd243fb0a753a46960573df39083ea90174ce463cf2a0ab523128","routed":0}
```

`8baccf4a` (exit=1):

```text
{"commit":"8baccf4ac9c44a38848d90c34df52392e804c168","finding_id":"RETENTION_FINDINGS","metric":4,"non_author":5,"policy_sha256":"db06e9810bbfd243fb0a753a46960573df39083ea90174ce463cf2a0ab523128","routed":0}
```

`a12c68ae` (exit=1):

```text
{"commit":"a12c68ae81257fb6f918bb165bcb39c73f82d212","finding_id":"RETENTION_FINDINGS","metric":4,"non_author":5,"policy_sha256":"db06e9810bbfd243fb0a753a46960573df39083ea90174ce463cf2a0ab523128","routed":0}
```

Remaining per-revision arrays (identical in all three): `forbidden_allowlist=[]`, `warnings` (stale allowlist rows) 0, allowlisted hits 104, total hits 113.

## Unallowlisted hits (path, line number, class — no line content)

Identical set at all three revisions:

```text
.ufo/waves/round-20/falsify/NoHarmRun/rg/.ufo/waves/round-18/frozen/c1-policy.json:8 R2
.ufo/waves/round-20/falsify/NoHarmRun/rg/.ufo/waves/round-18/frozen/c1-policy.json:11 R5
.ufo/waves/round-20/falsify/NoHarmRun/rg/.ufo/waves/round-18/frozen/c1-policy.json:12 R6
.ufo/waves/round-20/falsify/NoHarmRun/rg/.ufo/waves/round-18/frozen/c1-policy.json:14 R8
```

This is the same four-hit set round 30 measured (`.ufo/waves/round-30/w1/RetentionBase.md:36-38`: R2, R5, R6, R8 on lines 8, 11, 12, 14 of the same archived policy copy).

## Result

| revision | role | metric | routed | non_author | exit |
|---|---|---|---|---|---|
| a12c68ae81257fb6f918bb165bcb39c73f82d212 | entering tip | 4 | 0 | 5 | 1 |
| 2124cbcddd676102b3d59f0765cb42e8f05090ee | contract freeze | 4 | 0 | 5 | 1 |
| 8baccf4ac9c44a38848d90c34df52392e804c168 | receipts freeze | 4 | 0 | 5 | 1 |

Metric delta across all three revisions: 0 (4 → 4 → 4); the unallowlisted hit set is byte-identical (same path, line, class). The exit 1 at every revision is structural: the same inherited hits existed at the round-30 baseline `58b61681` (`.ufo/waves/round-30/evidence/tip-retention.txt:4`). No new retention surface appeared between the entering tip and either freeze commit, and no allowlist row went stale (warnings 0, `forbidden_allowlist` empty). The policy hash is identical at all three revisions and equals round 30's (`db06e981…128`, `.ufo/waves/round-30/w1/RetentionBase.md:15`), so the rules did not move between measurements.

Lineage, from read-only `git log -1 --format='%h %ci %s'` and `git merge-base --is-ancestor` in the sandbox: `2124cbcd` (2026-10-22 20:37:48 -0300, "round-31: freeze contract, counters, C2 fixtures and control scripts before data") is an ancestor of `8baccf4a` (20:38:46 -0300, "round-31: before receipts and do-nothing/shortcut control receipts for both counters, before any seat ran"); the entering tip `a12c68ae` (19:54:19 -0300, "round-30 verifier spot-check (integrator, hyaku): non-author admit/reject") is on a divergent line — neither freeze is its ancestor. The metric is nonetheless identical on both lines.

## Exact command for the L1 at the landed tip

Substitute the landed tip sha; round 30 recorded this exact shape (`.ufo/waves/round-30/evidence/tip-retention.txt:2`):

```sh
cd /home/vgpnk/Projects/shokunin/mori-shokunin && python3 -I -B tools/mori-retention-gate.py scan --repo /home/vgpnk/Projects/shokunin/mori-shokunin --rev <LANDED_TIP_SHA> --policy .ufo/waves/round-18/frozen/c1-policy.json --allowlist corpus/evidence/retention-allowlist.json
```

Bounds-compliant sandbox variant (what I ran; same result, only `--repo`/cwd differ):

```sh
cd /fast/scratch/hyaku/mori-r31/RetentionBase/repo && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git checkout --detach --quiet <LANDED_TIP_SHA> && timeout 120 python3 -I -B tools/mori-retention-gate.py scan --repo /fast/scratch/hyaku/mori-r31/RetentionBase/repo --rev <LANDED_TIP_SHA> --policy .ufo/waves/round-18/frozen/c1-policy.json --allowlist corpus/evidence/retention-allowlist.json
```

Expected at the landed tip, if wave-1 seats added no new retained-context tokens outside the allowlist and non-author paths: `metric=4 unallowlisted=4 routed=0`, exit 1 (structural, inherited set unchanged). Any metric above 4, a change in the four-hit set, or new `warnings`/`forbidden_allowlist` rows is wave-created signal for the L1 to adjudicate.

## Files, tools, cleanup

- Lane file written: `.ufo/waves/round-31/w1/RetentionBase.md` only (this report).
- Scratch artifacts (outside the lane): clone `/fast/scratch/hyaku/mori-r31/RetentionBase/repo` and saved scan JSONs `scan-2124cbcd.json`, `scan-8baccf4a.json`, `scan-a12c68ae.json` (full outputs, path/line-number/class/hash fields only).
- No tools were installed or updated. No build, test, lint, or formatter was run. Every command was capped with `timeout`; all scan processes completed synchronously and none remain running. No blockers.
