"use client";

import { useState } from "react";
import { askAssistant } from "@/lib/api";

export default function Home() {
  const [form, setForm] = useState({
    provider: "groq",
    api_key: "",
    mode: "sql",
    language: "sql",
    input: "",
  });

  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async () => {
    setLoading(true);
    setError("");
    setResponse("");

    try {
      const data = await askAssistant(form);
      setResponse(data.response);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-zinc-950 text-white p-10">
      <h1 className="text-3xl font-semibold mb-6">
        AI Code Review Assistant
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Left Panel */}
        <div className="space-y-4">
          <input
            placeholder="API Key"
            type="password"
            className="w-full p-2 bg-zinc-900 border border-zinc-700 rounded"
            onChange={(e) =>
              setForm({ ...form, api_key: e.target.value })
            }
          />

          <select
            className="w-full p-2 bg-zinc-900 border border-zinc-700 rounded"
            onChange={(e) =>
              setForm({ ...form, provider: e.target.value })
            }
          >
            <option value="groq">Groq</option>
            <option value="openai">OpenAI</option>
            <option value="gemini">Gemini</option>
          </select>

          <select
            className="w-full p-2 bg-zinc-900 border border-zinc-700 rounded"
            onChange={(e) =>
              setForm({ ...form, mode: e.target.value })
            }
          >
            <option value="review">Code Review</option>
            <option value="explain">Explain Code</option>
            <option value="generate">Generate Code</option>
            <option value="sql">SQL Assistant</option>
          </select>

          <input
            placeholder="Language (python, java, sql, js...)"
            className="w-full p-2 bg-zinc-900 border border-zinc-700 rounded"
            onChange={(e) =>
              setForm({ ...form, language: e.target.value })
            }
          />

          <textarea
            placeholder="Enter code or requirement..."
            rows={10}
            className="w-full p-2 bg-zinc-900 border border-zinc-700 rounded"
            onChange={(e) =>
              setForm({ ...form, input: e.target.value })
            }
          />

          <button
            onClick={handleSubmit}
            disabled={loading}
            className={`w-full p-2 rounded font-medium ${
              loading
                ? "bg-zinc-700 cursor-not-allowed"
                : "bg-blue-600 hover:bg-blue-700"
            }`}
          >
            {loading ? "Thinking…" : "Submit"}
          </button>
        </div>

        {/* Right Panel */}
        <div className="bg-zinc-900 border border-zinc-700 rounded p-4 overflow-auto">
          {error && (
            <div className="bg-red-950 border border-red-800 text-red-300 p-3 rounded text-sm mb-3">
              {error}
            </div>
          )}

          {!response && !error && (
            <div className="text-zinc-500 text-sm italic">
              Output will appear here…
            </div>
          )}

          {response && (
            <div className="relative bg-black border border-zinc-700 rounded p-4">
              <button
                onClick={() => navigator.clipboard.writeText(response)}
                className="absolute top-2 right-2 text-xs text-zinc-400 hover:text-white"
              >
                Copy
              </button>

              <pre className="text-sm font-mono whitespace-pre-wrap text-zinc-100 overflow-x-auto">
                {response}
              </pre>
            </div>
          )}
        </div>
      </div>
    </main>
  );
}
