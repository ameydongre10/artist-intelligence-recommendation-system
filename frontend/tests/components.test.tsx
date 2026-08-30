import React from 'react';
import { render, screen } from '@testing-library/react';
import { Badge } from '../components/ui/Badge';
import { LoadingState } from '../components/ui/LoadingState';
import { ErrorState } from '../components/ui/ErrorState';
import { TopTwoComparison } from '../components/recommendations/TopTwoComparison';
import { AnomalyList } from '../components/dashboard/AnomalyList';
import { CountUpNumber } from '../components/ui/CountUpNumber';
import { CandidateRecommendation, DetectedAnomalyGroup } from '../lib/types';

describe('Frontend UI Components', () => {
  test('renders Badge component with text and styling', () => {
    render(<Badge variant="emerald">VERIFIED</Badge>);
    expect(screen.getByText('VERIFIED')).toBeInTheDocument();
  });

  test('renders LoadingState with custom message', () => {
    render(<LoadingState message="Loading intelligence dossiers..." isColdStart={true} />);
    expect(screen.getByText('Loading intelligence dossiers...')).toBeInTheDocument();
    expect(screen.getByText(/intelligence service is warming up/i)).toBeInTheDocument();
  });

  test('renders ErrorState with retry button', () => {
    const handleRetry = jest.fn();
    render(<ErrorState title="Connection Error" message="Backend unavailable" onRetry={handleRetry} />);
    expect(screen.getByText('Connection Error')).toBeInTheDocument();
    expect(screen.getByText('Backend unavailable')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /retry/i })).toBeInTheDocument();
  });

  test('renders TopTwoComparison with Rank 1 and Rank 2 details', () => {
    const mockRank1: CandidateRecommendation = {
      rank: 1,
      artist_id: 'M01',
      artist_name: 'Meera & Arjun',
      category: 'musician',
      fit_reason: 'Demonstrated acoustic cafe demo take with vocal harmonies.',
      matched_requirements: [],
      supporting_evidence: [],
      confidence: 'HIGH',
      trade_offs: [],
      uncertainty_and_limitations: [],
    };

    const mockRank2: CandidateRecommendation = {
      rank: 2,
      artist_id: 'M03',
      artist_name: 'Raghav Sen',
      category: 'musician',
      fit_reason: 'Solo acoustic fingerpicking.',
      matched_requirements: [],
      supporting_evidence: [],
      confidence: 'HIGH',
      trade_offs: [],
      uncertainty_and_limitations: [],
    };

    render(<TopTwoComparison topTwo={[mockRank1, mockRank2]} />);
    expect(screen.getByText('Meera & Arjun')).toBeInTheDocument();
    expect(screen.getByText('Raghav Sen')).toBeInTheDocument();
    expect(screen.getByText(/RANK #1 PRIMARY/i)).toBeInTheDocument();
    expect(screen.getByText(/RANK #2 RUNNER-UP/i)).toBeInTheDocument();
  });

  test('renders AnomalyList safely with anomaly groups', () => {
    const mockAnomalies: DetectedAnomalyGroup[] = [
      {
        artist_folder: 'PO4_Drift',
        category: 'photographers',
        anomalies: ["Folder uses letter 'O' instead of digit '0'"],
      },
    ];

    render(<AnomalyList anomalies={mockAnomalies} />);
    expect(screen.getByText('PO4_Drift')).toBeInTheDocument();
    expect(screen.getByText("Folder uses letter 'O' instead of digit '0'")).toBeInTheDocument();
  });

  test('renders CountUpNumber component with prefix and suffix', () => {
    render(<CountUpNumber end={15} prefix="Total: " suffix=" Artists" duration={0} />);
    expect(screen.getByText(/Total: 15 Artists/i)).toBeInTheDocument();
  });
});
