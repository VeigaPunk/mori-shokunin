source: S602 — https://raw.githubusercontent.com/in-toto/docs/v1.0/in-toto-spec.md, in-toto Specification v1.0.0 (title page `Version 1.0.0`, dated Jun 02, 2023; tag `v1.0` → commit 926031f40be8db78f992f02f3e50e97a09db5320); pin `.ufo/waves/round-86/evidence/sources-r86/in-toto-spec-v1.0.md:1062-1068` (the link-metadata byproducts paragraph), `:1022-1046` (the link schema), `:329-334` (the Byproducts definition), `:344-347` (the Verification definition) and `:785-807` (the inspection record, which carries a `run` command); sha256 `17d3326e4cf58234619dbfe821cdc5187e55e2c89f7b63f03699c46588322097`, 87108 bytes, 2217 lines.
verified-at: 2026-11-04
recheck: 365d
coverage-map: calibration — execution evidence: what an execution record contains and what its stated verification actually checks; carries `knowledge/receipt-provenance-r85.md` (S600: a digest binds bytes at a revision) into the r86 C2 `# replay: required` rule; no frontier row advanced

# Execution evidence: a recorded command and its stdout are not a verified binding (round 86)

Axes: calibration. The source grounds the shape of an execution record and — the load-bearing part — the
scope its own default verification covers. It says nothing about mori, receipts, revisions, digests,
exit codes or this lane's counters; those are the lane's rules (r85 K3 for the receipt grammar, the r86
C2 contract for the replay rule) and are attributed here as the lane's, never as the source's.

## K1 — What an execution record contains

The link file "will contain the information recorded from the execution of a supply chain step"
(`:1012-1013`) and "lists relevant information, such as the command executed, the materials used, and
the changes made to such materials (products), as well as other host information" (`:1013-1015`). The
The schema at `:1025-1046` carries five fields (condensed below; the pin has the full literal,
including its `"..." : "..."` entries):

```json
{ "command" : "<COMMAND>",
  "materials": { "<ARTIFACT_NAME>": "<HASH>" },
  "products":  { "<ARTIFACT_NAME>": "<HASH>" },
  "byproducts": { "stderr": "", "stdout": "", "return-value": null },
  "environment": { "variables": "<ENV>", "filesystem": "<FS>", "workdir": "<CWD>" } }
```

`The COMMAND field contains the command and its arguments as executed by the functionary.`
(`:1053-1054`, 14 words). So the record names the command, hashes the inputs and outputs, and stores
the command's stdout/stderr/return value in a separate `byproducts` object. The record is signed:
`Link` is "metadata information gathered while performing a supply chain step or inspection, signed
by the functionary that performed the step" (`:318-321`).

## K2 — The spec's own split: recorded is not verified

The byproducts paragraph is the located limit (`:1062-1068`): the field is "an opaque dictionary";
`Byproducts are not verified by in-toto’s default verification routine.` (`:1063-1064`, 9 words);
the recorded information "can be used for further scrutiny during an inspection step"; the minimum
members are stdout, stderr and return-value, the last stored as an integer.

The terminology fixes the same split. `Byproducts`: "indirect results of carrying out a step, often
used to verify that a step was performed correctly … the stdout, stderr and return values are common
byproducts that can be inspected to verify the correctness of a step" (`:329-334`). And `Verification`
is "the process by which data and metadata included in the final product is used to ensure its
correctness. Verification is performed by the client by checking the supply chain layout and links for
correctness, as well as by performing the inspection steps" (`:344-347`).

Three consequences, one of them about this lane:

- **A recorded body does not certify itself.** The stdout is recorded *so that* a later check can use
  it; the spec states that the default routine does not check it. Writing down a command and its
  output is a record, not a binding — the same distinction the r85 entry drew between a digest over
  the bytes and the execution that produced them.
- **The signature is not the missing check.** The link is signed by the functionary (`:318-321`); the
  document states no check that the recorded command actually produced the recorded stdout. A
  signature names who produced the metadata, and the spec's only byproduct-scrutiny mechanism is an
  inspection (`:1064-1065`).
- **"Often used to verify" is not "verified".** The definition says byproducts are often used to
  verify correctness; the byproducts paragraph says the default verification does not verify them.
  Both are the document's words, and the difference is exactly where a replay rule has to sit.

## K3 — The re-execution mechanism the spec already has, and what it compares

An inspection is "operations that need to be performed on the final product at the time of
verification" (`:787-789`) and its record carries `"run": "<COMMAND>"` (`:795-807`) plus
`expected_materials` / `expected_products` artifact rules. So the spec does contain a re-execution
mechanism at verification time. What it checks is artifacts through artifact rules; the inspection's
own stdout is not compared to any recorded `byproducts.stdout`, because the document defines no such
comparison. The mechanical form — re-run the recorded command, compare the body — is therefore the
lane's construction on the spec's inspection shape, not a quotation from it.

Negative-claim sweeps on the pin (2026-11-04, commands in K5): the word `reproduc` occurs **0** times
in the whole specification; `stdout` occurs **16** times (2 prose uses at `:332` and `:1066`, 14 JSON
example values); `compar` occurs **once**, at `:959`, an artifact-rule code comment ("# compare both
sets"), not a byproduct rule. The spec never claims that a recorded body is reproducible and never
states a body-versus-command comparison.

## K4 — What this grounds for mori's r86 C2 rule, and what it does not

The r86 C2 predicate (`.ufo/waves/round-86/contract.md` P-C2) requires a `# replay: required`
receipt's body to equal the stdout of its `# cmd:`, executed in a scratch export of the receipt's own
`# rev:`, with `GIT_CONFIG_GLOBAL=/dev/null`. The mapping is:

| r86 receipt line | record field | ground |
|---|---|---|
| `# cmd: <text>` | `"command"` | the record names the command and its arguments as executed (`:1053-1054`) |
| `# ---` body (stdout) | `"byproducts": {"stdout": …}` | the body is the command's output, recorded (`:1036-1040`, `:1066-1067`) |
| `# counter-sha256:` | `"materials"/"products"` hashes | bytes at a revision are compared by digest — S600, not this source |
| `# rev:` | — (nothing) | the revision binding is the lane's own; the spec's `environment` is opaque (`:1070-1073`) |
| replay pass | inspection with `"run"` | re-execution at verification time (`:785-807`) |

The gain is the **necessity** argument, and it is the one the round needs: a receipt whose headers and
digests all verify is exactly the spec's `byproducts` case — a recorded command plus a recorded body
that the default verification never checks. The r86 rule adds the inspection the spec leaves to the
verifier: re-run the recorded command in the named tree and compare the body. S600 supplies the
byte-comparison rule for that comparison; this source supplies the reason the record alone cannot
stand in for it.

Not claimed: that in-toto requires reproducibility (it never uses the word — sweep above); that its
signature binds execution; that mori implements in-toto; or that the r86 rule is stronger than the
spec's verification model in general — it is stronger than *the byproducts clause*, on a different
artifact (a receipt body, not a software product).

## K5 — Named limits and the sweeps behind the negatives

- The document specifies a metadata format and a verification model, not a verifier on this host: no
  shell, no environment pinning (`environment` is "an opaque field", `:1070-1073`), no exit code, no
  byte-comparison algorithm, no revision-bound tree export.
- The byproduct requirement is a "should" over stdout/stderr/return-value (`:1065-1067`), and its
  scrutiny is a permission ("can be used", `:1064-1065`), not an obligation.
- Version-anchored: tag `v1.0` → commit `926031f4…`, title page `Version 1.0.0`, Jun 02, 2023. A later
  revision could add a byproduct rule; recheck at 365d and on a new tag.
- Sweep commands on the pin, 2026-11-04:
  `grep -ci 'reproduc' … → 0`; `grep -c 'stdout' … → 16` (lines 332, 1038, 1066, 1368, 1400, 1563,
  1594, 1628, 1813, 1845, 1877, 2051, 2083, 2115, 2147, 2179); `grep -ci 'byproduct' … → 22`;
  `grep -ci 'compar' … → 1` (line 959).
- The pin is raw Markdown as served by raw.githubusercontent (saved with a `.md` suffix, not the
  wave's `.html` template, because the bytes are not HTML); it begins with a UTF-8 BOM, and the quote
  above spans a line break, joined with one space.

## Gate

- URL: `https://raw.githubusercontent.com/in-toto/docs/v1.0/in-toto-spec.md` — HTTP 200, no redirect
  (final URL identical), two fetches byte-identical, sha256
  `17d3326e4cf58234619dbfe821cdc5187e55e2c89f7b63f03699c46588322097`, 87108 bytes, 2217 lines.
- Accessed: 2026-11-04.
- Located quote (9 words, verbatim, sentence begins mid-line 1063 and ends mid-line 1064, joined with
  one space; the apostrophe is U+2019):
  > Byproducts are not verified by in-toto’s default verification routine.
- Supporting quote (14 words, `:1053-1054`):
  > The COMMAND field contains the command and its arguments as executed by the functionary.
- Pin: `.ufo/waves/round-86/evidence/sources-r86/in-toto-spec-v1.0.md`.
