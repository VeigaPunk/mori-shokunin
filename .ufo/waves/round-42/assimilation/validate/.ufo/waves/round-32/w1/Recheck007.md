# Recheck S007 — C1 freshness (round 32, wave 1)

Seat: `MoriR32A2.Recheck007`. Question: does the live systemd-oomd man page still support the S007 teaches cell?

## 1. Fetch record

- id: S007
- url: https://www.freedesktop.org/software/systemd/man/latest/systemd-oomd.service.html
- redirected: no (curl `%{url_effective}` equals the population url)
- accessed: 2026-10-23T01:31:25Z (`date -u +%FT%TZ` at fetch)
- fetch: `curl -sSL --fail -m 60 <url> -o S007.src` → exit 0, HTTP 200, size_download 10542
- byte size of saved copy: 10542
- sha256 of saved copy: `56460ffb24d7ea3ccd771b7f834a460786b646038411c0744b981ad532af6f0a`
- scratch copy: `/fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck007/S007.src`
- fetch log: `/fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck007/S007.fetch.txt`
- normalised text (counter view): `/fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck007/S007.txt` (4444 bytes)
- page still identifies itself as "systemd 262" (anchor item), and all four anchor sections are present:
  Description, System requirements and configuration, Options `-n, --dry-run`, Signals `SIGHUP`.

## 2. Ready-to-paste row

```markdown
| S007 | https://www.freedesktop.org/software/systemd/man/latest/systemd-oomd.service.html | 2026-10-23T01:31:25Z | 56460ffb24d7ea3ccd771b7f834a460786b646038411c0744b981ad532af6f0a | "select a cgroup to terminate, and send SIGKILL to all processes in it"; "only descendant cgroups are eligible candidates for killing"; "systemd-oomd periodically polls PSI statistics for the system and those cgroups to decide when to take action" | current |
```

## 3. Quote → teaches-cell mapping

- teaches: "oomd selects eligible descendant cgroups and sends SIGKILL to all processes in the selected cgroup."
- Quote 1 `"select a cgroup to terminate, and send SIGKILL to all processes in it"` — the live Description's kill sentence; directly supports "sends SIGKILL to all processes in the selected cgroup".
- Quote 2 `"only descendant cgroups are eligible candidates for killing"` — the live Description's eligibility rule; directly supports "selects eligible descendant cgroups". (The full sentence continues "; the unit with its property set to kill is not a candidate"; the quoted clause does not drop that negation, it simply stops at the semicolon.)
- Quote 3 `"systemd-oomd periodically polls PSI statistics for the system and those cgroups to decide when to take action"` — bears on the scope cell "systemd-oomd PSI monitoring, kill selection and service behavior": monitoring is by PSI polling, and the kill follows the threshold decision.
- Verdict `current`: the live page says the same three things the teaches cell asserts (descendant-only eligibility, SIGKILL to all processes in the selected cgroup, PSI-driven selection). No statement in the page contradicts the row, so no `Round32` correction is drafted. Both used-by files (`corpus/knowledge/oom-kill-counter-kernel-only-r12.md:13`, `corpus/knowledge/userspace-oom-killers-r12.md:12`) cite exactly this SIGKILL-to-all-processes sentence, which is still live.

## 4. seat-check output

Command:
`timeout 300 python3 .ufo/waves/round-32/seat-check.py row S007 S007.src '"select a cgroup to terminate, and send SIGKILL to all processes in it"; "only descendant cgroups are eligible candidates for killing"; "systemd-oomd periodically polls PSI statistics for the system and those cgroups to decide when to take action"'`

```
sha256=56460ffb24d7ea3ccd771b7f834a460786b646038411c0744b981ad532af6f0a
quotes=3 words=[13, 8, 17] in_copy=[True, True, True]
shared_tokens=['cgroup', 'cgroups', 'descendant', 'eligible', 'oomd', 'processes', 'sigkill', 'system', 'systemd'] topic_ok=True
live_quotes_ok=True
ROW_CHECK=pass (judge R4 and R5 not checked here)
exit=0
```

## 5. Drift details

None. Verdict is `current`; no correction paragraph is required for S007.

Notes for the integrator: copy `/fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck007/S007.src` to `corpus/evidence/recheck-r32/S007.src` unchanged (sha above). Tooling: nothing installed or updated this seat; only `curl`, `sha256sum` and the frozen `seat-check.py` were used. No background jobs were left running.
