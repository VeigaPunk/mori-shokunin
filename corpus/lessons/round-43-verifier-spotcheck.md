# Round 43 verifier spot-check

author: hyaku closure (non-author integrator, @m_flash)

Reviewer: hyaku closure, fresh non-author integrator subagent dispatched by the
hyaku orchestrator. Did not author this round, did not amend either counter,
did not edit any lane-authored file, did not start round 44. Verified committed
bytes at lane tip `91cb221f35f7cb9afeff99ef1959512dabddfc46` (entering tip
`e3a2b58f72ba3bd52a90646f7285fb85f0ee5dd2`). Sibling gates were read, not
executed; every number below is a measurement this reviewer ran.

## Conformance

- Report `.ufo/reports/round-43/mori.md` is committed in the fleet repo. Two
  commits touch it: `484e6eff7cb668d5f753b079bfaaa6f4d0b98adf` (initial,
  authored 2026-10-24 23:17:49 -0300, committed 23:31:10) and
  `0c9e9999f8dcc7235ae2129d51ec9565885c7063` (amendment, authored 23:31:12,
  committed 2026-10-25 03:23:11). Both carry
  `mori-shokunin <mori@shokunin.local>`.
  `git log --format='%an %H' -- .ufo/reports/round-43/mori.md` shows that
  identity only.
- **Attribution defect (durable, status-neutral).** The report was not landed by
  the lane: the two commit subjects say so themselves (`hyaku sweep: L1
  returned without committing; attribution defect`, `operator stop sweep`). The
  lane identity is the `fleet-commit.sh --as mori` identity on a sweep commit,
  not lane authorship. History is not rewritten for attribution; the defect is
  recorded in the round notes. A swept report is still landed.
- **Ordering defect.** The initial filing (`484e6eff`, 23:31:10) preceded the
  lane's final commit `91cb221f` (2026-10-24 23:35:46), so at first filing the
  report did not land last. The 03:23 amendment cites the final tip and lands
  after it. The amendment, however, **rewrote filed bytes in place** (10
  insertions / 5 deletions on an already-filed report) where the protocol
  requires an erratum appended after the filed bytes and naming what it
  supersedes. Routed.
- `SHONEN` heading present, one line per box, four boxes: three `[~]` with
  resolvable pointers (`evidence/c1s-clause-map.txt`, `evidence/c1s-after.txt`,
  `w1-spec.json`) and one `[ ]`. No `[x]`: not promotion-ready, and promotion
  stays operator-owned. The report is not a marker — it names real committed
  work.
- Cited lane commits exist and are ancestors of the lane branch:
  `git merge-base --is-ancestor <h> master` holds for `dde525ea…`,
  `efb92cd5…`, `91cb221f…` and for entering tip `e3a2b58f…`. `HEAD` is
  detached at the tip; ancestry was tested against `master`, never `@{u}`.
- Lane repo clean:
  `git -C mori-shokunin status --porcelain` → empty;
  `scripts/hyaku/jj-lane.sh state …` → `ahead=0 behind=0
  local=remote=91cb221f…`; `git ls-remote origin refs/heads/master` →
  `91cb221f35f7cb9afeff99ef1959512dabddfc46`.
- Dispatched prompt `.ufo/prompts/mori-round-43.md` carries the template
  contract verbatim as sections 1–5 (MISSION/AXES binding, claims, frontier
  step, L2 floor, report path `.ufo/reports/round-43/mori.md`, commit-then-push,
  push scope, L0 side channel) plus the hyaku addendum §6. All five child-lane
  items resolve: report path/filename (§4:101), `SHONEN` heading (§4:118),
  commit-hash citation (§4 "Landed changes"/"Before → after"; addendum §6:325),
  report-lands-last (§6:325), lane write scope (§6:385, writes confined to
  `/home/vgpnk/Projects/shokunin/mori-shokunin`). The quoted L2 floor (8) matches
  `MISSION.md` §"L2 concurrency — required". Two items arrive only through the
  addendum, not the canonical rendering — the shipped `templates/round-prompt.md`
  still lacks an explicit lands-last clause and an explicit write-scope clause.
  Named for the operator; `templates/` is operator-side.
- Dispatch digest copied from the mutable `.ufo/watchdog.log`:
  `2026-10-24T21:21:34-03:00 launch mori round=43 pgid=2878367 driver=hyaku-inline attempt=1`
  and
  `2026-10-25T03:23:12-03:00 complete mori round=43; hyaku-inline attempt=1`.
- Wave evidence, counted from committed bytes: 72 seat logs
  (`git ls-tree -r --name-only 91cb221f .ufo/waves/round-43/logs | wc -l` →
  72; 64 `wave64/` + 8 `residual8/`); 10 seat reports (4 `Exec*.md` + 6
  `ResCrit*.md`); spec role mix
  `grep -oE '"(scout|scribe|executor|sentinel|connector|simplifier|revenger|reviewer|critic|mutation-tester)"'`
  on `w1-spec.json` → reviewer 12, critic 11, mutation-tester 8 (attack 31 =
  48.4%), scout 12, scribe 8, executor 8, sentinel 2, connector 1, simplifier 1,
  revenger 1 (build 33). `w1-settle.tsv` → 3 rc 0, 8 rc 1, 52 rc 124 (timeout);
  `w1-settle-residual.tsv` → 6 rc 0, 2 rc 124. The report's 8-exited-1 /
  52-killed / 6-of-8-residual figures hold.

## Claims

Re-measured at the lane tip unless a command names a revision. Neither counter
was amended after its freeze: `git show dde525ea:.ufo/waves/round-43/count-c1s.py
| sha256sum` and the tip copy both give
`93482248b46def2a2cec7238732af1551ef315517e76833c3843875313b65dc5`; `count-c2.py`
both give `a1e05c983c0595dae0aaaefe62513cd9c2264dca07eee5c1b869d73eebff5b88`.
The frozen round-42 counter is untouched:
`git diff e3a2b58f 91cb221f -- .ufo/waves/round-42/count-c1.py | wc -l` → `0`
and its sha is `105ce075f33120837ba5a49a1ad4f23a3dd7dc17fea506ab917140bc7f2053f6`.

### C1S operability — verified (measured), limitation disclosed and accepted

Before, re-read from the committed control receipt: `check self_at_rev FAIL
(absent)` → `C1S=unmet`, `exit=1` (`evidence/control-c1s-donothing.txt`). A
planted `print("C1S=met")` counter is scored `self_at_rev FAIL (bytes differ)` →
`C1S=unmet` (`evidence/control-c1s-junk.txt`). After, re-read from
`evidence/c1s-after.txt`:

```
check self_at_rev            PASS (match)
check frozen_sha             PASS (105ce075f331)
check frozen_sig             PASS (run params argv, timeout)
check v5_present             PASS (.ufo/waves/round-42/conform.py)
check sandbox_clone          PASS
check noharm_cwd             PASS (rc=0 MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0)
check v5_selftest_17         PASS (pass=17 fail=0 rc=0)
check mutant_*_present/kill  PASS (three mutants, pass=16 fail=1, each its own arm)
check frozen_still_crashes   PASS (rc=1 crash=True C1_line=False)
C1S=met
exit=0
```

Independent counts: `git show efb92cd5:.ufo/waves/round-43/evidence/c1s-after.txt
| grep -cE '^check'` → **14** (14 PASS); the green control
`control-c1s-green.txt` is also **14**. The report's "15 checks PASS" (and
`evidence/c1s-mutants.txt`'s "the healthy counter prints 15") is off by one:
the honest counter prints 14 check lines. The frozen P-C1S sentence's ten
clauses are each discharged by those 14 lines (`evidence/c1s-clause-map.txt`
lists 14 rows), so the verdict `C1S=met exit 0` stands on its own evidence.
The disclosed limitation is real and was self-reported: 4 of 8 mutation classes
survived (`evidence/c1s-mutants.txt`, mutation applied to both copies), i.e. the
counter is not tamper-evident; its identity is pinned by the committed sha256.
No claim is made that the counter would notice its own tampering. Axis:
**improved** (instrument now completes the frozen sentence and the no-harm arm
the r42 counter crashed before; score held at 7, no move claimed).

### C2 calibration — verified (re-measured independently)

Before (`evidence/control-c2-donothing.txt`): `check correction_row FAIL
(ids=[])`, `check scorecard_correction FAIL (count=0)`, 6 PASS / 8 checks →
`C2=unmet mismatches=2 exit=1`. After (`evidence/c2-after.txt`): 8/8 PASS →
`C2=met mismatches=0 exit=0`.

Every component re-derived by this reviewer, not read from the counter:

| component | command | observed |
|---|---|---|
| S235 row byte-identical | `git show 91cb221f:corpus/SOURCES.md \| grep -E '^\| S235 ' \| tr -d '\n' \| sha256sum` | `971df55e9e1ed8826e66dd31d12f9cbb5b2c727cf71201a2c0eabc7311e169a2` (the P-C2 pinned value; the counter hashes the line without its terminator) |
| correction row | `git show 91cb221f:corpus/SOURCES.md \| grep -F '\| S349 '` | row present, contains `corrects S235` and `a30dca99`; `grep -c 'a30cda99'` → 0 |
| SCORECARD correction, exactly once | `git show 91cb221f:SCORECARD.md \| grep -cF 'Round-43 calibration correction: r42-declaration-C1=met superseded; frozen counter printed no C1= line'` | `1` |
| declaration cell unrewritten | `… \| grep -cF '`C1=met` exit 0 (`evidence/c1-after.txt`)'` | `1` |
| PDF sha | `git show 91cb221f:corpus/evidence/sources-r42/S235.pdf \| sha256sum` | `9855a4986a312dfc946b1b97b6010a8e4f1e65a4a30dca99359e6df057ad8020` |

The S235 row is not rewritten and the round-42 declaration cell is still
standing; the supersession is append-only in both files. Axis: **improved**
(score held at 5).

### No-harm

`git diff --numstat e3a2b58f 91cb221f -- SCORECARD.md` → `32 0`; the axes table
and every score cell are unchanged (`git diff … -- SCORECARD.md | grep -E
'^[-+]\| (coverage|operability|depth|freshness|calibration|adjacency) '` → empty).
Round diff totals 255 added / 5 modified / 0 deleted; `SKILL.md`, `PROVINCE.md`
and `SHONEN.md` are untouched. Scores held: coverage 6, operability 7, depth 5,
freshness 5, calibration 5, adjacency 6. Evidence timestamps sit before the
commits that ship them (receipts `when 2026-10-24T22:53:03-03:00`, shipped in
`efb92cd5` at 23:19:34).

## Axes

| axis | verdict | why |
|---|---|---|
| operability | improved | C1S=met exit 0 at the counter's frozen bytes, no-harm arm `pass=22 fail=0`, entering tip unmet; score held 7; tamper limitation disclosed |
| calibration | improved | C2=met mismatches=0; both r42 self-assessment errors superseded append-only, re-derived here from bytes |
| coverage | unchanged | one admitted knowledge entry + a frontier map row; score held 6, no coverage move claimed |
| depth | unchanged | three knowledge entries with `source:`/`verified-at:`/`recheck:`; no depth move claimed |
| freshness | unchanged | new rows carry `90d`/`180d` rechecks; no freshness move claimed |
| adjacency | unchanged | detection-and-report only; two adjacent package entries refused with flips (`S350` host mutation, `S351` campaign `file://` + MESSAGE grep) |

No axis harmed.

## Spot-check

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S348 Python `subprocess.run` | admit | live https://docs.python.org/3/library/subprocess.html#subprocess.run (tag-stripped) | agree | Signature text contains the exact 8-word quote `shell=False, cwd=None, timeout=None, check=False, encoding=None, errors=None, text=None, env=None`; location named (signature line). It grounds the `cwd` clause the frozen r42 counter fails. |
| S470 `journalctl --disk-usage` | admit | live https://www.freedesktop.org/software/systemd/man/latest/journalctl.html | agree | Quote present verbatim: "Shows the current disk usage of all journal files. This shows the sum of the disk usage of all archived and active journal files." (24 words ≤ 25). `--disk-usage` entry, Commands section; same URL as S014 but a different scope (W04 duplicate-URL warning, deliberate). |
| S350 `systemd.scope(5)` | reject | live https://www.freedesktop.org/software/systemd/man/latest/systemd.scope.html | agree | Quote present verbatim (19 words). The refusal reason is the staged entry's recheck (`systemctl reset-failed` after creating a scope = host mutation), which `PROVINCE.md` (read-only probes; detection and report) puts outside the lane; the flip (read-only `MemoryMax` show of an already-failed scope) is a real read-only path. |
| S351 `journalctl --vacuum-size=` | reject | live https://www.freedesktop.org/software/systemd/man/latest/journalctl.html | agree | Quote present (18 words, option name then sentence). The rejection is about the staged entry's grounding (campaign `file://` note plus a kernel `MESSAGE` grep), not about the page; the flip is public-sentence-plus-committed-receipt, which is admissible. |

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin
mori` → `exit=0`, 243 rows, 19 W04 duplicate-URL warnings (16 pre-existing + S349
vs S235, S351 and S470 sharing the journalctl URL — all deliberate). Rows before
→ after, counted by this reviewer:
`git show <rev>:corpus/SOURCES.md | grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'`
→ 238 at `e3a2b58f`, 243 at `dde525ea` and at the tip. Reported 238 → 243 holds.

## Trends

- **expansion — improved.** Registry 238 → 243 (measured above), five rows added
  by tier (A: S348, S349, S470; B: S350, S351 rejected), three knowledge entries
  (`c1s-cwd-r43.md`, `s235-sha-correction-r43.md`,
  `journal-disk-usage-total-r51.md`), and one frontier row in
  `corpus/README.md` §"Round-43 coverage additions" — no Core move claimed.
- **quality — improved.** The two routed r42 false self-assessments are
  superseded append-only and falsifiable (an in-place rewrite of S235 or the
  declaration cell fails `count-c2.py`), QUALITY 115 and 116 each carry
  rationale plus a shown-able-to-fail check, and the round's own method defect
  (HEAD-only probe) became a lesson rather than a silent pass.
- **discernment — improved, with the lane's own numeric slips recorded.** All
  four sampled Gate decisions agree on re-open (two admits, two rejects), and
  the lane escalated its own method error instead of defending it. But two
  counts in the report are wrong (14 checks reported as 15; 8 rate-limited seat
  logs reported as 34) — recognition of its own evidence is not yet exact.
  Routed as defects below; it does not touch the admitted claims.

## Routed defects (mori, next round)

1. Report attribution: landed by fleet sweeps (`484e6eff`, `0c9e9999`), not by
   the lane. Durable record; never rewritten.
2. Filed-report bytes rewritten in place by `0c9e9999`; a correction must be an
   appended erratum naming the superseded text.
3. Count slips in the report and in `evidence/c1s-mutants.txt`: "15 checks"
   should be 14; "34 seat logs carry `provider.rate_limit: 429`" — observed 8
   (`git grep -l 'provider.rate_limit' 91cb221f -- .ufo/waves/round-43/logs`),
   while 39 logs merely contain the string `429` (byte counts, file sizes).
4. Gate-standard gaps on the two new counters: no `SKILL.md` registry row
   (entry command, verdict map, selftest spelling, pinned path, write scope,
   owner) and no `--selftest` self-invocation mode over isolated fixtures.
   Closure grades no gate conformant until the registry row exists.
5. C1S's receipt is measured at `dde525ea`, while the report's verdict says "at
   the landed tip"; the tip equivalence rests on the documented identical
   counter sha256. A tip-run receipt would close the gap.
6. Operator-side template: `templates/round-prompt.md` still carries neither an
   explicit report-lands-last clause nor a lane write-scope clause; this prompt
   got both from the hyaku addendum.

## Verdict

Both claims verified (C1S and C2 measured, receipts and component bytes
re-derived here); no axis harmed; both trends expansion and quality improved,
discernment improved with its defects routed. **Admit.**
