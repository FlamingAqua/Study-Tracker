'use client'

import { AuthGate } from '@/components/auth/AuthGate'
import { Shell } from '@/components/layout/Shell'
import { useTrackerData } from '@/hooks/useTrackerData'
import { Card } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Select } from '@/components/ui/select'
import { Progress } from '@/components/ui/progress'
import { useMemo, useState } from 'react'
import { Search } from 'lucide-react'
import { formatDateTime } from '@/lib/utils'

export default function ChaptersPage() {
  return <AuthGate><Shell><ChaptersContent /></Shell></AuthGate>
}

function ChaptersContent() {
  const { subjects, chapters } = useTrackerData()
  const [subjectFilter, setSubjectFilter] = useState('all')
  const [statusFilter, setStatusFilter] = useState('all')
  const [search, setSearch] = useState('')

  const filtered = useMemo(() => chapters.filter((chapter) => {
    return (subjectFilter === 'all' || chapter.subjectId === subjectFilter) && (statusFilter === 'all' || chapter.status === statusFilter) && `${chapter.name} ${chapter.subject} ${chapter.notes}`.toLowerCase().includes(search.toLowerCase())
  }), [chapters, search, statusFilter, subjectFilter])

  return (
    <div className="space-y-6">
      <Card>
        <h1 className="text-3xl font-bold">Chapter tracking</h1>
        <p className="mt-2 text-sm text-slate-500 dark:text-slate-400">Search, filter, and review all chapters for both MBBS subjects.</p>
        <div className="mt-5 grid gap-4 md:grid-cols-3">
          <Select value={subjectFilter} onChange={(e) => setSubjectFilter(e.target.value)}>
            <option value="all">All subjects</option>
            {subjects.map((subject) => <option key={subject.id} value={subject.id}>{subject.name}</option>)}
          </Select>
          <Select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)}>
            <option value="all">All statuses</option>
            <option value="not_started">Not started</option>
            <option value="studying">Studying</option>
            <option value="completed">Completed</option>
            <option value="revision_pending">Revision pending</option>
          </Select>
          <div className="relative md:col-span-1">
            <Search className="pointer-events-none absolute left-3 top-3.5 h-4 w-4 text-slate-400" />
            <Input className="pl-10" placeholder="Search chapters…" value={search} onChange={(e) => setSearch(e.target.value)} />
          </div>
        </div>
      </Card>

      <div className="grid gap-4 lg:grid-cols-2">
        {filtered.map((chapter) => (
          <Card key={chapter.id}>
            <div className="flex items-start justify-between gap-4">
              <div>
                <p className="text-lg font-semibold">{chapter.subject} • {chapter.name}</p>
                <p className="mt-1 text-sm text-slate-500">Updated {formatDateTime(chapter.lastUpdatedAt)}</p>
              </div>
              <Badge>{chapter.status.replace('_', ' ')}</Badge>
            </div>
            <div className="mt-4 flex items-center justify-between text-sm">
              <span>Completion</span>
              <span>{chapter.completionPercentage}%</span>
            </div>
            <Progress value={chapter.completionPercentage} />
            <p className="mt-3 text-sm text-slate-600 dark:text-slate-300">{chapter.notes || 'No notes added yet.'}</p>
          </Card>
        ))}
      </div>
    </div>
  )
}
