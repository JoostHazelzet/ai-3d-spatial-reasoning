# Setup Benchmark 


## Models to choose
In the task, select the following models:

| Model | Include | Reason |
|-------|---------|--------|
| Claude Sonnet 4.6 (Aug 2025) | ✅ | Latest Claude flagship; strong spatial reasoning and vision capabilities |
| Claude Opus 4.6 (Aug 2025) | ✅ | Top-tier Claude model; tests ceiling performance on executive functions |
| Claude Haiku 4.5 (Feb 2025) | ❌ | Fast/cheap model; likely insufficient for complex 3D reasoning tasks |
| Claude Opus 4.5 (Aug 2025) | ❌ | Redundant with 4.6; save cost by using latest version |
| Claude Sonnet 4.5 | ❌ | Older version; 4.6 supersedes for spatial reasoning capability |
| Claude Opus 4.1 (Mar 2025) | ❌ | Outdated; 4.6 offers better multimodal understanding capabilities |
| Claude Sonnet 4 (Mar 2025) | ❌ | Legacy model; insufficient coverage of current frontier capabilities |
| DeepSeek V3.2 (Jul 2025) | ✅ | Strong open-weight model; tests spatial reasoning without proprietary training |
| deepseek-v3.1 (Jul 2025) | ❌ | V3.2 supersedes; avoid testing multiple minor versions unnecessarily |
| DeepSeek-R1 (Jan 2025) | ✅ | Reasoning-focused model; critical for mental rotation benchmark testing |
| Gemini 3.1 Flash-Lite Preview (Jan 2025) | ❌ | Lightweight preview; insufficient for demanding 3D reconstruction tasks |
| Gemini 3.1 Pro Preview (Jan 2025) | ✅ | Latest Gemini flagship; strong vision and spatial reasoning |
| Gemini 3 Flash Preview | ❌ | Preview model; wait for stable release with verified capabilities |
| Gemini 2.5 Flash (Jan 2025) | ❌ | Mid-tier model; redundant with 3.1 Pro for capability ceiling |
| Gemini 2.5 Pro (Jan 2025) | ❌ | Older generation; 3.1 Pro supersedes for spatial tasks |
| Gemini 2.0 Flash Lite (Jun 2024) | ❌ | Outdated and lightweight; insufficient for complex multiview reasoning |
| Gemini 2.0 Flash (Jun 2024) | ❌ | Too old; spatial reasoning improved significantly in 3.x |
| Gemma 4 26B A4B (Jan 2025) | ✅ | Open model; tests mid-size capability on spatial reasoning |
| Gemma 4 31B (Jan 2025) | ❌ | Marginal improvement over 26B; redundant for benchmark diversity |
| Gemma 3 1B (Jan 2025) | ❌ | Too small; inadequate working memory for multi-view integration |
| Gemma 3 12B | ❌ | Smaller model; insufficient capacity for 3D reconstruction tasks |
| Gemma 3 27B | ❌ | Older generation; Gemma 4 supersedes spatial reasoning tests |
| Gemma 3 4B | ❌ | Tiny model; fails working memory requirements for benchmark |
| GPT-5.4 nano (Aug 2025) | ❌ | Nano size; too small for executive function tasks |
| GPT-5.4 mini (Aug 2025) | ✅ | Mid-tier OpenAI; cost-effective baseline for spatial reasoning comparison |
| GPT-5.4 (Aug 2025) | ✅ | OpenAI flagship; essential for competitive spatial reasoning benchmarking |
| gpt-oss-20b (Jun 2024) | ❌ | Outdated open model; newer alternatives available with better performance |
| gpt-oss-120b (Jun 2024) | ❌ | Old model; spatial capabilities eclipsed by 2025 releases |
| Qwen 3 Next 80B Thinking | ✅ | Reasoning-specialized; tests chain-of-thought on spatial transformation tasks |
| Qwen 3 Next 80B Instruct | ❌ | Non-reasoning variant; "Thinking" model more relevant for mental rotation |
| Qwen 3 Coder 480B A35B Instruct | ❌ | Code-focused; not optimized for visual spatial reasoning benchmarks |
| Qwen 3 235B A22B Instruct 2506 | ✅ | Largest Qwen; tests scaling laws on 3D reasoning |
| GLM-5 (Jan 2025) | ✅ | Chinese frontier model; adds geographic/training diversity to benchmark |


## Accelerator to choose

| Accelerator | Recommend | Reason |
|-------------|-----------|--------|
| None | ❌ | CPU inference too slow for large models; impractical runtime |
| GPU T4 x2 | ✅ | Modern architecture, 32GB total, handles open models efficiently |
| GPU P100 | ⚠️ | Older/slower than T4; acceptable fallback if T4 unavailable |
| TPU v5e-8 | ❌ | Limited framework support; incompatible with most LLM libraries |

**Rationale:** GPU T4 x2 provides the best balance of performance and compatibility. Most open models (DeepSeek, Gemma, Qwen) require GPU for reasonable inference speeds. Two T4s enable larger batch sizes or model parallelism. TPUs are restricted to JAX/TensorFlow, which limits model availability. For API-based models (Claude, GPT, Gemini), accelerator choice matters less, but GPU is essential for local open-weight evaluation.
