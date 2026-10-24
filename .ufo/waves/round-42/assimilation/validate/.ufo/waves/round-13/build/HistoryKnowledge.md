# HistoryKnowledge — round 13 report

**Seat:** leaf executor (no dispatch, no background jobs, no commits).
**Owned writes:** `corpus/knowledge/verdict-contract-r13.md` (new) and this report.
**Axes:** coverage (the note binds F01/F02 to admitted source anchors) and operability
(the note states the roll contract that the round's repair must satisfy).
**Verification:** none run — per contract, L1 owns integrated checks. Everything below is
source reading at pinned bytes plus one read-only URL fetch and one read-only `git diff`
inspection of a sibling's in-flight edit.

## Files changed

| path | change |
|---|---|
| `corpus/knowledge/verdict-contract-r13.md` | new; 6 sections + what-changes + delivery paths + `[UNKNOWN]` |

## What the note establishes

### F01 mechanism (§1), derived from audit-r11 Appendix B + source

- Deciding construct at `tools/mori-census.sh` sha `3da5b098…` `:1494`:
  `printf '%s\n' "$inwin" | sed -E … | grep -Fxq -- "<lane>-shokunin <lane@shokunin.local>"`
  inside an `if`, under `set -euo pipefail` (`:236`).
- `grep -Fxq` exits at the first match and closes stdin; `sed` still writing dies of
  SIGPIPE (S031, pipe(7): write after all read ends close). `pipefail` makes the pipeline
  status 141; the `if` context suppresses errexit, so 141 is read as "no subject" → row-C
  `progressing-weak` (`:1530-1533`) with `other_authored_commits` = the **whole window's**
  line count (`sibn` at `:1493`, emitted `:1532`).
- Audit's observed signature at its pin: expected `progressing`, actual
  `progressing-weak … other_authored_commits=12001`, rc 0, stderr 0 (Appendix B).
- Repair principle named as **capture membership**: matcher input already captured, so the
  only status read belongs to the matcher. Two in-repo precedents: selftest
  `$OUT_FILE` capture + grep at `:2227-2230` with its r9 rationale `:2217-2226`; drift
  section's "NO live pipes in this section" + here-string `sed` at `:1745-1749`.
- Kept out of the repair's blast radius: the exact `-Fx` identity grammar, and the
  independent full-read count (`awk 'END{print NR}'`).

### F02 mechanism (§2–§3), derived from audit-r11 Appendix C + source

- Base oracle (sha `448f7723…`) captures the first `^MORI_CENSUS:` line (`:570`) and uses it
  only in failure text (`:600`) and the differential shape grade (`:981-982`).
- It rejects rc>1 setup (`:572-576`) and missing roll (`:582-586`), then grades state
  (`:588-591`), finding (`:592-597`), case rc (`:598-601`), nonce (`:602-606`). It never
  checks the word, the roll count, the tuple, or word↔rc coupling — so the Appendix C
  proxy (`BANANA`, rows/rc preserved) scored `28/28` (audit measurement), and both mismatch
  arms pass by source reading (not executed here).
- Cardinality is invisible (`grep -m1`), and shape-invariance is differential
  (`:1002-1004`), so a consistently wrong word passes both sides. Guards outside
  `assert_case` (`:939-953`, `:985`) never read the roll.
- Asymmetry documented: the census's own selftest already asserts
  `^MORI_CENSUS: ${wverdict} ` on a captured file (`:2230`), i.e. the outside check was
  weaker than the inside one; that internal check still does not enforce cardinality.
- Admitted grammar table (`:7-8`, `:352-353`, `:1733-1734`, `:1736-1740`, `:360-372`,
  `:3008-3010`) plus two labelled `[INFERENCE]` invariants: `DRIFT ⇒ drift ≥ 1`,
  `CLEAN ⇒ drift = 0`.

### C1 coupling and class limits (§4–§5)

- New structured counts must not add a third word, a second `MORI_CENSUS:` line, or a roll
  flip without an explicit `warn|crit` emission; notice counts are not victim counts and
  scopes are never summed (r12 MESSAGE_ID note; QUALITY 15–16).
- Table of classes the repaired oracle can and cannot see: vocabulary, rc coupling,
  cardinality, grammar, missing roll = yes; counter truth, F01's size-dependent grade,
  `--selftest/--pin/--drift` modes, live host/journal delivery = no; the census selftest's
  own duplicate-roll gap = still open there.

## Exact retained evidence

- `sha256sum` at the frozen pins: census `3da5b098dc23aeb3e1c31ce82664b24a22c2847a168308a755525593881b3164`,
  oracle `448f77238c73a5c929a898dad0f0c495fd2a66cc4b90a00ae84ede69a86beeb5`; wave
  `frozen/inputs.json` matches; `sources-before.json` validates `corpus/SOURCES.md` (exit 0).
- S031 opened this session: `https://man7.org/linux/man-pages/man7/pipe.7.html`, man-pages
  6.19. Quoted text: writes after all read ends close generate SIGPIPE; default pipe capacity
  is 16 pages (65,536 B at 4 KiB pages).
- Line anchors verified by reading the frozen copies (not the mutable working tree), with the
  audit's r11 anchors noted as moved by r12 edits: audit `:1366-1374` → base `:1490-1494`;
  audit oracle `:569-585` → base capture `:570`, setup `:572-576`, crash `:582-586`.

## Risks and notes for L1

1. **In-flight sibling edit.** `tools/mori-silence-cases.sh` is already modified in the
   working tree (current sha `a8824408…`, base `448f7723…`; +77/−14). I did not treat it as
   the contract: the note cites base bytes only, and `§6 Pointer status` explicitly leaves
   post-repair SHAs/anchors/tally to L1. The in-flight diff does contain a `verdict_grade`
   (vocabulary + cardinality + rc coupling + here-string), which is consistent with the
   note's §3, but I make no claim that it lands or passes.
2. **No counts invented.** The note asserts no current case tally, no post-fix line number,
   and no measured post-fix result. The only numbers quoted are audit-r11's at its pins and
   the fixture construction the audit states (1 subject + 12,000 siblings → 12001).
3. **Anchor fragility.** All census anchors bind to `3da5b098…`. CensusFix's edit will move
   the `:1490-1494` construct; the note says so and tells the reader to re-anchor after
   integration rather than silently reusing the numbers.
4. **Scope of the note's claim.** It is a contract/mechanism note, not a repair review and
   not a falsification proof; §5 names the residual classes (counter truth, F01 size,
   non-live modes, live host).
5. **SOURCES.md registry (not mine to write).** S031 is still `queued` with `used-by: —` at
   `corpus/SOURCES.md:37`; the note now cites it (opened 2026-10-20). If the lane's registry
   convention is that a cited source flips to `mined` with the consuming note in `used-by`,
   that sweep is L1's. Separately, S013's `used-by` already names
   `corpus/knowledge/structured-journal-scopes-r13.md` (the C1 sibling note), so the two r13
   notes can be cross-referenced at integration.
6. **Tooling.** No installs or upgrades were needed; nothing was installed. No system
   package operations were run.

## Blockers

None. No credential material, raw journal `MESSAGE`, process environments or secret paths
were read; no remediation or external state was touched.
