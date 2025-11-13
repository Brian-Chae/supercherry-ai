import { useState } from 'react';
import { marketService } from '../services/market';

const Market = () => {
  const [symbol, setSymbol] = useState('');
  const [price, setPrice] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!symbol) return;
    
    setLoading(true);
    try {
      const data = await marketService.getCurrentPrice(symbol);
      setPrice(data);
    } catch (error) {
      console.error('Failed to fetch price:', error);
      alert('현재가 조회 실패: ' + (error.response?.data?.detail || error.message));
      setPrice(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">현재가</h1>
      
      <div className="bg-white p-6 rounded-lg shadow mb-6">
        <div className="flex gap-4">
          <input
            type="text"
            value={symbol}
            onChange={(e) => setSymbol(e.target.value)}
            placeholder="종목코드 입력 (예: 005930)"
            className="flex-1 px-4 py-2 border border-gray-300 rounded-md"
          />
          <button
            onClick={handleSearch}
            disabled={loading}
            className="px-6 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 disabled:bg-gray-400"
          >
            {loading ? '조회 중...' : '조회'}
          </button>
        </div>
      </div>

      {price && (
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">가격 정보</h2>
          <pre className="bg-gray-100 p-4 rounded overflow-auto">
            {JSON.stringify(price, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
};

export default Market;

