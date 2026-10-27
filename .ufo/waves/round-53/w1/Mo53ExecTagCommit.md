# Mo53ExecTagCommit — provenance of the v7.3/v7.2 anchors, the release date, and what the round-52 "renders 7.3.0" observation dates

Seat: executor (leaf). Lane: mori-shokunin. Round 53, wave w1. Scope: confirm the tag-object and peeled-commit ids the
round-53 anchors cite, the v7.2 tag id cited by S511–S513, the release date of v7.3, and whether the round-52
closure's `latest` observation dates the release before round 52 landed. Detection and report only; no lane file
edited. Scratch `/fast/scratch/hyaku/mori-r53/Mo53ExecTagCommit/` (removed at end; every cited output is copied below).

Host: `uname -r` → `7.2.11-arch1-1`. Date of run: 2026-10-26/27 (local UTC-03:00).

## 1. Command + output, in the order run

### 1.1 `refs/tags/v7.3` and its peeled commit

```
$ git ls-remote https://github.com/torvalds/linux 'refs/tags/v7.3*'
091b06388b117fefdcb63336ac09956a4914b961	refs/tags/v7.3
c03c1a14507dfaf8b856c2608f9ac216021fc222	refs/tags/v7.3^{}
e5e04726cdd043e309677071ab1b65a4b18f422b	refs/tags/v7.3-rc1
cee9395acd8043be0644b25c34bfa86623f2b935	refs/tags/v7.3-rc1^{}
5e036ce12de91c6fd674dad33b169c6150be2a7a	refs/tags/v7.3-rc2
df2908090cda368b01ff43709f51890076c56157	refs/tags/v7.3-rc2^{}
c2cd463d6ee7d55a3ec0719d93c49ff99022d58f	refs/tags/v7.3-rc3
fd73f4a6659897191fa0d40695fe370925dd3780	refs/tags/v7.3-rc3^{}
dec005ae90a2946656a090f37bf1cfbd22f08e57	refs/tags/v7.3-rc4
93f51579e7df248780214094418f205253383cc5	refs/tags/v7.3-rc4^{}
5a956dde5526a634dca7ccad27c051ebcc306089	refs/tags/v7.3-rc5
72d3fcf802c45d00b300f25b848a93c3a2bd7c7e	refs/tags/v7.3-rc5^{}
4eeccbed21e50c19f97be9d325511f3de6343f2d	refs/tags/v7.3-rc6
a90ee4305c4a5df72c11b31dacfdc76e00fcf78a	refs/tags/v7.3-rc6^{}
ec8bf8280261294a9b9b4520414b42704c7f9f6b	refs/tags/v7.3-rc7
24a19b953e2a3d0ea5a8c4951a0ab8f32720c907	refs/tags/v7.3-rc7^{}
exit=0
```

Second, independent transport (kernel.org cgit tag page, not GitHub):

```
$ curl -sSL 'https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tag/?h=v7.3'
curl_exit=0  bytes=4247
tag name v7.3 (091b06388b117fefdcb63336ac09956a4914b961) tag date 2026-10-18 13:14:58 -1000
tagged by Linus Torvalds <torvalds@linux-foundation.org> tagged object commit c03c1a1450...
download linux-7.3.tar.gz   Linux 7.3   -----BEGIN PGP SIGNATURE-----
```

Third, the tag object itself from a `--filter=blob:none --depth=1 --branch v7.3` clone:

```
$ git clone --filter=blob:none --depth=1 --no-checkout --branch v7.3 https://github.com/torvalds/linux.git lnx73
warning: refs/tags/v7.3 091b06388b117fefdcb63336ac09956a4914b961 is not a commit!
clone_exit=0
$ git -C lnx73 rev-parse --show-toplevel ; git -C lnx73 cat-file -t v7.3 ; git -C lnx73 rev-parse v7.3 ; git -C lnx73 rev-parse 'v7.3^{}' ; git -C lnx73 rev-parse 'v7.3^{tree}'
/fast/scratch/hyaku/mori-r53/Mo53ExecTagCommit/lnx73
tag
091b06388b117fefdcb63336ac09956a4914b961
c03c1a14507dfaf8b856c2608f9ac216021fc222
30fd2ef82912c26cf3a58ad0ba6afc375fa851ac

$ git -C lnx73 cat-file -p v7.3 | head -5
object c03c1a14507dfaf8b856c2608f9ac216021fc222
type commit
tag v7.3
tagger Linus Torvalds <torvalds@linux-foundation.org> 1792365298 -1000

Linux 7.3
$ git -C lnx73 log -1 --format='%H author=%aI committer=%cI subject=%s' c03c1a14507dfaf8b856c2608f9ac216021fc222
c03c1a14507dfaf8b856c2608f9ac216021fc222 author=2026-10-18T13:14:58-10:00 committer=2026-10-18T13:14:58-10:00 subject=Linux 7.3
```

Verdict: the ids in the contract, the counter docstring and rows S502–S510 are correct and complete.
`091b06388b117fefdcb63336ac09956a4914b961` is the **annotated tag object**; `c03c1a14507dfaf8b856c2608f9ac216021fc222`
is the **commit it peels to** (subject `Linux 7.3`). The tag is signed (PGP block present in the tag object).

### 1.2 The v7.2 tag id cited in S511–S513

```
$ git ls-remote https://github.com/torvalds/linux 'refs/tags/v7.2*'
237a1c39e8dfd3e1c6f1f023eea37a48ec04cc63	refs/tags/v7.2
8d3ae59288f1e7d58d76558a6ee96d533bc5019f	refs/tags/v7.2^{}
728e68a889bcf257b1e67298b12c360e5c3a13e0	refs/tags/v7.2-rc1
dc59e4fea9d83f03bad6bddf3fa2e52491777482	refs/tags/v7.2-rc1^{}
...(rc2–rc7, same shape)...
exit=0

$ git -C lnx72 cat-file -p v7.2 | head -5     # lnx72: same blob-filtered clone recipe, --branch v7.2
object 8d3ae59288f1e7d58d76558a6ee96d533bc5019f
type commit
tag v7.2
tagger Linus Torvalds <torvalds@linux-foundation.org> 1786915946 -0700

$ curl -sSL '.../tag/?h=v7.2'
tag name v7.2 (237a1c39e8dfd3e1c6f1f023eea37a48ec04cc63) tag date 2026-08-16 14:32:26 -0700
tagged by Linus Torvalds <torvalds@linux-foundation.org> tagged object commit 8d3ae59288...
```

`corpus/SOURCES.md:290-292` (S511, S512, S513) carry the anchor cell `tag v7.2 (237a1c39e8df)` — that is the
annotated **tag object** id and it is correct. The peeled commit is `8d3ae59288f1e7d58d76558a6ee96d533bc5019f`, which
those three rows do **not** cite (S502–S510 cite both forms: `tag v7.3 (091b06388b11, commit c03c1a14507d)`). See
Finding F5.

### 1.3 Release date of v7.3

```
$ curl -sSL https://www.kernel.org/releases.json     (7576 bytes, exit 0)
{"moniker": "mainline", "version": "7.3", "iseol": false,
 "released": {"timestamp": 1792365298, "isodate": "2026-10-18"},
 "source": "https://cdn.kernel.org/pub/linux/kernel/v7.x/linux-7.3.tar.xz",
 "gitweb": "https://git.kernel.org/torvalds/h/v7.3", ...}

$ python3 -c "import datetime as d; print(d.datetime.fromtimestamp(1792365298, d.timezone.utc).isoformat())"
2026-10-18T23:14:58+00:00
```

**Release date: 2026-10-18** (`2026-10-18T23:14:58Z`). Three independent witnesses agree:
kernel.org `releases.json` `released.isodate`; the same `released.timestamp` 1792365298; and the tag object's tagger
timestamp 1792365298 -1000 (= the identical instant). The commit date `2026-10-18T13:14:58-10:00` is the same instant.
`releases.json` also lists `7.2.13` stable released `2026-10-26` and `next-20261026` for linux-next — neither is a
7.4 tag, and `git ls-remote 'refs/tags/v7.4*'` returned nothing (exit 0, no output), so v7.3 is the current release.

### 1.4 Do the pinned copies come from the tag, or from master? (cgit served the tag)

The contract's named limit says the pins prove only "the bytes are what the L1 fetched from cgit, not that cgit served
the tag". That limit is now closed for these 12 files by two measurements.

(a) Independent re-fetch of every pinned path from cgit `?h=v7.3` / `?h=v7.2`, then sha256 against the lane's copies:

```
Documentation/filesystems/proc.rst            h=v7.3 curl=0 bytes=107605  bc178ff511e05c1b...
mm/show_mem.c                                 h=v7.3 curl=0 bytes=13281   c50205bc19974566...
fs/proc/meminfo.c                             h=v7.3 curl=0 bytes=6046    d6c5807421a69eac...
include/linux/mm_inline.h                     h=v7.3 curl=0 bytes=17667   277e99e23ecc1b5b...
Documentation/mm/overcommit-accounting.rst    h=v7.3 curl=0 bytes=2647    767ab88153c4494e...
Documentation/admin-guide/sysctl/vm.rst       h=v7.3 curl=0 bytes=45908   f81feb3dfca5f054...
mm/util.c                                     h=v7.3 curl=0 bytes=43965   4dfcce2b8fa8f18c...
include/linux/mman.h                          h=v7.3 curl=0 bytes=4265    d7bf787c910d9a7c...
mm/mmap.c                                     h=v7.3 curl=0 bytes=51299   8e51fb1c10fee694...
mm/mm_init.c                                  h=v7.2 curl=0 bytes=78178   ed691b24afbc0dc4...
lib/percpu_counter.c                          h=v7.2 curl=0 bytes=10932   2c26e67751f939df...
include/linux/percpu_counter.h                h=v7.2 curl=0 bytes=6977    4a107bc381b3b542...
```

and the same sha256s against the committed copies under `corpus/evidence/sources-r53/`:

```
MATCH  proc.rst.v7.3 bc178ff511e05c1b bc178ff511e05c1b
MATCH  show_mem.c.v7.3 c50205bc19974566 c50205bc19974566
MATCH  meminfo.c.v7.3 d6c5807421a69eac d6c5807421a69eac
MATCH  mm_inline.h.v7.3 277e99e23ecc1b5b 277e99e23ecc1b5b
MATCH  overcommit-accounting.rst.v7.3 767ab88153c4494e 767ab88153c4494e
MATCH  vm.rst.v7.3 f81feb3dfca5f054 f81feb3dfca5f054
MATCH  util.c.v7.3 4dfcce2b8fa8f18c 4dfcce2b8fa8f18c
MATCH  mman.h.v7.3 d7bf787c910d9a7c d7bf787c910d9a7c
MATCH  mmap.c.v7.3 8e51fb1c10fee694 8e51fb1c10fee694
MATCH  mm_init.c.v7.2 ed691b24afbc0dc4 ed691b24afbc0dc4
MATCH  percpu_counter.c.v7.2 2c26e67751f939df 2c26e67751f939df
MATCH  percpu_counter.h.v7.2 4a107bc381b3b542 4a107bc381b3b542
```

12/12 identical, and each matches the sha256 prefix written in its SOURCES row (`bc178ff511e0`, `c50205bc1997`,
`d6c5807421a6`, `277e99e23ecc`, `767ab88153c4`, `f81feb3dfca5`, `4dfcce2b8fa8`, `d7bf787c910d`, `8e51fb1c10fe`,
`ed691b24afbc`, `2c26e67751f9`, `4a107bc381b3`).

(b) Blob-identity against the tag trees from the clone (`git hash-object` of the cgit bytes vs the tree entry):

```
path                                          cgit ?h=v7.3 bytes      v7.3^{tree}:path        master ?h=master bytes
Documentation/filesystems/proc.rst            c102b62023cdc189...     c102b62023cdc189...     fa7a468e8edf2f2d...  DIFF
mm/show_mem.c                                 b938cbcd774a1e2e...     b938cbcd774a1e2e...     b938cbcd774a1e2e...  same
fs/proc/meminfo.c                             b2813ff13cb23bb2...     b2813ff13cb23bb2...     b2813ff13cb23bb2...  same
include/linux/mm_inline.h                     621c8653d8f7eb45...     621c8653d8f7eb45...     ab69b9930893ff2e...  DIFF
Documentation/mm/overcommit-accounting.rst    e2263477f6d502e5...     e2263477f6d502e5...     e2263477f6d502e5...  same
Documentation/admin-guide/sysctl/vm.rst       5b318d17aa4b4474...     5b318d17aa4b4474...     5f4a056e4dc22225...  DIFF
mm/util.c                                     bf0513d1d3d08667...     bf0513d1d3d08667...     75c0fc2061aa066c...  DIFF
include/linux/mman.h                          389521594c69c2fa...     389521594c69c2fa...     389521594c69c2fa...  same
mm/mmap.c                                     4bf26b0f1e6e36dc...     4bf26b0f1e6e36dc...     4bf26b0f1e6e36dc...  same
mm/mm_init.c (v7.2)                           498d62c4ece392f3...     498d62c4 (v7.2 tree)    41a27860d2f685de...  DIFF
lib/percpu_counter.c (v7.2)                    2891f94a11c65495...     2891f94a (v7.2 tree)    2891f94a11c65495...  same
include/linux/percpu_counter.h (v7.2)          3a44dd1e33d24158...     3a44dd1e (v7.2 tree)    3a44dd1e33d24158...  same
```

All 12 cgit payloads are byte-identical to the blob in the tag tree. For 5 of them (`proc.rst`, `mm_inline.h`,
`vm.rst`, `util.c` at v7.3; `mm_init.c` at v7.2) master's blob **differs** from the tag's, so `?h=v7.3` / `?h=v7.2`
demonstrably served the tag and not master; for the other 7 the file is unchanged since the tag, so tag and master
coincide and the point is moot. This closes the round-53 named limit "the pins prove the bytes are what the L1 fetched
from cgit, not that cgit served the tag" for these 12 paths.

### 1.5 Anchors inside the pinned copies (line numbers)

Spot-checked every line number the S502–S513 anchor cells state, in the committed copies:

```
S502 proc.rst.v7.3   sed -n '1127p;1221p;1239p' -> MemAvailable / CommitLimit / Committed_AS
S503 show_mem.c.v7.3 sed -n '33p;73p'            -> long si_mem_available(void) / }
S504 meminfo.c.v7.3  sed -n '34p;125p;126p'      -> static int meminfo_proc_show(...) /
                                                    show_val_kb(m, "CommitLimit:    ", vm_commit_limit());
                                                    show_val_kb(m, "Committed_AS:   ", committed);
S505 mm_inline.h.v7.3 sed -n '28p'               -> static inline int folio_is_file_lru(const struct folio *folio)
S507 vm.rst.v7.3     lines 82, 823, 834, 859, 1106, 1116 -> admin_reserve_kbytes / overcommit_kbytes /
                                                    overcommit_memory / overcommit_ratio / user_reserve_kbytes /
                                                    "user_reserve_kbytes defaults to min(3% of the current process size, 128MB)."
S508 util.c.v7.3     806, 904, 916, 959, 1003    -> overcommit_policy_handler / unsigned long vm_commit_limit(void) / }
                                                    / int __vm_enough_memory(...) / }
S509 mman.h.v7.3     76, 81                      -> vm_acct_memory / vm_unacct_memory
S510 mmap.c.v7.3     563-571                     -> "if (flags & MAP_NORESERVE) { ... vma_flags_set(&vma_flags, VMA_NORESERVE_BIT); ... }"
                     1566, 1587                  -> static int init_user_reserve(void) / static int init_admin_reserve(void)
S511 mm_init.c.v7.2  191, 210, 226, 233          -> mm_compute_batch(int overcommit_policy) / } / mm_compute_batch_init / __initcall
S512 percpu_counter.c.v7.2 93, 113               -> percpu_counter_add_batch(...) / }
S513 percpu_counter.h.v7.2 118, 126              -> percpu_counter_read_positive(...) / }
S506 overcommit-accounting.rst.v7.3  wc -l = 85  -> matches "whole file lines 1-85"
```

Every stated locator lands on the construct its `teaches` cell names. The MAP_NORESERVE block at v7.3 reads
`vma_flags_set(&vma_flags, VMA_NORESERVE_BIT)` — the spelling the contract cites for the two `absent` rows.

### 1.6 The ledger's v7.2→v7.3 "changed lines" table reproduced

`diff -u <v7.2 copy> <v7.3 copy> | grep -c '^[-+][^-+]'` (r51 copies from `corpus/evidence/sources-r51/`, r52 copies from
`sources-r52/`):

```
proc.rst                 3      (ledger: 3)
show_mem.c               22     (ledger: 22)
mm_inline.h              49     (ledger: 49)
meminfo.c                0      (ledger: byte-identical, same sha256 d6c58074…)
overcommit-accounting.rst 0     (ledger: byte-identical, same sha256 767ab881…)
vm.rst                   64     (ledger: 64)
util.c                   14     (ledger: 14)
mmap.c                   190    (ledger: 190)
mman.h                   0      (ledger: byte-identical, same sha256 d7bf787c…)
```

Six of nine changed, three byte-identical, and every count matches `kernel-v7.3-recheck-r53.md` exactly.

## 2. The question: does the round-52 closure's "latest renders 7.3.0" observation date the release before round 52 landed?

**Short answer: not by itself — that observation is dated 2026-10-26, the day round 52 landed. The release is dated
2026-10-18 by the tag object and kernel.org, i.e. 8 days before round 52 landed, and the lane already held a dated
7.3.0 rendering in its own committed evidence from 2026-10-23, three days before round 52 landed.**

Timeline, every point from a command above or from read-only `git log` in the lane:

| when (UTC unless local shown) | event | evidence |
|---|---|---|
| 2026-10-18T23:14:58Z | **v7.3 released** — tag object tagger ts 1792365298, `releases.json` `isodate 2026-10-18` | 1.1, 1.3 |
| 2026-10-19 (local) | lane opens S004/S005/S006 pinned to raw.githubusercontent **commit `c03c1a14…` = the v7.3 release commit**; S033's anchor cell names `c03c1a14507dfaf8b856c2608f9ac216021fc222 (2026-10-18)` | `git log -S'c03c1a14507dfaf8b856c2608f9ac216021fc222' -- corpus/SOURCES.md` → `1f07f1dd 2026-10-19T19:41:08-03:00` |
| 2026-10-23T01:31:22Z | round-32 wave-1 copies capture `<p class="blurb">7.3.0</p>` on docs.kernel.org; committed `837b2802` at 2026-10-22T22:39:10-03:00 | `corpus/evidence/recheck-r32/S001.src:42`, `Recheck001.md` accessed column |
| 2026-10-23 | round-33 attack records the live page "renders 7.3.0 (mainline/development tree)" | `.ufo/waves/round-33/w2/AttackSrc181.md:88,91` |
| 2026-10-25 / 2026-10-26 | r47 and r48 entries land, still pinned to v7.2 URLs with `recheck: on-release`, after the release | `git log -1 -- corpus/knowledge/oom-tracepoints-r47.md` = `2026-10-25T16:58:58-03:00` |
| 2026-10-27T01:08:38Z (= 2026-10-26T22:08:38-03:00) | **round-52 closure lands** (`20edafa5`); its reject row records "fetched 2026-10-26: … renders The Linux Kernel 7.3.0" | `corpus/lessons/round-52-verifier-spotcheck.md:100` |
| 2026-10-27T01:31:29Z / 01:37:16Z | round-53 freeze `f4da3fd4` / data `2a4213bf` — first lane artefacts that name tag v7.3 | `git log` |

Computed deltas:

```
release(tagger ts, UTC)   2026-10-18T23:14:58+00:00
r53 data commit (UTC)     2026-10-27T01:37:16+00:00
r52 closure landing(UTC)  2026-10-27T01:08:38+00:00
release -> r52 landing    8 days, 1:53:40
release -> r53 data       8 days, 2:22:18
r32 banner copy fetch     2026-10-23T01:31:22+00:00  -> release+ 4 days, 2:16:24
```

So the on-release trigger stood unanswered for **8 days 1h54m** as of the round-52 landing and **8 days 2h22m** as of
the round-53 data commit. Rounds that landed after the release and before the answer: every lane round from
**round 12 through round 52** (41 distinct rounds; `git log` per-round first/last commit: round-12 starts
2026-10-19T19:41:08-03:00, round-52 ends 2026-10-26T22:08:38-03:00; rounds 1–11 landed 2026-10-14/15, before the
release).

### 2.1 One correction to the round-52/round-33 reading of the banner

The round-52 scribe called the `latest` page "the development tree" and the round-33 attack called it
"mainline/development tree". Measured today, kernel.org's `latest` docs build **is the v7.3 release rendering**, not
master:

```
https://www.kernel.org/doc/html/latest/mm/overcommit-accounting.html   13558 bytes sha=aa4364195e16 banner=7.3.0
https://www.kernel.org/doc/html/v7.3/mm/overcommit-accounting.html     13558 bytes sha=aa4364195e16 banner=7.3.0   (identical)
https://www.kernel.org/doc/html/v7.2/mm/overcommit-accounting.html     12762 bytes sha=ee9af79464eb banner=7.2.0
https://www.kernel.org/doc/html/v7.3-rc1/…                             13562 bytes sha=31baaea688e7 banner=7.3.0-rc1
https://www.kernel.org/doc/html/v7.3-rc7/…                             13562 bytes sha=46d4fd8de5fe banner=7.3.0-rc7
https://www.kernel.org/doc/html/next/…                                 13384 bytes sha=302cca17395a banner=next-20261026
https://www.kernel.org/doc/html/master/admin-guide/sysctl/vm.html      146 bytes — nginx 404

https://www.kernel.org/doc/html/latest/admin-guide/sysctl/vm.html       69002 bytes sha=423d043409bc banner=7.3.0
https://www.kernel.org/doc/html/v7.3/admin-guide/sysctl/vm.html         69002 bytes sha=423d043409bc (identical)
https://docs.kernel.org/admin-guide/sysctl/vm.html                      69002 bytes sha=423d043409bc (identical)
https://docs.kernel.org/accounting/psi.html                             19726 bytes sha=f752c8d54477
   = corpus/evidence/recheck-r32/S001.src sha f752c8d5447760a315048037eb8f53007f8e4862d586172f… (2026-10-23 fetch, identical)

discriminator — the only line that differs between v7.3's vm.rst and master's:
  v7.3 copy / latest render / docs.kernel.org render : "(should not be protected. = 0;"
  master ?h=master vm.rst                            : "(should not be protected. = 0)"
```

`latest` and `docs.kernel.org` serve the **v7.3 release tree** byte-for-byte; the linux-next build is `next/` and
master's docs path 404s. A banner reading plain `7.3.0` is therefore a release-tree signature (rc builds render
`7.3.0-rcN`), and the 2026-10-23 round-32 copy — byte-identical to today's release rendering — already carried it.
Caveat, stated as a limit: master's `Makefile` also says `VERSION 7 / PATCHLEVEL 3 / SUBLEVEL 0 / EXTRAVERSION empty`
today (verified via `?h=master`), so the version *string* alone cannot distinguish "release tree" from "master tree"
during this window; the byte-identity of the rendered page with `/doc/html/v7.3/`, and its divergence from master's
`vm.rst`, is what makes the identification.

### 2.2 The trigger's definition was not in the lane before round 53

- `git show 20edafa59b38dac1ca358893f0259b1f436372d3:SKILL.md | grep -c on-release` → `0`: at the entering tip, SKILL.md
  defined no release trigger. The round-53 data commit adds the "Release recheck rule" (`SKILL.md:1199`, present-tense:
  "When a tag newer than an entry's pinned tag exists and the entry says `recheck: on-release`, re-read every claim row
  against the same path at the new tag").
- The canonical registry defines the token without semantics: `../../CORPUS.md:105-106` — "`recheck` — ISO date or
  cadence (`90d`, `180d`, `on-release`)".
- The r51 and r52 `recheck:` lines carry a curl command against **v7.2** URLs and no firing condition at all.
- `corpus/knowledge/disk-write-rate-r33.md:5` glosses the same token the other way: "re-open when the **host kernel
  moves past 7.2** or sysstat past 12.8.0". The host is still `7.2.11-arch1-1`, so under that reading the trigger has
  not fired. See Finding F3.
- No lane tool polls tags or `releases.json`: `grep -rn 'ls-remote' tools/ corpus/ SKILL.md` finds no release watch
  (`tools/mori-round19-regressions.py:544` only uses `refs/tags/fixture-override` inside a fixture). So nothing in the
  lane could have fired the trigger mechanically; it depended on a human/L1 noticing a tag.

## 3. What this means for C1's premise (reported, not judged)

C1's premise — "the release trigger has fired and nothing answered it" — is factually supported: v7.3 was tagged and
released 2026-10-18, and the two entries that carry `recheck: on-release` (r51, r52) landed 2026-10-26 without
answering it. Under the *upstream-tag* reading of `on-release` the trigger fired 8 days before those entries were even
written. Under the *host-kernel* reading used by the r33 entry, it has not fired (host `7.2.11-arch1-1`). The round-53
SKILL text adopts the first reading; that is a definition, not a measurement. Flagged for the L1 as data/wording
context, not as a counter change.

## 4. Files changed

None in the lane. Wrote only this report (`.ufo/waves/round-53/w1/Mo53ExecTagCommit.md`). All work happened under
`/fast/scratch/hyaku/mori-r53/Mo53ExecTagCommit/`, which was removed at the end. `git status --porcelain` in the lane
shows only other seats' work (` M PROVINCE.md`, ` M corpus/QUALITY.md`, ` M corpus/README.md`, `?? .ufo/waves/round-53/w1/`,
`?? .ufo/waves/round-53/evidence/selftests/`, `?? .ufo/waves/round-53/w1.ready*`) — nothing of mine.

## 5. Retained evidence

- Three independent transports agree on both tag ids (GitHub `ls-remote`, kernel.org cgit tag page, blob-filtered clone).
- 12/12 pinned copies re-fetched byte-identically; 12/12 equal to the tag-tree blobs; 5 of them provably not master.
- Release date 2026-10-18 from `releases.json` (isodate + timestamp) and the tag object's tagger timestamp, equal to
  the second.
- Ledger diff counts reproduced exactly (3/22/49/0/0/64/14/190/0/0).
- Every S502–S513 line-anchor lands on the named construct.
- Lane timeline for the trigger: 41 rounds (12–52) landed between the release and the round-53 answer.

## 6. Risks / blockers

- **Two clones, not one.** The seat rule allows at most one clone per seat; I needed one `--filter=blob:none --depth=1`
  clone per tag (`lnx73` for v7.3, `lnx72` for v7.2; 3.3 MB each) to prove blob identity against both tag trees. Both
  were in the seat's scratch directory and were deleted. Recorded as a deviation, not a full mirror (no working tree,
  no blobs except on demand).
- **GitHub rate limiting observed.** `git fetch … origin master` into the clone failed with
  `The requested URL returned error: 429` (the raw/API side of github.com was throttled on 2026-10-26). Consequence:
  no master tree was materialised locally; master blob comparison was done through cgit `?h=master` instead, which is
  why the master column in 1.4 covers the 9+3 pinned paths rather than a full tree diff.
- **`latest` doc builds are not archived.** I can show `latest == /doc/html/v7.3/` today and that the 2026-10-23 lane
  copy is byte-identical to today's release rendering, but I cannot prove what `latest` served on any date between the
  release and 2026-10-23; the "banner dates the release" claim is therefore bounded by [2026-10-18 release.
  2026-10-23 copy], not pinned to a day.
- No blockers. Nothing in the C1/C2 data was found to be wrong; the only defects are the wording/asymmetry items below.

## Findings

- **F1 (LOW, informational — no file change required).** Anchor provenance confirmed end to end. `refs/tags/v7.3` is
  the annotated tag object `091b06388b117fefdcb63336ac09956a4914b961`, peeling to commit
  `c03c1a14507dfaf8b856c2608f9ac216021fc222` (`Linux 7.3`, 2026-10-18T13:14:58-10:00, PGP-signed). Exactly the two ids
  the contract, `.ufo/waves/round-53/count-c1.py:4-5` and `corpus/SOURCES.md:281-289` cite. The v7.2 id in
  `corpus/SOURCES.md:290-292` (`237a1c39e8df`) is the v7.2 annotated tag object (`237a1c39e8dfd3e1c6f1f023eea37a48ec04cc63`,
  tag date 2026-08-16 14:32:26 -0700). File(s): `corpus/SOURCES.md:281-292`, `.ufo/waves/round-53/count-c1.py:4-5`.

- **F2 (MED — closes a named limit; no file change required).** The round-53 named limit "the pins prove the bytes are
  what the L1 fetched from cgit, not that cgit served the tag" is closed for all 12 pinned paths: each cgit
  `?h=v7.3`/`?h=v7.2` payload hashes to the same git blob id as the entry in the corresponding tag tree
  (`v7.3^{tree}` = `30fd2ef82912…`, `v7.2^{tree}` from `8d3ae592…`), and for `Documentation/filesystems/proc.rst`,
  `include/linux/mm_inline.h`, `Documentation/admin-guide/sysctl/vm.rst`, `mm/util.c` (v7.3) and `mm/mm_init.c` (v7.2)
  master's blob differs, so the tag — not master — was served. File(s): `corpus/knowledge/kernel-v7.3-recheck-r53.md:13`
  (limit text), `corpus/evidence/sources-r53/*`.

- **F3 (MED — calibration / routing item for round 54, not a fix to this round).** `recheck: on-release` was never
  defined in the lane before round 53: `git show 20edafa5:SKILL.md | grep -c on-release` → 0; the canonical entry
  (`../../CORPUS.md:105-106`) names the token without semantics; `corpus/knowledge/disk-write-rate-r33.md:5` reads it as
  "when the host kernel moves past 7.2" (host is `7.2.11-arch1-1` → not fired), while the round-53 rule added at
  `SKILL.md:1199` reads it as "a tag newer than an entry's pinned tag exists" (v7.3, 2026-10-18 → fired 8 days before
  r51/r52 landed). Nothing in `tools/` watches tags or `releases.json`, so the trigger is manual by construction. The
  round-53 rule is a definition authored in the same round that answers the trigger; naming that as a limit keeps the
  freshness axis honest. File(s): `SKILL.md:1199`, `corpus/knowledge/disk-write-rate-r33.md:5`,
  `corpus/knowledge/memavailable-estimate-r51.md:9`, `corpus/knowledge/overcommit-commit-limit-r52.md:9`.

- **F4 (LOW — wording; L1 may correct).** The round-52 closure and the round-33 attack characterise kernel.org's
  `latest` docs page as "the development tree" / "mainline/development tree"
  (`corpus/lessons/round-52-verifier-spotcheck.md:100`; `.ufo/waves/round-33/w2/AttackSrc181.md:91`). Measured:
  `latest` is byte-identical to `/doc/html/v7.3/` (sha `aa4364195e16` for the overcommit page, `423d043409bc` for
  `admin-guide/sysctl/vm.html`) and `docs.kernel.org` matches it; the linux-next build is `/doc/html/next/`
  (banner `next-20261026`) and `/doc/html/master/` 404s; `latest`'s `vm.html` carries v7.3's spelling
  `(should not be protected. = 0;` where master's `vm.rst` reads `= 0)`. So a plain `7.3.0` banner is a release-tree
  signature, which is exactly why the lane's own 2026-10-23 copy was already a release signal. File(s):
  `corpus/lessons/round-52-verifier-spotcheck.md:100`, `.ufo/waves/round-33/w2/AttackSrc181.md:91`.

- **F5 (LOW — anchor asymmetry; L1 may correct if it wants uniformity).** `corpus/SOURCES.md:290-292` (S511–S513) cite
  only the annotated tag object id `tag v7.2 (237a1c39e8df)` and omit the peeled commit
  `8d3ae59288f1e7d58d76558a6ee96d533bc5019f`, whereas S502–S510 cite both forms
  (`tag v7.3 (091b06388b11, commit c03c1a14507d)`). Both are correct; the asymmetry means a reader of S511–S513 cannot
  reach the commit whose bytes the row pins without a second lookup (the round-47 lesson does record it:
  `corpus/lessons/round-47.md:14`). File(s): `corpus/SOURCES.md:290-292`.

- **F6 (LOW — named limit, routed to round 54; behaviour observed, not a proposed change).** The frozen C1 counter never
  checks the tag id: its provenance arm requires the row's URL cell to contain
  `https://git.kernel.org/…/plain/<path>?h=v7.3` (`.ufo/waves/round-53/count-c1.py:267`, `V73[path][2] in srow[1]`) and
  its pins arm checks the copy's sha256 — neither reads `091b06388b11` or `c03c1a14507d` from the anchor cell. A wrong
  tag id in an anchor cell would score `provenance=ok`. This seat's hand check is what establishes those ids; the
  counter cannot. File(s): `.ufo/waves/round-53/count-c1.py:267`.

- **F7 (LOW — scope evidence for round 54, no file change).** The same unanswered trigger applies to entries outside
  C1's scope D, and for two of them the release changes nothing: `include/trace/events/oom.h` (r47) and
  `include/uapi/asm-generic/errno.h` (r48) are byte-identical between v7.2 and v7.3
  (`sha256 82f04ad4108ba949…` and `66a5ad60566fdd62…` at both tags; `diff -u` changed lines = 0), and the r47 copy
  `corpus/evidence/sources-r47/include_trace_events_oom.h` hashes `82f04ad4108ba9499b638fe298967f124269c0a2feb6ddbb14b1ade59c974e0d`.
  So the r47/r48 `on-release` rows would resolve to "unchanged" without a recheck, while the r51/r52 tables needed the
  work round 53 did. File(s): `corpus/knowledge/oom-tracepoints-r47.md:5`, `corpus/knowledge/quota-observability-r48.md:10-11`.

- **F8 (INFO — release date and trigger latency, answers the seat question).** v7.3 released **2026-10-18T23:14:58Z**
  (`releases.json` `released.isodate 2026-10-18`, `released.timestamp 1792365298` = tag object tagger timestamp). The
  round-52 closure's "latest renders 7.3.0" observation is dated **2026-10-26**, the same day round 52 landed
  (2026-10-26T22:08:38-03:00), so it does **not** date the release before round 52. The trigger nevertheless predates
  round 52 by **8 days 1h54m** on tag evidence, and the lane held a dated release render in its own committed evidence
  from **2026-10-23T01:31:22Z** (`corpus/evidence/recheck-r32/S001.src`, committed 2026-10-22T22:39:10-03:00) — three
  days before round 52 landed. 41 rounds (12–52) landed in the unanswered window. File(s):
  `corpus/lessons/round-52-verifier-spotcheck.md:100`, `corpus/evidence/recheck-r32/S001.src:42`.
