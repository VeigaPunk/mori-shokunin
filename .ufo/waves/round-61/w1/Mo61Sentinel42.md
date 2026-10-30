# Mo61Sentinel42 — scoped credential/source scan

## Result

**Severity: none established on the assigned surface.** No credential, private key, session transcript, credentialed URL, or private endpoint was identified in the files scanned under:

- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-61/`
- `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r61/`

**Exploit path / impact:** none established by this scan. **Smallest remediation:** none indicated for the scanned contents. This is a pattern-based negative result, not a guarantee that arbitrary encodings cannot conceal secrets. Concurrent reports arriving after the last scan are not covered.

Axes: credential exposure, source integrity, evidence accuracy. No frozen contract or counter amendment proposed.

## Scan evidence

Recursive scans covered the wave files, dispatch payloads, receipts, assimilation lists, bytecode artifacts, and the then-present `w1/` reports. The final inventory before writing this report contained 70 files across the two trees.

Executed pattern families and observed output:

| Family | Output |
|---|---|
| GitHub/GitLab, AWS AKIA/ASIA, Google API, Slack, OpenAI-shaped, npm, Hugging Face tokens | No provider-token matches identified |
| PEM private-key headers, SSH public-key payloads, JWT-shaped strings | No matches in the final combined sweep |
| Credentialed `scheme://user:password@host` URLs | No matches |
| Authorization/Cookie/X-Api-Key header forms | No credential headers identified |
| `.env*`, `.netrc`, `*.pem`, `*.key`, `*.p12`, credential-named files | No files identified |
| Session transcript markers / environment dumps | No transcripts or dumps identified |
| Zero-width/bidi codepoints in six source copies | No matches |
| Symlinks in scope | None observed |

Commands included recursive `grep` with provider-specific expressions, generic credential vocabulary, URL extraction, and a supplemental entropy sweep. The final provider/PEM/JWT sweep returned no output. The entropy sweep was heuristic and inspected its top 40 candidates; it is not exhaustive evidence of absence.

False positives inspected:

- `corpus/evidence/sources-r61/Kconfig:170-171`: `CC_HAS_ALLOC_TOKEN` / compiler allocation-token flag.
- `corpus/evidence/sources-r61/cgroup-v2.rst:809`: special token `max`.
- `corpus/evidence/sources-r61/kernel-parameters.txt:8104-8108`: USB device authorization parameter.
- `.ufo/waves/round-61/count-c3.py:44-48,166-172`: counter token names and expectation pins, not credentials.
- `Kconfig:138,152`: public LLVM commit hashes.
- `.ufo/waves/round-61/w1/Mo61RevC1.md:35`: `example.invalid` synthetic test URL, not a private service.
- `agent://all` references occur as instruction text; `xd://lsp` references are tool names, not session credentials.

The extracted URLs were public documentation, kernel, compiler, GitHub, research, and upstream project links, plus a reserved synthetic example. No embedded authentication or private URL was identified. Absolute local paths disclose workspace layout, which is already explicit in the assignment; no credential value was found in those paths.

`w1/swarm-registry.json` was mode 0600 and contained roster metadata with null agent IDs when inspected, not authentication material.

## Source integrity — independently fetched upstream bytes

All six local SHA-256 values match both the frozen `count-c2.py:29-35` PINS and the bytes read from freeze revision `7370a731abcafc4c803111de7c22cd6264d63be1`:

```text
psi.rst              11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692
psi.c                c4edc1e7c18ca76e6e29668093fa0b26d4251cb088f2d5feab24681f285ec63f
psi_types.h          483269b27c82b438450632555aba2ba8a9c47b608243f78a029c4300b3618ccc
cgroup-v2.rst        2750c11a6324e18f4d3a9bb63032b55f3268bd7077b80897af2f15a712611b68
Kconfig              d37de2a11baf81cbe6fb3c9ae271e5808a2c6be17f8980fe0375f6e67e677e0d
kernel-parameters.txt b5a13c038a27e688380bbcaa8cdbcad24543ad6b64de0c3d5709bc32c94cb39a
```

I independently fetched all six public URLs under
`https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/`
with `?h=v7.3`, using `curl --fail --location --silent --show-error --max-time 90`, and compared their SHA-256 values to the local copies. **All six returned UPSTREAM-MATCH.** Paths used:

```text
Documentation/accounting/psi.rst
kernel/sched/psi.c
include/linux/psi_types.h
Documentation/admin-guide/cgroup-v2.rst
init/Kconfig
Documentation/admin-guide/kernel-parameters.txt
```

This establishes byte identity with the content served by those upstream URLs during this seat, not an independent signed-tag verification.

### Three spot-opens

- `corpus/evidence/sources-r61/psi.rst:1-60`: PSI RST anchor/title, April 2018 date, Johannes Weiner authorship, and pressure-interface documentation.
- `corpus/evidence/sources-r61/psi.c:1-45`: GPL-2.0 SPDX header, Facebook/Google copyright and upstream authorship, SOME/FULL model commentary.
- `corpus/evidence/sources-r61/psi_types.h:1-60`: GPL-2.0 SPDX header, Linux header guard/includes, task-state/resource enums.

These are kernel-source contents, not HTML access-denial pages or generated placeholder files. Upstream byte identity is the substantive pristine-copy evidence.

All six files ended in a newline and had no NUL bytes detected. Non-ASCII source lines were limited to an upstream right apostrophe in `cgroup-v2.rst:450` and en dashes in `kernel-parameters.txt:5283-5285`; the upstream comparison covers those bytes too.

## Non-findings / exclusions

- `file(1)` calls `evidence/control-c3-do-nothing.txt` a Clarion encrypted data file and `assimilation/reg-ids` an S-record. These are heuristic misclassifications: the former is the plain-text `C3=unmet …` receipt; both files passed the ASCII-content check. No encrypted payload was established.
- Local `__pycache__` files were gitignored and absent from the freeze tree. Recursive comparison of their code/constant structures to the source found equality for all three counters. No stale-cache defect was established on the frozen execution path. Generic scratch bytecode experiments do not establish a round-61 defect.
- A direct scratch `git show --output=…` experiment demonstrated Git's normal output-option behavior. It did **not** establish a counter exploit, credential exposure, or repo-controlled option injection. Counter-level tests used an unsuitable default repository and cannot support that claim. No finding is asserted from them.
- Source identity between release tags does not prove how a ledger author performed a recheck. No judgment of C2 acceptance, freshness, or closure is made here.

## Execution and cleanup

Read frozen contract and operator RULES first. Disk guard returned rc=0 with scratch 370.3G free (54% used); no ENOSPC.

No tools installed/upgraded. Used existing Python 3.14.8, Git, curl, hashing and text tools. No credential helper was invoked intentionally and no credential value was obtained. No counter, contract, registry, corpus, production file, or lane/fleet VCS state was edited.

Additional scratch-only fixtures were created for the excluded experiments above; those included local Git init/add/commit operations with throwaway identity, never lane/fleet Git mutation. They are not acceptance evidence for this seat's scoped result.

Scratch `/fast/scratch/hyaku/mori-r61/Mo61Sentinel42/` was removed; tool output confirmed `scratch removed`. Only this report remains. No remediation applied. No build/test/closure judgment performed.
