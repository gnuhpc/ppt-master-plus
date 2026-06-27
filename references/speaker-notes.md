# Speaker Notes Standard

Use this standard whenever generating `<project>/notes/total.md`.

## Purpose

Write a delivery-ready spoken script, not an outline, bullet recap, or restatement of visible slide text. A presenter should be able to speak naturally from the notes without inventing missing logic.

## Required Structure Per Slide

1. Open with the slide's role in the narrative or a transition from the previous slide.
2. Explain how to read the visual and the relationship among its elements.
3. Interpret the important implication, tradeoff, example, or decision. Do not merely enumerate labels.
4. Close with the takeaway and, except on the final slide, a natural bridge to the next slide.

Use connected spoken paragraphs. Avoid bullet-only notes, fragments, stage directions, and phrases such as "讲稿要点", "此处介绍", or "照着页面讲".

## Length Guidance

- Chinese decks: 300-500 Chinese characters for a normal content slide; 200-350 for a cover or section divider.
- English decks: 220-380 words for a normal content slide; 140-240 for a cover or section divider.
- Adjust for a user-specified speaking time. Prefer useful reasoning over padding.

## Content Rules

- Add information that helps delivery: definitions, causal links, examples, assumptions, risks, and business meaning.
- Explain diagrams in the order the audience should read them.
- Introduce acronyms and code identifiers in natural language; do not read code syntax mechanically.
- Keep terminology and claims consistent with the source and visible slide.
- Maintain cross-slide continuity so the deck sounds like one talk, not isolated page summaries.
- Update the notes whenever a slide's message, diagram, or wording changes materially.

## Pre-export Gate

Run:

```bash
python3 ${SKILL_DIR}/scripts/check_speaker_notes.py <project_path>
```

Fix every error before `total_md_split.py` and PPTX export. Warnings require review but may be accepted when the slide is intentionally brief.
