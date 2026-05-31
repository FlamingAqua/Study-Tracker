'use client'

import { AuthGate } from '@/components/auth/AuthGate'
import { Shell } from '@/components/layout/Shell'
import { useTrackerData } from '@/hooks/useTrackerData'
import { Card } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, LineChart, Line } from 'recharts'
import { formatDateOnly } from '@/lib/utils'

export default function AnalyticsPage() {
  return <AuthGate><Shell><AnalyticsContent /></Shell></AuthGate>
}

function AnalyticsContent() {
  const { derived } = useTrackerData()

  return (
    <div className="space-y-6">
      <Card>
        <h1 className="text-3xl font-bold">Analytics</h1>
        <p className="mt-2 text-sm text-slate-500 dark:text-slate-400">Weekly pace, streaks, progress trend, and estimated completion date.</p>
        <div className="mt-4 flex flex-wrap gap-2">
          <Badge>Streak: {derived.streak} days</Badge>
          <Badge>Completion: {derived.completionPercent}%</Badge>
          <Badge>Estimated: {formatDateOnly(derived.estimatedCompletionDate)}</Badge>
        </div>
      </Card>

      <div className="grid gap-4 lg:grid-cols-2">
        <Card>
          <h2 className="text-lg font-semibold">Weekly hours</h2>
          <div className="mt-4 h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={derived.weeklyHours}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="day" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="hours" fill="#2aa69d" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>

        <Card>
          <h2 className="text-lg font-semibold">Trend line</h2>
          <div className="mt-4 h-80">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={derived.weeklyHours}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="day" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="hours" stroke="#0ea5e9" strokeWidth={3} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </div>
    </div>
  )
}
