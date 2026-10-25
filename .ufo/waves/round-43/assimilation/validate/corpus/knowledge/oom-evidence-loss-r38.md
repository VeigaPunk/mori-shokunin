
# The OOM evidence chain has a lossy link below the journal

source: S232 — https://gihyo.jp/article/2026/03/linux_containers-0061 — §「メモリコントローラの状態通知」 — 公開日 2026-03-10 (加藤泰文)
source: S233 — https://gihyo.jp/article/2024/08/linux_containers-0056 — §「メモリ使用の制限値」 — 公開日 2024-08-16 (加藤泰文)
source: S234 — https://raw.githubusercontent.com/openeuler-mirror/iSulad/5a79e5e2f46296d8d994f38fa32b429774f33b61/src/daemon/modules/container/supervisor/supervisor.c — fn container_supervisor_add_exit_monitor() — commit 5a79e5e2f46296d8d994f38fa32b429774f33b61
source: S235 — https://www.openeuler.org/whitepaper/openEuler%2024.03%20LTS%20%E6%8A%80%E6%9C%AF%E7%99%BD%E7%9A%AE%E4%B9%A6.pdf — p.27 §「约束限制」项 iSulad 小节 — 24.03 LTS, PDF sha256 9855a4986a312dfc946b1b97b6010a8e4f1e65a4a30dca99359e6df057ad8020
source: S241 — https://learn.microsoft.com/ja-jp/troubleshoot/azure/virtual-machines/linux/oom-swap-file-linux-vm — §「診断」 — updated_at 2026-10-14, KB 4010058 (ms.translationtype: MT)
verified-at: 2026-10-24
recheck: 180d — `curl -fsSL 'https://raw.githubusercontent.com/openeuler-mirror/iSulad/5a79e5e2f46296d8d994f38fa32b429774f33b61/src/daemon/modules/container/supervisor/supervisor.c' | grep -c 'epoll_loop_add_handler'` -> 2 (ran 2026-10-24)
recheck: 180d — `curl -fsSL 'https://www.openeuler.org/whitepaper/openEuler%2024.03%20LTS%20%E6%8A%80%E6%9C%AF%E7%99%BD%E7%9A%AE%E4%B9%A6.pdf' -o recheck.pdf && pdftotext -enc UTF-8 recheck.pdf - | grep -c '无法成功捕捉容器'` -> 1 (ran 2026-10-24)
recheck: 180d — `curl -fsSL 'https://gihyo.jp/article/2026/03/linux_containers-0061' | grep -c POLLPRI` -> 4 (ran 2026-10-24)
coverage-map: FR1
ground: frontier item **FR1** — "event-time kernel summary/victim token validation and fleet correlation remain frontier"

### Claim

The absence of an OOM record is not evidence that no OOM occurred. Three
independent loss mechanisms sit **below** the kernel journal, and each has its own
source.

**1 — Path-bound delivery.** A container runtime receives a cgroup OOM
notification through an eventfd registered in its epoll loop, and that registration
is bound to the container's cgroup path, resolved once at setup time (S234). A
cgroup OOM *also* deletes that path. The consequence is stated plainly in the
openEuler 24.03 LTS whitepaper: if the runtime handles the OOM event after the
cgroup path has been deleted, the event cannot be captured and the reported
`reason` field may be wrong (S235). The same source records that the `reason`
field gained an `OOMKilled` value precisely so a user could tell whether a
container was killed for memory (S235).

**2 — No record at all.** `memory.high` imposes reclaim pressure and **never**
invokes the OOM killer (S233), so a cgroup can sit above its limit with no OOM
record of any kind. `memory.max` is the absolute limit that does call it.

**3 — No retrospective diagnosis.** A vendor's own operational guidance states
that memory diagnosis must be performed at the moment of detection because it
usually cannot be done afterwards (S241).

### What survives the loss

What survives independently of the runtime's attribution is the cgroup's **own**
`memory.events` counter. The English upstream documentation the lane already holds
states the semantics (registry row S002) — `memory.events` counts a cgroup **and
its descendants**, `memory.events.local` counts only the cgroup's own events — so
the pair of counters, read together, distinguishes an OOM in the watched cgroup
from an OOM in a descendant, and that distinction is checkable rather than
assumed. The Japanese account of the same files adds the part the lane did not
have: the counters notify on change through inotify `IN_MODIFY` or poll
`POLLPRI` (S232), which is a resident watcher rather than a one-shot census.

### Boundaries

- The claim is about the **runtime layer**, not the kernel: the host's own kernel
  journal records are a different evidence path, governed by
  `kernel-oom-line-attribution-r12.md`. This entry does **not** claim the kernel
  lost a record.
- It is scoped to runtimes that deliver OOM through a **path-bound** eventfd.
  S234 is one such runtime; the entry must not be generalised to all runtimes.
- The Chinese-language sources are **one vendor's** (openEuler / iSulad) —
  authoritative for that product, illustrative of the mechanism.
- S232 and S233 are **tier-B** Japanese secondary accounts; the upstream kernel
  documentation the lane already holds remains primary for the counter semantics.
- S241 is a **machine-translated** localisation (the page declares
  `ms.translationtype: MT`), so it is tier B.
- Nothing here licenses a remediation; nothing here changes a quota, a limit or a
  cgroup setting.

### Probe shape

A probe that wants to survive this loss must not read only the runtime's reason
field. It would read, for the cgroup it watches, the **cgroup's own
`memory.events` and `memory.events.local` counters**, and report a *pair*
(`memory.events` delta, `memory.events.local` delta) rather than a single
"was there an OOM" bit — because the pair distinguishes "OOM in this cgroup" from
"OOM in a descendant".

Where the pair is available, the **notification** path (inotify `IN_MODIFY` /
poll `POLLPRI`, per S232) is the resident alternative to a one-shot census. It is
a resident watcher, not a census probe: the lane's one-shot census cannot be
retrofitted with it, and a watcher started after the event has already missed it.

### What it changes for mori

`kernel-oom-line-attribution-r12.md` §[UNKNOWN] already asks: *"Whether every
kernel OOM victim produces both retained records, and whether records were lost
outside the retained journal, remain unknown."* This entry narrows that question
to a **specific, named, independently sourced loss mechanism** and gives it a
probe shape. It does **not** close it: the runtime-layer loss is not the
journal-layer loss, and the lane's own UNKNOWN stays open.

### Delivery paths this cannot see

A runtime that does not deliver OOM through a path-bound eventfd; a host whose
kernel journal retains the record regardless; any OOM that did not occur in a
cgroup at all.

---

---

### Round-42 adoption provenance

Admitted from the shokuknow `merge/mori/` package (campaign
`corpus-expansion-1`) in round 42 on the OOM-evidence-chain theme.
Every cited source was re-opened and re-fetched by the lane on
2026-10-24: S232 (html copy, POLLPRI count 4), S233 (html copy,
memory.high worked example and dmesg OOM record located), S234 (source
copy, `epoll_loop_add_handler` under `ENABLE_OOM_MONITOR` located), S235
(PDF sha256 byte-identical to the whitepaper pin, 无法成功捕捉容器
located), S241 (html copy, 診断 section and `ms.translationtype: MT`
located). Copies under `corpus/evidence/sources-r42/`; Gate quotes in
`corpus/lessons/round-42.md`.
