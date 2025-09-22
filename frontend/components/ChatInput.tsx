'use client'

import { useState } from 'react'

interface ChatInputProps {
  onSubmit: (message: string) => void
}

export default function ChatInput({ onSubmit }: ChatInputProps) {
  const [message, setMessage] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (message.trim()) {
      onSubmit(message.trim())
      setMessage('')
    }
  }

  return (
    <div className="absolute bottom-0 left-0 right-0 p-4">
      <form onSubmit={handleSubmit} className="max-w-2xl mx-auto">
        <div className="flex gap-2">
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Talk to Mistral le Sassy Chat..."
            className="flex-1 px-4 py-3 rounded-full border border-gray-200 bg-white/90 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-mistral-orange focus:border-transparent shadow-lg"
          />
          <button
            type="submit"
            className="px-6 py-3 bg-mistral-orange text-white rounded-full hover:bg-orange-600 transition-colors shadow-lg font-medium"
          >
            Send
          </button>
        </div>
      </form>
    </div>
  )
}