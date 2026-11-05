# Round 98 — verifier spot-check (mori)

author: hyaku closure (non-author integrator, @m_zfl)

Closure of lane-round mori r98. Report `.ufo/reports/round-98/mori.md` (fleet repo); prompt
`.ufo/prompts/mori-round-98.md`; entering `b2a67ce562bbf2f0cc73f47d8e79f792badf5e63`, tip
`db9f1b78b93d1e27d194b4d035d69524b24fd001`. Driver digest (copied from `.ufo/watchdog.log`):
`2026-11-05T18:20:26-03:00 launch mori round=98 pgid=816285 driver=hyaku-inline attempt=1`;
`2026-11-05T18:49:18-03:00 complete mori round=98; hyaku-inline attempt=1`.
Measurements below were run by this closure on 2026-11-05 (~21:55Z–22:05Z) over `git archive` trees of `b2a67ce5`
(before) and `db9f1b78` (after) under `/fast/scratch/hyaku/closure-mori-r98/`. No lane gate, `--selftest` or frozen
counter (`count-c1.py`, `count-c2.py`, `mori-scorecard-calibration.py`) was executed by this closure (PROTOCOL
§Gate standard, Closure consequence). The C1 tool is registered as a **probe** (SKILL.md Round98 row); its read-only
live mode and journal mode were run against closure-built inputs to re-derive the capability (§2 C1).

## 1. Step-1 conformance

| check | command | observed | result |
|---|---|---|---|
| report committed by lane identity | `git log --format='%an <%ae> %H %cI' -- .ufo/reports/round-98/mori.md` | `mori-shokunin <mori@shokunin.local> 78e7de2538af…` 2026-11-05T18:48:55-03:00 (after the last lane commit 18:48:13) | pass |
| `SHONEN` heading, one line per box | read report §SHONEN | 4 lines, each `[~]` with a pointer | pass |
| cited commits exist + ancestor of `master` | `git cat-file -e <h>^{commit}`; `git merge-base --is-ancestor <h> master` for `b75e26cc beab7bbb 600deb7e 379a2f61 e4fb203f db9f1b78` (+ entering `b2a67ce5`) | all exist, all ancestors | pass |
| lane pushed | `scripts/hyaku/jj-lane.sh state …/mori-shokunin` | `branch=master local=db9f1b78… remote=db9f1b78… ahead=0 behind=0 head=detached tracked=0 untracked=0`; `ls-remote origin refs/heads/master` → `db9f1b78…` | pass |
| no uncommitted round work | `git status --porcelain` | empty (r97 D1 seat files committed as `beab7bbb`) | pass |
| prompt carries template contract | `diff <(sed -n 1,140p prompt) templates/round-prompt.md` (fleet template = kimi-shokunin template, `cmp` equal) | only `{{LANE}} {{ROUND}} {{FLEET_ROOT}} {{AXES}}` substitutions differ; §1–§5 headings identical; 0 unrendered `{{`; hyaku addendum §6 + §7 present | pass |

Not a marker: six lane commits, 55 files, +5223/−36 (`git diff --stat b2a67ce5 db9f1b78`). Status `ok`.

## 2. Claims — re-check

### C1 coverage, capability — `tools/mori-userns-runway.py` (user-namespace runway + sudo sysctl-write scan)

Re-measured (structure, live surface, closure-generated fixtures); counter receipts evidence-verified:

- New ground, before→after: `ls tools/mori-userns-runway.py` absent→present (342 lines);
  `grep -ci namespace PROVINCE.md` 0→2; `grep -c tools/mori-userns-runway.py` PROVINCE.md 0→1, SKILL.md 0→2 (Round98
  registry row, kind `probe`, 8 fields); `corpus/knowledge/userns-runway-r98.md` absent→69 lines with `source:` S629–S632,
  `verified-at:`, `recheck:`; SOURCES rows S629–S632 tier A, `mined`, opened 2026-11-05, used-by that entry.
- Source reading: the tool reads `DIR/sys/user/max_user_namespaces`, `readlink`s each `DIR/<pid>/ns/user`, counts
  distinct targets other than `4026531837` (= S631/S632 `PROC_USER_INIT_INO`/`0xEFFFFFFD`); the journal scan keeps only
  `sudo[` lines with ` COMMAND=` and classifies via `shlex` — no fixture-keyed lookup in the landed bytes.
- Live, independent: `cat /proc/sys/user/max_user_namespaces` → `122865`; `for p in /proc/[0-9]*; do readlink $p/ns/user;
  done | sort -u | grep -vc 4026531837` → `6`. Probe live: `USERNS_RUNWAY limit=122865 used_lb=6 pids=3002 unreadable=2754
  runway=122859 low=32 state=ok` rc 0 — equal.
- Incident capture, independent: `grep -E 'proc/sys|sysctl' evidence/journal-incident-r98.txt | sed 's/.*COMMAND=//' |
  sort | uniq -c` → 6 writes (`echo 0 >` ×2, `echo 15638 >`, `sysctl user.max_user_namespaces=15638`, `sysctl -w …=10000`,
  `sysctl -w …=122865`) + 2 reads (`sysctl -a`), one key, two zero writes. Probe `--journal` → `SYSCTL_WRITES n=6 keys=1
  userns_zero=2` rc 1 — equal; capture sha256 `97850413…79738` = `INCIDENT_SHA` pinned in `count-c1.py:34`.
- Closure-generated fixtures (not in any frozen battery, so a fixture-shape lookup cannot know them): fake proc with
  limit 7 and links {init, 9001, 9002, 9002, 9003…9007} → `limit=7 used_lb=7 … runway=0 state=exhausted` rc 1
  (expected 7 distinct non-initial); limit 0 + init-only → `used_lb=0 runway=0 state=exhausted` rc 1; journal line
  `sysctl kernel.pid_max=99999 user.max_user_namespaces=0` plus a `sysctl -n` read → `n=2 keys=2 userns_zero=1` rc 1. All
  as derived by hand.
- Committed evidence: `before-c1.txt` `C1=unmet cases_ok=0/15 …` exit 1; `landing-c1.txt`/`final-c1.txt` (rev
  `e4fb203f`) `C1=met cases_ok=15/15 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) registry=met
  sourced=met(S629,S630,S631,S632) province=met checks_failed=-` exit 0; `controls-r98.txt` header pins
  `count-c1.py=a9f140bd…`, `CONTROLS_DONE unexpected=0`. Matches the report.
- Counter defect (not a claim defect): `w1/Mo98CritC1.md` shows a fixture-shape lookup stub also passes the frozen
  counter 15/15 and the live conjunct checks only the limit echo. The landed tool is not that stub (source reading and
  the closure fixtures above), so the claim verifies on this closure's own measurement; the counter's weakness is
  routed (D1) and already grounded as QUALITY 209.

Verdict: **coverage improved** (verifies; capability `user-namespace runway and sysctl-write scan` enters).

### C2 calibration — SCORECARD `## Axes` Last-change cells match the admitted r97 closure

Re-measured (independent of the lane's gate and counter):

- Fleet `MANIFEST.json`: highest admitted mori `type: closure` lane_round grading each axis improved/harmed →
  operability 97, freshness 97 (rounds[1384]), calibration 93, depth 86, coverage 80, adjacency 19.
- Last-change cell leads, before (`b2a67ce5`): operability `round 93`, freshness `round 82` (2 mismatches), others
  equal; after (`db9f1b78`): operability `round 97`, freshness `round 97` (0 mismatches).
- Line-by-line compare of SCORECARD before/after: only lines 11 and 13 differ above the appended tail; on both the
  text before the last ` | ` (Axis, Score, Evidence) is byte-equal and the new cell = `round 97 (improved, score held); `
  + the old cell. Remaining change is a pure append (+25 lines: round-98 verdict, capability row, Planned r99).
- Committed evidence: `before-c2.txt` `C2=unmet mismatches=2 … mismatched_axes=operability,freshness` exit 1;
  `landing-c2.txt`/`final-c2.txt` `C2=met mismatches=0 columns_unchanged=yes tool=ok tool_rc=0` exit 0. Matches.

Verdict: **calibration improved** (verifies).

### Harm check

`git diff --numstat b2a67ce5 db9f1b78 | awk '$2>0'` → only `SCORECARD.md` (−2, the two cells above) and
`.ufo/waves/round-97/w1/Mo97ScribeLog.md` (−34, the r97 D1 late-seat bytes committed as-is). `corpus/knowledge/`: +69,
one new file; SKILL.md, PROVINCE.md, QUALITY.md, SOURCES.md, LOG.md: append-only.

| axis | verdict | basis |
|---|---|---|
| coverage | improved | C1 above |
| calibration | improved | C2 above |
| operability | unchanged | not claimed; the new tool is counted under coverage |
| depth | unchanged | not claimed; knowledge entry counted under coverage |
| freshness | unchanged | no existing row re-verified or re-pinned this round |
| adjacency | unchanged | PROVINCE boundary note routes repair to tsukuroi and sysctl policy to the operator; not absorbed (`w1/Mo98ConnSibling.md`) |

## 3. Discernment spot-check (`corpus/lessons/round-98.md` `## Gate`)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S629 kernel sysctl/user.rst v7.2 | admit, mined, tier A | `curl https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/sysctl/user.rst` → 200, 2564 B, sha256 `2a83137d…7207a` = pin | agree | quote found at lines 77-78 under `max_user_namespaces`, 16 words (≤25); the file defines the knob, tier A honest; the lane also notes the identical text under `max_uts_namespaces` (upstream copy-paste), located instance correct |
| S630 unshare(2) | admit, mined, tier A | `curl https://man7.org/linux/man-pages/man2/unshare.2.html` → 200, 25450 B, sha256 `bc19c6eb…972a` = pin | agree | ENOSPC (since Linux 4.9) entry, raw lines 252-256; quote present after tag-strip, 17 words |
| S631/S632 proc_ns.h, nsfs.h v7.2 | admit, mined, tier A | live sha256 `63376480…d537`, `da2a23c3…4d65` = pins; line 44 `\tPROC_USER_INIT_INO\t= USER_NS_INIT_INO,`, line 50 `\tUSER_NS_INIT_INO\t= 0xEFFFFFFDU,` | agree | quotes located, tab caveat stated in the row; together they ground the tool's `4026531837` constant |
| re-scope S627 user_namespaces(7) as limit ground | reject | `curl https://man7.org/linux/man-pages/man7/user_namespaces.7.html` → 200, 59987 B; tag-stripped text has no `max_user_namespaces` or `/proc/sys/user` | agree | the page does not state the limit semantics, and S627 is a rejection row for another scope; re-scoping in place would break CORPUS SOURCES rule 2 |

SOURCES row re-opened: S629 (above) — quote present, 16 words, location correct.
Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` → exit 0, `mori ok
…/mori-shokunin/corpus/SOURCES.md`, 43 `W04` (= `census-after.txt` 43), no other finding. Rows
`grep -cE '^ {0,3}\| *S[0-9]{3,}' corpus/SOURCES.md`: 400 → 404.

## 4. Trend verdicts

- **expansion: improved** — one new knowledge entry on ground uncovered at entering (`git show b2a67ce5:PROVINCE.md |
  grep -ci namespace` → 0), each `source:` a `mined` row opened this round; capability row added to SCORECARD.
- **quality: unchanged** — the four new rows match their pins at write time; no pre-existing entry was re-verified,
  deepened or superseded, and no admitted entry failed a re-check. The lane's `improved` (new rows byte-identical live)
  describes admission quality, not the LEARNING quality observable.
- **discernment: improved** — this outside spot-check agrees with the gate on the admits (S629–S632) and the reject
  (S627 re-scope); the counter disagreement from the lane's own critic became lesson Mistake 4 with grounded QUALITY 209.

## 5. Routed defects (lane fixes next round)

- **D1** C1 counter gameable by a fixture-shape lookup stub; live conjunct checks only the limit echo
  (`w1/Mo98CritC1.md`). Already QUALITY 209 + SCORECARD Planned r99 item 1; the next capability counter must score
  measurement-time fixtures with independently computed answers, and a live `used_lb` cross-check.
- **D2** mutant m03 (used > limit clamping) survives; classifier gaps F1–F3 (`w1/Mo98MutC1.md`, `w1/Mo98RevC1.md`) —
  carried in Planned r99.
- **D3** SCORECARD operability/freshness Evidence cells still cite pre-r97 closures; the r96 calibration gate pins them to
  base `66c5518e` (`w1/Mo98RevC2.md`) — Planned r99 item 2.
- **D4** carried: r97 auditor residuals R1–R3, calibration survivor M10, 31 `prefix_only` digest rows, operator L0
  mori | round-94/95/96.

## 6. Closure result

status `ok`; both claims verify; no axis harmed → **admitted**.
