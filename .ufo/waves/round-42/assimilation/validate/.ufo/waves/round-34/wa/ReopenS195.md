measured 2026-10-23T05:38:49Z

# Reopen S195 — sysstat common.c v12.8.0 (is_device)

Scope: SOURCES.md row S195 at 8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3 (line 201), committed copy corpus/evidence/sources-r34/S195.src, live re-fetch.

## Live fetch vs committed copy

Commands (scratch /fast/scratch/hyaku/mori-r34/a2-MoriR34A2.ReopenS195/):
- `curl -sSL --fail -m 60 -o s195-live-1.c https://raw.githubusercontent.com/sysstat/sysstat/v12.8.0/common.c` at 2026-10-23T05:38:42Z
- `curl -sSL --fail -m 60 -o s195-live-2.c <same url>` at 2026-10-23T05:38:42Z
- sha256 (each, identical): 4aa91c92577ac27970c55b3778e0718a575a17cf86b40d3bbb9ed8d4412eac21; 47807 bytes each.
- Committed copy S195.src sha256: 4aa91c92577ac27970c55b3778e0718a575a17cf86b40d3bbb9ed8d4412eac21; `cmp -l S195.src s195-live-1.c | wc -l` = 0 (byte-identical).
- Two live downloads identical (cmp -s), URL resolved on `v12.8.0` tag.

## Clause-by-clause judgement (teaches cell)

Row teaches: `is_device() returns TRUE for a device and FALSE for a partition; a device is assumed virtual when no /sys/block/<device>/device link exists.`

1. "is_device() returns TRUE for a device and FALSE for a partition" — SUPPORTED.
   Quote: S195.src:208 (12 words): "TRUE if @name is a device, and FALSE if it's a partition."
2. "a device is assumed virtual when no /sys/block/<device>/device link exists." — SUPPORTED.
   Quote: S195.src:204-205 (12 words): "The device is assumed to be virtual if no /sys/block/<device>/device link exists."

Neither clause is labelled `lane rule:`; both have contiguous located quotes from the copy.

## Anchor check

Anchor: `common.c:197-224; tag v12.8.0`. In S195.src, lines 197-210 are the doc comment for is_device (including both quoted clauses at 204-205 and 208); line 211 is `int is_device(const char *sysdev, char *name, int allow_virtual)`; lines 212-224 are the body: name-slash replacement, snprintf building `%s/%s/%s%s` with `"/device"` appended when `allow_virtual` is false (line 220-221), and `return !(access(syspath, F_OK));` (line 223). The anchor range holds the cited code, and the body implements exactly the documented behavior (the `access()` on the dir `/device` path is the "no … device link exists" test).

## Proposed Gate row

| S195 | https://raw.githubusercontent.com/sysstat/sysstat/v12.8.0/common.c | 2026-10-23 | 4aa91c92577ac27970c55b3778e0718a575a17cf86b40d3bbb9ed8d4412eac21 | S195.src:208,204-205 | admit, A, mined |

VERDICT: admit

Tooling: no installs/updates performed (curl, sha256sum, date already present).
