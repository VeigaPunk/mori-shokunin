# Round 28, wave 2 — ReopenS150 (seat MoriR28.ReopenS150)

**Verdict: partial** — attacked row S150 (supersedes S129) at
`f2de0eedcd60d2e354da75265ea6122bc3896073`. The row itself, its Gate line, its supersession prefix, its
used-by citations and the `readers_left` move all hold against re-fetched bytes; but the wave-1
SupersedeS129 report flagged `corpus/knowledge/oom-victim-selection-r27.md:200` as surviving defective
wording, and that line is unchanged at this revision: it still says the `systemd.exec` default
"describes the system manager", which contradicts the row's established "the page names no manager
type".

Attack revision read as committed bytes only (`git show f2de0eed:<path>`). No lane writes except this
file. Fetches re-opened 2026-10-22T18:54:08Z (`date -u +%FT%TZ`).

## Check 1 — Gate line (`corpus/lessons/round-28.md:69`): holds

Committed line: `| S150 | https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.exec.xml
(with …/man/systemd-system.conf.xml) | 2026-10-22T17:58:56Z | 44b89bff…d844 | systemd.exec.xml:1299-1300
"If not specified, defaults to the OOM score adjustment level of the service manager itself, which is
normally at 0." (20 words) | admit, A, mined (MoriR28.SupersedeS129) |`

- My fetch now: `curl -sS -L` → exec.xml HTTP 200, 343,315 B, sha256
  `44b89bffce737aff803966c207329e9fe2d28ad07709a4bb8e0edf6a4ec0d844` — **equal to the Gate sha256, no
  drift**; conf.xml HTTP 200, 49,977 B, sha256
  `161359987affadc8e4a533bc9117bbbd98053cb807808b623eb24794b49b0c58` — equal to the row's second digest.
- Quote verbatim in fetched exec.xml:1299-1300, whitespace-folded across the wrap ("itself,\n which").
  20 words ≤ 25.

## Check 2 — every S150 cell against the bytes: holds

Row at committed `corpus/SOURCES.md:155`; 13 fields, `teaches` opens exactly `supersedes S129 — `.

- source/URLs: both HTTP 200 re-fetched (above); `git ls-remote` gives `refs/tags/v262` =
  `1f7dffaf714cc4488159c498b7a17cf34c5a96d5`, `v262^{}` = `8cc40e0c5e9234bf45084751ac53b1fbfe70b492` —
  matches the anchor's recorded tag object/commit.
- Anchor lines all located in fetched bytes: exec.xml :1293 `<term><varname>OOMScoreAdjust=`, :1295-1296
  "executed processes", :1296-1297 "-1000 … 1000", :1299-1300 unset default, :1302-1305 OOMPolicy
  cross-ref, :4890-4891 "problems during process invocation", :4934-4938 `EXIT_OOM_ADJUST` 206;
  conf.xml :301 term, :303-305 "defaults to unset … inherit the service manager's OOM score adjustment
  value", :305-307 unprivileged user → "plus 100", :307-308 "may be used to pick a global default",
  :310-311 "has no effect on the OOM score adjustment value of the service manager process itself",
  :313 `<xi:include … v250`, :49-55 system.conf vs user.conf.
- "names no manager type": `grep -n 'system manager'` in exec.xml hits only :3367, :4185, :4208 — none
  in the cited spans; `grep -c 'DefaultOOMScoreAdjust' exec.xml` = 0, supporting the teaches' [INFERENCE]
  that the two pages do not reconcile each other.
- teaches: `mined`, non-empty `used-by`, differs from S129's cell after the prefix — the counter itself
  counts it (below).

## Check 3 — the named defect actually fixed, not copied: holds

Wave-1 `w1/SupersedeS129.md:136-138` names the defect: M2's unflagged derivation ("so user units inherit
manager+100 unless they set the value"), L1 ("normally 0 for the system manager"), L2 ("the setting
never changes the manager's own score" ambiguous between per-unit and manager-wide). S129's teaches is
unchanged in the registry (QUALITY 81: `changed=0`, row intact). S150's teaches is rewritten, not copied:
the derivation is replaced by the literal byte claims plus an explicit `[INFERENCE]` sentence ("What a
unit of a user manager inherits when it sets no `OOMScoreAdjust=` is not stated by either page"); "the
page names no manager type" replaces L1; "`DefaultOOMScoreAdjust=` leaves the manager process's own
value unchanged" resolves L2. Every rewritten claim verified verbatim in §2.

## Check 4 — used-by paths cite S150: holds

`used-by`: `corpus/knowledge/oom-victim-selection-r27.md, SKILL.md, PROVINCE.md, corpus/README.md,
corpus/lessons/round-28.md`. Word-citations confirmed at the rev: oom-victim-selection :1 (source line),
:72 (heading), :78 (manual-sentence cites `systemd-system.conf.xml:305-306` and `systemd.exec.xml:1299-1300`
as S150); SKILL.md:722; PROVINCE.md:378; README.md:36; lesson:69. `git grep -n 'S129'` over
SKILL.md/PROVINCE.md/README.md/corpus/knowledge at the rev yields no `\bS129\b` citation — only the seat
name "ReopenS129" (no word boundary). `bash count-c1.sh f2de0eed` prints `superseding=7/8
ids=S096,S097,S127,S128,S129,S131,S140`, **no `fail S150` line**, `readers_left=0`; C1=unmet solely for
`fail S147 row_absent` (S101's row, outside this seat's scope — note S147 is also absent from the Gate
table at :65-71).

## Check 5 — no live reader still states the defective wording (QUALITY 77): PARTIAL

Wave-1's sweep list (`w1/SupersedeS129.md:140-161`) against the committed diff `6ebd518f..f2de0eed`:

- Citation moves done: every live citation now names S150 (check 4).
- Defensible residues now grounded to code/host, not the manual: SKILL.md:730 "(manager 100, children
  100 more)" cites `main.c:3063` + `user@.service.in:35`; README.md:36 / PROVINCE.md:375-376 trace the
  fleet's 200 to "systemd's per-user manager" (S130 code + host read, no manual reading claimed);
  oom-victim :86-87 "inherits 200" follows the `fork`/`execve` code bullets (S148); :166 decision row is
  hedged "most likely" and grounded to Fact 3.
- **Residual defect — oom-victim-selection-r27.md:200 (unchanged at this rev; wave-1's LOW finding 199-200
  said "the prose sweep should too")**: "the `systemd.exec` default quoted at `kill-event-deep-r8.md:142`
  describes the system manager". S150 establishes the page names no manager type (`exec.xml` manager-type
  grep above); this line repeats the L1-class misreading in a live reader that now cites S150 at :78.

## Findings

- **LOW-MEDIUM — `corpus/knowledge/oom-victim-selection-r27.md:200` retains the misreading S150
  corrects.** Contradicts the live reader's own :78 and S150's "names no manager type". Flagged for the
  sweep by the drafting seat and left standing at the attack revision. Not a counter break
  (`readers_left` counts id citations, not wording).

## Residual risk / gaps

- I did not re-verify S129's first-published hash (`2c3141c9…b849`, report claim); the counter's
  `changed=0` already establishes no in-place edit.
- The two QUALITY-77 note lines at `harness-job-capacity-r25.md:328` and `system-pressure-r24.md:239`
  name unrelated sweeps, not S129's wording.
- S130's scope cell still says "the manual sentence is row S129" — immutable under QUALITY 81 per the
  wave-1 report; SOURCES.md is not in the counter's READERS set.

## Bounds

- Wrote only this file. Lane read via `git show`/`git grep`/`git diff`/`git ls-remote` only; no
  add/commit/stash/checkout; no jj command; no unit, process, /etc, harness or MCP file touched.
- Fetches: `curl -sS -L`, HTTP 200, no challenge; digests recorded above; 2026-10-22T18:54:08Z.
- Tools: curl, sha256sum, git (read-only), grep/sed; installs/upgrades: none (pacman paused; not needed).
- No privacy-bound value (uid, pid, user@ unit, journal text, /etc/default/earlyoom, prefer/avoid
  expressions, OMP settings) appears above; quoted prose "100 + 100" is lane knowledge text.

Report: `.ufo/waves/round-28/w2/ReopenS150.md`
