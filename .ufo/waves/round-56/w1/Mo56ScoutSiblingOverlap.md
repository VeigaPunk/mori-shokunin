# Mo56ScoutSiblingOverlap — sibling-overlap scan (driver-liveness reader / vote binder / registry duplicate-url)

Seat: Mo56ScoutSiblingOverlap (mori-shokunin, round 56 wave w1, scout).
Scope: do the sibling lanes kumitate / tsukuroi / souji / kama hold (a) a
driver-liveness reader of `.ufo/watchdog.log` or (b) a seat-output vote
binder, in their `tools/` or `corpus/knowledge/`; and do their
`corpus/SOURCES.md` registries already hold an `rfc-editor.org/rfc8259` row
or an own-work row for the fleet driver writer scripts (duplicate-url class).
Method: read-only `grep -rl/-n` over the four sibling repos plus mori's own
registry for contrast. No writes anywhere except this report. No tools
installed. Scratch `/fast/scratch/hyaku/mori-r56/Mo56ScoutSiblingOverlap/`
created for TMPDIR and removed before finishing. This wave carries no vote
items; no line below starts with a vote keyword.

## Question 1 — driver-liveness reader of `.ufo/watchdog.log`

Reference grammar (from the frozen C1 tool
`tools/mori-driver-liveness.py:23-37`): ISO-8601-ts-first lines shaped
`launch|complete|lane-dead-no-report|launch-fail|wrap <lane> round=<n> ...`,
writers `scripts/hyaku/inline.sh` (`:149/:176/:182`) and
`scripts/shokunin-watchdog.sh` (`:266/:405/:448/:398/:241-249`).

Per-lane result — no sibling holds a reader:

- kumitate-shokunin: no `tools/` directory exists
  (`ls /home/vgpnk/Projects/shokunin/kumitate-shokunin/tools/` →
  "No such file or directory", exit 2). Only knowledge hit for
  `watchdog.log` is `corpus/knowledge/ops-watchers.md:70`, which describes the
  kimi hub ops-watcher telemetry vocabulary (`watchdog_log_rotated`,
  `watchdog_log_rotate_failed`, rotation cap) — the hub substrate, not the
  hyaku driver log. `corpus/knowledge/round-close-gate.md:68,94,122` cites
  `scripts/shokunin-watchdog.sh:3-4,44` for the round-close gate semantics
  (`report_of()` is the completion signal) — a contract citation, not a log
  parser. `corpus/knowledge/kimi-skills-plugins.md:116,124` lists the script
  file in a skills census.
- tsukuroi-shokunin: zero references to `.ufo/watchdog.log` in `tools/`
  (grep `watchdog.log` over `tools/` → no output, exit 1). Knowledge
  `watchdog` hits are unrelated planes: `oom-event-plane.md:62,119` (Chromium
  GPU-watchdog thread as OOM symptom), `degraded-triage-r4.md:478,486`
  (Hyprland `--watchdog-fd`), `adjacency-handoffs-fleet-r1.md:107` (an
  adjacency *request to mori* to run a watchdog/wave capture — mori-side
  work), plus `host-health-report-r3.md`, `journal-boot-plane.md`.
- souji-shokunin: `tools/` references `.ufo/watchdog.log` only to exclude or
  prune it, never to read it: `souji-verify.sh:35` ("never touched"),
  `:546` (path guard returning 1), `:759` (rsync exclude
  `!**/.ufo/watchdog.log`); `souji-census.sh:14,51,91,480,1211,1251,1280,1288`
  (mtime-walk prune, ls-files excludes); and selftest fixtures
  `:2098,2104,2210` (writes a decoy `watchdog-secret` log inside a fixture
  repo to prove the census never opens it). Hygiene-lane exclusion, not a
  liveness reader.
- kama-shokunin: zero `watchdog` hits in `tools/` or `corpus/knowledge/`
  (grep exit 1). The kama "watchdog"-adjacent tools are engine probes
  (`kama-probe.sh`, `kama-ollama-evidence.py`, `kama-llamacpp-live.py`) for
  model-server health, unrelated to the fleet driver log.

Negative-grammar sweep, all four lanes: grep for
`inline\.sh|shokunin-watchdog|hyaku-inline|lane-dead-no-report|launch-fail`
over each sibling `tools/` + `corpus/knowledge/` matched only
kumitate `round-close-gate.md` / `kimi-skills-plugins.md` (citations above)
and kama `kama-context-capacity.py:313` / `kama-llamacpp-live.py:2240`
(string literal `launch-failed:{exc}` in Python exception records — engine
launch failure, hyphenated, no relation to the driver `launch-fail` line
shape). tsukuroi and souji: zero matches.

## Question 2 — seat-output vote binder in siblings

Reference binder (frozen C2 tool `tools/mori-vote-bind.py`): accepts
plain-text vote lines and JSON string-scalar-wrapped votes from seat outputs,
emits `TALLY rows= agree= double= single= zero= dissent= voters=
bound_voters=`.

Per-lane result — no sibling holds a seat-output vote binder:

- kumitate: grep `\bvote\b|voter` over `tools/` (absent) and
  `corpus/knowledge/` → zero hits.
- tsukuroi: the RECHECK-term hits are a different object —
  `tools/check-recheck-commands.py` (read of lines 1-30) is a
  recheck-*procedure* gate that scans knowledge `recheck:` lines for forbidden
  binaries (pacman-class) at an immutable revision; it never parses seat
  outputs or wave vote lines. `tsukuroi-census.sh` / `check-path-reconciliation.py`
  matched the field-name sweep (`agree=`/`double=`) only as generic census
  text, not a vote schema.
- souji: quarantine/census scripts matched the RECHECK|ENTAIL|tally sweep on
  unrelated hygiene text; no ENTAIL/RECHECK tokens at all in the sampled
  `impl-47.sh`, `impl-37.sh`, `cand-a1-quarantine.sh` (grep exit 1). No binder.
- kama: `tools/echo-recheck.py` (read of lines 1-40) re-runs the round-27
  llama-server echo probe and compares engine receipts — engine-side, not
  seat-output binding. `tools/instrument-agreement.py:7,89-169` emits
  `IA runs=N agree=A disagree=D digest=<sha256>` — instrument agreement across
  engine runs, a distinct schema from the seat-vote `TALLY rows=` shape.
  `tools/round44-verdict-ledger-audit.py:51,252` emits
  `rows=R valid=V missing=M bad=B agree=a overclaim=o underclaim=u` over
  kama's own verdict ledger, again not seat-output vote lines. No
  `bound_voters` / `seat-output` tokens anywhere in the four lanes' tools or
  knowledge (grep exit 1 each).

## Question 3 — sibling `corpus/SOURCES.md` registry duplicate-url scan

All four sibling registries exist and were grepped read-only.

- `rfc-editor.org/rfc8259` row: PRESENT in kama-shokunin only —
  `kama-shokunin/corpus/SOURCES.md:148` row S136 and `:151` row S139
  ("supersedes S136"), both titled "RFC 8259 — The JavaScript Object Notation
  (JSON) Data Interchange Format — https://www.rfc-editor.org/rfc/rfc8259.txt",
  both pinned "raw sha256
  61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7",
  used-by kama's echo-discrimination knowledge (S136 →
  `corpus/knowledge/echo-discriminating-counters.md`). That sha256 is
  byte-identical to the one pinned in mori's new S545
  (`mori-shokunin/corpus/SOURCES.md:325`). kumitate has a related-but-distinct
  row S104 (RFC 8785 JCS, whose quote mentions RFC 8259 by reference; different
  document and URL). tsukuroi and souji registries: zero `rfc8259|rfc-editor`
  hits (grep exit 1). Mori's own registry had no prior 8259 row (grep `8259`
  over `mori-shokunin/corpus/SOURCES.md` → only line 325, S545).
- Own-work row for the fleet driver scripts (`scripts/hyaku/inline.sh`,
  `scripts/shokunin-watchdog.sh`): ABSENT in all four sibling registries
  (grep `shokunin-watchdog|inline\.sh` over each sibling `corpus/SOURCES.md`
  → no output, exit 1 each). Nearby but distinct kumitate own-work rows cite
  other fleet files: S058 (`.ufo/waves/hyaku/PHASE4.md`), S061/S090
  (`scripts/hyaku/lane-addendum.md`), S038 (`scripts/ufo-swarm-wave.mjs` in a
  pinned upstream clone). Mori's S544
  (`mori-shokunin/corpus/SOURCES.md:324`) is the first registry row, in any
  of the five lanes' registries, citing the two driver writer scripts.

Assessment of the duplicate-url class: per-lane `SOURCES.md` registries are
independent corpora — each lane mines sources for its own knowledge and
tools — so kama's S136/S139 does not collide with mori's S545 inside mori's
registry, and the byte-identical sha256 means no digest conflict. The overlap
is informational: the same pinned RFC 8259 bytes now ground two lane
knowledges (kama: llama-server decoded-echo discrimination; mori: dual-shape
seat-output vote binding). No sibling registry row needed re-pinning or
superseding as a consequence of round 56.

## Evidence log (commands, observed output, exit codes)

All commands run from the fleet root with absolute paths; read-only.

```
$ ls -d /home/vgpnk/Projects/shokunin/*/        # lane discovery
…/kumitate-shokunin/ …/kama-shokunin/ …/mori-shokunin/ …/souji-shokunin/
…/tsukuroi-shokunin/ …                        exit 0

$ ls /home/vgpnk/Projects/shokunin/kumitate-shokunin/tools/
ls: cannot access '…/kumitate-shokunin/tools/': No such file or directory   exit 2

$ for lane in kumitate tsukuroi souji kama; do
    grep -rl watchdog.log <lane>/tools/ <lane>/corpus/knowledge/; done
kumitate: corpus/knowledge/ops-watchers.md
souji:    tools/{souji-verify.sh, souji-census.sh, souji-vault-verify.sh,
          souji-quarantine.sh, souji-seat-audit.py, souji-cert-evidence.py,
          impl-*.sh, souji-census.impl-*.sh, souji-vault-verify.impl-*.sh,
          souji-verify.impl-*.sh, souji-quarantine.impl-*.sh,
          souji-verify.spec.md, souji-verify.r9-s18.sh,
          souji-vault-verify.r9-s18.sh, souji-quarantine.r9-s18.sh,
          souji-guard.r9-s18.sh, qrun-11.sh, cand-*-*.sh}   (all exclusion-only,
          confirmed at souji-verify.sh:35,546,759 and souji-census.sh:14,51,91,
          480,1211,1251,1280,1288,2098,2104,2210)
tsukuroi: (none)   kama: (none)                          exit 0/1 per lane

$ for lane in kumitate tsukuroi souji kama; do
    grep -rlE "inline\.sh|shokunin-watchdog|hyaku-inline|lane-dead-no-report|
               launch-fail" <lane>/tools/ <lane>/corpus/knowledge/; done
kumitate: corpus/knowledge/round-close-gate.md, corpus/knowledge/kimi-skills-plugins.md
kama:     tools/kama-context-capacity.py (line 313), tools/kama-llamacpp-live.py (line 2240)
tsukuroi: (none)   souji: (none)                         exit 0/1 per lane

$ for lane in kumitate tsukuroi souji kama; do
    grep -rliE "\bvote\b|voter" <lane>/tools/ <lane>/corpus/knowledge/; done
kama: corpus/knowledge/endpoint-identity.md              # unrelated (endpoint identity)
all other lanes: (none)                                  exit 0/1 per lane

$ for lane in kumitate tsukuroi souji kama; do
    grep -rlE "voted=|double=|bound_voters|agree=|seat-output|seat_output" \
      <lane>/tools/ <lane>/corpus/knowledge/; done
tsukuroi: tools/tsukuroi-census.sh, tools/check-path-reconciliation.py
souji:    tools/impl-47.sh, tools/impl-37.sh
kama:     tools/instrument-agreement.py, round44-verdict-ledger-audit.py,
          round45-claim-outcome-audit.py, round45-claim-outcome-audit-v2.py,
          manifest-crosscheck.py
(all inspected: census text / engine-side IA runs= / verdict-ledger rows=;
 none is a seat-output vote binder)                       exit 0/1 per lane

$ for lane in kumitate tsukuroi souji kama; do
    grep -niE "rfc.?8259|rfc-editor" <lane>/corpus/SOURCES.md; done
kama: line 148 (S136), line 151 (S139 supersedes S136), plus a 2026-10-23
      search-log note at line 289; kumitate: lines 115 (S102, RFC 3339),
      117 (S104, RFC 8785 — different document)
tsukuroi/souji: (none)                                   exit 0/1 per lane

$ for lane in kumitate tsukuroi souji kama; do
    grep -nE "shokunin-watchdog|inline\.sh" <lane>/corpus/SOURCES.md; done
(all four lanes: no output)                                exit 1

$ grep -n 8259 /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
325:| S545 | RFC 8259 … sha256 61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7 …   exit 0
```

Registry sizes at read time: kama `corpus/SOURCES.md` 611 lines; mori
`corpus/SOURCES.md` 391 lines. Row pointers:
`kama-shokunin/corpus/SOURCES.md:148` (S136), `:151` (S139);
`mori-shokunin/corpus/SOURCES.md:324` (S544), `:325` (S545);
`kumitate-shokunin/corpus/knowledge/round-close-gate.md:68,94,122`;
`kumitate-shokunin/corpus/knowledge/ops-watchers.md:70`;
`souji-shokunin/tools/souji-verify.sh:35,546,759`;
`souji-shokunin/tools/souji-census.sh:14,51,91,480,1211,1251,1280,1288,2098,2104,2210`;
`tsukuroi-shokunin/tools/check-recheck-commands.py:1-30`;
`kama-shokunin/tools/echo-recheck.py:1-40`;
`kama-shokunin/tools/instrument-agreement.py:7,89-169`;
`kama-shokunin/tools/round44-verdict-ledger-audit.py:51,252`;
`tsukuroi-shokunin/corpus/knowledge/oom-event-plane.md:62,119`;
`tsukuroi-shokunin/corpus/knowledge/degraded-triage-r4.md:478,486`;
`tsukuroi-shokunin/corpus/knowledge/adjacency-handoffs-fleet-r1.md:107`;
`kama-shokunin/tools/kama-context-capacity.py:313`;
`kama-shokunin/tools/kama-llamacpp-live.py:2240`.

## Limits

- Sibling scope limited to the four named lanes' `tools/`, `corpus/knowledge/`,
  and `corpus/SOURCES.md`, per the seat spec. Sibling `.ufo/waves/` scratch and
  lanes outside the named four were not scanned.
- The souji exclusion finding rests on grep of every `watchdog.log`-matching
  file plus spot reads of the two main scripts; individual `impl-*.sh` /
  `cand-*.sh` files were grep-matched but not opened line by line (their
  matches sit beside the same prune/exclude patterns in souji-verify.spec.md).
  Confidence still high: souji's lane charter is read-only hygiene with
  `.ufo/watchdog.log` on its never-traverse list by design.
- mori's own S544/S545 text was read from the working-tree registry at the
  freeze tip; no attempt made to re-verify the pinned sha256 values against
  the source bytes (other seats own that).

## Findings

- LOW — duplicate-url class, informational only: `kama-shokunin/corpus/SOURCES.md:148` (S136) and `:151` (S139) already register `https://www.rfc-editor.org/rfc/rfc8259.txt` with raw sha256 `61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7`, byte-identical to mori's new S545 (`mori-shokunin/corpus/SOURCES.md:325`). Cross-lane registries are independent, so no mori-registry duplicate and no re-pin consequence; noted for round-57 awareness that two lanes now ground knowledge on the same pinned RFC 8259 bytes.
- LOW — absence confirmed (novelty of C1 surface): no sibling lane holds a driver-liveness reader of `.ufo/watchdog.log`; the only sibling citations of the writer script `scripts/shokunin-watchdog.sh` are semantic (kumitate `corpus/knowledge/round-close-gate.md:68,94,122`, `kimi-skills-plugins.md:116,124`), and souji's tools reference the log only to exclude/prune it (`souji-shokunin/tools/souji-verify.sh:35,546,759`, `souji-census.sh:14,51,91,480,1211,1251,1280,1288`).
- LOW — absence confirmed (novelty of C2 surface): no sibling lane holds a seat-output vote binder; the nearest shapes are kama's engine-side `IA runs=N agree=A disagree=D` (`kama-shokunin/tools/instrument-agreement.py:7`) and verdict-ledger `rows=R valid=V …` (`kama-shokunin/tools/round44-verdict-ledger-audit.py:51`), and tsukuroi's recheck-procedure gate (`tsukuroi-shokunin/tools/check-recheck-commands.py:1-30`) — none binds seat-output vote lines.
- LOW — no sibling own-work registry row for the fleet driver scripts: zero rows citing `scripts/hyaku/inline.sh` or `scripts/shokunin-watchdog.sh` in any of the four sibling `corpus/SOURCES.md` files (grep exit 1); mori S544 (`mori-shokunin/corpus/SOURCES.md:324`) is the first such row across the five lanes scanned.
