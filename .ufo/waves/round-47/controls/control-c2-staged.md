
# The OOM lifecycle an observer can hook is three named tracepoints

source: S507 — https://doi.org/10.1109/TSC.2026.3698682 — §design (eBPF/LSM paragraph) and §evaluation — the publisher's deposited VOR PDF, IEEE Trans. Services Computing, vol. 19, no. 4, pp. 3015–3028, August 2026, licence CC BY 4.0
verified-at: 2026-10-23
recheck: 180d — `pdftotext -enc UTF-8 roma.pdf - | grep -c 'mark_victim'` -> 3 (ran 2026-10-23)
coverage-map: FR13
ground: frontier item **FR13** — "eBPF kill/OOM tracing (art F5) … Boundary: privilege and version matter; a resident tracer is outside the census, so retain this as knowledge/frontier only"

### Claim

**The OOM lifecycle an observer can hook has exactly three named tracepoints, and
the kernel's OOM victim selection has no container context at all.**

The paper hooks "OOM-related kernel tracepoints such as `mark_victim`,
`start_task_reaping`, and `finish_task_reaping` to record OOM-triggering process
metadata" (S507). That is the concrete form of what FR13 calls eBPF kill/OOM
tracing: **the kill is marked, the reaping is started, and the reaping is
finished** — three points at which an observer can attach a process's identity to
an OOM event.

The kernel-side limitation is stated in the same paper: cgroup-based memory
controls "rely solely on per-process memory usage, lacking awareness of container
context", and the OOM killer "employs heuristic scoring to select victim
processes, often failing to distinguish between core system daemons and normal
workloads" (S507). So a victim is chosen from a **per-process** score with no
notion of which workload it belongs to.

### Why the paper's remedy matters to this lane

The paper closes that gap with two LSM hooks — `lsm_oom_kill_check()`, which
"intercepts victim selection and excludes system-critical or cross-container
targets", and `lsm_oom_cleanup_container()`, which reclaims the IPC, tmpfs and
shared memory a killed container leaves behind. Both are "installed via standard
LSM points and require no kernel patching or reboot" (S507).

The measured cost is **6.94 % throughput overhead across eight workloads**; under
eight concurrent attackers, "benign throughput retention remains 92.6 % with
ROMA, compared with 82.4 %" for the baseline (S507). The gap the paper names —
a malicious container killing a co-located service and leaving unreclaimed shared
memory that accumulates into a denial of service — is the *same shape* as the
co-tenancy the lane measured on its own host (see
`host-oom-activity-r42.md`).

### Boundaries

- **FR13's boundary governs this entry.** A resident tracer is outside the
  census, so this is retained as **knowledge and frontier only**: the paper
  describes a mechanism mori does not install and must not propose. The lane
  reads; it does not trace.
- Privilege and version matter: the hooks are LSM points and the tracing is
  eBPF, and the paper states neither is kernel-patching-free to *deploy*.
- The evaluation is the authors' measurement on their workloads, not on this
  lane's host, and it was not reproduced here.
- It is about **containers sharing a kernel**. It says nothing about a host that
  runs one workload per cgroup.

### Probe shape

Nothing new is added to the census. What the entry changes is the **vocabulary**
an attribution may use: an OOM event that mori observes has a *mark*, a *reaping
start* and a *reaping end*, and the kernel's choice of victim is a per-process
score with no workload attribution attached. Any future attribution that claims
"this seat caused that OOM" is claiming something the kernel did not know.

### What it changes for mori

FR13 stops being a topic and becomes a set of named points in a lifecycle. That
lets the lane say precisely what it does *not* know: it knows the victim, and it
does not know the culprit.

---
