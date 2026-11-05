# Mo98ScribeLesson — round-98 lesson body (draft for the L1 to integrate)

Seat: scribe, wave w1, round 98 attempt 1. Lane `mori-shokunin`. Draft only — this file is the L1's
material; it is not the lesson. The L1 integrates the two sections below into
`corpus/lessons/round-98.md`.

Scope of this seat: **the `## Gate` section (S629–S632 with located quotes, one rejected candidate)
and the `## Mistakes` section (three rows)**. Nothing else in the round was audited here.

Lane/contract facts read (never edited):

- entering `b2a67ce562bbf2f0cc73f47d8e79f792badf5e63`; freeze `b75e26ccd771b872099ef7233a61e3e91d9f6f7a`;
  landing `600deb7ed2695f54b289cf5b6c3931e0fa9c8bb3`; lane HEAD `379a2f616c146f29341987e73b2828a0ce728ce2`.
- frozen counters: `count-c1.py` sha256 `a9f140bdd53ae0a17da3bd4549d6db6cb2db68298cd97cc73f51db0e8a152e44`,
  `count-c2.py` sha256 `d6fe755fff2e2805c6550ff9bfe0b53c369d5dd8c9799fe4e02bd1e5e73c01fd`.

---

## 1. `## Gate` — draft body (L1 integrates)

New rows written this round (CORPUS rule 1). Each URL was opened 2026-11-05 and pinned under
`corpus/evidence/sources-r98/`; the pinned bytes were re-fetched live on 2026-11-05 and hash-identical
to the pins (re-fetch digests in §Evidence B). Every quote below is ≤25 words and was located
whitespace-normalized in the pinned copy; the raw-byte count is 0 for all four because each pinned
file wraps or marks up the quoted span (line break, `<i>` tag, or a tab before `=`), so a raw
substring grep would report a false miss.

| row | URL | access (UTC) | located quote (≤25 words) | decision |
|---|---|---|---|---|
| S629 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/sysctl/user.rst | 2026-11-05, 2564 B, sha256 `2a83137d…7207a` | "The maximum number of user namespaces that any user in the current user namespace may create." (16 words; pinned copy `corpus/evidence/sources-r98/S629-user.rst`, `max_user_namespaces` section, raw lines 77-78; whitespace-normalized count **2** — the identical sentence recurs under `max_uts_namespaces` at raw lines 83-84, an upstream doc copy-paste, so the *section* locates it, not the string alone) | admit, mined, tier A |
| S630 | https://man7.org/linux/man-pages/man2/unshare.2.html | 2026-11-05, 25450 B, sha256 `bc19c6eb…972a` | "doing so would have caused the limit defined by the corresponding file in /proc/sys/user to be exceeded." (17 words; pinned copy `corpus/evidence/sources-r98/S630-unshare.2.html`, ERRORS section, the third ENOSPC entry (since Linux 4.9), raw lines 254-256; the span crosses the `<i>/proc/sys/user</i>` markup, so it is located only after tag-stripping plus whitespace normalization) | admit, mined, tier A |
| S631 | https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/proc_ns.h | 2026-11-05, 2004 B, sha256 `63376480…d537` | "PROC_USER_INIT_INO = USER_NS_INIT_INO," (3 words; pinned copy `corpus/evidence/sources-r98/S631-proc_ns.h`, enum of initial namespace inodes, raw line 44; the source separates the name from `=` with a tab, so the quoted space form differs from the raw bytes by one whitespace character) | admit, mined, tier A |
| S632 | https://raw.githubusercontent.com/torvalds/linux/v7.2/include/uapi/linux/nsfs.h | 2026-11-05, 3843 B, sha256 `da2a23c3…4d65` | "USER_NS_INIT_INO = 0xEFFFFFFDU," (3 words; pinned copy `corpus/evidence/sources-r98/S632-nsfs.h`, enum of NS_INIT_INO values, raw line 50; tab before `=` as in S631) | admit, mined, tier A |

**Rejected candidate (one row, so a closure can sample it — QUALITY 60 requires a rejected row to
carry a located quote of at most 25 words; QUALITY 86 requires the reject row to name the source and
a non-empty quote):**

| row | URL | access (UTC) | located quote (≤25 words) | decision |
|---|---|---|---|---|
| S627 | https://man7.org/linux/man-pages/man7/user_namespaces.7.html | 2026-11-05, 59987 B, sha256 `276480f2…b1301b4` (byte-identical to the r95 fetch the row already records, so the page did not change since S627 was judged) | "The kernel imposes (since Linux 3.11) a limit of 32 nested levels of user namespaces." (15 words; DESCRIPTION, "Nested namespaces, namespace membership" paragraph) | reject, re-using S627 as the ground for the per-user namespace-count limit or its ENOSPC signature; the page carries **no** `/proc/sys/user` limit text at all (0 occurrences of `/proc/sys/user` and of `max_user_namespaces` in the 59987 B body), and the one limit statement it does carry (32 nested levels, `EUSERS`) is a different limit with a different errno than the per-user count limit (`ENOSPC`) that S629 and S630 already ground. S627 stays rejected for its own r95 scope, whose flip (a located mount-propagation statement) is unmet and untouched here; re-scoping a rejected row in place would break CORPUS rule 2 (only `status`, `recheck` and `used-by` may change). Flip: a located statement in `user_namespaces(7)` naming the per-user namespace-count limit or its ENOSPC failure, which would open as a **new row** for that scope, not as a re-opening of S627 |

Row changes logged old→new: none (four new rows; no existing row's `status`, `recheck` or `used-by`
changed).

### 1a. Why S627 is not re-opened here (the L1's question, answered)

- S627 was rejected in r95 for a **different scope** (mount-event non-propagation). Its recorded flip is
  "a located propagation statement in `user_namespaces(7)`"; that flip is a statement about *mount
  propagation*, so satisfying or failing it says nothing about the r98 scope.
- Re-opening it for the r98 scope would be **wrong on the merits, not merely on procedure**: the page
  has zero `/proc/sys/user` and zero `max_user_namespaces` occurrences, so it cannot carry the limit
  semantics even if its status were flipped. Its only limit sentence is the 32-nesting-level limit
  with `EUSERS` — a nesting-depth limit, not the per-user count limit, and `EUSERS` ≠ `ENOSPC`.
  Citing it for the ENOSPC signature would be a scope error of exactly the kind the r95 rejection
  recorded.
- The lane's own rule forbids the in-place edit that a re-scope would need (only `status`,
  `recheck`, `used-by` may change on an existing row; a new scope is a new row).
- So: **do not re-open S627**. If a future claim needs `user_namespaces(7)`'s own text, open a new
  row (S633) for that scope. The flip above states exactly what would make that new row worth opening.

---

## 2. `## Mistakes` — draft body (L1 integrates)

Format follows the lane convention: class · evidence pointer · captured-by · fix, and each fix says
how it was shown able to fail.

| # | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M1 | **landing** — the round's evidence landed outside the commit that claims it: two r97 seat reports were written *after* the r97 final commit, so the r97 tree at `b6d03408` did not contain the reports the r97 closure read | `corpus/lessons/round-97-verifier-spotcheck.md` §5 D1 and §1 row "no uncommitted round work" (`git status --porcelain` → ` M .ufo/waves/round-97/w1/Mo97ScoutLive.md`, ` M .ufo/waves/round-97/w1/Mo97ScribeLog.md`, mtimes 18:14:29 / 18:15:41 vs the last commit 18:14:18); `git diff --stat b6d03408 beab7bbb -- .ufo/waves/round-97/w1/` → `Mo97ScoutLive.md | 20 +++++`, `Mo97ScribeLog.md | 126 +++---` | the r97 closure (non-author integrator), routed as D1; the r98 L1 landed it as commit `beab7bbb` "round-98: r97 late-seat addendum (r97 closure D1): Mo97ScoutLive/Mo97ScribeLog writes made after the r97 final commit, committed as-is" (parent `b75e26cc`) | the writes were committed as-is as a labelled late-seat addendum rather than edited, and the rule is stated for the next round: close every seat before the final commit; a late write must land in its own labelled addendum commit, never be folded silently into a later round's commit. Shown able to fail: the r97 closure's own `git status --porcelain` was the failing instance — it printed two ` M` lines at the r97 tip and named the defect — and at the r98 tip the same command over `.ufo/waves/round-97/` prints nothing, so the check discriminates clean from dirty |
| M2 | **number-drift** — the r97 lesson's own frontier number did not match the census it cites: `corpus/lessons/round-97.md` §Frontier step reads "42 W04", while the lane's committed r97 census receipts print **43** | `corpus/lessons/round-97.md:90` ("42 W04). Census after: see the report"); `.ufo/waves/round-97/evidence/census-before.txt` and `census-after.txt` — my own count `grep -c $'\tW04\t'` → **43** in *both* files (45 and 46 lines total; `census-after.txt` adds one `$ scripts/sources-census.sh validate …` command line, which is why its line count is 46); the r97 closure flagged the same 43 in `round-97-verifier-spotcheck.md` §3 ("43 `W04` warnings (same 43 as the lane's `census-before.txt`/`census-after.txt`)") and routed it as D2 | the r97 closure (D2), not the lane — the number was wrong in the lesson the lane committed | correction of record in the r98 lesson: the r97 file is **not** edited (append-only), and the r98 lesson states the count as 43 with the command that produces it. The r98 census receipt already agrees: `.ufo/waves/round-98/evidence/census-before.txt` → `grep -c $'\tW04\t'` = 43. Shown able to fail: the count is a plain `grep -c` over a committed receipt, so a re-reader gets 43 against the lesson's 42 with no interpretation; the r98 lesson must print the number it can regenerate, not the number it remembers |
| M3 | **scope** — the pre-freeze control battery for this round's own counter was itself wrong before the freeze: the draft `count-c1.py` (sha256 `5e2223af…a74c98d` at the time of the first run) expected a redaction case that **rejected a safe value**, i.e. it forbade the marker in a `sysctl` *value* position that the tool's own contract says is printable, so the tool was judged wrong for correct behaviour. (The draft's bytes are not recoverable — no git object, no disk path — so the marker placement is taken from the L1's own account of the run and corroborated by the probe in Evidence H; the receipts below are the primary evidence and are read directly.) | `.ufo/waves/round-98/evidence/controls-draft-prefreeze-r98.txt` (untracked at this tip; sha256 `3814209a…ed9e52`) — first run: `CONTROL c1 P1-positive-candidate expect=met rc=1 UNEXPECTED :: C1=unmet cases_ok=14/15 … checks_failed=case_J6-redaction`, closing `CONTROLS_DONE unexpected=1`; every other C1 control in that run also lists `case_J6-redaction` among its failures. Frozen receipt `.ufo/waves/round-98/evidence/controls-r98.txt` (sha256 `69a77861…bd73c`): `CONTROL c1 P1-positive-candidate expect=met rc=0 AS_EXPECTED :: C1=met cases_ok=15/15 …`, `CONTROLS_DONE unexpected=0`. Both headers record `candidate-tool=5ab134ee…2db2` — the tool is unchanged across the two runs, so the difference is the counter's expectation alone | the L1's own pre-freeze battery — the first run failed on the positive control | the frozen counter plants the marker only in the `user`/`PWD` fields the tool never prints, so the redaction case tests the tool's stated posture instead of contradicting it; the frozen counter and its receipt are the committed artefacts. Shown able to fail: the battery caught it **before the freeze** — the first run's positive control was `UNEXPECTED` with `checks_failed=case_J6-redaction` and `CONTROLS_DONE unexpected=1`, i.e. the draft predicate failed a candidate that was in fact correct; and the frozen case still discriminates, since the `K11-echoes-raw-journal-line` control in `controls-r98.txt` fails `case_J6-redaction` and `case_J1-incident` as expected |

### 2a. Notes on M3 (the L1's question, answered)

- **Did the pre-freeze control battery catch it? Yes — and that is the point of the row.** The
  first run was *not* green: `P1-positive-candidate … rc=1 UNEXPECTED … checks_failed=case_J6-redaction`,
  and the run closed `CONTROLS_DONE unexpected=1`. The frozen receipt is the *second*, green run.
  The difference between the two runs is the counter's own bytes (`count-c1.py` digest recorded in the
  receipt header changed between them), and the frozen counter is the one committed at the freeze.
- **The defect was in the instrument, not the tool.** The landing tool and the candidate tool are
  byte-identical (sha256 `5ab134ee…2db2` for both, §Evidence C). The tool never changed between the
  failing and the passing control run; only the counter's expectation changed.
- **Why the draft expectation was wrong.** The tool's documented posture is "fields only: no user
  name, PWD or command text; a value outside `[A-Za-z0-9._:/-]{1,32}` prints `?`". A marker such as
  `QQMARKER` is *inside* that printable charset, so printing it is correct behaviour. A counter that
  forbids it asserts a property the tool never promised. The frozen counter instead plants the marker
  in the `user`/`PWD` fields, which the tool genuinely never emits — a true redaction property.
- **Residue worth the L1's attention:** the failing receipt
  `.ufo/waves/round-98/evidence/controls-draft-prefreeze-r98.txt` is **untracked** at this tip
  (`git status --porcelain` lists it under `??`). M3 above quotes it as evidence. If the L1 wants M3 to
  rest on committed bytes rather than a working-tree file, that file must be committed; otherwise the
  row's pointer is to a file a later reader may not find. (Flagged, not fixed — committing it is the
  L1's cut.)

---

## 3. Verification performed by this seat (all commands read-only)

All measurements were taken in scratch `/fast/scratch/hyaku/mori-r98/Mo98ScribeLesson` (removed on
exit). No lane, fleet or host state was changed; no git mutation was run in the lane.

### Evidence A — quote verification against the pinned copies (whitespace-normalized)

```
S629 S629-user.rst raw_substr= 0 norm_substr= 2 words= 16 quote= The maximum number of user namespaces that any user in the c
S630 S630-unshare.2.html raw_substr= 0 norm_substr= 1 words= 17 quote= doing so would have caused the limit defined by the correspo
S631 S631-proc_ns.h raw_substr= 0 norm_substr= 1 words= 3 quote= PROC_USER_INIT_INO = USER_NS_INIT_INO,
S632 S632-nsfs.h raw_substr= 0 norm_substr= 1 words= 3 quote= USER_NS_INIT_INO = 0xEFFFFFFDU,
```

(raw = literal byte substring; norm = whitespace-normalized, and for S630 after HTML tag-stripping.
All four raw counts are 0 because of line wrapping / `<i>` markup / tab-before-`=`; all four
normalized counts are ≥1.)

### Evidence B — live re-fetch of each pinned source, 2026-11-05

```
2a83137d76138cd8355fa6d63d0200f8a92b01aa73880c6567f81b819eb7207a  S629-user.rst
bc19c6eb79eeca98f99357c724615b87e6ede1cf8eeaa7846c432e2d2f47972a  S630-unshare.2.html
63376480b58e72b13c36b69daf536a089a2af558544863e9e2f1fe37e7ffd537  S631-proc_ns.h
da2a23c34182dec8b65bf8be116e169d0970f68907024e00c6ada4c846c04d65  S632-nsfs.h
```

Identical to the four pinned copies' digests and to the digests recorded in `corpus/SOURCES.md`
(rows S629–S632) and in the freeze receipt header.

### Evidence C — candidate tool == landing tool

```
5ab134ee036f83851eb98a9027db699a5800130c5c13598cb37aeb2abe452db2  landing/tools/mori-userns-runway.py
5ab134ee036f83851eb98a9027db699a5800130c5c13598cb37aeb2abe452db2  .ufo/waves/round-98/candidate/tools/mori-userns-runway.py
```

### Evidence D — frozen C1 counter re-run at the landing revision (independent of the committed receipt)

`python3 .ufo/waves/round-98/count-c1.py --root <tree of 600deb7e> --work <scratch>` →

```
C1=met cases_ok=15/15 selftest=ok live=ok(limit=122865,used_lb=6,state=ok) registry=met sourced=met(S629,S630,S631,S632) province=met checks_failed=- root=/fast/scratch/hyaku/mori-r98/Mo98ScribeLesson/landing
```

exit 0. (`used_lb` differs from the committed landing receipt's 8 only because it counts the host's
live processes at run time; the frozen predicate compares limit/state, not the count.)

### Evidence E — frozen C2 counter re-run at the landing revision

`python3 .ufo/waves/round-98/count-c2.py 600deb7ed2695f54b289cf5b6c3931e0fa9c8bb3 --repo <lane> --work <scratch>` →

```
C2=met mismatches=0 columns_unchanged=yes tool=ok tool_rc=0 mismatched_axes=- rev=600deb7e
```

exit 0. Matches the committed `evidence/landing-c2.txt`.

### Evidence F — receipts, copied here (the four receipts this row cites)

`evidence/before-c1.txt` (sha256 `b4cdd7ae…c671`):

```
C1=unmet cases_ok=0/15 selftest=absent live=absent registry=met sourced=unmet province=unmet checks_failed=selftest,live,sourced,province root=/fast/scratch/hyaku/mori-r98/before/t
exit=1
```

`evidence/before-c2.txt` (sha256 `e710a1bf…5b`):

```
C2=unmet mismatches=2 columns_unchanged=yes tool=ok tool_rc=1 mismatched_axes=operability,freshness rev=b2a67ce562bb
exit=1
```

`evidence/landing-c1.txt` (sha256 `977e36c0…104`):

```
rev=600deb7ed2695f54b289cf5b6c3931e0fa9c8bb3 count-c1.py sha256=a9f140bdd53ae0a17da3bd4549d6db6cb2db68298cd97cc73f51db0e8a152e44
C1=met cases_ok=15/15 selftest=ok live=ok(limit=122865,used_lb=8,state=ok) registry=met sourced=met(S629,S630,S631,S632) province=met checks_failed=- root=/fast/scratch/hyaku/mori-r98/landing/t
exit=0
```

`evidence/landing-c2.txt` (sha256 `fe010c06…62c2`):

```
rev=600deb7ed2695f54b289cf5b6c3931e0fa9c8bb3 count-c2.py sha256=d6fe755fff2e2805c6550ff9bfe0b53c369d5dd8c9799fe4e02bd1e5e73c01fd
C2=met mismatches=0 columns_unchanged=yes tool=ok tool_rc=0 mismatched_axes=- rev=600deb7ed269
exit=0
```

*(verbatim file content; the two counter digests as committed are `count-c1.py` =
`a9f140bdd53ae0a17da3bd4549d6db6cb2db68298cd97cc73f51db0e8a152e44` and `count-c2.py` =
`d6fe755fff2e2805c6550ff9bfe0b53c369d5dd8c9799fe4e02bd1e5e73c01fd`.)*

### Evidence G — M2 census count, my own count over the committed r97 receipts

```
$ grep -c $'\tW04\t' .ufo/waves/round-97/evidence/census-before.txt   → 43
$ grep -c $'\tW04\t' .ufo/waves/round-97/evidence/census-after.txt    → 43
$ wc -l .ufo/waves/round-97/evidence/census-before.txt census-after.txt → 45 46
$ grep -c $'\tW04\t' .ufo/waves/round-98/evidence/census-before.txt   → 43
$ sed -n '90p' corpus/lessons/round-97.md → "  42 W04). Census after: see the report (must be exit 0)."
```

The one extra line in `census-after.txt` is the echoed command line `$ scripts/sources-census.sh
validate --root /home/vgpnk/Projects/shokunin mori` — not a warning.

### Evidence H — M3, the mechanism, probed directly against the landing tool

The draft counter's own bytes (sha256 `5e2223af…a74c98d`) are **not recoverable** — they are in no
git object in the lane (`git cat-file --batch-all-objects` searched by digest) and on no disk path I
could reach. So the *bytes* of the draft's J6 fixture were not read. What is established, and by
which means:

- **Observed (receipts):** the draft counter's J6 case failed against the candidate tool, including
  on the positive control, and the tool bytes never changed between the failing and passing runs
  (`candidate-tool=5ab134ee…2db2` in *both* receipt headers, identical to the landing tool's digest
  in Evidence C). The defect is therefore in the counter's expectation, not in the tool.
- **Observed (frozen counter, read):** the frozen `count-c1.py` plants its J6 marker only in the
  `user`/`PWD` fields (`zzsecretuser : PWD=/home/QQMARKER`, value `hostx`) and asserts
  `"QQMARKER" not in out and "zzsecretuser" not in out` — a true property of a field-only output.
- **Observed (probe of the mechanism):** with the landing tool, a marker placed in the **value**
  position *is* printed, while a marker placed only in `user`/`PWD` is *not*. `QQMARKER` matches the
  tool's printable-value charset `^[A-Za-z0-9._:/-]{1,32}$`, so printing it is the tool's contracted
  behaviour, not a leak.

The two probes (each a one-line journal file I wrote; `rc=1` = writes found, as expected):

```
$ python3 landing/tools/mori-userns-runway.py --journal valueonly.txt     # marker only in the VALUE
SYSCTL_WRITE ts=2026-11-05T12:00:00-03:00 pid=301 key=kernel.domainname value=QQMARKER via=sysctl
SYSCTL_WRITES n=1 keys=1 userns_zero=0

$ python3 landing/tools/mori-userns-runway.py --journal userpwd.txt        # marker in user/PWD only (frozen J6 shape)
SYSCTL_WRITE ts=2026-11-05T12:00:00-03:00 pid=301 key=kernel.domainname value=hostx via=sysctl
SYSCTL_WRITES n=1 keys=1 userns_zero=0

$ python3 -c "import re;print(bool(re.match(r'^[A-Za-z0-9._:/-]{1,32}$','QQMARKER')))"   → True
```

So a counter case that forbids the marker in the *value* position asserts a property the tool never
promised, and must fail a correct tool; the frozen case asserts the property the tool does promise.
That is the difference between the two runs.

The draft receipt's failing line:

```
CONTROL c1 P1-positive-candidate expect=met rc=1 UNEXPECTED :: C1=unmet cases_ok=14/15 selftest=ok live=ok(limit=122865,used_lb=7,state=ok) registry=met sourced=met(S999) province=met checks_failed=case_J6-redaction
```

and its close `CONTROLS_DONE unexpected=1`; the frozen receipt's corresponding lines:

```
CONTROL c1 P1-positive-candidate expect=met rc=0 AS_EXPECTED :: C1=met cases_ok=15/15 selftest=ok live=ok(limit=122865,used_lb=9,state=ok) registry=met sourced=met(S999) province=met checks_failed=-
CONTROLS_DONE unexpected=0
```

and the frozen `K11` control, which still fails the redaction case:

```
CONTROL c1 K11-echoes-raw-journal-line expect=unmet rc=1 AS_EXPECTED :: C1=unmet cases_ok=13/15 … checks_failed=case_J1-incident,case_J6-redaction
```

### Evidence I — S627 live body facts (for the reject row)

Fetched 2026-11-05: `sha256 276480f2185f65ee9ca1402c233a53780dd558a77bcc30127bbb5bfafb1301b4`, 59987 B —
identical to the digest the r95 lesson records for S627 (`corpus/lessons/round-95.md` §Gate S627
entry), so the page is unchanged. In the tag-stripped, whitespace-normalized body: `/proc/sys/user`
→ 0 occurrences; `max_user_namespaces` → 0 occurrences; `propagat` → 1 (the same unrelated hit the
r95 search recorded); `mount operations` → 0; "The kernel imposes (since Linux 3.11) a limit of 32
nested levels of user namespaces." → 1 occurrence (the quote used in the reject row).

---

## 4. Checks NOT run by this seat (named, not implied)

- The r97-cited `scripts/sources-census.sh validate` was **not** re-run by this seat; the M2 count is
  a `grep -c` over the committed r97 receipts, and the r98 census was not re-run at all
  (`.ufo/waves/round-98/evidence/census-after.txt` does not exist at this tip — the draft r98 lesson
  points at it, so the L1 must produce it or amend the pointer).
- The `tools/mori-gate-registry.py --audit-all` auditor was not re-run directly; C1's
  `registry=met` conjunct came from the frozen counter, which runs it internally.
- The S630 HTML was not re-validated against the live man7 page byte-for-byte beyond the sha256
  match (which is the stronger check anyway).
- Mutation testing of either frozen counter was not run.
- No sibling lane, no fleet file and no host configuration was read or touched beyond the paths
  listed above.

## 5. Findings the L1 should weigh before integrating

1. **M3's evidence file is untracked.** `evidence/controls-draft-prefreeze-r98.txt` is the only
   artefact that shows the pre-freeze positive control failing; `git status --porcelain` lists it
   under `??`. Either commit it or re-point M3's evidence at committed bytes.
2. **The untracked draft `corpus/lessons/round-98.md` already carries the r97-D2 correction** in its
   "Frontier step — census" section, and its Gate section already states the S629–S632 rows. My §1
   Gate table differs from the draft in three measured places: the S629 quote's whitespace-normalized
   count is **2** (the sentence recurs under `max_uts_namespaces` at raw lines 83-84), the S630
   quote needs tag-stripping to locate, and the S631/S632 quotes differ from the raw bytes by a tab.
   The draft also states S627's rejection as a prose paragraph rather than a Gate table row.
   QUALITY 86 asks for the reject decision as its own row naming the source and a non-empty located
   quote; my §1 table is written in that shape. **Caveat, stated plainly:** QUALITY 86's checker as
   written also fails the lane's own committed lessons — run over `600deb7e:corpus/lessons/round-95.md`
   it prints `gate_reject_rows=0 none_declared=0 malformed=0` and exits 1, and round-96/round-97 give
   `malformed=6`/`malformed=4` and exit 1 — so this criterion is not currently enforced against the
   lane's lessons and my table's passing the checker is not evidence of a lane-wide improvement.
   Offered as a shape the L1 may adopt, not as a compliance finding.
3. **S630's recorded anchor in `corpus/SOURCES.md` says "raw lines 252-256"** while the quote's own
   span is raw lines 254-256 (line 252 is the `ENOSPC (since Linux 4.9)` heading). Not an error —
   252-256 is the ENOSPC entry including its heading — but the lesson should cite the quote's span
   (254-256) so a reader can find the string, as my §1 row does.

---

## 6. Report

`Report: .ufo/waves/round-98/w1/Mo98ScribeLesson.md`
