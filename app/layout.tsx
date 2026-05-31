// @ts-ignore: side-effect CSS import
import './globals.css';
import type { Metadata } from 'next'
import { Providers } from '@/components/providers'

export const metadata: Metadata = {
  title: 'MBBS Study Tracker',
  description: 'Real-time MBBS study tracker for family accountability.',
  manifest: '/manifest.json',
}

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  )
}

