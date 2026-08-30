'use client';

import { AlertTriangle, RefreshCcw } from 'lucide-react';

interface ErrorStateProps {
  title?: string;
  message?: string;
  onRetry?: () => void;
}

export function ErrorState({
  title = 'Failed to load intelligence data',
  message = 'An unexpected error occurred while communicating with the backend.',
  onRetry,
}: ErrorStateProps) {
  return (
    <div className="flex flex-col items-center justify-center min-h-[320px] p-8 text-center bg-surface border border-accent-rose/30 rounded-xl animate-fadeIn">
      <div className="w-10 h-10 rounded-lg bg-accent-rose/10 flex items-center justify-center mb-3 text-accent-rose">
        <AlertTriangle className="w-5 h-5" />
      </div>
      <h3 className="text-base font-semibold text-text-primary mb-1.5">{title}</h3>
      <p className="text-xs md:text-sm text-text-muted max-w-md mb-5 leading-relaxed">{message}</p>
      {onRetry && (
        <button
          type="button"
          onClick={onRetry}
          className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-surface-subtle hover:bg-surface-muted text-text-primary text-xs font-semibold border border-border-strong transition-all focus:outline-none focus:ring-2 focus:ring-accent-primary/40 shadow-sm"
        >
          <RefreshCcw className="w-3.5 h-3.5" />
          <span>Retry Connection</span>
        </button>
      )}
    </div>
  );
}
