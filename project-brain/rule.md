# Project Rules, Standards and Engineering Guidelines

# Artist Intelligence & Recommendation System

## 1. Purpose

This document defines the mandatory engineering rules, technology boundaries, coding standards, AI boundaries, dependency policy, error-handling strategy, security requirements, testing standards, performance rules, Git workflow, documentation requirements, and deployment constraints for the project.

These rules exist to ensure that the application remains:

```text
Evidence-First
Transparent
Maintainable
Testable
Reproducible
Secure
Free-Tier Deployable
```

This document applies to:

- Frontend development
- Backend development
- AI-assisted processing
- Dataset processing
- Media analysis
- Recommendation logic
- Neo4j integration
- API design
- Testing
- Deployment
- Documentation

If a future implementation decision conflicts with this document, the architecture and assignment requirements must be reviewed before proceeding.

---

# 2. Core Engineering Principles

Every implementation decision should support at least one of the following:

```text
Evidence Quality
+
Recommendation Quality
+
Explainability
+
Reproducibility
+
Maintainability
```

Avoid adding features or dependencies simply because they are technically interesting.

The preferred principle is:

> Build the simplest implementation that clearly satisfies the assignment and produces a defensible result.

---

# 3. Mandatory Application Architecture

The project is a complete web application.

It must include:

```text
Next.js Frontend
        ↓
Hosted on Vercel
        ↓
HTTPS / REST API
        ↓
FastAPI Backend
        ↓
Intelligence + Matching + Ranking
        ↓
JSON / JSONL Artifacts
        +
Optional Neo4j Persistence
```

## Frontend Responsibilities

The frontend is responsible for:

- Navigation
- User interaction
- Data visualization
- Artist exploration
- Evidence inspection
- Hirer requirement display
- Recommendation display
- Refinement interaction
- Re-ranking comparison
- Loading states
- Error states

The frontend must not independently implement hidden recommendation logic.

---

## Backend Responsibilities

The backend is responsible for:

- Dataset processing
- Artist intelligence
- Hirer intelligence
- Evidence processing
- Matching
- Ranking
- Refinement question generation
- Follow-up processing
- Re-ranking
- Structured API responses
- Persistence access

---

# 4. Approved Technology Stack

## Frontend

Approved primary technologies:

| Technology | Purpose |
|---|---|
| Next.js | Frontend framework |
| React | UI rendering |
| TypeScript | Type safety |
| Tailwind CSS | Styling |
| Lucide React | Icons |

Preferred application model:

```text
Next.js App Router
+
TypeScript
+
Reusable Components
+
Server/Client Components only where appropriate
```

---

## Backend

Approved primary technologies:

| Technology | Purpose |
|---|---|
| Python | Core language |
| FastAPI | API framework |
| Pydantic | Validation and schemas |
| Uvicorn | ASGI server |
| Pytest | Testing |

The backend should use clear separation between:

```text
API
↓
Services
↓
Domain Logic / Engines
↓
Repositories
↓
Storage
```

---

## Data and Persistence

Approved:

| Technology | Purpose |
|---|---|
| JSON | Structured artifacts |
| JSONL | Record-based outputs |
| Neo4j | Optional graph persistence |
| Neo4j Python Driver | Neo4j integration |

Neo4j is optional.

It must only be introduced when relationship persistence improves:

- Traceability
- Evidence relationships
- Artist capability relationships
- Requirement matching relationships
- Recommendation history

If structured JSON/JSONL is sufficient for the assignment, Neo4j must not be introduced merely to increase technical complexity.

---

# 5. Free-Tier Infrastructure Rules

The project must be deployable without requiring paid infrastructure for normal evaluation.

Approved deployment direction:

```text
Frontend
→ Vercel

Backend
→ Render

Database, if required
→ Neo4j AuraDB Free Tier or equivalent supported free option
```

GitHub is the source repository.

## Infrastructure Rules

Do not make the core application dependent on:

- Paid-only APIs
- Paid-only databases
- Paid compute instances
- Infrastructure requiring credit card billing for normal evaluation
- Proprietary services without a fallback plan

If an AI provider requires a key, the implementation must:

1. Use environment variables.
2. Provide a controlled failure state if the key is absent.
3. Avoid exposing the key to the frontend.
4. Document the required configuration.

---

# 6. Approved Libraries and Dependencies

Dependencies should be minimal.

A dependency must have a clear purpose.

## Frontend Dependencies

### Required / Preferred

```text
next
react
react-dom
typescript
tailwindcss
lucide-react
```

### Optional

These may be added only when their value is clear:

| Library Type | Purpose |
|---|---|
| clsx / class-variance-authority | Conditional class composition |
| zod | Client-side schema validation |
| react-hook-form | Form management |
| Recharts | Data visualization if required |
| TanStack Query | API caching and async state if required |

Do not add multiple libraries that solve the same problem.

---

## Backend Dependencies

### Required / Preferred

```text
fastapi
uvicorn
pydantic
pytest
httpx
```

### Optional

| Dependency Type | Purpose |
|---|---|
| neo4j | Graph database integration |
| python-dotenv | Local environment loading |
| Pillow | Image metadata and processing where needed |
| OpenCV | Video/image processing where justified |
| librosa | Audio feature analysis where justified |
| ffmpeg-python | Media processing orchestration where justified |

Only install media-processing libraries that are actually required by the dataset pipeline.

---

# 7. Dependency Version Rules

1. Use stable versions compatible with the project.
2. Pin or constrain backend dependencies appropriately.
3. Avoid unmaintained libraries.
4. Avoid beta versions unless specifically required.
5. Do not install packages globally as a project dependency.
6. Document important dependency decisions.
7. Remove unused dependencies before submission.

Every major dependency should answer:

```text
What problem does this solve?
```

If the answer is unclear, do not add it.

---

# 8. What to Avoid

## Avoid Unnecessary Frameworks

Do not introduce additional major frameworks such as:

- Django
- Flask
- Express
- Multiple frontend frameworks

The approved architecture already provides:

```text
Next.js
+
FastAPI
```

Adding competing frameworks increases complexity without improving the assignment outcome.

---

## Avoid Over-Engineering

Do not add:

- Microservices
- Kubernetes
- Kafka
- Redis
- Message queues
- Multiple databases
- Authentication systems
- Complex event architectures

unless a concrete assignment requirement makes them necessary.

This project is an evaluation application, not a production hyperscale platform.

---

## Avoid Unnecessary Database Complexity

Do not introduce Neo4j if:

```text
JSON / JSONL
```

already provides sufficient reproducibility and traceability.

Use Neo4j when the graph model provides real value.

---

## Avoid Hidden Recommendation Logic

Do not place ranking algorithms:

- Only inside frontend components
- Inside UI event handlers
- Inside untraceable LLM prompts

Ranking logic must remain inspectable in backend domain code.

---

## Avoid Generic AI Output

Do not allow the system to produce:

```text
Artist A is the best choice.
```

without structured justification.

Every recommendation must connect to:

```text
Requirement
↓
Capability
↓
Evidence
↓
Recommendation
```

---

# 9. Data Rules

## Raw Data Is Immutable

Files under:

```text
data/raw/
```

must not be modified.

All processing outputs must be stored separately.

Example:

```text
data/
├── raw/
└── processed/
```

---

## Processed Data Must Be Reproducible

Important outputs should be reproducible from:

- The original dataset
- Processing configuration
- Defined pipeline logic

Important outputs include:

```text
dataset_inventory.json
artist_intelligence.json
hirer_intelligence.json
recommendations.json
reranking_results.json
```

---

## Unknown Is Not Negative

Never convert missing evidence into:

```text
Not Capable
```

Use explicit states such as:

```text
UNKNOWN
```

or:

```text
INSUFFICIENT_EVIDENCE
```

---

# 10. Artist Intelligence Rules

Artist intelligence must separate:

```text
Profile Claim
```

from:

```text
Demonstrated Capability
```

A self-description alone must not automatically create a demonstrated capability.

A demonstrated capability should include:

```text
Capability
+
Evidence
+
Source Reference
+
Confidence
```

If the evidence chain is incomplete, the result must communicate uncertainty.

---

# 11. Media Processing Rules

## Do Not Process Everything Blindly

The system should not automatically perform expensive deep analysis on every media file.

Use:

```text
Inventory
↓
Inspection
↓
Representative Selection
↓
Analysis
↓
Evidence Recording
```

---

## Selection Must Be Explainable

When representative media is selected, record:

- Artist
- Media identifier
- Media type
- Selection reason
- Processing result
- Processing status

If media is skipped, the system should be able to explain why when relevant.

---

## Processing Failures

Unreadable or damaged media must not crash the entire pipeline.

The system should record:

```text
status = FAILED
```

with a controlled reason.

Other valid media should continue processing.

---

# 12. AI Boundaries

AI is an assisting mechanism, not the source of truth.

## AI May Be Used For

- Structured extraction
- Text interpretation
- Media interpretation
- Capability suggestions
- Requirement extraction
- Contradiction detection
- Explanation generation

## AI Must Not

- Invent evidence
- Invent artist capabilities
- Hide uncertainty
- Treat claims as proof
- Produce unsupported recommendations
- Silently overwrite historical recommendations
- Continue repeated processing loops indefinitely

---

# 13. Anti-Hallucination Rules

Every significant conclusion should follow:

```text
Conclusion
↓
Capability / Requirement
↓
Evidence
↓
Source Reference
```

If evidence is unavailable:

```text
UNKNOWN
```

or:

```text
INSUFFICIENT_EVIDENCE
```

must be returned.

The AI layer must never convert:

```text
No Evidence
```

into:

```text
Negative Evidence
```

---

# 14. AI Loop and Retry Boundaries

AI calls and processing retries must have explicit limits.

Recommended rules:

```text
Maximum automatic retry attempts: 2
```

After the limit:

```text
Return controlled failure
+
Log the failure
+
Allow manual retry where appropriate
```

Do not create:

```text
Analyze
↓
Failure
↓
Analyze Again
↓
Failure
↓
Analyze Again
↓
...
```

Each processing task must have a terminal state:

```text
SUCCESS
FAILED
SKIPPED
INSUFFICIENT_EVIDENCE
```

---

# 15. Error Handling Rules

All application errors must be controlled.

## Backend Error Flow

```text
Exception
↓
Service-Level Handling
↓
Structured Application Error
↓
FastAPI Response
↓
Frontend Error State
```

## Standard API Error Shape

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "User-friendly explanation.",
    "details": null
  }
}
```

The exact schema may evolve, but error responses must remain consistent.

---

## Frontend Error Rules

The frontend must provide:

- Clear error messages
- Retry controls when useful
- Loading states
- Empty states
- No raw backend tracebacks

Example:

```text
Unable to load recommendation data.
Please try again.
```

Do not display:

- Stack traces
- Database errors
- Internal file paths
- Secrets

---

# 16. Logging Rules

Use structured logging where practical.

Log:

- Pipeline start
- Pipeline completion
- Processing failures
- Important validation failures
- Database connection failures
- External API failures

Do not log:

- API keys
- Passwords
- Database credentials
- Sensitive environment variables

Logs should help reproduce failures without exposing secrets.

---

# 17. API Design Rules

API endpoints must:

- Use clear resource naming.
- Validate inputs.
- Return predictable response structures.
- Use appropriate HTTP status codes.
- Avoid leaking implementation details.

Example status categories:

```text
200 → Success
201 → Created
400 → Invalid request
404 → Resource not found
422 → Validation failure
500 → Unexpected server error
503 → Dependency unavailable
```

Do not return `200 OK` for an operation that clearly failed.

---

# 18. Frontend Coding Rules

## Component Design

Prefer:

```text
Small
Reusable
Focused
Typed
```

components.

Avoid giant page files containing:

- API logic
- Ranking logic
- Complex transformations
- Multiple unrelated UI concerns

---

## API Access

Centralize API communication.

Recommended:

```text
frontend/
└── lib/
    └── api.ts
```

Do not scatter backend URLs across components.

Use:

```text
NEXT_PUBLIC_API_BASE_URL
```

for environment-specific API configuration.

---

## State Management

Use the simplest state mechanism that satisfies the requirement.

Prefer:

```text
React state
↓
Context only when necessary
↓
Dedicated state library only if complexity justifies it
```

Do not introduce global state management libraries without a clear need.

---

# 19. Backend Coding Rules

## Separation of Concerns

Recommended flow:

```text
Route
↓
Service
↓
Domain Engine / Pipeline
↓
Repository
```

Routes should not contain complex business logic.

Repositories should not contain recommendation policy.

Recommendation engines should not depend on HTTP request objects.

---

## Data Validation

Use Pydantic models for:

- Request validation
- Response contracts
- Structured internal data where useful

Do not pass unvalidated dictionaries throughout the entire application when a stable schema is known.

---

# 20. Naming Conventions

## Python

```text
snake_case
```

Examples:

```text
artist_service.py
recommendation_engine.py
get_artist_by_id()
```

Classes:

```text
PascalCase
```

Example:

```text
RecommendationService
```

Constants:

```text
UPPER_SNAKE_CASE
```

---

## TypeScript

Variables and functions:

```text
camelCase
```

Components and types:

```text
PascalCase
```

Examples:

```text
ArtistCard
RecommendationResult
getArtistDetails
```

Files should follow the existing Next.js conventions.

---

# 21. Code Style and Formatting

## General Rules

Code should be:

- Readable
- Consistent
- Modular
- Minimal
- Explicit where decisions matter

Avoid clever but difficult-to-maintain abstractions.

---

## Python

Recommended tooling:

```text
ruff
pytest
```

Optional formatting/lint configuration may include:

```text
black
```

if it does not conflict with the chosen project setup.

Choose one consistent formatting workflow.

---

## TypeScript

Use:

```text
ESLint
```

and the project's standard formatting configuration.

Before submission, frontend code should pass:

```text
npm run lint
```

and, where configured:

```text
npm run type-check
```

---

# 22. Commenting Rules

Do not add comments that merely repeat the code.

Bad:

```text
# Get artist
artist = get_artist()
```

Good comments explain:

- Why a decision exists
- Why a trade-off was made
- Why a non-obvious rule is necessary

Important recommendation and evidence logic should be documented when the reasoning cannot be understood directly from the code structure.

---

# 23. Git and Commit Standards

Use small, meaningful commits.

Recommended commit format:

```text
feat: add artist intelligence endpoint
fix: handle unreadable media files
docs: update architecture decisions
test: add ranking edge cases
refactor: separate matching engine
chore: update dependencies
```

Avoid commit messages such as:

```text
update
changes
final
fix everything
```

Do not combine unrelated changes into one commit when avoidable.

---

# 24. Branching Rules

For individual development, a simple workflow is acceptable:

```text
main
```

Optional:

```text
feature/<feature-name>
fix/<issue-name>
```

The main branch should remain:

- Buildable
- Testable
- Deployable

Do not leave intentionally broken experimental code on the submission branch.

---

# 25. Security and Data Privacy Rules

## Secrets

Secrets must only exist in:

```text
.env
```

or deployment environment variables.

Never commit:

```text
API keys
Passwords
Neo4j credentials
Private tokens
```

The repository must include:

```text
.env.example
```

with placeholder values only.

---

## Frontend Security

The frontend must never contain private backend secrets.

Variables prefixed with:

```text
NEXT_PUBLIC_
```

must be considered publicly exposed.

Do not place secret credentials in these variables.

---

## Backend Security

Validate:

- Artist IDs
- Hirer IDs
- Follow-up payloads
- Any file-related input

Do not trust frontend input.

---

# 26. Neo4j Rules

Neo4j is optional.

If used:

## Neo4j Should Store

- Artists
- Capabilities
- Claims
- Evidence metadata
- Requirements
- Match relationships
- Recommendation relationships

## Neo4j Should Not Store

- Large raw videos
- Large audio files
- Large image binaries
- Secrets
- Raw environment configuration

Use Neo4j for relationships.

Use file metadata or structured storage references for media.

---

# 27. Performance Rules

## Precompute Where Possible

Avoid:

```text
Frontend Request
↓
Reprocess Entire Dataset
↓
Return Result
```

Prefer:

```text
Dataset Processing
↓
Persist Structured Results
↓
API Retrieval
↓
Frontend Display
```

---

## Expensive Processing

Media processing should:

- Be selective.
- Be cached or persisted where appropriate.
- Avoid repeated analysis of unchanged files.

Follow-up processing may run dynamically because it represents new information.

---

# 28. Recommendation Rules

The recommendation engine must be:

```text
Requirement-Aware
Evidence-Aware
Uncertainty-Aware
Explainable
```

Every recommendation should connect:

```text
Hirer Requirement
↓
Artist Capability
↓
Supporting Evidence
↓
Recommendation Reason
```

Do not allow opaque ranking logic that cannot explain why an artist was ranked above another.

---

# 29. Refinement Question Rules

The system may ask:

```text
Maximum 2 questions
```

A question must satisfy at least one:

- Resolve an important unknown.
- Resolve a contradiction.
- Potentially change the ranking.
- Clarify a high-priority requirement.

Do not ask questions for information that will not affect the decision.

Recommendations should appear before refinement questions.

---

# 30. Re-Ranking Rules

Never silently overwrite the initial ranking.

Preserve:

```text
Initial Requirements
Initial Ranking
Initial Assumptions
```

Then record:

```text
Follow-Up Information
```

Then produce:

```text
Updated Requirements
Updated Ranking
Explanation of Change
```

The frontend must make before/after comparison visible.

---

# 31. Testing Rules

Testing is required for core logic.

## Backend Unit Tests

Test:

- Requirement extraction transformations where deterministic.
- Matching logic.
- Ranking logic.
- Refinement question limits.
- Unknown handling.
- Invalid IDs.
- Re-ranking behavior.

Important rule:

```text
Unknown ≠ Not Capable
```

must have explicit test coverage.

---

## Backend Integration Tests

Test:

- API endpoints.
- Request validation.
- Error responses.
- Data loading.
- Optional Neo4j integration if enabled.

---

## Frontend Validation

At minimum verify:

- Build succeeds.
- Lint succeeds.
- Type checking succeeds if configured.
- Critical pages render.
- API loading states work.
- API error states work.
- Recommendation and re-ranking views work.

---

# 32. Minimum Validation Commands

Before submission, the project should support appropriate commands such as:

## Frontend

```text
npm install
npm run lint
npm run build
```

If available:

```text
npm run type-check
npm test
```

## Backend

```text
pip install -r requirements.txt
pytest
```

The exact command structure may evolve, but all documented commands must work from a clean setup.

---

# 33. Documentation Rules

The repository must contain clear documentation.

Required:

```text
README.md
docs/PRD.md
docs/architecture.md
docs/rule.md
docs/phases.md
docs/design.md
docs/memory.md
```

The README should explain:

- Project purpose.
- Problem being solved.
- High-level architecture.
- Technology stack.
- Local setup.
- Environment variables.
- Running frontend.
- Running backend.
- Testing.
- Deployment.
- Assignment workflow.

Documentation must match the actual implementation.

Do not document features that do not exist.

---

# 34. Documentation Update Rule

When a major decision changes, update the relevant document.

Examples:

```text
Architecture changed
→ architecture.md

Product scope changed
→ PRD.md

Engineering rule changed
→ rule.md

Development progress changed
→ memory.md

Phase completion changed
→ phases.md
```

The documentation should remain synchronized with the codebase.

---

# 35. Deployment Rules

## Frontend

Deploy to:

```text
Vercel
```

The frontend must use environment-based API configuration.

Do not hard-code:

```text
localhost
```

as the production backend URL.

---

## Backend

Deploy to:

```text
Render
```

The backend must:

- Bind to the provided deployment port.
- Read configuration from environment variables.
- Configure production CORS correctly.
- Expose a health endpoint.

Recommended:

```text
GET /api/health
```

---

## Health Endpoint

The backend should provide a lightweight health check.

Example response:

```json
{
  "status": "healthy"
}
```

The health endpoint should not trigger expensive dataset processing.

---

# 36. CORS Rules

Allow only required frontend origins.

Development example:

```text
http://localhost:3000
```

Production example:

```text
https://<project>.vercel.app
```

Avoid:

```text
allow_origins=["*"]
```

in production unless there is a clearly documented reason.

---

# 37. Environment Configuration Rules

Every required environment variable must be documented in:

```text
.env.example
```

Example backend:

```text
ENVIRONMENT=development
FRONTEND_ORIGINS=http://localhost:3000
LOG_LEVEL=INFO

NEO4J_URI=
NEO4J_USERNAME=
NEO4J_PASSWORD=

AI_PROVIDER=
AI_API_KEY=
```

Example frontend:

```text
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

Do not place real values in `.env.example`.

---

# 38. Submission Quality Rules

Before final submission:

- [ ] Frontend builds successfully.
- [ ] Backend starts successfully.
- [ ] Core API endpoints work.
- [ ] Health endpoint works.
- [ ] Dataset inventory is available.
- [ ] Artist intelligence is visible.
- [ ] Hirer intelligence is visible.
- [ ] Top 2 recommendation is visible.
- [ ] Evidence is traceable.
- [ ] Maximum 2 refinement questions are enforced.
- [ ] Follow-up re-ranking works.
- [ ] Initial and updated rankings are distinguishable.
- [ ] Error states are handled.
- [ ] No secrets are committed.
- [ ] Documentation matches implementation.
- [ ] Production frontend communicates with production backend.
- [ ] Free-tier deployment is functional.

---

# 39. Final Decision Rule

When there are multiple possible technical approaches, choose the option that best satisfies:

```text
Assignment Requirement
        ↓
Evidence Quality
        ↓
Explainability
        ↓
Reliability
        ↓
Implementation Simplicity
        ↓
Free-Tier Compatibility
```

Do not choose a technology because it is more advanced.

Choose it because it improves the product.

---

# 40. Single Source of Truth

The following documents must remain aligned:

```text
PRD.md
architecture.md
rule.md
phases.md
design.md
memory.md
```

If implementation decisions change, update the relevant documents and record the major decision in `memory.md`.

The project's primary engineering philosophy is:

> Make every important recommendation explainable, every important conclusion traceable, and every major technical decision justified.
