# 3D Spatial Reasoning from Orthographic Projections

**A Cognitive Benchmark for Executive Functions**

---

### Your Team

Independent Researcher

### Problem Statement

**Core challenge:** Can AI models reconstruct 3D structure from partial 2D observations through mental transformation?

Given two orthographic projections of a 3D voxel scene (front and top views), models must infer the underlying 3D structure and predict a third, unseen projection (right view). This tests **executive functions**—specifically working memory, mental rotation, and cognitive flexibility.

**Why Executive Functions?** The bottleneck is not *recognizing what's there* (perception) but *transforming it to predict what it becomes from a new angle* (executive functions). The 2D inputs are abstracted symbolic grids—perceptual work is done. What remains requires:

1. **Working Memory**: Holding multiple coordinate frames while integrating constraints
2. **Mental Rotation**: Transforming the mental model to predict unseen perspectives  
3. **Cognitive Flexibility**: Switching between 2D projections and 3D structure

Like Shepard-Metzler mental rotation tasks, this tests active transformation, not passive matching—amplified by requiring 3D reconstruction *before* rotation.

**Why this matters for AGI:** Spatial transformation underlies engineering design, robotics, and medical imaging. Unlike benchmarks testing view *matching* (SpinBench) or perspective-taking in single images (ViewSpatial-Bench), we test *constructing* 3D structure from sparse observations—fundamentally harder.

**Text-only format:** ASCII grid representations avoid vision-specific confounds, testing pure spatial reasoning across all LLM architectures. 

---

### Task & Benchmark Construction

**Comparison with Existing Benchmarks:**

| Dimension | SpinBench | ViewSpatial-Bench | Our Benchmark |
|-----------|-----------|-------------------|---------------|
| **Input** | All views provided | Single rich image | Sparse views (2 or 5) |
| **Reasoning** | Match/classify views | Perspective-taking within scene | Construct 3D, predict unseen view |
| **3D Reconstruction** | Not required | Not required | **Core task** |
| **Modality** | Vision-only | Vision-only | **Text-only** |
| **Stimuli** | Photographs (confounded) | Photographs (confounded) | Synthetic grids (controlled) |

**Unique contributions:** First benchmark requiring 3D reconstruction from incomplete projections; text-only format isolates pure geometric reasoning; ARC-style grids control for perceptual confounds.

**Task Structure:**

1. **Multiple-Choice variant**: 
   - **Input**: Front and top views + 4 candidate right-view options
   - **Output**: Selected option (integer 1-4)
   - **Scoring**: 1.0 if correct, 0.0 otherwise

2. **Direct Prediction variant**: 
   - **Input**: 5 orthographic views (front, back, top, bottom, left)
   - **Output**: Predicted right view (2D grid)
   - **Scoring**: 1.0 for exact match, 0.33 for single-axis mirror (horizontal OR vertical), 0.17 for dual-axis mirror (both)
   - **Rationale**: Partial credit for near-miss spatial reasoning (correct geometry but wrong orientation)

**Format:** Structured 2D grids with coordinate annotations. ARC color coding: 0 = transparent, 1-9 = object colors. The 3D scene and its orthographics ASCII grids can be visualized like the following 3x3x3 reference scene:

![](https://www.googleapis.com/download/storage/v1/b/kaggle-user-content/o/inbox%2F2101774%2Fc7119e0247c9d34eb522e509c56d9624%2Fbf1a6f359e5734cd18472f35336f4f12.png?generation=1776232865013862&alt=media)
*The task in 3D with camera positions for the 6 views*
<br>

![](https://www.googleapis.com/download/storage/v1/b/kaggle-user-content/o/inbox%2F2101774%2F4950426b0f699a0405800c1942a7c905%2Fff2fca9c0e9783b77ad12c3f4fb52077.png?generation=1776239800119308&alt=media)
*The 6 othrographic views from the scene above*
<br>

**Selected models:**
In total 11 models are selected with following rationale:
- Represents current frontier capabilities across proprietary and open-weight alternatives
- Prioritizes latest flagship versions, excluding older generations
- Includes reasoning-specialized variants to test chain-of-thought on mental rotation

---

### Dataset

**Generation:** Seeded 3D voxel scenes (reproducible) → task-specific datasets (MC: front+top views + 4 options; 5V: 5 views → predict right view) → Kaggle upload.

**Statistics:** 100 tasks per variant; scene sizes 3×3×3 (1-4 objects), 4×4×4 (2-6 objects), 5×5×5 (3-8 objects). Deterministic generation with validated projections. Distractors use controlled error injection (spatial permutations, occlusion errors, color mutations).


---

### Technical Details

**Projection Algorithm:** Orthographic projection takes the first non-zero voxel along each axis. Python 3.11+ implementation with scene generation, projection, distractor generation, and task variants available at [GitHub Repository](https://github.com/joosthazelzet/ai-3d-spatial-reasoning).

---

### Results, Insights, and Conclusions

*Detailed analysis and visualizations available in [`https://github.com/joosthazelzet/ai-3d-spatial-reasoning/src/evaluation/analysis.ipynb`](https://github.com/joosthazelzet/ai-3d-spatial-reasoning/src/evaluation/analysis.ipynb)*

**Results: Accuracies**
This overview shows the accuracies of the 6 benchmark tasks for the 11 tested models. The top 3 results are marked with Gold, Silver and Bronze.

![](https://www.googleapis.com/download/storage/v1/b/kaggle-user-content/o/inbox%2F2101774%2F02047ae90198055e7a829c4f1bc27c39%2FScreenshot%202026-04-15%20at%2020.47.14.png?generation=1776278887327077&alt=media)

**Data Quality:** 31 MC 3×3×3 tasks had duplicate correct answers (corrected in results). Some 5V tasks have ambiguous reconstructions (limitation noted). Runtime scaled 3-4× from simple to complex scenes; 5×5×5 limited to 20 tasks to avoid timeouts.

**Statistics:** 2,640 total tasks; 61 (2.3%) runtime errors; 34 (2.6%) received partial credit for flipped predictions.

**Errors:** GLM-5 had 46 runtime errors (all `TypeError` from API issues, not reasoning failures). Qwen3-Next: 13 errors, Gemma-4: 9 errors, Claude: 1 error.

**Key Findings**

**1. Model Performance**

**Gemini-3.1 Pro** dominated (MC: 100%/98%/100%; 5V: 96%/92%/90%). **DeepSeek-R1** specialized in MC (92%/86%/90%) but dropped on 5V (52%/46%/43%), suggesting constrained answer spaces help. **Reasoning models** showed mixed results—some excelled (DeepSeek-R1), others collapsed on 5V (Qwen3-Next: 76% → 10%).

**2. Complexity Scaling**

3×3×3 → 5×5×5 degradation on 5V tasks: **graceful** (Gemini: 96→90%), **moderate** (GLM-5: 98→45%, Claude Sonnet: 81→30%, Gemma: 86→45%), **catastrophic** (GPT-5.4: 53→3%, Qwen3-235B: 18→0%). Several models (GPT-5.4-mini, Qwen3-235B, DeepSeek-V3) performed near-zero across all sizes, suggesting they lack basic spatial reasoning capability rather than showing degradation.

**3. MC vs Direct Prediction Gap**

Models consistently scored higher on MC than 5V tasks (e.g., DeepSeek-R1: 92% MC vs 52% 5V at 3×3×3). Since these tasks differ in both input count *and* output format (selection vs generation), this likely reflects that constrained answer spaces are easier than free-form spatial generation, rather than a pure effect of additional views.


**AGI Implications**

This benchmark exposes a gap between pattern recognition and constructive spatial reasoning. Most models can select correct answers from options (MC) but fail at generating spatial predictions from scratch (5V), and performance degrades sharply with scene complexity. This suggests current LLMs treat spatial tasks as pattern matching rather than performing genuine 3D mental transformation—a core cognitive primitive for tool use, design, and physical interaction.

---

### Organizational Affiliations

Independent researcher at Linq-it Media B.V. (www.linq-it.com)

---

### References & Citations

**Cognitive Foundations:**
- Shepard, R. N., & Metzler, J. (1971). Mental rotation of three-dimensional objects. *Science*, 171(3972), 701-703.

**Related Benchmarks:**
- Zhang et al. (2025). SpinBench: Perspective and Rotation as a Lens on Spatial Reasoning in VLMs. *ICLR 2026*.
- ZJU-REAL Lab. ViewSpatial-Bench: Multi-perspective Spatial Localization and Understanding. HuggingFace.

**Measuring AGI:**
- DeepMind (2026). Measuring progress toward AGI: A cognitive framework. https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/measuring-progress-toward-agi/measuring-progress-toward-agi-a-cognitive-framework.pdf

**Synthetic Reasoning:**
- Chollet, F. (2019). On the Measure of Intelligence. *arXiv:1911.01547*.
- ARC Prize. https://arcprize.org/



