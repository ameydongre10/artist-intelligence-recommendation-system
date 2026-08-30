'use client';

import { ShieldCheck, Cpu, Database } from 'lucide-react';
import { Badge } from '@/components/ui/Badge';

interface HeaderProps {
  title: string;
  subtitle?: string;
  badge?: string;
  phaseTag?: string;
}

export function Header({ title, subtitle, badge, phaseTag }: HeaderProps) {
  return (
    <header className="py-6 px-6 md:px-8 border-b border-border-subtle bg-surface-elevated/80 backdrop-blur-sm sticky top-0 z-20 transition-colors duration-150">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 max-w-7xl">
        <div className="space-y-1">
          <div className="flex items-center gap-2.5 flex-wrap">
            {phaseTag && (
              <span className="font-mono text-[10px] font-semibold px-2 py-0.5 rounded bg-accent-primary/10 text-accent-primary border border-accent-primary/25">
                {phaseTag}
              </span>
            )}
            <h1 className="text-xl md:text-2xl font-bold text-text-primary tracking-tight">
              {title}
            </h1>
            {badge && (
              <Badge variant="emerald" size="sm">
                {badge}
              </Badge>
            )}
          </div>
          {subtitle && (
            <p className="text-xs md:text-sm text-text-secondary leading-relaxed max-w-3xl">
              {subtitle}
            </p>
          )}
        </div>

        <div className="flex items-center gap-2 text-xs text-text-muted self-start md:self-auto shrink-0">
          <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-surface-subtle border border-border-subtle font-mono text-[11px]">
            <ShieldCheck className="w-3.5 h-3.5 text-accent-emerald shrink-0" />
            <span className="text-text-secondary">Grounded Citations</span>
          </div>
          <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-surface-subtle border border-border-subtle font-mono text-[11px]">
            <Cpu className="w-3.5 h-3.5 text-accent-primary shrink-0" />
            <span className="text-text-secondary">Deterministic</span>
          </div>
        </div>
      </div>
    </header>
  );
}
