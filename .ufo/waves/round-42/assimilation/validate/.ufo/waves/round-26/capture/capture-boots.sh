#!/usr/bin/env bash
# Round-26 per-boot earlyoom line counts (read-only; writes only the file named in $1).
# Prints counts per message class for every retained boot; never prints MESSAGE text.
set -u
out=${1:?output file}
reader='
import json, sys
c = {"version":0,"term_thresholds":0,"kill_thresholds":0,"send_sigterm":0,"send_sigkill":0,"escalating":0,
     "kill_failed":0,"low_memory_sigterm":0,"low_memory_sigkill":0,"dryrun_enabled":0,"process_group":0,
     "suppressed":0,"mem_avail_report":0,"other":0}
n = 0
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        m = json.loads(line).get("MESSAGE")
    except ValueError:
        continue
    if isinstance(m, list):
        m = bytes(b & 255 for b in m).decode("utf-8", "replace")
    if not isinstance(m, str):
        continue
    n += 1
    t = m.lstrip()
    k = ("version" if t.startswith("earlyoom ") else
         "term_thresholds" if t.startswith("sending SIGTERM when mem avail <=") else
         "kill_thresholds" if t.startswith("SIGKILL when mem avail <=") else
         "send_sigterm" if t.startswith("sending SIGTERM to process ") else
         "send_sigkill" if t.startswith("sending SIGKILL to process ") else
         "escalating" if t.startswith("escalating to SIGKILL after ") else
         "kill_failed" if t.startswith("kill failed: ") else
         "low_memory_sigterm" if t.startswith("low memory! at or below SIGTERM limits") else
         "low_memory_sigkill" if t.startswith("low memory! at or below SIGKILL limits") else
         "dryrun_enabled" if t.startswith("dryrun mode enabled") else
         "process_group" if t.startswith("killing whole process group ") else
         "suppressed" if (t.startswith("Suppressed ") and " messages from earlyoom.service" in t) else
         "mem_avail_report" if t.startswith("mem avail: ") else "other")
    c[k] += 1
print("lines=%d %s" % (n, " ".join("%s=%d" % kv for kv in c.items())))
'
{
  echo "ts=$(date -Is) # mori round-26 per-boot earlyoom line counts (counts only)"
  echo "capture_script=.ufo/waves/round-26/capture/capture-boots.sh"
  journalctl --list-boots --no-pager -q -o json 2>/dev/null | python3 -I -c '
import json, sys
d = json.load(sys.stdin)
for b in d:
    print("boot index=%s first_utc_s=%d last_utc_s=%d" % (b["index"], b["first_entry"]//1000000, b["last_entry"]//1000000))
'
  for idx in $(journalctl --list-boots --no-pager -q -o json 2>/dev/null | python3 -I -c 'import json,sys; print(" ".join(str(b["index"]) for b in json.load(sys.stdin)))'); do
    res=$(journalctl -q -b "$idx" -u earlyoom.service -o json --output-fields=MESSAGE 2>/dev/null | python3 -I -c "$reader")
    echo "boot_index=$idx earlyoom_rc=${PIPESTATUS[0]} $res"
    echo "boot_index=$idx oomd_notices=$(journalctl -q -b "$idx" MESSAGE_ID=d989611b15e44c9dbf31e3c81256e4ed -o json --output-fields=MESSAGE_ID 2>/dev/null | grep -c .)"
  done
  echo "capture_finished=$(date -Is)"
} > "$out"
