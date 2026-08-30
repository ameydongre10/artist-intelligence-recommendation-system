'use client';

import { useEffect, useState } from 'react';

interface CountUpNumberProps {
  end: number;
  duration?: number;
  suffix?: string;
  prefix?: string;
  className?: string;
}

export function CountUpNumber({
  end,
  duration = 800,
  suffix = '',
  prefix = '',
  className = '',
}: CountUpNumberProps) {
  const [count, setCount] = useState<number>(0);

  useEffect(() => {
    // Check for prefers-reduced-motion safely
    if (typeof window !== 'undefined' && typeof window.matchMedia === 'function') {
      const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      if (prefersReducedMotion) {
        setCount(end);
        return;
      }
    }

    if (duration <= 0) {
      setCount(end);
      return;
    }

    let start = 0;
    const steps = 30;
    const stepTime = Math.max(16, Math.floor(duration / steps));
    const increment = end / steps;

    const timer = setInterval(() => {
      start += increment;
      if (start >= end) {
        setCount(end);
        clearInterval(timer);
      } else {
        setCount(Math.floor(start));
      }
    }, stepTime);

    return () => clearInterval(timer);
  }, [end, duration]);

  return (
    <span className={className}>
      {prefix}
      {count}
      {suffix}
    </span>
  );
}
