# CritV3Spec — v3 spec attack (round 48 w1)

Scope: review only; no production files changed. Axes impacted: **calibration** (C1), principally soundness (junk must not score green) and real-registry acceptance (honest pins must remain green).

## Counterexample and contradictions

1. **R1 header variants are not made consistent with R2 visibility.** R1 requires recognition of `self-test`, `selftest`, and `self test` case-insensitively. The entering v2 parser actually recognizes only a header cell exactly equal to `self-test` after `.lower()`. R2 marks a row hidden only when it is *not part of a parsed table*. Thus the intended recovery depends on R1 changing table parsing before R2 classifies rows; merely adding an R1 finding after parsing leaves variant-header rows outside the parsed table and risks duplicate/misclassified findings. R2 also needs an explicit precedence: recognized alternate headers form parsed tables, and only malformed/terminated tables' relevant rows become hidden. This is fixable spec/implementation coordination, not a reason to reject the goal.

2. **R4 prose and baseline-binding identity disagree.** R4 says a *new or old* row using a baseline prefix with a different argv is `rebound`, and describes a baseline set of `prefix → bound argv`. The entering implementation actually compares `(row name, prefix, ordinal)` keys (`pin_bindings`/`check`), so a newly named row never matches a baseline key. New rows are explicitly in scope per R4; row name therefore cannot be part of that identity. Small correction: define and enforce the global set of allowed argv per baseline prefix (with an explicit policy for prefixes that legitimately bind multiple commands); do not use row-name equality as the prerequisite for rebound.

3. **R5 is underspecified for cells with multiple paths.** “Nearest preceding path in the same cell” gives a deterministic lexical rule, but not necessarily the path the prose's count qualifies; R6 instead permits any named path for a digest. This is a policy inconsistency when a cell names multiple artifacts. For R5 either require a single explicitly bound path/count pair, or specify that every line-count claim binds to the immediately preceding command/path token and add ambiguity as `unparsed`. The real entering registry's `(743 lines)` pin is not a false red: it is the `tools/mori-gate-registry.py` self-test artifact, and that file has 743 newline-terminated lines.

4. **R3's boundary for “ASCII tally pin” is unclear.** The first-token non-ASCII rule and NFKC-casefold rule can both fire on one span, while R8 requests separate arms for each rule. Require one finding per malformed span (not per rule) and define the accepted ASCII prefix/tally grammar, including whether a tally token after leading punctuation/text is an unparsed residue (R7 says it is).

## Real-registry R5 spot test

I ran a scratch-only implementation of the stated nearest-preceding-path line-count rule against the entering revision's extracted `SKILL.md` and the real target from git:

```text
line=184 path='tools/mori-gate-registry.py' pin=743
actual_newline_count=743 mismatch=False
```

Command evidence for target file: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show e5dbac05459887d9597ea5d1da0d8e3d024e0d17:tools/mori-gate-registry.py | wc -l` → `743`, exit 0. A digest spot check also showed `37fd7c24ff52…` matches `.ufo/waves/round-45/count-c3.py`, and `69bf9b6eb29b…` matches `.ufo/waves/round-45/fixtures/mutants/count-c3.py` at the same revision. I did not run the candidate v3 tool (none was supplied in this seat); therefore this is rule-level evidence, not a candidate acceptance claim.

## Three fresh junk edits (unified diffs against entering `SKILL.md`)

These illustrate missed/ambiguous classes, not claims that the frozen C1 counter scores them. Each is a single proposed edit; apply separately.

### J9 — new row reuses a baseline prefix with a different binding

R4 says this must be `rebound`; the entering implementation's row-name-keyed binding lookup cannot associate the new row with the baseline prefix.

```diff
--- a/SKILL.md
+++ b/SKILL.md
@@ -163,1 +163,2 @@
 |---|---|---|---|---|---|---|---|
+| calibration decoy | gate | `python3 tools/mori-gate-registry.py --rev <rev>` | 0/1/2 | `python3 tools/mori-gate-registry.py --selftest` → `PIN_CHECK_SELFTEST pass=999 fail=0` | none | none | mori |
```

### J10 — ASCII-dot truncated digest

R6 only recognizes the U+2026 ellipsis form. Replacing the existing shortened digest with ASCII dots removes it from both the full SHA-256 recognizer and the specified truncated-digest recognizer, leaving a wrong digest-like pin unmeasured.

```diff
--- a/SKILL.md
+++ b/SKILL.md
@@ -192,1 +192,1 @@
-| r45 corpus coverage (C3) | gate | `python3 .ufo/waves/round-45/count-c3.py <rev> --entry PATH --row S###` (`--entry`, `--row` and `--coverage-map` are each repeatable; `--root` defaults to the parent directory of `--repo`; `--census PATH` defaults to `<root>/scripts/sources-census.sh`; `--readme`, `--repo`, `--timeout S`, `--selftest`) | 0 → `C3=met rev=… entries=N rows=… census_sha256=…` · 1 → `C3=unmet` (an entry absent or missing `source:`/`verified-at:`/`recheck:`/`coverage-map:`, a declared row absent, not `mined`, or not naming the entry in `used-by`, a token collision such as S473 against S4731 or FR5 against FR12, a red census, or no README map row) · 2 → `C3_SETUP` (usage, a missing `--entry` or `--row`, unresolvable revision, census timeout) | `python3 .ufo/waves/round-45/count-c3.py --selftest` → measured `C3_SELFTEST pass=19 fail=0` rc 0 at sha256 `37fd7c24ff52…`; the mutant `.ufo/waves/round-45/fixtures/mutants/count-c3.py` (sha256 `69bf9b6eb29b…`) disables the census exit check (`proc.returncode == 0` to `True`) and its own run reads `C3_SELFTEST pass=17 fail=2` rc 1 | `--census` default `<root>/scripts/sources-census.sh`, whose sha256 the verdict line prints; the `corpus/README.md` map section; the declared entries and rows; lane `mori` | stdout only; fixtures are written under a `c3st-` `tempfile.mkdtemp` in the caller TMPDIR; the census arm executes `bash <root>/scripts/sources-census.sh validate --root <root> mori` with the caller's privileges, so that caller-named program is not sandboxed | mori |
+| r45 corpus coverage (C3) | gate | `python3 .ufo/waves/round-45/count-c3.py <rev> --entry PATH --row S###` (`--entry`, `--row` and `--coverage-map` are each repeatable; `--root` defaults to the parent directory of `--repo`; `--census PATH` defaults to `<root>/scripts/sources-census.sh`; `--readme`, `--repo`, `--timeout S`, `--selftest`) | 0 → `C3=met rev=… entries=N rows=… census_sha256=…` · 1 → `C3=unmet` (an entry absent or missing `source:`/`verified-at:`/`recheck:`/`coverage-map:`, a declared row absent, not `mined`, or not naming the entry in `used-by`, a token collision such as S473 against S4731 or FR5 against FR12, a red census, or no README map row) · 2 → `C3_SETUP` (usage, a missing `--entry` or `--row`, unresolvable revision, census timeout) | `python3 .ufo/waves/round-45/count-c3.py --selftest` → measured `C3_SELFTEST pass=19 fail=0` rc 0 at sha256 `37fd7c24ff53...`; the mutant `.ufo/waves/round-45/fixtures/mutants/count-c3.py` (sha256 `69bf9b6eb29b…`) disables the census exit check (`proc.returncode == 0` to `True`) and its own run reads `C3_SELFTEST pass=17 fail=2` rc 1 | `--census` default `<root>/scripts/sources-census.sh`, whose sha256 the verdict line prints; the `corpus/README.md` map section; the declared entries and rows; lane `mori` | stdout only; fixtures are written under a `c3st-` `tempfile.mkdtemp` in the caller TMPDIR; the census arm executes `bash <root>/scripts/sources-census.sh validate --root <root> mori` with the caller's privileges, so that caller-named program is not sandboxed | mori |
```

### J11 — alternate line-count syntax

R5 recognizes only `(<digits> lines)`. An equivalent count phrased as `(<digits>-line file)` is invisible to R5; if it is stale, the registry can retain a false assertion without a mismatch.

```diff
--- a/SKILL.md
+++ b/SKILL.md
@@ -184,1 +184,1 @@
-| r44 gate registry (C2) | gate | `python3 tools/mori-gate-registry.py --rev <rev> --audit <repo-relative path> [--audit ...]` (`--registry PATH`, `--repo PATH`, `--selftest`) | 0 `REGISTRY=met` · 1 `REGISTRY=unmet` (unregistered path, a missing standard cell, an entry path that does not resolve at the revision, or no `--selftest` mode in the tool) · 2 `REGISTRY_SETUP` (usage, unresolvable revision, absent registry or gate table) | `python3 tools/mori-gate-registry.py --selftest` → measured `GATE_REGISTRY_SELFTEST pass=15 fail=0` at sha256 `8b82ac999091ebe65e765ed69f759910a57049ff0e7c5c4aa56df9c7168f5832` (743 lines); v2 covers second-table registration, duplicate names, comment-only selftest, population mode and escape flags | in-script fixture registry rows; the audited surface is this SKILL.md `## Gates` table at `--rev` | stdout only; reads registry and audited files from git at the requested revision | mori |
+| r44 gate registry (C2) | gate | `python3 tools/mori-gate-registry.py --rev <rev> --audit <repo-relative path> [--audit ...]` (`--registry PATH`, `--repo PATH`, `--selftest`) | 0 `REGISTRY=met` · 1 `REGISTRY=unmet` (unregistered path, a missing standard cell, an entry path that does not resolve at the revision, or no `--selftest` mode in the tool) · 2 `REGISTRY_SETUP` (usage, unresolvable revision, absent registry or gate table) | `python3 tools/mori-gate-registry.py --selftest` → measured `GATE_REGISTRY_SELFTEST pass=15 fail=0` at sha256 `8b82ac999091ebe65e765ed69f759910a57049ff0e7c5c4aa56df9c7168f5832` (742-line file); v2 covers second-table registration, duplicate names, comment-only selftest, population mode and escape flags | in-script fixture registry rows; the audited surface is this SKILL.md `## Gates` table at `--rev` | stdout only; reads registry and audited files from git at the requested revision | mori |
```

## Smallest safe corrections

- R1: specify parser behavior and precedence alongside R2; cover every spelling and case variant in one acceptance test plus a hidden-row test.
- R4: bind baseline permissions by prefix to its set of argv identities, not by `(row name, prefix, ordinal)`; test a renamed/new row.
- R5/R6: define supported count/digest syntax and scope explicitly; reject or report unparsed pin-like residue rather than silently ignoring it. For multi-path rows, require unambiguous associations (or explicitly state and test the chosen binding policy).
- Add J9–J11 as independent mutation cases and state their expected verdicts. No tools were installed or updated.
