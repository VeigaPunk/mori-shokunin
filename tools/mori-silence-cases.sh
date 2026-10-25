#!/usr/bin/env bash
# mori-silence-cases.sh — behavioral counting driver for mori-census.sh lane
# silence grading (mori-shokunin r2). Scenario-owner file; census internals
# belong to the implementation owner.
#
# Usage:
#   bash tools/mori-silence-cases.sh [path-to-census]
#     census path default: <this dir>/mori-census.sh
#     exit 0 iff every case matched; setup failure exits 2.
#   bash tools/mori-silence-cases.sh --selftest
#     bounded self-check over this case table's own fixtures (it never runs the
#     suite): table structure, the final-roll grader, state parsing, seed
#     determinism, then three case functions end to end against the real census.
#     Prints MORI_SILENCE_CASES_SELFTEST pass=<n> fail=<n>;
#     exit 0 all checks passed, 1 a check failed, 2 setup. Fixtures live under
#     $TMPDIR (absolute, required) and are removed on exit.
#
# What it does:
#   Builds per-case hermetic fixture trees (temp dirs, removed on exit) with
#   REAL git repositories and REAL author/committer identities (deterministic
#   commit dates via GIT_*_DATE, file mtimes via touch -d @epoch), a pinned
#   clock (MORI_NOW_EPOCH=1700000000), and quiet host stubs (pgrep/journalctl/
#   df/tmux dispatcher; no network; git is the real binary from /usr/bin).
#   The launch/close ledger is the REAL watchdog log: fixtures append
#   real-grammar lines to $MORI_UFO_DIR/watchdog.log in file order — the same
#   file the live driver writes (scripts/shokunin-watchdog.sh:81,83,106,109).
#   Each case runs the actual census CLI (bash "$CENSUS", no --selftest) and
#   grades behavior only: exact per-lane state, presence/absence of the
#   LANE_SILENT finding, census exit rc and the MORI_CENSUS final roll graded
#   against its admitted grammar (see "Verdict integrity" below). It never
#   greps census source, wiring, or default constants.
#   Anti-sniff: every case tree is a mktemp dir carrying NO case id in any
#   path handed to the census (MORI_SHOKUNIN_ROOT / MORI_UFO_DIR / MORI_STUB_DIR
#   / ...), and no fixture-marker variable is exported; case `shape-invariance`
#   proves a census cannot branch on the fixture directory name. Every fixture
#   also carries per-run fresh content (nonce token + run salt), so a memorized
#   content table from a previous run has no key to match.
#
# Output (one line per case in SHUFFLED order, then the run header, then the
# tally — r6: the header is printed only AFTER the last case has run):
#   PASS <id> ... | FAIL <id> ... (one line per case; no run secrets)
#   SHUFFLE_SEED=<seed>           seeds the case-order shuffle
#   RUN_NONCE=<nonce>             per-run fixture nonce every case must echo
#   CASE_ORDER=<id> <id> ...      the order this run executed
#   MORI_SILENCE_CASES: matched=N total=M
#   exit 0 iff matched == total.
#
# Verdict integrity (r13, closes audit-r11 F02 / Appendix C). Every case grades
# the FINAL ROLL, not the presence of a prefix — including the two guards that
# do not go through assert_case (readonly-no-mutation, shape-invariance). The
# admitted contract is the census's own:
#   MORI_CENSUS: CLEAN|DRIFT (findings=N drift=M unavailable=U surfaces=S)
# and it is satisfied only when ALL of these hold:
#   * exactly ONE line begins `MORI_CENSUS:` — a second roll is ambiguous, so it
#     is a FAIL, not a "last line wins";
#   * that line matches the whole grammar above — a substituted word (r11's
#     proxy renamed CLEAN/DRIFT to BANANA and kept the real rc) or a mangled
#     tail is a FAIL, not an accepted prefix;
#   * that line is the LAST non-empty line of the run — "final" means final; a
#     valid-looking roll followed by more output is a replayed or moved roll;
#   * the process rc is the word's contract: CLEAN => 0, DRIFT => 1. CLEAN with
#     rc 1 and DRIFT with rc 0 are FAILs; rc > 1 is a crash and is rejected
#     before the roll is read (never graded as DRIFT);
#   * the word agrees with drift=: ROLL flips to DRIFT exactly when a warn|crit
#     finding increments N_DRIFT (`emit_finding` warn|crit branch), so CLEAN
#     with drift>0 and DRIFT with drift=0 are FAILs. surfaces= and unavailable=
#     are NOT cross-counted: lane rows bypass emit_surface and append to
#     SURFACE_LINES directly (`SURFACE_LINES+=("SURFACE lane.` in
#     probe_silence);
#   * no raw target bytes reach per-case stdout: a malformed roll is echoed
#     through redact(), because it can carry the per-run nonce.
# corpus/knowledge/audit-r11.md:156,376-407; census usage() "Verdict:" contract
# and run_census's final `printf 'MORI_CENSUS: ...'` (line numbers shift under
# the round-13 census rewrite — cite the symbols, not the lines).
#
# Run-order channel (r5). Round 4 admitted one residual spoofing channel: the
# cases ran in fixed source order and carried no per-run secret, so a census
# with no grading logic could count its own invocations and replay a canned
# grade sequence (corpus/knowledge/verdict-machine-r4.md §2.4). Two independent,
# unpredictable-per-run defenses; both are logged in the header:
#   * seeded shuffle — Fisher-Yates over the 28 case ids driven by a local
#     xorshift32 seeded from RUN_SEED (pin: MORI_SHUFFLE_SEED=<int>; same seed
#     => same order). Invocation position does not map to a case identity.
#   * per-run nonce — RUN_NONCE is generated independently of the seed
#     (pin: MORI_RUN_NONCE=<int>), exported to the census as MORI_RUN_NONCE,
#     written into every fixture (a $CASE_DIR/run-nonce file and a
#     $CASE_DIR/nonce-<N> directory) and handed to the census as its disk
#     target, so the census's own disk row echoes the literal token `nonce-<N>`.
#     Every case requires the CURRENT run's token in its census output: a
#     canned answer is missing it, a replayed answer carries a stale one — both
#     FAIL the case.
#
# Stdout/environ backchannel (r6, closes r5 residual R1). The r5 revision logged
# the run header BEFORE the case loop, so a same-user census could read
# SHUFFLE_SEED/RUN_NONCE/CASE_ORDER from this process while it ran: through
# /proc/<oracle>/fd/1 when stdout is a captured regular file, and through
# /proc/<oracle>/environ when the operator pinned MORI_SHUFFLE_SEED (the pin
# arrives through the environment). Both channels are closed here:
#   * the header is printed only AFTER every case has run — during the loop only
#     PASS/FAIL lines appear, and those carry no run secret (failure texts
#     redact the nonce token; case ids were never secret);
#   * the pinned values are removed from the process tree before any census can
#     run: when a pin is present, the oracle re-execs itself once with the pins
#     dropped from its environment and passes them through a pipe fd (drained at
#     startup; no env, no argv, no file). /proc/<oracle>/environ shows the
#     exec-time environment, so the re-exec — not a runtime `unset` — is what
#     scrubs the channel (measured 2026-10-15; see the re-exec block below).
#
# Content-keyed memorization (r6, closes r5 residual R2). A census that learned
# a (fixture bytes -> output row) table from one observed run could replay it
# because every fixture was byte-stable across runs apart from the nonce
# artifacts it could exclude by name. Now every fixture's content is per-run:
#   * the live nonce token and a per-run RUN_SALT are woven into every committed
#     file body and every commit message, so the .git objects change too;
#   * case_skeleton adds per-run salt/blob files (random names and content)
#     under CASE_DIR, outside every graded tree — a memorized fingerprint cannot
#     match, and file-count variation is not pattern-normalizable.
# Tables learned from a previous run are therefore stale; the round-6 note lists
# the discriminating cases and the residual normalizing-attacker class.
#
# Grading against old (r1 rolling-window) and new (r2 launch-aware) census:
#   If the census emits per-lane rows `SURFACE lane.<id>: <state> (...)` the
#   observed state is read from the lane row (api=lane). Otherwise, for these
#   single-lane-roster fixtures, the state is DERIVED from the aggregate
#   `SURFACE silence:` counters (silent=/progressing=/progressing_weak=/
#   skipped=), the LANE_SILENT finding and the rc (api=aggregate). `total` is
#   independent of which row API the census provides, so genuinely correct
#   baseline behavior counts as matched; only semantic/lifecycle/attribution
#   differences decide improvement. Honest tally, not a green stamp: against
#   the r1 census the launch/closure/attribution cases FAIL by design — those
#   failures ARE the measured r2 contract gap, and the count is reported as-is.
#
# Census-side interface this driver assumes (r2 contract; the grammar and the
# paths are the LIVE-measured ones, anchored in
# corpus/knowledge/lane-silence-r2.md and in the live probes cited below):
#   ledger file            $MORI_UFO_DIR/watchdog.log — the file the live
#                          driver appends to (scripts/shokunin-watchdog.sh:81,
#                          83,106,109,114). The driver writes the fixture
#                          ledger there and exports MORI_TIMELINE_FILE to the
#                          same path, so an implementation exposing that
#                          override reads the identical source. There is no
#                          separate synthetic ledger file.
#   ledger line grammar    "<ISO-8601+offset> launch <lane> round=<N> pid=<pid>"
#                          "<ISO-8601+offset> launch <lane> round=<N> runId=<rid>"
#                          "<ISO-8601+offset> complete <lane> round=<N>; respawning"
#                          "<ISO-8601+offset> wrap <lane> round=<N> complete; NOT respawning (fleet-wrap)"
#                          "<ISO-8601+offset> steer <lane> -> round <N>"  (legacy)
#                          "launch-fail" never starts a mission. Three launch
#                          tails occur live (measured 50 pid= / 93 runId= /
#                          4 mission= lines; silence-grading-r2.md:234), so
#                          the parser must ignore the tail field — the cases
#                          exercise all three.
#                          Line order = event order; the later line wins.
#   states                 silent | progressing | progressing-weak | young |
#                          not-open | unavailable
#   lane identity          author name "<lane>-shokunin" AND email
#                          "<lane>@shokunin.local" (exact match, both fields)
#   report close path      ".ufo/reports/round-<N>/<lane>.md" in the
#                          fleet-root repo (live probe: `git cat-file -e
#                          HEAD:.ufo/reports/round-10/aggregator.md` rc 0;
#                          `report_of()` at scripts/shokunin-watchdog.sh:45);
#                          closure = committed at HEAD AND latest commit
#                          touching that path has %ct strictly > latest
#                          matching launch AND %ct <= NOW
#   gate                   grade only when NOW - launch_epoch > LANE_SILENCE_S
#                          (strictly greater; age exactly gate => young)
#
# Determinism: fixed epoch NOW=1700000000 (unchanged since r5 — the per-run
# nonce is a fixture/target token, not a clock shift), LANE_SILENCE_S=900,
# TZ=UTC, LC_ALL=C, env -i census runs, single lane in MORI_ROSTER_LANES per
# case. Per-run variation: the case ORDER, the fixture nonce/nonce token, and
# the content salt (never pinnable, never printed, never grade-bearing). Pin
# seed+nonce (MORI_SHUFFLE_SEED / MORI_RUN_NONCE) for the same order and nonce;
# pinned stdout stays byte-identical because no case's grade depends on the salt.
# Writes happen only under the fresh mktemp work dir; census must not mutate
# any fixture (guarded by case readonly-no-mutation).
set -euo pipefail
set +o xtrace

SELF=$(readlink -f -- "${BASH_SOURCE[0]}" 2>/dev/null || {
  p=$0
  case "$p" in /*) printf '%s' "$p" ;; *) printf '%s' "$PWD/$p" ;; esac
})
SCRIPT_DIR=$(cd -- "$(dirname -- "$SELF")" && pwd)
# --selftest is an argv branch of its own, never a census path: it runs the
# bounded self-check below and never the suite.
SELFTEST=0
case "${1:-}" in
  --selftest) SELFTEST=1; shift ;;
esac
CENSUS=${1:-$SCRIPT_DIR/mori-census.sh}
[ $# -gt 1 ] && { printf 'usage: mori-silence-cases.sh [path-to-census]\n       mori-silence-cases.sh --selftest\n' >&2; exit 2; }
[ "$SELFTEST" = 1 ] && [ $# -gt 0 ] && { printf 'mori-silence-cases: --selftest takes no census path\n' >&2; exit 2; }
[ -f "$CENSUS" ] && [ -r "$CENSUS" ] || { printf 'mori-silence-cases: census not readable: %s\n' "$CENSUS" >&2; exit 2; }
command -v git >/dev/null 2>&1 || { printf 'mori-silence-cases: real git required on PATH\n' >&2; exit 2; }

# setup failures must be loud and distinct from case verdicts (documented exit 2)
die() { printf 'mori-silence-cases: %s\n' "$*" >&2; exit 2; }

# ---- run entropy: case-order seed + fixture nonce + content salt --------------
# Three independent unpredictable values. The first two are logged in the run
# header (r5); the salt is deliberately never printed:
#   RUN_SEED  seeds the case-order shuffle (see CASE REGISTRY at the bottom).
#             The shuffle is a Fisher-Yates over the 28 ids driven by a local
#             xorshift32, so "same seed => same order" is reproducible in this
#             file, not via bash's RANDOM. Pin it: MORI_SHUFFLE_SEED=<int>.
#             Never exported to the census: the SUT must not be able to read
#             the order. r6: a pin present in this process's environment is
#             moved out of /proc/<pid>/environ by a one-time self re-exec at
#             startup (see the re-exec block below; a runtime `unset` cannot
#             change the exec-time environ region).
#   RUN_NONCE is the per-run fixture nonce. It is NOT derived from the seed, so
#             guessing the order seed does not reveal it, and it is regenerated
#             independently each run, so a replayed previous run carries a
#             stale value. It reaches the census three ways: exported as
#             MORI_RUN_NONCE, written into every fixture
#             ($CASE_DIR/run-nonce), and used as the name of the fixture's disk
#             target directory, which the census echoes in its own disk row as
#             `targets=<case-dir>/nonce-<N>`. assert_case requires that token in
#             every case's census output. Pin it: MORI_RUN_NONCE=<int>
#             (operator reproducibility only; a normal run never sets it).
#             r6: like the seed, removed from this process's environment by the
#             one-time self re-exec when it is pinned.
rand32() {
  local v=''
  if [ -r /dev/urandom ]; then
    v=$(od -An -N4 -tu4 < /dev/urandom 2>/dev/null | tr -dc '0-9' || true)
  fi
  case "$v" in ''|*[!0-9]*) v=0 ;; esac
  if [ "$v" -eq 0 ]; then
    v=$(( ((RANDOM << 16) | RANDOM) ^ ($$ << 7) ^ ($(date +%s) & 65535) ))
    [ "$v" -gt 0 ] || v=1
  fi
  printf '%s' "$v"
}

RUN_SEED=${MORI_SHUFFLE_SEED:-}
RUN_NONCE=${MORI_RUN_NONCE:-}
# r6 R1 (environ channel): the reproducibility pins arrive through this
# process's environment. A runtime `unset` does NOT scrub /proc/<pid>/environ —
# measured 2026-10-15: /proc/pid/environ shows the exec-time environment region,
# which a running bash never rewrites (an earlier "unset scrubs it" reading was
# an artifact of bash exec-optimizing its last command into sleep and replacing
# the process image). So when a pin is present this process re-execs itself ONCE
# with the pins removed from the exported environment; the values travel through
# a pipe fd — no env, no argv, no file — that is drained at startup, before the
# first fixture exists. The pre-exec image carries the pins for the few
# milliseconds before the exec; no census invocation exists yet (the first one
# runs only after fixture setup), so no living census can read them.
if [ "${MORI_CASES_SCRUBBED:-}" != 1 ]; then
  case "${MORI_SHUFFLE_SEED:-}${MORI_RUN_NONCE:-}" in
    '') ;;  # nothing pinned: this process's environ carries no run secret
    *)
      exec 3< <(printf '%s|%s\n' "${MORI_SHUFFLE_SEED:-}" "${MORI_RUN_NONCE:-}")
      export MORI_CASES_SCRUBBED=1
      unset MORI_SHUFFLE_SEED MORI_RUN_NONCE
      if [ "$SELFTEST" = 1 ]; then
        exec bash "$SELF" --selftest
      fi
      exec bash "$SELF" "$CENSUS"
      ;;
  esac
fi
if [ "${MORI_CASES_SCRUBBED:-}" = 1 ]; then
  IFS='|' read -r RUN_SEED RUN_NONCE <&3 || die "pinned-entropy channel read failed"
  exec 3<&-
fi
case "$RUN_SEED" in
  '') RUN_SEED=$(rand32) ;;
  *[!0-9]*) die "MORI_SHUFFLE_SEED must be a non-negative integer" ;;
esac
[ "$RUN_SEED" -ne 0 ] || RUN_SEED=1
case "$RUN_NONCE" in
  '') RUN_NONCE=$(rand32) ;;
  *[!0-9]*) die "MORI_RUN_NONCE must be a non-negative integer" ;;
esac
[ "$RUN_NONCE" -ne 0 ] || RUN_NONCE=1
NONCE_TOKEN="nonce-$RUN_NONCE"

# r6 R2: per-run content salt — a third, independent unpredictable value woven
# into fixture bodies and commit messages (and named in per-run blob files). It
# never affects any grade and never appears on stdout; its job is to make every
# fixture's byte content unique per run, so a content memorizer that learned
# (bytes -> row) from a previous run has no key to match today.
RUN_SALT_HEX=$(printf '%08x%08x' "$(rand32)" "$(rand32)")
RUN_SALT="salt-$RUN_SALT_HEX"

# ---- pinned time base --------------------------------------------------------
T0=1700000000            # NOW for every case
GATE=900                 # MORI_LANE_SILENCE_S for every case
OLD=1699998000           # launch age 2000  (> GATE: open-and-old)
VOLD=1699996000          # launch age 4000  (older open anchor)
PRE=1699995000           # pre-launch commit anchor
MW=1699999100            # NOW-GATE: r1 rolling-window start (all fixtures that
                         # want the r1 window to MISS use commit/mtime <= this;
                         # "recent unexplained" files use NOW-60=1699999940)
RECENT=1699999940        # NOW-60: inside any sane r1 window and post-launch
FUT=1700000300           # NOW+300: future-dated commit (must never close)

if [ "$SELFTEST" = 1 ]; then
  # --selftest fixtures live under the caller's TMPDIR only (never /tmp).
  case "${TMPDIR:-}" in
    /*) ;;
    *) die "--selftest requires an absolute TMPDIR" ;;
  esac
  [ -d "$TMPDIR" ] || die "--selftest TMPDIR is not a directory: $TMPDIR"
  WORK=$(mktemp -d "$TMPDIR/mori-silence-cases-selftest.XXXXXX") || die "mktemp under TMPDIR failed"
else
  WORK=$(mktemp -d /tmp/mori-silence-cases.XXXXXX)
fi
MORI_CASES_WORK=$WORK
trap 'chmod -R u+rwX "$MORI_CASES_WORK" 2>/dev/null; rm -rf -- "$MORI_CASES_WORK"' EXIT INT TERM
BIN=$WORK/bin
mkdir -p "$BIN" "$WORK/home"

# host stub dispatcher: answers only from $CASE_STUB (fixture-shaped, same
# idiom the census selftest uses; git deliberately NOT stubbed — real repos)
cat > "$BIN/.dispatch" <<'STUB'
#!/usr/bin/env bash
set -uo pipefail
name=${0##*/}
fx=${MORI_STUB_DIR:-}
[ -n "$fx" ] || { printf 'stub dispatcher: MORI_STUB_DIR unset\n' >&2; exit 97; }
rc_of() { local f="$fx/$1.rc"; if [ -f "$f" ]; then cat "$f"; else printf 0; fi; }
out_of() { local f="$fx/$1"; if [ -f "$fx/$1" ]; then cat "$f"; fi; }
case "$name" in
  pgrep)     out_of pgrep;     exit "$(rc_of pgrep)" ;;
  journalctl)
    # r13: structured queries (`-o json`, `--output=json`, `--output json`) are
    # served from journal.json — empty in every fixture, i.e. zero records —
    # while text queries keep reading journal. rc is shared: the query ran.
    jf=journal
    for a in "$@"; do
      case "$a" in *json*) jf=journal.json ;; esac
    done
    out_of "$jf"
    exit "$(rc_of journal)"
    ;;
  df)        out_of df;        exit "$(rc_of df)" ;;
  tmux)      out_of tmux;      exit "$(rc_of tmux)" ;;
esac
printf 'stub dispatcher: unknown %s\n' "$name" >&2
exit 96
STUB
chmod 700 "$BIN/.dispatch"
for c in pgrep journalctl df tmux; do ln -s .dispatch "$BIN/$c"; done

PASS_N=0
TOTAL_N=0
FAILED_IDS=()

iso() { date -u -d "@$1" +%Y-%m-%dT%H:%M:%S+00:00; }

# ---- fixture skeleton --------------------------------------------------------
# case_skeleton — quiet stubs/logs for the case tree named by the CASE_* globals.
# Split out of new_case so the shape-invariance case can build the same bytes
# under two independent, randomly named directory trees.
case_skeleton() {
  mkdir -p "$CASE_ROOT" "$CASE_UFO/state" "$CASE_UFO/waves" "$CASE_DIR/cgroup" "$CASE_STUB" "$CASE_DIR/home"

  # per-run nonce artifacts: a fixture file plus the disk target directory. Both
  # live in CASE_DIR, the parent of every fixture repo (root/, ufo/), so they
  # are never untracked files inside a graded tree; the census echoes the target
  # path in its disk row, which is how assert_case sees the current nonce.
  printf '%s\n' "$RUN_NONCE" > "$CASE_DIR/run-nonce"
  mkdir -p "$CASE_DIR/$NONCE_TOKEN"

  # r6 R2: per-run content variation under CASE_DIR — one salt file plus 0-2
  # random blob files, random names and random content, old mtimes so no
  # recent-file window sees them. No census surface walks CASE_DIR itself
  # (MORI_SHOKUNIN_ROOT / MORI_UFO_DIR / STATE_DIR / WAVES_DIR all live under
  # it), but every content fingerprint does: an attacker that memorized
  # (bytes -> row) from a previous run cannot match today's tree, and varying
  # the file COUNT is not pattern-normalizable by excluding known names.
  printf '%s\n' "$RUN_SALT_HEX" > "$CASE_DIR/$RUN_SALT"
  touch -d "@$PRE" "$CASE_DIR/$RUN_SALT"
  local nb i
  nb=$(( 0x${RUN_SALT_HEX:0:4} % 3 ))
  for (( i = 0; i < nb; i++ )); do
    printf 'blob %s %s\n' "$RUN_SALT_HEX" "$(rand32)" > "$CASE_DIR/blob-$i-$RUN_SALT_HEX"
    touch -d "@$PRE" "$CASE_DIR/blob-$i-$RUN_SALT_HEX"
  done

  # quiet watchdog: process stub + fresh log (content uses the real tick grammar)
  printf '%s tick=1\n' "$(iso "$T0")" > "$CASE_UFO/watchdog.log"
  touch -d "@$T0" "$CASE_UFO/watchdog.log"
  printf '1\n' > "$CASE_UFO/state/$CASE_LANE.round"
  printf '3\n' > "$CASE_UFO/state/kagi.mission"
  printf '1234 bash /path/scripts/shokunin-watchdog.sh\n' > "$CASE_STUB/pgrep"
  printf '0' > "$CASE_STUB/pgrep.rc"
  # quiet waves: one settled
  mkdir -p "$CASE_UFO/waves/wave-settled"
  printf '{"wave":"wave-settled"}\n' > "$CASE_UFO/waves/wave-settled/swarm-registry.json"
  printf '{"wave":"wave-settled"}\n' > "$CASE_UFO/waves/wave-settled/dispatch.json"
  printf '{"schema":"ufo-swarm-results-v1","members":[]}\n' > "$CASE_UFO/waves/wave-settled/results.json"
  touch -d "@$T0" "$CASE_UFO/waves/wave-settled"/*.json
  # quiet cgroup / meminfo
  printf 'low 0\nhigh 0\nmax 0\noom 0\noom_kill 0\noom_group_kill 0\n' > "$CASE_DIR/cgroup/memory.events"
  printf '123456\n' > "$CASE_DIR/cgroup/memory.current"
  printf 'MemAvailable: 20000000 kB\n' > "$CASE_DIR/meminfo"
  # quiet journal / disk / tmux stubs
  # r13: empty output is the zero-record answer for BOTH journal grammars — the
  # text form (`--no-pager`) and the structured form (`-o json` MESSAGE_ID
  # queries). The structured channel gets its own file so a JSON probe never
  # parses a text fixture; both stay empty because every case is a QUIET
  # journal and no case seeds journal content. rc 0 = the query itself worked.
  : > "$CASE_STUB/journal"
  : > "$CASE_STUB/journal.json"
  printf '0' > "$CASE_STUB/journal.rc"
  printf 'Filesystem 1024-blocks Used Available Capacity Mounted on\n/dev/fx 1000000 10000 990000 2%% /fx\n' > "$CASE_STUB/df"
  printf '0' > "$CASE_STUB/df.rc"
  printf 'fx_session: 1 windows\n' > "$CASE_STUB/tmux"; printf '0' > "$CASE_STUB/tmux.rc"
  # r7 pinnable inputs: census-r4 grades a since-boot write average from
  # MORI_DISKSTATS / MORI_UPTIME (defaults /proc/diskstats, /proc/uptime). Left
  # unpinned, the live uptime's integer seconds tick inside the disk row between
  # two runs and break the two-shape stdout invariance of case 28.
  printf '100000.00 20000.00\n' > "$CASE_STUB/uptime"
  : > "$CASE_STUB/diskstats"
  # the launch/close ledger IS this watchdog log (no separate ledger file)
}

# new_case <id> <lane> [ufo-relative-under-root]  — default ufo outside root.
# The case tree lives under a mktemp dir with NO case id inside (anti-sniff:
# no path handed to the census — MORI_SHOKUNIN_ROOT, MORI_UFO_DIR,
# MORI_STUB_DIR, MORI_DISK_TARGETS, ... — encodes which case is running).
new_case() {
  CASE_ID=$1
  CASE_LANE=$2
  CASE_UFO_REL=${3:-../ufo}
  CASE_DIR=$(mktemp -d "$WORK/case.XXXXXXXX") || die "mktemp case dir failed"
  CASE_ROOT=$CASE_DIR/root
  case "$CASE_UFO_REL" in
    /*) CASE_UFO=$CASE_UFO_REL ;;
    ../*) CASE_UFO=$CASE_DIR/${CASE_UFO_REL#../} ;;
    *) CASE_UFO=$CASE_DIR/root/$CASE_UFO_REL ;;
  esac
  CASE_STUB=$CASE_DIR/stub
  case_skeleton
}

# ---- ledger verbs (real grammar; ledger file = $CASE_UFO/watchdog.log) --------
# The live driver appends "<ISO-8601+offset> launch|complete|wrap|tick ..." to
# .ufo/watchdog.log (scripts/shokunin-watchdog.sh:81,83,106,109,114); fixtures
# append the same grammar to the same file, and every append refreshes the log
# mtime to NOW — the live driver log is fresh while the daemon lives, so the
# watchdog surface must stay quiet in every case except ledger-missing-not-silent.
LG_PID=424242
LG_RID=lx-fixture0000
LG_MID=mission-fixture0000
ledger_touch() { touch -d "@$T0" "$CASE_UFO/watchdog.log"; }
jl_launch()     { printf '%s launch %s round=%s pid=%s\n'      "$(iso "$3")" "$1" "$2" "$LG_PID" >> "$CASE_UFO/watchdog.log"; ledger_touch; }
jl_launch_rid() { printf '%s launch %s round=%s runId=%s\n'    "$(iso "$3")" "$1" "$2" "$LG_RID" >> "$CASE_UFO/watchdog.log"; ledger_touch; }
jl_launch_mission() { printf '%s launch %s round=%s mission=%s\n' "$(iso "$3")" "$1" "$2" "$LG_MID" >> "$CASE_UFO/watchdog.log"; ledger_touch; }
jl_launch_fail(){ printf '%s launch-fail %s round=%s :: SUBSTRATE_CMD unset\n' "$(iso "$3")" "$1" "$2" >> "$CASE_UFO/watchdog.log"; ledger_touch; }
jl_complete()   { printf '%s complete %s round=%s; respawning\n' "$(iso "$3")" "$1" "$2" >> "$CASE_UFO/watchdog.log"; ledger_touch; }
jl_wrap()       { printf '%s wrap %s round=%s complete; NOT respawning (fleet-wrap)\n' "$(iso "$3")" "$1" "$2" >> "$CASE_UFO/watchdog.log"; ledger_touch; }
jl_steer()      { printf '%s steer %s -> round %s\n' "$(iso "$3")" "$1" "$2" >> "$CASE_UFO/watchdog.log"; ledger_touch; }
no_ledger()     { rm -f -- "$CASE_UFO/watchdog.log"; }

# ---- real git helpers ---------------------------------------------------------
# All git invocations: env -i, isolated HOME, no global/system config, fixed
# TZ/locale, explicit author+committer identity and commit dates (no clock).
git_q() { # <repo-dir> <git args...>
  local repo=$1; shift
  env -i PATH=/usr/bin:/bin HOME="$CASE_DIR/home" \
    GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null \
    TZ=UTC LC_ALL=C \
    git -c init.defaultBranch=main -c core.autocrlf=false -c gc.auto=0 \
    -C "$repo" "$@"
}

git_init() { # <repo-dir>
  mkdir -p "$1"
  env -i PATH=/usr/bin:/bin HOME="$CASE_DIR/home" \
    GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null TZ=UTC LC_ALL=C \
    git -c init.defaultBranch=main init -q "$1"
}

# gc <repo> <rel> <content> <ct> <aname> <amail> [cname] [cmail] [mtime] [msg]
# Deterministic stage-then-commit: exactly one commit per call, exactly the
# given content, explicit author+committer identity and dates. No `commit -a`,
# no `--allow-empty`, no operator chaining: measured, `commit -a --allow-empty`
# on a fresh repo creates an EMPTY root commit and leaves <rel> untracked, and
# the old `|| ... && ...` chain then ran its trailing commit without the `add`
# and died on "nothing added to commit but untracked files present" — before
# any case could run. Failure here is a fixture setup failure and exits 2.
gc() {
  local repo=$1 rel=$2 content=$3 ct=$4 an=$5 ae=$6
  local cn=${7:-$an} ce=${8:-$ae} mt=${9:-$ct} msg=${10:-update $rel}
  # r6 R2: every committed body carries the live nonce token and the run salt,
  # and every commit message carries the salt — so even a constant-blob commit
  # lands in a per-run git object. Exceptions are the two files whose bytes the
  # census itself parses: .gitignore patterns and *.round state numbers.
  case "$rel" in
    .gitignore|*/.gitignore|*.round) ;;
    *) content="$content [$NONCE_TOKEN $RUN_SALT_HEX]" ;;
  esac
  msg="$msg [$RUN_SALT_HEX]"
  mkdir -p "$repo/$(dirname -- "$rel")"
  printf '%s\n' "$content" > "$repo/$rel"
  touch -d "@$mt" "$repo/$rel"
  env -i PATH=/usr/bin:/bin HOME="$CASE_DIR/home" \
    GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null TZ=UTC LC_ALL=C \
    GIT_AUTHOR_NAME="$an" GIT_AUTHOR_EMAIL="$ae" \
    GIT_COMMITTER_NAME="$cn" GIT_COMMITTER_EMAIL="$ce" \
    GIT_AUTHOR_DATE="@$ct +0000" GIT_COMMITTER_DATE="@$ct +0000" \
    git -c init.defaultBranch=main -c core.autocrlf=false -c commit.gpgsign=false \
    -c gc.auto=0 -C "$repo" add -- "$rel" ||
  die "fixture git add failed: $rel in $repo"
  env -i PATH=/usr/bin:/bin HOME="$CASE_DIR/home" \
    GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null TZ=UTC LC_ALL=C \
    GIT_AUTHOR_NAME="$an" GIT_AUTHOR_EMAIL="$ae" \
    GIT_COMMITTER_NAME="$cn" GIT_COMMITTER_EMAIL="$ce" \
    GIT_AUTHOR_DATE="@$ct +0000" GIT_COMMITTER_DATE="@$ct +0000" \
    git -c init.defaultBranch=main -c core.autocrlf=false -c commit.gpgsign=false \
    -c gc.auto=0 -C "$repo" commit -q -m "$msg" ||
  die "fixture git commit failed: $rel in $repo (content unchanged since HEAD?)"
  touch -d "@$mt" "$repo/$rel"
}

# lane identity helpers (kagi fixture lanes; sibling = aggregator)
KAGI_NAME=kagi-shokunin;            KAGI_MAIL=kagi@shokunin.local
AGG_NAME=aggregator-shokunin;       AGG_MAIL=aggregator@shokunin.local
PROTO_NAME=protocol-shokunin;       PROTO_MAIL=protocol@shokunin.local

# ---- census run ---------------------------------------------------------------
# env -i: only the fixture env reaches the census. MORI_DISK_TARGETS points at
# the per-run nonce directory, so the census's own disk row echoes the current
# run's nonce token; MORI_RUN_NONCE carries it explicitly. RUN_SEED is
# deliberately NOT exported: the SUT must not be able to read the order seed.
CASE_OUT=''
CASE_RC=0
run_census() {
  set +e
  CASE_OUT=$(env -i \
    PATH="$BIN:/usr/bin:/bin" \
    HOME="$WORK/home" TZ=UTC LC_ALL=C \
    MORI_STUB_DIR="$CASE_STUB" \
    MORI_SHOKUNIN_ROOT="$CASE_ROOT" \
    MORI_UFO_DIR="$CASE_UFO" \
    MORI_WATCHDOG_LOG="$CASE_UFO/watchdog.log" \
    MORI_STATE_DIR="$CASE_UFO/state" \
    MORI_WAVES_DIR="$CASE_UFO/waves" \
    MORI_TIMELINE_FILE="$CASE_UFO/watchdog.log" \
    MORI_CGROUP_EVENTS="$CASE_DIR/cgroup/memory.events" \
    MORI_CGROUP_SERVICE_EVENTS="$CASE_DIR/cgroup/memory.events" \
    MORI_CGROUP_LOCAL_EVENTS="$CASE_DIR/cgroup/memory.events" \
    MORI_CGROUP_CURRENT="$CASE_DIR/cgroup/memory.current" \
    MORI_MEMINFO="$CASE_DIR/meminfo" \
    MORI_UPTIME="$CASE_STUB/uptime" \
    MORI_DISKSTATS="$CASE_STUB/diskstats" \
    MORI_DF_BIN="$BIN/df" \
    MORI_PGREP_BIN="$BIN/pgrep" \
    MORI_JOURNALCTL_BIN="$BIN/journalctl" \
    MORI_TMUX_BIN="$BIN/tmux" \
    MORI_DISK_TARGETS="$CASE_DIR/$NONCE_TOKEN" \
    MORI_RUN_NONCE="$RUN_NONCE" \
    MORI_ROSTER_LANES="$CASE_LANE" \
    MORI_NOW_EPOCH=$T0 \
    MORI_WATCHDOG_STALE_S=$GATE \
    MORI_WAVE_UNSETTLED_S=7200 \
    MORI_DISK_WARN_PCT=85 \
    MORI_DISK_CRIT_PCT=95 \
    MORI_LANE_SILENCE_S=$GATE \
    bash "$CENSUS" 2>&1)
  CASE_RC=$?
  set -e
}

# observed lane rows of a run (helper for the read-only mutation guard too)
lane_state_from_out() { # <lane> ; prints state or empty
  local l=$1 line
  line=$(printf '%s\n' "$CASE_OUT" | grep -m1 -E "^SURFACE lane\.${l}: " || true)
  [ -n "$line" ] || { printf ''; return 0; }
  local rest=${line#*: }
  printf '%s' "${rest%% *}"
}

aggregate_state_from_out() { # prints derived state or empty
  local d sil prog weak skip n
  d=$(printf '%s\n' "$CASE_OUT" | grep -m1 '^SURFACE silence:' || true)
  [ -n "$d" ] || { printf ''; return 0; }
  sil=$(printf '%s' "$d"  | sed -n 's/.*silent=\([0-9][0-9]*\).*/\1/p')
  prog=$(printf '%s' "$d" | sed -n 's/.*[^_]progressing=\([0-9][0-9]*\).*/\1/p')
  weak=$(printf '%s' "$d" | sed -n 's/.*progressing_weak=\([0-9][0-9]*\).*/\1/p')
  skip=$(printf '%s' "$d" | sed -n 's/.*skipped=\([0-9][0-9]*\).*/\1/p')
  n=0
  [ "${sil:-0}" = 1 ]  && { printf silent; return 0; }
  [ "${prog:-0}" = 1 ] && { printf progressing; return 0; }
  [ "${weak:-0}" = 1 ] && { printf progressing-weak; return 0; }
  [ "${skip:-0}" = 1 ] && { printf unavailable; return 0; }
  printf not-open
}

finding_present() { # 1 iff LANE_SILENT exists (roster is one lane)
  local n
  n=$(printf '%s\n' "$CASE_OUT" | grep -c '^FINDING LANE_SILENT' || true)
  [ "${n:-0}" -gt 0 ]
}

# nonce_present — 1 iff this case's census output carries the CURRENT run's
# nonce token. The token reaches the census through the fixture (disk-target
# path, MORI_RUN_NONCE env, run-nonce file) and is echoed in the census's own
# disk row; a canned answer cannot produce it and a replayed answer carries the
# previous run's value. Every case asserts it: stale or missing nonce FAILs.
nonce_present() { case "$CASE_OUT" in *"$NONCE_TOKEN"*) return 0 ;; *) return 1 ;; esac; }

# verdict_grade <output> <rc> — grade the final-roll contract; prints 'ok' or a
# reason (never a run secret). r13 / audit-r11 F02: asking whether a line
# begins `MORI_CENSUS:` let a proxy rename the roll to BANANA and still score
# 28/28. The admitted grammar is the census's own contract
# (census usage() "Verdict:" contract and run_census's final printf): exactly
# one line of
#   MORI_CENSUS: CLEAN|DRIFT (findings=N drift=M unavailable=U surfaces=S)
# whose word matches the process rc (CLEAN=>0, DRIFT=>1). Missing, duplicate,
# malformed, non-final and inconsistent rolls are all rejected. A malformed
# line is echoed only through redact(): it can carry the run nonce, and the r6
# rule keeps run secrets off per-case stdout.
# Here-strings keep the match fed by this shell's own capture — no live
# producer pipe exists to take SIGPIPE (corpus/QUALITY.md criterion 7).
VERDICT_RE='^MORI_CENSUS: (CLEAN|DRIFT) \(findings=[0-9]+ drift=([0-9]+) unavailable=[0-9]+ surfaces=[0-9]+\)$'
verdict_grade() {
  local out=$1 rc=$2 n line last word drift
  n=$(grep -c '^MORI_CENSUS:' <<<"$out" || true)
  case "${n:-0}" in
    0) printf 'missing'; return 0 ;;
    1) ;;
    *) printf 'duplicate (%s lines)' "$n"; return 0 ;;
  esac
  line=$(grep -m1 '^MORI_CENSUS:' <<<"$out")
  if [[ ! $line =~ $VERDICT_RE ]]; then
    # Never echo the roll unredacted: a malformed/replayed line can carry the
    # run nonce (r6). redact() replaces the current run's token only.
    printf 'malformed (line=%s)' "$(redact "$line")"
    return 0
  fi
  word=${BASH_REMATCH[1]}
  drift=${BASH_REMATCH[2]}
  # The census prints the roll and exits, so it owns the last non-empty line.
  # A valid-looking roll followed by more output is a replayed/moved roll, not
  # a verdict.
  last=$(awk 'NF { last = $0 } END { print last }' <<<"$out")
  if [ "$last" != "$line" ]; then
    printf 'not-final (the roll is not the last non-empty line)'
    return 0
  fi
  case "$word:$rc" in
    CLEAN:0|DRIFT:1) ;;
    *) printf 'inconsistent (word=%s rc=%s)' "$word" "$rc"; return 0 ;;
  esac
  # ROLL flips to DRIFT exactly when emit_finding increments N_DRIFT in its
  # warn|crit branch, so the word and drift= cannot disagree: CLEAN drift>0 and
  # DRIFT drift=0 are forged or mangled rolls. Compare the captured digits as
  # STRINGS — `$((10#…))` silently wraps (measured bash 5.3.15:
  # 10#18446744073709551616 => 0), so a forged `CLEAN drift=<2^64>` would pass
  # a numeric `==0` test. The census prints %d, so no leading zeros exist:
  # CLEAN is exactly `0`, DRIFT is `[1-9][0-9]*`. surfaces= and unavailable=
  # are deliberately NOT cross-counted: lane rows append to SURFACE_LINES
  # directly (`SURFACE_LINES+=("SURFACE lane.` in probe_silence) and never
  # increment N_SURFACES, so an honest run's surfaces= is smaller than its row
  # count.
  if [ "$word" = CLEAN ]; then
    if [ "$drift" = 0 ]; then printf 'ok'
    else printf 'inconsistent (CLEAN drift=%s)' "$drift"; fi
  else
    case "$drift" in
      [1-9]*) printf 'ok' ;;
      *) printf 'inconsistent (DRIFT drift=%s)' "$drift" ;;
    esac
  fi
}

# want_match <obs> <want[|want2[|...]]> — true iff obs exactly equals one of the
# '|'-separated alternatives. `case "$obs" in $want)` CANNOT express alternation:
# a `|` introduced by parameter expansion is a literal pattern character in bash
# (measured bash 5.3.15; corpus/evidence/cutover-r3-20261015T165712Z-oracle-counterfactual.log),
# which pinned the frozen oracle at 25/27. Alternatives are compared as exact
# strings, never patterns, so a state name can never act as a glob either.
want_match() {
  local obs=$1 w
  for w in ${2//|/ }; do
    if [ "$obs" = "$w" ]; then return 0; fi
  done
  return 1
}

# redact — strip the current run's nonce token from a census fragment before it
# is echoed into a per-case line. r6 R1: per-case stdout is written while later
# census invocations can still read this process's stdout via /proc, so no
# per-case line may carry a run secret (case ids are not secret).
redact() { printf '%s' "${1//$NONCE_TOKEN/nonce-<redacted>}"; }

# assert_case <id> <want-state[|set]> <want-finding 0|1|auto> <want-rc 0|1|auto>
# auto = consistency with observed state (finding/rc present iff silent).
# Every case additionally requires the per-run nonce token in the output (r5).
assert_case() {
  local id=$1 want=$2 wf=$3 wrc=$4
  run_census
  TOTAL_N=$((TOTAL_N + 1))

  local api obs
  obs=$(lane_state_from_out "$CASE_LANE")
  if [ -n "$obs" ]; then api=lane; else
    obs=$(aggregate_state_from_out); api=aggregate
  fi
  local fobs=0; finding_present && fobs=1
  local verdict vcheck
  verdict=$(printf '%s\n' "$CASE_OUT" | grep -m1 '^MORI_CENSUS:' || true)
  vcheck=$(verdict_grade "$CASE_OUT" "$CASE_RC")

  if [ "$CASE_RC" -gt 1 ]; then
    printf 'FAIL %s: census setup rc=%s; %s\n' "$id" "$CASE_RC" \
      "$(redact "$(printf '%s' "$CASE_OUT" | tail -n1 | tr '\n' '|')")"
    FAILED_IDS+=("$id"); return 0
  fi
  # r13 (F02): a `MORI_CENSUS:` prefix is not a verdict. Exactly one
  # well-formed CLEAN|DRIFT line whose word matches rc is required; a missing
  # roll here is the old crash signature (unreadable .git aborts mid-run), a
  # duplicate is ambiguous, and a substituted/mismatched roll is the proxy
  # attack from audit-r11 Appendix C. No want-state can excuse any of them.
  if [ "$vcheck" != ok ]; then
    printf 'FAIL %s: MORI_CENSUS verdict %s (rc=%s) — one well-formed CLEAN|DRIFT line matching its rc is required; got=[%s] tail=%s\n' \
      "$id" "$vcheck" "$CASE_RC" "$(redact "$verdict")" \
      "$(redact "$(printf '%s' "$CASE_OUT" | tail -n1 | tr '\n' '|')")"
    FAILED_IDS+=("$id"); return 0
  fi

  local ok=1 why=''
  if ! want_match "$obs" "$want"; then
    ok=0; why="state want [$want] got [$obs] via $api"
  fi
  local wff=$wf
  [ "$wf" = auto ] && { [ "$obs" = silent ] && wff=1 || wff=0; }
  if [ "$fobs" -ne "$wff" ]; then
    ok=0; why="$why finding want=$wff got=$fobs"
  fi
  local wrr=$wrc
  [ "$wrc" = auto ] && { [ "$obs" = silent ] && wrr=1 || wrr=0; }
  if [ "$CASE_RC" -ne "$wrr" ]; then
    ok=0; why="$why rc want=$wrr got=$CASE_RC verdict='$(redact "$verdict")'"
  fi
  # r5 run-order close: the output must carry the CURRENT run's nonce token.
  # r6: the failure text names no token — per-case lines must not put a run
  # secret on stdout while later invocations can still read it.
  local nonce_ok=0; nonce_present && nonce_ok=1
  if [ "$nonce_ok" -ne 1 ]; then
    ok=0; why="$why run-nonce missing: the current run's token is absent (canned/replayed output?)"
  fi

  if [ "$ok" = 1 ]; then
    PASS_N=$((PASS_N + 1))
    printf 'PASS %s (state=%s via %s finding=%s rc=%s nonce=1)\n' "$id" "$obs" "$api" "$fobs" "$CASE_RC"
  else
    FAILED_IDS+=("$id")
    printf 'FAIL %s: %s\n' "$id" "${why# }"
  fi
}

# count-only check (used by the read-only guard)
count_check() { # <id> <ok0/1> <detail>
  TOTAL_N=$((TOTAL_N + 1))
  if [ "$2" = 1 ]; then PASS_N=$((PASS_N + 1)); printf 'PASS %s\n' "$1"
  else FAILED_IDS+=("$1"); printf 'FAIL %s: %s\n' "$1" "$3"; fi
}

fx_fingerprint() {
  find "$CASE_DIR" -type f \( -path '*/.git/*' -prune -o -printf '%p|%T@|%s|' -exec sha256sum {} \; \) 2>/dev/null \
    | LC_ALL=C sort | sha256sum | cut -d' ' -f1
}

# =================================================================================
# CASES — each grades behavior of the actual census CLI on an isolated fixture.
# Want columns: lane state, LANE_SILENT present, census rc.
# Every case is a function named case_<id with '-' as '_'>. The runner at the
# bottom executes them in the SEED-SHUFFLED order (never in this source order),
# so a census cannot map its invocation position to a case identity.
# =================================================================================

# 1 — open mission older than gate, nothing attributed, no recent files.
case_silent_open() {
  new_case silent-open kagi
  git_init "$CASE_ROOT/kagi-shokunin"
  jl_launch kagi 7 "$OLD"
  gc "$CASE_ROOT/kagi-shokunin" LOG.md 'old work' "$PRE" "$KAGI_NAME" "$KAGI_MAIL"
  assert_case silent-open silent 1 1
}

# 2 — launch + matching complete: mission closed; old content must not be graded.
case_completed_not_open() {
  new_case completed-not-open kagi
  git_init "$CASE_ROOT/kagi-shokunin"
  jl_launch kagi 7 "$VOLD"
  jl_complete kagi 7 1699997000
  gc "$CASE_ROOT/kagi-shokunin" LOG.md 'old work' "$PRE" "$KAGI_NAME" "$KAGI_MAIL"
  assert_case completed-not-open not-open 0 0
}

# 3 — open mission age 800 < 900: under gate, not graded.
case_young_under_gate() {
  new_case young-under-gate kagi
  git_init "$CASE_ROOT/kagi-shokunin"
  jl_launch kagi 7 $((T0 - 800))
  gc "$CASE_ROOT/kagi-shokunin" LOG.md 'old work' "$PRE" "$KAGI_NAME" "$KAGI_MAIL"
  assert_case young-under-gate young 0 0
}

# 4 — age exactly at gate: grade is strictly-greater => young.
case_young_age_equals_gate() {
  new_case young-age-equals-gate kagi
  git_init "$CASE_ROOT/kagi-shokunin"
  jl_launch kagi 7 $((T0 - GATE))
  gc "$CASE_ROOT/kagi-shokunin" LOG.md 'old work' "$PRE" "$KAGI_NAME" "$KAGI_MAIL"
  assert_case young-age-equals-gate young 0 0
}

# 5 — future launch line cannot be old.
case_young_future_launch() {
  new_case young-future-launch kagi
  git_init "$CASE_ROOT/kagi-shokunin"
  jl_launch kagi 7 $((T0 + 1200))
  gc "$CASE_ROOT/kagi-shokunin" LOG.md 'old work' "$PRE" "$KAGI_NAME" "$KAGI_MAIL"
  assert_case young-future-launch young 0 0
}

# 6 — ledger exists with a launch-fail line for this lane (never a mission
#      start, scripts/shokunin-watchdog.sh:83) and a launch for another lane:
#      not-open for kagi, never silent.
case_nolane_launch_not_open() {
  new_case nolane-launch-not-open kagi
  git_init "$CASE_ROOT/kagi-shokunin"
  jl_launch_fail kagi 7 "$VOLD"
  jl_launch kengaku 2 "$VOLD"
  gc "$CASE_ROOT/kagi-shokunin" LOG.md 'old work' "$PRE" "$KAGI_NAME" "$KAGI_MAIL"
  assert_case nolane-launch-not-open not-open 0 0
}

# 7 — watchdog log (the launch ledger) absent entirely: not-open OR
#     unavailable, must not be silent.
case_ledger_missing_not_silent() {
  new_case ledger-missing-not-silent kagi
  git_init "$CASE_ROOT/kagi-shokunin"
  no_ledger
  gc "$CASE_ROOT/kagi-shokunin" LOG.md 'old work' "$PRE" "$KAGI_NAME" "$KAGI_MAIL"
  assert_case ledger-missing-not-silent 'not-open|unavailable' 0 0
}

# 8 — roster lane directory missing: unavailable, not silent (r1 skips => same).
case_repo_missing_unavailable() {
  new_case repo-missing-unavailable kagi
  jl_launch kagi 7 "$OLD"
  assert_case repo-missing-unavailable unavailable 0 0
}

# 9 — repo present but .git unreadable: must not become silent.
case_unreadable_git_unavailable() {
  new_case unreadable-git-unavailable kagi
  git_init "$CASE_ROOT/kagi-shokunin"
  jl_launch kagi 7 "$OLD"
  gc "$CASE_ROOT/kagi-shokunin" LOG.md 'old work' "$PRE" "$KAGI_NAME" "$KAGI_MAIL"
  chmod 000 "$CASE_ROOT/kagi-shokunin/.git"
  assert_case unreadable-git-unavailable unavailable 0 0
}

# 10 — complete then LATER launch line for the same round reopens the attempt
#      (line order matters); reopened attempt is old with nothing after => silent.
case_same_round_relaunch_silent() {
  new_case same-round-relaunch-silent kagi
  git_init "$CASE_ROOT/kagi-shokunin"
  jl_launch kagi 7 1699992800
  jl_complete kagi 7 1699994600
  jl_launch kagi 7 "$OLD"
  gc "$CASE_ROOT/kagi-shokunin" LOG.md 'old work' 1699991000 "$KAGI_NAME" "$KAGI_MAIL"
  assert_case same-round-relaunch-silent silent 1 1
}

# 11 — legacy 'steer' line is a start marker when no launch exists.
case_legacy_steer_open_silent() {
  new_case legacy-steer-open-silent kagi
  git_init "$CASE_ROOT/kagi-shokunin"
  jl_steer kagi 7 "$OLD"
  gc "$CASE_ROOT/kagi-shokunin" LOG.md 'old work' "$PRE" "$KAGI_NAME" "$KAGI_MAIL"
  assert_case legacy-steer-open-silent silent 1 1
}

# 12 — subject commit dated AFTER launch but OUTSIDE the r1 rolling window:
#      launch-aware attribution must grade progressing. Ledger uses the runId=
#      tail here — the parser must ignore the tail (both tails occur live).
case_subject_postlaunch_progressing() {
  new_case subject-postlaunch-progressing kagi
  git_init "$CASE_ROOT/kagi-shokunin"
  jl_launch_rid kagi 7 "$OLD"
  gc "$CASE_ROOT/kagi-shokunin" LOG.md 'old base' "$PRE" "$KAGI_NAME" "$KAGI_MAIL"
  gc "$CASE_ROOT/kagi-shokunin" notes.md 'postlaunch subject work' 1699998600 "$KAGI_NAME" "$KAGI_MAIL"
  assert_case subject-postlaunch-progressing progressing 0 0
}

# 13 — subject commit post-launch but HIDDEN BEHIND a later sibling HEAD commit
#      (both outside r1 window): scan ALL post-launch commits => progressing.
case_subject_hidden_behind_sibling_head() {
  new_case subject-hidden-behind-sibling-head kagi
  git_init "$CASE_ROOT/kagi-shokunin"
  jl_launch kagi 7 1699997000
  gc "$CASE_ROOT/kagi-shokunin" LOG.md 'old base' "$PRE" "$KAGI_NAME" "$KAGI_MAIL"
  gc "$CASE_ROOT/kagi-shokunin" sub.md 'subject work' 1699998000 "$KAGI_NAME" "$KAGI_MAIL"
  gc "$CASE_ROOT/kagi-shokunin" sib.md 'sibling work' 1699998500 "$AGG_NAME" "$AGG_MAIL"
  assert_case subject-hidden-behind-sibling-head progressing 0 0
}

# 14 — sibling-only commit post-launch; subject's last commit is PRE-launch;
#      clean checkout mtimes (LOG.md newer than launch, == commit ct) must NOT
#      be promoted to subject progress => progressing-weak.
case_sibling_clean_checkout_weak() {
  new_case sibling-clean-checkout-weak kagi
  git_init "$CASE_ROOT/kagi-shokunin"
  jl_launch kagi 7 "$OLD"
  gc "$CASE_ROOT/kagi-shokunin" LOG.md 'subject base' 1699997900 "$KAGI_NAME" "$KAGI_MAIL"
  gc "$CASE_ROOT/kagi-shokunin" LOG.md 'sibling edit' 1699998500 "$AGG_NAME" "$AGG_MAIL"
  touch -d '@1699998505' "$CASE_ROOT/kagi-shokunin/LOG.md"
  assert_case sibling-clean-checkout-weak progressing-weak 0 0
}

# 15 — author=sibling, committer=subject: attribution follows the AUTHOR.
case_author_sibling_committer_subject_weak() {
  new_case author-sibling-committer-subject-weak kagi
  git_init "$CASE_ROOT/kagi-shokunin"
  jl_launch kagi 7 "$OLD"
  gc "$CASE_ROOT/kagi-shokunin" LOG.md 'old base' "$PRE" "$KAGI_NAME" "$KAGI_MAIL"
  gc "$CASE_ROOT/kagi-shokunin" notes.md 'sibling-authored' 1699998600 "$AGG_NAME" "$AGG_MAIL" "$KAGI_NAME" "$KAGI_MAIL"
  assert_case author-sibling-committer-subject-weak progressing-weak 0 0
}

# 16 — author=subject, committer=sibling: still subject progress.
case_author_subject_committer_sibling_progress() {
  new_case author-subject-committer-sibling-progress kagi
  git_init "$CASE_ROOT/kagi-shokunin"
  jl_launch kagi 7 "$OLD"
  gc "$CASE_ROOT/kagi-shokunin" LOG.md 'old base' "$PRE" "$KAGI_NAME" "$KAGI_MAIL"
  gc "$CASE_ROOT/kagi-shokunin" notes.md 'subject-authored' 1699998600 "$KAGI_NAME" "$KAGI_MAIL" "$AGG_NAME" "$AGG_MAIL"
  assert_case author-subject-committer-sibling-progress progressing 0 0
}

# 17 — identity substring trap (name wrong, email exact): kagi-helper-shokunin
#      must NOT count as kagi-subject => sibling-only => progressing-weak.
case_substring_name_mismatch_weak() {
  new_case substring-name-mismatch-weak kagi
  git_init "$CASE_ROOT/kagi-shokunin"
  jl_launch kagi 7 "$OLD"
  gc "$CASE_ROOT/kagi-shokunin" LOG.md 'old base' "$PRE" "$KAGI_NAME" "$KAGI_MAIL"
  gc "$CASE_ROOT/kagi-shokunin" notes.md 'helper' 1699998600 'kagi-helper-shokunin' "$KAGI_MAIL"
  assert_case substring-name-mismatch-weak progressing-weak 0 0
}

# 18 — identity trap in the other field (name exact, email wrong):
#      kagi-helper@shokunin.local must NOT count => progressing-weak.
case_substring_email_mismatch_weak() {
  new_case substring-email-mismatch-weak kagi
  git_init "$CASE_ROOT/kagi-shokunin"
  jl_launch kagi 7 "$OLD"
  gc "$CASE_ROOT/kagi-shokunin" LOG.md 'old base' "$PRE" "$KAGI_NAME" "$KAGI_MAIL"
  gc "$CASE_ROOT/kagi-shokunin" notes.md 'wrong mail' 1699998600 "$KAGI_NAME" 'kagi-helper@shokunin.local'
  assert_case substring-email-mismatch-weak progressing-weak 0 0
}

# 19 — dirty uncommitted edit on the SAME path a sibling committed post-launch:
#      the dirty work is unexplained recent filesystem evidence => progressing.
case_dirty_same_path_as_sibling_progress() {
  new_case dirty-same-path-as-sibling-progress kagi
  git_init "$CASE_ROOT/kagi-shokunin"
  jl_launch kagi 7 1699997000
  gc "$CASE_ROOT/kagi-shokunin" LOG.md 'sibling edit' 1699998000 "$AGG_NAME" "$AGG_MAIL"
  printf 'subject dirty work %s %s\n' "$NONCE_TOKEN" "$RUN_SALT_HEX" > "$CASE_ROOT/kagi-shokunin/LOG.md"
  touch -d "@$RECENT" "$CASE_ROOT/kagi-shokunin/LOG.md"
  assert_case dirty-same-path-as-sibling-progress progressing 0 0
}

# 20 — untracked recent file with no post-launch commit: unexplained recent
#      files => progressing (filesystem evidence, attribution disclosed).
case_untracked_recent_progress() {
  new_case untracked-recent-progress kagi
  git_init "$CASE_ROOT/kagi-shokunin"
  jl_launch kagi 7 1699997000
  gc "$CASE_ROOT/kagi-shokunin" LOG.md 'old base' "$PRE" "$KAGI_NAME" "$KAGI_MAIL"
  mkdir -p "$CASE_ROOT/kagi-shokunin/scratch"
  printf 'wip %s %s\n' "$NONCE_TOKEN" "$RUN_SALT_HEX" > "$CASE_ROOT/kagi-shokunin/scratch/notes.md"
  touch -d "@$RECENT" "$CASE_ROOT/kagi-shokunin/scratch/notes.md"
  assert_case untracked-recent-progress progressing 0 0
}

# 21 — committed report post-launch CLOSES the mission; a later unrelated HEAD
#      commit must not break closure (path-scoped history, not overall HEAD).
#      Report path is the live one: .ufo/reports/round-2/<lane>.md.
case_committed_report_closes() {
  new_case committed-report-closes aggregator
  git_init "$CASE_ROOT"
  jl_launch aggregator 2 1699997000
  gc "$CASE_ROOT" README.md 'root base' "$PRE" "$AGG_NAME" "$AGG_MAIL"
  gc "$CASE_ROOT" .ufo/reports/round-2/aggregator.md 'round report' 1699998000 "$AGG_NAME" "$AGG_MAIL"
  gc "$CASE_ROOT" docs/other.md 'unrelated churn' 1699998500 "$AGG_NAME" "$AGG_MAIL"
  assert_case committed-report-closes not-open 0 0
}

# 22 — old committed report predates complete AND the same-round relaunch:
#      reopened attempt must stay open (old marker does not close) => silent.
#      Relaunch uses the mission= tail — the parser must ignore the tail.
case_old_report_before_relaunch_silent() {
  new_case old-report-before-relaunch-silent aggregator
  git_init "$CASE_ROOT"
  jl_launch aggregator 2 1699992800
  gc "$CASE_ROOT" .ufo/reports/round-2/aggregator.md 'previous report' 1699995000 "$AGG_NAME" "$AGG_MAIL"
  jl_complete aggregator 2 1699995100
  jl_launch_mission aggregator 2 "$OLD"
  assert_case old-report-before-relaunch-silent silent 1 1
}

# 23 — report path-change commit epoch EXACTLY == launch: closure is strict >
#      launch, so the attempt stays open => silent (with attribution strict too:
#      ct==launch is not post-launch, so no subject progress).
case_report_eq_launch_no_close() {
  new_case report-eq-launch-no-close aggregator
  git_init "$CASE_ROOT"
  jl_launch aggregator 2 "$OLD"
  gc "$CASE_ROOT" .ufo/reports/round-2/aggregator.md 'edge report' "$OLD" "$AGG_NAME" "$AGG_MAIL"
  assert_case report-eq-launch-no-close silent 1 1
}

# 24 — report path-change commit dated AFTER NOW: never closes. The commit is
#      authored by a real other lane (protocol), so the remaining open-mission
#      grade may legitimately be progressing-weak (future-dated sibling commit
#      seen) or silent (commits filtered at <= NOW) — never not-open, and never
#      subject progress; finding/rc must be consistent with the observed state.
case_report_future_no_close() {
  new_case report-future-no-close aggregator
  git_init "$CASE_ROOT"
  jl_launch aggregator 2 "$OLD"
  gc "$CASE_ROOT" .ufo/reports/round-2/aggregator.md 'future report' "$FUT" "$PROTO_NAME" "$PROTO_MAIL"
  assert_case report-future-no-close 'progressing-weak|silent' auto auto
}

# 25 — report file present but UNCOMMITTED (recent, untracked): does not close;
#      it is unexplained recent work => progressing.
case_untracked_report_progress() {
  new_case untracked-report-progress aggregator
  git_init "$CASE_ROOT"
  jl_launch aggregator 2 "$OLD"
  gc "$CASE_ROOT" README.md 'root base' "$PRE" "$AGG_NAME" "$AGG_MAIL"
  mkdir -p "$CASE_ROOT/.ufo/reports/round-2"
  printf 'draft %s %s\n' "$NONCE_TOKEN" "$RUN_SALT_HEX" > "$CASE_ROOT/.ufo/reports/round-2/aggregator.md"
  touch -d "@$RECENT" "$CASE_ROOT/.ufo/reports/round-2/aggregator.md"
  assert_case untracked-report-progress progressing 0 0
}

# 26 — main-repo lane: post-launch noise that MUST NOT confer progress —
#      tracked .ufo/state churn commit under the EXACT subject identity,
#      nested lane repository with fresh commits/files, ignored work/ tree
#      with a fresh file. Nothing inside the lane scope => silent.
case_main_repo_noise_silent() {
  new_case main-repo-noise-silent aggregator ../root/.ufo
  git_init "$CASE_ROOT"
  printf 'work/\n*-shokunin/\n' > "$CASE_ROOT/.gitignore"
  gc "$CASE_ROOT" .gitignore 'work/
*-shokunin/' "$PRE" "$AGG_NAME" "$AGG_MAIL" 'gitignore'
  jl_launch aggregator 3 "$OLD"
  gc "$CASE_ROOT" README.md 'root base' "$PRE" "$AGG_NAME" "$AGG_MAIL"
  mkdir -p "$CASE_ROOT/.ufo/state"
  printf '3\n' > "$CASE_ROOT/.ufo/state/aggregator.round"
  touch -d '@1699998600' "$CASE_ROOT/.ufo/state/aggregator.round"
  gc "$CASE_ROOT" .ufo/state/aggregator.round '3' 1699998600 "$AGG_NAME" "$AGG_MAIL" '' '' 1699998600 'driver state churn'
  mkdir -p "$CASE_ROOT/work"
  printf 'ignored wip %s %s\n' "$NONCE_TOKEN" "$RUN_SALT_HEX" > "$CASE_ROOT/work/inprogress.md"
  touch -d '@1699999940' "$CASE_ROOT/work/inprogress.md"
  git_init "$CASE_ROOT/kagi-shokunin"
  gc "$CASE_ROOT/kagi-shokunin" LOG.md 'nested lane work' 1699999000 "$KAGI_NAME" "$KAGI_MAIL"
  assert_case main-repo-noise-silent silent 1 1
}

# 27 — read-only guard: a census run must not mutate its fixture tree
#      (live mode writes nothing; consumer-visible contract), and it must
#      carry the current run's nonce like every other case.
case_readonly_no_mutation() {
  new_case readonly-no-mutation kagi
  git_init "$CASE_ROOT/kagi-shokunin"
  jl_launch kagi 7 "$OLD"
  gc "$CASE_ROOT/kagi-shokunin" LOG.md 'old base' "$PRE" "$KAGI_NAME" "$KAGI_MAIL"
  gc "$CASE_ROOT/kagi-shokunin" notes.md 'subject work' 1699998600 "$KAGI_NAME" "$KAGI_MAIL"
  before=$(fx_fingerprint)
  run_census
  after=$(fx_fingerprint)
  local vcheck
  vcheck=$(verdict_grade "$CASE_OUT" "$CASE_RC")
  if [ "$before" != "$after" ]; then
    count_check readonly-no-mutation 0 'census mutated fixture tree'
  elif [ "$vcheck" != ok ]; then
    # r13 (F02): the read-only guard is still a case — it must see the same
    # admitted final roll as every assert_case, not just absence of mutation.
    count_check readonly-no-mutation 0 \
      "MORI_CENSUS verdict $vcheck (rc=$CASE_RC) — one well-formed CLEAN|DRIFT line matching its rc is required"
  elif ! nonce_present; then
    count_check readonly-no-mutation 0 "run-nonce missing: the current run's token is absent (canned/replayed output?)"
  else
    count_check readonly-no-mutation 1 ''
  fi
}

# 28 — shape-invariance (anti-sniff): the SAME fixture bytes built twice under
#      two different mktemp directory names must grade byte-identically — state
#      + row API, LANE_SILENT presence, rc, MORI_CENSUS verdict — and normalize
#      to identical stdout (each run's own tree name replaced by a token). One
#      fixture, two names, no case id anywhere: a census that branches on the
#      fixture path or tries to identify the case from it fails one side.
shape_build() { # <base-dir> — open-old mission + post-launch subject commit
  CASE_LANE=kagi
  CASE_DIR=$1
  CASE_ROOT=$CASE_DIR/root
  CASE_UFO=$CASE_DIR/ufo
  CASE_STUB=$CASE_DIR/stub
  case_skeleton
  git_init "$CASE_ROOT/kagi-shokunin"
  jl_launch kagi 7 "$OLD"
  gc "$CASE_ROOT/kagi-shokunin" LOG.md 'old base' "$PRE" "$KAGI_NAME" "$KAGI_MAIL"
  gc "$CASE_ROOT/kagi-shokunin" notes.md 'subject work' 1699998600 "$KAGI_NAME" "$KAGI_MAIL"
}

shape_observe() { # grade of the last run_census, one line (reads CASE_OUT/CASE_RC)
  local api obs fobs=0 v
  obs=$(lane_state_from_out "$CASE_LANE")
  if [ -n "$obs" ]; then api=lane; else obs=$(aggregate_state_from_out); api=aggregate; fi
  finding_present && fobs=1
  v=$(printf '%s\n' "$CASE_OUT" | grep -m1 '^MORI_CENSUS:' || true)
  # r6: this grade string is echoed in shape FAIL lines while later census
  # invocations can still read this process's stdout, and a malformed roll can
  # carry the run nonce — redact at construction so every consumer is safe.
  printf 'state=%s api=%s finding=%s rc=%s verdict=[%s]' "$obs" "$api" "$fobs" "$CASE_RC" "$(redact "$v")"
}

case_shape_invariance() {
  shape_a=$(mktemp -d "$WORK/shape.XXXXXXXX") || die "mktemp shape dir failed"
  shape_b=$(mktemp -d "$WORK/shape.XXXXXXXX") || die "mktemp shape dir failed"
  local va vb

  shape_build "$shape_a"; run_census
  shape_grade_a=$(shape_observe); shape_norm_a=${CASE_OUT//$shape_a/<case-tree>}
  shape_nonce_a=0; nonce_present && shape_nonce_a=1
  va=$(verdict_grade "$CASE_OUT" "$CASE_RC")

  shape_build "$shape_b"; run_census
  shape_grade_b=$(shape_observe); shape_norm_b=${CASE_OUT//$shape_b/<case-tree>}
  shape_nonce_b=0; nonce_present && shape_nonce_b=1
  vb=$(verdict_grade "$CASE_OUT" "$CASE_RC")

  # r13 (F02): both shape runs must carry the admitted final roll. Equal-but-
  # bad grades (same BANANA, same duplicate, same rc mismatch) would otherwise
  # satisfy the invariance comparison; the contract is checked per side first.
  if [ "$va" != ok ] || [ "$vb" != ok ]; then
    count_check shape-invariance 0 "MORI_CENSUS verdict contract broken: A=[$(redact "$shape_grade_a")] verdict=$va B=[$(redact "$shape_grade_b")] verdict=$vb"
  elif [ "$shape_nonce_a" -ne 1 ] || [ "$shape_nonce_b" -ne 1 ]; then
    count_check shape-invariance 0 "run-nonce missing in a shape run: the current run's token is absent (canned/replayed output?)"
  elif [ "$shape_grade_a" != "$shape_grade_b" ]; then
    count_check shape-invariance 0 "same fixture graded differently under two dir names: A=[$shape_grade_a] B=[$shape_grade_b]"
  elif [ "$shape_norm_a" != "$shape_norm_b" ]; then
    count_check shape-invariance 0 "grades match but stdout differs under the two dir names (path-dependent output): A=[$shape_grade_a]"
  else
    count_check shape-invariance 1 ''
  fi
}

# =================================================================================
# CASE REGISTRY + SHUFFLED RUNNER — the 28 ids in source order. The runner
# executes them in a seed-shuffled order, so invocation position never maps to
# a case identity. Pin the order with MORI_SHUFFLE_SEED=<int> (same seed =>
# same order); the seed itself is never exported to the census.
# =================================================================================
CASE_IDS=(
  silent-open
  completed-not-open
  young-under-gate
  young-age-equals-gate
  young-future-launch
  nolane-launch-not-open
  ledger-missing-not-silent
  repo-missing-unavailable
  unreadable-git-unavailable
  same-round-relaunch-silent
  legacy-steer-open-silent
  subject-postlaunch-progressing
  subject-hidden-behind-sibling-head
  sibling-clean-checkout-weak
  author-sibling-committer-subject-weak
  author-subject-committer-sibling-progress
  substring-name-mismatch-weak
  substring-email-mismatch-weak
  dirty-same-path-as-sibling-progress
  untracked-recent-progress
  committed-report-closes
  old-report-before-relaunch-silent
  report-eq-launch-no-close
  report-future-no-close
  untracked-report-progress
  main-repo-noise-silent
  readonly-no-mutation
  shape-invariance
)

# xorshift32 (Marsaglia): deterministic next state from a nonzero seed. Used
# only for the order shuffle — the seed is unpredictable per run and never
# exported, so the SUT cannot read the order it is about to be graded in.
xs32() { # <state> -> next state
  local x=$1
  x=$(( x ^ ((x << 13) & 4294967295) ))
  x=$(( x ^ (x >> 17) ))
  x=$(( x ^ ((x << 5) & 4294967295) ))
  printf '%s' "$(( x & 4294967295 ))"
}

shuffle_case_ids() { # Fisher-Yates in place; same RUN_SEED => same order
  local i j t n=${#CASE_IDS[@]} st=$RUN_SEED
  for (( i = n - 1; i > 0; i-- )); do
    st=$(xs32 "$st")
    j=$(( st % (i + 1) ))
    t=${CASE_IDS[i]}; CASE_IDS[i]=${CASE_IDS[j]}; CASE_IDS[j]=$t
  done
}

# =================================================================================
# --selftest — bounded self-check over THIS case table's own fixtures. It never
# runs the suite. Three layers:
#   1. table structure: the ids are unique, every id has its case_<id>
#      function, no case_* function is unregistered, and each case builds the
#      fixture that carries its own id (shape-invariance builds its own tree);
#   2. the graders every case depends on, fed synthetic rolls: verdict_grade's
#      final-roll contract (missing / duplicate / malformed / non-final /
#      inconsistent, the r11 BANANA proxy, the 2^64 CLEAN-drift wrap), lane and
#      aggregate state parsing, want_match alternation, redaction, and shuffle
#      determinism over the case ids;
#   3. three case functions executed end to end against the real census, so a
#      broken fixture builder or an ungradeable census fails here first.
# Exit 0 every check passed, 1 a check failed, 2 setup (handled at startup).
# =================================================================================
ST_PASS=0
ST_FAIL=0

st_check() { # <ok0/1> <label>
  if [ "$1" = 1 ]; then
    ST_PASS=$((ST_PASS + 1))
  else
    ST_FAIL=$((ST_FAIL + 1))
    printf 'FAIL selftest: %s\n' "$2" >&2
  fi
}

st_verdict() { # <roll with %b escapes> <rc> <want: ok | reason prefix>
  local got
  got=$(verdict_grade "$(printf '%b' "$1")" "$2")
  case "$3" in
    ok) [ "$got" = ok ] ;;
    *)  case "$got" in "$3"*) return 0 ;; *) return 1 ;; esac ;;
  esac
}

st_main() {
  local n=${#CASE_IDS[@]} ids_sorted fns_sorted id body bad order_a order_b perm
  local saved_out=$CASE_OUT saved_seed=$RUN_SEED log ran passed failed
  local pass_before=$PASS_N total_before=$TOTAL_N fail_before=${#FAILED_IDS[@]}
  local -a saved_ids=("${CASE_IDS[@]}")

  # ---- 1. case table structure ------------------------------------------------
  ids_sorted=$(printf '%s\n' "${CASE_IDS[@]}" | LC_ALL=C sort)
  # case_skeleton is the shared tree builder, not a case: it is the only
  # case_-prefixed function outside the registry.
  fns_sorted=$(compgen -A function | grep -E '^case_[a-z0-9_]+$' \
    | grep -vx 'case_skeleton' | sed -e 's/^case_//' -e 's/_/-/g' | LC_ALL=C sort)
  st_check "$([ "$n" -gt 0 ] && printf 1 || printf 0)" \
    "case table is empty"
  st_check "$([ "$(printf '%s\n' "${CASE_IDS[@]}" | LC_ALL=C sort -u | wc -l)" -eq "$n" ] \
    && printf 1 || printf 0)" "case ids are not unique"
  st_check "$([ "$ids_sorted" = "$fns_sorted" ] && printf 1 || printf 0)" \
    "case registry and case_* functions disagree"
  bad=''
  for id in "${CASE_IDS[@]}"; do
    [ "$id" = shape-invariance ] && continue
    body=$(declare -f "case_${id//-/_}" || true)
    case "$body" in *"new_case $id "*) ;; *) bad="$bad $id" ;; esac
  done
  st_check "$([ -z "$bad" ] && printf 1 || printf 0)" \
    "case fixture does not name its id:$bad"

  # ---- 2. the graders every case depends on -----------------------------------
  st_check "$(st_verdict 'MORI_CENSUS: CLEAN (findings=0 drift=0 unavailable=0 surfaces=2)\n' 0 ok \
    && printf 1 || printf 0)" "verdict_grade rejects a clean final roll"
  st_check "$(st_verdict 'MORI_CENSUS: DRIFT (findings=3 drift=3 unavailable=0 surfaces=2)\n' 1 ok \
    && printf 1 || printf 0)" "verdict_grade rejects a drift final roll"
  st_check "$(st_verdict 'BANANA: DRIFT (findings=3 drift=3 unavailable=0 surfaces=2)\n' 1 missing \
    && printf 1 || printf 0)" "verdict_grade accepts a renamed roll (r11 proxy)"
  st_check "$(st_verdict 'MORI_CENSUS: CLEAN (findings=0 drift=0 unavailable=0 surfaces=2)\nMORI_CENSUS: CLEAN (findings=0 drift=0 unavailable=0 surfaces=2)\n' 0 duplicate \
    && printf 1 || printf 0)" "verdict_grade accepts a duplicate roll"
  st_check "$(st_verdict 'MORI_CENSUS: CLEAN (findings=1 drift=0 unavailable=0)\n' 0 malformed \
    && printf 1 || printf 0)" "verdict_grade accepts a malformed roll"
  st_check "$(st_verdict 'MORI_CENSUS: CLEAN (findings=0 drift=0 unavailable=0 surfaces=2)\ntrailing replay\n' 0 not-final \
    && printf 1 || printf 0)" "verdict_grade accepts a non-final roll"
  st_check "$(st_verdict 'MORI_CENSUS: CLEAN (findings=0 drift=0 unavailable=0 surfaces=2)\n' 1 inconsistent \
    && printf 1 || printf 0)" "verdict_grade accepts CLEAN with rc 1"
  st_check "$(st_verdict 'MORI_CENSUS: CLEAN (findings=1 drift=1 unavailable=0 surfaces=2)\n' 0 inconsistent \
    && printf 1 || printf 0)" "verdict_grade accepts CLEAN with drift>0"
  st_check "$(st_verdict 'MORI_CENSUS: DRIFT (findings=0 drift=0 unavailable=0 surfaces=2)\n' 1 inconsistent \
    && printf 1 || printf 0)" "verdict_grade accepts DRIFT with drift=0"
  st_check "$(st_verdict 'MORI_CENSUS: CLEAN (findings=0 drift=18446744073709551616 unavailable=0 surfaces=2)\n' 0 inconsistent \
    && printf 1 || printf 0)" "verdict_grade accepts a wrapped CLEAN drift value"

  CASE_OUT=$(printf 'SURFACE lane.kagi: silent age=2000\nSURFACE silence: silent=1 progressing=0 progressing_weak=0 skipped=0 unavailable=0')
  st_check "$([ "$(lane_state_from_out kagi)" = silent ] && printf 1 || printf 0)" \
    "lane row parse"
  st_check "$([ "$(aggregate_state_from_out)" = silent ] && printf 1 || printf 0)" \
    "aggregate row parse"
  CASE_OUT=$saved_out
  st_check "$(want_match silent 'silent|progressing' && printf 1 || printf 0)" \
    "want_match rejects a listed alternative"
  st_check "$(want_match young 'silent|progressing' && printf 0 || printf 1)" \
    "want_match accepts an unlisted state"
  st_check "$([ "$(redact "pre $NONCE_TOKEN post")" = 'pre nonce-<redacted> post' ] \
    && printf 1 || printf 0)" "redact leaks the run nonce"

  RUN_SEED=20261025; CASE_IDS=("${saved_ids[@]}"); shuffle_case_ids
  order_a=$(printf '%s ' "${CASE_IDS[@]}")
  CASE_IDS=("${saved_ids[@]}"); shuffle_case_ids
  order_b=$(printf '%s ' "${CASE_IDS[@]}")
  CASE_IDS=("${saved_ids[@]}"); RUN_SEED=$saved_seed
  st_check "$([ "$order_a" = "$order_b" ] && printf 1 || printf 0)" \
    "shuffle is not deterministic for one seed"
  perm=$(for id in $order_a; do printf '%s\n' "$id"; done | LC_ALL=C sort)
  st_check "$([ "$perm" = "$ids_sorted" ] && printf 1 || printf 0)" \
    "shuffle is not a permutation of the case ids"
  st_check "$([ "$order_a" != "$(printf '%s ' "${saved_ids[@]}")" ] && printf 1 || printf 0)" \
    "shuffle preserved source order"

  # ---- 3. bounded slice of the case table's own fixtures ----------------------
  log="$WORK/selftest-cases.log"
  : > "$log"
  for id in silent-open completed-not-open ledger-missing-not-silent; do
    "case_${id//-/_}"
  done > "$log" 2>&1 || true
  ran=$((TOTAL_N - total_before))
  passed=$((PASS_N - pass_before))
  failed=$(( ${#FAILED_IDS[@]} - fail_before ))
  st_check "$([ "$ran" -eq 3 ] && printf 1 || printf 0)" \
    "bounded case slice ran $ran case(s), expected 3"
  st_check "$([ "$passed" -eq 3 ] && [ "$failed" -eq 0 ] && printf 1 || printf 0)" \
    "bounded case slice passed=$passed failed=$failed"
  if [ "$passed" -ne 3 ] || [ "$failed" -ne 0 ]; then
    grep -E '^FAIL ' "$log" >&2 || true
  fi

  printf 'MORI_SILENCE_CASES_SELFTEST pass=%d fail=%d\n' "$ST_PASS" "$ST_FAIL"
  [ "$ST_FAIL" -eq 0 ] && exit 0
  exit 1
}

if [ "$SELFTEST" = 1 ]; then
  st_main
fi

shuffle_case_ids

# r6 R1: the run header is printed only AFTER the last case has run, so no
# living census invocation (nor any same-user process walking /proc) can read
# the seed, the shuffled order, or the nonce from this process's stdout while
# the cases are still executing. During the loop only PASS/FAIL lines are
# written, and those carry no run secret.
for case_it in "${CASE_IDS[@]}"; do
  "case_${case_it//-/_}"
done

printf 'SHUFFLE_SEED=%s\n' "$RUN_SEED"
printf 'RUN_NONCE=%s\n' "$RUN_NONCE"
printf 'CASE_ORDER=%s\n' "${CASE_IDS[*]}"

# =================================================================================
printf 'MORI_SILENCE_CASES: matched=%d total=%d\n' "$PASS_N" "$TOTAL_N"
if [ "$TOTAL_N" -eq 0 ]; then
  printf 'mori-silence-cases: no cases executed\n' >&2
  exit 2
fi
[ "$PASS_N" -eq "$TOTAL_N" ] && exit 0
printf 'mori-silence-cases: failed: %s\n' "${FAILED_IDS[*]}" >&2
exit 1
