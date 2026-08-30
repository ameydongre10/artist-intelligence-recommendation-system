# Technical Decision Note: Evidence-Aware Artist Intelligence & Recommendation System

## 1. Problem Framing & Core Objective
Evaluating creative talent (photographers, musicians, video editors) for specific freelance engagements is inherently difficult because hiring signals are unstructured, subjective, and prone to severe mismatch. In the provided dataset:
- Hirer requirements arrive through informal, conversational channels (WhatsApp, live chat, email, phone notes) containing ambiguous constraints and evolving briefs.
- Artist portfolios combine self-reported claims (profile `.docx` files) with uncurated multimodal portfolio assets (images, audio takes, video reels).

The goal of this system is to build a deterministic, explainable, and evidence-grounded decision intelligence pipeline that transforms messy multimodal portfolios and conversational briefs into traceable Top 2 recommendations, comparative trade-offs, and high-impact refinement questions.

---

## 2. Category-Specific Capability Framework
Rather than forcing all artists into generic capability buckets, we defined category-specific capability dimensions grounded directly in real-world creative deliverables:

```text
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│ Category Capability Dimensions                                                              │
├────────────────────────────────┬──────────────────────────────┬─────────────────────────────┤
│ Photographers                  │ Musicians                    │ Video Editors               │
├────────────────────────────────┼──────────────────────────────┼─────────────────────────────┤
│ • Product / Commercial Stills   │ • Live Performance Formats   │ • 9:16 Vertical Video Formats│
│ • Event & Workshop Storytelling│ • Vocal Harmonies & Ranges   │ • Narrative & Reel Pacing   │
│ • Unposed Candid Coverage      │ • Repertoire (Hindi/English) │ • Dialogue Caption Sync     │
│ • Controlled Studio Lighting   │ • Ambient vs Headline Sets   │ • Color Grading & Aesthetics│
│ • Macro Specular Reflection    │ • Acoustic vs Electronic PA  │ • Montage & Beat Matching   │
│ • High-Resolution Detail/DSLR  │ • Compact Stage Footprint    │ • Rapid Turnaround (Reels)  │
└────────────────────────────────┴──────────────────────────────┴─────────────────────────────┘
```

---

## 3. Epistemic State Isolation & Evidence Hierarchy
A foundational requirement of this system is strict epistemic discipline. We separate facts from claims, assumptions, and uncertainties using four mutually exclusive epistemic states:

1. **`DEMONSTRATED_EVIDENCE` (Highest Reliability):**
   - Directly verified against raw multimodal portfolio files.
   - Must include traceable file references, relative paths, media types, and exact timestamp/frame citations (e.g., `MA_cafe_demo_take1.wav` [0:00–1:45], `581888523...jpg` [macro product bottle reflection]).
2. **`CLAIM` (Unverified Self-Report):**
   - Statements from artist profile `.docx` documents or self-reported resumes.
   - Capped at maximum 40% capability weight and never elevated to demonstrated evidence without verifying portfolio media.
3. **`ASSUMPTION` (Operational Interpretation):**
   - Explicit operational working hypotheses (e.g., assuming a 2-person acoustic duo requires $< 4\text{ m}^2$ stage space).
   - Always paired with explicit rationale and risk impact.
4. **`UNKNOWN` (Explicit Neutral Uncertainty):**
   - Unstated or missing information (e.g., venue PA system status, unstated pricing).
   - **Strict Neutrality Rule:** Missing evidence is strictly neutral ($0\text{ pts}$ added, $0\text{ pts}$ deducted). An unknown never constitutes a negative capability penalty. Instead, unknowns reduce confidence levels and trigger targeted refinement questions.

---

## 4. Deterministic Scoring & Matching Methodology
To avoid black-box heuristics or uncalibrated LLM scoring, ranking is computed via a transparent, additive scoring formula (0–100 scale):

$$\text{Total Score} = \text{Requirement Fit } (0\text{--}50) + \text{Evidence Strength } (0\text{--}30) + \text{Constraint Compatibility } (0\text{--}20) - \text{Conflict Penalty } (0\text{--}40)$$

### Score Deconstruction:
- **Requirement Fit (0–50 pts):** Pro-rated requirement coverage ($\frac{50.0}{N_{\text{req}}}$ base per requirement) scaled by importance multipliers ($W_{\text{CRITICAL}} = 1.2$, $W_{\text{STANDARD}} = 1.0$, $W_{\text{LOW}} = 0.8$) and evidence demonstration scaling ($S_{\text{STRONG}} = 1.0$, $S_{\text{MODERATE}} = 0.8$, $S_{\text{LIMITED}} = 0.6$, $S_{\text{CLAIM}} = 0.4$, $S_{\text{UNKNOWN}} = 0.0$).
- **Evidence Strength (0–30 pts):** Additive empirical bonus for verified media evidence per requirement ($+6.0\text{ pts}$ for $\text{STRONG}$, $+4.0\text{ pts}$ for $\text{MODERATE}$, $+2.0\text{ pts}$ for $\text{LIMITED}$, $+1.0\text{ pts}$ for $\text{CLAIM}$, $+0.0\text{ pts}$ for $\text{UNKNOWN}$), capped at $30.0\text{ pts}$ total.
- **Constraint Compatibility (0–20 pts):** Baseline $20.0\text{ pts}$ for category and operational compatibility.
- **Conflict Penalties (0–40 pts):** Applied strictly to direct hard constraint violations (e.g., $+35.0\text{ pts}$ penalty for heavy metal band applied to quiet cafe background).

---

## 5. Top 2 Recommendations & Trade-Off Analysis
Every brief returns exactly Rank 1 (Primary Match) and Rank 2 (Comparable Runner-Up):

### Summary Across Briefs:
1. **Brief 1 (`01_cafe_music_whatsapp` / Rhea — Musician):**
   - **Rank 1:** `M01` (Meera & Arjun, Score: 92.0, HIGH Conf) — Demonstrated acoustic cafe demo take (`MA_cafe_demo_take1.wav`), dual English/Hindi vocal harmonies, talkable volume, compact footprint under ₹9k.
   - **Rank 2:** `M03` (Raghav Sen, Score: 81.0, HIGH Conf) — Intimate solo acoustic fingerpicking (`folk_acoustic-summer-walk.mp3`), ultra-quiet background listening, but slow ballad repertoire only.
   - **Trade-Off:** M01 provides richer vocal harmonies and versatile dynamic range with a 2-person footprint; M03 provides an ultra-compact solo footprint but is limited to slow-tempo folk ballads.
2. **Brief 2 (`02_skincare_photography_chat` / Nidhi — Photographer):**
   - **Rank 1:** `P02` (Kabir Mehta, Score: 94.0, HIGH Conf) — Demonstrated commercial product and cosmetic bottle/jar packaging photography with controlled specular reflections (`581888523...jpg`), 4:5 commercial aspect, based in Gurugram for 2-day turnaround.
   - **Rank 2:** `PO5` (Frames, Score: 84.0, HIGH Conf) — Demonstrated high-resolution DSLR product sharpness (20MP+ sensor detail), but based in Kolkata requiring travel/shipping logistics confirmation.
   - **Trade-Off:** P02 provides local proximity in Gurugram with proven cosmetic bottle packshots; PO5 offers higher raw sensor resolution but introduces travel friction.
3. **Brief 3 (`03_vertical_video_email` / Manu K. — Video Editor):**
   - **Rank 1:** `V01` (Nisha Kapoor, Score: 95.0, HIGH Conf) — Demonstrated 9:16 vertical short-form reels (`Video-11391.mp4`), food prep and customer reaction montage pacing, synchronized on-screen dialogue captions.
   - **Rank 2:** `V03` (Tara D'Souza / Rahul Gupta, Score: 83.0, HIGH Conf) — Demonstrated cinematic travel and lifestyle montages with rich color grading and rhythmic pacing, but speech captioning is unverified.
   - **Trade-Off:** V01 has direct vertical food reel pacing with synchronized dialogue subtitles; V03 has aesthetic color grading but lacks speech subtitle samples.
4. **Brief 4 (`04_leadership_event_photos` / Shalini — Photographer):**
   - **Rank 1:** `P01` (Aanya Rao, Score: 92.0, HIGH Conf) — Demonstrated dynamic, unposed candid event and workshop storytelling in Delhi/NCR (`587772091...jpg`), social-ready digital composition, same-evening delivery.
   - **Rank 2:** `PO5` (Frames, Score: 80.0, MEDIUM Conf) — Demonstrated high-resolution DSLR group framing for edge-to-edge sharpness on 120-person crowd, though based in Kolkata.
   - **Trade-Off:** P01 guarantees local South Delhi availability and unposed workshop storytelling; PO5 provides superior sensor resolution for large group prints but has travel uncertainty.

---

## 6. Targeted Refinement Questions ($\le 2$ Constraint)
To respect the hirer's time and cognitive load, questions are restricted to a strict maximum of 2 per brief. Questions are only included if the answer directly alters candidate suitability or ranking:
- **Brief 1:** (1) Cafe house PA / vocal mic readiness vs self-amplification; (2) Preferred proportion of Hindi contemporary vs English acoustic songs.
- **Brief 2:** (1) Product delivery to studio vs on-site Gurugram setup; (2) Hand model presence vs tabletop product-only framing.
- **Brief 3:** (1) Royalty-free background music vs trending Instagram audio commercial clearance; (2) Audio transcripts/timestamps for Friday delivery.
- **Brief 4:** (1) South Delhi conference on-camera bounce flash rules; (2) Corporate procurement budget ceiling.

---

## 7. Follow-Up Re-Ranking (`01_cafe_music_update`)
When Rhea's cafe brief updated from a 3-hour ambient background set ($\approx ₹7\text{k--}9\text{k}$) to a 45-minute celebratory headline showcase set for 80 launch guests ($₹15,000$ budget, small stage cleared):
- **Stage 1 Snapshot Preserved:** `M01` (92.0) > `M03` (81.0).
- **Stage 2 Recomputation:**
  - `M01` (Meera & Arjun): Score increased to **96.0** (`STABLE, Rank 1`). Rehearsal portfolio demonstrates energetic acoustic medley versatility (`MA_upbeat_medley_rehearsal.wav`) matching the launch night headline moment within ₹15k.
  - `M03` (Raghav Sen): Score decreased to **74.0** (`STABLE, Rank 2`). While still a valid acoustic fallback, his portfolio is exclusively contemplative and slow-tempo folk, introducing an energetic mismatch for a celebratory launch party.
- **Explanation:** Ordinal ranks held stable, but the confidence margin widened from $+11.0$ to $+22.0$ points based directly on demonstrated musical repertoire versatility.

---

## 8. Non-Goals & Architectural Boundaries
- **No Black-Box Scoring:** No uninterpretable neural rankers or hallucinated scores.
- **No Raw Data Mutation:** Original dataset files in `data/raw/Data set/` remain completely immutable.
- **No Premature Graph DB Overhead:** Neo4j was evaluated and deliberately omitted in favor of sub-millisecond, deterministic in-memory access over validated JSON/JSONL artifacts.
- **No Unverifiable Guarantees:** Unknown parameters (such as artist schedule or unstated travel fees) are transparently declared rather than assumed.
