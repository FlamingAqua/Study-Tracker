'use client'

import { useEffect, useMemo, useRef, useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { Clock3, Pause, Play, RotateCcw } from 'lucide-react'

export function StudyTimer({ onManualSave }: { onManualSave?: (minutes: number) => void }) {
  const [running, setRunning] = useState(false)
  const [seconds, setSeconds] = useState(0)
  const timerRef = useRef<number | null>(null)

  useEffect(() => {
    if (!running) return
    timerRef.current = window.setInterval(() => setSeconds((value) => value + 1), 1000)
    return () => {
      if (timerRef.current) window.clearInterval(timerRef.current)
    }
  }, [running])

  const minutes = useMemo(() => Math.floor(seconds / 60), [seconds])
  const display = useMemo(() => `${String(Math.floor(seconds / 3600)).padStart(2, '0')}:${String(Math.floor((seconds % 3600) / 60)).padStart(2, '0')}:${String(seconds % 60).padStart(2, '0')}`, [seconds])

  function stopAndSave() {
    setRunning(false)
    onManualSave?.(minutes)
  }

  return (
    <Card className="mt-4">
      <div className="flex items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2"><Clock3 className="h-4 w-4 text-brand-600" /><h3 className="font-semibold">Study timer</h3></div>
          <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">Useful for focused sessions and weekly totals.</p>
        </div>
        <p className="text-xl font-bold tabular-nums">{display}</p>
      </div>

      <div className="mt-4 flex flex-wrap gap-2">
        {!running ? (
          <Button type="button" onClick={() => setRunning(true)}><Play className="h-4 w-4" /><span className="ml-2">Start</span></Button>
        ) : (
          <Button type="button" onClick={() => setRunning(false)} className="bg-amber-600 hover:bg-amber-700"><Pause className="h-4 w-4" /><span className="ml-2">Pause</span></Button>
        )}
        <Button type="button" className="bg-white text-slate-900 hover:bg-slate-100 dark:bg-slate-900 dark:text-slate-100" onClick={stopAndSave}><RotateCcw className="h-4 w-4" /><span className="ml-2">Save & reset</span></Button>
        <Button type="button" className="bg-slate-900 hover:bg-slate-800 dark:bg-white dark:text-slate-900" onClick={() => { setSeconds(0); setRunning(false) }}>Reset only</Button>
      </div>
    </Card>
  )
}
