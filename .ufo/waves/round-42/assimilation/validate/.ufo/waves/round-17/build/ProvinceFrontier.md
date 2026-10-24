# ProvinceFrontier — round 17 documentation anchors for C1 and C2

Seat: `MoriR17.ProvinceFrontier-5` (leaf; no subagent dispatch). Date: 2026-10-20.
Lane repo: `/home/vgpnk/Projects/shokunin/mori-shokunin` (branch `master`, tip `24526ea`,
jj-colocated). No lane file was edited; the only write is this report. No tool was installed
or updated. No VCS mutation, no `journalctl`, no gate or selftest was run.

## Verdict

C1 lands as a new Core surface (`PROVINCE.md` after line 28; README coverage row after line 41;
optional new FR row after `PROVINCE.md:57` / `README.md:345`). C2 amends the existing `Lane
silence` surface (`PROVINCE.md:10,28`) and touches six census sites plus the finding-id and
severity registries. Two stale status sites are confirmed and quoted verbatim: `PROVINCE.md:25`
`(round-16 build; verification pending)` and
`corpus/knowledge/journal-cursor-window-r16.md:2` `Host systemd version was not verified; no
behaviour is claimed for any host version.` A third stale host-version cell is
`corpus/README.md:41` (`host systemd 261.2-1`); measured host is now `262-1` with a boot after
the upgrade. Draft appended supersede notes are in §3; they must be appended, never rewrite
history (`corpus/lessons/round-16-verifier-spotcheck.md:223` "Do not rewrite history.").

## 0. Observed evidence (commands and exit codes)

| # | Read / command | Result |
|---|---|---|
| O1 | `read PROVINCE.md` | 94 lines; Core 20-40, Frontier 42-57, Adjacent 59-90, Corrections 92-94 |
| O2 | `read corpus/README.md` | 349 lines; Coverage map 3-41, Known gaps 43-327, Frontier table 328-345, closing note 347-349 |
| O3 | `read corpus/knowledge/journal-cursor-window-r16.md` | 136 lines; `source:` line 1, `verified-at:` line 2, `recheck:` line 3 |
| O4 | `systemctl --version \| awk 'NR==1'` | `systemd 262 (262-1-arch)` rc0 |
| O5 | `pacman -Q systemd` | `systemd 262-1` rc0 (query only; no pacman transaction) |
| O6 | `grep -n systemd /var/log/pacman.log` | `:2487 systemd-libs 261.2-1 -> 262-1` (09:16:27), `:2531 systemd 261.2-1 -> 262-1` (09:16:28), `:2805 lib32-systemd`, `:2922 systemd-sysvcompat` (all 2026-10-20 -0300) |
| O7 | `awk '/^btime /{print $2}' /proc/stat` | `1792501016` = `2026-10-20T09:56:56-03:00`; upgrade epoch `1792498588` = 09:16:28, i.e. boot 40m28s after the upgrade |
| O8 | `git rev-parse --short=7 HEAD` | `24526ea` |
| O9 | `git symbolic-ref -q HEAD` | `refs/heads/master` rc0 |
| O10 | `git symbolic-ref -q refs/remotes/origin/HEAD` | `refs/remotes/origin/master` rc0 |
| O11 | `git for-each-ref --format='%(refname)' refs/heads` | `refs/heads/master` only |
| O12 | `git rev-parse --short=7 refs/heads/master` | `24526ea` (same as HEAD) |
| O13 | `git merge-base --is-ancestor HEAD refs/heads/master` | rc0 (HEAD is an ancestor of the branch; `HEAD_BRANCH_MISMATCH` would not fire today) |
| O14 | `sha256sum tools/mori-census.sh` vs `git show 24526ea:tools/mori-census.sh \| sha256sum` | `f1f8d1b62bb6…` both; working tree equals tip; `VERSION=census-r6` (`tools/mori-census.sh:268`) |
| O15 | `jq -c '.summary' .ufo/waves/round-16/evidence/capability-{before,after}/run-manifest.json` | before `{"capability_absent":64,"matched":0,"mismatched":0,"total":64}`; after `{"capability_absent":0,"matched":64,"mismatched":0,"total":64}`, `exit_code:0`, `verdict:"ok"`, gate `tools/mori-round16-regressions.py` sha256 `e70ed67c…`, tool sha256 `d61e0d22…`, `git.head 87a57c13…` |
| O16 | `sha256sum tools/mori-journal-window.py` vs `git show 87a57c1:…` and `git show 24526ea:…` | `d61e0d22…` in all three (verified tool bytes are current tool bytes) |
| O17 | `jq` on `.ufo/waves/round-16/evidence/live-window-manifest.json` | `observed_at 2026-10-20T09:12:11.722119+00:00`, head `87a57c13`, both scopes `MORI_JOURNAL_WINDOW_OK`, `records_after_anchor=0`, all four `positive_*=0` |
| O18 | `jq -r '.stdout' live-window-user.json \| jq` | confirms `finding_id MORI_JOURNAL_WINDOW_OK`, `records_after_anchor 0`, scope `user` |
| O19 | `.ufo/waves/round-16/runtime-versions.json` | `journalctl --version` = `systemd 261 (261.2-1-arch)` exit 0; Python 3.14.7; node v26.12.0 |
| O20 | `ls tools/mori-seat-terminal.py tools/mori-round17-seat-regressions.py tools/mori-round17-jj-regressions.py` | rc2, all three absent at this snapshot (C1/C2 not yet buildable) |
| O21 | `grep -n "verification pending" PROVINCE.md corpus/README.md` | one match, `PROVINCE.md:25` only |

## 1. C1 — seat terminal status: exact lines to advance or add

Contract interface: `.ufo/waves/round-17/contract.md:9-15` (claim), `:24-77` (tool contract,
fixtures), `:78-79` (fixture pack + gate). C1 is a *new* observability surface: a grep of
`PROVINCE.md`, `corpus/README.md` and `corpus/knowledge/*.md` for seat/transcript/OMP coverage
found no existing note or bullet (the "seat" hits are audit-seat prose, e.g.
`corpus/knowledge/audit-r11.md:3`).

| Target `file:line` | Current anchor | Action |
|---|---|---|
| `PROVINCE.md:10` | end of the **Owns (read-only probes)** sentence: `…; lane silence grading (silent / progressing / progressing-weak).` | Append one item before the period: seat terminal-status classification of OMP subagent transcripts (read-only, field-limited, detection only). This keeps the owned-surface list complete; line 9 already carries the journal window. |
| `PROVINCE.md:28` | last Core bullet, `- **Lane silence** — SURFACE lane.<id> rows…`; line 29 is blank, line 30 begins the Round-15 prose | Insert a new Core bullet **after line 28**: `- **Seat terminal status** — tools/mori-seat-terminal.py …` (draft in §1.1). Do not place it inside the journal bullets 24-25; it is a fleet-liveness surface parallel to lane silence. |
| `PROVINCE.md:40` | last Round-16 prose paragraph (`Round-16 C1 advances FR11 only…`) | Append a Round-17 paragraph after line 40 (before blank line 41 / `## Frontier` line 42): C1 advances the owned coverage axis for the terminal-record classes, with the contract's limits. |
| `PROVINCE.md:57` | `- **FR14 — Agent-workload telemetry** (art F6) … Mori is consume-only; telemetry emission belongs to the emitting lanes and orchestration.` | Either extend FR14 with a consume-side clause, or insert a **new FR15** after line 57 for the residual boundaries (§1.2). Do not claim FR14 advancement from a transcript-only read. |
| `PROVINCE.md:15` | Refuses: `…credential material (→ kagi).` | C1 respects this by never reading `credential_pin`/`session_init`/`custom` records (contract `:35-37`). State this in the new Core bullet; no edit to line 15 itself is required. |
| `PROVINCE.md:16` | `**Detection and report only — never remediation.**` | Binding for C1: never resume, reroute or edit a transcript. Restate in the bullet. |
| `PROVINCE.md:65` | Adjacent kumitate row: `Owns OMP task/hub orchestration and wave plan/run/record/collect semantics…` | Add a boundary clause (new Adjacent bullet after line 90, before `## Corrections` line 92): transcript *artifact* classification is mori's report-only read; dispatch, resume and re-routing stay kumitate's. Alternatively extend this row's Boundary cell. |
| `PROVINCE.md:68` | Adjacent kagi row: `Owns secrets…; mori never reads or reports credential material.` | Extend the same new Adjacent bullet: `credential_pin` records are skipped unread and never emitted; no errorMessage text, content or usage leaves the tool. |
| `corpus/README.md:41` | last Coverage-map row (`knowledge/journal-cursor-window-r16.md`); line 42 blank; line 43 `## Known gaps` | Insert one C1 note row after line 41. Proposed note path `corpus/knowledge/seat-terminal-status-r17.md`; Holds cell = the seven classes, per-prefix and per-provider/model tallies, exit contract, limits; Sources cell must cite registered S-rows. |
| `corpus/README.md:345` | last Frontier row, FR14 | If §1.2's FR15 is adopted, insert the matching README row after line 345 (line 346 blank, line 347 `## Known gaps — round-12 note`). Keep the two registries in sync (`PROVINCE.md:57` and `README.md:345`). |
| `corpus/README.md:43,347-349` | Known gaps + closing policy line | No C1 bullet in Known gaps. Line 349 binds: "Open items now live in `## Frontier`; the historical list above is unchanged." |
| `corpus/SOURCES.md:46,48` | last row S040; `## Paths` at line 48 | The C1/C2 note rows' Sources cells cannot cite S041+ until the registry seat admits them. S041-S048 are not registered rows at this snapshot; the r17 coverage row must not claim them. |

### 1.1 Draft Core bullet (append after `PROVINCE.md:28`)

```markdown
- **Seat terminal status** — explicit read-only probe `tools/mori-seat-terminal.py --sessions-dir DIR`
  (round-17 C1). Classifies each OMP seat transcript by its last `message` record inside a bounded
  tail read: `completed` / `aborted` / `dead_rate_limit` / `dead_quota` / `dead_error_other` /
  `incomplete` / `unavailable`, tallied per seat-name prefix and per provider/model
  (`mori-seat-terminal-v1`). Reads only `type`, `message.role`, `message.stopReason`,
  `message.errorStatus`, `message.provider`, `message.model`, the contract's named error-class
  tokens and the `(type=NNNN)`/`after N retries` digits; every other record type, including
  `credential_pin`, is skipped unread, and no `errorMessage` text, content or usage is ever emitted.
  Exit 0 = scan complete, no `dead_*`; 1 = scan complete with dead seats
  (`MORI_SEAT_TERMINAL_DEAD`); 2 = setup/unavailable (`MORI_SEAT_TERMINAL_SETUP`). Limits: a
  terminal error is the last observed state, not proof the session cannot resume; dead counts are
  seats, not distinct incidents; prefixes are naming conventions, not authenticated lane
  membership. Detection and report only — never resume, reroute or edit a transcript.
```

Status wording: at this snapshot the tool and both r17 gates are absent (O20), so the bullet must
not claim a passed gate. If L1 lands the tool before integration, add the measured gate tally and
receipt path; otherwise write "round-17 build; gate pending" — and do not repeat the r16
"verification pending" mistake after the gate lands.

### 1.2 Optional Frontier row (insert after line 57; mirror after `README.md:345`)

```markdown
- **FR15 — Seat terminal-status semantics and transcript-field trust.** First evidence:
  `.ufo/waves/round-17/contract.md:24-77`; round-17 C1 receipt (when present). Boundary: the
  classifier reports the last parsed message record inside a byte-bounded tail, so a truncated or
  rotated transcript can read `unavailable`; `(type=NNNN)` is a provider error token, not proof of
  the provider table's business meaning; 429 detection precedes quota detection by contract;
  prefixes are not authenticated lane membership; dead seats are not distinct incidents and a dead
  terminal record is not proof of non-resumption. No telemetry emission (FR14) and no orchestration
  action.
```

## 2. C2 — jj branch anchoring: exact lines to advance or add

Contract interface: `.ufo/waves/round-17/contract.md:16-22` (claim), `:80-93` (resolver, probe
sites, two findings, gate). Routed evidence:
`/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/jj-w1/reports/JjAuditMori.md` F3/F4, risk 1
(`:251-260`), remediation (`:285-291`), rows 1/2/5/6 (`:213-218`).

### 2.1 Province/document anchors

| Target `file:line` | Current anchor | Action |
|---|---|---|
| `PROVINCE.md:10` | `…; lane silence grading (silent / progressing / progressing-weak).` | Amend to name the basis: `branch-anchored (`refs/heads/<branch>`; resolution `symbolic-ref -q HEAD` → `refs/remotes/origin/HEAD` → unique `refs/heads/master|main`)` for report closure and authorship. |
| `PROVINCE.md:28` | Core `- **Lane silence** — SURFACE lane.<id> rows: launch-anchored authorship grading as silent, progressing, progressing-weak, young, not-open, or unavailable.` | Amend in place: replace "launch-anchored" with "launch-anchored and branch-anchored", and add the two drift findings. Draft in §2.2. This bullet is the only Core text that owns row-6 closure/authorship. |
| `PROVINCE.md:40` | last Round-16 paragraph | Append a Round-17 C2 paragraph after line 40: closure and authorship now read `refs/heads/<branch>`; `HEAD_BRANCH_MISMATCH` only when `merge-base --is-ancestor` returns 1 (other nonzero is probe error/unavailable); `LANE_AUTHOR_MISMATCH` only for the one-directional committer-vs-author rule. |
| `PROVINCE.md:47` | FR4 row: `Boundary: the census compares driver state with watchdog launch lines only; it does not establish MANIFEST admission or lane-LOG agreement.` | No change. C2 does not advance FR4; keep this boundary intact. |
| `PROVINCE.md:57` (optional) | FR14 | Not used by C2. If a bounded branch-ref Frontier row is wanted instead of a Core-only amendment, insert a new row after line 57 and mirror after `README.md:345`; scope it to ref selection and ancestry, never push/bookmark state. |
| `corpus/README.md:41` | last Coverage-map row | Insert one C2 note row after line 41 (proposed `corpus/knowledge/jj-branch-anchor-r17.md`): the resolver, the six probe sites, the two findings, the repo split, the gate sandbox scope. |
| `corpus/README.md:248-252` | `- **Row-6 closure is presence + window only (spec residual):** …` | Substance unchanged: C2 changes the *ref* row 6 reads, not presence+window semantics. Do not edit; the appended r17 note points here and to the spec lines below. |
| `corpus/README.md:334-335` | FR3 and FR4 rows | No change; C2 is not settlement semantics and not driver/MANIFEST/LOG reconciliation. |
| `corpus/README.md:345` / `347-349` | last FR row; Known gaps policy | Same insertion rule as C1 if a new FR row is adopted. No Known gaps bullet. |

### 2.2 Draft amendment for `PROVINCE.md:28`

```markdown
- **Lane silence** — `SURFACE lane.<id>` rows: launch-anchored, branch-anchored authorship grading
  as silent, progressing, progressing-weak, young, not-open, or unavailable. Report closure and
  authorship read `refs/heads/<branch>`, resolved `symbolic-ref -q HEAD` →
  `refs/remotes/origin/HEAD` → unique `refs/heads/master`/`main`, never bare `HEAD`. Two drift
  findings are additive: `HEAD_BRANCH_MISMATCH` when HEAD resolves and is not an ancestor of the
  branch tip (`merge-base --is-ancestor` status 1; any other nonzero is probe error, not a
  mismatch), and `LANE_AUTHOR_MISMATCH` when a post-launch commit on the branch has committer
  `<lane>-shokunin <lane>@shokunin.local` but a different author. Row A/B/C grading semantics are
  otherwise unchanged; neither finding establishes push state, authenticated authorship or wave
  settlement.
```

### 2.3 Census probe sites to change (working tree = tip `24526ea`, sha `f1f8d1b6…`, `VERSION=census-r6` at `:268`)

| `tools/mori-census.sh:line` | Current code / text | Required C2 change |
|---|---|---|
| `:1944` | decision-row comment `#   6 closed       report at HEAD, newest path commit ct in (launch, NOW]` | Say `report at refs/heads/<branch>`. |
| `:2092` | comment `# Row 6: report present at HEAD AND newest commit touching it in (launch, NOW].` | Same wording change; this is the row-6 spec comment. |
| `:2100` | `cap env GIT_OPTIONAL_LOCKS=0 "$GIT_BIN" -C "$ROOT" cat-file -e "HEAD:$rpath"` | `refs/heads/<branch>:$rpath`; resolve the branch **for `$ROOT`** (fleet root), not the lane repo. |
| `:2102` | `cap env GIT_OPTIONAL_LOCKS=0 "$GIT_BIN" -C "$ROOT" log -1 --format=%ct -- "$rpath"` | Add the resolved branch ref as the revision before `-- "$rpath"`; default `HEAD` must not remain. |
| `:2197` | `cap env -u GIT_DIR … -C "$repo" rev-parse --verify -q HEAD` | `--verify -q refs/heads/<branch>`; resolve the branch **for `$repo`** (lane repo). This is the row-9 presence check and the place `has_head` is set. |
| `:2207` | `cap env -u GIT_DIR … -C "$repo" log "${lg_args[@]}"` (default revision = `HEAD`; `lg_args` built at `:2200`) | Append `refs/heads/<branch>` as the revision. Keep the root-lane pathspec excludes at `:2205` unchanged. |
| `:2276` | usage string: `…; git -C <root> cat-file -e HEAD:.ufo/reports/round-<N>/<lane>.md` | Replace with the branch-ref form so `--help` matches behavior. |
| `:241-260` | stable finding-id list (`# Finding ids (stable compare contract):` `:241`; tail `TMUX_FRESHNESS_UNAVAILABLE` `:260`) | Append `HEAD_BRANCH_MISMATCH LANE_AUTHOR_MISMATCH` (contract `:86-93`). |
| `:405-418` | `# severity: info does not flip ROLL; warn|crit flips to DRIFT` (`:405`); `emit_finding` case `warn|crit` (`:412-417`) | The contract's "severity drift" is not a literal token: `drift` is the ROLL result. Emit the new findings as `warn` (or `crit` if L1 chooses), never `info`, or they cannot flip DRIFT. |

Resolver source discrepancy (must be handled, not hidden):

- `contract.md:82-83` says resolve "like `scripts/hyaku/jj-lane.sh detect_branch`:
  `symbolic-ref -q HEAD` → `refs/remotes/origin/HEAD` → unique of
  `refs/heads/master`/`refs/heads/main`".
- The actual fleet helper `scripts/hyaku/jj-lane.sh:115-126` has only two steps: `symbolic-ref -q
  HEAD` restricted to `refs/heads/*` and gated by `valid_branch` (`:117-120`), then
  `symbolic-ref -q refs/remotes/origin/HEAD` (`:121-124`), else rc1. **There is no
  master/main-unique fallback in the helper.** The census must add that third step; it cannot be
  described as "already like the helper".
- Measured lane state (O9-O13): HEAD is attached to `refs/heads/master`, `origin/HEAD` resolves to
  `refs/remotes/origin/master`, only `refs/heads/master` exists locally, HEAD == branch ==
  `24526ea`, ancestor rc0. So the resolver is exercised by the current state, but the mismatch
  branches are not live-observable here (they must come from the gate's colocated sandboxes).
- Repo split: row 6 uses `-C "$ROOT"` (`:2100,:2102`), row 9 uses `-C "$repo"` (`:2197,:2207`).
  Resolve the branch separately per probe site; a single cached ref would silently grade a child
  lane against the fleet root's branch.

### 2.4 Spec notes a C2 supersede must name (history not rewritten)

| `file:line` | Text to cite as the superseded basis |
|---|---|
| `corpus/knowledge/silence-grading-r2.md:104` | decision row 6: `committed report at HEAD **and** newest commit touching that path has launch < ct ≤ NOW` |
| `corpus/knowledge/silence-grading-r2.md:109-110` | measured anchors: `git cat-file -e HEAD:.ufo/reports/round-10/aggregator.md` rc 0 |
| `corpus/knowledge/silence-grading-r2.md:182` | predicate: `report present at HEAD (git cat-file -e HEAD:<path> rc 0)` |
| `corpus/knowledge/silence-cutover-r3.md:43` | spec-row map: `ps_report_closed :648-661: cat-file -e HEAD:<path> rc 0 AND …` |
| `corpus/knowledge/silence-cutover-r3.md:174,178` | fixture rows that exercise row 6 (kept; the fixture intent is unchanged) |

## 3. Stale wording and appended supersede drafts

### 3.1 `PROVINCE.md:25` — the stale window-probe status (verbatim)

> `- **Same-boot journal window since anchor** — explicit read-only probe `tools/mori-journal-window.py --anchor PATH --scope user|system` (round-16 build; verification pending).`

The stale token is exactly `(round-16 build; verification pending)`. It is the only
`verification pending` occurrence in `PROVINCE.md` and `corpus/README.md` (O21). The round-16
closure already routes it: `corpus/lessons/round-16-verifier-spotcheck.md:220-223` (open-queue
item 4, "Stale wording after closure"). The verification facts that supersede it are O15-O18:
gate 64/64 at `87a57c1`, `verdict ok`, and per-scope live `MORI_JOURNAL_WINDOW_OK` with
`records_after_anchor=0`. Draft appended note (place under a new `## Corrections (round 17)`
section after `PROVINCE.md:94`, matching the `## Corrections (round 12)` pattern at line 92):

```markdown
## Corrections (round 17)

- **Supersede — `PROVINCE.md:25` "(round-16 build; verification pending)".** The window probe is
  verified at its declared finite scope; the phrase is superseded, not rewritten. Round-16
  evidence: `capability-before` summary `{"capability_absent":64,"matched":0,"mismatched":0,
  "total":64}` vs `capability-after` `{"capability_absent":0,"matched":64,"mismatched":0,
  "total":64}`, `exit_code:0`, `verdict:"ok"`, gate `tools/mori-round16-regressions.py` sha256
  `e70ed67c…`, tool `tools/mori-journal-window.py` sha256 `d61e0d22…` at `git.head 87a57c13…`.
  The tool sha256 is identical at lane tip `24526ea`, so the verified bytes are current. Live
  receipts `.ufo/waves/round-16/evidence/live-window-manifest.json`
  (`observed_at 2026-10-20T09:12:11Z`, head `87a57c13`) and `live-window-{user,system}.json`
  (`MORI_JOURNAL_WINDOW_OK`, `records_after_anchor=0`, all four `positive_*=0`; anchor-only
  captures). Closure: `corpus/lessons/round-16-verifier-spotcheck.md:11` (admitted at finite
  scope) and `:220-223` (this supersede). Unchanged limits: alias false refusal, rotation/vacuum,
  cross-boot ordering, completeness, unique victim, authenticated emitter; unavailable is not
  zero. The closure's execution-nonconformance items (`:202-219`) are not waived.
```

### 3.2 `corpus/knowledge/journal-cursor-window-r16.md:2` — verified-at host version (verbatim)

> `verified-at: 2026-10-20 — the four public systemd 262 pages above were opened for this note by static reads. No journal was queried, no host journalctl query was run, and no fixture, wrapper, test or gate was run. Host systemd version was not verified; no behaviour is claimed for any host version.`

The stale sentence is `Host systemd version was not verified; no behaviour is claimed for any
host version.` It was true for the note author, but the wave's own runtime record did pin the
host: `.ufo/waves/round-16/runtime-versions.json` records `journalctl --version` =
`systemd 261 (261.2-1-arch)`, exit 0 (O19). Draft appended note (append after line 136; do not
rewrite line 2):

```markdown
## Supersession — host systemd version (appended 2026-10-20, round 17)

The `verified-at:` sentence (line 2) "Host systemd version was not verified; no behaviour is
claimed for any host version." is superseded as a host-version record only.

- **Round-16 host:** `journalctl --version` = `systemd 261 (261.2-1-arch)`, exit 0
  (`.ufo/waves/round-16/runtime-versions.json`). The two live window captures
  (`evidence/live-window-manifest.json`, `observed_at 2026-10-20T09:12:11Z`) therefore ran on
  261.2-1, i.e. on a version older than the four systemd 262 man pages this note cites.
- **Upgrade:** `/var/log/pacman.log` records `systemd 261.2-1 -> 262-1` at `2026-10-20T09:16:28-
  0300` (`:2531`; `systemd-libs` `:2487`, `lib32-systemd` `:2805`, `systemd-sysvcompat` `:2922`).
  The host booted at `2026-10-20T09:56:56-0300` (`/proc/stat btime 1792501016`), 40m28s after the
  upgrade, so this boot is on the 262-1 package set. [INFERENCE] PID1 is the 262-1 binary because
  the boot postdates the upgrade; no direct query of PID1's version was made.
- **Round-17 read-only measurements:** `systemctl --version` first line `systemd 262
  (262-1-arch)`; `pacman -Q systemd` -> `systemd 262-1` (query only, no pacman transaction).

Consequences: the installed package now matches the cited man-page version at the version level
only. **No host cursor, seek-fallback, alias, vacuum, rotation or cross-boot behaviour was
measured on either 261.2-1 or 262-1**, and the note's `[UNKNOWN]` entries stand unchanged. The
261.2-1 live captures say nothing about the 262-1 host; any live window claim on 262-1 requires a
fresh measured capture. "No behaviour is claimed for any host version" remains true.
```

### 3.3 `corpus/README.md:41` — host-version cell (verbatim tail)

> `| S014/S015/S039/S040; host systemd 261.2-1 \`--help\`/\`man\` checks only, no journal read |`

This cell is historical, not current: 261.2-1 was the round-16 host (O19), and the host is now
262-1 (O4-O7). Its "no journal read" clause describes the *note author* (line 2 of the note) and
remains true, but the *wave's* live receipts did read two journal scopes (O17-O18) - the two
statements must not be conflated in the new row. Do not rewrite line 41; put the correction in
the round-17 coverage row's Sources/Notes cell, e.g.:

```text
host systemd 261.2-1 at round 16 (`runtime-versions.json`); upgraded to 262-1 2026-10-20T09:16:28-0300, boot 09:56:56-0300. The r16 note's "no journal read" is the note author's scope; round-16 wave live receipts did read two journal scopes (`evidence/live-window-{user,system}.json`).
```

## 4. Confidence and remaining unknowns

Observed (cited above): all line numbers and quotes; host versions and pacman log; boot time; git
tip/ref state and census sha; round-16 gate and live receipts; absence of the three round-17
tools; the single `verification pending` occurrence.

[INFERENCE]: that PID1 on the current boot is the 262-1 binary (package upgrade precedes boot by
40m28s; no downgrade between). That the two r16 live window captures ran on 261.2-1 (they precede
the logged 09:16:28-0300 upgrade, and no 262 transaction is logged before that). That a live run of
the census on this lane today would produce no `HEAD_BRANCH_MISMATCH` (only the read-only ancestor
check was run, not the census). That the r16 closure's "host 261.2-1 from version lookups"
(`round-16-verifier-spotcheck.md:222`) refers to the same `journalctl --version` capture as
`runtime-versions.json`.

[UNKNOWN] / open:
- C1 tool, C1 gate and C2 gate absent at this snapshot (O20); no delivery or gate result can be
  cited in the province text yet.
- `corpus/SOURCES.md` ends at S040 (`:46`; `## Paths` `:48`); S041-S048 are not registered, so
  new coverage rows cannot cite them as sources yet.
- Whether the note's four pages were re-fetched this round is outside this seat (the note's own
  `recheck:` line 3 is the executable check; it was not run here).
- The behavior of `journalctl --cursor=` on an absent cursor remains undocumented
  (`journal-cursor-window-r16.md:5-9`), and no host version is measured for it.
- Whether the r17 integration will choose a new Frontier row or a Core-only amendment for C2 is
  L1's decision; both insertion points are given (§1.2, §2.1).

## 5. Handoff

- Append (§3.1) to `PROVINCE.md` end under `## Corrections (round 17)`; append (§3.2) to
  `corpus/knowledge/journal-cursor-window-r16.md` after line 136; correct the host-version claim
  in the new r17 coverage row (do not rewrite `corpus/README.md:41`).
- Add the C1 Core bullet after `PROVINCE.md:28`, amend `PROVINCE.md:28` for C2, extend
  `PROVINCE.md:10`, append round-17 prose after `PROVINCE.md:40`, and add coverage rows after
  `corpus/README.md:41` (one per note).
- If a Frontier row is adopted, insert after `PROVINCE.md:57` and mirror after `corpus/README.md:345`.
- For C2 code: six census sites (`:1944,:2092,:2100,:2102,:2197,:2207`), usage `:2276`,
  finding list `:241-260`, severity use `:405-418`; resolver step 3 must be added (helper lacks
  it, `scripts/hyaku/jj-lane.sh:115-126`); resolve per repo (`$ROOT` row 6 vs `$repo` row 9).
