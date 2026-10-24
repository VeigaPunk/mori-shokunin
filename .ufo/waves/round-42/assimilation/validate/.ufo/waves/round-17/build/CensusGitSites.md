# CensusGitSites — git call map and C2 insertion points (round 17, wave 1)

Seat: `MoriR17.CensusGitSites-5` (scout, read-only). Lane census at
`/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-census.sh`
sha256 `f1f8d1b62bb617bbcc4664057ab807d3fed8c275b7aabbdf7b373323c5501ff7`
(identical to `git show 24526ea:tools/mori-census.sh`; 4189 lines).
Reference: `/home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh`
sha256 `3369dc27b4909a9d1c2def774b128fb4a8cb71953ac9b12de4c8519b9024e421` (711 lines).
Contract: `.ufo/waves/round-17/contract.md` §C2. Routed evidence:
`.ufo/waves/hyaku/jj-w1/reports/JjAuditMori.md` (F3/F4, rows 1/2/5/6).

Semantic-tool note: this seat exposes no `lsp` device (tool inventory has no `lsp`
tool; the mounted MCP routes are REA-only and do not index shell sources), so symbol
tracing used `read`/literal `grep` only. Every line below was read directly; claims
about intended runtime semantics are marked **[INFERENCE]**.

## Axes (godspeed)

1. **Correctness of the branch anchor** — resolve the same way `detect_branch` +
   `cmd_state` do, and never let a stub's empty output masquerade as a ref.
2. **Fixture compatibility** — 4 existing git verbs, 22 fixture-slot writes, 96
   `check` cases; the new probes must be inert unless a fixture supplies evidence.
3. **Gate observability** — each new finding must be provokable and each control
   (attached, detached-at-tip) must be structurally provable CLEAN.

## 1. Every git invocation (production code)

All production calls go through `GIT_BIN` (`MORI_GIT_BIN`, defined line 307) and
the `cap` helper (lines 548-556, which captures stdout+stderr and rc without `set -e`).

| # | line | exact argv (after `-C <repo>`) | class | C2 disposition |
|---|------|--------------------------------|-------|----------------|
| 1 | 2100 | `env GIT_OPTIONAL_LOCKS=0 git -C "$ROOT" cat-file -e "HEAD:$rpath"` | D (HEAD-anchored read) | row 6: replace `HEAD` with `refs/heads/$branch`; add the `-u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE` scrub (currently missing here — audit F10) |
| 2 | 2102 | `env GIT_OPTIONAL_LOCKS=0 git -C "$ROOT" log -1 --format=%ct -- "$rpath"` | D (default rev = HEAD) | row 6: insert the rev before `--`: `log -1 --format=%ct "refs/heads/$branch" -- "$rpath"`; same env scrub |
| 3 | 2129 | `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_OPTIONAL_LOCKS=0 git -C "$repo" rev-parse --git-dir` | D | unchanged: row-1 readability gate; hardware already correct |
| 4 | 2180 | `env … git -c core.fsmonitor=false -c core.quotePath=false -C "$repo" ls-files -mo --exclude-standard` | C | unchanged (audit F5/F6/F7 measured it jj-safe); row B input |
| 5 | 2197 | `env … git -C "$repo" rev-parse --verify -q HEAD` | D | row 9: verify the anchor rev (`refs/heads/$branch` when resolved, else `HEAD`); a second HEAD-only resolve is needed for the mismatch detail |
| 6 | 2207 | `env … git -C "$repo" log "${lg_args[@]}"` (implicit HEAD; root lanes add pathspecs) | D | row 9: append `"$rev"` **inside** `lg_args`, before the pathspec `--`; add a second log for committer identity (see §5) |

Not invocations:
- 2276 is a documentation string (`local cmd="git -C <repo> log … cat-file -e HEAD:…"`)
  emitted verbatim on the silence surface. It must be updated when the probes change,
  or the row advertises probes the code no longer runs.
- 2846-2859 is the selftest stub dispatcher (below); 2866 only symlinks `git`.
- Header/usage mentions (198-199, 223, 307, 393-394) are prose.

No other git call exists in the file: a `GIT_BIN` scan finds exactly lines
2100, 2102, 2129, 2180, 2197, 2207 plus definitions 223/307 and the env pin 2963.

Measured reference behavior (git 2.56.0, lane repo at 24526ea):

```
git symbolic-ref -q HEAD                         -> refs/heads/master          rc=0
git symbolic-ref -q refs/remotes/origin/HEAD     -> refs/remotes/origin/master rc=0
git show-ref -q --verify refs/heads/master       -> (no stdout with -q)        rc=0
git show-ref -q --verify refs/heads/main         ->                            rc=1
git merge-base --is-ancestor HEAD refs/heads/master                           rc=0
git merge-base --is-ancestor 984df90c… refs/heads/master  (other root)        rc=1
git rev-parse HEAD / refs/heads/master           -> 24526ea… both (equal)
ls -d .jj                                        -> present (lane is colocated)
```

`show-ref -q` prints **nothing on success** — a resolver must key the fallback on
rc, not on output (this is also why the stub needs explicit `.rc` files; §4).

## 2. Where the branch must come from

Mirror `jj-lane.sh:115-126` (`detect_branch`) plus the unique-master/main fallback of
`jj-lane.sh:162-167` (`cmd_state`):

1. `symbolic-ref -q HEAD` → `refs/heads/<b>` (only if `valid_branch`, `jj-lane.sh:85`).
2. `symbolic-ref -q refs/remotes/origin/HEAD` → `refs/remotes/origin/<b>`.
3. exactly one of `show-ref -q --verify refs/heads/master` / `refs/heads/main` (rc 0).

Two repos are queried for different rows:
- **row 6** always queries `$ROOT` (report paths are fleet-root-relative, census:2092-2096),
  so resolve `$ROOT`'s branch once per probe run.
- **row 9** queries the lane repo `$repo` (line 2115), so resolve per lane, after the
  repo-absent/readability gates (2124-2133), so an absent lane never triggers stub calls.

`valid_branch` must be replicated; a malicious or stub-echoed multi-line value must not
become a revspec. Suggested helper, inserted **after line 1975** (`is_int`, before
`in_lane_scope`):

```bash
# Mirror scripts/hyaku/jj-lane.sh valid_branch (:85): a branch name, never a revset.
is_branch_name() { # <name>
  case "$1" in ''|jj/*|*..*) return 1 ;; esac
  [[ $1 =~ ^[a-zA-Z0-9][a-zA-Z0-9._/-]*$ ]]
}
# Read-only branch resolution (detect_branch :115-126 + cmd_state :162-167).
# Empty/rc1 = unresolved; callers then keep the legacy HEAD behavior.
repo_branch() { # <repo> -> branch on stdout, rc 0
  local repo=$1 b c=0 cand=''
  cap env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_OPTIONAL_LOCKS=0 \
    "$GIT_BIN" -C "$repo" symbolic-ref -q HEAD
  if [ "$CAP_RC" -eq 0 ]; then
    b=${CAP_OUT%%$'\n'*}; b=${b//[[:space:]]/}
    case $b in
      refs/heads/*) b=${b#refs/heads/}
        if is_branch_name "$b"; then printf '%s' "$b"; return 0; fi ;;
    esac
  fi
  cap env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_OPTIONAL_LOCKS=0 \
    "$GIT_BIN" -C "$repo" symbolic-ref -q refs/remotes/origin/HEAD
  if [ "$CAP_RC" -eq 0 ]; then
    b=${CAP_OUT%%$'\n'*}; b=${b//[[:space:]]/}
    case $b in
      refs/remotes/origin/*) b=${b#refs/remotes/origin/}
        if is_branch_name "$b"; then printf '%s' "$b"; return 0; fi ;;
    esac
  fi
  cap env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_OPTIONAL_LOCKS=0 \
    "$GIT_BIN" -C "$repo" show-ref -q --verify refs/heads/master
  if [ "$CAP_RC" -eq 0 ]; then c=$((c + 1)); cand=master; fi
  cap env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_OPTIONAL_LOCKS=0 \
    "$GIT_BIN" -C "$repo" show-ref -q --verify refs/heads/main
  if [ "$CAP_RC" -eq 0 ]; then c=$((c + 1)); cand=main; fi
  [ "$c" -eq 1 ] || return 1
  printf '%s' "$cand"
}
```

Boundary to state in the code comment: when resolution fails the census keeps the old
`HEAD` anchor (no verdict change) rather than inventing a branch; the gate sandboxes
always resolve, so the delivered behavior is branch-anchored where a branch exists.

## 3. Exact insertion points — `refs/heads/<branch>`

Line numbers are the **entering** file; apply edits bottom-up or anchor on text.

### 3.1 row 6 — `ps_report_closed` (2097-2109)

- 2097 signature → `ps_report_closed() { # <lane> <round> <launch_epoch> <branch> -> rc 0 = closed`
- 2098 → `local lane=$1 round=$2 launch=$3 branch=${4:-}`
- 2099 → add `rev="HEAD"`; then `[ -n "$branch" ] && rev="refs/heads/$branch"`
- 2100 → `cap env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_OPTIONAL_LOCKS=0 "$GIT_BIN" -C "$ROOT" cat-file -e "$rev:$rpath"`
- 2102 → `cap env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_OPTIONAL_LOCKS=0 "$GIT_BIN" -C "$ROOT" log -1 --format=%ct "$rev" -- "$rpath"`

Call site: line 2188 → `ps_report_closed "$lane" "$LA_ROUND" "$LA_EPOCH" "$root_branch"`.
Resolution: in `probe_silence`, add `local … root_branch=''` to the declaration at 2277 and
insert after the ledger load (after 2283, before the loop at 2285):

```bash
  root_branch=$(repo_branch "$ROOT") || root_branch=''
```

`ps_report_closed` is best-effort by design (2093-2096); with an unresolved branch it
keeps `HEAD`, so a repo without master/main is not newly graded unavailable.

### 3.2 row 9 — `grade_lane` (2194-2237)

- 2195 locals → add `branch='' rev=HEAD head_sha='' br_sha='' n_ident=0`
- 2196 → replace `local expected` with `local expected="$lane-shokunin <$lane@shokunin.local>"`
  (it is needed by the mismatch scan; delete the re-assignment at 2231 to avoid drift)
- insert immediately after 2196, before the rev-parse at 2197:

```bash
  branch=$(repo_branch "$repo") || branch=''
  [ -n "$branch" ] && rev="refs/heads/$branch"
```

- 2197 → verify the anchor, not bare HEAD: `… rev-parse --verify -q "$rev"`
- 2198-2199 → unchanged; inside the `if`, capture the anchor hash:
  `br_sha=${CAP_OUT%%$'\n'*}; br_sha=${br_sha//[[:space:]]/}`
- 2200 → `local lg_args=(--since="@$LA_EPOCH" --format='%ct %an <%ae>' "$rev")`
  and add `local paths=()`; move the root-lane pathspec appends (2204-2206) onto
  `paths` (`paths+=(-- . ':(exclude).ufo' ':(exclude,glob)**/*-shokunin/**')`), then
- 2207 → `cap … "$GIT_BIN" -C "$repo" log "${lg_args[@]}" "${paths[@]+"${paths[@]}"}"`

Argument order is mandatory: the rev must sit **before** the `--` pathspec. Appending
`"$rev"` to the current `lg_args` after 2206 would place it after `--` and silently
turn it into a pathspec.

Empty-array note: the file already uses the `${X[@]+…}` guard shape (e.g. 2995), so
keep it for `paths` under `set -u`.

### 3.3 comment/doc updates

- 1944: `report at HEAD` → `report at refs/heads/<branch>`
- 1947-1951: add `anchor=refs/heads/<branch>` to the row-9 description and name the two
  new findings under row 9.
- 2097 comment “present at HEAD” → “present at `refs/heads/<branch>`”.
- 2194 heading `-- row 9: authorship` → `-- row 9: authorship (branch-anchored)`.
- 2276 `cmd=` string: replace `cat-file -e HEAD:` with `cat-file -e refs/heads/<branch>:`
  and add `symbolic-ref -q HEAD` / `merge-base --is-ancestor`.
- 241-261 finding-id block: add a line after 260:
  `#   HEAD_BRANCH_MISMATCH LANE_AUTHOR_MISMATCH` (before the closing `#` at 261).
- Optional observability: add `anchor=${rev}` to the row-A/C `GL_EXTRA` (2241, 2268)
  so a gate can assert branch anchoring on a non-finding row. Safe for existing
  selftest regexes (they match `^SURFACE lane\.kagi: progressing ` and `basis=row-A`).

## 4. Exact insertion points — the two findings

Both use `emit_finding` (406-418): only `warn|crit` flips the roll; “severity drift” in
the contract therefore maps to `severity=warn`.

### 4.1 `HEAD_BRANCH_MISMATCH` (insert after 2199, inside the `has_head` block)

```bash
    # C2: HEAD must be on the lane branch. Distinguish "not an ancestor" (rc 1 =
    # the finding) from an error (rc > 1 = not a mismatch; git-merge-base docs,
    # corpus S046). Only 40-hex inputs are compared, so stub/empty output is inert.
    if [ -n "$branch" ] && is_sha40 "$br_sha"; then
      cap env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_OPTIONAL_LOCKS=0 \
        "$GIT_BIN" -C "$repo" rev-parse --verify -q HEAD
      head_sha=${CAP_OUT%%$'\n'*}; head_sha=${head_sha//[[:space:]]/}
      if [ "$CAP_RC" -eq 0 ] && is_sha40 "$head_sha"; then
        cap env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_OPTIONAL_LOCKS=0 \
          "$GIT_BIN" -C "$repo" merge-base --is-ancestor "$head_sha" "$rev"
        if [ "$CAP_RC" -eq 1 ]; then
          emit_finding HEAD_BRANCH_MISMATCH warn \
            "lane=$lane head=${head_sha:0:7} branch=$branch branch_tip=${br_sha:0:7} basis=merge-base"
        fi
      fi
    fi
```

Add `is_sha40() { [[ ${1:-} =~ ^[0-9a-f]{40}$ ]]; }` next to `is_branch_name` (after 1975).
`br_sha` is the resolved `"$rev"` hash (2198), i.e. the branch tip; `head_sha` is a
second, explicit HEAD resolution. Using the captured hash instead of the literal `HEAD`
avoids a HEAD move between the two calls and is semantically identical.

Placement is before the log call, so the finding is emitted for every lane state that
reaches row 9 (including a later early `progressing` return at 2239) and before any
row-1 error inside the log block. Contract detail is satisfied: lane, short head,
short branch tip.

### 4.2 `LANE_AUTHOR_MISMATCH` (insert after 2212; emit before 2239)

Identity scan needs the committer, which the current `%ct %an <%ae>` format does not
carry. Use a second `log` invocation (same window and pathspecs, tab-separated fields)
rather than changing the rate-sensitive author parse at 2213-2235:

```bash
    cap env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_OPTIONAL_LOCKS=0 \
      "$GIT_BIN" -C "$repo" log --since="@$LA_EPOCH" \
      --format='%ct%x09%cn <%ce>%x09%an <%ae>' "$rev" "${paths[@]+"${paths[@]}"}"
    if [ "$CAP_RC" -eq 0 ]; then
      ident=$(awk -F'\t' -v lo="$LA_EPOCH" -v hi="$NOW_EPOCH" \
        'NF==3 && $1 ~ /^[0-9]+$/ && $1+0 > lo+0 && $1+0 <= hi+0 { print }' <<< "$CAP_OUT")
      if [ -n "$ident" ]; then
        n_ident=$(awk -F'\t' -v exp="$expected" \
          '$2 == exp && $3 != exp { n++ } END { print n + 0 }' <<< "$ident")
      fi
    fi
```

Emit after the `inwin` block closes (after 2237, before the `subj` return at 2239):

```bash
  if [ "$n_ident" -gt 0 ]; then
    emit_finding LANE_AUTHOR_MISMATCH warn \
      "lane=$lane round=$LA_ROUND commits=$n_ident committer=$expected basis=row-9"
  fi
```

Rules encoded: exact whole-field identity (`$2 == exp`), post-launch strict window
(`> launch`, `<= NOW`, same as the author pass), branch rev, root-lane pathspecs, and
no pipeline into an early-exit consumer (the F01 lesson at 2217-2225). If the identity
log errors, no finding is emitted (an unreadable scan is not evidence of a violation);
optionally disclose `ident_scan=unavailable` in the row extra — do not flip the verdict.

`grep`-free membership also keeps the 12k-history case linear: two awk passes, no
producer feeding a reader.

## 5. Stub-git dispatcher (2846-2866) — exact anatomy and insertion

```
2846  git)
2847    verb=''
2848    for a in "$@"; do
2849      case "$a" in
2850        rev-parse) verb=rev-parse; break ;;
2851        ls-files) verb=ls-files; break ;;
2852        cat-file) verb=cat-file; break ;;
2853        log)
2854          case " $* " in *" -1 "*) verb=log1 ;; *) verb=log ;; esac
2855          break ;;
2856      esac
2857    done
2858    [ -n "$verb" ] || verb=other
2859    out_of "git-$verb"; exit "$(rc_of "git-$verb")" ;;
2860  esac
2861  printf 'fixture dispatcher: unknown %s\n' "$name" >&2
2862  exit 96
2863  STUB
2864  chmod 700 "$bin/.dispatch"
2865  local c
2866  for c in pgrep journalctl df tmux git; do ln -s .dispatch "$bin/$c"; done
```

`out_of`/`rc_of` (2786-2787) answer from `$fx/stub/<slot>` and `<slot>.rc`; **an absent
file answers empty output with rc 0** (2779-2783). That default is the main falsifier
for this change: an empty `symbolic-ref` result and two rc-0 `show-ref` answers must be
treated as unresolved/ambiguous, never as “branch present”.

Replace 2848-2857 with:

```bash
    for a in "$@"; do
      case "$a" in
        rev-parse)
          case " $* " in
            *" refs/heads/"*) verb=rev-parse-branch ;;
            *) verb=rev-parse ;;
          esac
          break ;;
        symbolic-ref)
          case " $* " in
            *" refs/remotes/origin/HEAD"*) verb=symbolic-ref-origin ;;
            *) verb=symbolic-ref ;;
          esac
          break ;;
        show-ref)
          case " $* " in
            *" refs/heads/main"*) verb=show-ref-main ;;
            *) verb=show-ref-master ;;
          esac
          break ;;
        merge-base) verb=merge-base; break ;;
        ls-files) verb=ls-files; break ;;
        cat-file) verb=cat-file; break ;;
        log)
          case " $* " in
            *"%cn"*) verb=log-ident ;;
            *" -1 "*) verb=log1 ;;
            *) verb=log ;;
          esac
          break ;;
      esac
    done
```

Why each split exists:
- `rev-parse` stays the legacy slot for `--git-dir` (2129) and `HEAD` (mismatch), so
  `sil-git-unreadable` (`git-rev-parse.rc=128`, 3782) keeps grading row-1 unchanged.
  Branch verification gets `git-rev-parse-branch`.
- `symbolic-ref` needs two answers: attached HEAD and origin/HEAD fallback.
- `show-ref` needs per-candidate rcs (with `-q`, success has no stdout).
- `log` is already split on `-1`; `%cn` identifies the identity call. Check `%cn`
  first; the identity call has no `-1` today but ordering makes the intent explicit.
- Slot names are free: the only existing slots are `git-cat-file`, `git-log`,
  `git-log1`, `git-rev-parse` (verified by scan; no collisions).

Update the comment at 2927-2929 to list `symbolic-ref / symbolic-ref-origin /
show-ref-master / show-ref-main / merge-base / rev-parse-branch / log-ident`.

## 6. How selftest lanes are built, and how a fixture sets HEAD/log output

`run_selftest` (2762) is hermetic:

- 2768: `MORI_SELFTEST_WORK=$(mktemp -d /tmp/mori-census-selftest.XXXXXX)` — **absolute
  `/tmp`, ignores `$TMPDIR`**. A seat running this selftest is required to use
  `TMPDIR=<clone>/.scratch`; with this line the selftest still writes `/tmp`. For a
  compliant run the census must change it to
  `mktemp -d "${TMPDIR:-/tmp}/mori-census-selftest.XXXXXX"` and update the claims at
  198-199 and 393-394. This is a one-file change and a hard prerequisite for the
  executor’s own selftest under the wave rules.
- 2770-2773: EXIT/INT/TERM trap chmods then removes the work tree.
- 2784-2863: the dispatcher above; 2864-2866 installs it as `$work/bin/{pgrep,journalctl,df,tmux,git}`.
- `fx_quiet` (2882-2932) builds the baseline fixture:
  `ufo/state`, `ufo/waves`, `stub/`, `cgroup/`, `lanes/kagi-shokunin`, `root/`, a
  watchdog log, one settled wave, cgroup/meminfo/diskstats/uptime files, tmux stubs,
  and (2927-2931) the git comment + `lanes/kagi-shokunin/LOG.md`.
- `sut_env` (2941-2974) is the single env every invocation gets, via
  `env -i "${SUT_ENV[@]}" … bash "$SELF"` (2995): `PATH=$bin:/usr/bin:/bin`,
  `MORI_FIXTURE=$FX`, `MORI_SHOKUNIN_ROOT=$FX/root`, `MORI_UFO_DIR=$FX/ufo`,
  `MORI_FLEET_CONF=$FX/root/shokunin.conf`, `MORI_GIT_BIN=$bin/git`,
  `MORI_ROSTER_LANES=kagi`, `MORI_NOW_EPOCH=${PIN_NOW:-1700000000}`,
  `MORI_LANE_SILENCE_S=7200`, plus every journal/cgroup/disk override.
- A lane repo is **`$FX/root/<lane>-shokunin`** (`lane_repo`, 1967-1972); root lanes
  (`protocol|aggregator`) use `$FX/root` (`is_root_lane`, 1974). Cases create it with
  `mkdir -p "$FX/root/kagi-shokunin"`; the `$FX/lanes/…` tree is only the watchdog
  freshness path, not a lane repo.
- Roster: `MORI_ROSTER_LANES` wins (`resolve_roster`, 442-447); cases override it via
  `EXTRA_ENV=(MORI_ROSTER_LANES=…)`.
- `check` (2976-3050): freshens mtimes to `env_now` unless `SKIP_FRESHEN=1`; hashes the
  fixture before/after (`fx_no_mutation`); runs the census with `2>&1`; asserts exact
  rc, `^MORI_CENSUS: <verdict> `, absence of bash diagnostics, then every regex;
  resets `EXTRA_ENV`. There is **no negative-regex assertion**, so “no finding” is
  proven structurally by `CLEAN` + `progressing` (any `warn` would flip DRIFT).
- `PIN_NOW` is first set at 3090; `ts_iso` at 3175.

Fixture recipes (silence block, 3636-3798):

| fact | fixture file | shape |
|------|--------------|-------|
| HEAD sha / rev-parse rc | `$FX/stub/git-rev-parse[.rc]` | 40-hex line; rc file e.g. `128` (3782) |
| branch tip sha | new `$FX/stub/git-rev-parse-branch[.rc]` | 40-hex line |
| attached HEAD | new `$FX/stub/git-symbolic-ref[.rc]` | `refs/heads/master`; `.rc=1` for detached |
| origin/HEAD | new `$FX/stub/git-symbolic-ref-origin` | `refs/remotes/origin/master` |
| master/main fallback | new `$FX/stub/git-show-ref-{master,main}.rc` | `0` / `1` (no stdout with `-q`) |
| ancestry | new `$FX/stub/git-merge-base.rc` | `0` ancestor, `1` not ancestor, `>1` error |
| post-launch authors | `$FX/stub/git-log` | `"<ct> <an> <<ae>>"` per line (3647, 3658, 3705) |
| report-path commit ct | `$FX/stub/git-log1` | `<ct>` (3748) |
| report path presence | `$FX/stub/git-cat-file.rc` | `0` present / `1` absent (3628, 3747) |
| committer/author pairs | new `$FX/stub/git-log-ident` | `"<ct>\t<cn> <<ce>>\t<an> <<ae>>"` per line |
| modified/untracked | `$FX/stub/git-ls-files` | path lines (row B) |

Baseline additions in `fx_quiet` (insert after 2926, before the comment at 2927):

```bash
    printf 'refs/heads/master\n' > "$d/stub/git-symbolic-ref"; printf 0 > "$d/stub/git-symbolic-ref.rc"
    printf 'refs/remotes/origin/master\n' > "$d/stub/git-symbolic-ref-origin"
    printf 0 > "$d/stub/git-show-ref-master.rc"
    printf 1 > "$d/stub/git-show-ref-main.rc"
    printf '0123456789abcdef0123456789abcdef01234567\n' > "$d/stub/git-rev-parse"
    printf '0123456789abcdef0123456789abcdef01234567\n' > "$d/stub/git-rev-parse-branch"
    printf 0 > "$d/stub/git-merge-base.rc"
```

This makes every existing case traverse the new resolver and the ancestry check with
head == branch tip, so the ~60 existing cases become control coverage against false
positives. Cases that set `git-rev-parse.rc=128` still die at row 1 (2129) unchanged.

New cases (insert after 3798, before the `wave-age-unreadable` case at 3800):

1. `jj-head-ahead`: `git-rev-parse` = `1111…`, `git-rev-parse-branch` = `2222…`,
   `git-merge-base.rc=1`, `git-log` subject post-launch, `git-log-ident` committer ==
   author == lane, `git-cat-file.rc=1`. Expect `1 DRIFT`,
   `FINDING HEAD_BRANCH_MISMATCH severity=warn`, detail
   `lane=kagi head=1111111 branch=master branch_tip=2222222`, and
   `^SURFACE lane\.kagi: progressing ` (proves grading still used the branch).
2. `jj-author-mismatch`: head == branch tip, merge-base 0; `git-log` author
   `outsider <outsider@example.invalid>` post-launch; `git-log-ident` line
   `1699998600\tkagi-shokunin <kagi@shokunin.local>\toutsider <outsider@example.invalid>`.
   Expect `1 DRIFT`, `FINDING LANE_AUTHOR_MISMATCH severity=warn .* commits=1`,
   row `progressing-weak` (row-C).
3. `jj-detached-at-tip`: `printf 1 > git-symbolic-ref.rc` and remove the output file;
   origin slot still `refs/remotes/origin/master`; head == branch tip; merge-base 0;
   subject commit. Expect `0 CLEAN` + `progressing` — CLEAN structurally proves neither
   new finding fired while the resolver still found master through origin/HEAD.
4. `plain-attached-control`: baseline shape (attached HEAD == branch tip, merge-base 0)
   plus a subject commit → `0 CLEAN`, `progressing`, `basis=row-A`.

Also keep the existing subject/pre-launch/weak cases untouched: they now double as
controls that a committer-less `git-log` fixture cannot fabricate a mismatch.

## 7. Gate observability (handoff to JjGate / L1)

The gate builds real colocated sandboxes; the census reads them with real git because
`MORI_GIT_BIN` is unset (contract §C2 gate). Reference sequence in
`jj-lane.sh`: `metaedit --update-author` (596-601), `jj commit` (602-605),
`bookmark set` **after** the commit (658-659). Therefore:

- **A. HEAD ahead of branch (no mismatch control):** commit via jj, do **not** run
  `bookmark set`. `HEAD` is the new commit, `refs/heads/<b>` is its parent →
  `merge-base --is-ancestor HEAD refs/heads/<b>` = rc 1 → `HEAD_BRANCH_MISMATCH`.
  The entering census grades from HEAD and emits nothing for this case (its assertion
  “finding present” must fail).
- **B. author ≠ lane, committer = lane:** commit with per-command `user.name=lane-shokunin`
  but without `metaedit --update-author`, with the sandbox’s ambient identity as author;
  then `bookmark set <b> -r <commit>`. Post-launch → `LANE_AUTHOR_MISMATCH`; entering
  census folds it into `other_authored_commits` (assertion fails).
- **C. detached HEAD at branch tip:** `bookmark set` to the same commit jj left `HEAD`
  on → rc 0, no finding; passing under both censuses.
- **D. plain git repo:** attached, head == branch tip → no findings, identical verdict
  and exit under both censuses (control).
- Errors: `merge-base` rc > 1 must not count as a mismatch; a sandbox with no
  master/main resolves nothing and must not be graded drift.

Census env the gate must stub so no live probe runs (from `sut_env`, 2941-2974):
`MORI_JOURNALCTL_BIN`, `MORI_TMUX_BIN`, `MORI_PGREP_BIN`, `MORI_DF_BIN`,
`MORI_CGROUP_EVENTS/_SERVICE_EVENTS/_LOCAL_EVENTS/_CURRENT/_PRESSURE/_MAX`,
`MORI_MEMINFO`, `MORI_DISKSTATS`, `MORI_UPTIME`, `MORI_WATCHDOG_LOG`,
`MORI_TIMELINE_FILE`, `MORI_STATE_DIR`, `MORI_WAVES_DIR`, `MORI_ROSTER_LANES`,
`MORI_NOW_EPOCH`. The branch probes need **real git**, so leave `MORI_GIT_BIN` unset
for sandbox cases.

## 8. Risks / falsifiers for the executor

1. **Stub rc-0 default.** Absent `git-symbolic-ref` answers rc 0 with empty output;
   absent `git-show-ref-master/main` answers rc 0 for both. A resolver that trusts rc
   alone concludes “branch present” twice, or `refs/heads/` empty. Count rc for
   show-ref, require a shape-valid symbolic-ref value, and require 40-hex hashes
   before any mismatch computation.
2. **rc > 1 is not a mismatch.** Only `--is-ancestor` rc 1 means “not an ancestor”
   (measured here; corpus S046 draft states the same). Collapsing 128 into the finding
   would misreport an unreadable repo.
3. **Argument order.** `git log --since=… --format=… <rev> -- <pathspec>`: the rev must
   precede `--`. The current code appends pathspecs to `lg_args` (2204-2206), so the rev
   must be inserted at 2200 or the pathspec/rev roles invert.
4. **No early-return hole.** Both findings must be emitted before the `subj` return at
   2239; otherwise a progressing lane never reports a mismatch.
5. **F01 pipe rule.** Parse with `awk … <<< "$var"` and whole-field equality; do not
   pipe a 12k-line producer into an early-exit consumer (2217-2225).
6. **`set -u` + empty arrays.** Use the `${paths[@]+"${paths[@]}"}` guard already used
   elsewhere in the file.
7. **`/tmp` in the selftest.** Line 2768 writes to absolute `/tmp`; the wave rules
   require `TMPDIR=<clone>/.scratch`. Patch to `${TMPDIR:-/tmp}` and update 198-199 /
   393-394, or the executor’s own selftest run violates the scratch rule.
8. **Pinned baselines.** `--pin` baselines are non-volatile on findings; a baseline
   pinned by the entering census will drift against the delivered census by design.
   The in-script pin/drift cases re-pin each run, so `--selftest` stays green.
9. **Root lanes.** `protocol|aggregator` use `$ROOT` as their repo, so their row-9
   branch is the fleet root’s branch; keep the pathspec excludes unchanged (2204-2206)
   or row A will start counting `*-shokunin/**` commits.
10. **Live noise.** `HEAD_BRANCH_MISMATCH` is not launch-window-gated; every unbookmarked
    jj working-copy parent (the normal gap between `jj commit` and `bookmark set`,
    `jj-lane.sh:602-659`) will grade DRIFT. That is the contract’s stated semantics,
    but L1 should be told it is a noisy-by-design signal, not a fault.
11. **Live baseline (observed today).** Lane `.jj` exists; `HEAD` == `refs/heads/master`
    == `24526ea…`. Last 25 branch commits with a `mori-shokunin` committer all carry the
    lane author too, so neither finding would fire on the lane at this tip
    (read-only `git log --format='%h|%an <%ae>|%cn <%ce>|%ci' -25 refs/heads/master`).

## 9. Verification commands actually run (read-only)

| command | result |
|---|---|
| `sha256sum tools/mori-census.sh` and `git show 24526ea:tools/mori-census.sh \| sha256sum` | both `f1f8d1b6…`, exit 0 |
| `git -C . rev-parse HEAD` / `refs/heads/master` | `24526ea…` both |
| `git merge-base --is-ancestor HEAD refs/heads/master` | rc 0 |
| `git merge-base --is-ancestor 984df90c… refs/heads/master` | rc 1 (second root, measured) |
| `git symbolic-ref -q HEAD` | `refs/heads/master`, rc 0 |
| `git symbolic-ref -q refs/remotes/origin/HEAD` | `refs/remotes/origin/master`, rc 0 |
| `git show-ref -q --verify refs/heads/master` / `main` | rc 0 / rc 1 (no stdout with `-q`) |
| `git --version` | 2.56.0 |
| `ls -d .jj` | present (colocated) |
| `wc -l tools/mori-census.sh` | 4189 |

No selftest was run: it is not this item’s command, and line 2768 would write `/tmp`.
No installs, no pacman, no VCS mutation, no `/tmp` writes. The report file is the only write.

## 10. Remaining unknowns

- Whether L1 wants unresolved-branch repos to stay on `HEAD` (recommended, preserves
  every existing verdict) or to be graded unavailable. Contract does not say; the gate
  always resolves, so it cannot decide this.
- Whether `HEAD_BRANCH_MISMATCH` should be gated to the launch window. Contract §C2
  states no window; the current draft treats it as always-on.
- Exact gate case count/assertion vocabulary (`match|mismatch|capability_absent` style)
  is JjGate’s; this report specifies the six sandbox states and their expected finding
  presence, not the gate’s file format.
- The `--drift` non-volatile field set after adding `anchor=` (if adopted) is a
  deliberate baseline change; no consumer of pinned baselines was checked by this seat.
