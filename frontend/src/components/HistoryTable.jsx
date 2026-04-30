export default function HistoryTable({ data }) {
  return (
    <div className="bg-gray-800 p-4 rounded-xl">
      <h2 className="font-semibold mb-3">History</h2>

      <table className="w-full text-sm">
        <thead className="text-gray-400 border-b border-gray-600">
          <tr>
            <th className="p-2 text-left">Prompt</th>
            <th className="p-2 text-left">Latency</th>
            <th className="p-2 text-left">Tokens</th>
            <th className="p-2 text-left">Cost</th>
            <th className="p-2 text-left">Cached</th>
          </tr>
        </thead>

        <tbody>
          {data.map((item) => (
            <tr key={item.id} className="border-b border-gray-700 hover:bg-gray-700 transition">
              <td className="p-2">{item.prompt}</td>
              <td className="p-2">{item.latency_ms}</td>
              <td className="p-2">{item.tokens}</td>
              <td className="p-2">
                ${item.cost ? item.cost.toFixed(6) : "0.000000"}
                </td>
              <td className="p-2">
                {item.cached ? "Yes" : "No"}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}