# UI/UX Design Specification

# Artist Intelligence & Recommendation System

## 1. Purpose

This document defines the complete UI/UX design direction for the deployed **Artist Intelligence & Recommendation System**.

The interface is not intended to be a generic dashboard or portfolio gallery.

It must visually communicate a decision-making process:

```text
Raw Information
        ↓
Structured Intelligence
        ↓
Evidence
        ↓
Recommendation
        ↓
Refinement
        ↓
Updated Decision
```

The design must help an evaluator quickly understand:

- What data exists.
- What the system extracted.
- What is claimed.
- What is demonstrated.
- What evidence supports a conclusion.
- What the hirer actually needs.
- What remains uncertain.
- Why the Top 2 artists were selected.
- What trade-offs exist.
- How follow-up information changes the ranking.

The UI should prioritize:

```text
Clarity
+
Evidence Visibility
+
Decision Transparency
+
Visual Hierarchy
+
Interactive Exploration
```

over unnecessary decoration.

---

# 2. Design Goals

## Primary Goal

Make the complete intelligence and recommendation workflow understandable through the frontend without requiring the evaluator to inspect raw JSON, run scripts, or read backend code.

## Secondary Goals

The interface should:

- Feel modern and technically polished.
- Support fast evaluation.
- Make complex relationships easy to understand.
- Keep uncertainty visible.
- Encourage exploration without overwhelming the user.
- Work on desktop and mobile.
- Clearly distinguish different data states.
- Provide responsive feedback during processing and API communication.

---

# 3. Target Experience

The primary evaluator journey is:

```text
Landing / Dashboard
        ↓
Understand Dataset
        ↓
Explore Artists
        ↓
Inspect Artist Intelligence
        ↓
Trace Evidence
        ↓
Inspect Hirer Requirements
        ↓
View Top 2 Recommendation
        ↓
Compare Trade-Offs
        ↓
Answer / Review Refinement Questions
        ↓
Inspect Updated Ranking
```

The interface should make this journey obvious through navigation and progressive disclosure.

The user should never feel forced to understand the entire technical architecture before understanding the recommendation.

---

# 4. Design Philosophy

The visual language should feel like:

```text
AI Intelligence Console
+
Creative Portfolio System
+
Decision Analytics Dashboard
```

It should not feel like:

- A plain admin panel.
- A generic SaaS template.
- A social media application.
- A visually overloaded cyberpunk interface.
- A portfolio website with no decision intelligence.

The dark theme provides the base environment, while accent colors communicate meaning and interaction.

---

# 5. Color and Theme System

## Base Theme

The primary experience is a **dark interactive interface**.

The background should create depth through multiple surface layers rather than relying on one flat black color.

Suggested visual structure:

```text
Page Background
↓
Section Surface
↓
Card Surface
↓
Interactive / Elevated Surface
```

Use neutral dark tones for the structural foundation.

Avoid:

```text
Pure black everywhere
```

because it can flatten hierarchy and make long-form information difficult to scan.

---

## Accent Colors

The required interactive accent family is:

```text
Blue
Orange
Purple
Red
```

These colors should have semantic roles rather than being applied randomly.

### Blue — Primary Intelligence and Interaction

Use for:

- Primary buttons.
- Active navigation.
- Links.
- Selected filters.
- Verified or strongly supported information.
- Primary data relationships.
- Important interactive states.

Concept:

```text
Blue = Active / Primary / Intelligence
```

---

### Orange — Attention and Trade-Off

Use for:

- Important trade-offs.
- Medium-confidence information.
- Areas requiring attention.
- Pending decisions.
- Important assumptions.

Concept:

```text
Orange = Attention / Trade-Off / Review
```

---

### Purple — AI and Derived Intelligence

Use for:

- AI-assisted analysis.
- Derived insights.
- Intelligence processing.
- Refinement suggestions.
- Recommendation reasoning.
- Re-ranking transitions.

Concept:

```text
Purple = AI / Derived Intelligence
```

---

### Red — Risk, Conflict and Failure

Use for:

- Contradictions.
- Failed processing.
- Important warnings.
- Critical uncertainty.
- Error states.

Concept:

```text
Red = Conflict / Failure / Risk
```

Red should not be used as a general decorative color.

---

# 6. Semantic State System

Every important state should have a consistent visual representation.

| State | Meaning | Suggested Visual Direction |
|---|---|---|
| Verified / Strong Evidence | Strong support exists | Blue accent |
| AI-Derived Insight | Generated or interpreted intelligence | Purple accent |
| Attention / Trade-Off | Requires review or comparison | Orange accent |
| Conflict / Error | Contradiction or failure | Red accent |
| Unknown | Information unavailable | Neutral muted surface |
| Insufficient Evidence | Not enough proof to conclude | Neutral + subtle warning treatment |
| Processing | Operation in progress | Blue/Purple animated indicator |
| Success | Completed operation | Positive semantic indicator, distinct from recommendation colors |

Important:

```text
Unknown
```

must never visually appear equivalent to:

```text
Negative
```

The UI should explicitly label unknown states.

---

# 7. Typography

## Font Direction

Use a modern, highly readable sans-serif font.

Preferred characteristics:

- Strong screen readability.
- Good number rendering.
- Clear hierarchy.
- Support for dense dashboard information.
- Professional but not overly corporate.

A suitable implementation may use a font available through the Next.js font system.

The final font choice should prioritize readability over novelty.

---

## Typography Hierarchy

Recommended hierarchy:

```text
Display / Page Title
        ↓
Section Title
        ↓
Card Title
        ↓
Body
        ↓
Metadata
        ↓
Evidence Reference
```

### Page Titles

Used for:

- Artists
- Hirer Intelligence
- Recommendations
- Re-Ranking

Should be visually strong and easy to identify.

### Section Titles

Used to separate:

- Claims
- Demonstrated Capabilities
- Evidence
- Unknowns
- Assumptions
- Trade-Offs

### Body Text

Must remain comfortable to read on dark surfaces.

### Metadata

Use smaller, muted text for:

- Source identifiers
- File types
- Processing timestamps
- Confidence labels
- IDs

Do not use excessively small text for important evidence.

---

# 8. Spacing and Layout

Use a consistent spacing system.

The interface should rely on:

```text
Whitespace
+
Grouping
+
Alignment
+
Surface Hierarchy
```

rather than excessive borders.

Recommended layout principles:

- Consistent horizontal page padding.
- Clear separation between major sections.
- Moderate density for dashboards.
- More breathing room around recommendation results.
- Cards should support scanning rather than becoming large text containers.

Avoid:

- Too many nested cards.
- Excessive rounded containers.
- Every paragraph inside a bordered box.

---

# 9. Application Shell

The main application shell should contain:

```text
┌───────────────────────────────────────────────┐
│ Top Bar / Brand / Status                      │
├───────────────┬───────────────────────────────┤
│ Navigation    │ Main Content                  │
│               │                               │
│ Dashboard     │ Dynamic Page Content          │
│ Artists       │                               │
│ Hirer Brief   │                               │
│ Recommendations                               │
│ Re-Ranking    │                               │
└───────────────┴───────────────────────────────┘
```

## Desktop

Preferred structure:

- Persistent sidebar where appropriate.
- Main content area.
- Top-level status or environment indicator.
- Responsive content width.

## Mobile

Navigation should collapse into:

- Drawer.
- Sheet.
- Or compact mobile navigation.

Do not simply shrink the desktop sidebar until it becomes unusable.

---

# 10. Navigation

Primary navigation:

```text
Overview
Artists
Hirer Intelligence
Recommendations
Re-Ranking
```

Optional secondary navigation:

```text
Evidence
Dataset
System Status
```

Navigation must communicate the workflow.

Recommended conceptual sequence:

```text
Data
→ Intelligence
→ Decision
→ Update
```

The active page should be clearly visible using the primary interaction color.

---

# 11. Dashboard Design

## Purpose

The dashboard should provide immediate understanding of the project and available data.

It should answer:

> What is inside this system, and where should I begin?

## Dashboard Sections

### Hero / Introduction

Display:

- Product name.
- One-sentence purpose.
- Short explanation of evidence-first recommendations.

Example structure:

```text
Artist Intelligence
Evidence-backed recommendations from incomplete portfolios and hirer requirements.
```

---

### Dataset Summary

Use compact metrics such as:

```text
Total Artists
Available Categories
Media Items
Hirer Cases
Processed Records
```

Metrics should link to deeper exploration where useful.

---

### Intelligence Status

Display processing states:

```text
Artist Intelligence
Hirer Intelligence
Recommendation Engine
Data Availability
```

Use semantic state indicators.

---

### Quick Start Flow

Show a simple visual sequence:

```text
1. Explore Artists
2. Inspect Hirer Needs
3. Review Recommendations
4. Compare Re-Ranking
```

This is particularly useful for assignment evaluation.

---

# 12. Artist Explorer Design

## Purpose

Allow the evaluator to discover the available artists without immediately exposing every detail.

## Layout

Recommended structure:

```text
Page Header
        ↓
Search / Filters
        ↓
Category Controls
        ↓
Artist Grid / List
```

Each artist card may display:

- Artist name or ID.
- Category.
- Short intelligence summary.
- Number or presence of evidence records.
- Capability highlights.
- Confidence summary.

The card should allow navigation to the artist detail page.

Avoid displaying long paragraphs on artist cards.

---

# 13. Artist Detail Design

The artist detail page is one of the most important screens.

## Page Structure

```text
Artist Header
        ↓
Profile Overview
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

---

## Artist Header

Display:

- Artist name.
- Category.
- Summary.
- High-level evidence status.

If visual media exists and is useful, use a relevant media preview.

Do not use decorative images unrelated to the dataset.

---

## Claims Section

Claims must be clearly labeled.

Example:

```text
CLAIMED
Motion Graphics
```

A claim should not visually imply verification.

Suggested treatment:

- Neutral or orange-accented label.
- Explicit source context.

---

## Demonstrated Capabilities

This section should use a stronger visual treatment.

Example:

```text
DEMONSTRATED

✓ Capability Name
Evidence strength: Strong
```

Each capability should be expandable to reveal evidence.

---

## Unknown / Insufficient Evidence

This section should explicitly communicate:

```text
Insufficient evidence available to verify X.
```

Avoid red unless the state represents an actual failure or contradiction.

Unknown is informational, not necessarily negative.

---

# 14. Evidence Explorer Design

## Purpose

Allow the evaluator to answer:

> Why does the system believe this?

## Evidence Card

Each evidence item may contain:

```text
Evidence Type
Source
Capability Supported
Evidence Summary
Confidence
Media / File Reference
```

If supported by the implementation, users can expand the card to inspect:

- Media metadata.
- Source excerpt.
- Selection rationale.
- Processing result.

---

## Evidence Trace

For important recommendations, visualize:

```text
Requirement
      ↓
Capability
      ↓
Evidence
```

This can be represented through:

- Connected cards.
- Step indicators.
- Relationship lines.
- Expandable trace panels.

The design should remain understandable without requiring a complex graph visualization.

---

# 15. Hirer Intelligence Design

## Purpose

Convert an unstructured conversation into an understandable decision brief.

The page should visually separate:

```text
Known
Assumed
Unknown
Conflicting
```

## Recommended Layout

```text
Hirer Brief Header
        ↓
Known Requirements
        ↓
Preferences + Constraints
        ↓
Assumptions
        ↓
Unknowns
        ↓
Contradictions
```

---

## Known Requirements

Use the strongest visual emphasis because these directly influence the current ranking.

Each requirement can show:

- Requirement description.
- Importance.
- Source.
- Confidence if relevant.

---

## Assumptions

Use an orange-accented treatment.

Explicitly label:

```text
ASSUMPTION
```

Do not visually merge assumptions with confirmed requirements.

---

## Unknowns

Use muted neutral treatment.

Example:

```text
UNKNOWN
Budget information is not available.
```

---

## Contradictions

Use red-accented treatment.

Each contradiction should explain:

- The conflicting statements.
- Why the conflict matters.
- Whether clarification may affect ranking.

---

# 16. Recommendations Design

This is the primary decision screen.

The design should answer immediately:

```text
Who are the current Top 2 artists?
```

## Page Structure

```text
Recommendation Header
        ↓
Decision Context
        ↓
Top 2 Artist Comparison
        ↓
Why They Fit
        ↓
Evidence Trace
        ↓
Trade-Offs
        ↓
Uncertainty
        ↓
Refinement Questions
```

---

# 17. Top 2 Recommendation Cards

The Top 2 should be visually distinct.

## Rank 1

Should have the strongest visual emphasis.

Display:

```text
#1 Recommended
Artist
Overall Match Context
Key Strengths
Trade-Off
Confidence
```

The primary recommendation should not visually hide its limitations.

---

## Rank 2

Display as a strong alternative.

Show:

```text
#2 Alternative
Artist
Where This Artist Is Stronger
Where This Artist Is Weaker
Key Evidence
Trade-Off
```

The comparison should make the decision understandable rather than simply showing two score bars.

---

# 18. Recommendation Explanation Design

Each recommendation should support progressive disclosure.

## Summary Level

Show:

```text
Why this artist fits.
```

## Detailed Level

Allow inspection of:

```text
Requirement
↓
Matched Capability
↓
Supporting Evidence
```

The evaluator should be able to move from a simple recommendation to detailed evidence without leaving the page unnecessarily.

---

# 19. Trade-Off Visualization

Trade-offs should be explicit.

Recommended comparison structure:

| Decision Area | Rank 1 | Rank 2 |
|---|---|---|
| Requirement A | Strong | Moderate |
| Requirement B | Moderate | Strong |
| Evidence Strength | Strong | Strong |
| Important Unknown | Limited | Moderate |

The exact information should come from the recommendation engine rather than being hard-coded.

Avoid excessive numeric precision.

For example:

```text
82.739%
```

is usually less understandable than:

```text
Strong Match
```

unless the precise score is necessary and explainable.

---

# 20. Confidence and Uncertainty Design

Confidence should not be represented as absolute truth.

Prefer understandable labels:

```text
High Evidence Support
Moderate Evidence Support
Limited Evidence
Insufficient Evidence
```

If numerical confidence is shown, pair it with a text explanation.

Example:

```text
High Evidence Support
Confidence: 0.86
```

Never display confidence without context.

---

# 21. Refinement Question Design

The application must ask at most:

```text
2 questions
```

## Question Card

Each question should display:

```text
Question
```

Then:

```text
Why this matters
```

Then:

```text
Possible ranking impact
```

Example structure:

```text
QUESTION 1

Which requirement should be prioritized most?

WHY THIS MATTERS
The current top two artists are strong in different areas.

POTENTIAL IMPACT
This answer may change the top-ranked artist.
```

Use purple as the primary accent because this represents derived decision intelligence.

---

# 22. Re-Ranking Design

The re-ranking screen must preserve decision history.

Do not simply replace the old ranking with the new one.

## Required Flow

```text
Initial State
        ↓
Follow-Up Information
        ↓
Updated State
```

---

## Initial Ranking

Show:

```text
#1 Artist
#2 Artist
```

with a summary of the original assumptions.

---

## Follow-Up

Display:

- New information.
- Resolved unknowns.
- Changed priorities.

Clearly label the information as:

```text
NEW INFORMATION
```

---

## Updated Ranking

Show:

```text
Previous Rank
→
New Rank
```

Example:

```text
#2 → #1
```

or:

```text
#1 → #1
Ranking remained stable
```

---

## Change Explanation

The system must explain:

```text
What changed?
Why did it change?
Which requirement was affected?
Which evidence or capability became more important?
```

This is a critical evaluator-facing feature.

---

# 23. Data Visualization Guidelines

Visualizations should only be added when they improve understanding.

Possible useful visualizations:

- Artist category distribution.
- Evidence coverage.
- Requirement importance.
- Recommendation comparison.
- Ranking movement.

Avoid charts that exist only for decoration.

## Chart Rules

- Every chart needs a clear title.
- Every important value needs context.
- Avoid excessive colors.
- Use semantic colors consistently.
- Ensure accessibility and readable labels.

---

# 24. Loading States

The application must communicate processing.

Use:

- Skeleton loading for page content.
- Inline loading indicators for actions.
- Progress or status messages for longer operations.

Example:

```text
Analyzing follow-up information...
Updating recommendation...
```

Do not leave the user staring at an unchanging screen.

---

# 25. Error States

Errors should be clear and controlled.

Example:

```text
Unable to load artist intelligence.

The data could not be retrieved right now.
Please try again.
```

Where useful, provide:

```text
Retry
```

Do not expose:

- Stack traces.
- Raw API exceptions.
- Database errors.
- Internal infrastructure details.

---

# 26. Empty States

Empty states should explain what is missing.

Example:

```text
No supporting evidence is currently available for this capability.
```

Do not use vague messages such as:

```text
No data.
```

when a more useful explanation can be shown.

---

# 27. Responsive Design

The application must support:

```text
Desktop
Tablet
Mobile
```

## Desktop

Prioritize:

- Comparison.
- Evidence inspection.
- Dense but readable information.
- Side-by-side recommendation analysis.

## Tablet

Reduce multi-column density while preserving hierarchy.

## Mobile

Convert:

```text
Side-by-side
```

into:

```text
Stacked sections
```

Important information must remain visible without horizontal scrolling.

Tables should transform into cards or scrollable containers when necessary.

---

# 28. Accessibility Rules

The UI should support:

- Readable contrast.
- Keyboard navigation.
- Visible focus states.
- Semantic HTML.
- Meaningful labels.
- Accessible buttons.
- Color-independent status labels.

Do not rely only on color to communicate:

```text
Success
Warning
Failure
Unknown
```

Every state should also include text, iconography, or labels.

---

# 29. Motion and Interaction

Use motion to communicate state changes.

Appropriate uses:

- Card hover feedback.
- Page transitions.
- Expand/collapse.
- Ranking movement.
- Loading indicators.
- Re-ranking updates.

Avoid:

- Constant decorative animation.
- Excessive movement.
- Long blocking animations.

Motion should support comprehension.

---

# 30. Processing and Performance Experience

The frontend should feel responsive even when backend operations take time.

Preferred strategy:

```text
Initial Data
→ Load Quickly

Heavy Processing
→ Show Status

Completed Result
→ Update UI
```

Where possible:

- Precomputed intelligence should load from persisted results.
- Follow-up re-ranking can trigger dynamic processing.
- Repeated unchanged processing should be avoided.

The UI must not freeze during asynchronous operations.

---

# 31. Preferred Language and Content Tone

The primary application language is:

```text
English
```

The writing style should be:

- Clear.
- Direct.
- Professional.
- Easy to understand.
- Evidence-oriented.

Avoid:

- Excessive AI terminology.
- Long paragraphs.
- Unexplained technical jargon.
- Overconfident wording.

Preferred wording:

```text
Supported by available evidence
```

instead of:

```text
Proven with certainty
```

when the data does not justify absolute certainty.

---

# 32. Content Rules

Every important conclusion shown in the UI should answer one or more:

```text
What do we know?
What supports this?
What is assumed?
What is unknown?
Why does this affect the decision?
```

The UI should preserve the project's evidence chain:

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

# 33. Component Design System

Recommended reusable components:

```text
AppShell
Sidebar
TopBar
PageHeader
SectionHeader

MetricCard
ArtistCard
CapabilityCard
EvidenceCard
RequirementCard

StatusBadge
ConfidenceBadge
EvidenceBadge

RecommendationCard
TradeOffCard
QuestionCard
RankingChangeCard

LoadingState
ErrorState
EmptyState
```

The exact names may change, but repeated UI patterns should be implemented as reusable components.

Avoid duplicating complex UI structures across pages.

---

# 34. Suggested Page Structure

```text
app/
├── page.tsx
├── artists/
│   ├── page.tsx
│   └── [artistId]/
│       └── page.tsx
├── hirers/
│   ├── page.tsx
│   └── [hirerId]/
│       └── page.tsx
├── recommendations/
│   ├── page.tsx
│   └── [hirerId]/
│       └── page.tsx
├── reranking/
│   └── [hirerId]/
│       └── page.tsx
└── layout.tsx
```

Reusable UI:

```text
components/
├── layout/
├── artists/
├── evidence/
├── hirers/
├── recommendations/
├── reranking/
└── ui/
```

API communication:

```text
lib/
└── api.ts
```

Types:

```text
types/
├── artist.ts
├── evidence.ts
├── hirer.ts
└── recommendation.ts
```

---

# 35. Frontend-to-Backend UX Rules

The frontend communicates with:

```text
FastAPI Backend
```

using:

```text
NEXT_PUBLIC_API_BASE_URL
```

The UI must handle all API states:

```text
Loading
Success
Empty
Error
Unavailable
```

If the backend is unavailable, the UI should clearly communicate this rather than appearing permanently empty.

Example:

```text
The intelligence service is currently unavailable.
Please try again shortly.
```

---

# 36. Vercel and Render Production UX

The production application must work through:

```text
Vercel Frontend
        ↓
Render Backend
```

The frontend must not contain:

```text
localhost
```

as the production API endpoint.

Production validation should confirm:

- Pages load correctly.
- API requests succeed.
- CORS is configured correctly.
- Backend cold-start or temporary availability states are handled gracefully.
- Retry behavior does not create repeated request loops.

---

# 37. Anti-Patterns to Avoid

Do not:

- Use every accent color in every component.
- Hide uncertainty behind a single score.
- Display claims as verified capabilities.
- Show raw JSON to users as the primary interface.
- Build giant unreadable dashboard tables.
- Add charts without decision value.
- Use endless loading spinners.
- Show technical exceptions to the evaluator.
- Make the Top 2 recommendation visually ambiguous.
- Ask more than two refinement questions.
- Replace initial rankings without showing history.
- Use decorative AI effects that reduce readability.

---

# 38. Final UI Acceptance Checklist

## Foundation

- [ ] Dark theme is implemented.
- [ ] Blue, orange, purple, and red have consistent semantic roles.
- [ ] Typography hierarchy is clear.
- [ ] Layout is responsive.

## Dashboard

- [ ] Dataset summary is visible.
- [ ] System workflow is understandable.
- [ ] Navigation is clear.

## Artists

- [ ] Artists can be explored.
- [ ] Artist details are accessible.
- [ ] Claims are separated from demonstrated capabilities.
- [ ] Evidence is inspectable.
- [ ] Unknowns are visible.

## Hirer Intelligence

- [ ] Known requirements are visible.
- [ ] Assumptions are explicitly labeled.
- [ ] Unknowns are explicitly labeled.
- [ ] Contradictions are visible.

## Recommendations

- [ ] Top 2 is immediately understandable.
- [ ] Rank 1 and Rank 2 are visually distinct.
- [ ] Evidence supports recommendation explanations.
- [ ] Trade-offs are visible.
- [ ] Uncertainty is visible.

## Refinement

- [ ] No more than 2 questions are shown.
- [ ] Why each question matters is visible.
- [ ] Potential ranking impact is visible.

## Re-Ranking

- [ ] Initial ranking is preserved.
- [ ] Follow-up information is visible.
- [ ] Updated ranking is visible.
- [ ] Rank movement is understandable.
- [ ] Changes are explained.

## Reliability

- [ ] Loading states exist.
- [ ] Error states exist.
- [ ] Empty states are meaningful.
- [ ] Backend unavailability is handled gracefully.

## Deployment

- [ ] Vercel frontend uses production API configuration.
- [ ] Render backend integration works.
- [ ] Production CORS is validated.

---

# 39. Final Design Definition

The final interface should feel like a transparent intelligence product rather than a black-box AI tool.

The evaluator should be able to follow the complete chain:

```text
DATA
 ↓
ARTIST INTELLIGENCE
 ↓
HIRER INTELLIGENCE
 ↓
EVIDENCE
 ↓
TOP 2 DECISION
 ↓
TRADE-OFFS
 ↓
REFINEMENT
 ↓
UPDATED RANKING
```

The visual design succeeds when a user can understand both:

```text
What the system recommends
```

and:

```text
Why the system recommends it
```

without needing to inspect the underlying source code.

The final UI principle is:

> Every important decision should be easy to understand, every important conclusion should expose its evidence, and every important uncertainty should remain visible.
