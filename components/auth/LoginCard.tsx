'use client'

import { ShieldCheck, Chrome, Sparkles } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { signInWithGoogle } from '@/lib/auth'
import { useToast } from '@/components/ui/toast'

export function LoginCard() {
  const { toast } = useToast()

  async function handleSignIn() {
    try {
      await signInWithGoogle()
      toast({ title: 'Welcome back', description: 'Syncing your latest study progress.', variant: 'success' })
    } catch (error) {
      toast({ title: 'Login failed', description: error instanceof Error ? error.message : 'Please try again.', variant: 'error' })
    }
  }

  return (
    <div className="mx-auto grid min-h-[calc(100vh-8rem)] max-w-5xl place-items-center">
      <Card className="w-full max-w-3xl overflow-hidden p-0">
        <div className="grid gap-0 lg:grid-cols-2">
          <div className="bg-gradient-to-br from-brand-600 to-emerald-600 p-8 text-white">
            <div className="inline-flex items-center gap-2 rounded-full bg-white/15 px-3 py-1 text-xs font-semibold">
              <Sparkles className="h-3.5 w-3.5" />
              Medical study accountability
            </div>
            <h1 className="mt-5 text-3xl font-bold leading-tight">Track chapters, study hours, revisions, and streaks in real time.</h1>
            <p className="mt-4 text-sm leading-6 text-white/90">Built for a sister in MBBS and a brother who wants a clear, live view of progress, revision needs, and daily consistency.</p>
            <div className="mt-8 space-y-3 text-sm">
              <div className="flex items-center gap-2"><ShieldCheck className="h-4 w-4" /> Authorized Google accounts only</div>
              <div className="flex items-center gap-2"><ShieldCheck className="h-4 w-4" /> Realtime Firestore sync</div>
              <div className="flex items-center gap-2"><ShieldCheck className="h-4 w-4" /> Mobile-friendly dashboard</div>
            </div>
          </div>

          <div className="flex flex-col justify-center p-8">
            <h2 className="text-2xl font-bold text-slate-900 dark:text-slate-100">Sign in with Google</h2>
            <p className="mt-2 text-sm text-slate-500 dark:text-slate-400">Use one of the approved family accounts to access the tracker.</p>
            <Button className="mt-6 w-full" onClick={handleSignIn}>
              <Chrome className="h-4 w-4" />
              <span className="ml-2">Continue with Google</span>
            </Button>
            <p className="mt-5 text-xs text-slate-500 dark:text-slate-400">Tip: After signing in, the dashboard starts listening to Firestore updates instantly.</p>
          </div>
        </div>
      </Card>
    </div>
  )
}
