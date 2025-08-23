import type { Metadata } from 'next'
import './globals.css'
import Navigation from '@/components/Navigation'

export const metadata: Metadata = {
  title: 'BlockLure AI - AI-Driven Blockchain Honeypot for Adaptive Cyber Defense',
  description: 'Next-generation honeypot system combining AI, Blockchain, and Cybersecurity for real-time threat detection and analysis',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="antialiased">
        <Navigation />
        {children}
      </body>
    </html>
  )
}
