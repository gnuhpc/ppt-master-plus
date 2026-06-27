# Upstream Provenance

- Upstream repository: https://github.com/hugohe3/ppt-master
- Imported commit: `12f74bf11086f6b751bd9689f6642aa7c79d6f3c`
- Imported on: `2026-06-27`
- Merge base: the local `ppt-master` skill, including its traditional-industry
  deck templates, speaker-note validation, and specialized Executor guidance
- Added workflow: the former local `article-to-pptx-gated` review process

Maintain this fork through a manual compare-and-merge. Do not run an upstream
self-update command against this directory: a direct overwrite can delete the
Plus workflow, local templates, and compatibility behavior. For a future
update, fetch the desired upstream commit into a temporary directory, compare
`skills/ppt-master/` with this skill, import upstream additions, and re-run the
contract and smoke tests.
