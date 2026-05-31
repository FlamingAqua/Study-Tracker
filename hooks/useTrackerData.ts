'use client'

import { useEffect, useMemo, useState } from 'react'
import { seedDemoData, listenAnalytics, listenChapters, listenRevisionQueue, listenStudyLogs, listenSubjects } from '@/lib/firestore'
import type { AnalyticsSummary, Chapter, RevisionItem, StudyLog, Subject } from '@/lib/types'
import { getCompletionPercent, getCurrentChapter, getEstimatedCompletionDate, getHeatmapData, getPendingChapters, getStudyStreak, getSubjectCompletion, getWeeklyHours } from '@/lib/utils'
import { saveAnalytics } from '@/lib/firestore'
import { GROUP_ID } from '@/lib/constants'

export function useTrackerData() {
  const [subjects, setSubjects] = useState<Subject[]>([])
  const [chapters, setChapters] = useState<Chapter[]>([])
  const [logs, setLogs] = useState<StudyLog[]>([])
  const [revisionQueue, setRevisionQueue] = useState<RevisionItem[]>([])
  const [analytics, setAnalytics] = useState<AnalyticsSummary | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let mounted = true
    Promise.resolve(seedDemoData())
      .catch((err) => setError(err instanceof Error ? err.message : 'Failed to seed demo data'))
      .finally(() => mounted && setLoading(false))

    const unsubscribers = [
      listenSubjects(setSubjects),
      listenChapters(setChapters),
      listenStudyLogs(setLogs),
      listenRevisionQueue(setRevisionQueue),
      listenAnalytics(setAnalytics),
    ]

    return () => unsubscribers.forEach((unsubscribe) => unsubscribe())
  }, [])

  const derived = useMemo(() => {
    const completionPercent = getCompletionPercent(chapters)
    const currentChapter = getCurrentChapter(chapters)
    const pendingChapters = getPendingChapters(chapters)
    const streak = getStudyStreak(logs)
    const weeklyHours = getWeeklyHours(logs)
    const heatmap = getHeatmapData(logs)
    const estimatedCompletionDate = getEstimatedCompletionDate(chapters, logs)
    const subjectCompletion = subjects.map((subject) => ({ ...subject, completion: getSubjectCompletion(chapters, subject.id) }))
    const totalHours = Number(logs.reduce((sum, log) => sum + Number(log.hoursStudied || 0), 0).toFixed(1))
    const weeklyHoursTotal = Number(weeklyHours.reduce((sum, item) => sum + item.hours, 0).toFixed(1))
    const completedCount = chapters.filter((chapter) => chapter.status === 'completed').length
    const pendingCount = chapters.length - completedCount

    return {
      completionPercent,
      currentChapter,
      pendingChapters,
      streak,
      weeklyHours,
      heatmap,
      estimatedCompletionDate,
      subjectCompletion,
      totalHours,
      weeklyHoursTotal,
      completedCount,
      pendingCount,
    }
  }, [chapters, logs, subjects])

  useEffect(() => {
    if (chapters.length === 0) return
    void saveAnalytics({
      groupId: GROUP_ID,
      totalHours: derived.totalHours,
      totalCompleted: derived.completedCount,
      totalPending: derived.pendingCount,
      streak: derived.streak,
      weeklyHours: derived.weeklyHoursTotal,
      estimatedCompletionDate: derived.estimatedCompletionDate.toISOString(),
      updatedAt: new Date().toISOString(),
    })
  }, [chapters.length, derived.totalHours, derived.completedCount, derived.pendingCount, derived.streak, derived.weeklyHoursTotal, derived.estimatedCompletionDate])

  return { subjects, chapters, logs, revisionQueue, analytics, loading, error, derived }
}
