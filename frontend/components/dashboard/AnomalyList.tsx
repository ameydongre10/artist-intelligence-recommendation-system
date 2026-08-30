'use client';

import { AlertTriangle, FolderGit2, ShieldAlert } from 'lucide-react';
import { Badge } from '@/components/ui/Badge';
import { DetectedAnomalyGroup } from '@/lib/types';

interface AnomalyListProps {
  anomalies?: DetectedAnomalyGroup[];
}

export function AnomalyList({ anomalies }: AnomalyListProps) {
  if (!anomalies || anomalies.length === 0) {
    return null;
  }

  return (
    <div id="anomalies" className="p-6 rounded-xl bg-surface border border-border-subtle space-y-5 animate-revealUp">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-4 border-b border-border-subtle">
        <div>
          <h2 className="text-sm font-bold text-text-primary uppercase tracking-wider flex items-center gap-2">
            <ShieldAlert className="w-4 h-4 text-accent-amber" />
            <span>Preserved Dataset & Identifier Anomalies ({anomalies.length})</span>
          </h2>
          <p className="text-xs text-text-muted mt-0.5">
            Factual inconsistencies discovered during inventory (e.g. typos, ID collisions, mislabelled folders) preserved with canonical resolutions.
          </p>
        </div>
        <span className="font-mono text-[10px] text-accent-amber px-2.5 py-1 rounded bg-accent-amber/10 border border-accent-amber/25 self-start sm:self-auto">
          ZERO DATA LOSS POLICY
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {anomalies.map((a, idx) => (
          <div
            key={a.artist_folder || idx}
            className="p-4 rounded-lg bg-surface-subtle border border-border-subtle hover:border-border-strong transition-colors space-y-2.5 flex flex-col justify-between"
          >
            <div>
              <div className="flex items-center justify-between gap-2">
                <div className="flex items-center gap-2">
                  <Badge variant="amber">{a.artist_folder}</Badge>
                  <span className="text-xs font-mono text-text-muted capitalize">
                    {a.category?.replace(/_/g, ' ')}
                  </span>
                </div>
                <span className="text-[10px] font-mono text-text-muted">
                  {a.anomalies?.length || 0} {a.anomalies?.length === 1 ? 'discrepancy' : 'discrepancies'}
                </span>
              </div>

              {a.anomalies && a.anomalies.length > 0 && (
                <ul className="mt-2.5 space-y-1.5 text-xs text-text-secondary font-mono text-[11px]">
                  {a.anomalies.map((msg, mIdx) => (
                    <li key={mIdx} className="flex items-start gap-2 leading-relaxed">
                      <span className="text-accent-amber shrink-0 mt-0.5">•</span>
                      <span>{msg}</span>
                    </li>
                  ))}
                </ul>
              )}
            </div>

            <div className="pt-2 border-t border-border-subtle/70 text-[10px] font-mono text-text-muted flex items-center justify-between">
              <span>Status: Preserved in Inventory</span>
              <span>Canonical Resolved</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
