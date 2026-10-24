# RevAssimEntries — QUALITY gate-check of the two admitted round-42 entries

Reviewer seat: `RevAssimEntries` (leaf, read-only except this report).
Targets: `corpus/knowledge/oom-evidence-loss-r38.md` (FR1),
`corpus/knowledge/oom-victim-context-r41.md` (FR13, FR1).
Read-time tip: `34b926730c30e0251e1aec531863d8355dc491f1` per assignment.
Verification surface: the entry bytes, `corpus/QUALITY.md`, `PROVINCE.md:44,56`,
`corpus/SOURCES.md:238-244`, `corpus/lessons/round-42.md` Gate/M3, and the
committed evidence copies `corpus/evidence/sources-r42/` (read locally; no
live re-fetch performed — see residual risk).

## Findings by severity

### F1 — HIGH · `oom-victim-context-r41.md:4` — provenance contradicts the lane's own record (QUALITY 2, measured anchor)

The trio's source line reads:

> `source: S262 — … — Abstract and TLDR, as recorded by the publisher's Semantic Scholar record and by OpenAlex`

Three committed records say the Semantic Scholar record **does not exist / was
not usable**:

- `corpus/SOURCES.md:243` (S262 anchor cell): "ieeexplore returns HTTP 202
  with 0 bytes from this host; **Semantic Scholar lacks the DOI**".
- `corpus/lessons/round-42.md` M3: "the staged S262 row's recheck command
  (`aaron papers fetch … -m s2`) no longer resolves (**Semantic Scholar now
  answers 'DOI not in Semantic Scholar'**); … re-grounded on the OpenAlex
  deposited-abstract record".
- The retained copy `corpus/evidence/sources-r42/S262.oa.json` is an
  OpenAlex work record only (`ids`: openalex + doi); its `tldr` field is
  `None` and it contains zero mentions of `semantic`/`arxiv`/`openreview`.

So the entry claims a TLDR "recorded by the publisher's Semantic Scholar
record" that, on the lane's own evidence, was never retrieved. The retained
abstract supports every claim the body makes (see verification list), so the
defect is confined to the provenance line: it names a carrier and an artifact
(TLDR) the lane does not hold. Under QUALITY 2 the anchor for this statement
is not measurable — it asserts provenance for bytes that were not read.
[INFERENCE]: the line is plausibly stale pre-M3 draft text — the package
originally grounded on S2, M3 re-grounded on OpenAlex, and the sweep missed
this source line (QUALITY 9 territory: a replacement anchor landed without a
sweep of every mention).

Smallest safe correction: drop "and TLDR, as recorded by the publisher's
Semantic Scholar record" from the source line; the entry already carries the
correct OpenAlex-only provenance in its adoption-provenance block.

### F2 — LOW · `oom-victim-context-r41.md:1` — stray duplicate `source:` line above the title, disagreeing with line 4

File opens:

```
1  source: S262 — … — Abstract, as carried by the publisher-deposited OpenAlex record — …
2  # The kernel's OOM victim selection has no container context
3
4  source: S262 — … — Abstract and TLDR, as recorded by the publisher's Semantic Scholar record and by OpenAlex — …
```

Every sibling entry (`oom-evidence-loss-r38.md`, `conform-source-order-r42.md`,
`source-drift-content-anchor-r38.md`, `kernel-oom-line-attribution-r12.md`)
opens with the H1 and places the provenance trio beneath it. Here line 1 is a
floating pre-title fragment that **disagrees with line 4** — ironically it is
the *correct* (OpenAlex-only) version, while the canonical-position line is
the wrong one (F1). Cosmetic-plus: no conform arm parses entry headers, but
the duplicated, conflicting provenance is exactly the kind of surface
QUALITY 9's "a replacement artifact lands with a sweep of every mention" is
meant to prevent.

### F3 — LOW · `oom-victim-context-r41.md:46` — IEEE document id `11540439` has no anchor in the lane record

The boundary cell states "`ieeexplore.ieee.org/document/11540439` returns
HTTP 202 with a 0-byte body from this host (re-observed 2026-10-24)". Neither
the S262 registry row, the lesson, nor the retained OpenAlex record names
that document id (`ids` carries only `openalex` + `doi`; no `ieeexplore`
substring anywhere in `S262.oa.json`). The claim itself (paywall 202) is
plausible and consistent with the lesson, but the URL it was observed on is
unanchored: if the doc-id is wrong, the "re-observed" access record is
meaningless. QUALITY 9-adjacent (a pointer that must resolve at the carrying
commit); the lesson's "0 bytes from ieeexplore" record does not pin the URL.

### F4 — INFO · `oom-evidence-loss-r38.md` — `memory.high` "never" is tier-B-sourced for an upstream semantic

"`memory.high` imposes reclaim pressure and **never** invokes the OOM killer
(S233)". The retained S233 copy does show the 128MB `memory.high` worked
example with no OOM record beside the `memory.max` dmesg OOM example
(節「メモリ使用の制限値」, `memory.highに制限値128MBを追加` located), and the
upstream semantics in S002 back the direction of the claim — `memory.high` is
throttle, not a kill trigger. The entry is honest about tiering (boundaries:
"S232 and S233 are tier-B Japanese secondary accounts; the upstream kernel
documentation … remains primary") — but this particular claim is a *primary*
semantic, cited only to the tier-B worked example while the primary source
the lane holds (S002 `memory.high` semantics) is not named on this line.
Directionally correct and scope-limited by the entry's own boundaries; not a
falsifiability defect. Observation only.

## Gate answers (assignment checklist)

1. **Provenance trio present** — PARTIAL PASS.
   - r38: `source:` ×5, `verified-at: 2026-10-24`, `recheck:` ×3 covering
     S234, S235, S232 (S233/S241 uncovered by recheck lines but the rows
     carry `180d` — pattern matches convention; sources opened by name).
   - r41: trio fields exist but the `source:` line is (a) duplicated in a
     stray pre-title fragment (F2) and (b) internally contradicted on the
     Semantic Scholar/TLDR carrier (F1).
2. **Claims falsifiable or marked opinion** — PASS with F1 caveat.
   - r38: three loss mechanisms each S-anchored (S234+S235, S233, S241);
     survivor semantics anchored to S002 + S232; every claim checkable.
   - r41: victim-context claim, co-located kill and leaked-resource claims,
     remedy shape, and the 6.94 % / 6.9 s / 8 attackers / 24 h / 64
     container figures are all verbatim-supported by the retained abstract
     and explicitly attributed to the paper ("The paper's own study
     finding", "The lane has not reproduced it") — correctly marked as
     authors' measurement, not lane observation.
3. **Boundaries named** — PASS. Both carry `### Boundaries` *and* `###
   Delivery paths this cannot see` (QUALITY 17). r38 correctly refuses
   generalization beyond path-bound eventfd runtimes and one vendor; r41
   correctly scopes to abstract-level claims and shared-kernel deployments
   and discloses the paywalled body.
4. **Detection/report-only province respected** — PASS. r38: "Nothing here
   licenses a remediation; nothing here changes a quota, a limit or a
   cgroup setting" (:66-67); probe shape is conditional knowledge, no
   retrofit asserted. r41: "mori observes and reports; it does not install
   LSM hooks or eBPF programs" (:55-56). No remediation proposed anywhere.
5. **FR1/FR13 coverage-map ground real** — PASS.
   - r38 `ground:` quote is a verbatim substring of `PROVINCE.md:44`
     ("event-time kernel summary/victim token validation and fleet
     correlation remain frontier"); FR1 exists as a live frontier row.
   - r41 quotes FR13 verbatim (`PROVINCE.md:56` "eBPF kill/OOM tracing")
     and FR1 verbatim. Both entries remain coverage-map ground; the README
     round-42 block (`corpus/README.md:611-619`) registers them with no
     false Core move.
   - The quoted r12 UNKNOWN (`kernel-oom-line-attribution-r12.md:25-26`)
     is byte-verbatim.

## Anchor verification exercised (all local, all passed)

- `S234.c` (commit-pinned): `container_supervisor_add_exit_monitor` :327;
  `merge_container_cgroups_path` resolves the cgroup path at setup :348;
  `epoll_loop_add_handler(&g_supervisor_descr, oom_handler_info->oom_event_fd,
  oom_handle_cb, …)` :381 under `ENABLE_OOM_MONITOR`. `epoll_loop_add_handler`
  count = 2, matching the recheck expectation.
- `S235.pdf`: sha256 `9855a498…d8020` byte-identical to the registry pin;
  `pdftotext … | grep -c 无法成功捕捉容器` → 1; `OOMKilled` present.
- `S232.html`: `POLLPRI` count 4; 状態通知 section carries both `IN_MODIFY`
  and `POLLPRI` notification text — supports the "inotify `IN_MODIFY` or
  poll `POLLPRI`" claim.
- `S233.html`: `memory.highに制限値128MBを追加` worked example located;
  `memory.max`/OOM-killer dmesg example present.
- `S241.html`: `ms.translationtype = MT`, `ms.date = 2025-09-15`,
  `updated_at = 2026-10-14`, KB 4010058 — all as the trio and registry
  state; the diagnosis-at-detection sentence ("診断は、エラーが検出された時点で
  行う必要があります") is verbatim.
- `S262.oa.json`: OpenAlex W7163066205; IEEE TSC vol. 19 no. 4
  pp. 3015–3028, 2026; abstract verbatim-contains "lack sufficient
  container context", "eBPF-based monitoring with two lightweight LSM
  hooks", "6.94% throughput overhead across eight workloads", "recovery
  time within 6.9 seconds", "24-hour runs with up to 64 containers".
- Registry rows S232–S235/S241/S262 (`SOURCES.md:238-243`): used-by cells
  name exactly `oom-evidence-loss-r38.md` / `oom-victim-context-r41.md`;
  S262's own anchor cell already records "Semantic Scholar lacks the DOI".

## Residual risk / verification gaps

- Live fetches were not re-run; byte-equality of `sources-r42/` copies
  against live pages is taken from the Gate record (recheck commands all
  carried the `ran 2026-10-24` marker and expected counts reproduced on the
  copies).
- S262 full text remains paywalled; the entry's abstract-only scope makes
  this a declared boundary, not a gap, but the 6.94 %/6.9 s figures are
  authors' claims as labelled — correctly not promoted to lane measurement.
- F1's fix is mechanical (sweep the stale S2/TLDR wording); if a Semantic
  Scholar record does exist under a different lookup, the fix inverts —
  recommend the integrator verify the S2 lookup result once more before
  editing. My evidence says the record is absent as of the lane's own
  2026-10-24 checks.

## Verdict

- `oom-evidence-loss-r38.md`: **admit-clean** — QUALITY gates 1–3, 17 all
  pass; provenance trio complete and internally consistent.
- `oom-victim-context-r41.md`: **admit-with-errata** — substance fully
  sourced and falsifiable at its declared abstract scope, but the source
  trio carries a contradicted Semantic Scholar/TLDR claim (F1) and a
  conflicting duplicate fragment (F2); F3 is an unanchored pointer. All
  three are bounded to the provenance/header surface; no claim in the body
  is affected.
