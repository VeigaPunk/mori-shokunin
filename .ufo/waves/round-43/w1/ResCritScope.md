# ResCritScope — round-43 residual attack on the scope bound

Seat: w1 residual critic (leaf, no dispatch). Date: 2026-10-25T01:54Z (audit window began 2026-10-24T22:46Z).
Scope bound under attack: the round-43 diff of mori-shokunin vs `master`, excluding `.ufo/waves/round-43/w1`, grepped for
`systemctl | vacuum | pacman | kill | reset-failed | rm -rf | service`. Any host mutation = FAIL.

## What the bound did during the audit (moving target — three timepoints)

1. T1 22:46Z — `git diff master --stat -- . ':!.ufo/waves/round-43/w1'`: 4 files, 25 insertions
   (SCORECARD.md, corpus/QUALITY.md, corpus/README.md, corpus/SOURCES.md). 60 diff lines.
2. T2 ~22:47Z — canonical grep on the live diff: **5 matches, all prose** (verbatim below).
3. T3 22:48Z — commit `dde525ea` "round-43: successor operability counter (C1S), calibration repair (C2),
   one-theme assimilation" landed on master while the audit ran. The identical canonical command then
   returned an **empty diff** (0 lines, `grep_exit=1`) — the bound stopped seeing the round's content the
   moment it was committed. Committed range `e3a2b58f..master`: 171 files, 30,052 insertions, including
   `count-c1s.py` (172 lines), `count-c2.py` (91), `assimilation/validate/tools/mori-disk-rate.py` (300).

## T2 canonical grep (pre-commit, verbatim)

Command: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff master -- . ':!.ufo/waves/round-43/w1' | grep -nE 'systemctl|vacuum|pacman|kill|reset-failed|rm -rf|service'`

```
52:+  `systemctl reset-failed` recheck is host mutation; S351 `journalctl(1)` —
112:+Resource-runway ground the map did not hold as a core reading: `journalctl --disk-usage` is a total over archived and active files the command can see, not a per-journal share (`knowledge/journal-disk-usage-total-r51.md`, S470, page re-opened 2026-10-24). A live read-only invocation printed `Archived and active journals take up 269M in the file system.` No vacuum, rotate, or journald change. Two assimilation entries on adjacent ground were refused (campaign file:// plus a MESSAGE grep; `reset-failed` host mutation) — reasons and flips in `corpus/lessons/round-43.md`.
119: | S262 | ROMA: ... an OOM can kill a co-located service and leave shared memory, message queues, semaphores and tmpfs unreclaimed — per the authors' abstract | ...
123:+| S350 | systemd.scope(5) — ... REJECTED: the staged failed-scope entry grounds its recheck in systemctl reset-failed after creating a scope, a host mutation outside mori's detection-and-report province; flip: a read-only MemoryMax show of an already-failed scope, with no reset-failed and no scope creation | rejected | ...
124:+| S351 | journalctl(1) — ... --vacuum-size= removes the oldest archived journal files until the disk space they use falls below the specified size ... REJECTED ... | rejected | ...
```

Classification: lines 52/112/123/124 are refusal records that *name* refused host mutations; 119 is a
context line quoting a paper abstract ("can kill a co-located service"). No executable vector.

## T3+ committed-range audit (the content the bound went blind to)

Command: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff e3a2b58f master -- . ':!.ufo/waves/round-43/w1' > /tmp/rescrit_r43c.diff` (31,096 lines), then per-term counts over all added lines:

```
systemctl      29
vacuum         47
pacman         28
kill           908
reset-failed   19
rm -rf         1
service        175
```

Every hit inspected; classification:

- Prose/refusal records: lessons and SOURCES rows naming `systemctl --user reset-failed` and
  `--vacuum-size=` **as rejected** host mutations (S350/S351, `corpus/lessons/round-43.md`).
- Read-only queries quoted as census receipts: `systemctl show|is-active|is-enabled`,
  `pacman -Q|-Qi`, `journalctl --disk-usage`, `journalctl -k ... --grep ... | wc -l`.
- Vocabulary: "kill" (908) is OOM/SIGKILL/"Killed process"/"skill" terminology in knowledge docs;
  "service" (175) is unit vocabulary and the journal name "Services Computing".
- `pacman -Syu` / `pacman -U` mentions describe past `/var/log/pacman.log` records, detection only.

### Strongest counterexample tried — the one executable `rm -rf`

Diff line 11091, inside `.ufo/waves/round-43/assimilation/validate/corpus/knowledge/progressing-weak-r2.md`
(an embedded check block a future seat may extract to /tmp and run):

```
303:WORK=$(mktemp -d /tmp/mori-authorship-check.XXXXXX)
304:export MORI_PR_WORK=$WORK
305:trap 'rm -rf -- "${MORI_PR_WORK:-}"' EXIT INT TERM
```

Adjudication: `rm -rf` is scoped to the block's own `mktemp -d` directory under `/tmp`, quoted, `--`-guarded,
`-f` makes the unset-variable empty-operand a no-op. Self-cleanup of a /tmp sandbox — compliant with lane
bounds, not a host mutation. ATTACK REJECTED.

### Runtime surface of the three committed scripts

- `count-c1s.py`: subprocess targets are `git -C LANE show rev:path` (read-only) and the conform checker in
  `--selftest` mode against a scratch clone; it temporarily rewrites the v5 checker bytes for mutant arms and
  restores them (repo-file round-trip, not host state). "kill" appears only as `mutant_kill_*` check names.
- `count-c2.py`: one `subprocess.run`, same read-only pattern.
- `assimilation/validate/tools/mori-disk-rate.py`: `os.open(path, os.O_RDONLY)` only; stdout writes only.

## Findings

1. **Substance: clean.** Zero executable host-mutation vectors in the round-43 diff at any timepoint.
   The round's own refusal records (S350 reset-failed, S351 vacuum) are the diff's only mutation-adjacent
   text, and they reject those moves.
2. **Defect in the bound itself (fixable, not a round-killer):** `git diff master` is time-of-day sensitive.
   After the round commits to master, the assigned command inspects an empty diff and can never FAIL
   anything — a tripwire that goes no-op exactly when the work lands. Smallest safe correction: run the
   same term grep against the committed round range (`git diff <entering-tip> master`, here
   `e3a2b58f..master`) and re-run after each commit; the T3 committed-range audit above is that correction,
   executed.
3. Cosmetic: `git rev-parse --short master HEAD` (chained) errored "Needed a single revision" in this
   session while each rev resolves individually; the substantive diff/grep commands were unaffected.

Frozen counters untouched (scratch copies and `git show` only); no lane Git/jj/index mutation; no writes
outside this report file and /tmp scratch (`/tmp/rescrit_r43.diff`, `/tmp/rescrit_r43b.diff`,
`/tmp/rescrit_r43c.diff`).

VERDICT: SURVIVED
Command: git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff master -- . ':!.ufo/waves/round-43/w1' | grep -nE 'systemctl|vacuum|pacman|kill|reset-failed|rm -rf|service'
Output: (no lines; grep exit code 1 — diff vs master is empty at final run 2026-10-25T01:54:32Z, master=dde525ea, because the round-43 work was committed mid-audit; the pre-commit run of the identical command returned the 5 prose matches pasted verbatim above, and the committed-range re-audit e3a2b58f..master found 0 executable host-mutation vectors)
