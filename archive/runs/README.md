# archive/runs/

Run-level snapshots that are not the active canonical reporting run.

Structure:

- `<run-id>/predictions/`: prediction files for that run snapshot.
- `<run-id>/results/`: full results tree for that run snapshot.

Policy:

- Keep active canonical reporting artifacts in `predictions/runs/` and `results/runs/`.
- Move equivalent verification or superseded runs here to keep active paths easy to read.
