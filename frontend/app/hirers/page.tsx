'use client';

import { useEffect, useState } from 'react';
import { Header } from '@/components/ui/Header';
import { BriefCard } from '@/components/hirers/BriefCard';
import { LoadingState } from '@/components/ui/LoadingState';
import { ErrorState } from '@/components/ui/ErrorState';
import { api, ApiError } from '@/lib/api';
import { HirerBriefSummary } from '@/lib/types';
import { FileText, Sparkles, ArrowRight, RefreshCw } from 'lucide-react';
import Link from 'next/link';

export default function HirersPage() {
  const [briefs, setBriefs] = useState<HirerBriefSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isColdStart, setIsColdStart] = useState(false);

  const loadBriefs = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.getHirerBriefs();
      setBriefs(data);
    } catch (err: any) {
      if (err instanceof ApiError) {
        setIsColdStart(err.isColdStart);
        setError(err.message);
      } else {
        setError(err.message || 'Failed to load hirer briefs');
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadBriefs();
  }, []);

  return (
    <div className="flex-1 flex flex-col min-h-full">
      <Header
        title="Hirer Intent & Briefs Explorer"
        subtitle="Operational requirements, hard limits, and verbatim quotes extracted from real hirer conversations across WhatsApp, Email, and Phone notes."
        phaseTag="PHASE 4 ARTIFACT"
      />

      <div className="p-6 md:p-8 space-y-6 max-w-7xl">
        {/* Dynamic Follow-Up Update Spotlight */}
        <div className="p-5 rounded-xl bg-surface border border-accent-indigo/30 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-lg bg-accent-indigo/10 text-accent-indigo border border-accent-indigo/20 shrink-0">
              <RefreshCw className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-text-primary">
                Follow-Up Requirement Update Tracked
              </h3>
              <p className="text-xs text-text-secondary mt-0.5">
                Brief 01 (Cafe Music WhatsApp) contains a downstream requirement change from ambient cafe background to an upbeat launch night set.
              </p>
            </div>
          </div>
          <Link
            href="/reranking"
            className="inline-flex items-center gap-2 px-3.5 py-2 rounded-lg bg-accent-indigo text-white text-xs font-semibold hover:bg-accent-indigo/90 transition shadow-sm shrink-0 self-start sm:self-auto"
          >
            <span>View Re-Ranking Analysis</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        {loading && <LoadingState message="Fetching structured hirer briefs..." isColdStart={isColdStart} />}

        {error && (
          <ErrorState
            title="Hirer Briefs Unavailable"
            message={error}
            onRetry={loadBriefs}
          />
        )}

        {!loading && !error && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-5 animate-revealUp">
            {briefs.map((brief) => (
              <BriefCard key={brief.brief_id} brief={brief} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
