import { useState } from "react";
export default function PromptBox({ onSubmit }) {
  const [prompt, setPrompt] = useState("");

  return (
    <div className="space-y-3">
      <textarea
        className="w-full p-3 rounded-lg bg-gray-700 text-white border border-gray-600 focus:outline-none"
        rows={4}
        placeholder="Type your prompt here..."
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
      />

      <button
        onClick={() => onSubmit(prompt)}
        className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg w-full font-semibold"
      >
        Generate
      </button>
    </div>
  );
}