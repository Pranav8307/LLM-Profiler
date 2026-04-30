export default function AnalyticsPanel({ data }) {
  if (!data) return null;

  return (
    <div className="bg-gray-800 p-5 rounded-xl space-y-4 shadow-lg">
      <h2 className="text-lg font-semibold">Analytics</h2>

      <div className="space-y-2 text-gray-300 text-sm">
        <p>Total Requests: {data.total_requests}</p>
        <p>Avg Latency: {data.avg_latency} ms</p>
        <p>Total Tokens: {data.total_tokens}</p>
        <p>Cache Hit Rate: {data.cache_hit_rate}%</p>
      </div>

      <div className="border-t border-gray-600 pt-3 space-y-2">
        <p className="text-green-400 font-semibold">
          Saved: ${Number(data.cost_saved || 0).toFixed(6)}
        </p>

        <p className="text-red-400">
          Spent: ${Number(data.total_cost || 0).toFixed(6)}
        </p>
      </div>
    </div>
  );
}