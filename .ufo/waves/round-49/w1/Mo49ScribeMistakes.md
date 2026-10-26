# Mo49ScribeMistakes — round 49 / w1 — `## Mistakes` draft for `corpus/lessons/round-49.md`

Seat: `Mo49ScribeMistakes` (leaf; no subagents). Target: the `## Mistakes` section of
`corpus/lessons/round-49.md`, which does not exist yet (`ls corpus/lessons/round-49.md` → `No such file
or directory`, exit 2). Mined only from round 48 and the round-48 closure, as assigned.

Read-only seat: no lane file was edited, no lane tool was executed, no scratch directory was needed, no
tool was installed or upgraded. Every statement below is either a read of committed bytes/a committed
receipt or a read-only `git` query plus `find`/`wc` counts; nothing was re-run.

## 1. Draft — `## Mistakes` (fenced for the L1 to paste)

```markdown
## Mistakes

| id | class | evidence | captured-by | fix |
|---|---|---|---|---|
| M1 | survivor | The round-48 C1 counter handed each variant to the tool as `--skill <scratch>/variant-J1.md … variant-H4.md` and `TMPDIR=<scratch>/c1-<variant>-…` (`.ufo/waves/round-48/count-c1.py:238,247`), so a tool that read neither `SKILL.md` nor any row printed `C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=12` (exit 0) by branching on the name (`.ufo/waves/round-48/w1/CritC1Counter.md:26-52`, the two channels at `:49-50`, reproducer at `:28-33`) | none — QUALITY 126's harness-leak check is tool-scoped: it "claims only that the tool doesn't exploit them", and records the harness leak itself as residual (`w2/R48RevQuality.md:71-73`) | Opaque handles in this round's frozen counter: the `SKILL.md` copy and the per-run scratch dir are a sha256 prefix of their bytes, the run order follows that hash, and runs are launched against `TMPDIR=t-<hash>` (`count-c1.py:216-221,257,274`), with selftest arm `handles_carry_no_variant_name` rejecting any handle matching `variant\|junk\|honest\|[JNH]\d\|real` (`count-c1.py:374-376`); the honest pin-moving edit H5 that F1 asked for (`w1/CritC1Counter.md:64-68`) is also in the set. **Shown able to fail**, by the sniffer pair, both opened: the name-keyed control (`controls/stub-filename-sniffer.py`, keys on `variant-[JN]\d\|c1-[JN]\d`) scores `C1=met … variants=12 rev=b3e3453d…` under the round-48 counter (`.ufo/waves/round-49/evidence/control-c1-sniffer-under-r48-counter.txt`, exit 0) and `C1=unmet junk_met=18 honest_unmet=0 real=met errors=0 variants=26 rev=b3e3453d…` under this round's counter (`evidence/control-c1-stub-filename-sniffer.txt`, exit 1) — every `N*`/`J*` line `got=met`, so the control cannot reach `met` |
| M2 | landing | After round 48, `git status --porcelain` still showed 114 untracked `.scratch/{c1-*,pin-*,r48-*,r48w2-*}` directories (12/41/32/29) of seat-run debris (`corpus/lessons/round-48-verifier-spotcheck.md:20`, defects at `:23-25`, routed defect 1 at `:100`) | none — QUALITY 80 carries the pathspec `.ufo/waves/round-<N>/` (`corpus/QUALITY.md:368-372`), and `tools/mori-unlanded-check.py:15` excludes `.scratch/` "on purpose" | `.gitignore` entry plus a round-end removal (contract, "Round-48 routed defects carried"). **Not yet shown** at the entering tip: `git show b3e3453d:.gitignore` lists four entries (`.ufo/interactive-sessions/`, `.ufo/worktrees/`, `__pycache__/`, `*.pyc`) and no `.scratch`; `git diff b3e3453d -- .gitignore tools/mori-unlanded-check.py` is empty; the class has grown — `find .scratch -mindepth 1 -maxdepth 1 -type d` → 184, of which 120 carry a round-48 prefix with an mtime before the freeze commit `0df17b7b` (2026-10-25T21:36:32-03:00), the excess over the closure's 114 coming from counter-run scratch (`count-c1.py:332` makes `c1-*` under `.scratch`; `tools/mori-pin-check.py:405` makes `pin-tmp-*`) |
| M3 | landing | Round 48's filed report commit `e60eb16757781b9303b90e6d6972b2b8953d6d86` (fleet repo) has **author** date `2026-10-25T20:22:17-03:00` while it cites lane commit `14c5110d65a2f225e7316e1996e92090b9b8e7cb` authored `2026-10-25T20:26:17-03:00`; only its committer date (`20:27:04`) is after the tip (`corpus/lessons/round-48-verifier-spotcheck.md:23-26`, routed defect 2 at `:101`) | none — no QUALITY criterion reads a commit's author date; the nearest, 75, states the limit outright: "both times are lane-written (a backdated commit passes)" (`QUALITY.md:329-336`, the clause at `:333`) | File the report with an author date at or after the lane tip it cites. **Not yet shown** — there is no instrument for it and this round's report does not exist yet; the observable is `git -C /home/vgpnk/Projects/shokunin log -1 --format='%aI %cI' <report commit>` against the cited tip's `%aI` |
| M4 | survivor | Seven of fourteen new junk probes printed `PIN_CHECK=met` exit 0 against the landed v3 at `e4dfff32`: `v1_html_comment`, `v2_zwsp_header_prefix`, `v3b_tab_fence`, `v4_fourspace`, `v6_dup_authority`, `v7_split_tally`, `v8_html_table`, while P-C1 stayed `C1=met` (`.ufo/waves/round-48/w2/R48CritV3Junk1.md:13-19`, table at `:62-75`, "Seven survivors, seven caught" at `:77`, repair set at `:451-476`) | none — QUALITY 125's check is `hidden=0 unparsed=0`, which is exactly what each survivor printed (`R48CritV3Junk1.md:62,64,68,69,73,74,75`), and QUALITY 126's check is `junk_met=0` over the eight J edits only, so no criterion's check goes red on these shapes | The seven shapes enter this round's frozen counter as N1–N7 (`count-c1.py:20-26` and `NEW_VARIANTS` at `:206-209`), so the landed tool must score each `unmet`. **Shown able to fail**: the entering tool (`controls/tool-v3-entering.py`, sha256 `85a89a3b…` = `tools/mori-pin-check.py` at `b3e3453d`) prints `C1=unmet junk_met=9 honest_unmet=0 real=met errors=0 variants=26`, with N1–N7 and N9 `got=met rc=0` (`evidence/control-c1-tool-v3-entering.txt`, exit 1); the five round-48 surface rules alone leave `junk_met=1` (N9, `evidence/control-c1-tool-r48-surface-fixes.txt`, exit 1). **Not yet shown**: no repaired tool has landed — `sha256sum tools/mori-pin-check.py` is still `85a89a3b6ba4eb5ed0b3f784763cfe78652e6493b055b3dcf8924feaffff82e1`, `git diff b3e3453d -- tools/ SKILL.md` is empty, and `ls .ufo/waves/round-49/evidence/` holds no `after-c1` receipt; the target is `C1=met … variants=26` at the landed tip |
```

## 2. Captured-by check (QUALITY 115-128 read directly)

Read `corpus/QUALITY.md:925-1087`; criteria 115–128 occupy `:938-1087` (the numbers are criterion
numbers, not line numbers). Relevant candidates and why each row's cell is `none`:

| criterion | what its check would have to see | why it does not capture the row |
|---|---|---|
| 80 (`:368-372`) | `git status --porcelain --untracked-files=all -- .ufo/waves/round-<N>/` prints nothing | pathspec excludes `.scratch/`; M2's directories are outside it |
| 75 (`:329-336`) | wave `at` times vs dispatch commits | its own limit line (`:333`) admits "a backdated commit passes"; M3's author-date defect is a report commit, not a wave row |
| 125 (`:1052-1061`) | `hidden=0 unparsed=0` from the pin checker | the seven M4 survivors printed `hidden=0 unparsed=0` (`R48CritV3Junk1.md:62-75`), i.e. the check was green on them |
| 126 (`:1062-1069`) | `junk_met=0` over the counter's frozen J set, and tool bytes with no variant/scratch-name branch | the J-only set is green while N1–N7 survive (M4); for M1 the reviewer records that 126 is tool-scoped and the harness still leaked both channels (`w2/R48RevQuality.md:71-73`) |

`corpus/lessons/round-48.md:111-117` rows M1, M3, M4, M5, M6, M7 are **not** carried into this table:
M1/M5 were fixed by `tools/mori-unlanded-check.py`, M3 by v3 R9/R10 with D7 routed, M4 by the R6 pin
repair, M6 by unique wave-2 seat names plus this round's `Mo49*` names, M7 by the erratum at
`corpus/lessons/round-48.md:150-153`.

## 3. Evidence read (command → output → exit)

Read-only git, all run in `/home/vgpnk/Projects/shokunin/mori-shokunin` unless noted:

```
$ git log -1 --format='%H%nauthor=%an %aI%ncommitter=%cn %cI' 14c5110d
14c5110d65a2f225e7316e1996e92090b9b8e7cb
author=mori-shokunin 2026-10-25T20:26:17-03:00
committer=mori-shokunin 2026-10-25T20:26:18-03:00      exit 0
$ git log -1 --format='%H %aI' b3e3453d
b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 2026-10-25T20:30:51-03:00      exit 0
$ git log -1 --format='freeze=%H %cI' 0df17b7b
freeze=0df17b7b4e667dd0aaaef0adc7d7d9973e6aa115 2026-10-25T21:36:32-03:00      exit 0
$ cd /home/vgpnk/Projects/shokunin && git log -1 --format='%H%nauthor=%an %aI%ncommitter=%cn %cI%n%s' e60eb167
e60eb16757781b9303b90e6d6972b2b8953d6d86
author=mori-shokunin 2026-10-25T20:22:17-03:00
committer=mori-shokunin 2026-10-25T20:27:04-03:00
round-48: mori report                                    exit 0
$ git show b3e3453d:.gitignore
.ufo/interactive-sessions/
.ufo/worktrees/
__pycache__/
*.pyc                                                    exit 0
$ git diff --stat b3e3453d -- .gitignore tools/mori-unlanded-check.py
(no output)                                              exit 0
$ git diff --stat b3e3453d -- tools/ SKILL.md corpus/
 corpus/evidence/sources-r49/host-journal-reach.txt      |  98 ++++++
 corpus/evidence/sources-r49/journalctl.1.html           | 463 ++++++++++++++++++++
 corpus/evidence/sources-r49/journald.conf.5.html        | 322 ++++++++++++++++++
 corpus/evidence/sources-r49/systemd-journald.service.8.html | 189 +++++++
 4 files changed, 1072 insertions(+)                       exit 0
$ sha256sum tools/mori-pin-check.py
85a89a3b6ba4eb5ed0b3f784763cfe78652e6493b055b3dcf8924feaffff82e1  tools/mori-pin-check.py   exit 0
$ find .scratch -mindepth 1 -maxdepth 1 -type d | wc -l                     → 184
$ find .scratch -mindepth 1 -maxdepth 1 -type d ! -newermt '2026-10-25T21:36:32-03:00' | wc -l → 132
$ find .scratch -mindepth 1 -maxdepth 1 -type d -newermt '2026-10-25T21:36:32-03:00'  | wc -l → 52
$ find .scratch ... ! -newermt <freeze> \( -name 'c1-*' -o -name 'pin-*' -o -name 'r48-*' -o -name 'r48w2-*' \) | wc -l → 120
$ git ls-files --others --directory -- .scratch | wc -l                     → 173 (grew to 184 by the find above; seats still running)
```

Committed receipts opened (verdict line quoted verbatim; trailing `exit=N` line is the receipt's own):

```
evidence/control-c1-sniffer-under-r48-counter.txt
  C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=12 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86
  exit=0
evidence/control-c1-stub-filename-sniffer.txt
  C1=unmet junk_met=18 honest_unmet=0 real=met errors=0 variants=26 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86
  exit=1   (N1-N10 and J1-J8 all got=met)
evidence/control-c1-tool-v3-entering.txt
  C1=unmet junk_met=9 honest_unmet=0 real=met errors=0 variants=26 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86
  exit=1   (N1-N9 got=met; N10 unmet)
evidence/control-c1-tool-r48-surface-fixes.txt
  C1=unmet junk_met=1 honest_unmet=0 real=met errors=0 variants=26 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86
  exit=1   (N9 got=met)
evidence/selftest-c1.txt
  PASS handles_carry_no_variant_name  []
  PASS filename_sniffer_not_met  C1=unmet junk_met=17 … variants=24 …
  C1_SELFTEST pass=44 fail=0
```

Counter/source readings, not runs: `.ufo/waves/round-49/count-c1.py:216-229` (opaque tag, neutral
`TMPDIR`, hash-ordered jobs at `:275`), `:332` (`mkdtemp(prefix="c1-", dir=<repo>/.scratch)`),
`.ufo/waves/round-48/count-c1.py:238,247` (the two leaked names),
`tools/mori-pin-check.py:405` (`mkdtemp(prefix="pin-tmp-", dir=tmp_parent)`),
`tools/mori-unlanded-check.py:15` (`.scratch` outside scope "on purpose").

## 4. Known limits of this report

- Nothing was executed except reads and `find`/`wc`: no counter run, no pin-check run, no clone. The
  fix columns for M1 and M4 therefore rest on committed receipts, not on a fresh measurement.
- The `.scratch` counts are a moving target while seats run; the numbers above are one read, and the
  prefix split (120) exceeds the closure's 114 without proof of which dirs are new — the two
  instrument lines that create such dirs are named, the difference is not resolved.
- `tools/mori-pin-check.py` was `85a89a3b…` at read time; if a C1 executor lands the tool before
  integration, M4's "not yet shown" must be re-read, not copied.
- The seat did not check whether the L1 intends further `## Mistakes` rows from round-49 evidence
  itself; this draft covers only the four carried rows named in the assignment.

## Findings

- **MED** — `.scratch/` residue is carried with no remediation landed: `.gitignore` at `b3e3453d` has
  no `.scratch` entry, `tools/mori-unlanded-check.py:15` excludes it by design, and the count stands
  at 184 directories (120 round-48-prefixed with pre-freeze mtime). Files: `.gitignore`,
  `tools/mori-unlanded-check.py:15`; pointer `corpus/lessons/round-48-verifier-spotcheck.md:20,23-25,100`.
- **MED** — the report author-date defect (M3) has neither a QUALITY criterion nor an instrument, and
  QUALITY 75's own text admits a backdated commit passes (`corpus/QUALITY.md:333`); the only future
  observable is a hand comparison of `%aI` between the report commit and the tip it cites. File:
  `corpus/lessons/round-48-verifier-spotcheck.md:23-26`.
- **MED** — the seven v3 survivor shapes are now scored as N1–N7 but the target remains unproven:
  `tools/mori-pin-check.py` is still the entering v3 (`85a89a3b…`), `git diff b3e3453d -- tools/
  SKILL.md` is empty, and `.ufo/waves/round-49/evidence/` has no `after-c1` receipt. File:
  `tools/mori-pin-check.py`; receipt `evidence/control-c1-tool-v3-entering.txt`.
- **LOW** — the round-48 closure's 114 and this read's 120/184 for the same class are not comparable
  without a timestamp and prefix scope, because counter-run scratch keeps being created under
  `.scratch` (`count-c1.py:332`, `tools/mori-pin-check.py:405`). File:
  `corpus/lessons/round-48-verifier-spotcheck.md:20`.
- **LOW** — QUALITY 126's harness-leak clause is tool-scoped (`w2/R48RevQuality.md:71-73`), so the
  *counter*-side handle rule that closes M1 (opaque names, hash order, no name in `TMPDIR`) is
  enforced only by this round's counter code and its selftest arm, not by any criterion check. File:
  `corpus/QUALITY.md:1062-1069`; code `count-c1.py:216-221,374-376`.
