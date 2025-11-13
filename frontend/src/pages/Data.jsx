import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const Data = () => {
  // 샘플 데이터
  const sampleData = [
    { name: '1월', 코스피: 2500, 코스닥: 800 },
    { name: '2월', 코스피: 2550, 코스닥: 820 },
    { name: '3월', 코스피: 2600, 코스닥: 850 },
    { name: '4월', 코스피: 2650, 코스닥: 870 },
    { name: '5월', 코스피: 2700, 코스닥: 890 },
  ];

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">데이터 / 지수</h1>
      
      <div className="bg-white p-6 rounded-lg shadow mb-6">
        <h2 className="text-lg font-semibold mb-4">주요 지수</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 className="text-md font-medium mb-2">코스피</h3>
            <p className="text-2xl font-bold text-blue-600">2,700</p>
          </div>
          <div>
            <h3 className="text-md font-medium mb-2">코스닥</h3>
            <p className="text-2xl font-bold text-green-600">890</p>
          </div>
        </div>
      </div>

      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-lg font-semibold mb-4">지수 추이</h2>
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={sampleData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="코스피" stroke="#3b82f6" />
            <Line type="monotone" dataKey="코스닥" stroke="#10b981" />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default Data;

