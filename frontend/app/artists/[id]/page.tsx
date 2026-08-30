'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { Header } from '@/components/ui/Header';
import { DemonstratedEvidenceView } from '@/components/artists/DemonstratedEvidenceView';
import { LoadingState } from '@/components/ui/LoadingState';
import { ErrorState } from '@/components/ui/ErrorState';
import { api, ApiError } from '@/lib/api';
import { ArtistDetail } from '@/lib/types';
import { formatCategoryName, getConfidenceBadgeClass } from '@/lib/utils';
import { ArrowLeft, Camera, Music, Video, ShieldAlert, Folder, CheckCircle } from 'lucide-react';
import Link from 'next/link';

export default function ArtistDetailPage() {
  const params = useParams();
  const router = useRouter();
  const artistId = params?.id as string;

  const [artist, setArtist] = useState<ArtistDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isColdStart, setIsColdStart] = useState(false);

  const loadArtist = async () => {
    if (!artistId) return;
    setLoading(true);
    setError(null);
    try {
      const data = await api.getArtistDetail(artistId);
      setArtist(data);
    } catch (err: any) {
      if (err instanceof ApiError) {
        setIsColdStart(err.isColdStart);
        setError(err.message);
      } else {
        setError(err.message || 'Failed to load artist details');
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadArtist();
  }, [artistId]);

  return (
    <div className="flex-1 flex flex-col min-h-full">
      <Header
        title={`Artist Dossier: ${artistId}`}
        subtitle="Independent capability evaluation, physical portfolio citations, and self-reported profile statements."
        badge={artist ? `${artist.confidence} Confidence` : undefined}
        phaseTag="DOSSIER VIEW"
      />

      <div className="p-6 md:p-8 space-y-6 max-w-7xl">
        <Link
          href="/artists"
          className="inline-flex items-center gap-2 text-xs font-mono text-text-muted hover:text-text-primary transition-colors mb-2"
        >
          <ArrowLeft className="w-3.5 h-3.5" /> Back to Artists Directory
        </Link>

        {loading && <LoadingState message={`Fetching intelligence dossier for ${artistId}...`} isColdStart={isColdStart} />}

        {error && (
          <ErrorState
            title="Artist Profile Not Found"
            message={error}
            onRetry={loadArtist}
          />
        )}

        {!loading && !error && artist && (
          <div className="space-y-8 animate-revealUp">
            {/* Identity & Metadata Banner */}
            <div className="p-6 rounded-xl bg-surface border border-border-subtle flex flex-col md:flex-row md:items-center justify-between gap-6">
              <div className="space-y-1.5">
                <div className="flex items-center gap-2 flex-wrap">
                  <span className="font-mono text-xs font-bold text-accent-primary bg-accent-primary/10 px-2 py-0.5 rounded border border-accent-primary/25">
                    {artist.artist_id}
                  </span>
                  <span className="text-xs font-mono text-text-muted">
                    Category: {formatCategoryName(artist.category)}
                  </span>
                  <span className="text-xs font-mono text-text-muted">
                    • Status: {artist.identifier_status}
                  </span>
                </div>
                <h2 className="text-2xl md:text-3xl font-bold text-text-primary tracking-tight">
                  {artist.declared_name || artist.source_folder_name}
                </h2>
                <div className="flex items-center gap-2 text-xs text-text-muted font-mono pt-1">
                  <Folder className="w-3.5 h-3.5 text-text-muted shrink-0" />
                  <span>Raw Folder: {artist.source_folder_name}</span>
                </div>
              </div>

              <div className="flex flex-col md:items-end gap-2 shrink-0">
                <span className={`text-xs font-mono font-bold px-3 py-1 rounded-full border ${getConfidenceBadgeClass(artist.confidence)}`}>
                  {artist.confidence} OVERALL CONFIDENCE
                </span>
                <span className="text-[11px] font-mono text-text-muted">
                  Deterministic ID Match
                </span>
              </div>
            </div>

            {/* Documented Anomaly Banner if present */}
            {artist.discrepancies_and_anomalies && artist.discrepancies_and_anomalies.length > 0 && (
              <div className="p-4 rounded-xl bg-accent-amber/10 border border-accent-amber/25 text-xs space-y-2">
                <div className="flex items-center gap-2 text-accent-amber font-semibold">
                  <ShieldAlert className="w-4 h-4 shrink-0" />
                  <span>Preserved Anomaly Note:</span>
                </div>
                <ul className="list-disc list-inside text-text-secondary font-mono space-y-1 text-[11px]">
                  {artist.discrepancies_and_anomalies.map((disc, idx) => (
                    <li key={idx} className="leading-relaxed">
                      {disc}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Epistemic Breakdown View */}
            <DemonstratedEvidenceView
              demonstratedCapabilities={artist.demonstrated_capabilities}
              profileClaims={artist.profile_claims}
              unknowns={artist.unknowns}
            />
          </div>
        )}
      </div>
    </div>
  );
}
