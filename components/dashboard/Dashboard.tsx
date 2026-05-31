'use client'

import { type ComponentType, useMemo, useState } from 'react'
import { Bar, BarChart, CartesianGrid, Cell, Line, LineChart, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { BookMarked, CalendarClock, Clock3, Flame, FileDown, Filter, GraduationCap, Loader2, NotebookPen, PlayCircle, RefreshCw, Search, Target, TimerReset } from 'lucide-react'
import { useTrackerData } from '@/hooks/useTrackerData'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Progress } from '@/components/ui/progress'
import { Select } from '@/components/ui/select'
import { formatDateOnly, formatDateTime, toISODate } from '@/lib/utils'
import { useToast } from '@/components/ui/toast'
import { useUserProfile } from '@/hooks/useUserProfile'
import { upsertChapterStatus, markRevisionDone } from '@/lib/firestore'
import { exportElementToPdf } from '@/lib/pdf'
import { enableBrowserNotifications, sendBrowserNotification } from '@/lib/notifications'
import type { Chapter, RevisionItem } from '@/lib/types'
import { GROUP_ID } from '@/lib/constants'
import { StudyTimer } from '@/components/dashboard/StudyTimer'
import AIAssistant from "@/components/ai/AIAssistant";
const statusOptions = [
  { value: 'all', label: 'All statuses' },
  { value: 'not_started', label: 'Not started' },
  { value: 'studying', label: 'Studying' },
  { value: 'completed', label: 'Completed' },
  { value: 'revision_pending', label: 'Revision pending' },
]

export function Dashboard() {
  const { profile } = useUserProfile()
  const { subjects, chapters, logs, revisionQueue, loading, error, derived } = useTrackerData()
  const { toast } = useToast()
  const [subjectFilter, setSubjectFilter] = useState('all')
  const [statusFilter, setStatusFilter] = useState('all')
  const [search, setSearch] = useState('')
  const [selectedChapterId, setSelectedChapterId] = useState('')
  const [notes, setNotes] = useState('')
  const [hours, setHours] = useState('1')
  const [tomorrowTarget, setTomorrowTarget] = useState('')
  const [progress, setProgress] = useState('25')
  const [chapterStatus, setChapterStatus] = useState<Chapter['status']>('studying')
  const [busy, setBusy] = useState(false)

  const filteredChapters = useMemo(() => {
    return chapters.filter((chapter) => {
      const matchesSubject = subjectFilter === 'all' || chapter.subjectId === subjectFilter
      const matchesStatus = statusFilter === 'all' || chapter.status === statusFilter
      const matchesSearch = `${chapter.name} ${chapter.subject} ${chapter.notes}`.toLowerCase().includes(search.toLowerCase())
      return matchesSubject && matchesStatus && matchesSearch
    })
  }, [chapters, search, statusFilter, subjectFilter])

  const currentChapter = derived.currentChapter || chapters[0] || null

  const pieData = subjects.map((subject) => ({ name: subject.name, value: subject.completion }))
  const chartPalette = ['#2aa69d', '#0ea5e9']

  async function handleSaveProgress() {
    if (!profile) return
    const chapter = chapters.find((item) => item.id === selectedChapterId)
    if (!chapter) {
      toast({ title: 'Select a chapter', description: 'Pick the chapter you are updating first.', variant: 'error' })
      return
    }

    setBusy(true)
    try {
      await upsertChapterStatus({
        chapterId: chapter.id,
        subjectId: chapter.subjectId,
        subject: chapter.subject,
        chapterName: chapter.name,
        status: chapterStatus,
        completionPercentage: Number(progress),
        notes,
        hoursStudied: Number(hours),
        user: profile,
        tomorrowTarget,
      })
      toast({ title: 'Progress saved', description: `${chapter.name} updated successfully.`, variant: 'success' })
      sendBrowserNotification('Study Tracker', `${chapter.name} updated to ${chapterStatus}`)
      setNotes('')
      setTomorrowTarget('')
    } catch (error) {
      toast({ title: 'Save failed', description: error instanceof Error ? error.message : 'Unable to save progress.', variant: 'error' })
    } finally {
      setBusy(false)
    }
  }

  async function handleEnableNotifications() {
    try {
      await enableBrowserNotifications()
      toast({ title: 'Notifications enabled', description: 'Browser reminders are ready.', variant: 'success' })
    } catch (error) {
      toast({ title: 'Notification setup failed', description: error instanceof Error ? error.message : 'Could not enable notifications.', variant: 'error' })
    }
  }

  async function handleMarkRevisionDone(item: RevisionItem) {
    setBusy(true)
    try {
      await markRevisionDone(item.id)
      toast({ title: 'Revision completed', description: `${item.chapterName} marked as done.`, variant: 'success' })
    } catch (error) {
      toast({ title: 'Could not update revision', description: error instanceof Error ? error.message : 'Please try again.', variant: 'error' })
    } finally {
      setBusy(false)
    }
  }

  async function handleExportPdf() {
    try {
      await exportElementToPdf('dashboard-export', `mbbs-progress-${toISODate()}.pdf`)
      toast({ title: 'PDF exported', description: 'Your progress report has been downloaded.', variant: 'success' })
    } catch (error) {
      toast({ title: 'Export failed', description: error instanceof Error ? error.message : 'Could not generate PDF.', variant: 'error' })
    }
  }

  if (loading) {
    return <div className="grid min-h-[60vh] place-items-center text-slate-500"><Loader2 className="h-6 w-6 animate-spin" /></div>
  }

  if (error) {
    return <Card><p className="text-rose-600">{error}</p></Card>
  }

  return (
    <div id="dashboard-export" className="space-y-6">
      <section className="grid gap-4 lg:grid-cols-[1.5fr,1fr]">
        <Card>
          <div className="flex flex-col gap-5 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <Badge>Group {GROUP_ID}</Badge>
              <h1 className="mt-3 text-3xl font-bold tracking-tight">Study progress dashboard</h1>
              <p className="mt-2 max-w-2xl text-sm text-slate-500 dark:text-slate-400">Realtime view. Updates appear instantly when a chapter is changed on mobile.</p>
            </div>
            <div className="grid grid-cols-2 gap-3 sm:min-w-[260px]">
              <div className="rounded-2xl bg-slate-50 p-4 dark:bg-slate-800/60">
                <p className="text-xs text-slate-500">Streak</p>
                <p className="mt-1 text-2xl font-bold">{derived.streak} days</p>
              </div>
              <div className="rounded-2xl bg-slate-50 p-4 dark:bg-slate-800/60">
                <p className="text-xs text-slate-500">Hours</p>
                <p className="mt-1 text-2xl font-bold">{derived.totalHours}</p>
              </div>
            </div>
          </div>

          <div className="mt-6 grid gap-4 md:grid-cols-3">
            <Metric icon={GraduationCap} title="Completion" value={`${derived.completionPercent}%`} caption={`${derived.completedCount} completed chapters`} />
            <Metric icon={Clock3} title="Study hours" value={`${derived.totalHours}h`} caption={`${derived.weeklyHoursTotal}h this week`} />
            <Metric icon={Target} title="Completion date" value={formatDateOnly(derived.estimatedCompletionDate)} caption="Based on recent pace" />
          </div>
        </Card>

        <Card className="flex flex-col gap-4">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold">Today’s focus</h2>
            <Badge>{currentChapter ? currentChapter.status.replace('_', ' ') : 'No active chapter'}</Badge>
          </div>
          <div className="rounded-3xl bg-gradient-to-br from-brand-500 to-emerald-600 p-5 text-white shadow-soft">
            <p className="text-xs uppercase tracking-[0.24em] text-white/80">Current chapter</p>
            <p className="mt-2 text-xl font-bold">{currentChapter ? `${currentChapter.subject} • ${currentChapter.name}` : 'No active chapter selected'}</p>
            <p className="mt-2 text-sm text-white/85">{currentChapter ? `Last updated ${formatDateTime(currentChapter.lastUpdatedAt)}` : 'Select a chapter below to begin tracking.'}</p>
          </div>
          <div className="grid grid-cols-2 gap-3 text-sm">
            <div className="rounded-2xl bg-slate-50 p-4 dark:bg-slate-800/60">
              <p className="text-slate-500">Pending chapters</p>
              <p className="mt-1 text-2xl font-bold">{derived.pendingCount}</p>
            </div>
            <div className="rounded-2xl bg-slate-50 p-4 dark:bg-slate-800/60">
              <p className="text-slate-500">Revision queue</p>
              <p className="mt-1 text-2xl font-bold">{revisionQueue.length}</p>
            </div>
          </div>
        </Card>
      </section>

      <section className="grid gap-4 xl:grid-cols-[1.4fr,0.9fr]">
        <Card>
          <div className="flex flex-wrap items-end justify-between gap-3">
            <div>
              <h2 className="text-lg font-semibold">Study controls</h2>
              <p className="text-sm text-slate-500 dark:text-slate-400">Update status, notes, hours studied, and tomorrow’s target.</p>
            </div>
            <div className="flex flex-wrap gap-2">
              <Button type="button" className="bg-white text-slate-900 hover:bg-slate-100 dark:bg-slate-900 dark:text-slate-100" onClick={handleEnableNotifications}><CalendarClock className="h-4 w-4" /><span className="ml-2">Reminders</span></Button>
              <Button type="button" className="bg-slate-900 hover:bg-slate-800 dark:bg-white dark:text-slate-900" onClick={handleExportPdf}><FileDown className="h-4 w-4" /><span className="ml-2">Export PDF</span></Button>
            </div>
          </div>

          <div className="mt-5 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
            <div>
              <label className="mb-2 block text-sm font-medium">Subject</label>
              <Select value={subjectFilter} onChange={(e) => setSubjectFilter(e.target.value)}>
                <option value="all">All subjects</option>
                {subjects.map((subject) => <option key={subject.id} value={subject.id}>{subject.name}</option>)}
              </Select>
            </div>
            <div>
              <label className="mb-2 block text-sm font-medium">Status</label>
              <Select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)}>
                {statusOptions.map((option) => <option key={option.value} value={option.value}>{option.label}</option>)}
              </Select>
            </div>
            <div className="md:col-span-2">
              <label className="mb-2 block text-sm font-medium">Search</label>
              <div className="relative">
                <Search className="pointer-events-none absolute left-3 top-3.5 h-4 w-4 text-slate-400" />
                <Input className="pl-10" value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Search chapters, notes, or subject…" />
              </div>
            </div>
          </div>

          <div className="mt-5 grid gap-4 lg:grid-cols-2">
            <div>
              <label className="mb-2 block text-sm font-medium">Chapter</label>
              <Select value={selectedChapterId} onChange={(e) => setSelectedChapterId(e.target.value)}>
                <option value="">Select chapter</option>
                {filteredChapters.map((chapter) => <option key={chapter.id} value={chapter.id}>{chapter.subject} • {chapter.name}</option>)}
              </Select>
            </div>
            <div>
              <label className="mb-2 block text-sm font-medium">Status</label>
              <Select value={chapterStatus} onChange={(e) => setChapterStatus(e.target.value as Chapter['status'])}>
                <option value="not_started">Not started</option>
                <option value="studying">Studying</option>
                <option value="completed">Completed</option>
                <option value="revision_pending">Revision pending</option>
              </Select>
            </div>
            <div>
              <label className="mb-2 block text-sm font-medium">Completion %</label>
              <Input type="number" min="0" max="100" value={progress} onChange={(e) => setProgress(e.target.value)} />
            </div>
            <div>
              <label className="mb-2 block text-sm font-medium">Hours studied</label>
              <Input type="number" step="0.5" min="0" value={hours} onChange={(e) => setHours(e.target.value)} />
            </div>
            <div className="lg:col-span-2">
              <label className="mb-2 block text-sm font-medium">Notes</label>
              <textarea value={notes} onChange={(e) => setNotes(e.target.value)} rows={4} className="w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm outline-none transition focus:border-brand-500 focus:ring-2 focus:ring-brand-100 dark:border-slate-700 dark:bg-slate-950 dark:text-slate-100" placeholder="Write what was studied, doubts, mnemonics, or key points…" />
            </div>
            <div className="lg:col-span-2">
              <label className="mb-2 block text-sm font-medium">Tomorrow’s target</label>
              <Input value={tomorrowTarget} onChange={(e) => setTomorrowTarget(e.target.value)} placeholder="For example: finish toxicology questions and revise injury patterns" />
            </div>
          </div>

          <div className="mt-5 flex flex-wrap items-center gap-3">
            <Button type="button" onClick={handleSaveProgress} disabled={busy}><PlayCircle className="h-4 w-4" /><span className="ml-2">{busy ? 'Saving…' : 'Save update'}</span></Button>
            <Button type="button" className="bg-white text-slate-900 hover:bg-slate-100 dark:bg-slate-900 dark:text-slate-100" onClick={() => { setSelectedChapterId(''); setNotes(''); setTomorrowTarget(''); setProgress('25'); setHours('1'); }}><TimerReset className="h-4 w-4" /><span className="ml-2">Reset</span></Button>
          </div>
        </Card>

        <Card>
  <AIAssistant />
</Card>
      </section>

      <section className="grid gap-4 xl:grid-cols-[1.1fr,0.9fr]">
        <Card>
          <div className="flex items-center justify-between gap-3">
            <div>
              <h2 className="text-lg font-semibold">Subject completion</h2>
              <p className="text-sm text-slate-500 dark:text-slate-400">Progress bar per subject.</p>
            </div>
            <Badge>{chapters.length} chapters</Badge>
          </div>
          <div className="mt-5 space-y-4">
            {derived.subjectCompletion.map((subject) => (
              <div key={subject.id}>
                <div className="mb-2 flex items-center justify-between text-sm">
                  <span className="font-medium">{subject.name}</span>
                  <span className="text-slate-500">{subject.completion}%</span>
                </div>
                <Progress value={subject.completion} />
              </div>
            ))}
          </div>
        </Card>

        <Card>
          <h2 className="text-lg font-semibold">Charts</h2>
          <div className="mt-5 grid gap-5">
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={derived.weeklyHours}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="day" />
                  <YAxis />
                  <Tooltip />
                  <Line type="monotone" dataKey="hours" stroke="#2aa69d" strokeWidth={3} />
                </LineChart>
              </ResponsiveContainer>
            </div>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie data={pieData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={86} label>
                    {pieData.map((entry, index) => <Cell key={entry.name} fill={chartPalette[index % chartPalette.length]} />)}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>
        </Card>
      </section>

      <section className="grid gap-4 lg:grid-cols-2">
        <Card>
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold">Revision queue</h2>
            <Badge>{revisionQueue.length} pending</Badge>
          </div>
          <div className="mt-4 space-y-3">
            {revisionQueue.length === 0 ? <p className="text-sm text-slate-500">No revision reminders yet.</p> : revisionQueue.map((item) => (
              <div key={item.id} className="rounded-2xl border border-slate-200 p-4 dark:border-slate-800">
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <p className="font-semibold">{item.chapterName}</p>
                    <p className="text-sm text-slate-500">{item.subject} • Due {formatDateOnly(item.dueDate)} • Day {item.offsetDays}</p>
                  </div>
                  <Button type="button" className="px-3 py-2 text-xs" onClick={() => handleMarkRevisionDone(item)} disabled={busy}><RefreshCw className="h-3.5 w-3.5" /><span className="ml-2">Done</span></Button>
                </div>
              </div>
            ))}
          </div>
        </Card>

        <Card>
          <h2 className="text-lg font-semibold">Recent study activity</h2>
          <div className="mt-4 space-y-3">
            {logs.slice(-6).reverse().map((log) => (
              <div key={log.id} className="rounded-2xl bg-slate-50 p-4 dark:bg-slate-800/60">
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <p className="font-semibold">{log.chapterName}</p>
                    <p className="text-sm text-slate-500">{log.subject} • {log.status.replace('_', ' ')}</p>
                  </div>
                  <Badge>{log.hoursStudied}h</Badge>
                </div>
                <p className="mt-2 text-sm text-slate-600 dark:text-slate-300">{log.notes || 'No notes added.'}</p>
                <p className="mt-2 text-xs text-slate-500">Target: {log.tomorrowTarget || 'Not set'} • {formatDateTime(log.createdAt)}</p>
              </div>
            ))}
          </div>
        </Card>
      </section>

      <section className="grid gap-4 lg:grid-cols-2">
        <Card>
          <div className="flex items-center gap-2">
            <Flame className="h-4 w-4 text-orange-500" />
            <h2 className="text-lg font-semibold">Heatmap</h2>
          </div>
          <div className="mt-4 grid grid-cols-7 gap-2">
            {derived.heatmap.map((day) => (
              <div key={day.date} title={`${day.date}: ${day.hours}h`} className="aspect-square rounded-xl border border-slate-200 bg-white p-2 text-[10px] text-slate-500 dark:border-slate-800 dark:bg-slate-900">
                <div className={day.hours > 0 ? 'h-full rounded-lg bg-brand-500/80' : 'h-full rounded-lg bg-slate-100 dark:bg-slate-800'} />
              </div>
            ))}
          </div>
        </Card>

        <Card>
          <div className="flex items-center gap-2">
            <NotebookPen className="h-4 w-4 text-brand-600" />
            <h2 className="text-lg font-semibold">Chapter list</h2>
          </div>
          <div className="mt-4 max-h-[28rem] space-y-3 overflow-auto pr-1">
            {filteredChapters.map((chapter) => (
              <div key={chapter.id} className="rounded-2xl border border-slate-200 p-4 dark:border-slate-800">
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <p className="font-semibold">{chapter.subject} • {chapter.name}</p>
                    <p className="text-sm text-slate-500">{chapter.status.replace('_', ' ')} • Updated {formatDateTime(chapter.lastUpdatedAt)}</p>
                  </div>
                  <Badge>{chapter.completionPercentage}%</Badge>
                </div>
                <div className="mt-3"><Progress value={chapter.completionPercentage} /></div>
                <p className="mt-2 text-sm text-slate-600 dark:text-slate-300">{chapter.notes || 'No notes yet.'}</p>
              </div>
            ))}
          </div>
        </Card>
      </section>
    </div>
  )
}

function Metric({ icon: Icon, title, value, caption }: { icon: ComponentType<{ className?: string }>; title: string; value: string; caption: string }) {
  return (
    <div className="rounded-3xl bg-slate-50 p-4 dark:bg-slate-800/60">
      <div className="flex items-center justify-between">
        <p className="text-sm text-slate-500">{title}</p>
        <Icon className="h-4 w-4 text-brand-600" />
      </div>
      <p className="mt-3 text-2xl font-bold">{value}</p>
      <p className="mt-1 text-xs text-slate-500">{caption}</p>
    </div>
  )
}
