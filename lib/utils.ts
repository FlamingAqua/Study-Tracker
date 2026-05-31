import { addDays, differenceInCalendarDays, format, isSameDay, parseISO, startOfDay, subDays } from 'date-fns'
import type { Chapter, StudyLog } from '@/lib/types'

export function cn(...inputs: Array<string | false | null | undefined>) {
  return inputs.filter(Boolean).join(' ')
}

export function formatDateTime(value: string | Date) {
  const date = typeof value === 'string' ? new Date(value) : value
  return format(date, 'MMM d, yyyy • h:mm a')
}

export function formatDateOnly(value: string | Date) {
  const date = typeof value === 'string' ? new Date(value) : value
  return format(date, 'MMM d, yyyy')
}

export function toISODate(value: Date = new Date()) {
  return format(value, 'yyyy-MM-dd')
}

export function daysFromNow(days: number) {
  return addDays(new Date(), days).toISOString()
}

export function getCompletionPercent(chapters: Chapter[]) {
  if (!chapters.length) return 0
  const done = chapters.filter((chapter) => chapter.status === 'completed').length
  return Math.round((done / chapters.length) * 100)
}

export function getSubjectCompletion(chapters: Chapter[], subjectId: string) {
  const list = chapters.filter((chapter) => chapter.subjectId === subjectId)
  if (!list.length) return 0
  const done = list.filter((chapter) => chapter.status === 'completed').length
  return Math.round((done / list.length) * 100)
}

export function getCurrentChapter(chapters: Chapter[]) {
  return [...chapters]
    .sort((a, b) => new Date(b.lastUpdatedAt).getTime() - new Date(a.lastUpdatedAt).getTime())
    .find((chapter) => chapter.status === 'studying' || chapter.status === 'revision_pending') || null
}

export function getPendingChapters(chapters: Chapter[]) {
  return chapters.filter((chapter) => chapter.status !== 'completed')
}

export function getRevisionQueue(chapters: Chapter[]) {
  return chapters.filter((chapter) => chapter.revisionStatus === 'due' || chapter.revisionStatus === 'none' && chapter.status === 'completed')
}

export function getStudyStreak(logs: StudyLog[]) {
  const uniqueDays = new Set(logs.map((log) => format(new Date(log.createdAt), 'yyyy-MM-dd')))
  let streak = 0
  let cursor = startOfDay(new Date())

  while (uniqueDays.has(format(cursor, 'yyyy-MM-dd'))) {
    streak += 1
    cursor = subDays(cursor, 1)
  }

  return streak
}

export function getWeeklyHours(logs: StudyLog[]) {
  const result: Array<{ day: string; hours: number }> = []
  for (let i = 6; i >= 0; i -= 1) {
    const day = subDays(new Date(), i)
    const key = format(day, 'EEE')
    const hours = logs
      .filter((log) => isSameDay(new Date(log.createdAt), day))
      .reduce((sum, log) => sum + Number(log.hoursStudied || 0), 0)
    result.push({ day: key, hours: Number(hours.toFixed(1)) })
  }
  return result
}

export function getHeatmapData(logs: StudyLog[], days = 35) {
  const map = new Map<string, number>()
  logs.forEach((log) => {
    const key = format(new Date(log.createdAt), 'yyyy-MM-dd')
    map.set(key, (map.get(key) || 0) + Number(log.hoursStudied || 0))
  })

  return Array.from({ length: days }, (_, index) => {
    const date = subDays(new Date(), days - index - 1)
    const key = format(date, 'yyyy-MM-dd')
    return {
      date: key,
      hours: Number((map.get(key) || 0).toFixed(1)),
      label: format(date, 'EEE'),
    }
  })
}

export function getEstimatedCompletionDate(chapters: Chapter[], logs: StudyLog[]) {
  const remaining = chapters.filter((chapter) => chapter.status !== 'completed').length
  const avgPerDay = Math.max(0.2, logs.reduce((sum, log) => sum + Number(log.hoursStudied || 0), 0) / Math.max(1, new Set(logs.map((log) => format(new Date(log.createdAt), 'yyyy-MM-dd'))).size))
  const chaptersPerDay = Math.max(0.2, avgPerDay / 2)
  const daysNeeded = Math.ceil(remaining / chaptersPerDay)
  return addDays(new Date(), daysNeeded)
}

export function safeDate(value?: string | null) {
  if (!value) return null
  try {
    return parseISO(value)
  } catch {
    return null
  }
}
