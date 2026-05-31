'use client'

import { AuthGate } from '@/components/auth/AuthGate'
import { Shell } from '@/components/layout/Shell'
import { Dashboard } from '@/components/dashboard/Dashboard'
import AIAssistant from "@/components/ai/AIAssistant";
export default function Page() {
  return (
    <AuthGate>
      <Shell>
        <Dashboard />
        <AIAssistant />
      </Shell>
    </AuthGate>
  )
}

