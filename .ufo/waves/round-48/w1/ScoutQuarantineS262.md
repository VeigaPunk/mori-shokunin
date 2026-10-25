# ScoutQuarantineS262 — hand-check quarantine row S262 (mori)

**Verdict: PRESENT.** The cited source — the ROMA paper, doi `10.1109/TSC.2026.3698682` — exists and is fetchable today from this host; a quote is located byte-for-byte in both the OpenAlex record (committed copy and a fresh fetch) and the publisher-deposited VOR PDF. The original "could not be fetched" record is explained by the IEEE bot wall (HTTP 202/0 on the DOI and article page; HTTP 418 on the PDF without a browser user-agent), not by absence of the source.

---

## 1. What the register row says

Source: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md:357` (section "## Rows whose quotes were NEVER CHECKED"):

```
| `mori` | round4 | S262` | the cited source could not be fetched, so no quote was checked | https://doi.org/10.1109/TSC.2026.3698682 |
```

The census finding behind it (`quote-lint-full-v5.json`):

```json
{"lane": "mori", "round": "round4", "id": "S262",
 "verdict": "fetch-failed", "detail": "https://doi.org/10.1109/TSC.2026.3698682"}
```

The negative-cache marker the census left for the DOI (`corpus-expansion-1/.qcache/<sha24>.fail`) confirms the failure mode:

```
rc=0
```

(`curl -fsSL` exited 0 but the response body was 0 bytes — the IEEE 202/0-byte bot-challenge response, not a network error. The `.raw` cache file is 0 bytes.)

## 2. Staged vs lane: same document

- **Staged:** `/home/vgpnk/Projects/shokuknow/merge/mori/SOURCES.append.md` contains **no literal S262 row** (staged ids run S471–S606; `grep -c 'S262'` → 0). The two staged ROMA rows are **S501** (abstract-level claims, via Semantic Scholar/OpenAlex) and **S507** (full text, publisher-deposited VOR PDF). `MERGE-REPORT.md` maps both to the lane's S262:
  - `| S501 | S262 | The kernel's default OOM victim selection has no container context … |`
  - `| S507 | S262 | The OOM lifecycle an observer can hook is named: mark_victim, start_task_reaping, finish_task_reaping … |`
- **Lane row:** `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md:243` — `S262 | ROMA: … (doi 10.1109/TSC.2026.3698682) | paper | A | the paper's abstract-level claims as recorded by the publisher's deposited metadata … | OpenAlex work record … | mined | 2026-10-24 | 180d | corpus/knowledge/oom-victim-context-r41.md` — the ROMA abstract record.

Both point at the **same document** (ROMA, doi `10.1109/TSC.2026.3698682`, IEEE Trans. Services Computing vol. 19 no. 4, pp. 3015–3028, 2026). The staged S501 is the renumbered twin of the register's round-4 S262; the lane adopted it as S262 in round 42 and additionally holds the full-text row S478 (round 47, VOR PDF).

## 3. Fetching the cited source myself (2026-10-25)

**3a. The DOI and the IEEE landing page — still bot-walled (as the register recorded):**

```
$ curl -sSL -o /dev/null -w 'plain: http=%{http_code} bytes=%{size_download} url=%{url_effective}\n' --max-time 40 'https://doi.org/10.1109/TSC.2026.3698682'
plain: http=202 bytes=0 url=https://ieeexplore.ieee.org/document/11540439/
$ curl -sSL -A 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36' \
    -o /dev/null -w 'browser: http=%{http_code} bytes=%{size_download} url=%{url_effective}\n' --max-time 40 'https://doi.org/10.1109/TSC.2026.3698682'
browser: http=202 bytes=0 url=https://ieeexplore.ieee.org/document/11540439/
$ curl -sSL -A 'Mozilla/5.0 … Chrome/131.0.0.0' -o landing.html -w 'http=%{http_code} bytes=%{size_download}\n' --max-time 40 'https://ieeexplore.ieee.org/document/11540439'
http=202 bytes=0
```

**3b. The publisher's deposited VOR PDF — reachable with a browser user-agent (the route the lane used for S478):**

```
$ curl -sSL -o roma-plain.pdf -w 'http=%{http_code} bytes=%{size_download}\n' --max-time 60 'https://ieeexplore.ieee.org/ielx8/4629386/11644734/11540439.pdf'
http=418 bytes=15410
$ curl -sSL -A 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36' \
    -o roma.pdf -w 'http=%{http_code} bytes=%{size_download}\n' --max-time 60 'https://ieeexplore.ieee.org/ielx8/4629386/11644734/11540439.pdf'
http=200 bytes=2357114
$ sha256sum roma.pdf
1603404dd25b3a0dff93f2dcb23c75b671d4e2d78da3cce8f461e87ebde6add2  roma.pdf
$ curl -sSL -A 'Mozilla/5.0 … Chrome/131.0.0.0' -o x.pdf -w 'http=%{http_code} bytes=%{size_download}\n' --max-time 60 'https://xplorestaging.ieee.org/ielx8/4629386/11644734/11540439.pdf'
http=200 bytes=2357114
$ sha256sum x.pdf
1603404dd25b3a0dff93f2dcb23c75b671d4e2d78da3cce8f461e87ebde6add2  x.pdf
```

sha256 `1603404d…eadd2` matches the lane row S478's pin exactly, and the complete-page cross-check in round 47's `w1/ScoutROMA.md` (§1). The PDF's first page prints `IEEE TRANSACTIONS ON SERVICES COMPUTING, VOL. 19, NO. 4, JULY/AUGUST 2026` / page `3015` / title `ROMA: Enhancing Container OOM Resilience via Reinforced Isolation and Adaptive`.

**3c. OpenAlex — 200, abstract identical to the committed copy:**

```
$ curl -sSL -o oa.json -w 'http=%{http_code} bytes=%{size_download}\n' --max-time 60 'https://api.openalex.org/works/https://doi.org/10.1109/TSC.2026.3698682'
http=200 bytes=67270
```

`python3` comparison of the fresh fetch against the committed `corpus/evidence/sources-r42/S262.oa.json`: `abstract_inverted_index` **equal: True**, `title`, `doi`, `biblio`, `open_access` all equal; the only diffs are bibliography fields (e.g. `authorships[].observed_orcids`) and formatting.

**3d. Semantic Scholar — 200, TLDR present:**

```
$ curl -sSL -o s2.json -w 'http=%{http_code} bytes=%{size_download}\n' --max-time 60 \
    'https://api.semanticscholar.org/graph/v1/paper/DOI:10.1109/TSC.2026.3698682?fields=title,abstract,tldr,externalIds'
http=200 bytes=2932
$ python3 -m json.tool s2.json | sed -n '1,25p'
{
    "paperId": "2ab2ccce455572de03406c2b8f8aa399da76500a",
    "externalIds": { "DBLP": "journals/tsc/LiWZLMGW26", "DOI": "10.1109/TSC.2026.3698682", "CorpusId": 288883898 },
    "title": "ROMA: Enhancing Container OOM Resilience via Reinforced Isolation and Adaptive Shared Resource Reclamation",
    "openAccessPdf": { "url": "https://doi.org/10.1109/tsc.2026.3698682", "status": "HYBRID", "license": "CCBY", … },
    "tldr": { "text": "ROMA introduces container awareness into the OOM handling path while maintaining low runtime overhead, and combines eBPF-based monitoring with two lightweight LSM hooks to confine OOM victim selection to the offending container and to proactively reclaim shared resources left behind after OOM events." }
}
```

## 4. Locating a quote

The row's quote (20 words, within the 6–25 band): **"Our study shows that Linux cgroups and the default Out-of-Memory (OOM) mechanism lack sufficient container context when selecting victim processes."**

- **OpenAlex (fresh fetch and committed copy), by reconstructing the abstract inverted index:**

```
$ python3 - <<'EOF'
import json
def abspath(p):
    d=json.load(open(p)); inv=d['abstract_inverted_index']; pos={}
    for w,idxs in inv.items():
        for i in idxs: pos[i]=w
    return ' '.join(pos[i] for i in sorted(pos))
q='lack sufficient container context when selecting victim processes'
for p in ['oa.json','/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r42/S262.oa.json']:
    a=abspath(p); print(p, 'QUOTE PRESENT:', q in a)
EOF
oa.json QUOTE PRESENT: True
…/sources-r42/S262.oa.json QUOTE PRESENT: True
```

The reconstructed abstract begins: "Container-based virtualization is a cornerstone of modern cloud orchestration … Our study shows that Linux cgroups and the default Out-of-Memory (OOM) mechanism lack sufficient container context when selecting victim processes. As a result, …" (1456 bytes).

- **VOR PDF text (`pdftotext -enc UTF-8`), printed page 3015 (physical page 1):**

```
$ pdftotext -f 1 -l 1 roma.pdf - | grep -c 'lack sufficient container context when selecting victim processes'
1
$ pdftotext -f 1 -l 1 roma.pdf - | sed -n '1,6p'
IEEE TRANSACTIONS ON SERVICES COMPUTING, VOL. 19, NO. 4, JULY/AUGUST 2026
3015
ROMA: Enhancing Container OOM Resilience via
Reinforced Isolation and Adaptive
```

The full sentence is on page 1: "that Linux cgroups and the default Out-of-Memory (OOM) mechanism lack sufficient container context when selecting victim processes." (line 15 of the page-1 extract).

- **The staged S507 full-text quotes also verify** (15–20 words, located on pages 2/5/6 of the PDF):
  - "It leverages eBPF to hook into OOM-related kernel tracepoints such as mark_victim, start_task_reaping, and finish_task_reaping" — page 2 (whitespace fold; the PDF wraps the line);
  - "lsm_oom_kill_check() to select victim processes within" — page 5;
  - "oom:mark_victim, oom:start_task_reaping, and" — page 6.

## 5. Verdict

**PRESENT** — with two precision notes:

1. The document is the same on both sides of the quarantine: the register's `mori round4 S262` and the lane's row `S262` both name the ROMA paper (doi `10.1109/TSC.2026.3698682`); the staged package's twin rows are S501 (abstract-level) and S507 (full text), both mapped to S262 by `MERGE-REPORT.md`.
2. The register's "could not be fetched" was accurate at the time and remains true of the **DOI landing path** (HTTP 202/0-bytes from IEEE, HTTP 418 on the PDF without a browser UA). The source is nevertheless verifiable: the publisher's deposited VOR PDF downloads with a browser user-agent (sha256 matches the lane's S478 pin), and the OpenAlex abstract record (committed and fresh) contains the quote verbatim. The quarantine reason was a bot-wall/protocol artifact, not an absent source.

## 6. Tooling (operator directive 2026-10-19)

No tool installed or upgraded. `curl`, `pdftotext` (`/usr/bin/pdftotext`) already present; no pacman transaction (pacman paused host-wide; nothing needed it). All fetches ran under `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ScoutQuarantineS262/`; no production file was touched, `/home/vgpnk/Projects/shokuknow` was read-only.
