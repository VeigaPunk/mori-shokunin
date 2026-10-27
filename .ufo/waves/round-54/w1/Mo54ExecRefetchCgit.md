# Mo54ExecRefetchCgit — independent cgit re-fetch of the C1 v7.3 copies (and the v7.2 side)

Seat: independent source re-fetching (mori round 54, wave w1). Read-only: no lane file, no counter, no vote line
was written by this seat; the only file it writes is this report. All fetches 2026-10-27 from
`https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/<path>?h=<tag>` into
`/fast/scratch/hyaku/mori-r54/Mo54ExecRefetchCgit/` (removed at the end; every cited value is copied below).

Scope: the seven C1 paths named in the seat order — `mm/memcontrol.c`, `mm/oom_kill.c`,
`lib/percpu_counter.c`, `include/linux/percpu_counter.h`, `include/uapi/asm-generic/errno.h`, `mm/util.c`,
`mm/mm_init.c` — each at v7.3 (against `count-c1.py` `_COPIES` and `evidence/freeze-sha256.txt`) and at v7.2
(against the lane's committed v7.2 copies). Not in scope: `cgroup-v2.7.3.html` / `cgroup-v2.7.2.html`
(docs.kernel.org rendered pages) and the five C2 copies; this seat did not fetch them.

## 1. Tag resolution (`git ls-remote`, rc 0)

```
091b06388b117fefdcb63336ac09956a4914b961	refs/tags/v7.3
c03c1a14507dfaf8b856c2608f9ac216021fc222	refs/tags/v7.3^{}
237a1c39e8dfd3e1c6f1f023eea37a48ec04cc63	refs/tags/v7.2
8d3ae59288f1e7d58d76558a6ee96d533bc5019f	refs/tags/v7.2^{}
```

The tag object and peeled commit agree with the SOURCES cells: S515–S520 say "tag v7.3 (091b06388b11, commit
c03c1a14507d)" and S511–S513 say "tag v7.2 (237a1c39e8df)". `?h=v7.3` and `?h=v7.2` are therefore two distinct,
existing tags whose peeled commits are `c03c1a14507d` and `8d3ae59288f1`.

## 2. v7.3 re-fetch vs the frozen pins — 7 of 7 match

| path | HTTP | bytes | sha256 (fresh fetch) | frozen pin (`_COPIES` = `freeze-sha256.txt`) | match |
|---|---|---|---|---|---|
| `mm/memcontrol.c` | 200 | 165998 | `bdb6159cc2378c44c356b6788f521812f15c4d4936e8b09c66ef70b56bcc41a1` | same | yes |
| `mm/oom_kill.c` | 200 | 34311 | `452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e` | same | yes |
| `lib/percpu_counter.c` | 200 | 10932 | `2c26e67751f939dfb21ff6221884280ae84a2a94a54de4468fb9dc8746130d6d` | same | yes |
| `include/linux/percpu_counter.h` | 200 | 6977 | `4a107bc381b3b5425b8ff441f7487d97ba6883dc6f5b426c4bd361ad7cbef896` | same | yes |
| `include/uapi/asm-generic/errno.h` | 200 | 5826 | `66a5ad60566fdd62e41701bcfc42bfeca5e5696ad1d47d78981575e0c51622be` | same | yes |
| `mm/util.c` | 200 | 43965 | `4dfcce2b8fa8f18c350565950a10248b3590e3d3c0c9335fef6d47daa7a9e1f2` | same | yes |
| `mm/mm_init.c` | 200 | 76467 | `678410005f881a64ae94d180c82174dc4474679b056ace69b6bc3d23978f976c` | same | yes |

`curl_rc=0` on every row; the pin values are the `_COPIES` literals of `.ufo/waves/round-54/count-c1.py:67-84` and
the `corpus/evidence/sources-r54/*.v7.3` / `corpus/evidence/sources-r53/{util.c,mm_init.c}.v7.3` lines of
`evidence/freeze-sha256.txt`. The committed copies (`sha256sum` on the lane) hash to the same values, so
committed copy = frozen pin = today's server bytes for all seven.

First attempt: three of the seven requests came back **HTTP 503** (nginx 190-byte body, curl rc 0) —
`mm/oom_kill.c`, `include/linux/percpu_counter.h`, `mm/mm_init.c`; the other four were 200. Each was retried
sequentially after `sleep 6` and returned 200 on the first retry. A fetch loop that trusts rc alone would have
written the 190-byte error page into the copy (finding 3).

## 3. v7.2 re-fetch vs the lane's committed v7.2 copies — 7 of 7 match

| path @ v7.2 | HTTP | bytes | sha256 (fresh) | lane copy | sha256 of lane copy | match |
|---|---|---|---|---|---|---|
| `mm/memcontrol.c` | 200 | 160768 | `8a28e0bc010e0575fbf9d1739643686e271bcf5a76c0284081df537a4041fd5e` | `sources-r50/memcontrol.c.v7.2` | same | yes |
| `mm/oom_kill.c` | 200 | 34311 | `452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e` | `sources-r50/oom_kill.c.v7.2` | same | yes |
| `mm/util.c` | 200 | 43913 | `e702754c45bd7bd69e5da22a6505c9c1016eaafe6e883b746cc3cdbd413ebe7c` | `sources-r52/util.c.v7.2` | same | yes |
| `mm/mm_init.c` | 200 | 78178 | `ed691b24afbc0dc45090e149d115d707af0c5f7369a10b7722d491075f26a754` | `sources-r53/mm_init.c.v7.2` | same | yes |
| `lib/percpu_counter.c` | 200 | 10932 | `2c26e67751f939dfb21ff6221884280ae84a2a94a54de4468fb9dc8746130d6d` | `sources-r53/percpu_counter.c.v7.2` | same | yes |
| `include/linux/percpu_counter.h` | 200 | 6977 | `4a107bc381b3b5425b8ff441f7487d97ba6883dc6f5b426c4bd361ad7cbef896` | `sources-r53/percpu_counter.h.v7.2` | same | yes |
| `include/uapi/asm-generic/errno.h` | 200 | 5826 | `66a5ad60566fdd62e41701bcfc42bfeca5e5696ad1d47d78981575e0c51622be` | `sources-r48/errno.h` | same | yes |

Every committed v7.2 copy is byte-exact to today's server bytes for the v7.2 tag.

## 4. v7.2 vs v7.3 identity, and the master discriminant

`cmp` on the two fetched sets:

```
mm/oom_kill.c                        IDENTICAL  34311 bytes
lib/percpu_counter.c                 IDENTICAL  10932 bytes
include/linux/percpu_counter.h       IDENTICAL   6977 bytes
include/uapi/asm-generic/errno.h     IDENTICAL   5826 bytes
mm/memcontrol.c                      DIFFERS    160768 -> 165998  (258 changed lines)
mm/util.c                            DIFFERS     43913 ->  43965  (14 changed lines)
mm/mm_init.c                         DIFFERS     78178 ->  76467  (211 changed lines)
```

Four of the seven C1 copies are byte-identical between the two tags. That is a property of the files, not a
copy error: the same four bytes also equal the lane's v7.2 copies from earlier rounds (section 3), and the cgit
`h=` parameter provably discriminates on this server because `mm/oom_kill.c` and `mm/util.c` differ between v7.2
and v7.3 and again from `?h=master`:

```
mm/oom_kill.c                h=master -> 200 34013 sha256 7c2e80300a224dbd1e694827c1bd330ebb5c88150e3ce06939919ce1f8768ec5
mm/util.c                    h=master -> 200 45670 sha256 80f0c2b65ea9f5b95984b372a96ae465348877e3e3f605af4902bbe5ddc85f7e
include/linux/percpu_counter.h h=master -> 200 6977 sha256 4a107bc381b3 (== v7.2 == v7.3)
lib/percpu_counter.c         h=master -> 200 10932 sha256 2c26e67751f9 (== v7.2 == v7.3)
include/uapi/asm-generic/errno.h h=master -> 200 5826 sha256 66a5ad60566f (== v7.2 == v7.3)
```

So `?h=v7.3` is not `?h=master` and not `?h=v7.2` for the files that moved; for the four stable files no tag
choice can be told apart by bytes alone, and none needs to be — the bytes served for v7.3 are the bytes the
lane holds.

Determinism: a second fetch of `mm/memcontrol.c`, `mm/oom_kill.c` and `lib/percpu_counter.c` at `?h=v7.3` gave
200 with sha256 `bdb6159c…`, `452f1348…`, `2c26e677…` — identical to the first fetch. No proxy-injected bytes.

Operational note: `?h=master` answers **301** with a 0-byte body unless `curl -L` is used; `-L` follows to the
tagless URL and returns 200. A fetch helper that omits `-L` and does not check the status writes an empty file.

## 5. Ledger rows checked against the fresh bytes (not against the lane copies)

For each row of `corpus/knowledge/kernel-v7.3-recheck-r54.md` (31 rows, parsed from the `## Ledger` table) this
seat whitespace-collapsed the row's backticked quote, located it in the **freshly fetched** copy of the row's
S-id path, and derived the 1-based line of the raw file on which the occurrence begins. 24 rows are covered by
this seat's seven paths; the other 7 are the S520 rendered-docs rows (out of scope, marked `not checked`).

| h | source | copy | ledger line | computed v7.3 line(s) | computed v7.2 line(s) | verdict |
|---|---|---|---|---|---|---|
| 4aab78fbca9c | S518 | percpu_counter.h | 121 | 121 | 121 | match |
| c8fb3a4fb56f | S517 | percpu_counter.c | 100 | 100 | 100 | match |
| 0d09a65619e5 | S514 | mm_init.c | 198 | 198 | 194 | match |
| 47887dc7067f | S514 | mm_init.c | 203 | 203 | 199 | match |
| da4075a0131e | S514 | mm_init.c | 208 | 208 | 204 | match |
| 196504e1a96c | S508 | util.c | 820 | 820 | 820 | match |
| 3b7ff65291be | S508 | util.c | 937 | 937 | 937 | match |
| 646b97a23371 | S508 | util.c | 994 | 994 | 994 | match |
| 0145725d3c6c | S515 | memcontrol.c | 4997 | 4997 | 4913 | match |
| 16a3733a5002 | S515 | memcontrol.c | 1872 | 1872 | 1827 | match |
| 26b9666a61be | S515 | memcontrol.c | 1824 | 1824 | 1779 | match |
| 90f96cf997c2 | S515 | memcontrol.c | 1845 | 1845 | 1800 | match |
| a4965056de62 | S515 | memcontrol.c | 1854 | 1854 | 1809 | match |
| adf25120cfe8 | S515 | memcontrol.c | 2041 | 2041 | 1996 | match |
| de58513701cb | S515 | memcontrol.c | 1819 | 1819 | 1774 | match |
| f5626c899cea | S515 | memcontrol.c | 1850 | 1850 | 1805 | match |
| 0aa4618b2166 | S516 | oom_kill.c | 446 | 446 | 446 | match |
| 3a75d41492ad | S516 | oom_kill.c | 945 | 945 | 945 | match |
| 53d8f38c2827 | S516 | oom_kill.c | 1169 | 1169 | 1169 | match |
| b962596a058b | S516 | oom_kill.c | 1030 | 1030 | 1030 | match |
| d6bf02678216 | S516 | oom_kill.c | 424 | 424 | 424 | match |
| e4e93c6a050c | S516 | oom_kill.c | 934 | 934 | 934 | match |
| fdc2273230e1 | S516 | oom_kill.c | 465 | 465 | 465 | match |
| 687e03745cd9 | S519 | errno.h | 107 | 107 | 107 | match |

`checked=24 mismatch=0`; every quote occurs exactly once in its v7.3 copy, so the named line is the first line
of the occurrence, not an arbitrary one among several. The computed v7.2 lines also reproduce the ledger's
`## Moved` table exactly (mm_init.c 194→198, 199→203, 204→208 = +4; memcontrol.c 1774→1819 … 4913→4997 = +45 /
+84; util.c, oom_kill.c, percpu_counter.c/.h, errno.h +0), which re-verifies that table from independent bytes.

Set bookkeeping: the 31 ledger hashes and the 31 hashes of `evidence/c1-claims.txt` are the same set (`diff`
empty); per entry 8 `commit-runway-read-r53`, 22 `oom-memcg-stat-r50`, 1 `quota-observability-r48`, matching the
contract's scope sentence; no duplicate hash in the ledger.

## 6. What this seat did not verify

- The seven S520 rows (rendered `docs.kernel.org/7.3/admin-guide/cgroup-v2.html` lines 1225/1409/1430/1437/1443/
  1446/1465) — outside the assigned seven cgit paths; UNVERIFIED here.
- That the counter's own derivation/count agrees at the landed tip — other seats run the counters.
- Dispositions: `holds` on all 31 rows is the L1's pre-vote label; the meaning is the voters' arm, not bytes.
- Server trust: a 200 from cgit and a matching sha256 prove the bytes are reproducible and equal to the pins;
  they do not prove the server served the tag it was asked for. The master/v7.2 discriminants above make a
  wrong-ref answer implausible for the three files that moved; for the four stable files the question is moot.

## Housekeeping

Scratch `/fast/scratch/hyaku/mori-r54/Mo54ExecRefetchCgit/` (mkdir -p, `TMPDIR` inside it) held the 14 fetched
files, the five discriminant/repeat fetches and the verification script; removed with `rm -rf` after this report
was written. No tool installed or upgraded (curl, git, python3 already present; no pacman). No fleet, lane, jj or
git-index mutation — read-only `git ls-remote` against kernel.org only, `sha256sum`/`cmp` on lane copies. No host
sysctl, cgroup, log-line count or memory action. No credential or session material read.

## Findings

1. LOW — the pin arm cannot, by itself, separate a v7.2 relabel from a genuine v7.3 copy for four of the seven C1
   copies, because those files are byte-identical across the two tags: `corpus/evidence/sources-r54/oom_kill.c.v7.3`
   (`452f1348…`), `percpu_counter.c.v7.3` (`2c26e677…`), `percpu_counter.h.v7.3` (`4a107bc3…`) and `errno.h.v7.3`
   (`66a5ad60…`). Ten of the 31 rows (S516 ×7, S517, S518, S519) sit on such copies. The contract's `v72-copies`
   control reading ("v7.2 bytes as v7.3 fail the pins") holds only because `memcontrol.c`, `util.c` and
   `mm_init.c` moved; the separator is those three files, not the pin arm in general. Not a data defect — the
   identity is real, verified against both tags and against `?h=master` — but it should be a named limit in the
   round-54 report and a routed item for round 55 (a per-file tag-unstable floor, or a `changed` row required per
   tag that moved).
2. LOW — `corpus/knowledge/kernel-v7.3-recheck-r54.md` carries no `changed` disposition: all 31 rows are `holds`.
   Consistent with the bytes (every v7.2 quote still occurs at v7.3, section 5), but the disposition arm has zero
   discrimination this round; the only evidence that the recheck is not a blanket relabel is the line/moved arm
   and the byte-level difference in the three changed files. Worth stating in the report rather than leaving the
   all-`holds` shape to be read as a lazy label.
3. LOW — git.kernel.org cgit returned **HTTP 503** (nginx, 190-byte body, curl rc 0) for three of seven first
   attempts, and **301 with a 0-byte body** for `?h=master` without `-L`. A fetch helper that trusts `curl` rc or
   writes the body unconditionally produces a 190-byte or empty "copy" that no pin would catch until the sha256
   check runs. Route to round 55 as an argument for fetch scripts that assert `http_code == 200` and a minimum
   size before replacing a copy (this seat's retries: `sleep 6`, then 200 on the first retry for all three).
4. LOW — 7 of 31 C1 rows (all S520) rest on the rendered `docs.kernel.org/7.3` page, which this seat was not
   assigned to fetch; those rows have no independent byte re-fetch in this wave's evidence from this seat. The
   seven cgit-backed rows sets are fully re-fetched; a docs re-fetch seat should be named explicitly if the wave
   wants the rendered page covered too.
