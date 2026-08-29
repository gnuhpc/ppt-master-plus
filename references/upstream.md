# Upstream Provenance

- Upstream repository: https://github.com/hugohe3/ppt-master
- Imported commit: `d6bcaf96b7946667f4a8871b0688b903181db527` (`v5.1.0`)
- Imported on: `2026-08-29`
- Merge base: the local `ppt-master` skill, including its traditional-industry
  deck templates, speaker-note validation, and specialized Executor guidance
- Added workflow: the former local `article-to-pptx-gated` review process

Maintain this fork through a manual compare-and-merge. Do not run an upstream
self-update command against this directory: a direct overwrite can delete the
Plus workflow, local templates, and compatibility behavior. For a future
update, fetch the desired upstream commit into a temporary directory, compare
`skills/ppt-master/` with this skill, import upstream additions, and re-run the
contract and smoke tests.

## Additive capability overlay — 2026-08-29

- Source package: reviewed local `ppt-master` snapshot, metadata version `5.1.0`.
- Source commit: `d6bcaf96b7946667f4a8871b0688b903181db527`.
- Vendored runtime: `vendor/ppt-master/scripts/`, excluding `confirm_ui/`,
  `svg_editor/`, `update_repo.py`, and the runtime attribution gate.
- Integrity inventory: `vendor/ppt-master/MANIFEST.sha256`.
- References: namespaced under `references/ppt-master-core/`; upstream round-trip
  capabilities are active through the Plus routes, while upstream Quick and UI
  authorities do not replace the frozen Plus behavior.
- Templates: additive union of Brand/Style/Layout/Deck/Chart/Table/Sound/Icon
  resources. Existing Plus paths and index records win every collision.
- Collision decisions: the existing `flink_ai_style` workspace and every other
  same-ID Plus workspace stayed byte-for-byte authoritative; the upstream
  `project_schedule_table -> gantt_chart` Chart alias was dropped because Plus
  already owns a canonical `project_schedule_table` asset.
- Unified runtime: every public Plus entrypoint runs the vendored engine; SVG
  semantics and optional fields select feature behavior only, never a second
  legacy implementation.
- Validation split: existing Plus Brand/Layout/Deck workspaces are validated by
  the preserved Plus validator; the 41 imported Master Brand/Style/Layout/Deck
  workspaces are validated by the vendored current-contract validator. The
  merged Chart/Table catalog resolves all 145 canonical assets.

Future updates must repeat this selective merge. Never replace `SKILL.md`,
`scripts/confirm_ui/`, `scripts/svg_editor/`, `workflows/live-preview.md`, or
`workflows/gated-production.md`, and never overwrite a locally modified Plus
template.
