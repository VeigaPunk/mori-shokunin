# Round 98 — lesson (mori, L1 MoriR98, attempt 1)

Entering `b2a67ce562bbf2f0cc73f47d8e79f792badf5e63` (r97 admitted). Frozen contract `.ufo/waves/round-98/contract.md`
at freeze `b75e26ccd771b872099ef7233a61e3e91d9f6f7a`, with every control (do-nothing, forgery through the tool's
public CLI, positive) executed and committed first: `.ufo/waves/round-98/evidence/controls-r98.txt`
(`CONTROLS_DONE unexpected=0`, 19 lines `AS_EXPECTED`). Landing `600deb7ed2695f54b289cf5b6c3931e0fa9c8bb3`.

## Claims (frozen)

- **C1 coverage, capability acquisition** — `tools/mori-userns-runway.py`: user-namespace runway read
  (limit vs distinct non-initial namespaces on readable process links; ok/low/exhausted; limit 0 = exhausted) and a
  sudo-journal scan for kernel-tunable writes. New ground: at entering no PROVINCE line, tool or knowledge entry
  named user namespaces. Before `C1=unmet cases_ok=0/15`; landing `C1=met cases_ok=15/15 ... checks_failed=-`.
- **C2 calibration** — SCORECARD `## Axes` Last-change cells for operability and freshness lead with the admitted
  r97 closure (MANIFEST rounds[1384]). Before `C2=unmet mismatches=2`; landing `C2=met mismatches=0`.

## Gate

New rows written this round (CORPUS rule 1), all opened 2026-11-05 by the L1 (fetch log
`.ufo/waves/round-98/contract.md` era; HTTP 200 each), pinned at `corpus/evidence/sources-r98/`:

| row | URL | access (UTC) | located quote (≤25 words) | decision |
|---|---|---|---|---|
| S629 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/sysctl/user.rst | 2026-11-05T21:30:51Z, 2564 B, sha256 `2a83137d…7207a` | "The maximum number of user namespaces that any user in the current user namespace may create." (lines 77-78, 16 words) | admit, mined, tier A |
| S630 | https://man7.org/linux/man-pages/man2/unshare.2.html | 2026-11-05T21:30:52Z, 25450 B, sha256 `bc19c6eb…972a` | "doing so would have caused the limit defined by the corresponding file in /proc/sys/user to be exceeded." (raw lines 254-256, 17 words) | admit, mined, tier A |
| S631 | https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/proc_ns.h | 2026-11-05T21:30:52Z, 2004 B, sha256 `63376480…d537` | "PROC_USER_INIT_INO = USER_NS_INIT_INO," (line 44, tab before `=`, 3 words) | admit, mined, tier A |
| S632 | https://raw.githubusercontent.com/torvalds/linux/v7.2/include/uapi/linux/nsfs.h | 2026-11-05T21:30:58Z, 3843 B, sha256 `da2a23c3…4d65` | "USER_NS_INIT_INO = 0xEFFFFFFDU," (line 50, tab before `=`, 3 words) | admit, mined, tier A |

Rejected this round: re-using S627 (user_namespaces(7), rejected r95 for mount-propagation scope) as the ground for
the limit semantics. Reason: the limit and its charging rule are stated by the kernel's own sysctl documentation
(S629, tier A, the file that defines the knob), and S627's row is a rejection for another scope; re-scoping it in
place would break CORPUS rule 2 (only status/recheck/used-by change). Flip: a claim that needs user_namespaces(7)'s
own text (e.g. the capability model inside a namespace) would open it as a new row for that scope.

Row changes logged old→new: none (four new rows; no existing row's status, recheck or used-by changed).

Assimilation: none this round (no `merge/mori/` theme fits user-namespace runway or the calibration cells).
considerthese: `considerthese/2026-11-05.md` proposals 1–5 read; none taken (proposal 4, a sibling host-literal
sweep, is report-only and outside both claims).

## Frontier step — census

Round start (`.ufo/waves/round-98/evidence/census-before.txt`): `mori ok`, exit 0, 43 `W04` warnings, 400 rows.
Round end: see `.ufo/waves/round-98/evidence/census-after.txt`.
Correction of record (r97 closure D2): `corpus/lessons/round-97.md` §Frontier step says "42 W04"; the census and the
r97 receipts print 43 (`grep -c W04 .ufo/waves/round-97/evidence/census-before.txt` → 43). The r97 file is not edited.
Gate wording notes from the wave (`w1/Mo98ScribeLesson.md` §5, `w1/Mo98ScoutSrc.md`): the S629 quote also occurs, word
for word, under `max_uts_namespaces` (raw lines 83-84); the located instance is the `max_user_namespaces` section
(lines 77-78). The S630 quote spans raw lines 254-256 (line 252 is the entry's heading) and locates only after tags
are stripped. The S631/S632 quotes have a tab before `=` in the raw bytes. The four rows re-opened live by
`Mo98ScoutSrc`: byte-identical to the pins, verdict `supported` ×4. The S631 teaches cell goes one inference step
beyond the file's text: the file only names the constant, and the host's `user:[4026531837]` link supplies the rest.

## Wave findings (w1, 13 seats, 0 dead)

- C1 tool genuine: live delta +3 with three `unshare -Ur` holders, nested chain, low state, journal scan of the day
  (`w1/Mo98ExecTrial.md`); `used_lb` = lsns distinct non-initial count, 6 = 6 (`w1/Mo98ScoutHost.md`); mutation
  13/14 killed, survivor m03 (used > limit clamping; no fixture exercises it) (`w1/Mo98MutC1.md`); review holds
  with classifier gaps F1–F3 documented (`w1/Mo98RevC1.md`); fd-held namespace invisible, lower-bound wording
  confirmed (`w1/Mo98CritLB.md`, H holds).
- C1 counter defect: a fixture-shape lookup stub passes the frozen counter, `cases_ok=15/15`, and the live leg
  checks only the limit echo (`w1/Mo98CritC1.md`, VERDICT needs-amend). The claim stays as frozen. Post-hoc, outside
  the claim, the randomized check `xcheck-random-r98.py` passes the landing tool and fails the constant stub
  (`evidence/xcheck-random-r98.txt`). New QUALITY 209.
- C2 holds (`w1/Mo98CritC2.md`, `w1/Mo98RevC2.md`, `w1/Mo98ExecCalib.md`). Framing note (RevC2): the gate checks
  the Last-change cells against the fleet MANIFEST. The freshness and operability Evidence cells still cite older
  closures, and the instrument pins those cells to base `66c5518e`, so it cannot move them. Routed.
- The incident's bwrap ENOSPC text is not in the journal (`w1/Mo98ScoutHost.md`), so the knowledge entry keeps "not
  captured".
- Adjacency: no sibling owns this detection; routes go to tsukuroi (repair) and the operator (sysctl policy)
  (`w1/Mo98ConnSibling.md`).

## Mistakes (CORPUS: class · evidence · captured-by · fix)

| # | class | evidence | captured-by | fix |
|---|---|---|---|---|
| 1 | landing | r97 seat reports `Mo97ScoutLive.md`/`Mo97ScribeLog.md` changed after the r97 final commit (`corpus/lessons/round-97-verifier-spotcheck.md` §5 D1) | the run-10 rule "file only after WAVE-DONE"; r97 committed its final receipts before every seat's last write | committed as a labelled addendum `beab7bbb`. This round runs `git status --porcelain .ufo/waves/round-98` after WAVE-DONE and before the final commit. Shown able to fail: at r98 entering the same command listed 2 modified files |
| 2 | number-drift | `corpus/lessons/round-97.md:90` says 42 W04; `grep -c W04 .ufo/waves/round-97/evidence/census-before.txt` → 43 | none: a number written without its command (CORPUS "a count carries its command") | correction of record above. This lesson's census numbers carry their command. Shown able to fail: the r97 line printed 42 against a command that prints 43 |
| 3 | vacuous | first pre-freeze control run: `P1-positive-candidate ... UNEXPECTED ... checks_failed=case_J6-redaction`, `CONTROLS_DONE unexpected=1` (`.ufo/waves/round-98/evidence/controls-draft-prefreeze-r98.txt`); the draft counter planted the redaction marker in a printable value | the positive control (QUALITY 206) caught it before the freeze | the frozen counter plants the marker only in the user/PWD fields, and K11 (raw-line echo) proves the case still discriminates. Shown able to fail: the draft receipt |
| 4 | survivor | a fixture-shape lookup stub passes the frozen `count-c1.py` (`w1/Mo98CritC1.md`); mutant m03 survives the battery (`w1/Mo98MutC1.md`) | none before this round. K1 was a constant printer, not a per-fixture lookup | QUALITY 209 plus the post-hoc randomized check. Shown able to fail: the stub passes the frozen counter, and the constant stub scores 0/40 under the randomized check |

## Census at round end

`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` → see
`.ufo/waves/round-98/evidence/census-after.txt` (rows `grep -cE '^ {0,3}\| *S[0-9]{3,}' corpus/SOURCES.md`: 400 → 404).
