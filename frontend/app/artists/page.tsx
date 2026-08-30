'use client';

import { useEffect, useState, useMemo } from 'react';
import { Header } from '@/components/ui/Header';
import { ArtistCard } from '@/components/artists/ArtistCard';
import { LoadingState } from '@/components/ui/LoadingState';
import { ErrorState } from '@/components/ui/ErrorState';
import { api, ApiError } from '@/lib/api';
import { ArtistSummary } from '@/lib/types';
import { Camera, Music, Video, Filter, Search } from 'lucide-react';
import { cn } from '@/lib/utils';

export default function ArtistsPage() {
  const [artists, setArtists] = useState<ArtistSummary[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isColdStart, setIsColdStart] = useState(false);

  const loadArtists = async (category?: string) => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.getArtists(category);
      setArtists(data);
    } catch (err: any) {
      if (err instanceof ApiError) {
        setIsColdStart(err.isColdStart);
        setError(err.message);
      } else {
        setError(err.message || 'Failed to load artists');
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadArtists(selectedCategory);
  }, [selectedCategory]);

  const filteredArtists = useMemo(() => {
    if (!searchQuery.trim()) return artists;
    const q = searchQuery.toLowerCase();
    return artists.filter(
      (a) =>
        a.artist_id.toLowerCase().includes(q) ||
        (a.declared_name && a.declared_name.toLowerCase().includes(q)) ||
        a.source_folder_name.toLowerCase().includes(q)
    );
  }, [artists, searchQuery]);

  const categories = [
    { id: 'all', label: 'All Artists (15)', icon: Filter },
    { id: 'photographer', label: 'Photographers (5)', icon: Camera },
    { id: 'musician', label: 'Musicians (5)', icon: Music },
    { id: 'video_editor', label: 'Video Editors (5)', icon: Video },
  ];

  return (
    <div className="flex-1 flex flex-col min-h-full">
      <Header
        title="Artist Intelligence Explorer"
        subtitle="Comprehensive dossiers for 15 creative artists with category dimensions, verified portfolio evidence, and self-reported profile claims."
        phaseTag="PHASE 3 ARTIFACT"
      />

      <div className="p-6 md:p-8 space-y-6 max-w-7xl">
        {/* Controls Toolbar */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          {/* Category Filter Chips */}
          <div className="flex items-center gap-2 overflow-x-auto pb-1">
            {categories.map((cat) => {
              const Icon = cat.icon;
              const isActive = selectedCategory === cat.id;
              return (
                <button
                  type="button"
                  key={cat.id}
                  onClick={() => setSelectedCategory(cat.id)}
                  className={cn(
                    'flex items-center gap-2 px-3.5 py-2 rounded-lg text-xs font-mono font-semibold transition-all whitespace-nowrap border',
                    isActive
                      ? 'bg-accent-primary text-white border-accent-primary shadow-sm'
                      : 'bg-surface text-text-secondary border-border-subtle hover:text-text-primary hover:bg-surface-subtle hover:border-border-strong'
                  )}
                >
                  <Icon className="w-3.5 h-3.5" />
                  <span>{cat.label}</span>
                </button>
              );
            })}
          </div>

          {/* Quick Search */}
          <div className="relative min-w-[240px]">
            <Search className="w-4 h-4 text-text-muted absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Search by ID or name..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-9 pr-4 py-2 rounded-lg bg-surface border border-border-subtle text-xs text-text-primary placeholder:text-text-muted focus:outline-none focus:ring-2 focus:ring-accent-primary/40 focus:border-accent-primary transition-all font-mono"
            />
          </div>
        </div>

        {loading && <LoadingState message="Fetching artist intelligence profiles..." isColdStart={isColdStart} />}

        {error && (
          <ErrorState
            title="Artist Data Unavailable"
            message={error}
            onRetry={() => loadArtists(selectedCategory)}
          />
        )}

        {!loading && !error && (
          <>
            {filteredArtists.length === 0 ? (
              <div className="p-12 text-center bg-surface border border-border-subtle rounded-xl text-text-muted text-xs">
                No artists matched your filter criteria.
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5 animate-revealUp">
                {filteredArtists.map((artist) => (
                  <ArtistCard key={artist.artist_id} artist={artist} />
                ))}
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
