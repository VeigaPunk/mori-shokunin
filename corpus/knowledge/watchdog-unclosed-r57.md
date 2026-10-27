source: S548 — `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-driver-liveness.py` (copy: `corpus/evidence/sources-r57/mori-driver-liveness.py`, sha256 `6b3dba74c639190e7e96b6bed8e6ac8f285a51ce6d910fbe92e6dd39bf7be997`)
verified-at: 2026-10-27; working-tree source and captured copy hash matched
recheck: `cmp tools/mori-driver-liveness.py corpus/evidence/sources-r57/mori-driver-liveness.py`

# Interpreting the driver-liveness `unclosed` diagnostic

`unclosed` is a pairing count: it counts launch keys still present in the parser's pairing list after processing the captured log. It is not a count of processes currently running, and it does not establish a lane failure or a settled/unsettled wave. The separate `in_flight` field is also only a last-event log fact. These readings are bounded to the parser grammar and bytes supplied to the probe; log truncation, omitted records, or unrecognized event text can change what remains unmatched.

| Claim | Located source quote | Interpretation / limit |
|---|---|---|
| K1 | `row["open_launches"].append(key)` (`:133`) | A parsed launch adds a pairing key; it does not query a process. |
| K2 | `close_round()` (`:143`) | A parsed completion invokes the pairing-close routine; the counter follows recognized log events. |
| K3 | `row["open_launches"].remove(key)` (`:118`) | A matching recognized close removes a key; the remaining count is grammar- and key-dependent. |
| K4 | `close_round()` (`:150`) | A parsed wrap also invokes the close routine; wrap is not a process probe. |
| K5 | `row["open_launches"] = [k for k in row["open_launches"] if k[0] != int(round_s)]` (`:157`) | A parsed dead event clears same-round pairings; the output is not simply cumulative launches minus completes. |
| K6 | `row["launch_fails"] += 1` (`:162`) | A launch-fail is counted separately and does not call the close routine in this branch. |
| K7 | `row["last_event"] == "launch"` (`:172`) | `in_flight` means the last parsed event was launch; it does not test whether the launched process still exists. |
| K8 | `"unclosed": len(row["open_launches"])` (`:173`) | `unclosed` is the current parser pairing-list length, not a present-running count. |

The parser reads the supplied log snapshot; conclusions describe those bytes, not an authenticated event stream or the live state at a later time. The probe's output is detection/report only. It does not determine authoritative swarm settlement semantics, which remain kumitate's domain.
