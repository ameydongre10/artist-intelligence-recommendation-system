# Architecture

## 1. Purpose

This document defines the high-level architecture, application structure, major components, data flow, technology stack, deployment strategy, and important implementation boundaries for the **Artist Intelligence & Recommendation System**.

The system is not only an AI/data-processing pipeline. It is a complete application consisting of:

- A frontend application for evaluators and users
- A backend API
- An artist intelligence pipeline
- Hirer requirement understanding
- Evidence-based matching and ranking
- Recommendation and refinement logic
- Follow-up processing and re-ranking
- Optional persistent graph storage using Neo4j
- Free-tier deployment using Vercel and Render

The architecture must prioritize:

```text
Evidence
+
Traceability
+
Explainability
+
Reproducibility
+
Maintainability
+
Free-Tier Deployability
```

---

# 2. Architecture Overview

The complete system architecture is:

```text
                         ┌─────────────────────────────┐
                         │         Evaluator / User    │
                         └──────────────┬──────────────┘
                                        │
                                        ▼
                         ┌─────────────────────────────┐
                         │       FRONTEND APPLICATION  │
                         │                             │
                         │  Next.js + TypeScript       │
                         │  Tailwind CSS               │
                         │  Interactive Dashboard      │
                         │                             │
                         │  • Dataset Overview         │
                         │  • Artist Intelligence      │
                         │  • Evidence Explorer        │
                         │  • Hirer Brief Analysis     │
                         │  • Top 2 Recommendations    │
                         │  • Refinement Questions     │
                         │  • Re-Ranking Comparison    │
                         └──────────────┬──────────────┘
                                        │
                                  HTTPS / REST API
                                        │
                                        ▼
                         ┌─────────────────────────────┐
                         │         BACKEND API         │
                         │                             │
                         │        FastAPI              │
                         │                             │
                         │  • API Routes               │
                         │  • Request Validation       │
                         │  • Service Layer            │
                         │  • Error Handling           │
                         │  • Orchestration            │
                         └──────────────┬──────────────┘
                                        │
             ┌──────────────────────────┼──────────────────────────┐
             │                          │                          │
             ▼                          ▼                          ▼
┌────────────────────────┐ ┌────────────────────────┐ ┌────────────────────────┐
│ Artist Intelligence    │ │ Hirer Intelligence     │ │ Recommendation Engine  │
│ Pipeline               │ │ Pipeline               │ │                        │
│                        │ │                        │ │ • Requirement Match    │
│ • Dataset Inventory    │ │ • Conversation Parse   │ │ • Evidence Weighting   │
│ • Profile Extraction   │ │ • Known Requirements   │ │ • Uncertainty          │
│ • Media Selection      │ │ • Assumptions          │ │ • Top 2 Ranking        │
│ • Media Analysis       │ │ • Unknowns             │ │ • Trade-offs           │
│ • Capability Evidence  │ │ • Contradictions       │ │ • Refinement Questions │
└────────────┬───────────┘ └────────────┬───────────┘ └────────────┬───────────┘
             │                          │                          │
             └──────────────────────────┼──────────────────────────┘
                                        │
                                        ▼
                         ┌─────────────────────────────┐
                         │      FOLLOW-UP / RE-RANKING │
                         │                             │
                         │ • Preserve Initial Ranking  │
                         │ • Process New Information   │
                         │ • Update Requirements       │
                         │ • Recalculate Ranking       │
                         │ • Explain Changes           │
                         └──────────────┬──────────────┘
                                        │
                         ┌──────────────┴──────────────┐
                         │                             │
                         ▼                             ▼
             ┌────────────────────────┐    ┌────────────────────────┐
             │ Structured Files       │    │ Neo4j Graph Database   │
             │ JSON / JSONL           │    │ Optional Persistence   │
             │                        │    │                        │
             │ • Inventory            │    │ Artist Relationships   │
             │ • Profiles             │    │ Evidence Relationships │
             │ • Evidence             │    │ Requirement Links      │
             │ • Rankings             │    │ Recommendation Graph   │
             └────────────────────────┘    └────────────────────────┘
```

---

# 3. System Design Principle

The system follows an **evidence-first, backend-driven architecture**.

The frontend must not independently calculate or invent recommendation logic.

The core decision flow remains:

```text
Raw Dataset
    ↓
Dataset Inventory
    ↓
Profile Claims
+
Selected Media Evidence
    ↓
Structured Artist Intelligence
    ↓
Hirer Requirement Intelligence
    ↓
Evidence-Based Matching
    ↓
Ranking
    ↓
Top 2 Recommendation
    ↓
Trade-offs + Uncertainty
    ↓
Maximum 2 Refinement Questions
    ↓
Follow-Up Information
    ↓
Re-Ranking
```

The frontend is responsible for:

- Displaying intelligence
- Visualizing evidence
- Allowing evaluator interaction
- Showing recommendations
- Showing assumptions and uncertainty
- Collecting follow-up answers
- Displaying before/after ranking changes

The backend is responsible for:

- Processing
- Validation
- Intelligence orchestration
- Matching
- Ranking
- Re-ranking
- Data persistence
- Explainability generation

---

# 4. Frontend Architecture

## 4.1 Frontend Purpose

A complete frontend application must be developed.

The frontend should allow an evaluator to explore the complete system instead of only reading generated JSON files.

The UI should demonstrate:

1. What exists in the dataset
2. What the system learned about each artist
3. What evidence supports those conclusions
4. What the hirer actually needs
5. What information is assumed or unknown
6. Which two artists are recommended
7. Why they are recommended
8. What trade-offs exist
9. What questions could change the ranking
10. How follow-up information changes the recommendation

---

## 4.2 Frontend Pages

Recommended application pages:

```text
/
│
├── /dashboard
│   └── System overview and dataset summary
│
├── /artists
│   ├── Artist list
│   └── Category filtering
│
├── /artists/[artistId]
│   ├── Artist profile
│   ├── Claims
│   ├── Demonstrated capabilities
│   ├── Evidence
│   ├── Confidence
│   └── Unknowns
│
├── /hirers
│   └── Hirer conversation list
│
├── /hirers/[hirerId]
│   ├── Known requirements
│   ├── Assumptions
│   ├── Contradictions
│   └── Important unknowns
│
├── /recommendations/[hirerId]
│   ├── Top 2 recommendations
│   ├── Requirement matching
│   ├── Evidence explanation
│   ├── Trade-offs
│   └── Refinement questions
│
└── /re-ranking/[hirerId]
    ├── Initial ranking
    ├── Follow-up information
    ├── Updated ranking
    └── What changed and why
```

---

## 4.3 Frontend Component Structure

The frontend should be component-driven.

Important components include:

```text
components/
├── layout/
│   ├── Sidebar
│   ├── Header
│   └── PageContainer
│
├── dashboard/
│   ├── DatasetSummary
│   ├── ArtistCategoryChart
│   ├── ProcessingStatus
│   └── SystemOverview
│
├── artists/
│   ├── ArtistCard
│   ├── ArtistList
│   ├── CapabilityMatrix
│   ├── EvidencePanel
│   ├── ClaimVsEvidence
│   └── ConfidenceIndicator
│
├── hirers/
│   ├── HirerBrief
│   ├── RequirementList
│   ├── AssumptionPanel
│   ├── UnknownsPanel
│   └── ContradictionAlert
│
├── recommendations/
│   ├── RecommendationCard
│   ├── RequirementMatch
│   ├── TradeoffPanel
│   ├── EvidenceExplanation
│   └── RefinementQuestionCard
│
└── reranking/
    ├── RankingComparison
    ├── ChangeExplanation
    └── FollowUpImpact
```

---

# 5. Backend Architecture

The backend is the intelligence and orchestration layer.

Recommended structure:

```text
Client Request
      ↓
FastAPI Router
      ↓
Request Validation
      ↓
Service Layer
      ↓
Domain Logic / Intelligence Pipeline
      ↓
Repository Layer
      ↓
JSON / JSONL / Neo4j
      ↓
Structured API Response
```

The backend should not contain frontend-specific rendering logic.

The frontend should not contain hidden recommendation algorithms.

---

# 6. Backend Components

## 6.1 API Layer

Responsibilities:

- Receive frontend requests
- Validate inputs
- Return structured responses
- Apply consistent error responses

Example endpoints:

```text
GET    /api/health

GET    /api/dataset/summary

GET    /api/artists
GET    /api/artists/{artist_id}
GET    /api/artists/{artist_id}/evidence

GET    /api/hirers
GET    /api/hirers/{hirer_id}

GET    /api/recommendations/{hirer_id}

POST   /api/recommendations/{hirer_id}/refine

GET    /api/reranking/{hirer_id}

POST   /api/reranking/{hirer_id}
```

The exact routes may evolve during implementation, but the separation of concerns should remain.

---

## 6.2 Artist Intelligence Pipeline

Responsibilities:

```text
Dataset Discovery
    ↓
Artist Identification
    ↓
Profile Extraction
    ↓
Claim Extraction
    ↓
Media Inventory
    ↓
Representative Media Selection
    ↓
Media Analysis
    ↓
Capability Assessment
    ↓
Evidence Linking
    ↓
Structured Artist Intelligence
```

Output example:

```text
Artist
├── Identity
├── Category
├── Profile Claims
├── Demonstrated Capabilities
├── Evidence
├── Confidence
├── Unknowns
└── Processing Metadata
```

---

## 6.3 Hirer Intelligence Pipeline

Responsibilities:

```text
Conversation
    ↓
Requirement Extraction
    ↓
Normalization
    ↓
Classification
```

The output must separate:

```text
Known Requirements
Assumptions
Unknowns
Contradictions
Preferences
Constraints
```

---

## 6.4 Recommendation Engine

Responsibilities:

```text
Hirer Requirements
        +
Artist Capabilities
        +
Evidence Strength
        +
Uncertainty
        ↓
Requirement Matching
        ↓
Weighted Comparison
        ↓
Ranking
        ↓
Top 2 Selection
        ↓
Trade-off Explanation
```

The recommendation engine should not depend only on an LLM-generated opinion.

Structured matching must remain the primary decision mechanism.

AI may assist with interpretation and explanation, but final recommendation logic must remain traceable.

---

## 6.5 Refinement Engine

Responsibilities:

- Identify uncertain requirements
- Estimate which unknown could most affect the ranking
- Select a maximum of two questions
- Avoid unnecessary questions

Output:

```text
Question
+
Why It Matters
+
Potential Ranking Impact
```

---

## 6.6 Follow-Up and Re-Ranking Engine

Responsibilities:

```text
Initial Recommendation
        ↓
Preserve Snapshot
        ↓
Receive Follow-Up Information
        ↓
Update Requirement State
        ↓
Recalculate Matching
        ↓
Generate Updated Ranking
        ↓
Compare Before vs After
        ↓
Explain Change
```

The original recommendation must never be silently overwritten.

---

# 7. Data Architecture

The project can operate using two storage layers.

## Layer 1 — Structured Files

Use JSON and JSONL for:

- Dataset inventory
- Intermediate outputs
- Artist intelligence
- Hirer intelligence
- Evidence records
- Ranking snapshots
- Evaluation artifacts

Example:

```text
data/
├── raw/
├── processed/
│   ├── dataset_inventory.json
│   ├── artist_profiles.json
│   ├── artist_intelligence.json
│   ├── hirer_intelligence.json
│   ├── recommendations.json
│   └── reranking_results.json
│
└── evaluation/
    ├── selection_log.json
    ├── validation_report.json
    └── test_cases.json
```

This approach is simple, reproducible, and suitable for the assignment.

---

## Layer 2 — Neo4j Graph Database

Neo4j should be used only if persistent graph relationships improve the application.

Recommended graph model:

```text
(:Artist)
    -[:HAS_CLAIM]->
(:Claim)

(:Artist)
    -[:HAS_CAPABILITY]->
(:Capability)

(:Capability)
    -[:SUPPORTED_BY]->
(:Evidence)

(:Evidence)
    -[:FROM_MEDIA]->
(:Media)

(:Hirer)
    -[:HAS_REQUIREMENT]->
(:Requirement)

(:Artist)
    -[:MATCHES {score, confidence}]->
(:Requirement)

(:Recommendation)
    -[:RECOMMENDS {rank}]->
(:Artist)
```

Neo4j is particularly useful for:

- Artist-to-capability relationships
- Capability-to-evidence traceability
- Hirer requirement relationships
- Recommendation traceability
- Graph exploration in future versions

Neo4j should not be added only for complexity.

If the assignment workflow works reliably with structured files, JSON/JSONL remains the simpler primary data store.

---

# 8. Component Interaction

## Initial Processing

```text
Dataset
    ↓
Inventory Service
    ↓
Artist / Media Classification
    ↓
Profile + Media Processing
    ↓
Artist Intelligence
    ↓
JSON / JSONL
    ↓
Optional Neo4j Persistence
    ↓
API
    ↓
Frontend
```

## Recommendation Flow

```text
Frontend
    ↓
Recommendation API Request
    ↓
Hirer Intelligence Service
        +
Artist Intelligence Service
        ↓
Matching Engine
        ↓
Ranking Engine
        ↓
Recommendation Explanation
        ↓
API Response
        ↓
Frontend Recommendation View
```

## Re-Ranking Flow

```text
Frontend Follow-Up Input
        ↓
POST /reranking/{hirer_id}
        ↓
Follow-Up Processor
        ↓
Requirement Update
        ↓
Re-Matching
        ↓
Updated Ranking
        ↓
Before / After Comparison
        ↓
Persist Snapshot
        ↓
Frontend Comparison View
```

---

# 9. Frontend to Backend Communication

The frontend communicates with FastAPI through a configurable API base URL.

Example environment variable:

```text
NEXT_PUBLIC_API_BASE_URL=https://your-backend-url
```

Development:

```text
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

Production:

```text
NEXT_PUBLIC_API_BASE_URL=https://your-render-backend.onrender.com
```

The frontend must never hard-code environment-specific backend URLs inside application components.

---

# 10. Deployment Architecture

The project should be deployable using free or free-tier infrastructure.

```text
                         ┌─────────────────────┐
                         │       User          │
                         └──────────┬──────────┘
                                    │
                                    ▼
                     ┌───────────────────────────┐
                     │         VERCEL            │
                     │                           │
                     │ Next.js Frontend          │
                     │                           │
                     │ artist-intelligence-app   │
                     └─────────────┬─────────────┘
                                   │ HTTPS API
                                   ▼
                     ┌───────────────────────────┐
                     │         RENDER            │
                     │                           │
                     │ FastAPI Backend           │
                     │                           │
                     │ Intelligence + API Layer  │
                     └─────────────┬─────────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    │                             │
                    ▼                             ▼
        ┌──────────────────────┐      ┌──────────────────────┐
        │ JSON / JSONL Storage │      │ Neo4j AuraDB         │
        │ Processed Artifacts  │      │ Optional Graph DB     │
        └──────────────────────┘      └──────────────────────┘
```

---

# 11. Hosting Responsibilities

## Vercel

Vercel hosts:

- Next.js frontend
- Static assets
- Frontend environment variables
- User interface

Frontend deployment target:

```text
https://<project>.vercel.app
```

---

## Render

Render hosts:

- FastAPI backend
- API endpoints
- Backend environment variables
- Intelligence orchestration

Backend deployment target:

```text
https://<project>.onrender.com
```

Recommended production command:

```text
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

---

## Neo4j

If graph persistence is required, use Neo4j AuraDB free tier or another supported free Neo4j deployment.

Neo4j stores relationships, not raw large media files.

Do not store:

- Raw videos
- Raw audio
- Large image binaries

Instead store:

```text
Media ID
File Path or URL
Metadata
Analysis Results
Evidence References
```

---

# 12. Folder and File Structure

Recommended repository structure:

```text
artist-intelligence-system/
│
├── frontend/
│   ├── app/
│   │   ├── page.tsx
│   │   ├── dashboard/
│   │   ├── artists/
│   │   ├── hirers/
│   │   ├── recommendations/
│   │   └── reranking/
│   │
│   ├── components/
│   │   ├── layout/
│   │   ├── dashboard/
│   │   ├── artists/
│   │   ├── hirers/
│   │   ├── recommendations/
│   │   ├── reranking/
│   │   └── ui/
│   │
│   ├── lib/
│   │   ├── api.ts
│   │   ├── utils.ts
│   │   └── constants.ts
│   │
│   ├── hooks/
│   ├── types/
│   ├── public/
│   ├── package.json
│   └── .env.example
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   │
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── health.py
│   │   │   │   ├── dataset.py
│   │   │   │   ├── artists.py
│   │   │   │   ├── hirers.py
│   │   │   │   ├── recommendations.py
│   │   │   │   └── reranking.py
│   │   │   │
│   │   │   └── dependencies.py
│   │   │
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── logging.py
│   │   │   └── exceptions.py
│   │   │
│   │   ├── models/
│   │   │   ├── artist.py
│   │   │   ├── evidence.py
│   │   │   ├── capability.py
│   │   │   ├── hirer.py
│   │   │   ├── requirement.py
│   │   │   └── recommendation.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── artist.py
│   │   │   ├── hirer.py
│   │   │   └── recommendation.py
│   │   │
│   │   ├── services/
│   │   │   ├── dataset_service.py
│   │   │   ├── artist_service.py
│   │   │   ├── hirer_service.py
│   │   │   ├── recommendation_service.py
│   │   │   └── reranking_service.py
│   │   │
│   │   ├── pipelines/
│   │   │   ├── inventory/
│   │   │   ├── profile_processing/
│   │   │   ├── media_processing/
│   │   │   ├── capability_assessment/
│   │   │   └── hirer_processing/
│   │   │
│   │   ├── engines/
│   │   │   ├── matching.py
│   │   │   ├── ranking.py
│   │   │   ├── refinement.py
│   │   │   └── explanation.py
│   │   │
│   │   └── repositories/
│   │       ├── json_repository.py
│   │       └── neo4j_repository.py
│   │
│   ├── data/
│   │   ├── raw/
│   │   ├── processed/
│   │   └── evaluation/
│   │
│   ├── tests/
│   │   ├── unit/
│   │   ├── integration/
│   │   └── fixtures/
│   │
│   ├── requirements.txt
│   └── .env.example
│
├── docs/
│   ├── PRD.md
│   ├── architecture.md
│   ├── rule.md
│   ├── phases.md
│   ├── design.md
│   └── memory.md
│
├── README.md
└── .gitignore
```

---

# 13. Technology Stack

## Frontend

| Technology | Purpose |
|---|---|
| Next.js | Frontend framework |
| TypeScript | Type safety |
| Tailwind CSS | Styling |
| Lucide React | Icons |
| React | UI rendering |

Optional frontend libraries should only be added when they directly improve usability or evaluation clarity.

---

## Backend

| Technology | Purpose |
|---|---|
| Python | Core implementation language |
| FastAPI | Backend API |
| Pydantic | Data validation and contracts |
| Uvicorn | ASGI server |
| Pytest | Backend testing |

---

## Data and Persistence

| Technology | Purpose |
|---|---|
| JSON | Structured processed artifacts |
| JSONL | Incremental or record-based outputs |
| Neo4j | Optional graph persistence and traceability |
| Neo4j Python Driver | Backend database communication |

---

## Deployment

| Service | Purpose |
|---|---|
| Vercel | Frontend hosting |
| Render | Backend hosting |
| Neo4j AuraDB | Optional graph database |
| GitHub | Source control and repository |

All deployment choices should remain free or free-tier compatible.

---

# 14. Environment Variables

## Frontend

```text
NEXT_PUBLIC_API_BASE_URL=
```

## Backend

```text
ENVIRONMENT=
FRONTEND_ORIGINS=
LOG_LEVEL=

NEO4J_URI=
NEO4J_USERNAME=
NEO4J_PASSWORD=

AI_PROVIDER=
AI_API_KEY=
```

Only variables actually required by the final implementation should be used.

Secrets must never be committed to GitHub.

---

# 15. CORS Architecture

Because the frontend and backend are hosted on separate domains:

```text
Vercel Frontend
        ↓
Render Backend
```

The backend must explicitly allow the production frontend origin.

Example conceptual configuration:

```text
Allowed Origins:
- http://localhost:3000
- https://<project>.vercel.app
```

Avoid permissive wildcard CORS in production unless there is a documented requirement.

---

# 16. Error Flow

The complete error path should be:

```text
Pipeline / Database Error
        ↓
Service Layer
        ↓
Structured Application Error
        ↓
FastAPI Error Response
        ↓
Frontend Error State
        ↓
User-Friendly Message
```

Example API response:

```json
{
  "success": false,
  "error": {
    "code": "ARTIST_NOT_FOUND",
    "message": "The requested artist could not be found.",
    "details": null
  }
}
```

The frontend should show:

- Clear error state
- Retry action where appropriate
- No raw stack traces
- No exposure of secrets

---

# 17. Processing vs Request-Time Architecture

Heavy dataset processing should not unnecessarily run on every frontend request.

Preferred approach:

```text
Dataset Processing
    ↓
Generate Structured Artifacts
    ↓
Persist Results
    ↓
API Reads Structured Results
    ↓
Frontend Displays Results
```

This reduces:

- API latency
- Repeated processing
- Hosting resource usage
- Risk of backend timeouts

On-demand processing should only be used where required, such as:

- New follow-up information
- Explicit re-ranking
- New user input

---

# 18. Architecture Boundaries

## Frontend Must Not

- Independently rank artists
- Store secrets
- Perform hidden business logic
- Invent evidence
- Make unsupported AI conclusions

## Backend Must Not

- Depend on frontend rendering details
- Return unstructured recommendation text without supporting data
- Mix API routing with complex domain logic
- Silently overwrite ranking history

## Database Must Not

- Store secrets in plain text
- Store raw large media unnecessarily
- Become mandatory if structured artifacts are sufficient

---

# 19. Scalability and Maintainability

The system should allow future replacement of individual layers.

For example:

```text
JSON Repository
        ↓
can later be replaced by
        ↓
Neo4j Repository
```

or:

```text
One AI Provider
        ↓
can later be replaced by
        ↓
Another AI Provider
```

without rewriting:

- API routes
- Core data contracts
- Matching logic
- Frontend pages

This separation should be achieved through services, interfaces, schemas, and repository abstractions.

---

# 20. Final Architecture Summary

The final application architecture is:

```text
                    USER / EVALUATOR
                           │
                           ▼
                NEXT.JS FRONTEND
                  Hosted on Vercel
                           │
                    HTTPS REST API
                           │
                           ▼
                  FASTAPI BACKEND
                  Hosted on Render
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
Artist Intelligence   Hirer Intelligence   Recommendation
Pipeline              Pipeline             + Ranking Engine
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                           ▼
                  Structured Outputs
                    JSON / JSONL
                           │
                   Optional Persistence
                           │
                           ▼
                    NEO4J AURADB
                           │
                           ▼
               Follow-Up + Re-Ranking
                           │
                           ▼
              Transparent Before/After UI
```

The final architecture must ensure that the evaluator can:

1. Open the deployed frontend.
2. Explore the artist dataset.
3. Inspect artist intelligence.
4. Trace capabilities to evidence.
5. Inspect hirer requirements and unknowns.
6. View Top 2 recommendations.
7. Understand trade-offs and uncertainty.
8. Answer refinement questions.
9. Trigger or inspect re-ranking.
10. Compare the original and updated recommendation.

The system should remain:

```text
Evidence-First
Transparent
Modular
Testable
Reproducible
Free-Tier Deployable
```
