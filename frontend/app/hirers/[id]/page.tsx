'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { Header } from '@/components/ui/Header';
import { EpistemicRequirementView } from '@/components/hirers/EpistemicRequirementView';
import { LoadingState } from '@/components/ui/LoadingState';
import { ErrorState } from '@/components/ui/ErrorState';
import { api, ApiError } from '@/lib/api';
import { HirerBriefDetail } from '@/lib/types';
import { formatCategoryName } from '@/lib/utils';
import { ArrowLeft, Clock, MapPin, DollarSign, Sparkles, RefreshCw, MessageSquare } from 'lucide-react';
import Link from 'next/link';

export default function HirerBriefDetailPage() {
  const params = useParams();
  const briefId = params?.id as string;

  const [brief, setBrief] = useState<HirerBriefDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isColdStart, setIsColdStart] = useState(false);

  const loadBrief = async () => {
    if (!briefId) return;
    setLoading(true);
    setError(null);
    try {
      const data = await api.getHirerBriefDetail(briefId);
      setBrief(data);
    } catch (err: any) {
      if (err instanceof ApiError) {
        setIsColdStart(err.isColdStart);
        setError(err.message);
      } else {
        setError(err.message || 'Failed to load hirer brief');
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadBrief();
  }, [briefId]);

  const hasFollowUp = briefId.includes('01_cafe');

  return (
    <div className="flex-1 flex flex-col min-h-full">
      <Header
        title={`Hirer Brief Dossier: ${briefId}`}
        subtitle="Structured analysis of hirer conversation, operational limits, known requirements, and assumptions."
        badge={brief ? formatCategoryName(brief.target_category) : undefined}
        phaseTag="REQUIREMENTS DOSSIER"
      />

      <div className="p-6 md:p-8 space-y-6 max-w-7xl">
        <Link
          href="/hirers"
          className="inline-flex items-center gap-2 text-xs font-mono text-text-muted hover:text-text-primary transition-colors mb-2"
        >
          <ArrowLeft className="w-3.5 h-3.5" /> Back to Hirer Briefs Directory
        </Link>

        {loading && <LoadingState message={`Fetching structured brief for ${briefId}...`} isColdStart={isColdStart} />}

        {error && (
          <ErrorState
            title="Hirer Brief Not Found"
            message={error}
            onRetry={loadBrief}
          />
        )}

        {!loading && !error && brief && (
          <div className="space-y-8 animate-revealUp">
            {/* Header & Operational Snapshot Card */}
            <div className="p-6 rounded-xl bg-surface border border-border-subtle space-y-5">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div className="space-y-1">
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="font-mono text-xs font-bold text-accent-indigo bg-accent-indigo/10 px-2 py-0.5 rounded border border-accent-indigo/25">
                      {brief.brief_id}
                    </span>
                    <span className="text-xs font-mono text-text-muted capitalize">
                      Channel: {brief.channel.replace(/_/g, ' ')}
                    </span>
                  </div>
                  <h2 className="text-2xl md:text-3xl font-bold text-text-primary tracking-tight mt-1">
                    {brief.hirer_name} &bull; {formatCategoryName(brief.target_category)} Brief
                  </h2>
                </div>

                <div className="flex items-center gap-3 shrink-0 flex-wrap">
                  <Link
                    href={`/recommendations?brief=${encodeURIComponent(brief.brief_id)}`}
                    className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-accent-primary text-white text-xs font-semibold hover:bg-accent-primary/90 transition shadow-sm"
                  >
                    <Sparkles className="w-3.5 h-3.5" />
                    <span>View Recommendations</span>
                  </Link>

                  {hasFollowUp && (
                    <Link
                      href="/reranking"
                      className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-surface-subtle hover:bg-surface-muted text-text-primary text-xs font-semibold border border-border-strong transition"
                    >
                      <RefreshCw className="w-3.5 h-3.5 text-accent-indigo" />
                      <span>Follow-Up Re-Ranking</span>
                    </Link>
                  )}
                </div>
              </div>

              {/* Situation Narrative */}
              <div className="p-4 rounded-lg bg-surface-subtle border border-border-subtle text-xs text-text-secondary leading-relaxed">
                <span className="font-semibold text-text-primary block mb-1">Operational Context:</span>
                {brief.context.situation}
              </div>

              {/* Operational Metadata Grid */}
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs font-mono">
                <div className="p-3 rounded-lg bg-surface-subtle border border-border-subtle flex items-center gap-2.5">
                  <Clock className="w-4 h-4 text-text-muted shrink-0" />
                  <div>
                    <div className="text-[10px] text-text-muted">Target Timeline</div>
                    <div className="text-text-primary font-semibold">
                      {brief.context.target_date_or_timeline}
                    </div>
                  </div>
                </div>
                <div className="p-3 rounded-lg bg-surface-subtle border border-border-subtle flex items-center gap-2.5">
                  <MapPin className="w-4 h-4 text-text-muted shrink-0" />
                  <div>
                    <div className="text-[10px] text-text-muted">Location / Venue</div>
                    <div className="text-text-primary font-semibold">
                      {brief.context.location_or_venue}
                    </div>
                  </div>
                </div>
                <div className="p-3 rounded-lg bg-surface-subtle border border-border-subtle flex items-center gap-2.5">
                  <DollarSign className="w-4 h-4 text-accent-emerald shrink-0" />
                  <div>
                    <div className="text-[10px] text-text-muted">Audience / Scale</div>
                    <div className="text-text-primary font-semibold">
                      {brief.context.audience_or_scale || 'Within Category Parameters'}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Epistemic Breakdown View */}
            <EpistemicRequirementView
              knownRequirements={brief.known_requirements}
              hardConstraints={brief.hard_constraints}
              preferences={brief.preferences}
              deliverables={brief.deliverables}
              assumptions={brief.assumptions}
              unknowns={brief.unknowns}
              ambiguities={brief.ambiguities}
              contradictions={brief.contradictions}
            />
          </div>
        )}
      </div>
    </div>
  );
}
