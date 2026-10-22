# ReviewProvinceReadme — round-25 appended sections of PROVINCE.md and corpus/README.md (FR15)

Verdict: **held** — both appends are addition-only and adjacency-correct, and most line
references are exact. One MEDIUM stale-pointer finding and two LOW precision findings should
be fixed before bind. Nothing is broken.

Reviewed: the round-25 appended blocks PROVINCE.md:291-355 and corpus/README.md:483-522,
landed in 1888bc6 (the only commit touching these two files in 28b79d3d..HEAD), measured at
tip 07a31ae against base 28b79d3d. All position checks were done by raw line pins plus grep;
no LSP server answers these markdown files in this session, so grep/raw-read is the recorded
fallback, not semantic proof.

## Findings

### MEDIUM F1 — stale first-evidence pointer `harness-job-capacity-r25.md:28-213` at tip
- Where: PROVINCE.md:322 and corpus/README.md:497.
- It was correct when written: at 1888bc6 the knowledge file is 303 lines with `## Facts` at
  28, `## Decision table` at 192, last row (hyaku gate) at 212, blank at 213, `## Limits` at
  214 — so 28-213 covered exactly Facts plus the decision table.
- Wave-2 knowledge amendments shifted it: d3b7af2 ("harness entry records whose ground each
  fact is", with a `Whose ground (wave-2 CriticC2Admission)` section above Facts) and
  51dc820 grew the file to 311 lines (numstat 1888bc6→HEAD: +10/−2). At tip 07a31ae, line 28
  is `**Whose ground (wave-2 CriticC2Admission).**…` prose, `## Facts` is at 36,
  `## Decision table` at 200, the hyaku row at 220, `## Limits` at 222.
- Effect: dereferencing 28-213 at the landed tip starts in the Whose-ground prose and stops
  eight rows short of the table's end, so the pointer no longer addresses the evidence span
  it names in two landed files.
- Smallest fix: after the knowledge file's still-open wave-2 edit settles, re-pin both sites
  to the tip span (36-221 at 07a31ae; 36-199 if only the Facts rows are meant), recomputing
  at edit time.

### LOW F2 — SOURCES id list contradicts its own line range ("S098–S103" vs `104-110,118-119`)
- Where: PROVINCE.md:318-320 and corpus/README.md:488.
- Raw pins: corpus/SOURCES.md 101=S095, 104=S098, 108=S102, 110=S104, 118=S112, 119=S113, so
  the cited range `104-110` = S098–S104 (seven rows). The id list names only S098–S103 and
  drops S104 — but S104 is opened and admitted this round (SOURCES.md:110: status `mined`,
  2026-10-22, used-by `corpus/knowledge/harness-job-capacity-r25.md`) and the knowledge
  file's own source line says "Rows S098–S104 and S112–S113 were opened and admitted in
  round 25" (harness-job-capacity-r25.md:1). The appends are the only places that say S103.
- "all at oh-my-pi tag `v18.12.6` (commit `45c35e40…`)": false for S104, which is the
  2026-02-22 introduction commit (twinned SHA, tag lineage pre-v15.1.9), not a tag checkout.
  In PROVINCE.md:320 the own-work row S102 is correctly carved out ("plus the installed
  binary as an own-work row (S102)"); README.md:488 has no carve-out, so its "all at tag"
  is false for two of the nine rows its own range dereferences to.
- Smallest fix: write "S098–S104 and S112–S113"; scope the "at tag v18.12.6" clause to
  S098–S101 + S103 + S112–S113, name S104 as the introduction-commit row, and add the
  own-work carve-out for S102 in README.md:488.

### LOW F3 — "a fourth resource class" states no counting basis
- Where: PROVINCE.md:346-347 ("extends the owned read-only probe list named at
  `PROVINCE.md:6-10` with a fourth resource class").
- PROVINCE.md:6-10 names five probe families (watchdog liveness; waves settlement; kill/OOM
  journal+cgroup records; resource runway; lane silence). On a plain family count the harness
  ceiling is the sixth, not the fourth; "fourth" is reachable only under an unstated
  grouping. The round-24 bullet of the same template (PROVINCE.md:274-277) avoided this by
  naming the ground it extended.
- Smallest fix: "with a further resource class", or name the counting ("after the journal/
  cgroup, disk and memory runway classes").

## Held (verified)

1. **Additions-only purity.** `git diff --stat 28b79d3d -- PROVINCE.md corpus/README.md` →
   105 insertions, 0 deletions; exactly two end-of-file hunks (PROVINCE.md
   `@@ -288,3 +288,68 @@`, corpus/README.md `@@ -480,3 +480,43 @@`). Both files are clean vs
   HEAD (`git diff HEAD --stat` empty for them), so this is the landed diff. No existing FR
   row rewritten; PROVINCE.md:3-16 and 6-10 are byte-unchanged, exactly as the append claims.
2. **Pointer targets exact.** README FR table = lines 332-345 (raw pins: 331 separator, 332
   FR1, 336 FR5, 338 FR7, 345 FR14); PROVINCE FR counterparts = 44-57 (44 FR1, 57 FR14);
   PROVINCE.md:6 opens the `**Owns (read-only probes):**` paragraph, :10 closes it. The
   appended notes' citations of 332-345, 44-57, 6-10 and 3-16 are all correct.
3. **FR15 registered only in the appended note.** The FR table still ends at FR14; "FR14 is
   not advanced" is true (row byte-unchanged, and the telemetry-vs-binary-read distinction
   drawn in README.md:503-509 is sound).
4. **Adjacency held.** kumitate PROVINCE.md:3 (Domain scopes OMP task/hub) and :19 (OMP
   harness contract frontier entry) raw-pinned; kumitate's
   `corpus/knowledge/omp-task-contract.md` has zero `maxJobs` hits and records "The effective
   live OMP setting is UNKNOWN." (line 197) — precisely what PROVINCE.md:339-340 claims.
   Mori's own Adjacent table already assigns kumitate OMP task/hub orchestration. Operator
   owns configuration: mori PROVINCE.md:16 ("Detection and report only — never remediation"),
   the appends propose no settings change, and the knowledge file agrees ("Changing the cap
   is the operator's."). Nothing absorbed.
5. **Quoted tool facts match the landed tool** (tools/mori-job-runway.py): schema
   mori-job-runway-v1 (:98), verdicts and exits 0/1/0/2 (:44-47, :101-103), `--config`
   default `~/.omp/agent/config.yml` (:110, :631), `--binary` default the real path of `omp`
   on PATH (:616-620, :636), `effective = max(1, min(clamp, base))` (:43), read-only /
   never-runs-omp (:14-15), selftest prefix (:99).
6. **Host numbers corroborated**: configured 200, clamp 100 at one site, default 100 at one
   site, effective 100, RUNWAY_CLAMPED exit 1, selftest PASS 21/21 — contract.md:41-44 and
   :60-63, the knowledge verified-at line, and S102's single byte offsets. The appended
   sections assert nothing beyond these.
7. **Seat-gate numbers grounded**: "(85 on this host, default 200; the harness cap is 100)"
   matches the knowledge decision-table hyaku row (line 212 at the append commit, 220 at
   tip), whose boundary text also carries the "different population" claim; the gate is
   described, not judged.
8. **Convention kept.** The append reuses the round-24 "Owns-scope extension (append-only;
   `PROVINCE.md:6-10` …)" template (precedent at PROVINCE.md:274-277) and the README
   "coverage additions" table format from round 17. Date 2026-10-22 is correct.

## Residual risk and verification gaps

- The knowledge file is uncommitted-modified in the working tree (` M`) and a sibling seat
  was editing it during this review — I observed both the 303-line and 311-line layouts in
  the working tree within minutes. Every tip pin above is from committed HEAD 07a31ae; the
  F1 re-pin must be recomputed after that edit lands and before bind.
- I did not re-run the tool, its selftest, or live reads; the runtime re-checks belong to the
  rerun seats. My checks are structural and textual; unrun checks are not claimed as passes.
- SOURCES row content integrity (blob hashes, scopes, discernment) is RowChousa's scope; I
  verified only row identity at the cited line numbers.
- Kumitate's contract entry pins docs at upstream `main` against installed omp/18.12.3
  (round-34 skew, its line 205); mori's append claims only what that entry records (no
  maxJobs row, UNKNOWN live setting), which holds regardless of the skew.

## Tooling

No tools installed or upgraded (none needed); pacman untouched.

Report: .ufo/waves/round-25/w2/ReviewProvinceReadme.md
