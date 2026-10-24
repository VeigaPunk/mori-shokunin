# SrcK8sController — frontier source for C2 framing (round 20)

Seat: MoriR20.SrcK8sController (leaf, no subagents). Scope: propose one SOURCES row and a located quote for desired-versus-current state observation. No lane file was edited; no checks were run.

## Source opened

- URL: https://kubernetes.io/docs/concepts/architecture/controller/ (page title "Controllers | Kubernetes")
- Opened: 2026-10-21 via the reader (markdown rendering). Page metadata shows `article:modified_time` 2024-09-01T01:54:45+03:00; the page footer says "Last modified September 01, 2024".
- Rendering is not line-pinned. Anchors below are section headings plus sentence position, not line numbers.

## Located quotes (verbatim from the fetched text, each under 25 words)

Q1 — primary, desired vs current state definition.
Section "Controller pattern", third sentence of the first paragraph:
> "The controller(s) for that resource are responsible for making the current state come closer to that desired state."
Word count: 18.

Q2 — scope caution on settlement; the cluster need not reach a stable state.
Section "Desired versus current state", paragraph 2, final sentence:
> "potentially, your cluster never reaches a stable state."
Word count: 8.

Q3 — the reporting step (a controller reports current state to the API server; it does not only observe). Included for contrast, not for support.
Section "Direct control", paragraph 4:
> "then reports the current state back to your cluster's API server."
Word count: 11.

Each quote was checked against the fetched text above; none is paraphrased. Line breaks in the rendering (for example "desired\nstate") are whitespace only.

## Proposed SOURCES row (for L1 to admit; not written to corpus/SOURCES.md)

Next unused id: **S066**. Verified: the registry in `corpus/SOURCES.md` runs S001–S065 (rows at lines 7–71); the file's Leads section names no S-number. Bash manual lead remains unnumbered.

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S066 | Kubernetes Controllers concept page — https://kubernetes.io/docs/concepts/architecture/controller/ | docs | B | desired-versus-current-state vocabulary for control loops; conceptual overview, not a normative API or behavior spec | "Controller pattern" third sentence (Q1); "Desired versus current state" final sentence of paragraph 2 (Q2); page modified 2024-09-01, fetched 2026-10-21; rendering not line-pinned | Name the declared spec as desired state and the observed state as current state; an observed gap is not evidence that anything reconciled it, and a settled state is not guaranteed. This page's controllers act to close the gap, so it does not support an observe-only design. | queued | 2026-10-21 | 180d | — |

Field notes for L1:
- **Tier.** B follows the instruction for our host. Precedent cuts the other way: S028 (Kubernetes probes, same publisher, also explanatory docs) is tier A. Tier B is defensible here because this page is conceptual prose, not a normative spec of any API we measure. L1 should decide; if A is chosen for consistency with S028, change only the tier cell.
- **used-by** is `—`: no knowledge note cites S066 yet. Do not fill it until a lesson or note does.
- **status** `queued`: the row is proposed, not mined.

## Scope verdict: what the source does and does not support

Supports:
- The vocabulary "desired state" (the spec) and "current state" (what is observed) — Q1. This is the term pair C2 needs for observed-versus-declared comparison.
- Settlement is not guaranteed — Q2. This supports reporting "unsettled" as a real state rather than as a failure.

Does not support:
- **"mori reports observed-vs-declared settlement, it does not reconcile."** The page defines controllers as loops that *make changes* to close the gap (Q1 and the "Controller pattern" section). Its observe-and-report step (Q3) is part of a controller that also acts. The page describes no observe-only component; the only observer it mentions is "Other control loops can observe that reported data and take their own actions" (section "Direct control"). The non-reconciling stance is therefore **our design decision, not a Kubernetes claim**. Any knowledge note must state it as mori's own boundary and cite this row only for the vocabulary.
- Any claim that Kubernetes behaves this way in production, or that any specific controller's reconciliation is correct. The page does not measure behavior.

Recommended wording for a later knowledge note (L1 to decide whether to use it): "Kubernetes names the declared spec 'desired state' and the observed state 'current state' [S066]; mori adopts the same pair for observation only and does not reconcile — that boundary is mori's own."

## Quote gap check

No quote was invented. The three quotes above are the only Kubernetes wording used. If L1 wants a second located quote for "does not reconcile", none exists on this page; the honest outcome is that the stance stays unsourced.

## Incidental exposure (disclosure)

While locating the SOURCES.md registry, I ran one lane-wide keyword grep (`(?i)tier ?B|SOURCES`) with no path narrowing to the corpus. It returned incidental matches from `.jj/repo/op_store/operations/` and from `.ufo/interactive-sessions/` transcript files. The contract forbids opening retained interactive-session transcripts. I did not open those files or cite them, but their fragments appeared in the grep output and were therefore seen. No content from them is used in this report. I did not repeat the grep.

## Tools

No installs or updates. Nothing was installed by this seat.

## Commands / checks for L1 to run

- Re-fetch https://kubernetes.io/docs/concepts/architecture/controller/ and confirm the three quotes verbatim (the rendering may change; the 2024-09-01 modified date should match).
- Confirm S066 is unused in `corpus/SOURCES.md` at the integration tip.
- Decide tier (B recommended; A only if consistency with S028 is preferred).

## Out of scope (not done)

- No edits to `corpus/SOURCES.md`, any knowledge note, the lesson, the census script, baselines, MANIFEST, or the git/jj state.
- No check of other Kubernetes pages (for example, the extension-patterns or Job pages linked from this page). Only the cited page was opened.
- No behavioral verification of any Kubernetes controller.

## Findings summary

1. Proposed row S066, tier B (L1 may switch to A to match S028), status queued, recheck 180d.
2. Located quotes: Q1 (18 words, "Controller pattern"), Q2 (8 words, "Desired versus current state"), Q3 (11 words, "Direct control", contrast only).
3. The source supports desired/current vocabulary and non-guaranteed settlement; it does not support mori's observe-only, non-reconciling boundary, which is mori's own decision and must be stated as such.
