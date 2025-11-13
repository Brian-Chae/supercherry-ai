import { useState, useEffect } from 'react';
import api from '../services/api';

const News = () => {
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(false);
  const [symbol, setSymbol] = useState('');

  const handleLoad = async () => {
    setLoading(true);
    try {
      const response = await api.get('/api/news', {
        params: symbol ? { symbol } : {},
      });
      setNews(Array.isArray(response.data) ? response.data : []);
    } catch (error) {
      console.error('Failed to fetch news:', error);
      setNews([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    handleLoad();
  }, []);

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">뉴스</h1>
      
      <div className="bg-white p-6 rounded-lg shadow mb-6">
        <div className="flex gap-4">
          <input
            type="text"
            value={symbol}
            onChange={(e) => setSymbol(e.target.value)}
            placeholder="종목코드 필터 (선택사항)"
            className="flex-1 px-4 py-2 border border-gray-300 rounded-md"
          />
          <button
            onClick={handleLoad}
            disabled={loading}
            className="px-6 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 disabled:bg-gray-400"
          >
            {loading ? '조회 중...' : '조회'}
          </button>
        </div>
      </div>

      <div className="space-y-4">
        {news.length === 0 && !loading && (
          <div className="bg-white p-6 rounded-lg shadow text-center text-gray-500">
            뉴스가 없습니다.
          </div>
        )}
        
        {news.map((item, index) => (
          <div key={index} className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-lg font-semibold mb-2">{item.title || '제목 없음'}</h3>
            <p className="text-gray-600 mb-2">{item.content || item.description || ''}</p>
            <p className="text-sm text-gray-400">{item.date || item.published_at || ''}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default News;

