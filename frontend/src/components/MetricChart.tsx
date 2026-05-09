import { useApi } from '../hooks/useApi';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

interface Reading {
  id: number;
  sensor_id: string;
  value: number;
  timestamp: string;
  location: { lat: number; lon: number };
}

export function MetricChart() {
  const { data, loading, error } = useApi<Reading[]>('/api/v1/sensors/readings');

  if (loading) return <div>Загрузка данных...</div>;
  if (error) return <div className="error">Ошибка: {error}</div>;
  if (!data || data.length === 0) return <div>Нет данных для отображения</div>;

  const chartData = data.map((item) => ({
    timestamp: new Date(item.timestamp).toLocaleString(),
    value: item.value,
  }));

  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart data={chartData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="timestamp" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="value" stroke="#8884d8" activeDot={{ r: 8 }} />
      </LineChart>
    </ResponsiveContainer>
  );
}