# Mode: academic

Academic research and literature presentation mode. Reading-first, high density, evidence-driven. Prioritizes academic integrity, source fidelity, and vector editability over marketing flash. For journal clubs, lab meetings, PhD/thesis defenses, academic conferences, and research talk pitches.

---

## 1. Narrative Skeleton

**Evidence-driven progression**: The slide sequence replicates a rigorous academic inquiry. The narrative arc moves from establishing a gap in current research to validating claims using concrete empirical evidence, followed by critical analysis.

The standard research narrative structure:

| Stage | Role | Where |
|---|---|---|
| Context & Gap | Background literature, state of the art, and core problem statement | First 1-2 pages |
| Contribution | Stated thesis, main contributions, and headline claims | Early pages |
| Method | Detailed technical framework, mathematics, and algorithms | Middle pages (in-depth) |
| Empirical Results | Quantitative evaluation, comparison tables, and figures | Core body pages |
| Critique & Limitations | Ablation studies, failure cases, and stated boundaries of the work | Late pages |
| Future Work & Q&A | Next steps and seed questions for academic discussion | Closing / Appendix |

### Action Titles
Slide titles should state the specific claim or finding verified by that page's evidence, rather than a generic section label:

| Weak (topic / label) | Strong (academic assertion) |
|---|---|
| "Results" | "Proposed method cuts execution latency by 1.8× under equal perplexity" |
| "Equation 3" | "Softmax scaling prevents coordinate overflow in long-sequence attention" |
| "Ablation Study" | "Removing spatial attention decays BLEU score by 4.2 points" |

---

## 2. Hard Integrity Guardrails

To preserve academic rigor, the Executor must follow these strict rules during slide generation:

1. **Zero Data Fabrication**: Every number, coordinate, and metric must come directly from the source paper. Never approximate, invent, or round data values to fit a layout.
2. **Zero Citation Fabrication**: All citations must map to verified references. If a citation key cannot be verified, write it as a visible `[UNVERIFIED: cite_key]` placeholder; never invent placeholder authors or DOIs.
3. **Zero Figure Fabrication**: Use real figures extracted from the paper (using bounding boxes) rather than generating decorative mockups. If a figure cannot be located, write `[MISSING: Figure N]`.
4. **Data-Bound Charts**: Charts must be plotted with exact coordinates matching the reported values. Never draw eyeballed bar charts or estimated lines.
5. **No Neighbor Bleed**: Figures and tables must be cleanly isolated. Strip all page headers, footers, and DOI margins from crops.

---

## 3. Page-Structure Tendencies

- **KaTeX/LaTeX Integration**: Display and inline mathematical equations must be rendered as native vector text using KaTeX markup (e.g. `$$\mathrm{softmax}(x)$$`), ensuring text-level editability in output files.
- **Progressive Density**: Relax the "one message per slide" rule for dense slides (such as multi-column results tables or complex methods). Provide a clear hierarchy: high-contrast assertion headers, followed by structured evidence grids.
- **Protagonist Rule for Figures**: A slide dedicated to a key figure should keep captions to a single line and move long descriptive paragraphs into speaker notes. If necessary, activate "Hero Mode" (increasing image heights to 700px) to ensure small labels remain legible.
- **12px Legibility Floor**: Ensure no text elements or captions are sized below 12px in standard projection viewports to maintain legibility.

---

## 4. Speaker-Notes Register

Precise, descriptive, and scholarly. The speaker notes must state the primary claim of the slide in the first sentence, explain the methodology details (parameters, datasets, metrics), and explicitly detail the scope conditions and hedges. Cite sources for every key figure or data table referenced.
