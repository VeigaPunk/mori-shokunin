# Mo91Sc01Src — frontier step sources (round 91, w1, attempt 1)

Seat: Mo91Sc01Src (scout). Lane repo: /home/vgpnk/Projects/shokunin/mori-shokunin. Entering revision 79eaa8cfe5e0b9b1c5ff45f524199d4a123f0520. Access date: 2026-11-05 (UTC). No lane file was read beyond corpus/SOURCES.md (read-only `git show`, for the row schema). No git mutation, no commit, no push.

## Result

| Item | Status |
|---|---|
| Source A (S617, C1 calibration) | opened: https://web.eecs.umich.edu/~weimerw/2022-481F/readings/mutation-testing.pdf |
| Source B (S618, C2 freshness) | opened: https://sre.google/sre-book/monitoring-distributed-systems/ |
| SOURCES rows | 2 drafted, 11 fields each, written to candidates/SOURCES.rows.md |

## Source A — Jia & Harman, IEEE TSE 2011, DOI 10.1109/TSE.2010.62

Attempts, in order:
1. `read https://doi.org/10.1109/TSE.2010.62` returned CrossRef metadata only (title, authors, journal, date; "No abstract available"). No full text. Not used as the text source.
2. `curl -sSL -o /dev/null https://doi.org/10.1109/TSE.2010.62` gave HTTP 302 to `http://ieeexplore.ieee.org/document/5487526/` (paywalled publisher landing). Not used.
3. OPENED (used): `read https://web.eecs.umich.edu/~weimerw/2022-481F/readings/mutation-testing.pdf` (markit conversion; the text carries the IEEE TSE layout and the authors' names). curl final URL = same, HTTP 200, application/pdf, 1181976 bytes.
   - This is a course-hosted copy of the paper, not the authors' own site. Not the publisher's version; the IEEE copy was not checked (paywalled).
   - Not used: https://mutationtesting.uni.lu/TR-09-06.pdf (a technical-report version, a different document from the TSE article).

Receipts:
- PDF sha256: 056ac9b99410321c7cb80a29284c4ca106456e1a0cf64b6f4d633ba83edff342 (1181976 bytes)
- Text extracted with `pdftotext jia-harman-umich.pdf jia-harman-raw.txt` (/usr/bin/pdftotext, pre-installed). Raw text sha256: 0debc82d0b86ecf43b05a687cdf34c60eedfc16b0b536f28c54fc2b80b7cd15c
- Quote (14 words, verbatim, Section I opening, raw text line 21): "Mutation Testing is a fault-based testing technique which provides a testing criterion called the"
- Verification: `grep -c -F '<quote>' jia-harman-raw.txt` → `1`

Other facts from the same text, checked by grep/read but not quoted in the row:
- Section II-B: killed/survived definitions and "The mutation score (MS) is the ratio of the number of killed mutants over the total number of non-equivalent mutants."
- Section IV: equivalent-mutant detection is undecidable ("program equivalence is undecidable", citing Budd and Angluin).

## Source B — Google SRE book, Chapter 6 "Monitoring Distributed Systems"

- OPENED: `read https://sre.google/sre-book/monitoring-distributed-systems/` (native HTML). curl final URL = same, HTTP 200, text/html, 73467 bytes.
- HTML sha256: 3117d94aca6d7422db18b210a4142718388523a4ea2082df539ffe9a8c4c2a75
- Quote (20 words, verbatim, section "Setting Reasonable Expectations for Monitoring", second paragraph; line 542 is that heading in the saved HTML): "Observational experiments conducted over a very long time horizon (months or years) with a low sampling rate (hours or days)"
- Verification: `grep -c -F '<quote>' sre-ch6.html` → `1`
- Fit caveat: the chapter states no drift or data-freshness test. The sentence is about sampling cadence against the observation horizon. The row's scope says so.

## SOURCES rows drafted

File: /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-91/w1/candidates/SOURCES.rows.md
sha256: 71036ef4 89fce4f5 e4f5e07d 84d6fd68 508b49f1 94895da8 4d77c96c 13175866 906e (71036ef489fce4f5e07d84d6fd68508b49f194895da84d77c96c13175866906e)
Check: `awk -F'|' '{print NR": fields="NF-2}'` → `1: fields=11`, `2: fields=11`. No escaped pipes. Each row is one line.

Row S617 (verbatim):
| S617 | An Analysis and Survey of the Development of Mutation Testing, Yue Jia and Mark Harman, IEEE TSE 2011, DOI 10.1109/TSE.2010.62; open copy https://web.eecs.umich.edu/~weimerw/2022-481F/readings/mutation-testing.pdf | paper | A | mutation kill, mutation score and equivalent-mutant definitions, the ground for calibrating an unarmed mutant kill rule | Section I opening sentence (raw text line 21, quote verified); Section II-B definitions of killed and mutation score; Section IV equivalent-mutant undecidability; PDF sha256 056ac9b99410321c7cb80a29284c4ca106456e1a0cf64b6f4d633ba83edff342, 1181976 bytes, HTTP 200 | A mutant is killed when its result differs from the original on some test; the mutation score is killed mutants over non-equivalent mutants; equivalent mutants are undecidable, so a score cannot always reach 100 percent. | mined | 2026-11-05 | 90d | none yet |

Row S618 (verbatim):
| S618 | Google SRE book, Chapter 6 Monitoring Distributed Systems, https://sre.google/sre-book/monitoring-distributed-systems/ | docs | A | sampling resolution matched to the observation horizon of a trend question; adjacent to snapshot freshness, not a drift or freshness test | Setting Reasonable Expectations for Monitoring, paragraph 2 (quote verified); Choosing an Appropriate Resolution for Measurements; page sha256 3117d94aca6d7422db18b210a4142718388523a4ea2082df539ffe9a8c4c2a75, 73467 bytes, HTTP 200 | Long-horizon, low-rate observation tolerates sparse samples because a missed sample will not hide a long-running trend; questions with short horizons need finer resolution. | mined | 2026-11-05 | 90d | none yet |

## Files written

| Path (absolute) | sha256 |
|---|---|
| /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-91/w1/candidates/SOURCES.rows.md | 71036ef489fce4f5e07d84d6fd68508b49f194895da84d77c96c13175866906e |
| /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-91/w1/Mo91Sc01Src.md | this file (not self-hashed) |

Scratch (deleted before yield): /fast/scratch/hyaku/mori-r91/Mo91Sc01Src/ holding jia-harman-umich.pdf, jia-harman-umich.txt (layout-mode, not used for verification), jia-harman-raw.txt, sre-ch6.html. The empty landing-page file was removed.

## Tooling

No installs or upgrades. Used pre-installed curl and pdftotext. pacman was not run. Nothing was written to ~/.local/bin or any PATH directory.

## Limits and open defects

1. S617 is a course-hosted PDF, not the IEEE publisher PDF or an author site. Its text matches the TSE article's layout, but this seat did not compare it with the IEEE version.
2. S617 quote is verified against pdftotext output. Layout-mode extraction does not contain the same line breaks, so the quote was checked only against the raw (non-layout) text.
3. S618 is adjacent, not a drift or freshness reference. The task asked for a source that states a practice for dated snapshots, drift or freshness. This source states sampling-cadence guidance only. If the L1 needs a true drift or freshness reference, S618 is a weak match and a second source is needed. No second source was opened, because the assignment called for one B source.
4. Tier letters follow the fleet convention as read from corpus/SOURCES.md: A for primary or official sources (S001–S024 use A for specs, docs and code). S617 is a peer-reviewed paper and S618 is the official book site. The schema header does not define tiers in the lines read, so this is an assumption.
5. Recheck 90d for both rows.
6. The `file` utility reports the S617 PDF as "2 page(s)". This is a misreport; pdftotext extracted the full text.
