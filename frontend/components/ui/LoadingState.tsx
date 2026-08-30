'use client';

import { Loader2, Server } from 'lucide-react';

interface LoadingStateProps {
  message?: string;
  isColdStart?: boolean;
}

export function LoadingState({
  message = 'Loading intelligence artifacts...',
  isColdStart = false,
}: LoadingStateProps) {
  return (
    <div className="flex flex-col items-center justify-center min-h-[320px] p-8 text-center bg-surface border border-border-subtle rounded-xl animate-fadeIn">
      <div className="relative mb-4">
        <div className="w-10 h-10 rounded-full border-2 border-accent-primary/20 flex items-center justify-center">
          <Loader2 className="w-5 h-5 text-accent-primary animate-spin" />
        </div>
      </div>
      <h3 className="text-sm font-semibold text-text-primary mb-1">{message}</h3>
      <p className="text-xs text-text-muted font-mono">Connecting to FastAPI engine</p>

      {isColdStart && (
        <div className="mt-4 max-w-md p-3.5 rounded-lg bg-accent-primary/10 border border-accent-primary/25 text-xs text-text-secondary flex items-start gap-2.5">
          <Server className="w-4 h-4 text-accent-primary shrink-0 mt-0.5" />
          <p className="text-left leading-relaxed">
            The intelligence service is warming up. This takes a few seconds on cold starts.
          </p>
        </div>
      )}
    </div>
  );
}
