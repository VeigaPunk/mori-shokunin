# Mo54ExecRefetchGit — independent channel for the C1 and C2 pins (round 54, wave w1)

Seat: `Mo54ExecRefetchGit`, leaf, one v2 wave. Lane `mori-shokunin`. Date 2026-10-27.
Task: re-fetch the v7.3 bytes behind S515–S519 and S521–S524 over a channel other than the L1's copy step
(annotated tag object + blob-filtered fetch + cgit `?h=v7.3`) and compare each blob's sha256 with the copies in
`corpus/evidence/sources-r54/`. Read-only: this seat wrote only this file and its scratch; no counter, predicate,
ledger, entry, SOURCES row or fleet file was touched. No subagents. No tool installs.

Data revision under test: `78295c764093ff1f6cee08d7246679900bde7265` (L1 data commit; per-row claim files added in
that same commit). Freeze commit: `6830f3af992d906bfa1e17e3743e631ab834f67c`. Entering tip: `39dcf4d7e410d362781a47e8365ca23b5c807598`.

## Method (commands verbatim, scratch `/fast/scratch/hyaku/mori-r54/Mo54ExecRefetchGit/`)

```
S=/fast/scratch/hyaku/mori-r54/Mo54ExecRefetchGit
mkdir -p $S/tmp; export TMPDIR=$S/tmp
git -C $S/repo init -q
git -C $S/repo remote add origin https://github.com/torvalds/linux
git -C $S/repo rev-parse --show-toplevel   -> /fast/scratch/hyaku/mori-r54/Mo54ExecRefetchGit/repo
git -C $S/repo fetch --depth 1 --filter=blob:none origin tag v7.3
    -> " * [new tag]         v7.3       -> v7.3", real 0m9.407s, rc=0
git -C $S/repo rev-parse v7.3^{commit}   -> c03c1a14507dfaf8b856c2608f9ac216021fc222
git -C $S/repo rev-parse v7.3            -> 091b06388b117fefdcb63336ac09956a4914b961
git -C $S/repo cat-file -t v7.3          -> tag
git -C $S/repo log -1 --format='%H %ci %s' v7.3^{commit}
    -> c03c1a14507dfaf8b856c2608f9ac216021fc222 2026-10-18 13:14:58 -1000 Linux 7.3
```

No full clone: depth 1, `--filter=blob:none`; the tree objects arrived with the commit, blobs on demand by sha1
(git verifies the sha1 of every promisor blob it writes, so a served blob is by construction the v7.3 tree blob).

Fetch of the nine blobs, `git show v7.3:<path>` into `repo/out/`, plus the same nine over the authorised cgit
channel into `cgit/`:

```
curl -sS -o <f> -w '%{http_code}' "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/<path>?h=v7.3"
```

Independent structural check per file (does the refetched byte stream hash to the v7.3 tree entry?):

```
git -C $S/repo ls-tree v7.3 -- <path>        # blob sha1 recorded in the commit's tree
git -C $S/repo hash-object -t blob -- <refetched file>
```

Registry and freeze consistency:

```
sha256sum corpus/evidence/sources-r54/*.v7.3 corpus/evidence/sources-r54/cgroup-v2.7.3.html
git -C mori-shokunin show 78295c76:corpus/evidence/sources-r54/<f> | sha256sum
grep -n 'sources-r54' .ufo/waves/round-54/evidence/freeze-sha256.txt
```

## Result 1 — tag identity agrees on both hosts and with the registry

- GitHub annotated tag object `091b06388b117fefdcb63336ac09956a4914b961` → commit
  `c03c1a14507dfaf8b856c2608f9ac216021fc222`, subject `Linux 7.3`, commit date 2026-10-18 13:14:58 -1000.
- kernel.org cgit tag page (`…/tag/?h=v7.3`, http 200, 4247 bytes) reports the same object
  `091b06388b117fefdcb63336ac09956a4914b961`, the same commit `c03c1a14507dfaf8b856c2608f9ac216021fc222`,
  subject `Linux 7.3`, and a PGP signature block.
- `corpus/SOURCES.md` rows S515–S524 and S521–S524 all record `tag v7.3 (091b06388b11, commit c03c1a14507d)`.
  Agreement: exact, on both hosts.

## Result 2 — per path: nine code/doc blobs, all EQUAL

Every refetched byte stream (a) sha256-matches the `sources-r54` copy, (b) sha256-matches the copy committed at the
data revision R, and (c) hashes to the blob sha1 recorded in the v7.3 tree. Channel column: GH = GitHub promisor
`git show v7.3:<path>`, CG = cgit `?h=v7.3` (http 200 for all nine).

| row | path | refetch channels | v7.3 tree blob sha1 | sha256 (refetched = copy) | verdict |
|---|---|---|---|---|---|
| S515 | mm/memcontrol.c | GH + CG | 856a7d07586cccee71858804c961b5d38352e68e | bdb6159cc2378c44c356b6788f521812f15c4d4936e8b09c66ef70b56bcc41a1 | equal |
| S516 | mm/oom_kill.c | GH + CG | 5f372f6e26fa329d3152fac961a7bdb82d7f06cd | 452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e | equal |
| S517 | lib/percpu_counter.c | CG (GH 429) | 2891f94a11c654958fb52f8d965d06b62719500c | 2c26e67751f939dfb21ff6221884280ae84a2a94a54de4468fb9dc8746130d6d | equal |
| S518 | include/linux/percpu_counter.h | CG (GH 429) | 3a44dd1e33d241589fce9fb8b629cd6fa32c6a12 | 4a107bc381b3b5425b8ff441f7487d97ba6883dc6f5b426c4bd361ad7cbef896 | equal |
| S519 | include/uapi/asm-generic/errno.h | CG (GH 429) | bd78e69e0a43f190dffb9870e9cc68d5391f2b8d | 66a5ad60566fdd62e41701bcfc42bfeca5e5696ad1d47d78981575e0c51622be | equal |
| S521 | mm/memory-failure.c | CG (GH 429) | a8b03e2920ba8accd7861b8411548d8238dcd4cc | 94d24a605b61f94ad1d10ab3db26aed12cb6113af15431ff873da5b98ca48003 | equal |
| S522 | Documentation/mm/hwpoison.rst | CG (GH 429) | 71b4b45c350555be89fcb60afe76d024809b39ea | 8011bb158129776bbb38ed5808959bd14d17489527ed3987dbc3d21d27e3ecb7 | equal |
| S523 | Documentation/ABI/stable/sysfs-devices-node | GH + CG | 2d0e023f22a71abbe2399ab0c121239c7f9182aa | d852f950e42d92b862792477a892e77973ddb6a345bdb1748d2e7c5020198665 | equal |
| S524 | include/trace/events/memory-failure.h | GH + CG | 7a8ee5d1a44e4d0d9aa04a42cf5b13d5dd67c3b9 | a395e62b36ace3d1295fd3e9e469fc525f67c7787f529a380633d6b800f051ea | equal |

Sizes as served: memcontrol.c 165998, oom_kill.c 34311, percpu_counter.c 10932, percpu_counter.h 6977, errno.h 5826,
memory-failure.c 82847, hwpoison.rst 6026, sysfs-devices-node 8149, memory-failure-trace.h 2964 bytes.

`git hash-object` comparison, one line per path (`tree=` from `ls-tree v7.3`, `refetched=` from `hash-object`); the
two columns are identical in all nine rows, so the cgit and GitHub byte streams are the same objects the v7.3 commit
tree names:

```
tree=856a7d07586cccee71858804c961b5d38352e68e refetched=856a7d07586cccee71858804c961b5d38352e68e mm/memcontrol.c
tree=5f372f6e26fa329d3152fac961a7bdb82d7f06cd refetched=5f372f6e26fa329d3152fac961a7bdb82d7f06cd mm/oom_kill.c
tree=2891f94a11c654958fb52f8d965d06b62719500c refetched=2891f94a11c654958fb52f8d965d06b62719500c lib/percpu_counter.c
tree=3a44dd1e33d241589fce9fb8b629cd6fa32c6a12 refetched=3a44dd1e33d241589fce9fb8b629cd6fa32c6a12 include/linux/percpu_counter.h
tree=bd78e69e0a43f190dffb9870e9cc68d5391f2b8d refetched=bd78e69e0a43f190dffb9870e9cc68d5391f2b8d include/uapi/asm-generic/errno.h
tree=a8b03e2920ba8accd7861b8411548d8238dcd4cc refetched=a8b03e2920ba8accd7861b8411548d8238dcd4cc mm/memory-failure.c
tree=71b4b45c350555be89fcb60afe76d024809b39ea refetched=71b4b45c350555be89fcb60afe76d024809b39ea Documentation/mm/hwpoison.rst
tree=2d0e023f22a71abbe2399ab0c121239c7f9182aa refetched=2d0e023f22a71abbe2399ab0c121239c7f9182aa Documentation/ABI/stable/sysfs-devices-node
tree=7a8ee5d1a44e4d0d9aa04a42cf5b13d5dd67c3b9 refetched=7a8ee5d1a44e4d0d9aa04a42cf5b13d5dd67c3b9 include/trace/events/memory-failure.h
```

## Result 3 — S520 rendered page: equal today (not a git object)

`https://docs.kernel.org/7.3/admin-guide/cgroup-v2.html` → http 200, 172967 bytes,
sha256 `b478c1bae99899df476d6b4989cbb516f7ca93c5f009cdff64b802bbc24f3d4b` = the `sources-r54/cgroup-v2.7.3.html`
copy, and the page's only version token is `7.3.0`. This path has no git blob to anchor it (see limit L1 below).

## Result 4 — freeze list, data revision and registry agree

All ten copies are listed in `.ufo/waves/round-54/evidence/freeze-sha256.txt` lines 24–33 with exactly the sha256
this seat computed, and each copy at data revision R (`git show 78295c76:corpus/evidence/sources-r54/<f>`) is
byte-identical to the working-tree file and to the upstream blob. 10/10 `same`.

Registry prefixes re-derived from the bytes, all ten matching the `sha256 <12 hex>` cell of `corpus/SOURCES.md`:
S515 `bdb6159cc237`, S516 `452f1348e79c`, S517 `2c26e67751f9`, S518 `4a107bc381b3`, S519 `66a5ad60566f`,
S520 `b478c1bae998`, S521 `94d24a605b61`, S522 `8011bb158129`, S523 `d852f950e42d`, S524 `a395e62b36ac`.

## Result 5 — the anchors the rows cite land where the rows say

Boundary lines printed from the `sources-r54` copies (which are now proven upstream bytes). Every cited anchor
resolves to the construct the row describes:

```
memory-failure.c:37   #define pr_fmt(fmt) "Memory failure: " fmt
memory-failure.c:72   static int sysctl_memory_failure_early_kill __read_mostly;
memory-failure.c:78   static int sysctl_panic_on_unrecoverable_mf __read_mostly;
memory-failure.c:134  static const struct ctl_table memory_failure_table[] = {
memory-failure.c:171  };
memory-failure.c:286  static int kill_proc(struct to_kill *tk, unsigned long pfn, int flags)
memory-failure.c:311  }
memory-failure.c:462  static void kill_procs(struct list_head *to_kill, bool forcekill,
memory-failure.c:490  }
memory-failure.c:871  static const char *action_name[] = {
memory-failure.c:876  };
memory-failure.c:1281 static int action_result(unsigned long pfn, enum mf_action_page_type type,
memory-failure.c:1298 }
memory-failure-trace.h:7    #define TRACE_SYSTEM ras
memory-failure-trace.h:74   TRACE_EVENT(memory_failure_event,
memory-failure-trace.h:98   );
hwpoison.rst:54   Failure recovery modes
hwpoison.rst:74   User control
sysfs-devices-node:192  What:  /sys/devices/system/node/nodeX/memory_failure/total
sysfs-devices-node:229  recovered by memory error recovery attempt.
memcontrol.c:1850 pr_info("memory: usage %llukB, limit %llukB, failcnt %lu\n",
memcontrol.c:1854 pr_info("swap: usage %llukB, limit %llukB, failcnt %lu\n",
memcontrol.c:2041 pr_info("Tasks in ");
oom_kill.c:465    if (is_memcg_oom(oc))
oom_kill.c:945    pr_err("%s: Killed process %d (%s) total-vm:%lukB, anon-rss:%lukB, file-rss:%lukB, ...
percpu_counter.c:100  if (unlikely(abs(count + amount) >= batch)) {
percpu_counter.h:121  s64 ret = READ_ONCE(fbc->count);
errno.h:107           #define EDQUOT 122 /* Quota exceeded */
```

Line-count ceilings also hold for every cited line (max cited line ≤ file length): memcontrol.c 4997/6218,
oom_kill.c 1169/1257, percpu_counter.c 100/407, percpu_counter.h 121/286, errno.h 107/127,
memory-failure.c 1298/3029, hwpoison.rst 105/182, sysfs-devices-node 229/238, memory-failure-trace.h 98/102,
cgroup-v2.7.3.html 1465/3314.

## Result 6 — three of the ten v7.3 copies are byte-identical to their v7.2 twins

```
2c26e67751f9...  sources-r53/percpu_counter.c.v7.2  ==  sources-r54/percpu_counter.c.v7.3
4a107bc381b3...  sources-r53/percpu_counter.h.v7.2  ==  sources-r54/percpu_counter.h.v7.3
66a5ad60566f...  sources-r48/errno.h                ==  sources-r54/errno.h.v7.3
```

This confirms S519's own parenthetical ("byte-identical to v7.2, same sha256 as S481's copy") and quantifies the
contract's named limit: for three of the ten copies the pin arm cannot separate a v7.2 relabel from a real v7.3
fetch, because the bytes are the same in both releases. For the other seven the pin arm does separate them.

## Environment facts (recorded, not a lane defect)

A single depth-1 blobless fetch plus nine `git show` calls exhausted GitHub's blob endpoint: four blobs served
(memcontrol.c, oom_kill.c, sysfs-devices-node, memory-failure-trace.h), five refused with
`remote: This request was rate-limited due to too many requests` / `fatal: unable to access …: The requested URL returned error: 429`.
The authorised cgit `?h=v7.3` channel served all nine with http 200, so no path is unverified — but a seat that can
reach only GitHub cannot complete this check on this host right now.

## Limits of this check (mine, named)

- L1. S520 is a rendered page, not a content-addressed object. My equality reading (`b478c1bae998…`, footer 7.3.0)
  is a point-in-time agreement; docs.kernel.org re-renders per minor release, so a later re-fetch can legitimately
  differ while the content is unchanged. The pin is still the only available anchor for that row.
- L2. I proved the bytes at these nine paths are the v7.3 bytes and that the copies hold them. I did not prove any
  ledger row's disposition or any C2 entailment — that is the voters' arm, and my channel does not make me an
  independent judge of those words.
- L3. The GitHub side of the comparison is a sha1-addressed promisor fetch: it proves "the object the v7.3 tree
  names", and the tag object agrees with kernel.org's annotated tag, but neither host's `v7.3` ref is
  cryptographically attested by me beyond the PGP block being present on the cgit tag page (not verified against a
  keyring).
- L4. Anchor spot-check: I printed boundary lines, not every line of every cited range; an off-by-one inside a
  range would not be caught here.

Scratch `/fast/scratch/hyaku/mori-r54/Mo54ExecRefetchGit` (4.1 MB) was removed after this report was written.

## Findings

1. LOW — `corpus/SOURCES.md` S520 row + `corpus/evidence/sources-r54/cgroup-v2.7.3.html`: the only non-git pin in
   the round-54 pin set. It matches today (sha256 `b478c1bae998…`, footer 7.3.0), but a rendered page is mutable, so
   a future `pins=bad` on that row can be a re-render rather than a data error. Pin rules are frozen this round;
   route to round 55 (e.g. record the render date alongside the sha256, or accept it as a point-in-time anchor).
2. LOW — environment: GitHub's promisor blob endpoint answered 429 for five of the nine blobs during a single
   `--depth 1 --filter=blob:none` fetch (2026-10-27). The cgit `?h=v7.3` fallback served all nine. Any future seat
   told to verify pins "over git" should budget for this and prefer cgit or one batched `git cat-file --batch`.
3. LOW — `corpus/SOURCES.md` S517, S518, S519 rows: three of the ten v7.3 copies are byte-identical to their v7.2
   counterparts (`lib/percpu_counter.c`, `include/linux/percpu_counter.h`, `include/uapi/asm-generic/errno.h`). The
   pins are honest, but the pin arm alone cannot show those three rows were re-read at v7.3; the line arm and the
   votes carry that. Already a named limit in the contract; this is its measured size (3 of 10 copies).
4. INFO — no divergence found: nine of nine git blobs and the one rendered page are byte-identical to the copies in
   `corpus/evidence/sources-r54/`, to the copies at data revision `78295c76`, and to the sha256 recorded in
   `freeze-sha256.txt` (lines 24–33) and in the `corpus/SOURCES.md` anchor cells. This seat raises no data
   correction.
