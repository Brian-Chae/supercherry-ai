import api from './api';

export const tradingAccountService = {
  getTradingAccounts: async () => {
    const response = await api.get('/api/trading-account');
    return response.data;
  },

  createTradingAccount: async (accountData) => {
    const response = await api.post('/api/trading-account', accountData);
    return response.data;
  },

  getTradingAccount: async (accountId) => {
    const response = await api.get(`/api/trading-account/${accountId}`);
    return response.data;
  },
};

