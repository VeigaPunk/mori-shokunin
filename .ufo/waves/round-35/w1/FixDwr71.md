measured 2026-10-23T08:52:01Z

# Routed defect 3 — disk-write-rate-r33 provenance

Axes: commit-path resolvability; row-judgment provenance; verdict traceability.

## Behavior

Draft an append-only replacement note naming the committed row-audit reports. The current line 71 names the uncommitted `round-34/w1/` drafting directory and only the generic `wa/` directory (`corpus/knowledge/disk-write-rate-r33.md:70-72`).

VERDICT: current line-71 pointer: unsupported

At commit `dd76eb79`, the `w1/` pathspec returned no entries, while `wa/` contains named judge reports. The drafting outputs are therefore not committed in this audited tree. Evidence: `timeout 30s git -C /home/vgpnk/Projects/shokunin/mori-shokunin ls-tree -r dd76eb79 --name-only -- .ufo/waves/round-34/w1/ .ufo/waves/round-34/wa/` returned only `.ufo/waves/round-34/wa/...` paths, including `JudgeRow3r.md`, `JudgeRow6r.md`, `JudgeRow7r.md`, and `JudgeRow13r.md`; it returned no `w1/` path. The committed source line itself is shown by `git show dd76eb79:corpus/knowledge/disk-write-rate-r33.md` and is at `corpus/knowledge/disk-write-rate-r33.md:71`.

## Findings

The committed wave-A audits judged all four original repaired rows supported: `wa/JudgeRow3r.md:33`, `wa/JudgeRow6r.md:68`, `wa/JudgeRow7r.md:43`, and `wa/JudgeRow13r.md:61`. The committed wave-B re-judgements are `wb/ReJudgeRow3r.md:36`, `wb/ReJudgeRow6r.md:117`, `wb/ReJudgeRow7r.md:66`, and `wb/ReJudgeRow13r.md:82`. Their findings are respectively unsupported, supported, supported, and supported. The residual report `wb/residual/MoriR34A3.JudgeRow3r2.md:95` judged superseding row 3r2 supported.

The row-3r disagreement is verbatim: `wa/JudgeRow3r.md:33` says `VERDICT: row 3r: supported`; `wb/ReJudgeRow3r.md:36` says `VERDICT: row 3r: unsupported`. The residual 3r2 judgment is a later, different row: `VERDICT: row 3r2: supported` (`wb/residual/MoriR34A3.JudgeRow3r2.md:95`). Preserve this distinction; do not collapse it into a single 3r verdict.

Path checks used the required committed-tree query. `timeout 30s git -C /home/vgpnk/Projects/shokunin/mori-shokunin ls-tree -r dd76eb79 --name-only -- corpus/knowledge/disk-write-rate-r33.md .ufo/waves/round-34/wb/ReJudgeRow3r.md .ufo/waves/round-34/wb/ReJudgeRow6r.md .ufo/waves/round-34/wb/ReJudgeRow7r.md .ufo/waves/round-34/wb/ReJudgeRow13r.md .ufo/waves/round-34/wb/residual/MoriR34A3.JudgeRow3r2.md` returned each of those exact paths. The complete `wb/` listing (`timeout 30s git -C /home/vgpnk/Projects/shokunin/mori-shokunin ls-tree -r dd76eb79 --name-only -- .ufo/waves/round-34/wb/`) contains no `RepairRow*` path; the `w1/` query above returned none. Thus the named drafting-seat outputs were not committed at `dd76eb79`. The queried `wa/` listing returned the four named JudgeRow reports above.

### DRAFT disk-write-rate-r33 correction

```DRAFT disk-write-rate-r33 correction
**Round-34 audit provenance correction (append-only).** The attempt-1 drafting-seat outputs (RepairRow03, RepairRow06, RepairRow07, and RepairRow13) were not committed at `dd76eb79`; the committed wave-A judgments are `.ufo/waves/round-34/wa/JudgeRow3r.md`, `.ufo/waves/round-34/wa/JudgeRow6r.md`, `.ufo/waves/round-34/wa/JudgeRow7r.md`, and `.ufo/waves/round-34/wa/JudgeRow13r.md`. The later wave-B re-judgements are `.ufo/waves/round-34/wb/ReJudgeRow3r.md`, `.ufo/waves/round-34/wb/ReJudgeRow6r.md`, `.ufo/waves/round-34/wb/ReJudgeRow7r.md`, and `.ufo/waves/round-34/wb/ReJudgeRow13r.md`; their verdicts are unsupported, supported, supported, and supported, respectively. Wave A judged row 3r supported, while wave B judged row 3r unsupported (`JudgeRow3r.md:33`; `ReJudgeRow3r.md:36`). The later residual report `.ufo/waves/round-34/wb/residual/MoriR34A3.JudgeRow3r2.md` judged superseding row 3r2 supported.
```

## Gates and touched surfaces

- Read-only evidence checks: `git show` of the target at `dd76eb79`; `git ls-tree -r dd76eb79 --name-only` for the round-34 `w1/`, `wa/`, `wb/`, and explicit report paths; read the listed audit reports. No build, test, lint, counter, or runtime gate was run.
- This report is the only file written: `.ufo/waves/round-35/w1/FixDwr71.md`. No product files or judge artifacts were edited. No tool installed or updated; `~/.omp/agent/RULES.md` was read first.

## Out of scope

No re-judgment of the row evidence, C1 counter run, commit mutation, or change to the knowledge entry. The block above is a draft for the integration owner, not an applied edit.

## Artifact path

`.ufo/waves/round-35/w1/FixDwr71.md`
