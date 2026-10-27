# Mo56SecReports — credential / private-URL / hostname scan of the round-56 artifacts

Seat: Mo56SecReports (leaf; no subagent dispatch). Lane: mori-shokunin.
Measured revision: `8be2717b0809281d07dffe83dad424a4859e0747` (extracted with
`git archive` into scratch); the worktree at `acc62f54` was also scanned for the
files added after that revision, and results are reported separately below.
Scratch: `/fast/scratch/hyaku/mori-r56/Mo56SecReports/` (removed after the scan; every
file cited here was read from the extracted tree or the fleet repo, both read-only).
No tool was installed, upgraded or pinned; no pacman transaction was attempted.

Axes: (a) credential material, (b) private/internal URLs, (c) live hostnames beyond
the fleet, (d) the two new registry rows against the no-credential rule, and the
exposure surfaces the two new tools create when they consume untrusted text.

## Scope of the scan

Files measured (32 at the stated revision, plus `corpus/SOURCES.md` for the rows):

```
.ufo/waves/round-56/{contract.md,count-c1.py,count-c2.py,controls/controls.py}
.ufo/waves/round-56/evidence/{c1-at-freeze,c2-at-freeze,c2-old-counter-voted0,census-start,
                              controls,driver-liveness-live,freeze-sha256,
                              selftest-c1-counter,selftest-c2-counter,selftest-vote-bind,
                              tally-r55}.txt
.ufo/waves/round-56/fixtures/driver/{attempt-rollover,fails-and-dead,hyaku-pairing,in-flight,
                                     legacy-grammar,malformed,state-shapes,two-lanes,variants}
.ufo/waves/round-56/fixtures/driver/state-shapes/state/{mori.round,tabi.round/inner}
tools/mori-driver-liveness.py   tools/mori-vote-bind.py
corpus/knowledge/driver-liveness-r56.md   corpus/knowledge/vote-binding-r56.md
corpus/evidence/sources-r56/rfc8259.txt   corpus/evidence/sources-r56/watchdog-log-grammar.txt
corpus/SOURCES.md (rows S544, S545)
```

## (a) Credential material — zero hits

Pattern (case-insensitive; the assignment's list plus common token shapes):

```
BEGIN [A-Z ]*PRIVATE KEY|BEGIN OPENSSH PRIVATE|op://|server\.token|session=|Set-Cookie|
[Cc]ookie:|Authorization:|Bearer[[:space:]]|ghp_|github_pat_|AKIA[0-9A-Z]{16}|xoxb-|
api[_-]?key|client_secret|refresh_token
```

(The `op:` and `session=` fragments above are regex literals of the rule being searched
for, not values; the same holds for the later quotation of `SKILL.md:147` in section (d).)

Per-file result: `hits=0` for all 32 measured files (the pattern run prints one line per
file; no line deviates), and the aggregate is `sum_hits=0`:

```
$ grep -rEci -- "$PAT" .ufo/waves/round-56 tools/mori-driver-liveness.py tools/mori-vote-bind.py \
      corpus/knowledge/driver-liveness-r56.md corpus/knowledge/vote-binding-r56.md \
      corpus/evidence/sources-r56/*.txt corpus/SOURCES.md | awk -F: '{s+=$NF} END{print "sum_hits="s+0}'
sum_hits=0            # exit 0
```

Session/agent-path shapes were checked separately (`.omp`, `omp://`, `agent://`,
`history://`, `local://`, `sessions?/`, `keyring`, `1password`, `HL_*TOKEN`, `uuid`):
one combined `grep -rEnI` over the same set returned no line and exit 1 — i.e. the
string `1password`/`HL_INITIAL_WORKSPACE_TOKEN` that `SKILL.md`'s exclusions section
names is **not** reproduced in any round-56 artifact or in either new tool.

Machine hostname: `grep -rFIl -- "$(hostname)"` over the round-56 tree, both tools, the
two entries and the two evidence copies returned no file, exit 1 (full and short form).

## (b) Private URLs — none; only public sources

URL inventory (`grep -EoI 'https?://[^ )"<>`]+'`) over the 32 files:

- round-56 artifacts (contract, counters, controls, all receipts, all fixtures): **0 URLs**.
- the two knowledge entries: **0 URLs**.
- `corpus/evidence/sources-r56/watchdog-log-grammar.txt`: **0 URLs**.
- `corpus/evidence/sources-r56/rfc8259.txt`: 18 URLs, every one a public IETF/IETF-
  trustee/Unicode/ECMA reference inside the published RFC body
  (`rfc-editor.org/info/rfc7159`, `rfc-editor.org/errata/eid…`, `unicode.org/versions/latest/`, …).
- `evidence/census-start.txt`: public registry hosts only (`github.com`, `man7.org`,
  `docs.python.org`, `kubernetes.io`, `ftp.gnu.org`, `www.freedesktop.org`, …).

No loopback endpoint, no `ssh://`, no internal domain (`*.local`/`*.internal`/`*.lan`),
no IPv4 literal anywhere in the 32 files (`grep -EoI '\b([0-9]{1,3}\.){3}[0-9]{1,3}\b'`:
no line). The only machine-specific strings are local absolute paths
(`/home/vgpnk/Projects/shokunin/…`, 6 occurrences: `controls/controls.py:70`,
`count-c1.py:178`, `count-c2.py:145`, `evidence/census-start.txt:24`,
`evidence/driver-liveness-live.txt:287`, `evidence/freeze-sha256.txt:11,12`) and fleet
lane names; both are already the lane's established artifact vocabulary, not URLs.

## (c) Hostnames beyond the fleet — none

- The live receipt `evidence/driver-liveness-live.txt` (304 lines) contains only lane
  names (`mori`, `kake`, `kama`, `tabi`, `tsukuroi`, …), epoch timestamps, counts and the
  fleet path `.ufo/watchdog.log`; no host string, no URL, no credential.
- Fixture logs contain lane names plus driver-line fields only.

**Evidence-copy integrity (checked because a tampered extract is an injection vector).**
The RFC copy is byte-identical to the current publication, not merely to its own pin:

```
$ curl -fsSL --max-time 60 https://www.rfc-editor.org/rfc/rfc8259.txt -o demo/rfc8259.pub   # curl_rc=0
$ sha256sum demo/rfc8259.pub tree/corpus/evidence/sources-r56/rfc8259.txt
61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7  demo/rfc8259.pub
61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7  tree/corpus/evidence/sources-r56/rfc8259.txt
$ cmp -s … && echo IDENTICAL        # IDENTICAL
```

Its pin equals the S545 cell and `evidence/freeze-sha256.txt:11`. A scan of the copy for
injected instruction text (`ignore (all|previous)`, `instruction`, `RECHECK`, `ENTAIL`,
`vote`, `seat`, `system prompt`) returned no line (exit 1), so the copy is a verbatim RFC,
not a carrier.

The second extract is faithful to the writers it cites (read-only read of the fleet repo):

```
$ sed -n '149p;176p;182p' scripts/hyaku/inline.sh
  log "launch $lane round=$n pgid=$$ driver=hyaku-inline attempt=$a"
  log "complete $lane round=$n; hyaku-inline attempt=$(claim "$lane" attempt)"
  log "lane-dead-no-report $lane round=$n; retry same round (hyaku-inline attempt=$a: $why)"
$ sed -n '266p;405p;448p' scripts/shokunin-watchdog.sh
  log "launch $lane round=$n pgid=$pid"
      log "complete $lane round=$n; advancing to round=$((n+1))"
        log "lane-dead-no-report $lane round=$n; retry same round"      # exit 0
```

Both files hash to their frozen pins (`38ba3e6b…a417796`, `61a5378f…4cd2d7`) and the two
tools hash to `6b3dba74…be997` / `8be1acdb…dfa6bca`, matching `evidence/freeze-sha256.txt`;
`cmp` of the worktree copies against the `8be2717b` tree copies prints `same` for both.

## (d) Registry rows S544 / S545 against the no-credential rule

`SKILL.md:147` — "Credentials, oauth, `server.token` and session material are SHAPE
ONLY"; `PROVINCE.md:68` — mori "never reads or reports credential material".

- S544 (`corpus/SOURCES.md:324`, own-work): names two local scripts, six line anchors and
  a local extract path + sha256. No URL, no token, no session material.
- S545 (`corpus/SOURCES.md:325`, spec): one public RFC URL, section/line anchors, the
  copy path + sha256. Public source, no credential shape.
- `grep -icE 'token|credential|secret|oauth|password'` over both rows: 0.

Rows are compliant with the rule as written.

## Exposure surfaces the new tools create (the only sub-findings on this axis)

Neither tool holds a credential, and neither opens a network socket, forks, or evaluates
code: `grep -nE 'urllib|socket|requests|http\.client|subprocess|os\.system|eval\(|exec\(|compile\('`
over both tools returns only `re.compile` lines (the regex tables at
`tools/mori-driver-liveness.py:54-62`, `tools/mori-vote-bind.py:64-65`) and no line for
`urllib`, `socket`, `subprocess`, `os.system`, `eval(` or `exec(`. Both do
**echo untrusted text back into their stdout**, which is the one way a credential could
reach a receipt or a wave log through them:

1. `tools/mori-driver-liveness.py:89` keeps `raw[:120]` of each malformed line, up to
   `MAX_MALFORMED_EXAMPLES = 3` (`:63`), and prints them in `log.examples`. The log path is
   operator-supplied (`--log`, `:454`) and is opened after `os.path.isfile(log_path)`
   (`:204`), which follows symlinks; there is no containment/refusal check anywhere in the
   file (`grep -n 'refus'` matches only the selftest case name `t_malformed_refusal` at
   `:322`). Reproduced in scratch with a fixture file holding a credential-shaped first
   line:

   ```
   $ python3 tools/mori-driver-liveness.py --log "$S/demo/credish.txt" --now 1793107000
   [ "sk-DEMO-NOT-A-REAL-KEY-…", "ordinary prose line", "third line" ]   # malformed 4, rc 0
   ```

   and through a symlink named `watchdog.log` pointed at the same file: same echo, `rc 0`.
   The committed live receipt is clean (`"examples": []`), so nothing leaked this round;
   the exposure is the capability, not an occurrence. This is exactly the class
   `SKILL.md`'s "Secret-exposure exclusions" already ruled out for `MORI_CGROUP_CURRENT`
   ("an operator-pointed … would print another file's first line; the probe refuses
   out-of-tree paths shape-only"). The new probe has no equivalent refusal.
2. `tools/mori-vote-bind.py:435` prints the free-text tail `rest` of a bound vote line
   (`rest` is `(.*)` at `VOTE_RE:64`; stored at `:94`/`:106`). Measured: a 4,000-character
   tail produces a 4,038-byte `VOTE …` line on stdout (`rc 0`); a JSON string scalar
   `{"a":"RECHECK <hash12> holds <tail>"}` echoes `<tail>` verbatim. A secret written on
   the same line as a vote-shaped token would land in the tally log.

## Limits (UNVERIFIED / not attempted)

- Nothing outside the listed 32 files, `corpus/SOURCES.md` and the post-freeze additions
  (`w1-spec.json`, `w1-dispatch.json`, `build-w1-spec.py`, `w1/*.md`) was scanned; host
  credential stores were neither read nor enumerated (that is kagi's province).
- The post-freeze additions were scanned with the same URL/credential patterns: the only
  URL-shaped matches are the public `rfc-editor.org` citations inside four `w1/*.md`
  reports and the S545 row, none of them new material (`w1-spec.json:284`,
  `w1-dispatch.json:701`, `build-w1-spec.py:199` match the pattern only through the word
  `token` inside this seat's own prompt text, not through a value).
- I did not fetch any source other than `rfc8259.txt`; no other copy was re-verified
  against its upstream (provenance is another seat's axis).
- I did not run either counter; the receipts' claims about `C1`/`C2` are outside this
  seat's surface and were only read as bytes.

## Findings

- **SR-1 — MED — `tools/mori-driver-liveness.py:89` (with `:63`, `:204`, `:454`, `:240`).**
  Malformed-line examples echo up to 3 × 120 raw characters of any `--log` path, the path
  is arbitrary, and `os.path.isfile` follows a symlink, so an operator- or lane-pointed
  file is echoed into JSON with no containment refusal. Reproduced (rc 0) with both a
  direct path and a `watchdog.log` symlink; no occurrence in the committed receipt
  (`evidence/driver-liveness-live.txt`, `"examples": []`). Smallest remediation: refuse a
  log path that does not resolve under the fleet root's `.ufo/` (or under the `--fixture`
  dir) with `DRIVER_LIVENESS_UNAVAILABLE` + `refused:outside-fleet`, and/or reduce the
  example to its first token plus a length. Because pins are frozen, this routes to
  round 57 unless the L1 elects a re-pin.
- **SR-2 — LOW — `tools/mori-vote-bind.py:435` (with `:64`, `:94`, `:106`).** The binder
  prints the unbounded `rest` tail of every bound vote line (measured 4,038 bytes from one
  line, rc 0). Any secret sharing a line with a vote-shaped token would be echoed into the
  tally output. Smallest remediation: cap `rest` in the printed field (e.g. 80 chars with
  an ellipsis) or print `rest_len` instead of the text.
- **SR-3 — LOW (informational) — `.ufo/waves/round-56/fixtures/driver/in-flight/watchdog.log:1`,
  also `hyaku-pairing:1`, `malformed:2`, `state-shapes:1`, `two-lanes:1-2`.** The fixtures
  copy a real historical host process-group id (`pgid=620717`, and `pgid=336804` for kake)
  verbatim from `.ufo/watchdog.log`; the `in-flight` line is byte-identical to the live log
  line for `2026-10-27T10:08:36-03:00`. Neither group is live now (`ps -eo pgid=` shows no
  member for either; `/proc/620717` absent). Not credential material, but live host state
  that a synthetic id would have served as well. No action required this round.
- **SR-4 — LOW — `tools/mori-driver-liveness.py:240` (note text), docstring `:37`.** The
  emitted note "state \*.round values are never read here; symlinks never followed" is
  true for the state directory only; the `--log` input does follow symlinks (`:204`). A
  reader can over-read the note as a whole-tool guarantee. Smallest remediation: scope the
  note to the state directory explicitly, or make the log path refusal from SR-1 true.

Clean-scan result (no finding): no credential material, no private or internal URL, no
IPv4 literal, and no hostname beyond the fleet appears in any round-56 artifact, either
new tool, either entry, either evidence copy or either new registry row; the RFC copy is
byte-identical to the published text and the grammar extract matches its writer scripts
line for line.
