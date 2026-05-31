'use client'

import { AuthGate } from '@/components/auth/AuthGate'
import { Shell } from '@/components/layout/Shell'
import AdminDashboard from '@/components/dashboard/AdminDashboard'

export default function AdminPage() {
  return (
    <AuthGate>
      <Shell>
        <AdminDashboard />
      </Shell>
    </AuthGate>
  )
}