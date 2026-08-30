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
});
