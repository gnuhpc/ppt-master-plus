# Reconstruct Image / Screenshot PPTX Workflow

> **Purpose**: Convert existing image-first PPT slides, PDF screenshots, or AI-generated poster slides into 100% native, fully editable PowerPoint (`.pptx`) decks with separate background images and re-created textframes and shapes.

---

## Workflow Steps

### Step 1: Image & Layout Intake
1. Place input slide images (`.png` / `.jpg` / `.webp`) or PDF file in `<project_path>/sources/`.
2. Extract text content, bounding boxes, and element hierarchies using OCR / Vision LLM:
   ```bash
   python3 ${SKILL_DIR}/scripts/source_to_md/pdf_to_md.py <project_path>/sources/<input_file>
   ```

### Step 2: Background Masking & Cleaning (Gemini Mask / OpenCV)
1. For each slide image, detect and mask text areas to generate a clean background image (devoid of text).
2. Save clean background images into `<project_path>/images/bg_slide_NN.png`.
3. Extract standalone icons and vector shapes into `<project_path>/images/icon_NN_XX.png`.

### Step 3: Reconstruction to Python-PPTX Script
1. Generate `reconstruct_deck.py` using `python-pptx`:
   - Insert `bg_slide_NN.png` as the slide background.
   - Re-create native PPTX TextFrames at the exact bounding box coordinates `(left, top, width, height)`.
   - Set font family, font size, text color, alignment, and word wrap matching original layout.
   - Insert native shapes/lines for cards and containers.

### Step 4: Visual Comparison & Quality Check
1. Render generated PPTX pages to PNG images.
2. Run `visual_compare_qa` (or `svg_quality_checker.py`) to verify text alignment and font size fidelity between original input images and output `.pptx` slides.

### Step 5: Final Export
1. Save the finished editable deck to `<project_path>/output/<project_name>_reconstructed.pptx`.
