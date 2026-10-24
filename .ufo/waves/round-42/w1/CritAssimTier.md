# CritAssimTier — attack on round-42 tier calls (S262, S234, S235)

Contract text (`/home/vgpnk/Projects/shokunin/CORPUS.md:93-97`, cached copy
`corpus/evidence/sources-r36/S205.src:93-97`):

> `tier` — scoped to `scope`, never global. **A**: primary or authoritative for that scope
> (spec, official docs, source code, original paper, maintainer statement, the lane's own
> re-runnable gate output). **B**: strong secondary (expert write-up with reproducible
> detail, survey, textbook). **C**: lead only — never sole support for an admitted entry.

| row | landed tier | verdict | recommended tier |
|---|---|---|---|
| S262 (ROMA paper via OpenAlex) | A | **fails** | **B** |
| S234 (iSulad supervisor.c, openeuler-mirror) | A | holds | A |
| S235 (openEuler 24.03 LTS whitepaper) | A | holds | A |

## 1 — S262 should be B, not A

**Counterexample.** The row's scope reads "the paper's abstract-level claims as recorded
by the publisher's deposited metadata," but the opened source is not the paper and not the
publisher's deposit. The anchor cell itself records that `ieeexplore` returned HTTP 202
with 0 bytes from this host and Semantic Scholar lacks the DOI. The only bytes held
(`corpus/evidence/sources-r42/S262.oa.json`) are **OpenAlex's own work record** — a
third-party index database's re-encoding. The abstract is not served text: it is a
`abstract_inverted_index` position map (159 terms) that I reconstructed by position-sort;
the record carries no field stating IEEE deposited that abstract. "Publisher-deposited"
is an unverified provenance claim written into scope, anchor, the lesson Gate
(`corpus/lessons/round-42.md:45-46` "publisher-deposited OpenAlex record") and the adopted
entry header — false provenance, the exact class this lane exists to catch.

**Why A fails against the contract.** The tier-A enumeration is source-object typed:
"spec, official docs, source code, original paper, maintainer statement, the lane's own
re-runnable gate output." For a row of `kind: paper`, A means the original paper (or its
publisher record) was opened. An aggregator's abstract index is none of the six
enumerations; scoping the claim down to "abstract-level" does not promote the carrier —
otherwise any registry lookup becomes "primary" for its own contents. The in-registry
precedent cuts the same way: **S057** is `paper | C` with anchor "Abstract only
(CrossRef, Perspectives on Psychological Science, 2012-11); body not opened" — a
CrossRef-deposited abstract was tiered C (lead) precisely because the body was not opened
and the carrier was a metadata feed. S262 differs from S057 in two ways that lift it above
C — the abstract is fully quoted and located, and its claim is unique (not a duplicate of
an existing A row) — but nothing lifts it to A: the publisher's record was unreachable and
the held bytes are OpenAlex's. B ("strong secondary … with reproducible detail") is the
honest tier: an index database's reconstructible abstract of a peer-reviewed paper is a
strong secondary, not the primary.

**Why B (not C).** The contract restricts only C: "lead only — never sole support for an
admitted entry." B may be sole support, so `corpus/knowledge/oom-victim-context-r41.md`
survives the downgrade. C would also overstate the defect: the abstract was re-located and
quoted, unlike S057's unquoted lead.

## 2 — S234 stays A (the suggested "runtime source → B" attack fails)

The counterargument that a mirror or a runtime source cannot be A contradicts the
contract's own enumeration: **"source code" is explicitly a tier-A object**, and the
contract imposes no canonical-host condition. The row pins commit
`5a79e5e2f46296d8d994f38fa32b429774f33b61`, which binds the fetched bytes via git
content-addressing; the retained copy
`corpus/evidence/sources-r42/S234.c` contains all anchored facts (`supervisor_exit_cb`:280,
`oom_handle_cb`:305, `merge_container_cgroups_path`:348,
`common_get_cgroup_oom_handler`:375, `epoll_loop_add_handler` under `ENABLE_OOM_MONITOR`:381,
`exit_code = 137`:289 — the 137 anchor reads "行 280" in the row but the literal lands at
:289 inside the same function; a nit, not a tier defect). The scope is correctly hedged to
"how one container runtime receives a cgroup OOM notification … not the kernel's
victim-selection policy," and the citing entry states the boundary itself
(`oom-evidence-loss-r38.md:60-61`: "authoritative for that product, illustrative of the
mechanism"). Every existing tier-A code row in the registry is fetched from a host the
source's publisher does not own (raw.githubusercontent.com serving systemd, bpftrace,
Linux); if mirror/middleman hosting demoted code to B, most of the A-tier code rows would
fall with it. A holds.

## 3 — S235 stays A (the suggested "vendor source → B" attack fails)

A vendor whitepaper is not primary for general kernel semantics — but that is not the
claimed scope. The scope is "openEuler's own statement of the limitation of its container
runtime's OOM-event capture and of the ContainerStatus reason field"; for a vendor's own
statement about its own product, the vendor's document is "official docs" — a tier-A
enumeration. Precedent is consistent: S043 (Z.AI's own API error docs) is A; the S241
sibling is B *because it is machine-translated* (`ms.translationtype: MT` — confirmed in
`S241.html`), i.e., a derived rendering, which is the correct discriminator this row does
not share. The anchor verifies: p.27 「约束限制」 quote located
(`pdftotext`, `无法成功捕捉容器` count 1; `reason`/`OOMKilled` at extracted line 1119),
PDF sha256 `9855a4986a…` byte-identical to the pin. A holds.

## Adjacent defect found while attacking (not a tier call)

`corpus/knowledge/oom-victim-context-r41.md` carries **two `source:` headers**:
line 1 names "the publisher-deposited OpenAlex record," line 4 names "the publisher's
Semantic Scholar record and by OpenAlex." Line 4 is stale pre-re-grounding text —
lesson M3 (`round-42.md:83`) records that Semantic Scholar answered "DOI not in Semantic
Scholar" and the recheck failed; the row's own anchor says the same. The landed entry thus
asserts a source that provably does not carry the work — an internal false-provenance
contradiction independent of the tier question. (Also, neither OpenAlex nor Semantic
Scholar is "the publisher"; IEEE is.)

## Impacted axes

- **Provenance/contract fidelity:** S262's A inflates an aggregator record to primary and
  bakes an unverified "publisher-deposited" claim into scope+anchor+gate+entry (1 axis, 1 row).
- **Consistency:** S057's aggregator-abstract-at-C versus S262's aggregator-abstract-at-A
  is the same evidence class tiered two apart.
- **Census hygiene:** no enum/tier-inflation trip (`t=="A" && k=="community"` only); a
  downgrade is invisible to the mechanical checks — judgment input only.

## Smallest safe correction

1. New row `S3NN | …same source… | paper | B | … | teaches: "supersedes S262 — the held
   bytes are OpenAlex's work record (abstract inverted index), not the publisher's
   deposit; IEEE unreachable (HTTP 202/0-byte) and Semantic Scholar lacks the DOI, so the
   abstract-level claims are strong-secondary, not the original paper"` — append-only rule
   (contract §2) forbids editing S262 in place; tier changes by supersession are the
   established pattern (S073/S074/S075/S076).
2. In `corpus/knowledge/oom-victim-context-r41.md`: drop the stale line-4 `source:` header
   (Semantic Scholar), keep the OpenAlex one, and correct "publisher's"/"publisher-deposited"
   to "OpenAlex" wherever it asserts deposit provenance.
3. Optional nit: S234 anchor "exit_code = 137" is at `S234.c:289`, not 行 280 — fold the
   line fix into the superseding-row pass only if the anchor cell is otherwise touched;
   it does not affect the tier.

No installs this seat (pacman paused host-wide; no tool needed beyond python3/pdftotext
already present).
