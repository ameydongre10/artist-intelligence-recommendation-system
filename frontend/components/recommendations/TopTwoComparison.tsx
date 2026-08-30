'use client';

import { Trophy, Medal, ArrowRight } from 'lucide-react';
import Link from 'next/link';
import { CandidateRecommendation } from '@/lib/types';
import { formatCategoryName, getConfidenceBadgeClass } from '@/lib/utils';
import { Badge } from '@/components/ui/Badge';
import { MediaEvidenceCard } from '@/components/media/MediaEvidenceCard';

interface TopTwoComparisonProps {
  topTwo: [CandidateRecommendation, CandidateRecommendation];
}

export function TopTwoComparison({ topTwo }: TopTwoComparisonProps) {
  const [rank1, rank2] = topTwo;

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 animate-revealUp">
      {/* Rank 1 Card: Highlighted Primary Candidate */}
      <div className="p-6 md:p-7 rounded-xl bg-surface border-2 border-accent-emerald/40 relative flex flex-col justify-between shadow-sm">
        <div className="space-y-5">
          <div className="flex items-center justify-between pb-4 border-b border-border-subtle">
            <div className="flex items-center gap-2 flex-wrap">
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-md text-xs font-mono font-bold bg-accent-emerald text-white tracking-wider shadow-sm">
                <Trophy className="w-3.5 h-3.5" /> RANK #1 PRIMARY
              </span>
              <span className="text-xs font-mono text-text-muted">ID: {rank1.artist_id}</span>
            </div>
            <span className={`text-[10px] font-mono font-semibold px-2.5 py-0.5 rounded-full border ${getConfidenceBadgeClass(rank1.confidence)}`}>
              {rank1.confidence} CONFIDENCE
            </span>
          </div>

          <div>
            <h3 className="text-xl md:text-2xl font-bold text-text-primary tracking-tight">{rank1.artist_name}</h3>
            <p className="text-xs font-mono text-text-muted mt-0.5">{formatCategoryName(rank1.category)}</p>
          </div>

          {/* Fit Reason Narrative */}
          <div className="p-4 rounded-lg bg-surface-subtle border border-border-subtle text-xs text-text-secondary leading-relaxed">
            <span className="text-accent-emerald font-bold uppercase text-[11px] block mb-1 font-mono">
              Primary Fit Rationale:
            </span>
            {rank1.fit_reason}
          </div>

          {/* Matched Requirements Chain */}
          <div className="space-y-2.5">
            <span className="text-[11px] font-mono font-bold text-text-muted uppercase tracking-wider block">
              Requirement-by-Requirement Evidence Chain:
            </span>
            <div className="space-y-2">
              {rank1.matched_requirements.map((m, idx) => (
                <div
                  key={idx}
                  className="p-3 rounded-lg bg-surface-subtle/70 border border-border-subtle text-xs space-y-1"
                >
                  <div className="flex items-center justify-between gap-2">
                    <span className="font-mono text-accent-indigo font-semibold text-xs">
                      {m.dimension.replace(/_/g, ' ').toUpperCase()}
                    </span>
                    <Badge variant={m.match_status.includes('STRONG') ? 'emerald' : 'blue'} size="sm">
                      {m.match_status.replace(/_/g, ' ')}
                    </Badge>
                  </div>
                  <p className="text-text-secondary text-[11px] leading-relaxed">{m.fit_explanation}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Supporting Technical Media Citations */}
          {rank1.supporting_evidence && rank1.supporting_evidence.length > 0 && (
            <div className="space-y-2.5">
              <span className="text-[11px] font-mono font-bold text-text-muted uppercase tracking-wider block">
                Direct Portfolio Citations ({rank1.supporting_evidence.length}):
              </span>
              <div className="space-y-2.5">
                {rank1.supporting_evidence.map((cit) => (
                  <MediaEvidenceCard key={cit.evidence_id} citation={cit} />
                ))}
              </div>
            </div>
          )}

          {/* Trade-offs & Limitations */}
          {rank1.trade_offs && rank1.trade_offs.length > 0 && (
            <div className="p-3.5 rounded-lg bg-accent-amber/10 border border-accent-amber/25 text-xs space-y-1">
              <span className="text-accent-amber font-bold text-[11px] font-mono block">Operational Considerations:</span>
              <ul className="list-disc list-inside text-text-secondary space-y-0.5 text-[11px]">
                {rank1.trade_offs.map((to, idx) => (
                  <li key={idx} className="leading-relaxed">{to}</li>
                ))}
              </ul>
            </div>
          )}
        </div>

        <div className="mt-6 pt-4 border-t border-border-subtle">
          <Link
            href={`/artists/${rank1.artist_id}`}
            className="flex items-center justify-center gap-2 w-full py-2.5 rounded-lg bg-surface-subtle hover:bg-surface-muted text-text-primary text-xs font-semibold border border-border-strong transition-all focus:outline-none focus:ring-2 focus:ring-accent-primary/40 shadow-sm"
          >
            <span>Inspect Full Artist Dossier</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>
      </div>

      {/* Rank 2 Card: Comparative Runner-Up Candidate */}
      <div className="p-6 md:p-7 rounded-xl bg-surface border border-border-subtle flex flex-col justify-between shadow-sm">
        <div className="space-y-5">
          <div className="flex items-center justify-between pb-4 border-b border-border-subtle">
            <div className="flex items-center gap-2 flex-wrap">
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-md text-xs font-mono font-bold bg-surface-muted text-text-primary border border-border-strong tracking-wider">
                <Medal className="w-3.5 h-3.5 text-text-muted" /> RANK #2 RUNNER-UP
              </span>
              <span className="text-xs font-mono text-text-muted">ID: {rank2.artist_id}</span>
            </div>
            <span className={`text-[10px] font-mono font-semibold px-2.5 py-0.5 rounded-full border ${getConfidenceBadgeClass(rank2.confidence)}`}>
              {rank2.confidence} CONFIDENCE
            </span>
          </div>

          <div>
            <h3 className="text-xl md:text-2xl font-bold text-text-primary tracking-tight">{rank2.artist_name}</h3>
            <p className="text-xs font-mono text-text-muted mt-0.5">{formatCategoryName(rank2.category)}</p>
          </div>

          {/* Fit Reason Narrative */}
          <div className="p-4 rounded-lg bg-surface-subtle border border-border-subtle text-xs text-text-secondary leading-relaxed">
            <span className="text-text-muted font-bold uppercase text-[11px] block mb-1 font-mono">
              Comparative Fit Rationale:
            </span>
            {rank2.fit_reason}
          </div>

          {/* Matched Requirements Chain */}
          <div className="space-y-2.5">
            <span className="text-[11px] font-mono font-bold text-text-muted uppercase tracking-wider block">
              Requirement-by-Requirement Evidence Chain:
            </span>
            <div className="space-y-2">
              {rank2.matched_requirements.map((m, idx) => (
                <div
                  key={idx}
                  className="p-3 rounded-lg bg-surface-subtle/70 border border-border-subtle text-xs space-y-1"
                >
                  <div className="flex items-center justify-between gap-2">
                    <span className="font-mono text-accent-indigo font-semibold text-xs">
                      {m.dimension.replace(/_/g, ' ').toUpperCase()}
                    </span>
                    <Badge
                      variant={
                        m.match_status.includes('STRONG')
                          ? 'emerald'
                          : m.match_status.includes('UNKNOWN')
                          ? 'slate'
                          : 'blue'
                      }
                      size="sm"
                    >
                      {m.match_status.replace(/_/g, ' ')}
                    </Badge>
                  </div>
                  <p className="text-text-secondary text-[11px] leading-relaxed">{m.fit_explanation}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Supporting Technical Media Citations */}
          {rank2.supporting_evidence && rank2.supporting_evidence.length > 0 && (
            <div className="space-y-2.5">
              <span className="text-[11px] font-mono font-bold text-text-muted uppercase tracking-wider block">
                Direct Portfolio Citations ({rank2.supporting_evidence.length}):
              </span>
              <div className="space-y-2.5">
                {rank2.supporting_evidence.map((cit) => (
                  <MediaEvidenceCard key={cit.evidence_id} citation={cit} />
                ))}
              </div>
            </div>
          )}

          {/* Trade-offs & Limitations */}
          {rank2.trade_offs && rank2.trade_offs.length > 0 && (
            <div className="p-3.5 rounded-lg bg-accent-amber/10 border border-accent-amber/25 text-xs space-y-1">
              <span className="text-accent-amber font-bold text-[11px] font-mono block">Operational Considerations:</span>
              <ul className="list-disc list-inside text-text-secondary space-y-0.5 text-[11px]">
                {rank2.trade_offs.map((to, idx) => (
                  <li key={idx} className="leading-relaxed">{to}</li>
                ))}
              </ul>
            </div>
          )}
        </div>

        <div className="mt-6 pt-4 border-t border-border-subtle">
          <Link
            href={`/artists/${rank2.artist_id}`}
            className="flex items-center justify-center gap-2 w-full py-2.5 rounded-lg bg-surface-subtle hover:bg-surface-muted text-text-primary text-xs font-semibold border border-border-strong transition-all focus:outline-none focus:ring-2 focus:ring-accent-primary/40 shadow-sm"
          >
            <span>Inspect Full Artist Dossier</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>
      </div>
    </div>
  );
}
