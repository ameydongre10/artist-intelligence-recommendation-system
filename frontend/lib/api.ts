/**
 * API Client with Cold-Start Resilience, Retries, and Error Formatting.
 */

import {
  SystemStatus,
  DatasetSummary,
  ArtistSummary,
  ArtistDetail,
  HirerBriefSummary,
  HirerBriefDetail,
  RecommendationSummary,
  RecommendationDetail,
  ReRankingResult,
} from './types';

const API_BASE_URL = (
  process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000'
).replace(/\/+$/, '');

export class ApiError extends Error {
  status: number;
  isColdStart: boolean;

  constructor(message: string, status: number = 500, isColdStart: boolean = false) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.isColdStart = isColdStart;
  }
}

async function fetchWithRetry<T>(
  endpoint: string,
  options: RequestInit = {},
  retries: number = 3,
  backoffMs: number = 1000
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;

  for (let attempt = 0; attempt <= retries; attempt++) {
    try {
      const res = await fetch(url, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
      });

      if (!res.ok) {
        let errorDetail = `Request failed with status ${res.status}`;
        try {
          const errJson = await res.json();
          errorDetail = errJson.detail || errJson.error || errorDetail;
        } catch {
          // ignore non-json response
        }
        throw new ApiError(errorDetail, res.status, false);
      }

      return (await res.json()) as T;
    } catch (err: any) {
      const isLastAttempt = attempt === retries;
      const isNetworkError =
        err.name === 'TypeError' ||
        err.message?.includes('fetch') ||
        err.message?.includes('NetworkError') ||
        err.message?.includes('Failed to fetch');

      if (isNetworkError && !isLastAttempt) {
        // Sleep with exponential backoff for backend cold start
        await new Promise((resolve) => setTimeout(resolve, backoffMs * Math.pow(2, attempt)));
        continue;
      }

      if (isLastAttempt && isNetworkError) {
        throw new ApiError(
          'The intelligence service is starting or temporarily unreachable. Please check your backend connection.',
          503,
          true
        );
      }

      if (err instanceof ApiError) {
        throw err;
      }

      throw new ApiError(err.message || 'An unexpected error occurred', 500);
    }
  }

  throw new ApiError('Maximum retry attempts exceeded', 500);
}

export const api = {
  getHealth: () => fetchWithRetry<{ status: string; service: string }>('/api/health'),

  getSystemStatus: () => fetchWithRetry<SystemStatus>('/api/system/status'),

  getDatasetSummary: () => fetchWithRetry<DatasetSummary>('/api/dataset/summary'),

  getArtists: (category?: string) => {
    const query = category && category !== 'all' ? `?category=${encodeURIComponent(category)}` : '';
    return fetchWithRetry<ArtistSummary[]>(`/api/artists${query}`);
  },

  getArtistDetail: (artistId: string) =>
    fetchWithRetry<ArtistDetail>(`/api/artists/${encodeURIComponent(artistId)}`),

  getHirerBriefs: () => fetchWithRetry<HirerBriefSummary[]>('/api/hirer-briefs'),

  getHirerBriefDetail: (briefId: string) =>
    fetchWithRetry<HirerBriefDetail>(`/api/hirer-briefs/${encodeURIComponent(briefId)}`),

  getRecommendations: () => fetchWithRetry<RecommendationSummary[]>('/api/recommendations'),

  getRecommendationDetail: (briefId: string) =>
    fetchWithRetry<RecommendationDetail>(`/api/recommendations/${encodeURIComponent(briefId)}`),

  getUpdatedRecommendation: (briefId: string) =>
    fetchWithRetry<ReRankingResult>(`/api/recommendations/${encodeURIComponent(briefId)}/updated`),
};
