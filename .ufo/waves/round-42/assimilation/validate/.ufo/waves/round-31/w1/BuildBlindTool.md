# wave 1 — BuildBlindTool (C2 tool, files-opened rule)

Seat: MoriR31.BuildBlindTool (leaf executor). Built from `.ufo/waves/round-31/rule-text.md` and the
round-30 gate `.ufo/waves/round-30/check-blind-wave.sh` only. Did **not** open `c2-fixtures.json` or
`count-c2.py`.

## Files

- `/fast/scratch/hyaku/mori-r31/BuildBlindTool/mori-blind-check.sh` — the tool, 366 lines (full paste below).
- `/fast/scratch/hyaku/mori-r31/BuildBlindTool/allow-r30.txt` — round-30 allowlist as an allow file, used by the regression.
- This report. No lane file outside it was written; no installs were needed (no new tools; bash 5.3.20, host git only).

## Behavior

`mori-blind-check.sh <lane-rev> <wave-report-dir> <writer-name-regex> <allow-file>`, run inside the repo.
Prints `scanned=N`, `blind_violations=M`, then one `path:line:rule` hit per line, sorted by path then line
(`LC_ALL=C sort -t: -k1,1 -k2,2n -s`). Exit 0 no hit, 1 hits, 2 usage/input error. `--selftest` builds
synthetic briefs in a mktemp repo (under `$TMPDIR`) and asserts an exact 13-record expectation plus an
exit-0 no-match run, a missing-allow-file exit 2, and an empty-revision exit 2.

Changes vs the round-30 gate:

- `round30_path_allowed` (A2/A3 hardcode) replaced by `load_allow_file` + `path_allowed`: one bash glob per
  non-blank, non-`#` line; `{report}` in a line substitutes the brief basename without `.md`; the candidate
  gets `file://` and leading `./` stripped before matching (`[[ $candidate == $pattern ]]`, works under `set -f`).
- Files-opened parser rewritten to clauses 1-5: block opens at any-level ATX heading (`^#{1,6}[[:space:]]`)
  whose text contains `files opened`/`opened files` (case-insensitive substring) or at a trimmed line starting
  `Files opened:`/`Opened files:` (case-insensitive); entries are marker lines `- `, `* `, `+ `, `N. `, `N) `
  or `|` rows, blank lines skipped; the block closes at the first heading or first other non-blank line.
  Separator rows (trimmed line of only `|`, `-`, `:`, spaces, with at least one `|` and one `-`) are not
  entries and retract the entry directly above them (the table header), including its already-appended hit.
  Clause 4 token handling keeps the round-30 stripper; the `:L`/`:L-M` suffix strip is now
  `^(.+):[0-9]+(-[0-9]+)?$` (rule form, no `:L:M`), applied to every stripped token, and an entry with no
  candidate is forbidden (restored; round-30 did this via `entry_has_path && ! has_candidate`).
- Clause 5: `file_entry_count` counts entries across all blocks (label form included); zero at EOF is one
  `writer-missing-files-opened-list` hit at line 1.
- Every forbidden entry gets its own hit at its own line (D1's first-hit-only limit removed). Retraction of a
  table header blank its recorded `violation_lines` slot and decrements the counter; empty slots are filtered
  before output.
- `writer-tool-source-citation` and `writer-tool-run-output` detectors byte-identical (diff-proven below),
  as are the shared protected/fence/derivation guard lines; only the old `in_files_list`/`files_h2_active`
  updates (round-30 gate lines 114-116) were removed as part of the parser replacement.

## Evidence

- `bash -n mori-blind-check.sh` → clean (after hoisting `num_marker_re` out of a `case` body; an unquoted
  `)` in a `=~` regex inside `case` is a bash parse error).
- `TMPDIR=/fast/scratch/hyaku/mori-r31/BuildBlindTool bash mori-blind-check.sh --selftest` → `PASS`, exit 0
  (14 synthetic briefs a-n in a mktemp repo; covers prose after a list, two forbidden entries in one list,
  label form open + label-form forbidden, table form with header-row retraction, numbered `1.`/`2)`, entry
  without path, deeper heading closing + files-opened heading reopening, own vs other scratch via `{report}`,
  kernel.org URL glob + `file://` strip + foreign URL, backticks/comma/`:10-12` and quoted `:42` stripping,
  missing block at line 1, plus the two round-30 detectors live (citation, tool-run) and json/derivation
  protection still holding).
- Byte identity: `diff <(sed -n '121,124p;135,154p' check-blind-wave.sh) <(sed -n '179,182p;183,202p' mori-blind-check.sh)`
  → empty (DETECTORS_BYTE_IDENTICAL). Guard lines 105-113/117-119 vs new 118-126/130-132 identical; old
  114-116 (removed `in_files_list` branch) shown verbatim in the diff.
- Round-30 gate baseline: `bash .ufo/waves/round-30/check-blind-wave.sh 5c99f2d4213b41966d670d10006a2ff5135273e4
  .ufo/waves/round-30/w1 '^CaseR30[a-d]\.md$'` → `scanned=4`, `blind_violations=1`,
  `.ufo/waves/round-30/w1/CaseR30a.md:105:writer-forbidden-opened-path`, exit 1.
- New gate, same rev/dir/regex plus `allow-r30.txt`:
  ```
  scanned=4
  blind_violations=3
  .ufo/waves/round-30/w1/CaseR30a.md:1:writer-missing-files-opened-list
  .ufo/waves/round-30/w1/CaseR30b.md:1:writer-missing-files-opened-list
  .ufo/waves/round-30/w1/CaseR30d.md:1:writer-missing-files-opened-list
  ```
  exit 1. **CaseR30a.md:105 is no longer a hit** (the required outcome).

## Regression analysis (for the L1 to keep or reject)

- Why `:105` fired before: the old parser never closed the block at prose, so `CaseR30a.md:105` ("The scratch
  JSON passed python3 json.load; ...", a non-entry line) was token-scanned and its `json.load` token became a
  forbidden hit. Under clauses 2-3 line 105 is an "other non-blank line": it closes the block and is never an
  entry.
- The three new `:1` hits are clause-5 consequences, not parser noise: CaseR30a (lines 96-103), CaseR30b
  (116-121) and CaseR30d (110-116) list opened files as **bare path lines with no marker**. Clause 2 defines
  entries by marker/table shape only, so those sections contain no entry, the block closes at the first bare
  path line, and the brief has "no entry in any block". The old gate tolerated this because its token loop set
  `entry_has_path` for any path-like token. CaseR30c, the only brief with a real `- ` list, is clean under the
  new rule (its entries strip to allowed paths, `:1-114` included). If round-31 fixtures encode bare-path
  sections as acceptable, that is a rule-text question for the L1, not a parser deviation; the tool follows
  the frozen clauses 1-5 exactly.
- Interpretation choices where the rule text left room: heading = ATX with required space, any level;
  heading/label text matched as literal case-insensitive substrings (single space, as written); separator must
  contain at least one `|` and one `-` (a bare `---` rule line is therefore an "other non-blank line" that
  closes the block, not a table row); `:L`/`:L-M` strip applies to URL tokens too (rule wording puts the strip
  before candidate classification; no regression-data URL ends in `:digits`).

## Risks / handoff

- If the L1 wants round-30 bare-path sections to pass, that needs a rule-text amendment, not a tool tweak.
- Sorting is `sort -t: -k1,1 -k2,2n -s`; hit paths containing `:` would mis-sort (none in lane data).
- No blocking issues. All processes run under `timeout`; tmp repos self-remove via the selftest trap.
- Note: report length exceeds the 250-line guidance because the assignment requires the full script paste.

## Full script

```bash
#!/usr/bin/env bash
set -o nounset -o pipefail
set -f
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE

usage() {
    printf 'usage: mori-blind-check.sh <lane-rev> <wave-report-dir> <writer-name-regex> <allow-file> | --selftest\n' >&2
}

fail() { printf 'blind check: %s\n' "$1" >&2; return 2; }

# Allow file: one bash glob per non-blank, non-# line. "{report}" in a line stands for the brief
# basename without .md. file:// and a leading ./ are stripped from the candidate before matching.
load_allow_file() {
    local file=$1 raw
    allow_pats=()
    if [[ ! -f $file || ! -r $file ]]; then
        fail 'allow file is not a readable file'
        return 2
    fi
    while IFS= read -r raw || [[ -n $raw ]]; do
        raw=${raw%$'\r'}
        [[ -z ${raw//[[:space:]]/} ]] && continue
        [[ $raw == '#'* ]] && continue
        allow_pats+=("$raw")
    done < "$file"
}

path_allowed() {
    local candidate=$1 pattern
    while [[ $candidate == file://* ]]; do candidate=${candidate#file://}; done
    while [[ $candidate == ./* ]]; do candidate=${candidate#./}; done
    for pattern in "${allow_pats[@]}"; do
        pattern=${pattern//'{report}'/$report_base}
        # shellcheck disable=SC2254  # the pattern comes from the allow file on purpose
        [[ $candidate == $pattern ]] && return 0
    done
    return 1
}

# Rule clause 4: an entry's candidates are its tokens, stripped of wrapping backticks, quotes and
# brackets, trailing ",;." and a ":L" / ":L-M" suffix, that contain "://", "/" or "." or equal
# LOG.md, SCORECARD.md, SKILL.md or PROVINCE.md. Sets entry_forbidden=1 when the entry has no
# candidate or some candidate matches no allow line.
inspect_entry_line() {
    local line=$1 token candidate last
    entry_forbidden=0
    entry_has_candidate=0
    for token in $line; do
        candidate=$token
        while [[ ${candidate:0:1} == '`' || ${candidate:0:1} == '"' || ${candidate:0:1} == "'" || ${candidate:0:1} == '(' || ${candidate:0:1} == '[' || ${candidate:0:1} == '{' || ${candidate:0:1} == '<' ]]; do candidate=${candidate:1}; done
        while [[ -n $candidate ]]; do
            last=${candidate: -1}
            case $last in '`'|'"'|"'"|')'|']'|'}'|'>'|','|';'|'.') candidate=${candidate:0:${#candidate}-1} ;; *) break ;; esac
        done
        if [[ $candidate =~ ^(.+):[0-9]+(-[0-9]+)?$ ]]; then candidate=${BASH_REMATCH[1]}; fi
        [[ -z $candidate ]] && continue
        if [[ $candidate == *://* || $candidate == *'/'* || $candidate == *.* || $candidate == LOG.md || $candidate == SCORECARD.md || $candidate == SKILL.md || $candidate == PROVINCE.md ]]; then
            entry_has_candidate=1
            path_allowed "$candidate" || entry_forbidden=1
        fi
    done
    if (( ! entry_has_candidate )); then entry_forbidden=1; fi
}

run_gate() {
    local repo_root=$1 revision=$2 wave_dir=$3 writer_re=$4 allow_file=$5 resolved_rev path relative base content
    local line lower_line trimmed_line trimmed_lower line_no in_case_json in_case_section in_derivation
    local block_open entry_line is_separator prev_was_entry last_entry_hit_idx file_entry_count
    local entry_forbidden entry_has_candidate report_base
    local pending_inputs pending_tool seen_run_verdict
    local has_verdict has_exit output_marker protected
    local hit
    local -a tree_paths=() allow_pats=() violation_lines=() printable=()
    local scanned=0 violations=0
    while [[ $wave_dir == ./* ]]; do wave_dir=${wave_dir#./}; done
    while [[ $wave_dir == */ ]]; do wave_dir=${wave_dir%/}; done
    if [[ -z $revision || -z $wave_dir || -z $writer_re || -z $allow_file || $wave_dir == /* || $wave_dir == . || $wave_dir == .. || $wave_dir == *'/../'* || $wave_dir == ../* || $wave_dir == */.. || $wave_dir == *:* ]]; then
        usage; return 2
    fi
    resolved_rev=$(git -C "$repo_root" rev-parse --verify --quiet --end-of-options "${revision}^{commit}" 2>/dev/null) || { fail 'invalid lane revision'; return 2; }
    if [[ $(git -C "$repo_root" cat-file -t "$resolved_rev:$wave_dir" 2>/dev/null) != tree ]]; then
        fail 'report directory is absent at revision'; return 2
    fi
    grep -E -q -- "$writer_re" /dev/null 2>/dev/null
    local regex_status=$?
    if (( regex_status > 1 )); then fail 'invalid writer-name regex'; return 2; fi
    load_allow_file "$allow_file" || return $?
    mapfile -d '' -t tree_paths < <(git -C "$repo_root" ls-tree -rz --name-only "$resolved_rev" -- "$wave_dir")
    local cite_file_re='mori-oom-killers[.]py[[:space:]]*:[[:space:]]*[0-9]+([[:space:]]*[-–][[:space:]]*[0-9]+)?|mori-oom-killers[.]py[[:space:]]+lines?[[:space:]]+[0-9]+([[:space:]]*[-–][[:space:]]*[0-9]+)?'
    local tool_header_re='(^|[^[:alnum:]_])tool[[:space:]]+lines?([[:space:]:|]|$)|(^|[^[:alnum:]_])tool[[:space:]]*:[[:space:]]*[0-9]+'
    local selftest_marker='MORI_OOM_KILLERS_SELFTEST:'
    local verdict_re='(^|[^[:alnum:]_])(KILLER_ACTED|KILLERS_QUIET|KILLERS_UNKNOWN)([^[:alnum:]_]|$)'
    local exit_re='(^|[^[:alnum:]_])exit[[:space:]]*[:=]?[[:space:]]*[012]([^[:alnum:]_]|$)'
    local input_flag_re='(^|[^[:alnum:]_])--inputs([=[:space:]]|$)'
    local tool_run_re='mori-oom-killers[.]py|tool[[:space:]_-]+(run|output|result)|run[[:space:]]+(of[[:space:]]+)?tool'
    local json_open_re='^[[:space:]]*(```|~~~)[[:space:]]*json([[:space:]]|$)'
    local fence_re='^[[:space:]]*(```|~~~)'
    local h2_re='^##[[:space:]]+'
    local heading_re='^#{1,6}[[:space:]]'
    local num_marker_re='^[0-9]+[.)][[:space:]]'
    for path in "${tree_paths[@]}"; do
        relative=${path#"$wave_dir"/}
        [[ $relative == */* || $relative != *.md ]] && continue
        base=${path##*/}
        [[ $base =~ $writer_re ]] || continue
        content=$(git -C "$repo_root" show "$resolved_rev:$path") || { fail 'unable to read committed report'; return 2; }
        report_base=${base%.md}
        ((scanned += 1))
        line_no=0; in_case_json=0; in_case_section=0; in_derivation=0
        block_open=0; prev_was_entry=0; last_entry_hit_idx=-1; file_entry_count=0
        pending_inputs=0; pending_tool=0; seen_run_verdict=0
        while IFS= read -r line || [[ -n $line ]]; do
            ((line_no += 1))
            lower_line=${line,,}
            trimmed_line=${line#"${line%%[![:space:]]*}"}
            trimmed_lower=${trimmed_line,,}
            protected=0
            if (( in_case_json )); then
                protected=1
                if [[ $line =~ $fence_re ]]; then in_case_json=0; fi
            elif [[ $line =~ $json_open_re ]] && (( in_case_section )); then
                protected=1; in_case_json=1
            fi
            if [[ $line =~ $h2_re ]]; then
                if [[ $lower_line == *derivation* ]]; then in_derivation=1; else in_derivation=0; fi
                if [[ $lower_line == *case* ]]; then in_case_section=1; else in_case_section=0; fi
            fi
            if (( in_derivation )) && [[ $trimmed_line == '|'* ]]; then protected=1; fi

            # Files-opened block parser (rule clauses 1-3).
            if [[ $line =~ $heading_re ]]; then
                block_open=0; prev_was_entry=0; last_entry_hit_idx=-1
                if [[ $lower_line == *'files opened'* || $lower_line == *'opened files'* ]]; then
                    block_open=1
                fi
            elif [[ $trimmed_lower == 'files opened:'* || $trimmed_lower == 'opened files:'* ]]; then
                block_open=1; prev_was_entry=0; last_entry_hit_idx=-1
            elif (( block_open )); then
                if [[ -z ${line//[[:space:]]/} ]]; then
                    prev_was_entry=0; last_entry_hit_idx=-1
                else
                    entry_line=0; is_separator=0
                    if [[ -z ${trimmed_line//[[:space:]:|-]/} && $trimmed_line == *-* && $trimmed_line == *'|'* ]]; then
                        is_separator=1
                    else
                        case $trimmed_line in
                            '- '*|'* '*|'+ '*|'|'*) entry_line=1 ;;
                            [0-9]*) [[ $trimmed_line =~ $num_marker_re ]] && entry_line=1 ;;
                        esac
                    fi
                    if (( is_separator )); then
                        # A separator row is not an entry, and neither is the row directly above it.
                        if (( prev_was_entry )); then
                            ((file_entry_count -= 1))
                            if (( last_entry_hit_idx >= 0 )); then
                                violation_lines[last_entry_hit_idx]=''
                                ((violations -= 1))
                            fi
                        fi
                        prev_was_entry=0; last_entry_hit_idx=-1
                    elif (( entry_line )); then
                        inspect_entry_line "$line"
                        if (( entry_forbidden )); then
                            violation_lines+=("$path:$line_no:writer-forbidden-opened-path")
                            ((violations += 1))
                            last_entry_hit_idx=$(( ${#violation_lines[@]} - 1 ))
                        else
                            last_entry_hit_idx=-1
                        fi
                        ((file_entry_count += 1))
                        prev_was_entry=1
                    else
                        block_open=0; prev_was_entry=0; last_entry_hit_idx=-1
                    fi
                fi
            fi

            if [[ $lower_line =~ $cite_file_re || $lower_line =~ $tool_header_re ]]; then
                ((violations += 1)); violation_lines+=("$path:$line_no:writer-tool-source-citation")
            fi

            if (( ! protected )); then
                output_marker=0
                [[ $line == *"$selftest_marker"* ]] && output_marker=1
                [[ $line =~ $input_flag_re ]] && pending_inputs=8
                [[ $lower_line =~ $tool_run_re ]] && { pending_tool=8; seen_run_verdict=0; }
                has_verdict=0; has_exit=0
                [[ $line =~ $verdict_re ]] && has_verdict=1
                [[ $lower_line =~ $exit_re ]] && has_exit=1
                if (( pending_inputs > 0 )) && (( has_verdict || has_exit )); then output_marker=1; pending_inputs=0; fi
                if (( pending_tool > 0 )); then
                    (( has_verdict )) && seen_run_verdict=1
                    if (( has_exit && seen_run_verdict )); then output_marker=1; pending_tool=0; seen_run_verdict=0; fi
                fi
                if [[ $lower_line =~ $tool_run_re ]] && (( has_verdict && has_exit )); then output_marker=1; fi
                if (( output_marker )); then
                    ((violations += 1)); violation_lines+=("$path:$line_no:writer-tool-run-output")
                fi
                (( pending_inputs > 0 )) && ((pending_inputs -= 1))
                (( pending_tool > 0 )) && ((pending_tool -= 1))
            fi
        done <<< "$content"
        if (( file_entry_count == 0 )); then
            violation_lines+=("$path:1:writer-missing-files-opened-list")
            ((violations += 1))
        fi
    done
    printf 'scanned=%d\nblind_violations=%d\n' "$scanned" "$violations"
    if (( violations > 0 )); then
        for hit in "${violation_lines[@]}"; do
            [[ -n $hit ]] && printable+=("$hit")
        done
        printf '%s\n' "${printable[@]}" | LC_ALL=C sort -t: -k1,1 -k2,2n -s
        return 1
    fi
    return 0
}

SELFTEST_TMPROOT=
selftest() {
    local tmp_root repo wave allow output status first rest second records line synthetic_rev
    local i=0
    local -a expected=(
        '.ufo/waves/round-31/w1/CaseR31b.md:2:writer-forbidden-opened-path'
        '.ufo/waves/round-31/w1/CaseR31b.md:3:writer-forbidden-opened-path'
        '.ufo/waves/round-31/w1/CaseR31d.md:2:writer-forbidden-opened-path'
        '.ufo/waves/round-31/w1/CaseR31e.md:6:writer-forbidden-opened-path'
        '.ufo/waves/round-31/w1/CaseR31f.md:3:writer-forbidden-opened-path'
        '.ufo/waves/round-31/w1/CaseR31g.md:2:writer-forbidden-opened-path'
        '.ufo/waves/round-31/w1/CaseR31h.md:2:writer-forbidden-opened-path'
        '.ufo/waves/round-31/w1/CaseR31i.md:3:writer-forbidden-opened-path'
        '.ufo/waves/round-31/w1/CaseR31j.md:4:writer-forbidden-opened-path'
        '.ufo/waves/round-31/w1/CaseR31k.md:3:writer-forbidden-opened-path'
        '.ufo/waves/round-31/w1/CaseR31l.md:1:writer-missing-files-opened-list'
        '.ufo/waves/round-31/w1/CaseR31m.md:2:writer-tool-source-citation'
        '.ufo/waves/round-31/w1/CaseR31m.md:5:writer-tool-run-output'
    )
    tmp_root=${TMPDIR:-/tmp}
    SELFTEST_TMPROOT=$(mktemp -d "$tmp_root/blind-check-selftest.XXXXXX") || { printf 'FAIL\n'; return 1; }
    trap 'rm -rf -- "$SELFTEST_TMPROOT"' EXIT
    repo="$SELFTEST_TMPROOT/repo"; wave='.ufo/waves/round-31/w1'; allow="$SELFTEST_TMPROOT/allow.txt"
    mkdir -p "$repo/$wave" && git -C "$repo" init -q || { printf 'FAIL\n'; return 1; }
    cat > "$allow" <<'EOF'
# one bash glob per line; {report} stands for the brief basename without .md
.ufo/waves/round-31/rule-text.md
/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-31/rule-text.md
/fast/scratch/hyaku/mori-r31/{report}
/fast/scratch/hyaku/mori-r31/{report}/*
https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/*
EOF
    # a: prose after a list closes the block; nothing after it is an entry.
    printf '%s\n' \
        '## Files opened' \
        '- .ufo/waves/round-31/rule-text.md' \
        'Prose after the list names /etc/shadow outside any block.' \
        '## Next' \
        '- /etc/shadow' > "$repo/$wave/CaseR31a.md"
    # b: two forbidden entries in one list, each hit at its own line.
    printf '%s\n' \
        '## Files opened' \
        '- /etc/passwd' \
        '- /etc/shadow' \
        '- .ufo/waves/round-31/rule-text.md' > "$repo/$wave/CaseR31b.md"
    # c: label form opens a block whose entries count (no missing-list hit).
    printf '%s\n' \
        '## Cases' \
        'All cases ran clean.' \
        'Files opened:' \
        '- .ufo/waves/round-31/rule-text.md' > "$repo/$wave/CaseR31c.md"
    # d: label form forbidden entry is hit at its own line.
    printf '%s\n' \
        'Opened files:' \
        '- /etc/passwd' > "$repo/$wave/CaseR31d.md"
    # e: table form; the header row above the separator is not an entry.
    printf '%s\n' \
        '## Files opened' \
        '' \
        '| path | why |' \
        '| --- | --- |' \
        '| .ufo/waves/round-31/rule-text.md | rule |' \
        '| /etc/passwd | probed |' > "$repo/$wave/CaseR31e.md"
    # f: numbered list with both N. and N) markers.
    printf '%s\n' \
        '## Files opened' \
        '1. .ufo/waves/round-31/rule-text.md' \
        '2) /etc/passwd' > "$repo/$wave/CaseR31f.md"
    # g: entry without any path candidate is one forbidden hit and still counts as an entry.
    printf '%s\n' \
        '## Files opened' \
        '- see the notes below' > "$repo/$wave/CaseR31g.md"
    # h: a deeper heading closes the block; a files-opened heading reopens one.
    printf '%s\n' \
        '## Files opened' \
        '- /etc/passwd' \
        '### Deeper' \
        '- /etc/shadow' \
        '## Opened files' \
        '- .ufo/waves/round-31/rule-text.md' > "$repo/$wave/CaseR31h.md"
    # i: own scratch allowed via {report}, other writer's scratch forbidden.
    printf '%s\n' \
        '## Files opened' \
        '- /fast/scratch/hyaku/mori-r31/CaseR31i/out.txt' \
        '- /fast/scratch/hyaku/mori-r31/CaseR31j/out.txt' > "$repo/$wave/CaseR31i.md"
    # j: kernel.org URL allowed by glob, file:// stripped before matching, foreign URL forbidden.
    printf '%s\n' \
        '## Files opened' \
        '- https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/proc_pid_stat.5?h=man-pages-6.20' \
        '- file:///fast/scratch/hyaku/mori-r31/CaseR31j/out.txt' \
        '- https://example.net/elsewhere.txt' > "$repo/$wave/CaseR31j.md"
    # k: backticks, trailing comma and a :L-M suffix are stripped; quoted :L path too.
    printf '%s\n' \
        '## Files opened' \
        '- `.ufo/waves/round-31/rule-text.md:10-12`,' \
        '- "/etc/passwd:42"' > "$repo/$wave/CaseR31k.md"
    # l: no files-opened block at all is one missing-list hit at line 1.
    printf '%s\n' \
        '## Cases' \
        'Nothing was opened here.' > "$repo/$wave/CaseR31l.md"
    # m: the two round-30 detectors stay live on unprotected lines.
    printf '%s\n' \
        '## Cases' \
        'See tools/mori-oom-killers.py:42.' \
        'Tool run output:' \
        'KILLERS_QUIET' \
        'exit 0' \
        '## Files opened' \
        '- .ufo/waves/round-31/rule-text.md' > "$repo/$wave/CaseR31m.md"
    # n: json fence in a Cases section and derivation table rows stay protected.
    printf '%s\n' \
        '## Cases' \
        '```json' \
        '{"expect":{"verdict":"KILLER_ACTED","exit":1},"marker":"MORI_OOM_KILLERS_SELFTEST: PASS"}' \
        '```' \
        '## Per-case derivation table' \
        '| verdict | KILLERS_QUIET | exit 0 |' \
        '| marker | MORI_OOM_KILLERS_SELFTEST: PASS |' \
        '## Files opened' \
        '- .ufo/waves/round-31/rule-text.md' > "$repo/$wave/CaseR31n.md"
    git -C "$repo" add "$wave" && git -C "$repo" -c user.name=BlindCheck -c user.email=blind@example.invalid commit -q -m synthetic || { printf 'FAIL\n'; return 1; }
    synthetic_rev=$(git -C "$repo" rev-parse HEAD) || { printf 'FAIL\n'; return 1; }
    if output=$(run_gate "$repo" "$synthetic_rev" "$wave" '^CaseR31[a-z]\.md$' "$allow" 2>&1); then status=0; else status=$?; fi
    first=${output%%$'\n'*}; rest=${output#*$'\n'}; second=${rest%%$'\n'*}; records=${rest#*$'\n'}
    if [[ $first != 'scanned=14' || $second != 'blind_violations=13' || $status != 1 ]]; then printf 'FAIL %s %s %s\n' "$first" "$second" "$status"; return 1; fi
    while IFS= read -r line; do
        if [[ ${expected[i]-} != "$line" ]]; then printf 'FAIL got %s want %s\n' "$line" "${expected[i]-}"; return 1; fi
        (( i += 1 ))
    done <<< "$records"
    (( i == ${#expected[@]} )) || { printf 'FAIL count %d\n' "$i"; return 1; }
    if output=$(run_gate "$repo" "$synthetic_rev" "$wave" '^WrittenByNobody[0-9]*\.md$' "$allow" 2>&1); then status=0; else status=$?; fi
    if [[ $output != $'scanned=0\nblind_violations=0' || $status != 0 ]]; then printf 'FAIL zero %s %s\n' "$output" "$status"; return 1; fi
    run_gate "$repo" "$synthetic_rev" "$wave" '^CaseR31[a-z]\.md$' "$SELFTEST_TMPROOT/absent-allow.txt" >/dev/null 2>&1
    [[ $? == 2 ]] || { printf 'FAIL missing allow file\n'; return 1; }
    run_gate "$repo" '' "$wave" '^CaseR31[a-z]\.md$' "$allow" >/dev/null 2>&1
    [[ $? == 2 ]] || { printf 'FAIL usage error\n'; return 1; }
    printf 'PASS\n'
}

if [[ ${1-} == --selftest ]]; then
    (( $# == 1 )) || { usage; exit 2; }
    selftest
    exit $?
fi
if (( $# != 4 )); then usage; exit 2; fi
repo_root=$(git rev-parse --show-toplevel 2>/dev/null) || { fail 'not inside a Git worktree'; exit 2; }
run_gate "$repo_root" "$1" "$2" "$3" "$4"
```
