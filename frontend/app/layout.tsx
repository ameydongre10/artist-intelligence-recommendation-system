import './globals.css';
import type { Metadata } from 'next';
import { Navbar } from '@/components/ui/Navbar';
import { ThemeProvider } from '@/components/theme/ThemeProvider';

export const metadata: Metadata = {
  title: 'AIRS — Artist Intelligence & Recommendation Console',
  description: 'Evidence-backed decision intelligence platform for creative artists, evaluating capability dossiers against hirer intent.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <script
          dangerouslySetInnerHTML={{
            __html: `
              (function() {
                try {
                  const stored = localStorage.getItem('airs-theme');
                  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
                  if (stored === 'dark' || (!stored && prefersDark) || stored === 'system') {
                    document.documentElement.classList.add('dark');
                    document.documentElement.classList.remove('light');
                  } else {
                    document.documentElement.classList.add('light');
                    document.documentElement.classList.remove('dark');
                  }
                } catch (e) {}
              })();
            `,
          }}
        />
      </head>
      <body className="bg-background text-text-primary flex min-h-screen antialiased selection:bg-accent-primary/20 selection:text-accent-primary">
        <ThemeProvider>
          <div className="flex w-full min-h-screen">
            <Navbar />
            <main className="flex-1 flex flex-col min-w-0 overflow-y-auto bg-background">
              {children}
            </main>
          </div>
        </ThemeProvider>
      </body>
    </html>
  );
}
