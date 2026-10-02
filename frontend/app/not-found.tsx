import Link from 'next/link';
import { ArrowLeft, Compass } from 'lucide-react';

export default function NotFound() {
  return (
    <div className="flex-1 flex flex-col items-center justify-center p-8 text-center min-h-[60vh]">
      <div className="p-4 rounded-full bg-accent-primary/10 border border-accent-primary/25 text-accent-primary mb-4">
        <Compass className="w-8 h-8 animate-spin-slow" />
      </div>
      <h1 className="text-3xl font-bold tracking-tight text-text-primary mb-2 font-mono">
        404 - Page Not Found
      </h1>
      <p className="text-sm text-text-secondary max-w-md mb-6 leading-relaxed">
        The requested intelligence artifact or dossier route could not be found.
      </p>
      <div className="flex items-center gap-3">
        <Link
          href="/"
          className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-accent-primary text-white text-xs font-semibold hover:bg-accent-primary/90 transition shadow-sm"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Return to Dashboard</span>
        </Link>
        <Link
          href="/artists"
          className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-surface-subtle hover:bg-surface-muted text-text-primary text-xs font-semibold border border-border-strong transition"
        >
          <span>Artists Directory</span>
        </Link>
      </div>
    </div>
  );
}
