#!/usr/bin/env bash
# Run the frozen round-39 `conform.py --selftest` without writing into the lane.
# The instrument hardcodes the lane path (`.ufo/waves/round-39/conform.py:53-54`) and makes its selftest work dirs
# under <lane>/.ufo/waves/round-39/scratch (`:491-492`), whatever TMPDIR says. This wrapper reads that path from the
# instrument, clones the lane (--no-local, read-only on the source) into a throwaway dir under $TMPDIR, checks the
# clone out at <rev>, and bind-mounts the clone over the hardcoded path (bubblewrap), so every write lands in the
# clone, which is removed on exit. Run it from a checkout or `git archive` of the lane (cwd = lane root).
# Usage: bash .ufo/waves/round-52/r39-conform-selftest.sh <rev> --selftest
set -euo pipefail
rev=${1:?usage: r39-conform-selftest.sh <rev> --selftest}
[ "${2:-}" = --selftest ] || { echo "usage: r39-conform-selftest.sh <rev> --selftest" >&2; exit 2; }
lane=$(sed -n 's/^LANE = "\(.*\)"$/\1/p' .ufo/waves/round-39/conform.py)
[ -n "$lane" ] && [ -d "$lane/.git" ] || { echo "r39-conform-selftest: hardcoded lane path not found" >&2; exit 2; }
s=$(mktemp -d "${TMPDIR:-/var/tmp}/r39-conform.XXXXXX")
trap 'rm -rf -- "$s"' EXIT
git clone -q --no-local "$lane" "$s/lane"
git -C "$s/lane" checkout -q --detach "$rev"
bwrap --dev-bind / / --bind "$s/lane" "$lane" --chdir "$lane" \
  env PYTHONDONTWRITEBYTECODE=1 python3 "$lane/.ufo/waves/round-39/conform.py" "$rev" --selftest
