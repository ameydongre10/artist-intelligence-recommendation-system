/**
 * TypeScript domain type definitions matching FastAPI backend models and processed artifacts.
 */

export type EpistemicState = 'CLAIM' | 'DEMONSTRATED_EVIDENCE' | 'ASSUMPTION' | 'UNKNOWN';
export type ArtistCategory = 'photographer' | 'musician' | 'video_editor';
export type ConfidenceLevel = 'HIGH' | 'MEDIUM' | 'LOW';
export type ImportanceLevel = 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';

export interface SystemStatus {
  status: 'healthy' | 'degraded';
  environment: string;
  version: string;
  artifacts_available: Record<string, boolean>;
  all_artifacts_ready: boolean;
}

export interface DetectedAnomalyGroup {
  artist_folder: string;
  category: string;
  anomalies: string[];
}

export interface DatasetSummary {
  dataset_version: string;
  total_files: number;
  total_artists: number;
  artists_by_category: Record<string, number>;
  total_hirer_briefs: number;
  total_follow_ups: number;
  total_media_files: number;
  detected_anomalies_count: number;
  detected_anomalies: DetectedAnomalyGroup[];
  artifacts_status: Record<string, string>;
}

export interface EvidenceCitation {
  evidence_id: string;
  file_name: string;
  relative_path: string;
  media_type: string;
  timestamp_or_frame: string;
  observed_features: string[];
  citation_text: string;
}

export interface DemonstratedCapability {
  capability_id: string;
  dimension: string;
  description: string;
  evidence_strength: 'STRONG' | 'MODERATE' | 'LIMITED';
  confidence: ConfidenceLevel;
  evidence_citations: EvidenceCitation[];
  epistemic_state: string;
}

export interface ProfileClaim {
  claim_id: string;
  dimension: string;
  statement: string;
  source_context: string;
  is_demonstrated: boolean;
  epistemic_state: string;
}

export interface UnknownCapability {
  unknown_id: string;
  dimension: string;
  description: string;
  reason: string;
  epistemic_state: string;
}

export interface ArtistSummary {
  artist_id: string;
  source_folder_name: string;
  category: ArtistCategory;
  declared_name?: string;
  identifier_status: string;
  confidence: ConfidenceLevel;
  demonstrated_capabilities_count: number;
  profile_claims_count: number;
  unknowns_count: number;
  discrepancies_and_anomalies: string[];
}

export interface ArtistDetail {
  artist_id: string;
  source_folder_name: string;
  category: ArtistCategory;
  declared_name?: string;
  identifier_status: string;
  profile_claims: ProfileClaim[];
  category_dimensions: Record<string, any>;
  demonstrated_capabilities: DemonstratedCapability[];
  unknowns: UnknownCapability[];
  confidence: ConfidenceLevel;
  discrepancies_and_anomalies: string[];
}

export interface RequirementItem {
  requirement_id: string;
  dimension: string;
  description: string;
  importance: ImportanceLevel;
  source_quote?: string;
  epistemic_state: string;
}

export interface ConstraintItem {
  constraint_id: string;
  constraint_type: string;
  value: string;
  is_hard_constraint: boolean;
  source_quote?: string;
}

export interface PreferenceItem {
  preference_id: string;
  description: string;
  is_flexible: boolean;
  source_quote?: string;
}

export interface DeliverableItem {
  deliverable_id: string;
  description: string;
  turnaround_expectation: string;
  is_mandatory: boolean;
  source_quote?: string;
}

export interface AssumptionItem {
  assumption_id: string;
  description: string;
  rationale: string;
  risk_impact: string;
  epistemic_state: string;
}

export interface UnknownItem {
  unknown_id: string;
  description: string;
  why_it_matters: string;
  is_decision_critical: boolean;
  epistemic_state: string;
}

export interface AmbiguityItem {
  ambiguity_id: string;
  statement: string;
  possible_interpretations: string[];
  decision_risk: string;
  source_quote: string;
}

export interface ContradictionItem {
  contradiction_id: string;
  statement_a: string;
  statement_b: string;
  impact_on_decision: string;
}

export interface HirerBriefSummary {
  brief_id: string;
  hirer_name: string;
  channel: string;
  target_category: ArtistCategory;
  situation: string;
  timeline: string;
  location: string;
  known_requirements_count: number;
  hard_constraints_count: number;
  unknowns_count: number;
  contradictions_count: number;
}

export interface HirerBriefDetail {
  brief_id: string;
  hirer_name: string;
  channel: string;
  source_file: string;
  target_category: ArtistCategory;
  raw_text: string;
  context: {
    situation: string;
    target_date_or_timeline: string;
    location_or_venue: string;
    audience_or_scale?: string;
  };
  known_requirements: RequirementItem[];
  preferences: PreferenceItem[];
  hard_constraints: ConstraintItem[];
  deliverables: DeliverableItem[];
  assumptions: AssumptionItem[];
  unknowns: UnknownItem[];
  ambiguities: AmbiguityItem[];
  contradictions: ContradictionItem[];
  decision_critical_factors: Array<{
    factor_id: string;
    dimension: string;
    factor_summary: string;
    importance: ImportanceLevel;
  }>;
}

export interface RequirementMatch {
  requirement_id: string;
  dimension: string;
  artist_capability_id?: string;
  match_status: string;
  fit_explanation: string;
  supporting_evidence: EvidenceCitation[];
}

export interface CandidateRecommendation {
  rank: number;
  artist_id: string;
  artist_name: string;
  category: ArtistCategory;
  fit_reason: string;
  matched_requirements: RequirementMatch[];
  supporting_evidence: EvidenceCitation[];
  confidence: ConfidenceLevel;
  trade_offs: string[];
  uncertainty_and_limitations: string[];
}

export interface TradeOffItem {
  dimension: string;
  rank_1_status: string;
  rank_2_status: string;
  decision_implication: string;
}

export interface RefinementQuestion {
  question_id: string;
  question_text: string;
  why_it_matters: string;
  potential_ranking_impact: string;
}

export interface RecommendationSummary {
  brief_id: string;
  hirer_name: string;
  summary_of_need: string;
  top_two: Array<{
    rank: number;
    artist_id: string;
    artist_name: string;
    category: string;
    confidence: string;
    evidence_citations_count: number;
  }>;
  refinement_questions_count: number;
}

export interface RecommendationDetail {
  brief_id: string;
  hirer_name: string;
  summary_of_need: string;
  top_two: [CandidateRecommendation, CandidateRecommendation];
  trade_off_analysis: TradeOffItem[];
  assumptions_made: string[];
  key_uncertainties: string[];
  refinement_questions: RefinementQuestion[];
}

export interface RankMovement {
  artist_id: string;
  artist_name: string;
  previous_rank: number;
  updated_rank: number;
  movement: 'STABLE' | 'UP' | 'DOWN';
  reason: string;
}

export interface ReRankingResult {
  brief_id: string;
  follow_up_update_id: string;
  follow_up_summary: string;
  initial_top_two: CandidateRecommendation[];
  updated_top_two: CandidateRecommendation[];
  rank_movements: RankMovement[];
  what_changed: string;
  why_ranking_changed: string;
}
