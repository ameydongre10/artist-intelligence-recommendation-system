import { api, ApiError } from '../lib/api';

describe('Frontend API Client', () => {
  beforeEach(() => {
    global.fetch = jest.fn();
  });

  afterEach(() => {
    jest.resetAllMocks();
  });

  test('getHealth returns health payload on 200 OK', async () => {
    const mockHealth = { status: 'healthy', service: 'artist-intelligence-api' };
    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => mockHealth,
    });

    const result = await api.getHealth();
    expect(result).toEqual(mockHealth);
    expect(global.fetch).toHaveBeenCalledTimes(1);
  });

  test('getArtists formats category query parameter correctly', async () => {
    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => [],
    });

    await api.getArtists('photographer');
    expect(global.fetch).toHaveBeenCalledWith(
      expect.stringContaining('/api/artists?category=photographer'),
      expect.anything()
    );
  });

  test('formats custom ApiError on 404 response', async () => {
    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: false,
      status: 404,
      json: async () => ({ detail: 'Artist not found' }),
    });

    await expect(api.getArtistDetail('UNKNOWN_ID')).rejects.toThrow(ApiError);
  });

  test('automatically switches to fallback backend when custom primary fails with network error', async () => {
    const { setActiveApiUrl, FALLBACK_API_URL, getActiveApiUrl } = require('../lib/api');
    setActiveApiUrl('https://custom-unreachable-backend.onrender.com');

    // First attempt against custom backend fails with NetworkError across retries
    (global.fetch as jest.Mock)
      .mockRejectedValueOnce(new TypeError('Failed to fetch'))
      .mockRejectedValueOnce(new TypeError('Failed to fetch'))
      .mockRejectedValueOnce(new TypeError('Failed to fetch'))
      .mockRejectedValueOnce(new TypeError('Failed to fetch'))
      // Then fallback succeeds
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ status: 'healthy', service: 'artist-intelligence-api' }),
      });

    const res = await api.getHealth();
    expect(res.status).toBe('healthy');
    expect(getActiveApiUrl()).toBe(FALLBACK_API_URL);
  }, 15000);
});
