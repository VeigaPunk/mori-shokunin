# RevAxisHarm — mori round 47, wave w2 — no-harm check across axes at T

- Seat: RevAxisHarm (leaf, no subagents). Date: 2026-10-25.
- T = `68d66ca53d89be5c34a62f46af7c37449d9f9b63`, E = `2d85e33d14198d388fd3cda9cc15ec07e57e7a53`, F = `63eecf2738db96f46b0bd02b1b2dfd66787493d0`.
- All git calls read-only in the lane repo (`git rev-parse --show-toplevel` = `/home/vgpnk/Projects/shokunin/mori-shokunin`, HEAD = T). Tool runs with `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47w2-RevAxisHarm`. No tracked path mutated; no fixture writes outside `.scratch`.

**Verdict up front: no harmed axis. All five checks hold.**

## Instrument identity (precondition for A2)

The v2 run must measure T's bytes, not the dirty working tree (`git status --porcelain` shows `M SCORECARD.md`, `M LOG.md` — in-flight wave work, see Context). Verified the tool copy used equals T:

```
$ sha256sum tools/mori-pin-check.py && git show 68d66ca5…:tools/mori-pin-check.py | sha256sum
9832e38c3863ba82f7a740921e8c9d23d6cf2e702c2bb62ee2ad71fcc21bc2b6  tools/mori-pin-check.py
9832e38c3863ba82f7a740921e8c9d23d6cf2e702c2bb62ee2ad71fcc21bc2b6  -
```

Identical → the working-tree `tools/mori-pin-check.py` is byte-identical to T's (v2). With `--rev T` the tool additionally reads SKILL.md from a `git archive` export of T, not the working tree.

## A1 — SCORECARD.md Axes table unchanged E→T — **holds**

```
$ git diff 2d85e33d… 68d66ca5… -- SCORECARD.md
(no output) exit=0
```

Empty diff over the whole file, so the Axes table is unchanged. Both revs have the file (`git cat-file -e` yes at E and T). Note: the *working tree* SCORECARD.md carries an uncommitted round-47 section (`git diff -- SCORECARD.md` = 30 lines, +16 content lines, "Round 47 — registry pins re-measured…"); that is in-flight wave bookkeeping, not part of T, and not judged here.

## A2 — every pre-existing registry pin still matches (v2 run at T) — **holds**

```
$ TMPDIR=…/r47w2-RevAxisHarm python3 tools/mori-pin-check.py \
    --rev 68d66ca5… --min-tally-pins 26 --baseline-rev 2d85e33d…
…33 `pin … state=match` lines (28 tally + 5 digest)…
PIN_CHECK=met tally_pins=28 digest_pins=5 mismatches=0 unparsed=0 no_command=0 \
  dropped=0 rebound=0 duplicate=0 min_tally_pins=26 rev=68d66ca5… baseline=yes
exit=0
```

- Every pin line is `state=match`; `mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0`.
- `baseline=yes` with `dropped=0 rebound=0`: every (row, pin) key present at E is still present at T with the same bound argv — no pre-existing pin was dropped or rebound.
- The two new rows' pins also match at T: `PIN_CHECK_SELFTEST pass=34 fail=0` (line 938) and `C2_SELFTEST pass=13 fail=0` (line 939).

**The one pre-existing registry row that changed E→T is a stale-pin repair, not a weakening.** `git diff E T -- SKILL.md` = 28 insertions, 1 deletion: the r38 "SOURCES append-only timing" row's self-test pin went `pass=15 fail=0` → `pass=22 fail=0`, plus two new rows and a Round47 prose section; no other pre-existing row touched. Direction check — the old pin was already false at E:

```
$ TMPDIR=…/r47w2-RevAxisHarm python3 tools/mori-pin-check.py --rev 2d85e33d… --min-tally-pins 26
pin line=912 kind=tally prefix=MORI_SOURCES_APPENDONLY_SELFTEST state=mismatch \
  pinned='pass=15 fail=0' observed='pass=22 fail=0' rc=0 \
  cmd='python3 tools/mori-sources-appendonly.py 2d85e33d… --selftest'
PIN_CHECK=unmet tally_pins=26 digest_pins=5 mismatches=1 … baseline=no
exit=1
```

At E the registry pinned `pass=15` while the registered tool printed `pass=22` (the row itself documents the cause: round-41 freeze `d72ac167` added seven selftest arms without updating the pin). The E→T edit moves the pin to the observed truth and it matches at T (`state=match pinned='pass=22 fail=0' observed='pass=22 fail=0' rc=0`). Calibration toward truth, consistent with claim C1's premise.

## A3 — no knowledge entry or SOURCES row deleted — **holds**

```
$ git diff --diff-filter=D --name-only 2d85e33d… 68d66ca5…
(no output) exit=0
```

Zero deleted files tree-wide. Row level:

- `corpus/knowledge/`: the only change is the added `corpus/knowledge/oom-tracepoints-r47.md` (A); the diff's only `^-` line is the `--- /dev/null` header of that new file — no removed knowledge content, no removed entry.
- `corpus/SOURCES.md`: stat = 5 insertions, 1 deletion. The single removed line is row **S005 rewritten in place**, not deleted — same row id, same URL, same schema cells; only the lifecycle cells moved:
  - at E: `… | The victim-mark tracepoint exposes PID, comm, UID, memory fields and oom_score_adj as a distinct event schema. | queued | 2026-10-19 | on-release | — |`
  - at T: `… | The victim-mark tracepoint exposes PID, comm, UID, memory fields and oom_score_adj as a distinct event schema. | mined | 2026-10-19 | on-release | corpus/knowledge/oom-tracepoints-r47.md |`
  New rows S475–S478 added. No row id removed; `corpus/README.md` and `corpus/QUALITY.md` diffs contain no removed content lines either (only their `--- a/…` headers).

## A4 — PROVINCE.md unchanged — **holds**

```
$ git diff 2d85e33d… 68d66ca5… -- PROVINCE.md
(no output) exit=0
$ git cat-file -e <E>:PROVINCE.md && git cat-file -e <T>:PROVINCE.md   # both yes
```

## A5 — adjacency respected (entry stays detection-and-report) — **holds**

`corpus/knowledge/oom-tracepoints-r47.md` (new) is observation and refusal, not intervention:

- Its Boundaries section: "**Knowledge only.** A resident tracer (eBPF, `perf`, tracefs `enable`) is outside the one-shot census and outside this lane's detection-and-report remit; **mori never enables an event or writes tracefs**. The host reading (S477) was `sudo -n ls`/`cat` of `/sys/kernel/tracing/events/oom/` only."
- Its recheck commands are read-only (`python3 .ufo/waves/round-47/count-c2.py <rev>`, `curl … | grep -c`); it refuses the staged "exactly three named tracepoints" headline as a calibration fix and routes attribution back to journal/cgroup evidence the lane already holds — no new mutation authority claimed.
- The two new SKILL.md registry rows declare read-only write scopes: C2 row `none (read-only git show)`; pin reconciler row `its own export and TMPDIR under <repo>/.scratch (removed on exit); runs the registered selftests, which write only their own temp dirs`. The S477 SOURCES row likewise scopes host access to `sudo -n ls`/`cat` under `/sys/kernel/tracing/events/oom`.

## Context observations (not judged, recorded for the wave)

- Working tree at measurement time: `M LOG.md`, `M SCORECARD.md` (uncommitted round-47 section being appended) and untracked `.scratch/*`, `.ufo/waves/round-47/w2*` files — in-flight wave-1/wave-2 work. Commit-level E→T diffs above are unaffected; UNVERIFIED who is writing them (out of seat scope).
- I did not re-derive C1's frozen-v1 scoring or C2's depth (other seats' claims); A2 evidence is the standing v2 tool at T, whose bytes were verified equal to T.

## Residual risk / verification gaps

- A2 relies on `tools/mori-pin-check.py` (v2) as the sanctioned instrument; its own correctness is audited by w1 seats (`RevPinCheckCode.md`), not re-audited here. Consistency signal: v2 independently reproduces the expected stale-pin mismatch at E and the clean slate at T.
- The v2 runs write their own transient export under the lane's `.scratch` (tool behavior, removed on exit; leftover `pin-check-*` dirs from other seats' runs remain untracked in the working tree).
- Working-tree SCORECARD/LOG edits are post-T state; if the wave lands them they are outside this seat's E→T scope.
