'use client'

import { useEffect, useRef } from 'react'
import { io, Socket } from 'socket.io-client'

interface SocketEvents {
  onCatAction?: (data: any) => void
  onCatResponse: (data: any) => void
}

export function useSocket({ onCatAction, onCatResponse }: SocketEvents) {
  const socketRef = useRef<Socket | null>(null)

  useEffect(() => {
    const socketUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
    console.log('Connecting to WebSocket:', socketUrl)
    socketRef.current = io(socketUrl)

    socketRef.current.on('connect', () => {
      console.log('WebSocket connected!')
    })

    socketRef.current.on('disconnect', () => {
      console.log('WebSocket disconnected')
    })

    socketRef.current.on('cat_action', (data) => {
      console.log('WebSocket cat_action:', data)
      if (onCatAction) onCatAction(data)
    })
    
    socketRef.current.on('cat_response', (data) => {
      console.log('WebSocket cat_response:', data)
      onCatResponse(data)
    })

    return () => {
      if (socketRef.current) {
        socketRef.current.disconnect()
      }
    }
  }, [onCatAction, onCatResponse])

  const sendMessage = (message: string) => {
    if (socketRef.current) {
      socketRef.current.emit('chat_message', { text: message })
    }
  }

  return { sendMessage }
}