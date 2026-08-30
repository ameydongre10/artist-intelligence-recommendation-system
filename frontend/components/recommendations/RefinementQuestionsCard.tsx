'use client';

import { HelpCircle, Sparkles, ArrowRight } from 'lucide-react';
import { RefinementQuestion } from '@/lib/types';
import { Badge } from '@/components/ui/Badge';

interface RefinementQuestionsCardProps {
  questions: RefinementQuestion[];
}

export function RefinementQuestionsCard({ questions }: RefinementQuestionsCardProps) {
  if (!questions || questions.length === 0) {
    return (
      <div className="p-5 rounded-xl bg-surface border border-border-subtle text-xs text-text-muted">
        No refinement questions necessary for this brief.
      </div>
    );
  }

  return (
    <div className="p-6 rounded-xl bg-surface border border-border-subtle space-y-5 animate-revealUp">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 border-b border-border-subtle">
        <div className="flex items-center gap-2.5">
          <Sparkles className="w-4 h-4 text-accent-indigo shrink-0" />
          <h2 className="text-sm font-bold text-text-primary uppercase tracking-wider">
            Targeted Refinement Questions (Max 2 Allowed)
          </h2>
        </div>
        <span className="font-mono text-[10px] text-accent-indigo px-2 py-0.5 rounded bg-accent-indigo/10 border border-accent-indigo/25 self-start sm:self-auto font-semibold">
          HIGH DECISION LEVERAGE
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {questions.map((q) => (
          <div
            key={q.question_id}
            className="p-5 rounded-lg bg-surface-subtle border border-border-subtle space-y-3 flex flex-col justify-between"
          >
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <Badge variant="indigo">{q.question_id}</Badge>
                <span className="text-xs font-bold text-text-primary font-mono">TARGET INQUIRY</span>
              </div>
              <p className="text-xs md:text-sm text-text-primary font-semibold leading-relaxed bg-surface p-3.5 rounded-md border border-border-subtle">
                {`"${q.question_text}"`}
              </p>
            </div>

            <div className="space-y-1.5 text-[11px] font-mono text-text-muted pt-2 border-t border-border-subtle/70">
              <div>
                <span className="text-text-secondary font-semibold">Why it matters:</span> {q.why_it_matters}
              </div>
              <div className="text-accent-indigo">
                <span className="text-text-secondary font-semibold">Ranking Impact:</span> {q.potential_ranking_impact}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
