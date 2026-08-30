'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { 
  LayoutDashboard, 
  Users, 
  FileText, 
  Sparkles, 
  RefreshCw,
  Terminal,
  Menu,
  X,
  Radio,
  Layers,
  ChevronRight
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { ThemeToggle } from '@/components/theme/ThemeToggle';

const navSections = [
  {
    title: 'Core Scanners',
    items: [
      { name: 'Console Overview', href: '/', icon: LayoutDashboard, tag: '01' },
      { name: 'Artist Intelligence', href: '/artists', icon: Users, tag: '02' },
      { name: 'Hirer Briefs', href: '/hirers', icon: FileText, tag: '03' },
    ],
  },
  {
    title: 'Decision Intelligence',
    items: [
      { name: 'Recommendations', href: '/recommendations', icon: Sparkles, tag: '04' },
      { name: 'Follow-Up Re-Ranking', href: '/reranking', icon: RefreshCw, tag: '05' },
    ],
  },
];

export function Navbar() {
  const pathname = usePathname();
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <>
      {/* Mobile Top Bar */}
      <div className="md:hidden fixed top-0 left-0 right-0 z-40 h-14 bg-surface-elevated/95 backdrop-blur border-b border-border-subtle flex items-center justify-between px-4">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-accent-primary text-white flex items-center justify-center font-mono font-bold text-xs shadow-sm">
            AI
          </div>
          <div>
            <span className="font-bold text-sm text-text-primary tracking-tight">AIRS</span>
            <span className="text-[10px] text-text-muted font-mono ml-1.5 px-1 py-0.2 rounded bg-surface-subtle border border-border-subtle">
              v1.0
            </span>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <ThemeToggle />
          <button
            type="button"
            onClick={() => setMobileOpen(!mobileOpen)}
            aria-label="Toggle navigation menu"
            className="p-2 rounded-lg text-text-secondary hover:text-text-primary hover:bg-surface-subtle transition"
          >
            {mobileOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </div>

      {/* Mobile Backdrop */}
      {mobileOpen && (
        <div
          onClick={() => setMobileOpen(false)}
          className="md:hidden fixed inset-0 z-40 bg-black/50 backdrop-blur-sm transition-opacity"
        />
      )}

      {/* Main Sidebar Rail */}
      <aside
        className={cn(
          'fixed md:sticky top-0 left-0 z-50 md:z-30 w-72 h-screen bg-surface-elevated border-r border-border-subtle flex flex-col shrink-0 transition-transform duration-200 ease-out',
          mobileOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'
        )}
      >
        {/* Brand Header */}
        <div className="p-5 border-b border-border-subtle flex items-center justify-between">
          <Link
            href="/"
            onClick={() => setMobileOpen(false)}
            className="flex items-center gap-3 group"
          >
            <div className="w-9 h-9 rounded-lg bg-accent-primary text-white flex items-center justify-center font-mono font-bold text-sm shadow-sm group-hover:scale-95 transition-transform">
              AI
            </div>
            <div>
              <div className="flex items-center gap-1.5">
                <span className="font-bold text-base text-text-primary tracking-tight">AIRS</span>
                <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-accent-primary/10 text-accent-primary border border-accent-primary/20">
                  CONSOLE
                </span>
              </div>
              <p className="text-[11px] text-text-muted font-medium">Artist Intelligence System</p>
            </div>
          </Link>

          <div className="hidden md:flex items-center">
            <ThemeToggle />
          </div>
        </div>

        {/* Navigation Sections */}
        <nav className="flex-1 p-3.5 space-y-6 overflow-y-auto">
          {navSections.map((section, sIdx) => (
            <div key={sIdx} className="space-y-1">
              <div className="px-3 py-1.5 text-[10px] font-mono uppercase tracking-wider text-text-muted font-semibold flex items-center justify-between">
                <span>{section.title}</span>
                <span className="text-[9px] text-text-muted/60">{section.items.length} VIEWS</span>
              </div>

              {section.items.map((item) => {
                const isActive =
                  pathname === item.href ||
                  (item.href !== '/' && pathname.startsWith(item.href));
                const Icon = item.icon;

                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    onClick={() => setMobileOpen(false)}
                    className={cn(
                      'group flex items-center justify-between px-3 py-2.5 rounded-lg text-xs font-medium transition-all duration-150',
                      isActive
                        ? 'bg-accent-primary/10 text-accent-primary font-semibold border border-accent-primary/20 shadow-sm'
                        : 'text-text-secondary hover:text-text-primary hover:bg-surface-subtle border border-transparent'
                    )}
                  >
                    <div className="flex items-center gap-2.5 min-w-0">
                      <Icon
                        className={cn(
                          'w-4 h-4 shrink-0 transition-colors',
                          isActive ? 'text-accent-primary' : 'text-text-muted group-hover:text-text-secondary'
                        )}
                      />
                      <span className="truncate">{item.name}</span>
                    </div>

                    <span
                      className={cn(
                        'font-mono text-[10px] px-1.5 py-0.2 rounded transition-colors',
                        isActive
                          ? 'text-accent-primary bg-accent-primary/10'
                          : 'text-text-muted/60 group-hover:text-text-muted'
                      )}
                    >
                      {item.tag}
                    </span>
                  </Link>
                );
              })}
            </div>
          ))}
        </nav>

        {/* Epistemic Grounding Info Panel */}
        <div className="p-3.5 border-t border-border-subtle bg-surface-subtle/50">
          <div className="p-3 rounded-lg border border-border-subtle bg-surface text-xs space-y-1.5">
            <div className="flex items-center justify-between">
              <span className="flex items-center gap-1.5 font-mono text-[11px] font-semibold text-text-primary">
                <span className="w-1.5 h-1.5 rounded-full bg-accent-emerald animate-pulse" />
                Epistemic Guardrails
              </span>
              <span className="text-[9px] font-mono text-text-muted">ACTIVE</span>
            </div>
            <p className="text-[11px] text-text-muted leading-relaxed">
              Claims <code className="font-mono text-[10px] text-accent-primary">CLAIM</code> strictly isolated from verified media citations <code className="font-mono text-[10px] text-accent-indigo">DEMONSTRATED</code>.
            </p>
          </div>
        </div>
      </aside>
    </>
  );
}
