'use client';

import { Scale, ArrowLeftRight } from 'lucide-react';
import { TradeOffItem } from '@/lib/types';
import { Badge } from '@/components/ui/Badge';

interface TradeOffCardProps {
  tradeOffs: TradeOffItem[];
}

export function TradeOffCard({ tradeOffs }: TradeOffCardProps) {
  if (!tradeOffs || tradeOffs.length === 0) {
    return null;
  }

  return (
    <div className="p-6 rounded-xl bg-surface border border-border-subtle space-y-5 animate-revealUp">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 border-b border-border-subtle">
        <div className="flex items-center gap-2.5">
          <Scale className="w-4 h-4 text-accent-indigo shrink-0" />
          <h2 className="text-sm font-bold text-text-primary uppercase tracking-wider">
            Comparative Trade-Off Evaluation (Rank 1 vs Rank 2)
          </h2>
        </div>
        <span className="font-mono text-[10px] text-text-muted">
          OBJECTIVE CAPABILITY DIFFERENTIALS
        </span>
      </div>

      <div className="space-y-4">
        {tradeOffs.map((to, idx) => (
          <div
            key={idx}
            className="p-5 rounded-lg bg-surface-subtle border border-border-subtle space-y-3.5"
          >
            <div className="flex items-center gap-2">
              <Badge variant="indigo" size="sm">
                DIMENSION: {to.dimension.replace(/_/g, ' ').toUpperCase()}
              </Badge>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
              <div className="p-3.5 rounded-md bg-surface border border-border-subtle space-y-1">
                <span className="text-accent-emerald font-mono font-bold text-[11px] block">
                  Rank 1 Candidate Status:
                </span>
                <p className="text-text-primary leading-relaxed">{to.rank_1_status}</p>
              </div>

              <div className="p-3.5 rounded-md bg-surface border border-border-subtle space-y-1">
                <span className="text-text-muted font-mono font-bold text-[11px] block">
                  Rank 2 Candidate Status:
                </span>
                <p className="text-text-primary leading-relaxed">{to.rank_2_status}</p>
              </div>
            </div>

            <div className="pt-2.5 border-t border-border-subtle/70 text-xs text-text-secondary flex items-start gap-2">
              <ArrowLeftRight className="w-3.5 h-3.5 text-accent-primary shrink-0 mt-0.5" />
              <div>
                <span className="font-bold text-text-primary">Decision Implication:</span>{' '}
                {to.decision_implication}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
