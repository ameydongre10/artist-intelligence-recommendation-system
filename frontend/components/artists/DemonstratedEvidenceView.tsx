'use client';

import { CheckCircle2, FileText, HelpCircle, ShieldCheck } from 'lucide-react';
import { DemonstratedCapability, ProfileClaim, UnknownCapability } from '@/lib/types';
import { Badge } from '@/components/ui/Badge';
import { MediaEvidenceCard } from '@/components/media/MediaEvidenceCard';

interface DemonstratedEvidenceViewProps {
  demonstratedCapabilities: DemonstratedCapability[];
  profileClaims: ProfileClaim[];
  unknowns: UnknownCapability[];
}

export function DemonstratedEvidenceView({
  demonstratedCapabilities,
  profileClaims,
  unknowns,
}: DemonstratedEvidenceViewProps) {
  return (
    <div className="space-y-10 animate-revealUp">
      {/* 1. Demonstrated Capabilities Section */}
      <div className="space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 border-b border-border-subtle">
          <div className="flex items-center gap-2.5">
            <span className="w-2.5 h-2.5 rounded-full bg-accent-indigo shrink-0" />
            <h2 className="text-base font-bold text-text-primary uppercase tracking-wider">
              01 // Verified Demonstrated Capabilities ({demonstratedCapabilities.length})
            </h2>
          </div>
          <Badge variant="indigo">PHYSICAL MEDIA EVIDENCE CITATIONS</Badge>
        </div>

        <div className="space-y-6">
          {demonstratedCapabilities.map((cap) => (
            <div
              key={cap.capability_id}
              className="p-6 rounded-xl bg-surface border border-border-subtle hover:border-border-strong transition-colors space-y-4"
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                <div className="flex items-center gap-2 flex-wrap">
                  <Badge variant="indigo" size="md">
                    {cap.dimension.replace(/_/g, ' ').toUpperCase()}
                  </Badge>
                  <span className="text-xs font-mono text-text-muted">
                    Strength: <span className="text-text-primary font-semibold">{cap.evidence_strength}</span>
                  </span>
                </div>
                <span className="text-xs font-mono text-accent-emerald flex items-center gap-1.5 font-semibold">
                  <ShieldCheck className="w-4 h-4" /> VERIFIED EVIDENCE
                </span>
              </div>

              <p className="text-sm text-text-primary leading-relaxed">{cap.description}</p>

              {/* Technical Media Citations */}
              {cap.evidence_citations && cap.evidence_citations.length > 0 && (
                <div className="pt-4 border-t border-border-subtle space-y-3">
                  <span className="text-[11px] font-mono font-bold text-text-muted uppercase tracking-wider block">
                    Observed Portfolio Media Assets ({cap.evidence_citations.length}):
                  </span>

                  <div className="grid grid-cols-1 gap-3.5">
                    {cap.evidence_citations.map((cit) => (
                      <MediaEvidenceCard key={cit.evidence_id} citation={cit} />
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* 2. Self-Reported Profile Claims Section */}
      <div className="space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 border-b border-border-subtle">
          <div className="flex items-center gap-2.5">
            <span className="w-2.5 h-2.5 rounded-full bg-accent-primary shrink-0" />
            <h2 className="text-base font-bold text-text-primary uppercase tracking-wider">
              02 // Self-Reported Profile Claims ({profileClaims.length})
            </h2>
          </div>
          <span className="font-mono text-[10px] text-text-muted px-2 py-0.5 rounded bg-surface-subtle border border-border-subtle">
            UNVERIFIED STATEMENTS FROM PROFILE DOCX
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {profileClaims.map((claim) => (
            <div
              key={claim.claim_id}
              className="p-5 rounded-xl bg-surface border border-border-subtle hover:border-border-strong transition-colors space-y-2.5 flex flex-col justify-between"
            >
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <Badge variant="blue">{claim.dimension.replace(/_/g, ' ').toUpperCase()}</Badge>
                  <span className="text-[10px] font-mono text-accent-primary px-1.5 py-0.2 rounded bg-accent-primary/10 border border-accent-primary/20">
                    CLAIM
                  </span>
                </div>
                <p className="text-xs text-text-secondary italic leading-relaxed">{`"${claim.statement}"`}</p>
              </div>

              <div className="text-[10px] font-mono text-text-muted pt-2 border-t border-border-subtle/60">
                Source: {claim.source_context}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* 3. Unknown Capabilities Section */}
      <div className="space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 border-b border-border-subtle">
          <div className="flex items-center gap-2.5">
            <span className="w-2.5 h-2.5 rounded-full bg-text-muted shrink-0" />
            <h2 className="text-base font-bold text-text-primary uppercase tracking-wider">
              03 // Unknown Dimensions & Information Limits ({unknowns.length})
            </h2>
          </div>
          <span className="font-mono text-[10px] text-text-muted px-2 py-0.5 rounded bg-surface-subtle border border-border-subtle">
            ZERO PENALTY / STRICTLY NEUTRAL
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {unknowns.map((ukn) => (
            <div
              key={ukn.unknown_id}
              className="p-5 rounded-xl bg-surface border border-border-subtle space-y-2 flex flex-col justify-between"
            >
              <div className="space-y-1.5">
                <div className="flex items-center justify-between">
                  <Badge variant="slate">{ukn.dimension.replace(/_/g, ' ').toUpperCase()}</Badge>
                  <span className="text-[10px] font-mono text-text-muted">UNKNOWN</span>
                </div>
                <p className="text-xs text-text-secondary leading-relaxed">{ukn.description}</p>
              </div>

              <div className="text-[11px] text-text-muted font-mono pt-2 border-t border-border-subtle/60">
                Reason: {ukn.reason}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
