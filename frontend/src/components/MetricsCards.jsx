export default function MetricsCards({ data }) {
  if (!data) return null;

  return (
    <div className="grid grid-cols-2 gap-4">
      <Card title="Latency" value={`${data.latency_ms ?? 0} ms`} />
      <Card title="Tokens" value={data.tokens ?? 0} />
      <Card
        title="Cost"
        value={`$${data.cost ? data.cost.toFixed(6) : "0.000000"}`}
      />
      <Card title="Cached" value={data.cached ? "Yes" : "No"} />
    </div>
  );
}

function Card({ title, value }) {
  return (
    <div className="bg-gray-800 p-4 rounded-xl text-center hover:scale-[1.02] transition">
      <p className="text-gray-400">{title}</p>
      <p className="text-xl font-bold">{value}</p>
    </div>
  );
}