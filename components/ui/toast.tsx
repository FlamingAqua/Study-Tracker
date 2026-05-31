'use client'

import { createContext, useContext, useMemo, useState } from 'react'
import { CheckCircle2, AlertTriangle, Info } from 'lucide-react'
import { cn } from '@/lib/utils'

type ToastVariant = 'success' | 'error' | 'info'

type ToastItem = { id: string; title: string; description?: string; variant: ToastVariant }

type ToastContextValue = {
  toast: (item: Omit<ToastItem, 'id'>) => void
}

const ToastContext = createContext<ToastContextValue | null>(null)

export function ToastProvider({ children }: { children: React.ReactNode }) {
  const [toasts, setToasts] = useState<ToastItem[]>([])

  const value = useMemo<ToastContextValue>(() => ({
    toast: (item) => {
      const id = crypto.randomUUID()
      setToasts((current) => [...current, { ...item, id }])
      window.setTimeout(() => {
        setToasts((current) => current.filter((toast) => toast.id !== id))
      }, 3200)
    },
  }), [])

  return (
    <ToastContext.Provider value={value}>
      {children}
      <div className="fixed right-4 top-4 z-50 space-y-3">
        {toasts.map((toast) => (
          <div
            key={toast.id}
            className={cn(
              'w-[min(92vw,380px)] rounded-2xl border bg-white/90 p-4 shadow-soft backdrop-blur dark:border-slate-700 dark:bg-slate-900/90',
              'animate-fadeIn'
            )}
          >
            <div className="flex items-start gap-3">
              <div className={cn('mt-0.5 rounded-full p-1.5', toast.variant === 'success' && 'bg-emerald-100 text-emerald-700', toast.variant === 'error' && 'bg-rose-100 text-rose-700', toast.variant === 'info' && 'bg-brand-100 text-brand-700')}>
                {toast.variant === 'success' && <CheckCircle2 className="h-4 w-4" />}
                {toast.variant === 'error' && <AlertTriangle className="h-4 w-4" />}
                {toast.variant === 'info' && <Info className="h-4 w-4" />}
              </div>
              <div>
                <p className="font-semibold text-slate-900 dark:text-slate-100">{toast.title}</p>
                {toast.description ? <p className="mt-1 text-sm text-slate-600 dark:text-slate-300">{toast.description}</p> : null}
              </div>
            </div>
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  )
}

export function useToast() {
  const value = useContext(ToastContext)
  if (!value) throw new Error('useToast must be used inside ToastProvider')
  return value
}
