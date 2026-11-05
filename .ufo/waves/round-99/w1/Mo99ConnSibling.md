# Mo99ConnSibling — sibling-overlap scan, round 99 w1 (connector, report only)

Scope: read-only scan of sibling lane repos under `/home/vgpnk/Projects/shokunin/` for tools/knowledge
that parse sudo journal lines, `COMMAND=`, `(command continued)`, sysctl writes or user-namespace
limits; classification against the three r99 defect classes (D1 POSIX splitter on sudo quoting,
D2 dropped `(command continued)` lines, D3 regex firing inside quotes/comments). No edits outside
this report; scratch `/fast/scratch/hyaku/mori-r99/Mo99ConnSibling` (removed). No tool installs
(none needed). Paths below are relative to `/home/vgpnk/Projects/shokunin/`.

## Method and coverage

Grep-tool searches, `gitignore: false` (first pass with gitignore on returned zero hits because the
fleet-root `.gitignore` excludes the lane repos — a false zero, re-run and discarded), case-insensitive,
patterns: `COMMAND=`, `command continued`, `max_user_namespaces`, `sysctl`, `/proc/sys`, `sudo\[`,
`SYSCTL_WRITE`, `syslog_maxlen|eventlog\.c|lbuf\.c`, `SysctlNestedShell`, `journalctl` (tools/ and
corpus/knowledge/ per lane). 20 sibling lanes matched by `*-shokunin`, plus `kumitate-shokinin`
(misspelled dir, does not match the glob) checked separately: **zero hits on every pattern**.
`SYSCTL_WRITE` outside mori: **zero matches** in all 21 sibling repos — the output token exists only
in mori's tool/counter fixtures. Sudo eventlog/lbuf grammar knowledge (`eventlog.c`, `lbuf.c`,
`syslog_maxlen`): zero outside mori. So no sibling parses sudo's `COMMAND=` rendering; C1's grammar
surface is uncontested.

## Hits and classification

1. **tsukuroi — `tools/check-recheck-commands.py` (`systemctl_violations`/`invocations`, bounded shell
   parser `segments`/`words`/`command_word`/`simple_commands`).** Input is tsukuroi's own `$ ` exec-log
   lines, not sudo journal output → D1/D2 not applicable. D3: comments dropped before tokenization and
   quoted text kept as one token (`falsify/SysctlEchoInert.md:14-25`, `SysctlNestedShell.md:9`,
   `WrapperSudoLong.md:27` G2 "words keeps quoted text as one token") — the same POSIX reading mori r99
   adopts, so no quote/comment defect. Documented residuals are tsukuroi-owned: depth>4, exact `-c`
   token only (`sudo bash -lc` payload invisible, G3), `sudo -s/-i` quoted payloads invisible (G2),
   `env -S`, `time` keyword (`lessons/round-20.md:40,42` R20-SYSTEMCTL/R20-BUSYBOX-PARSER; QUALITY 36-37).
   **Adjacent** — same log-grammar family, disjoint producer (lane exec log vs sudo journal); r98
   connector already recorded "tsukuroi should know the latter exists so a future incident is not
   double-claimed" (`mori-shokunin/.ufo/waves/round-98/w1/Mo98ConnSibling.md:107-110`); SYSCTL_WRITE
   zero-hit confirms no double claim today.
2. **tsukuroi — r24 archival captures `round-24/capture/l1-3/` and `l1-4/` `capture.txt:232`, plus
   `round-24/w1/ExecRecapture/cap{,2,3}/capture.txt` and `cap-head` `:239-243`:** capture pipeline is
   `journalctl _COMM=sudo … | grep -E "COMMAND=/usr/bin/(pacman|paccache|makepkg)" | … | cut -c1-220`.
   This is the **same defect class as mori's r98 capture mistake** (mori `contract.md:60-61`: r98 capture
   "filtered on COMMAND= and lost one `(command continued)` line"): the `COMMAND=` filter drops
   continuation lines, and `cut -c1-220` truncates argv mid-token (visible: `zcode-3.16.2-1-x8`,
   `tizen-sdb-2.3.2-3-x86_`, `openssl-1.0-1.0.2.u-`). The earlier keyword-filtered `l1`/`l1-2` captures
   kept the continuations (`capture/l1/capture.txt:168-174` — `pacman` appears inside continuation
   paths). **Overlap** (evidence the D2 capture defect recurs outside mori; cite, and route capture
   hygiene to tsukuroi). Impact today: archival only — tsukuroi counts/cites these lines, never
   classifies argv; cut paths are unquoted so mori's own tool would read them without unparsed lines and
   report n=0 writes (pacman is not a write in mori's grammar); a cut inside a quoted arg would fail
   closed exit 2, which is the correct behavior.
3. **mado — raw sudo journal captures, r35** (`round-35/scratch-evidence/RevEntryR14/probe-log.md:101-103`,
   `RevQuoteS204/verify.log:64`, `evidence.txt:165-167`, `SentProvenance/S204.1924b.txt:18-27`,
   `round-41/w1/ExecJournalHistory/finding.md:92`): content-key greps (`grep -i hypridle`) counting
   occurrences; commands short, no continuations involved, no argv parsing → none of D1/D2/D3 fired.
   mado itself discloses the adjacent filter-pollution hazard (own probes counted by later greps,
   `RevQuoteS204.md:117,272-274`) — the same "filter on a search key" family mori's QUALITY 211
   (2330-2335) already generalizes. **Adjacent / none** (mori reports, never absorbs; no route needed).
4. **mado — `tools/mado-globals.py:13-16,54-55`** (`journalctl -o short-iso` reader): unknown-format
   lines counted `ignored=`, all-ignored → `UNRECOGNIZED_FORMAT` exit 4, "never a silent NO_SESSIONS".
   **Adjacent** — design precedent for mori's r99 fail-closed `SYSCTL_WRITES_SETUP unparsed=U` exit 2
   (count + nonzero exit instead of silently reading as empty). No sudo grammar input.
5. **tsukuroi — census fail-closed postures**: `corpus/knowledge/executor-test-sufficiency.md:76-79`
   ("blocked: journalctl missing (fails closed) (exit 2, BLOCKED)", "empty journal is not a clean bill");
   the rc≥2-counted-as-zero fail-open was found and mutation-tested
   (`corpus/knowledge/memory-arm-mutants-s8.md:125-128` D9). **Adjacent** — second in-fleet precedent
   for mori's unparsed exit-2 posture; cite-able.
6. **chousa — sandbox capability reads** (`round-61/w1/CritC1Detached.md:60`, `round-62/w1/CritC1Sandbox.md:64`,
   `round-73/w1/R73S02/nsprobe-r73s02.txt:24`, `round-62/w1/CritC1Detached.md:22-23`): reads
   `max_user_namespaces=122865` as an environment capability (counter fails closed if 0; /proc/sys
   closed inside sandbox) — a consumer of the limit, not a detector of writes. **Adjacent**.
7. **kaidoku — sandbox primitive probes** (`corpus/knowledge` refs `r20` `ConnSandboxPatterns.md:26`,
   `ScoutSandboxPrimitives.md:26`, `CriticGuardSufficiency.md:25`; guards r92/r93): same capability-read
   class. **Adjacent**.
8. **kagi — `round-44/build/K44ScoutSources/S099.body:874` + `capture/S099.body` + `corpus/SOURCES.md:106`:**
   pinned copy of the fleet round-44 prompt whose §"Host incident (orchestrator, 2026-11-05)" narrates
   the same userns incident mori's tool detects — prose evidence of claim-sizing discipline, not a
   parser, no grammar surface. **None** (no route; mori's own knowledge already owns the incident facts).
9. **kengaku — `corpus/knowledge/attrib-r21.md:254-258`:** explicitly routes to mori ("mori reads
   journal/cgroup events as evidence and never owns state"), and kengaku r89's ReviewerR89a
   `0 → 15638 → 0` reset is one of the six writes mori's r99 tool reports. Routing already in place.
   **Adjacent** (corroboration loop, no action).
10. **None:** souji (guards + a pinned bwrap man page naming the sysctl, `round-34`/`census/round-34/src-S230.html:182`;
    LOG.md:2904 incident non-attribution), audio (`r64-reviewer/r64rev-formats.c:581`, `r83-boundary/r83b_run.py:46`
    read sysctls as test inputs), game-dev-3d (`reports/round-104/gate/regression.md:249` uses /proc/sys as
    an unwritable-dir gate case), game-dev-2d, kama (prose "command continued" only, `round-36/w1/out/ReviewC1Predicate/seat.log:100`),
    kake (own-unit journalctl only), tabi, tameshi (mutates tsukuroi's census, not sudo grammar), kotoba,
    kotodama, kumitate(-shokunin and -shokinin), kasegi, lore, revenger. tsukuroi's r76/78 journal-retention
    plane (`journald-retention-plane-r76.md`, `journald-path-usage-r78.md`, `tools/measure-journal-usage-r78.py`)
    and `check-journalctl-v262-corrections.py` own journald retention/field-filter semantics — retention and
    correction gates, not sudo write detection. **None**.

## Repair ownership

- **tsukuroi** owns OS state and its surfaces: the exec-log gate (`check-recheck-commands.py`), the
  census, journald retention, and its own r24 capture hygiene (finding 2 is routed there; mori reports,
  never absorbs or fixes sibling artifacts).
- **operator** owns sysctl policy: the 2026-11-05 incident, limit restoration, persistence decisions.
- **mori** owns detection/report of sudo-journal kernel-tunable writes (`SYSCTL_WRITE`/`SYSCTL_WRITES`,
  mori-only token) and never remediates.

## Proposed move (report-only; no r99 artifact changes)

Cite, at the next revision of `corpus/knowledge/sudo-log-grammar-r99.md` (frozen for r99 by the
contract), two cross-lane facts this scan grounds: (a) the dropped-continuation capture defect recurs
verbatim in tsukuroi r24 (`l1-3`/`l1-4` `grep COMMAND=` + `cut -c1-220` vs the keyword-filtered `l1`/
`l1-2` that kept continuations) — an independent-lane replication of QUALITY 211's rule, strengthening
it from a mori-local lesson to a fleet convention; (b) mori's fail-closed unreadable-input posture has
in-fleet precedents (mado-globals `ignored=`/`UNRECOGNIZED_FORMAT` exit 4; tsukuroi census BLOCKED exit 2
with the D9 fail-open mutant fixed; chousa r62 sandbox fail-closed on `max_user_namespaces=0`), so the
r99 `unparsed=U` exit-2 design is a convention, not an idiosyncrasy. Affected axes: calibration (C2) —
sharper, cross-lane-grounded evidence pointers at next revision; operability (C1) unharmed (no behavior
change; C1's grammar uncontested by any sibling). Route to tsukuroi, in their lane's channel, the
finding-2 observation. Risks: none to r99 claims — report-only; the citation must wait for the next
round's knowledge edit since the r99 file is frozen; a secondhand QUALITY blob copy in chousa
(`round-80/w1/R80ConnectorA/tsukuroi--corpus__QUALITY.md.blob`) must not be cited as tsukuroi's row
(it is a pinned copy; cite tsukuroi's own corpus).

## Verification

- `SYSCTL_WRITE` over all lanes, gitignore off: only mori files (tool, counters, wave reports) — grep
  output above, 34 files, every non-mori path absent.
- `command continued`: only prose/captures (chousa seat.log, mado SrcLuaRules, tsukuroi r24 captures,
  mori self) — no sibling parser.
- `syslog_maxlen|eventlog\.c|lbuf\.c`: only mori contract/dispatch/candidate/SOURCES/knowledge.
- `kumitate-shokinin` (not matched by the `*-shokunin` glob): `COMMAND=|command continued|
  max_user_namespaces|sysctl|journalctl|sudo\[|/proc/sys` → No matches found.
- First-pass gitignore-on zero-hit verified as a tool artifact (direct path grep succeeded where the
  glob path failed), re-run with gitignore off.
- Unrun: live `journalctl` re-reads, any sibling tool execution, and any check beyond the read-only
  greps and file reads cited above.
