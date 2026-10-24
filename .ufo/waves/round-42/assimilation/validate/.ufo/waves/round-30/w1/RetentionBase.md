# Retention baseline and synthetic probe

## Axes

- Baseline unallowlisted retention metric.
- Sensitivity of that metric to a synthetic service-manager-style token.

## Baseline evidence

Command run as requested:

```sh
cd /home/vgpnk/Projects/shokunin/mori-shokunin && python3 -I -B tools/mori-retention-gate.py scan --repo /home/vgpnk/Projects/shokunin/mori-shokunin --rev 58b61681a0e3f3b821a17d38a4e713ccd9921615 --policy .ufo/waves/round-18/frozen/c1-policy.json --allowlist corpus/evidence/retention-allowlist.json
```

The command emitted one compact JSON line. Its complete top-level summary fields were:

```text
{"commit":"58b61681a0e3f3b821a17d38a4e713ccd9921615","finding_id":"RETENTION_FINDINGS","forbidden_allowlist":[],"metric":4,"non_author":5,"policy_sha256":"db06e9810bbfd243fb0a753a46960573df39083ea90174ce463cf2a0ab523128","routed":0,"warnings":[]}
exit=1
```

The four unallowlisted hits were R2, R5, R6, and R8 on lines 8, 11, 12, and 14 of the archived policy copy `.ufo/waves/round-20/falsify/NoHarmRun/rg/.ufo/waves/round-18/frozen/c1-policy.json` (scan output). The summary line above omits the JSON's per-hit arrays; no matched source text was copied into this report.

## Sandbox synthetic probe

Created an isolated clone with `--no-hardlinks`, detached it at the measured baseline revision, and added one invented one-line fixture at `/fast/scratch/hyaku/mori-r30/RetentionBase/repo/corpus/evidence/sources-r30/retention-synthetic-probe.txt:1`. The fixture's value is intentionally not repeated here under the lane privacy rules. The clone and fixture are outside the lane repository.

Clone command and output:

```sh
mkdir -p /fast/scratch/hyaku/mori-r30/RetentionBase && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone --no-hardlinks /home/vgpnk/Projects/shokunin/mori-shokunin /fast/scratch/hyaku/mori-r30/RetentionBase/repo
Cloning into '/fast/scratch/hyaku/mori-r30/RetentionBase/repo'...
done.
```

Checkout output: `HEAD is now at 58b6168 round-29 verifier spot-check (integrator, hyaku): non-author admit/reject`.

Fixture commit command and output:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git add corpus/evidence/sources-r30/retention-synthetic-probe.txt && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -c user.name='RetentionBase synthetic probe' -c user.email='retentionbase@example.invalid' commit -m 'Synthetic retention scan probe' -- corpus/evidence/sources-r30/retention-synthetic-probe.txt
[detached HEAD e8ac014] Synthetic retention scan probe
 1 file changed, 1 insertion(+)
 create mode 100644 corpus/evidence/sources-r30/retention-synthetic-probe.txt
```

Sandbox scan command:

```sh
cd /fast/scratch/hyaku/mori-r30/RetentionBase/repo && python3 -I -B tools/mori-retention-gate.py scan --repo /fast/scratch/hyaku/mori-r30/RetentionBase/repo --rev HEAD --policy .ufo/waves/round-18/frozen/c1-policy.json --allowlist corpus/evidence/retention-allowlist.json
```

Its one-line JSON summary and observed fixture-hit count were:

```text
{"commit":"e8ac014df05c75adcc2912acb8e4b5ee49fbbb86","finding_id":"RETENTION_FINDINGS","forbidden_allowlist":[],"metric":4,"non_author":5,"policy_sha256":"db06e9810bbfd243fb0a753a46960573df39083ea90174ce463cf2a0ab523128","routed":0,"warnings":[]}
fixture hit count=0
exit=1
```

Thus, measured metric change was 0 (4 to 4): this particular synthetic fixture did not increase the scan metric. This is a result for the frozen rules, not a general privacy guarantee (policy `known_limit`, `.ufo/waves/round-18/frozen/c1-policy.json:29`).

## What the frozen scan counts

The policy scans tracked blobs at the selected revision, skips blobs with NUL bytes, and splits decoded text by newline (`.ufo/waves/round-18/frozen/c1-policy.json:5`). Its R1–R9 classes count: session-name-shaped timestamp/UUID prefixes (R1); session-store path references (R2); numbered tool-output artifact names (R3); personal Documents paths (R4); shell-history references (R5); privileged-configuration references (R6); operator configuration file/line references (R7); routing-table key names (R8); and session-record field-name patterns (R9) (`.ufo/waves/round-18/frozen/c1-policy.json:7-15`). The metric is unallowlisted hits, excluding non-author paths; routed hits are separately counted (`.ufo/waves/round-18/frozen/c1-policy.json:23-29`).

## Files, risks, blockers

- Lane file changed: `.ufo/waves/round-30/w1/RetentionBase.md` only. Sandbox clone and synthetic fixture are under `/fast/scratch/hyaku/mori-r30/RetentionBase/`.
- Risk/evidence for L1: baseline is already nonzero (4); the synthetic token did not match this policy, but the policy explicitly describes its patterns as a recall floor (`.ufo/waves/round-18/frozen/c1-policy.json:29`).
- No tools were installed or updated. No build, test, lint, or formatter was run. No blockers.
