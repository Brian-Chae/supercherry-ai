import { useState, useEffect } from 'react';
import { tradingAccountService } from '../services/tradingAccount';
import { balanceService } from '../services/balance';
import { orderService } from '../services/order';

const Dashboard = () => {
  const [tradingAccounts, setTradingAccounts] = useState([]);
  const [totalAssets, setTotalAssets] = useState(0);
  const [profitLoss, setProfitLoss] = useState(0);
  const [holdingCount, setHoldingCount] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    setLoading(true);
    try {
      const accounts = await tradingAccountService.getTradingAccounts();
      setTradingAccounts(accounts);

      // 모든 계정의 잔고 합산
      let totalValue = 0;
      let totalProfitLoss = 0;
      let totalHoldings = 0;

      for (const account of accounts.filter(acc => acc.is_active)) {
        try {
          const balances = await balanceService.getBalance(account.id);
          totalHoldings += balances.length;
          balances.forEach(balance => {
            if (balance.total_value) totalValue += balance.total_value;
            if (balance.profit_loss) totalProfitLoss += balance.profit_loss;
          });
        } catch (error) {
          console.error(`Failed to load balance for account ${account.id}:`, error);
        }
      }

      setTotalAssets(totalValue);
      setProfitLoss(totalProfitLoss);
      setHoldingCount(totalHoldings);
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const profitRate = totalAssets > 0 ? (profitLoss / (totalAssets - profitLoss)) * 100 : 0;

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">대시보드</h1>
        <button
          onClick={loadDashboardData}
          disabled={loading}
          className="px-4 py-2 bg-gray-500 text-white rounded-md hover:bg-gray-600 disabled:bg-gray-400"
        >
          {loading ? '새로고침 중...' : '새로고침'}
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold mb-2">총 자산</h3>
          <p className="text-3xl font-bold text-blue-600">
            {loading ? '...' : totalAssets.toLocaleString() + '원'}
          </p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold mb-2">손익</h3>
          <p className={`text-3xl font-bold ${profitLoss >= 0 ? 'text-red-600' : 'text-blue-600'}`}>
            {loading ? '...' : (profitLoss >= 0 ? '+' : '') + profitLoss.toLocaleString() + '원'}
          </p>
          <p className={`text-sm mt-2 ${profitRate >= 0 ? 'text-red-600' : 'text-blue-600'}`}>
            {loading ? '' : (profitRate >= 0 ? '+' : '') + profitRate.toFixed(2) + '%'}
          </p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold mb-2">보유 종목</h3>
          <p className="text-3xl font-bold">{loading ? '...' : holdingCount}</p>
        </div>
      </div>

      {/* 거래 계정 목록 */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-xl font-semibold mb-4">거래 계정</h2>
        {tradingAccounts.length > 0 ? (
          <div className="space-y-2">
            {tradingAccounts.map((account) => (
              <div key={account.id} className="p-3 bg-gray-50 rounded-md flex justify-between items-center">
                <div>
                  <span className="font-medium">{account.account_number}</span>
                  <span className={`ml-2 text-sm ${account.is_active ? 'text-green-600' : 'text-gray-500'}`}>
                    {account.is_active ? '(활성)' : '(비활성)'}
                  </span>
                </div>
                <span className="text-sm text-gray-500">
                  등록일: {new Date(account.created_at).toLocaleDateString()}
                </span>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-500">거래 계정이 없습니다. 설정에서 계정을 등록하세요.</p>
        )}
      </div>
    </div>
  );
};

export default Dashboard;

