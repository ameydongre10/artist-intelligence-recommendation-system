'use client';

import { Suspense, useEffect, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import { Header } from '@/components/ui/Header';
import { TopTwoComparison } from '@/components/recommendations/TopTwoComparison';
import { TradeOffCard } from '@/components/recommendations/TradeOffCard';
import { RefinementQuestionsCard } from '@/components/recommendations/RefinementQuestionsCard';
import { LoadingState } from '@/components/ui/LoadingState';
import { ErrorState } from '@/components/ui/ErrorState';
import { api, ApiError } from '@/lib/api';
import { RecommendationDetail, RecommendationSummary } from '@/lib/types';
import { Sparkles, RefreshCw, FileText, ChevronRight, ArrowRight } from 'lucide-react';
import Link from 'next/link';
import { cn } from '@/lib/utils';

function RecommendationsContent() {
  const searchParams = useSearchParams();
  const initialBriefParam = searchParams ? searchParams.get('brief') : null;

  const [summaries, setSummaries] = useState<RecommendationSummary[]>([]);
  const [selectedBriefId, setSelectedBriefId] = useState<string>(
    initialBriefParam || '01_cafe_music_whatsapp'
  );
  const [selectedDetail, setSelectedDetail] = useState<RecommendationDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [detailLoading, setDetailLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isColdStart, setIsColdStart] = useState(false);

  // Load summaries once
  const loadSummaries = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.getRecommendations();
      setSummaries(data);
      if (data.length > 0 && !selectedBriefId) {
        setSelectedBriefId(initialBriefParam || data[0].brief_id);
      }
    } catch (err: any) {
      if (err instanceof ApiError) {
        setIsColdStart(err.isColdStart);
        setError(err.message);
      } else {
        setError(err.message || 'Failed to load recommendations');
      }
    } finally {
      setLoading(false);
    }
  };

  // Load selected brief detail
  const loadDetail = async (briefId: string) => {
    if (!briefId) return;
    setDetailLoading(true);
    try {
      const data = await api.getRecommendationDetail(briefId);
      setSelectedDetail(data);
    } catch (err: any) {
      console.error(err);
    } finally {
      setDetailLoading(false);
    }
  };

  useEffect(() => {
    loadSummaries();
  }, []);

  useEffect(() => {
    if (selectedBriefId) {
      loadDetail(selectedBriefId);
    }
  }, [selectedBriefId]);

  return (
    <div className="flex-1 flex flex-col min-h-full">
      <Header
        title="Decision Intelligence & Recommendations"
        subtitle="Transparent Top 2 candidate matches, physical evidence chains, comparative trade-offs, and targeted refinement questions."
        badge="TOP 2 CONSTRAINT ENFORCED"
        phaseTag="PHASE 5 ARTIFACT"
      />

      <div className="p-6 md:p-8 space-y-8 max-w-7xl">
        {loading && <LoadingState message="Fetching recommendation intelligence..." isColdStart={isColdStart} />}

        {error && (
          <ErrorState
            title="Recommendations Unavailable"
            message={error}
            onRetry={loadSummaries}
          />
        )}

        {!loading && !error && (
          <div className="space-y-8 animate-revealUp">
            {/* Brief Selector Tabs */}
            <div className="space-y-2">
              <div className="flex items-center justify-between pb-2">
                <span className="font-mono text-xs font-bold text-text-muted uppercase tracking-wider">
                  Select Hirer Decision Brief (4 Active):
                </span>
                <span className="font-mono text-[11px] text-accent-primary">
                  100% Deterministic Engine
                </span>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
                {summaries.map((s) => {
                  const isSelected = selectedBriefId === s.brief_id;
                  return (
                    <button
                      type="button"
                      key={s.brief_id}
                      onClick={() => setSelectedBriefId(s.brief_id)}
                      className={cn(
                        'p-4 rounded-xl text-left transition-all border flex flex-col justify-between space-y-2',
                        isSelected
                          ? 'bg-surface border-accent-emerald text-text-primary shadow-sm ring-1 ring-accent-emerald/40'
                          : 'bg-surface/60 border-border-subtle hover:border-border-strong hover:bg-surface text-text-secondary'
                      )}
                    >
                      <div className="flex items-center justify-between">
                        <span className="font-mono text-[11px] font-bold text-accent-emerald">
                          {s.brief_id.split('_')[0]} BRIEF
                        </span>
                        <span className="text-[10px] font-mono text-text-muted">
                          {s.top_two[0]?.artist_id} &amp; {s.top_two[1]?.artist_id}
                        </span>
                      </div>

                      <div className="font-bold text-sm text-text-primary">{s.hirer_name}</div>
                      <p className="text-[11px] text-text-muted line-clamp-1">{s.summary_of_need}</p>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Selected Brief Decision Dossier */}
            {detailLoading && <LoadingState message="Loading decision dossier..." />}

            {!detailLoading && selectedDetail && (
              <div className="space-y-8">
                {/* Brief Header Card */}
                <div className="p-6 rounded-xl bg-surface border border-border-subtle flex flex-col md:flex-row md:items-center justify-between gap-4">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className="font-mono text-xs font-bold text-accent-emerald bg-accent-emerald/10 px-2 py-0.5 rounded border border-accent-emerald/25">
                        DECISION BRIEF: {selectedDetail.brief_id}
                      </span>
                      <span className="text-xs text-text-muted font-mono">
                        Hirer: {selectedDetail.hirer_name}
                      </span>
                    </div>
                    <h2 className="text-xl md:text-2xl font-bold text-text-primary tracking-tight mt-1">
                      {selectedDetail.summary_of_need}
                    </h2>
                  </div>

                  <div className="flex items-center gap-3 shrink-0 flex-wrap">
                    <Link
                      href={`/hirers/${selectedDetail.brief_id}`}
                      className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-lg bg-surface-subtle hover:bg-surface-muted text-text-primary text-xs font-semibold border border-border-strong transition"
                    >
                      <FileText className="w-3.5 h-3.5 text-text-muted" />
                      <span>View Source Brief</span>
                    </Link>

                    {selectedDetail.brief_id.includes('cafe') && (
                      <Link
                        href="/reranking"
                        className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-lg bg-accent-indigo text-white text-xs font-semibold hover:bg-accent-indigo/90 transition shadow-sm"
                      >
                        <RefreshCw className="w-3.5 h-3.5" />
                        <span>Inspect Re-Ranking</span>
                      </Link>
                    )}
                  </div>
                </div>

                {/* Top 2 Recommendations Comparison */}
                <TopTwoComparison topTwo={selectedDetail.top_two} />

                {/* Comparative Trade-Offs */}
                <TradeOffCard tradeOffs={selectedDetail.trade_off_analysis} />

                {/* Targeted Refinement Questions (Max 2) */}
                <RefinementQuestionsCard questions={selectedDetail.refinement_questions} />

                {/* Explicit Assumptions & Uncertainties Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="p-6 rounded-xl bg-surface border border-accent-amber/30 space-y-3">
                    <span className="text-xs font-bold text-accent-amber font-mono uppercase tracking-wider block">
                      Operational Assumptions Made:
                    </span>
                    <ul className="list-disc list-inside text-xs text-text-secondary space-y-1.5 leading-relaxed">
                      {selectedDetail.assumptions_made.map((a, idx) => (
                        <li key={idx}>{a}</li>
                      ))}
                    </ul>
                  </div>

                  <div className="p-6 rounded-xl bg-surface border border-border-subtle space-y-3">
                    <span className="text-xs font-bold text-text-muted font-mono uppercase tracking-wider block">
                      Key Epistemic Uncertainties:
                    </span>
                    <ul className="list-disc list-inside text-xs text-text-secondary space-y-1.5 leading-relaxed">
                      {selectedDetail.key_uncertainties.map((u, idx) => (
                        <li key={idx}>{u}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default function RecommendationsPage() {
  return (
    <Suspense fallback={<LoadingState message="Loading decision recommendations..." />}>
      <RecommendationsContent />
    </Suspense>
  );
}
