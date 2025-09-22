'use client'

import { motion, AnimatePresence } from 'framer-motion'

interface CatProps {
  position: { x: number; y: number }
  action: string
  mood: string
  thought: string
  response: string
}

export default function Cat({ position, action, mood, thought, response }: CatProps) {
  // Ensure cat stays within visible bounds
  const safePosition = {
    x: Math.max(10, Math.min(90, position.x)),
    y: Math.max(10, Math.min(90, position.y))
  }

  const getCatEmoji = () => {
    switch (action) {
      case 'sleeping': return '😴'
      case 'playing': return '😸'
      case 'grooming': return '😽' 
      case 'stretching': return '😺'
      default: return '😼'
    }
  }

  const getMoodColor = () => {
    switch (mood) {
      case 'playful': return 'text-orange-500'
      case 'sleepy': return 'text-blue-400'
      case 'curious': return 'text-purple-500'
      case 'aloof': return 'text-gray-600'
      case 'hungry': return 'text-yellow-500'
      default: return 'text-gray-800'
    }
  }

  return (
    <>
      <motion.div
        className={`absolute text-6xl ${getMoodColor()} select-none`}
        animate={{
          x: `${safePosition.x}vw`,
          y: `${safePosition.y}vh`,
        }}
        transition={{
          type: "spring",
          stiffness: 100,
          damping: 20,
          duration: 2
        }}
        style={{
          transform: 'translate(-50%, -50%)'
        }}
      >
        {getCatEmoji()}
      </motion.div>

      <AnimatePresence>
        {(thought || response) && (
          <motion.div
            className="absolute bg-white/90 backdrop-blur-sm rounded-lg px-3 py-2 shadow-lg border max-w-xs"
            style={{
              left: `${safePosition.x}vw`,
              top: `${safePosition.y - 15}vh`,
              transform: 'translate(-50%, -100%)'
            }}
            initial={{ opacity: 0, scale: 0.8, y: 10 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.8, y: -10 }}
            transition={{ duration: 0.3 }}
          >
            <div className="text-sm text-gray-800">
              {response || thought}
            </div>
            <div className="absolute top-full left-1/2 transform -translate-x-1/2 border-l-8 border-r-8 border-t-8 border-transparent border-t-white/90"></div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  )
}