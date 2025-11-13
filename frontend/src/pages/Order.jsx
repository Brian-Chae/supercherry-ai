import { useState, useEffect } from 'react';
import { orderService } from '../services/order';
import { tradingAccountService } from '../services/tradingAccount';

const Order = () => {
  const [formData, setFormData] = useState({
    trading_account_id: '',
    symbol: '',
    order_type: 'BUY',
    order_method: 'MARKET',
    quantity: '',
    price: '',
  });
  const [loading, setLoading] = useState(false);
  const [tradingAccounts, setTradingAccounts] = useState([]);
  const [orders, setOrders] = useState([]);
  const [loadingOrders, setLoadingOrders] = useState(false);

  useEffect(() => {
    loadTradingAccounts();
    loadOrders();
  }, []);

  const loadTradingAccounts = async () => {
    try {
      const accounts = await tradingAccountService.getTradingAccounts();
      setTradingAccounts(accounts);
      if (accounts.length > 0 && !formData.trading_account_id) {
        setFormData({ ...formData, trading_account_id: accounts[0].id });
      }
    } catch (error) {
      console.error('Failed to load trading accounts:', error);
    }
  };

  const loadOrders = async () => {
    setLoadingOrders(true);
    try {
      const orderList = await orderService.getOrders();
      setOrders(orderList);
    } catch (error) {
      console.error('Failed to load orders:', error);
    } finally {
      setLoadingOrders(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      await orderService.createOrder({
        ...formData,
        quantity: parseInt(formData.quantity),
        price: formData.price ? parseFloat(formData.price) : null,
      });
      alert('주문이 접수되었습니다.');
      setFormData({
        ...formData,
        symbol: '',
        quantity: '',
        price: '',
      });
      loadOrders(); // 주문 목록 새로고침
    } catch (error) {
      alert('주문 실패: ' + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">주문</h1>
      
      <div className="bg-white p-6 rounded-lg shadow">
        <form onSubmit={handleSubmit}>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                거래 계정
              </label>
              <select
                value={formData.trading_account_id}
                onChange={(e) => setFormData({ ...formData, trading_account_id: e.target.value })}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md"
              >
                <option value="">선택하세요</option>
                {tradingAccounts.map((account) => (
                  <option key={account.id} value={account.id}>
                    {account.account_number} {account.is_active ? '(활성)' : '(비활성)'}
                  </option>
                ))}
              </select>
              {tradingAccounts.length === 0 && (
                <p className="text-sm text-gray-500 mt-1">거래 계정이 없습니다. 설정에서 계정을 등록하세요.</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                종목코드
              </label>
              <input
                type="text"
                value={formData.symbol}
                onChange={(e) => setFormData({ ...formData, symbol: e.target.value })}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                주문 유형
              </label>
              <select
                value={formData.order_type}
                onChange={(e) => setFormData({ ...formData, order_type: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md"
              >
                <option value="BUY">매수</option>
                <option value="SELL">매도</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                주문 방법
              </label>
              <select
                value={formData.order_method}
                onChange={(e) => setFormData({ ...formData, order_method: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md"
              >
                <option value="MARKET">시장가</option>
                <option value="LIMIT">지정가</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                수량
              </label>
              <input
                type="number"
                value={formData.quantity}
                onChange={(e) => setFormData({ ...formData, quantity: e.target.value })}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md"
              />
            </div>

            {formData.order_method === 'LIMIT' && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  가격
                </label>
                <input
                  type="number"
                  value={formData.price}
                  onChange={(e) => setFormData({ ...formData, price: e.target.value })}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                />
              </div>
            )}
          </div>

          <div className="mt-6">
            <button
              type="submit"
              disabled={loading}
              className="w-full px-6 py-3 bg-blue-500 text-white rounded-md hover:bg-blue-600 disabled:bg-gray-400"
            >
              {loading ? '주문 중...' : '주문하기'}
            </button>
          </div>
        </form>
      </div>

      {/* 주문 내역 */}
      <div className="mt-8 bg-white p-6 rounded-lg shadow">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold">주문 내역</h2>
          <button
            onClick={loadOrders}
            disabled={loadingOrders}
            className="px-4 py-2 bg-gray-500 text-white rounded-md hover:bg-gray-600 disabled:bg-gray-400"
          >
            {loadingOrders ? '새로고침 중...' : '새로고침'}
          </button>
        </div>

        {orders.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">시간</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">종목</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">유형</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">방법</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">수량</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">가격</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">상태</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {orders.map((order) => (
                  <tr key={order.id}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      {new Date(order.created_at).toLocaleString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">{order.symbol}</td>
                    <td className={`px-6 py-4 whitespace-nowrap text-sm ${order.order_type === 'BUY' ? 'text-blue-600' : 'text-red-600'}`}>
                      {order.order_type === 'BUY' ? '매수' : '매도'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">{order.order_method}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">{order.quantity}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">{order.price?.toLocaleString() || '-'}</td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 py-1 text-xs rounded ${
                        order.status === 'EXECUTED' ? 'bg-green-100 text-green-800' :
                        order.status === 'PENDING' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-red-100 text-red-800'
                      }`}>
                        {order.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p className="text-gray-500 text-center py-8">주문 내역이 없습니다.</p>
        )}
      </div>
    </div>
  );
};

export default Order;

