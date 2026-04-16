# 3D Spatial Reasoning from Orthographic Projections

A cognitive benchmark for evaluating AI systems on 3D spatial reasoning, submitted to the [Kaggle Measuring AGI competition](https://www.kaggle.com/competitions/kaggle-measuring-agi).

## Benchmark Concept

Given orthographic projections of a 3D voxel scene, models must infer the underlying 3D structure and predict unseen viewpoints. This tests key cognitive abilities:

- **Working memory** — hold multiple views and spatial relations simultaneously
- **Mental rotation** — transform scenes to new viewpoints
- **Selective attention** — focus on geometry, not superficial patterns
- **Constructive reasoning** — build 3D structure from incomplete 2D projections

**Format:** Text-only (ASCII grid representations) compatible with all LLM architectures.

**Two variants:**
1. **Multiple-Choice:** Front + top views → select correct right view from 4 options
2. **Direct Prediction:** 5 views (front, back, top, bottom, left) → predict right view

## Dataset

Pre-generated benchmark datasets in JSON format are available in `datasets/kaggle_benchmark/`:
- 3×3×3, 4×4×4, and 5×5×5 voxel scenes
- Varying object counts and complexity levels
- Deterministic generation with reproducible seeds

## Setup

Requires Python 3.11+ with [uv](https://docs.astral.sh/uv/) for dependency management:

```bash
uv sync
source .venv/bin/activate
```

## Repository Structure

- `src/generation/` — Voxel scene generation and orthographic projection
- `src/benchmark/` — Dataset generation notebooks
- `src/task_viewer/` — Web-based task viewer
- `datasets/kaggle_benchmark/` — Final benchmark datasets
- `docs/` — Competition writeup and documentation

## License

MIT
