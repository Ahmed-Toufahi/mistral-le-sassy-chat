'use client'

import CatWorld from '../components/CatWorld'
import Instructions from '../components/Instructions'

export default function Home() {
  return (
    <main className="h-screen w-screen overflow-hidden bg-gradient-to-br from-blue-50 to-purple-50">
      <Instructions />
      <CatWorld />
    </main>
  )
}