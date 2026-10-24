# Round 33 wave 1 — S062 scoping findings

Axes: provenance, page-versus-lane attribution, minimality.

## Basis and behavior

The requested read-only command, `timeout 15s sh -c 'git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 7d382043:corpus/SOURCES.md | grep -n "^| S062 "'`, returned base row line 68 (tool output `artifact://10680`). The working row is also `corpus/SOURCES.md:68` and is text-identical. The round-32 Recheck entry is `corpus/lessons/round-32.md:42`; it records three quoted snippets and `current`.

The committed page copy is `corpus/evidence/recheck-r32/S062.src`. The cell's page-derived claims are supported there:

- “JCS canonical JSON serialization for hashing”: the page says “Cryptographic operations like hashing and signing need the data to be expressed in an invariant format” (`S062.src:134-136`) and “One way to address this is to create a canonical representation of the data” (`:138-142`). It calls JCS output a “hashable” representation (`:203-205`; raw copy uses `&quot;hashable&quot;`).
- “whitespace”: “Whitespace between JSON tokens <span class="bcp14">MUST NOT</span> be emitted” (`:378-379`).
- “string escapes”: the string-serialization rules specify lowercase hexadecimal notation and the predefined control-character escapes (`:441-460`), including `\b`, `\t`, `\n`, `\f`, and `\r` (`:449-453`).
- “ECMAScript number serialization” / “ECMAScript number text”: the page says JCS primitive serialization “is identical to that of ECMAScript” (`:417-423`) and requires JSON numbers to be serialized according to ECMA-262 (`:481-483`).
- “UTF-16 property-name sort”: the page says property-name strings are converted to arrays of UTF-16 code units before sorting (`:551-556`, and `:596-601`). The Recheck Q1 at `round-32.md:42` stops before “code units”; the page copy itself contains the fuller statement. This is a quote-boundary issue, not a lane-application clause; the verifier noted it at `round-32-verifier-spotcheck.md:106`.
- “UTF-8 output”: the preceding canonicalization result “MUST be encoded in UTF-8” (`:647-649`).
- “normative for JCS conformance”: the page calls itself a specification that defines the canonical representation (`:144-149`) and states the requirements with MUST language (for example `:378-379`, `:481-483`). This summarizes the page's JCS rules, not a separate lane application.
- “Informational independent submission (June 2020)”: the page says it is published for informational purposes and is independent of other RFC streams (`:157-165`); its metadata gives “June 2020” and “Independent Stream” (`:1681-1685`).
- In the teaches cell, “no duplicate names” is stated at `S062.src:326-328`; “error on NaN/Infinity” is stated at `:497-500`.

## Lane inference/application clauses and redraft

The scope cell contains no lane-specific application clause; the page copy supports each part as above. Two teaches clauses are not statements made by this page and should be declared as lane rules:

1. **“-0 is a parser SHOULD-error per the verified errata”** — the committed RFC page copy does not state this parser rule. Its end matter only links to RFC 8785 errata (`S062.src:1691-1692`); the row's anchor mentions an errata record (`corpus/SOURCES.md:68`), but the erratum text is not in this committed page copy. Proposed declaration: `lane rule: -0 is a parser SHOULD-error per the verified errata`.
2. **“a Python json.dumps identity matches JCS only inside a restricted domain”** — the RFC page copy does not state this Python/JCS comparison. S063 (`corpus/SOURCES.md:69`) is only a Python `json.dumps` parameter-contract row and explicitly says it cannot test JCS equivalence. Proposed declaration: `lane rule: a Python json.dumps identity matches JCS only inside a restricted domain`.

The existing comparison rows make this attribution explicit: S073 says its rejecting-`..`/absolute-path rule is “mori's own tool rule, not taught by this page” (`corpus/SOURCES.md:79`); S074 says the observe-only stance is “the lane's own boundary, not taught here” (`:80`); S076 calls the re-pin reading “the lane's own application, not taught here” (`:82`).

### Old and proposed cells

Scope — old:
```
JCS canonical JSON serialization for hashing: whitespace, string escapes, ECMAScript number serialization, UTF-16 property-name sort and UTF-8 output; normative for JCS conformance, Informational independent submission (June 2020)
```

Scope — proposed (unchanged):
```
JCS canonical JSON serialization for hashing: whitespace, string escapes, ECMAScript number serialization, UTF-16 property-name sort and UTF-8 output; normative for JCS conformance, Informational independent submission (June 2020)
```

Teaches — old:
```
A canonical form for hashing needs UTF-16 code-unit key order, ECMAScript number text, no whitespace, error on NaN/Infinity, no duplicate names; -0 is a parser SHOULD-error per the verified errata; a Python json.dumps identity matches JCS only inside a restricted domain.
```

Teaches — proposed (only the two declarations added):
```
A canonical form for hashing needs UTF-16 code-unit key order, ECMAScript number text, no whitespace, error on NaN/Infinity, no duplicate names; lane rule: -0 is a parser SHOULD-error per the verified errata; lane rule: a Python json.dumps identity matches JCS only inside a restricted domain.
```

Old → proposed diff:
```diff
-A canonical form for hashing needs UTF-16 code-unit key order, ECMAScript number text, no whitespace, error on NaN/Infinity, no duplicate names; -0 is a parser SHOULD-error per the verified errata; a Python json.dumps identity matches JCS only inside a restricted domain.
+A canonical form for hashing needs UTF-16 code-unit key order, ECMAScript number text, no whitespace, error on NaN/Infinity, no duplicate names; lane rule: -0 is a parser SHOULD-error per the verified errata; lane rule: a Python json.dumps identity matches JCS only inside a restricted domain.
```

## Judge-reason check

Yes, JudgeRecheck's S062 reason (`.ufo/waves/round-32/judge/JudgeRecheck.md:64`) misstates the cell as to “other rows” attributing the `json.dumps` clause. The teaches cell contains no row citation. A `json.dumps` search of `corpus/SOURCES.md` finds only S062 and S063; S063 does not assert the restricted-domain identity (it scopes its claim to parameters and rejects it as equivalence evidence; `corpus/SOURCES.md:69`). The reason is partly accurate only in that S062's `-0` clause says “per the verified errata”; it gives no erratum locator in the teaches cell. The closure note makes the same correction at `corpus/lessons/round-32-verifier-spotcheck.md:103` and routes the S062 issue at `:190-192`.

## Gates, touched surfaces, and limits

- Gate execution: none. I did not run the counter, judge, tests, fetches, or source-opening workflow; round-32 Recheck evidence was read, not recreated.
- Touched surface: this report only. The lane's source, evidence, lessons, and judge files were read only; no product files were edited.
- Out of scope: adjudication, changing the S062 row, verifying the external erratum, or independently testing Python serialization equivalence.
- Tool installs/updates: none.
- Artifact: `.ufo/waves/round-33/w1/ScopeS062.md`.
