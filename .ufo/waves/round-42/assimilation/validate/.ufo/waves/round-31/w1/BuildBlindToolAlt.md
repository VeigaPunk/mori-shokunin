# Round 31 wave 1 — BuildBlindToolAlt: independent second C2 implementation

Seat MoriR31.BuildBlindToolAlt. Deliverable: a second, independently written `tools/mori-blind-check.sh`
for the L1 to pick from, built only from `.ufo/waves/round-31/rule-text.md` and
`.ufo/waves/round-30/check-blind-wave.sh:76-162` (the two unchanged detectors).

## What was built

- Script (scratch): `/fast/scratch/hyaku/mori-r31/BuildBlindToolAlt/mori-blind-check.sh` (269 lines, executable).
  Full text pasted at the bottom of this report; the L1 can copy it to `tools/mori-blind-check.sh` verbatim if picked.
- Bash entry point + embedded `python3 -I -B` parser (quoted heredoc, no shell expansion into the parser).
- Interface (rule-text.md): `mori-blind-check.sh <lane-rev> <wave-report-dir> <writer-name-regex> <allow-file>`,
  plus `--selftest`. Output `scanned=N`, `blind_violations=M`, then one `path:line:rule` line per hit sorted by
  (path, line) — Python sort is stable, so same-line ties keep discovery order (citation before run-output,
  matching the gate's per-line order). Exit 0 no hit, 1 hits, 2 usage/input error.
- Scope: only top-level `*.md` files under the dir whose basename matches the writer regex; content read from the
  commit (`git show <rev>:<path>`), never the worktree.

## Argument validation (same shape as the round-30 gate)

Exactly 4 args else usage to stderr and exit 2; repo root via `git rev-parse --show-toplevel`; lane revision resolved
with `git rev-parse --verify --quiet "<rev>^{commit}"`; wave dir must be a tree at that revision (`git cat-file -t`
must print `tree`, a blob is rejected); writer regex probed with bash's own `[[ probe =~ $re ]]` and exit status 2
means invalid; allow file must be readable. Verified in probe 4 below.

## Files-opened rule (clauses 1-5, implemented from rule-text.md only)

1. Block opens at an ATX heading of any level (`^[ \t]*#{1,6}[ \t]+`) whose text contains `files opened` or
   `opened files` (case-insensitive), or at a trimmed line starting with `Files opened:` / `Opened files:`
   (case-insensitive; literal single space as the rule text writes it).
2. Entries are lines that, after optional indentation, start with `- `, `* `, `+ `, `N. `, `N) ` or `|`. A separator
   row (row whose characters are only `|`, `-`, `:`, spaces, tabs) is not an entry, and the row on the line directly
   above it is dropped (adjacency checked by line number, so a blank line keeps the header an entry).
3. Blank lines are skipped; the block closes at the first heading or first other non-blank line; that closing
   heading/label may itself open the next block.
4. Candidates are whitespace tokens, stripped to a fixed point of wrapping backticks/quotes/`()[]{}` brackets,
   trailing `,;.` and a trailing `:L` / `:L-M` suffix; kept when they contain `://`, `/` or `.` or equal `LOG.md`,
   `SCORECARD.md`, `SKILL.md`, `PROVINCE.md`. `file://` and leading `./` are stripped before matching only.
   Matching is `fnmatch.fnmatchcase` against every allow line with `{report}` replaced by the brief's basename
   without `.md`. An entry with no candidate, or with at least one candidate no allow line matches, produces one
   `writer-forbidden-opened-path` hit at the entry's own line.
5. A brief with zero entries across all blocks produces one `writer-missing-files-opened-list` hit at line 1.
6. Clause 6 detectors: see next section. `c2-fixtures.json` and `count-c2.py` were never opened.

## Ported detectors — fidelity notes

- All eight gate regexes (check-blind-wave.sh:77-84) are embedded with their text verbatim; `posix_to_py` replaces
  the inner `[:name:]` tokens so the gate's partially bracketed classes (`[[:space:]:|]`, `[[:space:]_-]`,
  `[=[:space:]]`) keep POSIX meaning under Python `re`. The first cut translated only whole `[[:space:]]` forms and
  silently broke the two mid-class uses (missing `writer-tool-run-output` and one citation hit); the selftest caught
  it and the fix is in.
- `writer-tool-source-citation` fires unconditionally: in the gate it sits outside the `!protected` guard. Verified
  by the selftest brief `detect/protected.md`, where citation text inside a json-in-case fence hits while the
  verdict+exit on the same protected line does not.
- `writer-tool-run-output` is skipped when protected; json-fence-in-case-section and derivation-table-row protection
  are state-for-state identical; `--inputs` sets an 8-line window decremented at the end of every unprotected line
  (the setting line itself included), a new tool-run mention resets the window and the verdict-seen flag, and the
  same-line verdict+exit rule matches the gate's final check.
- The phantom empty element after a trailing newline is dropped before line numbering, so numbers match the gate's
  `while IFS= read -r` loop exactly.

## Verification (all quoted output is from runs executed this session)

1. `bash -n` on the script: clean.
2. `--selftest` (mktemp repo under my scratch dir, 11 synthetic briefs in `clean/`, `files/`, `detect/`):
   `PASS clean`, `PASS files`, `PASS detect`, exit 0. Coverage: allow-glob match, `{report}` placeholder,
   `file://` + `./` + backtick + `:12` + quote stripping, forbidden entry, entry with no candidate, missing list,
   table header + separator handling, close at prose plus a second block opened by a label line, cite_file hit,
   tool-header hit, pending-window hit plus an expired window, json-in-case protection with unconditional citation
   inside the fence, derivation-table protection.
3. Differential vs the round-30 gate on 5 synthetic briefs (harness:
   `/fast/scratch/hyaku/mori-r31/BuildBlindToolAlt/run-differential.sh`). The gate's real interface is 3-arg — its
   usage line observed at runtime: `usage: check-blind-wave.sh <lane-rev> <wave-report-dir> <writer-name-regex> |
   --selftest` — so it cannot take an allow file; mine ran with 4 args. Briefs place each detector hit on line 1 so
   the gate's post-loop missing-list hit and my line-sorted output cannot diverge in order; the only files-rule
   output either tool produces on these briefs is `writer-missing-files-opened-list@1`, which both emit identically.
   Result: `STDOUT-IDENTICAL`, `RC-IDENTICAL (1)`. Both tools printed exactly:
   ```
   scanned=5
   blind_violations=9
   briefs/d1-cite.md:1:writer-tool-source-citation
   briefs/d1-cite.md:1:writer-missing-files-opened-list
   briefs/d2-header.md:1:writer-tool-source-citation
   briefs/d2-header.md:1:writer-missing-files-opened-list
   briefs/d3-runout.md:1:writer-tool-run-output
   briefs/d3-runout.md:1:writer-missing-files-opened-list
   briefs/d4-json.md:1:writer-missing-files-opened-list
   briefs/d5-deriv.md:1:writer-tool-run-output
   briefs/d5-deriv.md:1:writer-missing-files-opened-list
   ```
   Coverage: cite_file citation (d1), tool-header citation (d2), same-line run-output plus an expired `--inputs`
   window that must not hit (d3), json-in-case protection (d4: verdict+exit inside the fence, no run hit),
   derivation-table protection (d5: verdict+exit inside protected rows, no hit).
   An earlier differential run with path-bearing `## Files opened` entries also agreed on every detector line; the
   only diffs were the gate's `writer-forbidden-opened-path` lines (it has no allow file and flagged the entry),
   which is the D1-era behavior C2 replaces.
4. Input-error probes (exit status / stderr): 3 args → usage / 2; 5 args → usage / 2; regex `[` →
   `invalid writer-name regex: [` / 2; `nosuchrev^{commit}` → `lane revision does not resolve` / 2; `nosuchdir` →
   `wave-report-dir is not a tree at that revision` / 2; dir arg pointing at a file (blob) → same message / 2;
   missing allow file → `allow file not readable` / 2. Happy path on a real temp repo → `scanned=1`,
   `blind_violations=0`, exit 0.

## Known divergences from the round-30 gate (by design, not porting bugs)

- The files-opened rule is the round-31 rule text, not the gate's: per-entry forbidden hits, the allow-file
  interface, close at the first non-entry line, any-level headings and label lines, `{report}` placeholder.
- Label line is rule-literal `Files opened:` / `Opened files:` with a single space; the gate's label regex allowed
  runs of whitespace between the words.
- Candidate filter is rule-literal: any token containing `.` becomes a candidate, so prose like `e.g.` inside an
  entry line is a violating candidate unless an allow line matches. Flagging in case the fixtures intend otherwise.
- Python `re` is not POSIX ERE: common classes are translated; exotic writer regex constructs (backreferences,
  `\b`) are not bash-`[[ =~ ]]`-identical. Typical writer regexes behave the same.
- The pending-window decrement happens on the setting line itself (window covers lines k..k+7), matching the gate.

## Bounds compliance

- Wrote only: scratch files under `/fast/scratch/hyaku/mori-r31/BuildBlindToolAlt/` (tool, differential harness,
  throwaway repos, all cleaned or trapped) and this report. No lane git/jj writes; git writes only inside mktemp
  repos under my scratch; read-only git elsewhere.
- Every command ran under `timeout` <= 120 s; no background jobs; no subagents; nothing left running.
- Privacy: no uid, no real pid, no `user-<digits>.slice`, no journal MESSAGE text, no OMP settings values, no
  session ids anywhere in the artifacts.
- Tooling directive: nothing installed — no new tool was needed.
- Note: the mandated full-script paste pushes this file past the 250-line report bound; prose is kept minimal for
  that reason.

## Full script

````bash
#!/usr/bin/env bash
# mori-blind-check.sh — round-31 C2: files-opened rule over committed wave briefs.
# Independent second implementation (seat MoriR31.BuildBlindToolAlt). Rule and interface:
# .ufo/waves/round-31/rule-text.md. The two unchanged round-30 detectors and their
# json-in-case / derivation-table protection are ported line-faithfully from
# .ufo/waves/round-30/check-blind-wave.sh:76-162 (same regexes, same pending windows,
# citation detector outside the protected guard, run-output detector inside it).
# usage: mori-blind-check.sh <lane-rev> <wave-report-dir> <writer-name-regex> <allow-file>
#        mori-blind-check.sh --selftest          (synthetic briefs in a mktemp repo)
# exit: 0 = no hit, 1 = hits, 2 = usage or input error.
set -u
prog=${0##*/}

die2() { printf '%s: %s\n' "$prog" "$1" >&2; exit 2; }
usage() { printf 'usage: %s <lane-rev> <wave-report-dir> <writer-name-regex> <allow-file>\n       %s --selftest\n' "$prog" "$prog" >&2; }

run_parser() {  # repo_root resolved_rev wave_dir writer_re allow_file -> report on stdout, rc 0/1
python3 -I -B - "$@" <<'PYEOF'
import fnmatch, re, subprocess, sys

repo_root, resolved_rev, wave_dir, writer_src, allow_path = sys.argv[1:6]
NAMED = {'LOG.md', 'SCORECARD.md', 'SKILL.md', 'PROVINCE.md'}
SELFTEST_MARKER = 'MORI_OOM_KILLERS_SELFTEST:'
WRAP = '`"\'()[]{}'
SEP_CHARS = '|-: \t'

def die2(msg):
    sys.stderr.write('mori-blind-check.sh: %s\n' % msg)
    sys.exit(2)

def posix_to_py(src):
    # carry the gate's POSIX bracket classes into Python re with identical meaning;
    # replace the inner [:name:] token so it also works mid-class ([[:space:]:|] etc.)
    for a, b in (('[:space:]', ' \\t\\v\\f\\r'), ('[:alnum:]', '0-9A-Za-z'),
                 ('[:digit:]', '0-9'), ('[:alpha:]', 'A-Za-z'),
                 ('[:upper:]', 'A-Z'), ('[:lower:]', 'a-z')):
        src = src.replace(a, b)
    return src

def compile_ere(src, what):
    try:
        return re.compile(posix_to_py(src))
    except re.error as exc:
        die2('invalid %s: %s (%s)' % (what, src, exc))

# round-30 detectors: regex text verbatim from check-blind-wave.sh:77-84
CITE_FILE_RE = compile_ere(r'mori-oom-killers[.]py[[:space:]]*:[[:space:]]*[0-9]+([[:space:]]*[-–][[:space:]]*[0-9]+)?|mori-oom-killers[.]py[[:space:]]+lines?[[:space:]]+[0-9]+([[:space:]]*[-–][[:space:]]*[0-9]+)?', 'citation regex')
TOOL_HEADER_RE = compile_ere(r'(^|[^[:alnum:]_])tool[[:space:]]+lines?([[:space:]:|]|$)|(^|[^[:alnum:]_])tool[[:space:]]*:[[:space:]]*[0-9]+', 'tool-header regex')
VERDICT_RE = compile_ere(r'(^|[^[:alnum:]_])(KILLER_ACTED|KILLERS_QUIET|KILLERS_UNKNOWN)([^[:alnum:]_]|$)', 'verdict regex')
EXIT_RE = compile_ere(r'(^|[^[:alnum:]_])exit[[:space:]]*[:=]?[[:space:]]*[012]([^[:alnum:]_]|$)', 'exit regex')
INPUT_FLAG_RE = compile_ere(r'(^|[^[:alnum:]_])--inputs([=[:space:]]|$)', 'input-flag regex')
TOOL_RUN_RE = compile_ere(r'mori-oom-killers[.]py|tool[[:space:]_-]+(run|output|result)|run[[:space:]]+(of[[:space:]]+)?tool', 'tool-run regex')
JSON_OPEN_RE = compile_ere(r'^[[:space:]]*(```|~~~)[[:space:]]*json([[:space:]]|$)', 'json-fence regex')
FENCE_RE = compile_ere(r'^[[:space:]]*(```|~~~)', 'fence regex')
H2_RE = compile_ere(r'^##[[:space:]]+', 'h2 regex')
HEADING_RE = re.compile(r'^[ \t]*#{1,6}[ \t]+')
HEADING_TEXT_RE = re.compile(r'^[ \t]*#{1,6}[ \t]*')
FILES_TEXT_RE = re.compile(r'files opened|opened files')
NUM_ITEM_RE = re.compile(r'[0-9]+[.)] ')
LINE_SUFFIX_RE = re.compile(r':[0-9]+(?:-[0-9]+)?$')

try:
    allow_globs = [ln.strip() for ln in open(allow_path, encoding='utf-8').read().splitlines() if ln.strip()]
except OSError as exc:
    die2('cannot read allow file: %s' % exc)
writer_re = compile_ere(writer_src, 'writer-name regex')

def git(*args):
    return subprocess.run(('git', '-C', repo_root) + args, capture_output=True)

def candidate(token):
    # rule clause 4: strip wrapping backticks/quotes/brackets, trailing ,;., a :L or :L-M
    # suffix (to a fixed point), then strip file:// and ./ for matching only
    prev = None
    while prev != token:
        prev = token
        token = token.strip(WRAP).rstrip(',;.')
        m = LINE_SUFFIX_RE.search(token)
        if m:
            token = token[:m.start()]
    if token.startswith('file://'):
        token = token[7:]
    while token.startswith('./'):
        token = token[2:]
    return token

def entry_violates(line, base):
    cands = [c for c in (candidate(t) for t in line.split())
             if c and ('://' in c or '/' in c or '.' in c or c in NAMED)]
    if not cands:
        return True
    return any(not any(fnmatch.fnmatchcase(c, g.replace('{report}', base)) for g in allow_globs)
               for c in cands)

ls = git('ls-tree', '-rz', '--name-only', resolved_rev, '--', wave_dir)
if ls.returncode != 0:
    die2('git ls-tree failed: %s' % ls.stderr.decode('utf-8', 'replace').strip())

hits = []
scanned = 0
prefix = wave_dir + '/'
for raw in ls.stdout.split(b'\0'):
    if not raw:
        continue
    path = raw.decode('utf-8', 'replace')
    if not path.startswith(prefix):
        continue
    rel = path[len(prefix):]
    if '/' in rel or not rel.endswith('.md') or not writer_re.search(rel):
        continue
    show = git('show', resolved_rev + ':' + path)
    if show.returncode != 0:
        die2('unable to read committed report: ' + path)
    scanned += 1
    lines = show.stdout.decode('utf-8', 'replace').split('\n')
    if lines and lines[-1] == '':
        lines.pop()  # `while IFS= read -r` never yields the phantom line after the last \n
    base = rel[:-3]

    def flush(entries):
        n = 0
        for ln, text in entries:
            if entry_violates(text, base):
                hits.append((path, ln, 'writer-forbidden-opened-path'))
            n += 1
        return n

    # detector state (round-30 gate) and files-opened state (rule clauses 1-5)
    in_case_json = in_case_section = in_derivation = False
    pending_inputs = pending_tool = 0
    seen_run_verdict = False
    in_block = False
    block_entries = []
    total_entries = 0
    for i, line in enumerate(lines):
        line_no = i + 1
        lower = line.lower()
        trimmed = line.strip()
        # protection: json fence inside a case section, table rows inside derivation (gate)
        protected = False
        if in_case_json:
            protected = True
            if FENCE_RE.search(line):
                in_case_json = False
        elif in_case_section and JSON_OPEN_RE.search(line):
            protected = True
            in_case_json = True
        if H2_RE.search(line):
            in_derivation = 'derivation' in lower
            in_case_section = 'case' in lower
        if in_derivation and trimmed.startswith('|'):
            protected = True
        # detector 1: writer-tool-source-citation — fires unconditionally, like the gate
        if CITE_FILE_RE.search(lower) or TOOL_HEADER_RE.search(lower):
            hits.append((path, line_no, 'writer-tool-source-citation'))
        # detector 2: writer-tool-run-output — pending windows, skipped when protected (gate)
        if not protected:
            output_marker = SELFTEST_MARKER in line
            if INPUT_FLAG_RE.search(line):
                pending_inputs = 8
            if TOOL_RUN_RE.search(lower):
                pending_tool = 8
                seen_run_verdict = False
            has_verdict = bool(VERDICT_RE.search(line))
            has_exit = bool(EXIT_RE.search(lower))
            if pending_inputs > 0 and (has_verdict or has_exit):
                output_marker = True
                pending_inputs = 0
            if pending_tool > 0:
                if has_verdict:
                    seen_run_verdict = True
                if has_exit and seen_run_verdict:
                    output_marker = True
                    pending_tool = 0
                    seen_run_verdict = False
            if TOOL_RUN_RE.search(lower) and has_verdict and has_exit:
                output_marker = True
            if output_marker:
                hits.append((path, line_no, 'writer-tool-run-output'))
            if pending_inputs > 0:
                pending_inputs -= 1
            if pending_tool > 0:
                pending_tool -= 1
        # files-opened rule: clause 1 open (heading any level / label), clause 3 close
        is_head = HEADING_RE.match(line) is not None
        tl = trimmed.lower()
        is_label = tl.startswith('files opened:') or tl.startswith('opened files:')
        if in_block and (is_head or is_label):
            total_entries += flush(block_entries)
            block_entries = []
            in_block = False
        elif in_block and trimmed:
            t = line.lstrip()
            if t.startswith(('- ', '* ', '+ ')) or NUM_ITEM_RE.match(t) or t.startswith('|'):
                if t[0] == '|' and set(t) <= set(SEP_CHARS):
                    if block_entries and block_entries[-1][0] == line_no - 1:
                        block_entries.pop()  # header row directly above a separator row
                else:
                    block_entries.append((line_no, line))
            else:
                total_entries += flush(block_entries)
                block_entries = []
                in_block = False
        if not in_block and (is_label or (is_head and FILES_TEXT_RE.search(HEADING_TEXT_RE.sub('', line).lower()))):
            in_block = True
    if in_block:
        total_entries += flush(block_entries)
        block_entries = []
    if total_entries == 0:  # clause 5
        hits.append((path, 1, 'writer-missing-files-opened-list'))

hits.sort(key=lambda h: (h[0], h[1]))
sys.stdout.write('scanned=%d\nblind_violations=%d\n' % (scanned, len(hits)))
for p, ln, rule in hits:
    sys.stdout.write('%s:%d:%s\n' % (p, ln, rule))
sys.exit(1 if hits else 0)
PYEOF
}

if (( $# == 1 )) && [[ $1 == --selftest ]]; then
  base=${MORI_BLIND_CHECK_TMPDIR:-${TMPDIR:-/tmp}}
  work=$(mktemp -d "$base/mori-blind-check-selftest.XXXXXX") || die2 'mktemp failed'
  trap 'rm -rf "$work"' EXIT
  st=$work/repo
  git init -q "$st" || die2 'git init failed'
  w() { mkdir -p "$st/$(dirname "$1")"; printf '%s\n' "${@:2}" > "$st/$1"; }
  # clean: allow-glob match, {report} placeholder, file:// + ./ + backtick + :L + quote stripping
  w clean/placeholder.md '# Round 31 report' '' '## Files opened' '- corpus/placeholder-notes.md' '' 'Done.'
  w clean/strip.md '# Round 31 report' '' '## Files opened' '- `file://./scripts/shokunin-watchdog.sh:12`.' '- "corpus/strip-notes.md", read fully' '' 'Done.'
  # files-rule violations: forbidden entry, entry without candidate, no block, table header/separator, close+second block
  w files/forbidden.md '# Round 31 report' '' '## Files opened' '- scripts/shokunin-watchdog.sh' '- corpus/secret-drafts.md'
  w files/nocand.md '# Round 31 report' '' '## Files opened' '- triage notes and prose only'
  w files/missing.md '# Round 31 report' '' 'Prose only, no files section at all.'
  w files/table.md '# Round 31 report' '' '## Files opened' '| path | why |' '| ---- | --- |' '| corpus/table-slip.md | missed |'
  w files/close.md '# Round 31 report' '' '## Files opened' '- scripts/shokunin-watchdog.sh' 'Prose closes the first block.' '' 'Files opened:' '- corpus/late-block.md'
  # detectors: citation, tool-header citation, pending-window hit plus expired window, json+derivation protection
  w detect/cite.md '# Round 31 report' '' '## Files opened' '- scripts/shokunin-watchdog.sh' '' 'Ran mori-oom-killers.py:12-14 during triage.'
  w detect/cite2.md '# Round 31 report' '' '## Files opened' '- scripts/shokunin-watchdog.sh' '' 'Compare Tool lines: 40-120 before changing.'
  w detect/runout.md '# Round 31 report' '' '## Files opened' '- scripts/shokunin-watchdog.sh' '' '--inputs default flags were passed.' 'filler one' 'filler two' 'filler three' 'filler four' 'filler five' 'filler six' 'filler seven' 'Too late: KILLER_ACTED and exit 1 happened here.' '' 'tool run output: KILLERS_QUIET exit 0'
  w detect/protected.md '# Round 31 report' '' '## Files opened' '- scripts/shokunin-watchdog.sh' '' '## Case matrix' '```json' '{"cmd": "mori-oom-killers.py:1", "verdict": "KILLER_ACTED", "exit": 1}' '```' '' '## Derivation' '| step | run tool result |' '| ---- | --------------- |' '| 1 | KILLERS_UNKNOWN exit 2 |' '' '## Findings' 'Nothing else to report.'
  git -C "$st" add -A && git -C "$st" -c user.name=selftest -c user.email=selftest@invalid commit -qm briefs
  rev=$(git -C "$st" rev-parse HEAD)
  allow=$work/allow.txt
  printf '%s\n' 'scripts/shokunin-watchdog.sh' 'corpus/{report}-notes.md' > "$allow"
  fails=0
  expect() { local name=$1 dir=$2 erc=$3 want=$4; local got rc
    got=$(run_parser "$st" "$rev" "$dir" . "$allow"); rc=$?
    if [[ $got == "$want" && $rc == "$erc" ]]; then printf 'PASS %s\n' "$name"
    else printf 'FAIL %s (rc=%s want %s)\n%s\n' "$name" "$rc" "$erc" "$got"; fails=1; fi; }
  expect clean clean 0 $'scanned=2\nblind_violations=0'
  expect files files 1 $'scanned=5\nblind_violations=5\nfiles/close.md:8:writer-forbidden-opened-path\nfiles/forbidden.md:5:writer-forbidden-opened-path\nfiles/missing.md:1:writer-missing-files-opened-list\nfiles/nocand.md:4:writer-forbidden-opened-path\nfiles/table.md:6:writer-forbidden-opened-path'
  expect detect detect 1 $'scanned=4\nblind_violations=4\ndetect/cite.md:6:writer-tool-source-citation\ndetect/cite2.md:6:writer-tool-source-citation\ndetect/protected.md:8:writer-tool-source-citation\ndetect/runout.md:16:writer-tool-run-output'
  rm -rf "$work"
  trap - EXIT
  exit "$fails"
fi

(( $# == 4 )) || { usage; exit 2; }
lane_rev=$1 wave_dir=$2 writer_re=$3 allow_file=$4
repo_root=$(git rev-parse --show-toplevel 2>/dev/null) || die2 'not run inside a git repository'
wave_dir=${wave_dir#./}
wave_dir=${wave_dir%/}
[[ -n $wave_dir && $wave_dir != /* ]] || die2 'wave-report-dir must be a non-empty repo-relative path'
resolved_rev=$(git -C "$repo_root" rev-parse --verify --quiet "$lane_rev^{commit}") || die2 "lane revision does not resolve: $lane_rev"
[[ $(git -C "$repo_root" cat-file -t "$resolved_rev:$wave_dir" 2>/dev/null) == tree ]] || die2 "wave-report-dir is not a tree at that revision: $wave_dir"
{ [[ probe =~ $writer_re ]]; } 2>/dev/null
(( $? == 2 )) && die2 "invalid writer-name regex: $writer_re"
[[ -r $allow_file ]] || die2 "allow file not readable: $allow_file"
run_parser "$repo_root" "$resolved_rev" "$wave_dir" "$writer_re" "$allow_file"
````

