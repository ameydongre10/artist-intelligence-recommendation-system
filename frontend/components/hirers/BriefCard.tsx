'use client';

import Link from 'next/link';
import { FileText, ArrowRight, MessageSquare, Mail, Phone, Clock, MapPin } from 'lucide-react';
import { HirerBriefSummary } from '@/lib/types';
import { formatCategoryName } from '@/lib/utils';
import { Badge } from '@/components/ui/Badge';

interface BriefCardProps {
  brief: HirerBriefSummary;
}

export function BriefCard({ brief }: BriefCardProps) {
  const getChannelIcon = () => {
    switch (brief.channel) {
      case 'whatsapp':
      case 'chat':
        return <MessageSquare className="w-3.5 h-3.5 text-accent-emerald" />;
      case 'email':
        return <Mail className="w-3.5 h-3.5 text-accent-primary" />;
      case 'phone_notes':
        return <Phone className="w-3.5 h-3.5 text-accent-indigo" />;
      default:
        return <FileText className="w-3.5 h-3.5 text-text-muted" />;
    }
  };

  return (
    <Link
      href={`/hirers/${brief.brief_id}`}
      className="group block p-6 rounded-xl bg-surface border border-border-subtle hover:border-accent-indigo/40 hover:bg-surface-subtle/40 transition-all flex flex-col justify-between overflow-hidden shadow-sm"
    >
      <div className="space-y-4">
        <div className="flex items-start justify-between gap-3">
          <div className="min-w-0 flex-1">
            <div className="flex items-center gap-2 flex-wrap">
              <span className="font-mono text-xs font-bold text-accent-indigo shrink-0">
                {brief.brief_id}
              </span>
              <span className="flex items-center gap-1 text-[11px] font-mono text-text-muted capitalize px-2 py-0.5 rounded bg-surface-subtle border border-border-subtle shrink-0">
                {getChannelIcon()} {brief.channel.replace(/_/g, ' ')}
              </span>
            </div>
            <h3 className="font-bold text-base md:text-lg text-text-primary group-hover:text-accent-indigo transition-colors mt-2 line-clamp-1">
              {brief.hirer_name} &bull; <span className="text-text-secondary font-medium">{formatCategoryName(brief.target_category)}</span>
            </h3>
          </div>

          <Badge variant="indigo" size="sm" className="shrink-0">
            {formatCategoryName(brief.target_category)}
          </Badge>
        </div>

        <p className="text-xs text-text-secondary line-clamp-2 leading-relaxed">
          {brief.situation}
        </p>

        {/* Operational Constraints Context */}
        <div className="pt-3 border-t border-border-subtle/80 space-y-1.5 text-xs text-text-muted font-mono">
          <div className="flex items-center gap-2 min-w-0">
            <Clock className="w-3.5 h-3.5 text-text-muted shrink-0" />
            <span className="truncate">{brief.timeline}</span>
          </div>
          <div className="flex items-center gap-2 min-w-0">
            <MapPin className="w-3.5 h-3.5 text-text-muted shrink-0" />
            <span className="truncate">{brief.location}</span>
          </div>
        </div>

        {/* Epistemic Requirements Count Strip */}
        <div className="grid grid-cols-4 gap-2 pt-3 border-t border-border-subtle/80 text-center">
          <div className="p-1.5 rounded-lg bg-surface-subtle border border-border-subtle/60 min-w-0">
            <div className="text-xs font-bold text-accent-primary font-mono">
              {brief.known_requirements_count}
            </div>
            <div className="text-[10px] text-text-muted mt-0.5 truncate">Known</div>
          </div>
          <div className="p-1.5 rounded-lg bg-surface-subtle border border-border-subtle/60 min-w-0">
            <div className="text-xs font-bold text-accent-rose font-mono">
              {brief.hard_constraints_count}
            </div>
            <div className="text-[10px] text-text-muted mt-0.5 truncate">Limits</div>
          </div>
          <div className="p-1.5 rounded-lg bg-surface-subtle border border-border-subtle/60 min-w-0">
            <div className="text-xs font-bold text-text-muted font-mono">
              {brief.unknowns_count}
            </div>
            <div className="text-[10px] text-text-muted mt-0.5 truncate">Unknown</div>
          </div>
          <div className="p-1.5 rounded-lg bg-surface-subtle border border-border-subtle/60 min-w-0">
            <div className="text-xs font-bold text-accent-amber font-mono">
              {brief.contradictions_count}
            </div>
            <div className="text-[10px] text-text-muted mt-0.5 truncate">Conflicts</div>
          </div>
        </div>
      </div>

      <div className="mt-4 pt-3 border-t border-border-subtle/60 flex items-center justify-between text-xs text-text-muted group-hover:text-text-primary transition-colors font-medium">
        <span>Inspect Requirements Dossier</span>
        <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-0.5 transition-transform" />
      </div>
    </Link>
  );
}
