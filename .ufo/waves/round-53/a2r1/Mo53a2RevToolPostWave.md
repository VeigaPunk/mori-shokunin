# Mo53a2RevToolPostWave — post-wave tool review

Reviewed `tools/mori-commit-runway.py` and `tools/fixtures/mori-commit-runway/cases.json` from archived commit `34d97cd3eaea8c13b0f065afc52aac1e5cf518a5`. `git diff fd86307ad54c13edb8b6dd13182a2ad196f42fcd 34d97cd3eaea8c13b0f065afc52aac1e5cf518a5 --stat -- tools/` produced no diff: this revision carries the salvage’s post-wave tool files unchanged. The requested diff from `2a4213bf8da72f7cd78189baa5bb9be825dca1df` adds the bounded-read/strict parsing/case-id guards and three UNKNOWN fixtures; the fixture note accurately says REF accepts the three inputs, so these are additional tool input restrictions, not REF cases.

## Observed checks

- `export TMPDIR=/fast/scratch/hyaku/mori-r53/Mo53a2RevToolPostWave/tmp; python3 -I -B tools/mori-commit-runway.py --selftest` → exit 0; `MATCHER: rejected 26/26 corrupted expectations` and `MORI_COMMIT_RUNWAY_SELFTEST: PASS 31/31`.
- `python3 -I -B tools/mori-commit-runway.py` on this host → exit 0, JSON verdict `COMMIT_HEURISTIC`, mode 0, 32 present CPUs; no error. This is a host observation, not a general correctness claim.
- The isolated live command was run under `strace -f -e trace=open,openat,creat,write,pwrite64,rename,unlink,mkdir,rmdir`. The filtered trace had `WRITE_CANDIDATES 0`; the command exited 0. This checks the live-read path, not selftest (which intentionally writes temporary fixtures).
- Scratch-created hostile probes through the archived executable, each with a 5-second timeout: FIFO meminfo → exit 2, `not a regular file`; 1 MiB + 1 byte meminfo → exit 2, `larger than 1048576 bytes`; non-ASCII Arabic-Indic digits in MemTotal → exit 2, `not ASCII`; overlapping CPU list `0-2,1-3` → exit 2, `not ascending and disjoint`; `--page-kb 0` and `--page-kb 1025` → exit 2, each reports the `1..1024` bound; symlink loop as meminfo → exit 2, `unreadable (Too many levels of symbolic links)`. The selftest’s hostile checks additionally passed for directory-as-meminfo and traversal-ID refusal.

The guards match the implementation: `_read` opens nonblocking, checks `fstat` regular-file status, reads in bounded chunks, then ASCII-decodes; numeric patterns use ASCII digits and a 20-digit ceiling; `parse_cpulist` rejects non-ascending/overlapping ranges and counts above 65536; CLI page size requires a power of two in 1..1024; `_check_case` rejects unsafe IDs before fixture materialization. No actionable regression was observed in the requested scope.

## Residual risk and verification gaps

The live observation is environment-specific; selftest and hostile probes exercised the cited paths but do not establish behavior on every filesystem or host. The write audit covered the live CLI invocation; selftest intentionally creates and removes temporary files. I did not independently assess counter/reference correctness or unrelated round-53 surfaces.

## Findings

- No HIGH, MED, or LOW actionable findings in the reviewed tool and fixture changes.
