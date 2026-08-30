import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatCategoryName(category: string): string {
  switch (category?.toLowerCase()) {
    case 'photographer':
    case 'photographers':
      return 'Photographer';
    case 'musician':
    case 'musicians':
      return 'Musician';
    case 'video_editor':
    case 'video_editors':
      return 'Video Editor';
    default:
      return category || 'Unknown';
  }
}

export function getConfidenceBadgeClass(confidence: string): string {
  switch (confidence?.toUpperCase()) {
    case 'HIGH':
      return 'bg-accent-emerald/10 text-accent-emerald border-accent-emerald/30 dark:bg-emerald-500/15 dark:text-emerald-400 dark:border-emerald-500/30';
    case 'MEDIUM':
      return 'bg-accent-amber/10 text-accent-amber border-accent-amber/30 dark:bg-amber-500/15 dark:text-amber-400 dark:border-amber-500/30';
    case 'LOW':
      return 'bg-accent-rose/10 text-accent-rose border-accent-rose/30 dark:bg-rose-500/15 dark:text-rose-400 dark:border-rose-500/30';
    default:
      return 'bg-surface-subtle text-text-muted border-border-subtle';
  }
}

export function getEpistemicStateBadgeClass(state: string): string {
  switch (state?.toUpperCase()) {
    case 'DEMONSTRATED_EVIDENCE':
      return 'bg-accent-indigo/10 text-accent-indigo border-accent-indigo/30 dark:bg-indigo-500/15 dark:text-indigo-300 dark:border-indigo-500/30';
    case 'CLAIM':
      return 'bg-accent-primary/10 text-accent-primary border-accent-primary/30 dark:bg-sky-500/15 dark:text-sky-400 dark:border-sky-500/30';
    case 'ASSUMPTION':
      return 'bg-accent-amber/10 text-accent-amber border-accent-amber/30 dark:bg-amber-500/15 dark:text-amber-400 dark:border-amber-500/30';
    case 'UNKNOWN':
      return 'bg-surface-subtle text-text-muted border-border-subtle dark:bg-slate-800 dark:text-slate-400 dark:border-slate-700';
    default:
      return 'bg-surface-subtle text-text-muted border-border-subtle';
  }
}
