# Mo61ExecFetch — v7.3 source fetch verification

Read-only verification of the six frozen C2 source copies. Fetch used `curl --fail --location --silent --show-error` from each listed git.kernel.org plain URL; byte comparison used `cmp -s` against `corpus/evidence/sources-r61/<file>`. All six comparisons returned `MATCH`; no high finding.

| File | URL | Bytes | SHA-256 | Verdict | Access time (UTC) |
|---|---|---:|---|---|---|
| `psi.rst` | `https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/accounting/psi.rst?h=v7.3` | 6792 | `11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692` | MATCH | 2026-10-30T05:16:47Z |
| `psi.c` | `https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/kernel/sched/psi.c?h=v7.3` | 48860 | `c4edc1e7c18ca76e6e29668093fa0b26d4251cb088f2d5feab24681f285ec63f` | MATCH | 2026-10-30T05:16:48Z |
| `psi_types.h` | `https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/linux/psi_types.h?h=v7.3` | 5061 | `483269b27c82b438450632555aba2ba8a9c47b608243f78a029c4300b3618ccc` | MATCH | 2026-10-30T05:16:48Z |
| `cgroup-v2.rst` | `https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/admin-guide/cgroup-v2.rst?h=v7.3` | 135851 | `2750c11a6324e18f4d3a9bb63032b55f3268bd7077b80897af2f15a712611b68` | MATCH | 2026-10-30T05:16:49Z |
| `Kconfig` | `https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/init/Kconfig?h=v7.3` | 76059 | `d37de2a11baf81cbe6fb3c9ae271e5808a2c6be17f8980fe0375f6e67e677e0d` | MATCH | 2026-10-30T05:16:49Z |
| `kernel-parameters.txt` | `https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/admin-guide/kernel-parameters.txt?h=v7.3` | 319477 | `b5a13c038a27e688380bbcaa8cdbcad24543ad6b64de0c3d5709bc32c94cb39a` | MATCH | 2026-10-30T05:16:50Z |

## Reproduction evidence

Command shape (executed in seat scratch `/fast/scratch/hyaku/mori-r61/Mo61ExecFetch`; `TMPDIR` set there; scratch removed by exit trap after retaining the table above in this report):

```sh
curl --fail --location --silent --show-error "$url" -o "$dest"
wc -c < "$dest"
sha256sum "$dest"
cmp -s "$dest" "$ROOT/corpus/evidence/sources-r61/$f"
```

Captured per-file output, in table order:

```text
psi.rst | bytes=6792 | sha256=11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692 | MATCH | 2026-10-30T05:16:47Z
psi.c | bytes=48860 | sha256=c4edc1e7c18ca76e6e29668093fa0b26d4251cb088f2d5feab24681f285ec63f | MATCH | 2026-10-30T05:16:48Z
psi_types.h | bytes=5061 | sha256=483269b27c82b438450632555aba2ba8a9c47b608243f78a029c4300b3618ccc | MATCH | 2026-10-30T05:16:48Z
cgroup-v2.rst | bytes=135851 | sha256=2750c11a6324e18f4d3a9bb63032b55f3268bd7077b80897af2f15a712611b68 | MATCH | 2026-10-30T05:16:49Z
Kconfig | bytes=76059 | sha256=d37de2a11baf81cbe6fb3c9ae271e5808a2c6be17f8980fe0375f6e67e677e0d | MATCH | 2026-10-30T05:16:49Z
kernel-parameters.txt | bytes=319477 | sha256=b5a13c038a27e688380bbcaa8cdbcad24543ad6b64de0c3d5709bc32c94cb39a | MATCH | 2026-10-30T05:16:50Z
```

No tools installed. No code, counter, corpus, or VCS state modified. No blockers.
