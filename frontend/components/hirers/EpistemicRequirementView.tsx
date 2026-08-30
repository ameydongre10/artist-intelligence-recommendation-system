'use client';

import { 
  CheckCircle2, 
  AlertTriangle, 
  HelpCircle, 
  Lock, 
  Heart, 
  Package, 
  Compass, 
  Quote,
  ShieldAlert
} from 'lucide-react';
import { 
  RequirementItem, 
  ConstraintItem, 
  PreferenceItem, 
  DeliverableItem, 
  AssumptionItem, 
  UnknownItem, 
  AmbiguityItem, 
  ContradictionItem 
} from '@/lib/types';
import { Badge } from '@/components/ui/Badge';

interface EpistemicRequirementViewProps {
  knownRequirements: RequirementItem[];
  hardConstraints: ConstraintItem[];
  preferences: PreferenceItem[];
  deliverables: DeliverableItem[];
  assumptions: AssumptionItem[];
  unknowns: UnknownItem[];
  ambiguities: AmbiguityItem[];
  contradictions: ContradictionItem[];
}

export function EpistemicRequirementView({
  knownRequirements,
  hardConstraints,
  preferences,
  deliverables,
  assumptions,
  unknowns,
  ambiguities,
  contradictions,
}: EpistemicRequirementViewProps) {
  return (
    <div className="space-y-10 animate-revealUp">
      {/* 1. Hard Constraints Section */}
      <div className="space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 border-b border-border-subtle">
          <div className="flex items-center gap-2.5">
            <span className="w-2.5 h-2.5 rounded-full bg-accent-rose shrink-0" />
            <h2 className="text-base font-bold text-text-primary uppercase tracking-wider">
              01 // Hard Operational Constraints ({hardConstraints.length})
            </h2>
          </div>
          <Badge variant="rose">NON-NEGOTIABLE BOUNDARIES</Badge>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {hardConstraints.map((c) => (
            <div
              key={c.constraint_id}
              className="p-5 rounded-xl bg-surface border border-accent-rose/30 hover:border-accent-rose/50 transition-colors space-y-2.5 flex flex-col justify-between"
            >
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <Badge variant="rose">{c.constraint_type.toUpperCase()}</Badge>
                  <span className="text-[10px] font-mono text-accent-rose font-bold">HARD LIMIT</span>
                </div>
                <p className="text-sm font-bold text-text-primary leading-snug">{c.value}</p>
              </div>

              {c.source_quote && (
                <div className="text-xs text-text-muted italic bg-surface-subtle p-2.5 rounded-lg border border-border-subtle font-mono text-[11px] leading-relaxed">
                  {`"${c.source_quote}"`}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* 2. Explicit Known Requirements Section */}
      <div className="space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 border-b border-border-subtle">
          <div className="flex items-center gap-2.5">
            <span className="w-2.5 h-2.5 rounded-full bg-accent-primary shrink-0" />
            <h2 className="text-base font-bold text-text-primary uppercase tracking-wider">
              02 // Explicit Capability Requirements ({knownRequirements.length})
            </h2>
          </div>
          <Badge variant="blue">EPISTEMIC STATE: CLAIM</Badge>
        </div>

        <div className="space-y-3">
          {knownRequirements.map((r) => (
            <div
              key={r.requirement_id}
              className="p-5 rounded-xl bg-surface border border-border-subtle hover:border-border-strong transition-colors space-y-3"
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                <div className="flex items-center gap-2">
                  <Badge variant="blue">{r.dimension.replace(/_/g, ' ').toUpperCase()}</Badge>
                  <span className="text-xs font-mono text-text-muted">
                    Importance: <span className="font-semibold text-text-primary">{r.importance}</span>
                  </span>
                </div>
                <span className="text-[10px] font-mono text-accent-primary px-2 py-0.5 rounded bg-accent-primary/10 border border-accent-primary/25">
                  MANDATORY FIT CRITERION
                </span>
              </div>

              <p className="text-sm text-text-primary leading-relaxed">{r.description}</p>

              {r.source_quote && (
                <div className="flex items-start gap-2.5 text-xs text-text-secondary bg-surface-subtle p-3 rounded-lg border border-border-subtle font-mono">
                  <Quote className="w-4 h-4 text-text-muted shrink-0 mt-0.5" />
                  <span className="leading-relaxed">{`"${r.source_quote}"`}</span>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* 3. Soft Preferences & Deliverables Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Soft Preferences */}
        <div className="space-y-4">
          <div className="flex items-center gap-2.5 pb-3 border-b border-border-subtle">
            <span className="w-2.5 h-2.5 rounded-full bg-accent-indigo shrink-0" />
            <h2 className="text-base font-bold text-text-primary uppercase tracking-wider">
              03 // Soft Preferences ({preferences.length})
            </h2>
          </div>

          <div className="space-y-3">
            {preferences.map((p) => (
              <div
                key={p.preference_id}
                className="p-4 rounded-xl bg-surface border border-border-subtle space-y-2"
              >
                <div className="flex items-center justify-between">
                  <Badge variant="indigo">PREFERENCE</Badge>
                  <span className="text-[10px] font-mono text-text-muted">
                    {p.is_flexible ? 'Flexible Weighting' : 'Strict Priority'}
                  </span>
                </div>
                <p className="text-xs text-text-primary leading-relaxed">{p.description}</p>
                {p.source_quote && (
                  <p className="text-[11px] text-text-muted italic bg-surface-subtle p-2 rounded border border-border-subtle">
                    {`"${p.source_quote}"`}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Deliverables */}
        <div className="space-y-4">
          <div className="flex items-center gap-2.5 pb-3 border-b border-border-subtle">
            <span className="w-2.5 h-2.5 rounded-full bg-accent-emerald shrink-0" />
            <h2 className="text-base font-bold text-text-primary uppercase tracking-wider">
              04 // Expected Deliverables ({deliverables.length})
            </h2>
          </div>

          <div className="space-y-3">
            {deliverables.map((d) => (
              <div
                key={d.deliverable_id}
                className="p-4 rounded-xl bg-surface border border-border-subtle space-y-2"
              >
                <div className="flex items-center justify-between">
                  <Badge variant="emerald">DELIVERABLE</Badge>
                  <span className="text-[10px] font-mono text-accent-emerald font-semibold">
                    {d.turnaround_expectation}
                  </span>
                </div>
                <p className="text-xs text-text-primary leading-relaxed">{d.description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* 4. Operational Assumptions & Unknowns Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Assumptions */}
        <div className="space-y-4">
          <div className="flex items-center gap-2.5 pb-3 border-b border-border-subtle">
            <span className="w-2.5 h-2.5 rounded-full bg-accent-amber shrink-0" />
            <h2 className="text-base font-bold text-text-primary uppercase tracking-wider">
              05 // Operational Assumptions ({assumptions.length})
            </h2>
          </div>

          <div className="space-y-3">
            {assumptions.map((a) => (
              <div
                key={a.assumption_id}
                className="p-5 rounded-xl bg-surface border border-accent-amber/30 space-y-2.5"
              >
                <div className="flex items-center justify-between">
                  <Badge variant="amber">ASSUMPTION</Badge>
                  <span className="text-[10px] font-mono text-accent-amber font-bold">{a.assumption_id}</span>
                </div>
                <p className="text-xs font-semibold text-text-primary leading-relaxed">{a.description}</p>
                <div className="text-[11px] text-text-secondary font-mono space-y-1 bg-surface-subtle p-3 rounded-lg border border-border-subtle">
                  <div><span className="text-text-muted">Rationale:</span> {a.rationale}</div>
                  <div><span className="text-accent-rose">Risk Impact:</span> {a.risk_impact}</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Unknowns */}
        <div className="space-y-4">
          <div className="flex items-center gap-2.5 pb-3 border-b border-border-subtle">
            <span className="w-2.5 h-2.5 rounded-full bg-text-muted shrink-0" />
            <h2 className="text-base font-bold text-text-primary uppercase tracking-wider">
              06 // Unresolved Unknowns ({unknowns.length})
            </h2>
          </div>

          <div className="space-y-3">
            {unknowns.map((u) => (
              <div
                key={u.unknown_id}
                className="p-5 rounded-xl bg-surface border border-border-subtle space-y-2.5"
              >
                <div className="flex items-center justify-between">
                  <Badge variant="slate">UNKNOWN</Badge>
                  {u.is_decision_critical && (
                    <span className="text-[10px] font-mono text-accent-rose px-2 py-0.5 rounded bg-accent-rose/10 border border-accent-rose/25 font-bold">
                      DECISION CRITICAL
                    </span>
                  )}
                </div>
                <p className="text-xs font-semibold text-text-primary leading-relaxed">{u.description}</p>
                <div className="text-[11px] text-text-muted font-mono bg-surface-subtle p-3 rounded-lg border border-border-subtle">
                  <span className="text-text-secondary font-medium">Why it matters:</span> {u.why_it_matters}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* 5. Contradictions & Ambiguities */}
      {(contradictions.length > 0 || ambiguities.length > 0) && (
        <div className="space-y-4 pt-4 border-t border-border-subtle">
          <div className="flex items-center gap-2.5 pb-3 border-b border-border-subtle">
            <ShieldAlert className="w-4 h-4 text-accent-rose" />
            <h2 className="text-base font-bold text-text-primary uppercase tracking-wider">
              07 // Detected Ambiguities & Structural Tensions
            </h2>
          </div>

          <div className="grid grid-cols-1 gap-4">
            {contradictions.map((c) => (
              <div
                key={c.contradiction_id}
                className="p-5 rounded-xl bg-surface border border-accent-rose/30 space-y-3"
              >
                <div className="flex items-center justify-between">
                  <Badge variant="rose">STRUCTURAL CONTRADICTION</Badge>
                  <span className="text-[10px] font-mono text-accent-rose font-bold">{c.contradiction_id}</span>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                  <div className="p-3 rounded-lg bg-surface-subtle border border-border-subtle">
                    <span className="text-accent-rose font-mono font-bold">Statement A:</span>
                    <p className="text-text-secondary mt-1">{c.statement_a}</p>
                  </div>
                  <div className="p-3 rounded-lg bg-surface-subtle border border-border-subtle">
                    <span className="text-accent-rose font-mono font-bold">Statement B:</span>
                    <p className="text-text-secondary mt-1">{c.statement_b}</p>
                  </div>
                </div>
                <p className="text-xs text-text-muted font-mono pt-1">
                  <span className="text-text-secondary font-semibold">Decision Impact:</span> {c.impact_on_decision}
                </p>
              </div>
            ))}

            {ambiguities.map((a) => (
              <div
                key={a.ambiguity_id}
                className="p-5 rounded-xl bg-surface border border-accent-amber/30 space-y-2"
              >
                <div className="flex items-center justify-between">
                  <Badge variant="amber">AMBIGUITY</Badge>
                  <span className="text-[10px] font-mono text-accent-amber">{a.ambiguity_id}</span>
                </div>
                <p className="text-xs text-text-primary italic leading-relaxed">{`"${a.statement}"`}</p>
                <div className="text-[11px] text-text-muted font-mono bg-surface-subtle p-2.5 rounded-lg border border-border-subtle">
                  <span className="text-text-secondary font-medium">Interpretations:</span>{' '}
                  {a.possible_interpretations.join(' OR ')}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
