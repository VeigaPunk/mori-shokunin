measured 2026-10-23T07:51:07Z
# CritQ99Gap — criterion 99

VERDICT: 99 gap found

## Scope and axes

Axes attacked: **calibration** (whether the proposed shortcut battery establishes discrimination), **coverage** (R4's device union), and **operability/depth** (R2's numeric validity). The round names C1 coverage and C2 calibration in `.ufo/waves/round-34/contract.md:11-18,90-97`; the missing operations are explicit at `contract.md:34-47`.

Target: attempt-2 draft `/fast/scratch/hyaku/mori-r34/a3-L1/drafts/corpus_QUALITY.md:733-746`, especially its two controls and real-input two-sided bounds at lines 735-742. This draft is the object reviewed, not evidence of historical behavior.

Let `S=/fast/scratch/hyaku/mori-r34/a3-CritQ99Gap`, `C=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-34/count-c1-a1.py`. Two candidate programs only, committed in `S/clone`; baseline checkout command returned `HEAD is now at fd25213 round-34: wave A spec/dispatch (52 seats, attempt 2) before dispatch`. No lane commits.

## Candidate 1 — skip the full sysfs-only device union

VERDICT: C-sysfs-union survived

Revision `e5296e518dd5f9c1ccb95e30868ec236f001bb8c`. The sandbox commit changed only `sysfs_block_names`: retain only entries having a `partition` attribute instead of every block entry (`S/clone` at that revision, `tools/mori-disk-rate.py:202-209`; commit output: `1 file changed, 3 insertions(+), 1 deletion(-)`). Sampling, real sysfs classification, state logic and arithmetic remain the baseline operations.

This skips R4's enumeration of sysfs-only disks, stacked devices and virtual devices; it is not device-name classification, zero-rate substitution or FIFO-only sampling. R4 requires the complete union (`contract.md:43`; frozen oracle `C:79-85`).

Why the generated cases miss it: the generator omits both sample lines only in the `partition` branch (`C:180-203`, particularly 189-190). Consequently a sysfs-only non-partition is absent from that population even when all five classes and all six states are seen. Fed-live supplies a line for every real sysfs name (`C:302-311`).

Concrete witness: empty A and B, with `sys/class/block/sentinel/{device,slaves}` present. The candidate returns no devices; the frozen oracle requires `sentinel: {class: disk, state: absent, write_Bps: null}` and `host_basis: [sentinel]` (`S/probe-gap.py:20-24,30-40`; `S/witnesses.txt:2-7`).

Full frozen-counter receipt (`S/census-counter.txt:1-9`):

```text
measured_at=2026-10-23T07:47:38Z repo=/fast/scratch/hyaku/mori-r34/a3-CritQ99Gap/clone rev=e5296e518dd5f9c1ccb95e30868ec236f001bb8c
tool=present guard=clean seed=7618581794714252961
fixed_pass=12/12 random_pass=300/300
states_seen=['absent', 'bad-line', 'gone', 'new', 'ok', 'reset'] classes_seen=['disk', 'partition', 'stacked', 'unknown', 'virtual'] coverage=ok
live=ok
C1=met
exit=0
elapsed_seconds=11.345
```

## Candidate 2 — skip unsigned-decimal validation

VERDICT: C-validation-vocabulary survived

Revision `60c6167b06f2098c593f30b53fa6aa913dd29037`. This restores the full sysfs union and replaces unsigned-decimal validation with rejection of only characters in `-x.+?` (`S/clone/tools/mori-disk-rate.py:97-106,200-205`, at that revision). It still parses the actual sector counters, reads real sysfs attributes and samples twice; its unchanged live reader is at lines 173-182. This is a separate defect from candidate 1 and from the name/FIFO/zero shortcut described by the draft at lines 745-746.

Why it survives: the generator's malformed-token vocabulary is `-1`, `x`, `1.5`, `0x1f`, `+3`, and `?`; every one contains a blacklisted character. The independent wrong-token-count check remains (`C:131-142`; candidate source lines 97-104). No arbitrary unsigned-decimal validation occurs.

Concrete witness, interval 1000 ms:

```text
A: 8 0 sentinel oops 0 0 0 0 0 100 0 0 0 0
B: 8 0 sentinel oops 0 0 0 0 0 110 0 0 0 0
candidate: class=disk state=ok write_Bps=5120 host_write_Bps=5120
frozen oracle: class=disk state=bad-line write_Bps=null host_write_Bps=null
```

Both lines have 14 tokens, but `oops` violates R2 (`contract.md:35-36`; `C:41-52`). Actual witness output: `S/witnesses.txt:8-14` (`same=False`, command exit 0).

Full frozen-counter receipt (`S/lexical-counter.txt:1-9`):

```text
measured_at=2026-10-23T07:47:38Z repo=/fast/scratch/hyaku/mori-r34/a3-CritQ99Gap/clone rev=60c6167b06f2098c593f30b53fa6aa913dd29037
tool=present guard=clean seed=10903623619850494145
fixed_pass=12/12 random_pass=300/300
states_seen=['absent', 'bad-line', 'gone', 'new', 'ok', 'reset'] classes_seen=['disk', 'partition', 'stacked', 'unknown', 'virtual'] coverage=ok
live=ok
C1=met
exit=0
elapsed_seconds=11.349
```

## Would 99 cover these?

The following is a coverage assessment **[INFERENCE]**, not a claim that an unimplemented 99-compliant counter was run:

| Candidate | (i) Every-output label-keyed control | (ii) Harness-keyed control | Real-input two-sided bound |
|---|---|---|---|
| Sysfs union | No: it uses actual sample counters and sysfs attributes, not generator names as answers. | No: the same truncated union runs everywhere; no harness detector or real-input constant. | Not on the exercised host: even exact full-JSON equality accepted it. An absent non-partition requires a separate membership fixture. |
| Validation vocabulary | No: outputs depend on actual counters and sysfs, not names/ids/labels. | No: the same incomplete validator runs everywhere, not work only inside a detected harness. | Not on the exercised host: exact full-JSON equality accepted it. Numeric bounds do not require testing an ungenerated malformed token. |

Stronger-than-bounds diagnostic: two shared real `/proc/diskstats` samples 300 ms apart were passed to both candidate report functions and the unchanged frozen oracle. Both complete JSON objects matched exactly across the 11 observed devices (`S/probe-real-bound.py:18-33`; `S/real-bound.txt:1-6`):

```text
case=census shared_real_samples=2 interval_ms=300
real_host_devices=11 exact_json_equal=True
case=lexical shared_real_samples=2 interval_ms=300
real_host_devices=11 exact_json_equal=True
exit=0
```

This diagnostic is not a replacement C1 run or an implemented lower-bound check. It demonstrates why merely tightening real-host rate bounds cannot force discovery of these two semantic omissions on those inputs. Unseen future host populations and future control implementations were not tested.

## Smallest safe correction

Keep 99 as the specific label/harness/constant-output repair, but explicitly state that its controls and bounds are **not a certificate of rule-level discrimination**. To cover these demonstrated omissions in a future contract, add pre-data skip controls for (a) dropping sysfs-only non-partitions and (b) replacing general numeric validation with the generator's finite corruption vocabulary; score them against fixtures containing an absent disk and a non-decimal token outside that vocabulary, with exact device-set/state assertions (`S/witnesses.txt:2-13`).

This is a fixable discrimination/criterion-scope defect, not a proposed beneficial tradeoff. It does not refute 99's narrower claim about catching the particular `ef936fb4` shortcut, and it does not change either recorded `C1=met` receipt. Do not amend the frozen counter, rules or count; disposition of the round remains with the canonical judge (`contract.md:62-63,123-140`).

## Execution and containment

Each counter executed the requested inner command `timeout 600 python3 "$C" <revision> --repo "$S/clone"`, with no seed/count override. Exact outer commands are in `S/census-counter.txt:1` and `S/lexical-counter.txt:1`: 1 GiB address-space and 16 MiB per-file limits, a private mount namespace binding that candidate's scratch temporary directory onto `/tmp`. Thus the counter's temporary paths remain visible after its `/fast` hide without placing scratch outside the assigned directory. Both full runs completed concurrently, exit 0; both diagnostic commands completed, exit 0 (receipts above).

No tools installed or updated. No write-load files, block-device changes, lane Git writes, or background jobs were used. Report timestamp is the output of `timeout 120 sh -c 'ulimit -v 1048576; date -u +%FT%TZ'`: `2026-10-23T07:51:07Z`.
