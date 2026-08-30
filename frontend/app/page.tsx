'use client';

import { useEffect, useState } from 'react';
import { Header } from '@/components/ui/Header';
import { DatasetSummaryCard } from '@/components/dashboard/DatasetSummaryCard';
import { AnomalyList } from '@/components/dashboard/AnomalyList';
import { LoadingState } from '@/components/ui/LoadingState';
import { ErrorState } from '@/components/ui/ErrorState';
import { api, ApiError } from '@/lib/api';
import { DatasetSummary, SystemStatus } from '@/lib/types';
import { ArrowRight, Sparkles, Users, FileText, RefreshCw, Terminal, CheckCircle2, ShieldCheck } from 'lucide-react';
import Link from 'next/link';

export default function DashboardPage() {
  const [summary, setSummary] = useState<DatasetSummary | null>(null);
  const [systemStatus, setSystemStatus] = useState<SystemStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isColdStart, setIsColdStart] = useState(false);

  const loadData = async () => {
    setLoading(true);
    setError(null);
    setIsColdStart(false);

    try {
      const [sumData, statusData] = await Promise.all([
        api.getDatasetSummary(),
        api.getSystemStatus(),
      ]);
      setSummary(sumData);
      setSystemStatus(statusData);
    } catch (err: any) {
      if (err instanceof ApiError) {
        setIsColdStart(err.isColdStart);
        setError(err.message);
      } else {
        setError(err.message || 'Failed to load dataset summary');
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  return (
    <div className="flex-1 flex flex-col min-h-full">
      <Header
        title="Intelligence Console Overview"
        subtitle="Executive dashboard tracking foundational dataset metrics, multi-category artist portfolios, and verified recommendation pipelines."
        phaseTag="PHASE 1–8 VERIFIED"
      />

      <div className="p-6 md:p-8 space-y-8 max-w-7xl">
        {/* Strategic Gateway Banner */}
        <div className="p-6 rounded-xl bg-surface border border-border-subtle flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div className="space-y-2 max-w-2xl">
            <div className="flex items-center gap-2">
              <span className="font-mono text-xs font-bold text-accent-primary bg-accent-primary/10 px-2 py-0.5 rounded border border-accent-primary/20">
                SYSTEM CORE
              </span>
              <span className="text-xs text-text-muted font-mono">Epistemic Isolation Architecture</span>
            </div>
            <h2 className="text-xl md:text-2xl font-bold text-text-primary tracking-tight">
              Evidence-Backed Creative Artist Matching & Decision Intelligence
            </h2>
            <p className="text-xs md:text-sm text-text-secondary leading-relaxed">
              AIRS evaluates 15 creative artists against 4 real-world hirer conversations by enforcing a strict mathematical separation between self-reported profile claims and verified physical media evidence.
            </p>
          </div>

          {/* Quick Route Shortcuts */}
          <div className="flex flex-col sm:flex-row md:flex-col gap-2.5 shrink-0">
            <Link
              href="/recommendations"
              className="inline-flex items-center justify-between gap-3 px-4 py-2.5 rounded-lg bg-accent-primary text-white text-xs font-semibold hover:bg-accent-primary/90 transition shadow-sm"
            >
              <div className="flex items-center gap-2">
                <Sparkles className="w-4 h-4" />
                <span>Decision Recommendations</span>
              </div>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>

            <Link
              href="/reranking"
              className="inline-flex items-center justify-between gap-3 px-4 py-2.5 rounded-lg bg-surface-subtle hover:bg-surface-muted text-text-primary text-xs font-semibold border border-border-strong transition"
            >
              <div className="flex items-center gap-2">
                <RefreshCw className="w-4 h-4 text-accent-indigo" />
                <span>Follow-Up Re-Ranking</span>
              </div>
              <ArrowRight className="w-3.5 h-3.5 text-text-muted" />
            </Link>
          </div>
        </div>

        {loading && <LoadingState message="Connecting to Artist Intelligence API..." isColdStart={isColdStart} />}

        {error && (
          <ErrorState
            title="Backend Service Connection"
            message={error}
            onRetry={loadData}
          />
        )}

        {!loading && !error && summary && (
          <>
            {/* Quick Action Navigation Strip */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <Link
                href="/artists"
                className="group p-5 rounded-xl bg-surface border border-border-subtle hover:border-accent-primary/40 hover:bg-surface-subtle/50 transition-all flex items-center justify-between"
              >
                <div className="flex items-center gap-3.5">
                  <div className="p-2.5 rounded-lg bg-accent-primary/10 text-accent-primary border border-accent-primary/20">
                    <Users className="w-5 h-5" />
                  </div>
                  <div>
                    <h3 className="text-sm font-semibold text-text-primary group-hover:text-accent-primary transition-colors">
                      Artist Intelligence
                    </h3>
                    <p className="text-xs text-text-muted">15 artist dossiers &amp; media citations</p>
                  </div>
                </div>
                <ArrowRight className="w-4 h-4 text-text-muted group-hover:text-text-primary group-hover:translate-x-0.5 transition-all" />
              </Link>

              <Link
                href="/hirers"
                className="group p-5 rounded-xl bg-surface border border-border-subtle hover:border-accent-indigo/40 hover:bg-surface-subtle/50 transition-all flex items-center justify-between"
              >
                <div className="flex items-center gap-3.5">
                  <div className="p-2.5 rounded-lg bg-accent-indigo/10 text-accent-indigo border border-accent-indigo/20">
                    <FileText className="w-5 h-5" />
                  </div>
                  <div>
                    <h3 className="text-sm font-semibold text-text-primary group-hover:text-accent-indigo transition-colors">
                      Hirer Briefs
                    </h3>
                    <p className="text-xs text-text-muted">4 conversation briefs + 1 update</p>
                  </div>
                </div>
                <ArrowRight className="w-4 h-4 text-text-muted group-hover:text-text-primary group-hover:translate-x-0.5 transition-all" />
              </Link>

              <Link
                href="/recommendations"
                className="group p-5 rounded-xl bg-surface border border-border-subtle hover:border-accent-emerald/40 hover:bg-surface-subtle/50 transition-all flex items-center justify-between"
              >
                <div className="flex items-center gap-3.5">
                  <div className="p-2.5 rounded-lg bg-accent-emerald/10 text-accent-emerald border border-accent-emerald/20">
                    <Sparkles className="w-5 h-5" />
                  </div>
                  <div>
                    <h3 className="text-sm font-semibold text-text-primary group-hover:text-accent-emerald transition-colors">
                      Decision Matches
                    </h3>
                    <p className="text-xs text-text-muted">Top 2 candidates &amp; trade-offs</p>
                  </div>
                </div>
                <ArrowRight className="w-4 h-4 text-text-muted group-hover:text-text-primary group-hover:translate-x-0.5 transition-all" />
              </Link>
            </div>

            {/* Asymmetric Dataset Statistics & Pipeline */}
            <DatasetSummaryCard summary={summary} />

            {/* Documented Anomalies */}
            <AnomalyList anomalies={summary.detected_anomalies} />
          </>
        )}
      </div>
    </div>
  );
}
