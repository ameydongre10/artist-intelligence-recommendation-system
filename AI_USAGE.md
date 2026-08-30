# AI Usage & Transparency Log

This document provides a transparent, detailed disclosure of how Artificial Intelligence and Large Language Models (LLMs) were utilized during the design, implementation, and verification of the **Artist Intelligence & Recommendation System (AIRS)**.

---

## 1. AI Tools Utilized
- **AI Coding Assistant:** Google Antigravity IDE (powered by Google DeepMind Advanced Agentic Coding / Gemini models).
- **Environment:** Windows shell (PowerShell), Python 3.11, Node.js 22.

---

## 2. Separation of Responsibilities

```text
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│ Responsibility Matrix                                                                       │
├─────────────────────────────────────────────────────────────┬───────────────────────────────┤
│ AI Assisted / Generated Tasks                               │ Deterministic / Verified Tasks│
├─────────────────────────────────────────────────────────────┼───────────────────────────────┤
│ • Boilerplate schema scaffolding (Pydantic models)          │ • Immutable raw data preservation│
│ • Initial parser logic for docx tables and text briefs      │ • Factual quotation verification│
│ • Unit & integration test case drafting                     │ • 60/60 Pytest backend tests  │
│ • Next.js App Router component layout drafting              │ • 7/7 Jest frontend tests     │
│ • Documentation drafting (README, decision note, comments)  │ • Zero-error production build │
└─────────────────────────────────────────────────────────────┴───────────────────────────────┘
```

---

## 3. Explicit Verification of AI Outputs
AI-generated code and structured outputs were **never accepted blindly**. Every component was subjected to multiple validation gates:

1. **Deterministic Schema Validation:**
   - All generated JSON and JSONL artifacts (`dataset_inventory.json`, `artist_intelligence.jsonl`, `hirer_intelligence.json`, `recommendations.json`, `updated_recommendation.json`) are programmatically validated against strict Pydantic v2 domain schemas (`src/models/artifacts.py`).
2. **Evidence Traceability Gate:**
   - Every demonstrated artist capability must cite a real, existing portfolio file in `data/raw/Data set/` with exact timestamp or frame properties. No capability was permitted without physical file backing.
3. **Quotation Audit:**
   - 100% of hirer requirements in `hirer_intelligence.json` were audited against the source transcripts (`01_cafe_music_whatsapp.txt`, `02_skincare_photography_chat.txt`, `03_vertical_video_email.txt`, `04_leadership_event_photos.txt`, `01_cafe_music_update.txt`) to guarantee verbatim accuracy.
4. **Epistemic Discipline Enforcement:**
   - Automated tests explicitly check that `CLAIM` is never converted to `DEMONSTRATED_EVIDENCE`, `UNKNOWN` is never assigned a negative score, and assumptions are flagged with explicit rationale.
5. **Comprehensive Automated Test Coverage:**
   - 60 Python backend tests (`pytest -v`) verify schema compliance, category isolation, Top 2 count constraints, max-2 question limits, and re-ranking determinism.
   - 7 Jest frontend tests (`npm test`) verify UI component rendering and API client behavior.

---

## 4. Key Decisions Governed by Engineering Rules (Not AI Hallucination)
- **Neutrality of Missing Information:** The rule that `UNKNOWN` contributes $0\text{ pts}$ added and $0\text{ pts}$ deducted was hardcoded in `src/matching/scorer.py` to prevent penalizing artists for unstated portfolio aspects.
- **Top 2 Constraint:** The ranker strictly truncates the candidate list to exactly Rank 1 and Rank 2, enforcing comparative trade-off generation.
- **Max-2 Refinement Questions:** The refinement question engine is bounded by `max_questions <= 2` and only emits questions with high decision impact.
- **Preservation of Dataset Typo Anomalies:** Anomalous IDs (`PO4`, `PO5`, `VO4`, `VO5`) and multi-artist folders (`V03`) were documented in `dataset_inventory.json` rather than silently renamed or discarded.

---

## 5. Media Intelligence & Semantic Annotation Disclosure
- **Physical Media Extraction:** Programmatic inspection is strictly limited to verifiable technical metadata (Pillow image dimensions, aspect ratio, color mode, resolution tiers; audio/video container format, file existence, and byte size).
- **Semantic Portfolio Annotations:** High-level creative capability assessments (such as "two-part vocal harmony", "controlled cosmetic specular reflections", "snappy 9:16 short-form reel pacing") were authored by a human reviewer through manual inspection of the raw portfolio files and externalized into `data/processed/artist_capability_annotations.json`.
- **No Black-Box ML Claims:** We explicitly disclaim using computer vision or speech-to-text ML models for runtime feature extraction. The pipeline reads structured human-reviewed observations and validates them deterministically against real media files on disk.

---

## 6. Summary Statement
AI served as an accelerator for code authoring, type definition, and test construction. The core domain logic, scoring transparency, evidence verification, and artifact contracts were governed by deterministic code and verified through automated test suites.
