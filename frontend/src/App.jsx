import { useState, useEffect } from "react";
import { generate, getHistory, getAnalytics } from "./api";
import PromptBox from "./components/PromptBox";
import MetricsCards from "./components/MetricsCards";
import HistoryTable from "./components/HistoryTable";
import AnalyticsPanel from "./components/AnalyticsPanel";
import Charts from "./components/Charts";

export default function App() {
  const [response, setResponse] = useState(null);
  const [history, setHistory] = useState([]);
  const [analytics, setAnalytics] = useState(null);

  const fetchData = async () => {
    const h = await getHistory();
    const a = await getAnalytics();
    setHistory(h.data);
    setAnalytics(a.data);
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleGenerate = async (prompt) => {
    const res = await generate({ prompt, user_id: "test" });
    setResponse(res.data);
    fetchData();
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <h1 className="text-3xl font-bold mb-6">LLM Profiler</h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

        {/* LEFT */}
        <div className="lg:col-span-2 space-y-6">

          <div className="bg-gradient-to-r from-blue-500 to-purple-600 hover:opacity-90 px-4 py-2 rounded-lg w-full font-semibold">
            <h2 className="font-semibold mb-2">Generate</h2>
            <PromptBox onSubmit={handleGenerate} />
          </div>

          {response && (
            <div className="bg-gray-800 p-5 rounded-xl shadow-lg">
              <h2 className="font-semibold mb-3">Response</h2>
              <p className="text-gray-300 leading-relaxed whitespace-pre-wrap">
                {response.answer}
              </p>
            </div>
          )}

          <HistoryTable data={history} />
          <Charts data={history} />
        </div>

        {/* RIGHT */}
        <div className="space-y-6">

          {response && <MetricsCards data={response} />}

          <AnalyticsPanel data={analytics} />

        </div>

      </div>
    </div>
  );
}