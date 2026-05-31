import { cn } from '@/lib/utils'

export function Progress({ value, className }: { value: number; className?: string }) {
  return (
    <div className={cn('h-2.5 w-full rounded-full bg-slate-200 dark:bg-slate-800', className)}>
      <div className="h-2.5 rounded-full bg-gradient-to-r from-brand-500 to-emerald-500 transition-all" style={{ width: `${Math.max(0, Math.min(100, value))}%` }} />
    </div>
  )
}
