"""
Master Recommendation Engine.
Orchestrates the matching, ranking, trade-off generation, question formulation,
and follow-up re-ranking for all hirer briefs and updates.
Produces 'data/processed/recommendations.json' and 'data/processed/updated_recommendation.json'.
"""

import os
from typing import Dict, List, Any, Tuple
from src.models.artifacts import (
    ArtistIntelligenceRecord,
    RecommendationsArtifact,
    UpdatedRecommendationArtifact
)
from src.models.hirer import HirerIntelligenceArtifact
from src.models.recommendation import BriefRecommendation, ReRankingResult
from src.matching.ranking import rank_artists_for_brief
from src.matching.reranking import process_follow_up_reranking
from src.utils.file_utils import read_jsonl_file, read_json_file, write_json_file


class RecommendationEngine:
    """
    Orchestrator for matching, ranking, and follow-up re-ranking.
    """
    def __init__(
        self,
        artist_intelligence_path: str = "data/processed/artist_intelligence.jsonl",
        hirer_intelligence_path: str = "data/processed/hirer_intelligence.json",
        recommendations_output_path: str = "data/processed/recommendations.json",
        updated_recommendations_output_path: str = "data/processed/updated_recommendation.json"
    ):
        self.artist_intelligence_path = artist_intelligence_path
        self.hirer_intelligence_path = hirer_intelligence_path
        self.recommendations_output_path = recommendations_output_path
        self.updated_recommendations_output_path = updated_recommendations_output_path

    def run(self) -> Tuple[RecommendationsArtifact, UpdatedRecommendationArtifact]:
        """
        Executes full matching, initial recommendation generation, and follow-up re-ranking.
        """
        # 1. Ingest processed intelligence artifacts
        raw_artist_records = read_jsonl_file(self.artist_intelligence_path)
        artists = [ArtistIntelligenceRecord.model_validate(r) for r in raw_artist_records]

        raw_hirer_data = read_json_file(self.hirer_intelligence_path)
        hirer_artifact = HirerIntelligenceArtifact.model_validate(raw_hirer_data)

        # 2. Generate Initial Recommendations for all 4 briefs
        brief_recommendations: List[BriefRecommendation] = []
        for brief in hirer_artifact.briefs:
            rec = rank_artists_for_brief(brief, artists)
            brief_recommendations.append(rec)

        recommendations_artifact = RecommendationsArtifact(
            metadata={
                "pipeline_version": "1.0.0",
                "total_briefs_recommended": len(brief_recommendations),
                "scoring_framework": "Transparent additive scoring (Requirement Fit + Evidence Strength + Constraints - Penalties)",
                "evidence_principle": "Strict epistemic isolation (DEMONSTRATED_EVIDENCE > CLAIM > UNKNOWN)"
            },
            recommendations=brief_recommendations
        )

        # 3. Write initial recommendations artifact
        write_json_file(
            recommendations_artifact.model_dump(),
            self.recommendations_output_path,
            indent=2
        )

        # 4. Generate Re-Ranking for Follow-up Update
        cafe_initial_rec = next(
            r for r in brief_recommendations if r.brief_id == "01_cafe_music_whatsapp"
        )
        cafe_follow_up = next(
            fu for fu in hirer_artifact.follow_up_updates if fu.update_id == "01_cafe_music_update"
        )

        cafe_initial_brief = next(
            b for b in hirer_artifact.briefs if b.brief_id == "01_cafe_music_whatsapp"
        )

        reranking_result: ReRankingResult = process_follow_up_reranking(
            initial_recommendation=cafe_initial_rec,
            follow_up_record=cafe_follow_up,
            all_artists=artists,
            initial_brief=cafe_initial_brief
        )


        updated_artifact = UpdatedRecommendationArtifact(
            metadata={
                "pipeline_version": "1.0.0",
                "original_brief_id": cafe_initial_rec.brief_id,
                "follow_up_update_id": cafe_follow_up.update_id,
                "re_ranking_framework": "Comparative before-and-after requirement analysis"
            },
            reranking=reranking_result
        )

        # 5. Write updated recommendation artifact
        write_json_file(
            updated_artifact.model_dump(),
            self.updated_recommendations_output_path,
            indent=2
        )

        return recommendations_artifact, updated_artifact
