import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

export default function Charts({ data }) {
  if (!data || data.length === 0) return null;

  const chartData = data.map((item, index) => ({
    name: index + 1,
    latency: item.latency_ms,
    cost: Number(item.cost || 0),
  }));

  return (
    <div className="bg-gray-800 p-4 rounded-xl">
      <h2 className="mb-3 font-semibold">Performance Trends</h2>

      <ResponsiveContainer width="100%" height={250}>
        <LineChart data={chartData}>
          <XAxis dataKey="name" stroke="#aaa" />
          <YAxis stroke="#aaa" />
          <Tooltip />
          <Line type="monotone" dataKey="latency" />
          <Line type="monotone" dataKey="cost" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}