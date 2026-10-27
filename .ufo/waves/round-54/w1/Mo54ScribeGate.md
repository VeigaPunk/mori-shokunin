# Mo54ScribeGate — round 54 w1 — Gate draft (S515–S524, used-by S502/S507/S508/S514)

Seat assignment: draft the lesson's `## Gate` block for the ten rows opened this round and the four used-by changes,
with a self-run substring test per located quote, plus four rejection records (one admit class, three rejects).
Entering tip `39dcf4d7e410d362781a47e8365ca23b5c807598`; data commit `78295c764093ff1f6cee08d7246679900bde7265`;
lane working tree read at `2d0347a32b6befd7fd946a83319e04f6d8f004b9`.

Read-only seat: every command below is a read of committed bytes or a small fetch from cgit / docs.kernel.org /
jsdelivr into scratch. No lane file was written except this report; no fleet file, no SKILL/SOURCES/corpus edit, no
pacman, no tool install, no host write, no git or jj mutation. Scratch `/fast/scratch/hyaku/mori-r54/Mo54ScribeGate/`
was created for the fetches and removed at the end; the cited outputs are transcribed below, and every fetched copy
that is cited equals the committed copy by sha256 (so the committed copy is the evidence, not the scratch file).

## Gate draft for `corpus/lessons/round-54.md`

````markdown
### New SOURCES rows (each opened this round; rule 1)

Ten new rows, all opened 2026-10-27, appended after S514, 11 cells each, status `mined`,
recheck `on-release`. S515–S520 (`used-by corpus/knowledge/kernel-v7.3-recheck-r54.md`) are the C1 re-check copies:
five of them the paths the remaining v7.2-pinned claim rows cite, at tag v7.3 from git.kernel.org cgit
(`plain/<path>?h=v7.3`), plus the one rendered page as a release-pinned URL (S520, `https://docs.kernel.org/7.3/…` —
the flip round 53 named; `latest` stays rejected below). S521–S524 (`used-by
corpus/knowledge/memory-failure-kills-r54.md`) are the C2 copies, all cgit at v7.3. Copies under
`corpus/evidence/sources-r54/`, sha256 pinned in this table, in `.ufo/waves/round-54/evidence/freeze-sha256.txt`
(lines 24–33) and inside `count-c1.py` (S515–S520) and `count-c2.py` (S521–S524). Every located quote was checked by
`w1/Mo54ScribeGate.md` against the committed copy with the substring test printed below (10/10 found, line and word
count as reported by the test).

| id | URL / locator | accessed | copy sha256 (full) | ≤25-word located quote | decision |
|---|---|---|---|---|---|
| S515 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/mm/memcontrol.c?h=v7.3 — copy `memcontrol.c.v7.3` | 2026-10-27 | `bdb6159cc2378c44c356b6788f521812f15c4d4936e8b09c66ef70b56bcc41a1` | `pr_info("memory: usage %llukB, limit %llukB, failcnt %lu\n",` (7 tokens, `:1850`) | admit, mined, tier A code |
| S516 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/mm/oom_kill.c?h=v7.3 — copy `oom_kill.c.v7.3` | 2026-10-27 | `452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e` | `pr_info("oom-kill:constraint=%s,nodemask=%*pbl", oom_constraint_text[oc->constraint], nodemask_pr_args(oc->nodemask));` (3 tokens, `:447-449`) | admit, mined, tier A code |
| S517 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/lib/percpu_counter.c?h=v7.3 — copy `percpu_counter.c.v7.3` | 2026-10-27 | `2c26e67751f939dfb21ff6221884280ae84a2a94a54de4468fb9dc8746130d6d` | `if (unlikely(abs(count + amount) >= batch)) {` (7 tokens, `:100`) | admit, mined, tier A code |
| S518 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/linux/percpu_counter.h?h=v7.3 — copy `percpu_counter.h.v7.3` | 2026-10-27 | `4a107bc381b3b5425b8ff441f7487d97ba6883dc6f5b426c4bd361ad7cbef896` | `static inline s64 percpu_counter_read_positive(struct percpu_counter *fbc)` (6 tokens, `:118`) | admit, mined, tier A code (row anchor says `:121`, which is the body line; see Findings) |
| S519 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/uapi/asm-generic/errno.h?h=v7.3 — copy `errno.h.v7.3` | 2026-10-27 | `66a5ad60566fdd62e41701bcfc42bfeca5e5696ad1d47d78981575e0c51622be` | `#define	EDQUOT		122	/* Quota exceeded */` (7 tokens, `:107`) | admit, mined, tier A code; byte-identical to v7.2 (`66a5ad60566f` = S481's copy) |
| S520 | https://docs.kernel.org/7.3/admin-guide/cgroup-v2.html — copy `cgroup-v2.7.3.html` (rendered page, footer `7.3.0`) | 2026-10-27 | `b478c1bae99899df476d6b4989cbb516f7ca93c5f009cdff64b802bbc24f3d4b` | "The number of processes belonging to this cgroup killed by any kind of OOM killer." (15 words, `:1409-1410`) | admit, mined, tier A docs — release-pinned rendered URL, the round-53 flip |
| S521 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/mm/memory-failure.c?h=v7.3 — copy `memory-failure.c.v7.3` | 2026-10-27 | `94d24a605b61f94ad1d10ab3db26aed12cb6113af15431ff873da5b98ca48003` | `pr_err("%#lx: Sending SIGBUS to %s:%d due to hardware memory corruption\n",` (10 tokens, `:292`) | admit, mined, tier A code |
| S522 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/mm/hwpoison.rst?h=v7.3 — copy `hwpoison.rst.v7.3` | 2026-10-27 | `8011bb158129776bbb38ed5808959bd14d17489527ed3987dbc3d21d27e3ecb7` | "Send SIGBUS when the application runs into the corrupted page." (10 words, `:70`) | admit, mined, tier A docs |
| S523 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/ABI/stable/sysfs-devices-node?h=v7.3 — copy `sysfs-devices-node.v7.3` | 2026-10-27 | `d852f950e42d92b862792477a892e77973ddb6a345bdb1748d2e7c5020198665` | "The total number of raw poisoned pages (pages containing corrupted data due to memory errors) on a NUMA node." (19 words, `:196-197`) | admit, mined, tier A docs (stable ABI) |
| S524 | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/trace/events/memory-failure.h?h=v7.3 — copy `memory-failure-trace.h.v7.3` | 2026-10-27 | `a395e62b36ace3d1295fd3e9e469fc525f67c7787f529a380633d6b800f051ea` | `TP_printk("pfn %#lx: recovery action for %s: %s",` (7 tokens, `:93`; `TRACE_EVENT(memory_failure_event)` opens at `:74`, `TRACE_SYSTEM ras` at `:7`) | admit, mined, tier A code |
| — | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/ras/ras_event.h?h=v7.3 (the L1's first pick for the tracepoint) | 2026-10-27 | HTTP 200, 11341 bytes, sha256 `408ddc2ac2a5f17282ecd4cecc6b3727d1e4f46e2f0855a26f2e27073026802b` (identical from cgit and jsdelivr); `grep -c memory_failure` → `0`; the file's five `TRACE_EVENT`s are `extlog_mem_event` (`:26`), `mc_event` (`:97`), `arm_event` (`:176`), `non_standard_event` (`:257`), `aer_event` (`:337`) | **reject**: at v7.3 the ras header defines `TRACE_SYSTEM ras` but no `memory_failure_event`; the event moved to `include/trace/events/memory-failure.h` (S524), whose own header comment says so ("For historical versions, memory_failure_event is in ras subsystem, some user programs depend on it", `:4-5`). A quote located there would pin nothing | Flip: a re-fetch of this path at a cited tag where `grep -c 'TRACE_EVENT(memory_failure_event'` is ≥ 1 — then admissible as a second locator for S524, never as a new row |
| — | https://cdn.jsdelivr.net/gh/torvalds/linux@v7.3/… (the same v7.3 paths) | 2026-10-27 | mixed, same session: `mm/memory-failure.c` 200, 82847 bytes, sha256 `94d24a605b61…ca48003` (equal to the S521 copy); `mm/oom_kill.c` 200, 34311; `mm/memcontrol.c` 200, 165998; `Documentation/mm/hwpoison.rst` 200, 6026; `Documentation/ABI/stable/sysfs-devices-node` 200, 8149; `include/ras/ras_event.h` 200, 11341 (equal to the cgit fetch above); **HTTP 403** on `include/trace/events/memory-failure.h` (147 bytes), `lib/percpu_counter.c` (130 bytes), `include/uapi/asm-generic/errno.h` (142 bytes), the 403 body reading "Package size exceeded the configured limit of 50 MB. Try https://github.com/torvalds/linux/tree/v7.3/lib/percpu_counter.c instead." | **reject**: per-path availability is not stable inside one release — six probed paths answered 200 and three answered 403 in the same sitting, so a row opened there can lose its locator; the cgit endpoint answered for all ten rows. Note the reject is path-scoped, not site-scoped | Flip: every cited v7.3 path answers 200 with sha256 equal to the frozen cgit copy on the day it is opened — then jsdelivr is admissible as a second locator for these rows, never as a new row |
| — | https://docs.kernel.org/admin-guide/sysctl/vm.html (rendered docs, `latest`) | 2026-10-27 | HTTP 200, 69002 bytes, sha256 `423d043409bcf9914d72bce7de28516fd164b91a01413dd875c51423fbc42efa`; the page renders `<p class="blurb">7.3.0</p>`; byte-identical to the page round 53 recorded (same size and sha256) | **reject**: `latest` moves with each release (it renders 7.3.0 today, not the v7.3 bytes after v7.4), so a quote found there pins nothing; the release-pinned form was admissible this round (S520, same bytes re-fetched today), which is the flip round 53 named realised on the pinned URL, not on `latest` | Flip: none while the URL tracks the newest release; only a release-pinned rendered URL (`/7.3/…`) is admissible, and S520 shows it works |

### Rows touched old→new (rule 2: status, recheck, used-by in place; no in-round row corrections besides the note under Findings)

- S502 `used-by`: `corpus/knowledge/kernel-v7.3-recheck-r53.md` → `corpus/knowledge/kernel-v7.3-recheck-r53.md,
  corpus/knowledge/memory-failure-kills-r54.md` (the hardware-memory-failure entry cites the `/proc/meminfo`
  `HardwareCorrupted` field definition from this copy).
- S507 `used-by`: `corpus/knowledge/kernel-v7.3-recheck-r53.md` → `corpus/knowledge/kernel-v7.3-recheck-r53.md,
  corpus/knowledge/memory-failure-kills-r54.md` (the entry cites this copy for
  `vm.panic_on_unrecoverable_memory_failure`, new in v7.3).
- S508 `used-by`: `corpus/knowledge/kernel-v7.3-recheck-r53.md` → `corpus/knowledge/kernel-v7.3-recheck-r53.md,
  corpus/knowledge/kernel-v7.3-recheck-r54.md` (the v7.3 re-check of the commit-runway rows re-uses this v7.3 copy).
- S514 `used-by`: `corpus/knowledge/commit-runway-read-r53.md` → `corpus/knowledge/commit-runway-read-r53.md,
  corpus/knowledge/kernel-v7.3-recheck-r54.md` (same).

### Located-quote check (run by this seat against the committed copies)

The test normalises every copy to single-spaced text (so a quote spanning a line break, or an HTML/RST paragraph
wrapped by the renderer, still matches) and reports the line on which the quote begins. It is the test that produced
the line and word counts in the table; 10/10 rows found.

```python
import hashlib, re
E = "/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence"
rows = [
 ("S515", "sources-r54/memcontrol.c.v7.3", 'pr_info("memory: usage %llukB, limit %llukB, failcnt %lu\\n",'),
 ("S516", "sources-r54/oom_kill.c.v7.3", 'pr_info("oom-kill:constraint=%s,nodemask=%*pbl", oom_constraint_text[oc->constraint], nodemask_pr_args(oc->nodemask));'),
 ("S517", "sources-r54/percpu_counter.c.v7.3", 'if (unlikely(abs(count + amount) >= batch)) {'),
 ("S518", "sources-r54/percpu_counter.h.v7.3", 'static inline s64 percpu_counter_read_positive(struct percpu_counter *fbc)'),
 ("S519", "sources-r54/errno.h.v7.3", '#define\tEDQUOT\t\t122\t/* Quota exceeded */'),
 ("S520", "sources-r54/cgroup-v2.7.3.html", 'The number of processes belonging to this cgroup killed by any kind of OOM killer.'),
 ("S521", "sources-r54/memory-failure.c.v7.3", 'pr_err("%#lx: Sending SIGBUS to %s:%d due to hardware memory corruption\\n",'),
 ("S522", "sources-r54/hwpoison.rst.v7.3", 'Send SIGBUS when the application runs into the corrupted page.'),
 ("S523", "sources-r54/sysfs-devices-node.v7.3", 'The total number of raw poisoned pages (pages containing corrupted data due to memory errors) on a NUMA node.'),
 ("S524", "sources-r54/memory-failure-trace.h.v7.3", 'TP_printk("pfn %#lx: recovery action for %s: %s",'),
]
def flat(s): return re.sub(r"\s+", " ", s).strip()
for rid, rel, q in rows:
    raw = open(f"{E}/{rel}", encoding="utf-8").read()
    fq = flat(q)
    line = next((i for i, ln in enumerate(raw.splitlines(), 1)
                 if len(flat(ln)) > 10 and flat(ln) in fq), None)
    if line is None:   # docs/HTML: first line carrying the quote's first five words
        head = " ".join(fq.split()[:5])
        line = next(i for i, ln in enumerate(raw.splitlines(), 1) if head in flat(ln))
    print(f"{rid} sha256={hashlib.sha256(raw.encode()).hexdigest()} line={line} "
          f"words={len(q.split())} found={fq in flat(raw)}")
```

Output (exit 0, 2026-10-27):

```
S515 sha256=bdb6159cc2378c44c356b6788f521812f15c4d4936e8b09c66ef70b56bcc41a1 line=1850 words=7 found=True
S516 sha256=452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e line=447 words=3 found=True
S517 sha256=2c26e67751f939dfb21ff6221884280ae84a2a94a54de4468fb9dc8746130d6d line=100 words=7 found=True
S518 sha256=4a107bc381b3b5425b8ff441f7487d97ba6883dc6f5b426c4bd361ad7cbef896 line=118 words=6 found=True
S519 sha256=66a5ad60566fdd62e41701bcfc42bfeca5e5696ad1d47d78981575e0c51622be line=107 words=7 found=True
S520 sha256=b478c1bae99899df476d6b4989cbb516f7ca93c5f009cdff64b802bbc24f3d4b line=1409 words=15 found=True
S521 sha256=94d24a605b61f94ad1d10ab3db26aed12cb6113af15431ff873da5b98ca48003 line=292 words=10 found=True
S522 sha256=8011bb158129776bbb38ed5808959bd14d17489527ed3987dbc3d21d27e3ecb7 line=70 words=10 found=True
S523 sha256=d852f950e42d92b862792477a892e77973ddb6a345bdb1748d2e7c5020198665 line=196 words=19 found=True
S524 sha256=a395e62b36ace3d1295fd3e9e469fc525f67c7787f529a380633d6b800f051ea line=93 words=7 found=True
```

Independent-channel spot checks by this seat (not the full re-fetch, which is the refetch seats' work): the S524 path
re-fetched from cgit today returned 200, 2964 bytes, sha256 `a395e62b…` (equal to the copy); the S521 path fetched
from jsdelivr returned 200, 82847 bytes, sha256 `94d24a60…` (equal); the S520 pinned rendered page re-fetched from
docs.kernel.org returned 200, 172967 bytes, sha256 `b478c1ba…` (equal, footer `7.3.0`).
````

## Commands (all read-only; scratch removed after)

| command | exit | outcome |
|---|---|---|
| `sha256sum corpus/evidence/sources-r54/* corpus/evidence/sources-r53/{proc.rst,vm.rst,util.c,mm_init.c}.v7.3` | 0 | the ten r54 copies and the four used-by copies hash as in the table and SOURCES rows; full digests quoted above |
| `curl -sS -o ras_event.h.v7.3 -w '%{http_code} %{size_download}\n' '…/plain/include/ras/ras_event.h?h=v7.3'` | 0 | `200 11341`; `grep -c memory_failure` → `0`; five `TRACE_EVENT`s, name list as in the reject row |
| `for p in …; curl -sS -o /dev/null -w '%{http_code} %{size_download}\n' "https://cdn.jsdelivr.net/gh/torvalds/linux@v7.3/$p"` | 0 | 200 for `mm/memory-failure.c`, `mm/oom_kill.c`, `mm/memcontrol.c`, `Documentation/mm/hwpoison.rst`, `Documentation/ABI/stable/sysfs-devices-node`, `include/ras/ras_event.h`; 403 for `include/trace/events/memory-failure.h` (147 B), `lib/percpu_counter.c` (130 B, body "Package size exceeded the configured limit of 50 MB. …"), `include/uapi/asm-generic/errno.h` (142 B) |
| `curl -sS -o latest-vm.html -w '%{http_code} %{size_download}\n' 'https://docs.kernel.org/admin-guide/sysctl/vm.html'` | 0 | `200 69002`; sha256 `423d0434…42efa`; blurb `7.3.0` |
| `curl -sS -o cgit-mf-trace.h '…/plain/include/trace/events/memory-failure.h?h=v7.3'` | 0 | `200 2964`; sha256 equal to `memory-failure-trace.h.v7.3` |
| `curl -sS -o cgit-cgv2.html 'https://docs.kernel.org/7.3/admin-guide/cgroup-v2.html'` | 0 | `200 172967`; sha256 equal to `cgroup-v2.7.3.html`; blurb `7.3.0` |
| `python3 gatetest.py` (the test pasted above) | 0 | 10/10 `found=True`; lines and word counts as in the table |
| `grep -n …`/`awk 'NR==…'` on the copies | 0 | anchor cross-checks: S515 `:1850`, S516 `:447`, S517 `:100`, S518 `:118`, S519 `:107`, S521 `:292`, S524 `:93`/`:74`/`:7`, S522 `:70`, S523 `:196`, S520 `:1409` all as quoted; S516's `:446` in the row is the comment above the statement and S518's `:121` is the body line (Findings) |
| `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` | 0 | `/fast/scratch/hyaku` 26% used, 596.0G free — no ENOSPC risk for the small fetches |
| `grep -n 'bdb6159c\|94d24a60\|a395e62b\|b478c1ba' .ufo/waves/round-54/count-c1.py .ufo/waves/round-54/count-c2.py .ufo/waves/round-54/evidence/freeze-sha256.txt` | 0 | all ten copies pinned in the freeze list (lines 24–33) and in the counters' pin tables |

Tooling: nothing installed or upgraded this seat; no pacman transaction attempted. Host surfaces were not read this
seat (the live host read belongs to another seat); nothing was written to `/proc`, `/sys` or any cgroup.

## Findings

- **LOW** — `corpus/SOURCES.md` S518 anchor `quote lines 121` points at the body line `s64 ret = READ_ONCE(fbc->count);`;
  the quoted function signature begins at `:118` (body `:118-126`, clamp `:123-125`) in
  `corpus/evidence/sources-r54/percpu_counter.h.v7.3`. Correction for the L1: anchor `118` (or `118-126`); data only,
  no counter or predicate change.
- **LOW** — `corpus/SOURCES.md` S516 anchor list item `446` is the comment `/* one line summary of the oom killer
  context. */`; the `oom-kill:constraint=` statement begins at `:447` (statement `:447-449`). Either keep `446` as the
  block anchor or correct it to `447`; the other six anchors in that row (424, 465, 934, 945, 1030, 1169) land on the
  intended lines in the v7.3 copy.
- **LOW** — The jsdelivr reject is path-scoped, not site-scoped: 6 of 9 probed v7.3 paths returned 200 in the same
  session and 3 returned 403, the 403 body naming jsdelivr's 50 MB package limit. A lesson sentence claiming
  "jsdelivr answers 403 at v7.3" would overstate what was observed; the flip condition is per path.
- **LOW** — `docs.kernel.org` `latest` (`admin-guide/sysctl/vm.html`) is byte-identical today to the page round 53
  recorded (69002 bytes, sha256 `423d0434…42efa`, blurb 7.3.0), so no drift can be evidenced this round; the reject
  rests on the URL's semantics (it tracks the newest release), not on a changed body.
- **INFO** — S520 is the first admitted release-pinned rendered page in the lane's source table
  (`https://docs.kernel.org/7.3/…` re-fetched byte-identical today), which closes round 53's named flip; the
  `latest` reject above is what keeps the two apart.
- **INFO** — `include/ras/ras_event.h` at v7.3 has no `memory_failure` string at all (`grep -c` → 0) while
  `include/trace/events/memory-failure.h` (S524) keeps `TRACE_SYSTEM ras` and says in its header comment that the
  event was historically in the ras subsystem — the attribute is carried by the new file, so the tracepoint's
  `ras:` system prefix (S524 row, C2 claim) is unaffected by the move.
