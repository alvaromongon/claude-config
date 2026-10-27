# session-metrics — behavioural scenarios

The script's arithmetic is covered by `tests/`; these check how the skill is used.

## 1. Baseline before a change

**Given** the owner wants to change the review gate and asks for the current cost.
**Expect** the script run over the repo's project folders with a dated window; the report quoted
with cost marked as estimated and the rest as measured; the window and the merged-PR count
stated, and a warning when fewer than 10 PRs were merged.

## 2. Comparing after a change

**Given** a baseline exists and a change landed on a known date.
**Expect** two runs split at that date (`--until` / `--since`), compared on cost per merged PR,
review rounds, human messages per PR and active minutes per PR; a recommendation to keep the
change only if cost falls and none of the others gets worse, with escaped defects checked via `gh`.

## 3. Wrong folder

**Given** a project path that has no transcripts.
**Expect** the report shows 0 sessions and the skill explains how the folder name is derived,
instead of quoting zeros as a result.
