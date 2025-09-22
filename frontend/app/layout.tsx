import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Mistral le Sassy Chat',
  description: 'The autonomous AI feline',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}