# Mo53ConnSiblings — sibling-overlap scan (mori round 53, wave w1)

Seat scope: sibling overlap for C1 (v7.3 recheck ledger) and C2 (mori-commit-runway tool).
Lane: mori-shokunin. Scratch: `/fast/scratch/hyaku/mori-r53/Mo53ConnSiblings/` (created; only
empty `tmp/` inside, removed after run). No installs; no clones; disk-guard read 25% free on
/fast/scratch/hyaku (604.8G free) — no heavy run needed.

## Scan command (assignment text, run verbatim)

```
grep -rliE 'overcommit|CommitLimit|Committed_AS|percpu_counter|v7\.3|on-release' /home/vgpnk/Projects/shokunin/*-shokunin/corpus/knowledge /home/vgpnk/Projects/shokunin/*-shokunin/SKILL.md /home/vgpnk/Projects/shokunin/*-shokunin/PROVINCE.md /home/vgpnk/Projects/shokunin/*-shokunin/tools 2>/dev/null
```

Exit code 2 (grep's own convention: hits found, and some operand errors — a few globbed dirs are
absent; the emitted list was still complete for every existing operand). ~170 files hit. Raw term
counts per lane (same regex, `grep -rhoE` over the same four operands, `.scratch`/`.ufo/waves`
excluded by the operand set — `corpus/knowledge`, `SKILL.md`, `PROVINCE.md`, `tools` only):

| lane | overcommit | CommitLimit | Committed_AS | percpu_counter | v7.3 | on-release |
|---|---|---|---|---|---|---|
| mori | 181 | 49 | 46 | 18 | 49 | 24 |
| tsukuroi | 3 | 0 | 0 | 0 | 0 | 62 |
| kama | 0 | 0 | 0 | 0 | 0 | 41 |
| chousa | 0 | 0 | 0 | 0 | 0 | 25 |
| tabi | 0 | 0 | 0 | 0 | 0 | 17 |
| mado | 0 | 0 | 0 | 0 | 0 | 13 |
| kagi | 0 | 0 | 0 | 0 | 0 | 10 |
| souji | 0 | 0 | 0 | 0 | 0 | 4 |
| game-dev-2d | 0 | 0 | 0 | 0 | 0 | 3 |
| game-dev-3d | 0 | 0 | 0 | 0 | 0 | 2 |
| kaidoku | 0 | 0 | 0 | 0 | 0 | 20 |
| kasegi | 0 | 0 | 0 | 0 | 0 | 1 |
| kengaku | 0 | 0 | 0 | 0 | 0 | 3 |
| revenger | 0 | 0 | 0 | 0 | 0 | 3 |
| tameshi | 0 | 0 | 0 | 0 | 0 | 1 |
| all other *-shokunin lanes | 0 | 0 | 0 | 0 | 0 | 0 |

Reading: the commit-ledger subject matter (`overcommit`, `CommitLimit`, `Committed_AS`,
`percpu_counter`, `v7.3`) lives **only** in mori, plus three `overcommit` hits in tsukuroi.
`on-release` is a fleet-shared recheck cadence tag (present in 15 lanes' entries); per-lane it
gates each lane's own upstream (tabi: Chromium tags; kama: llama.cpp builds and tool revisions;
mado: hyprctl/hyprlang; game-dev-3d: Godot releases; souji: host git upgrades; kagi: vendor pages;
game-dev-2d/kengaku/tameshi: own-tool revisions). It is not, by itself, subject-matter overlap.

## Hit-by-lane assessment

### tsukuroi-shokunin (3 `overcommit` hits) — adjacent, no duplication, two live notes

- `corpus/knowledge/kill-event-deep-r8.md:262` and `corpus/knowledge/oom-event-plane.md:351`:
  pin `overcommit_memory=0` (with `panic_on_oom=0`, `oom_dump_tasks=1`, `swappiness=60`) as a
  host diagnostic setting for OOM-event analysis. Mori's `tools/mori-commit-runway.py` reads the
  **same five-plus files** (`/proc/sys/vm/overcommit_memory`, `overcommit_ratio`,
  `overcommit_kbytes`, `admin_reserve_kbytes`, `user_reserve_kbytes`) for a runway verdict.
  Different questions: tsukuroi records the setting to argue whether a missing kill record is a
  dump artifact; mori computes commit headroom. **Complementary, not duplicated.** Live check:
  `cat /proc/sys/vm/overcommit_memory /proc/sys/vm/overcommit_ratio` → `0`, `50`; `uname -r` →
  `7.2.11-arch1-1` — mori's live mode-0 reading is consistent with tsukuroi's pinned `=0`. If the
  host mode ever flips to 2, tsukuroi's pinned rows go stale *and* mori's tool becomes the only
  reader of the mode-dependent band: worth a named boundary line, not a conflict.
- `corpus/knowledge/btrfs-space-r30.md:18`: btrfs metadata-reservation "overcommit" — a different
  concept; no relation.
- Boundary text: `overcommit-commit-limit-r52.md:65` already cites `../tsukuroi-shokunin/
  PROVINCE.md:28,30-31` and declares "OS-state triage is tsukuroi's ground"; `commit-runway-read-
  r53.md:56` repeats it ("Choosing an overcommit mode… is the operator's; OS-state triage is
  tsukuroi's"). Tsukuroi PROVINCE line 49 (ADJ-04) routes fleet/wave attribution to mori. The
  contract's contested-scope question is already answered by both lanes' own text: runway reading
  (detection/report) is mori's; remediation triage is tsukuroi's/operator's. **No contested claim.**
- Kernel-pinned rows: `tsukuroi/corpus/SOURCES.md` carries **22 rows pinned to
  `torvalds/linux/v7.2`, all 22 with cadence `on-release`** (S115–S119, S132–S145, S148–S149,
  S156–S158, S182, S185, S201, S205: psi.rst, psi.c, psi.h, cgroup-v2.rst, oom_kill.c,
  btrfs volumes.c/sysfs.c/block-rsv.c/ioctl.c, tainted-kernels.rst, panic.c/h, module
  main.c/signing.c/module-signing.rst, proc.rst, errno-base.h). Each is scoped "for the host
  kernel 7.2.11" (still true: host runs 7.2.11). Their recheck procedures name "the host's kernel
  tag" (e.g. `mount-errno-contract-r37.md:5`) — i.e. package-bound, not upstream-tag-bound — so
  the v7.3 tag does not, by tsukuroi's own wording, fire them. But tsukuroi's S148 pins
  `proc.rst` lines 1965–2002, the **same file mori just diffed at v7.3** (see below).

### kama-shokunin — generic release-recheck mechanism, own-upstream scope

- `tools/release-recheck.py`, `tools/round44-release-recheck-audit.py`, `tools/round46-release-
  recheck-audit.py` (+ .pyc noise): draft/audit a release re-verification ledger over *kama's own*
  SOURCES rows whose source cell is a GitHub URL pinned to a 40-hex commit and cadence
  `on-release`. Same *shape* as mori's C1 ledger (per-row holds/drifted/removed + two-vote
  analog), different substrate (GitHub blobs for llama.cpp; mori pins kernel.org cgit tags, which
  kama's `url_re` cannot match — its population regex requires `github.com|raw.githubusercontent
  .com/<owner>/<repo>`).
- `corpus/knowledge/engine-pin-watch.md:14`: records S020's `on-release` for SGLang — own lane.
- **kama itself carries 2 `on-release` rows pinned to torvalds/linux v7.2** (S048 tcp_ipv6.c,
  S049 proc_net_tcp.rst) with cadence `on-release` keyed to kernel/Python changes in
  `loopback-listener-ownership.md:3` — package-bound again. Kama's lane is local model serving
  memory (llama.cpp); it does **not** read the host commit ledger — zero CommitLimit/Committed_AS
  hits anywhere. Mori's runway tool does not enter kama's serving-memory ground; the contested-
  scope check (kama = local model serving memory) finds no collision: the tool reads host
  `/proc/meminfo`, not service state, and mori PROVINCE:67 already declares "mori does not infer
  serving health from host/resource signals".

### tabi-shokunin — the closest precedent for the C1 mechanism, own-upstream scope

- `corpus/knowledge/chromium-156-release-pin-recheck.md`: a completed release-pin recheck —
  23 `on-release` rows re-opened at a newer Chromium Stable tag by frozen counter
  `scripts/check-release-pins.mjs` (verdicts holds/drifted, superseding rows at the new pin).
  Same claim shape as C1 (pinned-tag claims re-verified at the new tag, computed verdicts,
  ledger note). Scope: Chromium Gitiles pins only. **A sibling already runs a release-pin
  recheck mechanism — but for Chromium, not kernel; C1 is mori's first kernel-pin recheck,
  not a duplicate of tabi's.**
- `source-recheck-round-25.md`: six on-release rows re-opened (Chromium tags).

### chousa-shokunin — cadence machinery, not claims

- `recheck-due-r26.md` + `tools/research-gate.sh`: computes whether an entry's declared cadence
  is *due*; its own table says `on-release` = "event; no inferred calendar deadline… `event`
  does not certify that releases were monitored." Policy/meta machinery about the tag itself —
  no kernel-pinned claims; no contradiction with the C1 ledger.

### All other lanes — cadence tag only

game-dev-2d/3d (own-fixture reruns, Godot releases), kagi (vendor feature pages), kaidoku
(registry immutability/checkers), kasegi (cadence fired same-day), kengaku (own plans tooling),
mado (hyprctl/hyprlang pins), revenger (own-work entry), souji (host git upgrades), tameshi
(mutants tooling): every hit is the shared `on-release` convention over each lane's own
subject. No overlap with C1's kernel pins or C2's commit ledger.

## Does any sibling already run a release-recheck of kernel-pinned claims?

**No.** Kernel-pinned `on-release` rows exist in three lanes — mori (73 rows: `grep
'torvalds/linux' mori/corpus/SOURCES.md | grep -c on-release | …v7.2` → 73 v7.2 + 9 v7.3
rows), tsukuroi (22), kama (2) — but:

- mori's C1 ledger is the **first upstream-tag recheck any lane has run on kernel pins**. It
  covers only mori's own scope D (the two claim tables: 46 of 49 rows; contract's named limit:
  "D covers two entries' tables only"). Mori's own SOURCES.md still holds ~27 other v7.2
  `on-release` rows (S003 oom_kill.c, S082/S148-analog proc.rst mountinfo, S090–S095 psi
  set, S127, S143–S148) whose trigger is likewise not yet re-exercised at v7.3 — the contract
  named this residual explicitly, so it is a scoped limit, not a defect.
- tsukuroi's and kama's kernel-pin rechecks are host-package-bound ("the host's kernel tag");
  host is still 7.2.11, so they are dormant. No sibling tool or ledger re-verifies kernel
  upstream-tag claims.
- Reusable asset already on disk: mori's committed v7.3 copies under
  `corpus/evidence/sources-r53/` cover proc.rst — the same file tsukuroi's S148 pins at v7.2
  (lines 1965–2002). I diffed mori's own v7.2/v7.3 copies
  (`diff corpus/evidence/sources-r51/proc.rst.v7.2 corpus/evidence/sources-r53/proc.rst.v7.3`):
  **2 hunks, +1 line total** — typo fix at line 516 ("page page"→"page") and one inserted
  `ur` table row after line 610, both *before* tsukuroi's cited 1965–2002 range and outside
  the meminfo definitions. The mountinfo section text is unchanged; anchor lines would shift
  by +1. That is a free holds-verdict for tsukuroi's S148 whenever that row's recheck fires —
  but it is tsukuroi's recheck to run, not mori's; and tsukuroi's evidence rules may want its
  own fetched copy rather than mori's.

## Duplication / contradiction verdict

- **C2 tool (`mori-commit-runway.py`):** no sibling duplicates it (only mori reads
  CommitLimit/Committed_AS/percpu_counter anywhere under `tools/`, `corpus/knowledge`,
  `SKILL.md`, `PROVINCE.md` fleet-wide). No contradiction with tsukuroi's pinned
  `overcommit_memory=0` — live value is still 0, and the uses differ. Boundary text on both
  sides agrees (detection/report = mori; triage/remediation = tsukuroi/operator; serving
  memory = kama).
- **C1 ledger:** no sibling duplicates it; tabi (Gitiles) and kama (GitHub-commit) have
  convergent mechanisms on their own upstreams — three independent implementations of the
  same "release-pin recheck" pattern now exist (tabi round-29 counter, kama release-recheck
  draft/audit, mori C1 ledger+RECHECK seats). That is a compatible-synthesis observation for
  round 54 (a shared substrate for "rows pinned to an upstream tag, re-verified at the next
  tag"), not a contradiction. No fleet-wide claim anywhere asserts kernel-pin freshness — the
  C1 ledger's mori-scope claim is accurate.

## Findings

- **MED** — `tsukuroi-shokunin/corpus/SOURCES.md` rows S115–S205 (22 rows) and
  `kama-shokunin/corpus/SOURCES.md` S048–S049 pin `torvalds/linux` at tag `v7.2` with cadence
  `on-release`. If "release" for those rows is read as *upstream tag* rather than *host kernel
  package*, all 24 went due when v7.3 was tagged 2026-10-26. Their own procedures say "the
  host's kernel tag" (host still 7.2.11), so the defensible reading keeps them dormant — but
  the trigger ambiguity is a sibling-side freshness risk mori's v7.3 sweep surfaced. Routed
  item for round 54: state the sibling observation in the round report; recheck execution is
  each sibling's.
- **MED** — `mori-shokunin/corpus/SOURCES.md`: ~27 v7.2 `on-release` rows sit *outside* C1's
  scope D (S003, S082, S090–S095, S127, S143–S148, …). Contract named limit "D covers two
  entries' tables only" acknowledges this; recording it as a named limit of the claim (not a
  defect) for the report, and noting S148-proc.rst's v7.3 delta is provably benign (+1 line
  at 610, mountinfo text unchanged) if a future round wants to amortize a fleet-side proc.rst
  recheck on mori's already-committed v7.3 copy.
- **LOW** — Three lanes now implement the same release-pin recheck shape independently
  (tabi `scripts/check-release-pins.mjs` on Gitiles; kama `tools/release-recheck.py` +
  round44/46 audits on GitHub-commit pins; mori C1 ledger + RECHECK seats on kernel.org cgit
  pins). No contradiction; a round-54 synthesis candidate (shared verifier substrate) — the
  substrate differences are URL-shape and vote mechanics, not claim semantics.
- **LOW** — `mori-commit-runway.py` reads `/proc/sys/vm/overcommit_*` for live verdicts while
  tsukuroi's `kill-event-deep-r8.md`/`oom-event-plane.md` pin the same knob as a diagnostic
  snapshot. Complementary today (host mode 0, matching both); the first shared sysctl file
  read by both lanes' evidence is `overcommit_memory` — a boundary note in the round report
  would pre-empt a future "who owns the commit ledger" question. `overcommit-commit-limit-
  r52.md:65` and `commit-runway-read-r53.md:56` already disclaim sysctl ownership.
- **LOW** — Scan exit code 2: a few `*-shokunin/corpus/knowledge` operands do not exist
  (e.g. lanes without that dir); the emitted file list is complete for all existing operands
  (verified by the per-lane recount above). No hits were lost to the error.
