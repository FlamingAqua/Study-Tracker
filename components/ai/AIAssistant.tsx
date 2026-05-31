'use client'

import { useState } from 'react'

export default function AIAssistant() {
  const [prompt, setPrompt] = useState('')
  const [answer, setAnswer] = useState('')
  const [loading, setLoading] = useState(false)

  async function askAI() {
    if (!prompt) return

    setLoading(true)

    const res = await fetch('/api/ai', {
      method: 'POST',
      headers: {
        'Content-Type':
          'application/json',
      },
      body: JSON.stringify({
        prompt,
      }),
    })

    const data = await res.json()

    setAnswer(data.answer)
    setLoading(false)
  }

  return (
    <div className="space-y-4">
      <textarea
        className="w-full border rounded p-3"
        rows={5}
        value={prompt}
        onChange={(e) =>
          setPrompt(e.target.value)
        }
        placeholder="Ask anything..."
      />

      <button
        onClick={askAI}
        className="px-4 py-2 rounded bg-blue-600 text-white"
      >
        {loading
          ? "Thinking..."
          : "Ask AI"}
      </button>

      {answer && (
        <div className="border rounded p-4">
          {answer}
        </div>
      )}
    </div>
  )
}