PRESENT — the full-text quote attached to the quarantine register’s mori S268 is present in a publisher-deposited PDF fetched on 2026-10-25.

**Identity check.** The literal id `S268` is absent from both named files: `grep -c 'S268' /home/vgpnk/Projects/shokuknow/merge/mori/SOURCES.append.md` printed `0`; the same command on `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md` printed `0`. `git -C /home/vgpnk/Projects/shokunin/mori-shokunin log --oneline -S'S268' -- corpus/SOURCES.md` produced no rows. The quarantine register is `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md:358`: mori / round5 / S268, cited DOI `10.1109/TSC.2026.3698682`, class “the cited source could not be fetched, so no quote was checked.” The corresponding renumbered staged row is S507 in `merge/mori/SOURCES.append.md:43`, not S268; it gives the quote “It leverages eBPF to hook into OOM-related kernel tracepoints such as mark_victim, start_task_reaping, and finish_task_reaping.” The lane has S262 at `corpus/SOURCES.md:243` (same DOI, abstract-level OpenAlex record) and S478 at `:257` (same DOI, deposited full text). Therefore there is no lane row S268 to compare literally; the cited work is the same ROMA article as S262/S478, with S507/S478 describing full text and S262 abstract-level coverage.

**Fetch and quote evidence (commands and observed outputs).**

```sh
cd /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ScoutQuarantineS268
curl -sS -o doi_plain.html -w 'http=%{http_code} size=%{size_download} url=%{url_effective}\\n' -L --max-time 60 'https://doi.org/10.1109/TSC.2026.3698682'
# exit 0; http=202 size=0; redirected to https://ieeexplore.ieee.org/document/11540439/

UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
curl -sS -o roma_ielx8.pdf -w 'http=%{http_code} size=%{size_download} type=%{content_type}\\n' -L --max-time 120 -A "$UA" 'https://ieeexplore.ieee.org/ielx8/4629386/11644734/11540439.pdf'
# exit 0; http=200 size=2357114 type=application/pdf
sha256sum roma_ielx8.pdf
# 1603404dd25b3a0dff93f2dcb23c75b671d4e2d78da3cce8f461e87ebde6add2  roma_ielx8.pdf
pdftotext -enc UTF-8 roma_ielx8.pdf roma_ua.txt
# exit 0; 1405 lines, 81110 bytes
grep -n -C 2 -E 'mark_victim|start_task_reaping|finish_task_reaping' roma_ua.txt
# lines 138-141 include:
# 139 ... It leverages eBPF to hook into OOM-related kernel tracepoints such
# 140 as mark_victim, start_task_reaping, and finish_task_reaping to record OOM-triggering process
# 141 metadata. ROMA introduces two lightweight LSM hooks: (1)
grep -c 'mark_victim' roma_ua.txt
# 3
```

The fetched PDF’s SHA-256 matches lane S478’s recorded digest exactly. The register’s own S268 entry contains no quote (its never-checked table has only the cited URL); I located the concrete quote in its renumbered staged counterpart S507. This is **PRESENT**, not evidence that the DOI landing page itself serves bytes: plain DOI retrieval still returns HTTP 202/0 bytes. No tools were installed or updated.