# ExecROMAReopen — S478 source re-open

**Attack:** S478's publisher PDF identity, quoted wording, and printed page/section attribution in the round-47 OOM entry. **Verdict: holds.**

Evidence (absolute scratch path: `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47w2-ExecROMAReopen/`):

- Command: `curl -sL -A 'Mozilla/5.0 (X11; Linux x86_64) Chrome/128.0' https://ieeexplore.ieee.org/ielx8/4629386/11644734/11540439.pdf -o /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47w2-ExecROMAReopen/roma.pdf && sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47w2-ExecROMAReopen/roma.pdf` — output SHA-256 `1603404dd25b3a0dff93f2dcb23c75b671d4e2d78da3cce8f461e87ebde6add2`; exit 0.
- Command: `pdftotext -layout /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47w2-ExecROMAReopen/roma.pdf /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47w2-ExecROMAReopen/roma.txt && rg -n -C 2 'It leverages eBPF|3016|mark_victim' /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47w2-ExecROMAReopen/roma.txt` — exit 0. Output identifies printed page `3016` at extracted line 76 and the passage at lines 122–125: “it lever- / ages eBPF to hook into OOM-related kernel tracepoints such / as mark_victim, start_task_reaping, and fin- / ish_task_reaping …”. Layout hyphenation across lines combines to the exact 20-word sentence: “It leverages eBPF to hook into OOM-related kernel tracepoints such as mark_victim, start_task_reaping, and finish_task_reaping to record OOM-triggering process metadata.”

The PDF hash matches the specified publisher full-text bytes. The quoted sentence is in the introduction on printed page 3016; the extracted line wrap/hyphenation accounts for the line split, not a wording discrepancy. No tool installs. No blockers identified.
