# Production Mode Workflow

Use this workflow for deck creation, restructuring, and beautification
requests. Do not use it for read-only help such as listing
templates, explaining commands, or inspecting an existing project.

## Mode Selection Gate

Before intake or source transformation, ask the user to choose exactly one
production mode, in this exact order:

1. **逐页确定精修** (`Gated`) — stop at every gate below and require explicit
   approval for each slide.
2. **全自动一次性生成** (`Continuous`) — run the normal workflow in `SKILL.md`;
   keep its required design confirmation, then continue without per-stage or
   per-slide approval.

Do not silently choose a mode. Treat a mode already stated in the user's
request as the required choice and do not ask again.

The remaining sections apply only to **逐页确定精修** (`Gated`) mode.

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

Recommend the applicable main-pipeline, `beautify`, `native-enhance-pptx`, or
`create-template` route. If a slide benefits from a companion diagram skill,
apply `references/diagram-routing.md` and include that recommendation. Wait
for the user to approve the route.

## Per-slide Gate

Generate or refine one slide at a time. For each slide:

1. Re-read `spec_lock.md` and generate the SVG.
2. Write or update its delivery-ready speaker notes.
3. Run the relevant SVG checks and show the slide in Live Preview.
4. Apply browser annotations or chat feedback and preview it again.
5. Wait for explicit approval before moving to the next slide.

Do not interpret approval of one slide as approval of later slides.

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
