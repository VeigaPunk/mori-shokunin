# FixBlindGate

Files changed: `/fast/scratch/hyaku/mori-r30/FixBlindGate/check-blind-wave.sh`; `.ufo/waves/round-30/w1/FixBlindGate.md`.
Behavior: scans only matching writer reports; enforces the Round-30 allowlist, files-opened entries, source citations, and tool-output markers; `--selftest` checks planted classes and the exact round-29 report set.

```bash
#!/usr/bin/env bash
set -o nounset -o pipefail
set -f
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE

usage() {
    printf 'usage: check-blind-wave.sh <lane-rev> <wave-report-dir> <writer-name-regex> | --selftest\n' >&2
}

fail() { printf 'blind check: %s\n' "$1" >&2; return 2; }

# ROUND-30 ALLOWLIST (Amendment A2): only rule-text, own r30 scratch, and named HTTPS sources pass.
round30_path_allowed() {
    local candidate=$1 normalized=$1
    case $candidate in
        https://raw.githubusercontent.com/rfjakob/earlyoom/*|https://github.com/rfjakob/earlyoom/*|https://raw.githubusercontent.com/systemd/systemd/*|https://github.com/systemd/systemd/*|https://www.freedesktop.org/software/systemd/*) return 0 ;;
        file://*) candidate=${candidate#file://}; normalized=$candidate ;;
    esac
    while [[ $normalized == ./* ]]; do normalized=${normalized#./}; done
    [[ $normalized == "$rule_rel" || $normalized == "$rule_abs" || $normalized == "$own_scratch" || $normalized == "$own_scratch/"* ]]
}
# END ROUND-30 ALLOWLIST

inspect_entry_line() {
    local line=$1 token candidate last trimmed_line has_candidate=0
    entry_has_path=0; entry_forbidden=0
    trimmed_line=${line#"${line%%[![:space:]]*}"}
    case $trimmed_line in '- '*|'* '*|'+ '*|'|'*|[0-9]*) entry_has_path=1 ;; esac
    for token in $line; do
        candidate=$token
        while [[ ${candidate:0:1} == '`' || ${candidate:0:1} == '"' || ${candidate:0:1} == "'" || ${candidate:0:1} == '(' || ${candidate:0:1} == '[' || ${candidate:0:1} == '{' || ${candidate:0:1} == '<' ]]; do candidate=${candidate:1}; done
        while [[ -n $candidate ]]; do
            last=${candidate: -1}
            case $last in '`'|'"'|"'"|')'|']'|'}'|'>'|','|';'|'.') candidate=${candidate:0:${#candidate}-1} ;; *) break ;; esac
        done
        [[ -z $candidate ]] && continue
        if [[ $candidate == *://* ]]; then
            entry_has_path=1; has_candidate=1
            round30_path_allowed "$candidate" || entry_forbidden=1
            continue
        fi
        if [[ $candidate =~ ^(.+):[0-9]+([:-][0-9]+)?$ ]]; then candidate=${BASH_REMATCH[1]}; fi
        if [[ $candidate == *'/'* || $candidate == *.* || $candidate == LOG.md || $candidate == SCORECARD.md || $candidate == SKILL.md || $candidate == PROVINCE.md ]]; then
            entry_has_path=1; has_candidate=1
            round30_path_allowed "$candidate" || entry_forbidden=1
        fi
    done
    if (( entry_has_path && ! has_candidate )); then entry_forbidden=1; fi
}

run_gate() {
    local repo_root=$1 revision=$2 wave_dir=$3 writer_re=$4 resolved_rev path relative base content
    local line lower_line trimmed_line line_no in_case_json in_case_section in_derivation in_files_list files_h2_active
    local files_entry_seen files_forbidden_line files_forbidden_seen
    local own_scratch pending_inputs pending_tool seen_run_verdict
    local has_verdict has_exit output_marker protected
    local -a tree_paths=()
    local scanned=0 violations=0
    local -a violation_lines=()
    while [[ $wave_dir == ./* ]]; do wave_dir=${wave_dir#./}; done
    while [[ $wave_dir == */ ]]; do wave_dir=${wave_dir%/}; done
    if [[ -z $revision || -z $wave_dir || -z $writer_re || $wave_dir == /* || $wave_dir == . || $wave_dir == .. || $wave_dir == *'/../'* || $wave_dir == ../* || $wave_dir == */.. || $wave_dir == *:* ]]; then
        usage; return 2
    fi
    resolved_rev=$(git -C "$repo_root" rev-parse --verify --quiet --end-of-options "${revision}^{commit}" 2>/dev/null) || { fail 'invalid lane revision'; return 2; }
    if [[ $(git -C "$repo_root" cat-file -t "$resolved_rev:$wave_dir" 2>/dev/null) != tree ]]; then
        fail 'report directory is absent at revision'; return 2
    fi
    grep -E -q -- "$writer_re" /dev/null 2>/dev/null
    local regex_status=$?
    if (( regex_status > 1 )); then fail 'invalid writer-name regex'; return 2; fi
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
    local rule_rel='.ufo/waves/round-30/rule-text.md'
    local rule_abs="$repo_root/$rule_rel"
    for path in "${tree_paths[@]}"; do
        relative=${path#"$wave_dir"/}
        [[ $relative == */* || $relative != *.md ]] && continue
        base=${path##*/}
        [[ $base =~ $writer_re ]] || continue
        content=$(git -C "$repo_root" show "$resolved_rev:$path") || { fail 'unable to read committed report'; return 2; }
        local report_base=${base%.md}
        own_scratch="/fast/scratch/hyaku/mori-r30/$report_base"
        ((scanned += 1))
        line_no=0; in_case_json=0; in_case_section=0; in_derivation=0; in_files_list=0; files_h2_active=0
        files_entry_seen=0; files_forbidden_seen=0; files_forbidden_line=0
        pending_inputs=0; pending_tool=0; seen_run_verdict=0
        while IFS= read -r line || [[ -n $line ]]; do
            ((line_no += 1))
            lower_line=${line,,}
            trimmed_line=${line#"${line%%[![:space:]]*}"}
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
                if [[ $lower_line =~ files.*opened || $lower_line =~ opened.*files ]]; then in_files_list=1; files_h2_active=1; else in_files_list=0; files_h2_active=0; fi
            elif [[ $lower_line =~ ^[[:space:]]*(files[[:space:]]+opened|opened[[:space:]]+files)[[:space:]]*: ]]; then
                in_files_list=1; files_h2_active=0
            fi
            if (( in_derivation )) && [[ $trimmed_line == '|'* ]]; then protected=1; fi

            if [[ $lower_line =~ $cite_file_re || $lower_line =~ $tool_header_re ]]; then
                ((violations += 1)); violation_lines+=("$path:$line_no:writer-tool-source-citation")
            fi

            if (( in_files_list )); then
                if [[ -n ${line//[[:space:]]/} && ! $line =~ ^[[:space:]]*#{1,6}[[:space:]] ]]; then
                    inspect_entry_line "$line"
                    if (( entry_has_path && files_h2_active )); then files_entry_seen=1; fi
                    if (( entry_forbidden )) && (( ! files_forbidden_seen )); then
                        files_forbidden_seen=1; files_forbidden_line=$line_no
                    fi
                fi
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
        if (( ! files_entry_seen )); then
            ((violations += 1)); violation_lines+=("$path:1:writer-missing-files-opened-list")
        fi
        if (( files_forbidden_seen )); then
            ((violations += 1)); violation_lines+=("$path:$files_forbidden_line:writer-forbidden-opened-path")
        fi
    done
    printf 'scanned=%d\nblind_violations=%d\n' "$scanned" "$violations"
    if (( violations > 0 )); then printf '%s\n' "${violation_lines[@]}"; return 1; fi
    return 0
}

SELFTEST_TMPROOT=
selftest() {
    local tmp_root repo wave lane_root output status first rest second records line path_line rule file pair wanted found hit hits=0 matches
    local a=0 b=0 c=0 d=0 metadata=0
    local -a expected_pairs=(
        'CaseA207a.md|writer-forbidden-opened-path' 'CaseA207b.md|writer-forbidden-opened-path'
        'CaseA207c.md|writer-forbidden-opened-path' 'CaseA207d.md|writer-forbidden-opened-path'
        'CaseA210a.md|writer-forbidden-opened-path' 'CaseA210b.md|writer-forbidden-opened-path'
        'CaseA210c.md|writer-missing-files-opened-list' 'CaseA210c.md|writer-forbidden-opened-path'
        'CaseA210d.md|writer-forbidden-opened-path'
    )
    local -a false_hits=(
        'AxisOperability.md:19' 'BuildTipReceipts.md:5' 'BuildTipReceipts.md:135' 'BuildTipReceipts.md:136' 'BuildTipReceipts.md:137' 'BuildTipReceipts.md:140'
        'DraftQualityCriteria.md:75' 'DraftQualityCriteria.md:76' 'DraftQualityCriteria.md:77' 'DraftQualityCriteria.md:86'
        'ReviewLateMutCountC1Amended.md:78' 'ReviewLateMutHeadingCheck.md:37' 'ReviewLateMutHeadingCheck.md:39'
        'CaseA207a.md:1' 'CaseA207b.md:1' 'CaseA207c.md:1' 'CaseA207d.md:1' 'CaseA210a.md:1' 'CaseA210b.md:1' 'CaseA210d.md:1'
    )
    local -a actual_pairs=()
    lane_root=$(git rev-parse --show-toplevel 2>/dev/null) || { printf 'FAIL\n'; return 1; }
    tmp_root=${TMPDIR:-/tmp}
    SELFTEST_TMPROOT=$(mktemp -d "$tmp_root/blind-gate-selftest.XXXXXX") || { printf 'FAIL\n'; return 1; }
    trap 'rm -rf -- "$SELFTEST_TMPROOT"' EXIT
    repo="$SELFTEST_TMPROOT/repo"; wave='.ufo/waves/round-30/w1'
    mkdir -p "$repo/$wave" && git -C "$repo" init -q || { printf 'FAIL\n'; return 1; }
    printf '%s\n' '## Files opened' '- .ufo/waves/round-30/rule-text.md' '## Source note' 'See tools/mori-oom-killers.py:42.' > "$repo/$wave/CaseR30a.md"
    printf '%s\n' '## Files opened' '- .ufo/waves/round-30/rule-text.md' '## Run note' 'Tool run output:' 'KILLERS_QUIET' 'exit 0' 'MORI_OOM_KILLERS_SELFTEST: FAIL 0/1' '--inputs sample.json => KILLERS_UNKNOWN exit 2' > "$repo/$wave/CaseR30b.md"
    printf '%s\n' '## Cases' 'No files list.' > "$repo/$wave/CaseR30c.md"
    printf '%s\n' '## Files opened' '- tools/fixtures/mori-oom-killers/cases.json' > "$repo/$wave/CaseR30d.md"
    printf '%s\n' '## Files opened' '- .ufo/waves/round-30/rule-text.md' '## Metadata' '```json' '{"marker":"MORI_OOM_KILLERS_SELFTEST: FAIL"}' '```' > "$repo/$wave/CaseR30e.md"
    printf '%s\n' '## Cases' '```json' '{"expect":{"verdict":"KILLER_ACTED","exit":1},"marker":"MORI_OOM_KILLERS_SELFTEST: PASS"}' '```' '## Per-case derivation table' '| verdict | KILLERS_QUIET | exit 0 |' '| marker | MORI_OOM_KILLERS_SELFTEST: PASS |' '## Files opened' '- .ufo/waves/round-30/rule-text.md' '- /fast/scratch/hyaku/mori-r30/CaseR30z/input.json' '- https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c' > "$repo/$wave/CaseR30z.md"
    printf '%s\n' 'Tool lines 10-12' 'MORI_OOM_KILLERS_SELFTEST: FAIL' '## Files opened' '- tools/fixtures/mori-oom-killers/cases.json' > "$repo/$wave/NotWriter.md"
    git -C "$repo" add "$wave" && git -C "$repo" -c user.name=BlindGate -c user.email=blind@example.invalid commit -q -m synthetic || { printf 'FAIL\n'; return 1; }
    local synthetic_rev
    synthetic_rev=$(git -C "$repo" rev-parse HEAD) || { printf 'FAIL\n'; return 1; }
    if output=$(run_gate "$repo" "$synthetic_rev" "$wave" '^CaseR30[a-z]\.md$' 2>&1); then status=0; else status=$?; fi
    first=${output%%$'\n'*}; rest=${output#*$'\n'}; second=${rest%%$'\n'*}; records=${rest#*$'\n'}
    if [[ $first != scanned=6 || $second != blind_violations=* || $status != 1 ]]; then printf 'FAIL\n'; return 1; fi
    while IFS= read -r line; do
        [[ $line == *:writer-tool-source-citation ]] && a=1
        [[ $line == *:writer-tool-run-output ]] && b=1
        [[ $line == *:writer-missing-files-opened-list ]] && c=1
        [[ $line == *:writer-forbidden-opened-path ]] && d=1
        [[ $line == *CaseR30e.md:*:writer-tool-run-output ]] && metadata=1
        [[ $line == *CaseR30z.md:* || $line == *NotWriter.md:* ]] && { printf 'FAIL\n'; return 1; }
    done <<< "$records"
    (( a && b && c && d && metadata )) || { printf 'FAIL\n'; return 1; }

    # Exact round-29 (file, rule) set: those briefs allowed old lane reads; A210c also lacks an H2 list.
    if output=$(run_gate "$lane_root" d6d5cb0a .ufo/waves/round-29/w1 '^CaseA2(07|10)[a-d]\.md$' 2>&1); then status=0; else status=$?; fi
    first=${output%%$'\n'*}; rest=${output#*$'\n'}; second=${rest%%$'\n'*}; records=${rest#*$'\n'}
    if [[ $first != scanned=8 || $second != blind_violations=9 || $status != 1 ]]; then printf 'FAIL\n'; return 1; fi
    while IFS= read -r line; do
        path_line=${line%:*}; rule=${line##*:}; file=${path_line##*/}; file=${file%%:*}; pair="$file|$rule"; found=0
        for wanted in "${expected_pairs[@]}"; do [[ $pair == "$wanted" ]] && found=1; done
        (( found )) || { printf 'FAIL\n'; return 1; }
        for hit in "${false_hits[@]}"; do [[ $path_line == *"/$hit" ]] && { printf 'FAIL\n'; return 1; }; done
        actual_pairs+=("$pair"); ((hits += 1))
    done <<< "$records"
    (( hits == ${#expected_pairs[@]} )) || { printf 'FAIL\n'; return 1; }
    for wanted in "${expected_pairs[@]}"; do
        matches=0; for pair in "${actual_pairs[@]}"; do [[ $pair == "$wanted" ]] && ((matches += 1)); done
        (( matches == 1 )) || { printf 'FAIL\n'; return 1; }
    done
    printf 'PASS\n'
}

if [[ ${1-} == --selftest ]]; then
    (( $# == 1 )) || { usage; exit 2; }
    selftest
    exit $?
fi
if (( $# != 3 )); then usage; exit 2; fi
repo_root=$(git rev-parse --show-toplevel 2>/dev/null) || { fail 'not inside a Git worktree'; exit 2; }
run_gate "$repo_root" "$1" "$2" "$3"
```

SHA-256: `99e7ec038650f67d7e023b6bcb6cf20f98516d18ed953b0601228430ff4ce09b` (237 lines, executable).
Observed: temporary Git blob `19076d4beb1e5d49798fee0dfd1048aa24f92ba2` ran via process substitution: selftest `PASS`; d6d5cb0a: `scanned=8`, `blind_violations=9`, exit 1. A mutant disabling (d) printed `FAIL`, exit 1.
Round-29 findings: forbidden-path (d) at CaseA207a.md:196, CaseA207b.md:197, CaseA207c.md:194, CaseA207d.md:198, CaseA210a.md:205, CaseA210b.md:197, CaseA210c.md:196, CaseA210d.md:184; missing H2 (c) at CaseA210c.md:1. The selftest compares this exact report/rule set and excludes all 20 adjudicated false-positive file:line pairs.
Risk/blocker: no lane implementation files changed; L1 must integrate the scratch script and run the committed freeze blob against the Round-30 wave. No tools were installed or updated.
