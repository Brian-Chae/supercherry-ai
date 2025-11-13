import api from './api';

export const marketService = {
  getCurrentPrice: async (symbol, marketCode = 'J') => {
    const response = await api.get(`/api/market/current-price/${symbol}`, {
      params: { market_code: marketCode }
    });
    return response.data;
  },
};

