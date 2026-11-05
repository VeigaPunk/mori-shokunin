# mori round 98 — frozen claim contract (L1 MoriR98, attempt 1)

Entering revision: `b2a67ce562bbf2f0cc73f47d8e79f792badf5e63` (master = origin/master; `git status` shows only the two
r97 late-seat files routed as r97 closure D1). The r97 closure admitted the lane (operability, freshness improved);
the last three rejected closures before it (r94, r95, r96) failed on predicates a do-nothing control already met
and on a freshness predicate the vendor stamp could never meet. This contract therefore binds, before any wave
output: (1) do-nothing controls that FAIL at entering, (2) forgery controls through the public tool path so a
false green is rejected, (3) positive controls so blanket refusal is not a gain — executed and committed with this
freeze: `evidence/controls-r98.txt` (`CONTROLS_DONE unexpected=0`), produced by `controls-r98.sh <entering>`.

Frozen instrument bytes (recorded on the first line of `evidence/controls-r98.txt`): `count-c1.py`, `count-c2.py`,
and the incident capture `evidence/journal-incident-r98.txt` (sha256 pinned inside `count-c1.py`). Never edited
after this freeze; a defect found later is reported, not patched into the claim.

## C1 — coverage (score 6), capability acquisition: user-namespace runway and kernel-tunable write events

Surface moved: new resource-runway ground the lane did not hold (`grep -i namespace PROVINCE.md` → no line at
entering; no tool reads `/proc/sys/user/max_user_namespaces`). Motivating event: host incident 2026-11-05 (prompt
addendum): wave seats set `user.max_user_namespaces` to 0 via sudo (05:14:52, 05:22:02 -03; transient 10000/15638),
every bwrap sandbox then failed with ENOSPC until the orchestrator restored 122865. The capability: a read-only
`tools/mori-userns-runway.py` that (i) reads the limit and the user namespaces visible on readable process links and
states runway and an ok/low/exhausted state (limit 0 = exhausted), and (ii) scans sudo-logged journal commands for
kernel-tunable writes, counting writes that set the user-namespace limit to 0. Candidate bytes:
`.ufo/waves/round-98/candidate/tools/mori-userns-runway.py` (plus registry row and PROVINCE note drafts).
AXES.md coverage: "Fraction of the domain's real surfaces the skill governs (repo paths, tools, edge classes)".

Predicate P1 (same sentence as `count-c1.py` docstring): on the tree DIR of revision R, (a)
`tools/mori-userns-runway.py --selftest` exits 0 and its last line matches `MORI_USERNS_RUNWAY_SELFTEST: PASS (<n>
cases)`; (b) the tool answers every case of this counter's frozen fixture battery (9 runway cases built here, 6
journal cases including the committed incident capture) with the frozen exit code and summary fields; (c) a live
run on /proc exits 0 or 1 and reports the limit this counter reads itself from /proc/sys/user/max_user_namespaces;
(d) the lane's gate auditor `tools/mori-gate-registry.py --rev WORK --repo DIR --audit-all` prints `REGISTRY=met`;
(e) `corpus/knowledge/userns-runway-r98.md` cites in a `source:` line at least one S-id whose `corpus/SOURCES.md`
row is `mined`, opened 2026-11-05 or later, and lists that knowledge path in `used-by`; (f) one PROVINCE.md line
names both `user namespace` and `tools/mori-userns-runway.py`.

Counter: `git -C <lane> archive R | tar -x -C DIR` then `python3 .ufo/waves/round-98/count-c1.py --root DIR
[--work SCRATCH]`. Label `C1=met` / `C1=unmet`.
Before (do-nothing, entering): `C1=unmet cases_ok=0/15 selftest=absent live=absent registry=met sourced=unmet
province=unmet` exit 1 (`evidence/before-c1.txt`).
Target (after, landing): `C1=met cases_ok=15/15 selftest=ok live=ok(...) registry=met sourced=met(S...)
province=met checks_failed=-` exit 0.
Kill rule: any other output at the landing revision is unmet; no re-declaration, no counter edit.
Controls (committed, pre-freeze, through the tool's public CLI): constant printer (K1), pid-not-namespace counting
(K2), fail-open missing limit (K3), reads counted as writes (K4), non-sudo decoy lines accepted (K5), no registry
row (K6), no knowledge entry (K7), row not mined (K8), no PROVINCE line (K9), limit 0 read as ok (K10), raw
journal line echoed (K11) → all `unmet`; the full candidate tree with a stub source row (P1) → `met`.

Sourced: C1 rests on SOURCES rows opened this round (kernel `Documentation/admin-guide/sysctl/user.rst` for the
limit semantics; unshare(2)/clone(2) for the ENOSPC signature; `include/linux/proc_ns.h` for the initial
user-namespace inode) — the lesson `## Gate` carries URL, access date and located quote for each.

## C2 — calibration (score 5, lowest non-retired tier): SCORECARD Last-change cells match the admitted record

Surface moved: SCORECARD.md `## Axes` Last-change cells — the lane's self-assessment of when each axis last moved.
Entering state: the r97 closure (MANIFEST rounds[1384], admitted) graded operability and freshness improved, but the
cells still lead with round 93 (operability) and round 82 (freshness). AXES.md calibration: "SHONEN.md/SCORECARD
entries match observed repo state"; §9: a calibration claim counts mismatches between self-assessment and
observed state.

Predicate P2 (same sentence as `count-c2.py` docstring): at revision R, the lane's registered calibration gate
`tools/mori-scorecard-calibration.py`, taken from R with sha256 equal to its entering bytes, run as `<tool> R --repo
LANE --manifest MANIFEST`, exits 0 and prints `C1=met axes=6 mismatches=0 columns_unchanged=yes` — every SCORECARD
`## Axes` Last-change cell leads with the highest admitted mori closure round that graded the axis improved/harmed,
with Score and Evidence cells unchanged.

Counter: `python3 .ufo/waves/round-98/count-c2.py R`. Label `C2=met` / `C2=unmet`.
Before (do-nothing, entering): `C2=unmet mismatches=2 columns_unchanged=yes tool=ok tool_rc=1
mismatched_axes=operability,freshness` exit 1 (`evidence/before-c2.txt`).
Target (after, landing): `C2=met mismatches=0 columns_unchanged=yes tool=ok tool_rc=0 mismatched_axes=-` exit 0.
Kill rule: any other output at the landing revision is unmet.
Controls (committed, pre-freeze, scratch-clone fixture commits): one cell fixed (K1c), wrong verdict word (K2c),
Score cell edited (K3c), tool bytes changed (K4c) → `unmet`; both cells fixed (P1c) → `met`.

## Causal separation

C1 touches `tools/`, `SKILL.md` (registry append), `PROVINCE.md`, `corpus/knowledge/`, `corpus/SOURCES.md`; C2 touches
only two SCORECARD `## Axes` Last-change cells. Neither counter reads the other's surface (C1's registry conjunct
reads SKILL.md tables, not SCORECARD; C2 reads SCORECARD and MANIFEST only).

## Not claimed (honest scope)

- No score move is claimed; scores stay until a closure states one.
- `used_lb` is a lower bound (namespaces held only by fds/bind mounts, or behind other users' unreadable links, are
  invisible); the tool says so and the claim does not count them.
- The 31 `prefix_only` digest rows, the r97 auditor residuals R1–R3 and the calibration-counter survivor M10 are
  carried, not claimed.
