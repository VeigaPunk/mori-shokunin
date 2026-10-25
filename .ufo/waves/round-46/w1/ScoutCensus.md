# ScoutCensus — frozen sources census

## Observed

- Ran from fleet root: `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (default `census` mode; no options).
- Command completed with exit status 0. It emitted TSV counts to stdout; no warning/error messages appeared.
- Fleet totals: `rows=2975`; tiers A/B/C/invalid = `2465/400/110/0`; statuses queued/mined/rejected/invalid = `295/2475/205/0`; missing registries = `0`.
- Per-lane counts also appeared in stdout. The script header documents census exit 0 for clean results or warnings and exit 1 for E/overdue findings (or missing census), but the observed output showed no explicit warning lines.
- Source path: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`; its documented default mode is census and its output includes `FLEET.*` totals.

## Not established

This run establishes the command's observed status/output only; it does not establish validation-mode findings or whether warnings exist under other modes/options.
