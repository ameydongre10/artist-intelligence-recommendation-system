# Product Requirements Document (PRD)

# Artist Intelligence & Recommendation System

## 1. Product Overview

### 1.1 Product Name

**Artist Intelligence & Recommendation System**

### 1.2 Product Type

AI-assisted, evidence-first artist discovery, intelligence, and recommendation application.

### 1.3 Product Delivery

The final product will be delivered as a **deployed web application**, not only as a collection of scripts, notebooks, JSON outputs, or backend APIs.

The evaluator should be able to open the frontend application in a browser and interact with the system.

Deployment architecture:

```text
User / Evaluator
       ↓
Next.js Frontend
Hosted on Vercel
       ↓
REST API
       ↓
FastAPI Backend
Hosted on Render
       ↓
Structured Data / Optional Neo4j
```

The frontend is an essential part of the product because it demonstrates the complete decision-making workflow.

---

# 2. Product Goal

The goal is to build an application that can analyze incomplete artist portfolio information and incomplete hirer requirements to generate **transparent, evidence-backed artist recommendations**.

The application must answer:

> Based on the information currently available, which artists are the best match for the hirer's needs, what evidence supports that recommendation, what assumptions were made, what information is still unknown, and how would new information change the decision?

The system must not behave like a generic portfolio search engine.

It should behave as a:

```text
Decision Intelligence System
```

The application should transform raw and incomplete information into a structured decision process:

```text
Raw Artist Data
        +
Media Evidence
        +
Hirer Conversation
        ↓
Structured Intelligence
        ↓
Evidence-Based Matching
        ↓
Top 2 Recommendation
        ↓
Trade-offs + Uncertainty
        ↓
Maximum 2 High-Impact Questions
        ↓
Follow-Up Information
        ↓
Updated Recommendation
```

---

# 3. Core Purpose

The core purpose of the application is to solve the problem of making a reasonable hiring recommendation when the available information is incomplete.

The system must:

- Analyze artist information.
- Inspect available evidence.
- Distinguish claims from demonstrated capabilities.
- Understand incomplete hirer requirements.
- Identify assumptions and unknowns.
- Recommend the best two artists.
- Explain why they were selected.
- Show trade-offs.
- Ask only the most useful follow-up questions.
- Re-rank artists when new information becomes available.

The product should prioritize:

```text
Evidence
+
Relevance
+
Transparency
+
Uncertainty Awareness
+
Explainability
```

over:

```text
Complexity
```

---

# 4. Problem Statement

Artist portfolios and hirer conversations may both contain incomplete information.

For example:

- An artist may claim a capability without enough demonstrated evidence.
- A portfolio may contain multiple types of media with varying relevance.
- A hirer may describe preferences without specifying important constraints.
- Some requirements may be contradictory.
- New information may arrive after an initial recommendation.

A simple keyword search or LLM-generated answer is insufficient.

The product must instead build a traceable relationship between:

```text
Artist
    ↓
Capability
    ↓
Supporting Evidence
```

and:

```text
Hirer
    ↓
Requirement
    ↓
Importance / Constraint
```

The recommendation should result from matching these structured representations.

---

# 5. Target Users

## 5.1 Primary User: Assignment Evaluator

The primary user is the evaluator reviewing the technical assignment.

The evaluator needs to quickly understand:

- What data was provided.
- What the system extracted.
- How artists were analyzed.
- What evidence supports each capability.
- How hirer requirements were understood.
- Why specific artists were recommended.
- How uncertainty was handled.
- How the ranking changes after follow-up information.

The frontend must make this workflow visible and easy to inspect.

---

## 5.2 Secondary User: Hirer

The hirer is a conceptual end user who needs to find an artist for a specific project or requirement.

The hirer needs:

- Recommendations without needing to understand the complete dataset.
- Clear explanations.
- Awareness of assumptions.
- Visibility into trade-offs.
- Minimal unnecessary questioning.
- Updated recommendations when requirements change.

---

## 5.3 Future User: Internal Talent or Artist Operations Team

The architecture should allow future use by a team responsible for:

- Artist discovery
- Portfolio analysis
- Artist matching
- Recommendation review
- Decision auditing

This is not the primary assignment requirement, but the architecture should not prevent future expansion.

---

# 6. User Needs

## Evaluator Needs

The evaluator should be able to:

1. Open the deployed application.
2. Understand the dataset structure.
3. Browse artists by category.
4. Open an artist profile.
5. Compare claimed capabilities with demonstrated evidence.
6. Inspect evidence supporting a conclusion.
7. View confidence and uncertainty.
8. Inspect hirer requirements.
9. View assumptions and contradictions.
10. See the Top 2 recommendation.
11. Understand why each artist was selected.
12. See trade-offs.
13. View up to two refinement questions.
14. Submit or inspect follow-up information.
15. Compare initial and updated rankings.

---

## Hirer Needs

The hirer should receive:

```text
Best Current Recommendation
+
Why It Fits
+
Supporting Evidence
+
Trade-offs
+
Assumptions
+
Important Unknowns
```

The system should not overwhelm the hirer with unnecessary technical information.

Detailed evidence should remain available through the UI for transparency.

---

# 7. Product Scope

## In Scope

The application will include:

### Artist Intelligence

- Artist inventory.
- Category identification.
- Profile information.
- Claim extraction.
- Media inventory.
- Selective media analysis.
- Demonstrated capability assessment.
- Evidence references.
- Confidence.
- Unknown or insufficient evidence states.

### Hirer Intelligence

- Hirer conversation analysis.
- Requirement extraction.
- Known requirements.
- Preferences.
- Constraints.
- Assumptions.
- Unknowns.
- Contradictions.

### Recommendation

- Requirement-to-capability matching.
- Evidence-aware ranking.
- Top 2 recommendation.
- Recommendation explanation.
- Trade-off explanation.
- Uncertainty display.

### Refinement

- Maximum two high-impact questions.
- Explanation of why each question matters.
- Potential impact on ranking.

### Re-Ranking

- Preserve initial recommendation.
- Process follow-up information.
- Update requirement understanding.
- Recalculate rankings.
- Show before/after comparison.
- Explain what changed and why.

### Frontend Application

- Interactive dashboard.
- Artist exploration.
- Evidence exploration.
- Hirer brief analysis.
- Recommendation view.
- Re-ranking view.
- Error states.
- Loading states.
- Responsive interface.

---

## Out of Scope

The first version will not prioritize:

- Real-time collaboration.
- Full user authentication systems unless required.
- Artist self-service profile editing.
- Payment processing.
- Large-scale multi-tenant infrastructure.
- Continuous automated portfolio crawling.
- Real-time processing of arbitrary external portfolios.

The focus is the supplied assignment dataset and a strong demonstration of the required decision workflow.

---

# 8. Core Product Features

## Feature 1 — Dataset Intelligence Dashboard

### Purpose

Provide a clear entry point into the dataset and processing results.

### User Value

The evaluator can immediately understand what the system contains.

### Display

- Total artists.
- Artist categories.
- Available media.
- Hirer conversations.
- Processing status.
- Data completeness summary.

---

## Feature 2 — Artist Explorer

### Purpose

Allow users to browse all artists.

### Functionality

- Category filtering.
- Artist cards.
- Search if useful.
- Quick capability summary.
- Evidence availability.
- Confidence indicators.

The artist list should not pretend that every artist has complete evidence.

---

## Feature 3 — Artist Intelligence Profile

Each artist should have a dedicated frontend view.

The page should contain:

```text
Artist Identity
        ↓
Profile Information
        ↓
Claims
        ↓
Demonstrated Capabilities
        ↓
Supporting Evidence
        ↓
Confidence
        ↓
Unknown / Insufficient Evidence
```

A central UI requirement is to visually distinguish:

```text
CLAIMED
```

from:

```text
DEMONSTRATED
```

---

## Feature 4 — Evidence Explorer

### Purpose

Make the recommendation traceable.

The evaluator should be able to inspect:

- Source profile information.
- Relevant media.
- Evidence descriptions.
- Capability links.
- Confidence.
- Processing metadata where useful.

The system should answer:

> Why does the application believe this artist has this capability?

---

## Feature 5 — Hirer Requirement Analysis

The application should convert an unstructured conversation into structured requirements.

The frontend should separate:

```text
Known Requirements
```

```text
Preferences
```

```text
Constraints
```

```text
Assumptions
```

```text
Unknowns
```

```text
Contradictions
```

The user should never have to guess what information was explicitly provided versus inferred.

---

## Feature 6 — Evidence-Based Top 2 Recommendations

The application must generate and display the two strongest current matches.

Each recommendation should show:

- Rank.
- Artist.
- Why the artist fits.
- Relevant matched requirements.
- Supporting evidence.
- Confidence.
- Trade-offs.
- Important limitations.

The system should not provide unexplained scores.

If a score is displayed, it must be supported by understandable matching information.

---

## Feature 7 — Requirement-to-Evidence Matching

The recommendation view should make the matching process visible.

Conceptually:

```text
Hirer Requirement
        ↓
Artist Capability
        ↓
Supporting Evidence
        ↓
Match Assessment
```

This is a key feature because it directly supports evaluation of recommendation quality.

---

## Feature 8 — Trade-Off and Uncertainty View

A recommendation should not imply certainty when information is incomplete.

The UI must show:

- What is strongly supported.
- What is moderately supported.
- What is uncertain.
- What evidence is missing.
- What trade-off exists between the Top 2 artists.

Example:

```text
Artist A
Strong fit for requirement X
Limited evidence for requirement Y

Artist B
Strong evidence for requirement Y
Less aligned with requirement X
```

---

## Feature 9 — Maximum Two Refinement Questions

After presenting the initial recommendation, the system may ask at most two questions.

Each question should contain:

```text
Question
+
Why This Matters
+
Potential Impact on Ranking
```

The product must not ask questions merely to collect more information.

A question should only be selected if the answer could meaningfully improve or change the recommendation.

---

## Feature 10 — Follow-Up and Re-Ranking

The application must demonstrate how new information changes the decision.

The UI should display:

```text
INITIAL STATE
```

including:

- Initial requirements.
- Initial ranking.
- Initial assumptions.

Then:

```text
FOLLOW-UP INFORMATION
```

Then:

```text
UPDATED STATE
```

including:

- Updated requirements.
- Updated ranking.
- Ranking movement.
- What changed.
- Why the ranking changed or remained stable.

---

# 9. User Journey

## Journey 1 — Evaluator

```text
Open Deployed Frontend
        ↓
Dashboard
        ↓
Explore Dataset
        ↓
Inspect Artist Intelligence
        ↓
Inspect Evidence
        ↓
Open Hirer Brief
        ↓
Review Requirements + Unknowns
        ↓
View Top 2 Recommendations
        ↓
Inspect Trade-offs
        ↓
Review Refinement Questions
        ↓
View Follow-Up
        ↓
Compare Re-Ranking
```

The evaluator should be able to complete this journey without reading raw source files manually.

---

## Journey 2 — Hirer

```text
Open Hirer Requirement
        ↓
Understand Current Requirements
        ↓
Receive Top 2 Recommendation
        ↓
Review Why Each Artist Fits
        ↓
Review Trade-offs
        ↓
Answer Maximum 2 Questions
        ↓
Receive Updated Recommendation
```

---

# 10. Frontend Requirements

The frontend is a required product component.

It must be built using the approved frontend architecture.

## Core Requirements

- Modern responsive web application.
- Clear navigation.
- Dark interactive visual theme.
- Blue, orange, purple, and red semantic accents.
- Strong visual distinction between evidence states.
- Loading states.
- Empty states.
- Error states.
- Mobile and desktop usability.
- Accessible text contrast.

---

## Required Frontend Areas

### Dashboard

Shows:

- Dataset summary.
- Artist counts.
- Category breakdown.
- Processing status.
- Quick navigation.

### Artists

Shows:

- All artists.
- Categories.
- Intelligence summary.

### Artist Detail

Shows:

- Profile.
- Claims.
- Demonstrated capabilities.
- Evidence.
- Confidence.
- Unknowns.

### Hirer Brief

Shows:

- Original conversation or relevant summary.
- Known requirements.
- Preferences.
- Assumptions.
- Unknowns.
- Contradictions.

### Recommendations

Shows:

- Top 2 artists.
- Matching explanation.
- Evidence.
- Trade-offs.
- Confidence.
- Refinement questions.

### Re-Ranking

Shows:

- Initial ranking.
- Follow-up information.
- Updated ranking.
- Movement.
- Explanation.

---

# 11. Backend Requirements

The backend must provide the intelligence and API layer.

Primary responsibilities:

- Dataset processing.
- Structured artist intelligence.
- Hirer requirement analysis.
- Matching.
- Ranking.
- Refinement question selection.
- Follow-up processing.
- Re-ranking.
- Structured API responses.
- Error handling.

The backend should expose endpoints that the frontend can consume without direct access to internal processing files.

---

# 12. Data and Persistence Requirements

The project should use structured artifacts for reproducibility.

Primary artifacts may include:

```text
dataset_inventory.json
artist_profiles.json
artist_intelligence.json
hirer_intelligence.json
recommendations.json
reranking_results.json
```

If persistent relationship modeling is beneficial, Neo4j may be used to represent:

```text
Artist
    ↓
Capability
    ↓
Evidence
```

and:

```text
Hirer
    ↓
Requirement
    ↓
Artist Match
```

Neo4j should support traceability rather than introduce unnecessary complexity.

---

# 13. Recommendation Requirements

A valid recommendation must include:

1. Artist identity.
2. Rank.
3. Relevant hirer requirements.
4. Matching artist capabilities.
5. Supporting evidence.
6. Confidence or evidence strength.
7. Trade-offs.
8. Assumptions.
9. Important uncertainty.

The system must not simply state:

> Artist A is the best choice.

It should explain:

> Artist A is currently ranked first because the available evidence strongly supports capabilities that match the hirer's most important known requirements, while specific limitations or uncertainties remain visible.

---

# 14. AI Requirements and Boundaries

AI may assist with:

- Structured extraction.
- Media understanding.
- Capability interpretation.
- Requirement extraction.
- Explanation generation.

AI must not:

- Invent evidence.
- Convert unsupported claims into demonstrated capabilities.
- Hide uncertainty.
- Make opaque ranking decisions.
- Repeatedly loop through the same analysis without a stopping condition.

The preferred validation chain is:

```text
Conclusion
    ↓
Capability
    ↓
Evidence
    ↓
Source Reference
```

If this chain cannot be established, the system should return:

```text
Unknown
```

or:

```text
Insufficient Evidence
```

---

# 15. Error Handling Requirements

The application must handle:

- Missing files.
- Unreadable media.
- Invalid dataset structure.
- Missing artist IDs.
- Missing hirer IDs.
- Failed processing.
- Backend failures.
- Database connection failures if Neo4j is used.
- AI provider failures if AI processing is used.

The frontend should display clear messages such as:

```text
We could not load this artist's intelligence data.
Please try again.
```

It should not expose:

- Python stack traces.
- Database credentials.
- Internal exception details.
- API secrets.

---

# 16. Performance Requirements

The system should avoid processing the entire dataset for every user interaction.

Preferred model:

```text
Initial Processing
        ↓
Structured Intelligence
        ↓
Persisted Results
        ↓
Fast API Retrieval
        ↓
Interactive Frontend
```

Heavy processing should be reused when possible.

On-demand processing should primarily be used for:

- Follow-up information.
- Re-ranking.
- Explicit refresh or regeneration operations.

---

# 17. Deployment Requirements

The final project must be accessible online.

## Frontend

```text
Next.js
Hosted on Vercel
```

## Backend

```text
FastAPI
Hosted on Render
```

## Database

If required:

```text
Neo4j
Hosted using a free or free-tier deployment option such as Neo4j AuraDB
```

The project must remain functional using free or free-tier services.

No paid infrastructure should be required for the evaluator to use the core product.

---

# 18. Success Criteria

The product is successful if the evaluator can:

### Dataset Understanding

- [ ] Understand the supplied dataset through the application.

### Artist Intelligence

- [ ] Browse all artists.
- [ ] Inspect structured artist intelligence.
- [ ] Distinguish claims from demonstrated capabilities.
- [ ] Trace conclusions to evidence.
- [ ] See confidence and uncertainty.

### Hirer Understanding

- [ ] Inspect known requirements.
- [ ] See assumptions.
- [ ] See unknowns.
- [ ] Identify contradictions.

### Recommendations

- [ ] View a clear Top 2.
- [ ] Understand why each artist was selected.
- [ ] Inspect requirement-to-capability matching.
- [ ] Understand trade-offs.

### Refinement

- [ ] See no more than two high-impact questions.
- [ ] Understand why the questions matter.

### Re-Ranking

- [ ] Compare initial and updated rankings.
- [ ] Understand what new information changed.
- [ ] Understand why the ranking changed or remained stable.

### Product Delivery

- [ ] Open the deployed frontend.
- [ ] Use the frontend without manually running scripts.
- [ ] Access backend functionality through the deployed API.
- [ ] Inspect the complete workflow end-to-end.

---

# 19. Non-Functional Requirements

## Explainability

Every important recommendation should be traceable to structured evidence.

## Reliability

Failures should produce controlled error states.

## Maintainability

Frontend, backend, intelligence logic, and persistence must remain separated.

## Reproducibility

Important outputs should be stored or reproducible from the dataset.

## Security

Secrets must use environment variables and must not be committed.

## Free-Tier Compatibility

The product should remain deployable with:

- Vercel.
- Render.
- Neo4j free-tier options if persistence is required.

---

# 20. Product Constraints

The project must work within the constraints of the supplied assignment data.

The system should not:

- Invent missing portfolio information.
- Assume unsupported capabilities.
- Require perfect hirer requirements.
- Treat unknown as negative.
- Ask unlimited follow-up questions.
- Hide changes during re-ranking.

---

# 21. Final Product Definition

The final product is:

> A deployed, interactive web application that transforms incomplete artist portfolios and incomplete hirer conversations into structured intelligence and transparent, evidence-backed Top 2 recommendations.

The complete product consists of:

```text
Deployed Frontend
        +
Backend API
        +
Artist Intelligence Pipeline
        +
Hirer Intelligence Pipeline
        +
Evidence-Based Matching
        +
Recommendation Engine
        +
Refinement Logic
        +
Follow-Up Re-Ranking
        +
Structured Persistence
        +
Optional Neo4j Graph Relationships
```

The final experience should allow an evaluator to move from:

```text
Raw Information
```

to:

```text
Structured Evidence
```

to:

```text
Defensible Recommendation
```

and finally:

```text
Updated Decision After New Information
```

without losing visibility into how the system reached its conclusions.
