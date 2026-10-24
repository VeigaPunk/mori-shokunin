# Progressing-weak authorship proof (round 2) — seat `authorship-proof`

lane: mori-shokunin · seat: authorship-proof (round-2 flash wave, 13 seats) · written:
2026-10-15T15:42Z · measured on this host: git 2.55.0 · detection and report only
(`PROVINCE.md:16`) — this note and its check write only their own temp dirs, read the fleet
read-only, and never kill, restart, record `failed` or edit host state.

driver-citation scope: `mori-silence-cases.sh` refs in this note name the pre-wave candidate
revision `61db3df3`; the shipped revision is `505a7504` (line numbers moved; case ids stable).

derived from: `PROTOCOL.md:157-168` (grade semantics); `corpus/knowledge/lane-silence-r2.md`
(precursor decision table; authorship rows `:92-123`, identity policy `:105-123`);
`corpus/knowledge/silence-grading-r2.md:224-229` (this wave's deferral #6 — the proof defined
as the driver's authorship cases passing end-to-end); `SCORECARD.md:32-95` (blocked attempt);
`LOG.md:73-80` and `:146-152` (measured r1 divergences and the harness failure).

**Status — the r1 deferral, split in two; each half decided here.**

Round 1 deferred `progressing-weak` because "the probe cannot yet prove authorship"
(`corpus/README.md:13-14`; the in-code deferral at `tools/mori-census.sh:523-527`).

1. **Authorship discrimination — LANDED (this note).** A runnable check, executed here, proves
   the discrimination the weak grade rests on, on real git repositories with real identities:
   an exact-line author match over **all** post-launch commits separates lane-authored activity
   (`progressing`) from other-authored activity (`progressing-weak`) from no activity
   (`silent`), and never degrades missing data into `silent` (`unavailable`). It uses, and
   supplies, the corrected form of the identity recipe — the recipe as printed in the two
   precursor notes is byte-defective and matches nothing as written (D1 below).
2. **Production admission — STILL DEFERRED, preconditions named.** The census is still r1
   (`tools/mori-census.sh` sha256 `e3073a2b5e89bf717c1955e7a3d7bd995bf1096d61b6887af98b4517ee92f3f2`),
   so no run emits `progressing-weak`. The harness moved mid-wave: the bytes this seat first
   measured (driver sha256 `61db3df336fcd0facfaa9de6a5f0b5753047a450bbe85f685bc2d2a051b7011f`,
   15:29Z) exited 1 in fixture setup with no tally (D2 below); a sibling seat then rewrote the
   file, and on the new bytes (sha256
   `2cc205fc3666e1ab8b6ecf73228d86e2ae0515f915d4a4570f988327b3e6c11e`, measured 15:39Z) the
   candidate completes all 27 cases but the tally is not passing:
   `MORI_SILENCE_CASES: matched=10 total=27`, exit 1, all seven authorship cases among the
   17 failures (measured by this seat; the harness's own claim to make). The falsifiable claim
   a future round must register is stated at the end. **No passing tally, no census cutover,
   no live r2 grade is claimed here.**

## The check — how to run it, and the executed receipt

Extract this file's check block and run it (run the extraction from the lane root; the check
itself runs from any cwd and writes only its own `/tmp/mori-authorship-check.*` temp dirs,
removed on exit):

```
awk '/^###CHECK-BEGIN$/{f=1;next} /^###CHECK-END$/{f=0} f' \
  corpus/knowledge/progressing-weak-r2.md > /tmp/mori-authorship-check.sh
sha256sum /tmp/mori-authorship-check.sh
bash /tmp/mori-authorship-check.sh
```

Executed 2026-10-15T15:39:00Z on the file produced by the extraction command above
(byte-for-byte) — verbatim output:

```
mori-authorship-check r1 — git=git version 2.55.0 — script_sha256=9c91e0a011a99dfb9459f4a5cbedaecf432812a5a4237ec02e32fafd3801afd6
anchor LAUNCH=1699998000 PRE=1699995000 POST=1699998600 LANE=kagi
PASS lane-postlaunch (state=progressing)
PASS lane-hidden-behind-sibling-head (state=progressing)
PASS sibling-only-clean (state=progressing-weak)
PASS author-sibling-committer-lane (state=progressing-weak)
PASS author-lane-committer-sibling (state=progressing)
PASS substring-name-trap (state=progressing-weak)
PASS substring-email-trap (state=progressing-weak)
PASS prelaunch-lane-commit-only (state=silent)
PASS empty-repo (state=silent)
PASS missing-repo (state=unavailable)
MORI_AUTHORSHIP_CHECK: matched=10 total=10
```

exit **0** (`MORI_AUTHORSHIP_CHECK: matched=10 total=10`; `0 failed`).

### Decision function (4 rules, order of first match)

1. repo path absent, or `git rev-parse --git-dir` rc≠0 → `unavailable` (missing data must not
   become `silent`; closes the r1 shape at `observability-census-r1.md:182-184`).
2. no commits at all (`git rev-parse --verify -q HEAD` rc≠0) → `silent`.
3. `git log --after=@<launch_epoch> --format='%an <%ae>'` contains a line exactly equal to
   `"<lane>-shokunin <lane>@shokunin.local"` (`grep -Fxq --`, **closing `>` included**) →
   `progressing`.
4. otherwise: that log non-empty → `progressing-weak`; empty → `silent`.

Not covered by this check (named, owned by the cutover): row B filesystem evidence and the
lifecycle rows (open / closed / superseded) — `silence-grading-r2.md:84-107, 118, 153-166`.

### Check case ↔ driver case map

| check case | driver analogue (`tools/mori-silence-cases.sh`) |
|---|---|
| `lane-postlaunch` | `:438-443` `subject-postlaunch-progressing` |
| `lane-hidden-behind-sibling-head` | `:447-453` `subject-hidden-behind-sibling-head` |
| `sibling-only-clean` | `:458-464` `sibling-clean-checkout-weak` |
| `author-sibling-committer-lane` | `:467-472` `author-sibling-committer-subject-weak` |
| `author-lane-committer-sibling` | `:475-480` `author-subject-committer-sibling-progress` |
| `substring-name-trap` | `:484-489` `substring-name-mismatch-weak` |
| `substring-email-trap` | `:493-498` `substring-email-mismatch-weak` |
| `prelaunch-lane-commit-only` | nearest: `:356-361` `silent-open` (pre-launch lane commit is not credited) |
| `empty-repo` | new shape: no commits → `silent`, never `unavailable` |
| `missing-repo` | `:407-409` `repo-missing-unavailable` |

When the driver's authorship cases can run (precondition 1+2), they are the acceptance upgrade
of this check; until then this check is the runnable proof.

## Measured git micro-semantics the cutover must state (git 2.55.0, 2026-10-15)

Measured on scratch fixtures (not on the fleet), because the contract's wording ("post-launch";
row 6 "strictly post-launch", `lane-silence-r2.md:153-159`) and what `--after` actually does
can differ:

- **`--after=@T` includes a commit whose committer date equals `T`** — a fixture commit with
  `ct=1699998000` is listed by `git log --after=@1699998000`. Row 6's "strictly post-launch"
  therefore cannot be implemented by `--after` alone; an explicit `%ct > launch` comparison
  is needed. (The driver's `:544-548` case `report-eq-launch-no-close` expects exactly the
  strict behavior.)
- **`--after` filters on the committer date, not the author date** — fixture commit
  `at=1699997000 ct=1699999000` is listed; `at=1699999000 ct=1699997000` is not. The identity
  rows match the **author** fields (`%an/%ae`). For commits with `at≠ct`, the composition of
  the two filters needs one stated rule. This check's fixtures pin `at==ct` (the driver's
  `gc()` sets both, `:195-215`) and the live lane commits measured below also carry `at==ct`
  (e.g. mori: `at=1792041245 ct=1792041245`), so these receipts are invariant to the choice;
  the choice itself is left to the cutover.

## Live application (read-only, fleet root, 2026-10-15T15:35Z)

Anchor (per the precursor note's parser rule, `lane-silence-r2.md:69-72`):

```
grep -E ' launch mori round=' .ufo/watchdog.log | tail -1
  → 2026-10-15T01:50:57-03:00 launch mori round=2 pid=2685430
date -u -d '2026-10-15T01:50:57-03:00' +%s   → 1792039857
```

Per-lane authorship over the launch window (corrected identity pattern; `now=2026-10-15T15:35:16Z`):

| lane | post-launch commits | exact lane identity present | authors observed |
|---|---|---|---|
| kasegi | 3 | yes | 3× `kasegi-shokunin <kasegi@shokunin.local>` |
| kengaku | 3 | yes | 3× `kengaku-shokunin <kengaku@shokunin.local>` |
| kake | 3 | yes | 3× `kake-shokunin <kake@shokunin.local>` |
| kumitate | 3 | yes | 3× `kumitate-shokunin <kumitate@shokunin.local>` |
| kotoba | 3 | yes | 3× `kotoba-shokunin <kotoba@shokunin.local>` |
| kagi | 3 | yes | 3× `kagi-shokunin <kagi@shokunin.local>` |
| kama | 2 | yes | 2× `kama-shokunin <kama@shokunin.local>` |
| mori | 2 | yes | 2× `mori-shokunin <mori@shokunin.local>` |
| protocol (ROOT) | 40 | yes (1) | 29× `ci <ci@local>`, 3× `r18-devin-opus <tower@local>`, 2× `r18-routing <r18-routing@tower.local>`, 2× `r18-glm-legorder <tower@local>`, 2× `r18-battery <r18-battery@tower.local>`, 1× `r18-opencode-probe <ci@local>`, 1× `protocol-shokunin <protocol@shokunin.local>` |
| aggregator (ROOT) | 40 | **no** | same mix as protocol — **zero aggregator-authored commits** |

Commands (per lane): `git -C <repo> log --after=@1792039857 --format='%an <%ae>'` piped to
`grep -Fxq "<lane>-shokunin <lane>@shokunin.local>"`; ROOT lanes read the fleet root.
Whether each mission is open-and-old (lifecycle rows 1-9) is **not** decided here; measured
states for reference: `.ufo/state/{mori,aggregator,kasegi,protocol,kagi}.round` =
`2,10,17,14,16`; kasegi's post-launch commit subjects cite lane-internal rounds 21/17 — the
numbering provenance is a lifecycle/cutover question, noted, not decided.

**r1 reference measured in the same command window (ts=2026-10-15T15:35:16Z)** — command
`env MORI_ROSTER_LANES="protocol aggregator kasegi kengaku kake kumitate kotoba kagi kama" MORI_LANE_SILENCE_S=900 bash tools/mori-census.sh`,
exit 1, census sha before == after (quoted excerpts):

```
SURFACE silence: drift (cmd=git -C <repo> log -1 --format=%ct; find <repo> -newermt @window; silent=7 progressing=2 progressing_weak=0 skipped=0 window_s=900; ts=2026-10-15T15:35:16Z)
FINDING LANE_SILENT severity=warn obs=lane=kasegi head_epoch=1792041688 newest_epoch=1792043037 window_s=900 ts=2026-10-15T15:35:16Z script_sha256=e3073a2b5e89bf717c1955e7a3d7bd995bf1096d61b6887af98b4517ee92f3f2
FINDING LANE_SILENT severity=warn obs=lane=kengaku head_epoch=1792073378 newest_epoch=1792073299 window_s=900 … (5 more findings: kake, kumitate, kotoba, kagi, kama)
MORI_CENSUS: DRIFT (findings=24 drift=21 unavailable=0 surfaces=7)
```

Two live divergences between the two measurements, one in each direction:

- **Under-credit:** r1 reads `kasegi` `LANE_SILENT` while kasegi authored 3 commits after its
  launch — commit sparsity is not silence (`PROTOCOL.md:165-166`); the r1 rolling window
  (900 s here) is not the launch anchor.
- **Over-credit:** r1 reads both ROOT lanes `progressing` from recent root activity; for
  `aggregator` that activity is not aggregator-authored (0 of 40 post-launch commits) — the
  r1 defect shape recorded at `SKILL.md:118-121` / `LOG.md:78-80`, reproduced fresh.

**Row-B residue datum (why no live grade is asserted here).** `git -C . status --porcelain=v1`
over the fleet root returns exactly 2 entries: `?? .ufo/waves/shokunin-train-20261015-w17/`
and `?? research/round-18-kimi-model-routing/battery/scripts/__pycache__/` (1 fresh post-launch
file). The proposed row-B scope (`silence-grading-r2.md:158-166`) excludes `.ufo/*` and nested
`*-shokunin/*`, so the residue a cutover must adjudicate for ROOT lanes is exactly that one
untracked `__pycache__` file. Fresh-mtime tracked files (`PROTOCOL.md`, `LOG.md`, …) are
tracked-clean and do not enter row B.

## Defects and corrections (report-only; this seat edits no other file)

**D1 — the identity recipe as printed matches nothing.** `corpus/knowledge/lane-silence-r2.md:112`
(= `corpus/knowledge/silence-grading-r2.md:128`, same shape) reads:

```
  | grep -Fxq "<lane>-shokunin <lane>@shokunin.local"
```

byte-verified (`od`) as ending `local"` — the closing `>` is missing. `-Fxq` requires the whole
line and `%an <%ae>` lines end with `>`, so the recipe never matches a real lane commit:

```
$ printf 'kagi-shokunin <kagi@shokunin.local>\n' | grep -Fxq 'kagi-shokunin <kagi@shokunin.local'; echo rc=$?
rc=1
$ printf 'kagi-shokunin <kagi@shokunin.local>\n' | grep -Fxq 'kagi-shokunin <kagi@shokunin.local>'; echo rc=$?
rc=0
```

A census implemented from the recipe verbatim would find zero lane-authored commits and
mis-grade every progressing lane. The corrected form (used by this check) is the second line.

**D2 — driver `gc()` dies on its first call** (re-confirms `SCORECARD.md:83-85`; mechanism now
pinned). `tools/mori-silence-cases.sh:201` runs
`commit -q --allow-empty -am "$msg" 2>/dev/null || …`, and `:208-215` is the fallback
`add && commit`. `&&` binds after the whole `||` chain, so when the first commit **succeeds** —
it does: `--allow-empty` permits an empty commit and `-a` stages nothing for an untracked
file — the third command (a plain `commit`) still runs and fails. Minimal repro (middle
lines elided as `…`):

```
$ git init -q r; cd r; echo x > LOG.md
$ (git -c commit.gpgsign=false commit -q --allow-empty -am 'old work' 2>/dev/null || git add -- LOG.md && git -c commit.gpgsign=false commit -q -m 'old work')
On branch master
… nothing added to commit but untracked files present (use "git add" to track)
chain rc=1
$ git log --oneline  → one empty commit        $ git status --porcelain=v1  → ?? LOG.md
```

The file is never staged, the fallback never runs, and the driver stops in case 1's first
fixture commit (live run at the sha cited: exit **1**, output ending in the same advice line —
same shape as `LOG.md:146-152`). Also `:214`
carries the typo `core.autcrlf=false` (should be `autocrlf`); measured non-fatal — git
ignores the unknown key, rc 0 — but the intended config is never applied.

**D2 supersession (same wave, measured).** The bytes D2 describes no longer exist in the tree:
a sibling seat rewrote the file during the wave (sha
`2cc205fc3666e1ab8b6ecf73228d86e2ae0515f915d4a4570f988327b3e6c11e`, measured 15:39Z; the
file has moved again since — every driver figure in this note is pinned to its measurement
clock). On the 15:39Z bytes the candidate completes all 27 cases; 17 fail semantically
against the r1 census — `MORI_SILENCE_CASES: matched=10 total=27`, exit 1, the seven
authorship cases (`:438-498`) among the failures. Whether the rewrite fixes the chain is the
harness seat's claim to make; D2 is preserved as the measured mechanism at the sha it names,
and the falsifiable claim below requires the passing tally regardless.

**D3 — `--after` precision items** are in the micro-semantics section above: inclusive at
equality, and it filters the committer date while the identity rows match the author fields.

## Falsifiable claim registered for the next round

```
CLAIM (register for the next round):
  Once the r2 census implementation (precondition 1) and the harness reconciliation
  (precondition 2) land, then
  (a) `bash tools/mori-silence-cases.sh` exits 0 with
      `MORI_SILENCE_CASES: matched=N total=M` and N=M, including the authorship
      cases at tools/mori-silence-cases.sh:445-498; and
  (b) a live r2 census run emits per-lane rows in which a lane with no
      exact-lane-authored commit over its launch window and at least one
      other-authored commit reads `progressing-weak` — never `progressing`,
      never `silent`.
  FALSIFIED BY: a sibling-only lane graded `progressing` or `silent`; a tally with
  N<M; or no tally at all.
Preconditions (cross-ref silence-grading-r2.md:209-229):
  1  census r2 in tools/mori-census.sh (r1 today; authorship deferred at :523-527)
  2  harness `gc` chain reconciled — was: exit 1 in fixture setup, no tally
     (sha 61db3df3…, 15:29Z); in-wave rewrite (sha 2cc205fc…, 15:39Z) runs all
     27 cases but matched=10 total=27, exit 1 — the passing tally is the target
  3  timeline grammar binding (live `pid=|runId=|mission=` vs fixture `TIMESTAMP … ts=`)
  4  report path reconciliation (.ufo/reports/round-<N>/<lane>.md vs reports/<lane>.md)
  5  admission/receipt binding (parent-owned)
  6  D1: the identity recipe corrected in the notes it is quoted from
```

## Evidence status

- **Claimed (re-runnable):** the check and its 10/10 receipt (extracted-file sha
  `9c91e0a0…`, git 2.55.0); the two git micro-semantics with their fixture commands;
  the live authorship table (read-only, 15:35Z, corrected pattern); the r1 receipt quoted
  above (exit 1, sha `e3073a2b…` stable across the run); the two divergences; the root
  porcelain datum (2 entries); D1 byte check; D2 repro; harness measurements — `rc=1`/no
  tally at sha `61db3df3…` (15:29Z) and `matched=10 total=27`/exit 1 at sha `2cc205fc…` (15:39Z).
- **Not claimed:** any *passing* `MORI_SILENCE_CASES` tally; any r2 census behavior; any live per-lane
  r2 grade (the lifecycle and row-B adjudications above are open); any receipt binding,
  promotion or native judgment. Live figures are mutable observations pinned to a clock
  (root commits at 15:35Z include ≤4-minute-old merges), not a frozen baseline.
- **Move verdict (for the parent's ledger; the parent owns SCORECARD.md):** **improved** for
  the `progressing-weak` proof — the deferred discrimination is now executable, executed and
  live-applied, with the recipe defect that would have defeated it corrected in the proof.
  No axis is claimed harmed; production admission remains **deferred** with the preconditions
  above.

## The check body (extracted by the command at the top of this note)

```
###CHECK-BEGIN
#!/usr/bin/env bash
# mori progressing-weak authorship check r1 (seat authorship-proof, round 2).
# Reference decision for the authorship table on real-git fixtures: exact-line
# author-identity matching over ALL post-launch commits. Hermetic: writes only
# under its own mktemp dirs; isolated HOME/config; pinned epochs; no census,
# no network, no host reads. Exit 0 iff every case matched.
set -euo pipefail

LAUNCH=1699998000   # authorship anchor (launch epoch for every case)
PRE=1699995000      # pre-launch commit
POST=1699998600     # post-launch commit
WORK=$(mktemp -d /tmp/mori-authorship-check.XXXXXX)
export MORI_PR_WORK=$WORK
trap 'rm -rf -- "${MORI_PR_WORK:-}"' EXIT INT TERM
mkdir -p "$WORK/home"

gitq() {
  env -i PATH=/usr/bin:/bin HOME="$WORK/home" TZ=UTC LC_ALL=C \
    GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null \
    git -c init.defaultBranch=main -c commit.gpgsign=false -c core.autocrlf=false "$@"
}

commit_as() { # <repo> <rel> <ct> <aname> <amail> [<cname> <cmail>]
  local d=$1 rel=$2 ct=$3 an=$4 ae=$5 cn=${6:-$4} ce=${7:-$5}
  mkdir -p "$d/$(dirname -- "$rel")"
  printf 'rel=%s ct=%s\n' "$rel" "$ct" > "$d/$rel"
  touch -d "@$ct" "$d/$rel"
  gitq -C "$d" add -- "$rel"
  env -i PATH=/usr/bin:/bin HOME="$WORK/home" TZ=UTC LC_ALL=C \
    GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null \
    GIT_AUTHOR_NAME="$an" GIT_AUTHOR_EMAIL="$ae" \
    GIT_COMMITTER_NAME="$cn" GIT_COMMITTER_EMAIL="$ce" \
    GIT_AUTHOR_DATE="@$ct +0000" GIT_COMMITTER_DATE="@$ct +0000" \
    git -c init.defaultBranch=main -c commit.gpgsign=false -c core.autocrlf=false \
    -C "$d" commit -q -m "$rel"
}

newrepo() { local d=$WORK/$1; mkdir -p "$d"; gitq init -q "$d"; printf '%s' "$d"; }

grade() { # <repo> <lane> -> progressing | progressing-weak | silent | unavailable
  local repo=$1 lane=$2 authors rc
  [ -d "$repo" ] || { printf 'unavailable'; return 0; }
  set +e
  gitq -C "$repo" rev-parse --git-dir >/dev/null 2>&1; rc=$?
  set -e
  [ "$rc" -eq 0 ] || { printf 'unavailable'; return 0; }
  set +e
  gitq -C "$repo" rev-parse --verify -q HEAD >/dev/null 2>&1; rc=$?
  set -e
  [ "$rc" -eq 0 ] || { printf 'silent'; return 0; }
  set +e
  authors=$(gitq -C "$repo" log --after=@"$LAUNCH" --format='%an <%ae>' 2>/dev/null); rc=$?
  set -e
  [ "$rc" -eq 0 ] || { printf 'unavailable'; return 0; }
  if printf '%s\n' "$authors" | grep -Fxq -- "$lane-shokunin <$lane@shokunin.local>"; then
    printf 'progressing'; return 0
  fi
  if [ -n "$authors" ]; then printf 'progressing-weak'; return 0; fi
  printf 'silent'
}

LANE=kagi
LNAME=kagi-shokunin;      LMAIL=kagi@shokunin.local
SNAME=aggregator-shokunin; SMAIL=aggregator@shokunin.local
PASS=0; TOTAL=0; FAILED=()

ck() { # <id> <want> <repo>
  local id=$1 want=$2 got
  TOTAL=$((TOTAL + 1))
  got=$(grade "$3" "$LANE")
  if [ "$got" = "$want" ]; then
    PASS=$((PASS + 1)); printf 'PASS %s (state=%s)\n' "$id" "$got"
  else
    FAILED+=("$id"); printf 'FAIL %s (want=%s got=%s)\n' "$id" "$want" "$got"
  fi
}

SELF_SHA=$(sha256sum "$0" 2>/dev/null | cut -d' ' -f1 || printf 'unknown')
printf 'mori-authorship-check r1 — git=%s — script_sha256=%s\n' "$(git --version)" "$SELF_SHA"
printf 'anchor LAUNCH=%s PRE=%s POST=%s LANE=%s\n' "$LAUNCH" "$PRE" "$POST" "$LANE"

# 1 — explicit lane authorship post-launch => progressing
r=$(newrepo lane-postlaunch)
commit_as "$r" base.md "$PRE" "$LNAME" "$LMAIL"
commit_as "$r" work.md "$POST" "$LNAME" "$LMAIL"
ck lane-postlaunch progressing "$r"

# 2 — lane commit hidden behind a later sibling HEAD commit => still progressing
r=$(newrepo lane-hidden-behind-sibling-head)
commit_as "$r" base.md "$PRE" "$LNAME" "$LMAIL"
commit_as "$r" work.md "$POST" "$LNAME" "$LMAIL"
commit_as "$r" sib.md "$((POST + 200))" "$SNAME" "$SMAIL"
ck lane-hidden-behind-sibling-head progressing "$r"

# 3 — pre-launch lane commit + sibling-only post-launch, clean => progressing-weak
r=$(newrepo sibling-only-clean)
commit_as "$r" base.md "$PRE" "$LNAME" "$LMAIL"
commit_as "$r" sib.md "$POST" "$SNAME" "$SMAIL"
ck sibling-only-clean progressing-weak "$r"

# 4 — author=sibling, committer=lane => attribution follows the author => weak
r=$(newrepo author-sibling-committer-lane)
commit_as "$r" base.md "$PRE" "$LNAME" "$LMAIL"
commit_as "$r" sib.md "$POST" "$SNAME" "$SMAIL" "$LNAME" "$LMAIL"
ck author-sibling-committer-lane progressing-weak "$r"

# 5 — author=lane, committer=sibling => still lane-authored => progressing
r=$(newrepo author-lane-committer-sibling)
commit_as "$r" base.md "$PRE" "$LNAME" "$LMAIL"
commit_as "$r" work.md "$POST" "$LNAME" "$LMAIL" "$SNAME" "$SMAIL"
ck author-lane-committer-sibling progressing "$r"

# 6 — name substring trap: kagi-helper-shokunin with exact email => not the lane
r=$(newrepo substring-name-trap)
commit_as "$r" base.md "$PRE" "$LNAME" "$LMAIL"
commit_as "$r" near.md "$POST" "kagi-helper-shokunin" "$LMAIL"
ck substring-name-trap progressing-weak "$r"

# 7 — email substring trap: exact name, kagi-helper@ email => not the lane
r=$(newrepo substring-email-trap)
commit_as "$r" base.md "$PRE" "$LNAME" "$LMAIL"
commit_as "$r" near.md "$POST" "$LNAME" "kagi-helper@shokunin.local"
ck substring-email-trap progressing-weak "$r"

# 8 — lane's only commit is pre-launch; nothing post-launch => silent
r=$(newrepo prelaunch-lane-commit-only)
commit_as "$r" base.md "$PRE" "$LNAME" "$LMAIL"
ck prelaunch-lane-commit-only silent "$r"

# 9 — repo with no commits at all => silent (no evidence, not unavailable)
r=$(newrepo empty-repo)
ck empty-repo silent "$r"

# 10 — repo path absent => unavailable (missing data must not become silent)
ck missing-repo unavailable "$WORK/no-such-repo"

printf 'MORI_AUTHORSHIP_CHECK: matched=%d total=%d\n' "$PASS" "$TOTAL"
[ "$TOTAL" -gt 0 ] || { printf 'mori-authorship-check: no cases executed\n' >&2; exit 2; }
if [ "$PASS" -eq "$TOTAL" ]; then exit 0; fi
printf 'mori-authorship-check: failed: %s\n' "${FAILED[*]}" >&2
exit 1
###CHECK-END
```