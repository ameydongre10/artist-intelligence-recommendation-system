import React from 'react';
import { cn } from '@/lib/utils';

interface BadgeProps {
  children: React.ReactNode;
  variant?: 'default' | 'blue' | 'indigo' | 'emerald' | 'amber' | 'rose' | 'slate';
  size?: 'sm' | 'md';
  className?: string;
}

export function Badge({ children, variant = 'default', size = 'sm', className }: BadgeProps) {
  const variantStyles = {
    default:
      'bg-surface-subtle text-text-secondary border-border-subtle',
    blue:
      'bg-accent-primary/10 text-accent-primary border-accent-primary/25 dark:bg-accent-primary/15 dark:text-blue-400 dark:border-accent-primary/30',
    indigo:
      'bg-accent-indigo/10 text-accent-indigo border-accent-indigo/25 dark:bg-accent-indigo/15 dark:text-indigo-400 dark:border-accent-indigo/30',
    emerald:
      'bg-accent-emerald/10 text-accent-emerald border-accent-emerald/25 dark:bg-accent-emerald/15 dark:text-emerald-400 dark:border-accent-emerald/30',
    amber:
      'bg-accent-amber/10 text-accent-amber border-accent-amber/25 dark:bg-accent-amber/15 dark:text-amber-400 dark:border-accent-amber/30',
    rose:
      'bg-accent-rose/10 text-accent-rose border-accent-rose/25 dark:bg-accent-rose/15 dark:text-rose-400 dark:border-accent-rose/30',
    slate:
      'bg-surface-muted text-text-muted border-border-subtle dark:bg-surface-elevated dark:text-slate-400 dark:border-border-subtle',
  };

  const sizeStyles = {
    sm: 'text-[11px] px-2 py-0.5',
    md: 'text-xs px-2.5 py-1',
  };

  return (
    <span
      className={cn(
        'inline-flex items-center gap-1.5 rounded-md font-mono font-medium border tracking-tight transition-colors duration-150',
        sizeStyles[size],
        variantStyles[variant],
        className
      )}
    >
      {children}
    </span>
  );
}
