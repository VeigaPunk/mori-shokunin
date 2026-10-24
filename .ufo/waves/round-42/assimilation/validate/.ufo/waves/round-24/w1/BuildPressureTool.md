# BuildPressureTool scoped findings

## Files and behavior

Implementation: `/fast/scratch/hyaku/mori-r24-a2/wt-pressure/tools/mori-pressure.py` (new file, sandbox only).

- Standard library, executable Python 3 script; normal output is one JSON object.
- Reads cpu, memory, io, irq; strict ordered PSI grammar, duplicate/missing kinds rejected.
- Unavailable resources are null, never zero; open and read errors share errno mapping; EOPNOTSUPP carries no inferred cause.
- Local, uncalibrated avg10 threshold excludes system CPU full; IRQ some may be null.
- Interval mode uses second-read averages, nominal ratios rounded to six places, null CPU full delta/ratio, non-ok state propagation and counter regression state.
- Selftest resolves fixtures from script location, uses in-process open+read and no-op sleep hooks and subset matching as specified.
- A2/A3 read from lane contract lines 110–135. Documentation is included in the implementation docstring; lane knowledge/skill documentation belongs to the other seats.

## Identity and integration blocker

SHA256: `852d1ea7508004dc44690bb6e358625fbd07d89c26d4196793133559d8a773a5`

Line count: 569

Commit: **not created**. The seat's developer role forbids committing; only L1 may integrate. The requested sandbox commit is therefore blocked by that role instruction, not by Git failure. Base observed before editing: `29c1bf45dde6af48fc9a07aef447bd7d7f822cc5`; branch `r24-wt-pressure`.

## Retained evidence

`/fast/scratch/hyaku/mori-r24-a2/build-pressure-private/live-evidence.json` retains both exact commands, exit codes, stdout, stderr and raw before/after reads for each observation. Each tool invocation occurred exactly once; both exited 0, stderr empty, verdict PRESSURE_OK. Raw brackets are retained for L1's A2 bracket check; no automatic bracket assertion was run here.

### One-shot observation

Command: `python3 -I /fast/scratch/hyaku/mori-r24-a2/wt-pressure/tools/mori-pressure.py`

Exit: 0; stderr empty.

```json
{
  "findings": [],
  "resources": {
    "cpu": {
      "full": {
        "avg10": 0.0,
        "avg300": 0.0,
        "avg60": 0.0,
        "total": 0
      },
      "full_system_undefined": true,
      "notes": [
        "parsed from the kernel PSI line grammar",
        "system cpu 'full' is undefined by the kernel: reported, never used for a threshold"
      ],
      "some": {
        "avg10": 0.17,
        "avg300": 0.15,
        "avg60": 0.28,
        "total": 3857407
      },
      "state": "ok"
    },
    "io": {
      "full": {
        "avg10": 6.63,
        "avg300": 5.29,
        "avg60": 6.75,
        "total": 53877295
      },
      "notes": [
        "parsed from the kernel PSI line grammar"
      ],
      "some": {
        "avg10": 7.39,
        "avg300": 5.72,
        "avg60": 7.48,
        "total": 56100007
      },
      "state": "ok"
    },
    "irq": {
      "full": {
        "avg10": 0.98,
        "avg300": 0.49,
        "avg60": 0.92,
        "total": 9910336
      },
      "notes": [
        "parsed from the kernel PSI line grammar"
      ],
      "some": null,
      "state": "ok"
    },
    "memory": {
      "full": {
        "avg10": 1.22,
        "avg300": 0.54,
        "avg60": 0.84,
        "total": 6214226
      },
      "notes": [
        "parsed from the kernel PSI line grammar"
      ],
      "some": {
        "avg10": 1.22,
        "avg300": 0.56,
        "avg60": 0.86,
        "total": 6287394
      },
      "state": "ok"
    }
  },
  "root": "/proc/pressure",
  "schema": "mori-pressure-v1",
  "threshold": {
    "label": "local (not calibrated)",
    "metric": "avg10",
    "value": 10.0
  },
  "verdict": "PRESSURE_OK"
}
```

### Interval observation

Command: `python3 -I /fast/scratch/hyaku/mori-r24-a2/wt-pressure/tools/mori-pressure.py --interval 1`

Exit: 0; stderr empty.

```json
{
  "elapsed_us": 1000283,
  "findings": [],
  "interval_s": 1.0,
  "resources": {
    "cpu": {
      "full": {
        "avg10": 0.0,
        "avg300": 0.0,
        "avg60": 0.0,
        "stall_ratio": null,
        "total": 0,
        "total_delta_us": null
      },
      "full_system_undefined": true,
      "notes": [
        "parsed from the kernel PSI line grammar",
        "system cpu 'full' is undefined by the kernel: reported, never used for a threshold"
      ],
      "some": {
        "avg10": 0.17,
        "avg300": 0.15,
        "avg60": 0.28,
        "stall_ratio": 0.007465,
        "total": 3865206,
        "total_delta_us": 7465
      },
      "state": "ok"
    },
    "io": {
      "full": {
        "avg10": 6.63,
        "avg300": 5.29,
        "avg60": 6.75,
        "stall_ratio": 0.084137,
        "total": 53964357,
        "total_delta_us": 84137
      },
      "notes": [
        "parsed from the kernel PSI line grammar"
      ],
      "some": {
        "avg10": 7.39,
        "avg300": 5.72,
        "avg60": 7.48,
        "stall_ratio": 0.09174,
        "total": 56195042,
        "total_delta_us": 91740
      },
      "state": "ok"
    },
    "irq": {
      "full": {
        "avg10": 0.98,
        "avg300": 0.49,
        "avg60": 0.92,
        "stall_ratio": 0.011601,
        "total": 9922303,
        "total_delta_us": 11601
      },
      "notes": [
        "parsed from the kernel PSI line grammar"
      ],
      "some": null,
      "state": "ok"
    },
    "memory": {
      "full": {
        "avg10": 1.22,
        "avg300": 0.54,
        "avg60": 0.84,
        "stall_ratio": 0.008611,
        "total": 6222845,
        "total_delta_us": 8611
      },
      "notes": [
        "parsed from the kernel PSI line grammar"
      ],
      "some": {
        "avg10": 1.22,
        "avg300": 0.56,
        "avg60": 0.86,
        "stall_ratio": 0.008707,
        "total": 6296116,
        "total_delta_us": 8707
      },
      "state": "ok"
    }
  },
  "root": "/proc/pressure",
  "schema": "mori-pressure-v1",
  "threshold": {
    "label": "local (not calibrated)",
    "metric": "avg10",
    "value": 10.0
  },
  "verdict": "PRESSURE_OK"
}
```

## Checks not run, risks and blockers

- No build, linter, formatter or selftest was run: the developer wave role explicitly forbids tests while editing. Frozen `PASS 12/12` is **not claimed**. L1 should run the integrated `python3 -I tools/mori-pressure.py --selftest` and the retained raw-total bracket comparison after integration.
- The frozen cases were read from the other seat's clone, not edited. A throwaway copy of them and an early implementation copy were briefly placed under the private directory, not executed, and removed. No fixture file was written in either repo.
- LSP unavailable: the exposed tool inventory has no LSP definition/reference/refactor tool. This task creates a standalone tool, with no existing symbol callers to migrate.
- Severity precedence between two different non-ok read states is malformed, counter_regressed, unreadable, unsupported, absent. The contract only requires choosing a non-ok state.
- No host writes, triggers, service changes, package installs or updates; no tools installed. Existing Python reported 3.14.8.
- Code remains uncommitted for L1 integration. No parent/sibling production files changed.
