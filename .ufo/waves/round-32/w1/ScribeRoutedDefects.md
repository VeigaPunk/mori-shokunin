# Round 32 routed-defect scribe report

Axes: correctness/provenance; coverage of all six routes; staying within the report-only scope.

## Behavior

Prepared three ready-to-paste prose drafts: the six-row round-31 closure disposition table, QUALITY criterion 95, and round-32 Mistakes M1. The status language distinguishes contractually planned work from artifacts observed in this snapshot.

## Findings and evidence

- The round-31 closure routes six items at `corpus/lessons/round-31-verifier-spotcheck.md:209-227`. The frozen round-32 contract records their planned dispositions at `.ufo/waves/round-32/contract.md:67-80`.
- The QUALITY tail ends with criterion 94 at `corpus/QUALITY.md:665-679`; the next number for a new criterion is 95.
- The R4 implementation hashes the Recheck section, parses `judged-sha256`, and requires equality at `.ufo/waves/round-32/count-c1.py:195,201-216`. The expected judge receipt was not present when read: `read .ufo/waves/round-32/judge/JudgeRecheck.md` returned `Path ... not found`.
- The counter freeze and pre-data control-wave are recorded at `.ufo/waves/round-32/evidence/c1-controls.txt:1-3`; the controls and their outcomes are listed at `:8-23`.
- The inspected SKILL tail is still the Round31 blind-writer gate at `SKILL.md:772-782`; no Round32 registry row was observed. `read .ufo/waves/round-32/frozen/blind-check/expected.json` returned `Path ... not found`, and `read .ufo/waves/round-32/fixtures/edge-r32.json` returned `Path ... not found`.
- The inspected round-31 lesson tail shows the original M5 wording at `corpus/lessons/round-31.md:45-55`; no separate M5 correction was visible in that read. This is a snapshot finding, not a claim about later changes.

## Draft block — round-32 lesson disposition table

Status note: use as a truthful snapshot disposition; rows marked pending are not represented as completed.

```markdown
## Routed defects (round-31 closure §8) — disposition

| defect | disposition | evidence path |
|---|---|---|
| 1. M5 correction: the nonce masked a dropped last line on nine expected-hit fixtures across every rule. | Pending: append the M5 correction, preserving the original predicate as a conjunct; the inspected round-31 lesson tail shows the original M5 only. | `corpus/lessons/round-31.md:45-55`; `.ufo/waves/round-32/contract.md:69-70`; `corpus/lessons/round-31-verifier-spotcheck.md:211-213` |
| 2. Blind-writer gate registry and frozen baseline. | Pending: add the registry row under `SKILL.md ## Round32` with every PROTOCOL §Gate field, and land the baseline whose `expected.json` pins input digests. Neither planned artifact was observed at its specified path in this snapshot. | `SKILL.md:772-782`; `.ufo/waves/round-32/contract.md:71-72`; `.ufo/waves/round-32/frozen/blind-check/expected.json` (read: not found) |
| 3. Frozen P-C2 wording. | Recorded in the round-32 contract: state the omitted “no hit line outside the 16 briefs” clause there and leave the frozen round-31 file untouched. | `.ufo/waves/round-32/contract.md:73-75`; `corpus/lessons/round-31-verifier-spotcheck.md:217-218` |
| 4. Judge-versus-tip drift. | The counter's R4 binds `judged-sha256` to the measured tip section digest; the expected judge receipt was not observed in this snapshot. | `.ufo/waves/round-32/count-c1.py:195,201-216`; `.ufo/waves/round-32/contract.md:76-77`; `corpus/lessons/round-31-verifier-spotcheck.md:219-220`; `.ufo/waves/round-32/judge/JudgeRecheck.md` (read: not found) |
| 5. Counter use on real drafts before finalization. | Freeze the counter at `29f7d04355f17b5d45d6e00c40e2a5c3e5a2c9c4` before data seats; allow runs only after that freeze and make no subsequent counter changes. The C0 receipt records the frozen counter and control wave before data seats. | `.ufo/waves/round-32/contract.md:78-79`; `.ufo/waves/round-32/evidence/c1-controls.txt:1-3` |
| 6. Carried C2 ambiguities and tool edge cases. | Carried as committed failing fixtures for evidence only, with no tool change; the planned `edge-r32.json` was not present at its path in this snapshot. | `.ufo/waves/round-32/fixtures/edge-r32.json` (read: not found); `.ufo/waves/round-32/contract.md:80`; `corpus/lessons/round-31-verifier-spotcheck.md:224-227` |
```

## Draft block — QUALITY criterion 95

The tail of `corpus/QUALITY.md:665-679` ends at criterion 94. The proposed criterion turns round-31 defect 4 (`corpus/lessons/round-31-verifier-spotcheck.md:219-220`) into an explicit pass/fail check using the digest comparison in `.ufo/waves/round-32/count-c1.py:195,201-216`.

```markdown
## Criterion added round 32 — round-31 routed defect 4

95. A judge receipt names the SHA-256 of the bytes it judged, and the counter recomputes the SHA-256 of the measured tip's `## Recheck` section bytes and requires exact equality. A missing or malformed `judged-sha256`, or a digest unequal to the measured tip section, fails; naming a revision without binding the judged bytes is not sufficient. Check: at measured revision R, compare the receipt's `judged-sha256` with the SHA-256 of the `## Recheck` section at R; fail if the receipt has no single 64-hex digest or the values differ. ← `corpus/lessons/round-31-verifier-spotcheck.md:219-220`; `.ufo/waves/round-32/count-c1.py:195,201-216`.
```

## Draft block — round-32 Mistakes M1

The timeline in `corpus/lessons/round-31-verifier-spotcheck.md:41-53` says SrcPidMax ran imported counter helpers on its own real S173 Gate-row draft at 23:46–23:47, as a format check only; the closure routes the issue at `:221-223`. The spotcheck identifies itself as a non-author closure at `:3`.

```markdown
## Mistakes

- **M1 — counter code was run on a real draft before the counter was final (class: premature use of mutable counter code on draft data).** Evidence: the round-31 timeline records SrcPidMax importing `count-c1.py` helpers on its own drafted S173 Gate row; this was a format check only, with no `main()` or predicate verdict (`corpus/lessons/round-31-verifier-spotcheck.md:41-53`). The closure routes the same defect and requires keeping counter code away from real drafts until final (`corpus/lessons/round-31-verifier-spotcheck.md:221-223`). Captured-by: the non-author verifier's timeline review (`corpus/lessons/round-31-verifier-spotcheck.md:3,41-53,221-223`). Fix: freeze the counter before any data seat, let seats run it only after the freeze commit, and make no later changes (`.ufo/waves/round-32/contract.md:78-79`); the C0 receipt records the frozen counter and control wave before data seats (`.ufo/waves/round-32/evidence/c1-controls.txt:1-3`). Shown able to fail: the round-31 timeline is the negative case—the 23:46–23:47 real-draft helper run preceded A1 at 23:52:48Z, while the closure says the counter was still open to amendment (`corpus/lessons/round-31-verifier-spotcheck.md:36,41-42,52,221-223`). A freeze-order check must reject that ordering; the current C0 receipt records control-wave runs, not an automated rejection of a pre-freeze real-draft run (`.ufo/waves/round-32/evidence/c1-controls.txt:1-3,8-23`).
```

## Gates and touched surfaces

No source fetch, counter invocation, judge action, test, build, lint, formatter, shell command, git/jj command, or tool installation was performed. Only the report artifact was written; product files were not edited. The not-found observations above are reads at review time, not claims about later state.

## Out of scope

No corpus lesson, QUALITY criterion, SKILL registry, frozen baseline, fixture, counter, or judge receipt was edited or created. No round-32 data recheck was performed.

## Artifact path

`.ufo/waves/round-32/w1/ScribeRoutedDefects.md`
