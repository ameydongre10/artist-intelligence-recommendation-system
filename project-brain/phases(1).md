# Development Phases

# Artist Intelligence & Recommendation System

## Purpose

This document defines the complete development strategy for the project.

The work is divided into **8 phases** so that development progresses from understanding the assignment and dataset to building, testing, deploying, and validating the complete product.

The final system includes:

```text
Dataset
    ↓
Intelligence Processing
    ↓
Evidence Extraction
    ↓
Requirement Understanding
    ↓
Matching and Ranking
    ↓
FastAPI Backend
    ↓
Next.js Frontend
    ↓
Vercel + Render Deployment
```

Each phase has:

- Objective
- Tasks
- Deliverables
- Validation criteria
- Completion criteria

A phase should not be considered complete simply because code exists. The defined deliverables and validation checks should also pass.

---

# Phase 1 — Assignment, Dataset and Product Foundation

## Objective

Understand exactly what the assignment requires and establish the project foundation before implementation.

## Tasks

### 1.1 Assignment Analysis

Review and extract:

- Required outputs
- Expected workflow
- Dataset expectations
- Evaluation criteria
- Recommendation requirements
- Evidence requirements
- Hirer analysis requirements
- Follow-up and re-ranking requirements
- Deployment expectations, if applicable

Create a requirement checklist that can be used throughout development.

---

### 1.2 Dataset Inventory

Inspect the provided dataset and document:

- Available directories
- Artist records
- Hirer conversations
- Profile files
- Images
- Videos
- Audio files
- Metadata files
- File formats
- File counts
- Missing or unreadable files

Generate:

```text
data/processed/dataset_inventory.json
```

The raw dataset must remain unchanged.

---

### 1.3 Product and Engineering Documentation

Finalize and align:

```text
PRD.md
architecture.md
rule.md
phases.md
design.md
memory.md
```

Confirm that all documents reflect the final product architecture:

```text
Next.js Frontend
        ↓
Vercel
        ↓
FastAPI Backend
        ↓
Render
        ↓
Structured Data
        +
Optional Neo4j
```

---

## Deliverables

- Dataset inventory
- Requirement checklist
- Final project documentation
- Initial repository structure

---

## Validation

- [ ] Assignment requirements are explicitly listed.
- [ ] Dataset structure is understood.
- [ ] Raw data is not modified.
- [ ] Product scope is documented.
- [ ] Architecture is consistent across all `.md` files.

---

## Completion Criteria

Phase 1 is complete when the team can clearly answer:

> What must be built, what data is available, what evidence exists, and how will the final product be evaluated?

---

# Phase 2 — Project Setup and Core Architecture

## Objective

Create a clean, runnable full-stack project structure.

## Tasks

### 2.1 Repository Structure

Create the high-level structure:

```text
project-root/
├── frontend/
├── backend/
├── data/
│   ├── raw/
│   └── processed/
├── docs/
├── scripts/
├── tests/
└── README.md
```

The exact structure may evolve, but frontend and backend must remain clearly separated.

---

### 2.2 Frontend Setup

Initialize:

```text
Next.js
TypeScript
Tailwind CSS
```

Configure:

- App Router
- ESLint
- Environment variables
- API base URL
- Shared UI utilities
- Responsive layout foundation

Recommended environment variable:

```text
NEXT_PUBLIC_API_BASE_URL
```

---

### 2.3 Backend Setup

Initialize:

```text
Python
FastAPI
Pydantic
Pytest
```

Create:

```text
backend/app/
├── api/
├── core/
├── models/
├── schemas/
├── services/
├── engines/
├── repositories/
└── main.py
```

Create a health endpoint:

```text
GET /api/health
```

---

### 2.4 Environment Configuration

Create:

```text
frontend/.env.example
backend/.env.example
```

Do not commit secrets.

---

### 2.5 Initial Frontend-Backend Integration

Connect the frontend to the backend using a simple endpoint.

Validate:

```text
Next.js
    ↓
FastAPI
    ↓
Response
    ↓
Frontend UI
```

Configure CORS for local development.

---

## Deliverables

- Runnable frontend
- Runnable backend
- Health endpoint
- Environment examples
- Initial frontend-to-backend connection

---

## Validation

Frontend:

```text
npm install
npm run lint
npm run build
```

Backend:

```text
pip install -r requirements.txt
pytest
```

Integration:

- [ ] Frontend can call backend.
- [ ] Health endpoint returns successfully.
- [ ] CORS works locally.

---

## Completion Criteria

Phase 2 is complete when the application skeleton runs end-to-end locally.

---

# Phase 3 — Dataset Processing and Artist Intelligence

## Objective

Convert raw artist information into structured, traceable artist intelligence.

## Tasks

### 3.1 Artist Inventory

Identify all artists and generate stable identifiers.

For each artist, collect:

- Name or identifier
- Category
- Profile information
- Associated media
- Existing metadata

---

### 3.2 Claim Extraction

Extract explicit claims from profiles.

Examples of categories:

```text
Skill
Style
Medium
Experience
Specialization
```

Claims must remain distinguishable from verified evidence.

---

### 3.3 Media Inventory

For every media item, record:

```text
media_id
artist_id
file_type
file_path
format
processing_status
```

Where useful, also collect:

- Duration
- Dimensions
- File size
- Basic metadata

---

### 3.4 Representative Evidence Selection

Do not blindly run expensive analysis on every file.

Use:

```text
Inventory
↓
Inspect
↓
Select Representative Media
↓
Analyze
↓
Record Evidence
```

Record why media was selected.

---

### 3.5 Demonstrated Capability Generation

Create structured intelligence:

```text
Artist
↓
Claimed Capability
↓
Demonstrated Capability
↓
Evidence
↓
Confidence
↓
Unknown / Insufficient Evidence
```

---

### 3.6 Persist Results

Generate:

```text
data/processed/artist_intelligence.json
```

Additional files may be created if they improve clarity.

---

## Deliverables

- Artist inventory
- Media inventory
- Structured claims
- Demonstrated capabilities
- Evidence references
- Confidence states
- Unknown states

---

## Validation

- [ ] Every processed artist has a stable ID.
- [ ] Claims and demonstrated capabilities are separate.
- [ ] Evidence references are traceable.
- [ ] Failed media does not crash the pipeline.
- [ ] Unknown information is not treated as negative.

---

## Completion Criteria

Phase 3 is complete when an artist can be represented through a structured intelligence record that clearly distinguishes:

```text
Claimed
vs
Demonstrated
vs
Unknown
```

---

# Phase 4 — Hirer Intelligence and Requirement Modeling

## Objective

Transform incomplete hirer conversations into structured requirements.

## Tasks

### 4.1 Conversation Processing

Analyze available hirer conversations.

Extract:

```text
Known Requirements
Preferences
Constraints
Assumptions
Unknowns
Contradictions
```

---

### 4.2 Requirement Schema

Define a stable schema for requirements.

Each requirement should include fields such as:

```text
requirement_id
description
category
importance
source
certainty
```

The exact schema may evolve based on assignment data.

---

### 4.3 Assumption Detection

Separate:

```text
Explicitly Provided
```

from:

```text
Inferred / Assumed
```

Assumptions must never be silently merged into confirmed requirements.

---

### 4.4 Contradiction Detection

Detect potentially conflicting requirements.

Record:

- Conflicting statements
- Why they conflict
- Whether clarification is required

---

### 4.5 Persist Results

Generate:

```text
data/processed/hirer_intelligence.json
```

---

## Deliverables

- Structured hirer requirements
- Preferences
- Constraints
- Assumptions
- Unknowns
- Contradictions

---

## Validation

- [ ] Explicit requirements remain distinguishable from assumptions.
- [ ] Unknowns are preserved.
- [ ] Contradictions are visible.
- [ ] Source references are retained where possible.

---

## Completion Criteria

Phase 4 is complete when the system can explain exactly what it knows, what it assumes, and what remains unknown about the hirer's needs.

---

# Phase 5 — Matching, Ranking and Decision Intelligence

## Objective

Build the core recommendation engine.

## Tasks

### 5.1 Requirement-to-Capability Matching

Build the relationship:

```text
Hirer Requirement
        ↓
Artist Capability
        ↓
Evidence
        ↓
Match Assessment
```

Matching should consider:

- Relevance
- Evidence strength
- Requirement importance
- Confidence
- Unknowns
- Important constraints

---

### 5.2 Ranking

Generate a ranked list of artists.

The ranking logic must be:

- Inspectable
- Deterministic where practical
- Explainable
- Evidence-aware

Do not hide all ranking logic inside an LLM prompt.

---

### 5.3 Top 2 Recommendation

Return:

```text
Rank 1
Rank 2
```

For each recommendation include:

- Artist
- Matched requirements
- Supporting capabilities
- Supporting evidence
- Confidence
- Trade-offs
- Important uncertainty

---

### 5.4 Trade-Off Analysis

Explicitly compare the strongest alternatives.

Example structure:

```text
Artist A
+ Strong evidence for X
- Limited evidence for Y

Artist B
+ Strong evidence for Y
- Less aligned with X
```

---

### 5.5 Refinement Question Selection

Generate at most:

```text
2 high-impact questions
```

Each question must have a measurable purpose:

```text
Question
+
Why It Matters
+
Potential Ranking Impact
```

---

### 5.6 Follow-Up and Re-Ranking

Implement:

```text
Initial Requirements
↓
Initial Ranking
↓
Follow-Up Information
↓
Updated Requirements
↓
Updated Ranking
↓
Change Explanation
```

The initial recommendation must be preserved.

---

## Deliverables

- Matching engine
- Ranking engine
- Top 2 recommendation
- Trade-off analysis
- Maximum 2 refinement questions
- Re-ranking logic

---

## Validation

- [ ] Recommendations are evidence-backed.
- [ ] Every recommendation is explainable.
- [ ] Maximum 2 questions is enforced.
- [ ] Unknown does not equal negative.
- [ ] Initial rankings are preserved.
- [ ] Re-ranking changes are explained.

---

## Completion Criteria

Phase 5 is complete when the backend can produce a complete, defensible recommendation workflow from hirer requirements to updated rankings.

---

# Phase 6 — Backend API and Optional Neo4j Integration

## Objective

Expose the complete intelligence workflow through a clean API.

## Tasks

### 6.1 API Endpoints

Implement endpoints for:

```text
GET /api/health

GET /api/dashboard

GET /api/artists
GET /api/artists/{artist_id}

GET /api/artists/{artist_id}/evidence

GET /api/hirers
GET /api/hirers/{hirer_id}

GET /api/recommendations/{hirer_id}

POST /api/recommendations/{hirer_id}/refine
```

The exact endpoint structure may evolve, but the API must support the complete frontend workflow.

---

### 6.2 Response Schemas

Use Pydantic models for:

- Artist summaries
- Artist intelligence
- Evidence
- Hirer intelligence
- Recommendations
- Refinement questions
- Re-ranking results
- Error responses

---

### 6.3 Optional Neo4j Integration

Only add Neo4j if persistent relationship modeling provides clear value.

Possible graph:

```text
(Artist)
    -[CLAIMS]->
(Capability)

(Artist)
    -[DEMONSTRATES]->
(Capability)

(Capability)
    -[SUPPORTED_BY]->
(Evidence)

(Hirer)
    -[REQUIRES]->
(Requirement)

(Artist)
    -[MATCHES]->
(Requirement)
```

Neo4j must not become a dependency for storing raw media files.

---

### 6.4 Error Handling

Implement controlled responses for:

- Invalid IDs
- Missing data
- Processing failure
- Dependency failure
- AI provider failure
- Database failure

---

### 6.5 API Documentation

Use FastAPI's generated documentation for development and verification.

---

## Deliverables

- Working REST API
- Typed request/response schemas
- Controlled errors
- Optional Neo4j integration
- API documentation

---

## Validation

- [ ] Core endpoints return valid data.
- [ ] Invalid requests return controlled errors.
- [ ] Recommendation responses include explanations.
- [ ] Backend tests pass.
- [ ] Health endpoint remains lightweight.

---

## Completion Criteria

Phase 6 is complete when the complete product workflow is accessible through stable API endpoints.

---

# Phase 7 — Frontend Product Experience

## Objective

Build the evaluator-facing interactive web application.

## Tasks

### 7.1 Application Layout

Implement:

- Responsive navigation
- Page structure
- Shared layout
- Loading states
- Error states
- Empty states

Follow the approved dark interactive design direction.

---

### 7.2 Dashboard

Display:

- Dataset overview
- Artist count
- Category summary
- Available hirer cases
- Processing status
- Quick navigation

---

### 7.3 Artist Explorer

Implement:

- Artist listing
- Category filtering
- Search if useful
- Intelligence summary
- Evidence availability

---

### 7.4 Artist Detail

Display:

```text
Profile
Claims
Demonstrated Capabilities
Evidence
Confidence
Unknowns
```

The distinction between:

```text
Claimed
```

and:

```text
Demonstrated
```

must be visually obvious.

---

### 7.5 Hirer Brief

Display:

```text
Known Requirements
Preferences
Constraints
Assumptions
Unknowns
Contradictions
```

---

### 7.6 Recommendations

Build the main decision interface.

Display:

- Top 2 artists
- Ranking
- Why each artist fits
- Requirement matches
- Evidence
- Confidence
- Trade-offs
- Uncertainty
- Refinement questions

---

### 7.7 Re-Ranking Experience

Display:

```text
Initial Ranking
↓
Follow-Up Information
↓
Updated Ranking
↓
What Changed
```

Make ranking movement visually understandable.

---

### 7.8 API Integration

Connect all frontend screens to the deployed/local backend.

Use a centralized API layer.

Do not hard-code production URLs inside components.

---

## Deliverables

- Complete interactive frontend
- All required pages
- Backend integration
- Responsive design
- Loading/error/empty states

---

## Validation

- [ ] All major screens render.
- [ ] Artist intelligence is visible.
- [ ] Evidence can be inspected.
- [ ] Hirer intelligence is visible.
- [ ] Top 2 recommendation is visible.
- [ ] Re-ranking comparison works.
- [ ] API failures produce friendly messages.
- [ ] Frontend build passes.

---

## Completion Criteria

Phase 7 is complete when an evaluator can complete the entire assignment workflow through the web interface without manually running analysis scripts.

---

# Phase 8 — Testing, Deployment and Final Validation

## Objective

Validate, deploy, and prepare the final submission.

## Tasks

### 8.1 Backend Testing

Run:

```text
pytest
```

Test:

- Ranking logic
- Unknown handling
- Evidence handling
- Refinement limit
- Re-ranking
- API validation
- Error responses

---

### 8.2 Frontend Validation

Run:

```text
npm run lint
npm run build
```

If configured:

```text
npm run type-check
npm test
```

Verify major user flows manually.

---

### 8.3 Production Deployment

Deploy:

```text
Frontend
→ Vercel

Backend
→ Render
```

If Neo4j is required:

```text
Neo4j
→ AuraDB Free Tier or equivalent
```

---

### 8.4 Production Environment Configuration

Configure:

Frontend:

```text
NEXT_PUBLIC_API_BASE_URL
```

Backend:

```text
FRONTEND_ORIGINS
DATABASE_CONFIGURATION
AI_CONFIGURATION
```

Do not expose backend secrets to the frontend.

---

### 8.5 Production Integration Testing

Verify:

```text
Browser
↓
Vercel Frontend
↓
Render Backend
↓
Structured Data / Neo4j
```

Test:

- Health endpoint
- CORS
- Artist data
- Hirer data
- Recommendations
- Refinement
- Re-ranking
- Error handling

---

### 8.6 Final Documentation Review

Update:

```text
README.md
PRD.md
architecture.md
rule.md
phases.md
design.md
memory.md
```

Documentation must describe the final implemented system, not only the intended system.

---

### 8.7 Final Submission Checklist

#### Product

- [ ] Deployed frontend is accessible.
- [ ] Backend is accessible.
- [ ] Core workflow works end-to-end.

#### Intelligence

- [ ] Artist claims are separated from demonstrated evidence.
- [ ] Hirer assumptions and unknowns are visible.
- [ ] Recommendations are evidence-backed.

#### Recommendation

- [ ] Top 2 is clearly displayed.
- [ ] Trade-offs are visible.
- [ ] Maximum 2 refinement questions.
- [ ] Re-ranking works.

#### Engineering

- [ ] Tests pass.
- [ ] Frontend builds.
- [ ] No secrets are committed.
- [ ] Error states are controlled.
- [ ] Environment variables are documented.

#### Documentation

- [ ] README is complete.
- [ ] Architecture matches implementation.
- [ ] PRD matches implementation.
- [ ] Rule document matches implementation.
- [ ] Project memory is updated.

---

## Deliverables

- Deployed Vercel frontend
- Deployed Render backend
- Optional Neo4j deployment
- Passing tests
- Final documentation
- Final repository

---

## Completion Criteria

Phase 8 is complete when the evaluator can:

```text
Open the deployed frontend
        ↓
Understand the dataset
        ↓
Explore artists
        ↓
Inspect evidence
        ↓
Understand hirer requirements
        ↓
View the Top 2 recommendation
        ↓
Inspect trade-offs
        ↓
Review up to 2 refinement questions
        ↓
Provide follow-up information
        ↓
Observe the updated ranking
```

without requiring local setup or manual execution of the analysis pipeline.

---

# Phase Dependency Map

```text
Phase 1
Requirements + Dataset Understanding
        ↓
Phase 2
Full-Stack Project Foundation
        ↓
Phase 3
Artist Intelligence
        ↓
Phase 4
Hirer Intelligence
        ↓
Phase 5
Matching + Ranking + Re-Ranking
        ↓
Phase 6
FastAPI + Optional Neo4j
        ↓
Phase 7
Next.js Product Experience
        ↓
Phase 8
Testing + Vercel + Render Deployment
```

---

# Development Priority

The recommended implementation priority is:

```text
1. Correctness
2. Evidence Traceability
3. Recommendation Quality
4. Explainability
5. End-to-End Functionality
6. UI/UX Polish
7. Optional Infrastructure Complexity
```

A polished frontend with unsupported recommendations is not acceptable.

Likewise, a strong backend that the evaluator cannot interact with easily is incomplete.

The final goal is a balanced product:

```text
Strong Dataset Understanding
+
Evidence-Based Intelligence
+
Transparent Recommendation
+
Working Backend
+
Interactive Frontend
+
Free-Tier Deployment
```

---

# Definition of Done

The project is considered complete only when all 8 phases are complete and the following statement is true:

> The supplied dataset has been transformed into structured artist and hirer intelligence, evidence-backed Top 2 recommendations can be generated and explained, follow-up information can trigger transparent re-ranking, and the complete workflow is accessible through a deployed Next.js frontend connected to a FastAPI backend.
