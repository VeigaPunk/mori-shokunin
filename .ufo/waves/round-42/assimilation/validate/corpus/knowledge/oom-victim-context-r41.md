source: S262 — https://doi.org/10.1109/TSC.2026.3698682 — Abstract, as carried by the publisher-deposited OpenAlex record — IEEE Transactions on Services Computing, vol. 19, no. 4, pp. 3015–3028, 2026
# The kernel's OOM victim selection has no container context

source: S262 — https://doi.org/10.1109/TSC.2026.3698682 — Abstract and TLDR, as recorded by the publisher's Semantic Scholar record and by OpenAlex — IEEE Transactions on Services Computing, vol. 19, no. 4, pp. 3015–3028, 2026
verified-at: 2026-10-24
recheck: 180d — `curl -fsSL 'https://api.openalex.org/works/https://doi.org/10.1109/TSC.2026.3698682' | grep -c 'lack sufficient container context'` -> 1 (ran 2026-10-24)
coverage-map: FR13, FR1
ground: frontier item **FR13** — "eBPF kill/OOM tracing" · frontier item **FR1** — "event-time kernel summary/victim token validation and fleet correlation remain frontier"

### Claim

**The kernel's OOM victim selection is cgroup-scoped but not container-scoped,
and a peer-reviewed measurement says so.**

The paper's own study finding: 「Our study shows that Linux cgroups and the
default Out-of-Memory (OOM) mechanism lack sufficient container context when
selecting victim processes.」 (S262). On a shared kernel the consequence is that
one container's OOM can kill a **co-located** service, and can leave **shared
resources unreclaimed** — POSIX/SysV shared memory, message queues, semaphores
and tmpfs files — which accumulate over time into a denial of service.

The paper's proposed remedy is deliberately light: container awareness is added
to the OOM handling path by combining **eBPF-based monitoring with two
lightweight LSM hooks**, so that victim selection is confined to the offending
container and the leaked shared resources are proactively reclaimed after an OOM
event. The reported cost is **6.94 % throughput overhead across eight
workloads**, with recovery within **6.9 s** under up to eight concurrent
attackers, and stability over 24-hour runs with up to 64 containers (S262).

### Why this is the lane's business

FR1 is about *attributing* an OOM at event time, and the lane's held
`kernel-oom-line-attribution-r12.md` parses the kernel's OOM record to say which
process was killed. This paper says something that changes how that record
should be read: **the kernel's own choice of victim is not aware of the
container**, so on a shared kernel the victim's identity is not the container's
identity. A host observer who sees "process X was OOM-killed" cannot conclude
"container C caused it" — the kernel did not have the concept. Any fleet
correlation that attributes an OOM to a seat has to supply the container context
the kernel did not.

### Boundaries

- Only the **abstract-level claims** were retrieved. The full text is paywalled:
  `ieeexplore.ieee.org/document/11540439` returns HTTP 202 with a 0-byte body
  from this host (re-observed 2026-10-24; Semantic Scholar lacks the DOI; the
  OpenAlex record carries the deposited abstract, copy
  `corpus/evidence/sources-r42/S262.oa.json`), so the method, the measured overhead breakdown and the
  evaluation limits were not read. The scope of this entry is therefore the
  paper's own abstract and TLDR, as recorded by the publisher's metadata.
- It is a **peer-reviewed journal paper** (IEEE Trans. Services Computing), so
  the claim it makes about the kernel's behaviour is the authors' measured
  finding, not the lane's own observation. The lane has not reproduced it.
- The paper's *remedy* is out of scope: mori observes and reports; it does not
  install LSM hooks or eBPF programs.
- It is about **containers on a shared kernel**. It says nothing about a host
  running one workload per cgroup, and nothing about this lane's own fleet.

### Probe shape

An OOM attribution on a shared kernel must carry, in addition to the kernel's
own tokens, the **container context the kernel did not have**: which cgroup the
killed process belonged to, and which other cgroups were resident on the same
kernel at that moment. The first is a `cgroup` read at event time; the second
is the co-tenancy set. Without both, "the victim was process X" is the only
statement the evidence supports.

### What it changes for mori

FR13 gains a citable peer-reviewed anchor, and FR1 gains a constraint on its
own attribution: the kernel's OOM record names a **process**, and on a shared
kernel it cannot name the **container** that caused it. That is a boundary on
fleet correlation, stated by the literature rather than inferred.

### Delivery paths this cannot see

Single-workload hosts; cgroup-per-tenant deployments where the kernel's
cgroup-scoped selection already coincides with the container's; any observation
path that reads a runtime's own attribution rather than the kernel's.

---

---

### Round-42 adoption provenance

Admitted from the shokuknow `merge/mori/` package in round 42 on the
OOM-evidence-chain theme. The S262 abstract quote was re-located by the
lane on 2026-10-24 in the publisher-deposited OpenAlex record (abstract
inverted index); the full text remains paywalled from this host, so the
entry's abstract-only scope stands. Gate quote in
`corpus/lessons/round-42.md`.
