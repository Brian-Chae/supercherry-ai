import { useState, useEffect } from 'react';
import api from '../services/api';
import { tradingAccountService } from '../services/tradingAccount';

const Settings = () => {
  const [activeTab, setActiveTab] = useState('strategy');
  
  // 전략 설정 상태
  const [strategy, setStrategy] = useState({
    name: '',
    vwap_period: 1,
    entry_threshold: 0.5,
    exit_threshold: 1.0,
    stop_loss_percent: 2.0,
    take_profit_percent: 3.0,
    max_holding_days: 5,
  });

  // 거래 설정 상태
  const [trading, setTrading] = useState({
    default_order_method: 'MARKET',
    default_quantity: 1,
  });

  // 계정 설정 상태
  const [account, setAccount] = useState({
    account_number: '',
    app_key: '',
    app_secret: '',
  });
  const [tradingAccounts, setTradingAccounts] = useState([]);

  useEffect(() => {
    loadTradingAccounts();
  }, []);

  const loadTradingAccounts = async () => {
    try {
      const accounts = await tradingAccountService.getTradingAccounts();
      setTradingAccounts(accounts);
    } catch (error) {
      console.error('Failed to load trading accounts:', error);
    }
  };

  const handleStrategySave = async () => {
    try {
      await api.post('/api/strategy', strategy);
      alert('전략이 저장되었습니다.');
    } catch (error) {
      alert('저장 실패: ' + (error.response?.data?.detail || error.message));
    }
  };

  const handleAccountSave = async () => {
    try {
      await tradingAccountService.createTradingAccount(account);
      alert('계정이 연결되었습니다.');
      setAccount({
        account_number: '',
        app_key: '',
        app_secret: '',
      });
      loadTradingAccounts(); // 계정 목록 새로고침
    } catch (error) {
      alert('저장 실패: ' + (error.response?.data?.detail || error.message));
    }
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">설정</h1>
      
      <div className="bg-white rounded-lg shadow">
        {/* 탭 메뉴 */}
        <div className="border-b border-gray-200">
          <nav className="flex">
            <button
              onClick={() => setActiveTab('strategy')}
              className={`px-6 py-3 font-medium ${
                activeTab === 'strategy'
                  ? 'border-b-2 border-blue-500 text-blue-600'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              전략 설정
            </button>
            <button
              onClick={() => setActiveTab('trading')}
              className={`px-6 py-3 font-medium ${
                activeTab === 'trading'
                  ? 'border-b-2 border-blue-500 text-blue-600'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              거래 설정
            </button>
            <button
              onClick={() => setActiveTab('account')}
              className={`px-6 py-3 font-medium ${
                activeTab === 'account'
                  ? 'border-b-2 border-blue-500 text-blue-600'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              계정 설정
            </button>
          </nav>
        </div>

        {/* 탭 내용 */}
        <div className="p-6">
          {activeTab === 'strategy' && (
            <div className="space-y-4">
              <h2 className="text-lg font-semibold mb-4">VWAP 전략 설정</h2>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">전략 이름</label>
                <input
                  type="text"
                  value={strategy.name}
                  onChange={(e) => setStrategy({ ...strategy, name: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">VWAP 기간 (일)</label>
                  <input
                    type="number"
                    value={strategy.vwap_period}
                    onChange={(e) => setStrategy({ ...strategy, vwap_period: parseInt(e.target.value) })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">진입 임계값 (%)</label>
                  <input
                    type="number"
                    step="0.1"
                    value={strategy.entry_threshold}
                    onChange={(e) => setStrategy({ ...strategy, entry_threshold: parseFloat(e.target.value) })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">청산 임계값 (%)</label>
                  <input
                    type="number"
                    step="0.1"
                    value={strategy.exit_threshold}
                    onChange={(e) => setStrategy({ ...strategy, exit_threshold: parseFloat(e.target.value) })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">손절매 비율 (%)</label>
                  <input
                    type="number"
                    step="0.1"
                    value={strategy.stop_loss_percent}
                    onChange={(e) => setStrategy({ ...strategy, stop_loss_percent: parseFloat(e.target.value) })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">익절매 비율 (%)</label>
                  <input
                    type="number"
                    step="0.1"
                    value={strategy.take_profit_percent}
                    onChange={(e) => setStrategy({ ...strategy, take_profit_percent: parseFloat(e.target.value) })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">최대 보유 기간 (일)</label>
                  <input
                    type="number"
                    value={strategy.max_holding_days}
                    onChange={(e) => setStrategy({ ...strategy, max_holding_days: parseInt(e.target.value) })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  />
                </div>
              </div>

              <button
                onClick={handleStrategySave}
                className="px-6 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
              >
                저장
              </button>
            </div>
          )}

          {activeTab === 'trading' && (
            <div className="space-y-4">
              <h2 className="text-lg font-semibold mb-4">거래 설정</h2>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">기본 주문 방법</label>
                <select
                  value={trading.default_order_method}
                  onChange={(e) => setTrading({ ...trading, default_order_method: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                >
                  <option value="MARKET">시장가</option>
                  <option value="LIMIT">지정가</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">기본 수량</label>
                <input
                  type="number"
                  value={trading.default_quantity}
                  onChange={(e) => setTrading({ ...trading, default_quantity: parseInt(e.target.value) })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                />
              </div>
            </div>
          )}

          {activeTab === 'account' && (
            <div className="space-y-4">
              <h2 className="text-lg font-semibold mb-4">한국투자증권 계정 연결</h2>
              
              {/* 등록된 계정 목록 */}
              {tradingAccounts.length > 0 && (
                <div className="mb-6">
                  <h3 className="text-md font-medium mb-2">등록된 계정</h3>
                  <div className="space-y-2">
                    {tradingAccounts.map((acc) => (
                      <div key={acc.id} className="p-3 bg-gray-50 rounded-md flex justify-between items-center">
                        <div>
                          <span className="font-medium">{acc.account_number}</span>
                          <span className={`ml-2 text-sm ${acc.is_active ? 'text-green-600' : 'text-gray-500'}`}>
                            {acc.is_active ? '(활성)' : '(비활성)'}
                          </span>
                        </div>
                        <span className="text-sm text-gray-500">
                          {new Date(acc.created_at).toLocaleDateString()}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              <div className="border-t pt-4">
                <h3 className="text-md font-medium mb-4">새 계정 추가</h3>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">계좌번호</label>
                  <input
                    type="text"
                    value={account.account_number}
                    onChange={(e) => setAccount({ ...account, account_number: e.target.value })}
                    placeholder="예: 12345678-01"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">APP_KEY</label>
                  <input
                    type="text"
                    value={account.app_key}
                    onChange={(e) => setAccount({ ...account, app_key: e.target.value })}
                    placeholder="한국투자증권 API App Key"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">APP_SECRET</label>
                  <input
                    type="password"
                    value={account.app_secret}
                    onChange={(e) => setAccount({ ...account, app_secret: e.target.value })}
                    placeholder="한국투자증권 API App Secret"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  />
                </div>

                <button
                  onClick={handleAccountSave}
                  disabled={!account.account_number || !account.app_key || !account.app_secret}
                  className="mt-4 px-6 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed"
                >
                  계정 추가
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Settings;

