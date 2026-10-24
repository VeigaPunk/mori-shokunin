measured 2026-10-23T07:49:58Z

# Independent C1 shortcut rescore

Axes: C1 coverage validity; C2 calibration/discrimination; byte identity/provenance; containment. This is a technical review, not canonical admission or integration.

Paths below are relative to `/home/vgpnk/Projects/shokunin/mori-shokunin` unless absolute. Aliases: P = `.ufo/waves/round-34/evidence/ctl-postdata-shortcut/mori-disk-rate.py`; C = `.ufo/waves/round-34/count-c1-a1.py`; Q = `.ufo/waves/round-34/wa/CritPostDataShortcut.md`; K = `.ufo/waves/round-34/contract.md`; S = `/fast/scratch/hyaku/mori-r34/a3-CritShortcutRescore`. Alias citations retain the indicated path and line numbers.

## Independent finding, before reading Q

VERDICT: shortcut meets P-C1-A1
VERDICT: defect — the frozen counter does not distinguish this shortcut from the intended operation.

Both independent shortcut executions passed, as did the actual judged tool. This supports the honest-stop diagnosis about counter discrimination, not a claim that the real tool omits the work. The literal receipt remains `C1=met`; do not relabel it `C1=unmet`. Evidence: receipts below; C:406-419; real tool `tools/mori-disk-rate.py:175-199`.

Independence was recorded in `S/independent-verdict.txt:1-10` before opening Q. The prior report was subsequently treated as an audit object, never as evidence for the reruns.

### Byte identity

Executed, with timeout and memory caps: `git -C /fast/scratch/hyaku/mori-r34/a2-CritPostDataShortcut/clone show ef936fb4e0834d0a1ce676aef735debe2eef9d27:tools/mori-disk-rate.py | sha256sum` returned `cd5389b9790945dd6f9993f6516cc888ceb283426661207f947286254efcc8c6  -`. `sha256sum P` returned the same digest. Thus the untracked probe bytes match the sandbox revision being scored.

`git -C S/shortcut-clone show -s --format=%H%n%s ef936fb4e0834d0a1ce676aef735debe2eef9d27` returned that full revision and `probe: skip live two-sample read + R3 attributes`. Read-only `git ls-tree fd2521351c6cef47384aef30afbe1e4db7e6912e P Q tools/mori-disk-rate.py` listed only the actual tool: blob `c7ea8bdac9c98b8d350a489fb8aca3a4750bcfbf`. The probe/report are not evidence committed at the judged lane tip.

`git show fd2521351c6cef47384aef30afbe1e4db7e6912e:tools/mori-disk-rate.py | sha256sum` and the same command at `ba525e1a0394154837eea5090e8bd27ed69c539c` both returned `370932deb525b95135f0c30e4caaf2666b95c6feeffe76b70f06b48c09caa74b`. Current C and `git show fd2521351c6cef47384aef30afbe1e4db7e6912e:C` both hashed to `c14c3494d7356fa7c619a0e30c10cd9b71baa99eb0fb74cfd34c7f21b3b181e2`.

### Exactly what the probe skips

- It never opens or stats per-device `partition`, `slaves`, or `device` entries. It stats/lists only `<sysfs>/class/block`, then classifies by names: missing name -> unknown; dm/md pattern -> stacked; loop/zram/ram pattern -> virtual; extension of another listed name -> partition; otherwise disk. Evidence: P:18-20,39-68; observed trace `S/shortcut-live.trace:255-261`.
- Regular `/proc/diskstats`: exactly one open/read; no interval sleep; `fake()` supplies zero rates. FIFO: first read, type check, sleep, second read, computed deltas. Evidence: P:113-129,149-158. The trace shows `/proc/diskstats` is `S_IFREG`, one open, then only block-class enumeration: `S/shortcut-live.trace:255-261`.
- Real-host command: `timeout --kill-after=1 30 prlimit --as=2147483648 --cpu=25 -- strace -e trace=openat,newfstatat,getdents64,clock_nanosleep -o S/shortcut-live.trace python3 P --interval-ms 1000`; exit 0. All 11 devices were `ok`, all rates 0 B/s; basis `[nvme0n1,nvme1n1,sda,sr0]`, host rate 0. Devices: dm-0, nvme0n1, nvme0n1p1, nvme0n1p2, nvme1n1, nvme1n1p1, nvme1n1p2, sda, sda1, sda2, sr0. Evidence: `S/shortcut-live.json:1`. This is fabricated zero, not measured inactivity: P:120-122.
- The source does not universally mark every possible device ok: malformed/missing lines produce bad-line/absent (P:119-122). All 11 happened to be valid on this host. Short input lines are incorrectly retained as devices (P:28-32), whereas C:48-49 ignores them.

The defect is behavioral, not merely a different equivalent classifier: a harmless fixture with `class/block/loop0/device` makes R3 classify loop0 as disk, but the probe returns virtual. A one-token `orphan` sample creates a bad-line device instead of no device. Both direct probe executions exited 0. Evidence: `S/class-counterexample/sys/class/block/loop0/device`, `S/class-counterexample/short.diskstats:1`, `S/audit-counterexamples.txt:1-6`; C:56-70,41-53.

### Required receipts

Both clones were created with `timeout 120 prlimit --as=2147483648 --cpu=100 -- env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone --no-hardlinks SOURCE DEST`: shortcut source was the attempt-2 sandbox clone; actual source was the lane; destinations were `S/shortcut-clone` and `S/real-clone`. Both commands returned `done.`

For each run: `timeout --kill-after=1 600 prlimit --as=2147483648 --cpu=550 -- python3 C REV --repo CLONE`. No `--seed` or `--random` override; C:403-407 obtains each fresh seed and draws 300 cases. The three runs were concurrent; all exited 0. Full receipt text is retained at the cited scratch paths.

`S/shortcut-1.txt:1-7`:
```
measured_at=2026-10-23T07:45:07Z repo=/fast/scratch/hyaku/mori-r34/a3-CritShortcutRescore/shortcut-clone rev=ef936fb4e0834d0a1ce676aef735debe2eef9d27
tool=present guard=clean seed=17370950472440198283
fixed_pass=12/12 random_pass=300/300
states_seen=['absent', 'bad-line', 'gone', 'new', 'ok', 'reset'] classes_seen=['disk', 'partition', 'stacked', 'unknown', 'virtual'] coverage=ok
live=ok
C1=met
exit=0
```

`S/shortcut-2.txt:1-7`:
```
measured_at=2026-10-23T07:45:07Z repo=/fast/scratch/hyaku/mori-r34/a3-CritShortcutRescore/shortcut-clone rev=ef936fb4e0834d0a1ce676aef735debe2eef9d27
tool=present guard=clean seed=2169686788252312620
fixed_pass=12/12 random_pass=300/300
states_seen=['absent', 'bad-line', 'gone', 'new', 'ok', 'reset'] classes_seen=['disk', 'partition', 'stacked', 'unknown', 'virtual'] coverage=ok
live=ok
C1=met
exit=0
```

`S/real.txt:1-7`:
```
measured_at=2026-10-23T07:45:07Z repo=/fast/scratch/hyaku/mori-r34/a3-CritShortcutRescore/real-clone rev=fd2521351c6cef47384aef30afbe1e4db7e6912e
tool=present guard=clean seed=13134198396424284015
fixed_pass=12/12 random_pass=300/300
states_seen=['absent', 'bad-line', 'gone', 'new', 'ok', 'reset'] classes_seen=['disk', 'partition', 'stacked', 'unknown', 'virtual'] coverage=ok
live=ok
C1=met
exit=0
```

### Impact and smallest safe correction

C1: observed predicate success is insufficient evidence of the intended work; it is not evidence against the real implementation. C2: the battery missed this harness-keyed/name-keyed combination; that weakens calibration, not proof that every literal QUALITY 98 checklist condition failed. Identity: retain this probe's full revision/digest and these fresh receipts, not an assertion that the probe was committed in the lane. Evidence: K:65-88,111-150; C:259-293,296-366,408-419; committed clone `S/real-clone/corpus/QUALITY.md:715-731`.

Smallest safe correction now: report the discrimination defect and preserve the frozen counter, rules, seed count and tool. Do not carry Q's proposed live fixes forward as validated fixes. Moving the live test to a FIFO still lets this probe do the work only under test; requiring positive rates rejects valid zero-rate samples. [INFERENCE] A device can write inside the outer readings but outside the tool's inner interval, so outer growth does not establish a positive inner rate. R6 explicitly permits zero (K:46-47); the counter provides only an upper bound (C:273-278).

For a separately frozen successor, a name/attribute contradiction is a demonstrated way to kill this exact classifier (`S/audit-counterexamples.txt:1-3`). Independently observe two temporally separated regular-proc reads if that operation is claimed; do not substitute a positivity heuristic for this evidence. These are recommendations, not a new counter or a claimed complete repair.

Containment: no lane/fleet git writes, integration, canonical/orchestrator runtime invocation, package installation/update, background jobs, block-device operations, or write load. Direct artifacts were written only to S and this report. The expressly assigned canonical counter itself creates/removes temporary work via `tempfile.mkdtemp` (C:244-255,313-353,397-421); this is not a claim that its internal writes stay under S. All started commands were timeout/memory capped; the concurrent runner waited for completion and killed any remaining process group it owned. No other process was signalled.

## Audit of .ufo/waves/round-34/wa/CritPostDataShortcut.md

Each item attacks the stated claim in Q. `disagree — unverified` means exclude it from this round's evidence, not that its historical event was disproved. Prior timestamps, process histories, and old receipts are not authenticated by a present-day successful rerun.

VERDICT: agree — A01, Q:7-9: the probe meets the frozen predicate while skipping real-host two-sample measurement and R3 metadata access. Evidence: fresh receipts above; P:39-68,149-158; trace:255-261.
VERDICT: agree — A02, Q:10-11: receipt success does not distinguish this skip-work program from the intended operation. Evidence: both probe receipts and actual-tool receipt above; K:13-18.
VERDICT: agree — A03, Q:25-28: the named sandbox revision and subject identify the scored probe. Evidence: git show/hash commands above. This does not authenticate historical cloning procedure.
VERDICT: agree — A04, Q:32-36: regular-file mode reads once and returns zeros; FIFO mode reads twice. Evidence: P:149-158; trace:255-261; live JSON:1. Universal ok status is bounded to valid lines, as P:119-122 shows.
VERDICT: agree — A05, Q:37-41: class comes from listed names/patterns, not per-device metadata. Evidence: P:18-20,39-68; class-contradiction output `S/audit-counterexamples.txt:1-3`.
VERDICT: agree — A06, Q:42-44: short lines are retained, and the offline generator never emits fewer-than-three-token lines. Evidence: P:28-32; C:131-142,145-210; short-line output `S/audit-counterexamples.txt:4-6`.
VERDICT: disagree — A07, Q:46-66: the original two timestamps/seeds/exits and both-fresh label are unverified historical claims. Our two omitted-seed runs independently prove the substantive repeated pass; they do not authenticate those old executions. Evidence: fresh commands/receipts above; C:403-404.
VERDICT: disagree — A08, Q:68-70: the separate original pre-score differential harness execution is unverified. Current 312/312 and host-class success are independently established by our receipts, not by the alleged historical harness.
VERDICT: disagree — A09, Q:74-76: zero does not satisfy the bound for every device always. A falling outer counter makes the bound negative and rejects zero. Evidence: C:275-278. For valid nondecreasing outer counters, zero does satisfy this inequality.
VERDICT: agree — A10, Q:77-78: presence and ok/integer requirements do not themselves reject zero. Evidence: C:279-289.
VERDICT: agree — A11, Q:79-84: temporal two-read enforcement is in the FIFO arm, and successful live() leads to fed_live(). Evidence: C:318-365,408; two fresh live=ok receipts.
VERDICT: agree — A12, Q:85-88: the counter checks class values, not metadata-access provenance; current generated names correlate with classes. Evidence: C:111-178,233-238,271-272,364-365; P:58-68 reproduces all scored cases.
VERDICT: agree — A13, Q:94-95: the actual landed tool has two live reads and R3 metadata checks. Evidence: tools/mori-disk-rate.py:175-199; matching ba525e1/fd252135 tool digests above. Metadata existence/listing checks need not open attribute contents.
VERDICT: disagree — A14, Q:95-96: the historical 54613 B/s readings are unverified and are not needed for this finding. Our actual-tool receipt validates the predicate now, not that past host rate.
VERDICT: agree — A15, Q:97-99: on this host the probe reports the listed 11 devices with zero rates while passing. Evidence: S/shortcut-live.json:1 and both fresh shortcut receipts.
VERDICT: disagree — A16, Q:101: cheapest available is not established by the explored alternatives. The supported claim is fewer required reads/metadata operations, from P:39-68,149-158 versus tools/mori-disk-rate.py:175-199; no global minimum or benchmark was established.
VERDICT: agree — A17, Q:103-106: the described hide/capability-drop command matches the counter's isolation construction. Evidence: C:215-222,339-344. This verifies command structure, not historical execution of all listed probes.
VERDICT: disagree — A18, Q:108-110: original nested-namespace failure and the no-way-back causal conclusion were not independently reproduced; do not cite as new isolation proof.
VERDICT: disagree — A19, Q:111-112: original nested-mount failure and locked-mount diagnosis were not independently reproduced; do not cite as new isolation proof.
VERDICT: disagree — A20, Q:113-114: original parent-root denial, host Yama value, and exclusive causal attribution were not independently checked. None is needed for this shortcut finding.
VERDICT: disagree — A21, Q:115-118: /tmp is not the only visible/writable tree. Under the same hide/capability-drop operations, os.access reports /var/tmp and /dev/shm both present and writable. No write there was attempted. Evidence: S/audit-counterexamples.txt:7-9; C:219,339-340.
VERDICT: agree — A22, Q:122-126: the actual tool and shortcut receive indistinguishable success receipts; frozen-counter discrimination is defective. Evidence: three fresh receipts and K:62-63,131-140. This does not turn the literal predicate result into unmet or issue a canonical admission decision.
VERDICT: agree — A23, Q:127-132: the table does not name this populated-zero, FIFO-detecting/name-derived combination; the cited older control failures are accurately recorded. Evidence: K:69-79,145-146; evidence/c1-controls.txt:38-43. Read-only git show of 8e7c6867cd701596cfed5ac4af4d8da2a22e325d:tools/mori-disk-rate.py confirms its unconditional single-read/no-sleep live arm.
VERDICT: disagree — A24, Q:132-133: missing this subcase does not by itself prove QUALITY 98's literal category mapping failed. Skip-work and label-keyed categories are already mapped (K:71,77); criterion 98 checks named categories/receipts/ancestry, not exhaustive harness fingerprints (S/real-clone/corpus/QUALITY.md:715-731). Calibration is weakened; the stronger formal conclusion is unsupported.
VERDICT: disagree — A25, Q:139-142: using the same FIFO discipline is not sufficient to expose the regular-file shortcut; this very probe already passes that discipline twice. Evidence: P:154-158; C:339-365; our fresh receipts.
VERDICT: disagree — A26, Q:140-142: a positive-rate requirement is not a safe general correction and kills no all-zero case when no outer counter rises. Valid ok rates can be zero (K:46-47). [INFERENCE] Outer-only growth can coexist with an idle inner interval, yielding a false rejection.
VERDICT: agree — A27, Q:143-145: a generated class/name contradiction kills this exact name-derived classifier. Evidence: harmless loop0/device fixture and returned virtual class at S/audit-counterexamples.txt:1-3; oracle disk rule C:56-70.
VERDICT: agree — A28, Q:147-148: the counter and real tool remain byte-identical to the judged committed versions now. Evidence: counter/tool digests above. This establishes present identity, not historical custody.
VERDICT: disagree — A29, Q:152-158: the prior author's complete write history, absence of installations, command caps, and process cleanup are unverified historical claims. This review supplies its own containment account instead.
VERDICT: disagree — A30, Q:158: no writes outside scratch/report is too broad for canonical counter execution: its default temporary fixtures and extracted tool are created through mkdtemp, not a seat-scratch path. Evidence: C:244-255,313-353,397-421. Distinguish direct seat artifacts from counter-managed transient files.
AUDIT: agree 16 / disagree 14
