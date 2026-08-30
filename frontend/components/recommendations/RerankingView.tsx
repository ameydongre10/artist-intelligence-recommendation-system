'use client';

import { RefreshCw, ArrowRight, CheckCircle2, AlertCircle, TrendingUp, TrendingDown, Minus } from 'lucide-react';
import { ReRankingResult } from '@/lib/types';
import { Badge } from '@/components/ui/Badge';
import { getConfidenceBadgeClass } from '@/lib/utils';

interface RerankingViewProps {
  reranking: ReRankingResult;
}

export function RerankingView({ reranking }: RerankingViewProps) {
  return (
    <div className="space-y-10 animate-revealUp">
      {/* 1. Follow-Up Context Banner */}
      <div className="p-6 md:p-7 rounded-xl bg-surface border border-accent-indigo/40 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-border-subtle">
          <div className="flex items-center gap-2.5">
            <RefreshCw className="w-5 h-5 text-accent-indigo shrink-0" />
            <h2 className="text-base font-bold text-text-primary tracking-tight">
              Follow-Up Update Analysis: {reranking.follow_up_update_id}
            </h2>
          </div>
          <Badge variant="indigo">PARENT BRIEF: {reranking.brief_id}</Badge>
        </div>

        <p className="text-xs md:text-sm text-text-secondary leading-relaxed bg-surface-subtle p-4 rounded-lg border border-border-subtle">
          {reranking.follow_up_summary}
        </p>

        {/* Parameter Shifts Detected */}
        <div className="pt-2 space-y-2">
          <span className="font-mono text-[11px] font-bold text-accent-indigo uppercase tracking-wider block">
            Parameter Shifts Detected:
          </span>
          <pre className="font-mono text-xs text-text-primary whitespace-pre-line leading-relaxed bg-surface-subtle p-4 rounded-lg border border-border-subtle overflow-x-auto">
            {reranking.what_changed}
          </pre>
        </div>
      </div>

      {/* 2. Side-by-Side Comparison: Initial vs Updated Ranking */}
      <div className="space-y-4">
        <div className="flex items-center justify-between pb-3 border-b border-border-subtle">
          <h2 className="text-sm font-bold text-text-primary uppercase tracking-wider">
            Before vs After Top 2 Match Snapshots
          </h2>
          <span className="font-mono text-[10px] text-text-muted">STATE DELTA TRANSITION</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* INITIAL AMBIENT RANKING */}
          <div className="p-6 rounded-xl bg-surface border border-border-subtle space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-border-subtle">
              <div>
                <span className="text-[10px] font-mono font-bold text-text-muted uppercase tracking-wider block">
                  Stage 1 Context
                </span>
                <h3 className="text-sm font-bold text-text-primary">Initial Ambient Cafe Brief</h3>
              </div>
              <span className="text-xs font-mono text-text-muted bg-surface-subtle px-2.5 py-1 rounded border border-border-subtle">
                ₹7k–₹9k / 3 hrs
              </span>
            </div>

            <div className="space-y-3">
              {reranking.initial_top_two.map((c) => (
                <div
                  key={c.artist_id}
                  className="p-4 rounded-lg bg-surface-subtle border border-border-subtle space-y-2"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-bold px-2 py-0.5 rounded bg-surface-muted text-text-primary font-mono border border-border-strong">
                        RANK #{c.rank}
                      </span>
                      <span className="font-bold text-sm text-text-primary">{c.artist_name}</span>
                    </div>
                    <span className={`text-[10px] font-mono px-2 py-0.5 rounded-full border ${getConfidenceBadgeClass(c.confidence)}`}>
                      {c.confidence}
                    </span>
                  </div>
                  <p className="text-xs text-text-secondary leading-relaxed">{c.fit_reason}</p>
                </div>
              ))}
            </div>
          </div>

          {/* UPDATED LAUNCH NIGHT RE-RANKING */}
          <div className="p-6 rounded-xl bg-surface border-2 border-accent-emerald/40 space-y-4 shadow-sm">
            <div className="flex items-center justify-between pb-3 border-b border-border-subtle">
              <div>
                <span className="text-[10px] font-mono font-bold text-accent-emerald uppercase tracking-wider block">
                  Stage 2 Context
                </span>
                <h3 className="text-sm font-bold text-text-primary">Updated Launch Night Brief</h3>
              </div>
              <span className="text-xs font-mono text-accent-emerald bg-accent-emerald/10 px-2.5 py-1 rounded border border-accent-emerald/30 font-bold">
                ₹15k / 45m Headline
              </span>
            </div>

            <div className="space-y-3">
              {reranking.updated_top_two.map((c) => (
                <div
                  key={c.artist_id}
                  className="p-4 rounded-lg bg-surface-subtle border border-border-subtle space-y-2"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-bold px-2 py-0.5 rounded bg-accent-emerald text-white font-mono shadow-sm">
                        RANK #{c.rank}
                      </span>
                      <span className="font-bold text-sm text-text-primary">{c.artist_name}</span>
                    </div>
                    <span className={`text-[10px] font-mono px-2 py-0.5 rounded-full border ${getConfidenceBadgeClass(c.confidence)}`}>
                      {c.confidence}
                    </span>
                  </div>
                  <p className="text-xs text-text-secondary leading-relaxed">{c.fit_reason}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* 3. Rank Movement Explanations */}
      <div className="p-6 rounded-xl bg-surface border border-border-subtle space-y-5">
        <div className="flex items-center justify-between pb-3 border-b border-border-subtle">
          <h2 className="text-sm font-bold text-text-primary uppercase tracking-wider">
            Rank Movements &amp; Mathematical Scoring Deltas
          </h2>
          <span className="font-mono text-[10px] text-text-muted">TRANSPARENT EXPLANATIONS</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {reranking.rank_movements.map((m) => {
            const isUp = m.movement.toLowerCase().includes('up') || m.updated_rank < m.previous_rank;
            const isDown = m.movement.toLowerCase().includes('down') || m.updated_rank > m.previous_rank;

            return (
              <div
                key={m.artist_id}
                className="p-5 rounded-lg bg-surface-subtle border border-border-subtle space-y-2.5 text-xs flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-center justify-between gap-2">
                    <span className="font-bold text-sm text-text-primary">{m.artist_name}</span>
                    <span
                      className={`font-mono text-xs px-2 py-0.5 rounded border flex items-center gap-1 font-semibold ${
                        isUp
                          ? 'bg-accent-emerald/10 text-accent-emerald border-accent-emerald/30'
                          : isDown
                          ? 'bg-accent-amber/10 text-accent-amber border-accent-amber/30'
                          : 'bg-surface text-text-muted border-border-subtle'
                      }`}
                    >
                      {isUp && <TrendingUp className="w-3 h-3" />}
                      {isDown && <TrendingDown className="w-3 h-3" />}
                      Rank {m.previous_rank} &rarr; Rank {m.updated_rank} ({m.movement})
                    </span>
                  </div>
                  <p className="text-text-secondary leading-relaxed mt-2">{m.reason}</p>
                </div>

                <div className="text-[10px] font-mono text-text-muted pt-2 border-t border-border-subtle/60">
                  Artist ID: {m.artist_id}
                </div>
              </div>
            );
          })}
        </div>

        {/* Delta Explanation Narrative */}
        <div className="p-4 rounded-lg bg-surface-subtle border border-border-subtle text-xs text-text-secondary leading-relaxed space-y-1">
          <span className="font-bold text-accent-primary font-mono text-[11px] block">
            Comprehensive Rationale for Re-Ranking:
          </span>
          <p>{reranking.why_ranking_changed}</p>
        </div>
      </div>
    </div>
  );
}
