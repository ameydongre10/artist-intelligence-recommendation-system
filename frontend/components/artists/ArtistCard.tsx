'use client';

import Link from 'next/link';
import { Camera, Music, Video, ArrowRight, ShieldAlert } from 'lucide-react';
import { ArtistSummary } from '@/lib/types';
import { formatCategoryName, getConfidenceBadgeClass } from '@/lib/utils';

interface ArtistCardProps {
  artist: ArtistSummary;
}

export function ArtistCard({ artist }: ArtistCardProps) {
  const getCategoryIcon = () => {
    switch (artist.category) {
      case 'photographer':
        return <Camera className="w-4 h-4 text-accent-primary" />;
      case 'musician':
        return <Music className="w-4 h-4 text-accent-indigo" />;
      case 'video_editor':
        return <Video className="w-4 h-4 text-accent-cyan" />;
      default:
        return null;
    }
  };

  const hasAnomaly = artist.discrepancies_and_anomalies && artist.discrepancies_and_anomalies.length > 0;

  return (
    <Link
      href={`/artists/${artist.artist_id}`}
      className="group block p-5 rounded-xl bg-surface border border-border-subtle hover:border-accent-primary/40 transition-all hover:bg-surface-subtle/40 flex flex-col justify-between overflow-hidden shadow-sm"
    >
      <div className="space-y-4">
        {/* Header Row: Identity & Confidence Pill */}
        <div className="flex items-start justify-between gap-2.5">
          <div className="flex items-start gap-2.5 min-w-0 flex-1">
            <div className="p-2 rounded-lg bg-surface-subtle border border-border-subtle group-hover:border-border-strong transition-colors shrink-0 mt-0.5">
              {getCategoryIcon()}
            </div>
            <div className="min-w-0 flex-1">
              <div className="flex items-center gap-1.5 flex-wrap">
                <span className="font-mono text-xs font-bold text-accent-primary shrink-0">
                  {artist.artist_id}
                </span>
                <span className="text-[11px] text-text-muted font-mono truncate">
                  {formatCategoryName(artist.category)}
                </span>
              </div>
              <h3 className="font-bold text-sm md:text-base text-text-primary group-hover:text-accent-primary transition-colors mt-0.5 line-clamp-1 leading-snug break-words">
                {artist.declared_name || artist.source_folder_name}
              </h3>
            </div>
          </div>

          <span
            className={`text-[9px] font-mono font-bold px-2 py-0.5 rounded-full border whitespace-nowrap shrink-0 ${getConfidenceBadgeClass(
              artist.confidence
            )}`}
          >
            {artist.confidence} CONF
          </span>
        </div>

        {/* Epistemic Counts Grid */}
        <div className="grid grid-cols-3 gap-2 pt-3 border-t border-border-subtle/80 text-center">
          <div className="p-2 rounded-lg bg-surface-subtle border border-border-subtle/60 min-w-0">
            <div className="text-xs font-bold text-accent-indigo font-mono">
              {artist.demonstrated_capabilities_count}
            </div>
            <div className="text-[10px] text-text-muted mt-0.5 truncate" title="Verified Evidence">
              Evidence
            </div>
          </div>
          <div className="p-2 rounded-lg bg-surface-subtle border border-border-subtle/60 min-w-0">
            <div className="text-xs font-bold text-accent-primary font-mono">
              {artist.profile_claims_count}
            </div>
            <div className="text-[10px] text-text-muted mt-0.5 truncate" title="Profile Claims">
              Claims
            </div>
          </div>
          <div className="p-2 rounded-lg bg-surface-subtle border border-border-subtle/60 min-w-0">
            <div className="text-xs font-bold text-text-muted font-mono">
              {artist.unknowns_count}
            </div>
            <div className="text-[10px] text-text-muted mt-0.5 truncate" title="Unknown Dimensions">
              Unknowns
            </div>
          </div>
        </div>

        {/* Anomaly notice if present */}
        {hasAnomaly && (
          <div className="flex items-center gap-1.5 text-[10px] text-accent-amber font-mono bg-accent-amber/10 px-2.5 py-1 rounded-md border border-accent-amber/20 min-w-0">
            <ShieldAlert className="w-3.5 h-3.5 shrink-0" />
            <span className="truncate">Preserved Dataset Anomaly</span>
          </div>
        )}
      </div>

      <div className="mt-4 pt-3 border-t border-border-subtle/60 flex items-center justify-between text-xs text-text-muted group-hover:text-text-primary transition-colors font-medium">
        <span>Inspect Dossier</span>
        <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-0.5 transition-transform" />
      </div>
    </Link>
  );
}
