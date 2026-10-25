# R48ExecCensusEnd — registry end-state (census + append-only gate + row/histogram diff)

**Attacked:** the registry end-state at landed tip `e4dfff32d4f97c7ef250e9a7538fa75d4f284492` against
entering `e5dbac05459887d9597ea5d1da0d8e3d024e0d17` — fleet census `validate`, the lane's
append-only gate with `--round-base`, row counts, tier/status histograms and the added-id list.

**Verdict: HOLDS.** No class found in which the round's registry work escapes the instruments:
`round_changed=[]`, `deleted=[]`, 251 → 257 rows (+6, all `S479`-`S484`), zero in-place cell edits on
pre-existing rows, census `validate` exit 0 with output byte-identical to the round-start receipt.
Two scope limits and one contract-prose discrepancy are recorded below; neither falsifies the
end-state (limit classes `gate-field-scope`, `contract-prose-off-by-one`).

Fleet root `/home/vgpnk/Projects/shokunin`; lane root `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Scratch: `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48ExecCensusEnd/`
(`base.md`, `tip.md`, `census-end.txt`, `census.py`, fixture dirs `tmp.*`).
Every command below ran with `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48ExecCensusEnd`.
No installs or upgrades were made (nothing needed). No tracked file was edited; report only.

---

## 1. Fleet census `validate` at round end

```
$ cd /home/vgpnk/Projects/shokunin
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
mori	W04	S035 duplicate url raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in across scopes
mori	W04	S037 duplicate url www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html across scopes
mori	W04	S073 duplicate url docs.python.org/3/library/pathlib.html across scopes
mori	W04	S074 duplicate url kubernetes.io/docs/concepts/architecture/controller across scopes
mori	W04	S075 duplicate url ftp.gnu.org/gnu/bash/bash-5.3.tar.gz across scopes
mori	W04	S076 duplicate url michaelfeathers.silvrback.com/characterization-testing across scopes
mori	W04	S147 duplicate url raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/docs/settings.md across scopes
mori	W04	S148 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c across scopes
mori	W04	S149 duplicate url man7.org/linux/man-pages/man5/proc_pid_oom_score_adj.5.html across scopes
mori	W04	S150 duplicate url raw.githubusercontent.com/systemd/systemd/v262/man/systemd.exec.xml across scopes
mori	W04	S166 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c across scopes
mori	W04	S168 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst across scopes
mori	W04	S201 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/block/genhd.c across scopes
mori	W04	S218 duplicate url github.com/torvalds/linux/commit/b6866318657717c8914673a6394894d12bc9ff5e.patch across scopes
mori	W04	S220 duplicate url raw.githubusercontent.com/sysstat/sysstat/v12.8.0/iostat.c across scopes
mori	W04	S228 duplicate url docs.python.org/3/library/os.path.html across scopes
mori	W04	S349 duplicate url www.openeuler.org/whitepaper/openEuler%2024.03%20LTS%20%E6%8A%80%E6%9C%AF%E7%99%BD%E7%9A%AE%E4%B9%A6.pdf across scopes
mori	W04	S351 duplicate url www.freedesktop.org/software/systemd/man/latest/journalctl.html across scopes
mori	W04	S470 duplicate url www.freedesktop.org/software/systemd/man/latest/journalctl.html across scopes
mori	W04	S476 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c across scopes
mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
RC=0
```

- Last lines: `mori W04 S476 … oom_kill.c across scopes` then `mori ok …/corpus/SOURCES.md`; **exit 0**.
- 21 output lines = 20 `W04` + 1 `ok`; no `E01`-`E12` code. By the script's own contract
  (`scripts/sources-census.sh:22-33`) that certifies for all 257 rows: `NF=13`, valid id shape, no
  duplicate id, no duplicate URL+scope, kind/tier/status enums valid, `opened` a past ISO date,
  valid `recheck` cadence, no community row at tier A, **every `used-by` path exists on disk** (E11,
  which covers the new entry `corpus/knowledge/quota-observability-r48.md`), and no row-shaped source
  outside `## Registry`.
- Round-start receipt comparison (the round-end capture is `$TMPDIR/census-end.txt`, 21 lines):

```
$ diff -u mori-shokunin/.ufo/waves/round-48/evidence/census-start.txt $TMPDIR/census-end.txt && echo IDENTICAL_TO_START
IDENTICAL_TO_START
```

  So the +6 rows introduced **no** new `W04` duplicate-URL warning and no new `E` finding.
- Independent cross-check with the census instrument's own `census` mode (third parser):

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin mori
mori	rows	257
mori	tier.A	226
mori	tier.B	14
mori	tier.C	17
mori	status.mined	207
mori	status.queued	24
mori	status.rejected	26
FLEET	rows	257
FLEET	tier.A	226  FLEET.tier.B 14  FLEET.tier.C 17  FLEET.tier.invalid 0
FLEET	status.queued 24  FLEET.status.mined 207  FLEET.status.rejected 26  FLEET.status.invalid 0
FLEET	missing	0
RC=0
```

---

## 2. Append-only gate with `--round-base` (the `round_changed=[]` assertion)

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin
$ python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-sources-appendonly.py \
    e4dfff32d4f97c7ef250e9a7538fa75d4f284492 \
    --repo /home/vgpnk/Projects/shokunin/mori-shokunin \
    --round-base e5dbac05459887d9597ea5d1da0d8e3d024e0d17
P-C12: at revision R, tools/mori-sources-appendonly.py reports the timing line `supersede_timing ...`
changed S041 superseded_by=S206
changed S044 superseded_by=S207
changed S051 superseded_by=S208
changed S062 superseded_by=S209
changed S064 superseded_by=S210
changed S069 superseded_by=S226
changed S179 superseded_by=S211
changed S180 superseded_by=S212
changed S181 superseded_by=S213
changed S182 superseded_by=S201
changed S183 superseded_by=S214
changed S184 superseded_by=S215
changed S185 superseded_by=S216
changed S186 superseded_by=S217
changed S188 superseded_by=S218
changed S189 superseded_by=S219
changed S190 superseded_by=S220
changed S193 superseded_by=S202
appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S041,S044,S051,S062,S064,S067,S069,S070,S071,S083,S084,S090,S093,S096,S097,S101,S124,S127,S128,S129,S131,S140,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193,S226,S229,S235] round_changed=[]
supersede_timing superseded_as_of=[S041,S044,S051,S062,S064,S067,S069,S070,S071,S083,S084,S090,S093,S096,S097,S101,S124,S127,S128,S129,S131,S140,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193,S226,S229,S235] stale_supersede=[]
RC=0
```

- `round_changed=[]` **as required**; `deleted=[]`; `stale_supersede=[]`.
- **Read the exit code correctly:** `RC=0` here does *not* mean "no violations". `appendonly_violations=18`
  is the historical set (all 18 are long-landed supersede rewrites, `superseded_as_of` = the full
  eligible set, none stale). The tool's exit rule is `return 1 if result["round_changed"] else 0` under
  `--round-base` (`tools/mori-sources-appendonly.py:1109`), i.e. **in-round only**. A reader who takes
  `RC=0` as "clean registry" overstates it; a reader who takes it as "the round changed nothing" is
  correct.
- Only one commit in the round range touches the path, and the freeze commit does not:

```
$ git log --oneline e5dbac05..e4dfff32 -- corpus/SOURCES.md
e4dfff32 round-48: data — pin-check v3 + pin repair, unlanded check, FR2 quota entry (S479-S484), ...
$ git show --stat --oneline 4387cf94 -- corpus/SOURCES.md      # empty
$ git rev-list --count e5dbac05..e4dfff32
2
```

- Instrument receipt: `python3 tools/mori-sources-appendonly.py --selftest` → `MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0`, RC=0
  (a receipt only; the non-vacuity evidence below is independent).

### 2a. Non-vacuity controls (scratch fixtures, `mktemp -d` + `git init -q`, toplevel verified = `$D`)

| control | fixture action | gate output (tail) | rc |
|---|---|---|---|
| A legal append | append `S003`, nothing edited | `appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[]` | 0 |
| B immutable edit in range | rewrite `teaches` of `S001` | `appendonly_violations=1 ids=[S001] … round_changed=[S001]` | 1 |
| C delete in range | delete `S003` | `appendonly_violations=2 ids=[S001] deleted=[S003] … round_changed=[S001,S003]` | 1 |
| D add-then-delete in range | add `S002`, delete it again | `deleted S002` / `appendonly_violations=1 … deleted=[S002] … round_changed=[S002]` | 1 |
| E add-then-edit in range | add `S003`, rewrite its `teaches` | `appendonly_violations=2 ids=[S003] deleted=[S002] … round_changed=[S002,S003]` | 1 |

So `round_changed=[]` at the tip is a real measurement, not a blind spot for the two moves that could
hide a registry rewrite (add-then-delete, add-then-edit). **Limit (`gate-field-scope`):** a *legal*
append is deliberately not a "change" (control A), so `round_changed=[]` alone does **not** certify
that six rows were added — that fact comes from the row counts and the id diff in §3, and from the
census's per-row checks in §1. The gate also validates no row content (columns, enums, `used-by`
existence); that is the census's job and it ran clean.

---

## 3. Row counts, histograms, added ids

Count command as assigned:

```
$ for r in e5dbac05 e4dfff32; do echo "== $r"; git show <rev>:corpus/SOURCES.md | grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'; done
== e5dbac05459887d9597ea5d1da0d8e3d024e0d17
251
== e4dfff32d4f97c7ef250e9a7538fa75d4f284492
257
```

Working tree equals the tip blob (so the census measured the landed bytes, not a dirty file):

```
$ sha256sum corpus/SOURCES.md
bc9ecd96ac60a86089a0c3a9a78d43e567b5cddde2bcc3a26071fdd6b389e04f  corpus/SOURCES.md
$ git show e4dfff32:corpus/SOURCES.md | sha256sum
bc9ecd96ac60a86089a0c3a9a78d43e567b5cddde2bcc3a26071fdd6b389e04f  -
$ grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md
257
$ git status --porcelain corpus/SOURCES.md tools/     # empty
```

Histograms (11-column header `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`
identical at both revs; no `\|` escapes in either file, so cell splitting is unambiguous):

| revision | rows | tier A | tier B | tier C | status mined | queued | rejected |
|---|---|---|---|---|---|---|---|
| `e5dbac05` (entering) | 251 | 220 | 14 | 17 | 201 | 24 | 26 |
| `e4dfff32` (tip) | 257 | **226** | 14 | 17 | **207** | 24 | 26 |

Produced twice by independent parsers (python `$TMPDIR/census.py`; `awk -F'|'` on `$5`/`$9`) and once
by the census instrument's `census` mode (§1) — all three agree. Deltas are exactly +6 tier A, +6 mined.

Structural diff (python, id-keyed, base vs tip):

```
added   ['S479', 'S480', 'S481', 'S482', 'S483', 'S484']
removed []
tier shifts   {}
status shifts {}
cell edits (source/kind/opened/used) {}
dup ids base: []   dup ids tip: []
order preserved (base is prefix of tip): True
base n=251 first=S001 last=S478 max=S478
tip  n=257 first=S001 last=S484 max=S484
```

Because the base id sequence is exactly the first 251 ids of the tip sequence, the pre-existing
numeric gap set is unchanged, no id was renumbered, and no row moved. `S477`/`S478` already existed at
`e5dbac05` (lane rows) and are still present at the tip with unchanged cells — the staged entry's
`S477`/`S478` did not collide.

Added rows (all six are new rows at the tail; cells as landed):

| id | tier | status | kind | opened | recheck | used-by | URL |
|---|---|---|---|---|---|---|---|
| S479 | A | mined | docs | 2026-10-25 | 180d | corpus/knowledge/quota-observability-r48.md | https://man7.org/linux/man-pages/man8/xfs_quota.8.html |
| S480 | A | mined | docs | 2026-10-25 | 180d | corpus/knowledge/quota-observability-r48.md | https://man7.org/linux/man-pages/man2/quotactl.2.html |
| S481 | A | mined | code | 2026-10-25 | on-release | corpus/knowledge/quota-observability-r48.md | https://raw.githubusercontent.com/torvalds/linux/v7.2/include/uapi/asm-generic/errno.h |
| S482 | A | mined | docs | 2026-10-25 | 180d | corpus/knowledge/quota-observability-r48.md | https://help.aliyun.com/zh/nas/user-guide/set-quotas-on-the-subdirectories-of-nas-nfs-volumes |
| S483 | A | mined | code | 2026-10-25 | on-release | corpus/knowledge/quota-observability-r48.md | https://raw.githubusercontent.com/torvalds/linux/v7.2/arch/mips/include/uapi/asm/errno.h |
| S484 | A | mined | code | 2026-10-25 | on-release | corpus/knowledge/quota-observability-r48.md | https://raw.githubusercontent.com/torvalds/linux/v7.2/arch/sparc/include/uapi/asm/errno.h |

Renumbering by document (staged entry `/home/vgpnk/Projects/shokuknow/merge/mori/knowledge/corpus/knowledge/quota-observability-r38.md`
has 5 `source:` lines) matches by URL, with the entry's own `source:` lines at the tip (6 lines,
`S479`-`S484`) agreeing id-for-id:

- staged `S477` xfs_quota.8 → lane **S479**; staged `S478` quotactl.2 → lane **S480**;
  staged `S482` asm-generic `errno.h` → lane **S481**; staged `S479` aliyun NAS → lane **S482**.
- staged `S481` (RHEL 9 Japanese PDF) is not landed — consistent with the contract's HTTP 403 note.
- `S483` (mips `errno.h`) and `S484` (sparc `errno.h`) are lane-new; the entry's own `source:` lines
  label both `(boundary, not in the claims table)`, and the claims table cites only `S479`-`S482`.

**Limit (`contract-prose-off-by-one`):** `contract.md` describes the round-start receipt as "20 lines
of output with 19 W04 warnings plus one `ok`"; the frozen `evidence/census-start.txt` is **21 lines =
20 W04 + 1 `ok`**, and my round-end capture is byte-identical to it. The receipt and the round-end
measurement are consistent with each other; only the contract's sentence is off by one. This touches
no C1/C2 predicate.

**Observation for the C2 seats (not scored here):** the registry grew by 6 URLs while
`.ufo/waves/round-48/count-c2.py` freezes 4 (`COPIES`, lines 37-43: xfs_quota.8, quotactl.2,
asm-generic `errno.h`, aliyun NAS). `S483`/`S484` are therefore outside what the C2 counter can
locate; their registry correctness rests on the census (§1, which passed) and on the entry's
boundary labelling, not on a located quote. This is a stated boundary of the frozen counter, not a
failure of the registry end-state.

---

## What I did not check (UNVERIFIED)

- Any C1 or C2 predicate: not run, not scored (other seats own them).
- Whether the 257 rows' *content* is true; only structural/enum/used-by validity and the append-only
  relation were measured.
- `overdue` was run only informationally (`sources-census.sh overdue … --today 2026-10-25`, RC=0,
  `cadence` lines only); no overdue judgement is asserted.
- The untracked `.scratch/*` directories visible in `git status` belong to sibling seats; I did not
  touch them.
