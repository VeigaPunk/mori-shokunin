#!/usr/bin/env bash
set -u

usage() {
  printf 'usage: %s <parent-rev> <out-dir>\n' "${0##*/}" >&2
}

if [ "$#" -ne 2 ]; then
  usage
  exit 2
fi

repo=/home/vgpnk/Projects/shokunin/mori-shokunin
parent_arg=$1
out_arg=$2
fleet_rev=63729047644f839fe4c8cc97abd0d8bf741a5787

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P) || exit 2
if ! mkdir -p -- "$out_arg"; then
  printf 'cannot create output directory: %s\n' "$out_arg" >&2
  exit 2
fi
out_dir=$(cd -- "$out_arg" && pwd -P) || exit 2
work=$(mktemp -d -- "$script_dir/.tip-receipts.XXXXXXXX") || {
  printf 'cannot create sandbox under %s\n' "$script_dir" >&2
  exit 2
}
trap 'rm -rf -- "$work"' EXIT

unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE
git_cmd=(env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git)
clone=$work/repo
if ! "${git_cmd[@]}" clone --no-hardlinks "$repo" "$clone" >/dev/null 2>&1; then
  printf 'sandbox clone failed\n' >&2
  exit 2
fi
parent=$("${git_cmd[@]}" -C "$clone" rev-parse --verify --quiet "${parent_arg}^{commit}") || {
  printf 'invalid parent revision: %s\n' "$parent_arg" >&2
  exit 2
}
if [[ ! $parent =~ ^[0-9a-f]{40}$ ]]; then
  printf 'resolved parent is not a full 40-hex commit: %s\n' "$parent" >&2
  exit 2
fi
if ! "${git_cmd[@]}" -C "$clone" checkout --quiet --detach "$parent"; then
  printf 'cannot check out parent: %s\n' "$parent" >&2
  exit 2
fi

header="# measured at parent $parent; the landed tip adds only receipt files under .ufo/waves/round-29/evidence/"

write_receipt() {
  local name=$1 command=$2 captured=$3 status=$4
  {
    printf '%s\n' "$header"
    printf 'command: %s\n' "$command"
    if [ -s "$captured" ]; then
      cat -- "$captured"
      printf '\n'
    fi
    printf 'exit: %s\n' "$status"
  } > "$out_dir/$name" || return 1
}

run_counter() {
  local name=$1 script=$2 captured=$3 command=$4 extra_arg=${5-}
  local status
  if ! "${git_cmd[@]}" -C "$clone" cat-file -e "$parent:$script" 2>/dev/null; then
    printf 'counter absent at %s\n' "$parent" > "$captured"
    status=2
  else
    if [ -n "$extra_arg" ]; then
      (cd -- "$clone" && bash "$script" "$parent" "$extra_arg") > "$captured" 2>&1
    else
      (cd -- "$clone" && bash "$script" "$parent") > "$captured" 2>&1
    fi
    status=$?
  fi
  if ! write_receipt "$name" "$command" "$captured" "$status"; then
    printf 'cannot write receipt: %s/%s\n' "$out_dir" "$name" >&2
    return 2
  fi
  printf 'wrote %s (exit %s)\n' "$out_dir/$name" "$status"
}

c1_script=.ufo/waves/round-29/count-c1.sh
c1_command="bash $c1_script $parent $fleet_rev"
if ! run_counter tip-c1.txt "$c1_script" "$work/c1-output" "$c1_command" "$fleet_rev"; then
  exit 2
fi

c2_script=.ufo/waves/round-29/count-c2.sh
c2_command="bash $c2_script $parent"
if ! run_counter tip-c2.txt "$c2_script" "$work/c2-output" "$c2_command"; then
  exit 2
fi

retention_command="python3 -I -B tools/mori-retention-gate.py scan --repo $clone --rev $parent --policy .ufo/waves/round-18/frozen/c1-policy.json --allowlist corpus/evidence/retention-allowlist.json"
(cd -- "$clone" && python3 -I -B tools/mori-retention-gate.py scan --repo "$clone" --rev "$parent" --policy .ufo/waves/round-18/frozen/c1-policy.json --allowlist corpus/evidence/retention-allowlist.json) > "$work/retention-output" 2>&1
retention_status=$?
if ! write_receipt tip-retention.txt "$retention_command" "$work/retention-output" "$retention_status"; then
  printf 'cannot write receipt: %s/tip-retention.txt\n' "$out_dir" >&2
  exit 2
fi
printf 'wrote %s (exit %s)\n' "$out_dir/tip-retention.txt" "$retention_status"

# Exit 0 means all three receipts were written; each measured command's actual status is recorded in its receipt.
exit 0
