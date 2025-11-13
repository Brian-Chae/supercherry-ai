import { useState, useEffect } from 'react';
import { balanceService } from '../services/balance';
import { tradingAccountService } from '../services/tradingAccount';

const Balance = () => {
  const [tradingAccountId, setTradingAccountId] = useState('');
  const [balances, setBalances] = useState([]);
  const [loading, setLoading] = useState(false);
  const [tradingAccounts, setTradingAccounts] = useState([]);

  useEffect(() => {
    loadTradingAccounts();
  }, []);

  const loadTradingAccounts = async () => {
    try {
      const accounts = await tradingAccountService.getTradingAccounts();
      setTradingAccounts(accounts);
      if (accounts.length > 0 && !tradingAccountId) {
        setTradingAccountId(accounts[0].id);
        handleLoad(accounts[0].id);
      }
    } catch (error) {
      console.error('Failed to load trading accounts:', error);
    }
  };

  const handleLoad = async (accountId = null) => {
    const id = accountId || tradingAccountId;
    if (!id) return;
    
    setLoading(true);
    try {
      const data = await balanceService.getBalance(id);
      setBalances(data);
    } catch (error) {
      console.error('Failed to fetch balance:', error);
      alert('잔고 조회 실패: ' + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">잔고</h1>
      
      <div className="bg-white p-6 rounded-lg shadow mb-6">
        <div className="flex gap-4">
          <select
            value={tradingAccountId}
            onChange={(e) => {
              setTradingAccountId(e.target.value);
              if (e.target.value) {
                handleLoad(e.target.value);
              }
            }}
            className="flex-1 px-4 py-2 border border-gray-300 rounded-md"
          >
            <option value="">거래 계정 선택</option>
            {tradingAccounts.map((account) => (
              <option key={account.id} value={account.id}>
                {account.account_number} {account.is_active ? '(활성)' : '(비활성)'}
              </option>
            ))}
          </select>
          <button
            onClick={() => handleLoad()}
            disabled={loading || !tradingAccountId}
            className="px-6 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 disabled:bg-gray-400"
          >
            {loading ? '조회 중...' : '조회'}
          </button>
        </div>
        {tradingAccounts.length === 0 && (
          <p className="text-sm text-gray-500 mt-2">거래 계정이 없습니다. 설정에서 계정을 등록하세요.</p>
        )}
      </div>

      {balances.length > 0 && (
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">종목코드</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">수량</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">평균가</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">현재가</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">평가금액</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">손익</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">수익률</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {balances.map((balance) => (
                <tr key={balance.id}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">{balance.symbol}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">{balance.quantity}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">{balance.average_price?.toLocaleString()}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">{balance.current_price?.toLocaleString()}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">{balance.total_value?.toLocaleString()}</td>
                  <td className={`px-6 py-4 whitespace-nowrap text-sm ${balance.profit_loss >= 0 ? 'text-red-600' : 'text-blue-600'}`}>
                    {balance.profit_loss?.toLocaleString()}
                  </td>
                  <td className={`px-6 py-4 whitespace-nowrap text-sm ${balance.profit_loss_rate >= 0 ? 'text-red-600' : 'text-blue-600'}`}>
                    {balance.profit_loss_rate?.toFixed(2)}%
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default Balance;

