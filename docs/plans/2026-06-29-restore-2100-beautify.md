# Restore 2.10-Style PPTX Beautification Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Make `ppt-master-plus` beautify ambiguous PPTX requests with the same high-quality, re-architecting main-pipeline behavior as `ppt-master` v2.10.0, while keeping plus-only capabilities available when explicitly requested.

**Architecture:** Treat "beautify / optimize / make professional" as a request to rebuild the deck from extracted PPTX content through the main Strategist pipeline by default. Keep the current strict 1:1, verbatim, source-master-preserving flow as an explicit `faithful-beautify` route only when the user asks for unchanged page count/order/wording or source master preservation.

**Tech Stack:** Markdown skill/workflow contracts, existing `ppt_to_md.py` and `pptx_intake.py` source extraction, Confirm UI, `spec_lock.md`, SVG-to-PPTX exporter, pytest contract tests.

---

## Current Diagnosis

`ppt-master` v2.10.0 has no `workflows/beautify-pptx.md` and no PPTX Route Boundary. Existing PPTX files enter the normal source-processing pipeline: `ppt_to_md.py` extracts content, then Strategist freely chooses page count, story structure, page rhythm, style, images, and charts.

`ppt-master-plus` currently inherits the v2.11.0-style strict beautify route. The files that impose this behavior are:

- `/Users/gnuhpc/projects/skills/ppt-master-plus/SKILL.md`
- `/Users/gnuhpc/projects/skills/ppt-master-plus/workflows/beautify-pptx.md`
- `/Users/gnuhpc/projects/skills/ppt-master-plus/references/strategist.md`
- `/Users/gnuhpc/projects/skills/ppt-master-plus/references/executor-base.md`
- `/Users/gnuhpc/projects/skills/ppt-master-plus/templates/spec_lock_reference.md`
- `/Users/gnuhpc/projects/skills/ppt-master-plus/scripts/confirm_ui/static/app.js`
- `/Users/gnuhpc/projects/skills/ppt-master-plus/scripts/tests/test_skill_contract.py`

The strict route makes output worse for ordinary "美化 PPT" because it freezes the source page count/order/wording and defaults to source palette/fonts/master preservation. That preserves source defects instead of rebuilding a better deck.

## Target Behavior

Default PPTX beautification should behave like v2.10.0:

- Ambiguous "美化 / 优化 / 更专业 / polish this deck" means "treat the PPTX as source material and rebuild".
- Strategist may split, merge, drop, reorder, re-title, and synthesize slides from the extracted content.
- Source identity from `pptx_intake.py` is a reference, not a constraint.
- Page count is recommended, not locked.
- `content_divergence` is surfaced so the user can choose close / balanced / free restructuring.
- `preserve_master` is not used in the default beautify path.

Strict source-faithful beautification remains available only for explicit requests:

- "页数不变"
- "页面顺序不变"
- "文字一字不改"
- "保留原母版/版式"
- "我要贴回原模板"
- equivalent English wording such as "preserve wording/page count/source master"

## Task 1: Change PPTX Routing Contract

**Objective:** Make main-pipeline rebuild the default route for ambiguous PPTX beautification.

**Files:**

- Modify: `/Users/gnuhpc/projects/skills/ppt-master-plus/SKILL.md`
- Test: `/Users/gnuhpc/projects/skills/ppt-master-plus/scripts/tests/test_skill_contract.py`

**Step 1: Update the workflow index language**

In `Standalone Workflows`, change the `beautify` row from the current strict description to an explicit source-faithful route:

```markdown
| `faithful-beautify` | `workflows/beautify-pptx.md` | Explicit source-faithful re-layout for existing PPTX decks — preserve page count/order/wording and optionally source master/layouts. Not the default for generic "beautify". |
```

Do not rename the file yet unless the repo has no callers depending on `workflows/beautify-pptx.md`. Keep the file path stable in this task.

**Step 2: Replace `PPTX Route Boundary`**

Replace the current table with:

```markdown
| User intent | Route | Contract |
|---|---|---|
| Generic beautify / optimize / make professional, no explicit preservation constraints | Main pipeline | Treat PPTX as source material via `ppt_to_md` + `pptx_intake`; Strategist may re-architect page count, order, titles, structure, rhythm, and visual system |
| Explicitly preserve page count/order/wording and only improve layout/spacing | `faithful-beautify` | Strict 1:1 source slide mapping; text/data values frozen; source identity may be inherited after confirmation |
| Keep original master/layout/chrome or paste elements back into the source deck | `faithful-beautify` with `preserve_master` | Output slide N preserves source slide N layout/master mapping |
| Harvest the deck as a reusable future template | `create-template` | Build a template package, not a one-off generated deck |
| Keep the finished deck visually stable and append native optimizations | `native-enhance-pptx` | Patch enhancement metadata/media directly in OOXML; no SVG generation |
```

**Step 3: Replace the ambiguity rule**

Remove the current "Ambiguous requests ... MUST be clarified" wording. Add:

```markdown
Ambiguous requests such as "make this PPT more professional", "美化这份 PPT", or "optimize this deck" default to the main pipeline. Ask a clarification question only when the user mentions preservation but not enough to know which invariant matters. The default assumption is: improve the deck, not preserve the source author's slide breakdown.
```

**Step 4: Run contract checks**

Run:

```bash
cd /Users/gnuhpc/projects/skills/ppt-master-plus
python3 -m pytest scripts/tests/test_skill_contract.py -q
```

Expected: tests may fail if they assert the old strict route. Update those assertions in Task 7.

## Task 2: Reframe `beautify-pptx.md` As Explicit Faithful Mode

**Objective:** Keep the strict route, but make it opt-in and stop it from capturing generic beautify requests.

**Files:**

- Modify: `/Users/gnuhpc/projects/skills/ppt-master-plus/workflows/beautify-pptx.md`

**Step 1: Change title and trigger**

Change the heading to:

```markdown
# Faithful Beautify PPTX (Explicit 1:1 Re-layout)
```

Replace the trigger block with:

```markdown
**Trigger**: the user supplies a `.pptx` and explicitly asks to preserve one or more source invariants: page count, page order, per-slide wording, original master/layout, or paste-back compatibility. Generic "beautify / optimize / make professional" does not trigger this workflow; route those requests to the main SKILL.md pipeline.
```

**Step 2: Add a top warning**

Add near the top:

```markdown
> This workflow is intentionally conservative. It exists for source-faithful repair, not best-possible deck redesign. If the user wants the deck to look substantially better and did not require 1:1 preservation, use the main pipeline.
```

**Step 3: Remove generic examples**

Move "把这份 PPT 美化一下" and "make this deck look better" out of this workflow's positive examples. Replace them with examples containing preservation constraints:

```markdown
| Existing `.pptx` + explicit unchanged wording | "美化一下，但每页文字不要改" |
| Existing `.pptx` + exact page count/order | "页数和顺序保持不变，只重新排版" |
| Existing `.pptx` + source master | "保留原母版和版式，内容层重排" |
```

## Task 3: Restore 2.10-Style Main Pipeline For PPTX Inputs

**Objective:** Ensure the main pipeline uses PPTX intake as factual context only, not as replica constraints.

**Files:**

- Modify: `/Users/gnuhpc/projects/skills/ppt-master-plus/SKILL.md`
- Modify: `/Users/gnuhpc/projects/skills/ppt-master-plus/references/strategist.md`

**Step 1: Keep `pptx_intake.py`, but clarify ownership**

In `SKILL.md` Step 2 and Step 4, keep the `analysis/source_profile.json` language, but emphasize:

```markdown
For generic PPTX beautification, `analysis/source_profile.json` is context only. It may suggest canvas, chart/table presence, source images, and brand signals, but it must not lock page count, slide order, text wording, source palette, fonts, or master/layout preservation. The Markdown extracted by `ppt_to_md.py` is the content source; Strategist rebuilds the deck.
```

**Step 2: Add main-pipeline PPTX default to `strategist.md`**

Near the source-handling section, add:

```markdown
- Generic PPTX beautification / optimization routed through the main pipeline → treat the source deck as material to improve, not a finished slide breakdown to preserve. Use `sources/<stem>.md` for content, `analysis/source_profile.json` for factual context, and the user's `content_divergence` to decide how closely to follow the source. You may merge, split, drop, reorder, retitle, and reframe pages when it improves the story. Source palette/fonts are candidates, not truth.
```

**Step 3: Keep explicit faithful exception**

Keep the existing strict beautify paragraph, but rename it:

```markdown
- Faithful beautify workflow (`workflows/beautify-pptx.md`) → ...
```

This prevents the strict rule from applying to generic beautification.

## Task 4: Make Confirm UI Support The New Default

**Objective:** Ensure generic PPTX beautification gets the same two-tier creative choice flow as normal v2.10-style generation.

**Files:**

- Modify: `/Users/gnuhpc/projects/skills/ppt-master-plus/SKILL.md`
- Modify: `/Users/gnuhpc/projects/skills/ppt-master-plus/scripts/confirm_ui/static/app.js` only if tests or UI copy still imply locked beautify by default.

**Step 1: Use `content_divergence` on generic PPTX beautify**

Confirm the main pipeline already surfaces `content_divergence` in Tier 1. Add one sentence in `SKILL.md`:

```markdown
For generic PPTX beautification, `content_divergence` is the primary control for how close the rebuilt deck stays to the source. Blank means balanced redesign.
```

**Step 2: Hide locked page count unless faithful mode is active**

In `app.js`, keep page-count locking only when recommendations contain `page_count.locked === true`. Generic main-pipeline recommendations should write page count as a normal editable/range field.

**Step 3: Do not show `preserve_master` unless present**

The app already checks for `recommend.preserve_master` / `preserve_master`. Keep that behavior. Do not add `preserve_master` to main-pipeline recommendations.

## Task 5: Remove Preserve-Master Influence From Default Generation

**Objective:** Prevent master-preservation rules from biasing ordinary beautification into sparse overlays.

**Files:**

- Modify: `/Users/gnuhpc/projects/skills/ppt-master-plus/references/executor-base.md`
- Modify: `/Users/gnuhpc/projects/skills/ppt-master-plus/templates/spec_lock_reference.md`
- Modify: `/Users/gnuhpc/projects/skills/ppt-master-plus/SKILL.md`

**Step 1: Scope preserve-master rules to faithful mode**

In `executor-base.md`, keep all `preserve_master=true` rules, but add a clear guard:

```markdown
These rules apply only when `spec_lock.md` explicitly sets `preserve_master: true`. Generic PPTX beautification through the main pipeline must not set this flag and should generate complete slide backgrounds and visual systems normally.
```

**Step 2: Spec lock reference**

In `templates/spec_lock_reference.md`, make `preserve_master` optional and faithful-only:

```markdown
> `preserve_master` is omitted in normal/main-pipeline projects. Only faithful PPTX beautify writes it.
```

**Step 3: Export docs**

In `SKILL.md` Step 7, keep the `Beautify + preserve_master` export note, but retitle:

```markdown
> **Faithful beautify + preserve_master**
```

## Task 6: Decide Whether To Keep Or Retire The `beautify` Name

**Objective:** Avoid future agents routing generic "美化" into strict 1:1 mode because the workflow is named `beautify`.

**Files:**

- Modify: `/Users/gnuhpc/projects/skills/ppt-master-plus/SKILL.md`
- Optionally add: `/Users/gnuhpc/projects/skills/ppt-master-plus/workflows/faithful-beautify-pptx.md`

**Recommended path:** Keep the existing filename for compatibility, but change all user-facing labels to `faithful-beautify`.

Do not create a second duplicate workflow unless external callers require a new file path. Duplicate workflows are likely to drift.

## Task 7: Add Contract Tests For Routing Semantics

**Objective:** Lock in the new behavior so future syncs from v2.11-style logic do not regress it.

**Files:**

- Modify: `/Users/gnuhpc/projects/skills/ppt-master-plus/scripts/tests/test_skill_contract.py`

**Test cases to add or update:**

1. Generic beautify defaults to main pipeline:

```python
def test_generic_pptx_beautify_defaults_to_main_pipeline():
    skill = Path("SKILL.md").read_text()
    assert "Ambiguous requests" in skill
    assert "default to the main pipeline" in skill
    assert "Preserve → `beautify`; restructure → main pipeline" not in skill
```

2. Faithful beautify requires explicit preservation:

```python
def test_faithful_beautify_requires_explicit_preservation():
    workflow = Path("workflows/beautify-pptx.md").read_text()
    assert "explicitly asks to preserve" in workflow
    assert "Generic \"beautify / optimize / make professional\" does not trigger" in workflow
```

3. Main-pipeline PPTX facts are not constraints:

```python
def test_pptx_intake_is_context_not_constraint_for_generic_beautify():
    skill = Path("SKILL.md").read_text()
    assert "context only" in skill
    assert "must not lock page count" in skill
```

Run:

```bash
cd /Users/gnuhpc/projects/skills/ppt-master-plus
python3 -m pytest scripts/tests/test_skill_contract.py -q
```

Expected: all tests pass.

## Task 8: Update User-Facing Best Practices

**Objective:** Align docs with the new routing contract.

**Files:**

- Modify: `/Users/gnuhpc/projects/skills/ppt-master-plus/references/best-practices.md`
- Modify: `/Users/gnuhpc/projects/skills/ppt-master-plus/README.md` if it documents beautify routing

**Required wording:**

```markdown
Generic "美化 PPT" uses the main pipeline and may restructure the deck. Use faithful beautify only when the user explicitly requires unchanged wording/page count/order or source master preservation.
```

## Task 9: Manual End-To-End Verification

**Objective:** Compare behavior against v2.10.0 expectations and current strict mode.

**Files:**

- Use sample: `/Users/gnuhpc/projects/skills/ppt-master-plus/harness/testing/original-sample.pptx`

**Scenario A: generic beautify**

Prompt:

```text
请把 original-sample.pptx 美化得更专业
```

Expected:

- Routes to main pipeline.
- Does not enter `workflows/beautify-pptx.md`.
- Does not lock page count.
- Does not set `preserve_master`.
- Shows `content_divergence`.
- `design_spec.md §IX` may restructure slide count/order.

**Scenario B: faithful beautify**

Prompt:

```text
请把 original-sample.pptx 美化一下，但页数、顺序和每页文字都不要变，保留原母版
```

Expected:

- Routes to faithful beautify.
- Page count locked to source slide count.
- `preserve_master` shown and defaulted true.
- `spec_lock.md` contains `preserve_master: true` and `base_pptx`.

## Rollout Notes

Do not remove `pptx_intake.py`, `beautify_identity.py`, `beautify_inventory.py`, or master-preservation export support. They are valuable for explicit faithful mode and for source facts in the main pipeline.

The key change is behavioral: generic beautify should no longer preserve the source deck's mistakes by default.
