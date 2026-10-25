# ExecLiveRefetch — C2 source freshness

Scope: re-fetch the four Linux v7.2 source files assigned and compare SHA-256 with the committed copies. No tools were installed or updated.

## Evidence

All outputs below were observed directly; commands ran from `/home/vgpnk/Projects/shokunin/mori-shokunin`.

- `curl -fLsS https://raw.githubusercontent.com/torvalds/linux/v7.2/<path>` saved each file under `.scratch/r47-ExecLiveRefetch/<path>`; loop exited 0.
- `sha256sum .scratch/r47-ExecLiveRefetch/{include/trace/events/oom.h,mm/oom_kill.c,mm/page_alloc.c,fs/proc/base.c}` exited 0:

  ```text
  82f04ad4108ba9499b638fe298967f124269c0a2feb6ddbb14b1ade59c974e0d  include/trace/events/oom.h
  452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e  mm/oom_kill.c
  439ae8ec1e47cbf38770865e53e98bf2229e32a20c4b0f8178e6f19f34edbc50  mm/page_alloc.c
  cef1a2cf3f34f683e69d623c4df563d5c0dc6bd71dcb3d42f40dadb0084915c6  fs/proc/base.c
  ```

- Initial committed-path check using source directory names exited 1: the copies are flat filenames, not nested paths. Corrected `sha256sum corpus/evidence/sources-r47/{include_trace_events_oom.h,mm_oom_kill.c,mm_page_alloc.c,fs_proc_base.c}` exited 0 and returned the identical four hashes, respectively. Thus all four committed copies match their live v7.2 raw fetches.
- `git ls-remote https://github.com/torvalds/linux refs/tags/v7.2 'refs/tags/v7.2^{}'` exited 0:

  ```text
  237a1c39e8dfd3e1c6f1f023eea37a48ec04cc63 refs/tags/v7.2
  8d3ae59288f1e7d58d76558a6ee96d533bc5019f refs/tags/v7.2^{}
  ```

  Annotated tag resolves to commit `8d3ae59288f1e7d58d76558a6ee96d533bc5019f`.

## Risks / blockers

Freshness is verified against the live `v7.2` URL and all four hashes match. The tag resolution is the source anchor for S475/S476. No other risks or blockers observed.
