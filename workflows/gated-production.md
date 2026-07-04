# Gated Production Workflow (逐页精修)

This workflow defines the per-slide approval gates for **逐页确定精修** (`Gated`) mode.
It is activated automatically when `generation_mode: "gated"` is confirmed in the
Confirm UI — do not ask the user to choose a mode in chat; the choice lives in the
Confirm UI alongside all other design parameters.

The sections below apply only when `generation_mode: "gated"` is in effect.
They are the opposite of **全自动一次性生成** (`continuous`) mode: every generated
slide is a hard user-confirmation checkpoint, and the AI must not continue to the
next slide until the current slide has been approved.

> **Entry point from Confirm UI (normal path)**: when activated by SKILL.md Step 6 after a completed Confirm UI session, the Intake / Narrative / Outline / Production Route gates have already been satisfied by the main pipeline (Steps 1–5). Jump directly to the **Per-slide Gate** below. The earlier gates apply only when a full manual Gated session is started without Confirm UI.

## Intake Gate

Collect or infer the source, language, audience, purpose, slide count, output
location, title, scenario, and any existing PPTX role. Do not accept a
user-provided PPTX as a template to fill with new material; route it as source
material, beautification input, native enhancement input, or reusable-template
creation. Present the intake summary and wait for explicit approval before
reading or transforming source content.

## Narrative Analysis Gate

Read the approved source and produce:

- one-sentence thesis;
- concise source summary;
- key concepts, components, scenarios, paths, and challenges;
- recommended audience, deck type, goal, and narrative arc;
- content to preserve, compress, merge, or omit.

Keep every claim grounded in the source. Wait for approval before outlining.

## Outline Gate

Write `<topic>_ppt_outline.md` with one section per slide: page number, title,
core message, key points, implementable visual, and speaker-note draft. Show
the path and a slide-by-slide summary. Wait for approval before production.

## Production Route Gate

Recommend the applicable main-pipeline, `faithful-beautify`, `native-enhance-pptx`, or
`create-template` route. If a slide benefits from a companion diagram skill,
apply `references/diagram-routing.md` and include that recommendation. Wait
for the user to approve the route.

## Per-slide Gate

⛔ **BLOCKING PER PAGE**: each slide is its own stop. Step 4's global design
confirmation is not approval to generate the whole deck. The AI MUST wait for
explicit user approval of slide N before starting slide N+1.

Generate or refine one slide at a time. For each slide:

1. Re-read `spec_lock.md` and generate the SVG.
2. Write or update its delivery-ready speaker notes.
3. Run the relevant SVG checks and show the slide in Live Preview.
4. If the user clicks **Apply changes** with browser annotations, the AI-side `--wait-annotation` listener must return; immediately apply those annotations even though Step 7 has not run: remove resolved markers, run the SVG quality checker, and preview the slide again. Apply chat feedback through the same check-and-preview loop.
5. Wait for explicit approval before moving to the next slide.

**Preview surface rule**: per-slide style confirmation uses Live Preview directly. Do not render a PNG/screenshot of the slide and ask a model to visually re-check it as part of the approval loop. The optional `visual-review` workflow is not a substitute for the user's per-slide approval and must not be auto-run during this gate.

Do not interpret approval of one slide as approval of later slides. Do not
generate the next SVG "while waiting"; the wait is the product behavior of
逐页精修, not an idle gap to fill.

## Speaker Notes Gate

After every slide is approved, assemble `notes/total.md` and run:

```bash
python3 ${SKILL_DIR}/scripts/check_speaker_notes.py <project_path>
```

Fix missing coverage, placeholders, weak transitions, or insufficient spoken
detail before export. Continue only when the checker reports zero errors.

## Final Acceptance Gate

Run the normal post-processing and export pipeline. Report the editable PPTX
path and confirm that:

- the source thesis remains visible;
- every slide has one core message;
- all slides contain delivery-ready notes;
- no placeholders, clipping, overlap, or unreadably small text remain;
- diagrams are understandable and their editable sidecars are preserved.

Wait for explicit final acceptance. If the user requests changes, return to
the affected slide gate, update its notes, re-run validation, and re-export.
