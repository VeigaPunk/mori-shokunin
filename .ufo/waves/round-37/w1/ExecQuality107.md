# ExecQuality107 — QUALITY 107's check shown able to fail (before/after pair)

**Item attacked:** QUALITY 107 (`corpus/QUALITY.md:862-869`) — "A tool interface that requires
per-id lines is checked on those lines, not only on its summary: a program that prints the
correct summary lists and omits the per-id lines is rejected." The QUALITY 107 row names its
check as `python3 .ufo/waves/round-37/count-c1.py <tip>` (parses
`changed <id> superseded_by=<id|->` / `deleted <id>` against the hidden truth on every arm and
requires `negative summary-only.py rejected`) and its "shown able to fail" evidence as "the
round-36 counter scores the same fixture `C2=met`, exit 0".

This seat attacks exactly that QUALITY 107 before/after pair, against the negative fixture
`.ufo/waves/round-37/fixtures/summary-only.py` (honest summary lists, per-id `deleted <id>`
lines stripped).

**Axis names:**
- (a) **before-half** — the round-36 counter `.ufo/waves/round-36/count-c2.py` must score the
  summary-only fixture `C2=met`, exit 0 (the counter that cannot see per-id lines);
- (b) **after-half** — the round-37 counter `.ufo/waves/round-37/count-c1.py` must *reject* the
  same fixture (per-id grammar enforced), i.e. `C1=unmet`, exit 1, and its own negative arm must
  print `negative summary-only.py rejected`;
- (c) **discrimination, not breakage** — the after-half must still accept the honest tool at the
  scored tip (`C1=met`, exit 0); a counter that rejects everything would satisfy (b) while
  defeating QUALITY 107;
- (d) **reason attribution** — the rejection must be caused by the *per-id grammar* (the thing
  QUALITY 107 names), not by an incidental failure (missing file, wrong cwd, timeout);
- (e) **seed robustness** — the before/after verdict must not be a property of one lucky draw.

**Outcome:** the pair reproduces at every seed tried. No defect found.

---

## 1. BEFORE half — round-36 counter vs `fixtures/summary-only.py` (expect `C2=met`)

```
cd /home/vgpnk/Projects/shokunin/mori-shokunin && python3 .ufo/waves/round-36/count-c2.py bf0df77 --tool /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-37/fixtures/summary-only.py --seed 12; echo "EXIT=$?"
```

Full output:

```
P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
tool: /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-37/fixtures/summary-only.py
blind arm: 24/24 sandbox histories matched the hidden truth (2.4s; coverage: deletions=23 changed-back=14 superseded=11)
real arm: pass (0.3s)
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  tool exit=1
C2=met
seed=12
EXIT=0
```

**Read:** the round-36 counter, which compares only the summary line, accepts the fixture on all
24 blind histories and on the real arm — `C2=met`, exit 0. That is the "before" state QUALITY 107
needs, and it matches the frozen receipt `.ufo/waves/round-37/evidence/c1-before-summary.txt`
byte-for-byte on the substantive lines (`C2=met`, `seed=12`, `EXIT=0`, same oracle/tool lists).

## 2. AFTER half — round-37 counter vs the same fixture (expect rejected)

```
cd /home/vgpnk/Projects/shokunin/mori-shokunin && python3 .ufo/waves/round-37/count-c1.py e57c58b57c025364e79d130fbdf764d2674d83d6 --tool /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-37/fixtures/summary-only.py --seed 12; echo "EXIT=$?"
```

Full output:

```
P-C1: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed, and exactly the truth's per-id `changed`/`deleted` lines, on each of 24 sandbox SOURCES.md histories drawn at run time, on the lane's own history (rev 6bd57097, round base f10a320d) where the independent oracle lists at least one id, and on one run-time-drawn challenge history presented in real-arm clothing (lane path, lane git identity, lane title); and the same counter rejects all three negative fixtures: a real-arm memoizer, a constant printer, and a summary-only printer.
tool: .ufo/waves/round-37/fixtures/summary-only.py
blind arm: 1/24 sandbox histories matched the hidden truth (2.3s; coverage: deletions=23 changed-back=13 superseded=10)
  repo00 FAIL: per-id lines differ (malformed=0)
      want: changed=['S010', 'S196'] deleted=['S138', 'S217', 'S236', 'S263']
      got:  changed=['S010', 'S196'] deleted=[]
  repo01 FAIL: per-id lines differ (malformed=0)
      want: changed=['S002'] deleted=['S037', 'S146', 'S178']
      got:  changed=['S002'] deleted=[]
  repo02 FAIL: per-id lines differ (malformed=0)
      want: changed=['S013', 'S184'] deleted=['S017', 'S135', 'S165', 'S197']
      got:  changed=['S013', 'S184'] deleted=[]
  repo03 FAIL: per-id lines differ (malformed=0)
      want: changed=['S015'] deleted=['S058']
      got:  changed=['S015'] deleted=[]
  repo04 FAIL: per-id lines differ (malformed=0)
      want: changed=['S013'] deleted=['S174']
      got:  changed=['S013'] deleted=[]
  repo05 FAIL: per-id lines differ (malformed=0)
      want: changed=['S010', 'S251'] deleted=['S022', 'S077']
      got:  changed=['S010', 'S251'] deleted=[]
  repo06 FAIL: per-id lines differ (malformed=0)
      want: changed=['S120'] deleted=['S044', 'S075']
      got:  changed=['S120'] deleted=[]
  repo07 FAIL: per-id lines differ (malformed=0)
      want: changed=[] deleted=['S003']
      got:  changed=[] deleted=[]
  repo08 FAIL: per-id lines differ (malformed=0)
      want: changed=['S052'] deleted=['S038']
      got:  changed=['S052'] deleted=[]
  repo09 FAIL: per-id lines differ (malformed=0)
      want: changed=[] deleted=['S143']
      got:  changed=[] deleted=[]
  repo10 FAIL: per-id lines differ (malformed=0)
      want: changed=['S113'] deleted=['S142', 'S179', 'S246']
      got:  changed=['S113'] deleted=[]
  repo11 FAIL: per-id lines differ (malformed=0)
      want: changed=[] deleted=['S007', 'S195']
      got:  changed=[] deleted=[]
  repo12 FAIL: per-id lines differ (malformed=0)
      want: changed=['S089'] deleted=['S028', 'S176']
      got:  changed=['S089'] deleted=[]
  repo13 FAIL: per-id lines differ (malformed=0)
      want: changed=['S064'] deleted=['S077']
      got:  changed=['S064'] deleted=[]
  repo14 FAIL: per-id lines differ (malformed=0)
      want: changed=[] deleted=['S091', 'S109', 'S143', 'S157', 'S286']
      got:  changed=[] deleted=[]
  repo16 FAIL: per-id lines differ (malformed=0)
      want: changed=['S057', 'S100'] deleted=['S145', 'S288']
      got:  changed=['S057', 'S100'] deleted=[]
  repo17 FAIL: per-id lines differ (malformed=0)
      want: changed=[] deleted=['S247', 'S299']
      got:  changed=[] deleted=[]
  repo18 FAIL: per-id lines differ (malformed=0)
      want: changed=['S269'] deleted=['S118', 'S143', 'S224']
      got:  changed=['S269'] deleted=[]
  repo19 FAIL: per-id lines differ (malformed=0)
      want: changed=['S078'] deleted=['S258']
      got:  changed=['S078'] deleted=[]
  repo20 FAIL: per-id lines differ (malformed=0)
      want: changed=['S035'] deleted=['S092']
      got:  changed=['S035'] deleted=[]
  repo21 FAIL: per-id lines differ (malformed=0)
      want: changed=[] deleted=['S215']
      got:  changed=[] deleted=[]
  repo22 FAIL: per-id lines differ (malformed=0)
      want: changed=['S042', 'S225'] deleted=['S116', 'S127', 'S285']
      got:  changed=['S042', 'S225'] deleted=[]
  repo23 FAIL: per-id lines differ (malformed=0)
      want: changed=[] deleted=['S015', 'S295']
      got:  changed=[] deleted=[]
real arm: pass (0.3s)
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  tool exit=1
challenge arm (real-arm clothing): FAIL (0.1s)
  truth:  appendonly_violations=2 ids=[] deleted=['S180', 'S204'] superseded=[] round_changed=['S082', 'S180', 'S204']
  tool:   appendonly_violations=2 ids=[] deleted=['S180', 'S204'] superseded=[] round_changed=['S082', 'S180', 'S204']
  reason: per-id lines differ: want changed=[] deleted=['S180', 'S204'] got changed=[] deleted=[]
negative memo-n1.py     rejected (challenge: lists differ: want appendonly_violations=5 ids=['S128', 'S145'] deleted=['S085', 'S155', 'S227'] superseded=['S128'] round_changed=['S085', 'S145', 'S227'] got appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193])
negative const.py       rejected (blind 4/4 (repo200: lists differ))
negative summary-only.py rejected (blind 2/4 (repo200: per-id lines differ (malformed=0)))
C1=unmet
seed=12
EXIT=1
```

**Read:** the round-37 counter rejects the fixture — `C1=unmet`, exit 1. Two independent arms kill it:
the blind arm (`1/24`, 23 histories fail with `per-id lines differ`) and the challenge arm
(`FAIL … per-id lines differ: want changed=[] deleted=['S180', 'S204'] got changed=[] deleted=[]`).
The counter's own negative arm also prints `negative summary-only.py rejected`.

**Axis (d) — reason attribution:** every rejection line says `per-id lines differ`, with the
fixture's `deleted=[]` where the truth has `deleted=['S138', …]`. The summary lists themselves
match the oracle on the real arm and on the challenge arm (`tool:` line == `truth:` line). So the
rejection is caused by exactly the omission QUALITY 107 names — the per-id `deleted <id>` lines —
and by nothing else (no missing file, no cwd error, no timeout).

## 3. Discrimination control — the after-half still accepts the honest tool

```
cd /home/vgpnk/Projects/shokunin/mori-shokunin && python3 .ufo/waves/round-37/count-c1.py e57c58b57c025364e79d130fbdf764d2674d83d6 --seed 7; echo "EXIT=$?"
```

Full output:

```
P-C1: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed, and exactly the truth's per-id `changed`/`deleted` lines, on each of 24 sandbox SOURCES.md histories drawn at run time, on the lane's own history (rev 6bd57097, round base f10a320d) where the independent oracle lists at least one id, and on one run-time-drawn challenge history presented in real-arm clothing (lane path, lane git identity, lane title); and the same counter rejects all three negative fixtures: a real-arm memoizer, a constant printer, and a summary-only printer.
tool: /tmp/mori-c1-tool-wkk0zw_t/mori-sources-appendonly.py
blind arm: 24/24 sandbox histories matched the hidden truth (2.1s; coverage: deletions=22 changed-back=15 superseded=10)
real arm: pass (0.3s)
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  tool exit=1
challenge arm (real-arm clothing): pass (0.1s)
  truth:  appendonly_violations=2 ids=['S215'] deleted=['S089'] superseded=['S215'] round_changed=['S089', 'S172']
  tool:   appendonly_violations=2 ids=['S215'] deleted=['S089'] superseded=['S215'] round_changed=['S089', 'S172']
negative memo-n1.py     rejected (challenge: lists differ: want appendonly_violations=2 ids=[] deleted=['S034', 'S062'] superseded=[] round_changed=[] got appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193])
negative const.py       rejected (blind 4/4 (repo200: lists differ))
negative summary-only.py rejected (blind 3/4 (repo200: per-id lines differ (malformed=0)))
C1=met
seed=7
EXIT=0
```

**Read:** the after-half is a discriminating gate, not a blanket rejector: honest tool at the
scored tip → `C1=met`, exit 0; and the counter's own negative arm prints
`negative summary-only.py rejected` — the exact string QUALITY 107's check requires.

## 4. Seed robustness (axis e)

Before half, round-36 counter vs the fixture:

```
r36 seed=12 -> C2=met
  exit=0
r36 seed=41 -> C2=met
  exit=0
r36 seed=42 -> C2=met
  exit=0
r36 seed=43 -> C2=met
  exit=0
```

After half, round-37 counter vs the same fixture:

```
r37 seed=12 -> blind arm: 1/24 sandbox histories matched the hidden truth (2.3s; coverage: deletions=23 changed-back=13 superseded=10)
challenge arm (real-arm clothing): FAIL (0.1s)
negative summary-only.py rejected (blind 2/4 (repo200: per-id lines differ (malformed=0)))
C1=unmet
r37 seed=41 -> blind arm: 3/24 sandbox histories matched the hidden truth (2.7s; coverage: deletions=21 changed-back=14 superseded=12)
challenge arm (real-arm clothing): FAIL (0.1s)
negative summary-only.py rejected (blind 4/4 (repo200: per-id lines differ (malformed=0)))
C1=unmet
r37 seed=42 -> blind arm: 2/24 sandbox histories matched the hidden truth (3.0s; coverage: deletions=22 changed-back=16 superseded=8)
challenge arm (real-arm clothing): FAIL (0.1s)
negative summary-only.py rejected (blind 4/4 (repo200: per-id lines differ (malformed=0)))
C1=unmet
r37 seed=43 -> blind arm: 3/24 sandbox histories matched the hidden truth (2.6s; coverage: deletions=21 changed-back=15 superseded=10)
challenge arm (real-arm clothing): FAIL (0.1s)
negative summary-only.py rejected (blind 3/4 (repo200: per-id lines differ (malformed=0)))
C1=unmet
```

Verdict is seed-invariant on all four seeds: before = `C2=met`/exit 0, after = `C1=unmet`/exit 1.

---

## 5. Method notes / caveats (observation, not a defect)

- `--tool` must be an **absolute** path for both counters. With a relative path
  (`--tool .ufo/waves/round-37/fixtures/summary-only.py`) both counters resolve it against the
  sandbox cwd and every arm dies with
  `no summary line (exit 2): /usr/bin/python3: can't open file '//.ufo/waves/round-37/fixtures/summary-only.py'`.
  The r37 counter then prints `C1=unmet`/exit 1 for the wrong reason (a missing file, not the
  per-id grammar). This is a caller-side usage requirement, not a defect in the counter: the
  frozen contract (`.ufo/waves/round-37/contract.md`, "Before" block) and the frozen receipt
  `evidence/c1-before-summary.txt` both use absolute tool paths, and the r37 counter's own
  negative-arm path (which is repo-relative and resolved by the counter itself, not the sandbox)
  works fine. Flagged only so a future seat does not read a relative-path `C1=unmet` as a
  discrimination result.
- The round-37 counter prints its `tool:` line via `display_path` (repo-relative for lane paths,
  per r36 debt (e)); the round-36 counter prints the absolute path. That is the intended
  difference, not drift.
- Scratch: both counters use `tempfile.mkdtemp` and clean up; `.ufo/waves/round-37/scratch/` was
  empty after these runs. No lane file was modified by this seat (lane repo `git status` shows
  only other seats' untracked reports).
- No tool was installed or upgraded for this seat (nothing to install; python3 + the frozen
  counters sufficed).

## 6. Files changed

- `.ufo/waves/round-37/w1/ExecQuality107.md` (this report) — the only file written.

## 7. Verdict

The QUALITY 107 before/after pair reproduces: the round-36 counter scores
`fixtures/summary-only.py` as `C2=met`, exit 0; the round-37 counter rejects the same fixture
(`C1=unmet`, exit 1, reason `per-id lines differ`) while still accepting the honest tool at the
scored tip (`C1=met`, exit 0). QUALITY 107's check is shown able to fail, and it fails for the
reason the criterion names.

VERDICT: PASS
