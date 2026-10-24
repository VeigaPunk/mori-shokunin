#!/usr/bin/env bash
set -o nounset -o pipefail

usage() {
    printf 'usage: %s <lane-rev> <wave-report-dir> <writer-name-regex>\n' "${0##*/}" >&2
}

if (( $# != 3 )); then
    usage
    exit 2
fi

revision=$1
wave_dir=$2
writer_re=$3
while [[ $wave_dir == ./* ]]; do wave_dir=${wave_dir#./}; done
while [[ $wave_dir == */ ]]; do wave_dir=${wave_dir%/}; done

if [[ -z $revision || -z $wave_dir || -z $writer_re || $wave_dir == /* || $wave_dir == . || $wave_dir == .. || $wave_dir == *'/../'* || $wave_dir == ../* || $wave_dir == */.. || $wave_dir == *:* ]]; then
    usage
    exit 2
fi

repo_root=$(git rev-parse --show-toplevel 2>/dev/null) || {
    printf 'blind check: not inside a Git worktree\n' >&2
    exit 2
}
resolved_rev=$(git -C "$repo_root" rev-parse --verify --quiet --end-of-options "${revision}^{commit}" 2>/dev/null) || {
    printf 'blind check: invalid lane revision\n' >&2
    exit 2
}
if [[ $(git -C "$repo_root" cat-file -t "$resolved_rev:$wave_dir" 2>/dev/null) != tree ]]; then
    printf 'blind check: report directory is absent at revision\n' >&2
    exit 2
fi

grep -E -q -- "$writer_re" /dev/null 2>/dev/null
regex_status=$?
if (( regex_status > 1 )); then
    printf 'blind check: invalid writer-name regex\n' >&2
    exit 2
fi

mapfile -d '' -t tree_paths < <(git -C "$repo_root" ls-tree -rz --name-only "$resolved_rev" -- "$wave_dir")
report_paths=()
for path in "${tree_paths[@]}"; do
    relative=${path#"$wave_dir"/}
    [[ $relative == */* ]] && continue
    [[ $relative == *.md ]] && report_paths+=("$path")
done

# Construct sensitive markers in pieces so this source can be quoted in a clean report.
tool_file='mori-oom-killers''.''py'
tool_header='tool'' lines'
selftest_marker='MORI_OOM_KILLERS_''SELFTEST:'
quiet_marker='KILLERS_''QUIET'
input_flag='--''inputs'

files_header_re='^[[:space:]]*[*_#[:space:]]*(files([[:space:]]+(i[[:space:]]+)?)?(opened|read|accessed|consulted)|opened[[:space:]]+files)([[:space:]]*\([^)]*\))?[*_#[:space:]:]*$'
report_ref_re='(^|[[:space:]`(])(([^[:space:]`(]*/)?w[12]/[^[:space:]`),;]+[.]md)'
cite_file_re='mori-oom-killers[.]py([[:space:]]*:[[:space:]]*|[[:space:]]+(lines?[[:space:]]+)?)[0-9]+([[:space:]]*[-–][[:space:]]*[0-9]+)?'
cite_tool_re='(^|[^[:alnum:]_])tool[[:space:]]*:[[:space:]]*[0-9]+([[:space:]]*[-–][[:space:]]*[0-9]+)?'
result_re='(KILLER_ACTED|KILLERS_QUIET|KILLERS_UNKNOWN|exit[[:space:]]+[012])'
repro_id_re='(^|[^[:alnum:]_])([rReE][0-9]+[[:alnum:]_-]*|observed:|run[[:space:]]+[eE][0-9]+)'

violations=0
violation_lines=()
emit_violation() {
    local file=$1 line=$2 kind=$3
    ((violations += 1))
    violation_lines+=("$file:$line:$kind")
}

for path in "${report_paths[@]}"; do
    base=${path##*/}
    content=$(git -C "$repo_root" show "$resolved_rev:$path") || {
        printf 'blind check: unable to read committed report\n' >&2
        exit 2
    }
    is_writer=0
    if [[ $base =~ $writer_re ]]; then is_writer=1; fi
    line_no=0
    files_list_seen=0
    in_files_list=0
    list_has_content=0
    lower_line=
    while IFS= read -r line || [[ -n $line ]]; do
        ((line_no += 1))
        lower_line=${line,,}

        if (( ! is_writer )); then
            if [[ $line =~ $cite_file_re || $line =~ $cite_tool_re || $lower_line == *"$tool_header"* ]]; then
                emit_violation "$path" "$line_no" 'nonwriter-tool-citation'
            fi
            if [[ $line == *"$selftest_marker"* ]]; then
                after_marker=${line#*"$selftest_marker"}
                if [[ ! $after_marker =~ ^[[:space:]]+PASS[[:space:]]+(30/30|32/32)([[:space:]]|$) ]]; then
                    emit_violation "$path" "$line_no" 'nonwriter-tool-run-output'
                fi
            fi
            if [[ $line == *"$quiet_marker"* ]]; then
                after_marker=${line#*"$quiet_marker"}
                if [[ $after_marker =~ ^[[:space:]]+exit[[:space:]]+[0-9]+ ]]; then
                    emit_violation "$path" "$line_no" 'nonwriter-tool-run-output'
                fi
            fi
            if [[ $line == *"$input_flag"* ]] && [[ $line =~ $result_re ]]; then
                emit_violation "$path" "$line_no" 'nonwriter-tool-run-output'
            elif [[ $line =~ $repro_id_re && $line =~ $result_re ]]; then
                emit_violation "$path" "$line_no" 'nonwriter-tool-run-output'
            fi
            continue
        fi

        if [[ $lower_line =~ $files_header_re ]]; then
            files_list_seen=1
            in_files_list=1
            list_has_content=0
            continue
        fi
        if (( in_files_list )); then
            if [[ -z $line ]]; then
                if (( list_has_content )); then in_files_list=0; fi
                continue
            fi
            if [[ $line =~ ^[[:space:]]*#{1,6}[[:space:]] ]]; then
                in_files_list=0
                continue
            fi
            list_has_content=1
            forbidden=0
            if [[ $line == *"$tool_file"* || $line == *'corpus/lessons/'* ]]; then
                forbidden=1
            fi
            own_path="$wave_dir/$base"
            own_round=${wave_dir#*/waves/}
            own_wave=${wave_dir##*/}
            remaining=$line
            while [[ $remaining =~ $report_ref_re ]]; do
                candidate=${BASH_REMATCH[2]}
                while [[ $candidate == ./* ]]; do candidate=${candidate#./}; done
                if [[ $candidate != "$own_path" && $candidate != "$own_round/$base" && $candidate != "$own_wave/$base" && $candidate != *"/$own_path" ]]; then
                    forbidden=1
                fi
                matched=${BASH_REMATCH[0]}
                remaining=${remaining#*"$matched"}
            done
            if (( forbidden )); then
                emit_violation "$path" "$line_no" 'writer-forbidden-opened-path'
            fi
        fi
    done <<< "$content"
    if (( is_writer && ! files_list_seen )); then
        emit_violation "$path" 1 'writer-missing-files-opened-list'
    fi
done

printf 'blind_violations=%d\n' "$violations"
if (( violations > 0 )); then printf '%s\n' "${violation_lines[@]}"; fi
if (( violations == 0 )); then exit 0; else exit 1; fi
