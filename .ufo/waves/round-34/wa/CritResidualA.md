measured 2026-10-23T06:05:31Z

# Round 34 wave A — critic: C1 residual (a) and tool provenance

Lane tip attacked: `8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3` (master).
Judged object: `tools/mori-disk-rate.py`, blob `c7ea8bdac9c98b8d350a489fb8aca3a4750bcfbf`,
sha256 `370932deb525b95135f0c30e4caaf2666b95c6feeffe76b70f06b48c09caa74b` — byte-identical at
`ba525e1a0394154837eea5090e8bd27ed69c539c` (landing commit) and at the tip.
Sources: contract `.ufo/waves/round-34/contract.md`, counter `.ufo/waves/round-34/count-c1-a1.py`,
provenance `.ufo/waves/round-34/evidence/c1-tool-provenance.txt`.
Scratch: `/fast/scratch/hyaku/mori-r34/a2-critresiduala/`. No lane git/jj writes; no file written
in the lane except this report.

## Verdict

VERDICT: claimed operation

The landed tool is the claimed operation, not an echo of the counter. It is structurally incapable
of being an echo, it reads only the two declared sources, and it diverges from the oracle on an
input class the counter never generates — a copy of the oracle cannot diverge from it.

Two defects are reported below, neither of which is a counter-keying defect:
(1) the provenance receipt's non-access claim is contradicted by the artifact;
(2) the L1's live-arm fix is conformance to the counter's fed-live handshake, not an independent
correctness fix, and the receipt's framing of it is misleading.

## The attack, and why it fails

Six counter-keying vectors were checked against the tool bytes at the tip. Each is answered by
direct evidence, not inference.

**1. Detecting the counter's FIFO.** The landed tool has no FIFO detection: no `import stat`, no
`os.stat`, no `S_ISFIFO` (grep over `tool.py`: zero hits). `read_live_samples` (tool.py:175-184) is
three statements — read, sleep, read — with no mode inspection. The *draft* did detect a FIFO
(`ExecDiskRateTool/clone/tools/mori-disk-rate.py:184-187`), and the L1's fix deleted that branch
(receipt diff, verified byte-for-byte against the sandbox clone). The landed tool therefore cannot
distinguish a FIFO from a regular file, so it cannot be branching on the counter's harness.

**2. Detecting the counter's tmpfs or namespace.** No namespace or mount probing exists in the tool
(grep: no `tmpfs`, `unshare`, `namespace`, `setpriv`, `mount`, `getenv`, `environ`, `/proc/self`).
Under the counter's exact A1 sandbox (`unshare --user --map-root-user --mount` + tmpfs over `/home`
and `/fast` + `setpriv --bounding-set=-all`), an `strace -f` of the tool shows only
`/proc/diskstats`, `/sys/class/block/*`, and libc/`setpriv` reads — no `/home`, no `/fast`, no
`.ufo`, no counter path (`a1_trace.txt`).

**3. Special-casing interval 400.** The counter's fed-live uses `ms = 400` (count-c1-a1.py:312).
The tool contains no literal `400` (grep: zero hits). It works unchanged at `--interval-ms 300`
(live run) and 1000 (counter runs).

**4. Reading anything besides `/proc/diskstats` and `<sysfs>/class/block`.** `strace -f -e
trace=openat` of the offline arm touches only the two `--a`/`--b` files and `<sysfs>/class/block/*`
(`trace_offline.txt`); the live arm touches only `/proc/diskstats` and `/sys/class/block/*`
(`trace_live.txt`). The one other `/proc` read, `/proc/sys/vm/overcommit_memory`, is emitted by the
bare interpreter too (`b2.txt`, `python3 -c pass`), not by the tool.

**5. Structural copying of the oracle functions.** The oracle exposes `parse()` (count-c1-a1.py:41),
`classify()` (:56), `oracle()` (:73). The tool exposes `parse_sample()` (tool.py:90),
`classify()` (:187), `sysfs_block_names()` (:202), `device_state()` (:210), `build_report()` (:227)
and an argparse CLI (:257). The data models differ: the oracle's `parse` returns
`{name: ("ok"|"bad", value)}` by dict overwrite; the tool's `parse_sample` returns a tuple
`(sectors, malformed)` where `malformed` is a separate set. The tool cannot import the counter:
grep finds no `subprocess`, `importlib`, `exec`, `eval`, `__import__` or `popen` in it.

**6. Decisive: the tool and the oracle disagree.** On a sample where one device name appears twice,
first with a malformed line and then a good one, the tool reports `bad-line` and the oracle reports
`ok` with a rate:

```
input A: " 8 0 dd 1 2 3 4 5 6 9 10 xx 12 13 14 15 16 17 18 19"   (malformed)
         " 8 0 dd 1 2 3 4 5 6 9 10 55 12 13 14 15 16 17 18 19"   (good)
TOOL   : {'class': 'unknown', 'state': 'bad-line', 'write_Bps': None}
ORACLE : {'class': 'unknown', 'state': 'ok', 'write_Bps': 0}
```

Cause: the oracle's `parse` collapses each name by last-write-wins (count-c1-a1.py:51-52), so the
good line erases the bad one; the tool keeps a separate `malformed` set (tool.py:100-107) and
`device_state` gives `bad-line` precedence (tool.py:212-213). The tool's behaviour is the one the
contract's R5 wording ("bad-line (a bad line in either sample)") describes; the oracle's is not.
An oracle copy would agree with the oracle. This one does not.

**It computes the declared rates from its inputs.** Fed two generated samples over the host's real
device names through a FIFO on `/proc/diskstats` — with a writer protocol I wrote, not the
counter's — the tool reports `write_Bps = 1706666` for every device, which is exactly
`1000 sectors * 512 * 1000 // 300` (`indep_fed2.py`). The claim's operation is performed, not
echoed.

## Counter runs I executed (independent of the L1's receipts)

Frozen counter, unmodified, at the tip: `python3 .ufo/waves/round-34/count-c1-a1.py
8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3` → `fixed_pass=12/12 random_pass=300/300 coverage=ok
live=ok C1=met` (seed 9249322405757227811, `counter_tip.txt`). Three further fresh seeds (111, 222,
333) → `C1=met`, `live=ok` each. The L1's own receipt (`evidence/c1-after.txt`) reports the same at
`ba525e1`.

## Defect 1 — the provenance receipt's non-access claim is unsupported

`evidence/c1-tool-provenance.txt:2` states the draft was "written from contract text, not given this
counter". The counter was nonetheless present and readable in that seat's sandbox, byte-identical to
the frozen one:

- `/fast/scratch/hyaku/mori-r34/ExecDiskRateTool/clone/.ufo/waves/round-34/count-c1-a1.py`
  — sha256 `c14c3494d7356fa7c619a0e30c10cd9b71baa99eb0fb74cfd34c7f21b3b181e2`, identical to the
  lane's frozen counter at the same path.
- It is in the seat's clone HEAD `b9fb029` as blob `6cb6c484df924202bb62c0ae266ac98ebb71740f` —
  the same blob the lane has at `b9fb029`.

So the draft author had the counter's oracle available in the working tree. The receipt does not
disclose this, and "not given" is not the same as "not present". This does **not** make the tool an
echo — the structural and behavioural evidence above is independent of authorship, and the tool
diverges from the oracle — but the receipt's provenance sentence is unsupported as written, and the
process-evidence clause of contract residual (a) ("The lane tool is written by a seat that is not
given this counter", contract.md:83-86) rests on it.

Smallest safe correction: append one line to the receipt recording that the counter was present in
the seat's clone at `b9fb029` and that the tool's divergence from the oracle (duplicate-name case)
is the evidence that it was not derived from it. Nothing else changes; no counter, rule or seed
changes.

## Defect 2 — the live-arm fix is counter-handshake conformance, and the receipt frames it as a
## correctness fix

The receipt (lines 4-5) attributes the draft's `fed-no-interval` failure to the draft holding a
FIFO open across the sleep, and presents the fix as "the live arm opens, reads and closes the file
for each sample". The receipt's own measured line for the draft is `live=fed-no-interval`, and the
counter's `fed_live` fails that way when `marks["b_opened"]` is never set (count-c1-a1.py:356-359),
i.e. when the writer's ENXIO probe never observes the reader closing sample A
(count-c1-a1.py:322-331). I reproduced both states with the frozen counter: draft rev `54dc8567`
→ `live=fed-no-interval C1=unmet`; fixed rev `e94e0767` → `live=ok`.

But the draft was not broken. Under an independent FIFO writer protocol — serve A, close, sleep
0.4 s, reopen and serve B, the protocol in the dead seat's own harness
(`ExecDiskRateTool/tests/fed_live.sh:33-42`) — the draft produced the correct result
(`write_Bps = 1706666`, all devices `ok`), the same as the landed tool. The draft also ran correctly
against the real `/proc/diskstats`, where a second `read()` from the same fd returns 0 bytes
(`recheck.py`), so its open-twice branch was already the correct one for a regular file.

So the fix changed behaviour on exactly one path — the FIFO path — and the FIFO path exists only in
the counter's fed-live harness, which binds a FIFO over `/proc/diskstats` (count-c1-a1.py:339). The
fix made the tool conform to the counter's reader-close handshake. That is a legitimate change and
it does not make the tool counter-keyed: open/close/open is the correct way to obtain two fresh
samples of a file, and the landed tool applies it unconditionally. But the receipt's framing —
"the draft held a FIFO open across the sleep", presented as a defect of the draft — is misleading:
the draft was correct against a FIFO written the way the seat's own harness wrote one, and wrong
only against the counter's particular handshake.

Smallest safe correction: amend the receipt's process note to say the fix was made by the counter's
author to satisfy the fed-live reader-close handshake, that the draft was independently correct
against a FIFO written with an interval between samples, and that the landed tool's behaviour is
unconditional and therefore not harness-specific. No change to the tool, the counter, the rules or
the seed count.

## Observation for wave 2 — the oracle's R5 reading is the weaker one

Contract residual (c) (contract.md:83-88) sends each rule back to its source. On the duplicate-name
case the tool follows R5's wording and the oracle does not (see the divergence above). The oracle's
generator never emits two lines for one name in one sample (count-c1-a1.py:180-204) and real
`/proc/diskstats` never contains a repeated device name (`awk '{print $3}' /proc/diskstats | sort |
uniq -d` → empty), so the divergence is inert and affects no scored scenario. It is a fidelity note
on the frozen oracle, not a defect of the tool, and it is not mine to fix.

## Impacted axes

- C1 coverage: unaffected. The tool is the claimed operation; it is not an echo, and it is not
  counter-keyed on any of the six vectors.
- Provenance / process evidence: Defect 1 (unsupported non-access claim) and Defect 2 (misleading
  fix rationale) both bear on residual (a). Neither is inside P-C1-A1, which the contract states is
  authorship-independent (contract.md:83-86); both are reportable under that residual without
  touching the frozen counter, rules or seed count.
- C2 calibration: not attacked here.

## Limits of this review

- I did not attempt to break the counter itself; only the tool was attacked.
- The `/fast` FIFO namespace work ran inside `unshare --user --map-root-user --mount` sandboxes
  with tmpfs overlays over `/home` and `/fast`, as the counter does. No block device was created or
  attached, nothing under `/sys` was written, no lane or fleet repository was mutated, and no
  process I started outlived this review.
- The dead attempt-1 draft was read only as a lead and independently re-verified (I re-ran the
  frozen counter against both sandbox revisions myself); nothing from `.ufo/waves/round-34/w1/` is
  cited as evidence.

## Tooling

No tool was installed or updated for this review. `strace` (already present at `/usr/bin/strace`) was
used for the syscall traces; `python3` 3.14 and `git` (read-only) were used from the base system.
