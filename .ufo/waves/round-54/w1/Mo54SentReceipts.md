# Mo54SentReceipts — receipt integrity (round 54, wave w1)

Seat: sentinel, receipt integrity. Lane `mori-shokunin` at
`2d0347a3` (freeze `6830f3af`, data `1116c092` / `78295c76`, wave spec `2d0347a3`).
Scope: every file under `.ufo/waves/round-54/evidence/` — does it record the literal command it ran and its exit
code, and do the cheap commands reproduce their verdict line. Freeze manifest checked against
`6830f3af992d906bfa1e17e3743e631ab834f67c` bytes.

Host: read-only. No sysctl, no cgroup, no memory-failure injection, no kernel module, no pacman. No tool installed
or upgraded in this seat (nothing was needed). Scratch: `/fast/scratch/hyaku/mori-r54/Mo54SentReceipts/`,
removed at the end; one `git clone --shared` of the lane (toplevel asserted before the single commit there).

Two words that the vote counters read at line start are never used at line start in this report.

---

## 1. Inventory — 27 files

Anchor column: the commit whose tree holds the file (`F` = `6830f3af`, `D` = `78295c76`; the two at-data receipts
landed at `2d0347a3`; two files are worktree-only). "cmd" = a literal command on its own line (`command:` or a
`$ ` line); "exit" = an `exit=N` line or an explicit `$?` reading.

| file | anchor | cmd | exit | reproduced |
|---|---|---|---|---|
| c1-at-data.txt | D→2d0347a3 | yes (`command: python3 .ufo/waves/round-54/count-c1.py 78295c76…`) | yes `exit=1` | **yes**, byte-identical verdict, exit 1 |
| c2-at-data.txt | D→2d0347a3 | yes (same shape) | yes `exit=1` | **yes**, byte-identical verdict, exit 1 |
| c1-scope.txt | F | no | yes `exit=0` | **yes** (`count-c1.py --scope`), 32 lines identical, exit 0 |
| c2-claims.txt | D | no (data listing) | no | **yes** (21 hashes = `count-c2.py --hashes 78295c76`) |
| c1-claims.txt | D | no (data listing) | no | **yes** (31 hashes = `c1-scope.txt` set; 31 `v7.2-source` + `v7.3 copy` pairs) |
| census-start.txt | F | no | yes `exit=0` | **yes** (`bash scripts/sources-census.sh validate mori`), 24 lines identical, exit 0, 23 W04 |
| control-c1-do-nothing.txt | F | yes | yes `exit=1` | **yes**, identical verdict line |
| control-c2-do-nothing.txt | F | yes | yes `exit=1` | **yes**, identical verdict line |
| control-c1-copies-only.txt | F | yes | yes `exit=1` | **yes** (own clone, frozen overlay), identical verdict |
| control-c2-copies-only.txt | F | yes | yes `exit=1` | **yes** (same base commit), identical verdict |
| control-c1-no-votes.txt | F | yes | yes `exit=1` | not run — control commit gone |
| control-c1-no-line.txt | F | yes | yes `exit=1` | not run — control commit gone |
| control-c1-unsettled.txt | F | yes | yes `exit=1` | not run — control commit gone |
| control-c1-v72-copies.txt | F | yes | yes `exit=1` | not run — control commit gone |
| control-c1-witness.txt | F | yes | yes `exit=0` | not run — control commit gone |
| control-c2-no-votes.txt | F | yes | yes `exit=1` | not run — control commit gone |
| control-c2-quote-echo.txt | F | yes | yes `exit=1` | not run — control commit gone |
| control-c2-unlocated.txt | F | yes | yes `exit=1` | not run — control commit gone |
| control-c2-two-sources.txt | F | yes | yes `exit=1` | not run — control commit gone |
| control-c2-witness.txt | F | yes | yes `exit=0` | not run — control commit gone |
| selftest-c1.txt | F | **no** | yes `exit=0` | **yes** (`count-c1.py --selftest`), 57 pass/0 fail, identical |
| selftest-c2.txt | F | **no** | yes `exit=0` | **yes** (`count-c2.py --selftest`), 54 pass/0 fail, identical |
| sweeps.txt | F | 7 `$ ` lines, two labelled with `(exit=0)`; **no** per-command exit | partial | 5 of 7 reproduce; 1 does not; 1 not run |
| d3-relocation.txt | D | **no** | **no** | results verified (8/8 sha256, strays absent) |
| freeze-sha256.txt | F | no (manifest) | no | **yes**, 37/37 hashes match `6830f3af` bytes |
| gate-rejects.txt | worktree only | 5 `$ ` lines | **no** | fetch reproduced (sha256 + count) |
| receipt-stage-before.txt | worktree only | yes | yes `exit=1` | **not reproducible** — script absent at every rev |

Totals: 16 of 27 record a literal command with an exit code (2 at-data + 14 controls); 4 record an exit code but no
command (c1-scope, census-start, both selftests); 3 record `$ ` commands without exit codes (sweeps, gate-rejects,
and the label-prefixed sweep line inside sweeps); 4 record neither (c1-claims, c2-claims, d3-relocation,
freeze-sha256) — those four are data listings, not command receipts.

---

## 2. Freeze manifest against `6830f3af`

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin
$ F=6830f3af992d906bfa1e17e3743e631ab834f67c
$ while read -r h p; do a=$(git show "$F:$p" | sha256sum | cut -d' ' -f1); [ "$a" = "$h" ] && echo "OK $p" || echo "MISMATCH $p"; done < <(git show "$F:.ufo/waves/round-54/evidence/freeze-sha256.txt")
OK   … (37 lines, 37 OK, 0 MISMATCH)
exit=0
```

`manifest entries: 37`; freeze-commit files under `.ufo/waves/round-54/`: 26. Set difference:

```
NOT pinned: ['.ufo/waves/round-54/evidence/census-start.txt',
             '.ufo/waves/round-54/evidence/freeze-sha256.txt',
             '.ufo/waves/round-54/evidence/sweeps.txt']
pinned but absent: []
```

(`freeze-sha256.txt` cannot pin itself; the other two are the finding F3 below.)

Worktree bytes of every frozen file equal the freeze bytes (`count-c1.py`, `count-c2.py`, `controls/*.py`,
`contract.md` re-hashed: identical), so the claim is measured with the frozen bytes under either reading.

Server-side provenance, two independent re-fetches from git.kernel.org cgit at `?h=v7.3`:

```
$ curl -fsS -o memory-failure.c.v7.3 '…/plain/mm/memory-failure.c?h=v7.3'
bytes=82847 sha=94d24a605b61f94ad1d10ab3db26aed12cb6113af15431ff873da5b98ca48003   (= pin)
$ curl -fsS -o errno.h.v7.3 '…/plain/include/uapi/asm-generic/errno.h?h=v7.3'
bytes=5826  sha=66a5ad60566fdd62e41701bcfc42bfeca5e5696ad1d47d78981575e0c51622be   (= pin)
```

Also `curl …include/ras/ras_event.h?h=v7.3` → `bytes=11341 sha256=408ddc2a…` (matches `gate-rejects.txt`) and
`grep -c 'TRACE_EVENT(memory_failure_event' ras_event.h` → `0`, which is the exclusion that receipt records.

---

## 3. Reproduction log (literal command, output, exit)

All run from the lane root unless stated; `-B` suppresses bytecode only.

```
$ python3 -B .ufo/waves/round-54/count-c1.py 78295c764093ff1f6cee08d7246679900bde7265
C1=unmet scope=31 rows=31 matched=31 status_ok=31 line_ok=31 quote_ok=31 source_rows=ok pins=ok provenance=ok held=31 absent=0 holds=31 changed=0 voted=0 dissent=0 rev=78295c764093ff1f6cee08d7246679900bde7265 failed=votes
exit=1                      (= c1-at-data.txt verdict line, and its exit)
```

```
$ python3 -B .ufo/waves/round-54/count-c2.py 78295c764093ff1f6cee08d7246679900bde7265
C2=unmet claims=21 located=21 quote_missing=0 bad_rows=0 sources=6 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 rev=78295c764093ff1f6cee08d7246679900bde7265 failed=entailment
exit=1                      (= c2-at-data.txt verdict line, and its exit)
```

```
$ python3 -B .ufo/waves/round-54/count-c1.py --selftest | diff - <(git show 6830f3af:.ufo/waves/round-54/evidence/selftest-c1.txt)
58a59
> exit=0                      (the receipt's exit trailer only)
exit=0     C1_SELFTEST pass=57 fail=0
$ python3 -B .ufo/waves/round-54/count-c2.py --selftest | diff - <(git show 6830f3af:…/selftest-c2.txt)
55a56
> exit=0
exit=0     C2_SELFTEST pass=54 fail=0
```

```
$ python3 -B .ufo/waves/round-54/count-c1.py --scope | diff - <(git show 6830f3af:…/c1-scope.txt)
32a33
> exit=0
exit=0                      (31 scope rows + scope=31, identical)
```

```
$ bash scripts/sources-census.sh validate mori | diff - <(git show 6830f3af:…/census-start.txt)
24a25
> exit=0
exit=0                      (23 W04 rows, ok line, identical)
```

Do-nothing controls, reproduced against the lane itself (the control's `--repo` clone was just the entering tip):

```
$ python3 -B .ufo/waves/round-54/count-c1.py --repo /home/vgpnk/Projects/shokunin/mori-shokunin 39dcf4d7e410d362781a47e8365ca23b5c807598
C1=unmet scope=31 rows=0 matched=0 status_ok=0 line_ok=0 quote_ok=0 source_rows=bad pins=bad provenance=bad held=0 absent=0 holds=0 changed=0 voted=0 dissent=0 rev=39dcf4d7… failed=ledger_absent,pins
exit=1
$ python3 -B .ufo/waves/round-54/count-c2.py --repo … 39dcf4d7…
C2=unmet claims=0 located=0 quote_missing=0 bad_rows=0 sources=0 source_rows=bad pins=bad provenance=bad entailed=0 dissent=0 rev=39dcf4d7… failed=entry_absent,pins
exit=1
```

Copies-only controls, one clone (`--shared`, toplevel asserted, one commit inside it):

```
$ git clone -q --shared --no-checkout LANE $S/clone && git -C $S/clone rev-parse --show-toplevel
/fast/scratch/hyaku/mori-r54/Mo54SentReceipts/clone
$ git -C $S/clone checkout -q --detach 39dcf4d7…    # + the five frozen overlay files + sources-r54/
$ git -C $S/clone commit … -> base=9fc84de6d89101ce4473c26e21aec4346fd81b7d
$ python3 -B count-c1.py --repo $S/clone 9fc84de6
C1=unmet scope=31 rows=0 … pins=ok provenance=bad … voted=0 dissent=0 rev=9fc84de6 failed=ledger_absent
exit=1                      (verdict identical to control-c1-copies-only.txt modulo rev)
$ python3 -B count-c2.py --repo $S/clone 9fc84de6
C2=unmet claims=0 located=0 quote_missing=0 bad_rows=0 sources=0 source_rows=bad pins=ok provenance=bad entailed=0 dissent=0 rev=9fc84de6 failed=entry_absent
exit=1                      (identical to control-c2-copies-only.txt modulo rev)
```

Sweeps, command by command:

```
$ git grep -ilE "memory.failure|hwpoison|HardwareCorrupted|BUS_MCEERR" 39dcf4d7 -- corpus/knowledge SKILL.md PROVINCE.md tools
39dcf4d7:corpus/knowledge/kernel-v7.3-recheck-r53.md        exit=0   (identical)
$ git grep -cE "memory_failure|hwpoison" 39dcf4d7 -- corpus/knowledge/kernel-v7.3-recheck-r53.md
39dcf4d7:corpus/knowledge/kernel-v7.3-recheck-r53.md:2      exit=0   (identical)
$ grep -n panic_on_unrecoverable corpus/SOURCES.md          (worktree, today)
286:… / 362:… / 367:…    exit=0     (receipt records 286 and 353)
$ git show 6830f3af:corpus/SOURCES.md | grep -n panic_on_unrecoverable | cut -c1-90
286:| S507 | … / 353:- (round 53) `panic_on_unrecoverable_memory_failure` …   (identical at the freeze rev)
$ uname -r; sysfs /proc read
7.2.11-arch1-1
node0/{delayed,failed,ignored,recovered,total}=0,0,0,0,0
HardwareCorrupted:     0 kB
memory_failure_early_kill: 0 / memory_failure_recovery: 1 / enable_soft_offline: 1
cat: /proc/sys/vm/panic_on_unrecoverable_memory_failure: No such file or directory   (identical)
$ git show 6830f3af:corpus/SOURCES.md | grep -oE "^\| S[0-9]+" | tail -1 ; grep -cE "^\| S[0-9]+"
| S514   287                                                  (identical)
$ grep -rliE "memory.failure|hwpoison|SIGBUS|memcontrol|percpu_counter|EDQUOT|v7\.3" /home/vgpnk/Projects/shokuknow/merge/mori | wc -l
3                     exit=0        (receipt records 0)   <-- does not reproduce
$ git ls-remote https://github.com/torvalds/linux refs/tags/v7.3 'refs/tags/v7.3^{}'
(no output; the command hit a 300 s timeout)                 <-- not reproduced (network)
```

D3 relocation, results checked directly (the receipt records results, not a command):

```
sha256 of every relocated file == the receipt's value (8/8; e.g. oom_kill.c 452f1348… f756b4e, 0 b24122a0… c3a078)
lane root: 0 base.c main.c meminfo.c oom_kill.c sd-main.c user@.service.in MANPAGE.md -> all absent (worktree and HEAD)
'--repo': No such file or directory ; git ls-files -- '--repo' | wc -l -> 0
```

Assimilation sweep, per term over the same path (to size the miss):

```
memory.failure files=0  hwpoison files=0  SIGBUS files=0  percpu_counter files=0  v7\.3 files=0
memcontrol files=1      EDQUOT files=3 (12 occurrences)
matching files: knowledge/corpus/knowledge/quota-observability-r38.md (7 hits),
                knowledge/corpus/knowledge/quota-path-listing-r42.md (1), SOURCES.append.md (3)
tree unchanged since 2026-10-24 23:33 (find -newermt 2026-10-26 -> 0 files)
```

Control commits, reachability in the lane repo (`git cat-file -t` on each rev named by the receipts):

```
a6888a07… / e79f525f… / 9c52523b… / 6f4c148c… / 34b544d8… / f5b7a8c9…
ed10983d… / c3a724f9… / bd730353… / fa9e03bd… / 1fc15204… / d99c87a9…
-> all: fatal: git cat-file: could not get object info
39dcf4d7… -> commit
/fast/scratch/hyaku/mori-r54/l1/controls -> No such file or directory
```

---

## Findings

**F1 — MED.** `evidence/sweeps.txt`, the assimilation-sweep block (line reading
`$ assimilation sweep: grep -rliE … /home/vgpnk/Projects/shokuknow/merge/mori | wc -l` → `0`). Re-running the
recorded command yields `3`, not `0`: `merge/mori/knowledge/corpus/knowledge/quota-observability-r38.md` (7 hits,
EDQUOT/v7.2 errno material), `…/quota-path-listing-r42.md` (1), `merge/mori/SOURCES.append.md` (3). The tree has
not changed since 2026-10-24 23:33, so this is not drift. The frozen contract sentence built on it
(`contract.md`, "Assimilation: none — `merge/mori/` holds 0 files naming memory failure, hwpoison, SIGBUS,
percpu_counter or v7.3") survives *for those five terms taken singly* (each 0 files, measured above), but the
receipt's recorded output is false as written and no reader can tell which terms were actually measured. The
sweep line is also not a runnable command (it carries the label `assimilation sweep:` after `$`). Neither counter
reads `merge/`, so no claim score depends on it; the contract prose overstates a clean merge surface by hiding the
lane's own quota/EDQUOT entries. Route: round-55 item (contract prose is frozen this round).

**F2 — MED.** All fourteen control receipts name a `--repo` path under
`/fast/scratch/hyaku/mori-r54/l1/controls/`, and that directory is gone (`No such file or directory`). Twelve of
them name a rev that exists in no repository at all — `git cat-file -t` returns `could not get object info` for
`a6888a07`, `e79f525f`, `9c52523b`, `6f4c148c`, `34b544d8`, `f5b7a8c9`, `ed10983d`, `c3a724f9`, `bd730353`,
`fa9e03bd`, `1fc15204`, `d99c87a9` — i.e. every control except the do-nothing pair, which pins the entering tip
`39dcf4d7` (reachable). Those twelve receipts are assertions, not reproducible measurements; only four readings
could be re-derived (§3, all four identical): the two do-nothing ones from the lane itself, and the two copies-only
ones, whose base is fully determined by the entering tip plus the frozen overlay even though their recorded base
commits are gone. `contract.md` discloses the removal ("the control commits live only in those clones"),
so this is a named limit rather than a misstatement — but the round's control table rests on 10 unanchorable
numbers. Smallest remediation for round 55: have `controls.py` print each control commit's `git bundle` hash or
record the control commit tree hash plus the base tree hash, so a reader can at least detect a different run.

**F3 — MED.** `evidence/freeze-sha256.txt` (37 entries) does not pin `evidence/census-start.txt` or
`evidence/sweeps.txt`, although `contract.md` names both as landing in the freeze commit and states "Frozen bytes
are listed with sha256 in `evidence/freeze-sha256.txt`". Consequence: the two files that carry the round's census
and the claim-supporting sweeps can be edited in place without detection — and F1 shows one of them already
disagrees with its own re-run. Smallest remediation: extend the manifest (a second freeze commit with only new
pins is enough; no counter reads the manifest's coverage).

**F4 — LOW.** `evidence/selftest-c1.txt` and `evidence/selftest-c2.txt` record `exit=0` and 57/54 PASS lines but no
literal command. Both reproduce exactly with `python3 -B .ufo/waves/round-54/count-c{1,2}.py --selftest` (§3), the
invocation being inferable only from the counters' `Usage:` line. Adding the command line would make them
self-contained.

**F5 — LOW.** `evidence/census-start.txt` records no command (only output and `exit=0`). The command is
`bash scripts/sources-census.sh validate mori`; re-run today it returns exit 0 with 24 identical lines, so the
reading is sound — the receipt just does not name it, and `contract.md`'s "same command" for the round end has no
antecedent in the file.

**F6 — LOW.** `evidence/sweeps.txt`: of seven `$ ` lines only two carry an exit annotation (`(exit=0)`), one has
the command label in front of the command, and the `grep -n panic_on_unrecoverable corpus/SOURCES.md` line reads
the working tree with no revision anchor — it reproduces at `6830f3af` (286/353) but not on today's worktree
(286/362/367), so the receipt cannot be re-checked without knowing the rev. The `git ls-remote` line was not
reproduced here (300 s network timeout); the tag ids it records are consistent with the frozen copies but remain
UNVERIFIED from this seat.

**F7 — LOW.** `evidence/d3-relocation.txt` records results only — no command and no exit code. The results
themselves verify (8/8 sha256 match, all eight lane-root strays absent at HEAD and in the worktree, `--repo/`
gone, 0 tracked paths), so the receipt is accurate but not re-runnable.

**F8 — LOW.** `evidence/receipt-stage-before.txt` (worktree-only, untracked) records
`python3 .ufo/waves/round-54/checks/receipt-stage.py 39dcf4d7…` with `exit=1`, but that script exists at none of
`39dcf4d7`, `6830f3af`, `78295c76`, `2d0347a3` (`git cat-file -e … -> ABSENT` at all four). Until `checks/` is
landed, the receipt's 5 FLAG lines about rounds 50/53 citing intermediate receipts cannot be re-derived by anyone.

**F9 — LOW.** `evidence/gate-rejects.txt` (worktree-only, untracked) records five `$ ` commands and no exit code,
and the `grep -c` line's argument (`ras_event.h.v7.3`) does not match the file name in its own output
(`include_ras_ras_event.h.v7.3:0`), so the block was transcribed rather than captured verbatim. The underlying
facts do hold: a fresh cgit fetch is `bytes=11341 sha256=408ddc2a…` with `TRACE_EVENT(memory_failure_event`
count `0`, and the committed `sources-r54/memory-failure-trace.h.v7.3` has count `1` (§2, §3).

**F10 — LOW.** `evidence/c1-claims.txt`, `evidence/c2-claims.txt`, `evidence/c1-scope.txt` are data listings, not
command receipts; `c1-scope.txt` carries `exit=0` with no command. Their content is nevertheless consistent with
the counters: `c1-claims.txt`'s 31 hashes equal `count-c1.py --scope`'s set exactly (empty diff) with 31
`v7.2-source`/`v7.3 copy` pairs, and `c2-claims.txt`'s 21 hashes equal `count-c2.py --hashes 78295c76` exactly.

**Verified clean (no finding).** All 37 `freeze-sha256.txt` entries match the bytes at `6830f3af`; worktree bytes
of every frozen file equal the freeze bytes; both at-data counters reproduce their verdict line and exit code
(`C1=unmet … voted=0 failed=votes` exit 1; `C2=unmet claims=21 located=21 … entailed=0 failed=entailment` exit 1);
both selftests reproduce 57/0 and 54/0; the census reading reproduces (exit 0, 23 W04); the two `git grep` sweeps
reproduce exactly; the host memory-failure read reproduces verbatim on 7.2.11 with the v7.3 panic sysctl absent;
two v7.3 copies re-fetch byte-identically from cgit, so the pins are server-reproducible provenance for those
paths. Nothing in this seat observed a memory-failure event, and no host surface was written.
