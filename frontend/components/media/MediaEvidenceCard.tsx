'use client';

import { useState } from 'react';
import { 
  Camera, 
  Music, 
  Film, 
  Play, 
  Pause, 
  Sliders, 
  CheckCircle2, 
  Maximize2,
  Clock,
  Layers,
  Sparkles
} from 'lucide-react';
import { EvidenceCitation } from '@/lib/types';
import { Badge } from '@/components/ui/Badge';

interface MediaEvidenceCardProps {
  citation: EvidenceCitation;
}

export function MediaEvidenceCard({ citation }: MediaEvidenceCardProps) {
  const [isPlaying, setIsPlaying] = useState(false);

  const fileName = citation.file_name || '';
  const lowerName = fileName.toLowerCase();

  const isAudio = lowerName.endsWith('.mp3') || lowerName.endsWith('.wav') || lowerName.endsWith('.aac') || lowerName.includes('audio') || lowerName.includes('take') || lowerName.includes('demo');
  const isVideo = lowerName.endsWith('.mp4') || lowerName.endsWith('.mov') || lowerName.endsWith('.mkv') || lowerName.includes('reel') || lowerName.includes('video') || lowerName.includes('cut');
  const isPhoto = !isAudio && !isVideo;

  // Generate simulated waveform heights
  const waveformBars = [40, 65, 30, 85, 95, 55, 70, 45, 90, 100, 60, 40, 75, 80, 50, 65, 85, 30, 95, 70, 50, 80, 60, 40];

  return (
    <div className="rounded-xl bg-surface border border-border-subtle hover:border-accent-primary/40 transition-all overflow-hidden shadow-sm space-y-0 text-xs">
      {/* 1. Header Bar with File Type, File Name, and Verification Badge */}
      <div className="px-4 py-3 bg-surface-subtle border-b border-border-subtle flex flex-col sm:flex-row sm:items-center justify-between gap-2">
        <div className="flex items-center gap-2.5 min-w-0">
          <div className="p-1.5 rounded-lg bg-surface border border-border-subtle shrink-0">
            {isPhoto && <Camera className="w-3.5 h-3.5 text-accent-primary" />}
            {isAudio && <Music className="w-3.5 h-3.5 text-accent-indigo" />}
            {isVideo && <Film className="w-3.5 h-3.5 text-accent-cyan" />}
          </div>
          <div className="min-w-0">
            <span className="font-mono text-xs font-bold text-text-primary truncate block">
              {citation.file_name}
            </span>
          </div>
        </div>

        <div className="flex items-center gap-2 shrink-0">
          <span className="font-mono text-[10px] text-text-muted bg-surface px-2 py-0.5 rounded border border-border-subtle">
            {citation.timestamp_or_frame || 'Full Take'}
          </span>
          <span className="font-mono text-[10px] text-accent-emerald bg-accent-emerald/10 border border-accent-emerald/25 px-2 py-0.5 rounded flex items-center gap-1 font-semibold">
            <CheckCircle2 className="w-3 h-3" /> VERIFIED ASSET
          </span>
        </div>
      </div>

      {/* 2. Technical Media Inspector Body */}
      <div className="p-4 space-y-3.5">
        {/* AUDIO MEDIA INSPECTOR */}
        {isAudio && (
          <div className="p-3.5 rounded-lg bg-surface-subtle border border-border-subtle space-y-3">
            <div className="flex items-center justify-between gap-2">
              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={() => setIsPlaying(!isPlaying)}
                  aria-label={isPlaying ? 'Pause simulation' : 'Play simulated take'}
                  className="w-8 h-8 rounded-full bg-accent-indigo text-white flex items-center justify-center hover:bg-accent-indigo/90 transition shadow-sm shrink-0"
                >
                  {isPlaying ? <Pause className="w-3.5 h-3.5" /> : <Play className="w-3.5 h-3.5 ml-0.5" />}
                </button>
                <div className="font-mono text-[11px] text-text-muted">
                  {isPlaying ? (
                    <span className="text-accent-indigo font-semibold animate-pulse">Simulating Take Playback...</span>
                  ) : (
                    <span>Click to preview acoustic waveform</span>
                  )}
                </div>
              </div>

              <span className="font-mono text-[10px] text-text-muted bg-surface px-2 py-0.5 rounded border border-border-subtle">
                44.1kHz &bull; 16-bit PCM
              </span>
            </div>

            {/* Waveform Visualizer */}
            <div className="h-8 flex items-center gap-1 px-1 bg-surface rounded-md border border-border-subtle/80 overflow-hidden">
              {waveformBars.map((height, i) => (
                <div
                  key={i}
                  className={`flex-1 rounded-full transition-all duration-300 ${
                    isPlaying
                      ? 'bg-accent-indigo'
                      : i < 10
                      ? 'bg-accent-indigo/60'
                      : 'bg-border-strong'
                  }`}
                  style={{
                    height: isPlaying ? `${Math.max(20, (height + (i % 3) * 15) % 100)}%` : `${height}%`,
                    opacity: isPlaying ? 0.9 : 0.6,
                  }}
                />
              ))}
            </div>
          </div>
        )}

        {/* VIDEO MEDIA INSPECTOR */}
        {isVideo && (
          <div className="p-3.5 rounded-lg bg-surface-subtle border border-border-subtle space-y-2.5">
            <div className="flex items-center justify-between text-[11px] font-mono text-text-muted">
              <span className="flex items-center gap-1.5 text-text-secondary">
                <Clock className="w-3 h-3 text-accent-cyan" /> Timeline Scrubber: {citation.timestamp_or_frame}
              </span>
              <span className="bg-surface px-2 py-0.5 rounded border border-border-subtle">
                1080p @ 24fps
              </span>
            </div>

            {/* Simulated Video Scrubber Bar */}
            <div className="space-y-1">
              <div className="h-2 rounded-full bg-surface border border-border-subtle overflow-hidden relative">
                <div className="h-full bg-accent-cyan rounded-full w-2/5" />
              </div>
              <div className="flex justify-between text-[9px] font-mono text-text-muted">
                <span>00:00:00:00</span>
                <span className="text-accent-cyan font-bold">CITED FRAME</span>
                <span>00:02:15:00</span>
              </div>
            </div>
          </div>
        )}

        {/* PHOTO MEDIA INSPECTOR */}
        {isPhoto && (
          <div className="p-3 rounded-lg bg-surface-subtle border border-border-subtle flex items-center justify-between gap-2 font-mono text-[11px]">
            <div className="flex items-center gap-2 text-text-secondary">
              <Sliders className="w-3.5 h-3.5 text-accent-primary shrink-0" />
              <span>EXIF Artifact: 3:2 Ratio &bull; sRGB Color</span>
            </div>
            <span className="bg-surface px-2 py-0.5 rounded border border-border-subtle text-[10px] text-text-muted">
              Lossless Master
            </span>
          </div>
        )}

        {/* Citation Narrative */}
        <p className="text-xs text-text-secondary leading-relaxed bg-surface-subtle/50 p-3 rounded-lg border border-border-subtle/60">
          <span className="font-semibold text-text-primary block mb-0.5 font-mono text-[11px]">
            Observed Portfolio Evidence:
          </span>
          {citation.citation_text}
        </p>

        {/* Extracted Attributes & Observed Features Chips */}
        {citation.observed_features && citation.observed_features.length > 0 && (
          <div className="space-y-1.5 pt-1">
            <span className="text-[10px] font-mono font-semibold text-text-muted uppercase tracking-wider block">
              Extracted Feature Tags ({citation.observed_features.length}):
            </span>
            <div className="flex flex-wrap gap-1.5">
              {citation.observed_features.map((feat, idx) => (
                <span
                  key={idx}
                  className="font-mono text-[10px] px-2 py-0.5 rounded-md bg-surface-subtle text-text-secondary border border-border-subtle"
                >
                  #{feat}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
