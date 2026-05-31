export type UserRole = 'brother' | 'sister' | 'admin'
export type ChapterStatus = 'not_started' | 'studying' | 'completed' | 'revision_pending'
export type RevisionStatus = 'none' | 'due' | 'done'

export type Subject = {
  completion: number
  id: string
  groupId: string
  name: string
  totalChapters: number
  color: string
  createdAt: string
}

export type Chapter = {
  id: string
  groupId: string
  subjectId: string
  subject: string
  order: number
  name: string
  status: ChapterStatus
  completionPercentage: number
  notes: string
  hoursStudied: number
  revisionStatus: RevisionStatus
  revisionDueDates: string[]
  nextRevisionAt: string | null
  lastUpdatedAt: string
  completedAt: string | null
  updatedBy: string
}

export type StudyLog = {
  id: string
  groupId: string
  userId: string
  userName: string
  subjectId: string
  chapterId: string
  chapterName: string
  subject: string
  status: ChapterStatus
  hoursStudied: number
  notes: string
  tomorrowTarget: string
  createdAt: string
}

export type RevisionItem = {
  id: string
  groupId: string
  userId: string
  subjectId: string
  chapterId: string
  chapterName: string
  subject: string
  dueDate: string
  offsetDays: number
  status: 'pending' | 'done'
  createdAt: string
  completedAt: string | null
}

export type UserProfile = {
  uid: string
  email: string
  displayName: string
  photoURL: string
  role: UserRole
  groupId: string
  lastSeenAt: string
  createdAt: string
}

export type AnalyticsSummary = {
  id: string
  groupId: string
  totalHours: number
  totalCompleted: number
  totalPending: number
  streak: number
  weeklyHours: number
  estimatedCompletionDate: string | null
  updatedAt: string
}
