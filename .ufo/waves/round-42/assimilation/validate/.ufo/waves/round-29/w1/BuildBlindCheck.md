# BuildBlindCheck — round-28 M6 writer-blindness check

## Delivery and evidence

The checker is `/fast/scratch/hyaku/mori-r29/BuildBlindCheck/check-blind-wave.sh`; its SHA-256 is `b0573035ca4f16b8df48d97a074483bcffe1ff92746a3c7046418af29a5d6e0f` (`sha256sum` output). The M6 lesson evidence is `corpus/lessons/round-28.md:143-146`.

The supplied revision `06d6a5b8` did not resolve in the lane (`git cat-file -t 06d6a5b8` reported an invalid object name). I used `84abe93e6cde117b0bc86c46e163467596fa19a6`, the earliest complete wave-1 report tree found: report-path counts were 28 at `1c4c186e`, 30 at `f2de0eed`, 31 at `6b695b02`, and 32 at `84abe93e`. The diff from `6b695b02` to `84abe93e` adds `BuildCountC2.md` and modifies `MutCountC1.md` in that directory.

Observed falsifier, run from the lane repository:

```text
bash /fast/scratch/hyaku/mori-r29/BuildBlindCheck/check-blind-wave.sh 84abe93e6cde117b0bc86c46e163467596fa19a6 .ufo/waves/round-28/w1 '^CaseA2r'
blind_violations=38
exit 1
```

Violation locations (file and line numbers only; no matched text):

- `.ufo/waves/round-28/w1/BuildCountC2.md:23,144,214,223,232,233`
- `.ufo/waves/round-28/w1/CaseA2r03.md:187`
- `.ufo/waves/round-28/w1/CaseA2r06.md:1`
- `.ufo/waves/round-28/w1/CaseA2r10.md:1`
- `.ufo/waves/round-28/w1/CriticC2Design.md:39,40,64,66,68,71,79,85,86,90,92,172,193`
- `.ufo/waves/round-28/w1/ReviewA2SpecVsTool.md:13,15,16,18,19,20,21,22,23,48,49,58`
- `.ufo/waves/round-28/w1/ReviewQ80AtR27Tip.md:136`
- `.ufo/waves/round-28/w1/SupersedeS096.md:184`
- `.ufo/waves/round-28/w1/SupersedeS129.md:186`
- `.ufo/waves/round-28/w1/SupersedeS131.md:127`

Synthetic clean-clone run (the clone contains only synthetic fixture reports):

```text
bash /fast/scratch/hyaku/mori-r29/BuildBlindCheck/check-blind-wave.sh HEAD .ufo/waves/synthetic/w1 '^CaseA2r'
blind_violations=0
exit 0
```
The clone was then amended with this report as a committed non-writer fixture and rerun: `blind_violations=0`, exit 0.

No tool was installed or updated. The checks were the requested historical falsifier and synthetic clean-clone checks. No source tool was opened, copied, or run.

## Risks and blockers

The checker considers direct-child Markdown reports only, accepts a finite set of files-opened headings, and pins the two permitted older self-test tallies in its source. An unusual report extension/heading or changed older tally would need explicit checker adjustment. No blocker remains.

## Checker source

```bash
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
```
