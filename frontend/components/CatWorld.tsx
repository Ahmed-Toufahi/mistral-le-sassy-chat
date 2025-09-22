'use client'

import { useState, useEffect } from 'react'
import Cat from './Cat'
import ChatInput from './ChatInput'
import { useSocket } from '@/hooks/useSocket'

interface CatState {
  position: { x: number; y: number }
  mood: string
  action: string
  thought: string
}

export default function CatWorld() {
  const [catState, setCatState] = useState<CatState>({
    position: { x: 50, y: 50 },
    mood: 'playful',
    action: 'sitting',
    thought: 'Hello! I\'m ready to play!'
  })

  const [chatResponse, setChatResponse] = useState<string>('')

  const { sendMessage } = useSocket({
    onCatResponse: (data) => {
      console.log('WebSocket chat response received:', data)
      setChatResponse(data.text || "Meow!")
      setCatState(prev => ({
        position: data.new_position || prev.position,
        action: data.action || prev.action,
        mood: data.mood || prev.mood,
        thought: data.thought || prev.thought
      }))
      setTimeout(() => setChatResponse(''), 4000)
    }
  })

  const handleChatSubmit = async (message: string) => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      console.log('Sending chat message to:', `${apiUrl}/api/chat`)
      
      const response = await fetch(`${apiUrl}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: message })
      })
      
      if (response.ok) {
        const data = await response.json()
        console.log('Chat response data:', data)
        
        // Display the cat's response
        setChatResponse(data.text || "Meow!")
        
        // Update cat state with complete data
        setCatState(prev => ({
          position: data.new_position || prev.position,
          action: data.action || prev.action,
          mood: data.mood || prev.mood,
          thought: data.thought || prev.thought
        }))
        
        // Clear response after 4 seconds
        setTimeout(() => setChatResponse(''), 4000)
      } else {
        console.error('Chat request failed:', response.status)
        setChatResponse("*stretches and ignores you*")
        setTimeout(() => setChatResponse(''), 3000)
      }
    } catch (error) {
      console.error('Chat error:', error)
      setChatResponse("*tilts head in confusion*")
      setTimeout(() => setChatResponse(''), 3000)
    }
  }

  return (
    <div className="relative h-full w-full cat-container">
      <Cat 
        position={catState.position}
        action={catState.action}
        mood={catState.mood}
        thought={catState.thought}
        response={chatResponse}
      />
      <ChatInput onSubmit={handleChatSubmit} />
    </div>
  )
}