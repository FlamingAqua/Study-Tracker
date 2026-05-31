'use client'

import { AuthGate } from '@/components/auth/AuthGate'
import { Shell } from '@/components/layout/Shell'
import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { useTheme } from '@/hooks/useTheme'
import { useToast } from '@/components/ui/toast'
import { enableBrowserNotifications } from '@/lib/notifications'
import { seedDemoData } from '@/lib/firestore'
import { useUserProfile } from '@/hooks/useUserProfile'

export default function SettingsPage() {
  return <AuthGate><Shell><SettingsContent /></Shell></AuthGate>
}

function SettingsContent() {
  const { theme, toggleTheme } = useTheme()
  const { toast } = useToast()
  const { profile } = useUserProfile()

  async function handleSeed() {
    try {
      await seedDemoData()
      toast({ title: 'Seed completed', description: 'Default subjects and chapters are ready.', variant: 'success' })
    } catch (error) {
      toast({ title: 'Seed failed', description: error instanceof Error ? error.message : 'Could not seed demo data.', variant: 'error' })
    }
  }

  async function handleNotifications() {
    try {
      await enableBrowserNotifications()
      toast({ title: 'Notifications enabled', description: 'Browser reminders are now active.', variant: 'success' })
    } catch (error) {
      toast({ title: 'Notification error', description: error instanceof Error ? error.message : 'Could not enable notifications.', variant: 'error' })
    }
  }

  return (
    <div className="space-y-6">
      <Card>
        <h1 className="text-3xl font-bold">Settings</h1>
        <p className="mt-2 text-sm text-slate-500 dark:text-slate-400">Theme, notifications, and seed data.</p>
      </Card>

      <Card>
        <div className="grid gap-4 md:grid-cols-2">
          <div>
            <p className="text-sm font-semibold">Signed in as</p>
            <p className="mt-1 text-sm text-slate-500">{profile?.displayName || 'Loading profile…'}</p>
            <p className="text-sm text-slate-500">{profile?.email}</p>
          </div>
          <div className="flex flex-wrap gap-3 md:justify-end">
            <Button onClick={toggleTheme}>Toggle {theme === 'dark' ? 'light' : 'dark'} mode</Button>
            <Button className="bg-white text-slate-900 hover:bg-slate-100 dark:bg-slate-900 dark:text-slate-100" onClick={handleNotifications}>Enable reminders</Button>
            <Button className="bg-emerald-600 hover:bg-emerald-700" onClick={handleSeed}>Seed default data</Button>
          </div>
        </div>
      </Card>
    </div>
  )
}
