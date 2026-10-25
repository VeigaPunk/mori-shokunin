# ExecS478Recheck — round 48 wave 1

Seat: ExecS478Recheck (leaf). Scope: round-47 routed defect 5 (verifier spotcheck **§5 item 5**):
"Refetching S478 from the IEEE URL needs a browser User-Agent; say so in the row's recheck so a
plain-curl re-open does not read as `could not re-open`." Tools: none installed (existing host
`curl`, `pdfinfo`, `python3` used). Scratch: `.scratch/r48-ExecS478Recheck/`.

## Commands and outputs

### 1. Plain curl (no User-Agent) — HTTP 418

command:
curl -sS -o /dev/null -w 'plain_http_code=%{http_code}\n' https://ieeexplore.ieee.org/ielx8/4629386/11644734/11540439.pdf
output:
plain_http_code=418
exit code: 0

### 2. Browser User-Agent — HTTP 200, download into scratch

command:
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"; curl -sS -A "$UA" -o /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ExecS478Recheck/roma-11540439.pdf -w 'browser_http_code=%{http_code} size=%{size_download}\n' https://ieeexplore.ieee.org/ielx8/4629386/11644734/11540439.pdf
output:
browser_http_code=200 size=2357114
exit code: 0

### 3. sha256 + page count recorded, then PDF deleted

command (in scratch dir):
sha256sum roma-11540439.pdf && pdfinfo roma-11540439.pdf | grep -E '^(Pages|Title|File size):' && rm -v roma-11540439.pdf
output:
1603404dd25b3a0dff93f2dcb23c75b671d4e2d78da3cce8f461e87ebde6add2  roma-11540439.pdf
Title:           ROMA: Enhancing Container OOM Resilience via Reinforced Isolation and Adaptive Shared Resource Reclamation
Pages:           14
File size:       2357114 bytes
removed 'roma-11540439.pdf'
exit code: 0

sha256 matches the S478 row's pin exactly (same byte size 2357114); page count 14 (the staged
"4 pages" figure is the round-47 mistake; RevSourcesRows also measured 14).

### 4. Registry rows whose recheck cell is an ISO date earlier than 2026-10-25

command:
python3 - <<'EOF'
import re
path = "/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md"
ids = []
for ln, line in enumerate(open(path), 1):
    if not re.match(r'^\s{0,3}\| S\d+ \|', line):
        continue
    cells = line.replace('\\|', '\x00').split('|')
    cells = [c.strip().replace('\x00', '\\|') for c in cells[1:-1]]
    if len(cells) < 11:
        print("SHORT_ROW", ln, len(cells)); continue
    rc = cells[9]
    if re.fullmatch(r'\d{4}-\d{2}-\d{2}', rc) and rc < "2026-10-25":
        ids.append((cells[0], rc, ln))
print("count=%d" % len(ids))
for i, rc, ln in ids:
    print(i, rc, "line", ln)
EOF

output:
count=0

(no rows printed)

Cross-check (awk second witness, field 11 = recheck, only ISO-date cells):
command:
awk -F'|' '/^\s*\| S[0-9]+ \|/ { gsub(/^[ \t]+|[ \t]+$/, "", $11); if ($11 ~ /^[0-9]{4}-[0-9]{2}-[0-9]{2}$/) print $2 " " $11 }' /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md | wc -l
output:
0

Full scan of all 251 S-rows: every recheck cell is a symbolic cadence
(`on-release` 183, `180d` 28, `365d` 20, `90d` 19, `per-closure` 1); zero ISO-date recheck
cells exist anywhere in the registry, so count=0 rows have an ISO-date recheck earlier than
2026-10-25.

## Observed S478 row (baseline, SOURCES.md line 257)

| S478 | ROMA: Enhancing Container OOM Resilience via Reinforced Isolation and Adaptive Shared Resource Reclamation (IEEE Trans. Services Computing, 2026, CC BY 4.0) — publisher-deposited full text https://ieeexplore.ieee.org/ielx8/4629386/11644734/11540439.pdf (doi 10.1109/TSC.2026.3698682) | paper | A | the paper's own wording about which OOM tracepoints its eBPF observer hooks; not the kernel's tracepoint inventory (S475) and not any measurement on this host | printed page 3016, section I Introduction, the paragraph proposing ROMA (pdftotext lines 139-141); PDF 2357114 bytes, sha256 1603404dd25b3a0dff93f2dcb23c75b671d4e2d78da3cce8f461e87ebde6add2, fetched 2026-10-25 with a browser user agent | The paper names three OOM tracepoints as examples (such as), not as the kernel's complete set; it adds full text to the abstract-level scope of S262 | mined | 2026-10-25 | 180d | corpus/knowledge/oom-tracepoints-r47.md |

## Draft replacement cell (S478 recheck; only status/recheck/used-by may change in place)

Recheck cell (unchanged — the cadence stands after today's browser-UA recheck held):

```
180d
```

Valid form: NNd cadence. Status stays `mined`; used-by stays `corpus/knowledge/oom-tracepoints-r47.md`.

## Lesson Gate sentence (User-Agent note lives here, not in the cell)

```
S478 re-opens must use a browser User-Agent: curl -A 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36' https://ieeexplore.ieee.org/ielx8/4629386/11644734/11540439.pdf ; a plain curl returns HTTP 418 (anti-bot), which is not a source failure and must not be read as "could not re-open". Re-verified 2026-10-25: browser-UA fetch returned 200, sha256 1603404dd25b3a0dff93f2dcb23c75b671d4e2d78da3cce8f461e87ebde6add2, 14 pages, 2,357,114 bytes.
```
