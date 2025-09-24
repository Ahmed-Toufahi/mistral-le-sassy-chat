'use client'

export default function Instructions() {
  return (
    <div className="absolute top-4 left-4 bg-white/90 backdrop-blur-sm rounded-lg p-4 shadow-lg border max-w-sm z-10">
      <h2 className="text-lg font-bold text-mistral-orange mb-2">🐱 Meet Mistral le Sassy Chat!</h2>
      <div className="text-sm text-gray-700 space-y-1">
        <p><strong>Try saying:</strong></p>
        <ul className="list-disc list-inside space-y-1 text-xs">
          <li>"Hello kitty!"</li>
          <li>"Move up"</li>
          <li>"Move right"</li>
          <li>"What are you thinking?"</li>
          <li>"What's the meaning of life?"</li>
        </ul>
        <p className="mt-2 text-xs text-gray-500">
          This friendly cat loves to follow your commands and will move around when you ask!
        </p>
      </div>
    </div>
  )
}