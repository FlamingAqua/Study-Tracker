'use client'

import { AuthGate } from '@/components/auth/AuthGate'
import { Shell } from '@/components/layout/Shell'
import { Dashboard } from '@/components/dashboard/Dashboard'
export default function Page() {
  return (
    <AuthGate>
      <Shell>
        <Dashboard />
      </Shell>
    </AuthGate>
  )
}

