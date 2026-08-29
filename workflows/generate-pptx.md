---
description: Generate or redesign visible presentation pages through the frozen Plus Step 1–7 flow.
---

# Generate PPTX

This is the canonical Plus generation route. The Step 1–7 procedure, Eight
Confirmations, two blocking confirmations, `gated` / `continuous` / `split`
execution, page-by-page production, SVG Editor, Live Preview, and resume behavior
are defined in the top-level `SKILL.md` and remain unchanged.

Profiles:

- `profiles/faithful-beautify.md`: preserve wording, page order, and page count while redesigning.
- `profiles/image-to-pptx.md`: reconstruct ordered raster page frames into editable slides.

Stages:

- Source intake: `stages/topic-research.md` and `adapters/humanize-ppt-bridge.md`.
- Optional planning/execution: `stages/refine-spec.md`, `stages/resume-execute.md`.
- Optional review/output: `stages/verify-charts.md`, `stages/visual-review.md`,
  `stages/customize-animations.md`, `stages/generate-audio.md`.
- Shared infrastructure: `stages/live-preview.md`; `gated-production.md` describes
  an execution mode, not another route.

The SVG authoring constraints in `SKILL.md` apply only to this route. Native
round-trip routes do not hand-author replacement pages through this executor.
