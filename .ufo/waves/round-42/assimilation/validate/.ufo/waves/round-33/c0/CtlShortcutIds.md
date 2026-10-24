NEGATIVE CONTROL C1=met: whole-gate-quote, punctuation-only; the anti-shortcut target admits these controls.

# CtlShortcutIds — frozen P-C1 / R-J controls

Axes: factual honesty; shortcut sensitivity; exact-byte restoration; sandbox containment.

- Clone: `/fast/scratch/hyaku/mori-r33/CtlShortcutIds/repo`. Frozen base: `27969134d51ea15982db4f36c77e2decd2a22b07`. No lane or fleet Git writes.
- Detector: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py`; sha256 before: `7361f3e31f4a88afc7a50a907d9c2d5b66ca98306a633760ecc40ca53fa3d942`; after: `7361f3e31f4a88afc7a50a907d9c2d5b66ca98306a633760ecc40ca53fa3d942`. The counter was never modified.
- Script: `/fast/scratch/hyaku/mori-r33/CtlShortcutIds/controls.py`; sha256: `9e823361b57ef7808e7af3b0e3a6dfea70e65df75ce6c06c8f23d0a06c208175`.
- Machine receipts and per-file hashes: `/fast/scratch/hyaku/mori-r33/CtlShortcutIds/manifest.json`; raw stdout/stderr and result JSON files are in `/fast/scratch/hyaku/mori-r33/CtlShortcutIds`.
- Installs/updates: none. A guessed queue-sysfs URL returned HTTP 404; the successful replacement was discovered from the official v6.12 Documentation/block directory listing. All source acquisitions used curl -sSL --fail -m 60.
- These are sandbox-only fixture commits, not lane changes or proposed data. The judge statements are this seat's honest actual R-J decisions, not simulated favorable responses from another judge. No other judge/model/runtime was invoked.

## Frozen and supported pristine measurements

### frozen

Commit: `27969134d51ea15982db4f36c77e2decd2a22b07`. Exact counter command:

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py 27969134d51ea15982db4f36c77e2decd2a22b07 --repo /fast/scratch/hyaku/mori-r33/CtlShortcutIds/repo
```

Full stdout:

```text
rev=27969134d51ea15982db4f36c77e2decd2a22b07 repo=/fast/scratch/hyaku/mori-r33/CtlShortcutIds/repo
entry=absent
C1=unmet
```

Exit: `1`. Stderr: `(empty)`.

### baseline

Commit: `69e5a0f23fb674fe1f4eec44f433ff628500895c`. Exact counter command:

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py 69e5a0f23fb674fe1f4eec44f433ff628500895c --repo /fast/scratch/hyaku/mori-r33/CtlShortcutIds/repo
```

Full stdout:

```text
rev=69e5a0f23fb674fe1f4eec44f433ff628500895c repo=/fast/scratch/hyaku/mori-r33/CtlShortcutIds/repo
entry=present entry_sha256=8b905505d20958dfb25b4a3324637c9449d18c6cba98f55adfa20941a5c5b650 head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=10 rows_ok=10 distinct_rows=10 short_readings=0
new_id_rows=10 new_ids=5 (S180,S181,S182,S183,S184)
S180 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/admin-guide/iostats.rst
S181 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/block/stat.rst
S182 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/admin-guide/cgroup-v2.rst
S183 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/filesystems/proc.rst
S184 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/block/writeback_cache_control.rst
gates_ok=5/5 copies_ok=5/5 fetch_ok=5/5 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=10 supported_new=10 spans_bad=[] unsupported=[]
skill_rows=4
C1=met
```

Exit: `0`. Stderr: `(empty)`.

The frozen negative is expected unmet because the entry is absent. It is not the mutation baseline. The supported pristine fixture must pass before a rejected mutant is called killed.

## Sources and honest judgments

- S180: Linux I/O statistics fields; `https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/admin-guide/iostats.rst`; fetched bytes `/fast/scratch/hyaku/mori-r33/CtlShortcutIds/iostats.src`; sha256 `f76d7ea58954ae30cc7877bd48c71c9c3265726caebca54aafbc5d6fa5086923`.
- S181: Block layer statistics; `https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/block/stat.rst`; fetched bytes `/fast/scratch/hyaku/mori-r33/CtlShortcutIds/stat.src`; sha256 `4c35b795a518ceefea985f11e53b51f71d58fc99bf5a0920ca3738f13c90cb2e`.
- S182: Control Group v2 I/O; `https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/admin-guide/cgroup-v2.rst`; fetched bytes `/fast/scratch/hyaku/mori-r33/CtlShortcutIds/cgroup-v2.src`; sha256 `ad3bd37498a57cc249326fd5c2d609669b32611fe69d126df3c3abec1539f572`.
- S183: Proc task I/O accounting; `https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/filesystems/proc.rst`; fetched bytes `/fast/scratch/hyaku/mori-r33/CtlShortcutIds/proc.src`; sha256 `4577fa50db8fadbce338af1b64535608da42316208c962aeb08f4d91fe68636e`.
- S184: Explicit volatile write back cache control; `https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/block/writeback_cache_control.rst`; fetched bytes `/fast/scratch/hyaku/mori-r33/CtlShortcutIds/writeback_cache_control.src`; sha256 `f126397f886b4ae18c9935565f5ff942ad15ab0e51731fff7e7664b8ce8e1ce3`.
- Old-id-only control: S033 from `https://docs.kernel.org/admin-guide/iostats.html`, bytes `/fast/scratch/hyaku/mori-r33/CtlShortcutIds/S033.src`, sha256 `aeef40c141be7bb8e9e94c3fa94d7088b15c564112c61e8e93191883b09346de`.

Baseline rows are paraphrases of two located quotes from each new source. Each observation is only a topic label, and report explicitly means restate the citation rather than infer an intervention or a calculated rate.

1. **Supported** — Writes completed: `The completed writes field reports the total number of successfully completed writes.` Quote: “Field 5 -- # of writes completed (unsigned long) This is the total number of writes completed successfully.”
2. **Supported** — Written sectors: `The sectors written field reports the total number of sectors written successfully.` Quote: “Field 7 -- # of sectors written (unsigned long) This is the total number of sectors written successfully.”
3. **Supported** — Stat file layout: `The stat file contains seventeen decimal values on one whitespace separated line.` Quote: “The stat file consists of a single line of text containing 17 decimal values separated by whitespace.”
4. **Supported** — Sector unit: `These sectors mean standard UNIX sectors of 512 bytes rather than a device or filesystem specific block size.` Quote: “The "sectors" in question are the standard UNIX 512-byte sectors, not any device- or filesystem-specific block size.”
5. **Supported** — IO line keys: `The lines are not ordered and use $MAJ:$MIN device numbers as their keys.` Quote: “Lines are keyed by $MAJ:$MIN device numbers and not ordered.”
6. **Supported** — Page cache writeback: `Buffered writes and shared mmaps dirty page cache, and the writeback mechanism writes it asynchronously to the backing filesystem.` Quote: “Page cache is dirtied through buffered writes and shared mmaps and written asynchronously to the backing filesystem by the writeback mechanism.”
7. **Supported** — Write syscall accounting: `This documents an attempt to count write I/O syscalls such as write() and pwrite().` Quote: “Attempt to count the number of write I/O operations, i.e. syscalls like write() and pwrite().”
8. **Supported** — Write byte accounting: `The accounting attempts to count bytes this process caused to be sent to the storage layer, at page-dirtying time.` Quote: “Attempt to count the number of bytes which this process caused to be sent to the storage layer. This is done at page-dirtying time.”
9. **Supported** — Volatile caches: `Many storage devices have volatile write back caches, especially devices in the consumer market.` Quote: “Many storage devices, especially in the consumer market, come with volatile write back caches.”
10. **Supported** — Bio flag combination: `Both REQ_PREFLUSH and REQ_FUA flags may be set together on a single bio.` Quote: “The REQ_PREFLUSH and REQ_FUA flags may both be set on a single bio.”

Every control's exact row-level actual judgments are also committed in its receipt and saved in `judgments-<control>.json` in the scratch directory.

## Mechanical label/id shortcut

Negative: source labels become observations; the Gate words are reversed and an identifier-specific exact-rate guarantee is appended. All ten rows are honestly unsupported because the quotes never assert that guarantee. Expected C1=unmet through judge support, not a forged favorable verdict.

Sandbox: `/fast/scratch/hyaku/mori-r33/CtlShortcutIds/repo`. Mutant commit: `0cabf4b51321fbea50c7d17be0bacbc15be913b6`. Changed paths: `corpus/knowledge/disk-write-rate-r33.md`, `.ufo/waves/round-33/judge/JudgeC1Rows.md`.

Exact counter command:

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py 0cabf4b51321fbea50c7d17be0bacbc15be913b6 --repo /fast/scratch/hyaku/mori-r33/CtlShortcutIds/repo
```

Full stdout:

```text
rev=0cabf4b51321fbea50c7d17be0bacbc15be913b6 repo=/fast/scratch/hyaku/mori-r33/CtlShortcutIds/repo
entry=present entry_sha256=07d9ca5fb216630505f2985136638ca0c6fc789f2d1d4eea61b442e19a7e1822 head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=10 rows_ok=10 distinct_rows=10 short_readings=0
new_id_rows=10 new_ids=5 (S180,S181,S182,S183,S184)
S180 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/admin-guide/iostats.rst
S181 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/block/stat.rst
S182 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/admin-guide/cgroup-v2.rst
S183 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/filesystems/proc.rst
S184 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/block/writeback_cache_control.rst
gates_ok=5/5 copies_ok=5/5 fetch_ok=5/5 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=0 supported_new=0 spans_bad=[] unsupported=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
skill_rows=4
unmet_conditions=judge
C1=unmet
```

Exit: `1`. Stderr: `(empty)`. Printed: **C1=unmet**. Verdict against shortcut rejection: **killed**.

Before / mutated / restored sha256 for changed files:

| file | pristine | mutated | restored |
|---|---|---|---|
| `corpus/knowledge/disk-write-rate-r33.md` | `8b905505d20958dfb25b4a3324637c9449d18c6cba98f55adfa20941a5c5b650` | `07d9ca5fb216630505f2985136638ca0c6fc789f2d1d4eea61b442e19a7e1822` | `8b905505d20958dfb25b4a3324637c9449d18c6cba98f55adfa20941a5c5b650` |
| `.ufo/waves/round-33/judge/JudgeC1Rows.md` | `6727ca9209ce0ee1064ba25c5eda69f83057c498b1ec1df354b6b5bee4aff374` | `afd8d8daf8751df5effda0fa83d314bfcb162a251932e1ff44a64a354e7c1871` | `6727ca9209ce0ee1064ba25c5eda69f83057c498b1ec1df354b6b5bee4aff374` |

Restoration commit: `3c9d0ec219d82db3ba4deece207aabe5b5bb27ed`. Full tree: `9cb6b94e3bbb148c15c1e41555077c673cb68aba`, exactly equal to pristine tree `9cb6b94e3bbb148c15c1e41555077c673cb68aba`; all tracked fixture file hashes restored exactly. Same detector on restored bytes:

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py 3c9d0ec219d82db3ba4deece207aabe5b5bb27ed --repo /fast/scratch/hyaku/mori-r33/CtlShortcutIds/repo
```

Full stdout:

```text
rev=3c9d0ec219d82db3ba4deece207aabe5b5bb27ed repo=/fast/scratch/hyaku/mori-r33/CtlShortcutIds/repo
entry=present entry_sha256=8b905505d20958dfb25b4a3324637c9449d18c6cba98f55adfa20941a5c5b650 head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=10 rows_ok=10 distinct_rows=10 short_readings=0
new_id_rows=10 new_ids=5 (S180,S181,S182,S183,S184)
S180 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/admin-guide/iostats.rst
S181 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/block/stat.rst
S182 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/admin-guide/cgroup-v2.rst
S183 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/filesystems/proc.rst
S184 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/block/writeback_cache_control.rst
gates_ok=5/5 copies_ok=5/5 fetch_ok=5/5 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=10 supported_new=10 spans_bad=[] unsupported=[]
skill_rows=4
C1=met
```

Exit: `0`. Stderr: `(empty)`.

## Whole Gate quote copied into each reading

Copying alone is supported under literal R-J: the observation is a topic label, the reading is exactly its located quote, and report is defined as restating that quote with no extra fact. R-J has no paraphrase, calculation or synthesis requirement. Expected counter behavior under literal R-J: C1=met; a negative control against the stronger anti-shortcut intent.

Sandbox: `/fast/scratch/hyaku/mori-r33/CtlShortcutIds/repo`. Mutant commit: `fad276ef9c0bb3fe6aba7234e06e23de9ae5e994`. Changed paths: `corpus/knowledge/disk-write-rate-r33.md`, `.ufo/waves/round-33/judge/JudgeC1Rows.md`.

Exact counter command:

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py fad276ef9c0bb3fe6aba7234e06e23de9ae5e994 --repo /fast/scratch/hyaku/mori-r33/CtlShortcutIds/repo
```

Full stdout:

```text
rev=fad276ef9c0bb3fe6aba7234e06e23de9ae5e994 repo=/fast/scratch/hyaku/mori-r33/CtlShortcutIds/repo
entry=present entry_sha256=7ff716fd05d880150420ae3d083e5595da3dec7729c035ed195a7677507168db head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=10 rows_ok=10 distinct_rows=10 short_readings=0
new_id_rows=10 new_ids=5 (S180,S181,S182,S183,S184)
S180 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/admin-guide/iostats.rst
S181 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/block/stat.rst
S182 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/admin-guide/cgroup-v2.rst
S183 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/filesystems/proc.rst
S184 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/block/writeback_cache_control.rst
gates_ok=5/5 copies_ok=5/5 fetch_ok=5/5 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=10 supported_new=10 spans_bad=[] unsupported=[]
skill_rows=4
C1=met
```

Exit: `0`. Stderr: `(empty)`. Printed: **C1=met**. Verdict against shortcut rejection: **survived**.

Before / mutated / restored sha256 for changed files:

| file | pristine | mutated | restored |
|---|---|---|---|
| `corpus/knowledge/disk-write-rate-r33.md` | `8b905505d20958dfb25b4a3324637c9449d18c6cba98f55adfa20941a5c5b650` | `7ff716fd05d880150420ae3d083e5595da3dec7729c035ed195a7677507168db` | `8b905505d20958dfb25b4a3324637c9449d18c6cba98f55adfa20941a5c5b650` |
| `.ufo/waves/round-33/judge/JudgeC1Rows.md` | `6727ca9209ce0ee1064ba25c5eda69f83057c498b1ec1df354b6b5bee4aff374` | `798cb70035635e623e22d84354ab3e03009ed0b94905586f32c5c98c582e94fe` | `6727ca9209ce0ee1064ba25c5eda69f83057c498b1ec1df354b6b5bee4aff374` |

Restoration commit: `9aca02a9e4bb6d5f0636c090fe5452aa3e978888`. Full tree: `9cb6b94e3bbb148c15c1e41555077c673cb68aba`, exactly equal to pristine tree `9cb6b94e3bbb148c15c1e41555077c673cb68aba`; all tracked fixture file hashes restored exactly. Same detector on restored bytes:

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py 9aca02a9e4bb6d5f0636c090fe5452aa3e978888 --repo /fast/scratch/hyaku/mori-r33/CtlShortcutIds/repo
```

Full stdout:

```text
rev=9aca02a9e4bb6d5f0636c090fe5452aa3e978888 repo=/fast/scratch/hyaku/mori-r33/CtlShortcutIds/repo
entry=present entry_sha256=8b905505d20958dfb25b4a3324637c9449d18c6cba98f55adfa20941a5c5b650 head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=10 rows_ok=10 distinct_rows=10 short_readings=0
new_id_rows=10 new_ids=5 (S180,S181,S182,S183,S184)
S180 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/admin-guide/iostats.rst
S181 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/block/stat.rst
S182 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/admin-guide/cgroup-v2.rst
S183 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/filesystems/proc.rst
S184 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/block/writeback_cache_control.rst
gates_ok=5/5 copies_ok=5/5 fetch_ok=5/5 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=10 supported_new=10 spans_bad=[] unsupported=[]
skill_rows=4
C1=met
```

Exit: `0`. Stderr: `(empty)`.

## Exactly ten rows, two with only old id S033

Rows 8 and 10 honestly cite only S033 and use its real fetched committed copy and Gate quotes. Eight rows retain new ids, and all five new ids remain cited. All ten are factually supported under R-J. Expected C1=unmet because the supported-span check requires a cited new-id copy even on the two old-only rows.

Sandbox: `/fast/scratch/hyaku/mori-r33/CtlShortcutIds/repo`. Mutant commit: `1dca256143a9ef1b3c8a6773cc23baaf3cf7a20e`. Changed paths: `corpus/knowledge/disk-write-rate-r33.md`, `.ufo/waves/round-33/judge/JudgeC1Rows.md`.

Exact counter command:

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py 1dca256143a9ef1b3c8a6773cc23baaf3cf7a20e --repo /fast/scratch/hyaku/mori-r33/CtlShortcutIds/repo
```

Full stdout:

```text
rev=1dca256143a9ef1b3c8a6773cc23baaf3cf7a20e repo=/fast/scratch/hyaku/mori-r33/CtlShortcutIds/repo
entry=present entry_sha256=562a03deb41c36b9a10f3eba5ee2fd2d146dbc3d15e66f8a08252f93d7b98b06 head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=10 rows_ok=10 distinct_rows=10 short_readings=0
new_id_rows=8 new_ids=5 (S180,S181,S182,S183,S184)
S180 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/admin-guide/iostats.rst
S181 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/block/stat.rst
S182 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/admin-guide/cgroup-v2.rst
S183 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/filesystems/proc.rst
S184 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/block/writeback_cache_control.rst
gates_ok=5/5 copies_ok=5/5 fetch_ok=5/5 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=8 supported_new=8 spans_bad=[8, 10] unsupported=[]
skill_rows=4
unmet_conditions=judge
C1=unmet
```

Exit: `1`. Stderr: `(empty)`. Printed: **C1=unmet**. Verdict against shortcut rejection: **killed**.

Before / mutated / restored sha256 for changed files:

| file | pristine | mutated | restored |
|---|---|---|---|
| `corpus/knowledge/disk-write-rate-r33.md` | `8b905505d20958dfb25b4a3324637c9449d18c6cba98f55adfa20941a5c5b650` | `562a03deb41c36b9a10f3eba5ee2fd2d146dbc3d15e66f8a08252f93d7b98b06` | `8b905505d20958dfb25b4a3324637c9449d18c6cba98f55adfa20941a5c5b650` |
| `.ufo/waves/round-33/judge/JudgeC1Rows.md` | `6727ca9209ce0ee1064ba25c5eda69f83057c498b1ec1df354b6b5bee4aff374` | `0ce1016c63a7359f1b6e464099b5c04dd6fb85621b19bf4abeaba54251c38aa3` | `6727ca9209ce0ee1064ba25c5eda69f83057c498b1ec1df354b6b5bee4aff374` |

Restoration commit: `a131bba7a363a8bd5a863da512695b6f28aed323`. Full tree: `9cb6b94e3bbb148c15c1e41555077c673cb68aba`, exactly equal to pristine tree `9cb6b94e3bbb148c15c1e41555077c673cb68aba`; all tracked fixture file hashes restored exactly. Same detector on restored bytes:

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py a131bba7a363a8bd5a863da512695b6f28aed323 --repo /fast/scratch/hyaku/mori-r33/CtlShortcutIds/repo
```

Full stdout:

```text
rev=a131bba7a363a8bd5a863da512695b6f28aed323 repo=/fast/scratch/hyaku/mori-r33/CtlShortcutIds/repo
entry=present entry_sha256=8b905505d20958dfb25b4a3324637c9449d18c6cba98f55adfa20941a5c5b650 head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=10 rows_ok=10 distinct_rows=10 short_readings=0
new_id_rows=10 new_ids=5 (S180,S181,S182,S183,S184)
S180 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/admin-guide/iostats.rst
S181 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/block/stat.rst
S182 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/admin-guide/cgroup-v2.rst
S183 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/filesystems/proc.rst
S184 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/block/writeback_cache_control.rst
gates_ok=5/5 copies_ok=5/5 fetch_ok=5/5 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=10 supported_new=10 spans_bad=[] unsupported=[]
skill_rows=4
C1=met
```

Exit: `0`. Stderr: `(empty)`.

## Ten rows differing only by trailing punctuation

Negative for ten distinct teachings: all ten rows repeat one entire S180 quote and cite the same five real new ids; only zero through nine trailing periods differ. The facts remain honestly supported. Expected anti-shortcut result C1=unmet; lexical row distinctness may instead accept all ten.

Sandbox: `/fast/scratch/hyaku/mori-r33/CtlShortcutIds/repo`. Mutant commit: `76d5c2297a34be3121ea3e486d7f9fe874e6be1c`. Changed paths: `corpus/knowledge/disk-write-rate-r33.md`, `.ufo/waves/round-33/judge/JudgeC1Rows.md`.

Exact counter command:

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py 76d5c2297a34be3121ea3e486d7f9fe874e6be1c --repo /fast/scratch/hyaku/mori-r33/CtlShortcutIds/repo
```

Full stdout:

```text
rev=76d5c2297a34be3121ea3e486d7f9fe874e6be1c repo=/fast/scratch/hyaku/mori-r33/CtlShortcutIds/repo
entry=present entry_sha256=e0325c68d2342bba32a2971bf7903ae01763ab8f3909fe15d23ad090f10ad81c head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=10 rows_ok=10 distinct_rows=10 short_readings=0
new_id_rows=10 new_ids=5 (S180,S181,S182,S183,S184)
S180 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/admin-guide/iostats.rst
S181 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/block/stat.rst
S182 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/admin-guide/cgroup-v2.rst
S183 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/filesystems/proc.rst
S184 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/block/writeback_cache_control.rst
gates_ok=5/5 copies_ok=5/5 fetch_ok=5/5 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=10 supported_new=10 spans_bad=[] unsupported=[]
skill_rows=4
C1=met
```

Exit: `0`. Stderr: `(empty)`. Printed: **C1=met**. Verdict against shortcut rejection: **survived**.

Before / mutated / restored sha256 for changed files:

| file | pristine | mutated | restored |
|---|---|---|---|
| `corpus/knowledge/disk-write-rate-r33.md` | `8b905505d20958dfb25b4a3324637c9449d18c6cba98f55adfa20941a5c5b650` | `e0325c68d2342bba32a2971bf7903ae01763ab8f3909fe15d23ad090f10ad81c` | `8b905505d20958dfb25b4a3324637c9449d18c6cba98f55adfa20941a5c5b650` |
| `.ufo/waves/round-33/judge/JudgeC1Rows.md` | `6727ca9209ce0ee1064ba25c5eda69f83057c498b1ec1df354b6b5bee4aff374` | `c68b045e8fe4deb7a8846bed6e8ed5618042afb3b8bc2918341559fa4b53951a` | `6727ca9209ce0ee1064ba25c5eda69f83057c498b1ec1df354b6b5bee4aff374` |

Restoration commit: `a1f2aaa8e09bc7c64644e484bba310ccd357a853`. Full tree: `9cb6b94e3bbb148c15c1e41555077c673cb68aba`, exactly equal to pristine tree `9cb6b94e3bbb148c15c1e41555077c673cb68aba`; all tracked fixture file hashes restored exactly. Same detector on restored bytes:

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py a1f2aaa8e09bc7c64644e484bba310ccd357a853 --repo /fast/scratch/hyaku/mori-r33/CtlShortcutIds/repo
```

Full stdout:

```text
rev=a1f2aaa8e09bc7c64644e484bba310ccd357a853 repo=/fast/scratch/hyaku/mori-r33/CtlShortcutIds/repo
entry=present entry_sha256=8b905505d20958dfb25b4a3324637c9449d18c6cba98f55adfa20941a5c5b650 head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=10 rows_ok=10 distinct_rows=10 short_readings=0
new_id_rows=10 new_ids=5 (S180,S181,S182,S183,S184)
S180 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/admin-guide/iostats.rst
S181 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/block/stat.rst
S182 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/admin-guide/cgroup-v2.rst
S183 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/filesystems/proc.rst
S184 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/block/writeback_cache_control.rst
gates_ok=5/5 copies_ok=5/5 fetch_ok=5/5 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=10 supported_new=10 spans_bad=[] unsupported=[]
skill_rows=4
C1=met
```

Exit: `0`. Stderr: `(empty)`.

## Four identical Round33 SKILL lines

Negative: the valid table and honest receipt are unchanged; the four qualifying SKILL lines are replaced by four identical copies of the first. Expected C1=unmet because normalized lines are deduplicated.

Sandbox: `/fast/scratch/hyaku/mori-r33/CtlShortcutIds/repo`. Mutant commit: `93675a8c3119382af813e2c79072549f749c066d`. Changed paths: `SKILL.md`.

Exact counter command:

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py 93675a8c3119382af813e2c79072549f749c066d --repo /fast/scratch/hyaku/mori-r33/CtlShortcutIds/repo
```

Full stdout:

```text
rev=93675a8c3119382af813e2c79072549f749c066d repo=/fast/scratch/hyaku/mori-r33/CtlShortcutIds/repo
entry=present entry_sha256=8b905505d20958dfb25b4a3324637c9449d18c6cba98f55adfa20941a5c5b650 head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=10 rows_ok=10 distinct_rows=10 short_readings=0
new_id_rows=10 new_ids=5 (S180,S181,S182,S183,S184)
S180 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/admin-guide/iostats.rst
S181 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/block/stat.rst
S182 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/admin-guide/cgroup-v2.rst
S183 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/filesystems/proc.rst
S184 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/block/writeback_cache_control.rst
gates_ok=5/5 copies_ok=5/5 fetch_ok=5/5 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=10 supported_new=10 spans_bad=[] unsupported=[]
skill_rows=1
unmet_conditions=skill_rows
C1=unmet
```

Exit: `1`. Stderr: `(empty)`. Printed: **C1=unmet**. Verdict against shortcut rejection: **killed**.

Before / mutated / restored sha256 for changed files:

| file | pristine | mutated | restored |
|---|---|---|---|
| `SKILL.md` | `ed5b75e6960495d2282d286ee5d25887a90f0d3f488b6d5f039bb22d56ddd155` | `96577520ca41c055c64f464300db04af614da7f975028b5dfb0c5120ce913a40` | `ed5b75e6960495d2282d286ee5d25887a90f0d3f488b6d5f039bb22d56ddd155` |

Restoration commit: `e172183b3f10f77dc78ee00f8f761f137e91af79`. Full tree: `9cb6b94e3bbb148c15c1e41555077c673cb68aba`, exactly equal to pristine tree `9cb6b94e3bbb148c15c1e41555077c673cb68aba`; all tracked fixture file hashes restored exactly. Same detector on restored bytes:

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py e172183b3f10f77dc78ee00f8f761f137e91af79 --repo /fast/scratch/hyaku/mori-r33/CtlShortcutIds/repo
```

Full stdout:

```text
rev=e172183b3f10f77dc78ee00f8f761f137e91af79 repo=/fast/scratch/hyaku/mori-r33/CtlShortcutIds/repo
entry=present entry_sha256=8b905505d20958dfb25b4a3324637c9449d18c6cba98f55adfa20941a5c5b650 head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=10 rows_ok=10 distinct_rows=10 short_readings=0
new_id_rows=10 new_ids=5 (S180,S181,S182,S183,S184)
S180 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/admin-guide/iostats.rst
S181 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/block/stat.rst
S182 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/admin-guide/cgroup-v2.rst
S183 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/filesystems/proc.rst
S184 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/block/writeback_cache_control.rst
gates_ok=5/5 copies_ok=5/5 fetch_ok=5/5 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=10 supported_new=10 spans_bad=[] unsupported=[]
skill_rows=4
C1=met
```

Exit: `0`. Stderr: `(empty)`.

## Four distinct eleven-word SKILL lines

Negative: the valid table and honest receipt are unchanged; each replacement line includes Round33 and the required entry path but has exactly eleven whitespace-separated words. Expected C1=unmet because the threshold is twelve.

Sandbox: `/fast/scratch/hyaku/mori-r33/CtlShortcutIds/repo`. Mutant commit: `9f48187777e23205aabf62f9ec43d288b327ce33`. Changed paths: `SKILL.md`.

Exact counter command:

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py 9f48187777e23205aabf62f9ec43d288b327ce33 --repo /fast/scratch/hyaku/mori-r33/CtlShortcutIds/repo
```

Full stdout:

```text
rev=9f48187777e23205aabf62f9ec43d288b327ce33 repo=/fast/scratch/hyaku/mori-r33/CtlShortcutIds/repo
entry=present entry_sha256=8b905505d20958dfb25b4a3324637c9449d18c6cba98f55adfa20941a5c5b650 head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=10 rows_ok=10 distinct_rows=10 short_readings=0
new_id_rows=10 new_ids=5 (S180,S181,S182,S183,S184)
S180 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/admin-guide/iostats.rst
S181 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/block/stat.rst
S182 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/admin-guide/cgroup-v2.rst
S183 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/filesystems/proc.rst
S184 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/block/writeback_cache_control.rst
gates_ok=5/5 copies_ok=5/5 fetch_ok=5/5 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=10 supported_new=10 spans_bad=[] unsupported=[]
skill_rows=0
unmet_conditions=skill_rows
C1=unmet
```

Exit: `1`. Stderr: `(empty)`. Printed: **C1=unmet**. Verdict against shortcut rejection: **killed**.

Before / mutated / restored sha256 for changed files:

| file | pristine | mutated | restored |
|---|---|---|---|
| `SKILL.md` | `ed5b75e6960495d2282d286ee5d25887a90f0d3f488b6d5f039bb22d56ddd155` | `71986589fc9686fcbaed9141f1cdd9b5875100bf5e2e9f84e8f8fdb55fe703cb` | `ed5b75e6960495d2282d286ee5d25887a90f0d3f488b6d5f039bb22d56ddd155` |

Restoration commit: `a887e454d6b4f86e8af3adce39c947caf089dd78`. Full tree: `9cb6b94e3bbb148c15c1e41555077c673cb68aba`, exactly equal to pristine tree `9cb6b94e3bbb148c15c1e41555077c673cb68aba`; all tracked fixture file hashes restored exactly. Same detector on restored bytes:

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py a887e454d6b4f86e8af3adce39c947caf089dd78 --repo /fast/scratch/hyaku/mori-r33/CtlShortcutIds/repo
```

Full stdout:

```text
rev=a887e454d6b4f86e8af3adce39c947caf089dd78 repo=/fast/scratch/hyaku/mori-r33/CtlShortcutIds/repo
entry=present entry_sha256=8b905505d20958dfb25b4a3324637c9449d18c6cba98f55adfa20941a5c5b650 head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=10 rows_ok=10 distinct_rows=10 short_readings=0
new_id_rows=10 new_ids=5 (S180,S181,S182,S183,S184)
S180 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/admin-guide/iostats.rst
S181 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/block/stat.rst
S182 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/admin-guide/cgroup-v2.rst
S183 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/filesystems/proc.rst
S184 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/block/writeback_cache_control.rst
gates_ok=5/5 copies_ok=5/5 fetch_ok=5/5 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=10 supported_new=10 spans_bad=[] unsupported=[]
skill_rows=4
C1=met
```

Exit: `0`. Stderr: `(empty)`.

## Findings and containment

Whole-quote copying is supported by the frozen rule itself; the counter cannot reject it on the ground that no paraphrase or synthesis occurred. The punctuation-only control additionally turns one repeated supported fact into ten lexically distinct rows. These are coverage/target findings, not permission to change the frozen contract. The label-keyed filler shortcut is rejected only because the honest judge marks unsupported claims unsupported. Two old-only rows meet the eight-new-row allowance but cannot satisfy the separate new-copy-span requirement for all ten supports.

Final sandbox commit `a887e454d6b4f86e8af3adce39c947caf089dd78` has exact pristine tree `9cb6b94e3bbb148c15c1e41555077c673cb68aba`. Git writes occurred only under `/fast/scratch/hyaku/mori-r33/CtlShortcutIds/repo`. No integration, shipping, lane counter edits, or surviving child process is part of this probe. Each detector and external command had timeout at most 600 seconds; each child process group is killed/reaped in finally, including failures.
