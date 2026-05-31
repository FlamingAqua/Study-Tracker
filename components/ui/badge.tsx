import { cn } from '@/lib/utils'

export function Badge({ className, children }: { className?: string; children: React.ReactNode }) {
  return <span className={cn('inline-flex items-center rounded-full px-3 py-1 text-xs font-semibold', 'bg-brand-50 text-brand-700 dark:bg-brand-950 dark:text-brand-200', className)}>{children}</span>
}
