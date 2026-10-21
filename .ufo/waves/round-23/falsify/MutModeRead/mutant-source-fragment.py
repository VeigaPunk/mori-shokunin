# Exact behavior-bearing fragment from the isolated mutated scanner.
# Base: f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c
# Source: /fast/scratch/hyaku/mori-r23/MutModeRead/repo/tools/mori-quota-surface.py
# Function: scan_btrfs_sysfs; one inserted statement at mutant line 612.
# Full mutant SHA-256: 799c059e8779775c60020566945de09646bade2d3425673e515f43c2876da7c8
# This is a source fragment, not a standalone executable.
            if enabled_text == "1":
                enabled = True
                mode = btrfs_modes(read_sysfs_text(os.path.join(qgroups_path, "mode")))
            elif enabled_text == "0":
                enabled = False
