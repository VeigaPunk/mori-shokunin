# S065 fresh falsification

**Verdict: Agree with rejecting S065 as sole C2 measured-revision provenance evidence.** This is author-side falsification, not independent closure.

## Observed

- Re-opened https://docs.python.org/3/library/hashlib.html; it identifies itself as Python 3.15.0 documentation. The round-19 lesson quote at `corpus/lessons/round-19.md:43` is an exact 11-word excerpt: “This module implements a common interface to many different hash algorithms.” It appears in the public page's module introduction (`#module-hashlib`; reader extraction line 26), so the quote and its stated location are accurate.
- The S065 registry row at `corpus/SOURCES.md:71` marks the source C/rejected for sole measured-revision provenance and scopes it to hash API behavior. Its anchor cell lists the module introduction, Hash algorithms, and Hash Objects. The lesson disposition at line 43 is consistent: retain API accuracy, reject provenance support, and require separate revision linkage.
- Adverse evidence considered: the public page's BLAKE2 `Keyed hashing` section (`#keyed-hashing`; reader extraction lines 532–537) documents keyed authentication/prefix-MAC use. This can support a narrow keyed-message-authentication claim, but does not associate supplied bytes with a repository revision or establish that loaded inputs match a committed tree.

## Finding

The source's documented digest and keyed-authentication APIs do not establish measured-revision linkage. Thus the rejection as *sole* provenance evidence stands. Read broadly as claiming that `hashlib` cannot support any authentication, the rejection would be overbroad; the lesson and registry scopes avoid that claim. The registry anchor cell does not list the keyed-hashing section, a relevant caveat if the authentication boundary is discussed explicitly.

## Remaining unknown

The public documentation does not establish whether any actual receipt used keyed hashing, what it authenticated, or how receipt inputs were bound to a commit. Those require separate evidence. No tests or verification runs were performed.