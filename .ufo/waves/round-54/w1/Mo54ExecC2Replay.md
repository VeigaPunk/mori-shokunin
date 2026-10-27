# Mo54ExecC2Replay — independent replay of the C2 counter (leaf executor)

Assignment: run `count-c2.py` independently at the frozen rev and at the entering tip, run its selftest and
`--hashes`, compare with the three receipts, and write my own located-quote check (not importing the counter) for
all 21 rows. Read-only. No lane file written except this report. No subagent, no network mutation, no pacman.

Machine: MACHINE_ID (this workstation). Lane repo under test:
`/home/vgpnk/Projects/shokunin/mori-shokunin` at `R = 78295c764093ff1f6cee08d7246679900bde7265` (data commit),
entering tip `39dcf4d7e410d362781a47e8365ca23b5c807598`, freeze commit `6830f3af992d906bfa1e17e3743e631ab834f67c`.
Scratch `/fast/scratch/hyaku/mori-r54/Mo54ExecC2Replay/` (removed before finish). Disk guard `status` rc=0,
`/fast/scratch/hyaku` 26% used, 596.7G free — no ENOSPC risk. No tool installed or upgraded (nothing was needed).

## 1. Counter replay — the three assigned runs

All three were run with `cd /fast/scratch/hyaku/mori-r54/Mo54ExecC2Replay` (the tools' cwd is the fleet root, so the
absolute counter path was used and nothing relative could land in the fleet root). The counter's `repo` default
resolves to the lane repo (`__file__` four levels up), so no `--repo` was needed.

### 1.1 `count-c2.py 78295c764093ff1f6cee08d7246679900bde7265`

```
C2=unmet claims=21 located=21 quote_missing=0 bad_rows=0 sources=6 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 rev=78295c764093ff1f6cee08d7246679900bde7265 failed=entailment
exit=1
```

Receipt `evidence/c2-at-data.txt`:
```
C2=unmet claims=21 located=21 quote_missing=0 bad_rows=0 sources=6 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 rev=78295c764093ff1f6cee08d7246679900bde7265 failed=entailment
exit=1
```

**Identical, 1 line + exit, zero divergence.** The only failing arm is `entailment` (`entailed=0`), which is the
designed pre-vote state: the wave has cast no vote yet (`entailed=0` is what the contract's `c2 no-votes` control
demands at the data commit).

### 1.2 `count-c2.py --selftest`

```
PASS honest_met … PASS text_copy_keeps_angle_brackets
C2_SELFTEST pass=54 fail=0
exit=0
```

54 checks, 54 PASS, exit 0. Receipt `evidence/selftest-c2.txt` lists the same 54 names in the same order, same
`pass=54 fail=0`, exit 0. **Identical.**

### 1.3 `count-c2.py --hashes 78295c764093ff1f6cee08d7246679900bde7265`

21 lines, exit 0. Row hashes in entry order (all reproduced verbatim around the claims; listing cross-check below):

```
fcf9f378a818 ba07ddfe1488 e874fc1a128e 8426794e271e 4fdea8d0253f 4748dc4eb41e 3233412a93be
f5e240db68c0 2eb3990f7a81 c98ac2ffa163 5a235a277033 e3f8e075e4b2 63f08aa3baf0 e3b581d09d1d
77be7d2e2179 734269273c22 2401e4d865f0 c81900e6c688 4f693eb5f736 8248e6d24be8 257f4acfda4e
```

Cross-check against `evidence/c2-claims.txt` done by an independent parser (my own table splitter, my own hash):
`rows=21 listed=21 claims_in_listing=21`, `LISTING_MATCHES_ENTRY=True` — every one of the 21 hashes equals
`sha256(" ".join(claim.split())).hexdigest()[:12]` computed by me from the entry text at `R`, every listed claim
string equals the entry's claim cell character for character after strip, and every listed source id equals the
row's source cell. The listing is therefore not stale.

## 2. Control — do-nothing

`count-c2.py 39dcf4d7e410d362781a47e8365ca23b5c807598` (the entering tip, run against the lane repo instead of a
clone):

```
C2=unmet claims=0 located=0 quote_missing=0 bad_rows=0 sources=0 source_rows=bad pins=bad provenance=bad entailed=0 dissent=0 rev=39dcf4d7e410d362781a47e8365ca23b5c807598 failed=entry_absent,pins
exit=1
```

Receipt `evidence/control-c2-do-nothing.txt` (which used `--repo` on a throwaway clone):
`C2=unmet claims=0 … sources=0 source_rows=bad pins=bad provenance=bad entailed=0 dissent=0 … failed=entry_absent,pins`,
exit=1. **Identical counter line and exit**; the clone path in the receipt is the only difference (it is in the
`command:` line, not in the reading).

Extra probe I ran that the receipts also cover (`c2 copies-only`, the freeze state) — same counter, rev
`6830f3af992d906bfa1e17e3743e631ab834f67c`:

```
C2=unmet claims=0 located=0 quote_missing=0 bad_rows=0 sources=0 source_rows=bad pins=ok provenance=bad entailed=0 dissent=0 rev=6830f3af992d906bfa1e17e3743e631ab834f67c failed=entry_absent
exit=1
```

Matches `control-c2-copies-only.txt` (`C2=unmet claims=0 … pins=ok … failed=entry_absent`, exit=1). The three
readings separate exactly as the contract claims: no copies → `pins=bad`; copies at the freeze → `pins=ok`,
`entry_absent`; entry at the data commit → `pins=ok`, `located=21`, `entailed=0`, `failed=entailment`.

## 3. Frozen bytes — the counter and the six copies are the frozen bytes

`sha256sum` of the working tree, `git show R:<path>` of the committed bytes, and `evidence/freeze-sha256.txt`
agree on all seven artefacts:

| artefact | sha256 | wt = committed = freeze = upstream |
|---|---|---|
| `.ufo/waves/round-54/count-c2.py` | `d6b42f893b30…` | yes (committed at `R` hashes `d6b42f89…`) |
| `corpus/evidence/sources-r54/memory-failure.c.v7.3` | `94d24a605b61…` | yes |
| `corpus/evidence/sources-r54/hwpoison.rst.v7.3` | `8011bb158129…` | yes |
| `corpus/evidence/sources-r54/sysfs-devices-node.v7.3` | `d852f950e42d…` | yes |
| `corpus/evidence/sources-r54/memory-failure-trace.h.v7.3` | `a395e62b36ac…` | yes |
| `corpus/evidence/sources-r53/vm.rst.v7.3` | `f81feb3dfca5…` | yes |
| `corpus/evidence/sources-r53/proc.rst.v7.3` | `bc178ff511e0…` | yes |

Per-copy `git show R:<copy>` vs working tree: `SAME` for all six (no working-tree drift to trigger the contract's
`git show <freeze>:<path>` fallback). Entry `corpus/knowledge/memory-failure-kills-r54.md` at `R` and in the
working tree hash `a5062c3b1a90…` — identical, so the counter measured the bytes that are on disk.

### 3.1 Independent upstream re-fetch (my own network read, six requests, cgit `?h=v7.3`)

```
curl -sSL --max-time 60 -o upstream/<name> "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/<path>?h=v7.3"
# paths: mm/memory-failure.c, Documentation/mm/hwpoison.rst, Documentation/ABI/stable/sysfs-devices-node,
#        include/trace/events/memory-failure.h, Documentation/admin-guide/sysctl/vm.rst,
#        Documentation/filesystems/proc.rst
```

All six returned rc=0 with sizes `82847 / 6026 / 8149 / 2964 / 45908 / 107605`. Their `sha256sum`:

```
8011bb158129776bbb38ed5808959bd14d17489527ed3987dbc3d21d27e3ecb7  hwpoison.rst.v7.3
a395e62b36ace3d1295fd3e9e469fc525f67c7787f529a380633d6b800f051ea  memory-failure-trace.h.v7.3
94d24a605b61f94ad1d10ab3db26aed12cb6113af15431ff873da5b98ca48003  memory-failure.c.v7.3
bc178ff511e05c1b5e0c2413feb18223edcaeb2797ce499b714b98120cabf3c8  proc.rst.v7.3
d852f950e42d92b862792477a892e77973ddb6a345bdb1748d2e7c5020198665  sysfs-devices-node.v7.3
f81feb3dfca5f054cf8b76c71d7a4525a88d629d3ea8239743996b9d87bb391b  vm.rst.v7.3
```

All six equal the pins. So the committed copies are the real upstream v7.3 bytes as I fetched them today, not
merely self-consistent: the `pins=ok` arm is corroborated from outside the lane.

## 4. My own located-quote check (not importing `count-c2.py`)

`locate.py` (mine, 130 lines, in scratch): own table splitter (handles `\|`, leading/trailing pipes, fences,
`:---:` rule rows), own claim-hash, own `sources_row` lookup into `corpus/SOURCES.md`, and plain substring
containment of the whitespace-collapsed quote in the whitespace-collapsed copy **of that row's own source id**,
plus a scan of the other five copies. Everything read through `git show R:<path>`.

```
header=['claim', 'source', 'quote'] rows=21
TOTAL rows=21 located_in_own_copy=21 missing=0 bad=0
```

Per row (hash / source id / quote words / located in own copy / also present in another of the six copies /
line of the copy on which the quote begins, computed by a second script `lines.py` with an offset→line map; the
word counts and the 6..25 span are my own measurements, not the counter's):

| # | hash | sid | words | in own copy | in other copies | begin line | span (lines) | blank line inside |
|---|---|---|---|---|---|---|---|---|
| 1 | fcf9f378a818 | S521 | 8 | yes | none | 37 | 37–39 | yes (38) |
| 2 | ba07ddfe1488 | S521 | 13 | yes | none | 292 | 292–293 | – |
| 3 | e874fc1a128e | S521 | 11 | yes | none | 295 | 295–296 | – |
| 4 | 8426794e271e | S521 | 14 | yes | none | 302 | 302–303 | – |
| 5 | 4fdea8d0253f | S521 | 15 | yes | none | 470 | 470–472 | – |
| 6 | 4748dc4eb41e | S521 | 9 | yes | none | 483 | 483 | – |
| 7 | 3233412a93be | S521 | 9 | yes | none | 1291 | 1291–1292 | – |
| 8 | f5e240db68c0 | S521 | 12 | yes | none | 872 | 872–875 | – |
| 9 | 2eb3990f7a81 | S521 | 12 | yes | none | 1297 | 1297 | – |
| 10 | c98ac2ffa163 | S521 | 13 | yes | none | 1286 | 1286–1289 | – |
| 11 | 5a235a277033 | S521 | 12 | yes | none | 1271 | 1271–1274 | yes (1273) |
| 12 | e3f8e075e4b2 | S522 | 12 | yes | none | 64 | 64 | – |
| 13 | 63f08aa3baf0 | S522 | 20 | yes | none | 70 | 70–71 | – |
| 14 | e3b581d09d1d | S522 | 15 | yes | none | 59 | 59–60 | – |
| 15 | 77be7d2e2179 | S507 | 19 | yes | none | 514 | 514–515 | – |
| 16 | 734269273c22 | S507 | 19 | yes | none | 936 | 936–937 | – |
| 17 | 2401e4d865f0 | S523 | 19 | yes | none | 196 | 196–197 | – |
| 18 | c81900e6c688 | S523 | 19 | yes | none | 203 | 203–204 | – |
| 19 | 4f693eb5f736 | S524 | 19 | yes | none | 4 | 4–7 | – |
| 20 | 8248e6d24be8 | S524 | 7 | yes | none | 93 | 93 | – |
| 21 | 257f4acfda4e | S502 | 12 | yes | none | 1269 | 1269–1271 | – |

**No row's quote failed to locate in its own copy. No quote occurs a second time in its own copy, and none occurs
in any other of the five copies** (so a row's located quote is genuinely that file's text, not a shared sentence).
Every quote is 7–20 words (predicate allows 6–25), and my own claim-beyond-quote count is ≥8 for every row
(predicate floor 3; minimum is row 17 at 8).

Source rows: each of the six S-ids named by the 21 rows exists in `corpus/SOURCES.md` at `R` with `mined`,
`2026-10-27` (S521–S524) or `2026-10-26` (S502, S507) as the open date, a `?h=v7.3` URL, and this entry in the
used-by cell — read by my own parser, not the counter's.

Row distribution over the six copies: S521 11 rows, S522 3, S507 2, S523 2, S524 2, S502 1 = 21 rows, 6 sources
(the counter's `sources=6` is exactly this set).

## 5. Splice analysis — how the quotes sit in the raw files (named limit, evidence for round 55)

Because both the predicate and my check collapse whitespace, a quote cell may join several raw lines. Measured:

- 17 of 21 quotes span more than one raw line; only rows 6, 9, 12, 20 lie entirely on one line.
- Row 1 begins on line 37 and ends on 39 **across a blank line**, joining two independent top-level directives:

  ```
    36|
    37| #define pr_fmt(fmt) "Memory failure: " fmt
    38|
    39| #include <linux/kernel.h>
  ```

  The quoted span is therefore `#define pr_fmt(fmt) "Memory failure: " fmt #include <linux/kernel.h>` — the
  `#include` is presented as part of the prefix span. The claim ("every message … starts with the same prefix")
  is still true of line 37 alone, so this is presentation, not a false row.
- Row 11 crosses blank line 1273 inside one function body (`panic_on_unrecoverable_mf`, 1268–1275) — semantically
  one statement pair, harmless.
- Row 19 joins a comment terminator to a `#define` and carries bare comment `*` markers:
  lines 4–7 of the trace header are `* For historical versions, …`, `* some user programs depend on it.`, `*/`,
  `#define TRACE_SYSTEM ras`.
- Row 5 joins the continuation of one `pr_err(...)` (470–471) to the start of the next statement
  `do_send_sig_info(SIGKILL,` (472).

No quote skips intervening text: whitespace collapse maps newlines to one space and nothing else, so a
containment hit in the collapsed file implies the quoted tokens are adjacent modulo whitespace. The weakness is
one-directional: a quote cell can *present* two adjacent-but-distinct constructs as one quotation. That is a
property of the frozen predicate (`normalise_text` at `count-c2.py:87-88`, `re.sub(r"\s+", " ", text)`), named in the contract as "a located
quote proves the quoted words exist in the copy" — not a defect to fix this round.

## 6. The one row whose claim rests on a v7.3-new fact — independently checked

Rows 11 and 16 assert that `panic_on_unrecoverable_memory_failure` is new in v7.3. I fetched, independently of the
lane's copies,

- `Documentation/admin-guide/sysctl/vm.rst?h=v7.2` (42424 bytes, rc 0) and
- `mm/memory-failure.c?h=v7.2` (80516 bytes, rc 0)

and `grep -n panic_on_unrecoverable` returned **nothing in either file** (rc 1). In the v7.3 copy:

```
  78| static int sysctl_panic_on_unrecoverable_mf __read_mostly;
 163| 		.procname	= "panic_on_unrecoverable_memory_failure",
 164| 		.data		= &sysctl_panic_on_unrecoverable_mf,
 168| 		.proc_handler	= proc_dointvec_minmax,
 169| 		.extra1		= SYSCTL_ZERO,
 170| 		.extra2		= SYSCTL_ONE,
1268| static bool panic_on_unrecoverable_mf(enum mf_action_page_type type,
1271| 	if (!sysctl_panic_on_unrecoverable_mf)
1274| 	return type == MF_MSG_KERNEL && result == MF_IGNORED;
1294| 	if (panic_on_unrecoverable_mf(type, result))
1295| 		panic("Memory failure: %#lx: unrecoverable page", pfn);
```

So the "new in v7.3" part of rows 11 and 16 holds from my own fetch, the switch is a `static int` (default 0 =
off unless set), and its range is `SYSCTL_ZERO..SYSCTL_ONE`. Row 11's quote and wording match lines 1271–1274 and
the "reserved kernel page" of the claim is `MF_MSG_KERNEL` at 1274.

## 7. Host read (read-only, allowed paths only) — the entry's "On this host" section is accurate today

```
/sys/devices/system/node/node0/memory_failure/delayed=0  failed=0  ignored=0  recovered=0  total=0
HardwareCorrupted:     0 kB                      (/proc/meminfo)
memory_failure_recovery=1   memory_failure_early_kill=0   enable_soft_offline=1
panic_on_unrecoverable_memory_failure=ABSENT     (/proc/sys/vm/)
kernel=7.2.11-arch1-1
```

This is the same set of facts the entry records under "On this host (read-only, 2026-10-27)" — five node0
counters 0, `HardwareCorrupted: 0 kB`, recovery 1, early kill 0, soft offline 1, the v7.3 panic sysctl absent on
7.2.11. Single NUMA node on this host. Nothing was written; no poison injected; no sysctl touched. It also
confirms the counter's named limit "nothing here was observed firing": every counter is 0, so no live
memory-failure event exists to compare the lines against.

## 8. Vote arm state at the time of my run

`ls /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-54/w1-results.json` →
`No such file or directory`; `w1/` held `Mo54Rc01.md` and no `Mo54En*.md`. So `entailed=0` is correct at the data
rev for two independent reasons, and the arm cannot be spoofed by an early voter file: `entail_votes()` skips a
voter whose name is not in the results file (`count-c2.py:149-152`). P-C2 is therefore **unmet at the data commit
by design**, not by data failure — the whole located/sources/pins/provenance half is already at its target
(`claims=21`, `located=21`, `quote_missing=0`, `bad_rows=0`, `sources=6`, `source_rows=ok`, `pins=ok`,
`provenance=ok`), and only `entailed=21 dissent=0` is outstanding.

## 9. What I did not do (bounds)

- Did not run the C1 counter, the control runner, or any fixture/clone mutation — other seats hold those.
- Did not judge entailment; that is the twelve ENTAILMENT seats' and the L1's call. My rows above are location
  facts, not a vote. I wrote no line beginning with a vote keyword, so this report is inert to both counters.
- Did not attempt any host change; did not run pacman (host-wide pause honoured); installed no tool.
- Did not edit any lane file; this report is the only write.

## Findings

1. **LOW — replay agreement is exact.** `count-c2.py 78295c76…` reproduces `evidence/c2-at-data.txt` line for
   line (`claims=21 located=21 quote_missing=0 bad_rows=0 sources=6 source_rows=ok pins=ok provenance=ok
   entailed=0 dissent=0 failed=entailment`, exit 1), `--selftest` reproduces `pass=54 fail=0` exit 0, and
   `--hashes` reproduces all 21 hashes; the do-nothing control reproduces `evidence/control-c2-do-nothing.txt`
   (exit 1) and the freeze rev reproduces `control-c2-copies-only.txt`. Concerned file:
   `.ufo/waves/round-54/count-c2.py`. No divergence.
2. **LOW — the six v7.3 copies are the real upstream bytes.** My independent cgit re-fetch of all six
   `?h=v7.3` paths hashes to the six frozen sha256 values (`94d24a605b61…`, `8011bb158129…`, `d852f950e42d…`,
   `a395e62b36ac…`, `f81feb3dfca5…`, `bc178ff511e0…`), and `count-c2.py` at rev `R` hashes `d6b42f893b30…` =
   `evidence/freeze-sha256.txt`. Concerned files: `corpus/evidence/sources-r54/*.v7.3`,
   `corpus/evidence/sources-r53/{vm,proc}.rst.v7.3`, `.ufo/waves/round-54/count-c2.py`.
3. **LOW (confirming the frozen predicate) — all 21 quotes locate in their own copy.** My counter-independent
   checker: `rows=21 located_in_own_copy=21 missing=0 bad=0`; no quote repeats inside its copy or appears in any
   other of the five copies; words-per-quote 7–20; claim-beyond-quote ≥8. Concerned file:
   `corpus/knowledge/memory-failure-kills-r54.md` (claim table, rows 1–21).
4. **MED (named limit, round-55 routed, not fixable this round) — a located quote may splice distinct constructs
   across a line break or blank line.** 17/21 quotes span more than one raw line; row 1 (lines 37–39 of
   `memory-failure.c.v7.3`) presents `#define pr_fmt(fmt) "Memory failure: " fmt` and `#include <linux/kernel.h>`
   as one quotation across a blank line; row 19 (lines 4–7 of `memory-failure-trace.h.v7.3`) joins a comment
   terminator `*/` to `#define TRACE_SYSTEM ras`. Consequence: the located arm cannot distinguish a contiguous
   quotation from an adjacency join, and a reader can be shown two constructs as one. Concerned code:
   `count-c2.py:87-88` (`normalise_text` collapses all whitespace, newlines included); concerned rows: 1, 5,
   11, 19 of the entry. The claims of those rows still hold on their own text, so this is a presentation limit,
   not a false row.
5. **LOW — "new in v7.3" verified independently.** `panic_on_unrecoverable` is absent from
   `vm.rst?h=v7.2` (42424 B) and `mm/memory-failure.c?h=v7.2` (80516 B) — grep found nothing, rc 1 — and present
   in v7.3 as `static int sysctl_panic_on_unrecoverable_mf` (line 78), sysctl `SYSCTL_ZERO..SYSCTL_ONE`
   (169–170), used at 1271/1274/1294–1295. Concerned rows: entry rows 11 and 16;
   `corpus/evidence/sources-r54/memory-failure.c.v7.3:78,163-171,1268-1295`.
6. **LOW — the entry's live-host section is accurate today.** Read-only reads give node0
   `memory_failure/{total,ignored,failed,delayed,recovered}` all 0, `HardwareCorrupted: 0 kB`,
   `memory_failure_recovery=1`, `memory_failure_early_kill=0`, `enable_soft_offline=1`,
   `/proc/sys/vm/panic_on_unrecoverable_memory_failure` ABSENT, kernel `7.2.11-arch1-1` — identical to the
   entry's "On this host (read-only, 2026-10-27)" block. Concerned file:
   `corpus/knowledge/memory-failure-kills-r54.md`, "On this host" section.
7. **LOW — P-C2 is blocked only by the vote arm, and legitimately.** `entailed=0` with no
   `w1-results.json` and no `Mo54En*.md` present; the counter ignores a voter absent from the results file
   (`count-c2.py:149-152`), so the data commit cannot pass early. Target after votes:
   `entailed=21 dissent=0`. Concerned files: `.ufo/waves/round-54/w1-results.json` (absent),
   `.ufo/waves/round-54/w1/Mo54En01..12.md` (absent at my run).
8. **LOW (advisory, outside my C2 scope) — the same whitespace-collapse arm is stricter for C1's rendered HTML
   copy than for C2.** For `kind == "html"` the counter strips tags before collapse (`count-c2.py:96-101`
   `normalise`), so a C1 quote drawn from the rendered page can span removed markup; C2's six copies are all
   `kind == "text"`, so C2's located arm is pure whitespace collapse. Noted for the C1 attack seats / L1 to
   route; I did not evaluate C1.
