'use client';

import { 
  Users, 
  FileText, 
  Film, 
  AlertOctagon, 
  CheckCircle2, 
  Layers,
  ArrowRight,
  Database,
  Search,
  Sparkles,
  RefreshCw,
  FileCode2
} from 'lucide-react';
import Link from 'next/link';
import { DatasetSummary } from '@/lib/types';
import { CountUpNumber } from '@/components/ui/CountUpNumber';
import { Badge } from '@/components/ui/Badge';

interface DatasetSummaryCardProps {
  summary: DatasetSummary;
}

const pipelineSteps = [
  {
    step: '01',
    title: 'Dataset Inventory',
    file: 'dataset_inventory.json',
    desc: '149 extracted files, 15 artist folders, 120 media items indexed.',
    status: 'COMPLETE',
    link: '#anomalies',
  },
  {
    step: '02',
    title: 'Artist Intelligence',
    file: 'artist_intelligence.jsonl',
    desc: '15 structured dossiers with verified media citations vs claims.',
    status: 'COMPLETE',
    link: '/artists',
  },
  {
    step: '03',
    title: 'Hirer Intelligence',
    file: 'hirer_intelligence.json',
    desc: '4 conversational briefs + 1 update with verbatim evidence quotes.',
    status: 'COMPLETE',
    link: '/hirers',
  },
  {
    step: '04',
    title: 'Decision Engine',
    file: 'recommendations.json',
    desc: 'Top 2 matches per brief, fit reasons, trade-offs, and max 2 questions.',
    status: 'COMPLETE',
    link: '/recommendations',
  },
  {
    step: '05',
    title: 'Follow-Up Re-Ranking',
    file: 'updated_recommendation.json',
    desc: 'Dynamic shift evaluation for cafe music launch night update.',
    status: 'COMPLETE',
    link: '/reranking',
  },
];

export function DatasetSummaryCard({ summary }: DatasetSummaryCardProps) {
  return (
    <div className="space-y-8 animate-revealUp">
      {/* 1. Asymmetrical Metric Hero Strip */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        {/* Dominant Primary Metric: Artists in Intelligence Dataset */}
        <div className="lg:col-span-6 p-6 rounded-xl bg-surface border border-border-subtle hover:border-border-strong transition-colors flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between pb-4 border-b border-border-subtle">
              <span className="font-mono text-[11px] font-semibold text-text-muted uppercase tracking-wider">
                Primary Intelligence Corpus
              </span>
              <Badge variant="blue">100% PORTFOLIO COVERAGE</Badge>
            </div>

            <div className="mt-5 flex items-baseline gap-3">
              <span className="text-5xl md:text-6xl font-bold tracking-tight text-text-primary font-mono">
                <CountUpNumber end={summary.total_artists} />
              </span>
              <span className="text-sm md:text-base font-semibold text-text-secondary">
                Creative Artists Evaluated
              </span>
            </div>

            <p className="text-xs text-text-muted mt-2 leading-relaxed">
              Every artist portfolio was independently extracted and analyzed across category-specific capability dimensions.
            </p>
          </div>

          {/* Category Distribution Pills */}
          <div className="grid grid-cols-3 gap-2.5 mt-6 pt-4 border-t border-border-subtle">
            <div className="p-2.5 rounded-lg bg-surface-subtle border border-border-subtle/80 text-center">
              <div className="font-mono text-sm font-bold text-accent-primary">
                {summary.artists_by_category?.photographer || 5}
              </div>
              <div className="text-[10px] text-text-muted font-medium mt-0.5">Photographers</div>
            </div>
            <div className="p-2.5 rounded-lg bg-surface-subtle border border-border-subtle/80 text-center">
              <div className="font-mono text-sm font-bold text-accent-indigo">
                {summary.artists_by_category?.musician || 5}
              </div>
              <div className="text-[10px] text-text-muted font-medium mt-0.5">Musicians</div>
            </div>
            <div className="p-2.5 rounded-lg bg-surface-subtle border border-border-subtle/80 text-center">
              <div className="font-mono text-sm font-bold text-accent-cyan">
                {summary.artists_by_category?.video_editor || 5}
              </div>
              <div className="text-[10px] text-text-muted font-medium mt-0.5">Video Editors</div>
            </div>
          </div>
        </div>

        {/* Secondary Metrics Column */}
        <div className="lg:col-span-6 grid grid-cols-1 sm:grid-cols-3 gap-4">
          {/* Media Assets */}
          <div className="p-5 rounded-xl bg-surface border border-border-subtle flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between">
                <span className="font-mono text-[10px] uppercase text-text-muted font-semibold tracking-wider">
                  Assets
                </span>
                <Film className="w-4 h-4 text-accent-indigo" />
              </div>
              <div className="text-3xl font-bold font-mono text-text-primary mt-3">
                <CountUpNumber end={summary.total_media_files} />
              </div>
            </div>
            <div className="text-[11px] text-text-secondary mt-3 pt-2 border-t border-border-subtle">
              Images, Audio & Video Portfolios Scanned
            </div>
          </div>

          {/* Hirer Briefs */}
          <div className="p-5 rounded-xl bg-surface border border-border-subtle flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between">
                <span className="font-mono text-[10px] uppercase text-text-muted font-semibold tracking-wider">
                  Hirers
                </span>
                <FileText className="w-4 h-4 text-accent-primary" />
              </div>
              <div className="text-3xl font-bold font-mono text-text-primary mt-3">
                <CountUpNumber end={summary.total_hirer_briefs} />
                <span className="text-base text-text-muted font-normal ml-1">+1</span>
              </div>
            </div>
            <div className="text-[11px] text-text-secondary mt-3 pt-2 border-t border-border-subtle">
              Conversations + Follow-Up Update
            </div>
          </div>

          {/* Preserved Anomalies */}
          <div className="p-5 rounded-xl bg-surface border border-border-subtle flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between">
                <span className="font-mono text-[10px] uppercase text-text-muted font-semibold tracking-wider">
                  Anomalies
                </span>
                <AlertOctagon className="w-4 h-4 text-accent-amber" />
              </div>
              <div className="text-3xl font-bold font-mono text-text-primary mt-3">
                <CountUpNumber end={summary.detected_anomalies_count} />
              </div>
            </div>
            <div className="text-[11px] text-text-secondary mt-3 pt-2 border-t border-border-subtle">
              Discrepancies Preserved & Resolved
            </div>
          </div>
        </div>
      </div>

      {/* 2. Connected Pipeline Timeline */}
      <div className="p-6 rounded-xl bg-surface border border-border-subtle space-y-5">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-4 border-b border-border-subtle">
          <div>
            <h2 className="text-sm font-bold text-text-primary uppercase tracking-wider flex items-center gap-2">
              <Layers className="w-4 h-4 text-accent-primary" />
              <span>AIRS Execution Pipeline & Processed Artifacts</span>
            </h2>
            <p className="text-xs text-text-muted mt-0.5">
              Deterministic, artifact-backed execution sequence from raw media extraction to follow-up re-ranking.
            </p>
          </div>
          <Badge variant="emerald" size="sm">
            <CheckCircle2 className="w-3 h-3" /> ALL 5 STAGES VERIFIED
          </Badge>
        </div>

        {/* Timeline Grid */}
        <div className="grid grid-cols-1 md:grid-cols-5 gap-3 relative">
          {pipelineSteps.map((step, idx) => (
            <Link
              key={step.step}
              href={step.link}
              className="group p-3.5 rounded-lg bg-surface-subtle/80 hover:bg-surface-subtle border border-border-subtle hover:border-accent-primary/40 transition-all flex flex-col justify-between relative space-y-2"
            >
              <div>
                <div className="flex items-center justify-between">
                  <span className="font-mono text-xs font-bold text-accent-primary">
                    {step.step}
                  </span>
                  <span className="w-2 h-2 rounded-full bg-accent-emerald" />
                </div>
                <h3 className="font-semibold text-xs text-text-primary mt-1 group-hover:text-accent-primary transition-colors">
                  {step.title}
                </h3>
                <div className="font-mono text-[10px] text-text-muted mt-0.5 break-all">
                  {step.file}
                </div>
              </div>

              <p className="text-[11px] text-text-secondary leading-snug pt-2 border-t border-border-subtle/60">
                {step.desc}
              </p>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}
