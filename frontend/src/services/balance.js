import api from './api';

export const balanceService = {
  getBalance: async (tradingAccountId) => {
    const response = await api.get('/api/balance', {
      params: { trading_account_id: tradingAccountId }
    });
    return response.data;
  },
};

