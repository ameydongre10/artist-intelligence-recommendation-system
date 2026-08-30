'use client';

import { useTheme } from './ThemeProvider';
import { Sun, Moon } from 'lucide-react';
import { useEffect, useState } from 'react';

export function ThemeToggle({ className = '' }: { className?: string }) {
  const { resolvedTheme, toggleTheme } = useTheme();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return (
      <div className={`w-8 h-8 rounded-lg bg-surface-muted border border-border-subtle ${className}`} />
    );
  }

  const isDark = resolvedTheme === 'dark';

  return (
    <button
      type="button"
      onClick={toggleTheme}
      aria-label={`Switch to ${isDark ? 'light' : 'dark'} mode`}
      title={`Switch to ${isDark ? 'light' : 'dark'} mode`}
      className={`inline-flex items-center justify-center w-8 h-8 rounded-lg border transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-accent-primary/40 ${
        isDark
          ? 'bg-surface-elevated/70 border-border-subtle text-text-secondary hover:text-text-primary hover:border-border-strong hover:bg-surface-elevated'
          : 'bg-surface-elevated border-border-subtle text-text-secondary hover:text-text-primary hover:border-border-strong hover:bg-surface-subtle'
      } ${className}`}
    >
      {isDark ? (
        <Sun className="w-4 h-4 text-amber-400 transition-transform duration-200 rotate-0 hover:rotate-45" />
      ) : (
        <Moon className="w-4 h-4 text-indigo-600 transition-transform duration-200 rotate-0 hover:-rotate-12" />
      )}
    </button>
  );
}
