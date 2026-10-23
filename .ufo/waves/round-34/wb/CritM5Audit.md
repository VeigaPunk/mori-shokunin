measured 2026-10-23T07:55:47Z

# M5 provenance and interval audit

Axes: provenance accuracy; nominal-R6 rate correctness; oracle independence; FIFO interoperability; timing precision.

Paths: `L` = `/home/vgpnk/Projects/shokunin/mori-shokunin`; `E` = `/fast/scratch/hyaku/mori-r34/a3-CritM5Audit`; `P` = `/fast/scratch/hyaku/mori-r34/a3-L1/drafts/corpus_lessons_round-34.md`.
I recorded independent conclusions before opening either attempt-2 report (`E/independent-findings.txt:1-8`). This is a scoped criticism, not a C1 judgment; the frozen tool, counter, rules and seed count remain unchanged.

## Independent checks of M5

VERDICT: agree — M5:100-101: the counter was byte-present in the identified draft seat's clone. The draft at `/fast/scratch/hyaku/mori-r34/ExecDiskRateTool/clone/tools/mori-disk-rate.py` hashes to the receipt's exact `583cc423df49f1717d78b7ccd782e3c13fc2fd6271bd884e551afd42afdc98f1`. Clone HEAD `b9fb029e05dcfb79757c46821dc4b61cb79d1a29` tracks counter blob `6cb6c484df924202bb62c0ae266ac98ebb71740f`; committed and working clone counter bytes equal the lane's SHA256 `c14c3494d7356fa7c619a0e30c10cd9b71baa99eb0fb74cfd34c7f21b3b181e2` (`E/identity.json:2-7,22`). Availability is established; actual consultation or what appeared in the original prompt is not.

VERDICT: agree — M5:102: the draft already computes the specified nominal rates from regular files. A saved-file CLI run exited 0; a live regular-file update from sectors 100 to 104 at 200 ms produced 10240 Bps, exactly `4*512*1000//200` (`E/witnesses.json:2-52`). Capturing its actual `/proc/diskstats` reads independently checked all 11 reported devices against R6; the host result was 737280 Bps (`E/live-protocol.json:59-76`). This establishes R6 arithmetic, not equality to a measured-time physical rate.

VERDICT: agree — M5:101-103, with a necessary qualification: the L1 change repairs the frozen counter's FIFO reader-close interoperability, not regular-file arithmetic. `git show ba525e1a0394154837eea5090e8bd27ed69c539c -- tools/mori-disk-rate.py` shows the 300-line landed addition. Direct comparison against the hash-identified draft shows only removal of `import stat`, removal of the stat/FIFO branch, and replacement of the live docstring; the regular-file read/sleep/read sequence is unchanged (`E/draft-vs-ba.diff:3-47`).
Under the counter's reader-close protocol, my draft run returned A and an empty B (`gone/null`), whereas the landed tool obtained both samples (`ok/5120` at 400 ms); its writer-marker gap was 398.172104 ms (`E/live-protocol.json:2-56`). Under the original seat's write-A/close/sleep-400-ms/reopen/write-B protocol, both tools returned 1706666 Bps for all 11 real host names with nominal interval 300 ms (`E/audit-probes.json:2-26`; original protocol `/fast/scratch/hyaku/mori-r34/ExecDiskRateTool/tests/fed_live.sh:33-47`). The draft also works with a persistent writer (`E/witnesses.json:54-73`). Thus “only” must not erase the real FIFO behavior change or imply that failing the frozen predicate was not a defect of conformance.

VERDICT: agree — M5:104-105: the landed tool and the frozen oracle diverge on a duplicate-name sample. I built and executed this witness, with a fake sysfs disk entry and interval 200 ms:

```
A: 8 0 sda
   8 0 sda 0 0 0 0 0 0 100 0 0 0 0
B: 8 0 sda 0 0 0 0 0 0 104 0 0 0 0
```

The landed CLI exited 0 with `bad-line/null` and host null. The frozen oracle returned `ok/10240` and host 10240; reversing A's lines made the oracle return `bad-line/null` (`E/witnesses.json:75-136`). The tool retains any malformed occurrence; the oracle overwrites by name (`L/tools/mori-disk-rate.py:90-108,210-213`; `L/.ufo/waves/round-34/count-c1-a1.py:41-53`).

VERDICT: disagree — M5:105: divergence does **not** establish “so it is no copy.” Strong counterexample: I copied the frozen oracle function's exact code object and globals, replacing only its parser with a wrapper preserving any malformed occurrence. This explicitly oracle-derived implementation diverges from the original oracle and matches the landed tool on the same witness (`E/derived-witness.json:2-48`). This is not an allegation that the actual tool used that construction. Static inspection finds no runtime oracle import or harness-probing strings (`E/identity.json:8-19`; `E/audit-probes.json:72-90`), but independent authorship remains unproved.

VERDICT: agree — M5:106-108: the docstring's divisor equality is false. The executed code sleeps the nominal interval after finishing A and uses that nominal value in R6 (`L/tools/mori-disk-rate.py:175-184,227-240`). Five timestamped real `/proc/diskstats` runs per interval gave these read-start-to-read-start gaps, in ms (`E/timing.tsv:1-11`):

| nominal | run 1 | run 2 | run 3 | run 4 | run 5 |
|---|---|---|---|---|---|
| 200 | 200.276469 | 200.239078 | 200.388449 | 200.256838 | 200.304968 |
| 1000 | 1000.210863 | 1000.264252 | 1000.276772 | 1000.213542 | 1000.251882 |

Method: thin `perf_counter_ns` wrappers immediately around real open/read/close calls; unchanged live-sampling function body, no strace or added load (`E/timing.json:1-3`). Read-window lower bounds also exceeded nominal in all ten runs (`E/timing.tsv:2-11`). Kernel counters are collected during each read, not at one atomic timestamp: the source loops over devices and calls `part_stat_read_all` in the seq-file show callback (`L/corpus/evidence/sources-r33/S182.src:1369-1391,1416-1425`). [INFERENCE] instrumentation can itself add latency; these numbers are not an uninstrumented overhead bound.

VERDICT: disagree — M5:107's numerical/universal wording is not independently established here. The ten observed excesses were +0.119539% to +0.194224% at 200 ms and +0.021086% to +0.027677% at 1000 ms (`E/timing.tsv:2-11`). They support “all ten observed gaps were longer,” not a universal empirical bound or a newly measured under-load +0.07%–+6.4% range. I did not rerun the old load sweeps.

## Smallest safe correction

Replace the non-derivation inference with: “The counter was available in the draft author's clone. The tool has no observed runtime oracle dependency and is not semantically identical to the oracle on the duplicate-name witness; independent authorship is not established.” Describe the L1 change as a genuine frozen-fed-live conformance fix while preserving the draft's already-correct regular-file R6 behavior. Replace the divisor-equality assertion in the lesson with nominal-versus-observed timing, not a change to the judged bytes (`E/identity.json:2-23`; `E/derived-witness.json:2-48`; `E/live-protocol.json:2-76`; `L/.ufo/waves/round-34/contract.md:46,83-88`).
This is fixable provenance/documentation wording. Substituting measured elapsed time would change frozen R6, so it is not a safe correction to this round (`L/.ufo/waves/round-34/contract.md:46,62-63`).

## Audit of .ufo/waves/round-34/wa/CritResidualA.md

Each numbered item below is a factual proposition the round might cite. Agreement is scoped to the cited independent evidence, not certification of old traces or executions. A disagreement marked “not re-established” does not assert that an old execution never happened.

VERDICT: agree — A1, :6-8: landed tool identity across ba525e1a, 8d56809a and fd252135 is correct (`E/audit-probes.json:55-70`).
VERDICT: agree — A2, :32-37: the landed source has no FIFO-mode inspection; the draft branch was deleted (`E/audit-probes.json:72-90`; `E/draft-vs-ba.diff:22-47`).
VERDICT: agree — A3, :39-48: no explicit namespace/mount/environment probe or literal `400` exists in the tool; it also operates at other intervals in my runs (`E/audit-probes.json:2-26,72-90`; `E/timing.tsv:2-11`). The old trace itself was not rerun.
VERDICT: agree — A4, :50-62: the source explicitly reads the supplied sample paths and sysfs and has no runtime counter-import mechanism (`L/tools/mori-disk-rate.py:72-87,111-172,187-207,278-293`; `E/identity.json:8-19`). This is source inspection, not adoption of the prior syscall trace.
VERDICT: agree — A5, :56-61: the parser data models differ: last-write-wins tagged dictionary versus sectors dictionary plus persistent malformed set (`L/.ufo/waves/round-34/count-c1-a1.py:41-53`; `L/tools/mori-disk-rate.py:90-108`).
VERDICT: agree — A6, :64-78: malformed-then-valid duplicates produce the stated disagreement; the tool preserves the “a bad line in either sample” reading (`E/witnesses.json:75-136`; `L/.ufo/waves/round-34/contract.md:44-47`).
VERDICT: agree — A7, :156: the generator appends at most one A and one B line for each unique generated name (`L/.ufo/waves/round-34/count-c1-a1.py:145-166,179-205`). This does not establish independent authorship.
VERDICT: disagree — A8, :18-20,79,114-116: disagreement with the oracle cannot prove non-derivation; my deliberately oracle-derived counterexample defeats that inference (`E/derived-witness.json:2-48`).
VERDICT: agree — A9, :81-85: the 1000-sector delta at nominal 300 ms produces 1706666 Bps on every real host name in an independently supplied FIFO sample pair (`E/audit-probes.json:2-26`). My fresh test assigned a scratch FIFO to the module path; it did not reproduce the prior mount-namespace trace.
VERDICT: agree — A10, :97-112: the counter was available in the draft clone, so clone isolation/non-access is not demonstrated by “not given” wording (`E/identity.json:2-7,22`). Actual consultation is not proved either.
VERDICT: disagree — A11, :125-126: `fed-no-interval` is **not** returned when `b_opened` is absent. Absence returns `fed-single-read`; `fed-no-interval` means the recorded B-open/A-close gap is below 0.9 times the interval (`L/.ufo/waves/round-34/count-c1-a1.py:354-359`). My draft probe had no B before cleanup; cleanup then opened B only 48.108575 ms after the recorded A-close (`E/live-protocol.json:2-28`).
VERDICT: agree — A12, :130-141: the draft's original FIFO protocol and regular-file path work; reading `/proc/diskstats` again on the same unrewound descriptor gives EOF (`E/audit-probes.json:2-30`; `E/live-protocol.json:59-76`; `E/draft-vs-ba.diff:26-47`).
VERDICT: disagree — A13, :130,142-144: “the draft was not broken” is too broad. It fails the frozen reader-close protocol in a direct witness; call the change a conformance/interoperability fix, not an arithmetic fix and not a non-fix (`E/live-protocol.json:2-56`; `L/.ufo/waves/round-34/contract.md:133-137`).
VERDICT: disagree — A14, :157-159: one duplicate-free host observation does not establish “real /proc/diskstats never contains a repeated device name.” Keep the generator-uniqueness fact; do not promote a snapshot into a universal claim (the report's own :157-158 evidence is one enumeration; `L/.ufo/waves/round-34/count-c1-a1.py:179-205`).
VERDICT: disagree — A15, :89-93: the old counter passes are not re-established by this review, and the cited `evidence/c1-after.txt` is absent from ba525e1a, 8d56809a and fd252135 (`E/audit-probes.json:55-70`, each `git ls-tree <rev> .ufo/waves/round-34/evidence/c1-after.txt` returned no entry). The actual committed provenance receipt records the L1's fixed-candidate runs at `L/.ufo/waves/round-34/evidence/c1-tool-provenance.txt:58-60`; I ran no new full counter score.
VERDICT: agree — A16, :165-168: authorship is explicitly process evidence, not part of the predicate; this does not itself decide whether C1 passes (`L/.ufo/waves/round-34/contract.md:83-88`).
AUDIT: agree 11 / disagree 5

## Audit of .ufo/waves/round-34/wa/LabIntervalError.md

VERDICT: agree — B1, :15-23: the three revision hashes and MD5 match (`E/audit-probes.json:55-70`).
VERDICT: agree — B2, :25-28: the divisor is nominal `interval_ms`, not elapsed time (`L/tools/mori-disk-rate.py:175-184,227-240`; `L/.ufo/waves/round-34/contract.md:46`).
VERDICT: disagree — B3, :29: “only correct if” elapsed time equals nominal is too strong: an unchanged counter gives exactly zero for both denominators; integer rounding also matters (`E/audit-probes.json:40-53`; `E/floor-witness.py:3-9`, executed output `1706 < 1706.5528964735686` for an explicitly hypothetical 300.02-ms gap).
VERDICT: agree — B4, :51-64: read rather than open is the relevant sampling operation. The seq-file show callback collects counters while formatting each device (`L/corpus/evidence/sources-r33/S182.src:1369-1391,1416-1425`). It is not an atomic all-device snapshot exactly at syscall entry; I did not repeat the old 1-MiB-write experiment.
VERDICT: disagree — B5, :35-49,74-103,129-132,159-169: the historical invocation totals, loaded medians/tails, small-interval figures and under-load 5% hypothesis verdict are not re-established by my ten fresh runs. Uncommitted old outputs are audit objects, not fresh measurement evidence. Do not cite those figures as independently rerun here (`E/timing.tsv:2-11`; method `E/timing.json:2`).
VERDICT: agree — B6, :88-90: the direction “longer than nominal” holds for all ten independently observed read windows (`E/timing.tsv:2-11`), with no universal extrapolation.
VERDICT: disagree — B7, :123-124: `1.00038 * interval_ms` is not a universal lower bound. My 1000-ms read-start gaps are only 1.000210863–1.000276772 times nominal (`E/timing.tsv:7-11`). This does not refute the historical dataset's stated minimum.
VERDICT: disagree — B8, :107-109: fractional overstatement relative to the elapsed-time rate is `(G-N)/N`, ignoring floor, not `(G-N)/G`. For N=200 ms, G=212.85 ms and delta=512000 bytes, the executed calculation gives 6.425% versus the report formula's 6.037115% (`E/audit-probes.json:32-39`). This is an analytic witness, not a new loaded timing measurement.
VERDICT: disagree — B9, :109-117: the old rate experiment does not independently measure its numerator. Its program selects the largest reported rate and reconstructs the supposed delta from that same rate before calculating “true_Bps”; it neither reads independent counter samples nor identifies the writer's backing device (`/fast/scratch/hyaku/mori-r34/a2-LabIntervalError/rateerr.py:92-112`, inspected as the audit object). The table is a timing-derived calculation, not an independent end-to-end accuracy check.
VERDICT: disagree — B10, :118,165-166: “always positive” / “never under-reports” is not generally valid. Zero delta yields zero (`E/audit-probes.json:40-53`). With one sector, nominal 300 ms and an explicitly hypothetical real gap of 300.02 ms, executed R6 returns 1706 Bps versus 1706.552896 elapsed-time Bps: floor can reverse the sign (`E/floor-witness.py:3-9`; command `python3 -B E/floor-witness.py` returned `underreports_for_this_gap: true`). No host under-reporting observation is claimed.
VERDICT: agree — B11, :122-127: a longer gap does not itself violate the 0.9-interval floor, and the oracle uses the same nominal R6 denominator (`E/timing.tsv:2-11`; `L/.ufo/waves/round-34/count-c1-a1.py:101,358-365`). This is not a full C1 verdict.
VERDICT: agree — B12, :134-139: nominal-versus-real-time error is not, by itself, a deviation from frozen R6 (`L/.ufo/waves/round-34/contract.md:46`; `L/tools/mori-disk-rate.py:238-240`).
VERDICT: disagree — B13, :151-152: +0.07%–+6.43% should not be carried forward as an independently verified range or an invariant. My fresh 1000-ms excesses are below +0.07%; even the old report itself states a smaller historical minimum, 1.00038 times nominal at :88-89 (`E/timing.tsv:7-11`). The loaded maximum remains unrerun, not disproved.
VERDICT: agree — B14, :141-152: the docstring's asserted divisor equality is wrong; all ten fresh read-window lower bounds exceed nominal, whereas R6 divides by nominal (`E/timing.tsv:2-11`; `L/tools/mori-disk-rate.py:178-184,238-240`).
AUDIT: agree 7 / disagree 7

## Execution and limits

Executed foreground probes: `timeout 60s prlimit --as=536870912 --cpu=45 -- python3 -B E/independent.py identity`; 45-s bounded `witnesses` and `timing` modes; bounded `live_protocol.py`, `audit-probes.py`, `derived-witness.py`, and `floor-witness.py`. Outputs are the cited E JSON/TSV files. The first protocol probe failed its scratch feeder cleanup (`RuntimeError: feeder failed to terminate`); the retry fixed cleanup ordering and reused the already-captured real samples (`E/live_protocol.py:9-12,69-84`). It was not counted as a successful run.
No full frozen-counter score, load sweep, installation, service change, mount, block-device operation or background job was performed by this seat. All commands returned; FIFO feeders were joined or ended with their foreground process (`E/live_protocol.py:69-84`; `E/audit-probes.py:51-57`). Python reported `Python 3.14.8` from `timeout 15s prlimit --as=536870912 --cpu=10 -- python3 --version`; git was used read-only. No tools were installed or updated. The only lane write is this report; test inputs and results are under E.
