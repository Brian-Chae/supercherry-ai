import api from './api';

export const orderService = {
  createOrder: async (orderData) => {
    const response = await api.post('/api/order', orderData);
    return response.data;
  },

  getOrders: async (skip = 0, limit = 100) => {
    const response = await api.get('/api/order', {
      params: { skip, limit }
    });
    return response.data;
  },
};

