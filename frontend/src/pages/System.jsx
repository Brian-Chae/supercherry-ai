import { useState, useEffect } from 'react';
import api from '../services/api';

const System = () => {
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadStatus = async () => {
      try {
        const response = await api.get('/api/system/status');
        setStatus(response.data);
      } catch (error) {
        console.error('Failed to fetch system status:', error);
      } finally {
        setLoading(false);
      }
    };

    loadStatus();
  }, []);

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">시스템</h1>
      
      {loading ? (
        <div className="bg-white p-6 rounded-lg shadow text-center">로딩 중...</div>
      ) : status ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-lg font-semibold mb-2">API 연결 상태</h3>
            <p className={`text-2xl font-bold ${status.api_status === 'connected' ? 'text-green-600' : 'text-red-600'}`}>
              {status.api_status === 'connected' ? '연결됨' : '연결 안됨'}
            </p>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-lg font-semibold mb-2">활성 계정 수</h3>
            <p className="text-2xl font-bold">{status.active_accounts}</p>
          </div>
        </div>
      ) : (
        <div className="bg-white p-6 rounded-lg shadow text-center text-gray-500">
          상태 정보를 불러올 수 없습니다.
        </div>
      )}
    </div>
  );
};

export default System;

