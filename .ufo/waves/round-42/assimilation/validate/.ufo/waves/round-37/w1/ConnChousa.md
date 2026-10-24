# ConnChousa — does the r37 drift probe touch chousa's research domain?

Item attacked: the province boundary of this round's C2 tool surface (`tools/mori-source-drift.py`,
the drift probe) against the dead-zone boundary chousa admitted in round 34. This is a
verdict item, not a defect hunt on the predicates themselves.

## Chousa r34's admitted boundary (the other lane's ground)

- Chousa's domain is the deep-research method: "question framing, source hierarchy, citation
  chaining, claim-vs-source verification" (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-34/chousa.md:3-4`).
- The admitted dead zone: `verify-claims` transports a claim span to grep(1) as **one PCRE
  pattern of four bytes per span byte**; the PCRE2 compiled-pattern ceiling (~64K code units,
  row S065) binds at spans of **32765–32767 bytes** — under the execve `MAX_ARG_STRLEN` argv
  ceiling (32 pages, row S064) — so those spans read `CLAIM_SPAN_NOT_FOUND` even when the
  source holds them verbatim (`chousa-shokunin/corpus/knowledge/dead-zone-pcre-r34.md:6-32`;
  report `chousa.md:16-19,26-28`). Fixed on chousa's side by routing the window onto a chunk
  matcher (`TOK_DIRECT_SPAN_MAX` 32767→32764, `fe0f22e0`).
- The boundary is thus: **length-sensitive failure of claim-span verification via
  content-compiled regex through grep/PCRE2/execve**.

## What mori's r37 drift probe actually does

`tools/mori-source-drift.py --root .` reads mori's own `corpus/SOURCES.md`, re-fetches each
row's URL, and classifies copy-vs-body: `fresh` (sha256 equal), `excerpt` (stripped copy
occurs contiguously in the body), `drifted` (neither), `unavailable`, `no-copy`
(`tools/mori-source-drift.py:14-28,202-208`). The round's work names and mutation-pins the
two fetch policies (4 MiB bounded read; post-redirect public-destination check) and binds the
corpus (`corpus/knowledge/source-drift-hardening-r37.md:25-58`, contract P-C2).

## Verdict: stays inside mori's detection/report province

Element-by-element against chousa's four method pillars:

1. **Question framing** — the probe accepts no questions; its only inputs are mori's
   append-only registry rows (id + URL cells only: `parse_registry`,
   `tools/mori-source-drift.py:60-72`). No touch.
2. **Source hierarchy** — all rows are treated uniformly; the tier cell is never read, and the
   only ordering rule is mori's own corpus-storage rule (highest `sources-r<N>` copy,
   `:75-99`), not a hierarchy-of-authorities method. No touch.
3. **Citation chaining** — single hop row→copy→today's body; no citation graph. No touch.
4. **Claim-vs-source verification** — the probe never verifies a claim text against a source.
   It verifies **mori's committed copy bytes against today's body bytes** (sha256 / substring,
   `:202-208`) and disclaims the stronger reading in its own bytes: "a **byte-behavior**
   probe: `drifted` means the committed copy is not reproducible from today's body, never
   'the source changed'" (`corpus/knowledge/source-drift-hardening-r37.md:22-23`, docstring
   `:26-28`). Disposition is left to the operator (`...r37.md:68,79-81` — "disclosed, not
   remediated — detection and report only"). No touch.

The dead-zone mechanism specifically **cannot arise** in this probe: no content-derived
pattern is ever compiled (the only regexes are three static short patterns on row/URL/directory
text, `:46-48`), and the import list (`:31-44`) contains no `subprocess` — so neither chousa
ceiling (execve argv, S064; PCRE2 compile, S065) is reachable. A copy of exactly 32765–32767
bytes is hashed or substring-searched in CPython, both length-agnostic; no 32765-boundary
exists in `hashlib`/`bytes.__contains__`. The probe's own size boundary is a different window
with a different mechanism — bodies **over 4 MiB** grade `unavailable` as a memory-safety read
cap (`FETCH_MAX_BYTES`, `:54,163-165`), disclosed in this round's knowledge entry
(`...r37.md:77-78`, "No row currently does"). Analogous disclosed blind spot, mechanically
independent: nothing migrates in from chousa's window.

The boundary in force is written down where both lanes can see it: fleet CORPUS.md (installed
copy `corpus/evidence/sources-r36/S205.src:118-122`, row S205): "**No second method.** Claim
admission stays in `corpus/QUALITY.md`; the research method stays chousa's
(`chousa-shokunin/SKILL.md`: question → source hierarchy → citation chain → claim-vs-source
check)." This round's knowledge entry cites S205 as the corpus contract it operates under
(`...r37.md:5-7`). The probe sits on mori's side of that line (row/copy freshness), not
chousa's (method).

## Second-order surfaces traced

- **Runtime**: probe is read-only over `--root` (docstring `:26-27`); selftest serves on
  127.0.0.1 with `mkdtemp` scratch. No sibling-lane tool invoked; no writes under DIR.
- **Contract**: P-C2 binds only mori's tool, mori's rows S221–S225, lane commit `8ff9bba`;
  no chousa artifact is an input (`.ufo/waves/round-37/contract.md:52-78`).
- **Substrate**: disjoint engines — chousa's ceilings live in execve(2)/grep/PCRE2; mori's
  probe lives in CPython urllib/hashlib/bytes. Empty intersection.
- **Verification**: mori's selftest exercises fetch policies, not span matching; chousa's
  dead-zone probe (20 lengths × 5 content classes) has no analogue needed here.

## Contradictions stated (none smoothed over)

- Arguable contact #1: the `excerpt` containment check superficially resembles
  claim-vs-source (it asks "does mori's copy text occur in today's body?"). It stays on
  mori's side because the checked text is mori's own committed evidence copy, never a
  research claim, and the knowledge entry disclaims source-change inference. Watch line:
  if a future round fed *quote anchors* (claim text) into this check, that would cross the
  S205 line into chousa's pillar 4. Nothing in r37 does.
- Arguable contact #2: mori's census emits `SURFACE lane.chousa` rows (fleet watch,
  e.g. `corpus/evidence/baseline-r10-20261015T2231Z.json:32`). That is mori's fleet-wide
  detection province, predates r37, and is not the drift probe. The reverse-direction
  lineage (chousa's `research-gate.sh` comments citing mori's pin/drift idiom,
  `.ufo/waves/round-17/build/CensusConsumers.md:94-95`) is comment lineage only — chousa
  reads no mori files or ids, and mori reads none of chousa's.

## Measurements (commands and observed output)

1. `python3 tools/mori-source-drift.py --selftest` (lane repo, read-only) →
   `selftest exit_code PASS / row_states PASS / summary PASS / huge_cap PASS /
   redirect_private_refused PASS / missing_sources_exit2 PASS`,
   `MORI_SOURCE_DRIFT_SELFTEST: PASS (6 cases)`, exit=0 (4.57 s). The named arms exercise
   the two fetch policies; no case compiles content into a pattern.
2. Sweep `chousa|3276[0-9]|dead.?zone|pcre|research-gate|claim-vs-source` over
   `.ufo/waves/round-37/` → matches only the wave's own task-spec strings
   (`gen-wave-spec.py:572-577`, `w1-plan.json`, `w1-spec.json`, `w1-taskcall.json`,
   `w1-tasks.json` — this assignment's text). No claim, evidence, counter, or corpus file of
   the round references chousa's domain or dead zone.
3. Sweep `3276[0-9]|dead.?zone|pcre2?\b|PCRE` repo-wide → incidental only (scratch-JSON git
   digests, systemd build-flags string in `round-16/runtime-versions.json:17`); zero hits in
   `tools/` or the r37 corpus surface.
4. Static reads cited above: probe imports/classify/fetch (`tools/mori-source-drift.py`),
   knowledge entry, contract, S205 copy, chousa r34 report + dead-zone entry.

Tool installs: none (no install or upgrade performed this seat).

VERDICT: PASS
