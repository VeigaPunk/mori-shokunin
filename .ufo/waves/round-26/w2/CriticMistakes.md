# CriticMistakes — round 26, wave 2 (falsify)

Seat: MoriR26.CriticMistakes. Target: `corpus/lessons/round-26.md` section `## Mistakes` (lines 32-57) and
`corpus/QUALITY.md` criteria 78-79, read with `git show 16935e24c93fa7e7567413d7ec091339a5df1474:<path>`.
Scratch: `/fast/scratch/hyaku/mori-r26/CriticMistakes/` (per-revision allowlist copies only).
Tooling: nothing installed or upgraded. `pacman -Q earlyoom` was run as a query only, not a transaction.

## Verdict summary

| Item | Mistake real? | Captured-by honest? | Fix shown able to fail? | Verdict |
|---|---|---|---|---|
| M1 | yes, reproduced | yes | yes, reproduced | holds; low residual not recorded |
| M2 | yes, reproduced | yes | no command in lesson; I showed the scan can fail | **defect (medium)**: the fix sentence is false at its own commit; two recurrences omitted |
| M3 | yes | mostly; a sibling-lane rule went unnamed | no | holds, low gaps |
| M4 | yes, reproduced on host | yes | no command in lesson | **defect (medium)**: the sweep missed a contradicting sibling file |
| QUALITY 78 | — | cites `lessons/round-26.md (M1)` | — | holds; heading provenance wrong (low) |
| QUALITY 79 | — | cites `lessons/round-26.md (M4)` | — | holds; heading provenance wrong (low) |

## M1 — fail-open counting command: holds

- **Evidence pointer checked.** The as-typed `contract.md:38` command, run under `bash` from `/tmp` at `248408f5`, printed
  `bash: line 1: .ufo/waves/round-26/c1-phrases.txt: No such file or directory` then `stale_present=0` (exit 0).
  From the lane directory with `R=deadbeef` it printed `stale_present=0`. Both match the lesson (lines 35-37),
  `w1/CriticLearningRules.md:92` and `w1/CriticC1Width.md:48`.
- **Captured-by checked.** `round-20.md:30` is row M9, a counting-command defect (`LC_ALL`). `round-25.md:45-48` is M3,
  where first-cut predicates passed on paraphrase. Both are prior fail-capability lessons, so the claim is honest.
- **Fail command run.** `bash .ufo/waves/round-26/count-c1.sh deadbeef` printed `bad_rev` with exit 2. At `248408f5` it
  printed `stale_present=4 r26_entry=absent r26_new_source_ids=0 r12_names_r26=0` with exit 0. At the tip it printed
  `0 / present / 13 / 4`, exit 0. Running from `/tmp` gave the same result, so the counter does not depend on cwd.
  `count-c2.sh deadbeef` printed `bad_rev` (exit 2). At `248408f5` it printed `absent cases_commit=none tool_commit=none`
  (exit 2). The working-tree scripts equal the tip (`git diff --stat 16935e24 -- count-c1.sh count-c2.sh` prints nothing).
- **Residual not recorded (low).** `w1/MutC1Counter.md` §3 landed at `16935e2`, after the lesson's `327fbcc`. In its
  table, five of eight stale-statement mutants still print the after-value under the A1 counter: paraphrase, case
  change, moving the claim to another file, emphasis and zero-width space (rows M1, M2, M3, M5a/b, M6). It recommends
  gating `r12_names_r26 >= 1` and case-folding (§4.3, §5). This does not contradict QUALITY 78, whose scope is the
  working directory and a bad revision, but the lesson's M1 does not name the residual.
- Nit (no harm): with no argument, `count-c1.sh:3` `${1:?rev}` exits 1, not 2. It prints no count.

## M2 — the wave spec raised the retention scan: real, but the fix claim is false at its own commit

Command (each revision scanned with the allowlist committed at that revision, copied to scratch):
`python3 -I -B tools/mori-retention-gate.py scan --repo <lane> --rev <c> --policy .ufo/waves/round-18/frozen/c1-policy.json --allowlist <scratch>/al-<c>.json`

| Revision | Unallowlisted | New hit beyond the four round-20 fixture lines |
|---|---|---|
| `248408f5` (entering) | 4 | — |
| `28b0494` | 4 | — |
| `5e5e86f` | **6** | `wave1-spec.json:5` R7, `wave1-run.json:247` R7 |
| `5854050` | 4 | — |
| `327fbcc` (carries the lesson) | **5** | `SKILL.md:718` R7 |
| `4dba9cc` | 4 | — |
| `c6ea248` (carries the SCORECARD outcome) | **5** | `.ufo/waves/round-26/w1/DraftSkillFr10.md:157` R7 |
| `2ecb661` | 4 | — |
| `16935e2` (tip) | 4 | — |

A second, independent pass over all nine revisions gave the same counts, and every scan exited 1 (the four
round-20 fixture hits keep the gate red at every revision, including the entering tip).
I did not scan `99338de`, `c2fdd92`, `5b10649`, `278f02e`, `825f988`, `b4473ed`, `93aa1b9`, `738eec1` or `21386b9`.

- **Evidence pointer: holds.** The lesson's 4 → 6, `wave1-spec.json:5`, `wave1-run.json:247` and class R7 all match
  exactly. Captured-by holds: routed R8 is at `round-25-verifier-spotcheck.md:200-202`, and the catching seat is
  ReviewPrivacyDesign F2 (`w1/ReviewPrivacyDesign.md:48`).
- **Defect (medium): false statement and omitted recurrence.** The fix (lesson lines 47-48) says "scan re-run after
  every evidence commit; back to 4". At `327fbcc`, the commit that carries that sentence, the scan reads 5. It read 5
  again at `c6ea248`, whose `SCORECARD.md:1622` says "retention scan 4 at `4dba9cc7`". That is true of `4dba9cc` but
  not of the commit carrying the line. Each recurrence was repaired by a later name-only allowlist commit (`4dba9cc`,
  `2ecb661`). So the mistake recurred twice after its own fix, and the section does not say so. The no-harm contract
  (`contract.md:124-125`) still holds at the landed tip, because 4 equals the entering value.
- **Fix able to fail.** The lesson gives no command. The table above shows the scan does fail (6, 5, 5).
- **Smallest correction.** Amend M2's fix line to name both recurrences (`327fbcc` → `4dba9cc`, `c6ea248` → `2ecb661`).
  State that the scan runs before each commit lands, not after. Cite the scan command as the fail check.

## M3 — "active since" from an invocation timestamp: holds, low gaps

- **Evidence pointer: holds.** At `5e5e86f`, `LOG.md:1824` reads "active and enabled since 04:55:44 -03".
  `capture-boots.txt` shows earlyoom lines in boot -2 (8), boot -1 (252) and boot 0 (13), and none in boots -5 to -3.
  That supports "ran in each of the last three boots". `w1/ConnSiblingOverlap.md:81-84` cites the pacman install line
  and is the catching seat.
- **Fix present.** The r26 entry's `verified-at:` (line 2) separates the install date from the invocation start.
  The correction is appended at `LOG.md:1831-1836`. The original line 1824 stays, which matches `QUALITY.md:6`
  ("Errata are append-only blocks"). A `git grep` for `since 04:55|enabled since` at the tip finds only `LOG.md`, the
  lesson and `w1/ConnSiblingOverlap.md`.
- **Captured-by "none" (low).** That is true of mori's QUALITY, but `w1/ConnSiblingOverlap.md:81` cites a sibling rule
  ("earlyoom active-since is distinct from enabled-since", tsukuroi `corpus/lessons/round-18.md:115`). The fleet had
  already captured this class, from a sibling admitted as S125 in this very round.
- **Not shown able to fail; no criterion (low).** A ready fail check exists: `w1/ConnSiblingOverlap.md:130`,
  `git grep -n -E 'enabled since|never acted|has not acted' <rev> -- corpus/knowledge/userspace-oom-killers-r26.md`.
  At the tip it prints nothing (rc=1, run). The lesson should cite it.

## M4 — newer-upstream sentence in present tense: real; the fix's sweep is incomplete

- **Evidence pointer: holds.** At `248408f5`, `userspace-oom-killers-r12.md:6` contains
  "only `--kernel-oom` delegates to the kernel OOM killer". On the host, `strings /usr/bin/earlyoom | grep -c kernel-oom`
  gives 0, `earlyoom -v` gives `earlyoom 1.9.0`, and `pacman -Q earlyoom` gives `earlyoom 1.9.0-1`. This agrees with
  `w1/SrcEarlyoomReadme.md:79-92` (F1); `w1/DraftEntryR26.md:519` is §4.2. Line 6 at the tip scopes the option to the
  master README (S016) and says it is not in the installed 1.9.0.
- **Captured-by "none" holds.** Before 79, no QUALITY criterion names an installed-release check.
- **Not shown able to fail.** The lesson gives no command. I ran `git grep -l -F 'only \`--kernel-oom\` delegates'`
  under `corpus`: at `248408f5` it hits the r12 file; at the tip it hits only `corpus/lessons/round-26.md`, the
  lesson's own quote.
- **Counterexample (defect, medium; QUALITY 77 and 79).** `corpus/knowledge/oom-kill-counter-kernel-only-r12.md:21`
  still says, in the present tense and with no release scope: "`earlyoom --kernel-oom` delegates to the kernel; the
  counters can move if that route actually reaches a kernel OOM victim". Line 30 still says it "is the explicit
  delegation exception". The file is unchanged this round (`git log 248408f5..16935e24 -- <file>` is empty). Line 21
  contradicts `lessons/round-26.md:19-21`: "The installed 1.9.0 has no `--kernel-oom` option … so an earlyoom kill
  never moves kernel `oom_kill` counters". This is the "moved to another file" blind spot that `w1/MutC1Counter.md` §3
  row M3 named, and it is real in the same file that row used.
- **Smallest correction.** Scope `oom-kill-counter-kernel-only-r12.md:21` and `:30` to the master README (S016), and
  state that the installed 1.9.0 lacks the option, naming the r26 entry. Record this as a named correction row, and
  have M4's fix name the sweep.

## QUALITY 78-79

- **Cite form holds.** Each criterion cites its lesson: `QUALITY.md:359-360` → `lessons/round-26.md (M1)` and
  `QUALITY.md:364` → `(M4)`. This matches the lane's `#M` anchor style (`QUALITY.md:27-50`, for example
  `lessons/round-12.md#M20`).
- **Text holds.** 78 describes `count-c1.sh` accurately: committed phrase list at line 10, bad revision at line 4,
  missing file at line 8, short list at line 11.
- **Defect (low, provenance).** 78-79 sit under `## Criteria added round 25 — round-24 routed defects D1 and D2`
  (`QUALITY.md:338`). There is no round-26 heading, so the file attributes both criteria to round 25. Every earlier
  round has its own heading (`QUALITY.md:9-338`). Correction: add `## Criteria added round 26` before line 356.

## Round-26 mistakes the section omits

- **O1 (medium): M2 recurred twice after its fix.** See the M2 table (`327fbcc`, `c6ea248`). The fixing commits
  `4dba9cc` and `2ecb661` are visible in `git log 248408f5..16935e24`.
- **O2 (medium): the C2 contract's scope rule was fail-open, and a frozen case pinned the wrong answer.** A version line
  alone set `scope_complete` true when `ActiveEnterTimestampMonotonic` was missing or 0 (`contract.md:173-174`; fixed in
  `93aa1b9`). A stopped earlyoom that had sent signals this boot read quiet (`contract.md:175-179`; `738eec1`). For an
  active earlyoom, frozen `c02` still pins `KILLERS_QUIET`, so that stays a permanent limit. The same holds for frozen
  `c04` and `c19` (`contract.md:170-172`). These are L1 contract-design errors that drove five post-freeze tool
  changes. `lessons/round-26.md:26-30` frames them as a learning, with no Evidence, Captured-by, Fix or criterion.
- **O3 (low-medium): an L1-opened source row was admitted with a wrong teaching.** At `327fbcc`, S124 `teaches` said
  "not monitored … unless an ancestor is `kill`". The row is marked "opened by the L1" (`lessons/round-26.md:77`).
  Seat SrcResourceControlV262 showed it was wrong, and `16935e2` corrected it (`lessons/round-26.md:88-92`). The sweep
  is clean: the old wording survives only in the lesson's change log. It is logged as a Gate row change, not a mistake.
- **O4 (low): the lesson was written before wave 1 closed.** `MutC1Counter.md`, `SrcResourceControlV262.md` and
  rewrites of `SrcEarlyoomKillC.md` and `SrcEarlyoomUnit.md` landed at `16935e2`, after the lesson at `327fbcc`. Only
  S124 was carried back into the lesson. The working tree also holds an uncommitted 74-insertion, 88-deletion edit to
  `w1/SrcEarlyoomKillC.md` (`git diff --stat`), so a cited wave-1 report is still changing. [INFERENCE: the seat is
  still running per the peer roster.]

## Not run

- Retention scan at the nine intermediate revisions listed under M2.
- Mutation of `count-c2.sh` beyond the bad-revision and pre-tool revisions.
- A full-tree sweep for other present-tense earlyoom or oomd statements outside the `kernel-oom` and `since 04:55` greps.
