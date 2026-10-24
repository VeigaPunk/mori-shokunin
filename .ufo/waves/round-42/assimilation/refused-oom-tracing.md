# REFUSED (round 42): oom-tracing-tracepoints-r42.md

The package entry `corpus/knowledge/oom-tracing-tracepoints-r42.md` (the
round's OOM-evidence-chain theme, third candidate) was REFUSED in round 42.
Its only source row S268 (the ROMA paper's deposited VOR PDF, CC BY 4.0) was
unreachable from this host on 2026-10-24: doi.org resolves to
`ieeexplore.ieee.org/document/11540439`, which returns HTTP 202 with a
0-byte body, and the OpenAlex record reports `any_repository_has_fulltext:
False`. Without the PDF the entry's quotes (the three named tracepoints
`mark_victim`, `start_task_reaping`, `finish_task_reaping`; the two LSM
hooks; the 6.94% overhead figure) cannot be located, so the row is
quarantined-unverifiable — unreachable, not fabrication (register slice row
`mori round5 S268`, class cell "could not be fetched"). Flip condition: a
fetchable copy of the VOR PDF (repository mirror, OA deposit, or an
operator-side fetch); on flip the entry re-enters gating with quotes
re-located at the fetched copy. No campaign file was edited.
