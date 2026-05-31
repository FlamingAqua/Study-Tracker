'use client'

import Link from 'next/link'
import { BookOpenCheck, CalendarDays, LayoutDashboard, LogOut, MoonStar, Sparkles, SunMedium } from 'lucide-react'
import { usePathname } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'
import { useTheme } from '@/hooks/useTheme'
import { signOutUser } from '@/lib/auth'
import { useToast } from '@/components/ui/toast'
import Image from "next/image"; 
const nav = [
  { href: '/', label: 'Dashboard', icon: LayoutDashboard },
  { href: '/chapters', label: 'Chapters', icon: BookOpenCheck },
  { href: '/analytics', label: 'Analytics', icon: CalendarDays },
  { href: '/settings', label: 'Settings', icon: Sparkles },
]

export function Shell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname()
  const { theme, toggleTheme } = useTheme()
  const { toast } = useToast()

  async function handleLogout() {
    await signOutUser()
    toast({ title: 'Signed out', description: 'You are logged out safely.', variant: 'info' })
  }

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,_rgba(42,166,157,0.15),_transparent_42%),linear-gradient(to_bottom,_#f8fafc,_#eefbf9)] text-slate-900 dark:bg-[radial-gradient(circle_at_top,_rgba(42,166,157,0.15),_transparent_42%),linear-gradient(to_bottom,_#020617,_#0f172a)] dark:text-slate-100">
      <header className="sticky top-0 z-30 border-b border-white/50 bg-white/70 backdrop-blur dark:border-slate-800 dark:bg-slate-950/70">
        <div className="mx-auto flex max-w-7xl items-center justify-between gap-3 px-4 py-3 lg:px-8">
          <Link href="/" className="flex items-center gap-3">
  <Image
    src={
      theme === "dark"
        ? "/branding/logo-dark.png"
        : "/branding/logo-light.png"
    }
    alt="MBBS Study Tracker"
    width={44}
    height={44}
    priority
  />

  <div>
    <p className="text-sm font-semibold text-slate-900 dark:text-slate-100">
      MBBS Study Tracker
    </p>
    <p className="text-xs text-slate-500 dark:text-slate-400">
      Smart Medical Learning Platform
    </p>
  </div>
</Link>

          <div className="hidden items-center gap-2 md:flex">
            {nav.map((item) => {
              const Icon = item.icon
              const active = pathname === item.href
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={cn(
                    'inline-flex items-center gap-2 rounded-2xl px-4 py-2 text-sm font-medium transition',
                    active ? 'bg-brand-600 text-white shadow-soft' : 'text-slate-600 hover:bg-white hover:text-slate-900 dark:text-slate-300 dark:hover:bg-slate-900 dark:hover:text-white'
                  )}
                >
                  <Icon className="h-4 w-4" />
                  {item.label}
                </Link>
              )
            })}
          </div>

          <div className="flex items-center gap-2">
            <Button type="button" className="bg-white text-slate-900 hover:bg-slate-100 dark:bg-slate-900 dark:text-slate-100" onClick={toggleTheme}>
              {theme === 'dark' ? <SunMedium className="h-4 w-4" /> : <MoonStar className="h-4 w-4" />}
              <span className="ml-2 hidden sm:inline">{theme === 'dark' ? 'Light' : 'Dark'}</span>
            </Button>
            <Button type="button" className="bg-rose-600 hover:bg-rose-700" onClick={handleLogout}>
              <LogOut className="h-4 w-4" />
              <span className="ml-2 hidden sm:inline">Logout</span>
            </Button>
          </div>
        </div>

        <div className="mx-auto flex max-w-7xl gap-2 overflow-x-auto px-4 pb-3 md:hidden">
          {nav.map((item) => {
            const Icon = item.icon
            const active = pathname === item.href
            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  'inline-flex min-w-fit items-center gap-2 rounded-full px-4 py-2 text-sm font-medium transition',
                  active ? 'bg-brand-600 text-white' : 'bg-white text-slate-600 dark:bg-slate-900 dark:text-slate-300'
                )}
              >
                <Icon className="h-4 w-4" />
                {item.label}
              </Link>
            )
          })}
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-4 py-6 lg:px-8">{children}</main>
    </div>
  )
}
