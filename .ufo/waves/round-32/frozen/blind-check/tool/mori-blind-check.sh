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
