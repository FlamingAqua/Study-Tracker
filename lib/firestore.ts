import {
  addDoc,
  collection,
  doc,
  getDocs,
  limit,
  orderBy,
  query,
  setDoc,
  updateDoc,
  where,
  onSnapshot,
} from 'firebase/firestore'
import { db } from '@/lib/firebase'
import { DEFAULT_CHAPTERS, GROUP_ID, REVISION_OFFSETS_DAYS, SUBJECTS } from '@/lib/constants'
import type { AnalyticsSummary, Chapter, RevisionItem, StudyLog, Subject, UserProfile } from '@/lib/types'

function col(name: string) {
  return collection(db, name)
}

function withId<T extends Record<string, unknown>>(id: string, data: T) {
  const { id: _id, ...rest } = data as T & { id?: unknown }
  return { id, ...rest } as T & { id: string }
}

export async function seedDemoData() {
  const subjectSnap = await getDocs(query(col('subjects'), where('groupId', '==', GROUP_ID), limit(1)))
  if (!subjectSnap.empty) return

  const subjectWrites = SUBJECTS.map((subject) =>
    setDoc(doc(db, 'subjects', subject.id), {
      id: subject.id,
      groupId: GROUP_ID,
      name: subject.name,
      totalChapters: subject.totalChapters,
      color: subject.color,
      completion: 0,
      createdAt: new Date().toISOString(),
    } satisfies Subject)
  )

  const chapterWrites = DEFAULT_CHAPTERS.map((chapter) =>
    setDoc(doc(db, 'chapters', chapter.id), {
      id: chapter.id,
      groupId: GROUP_ID,
      subjectId: chapter.subjectId,
      subject: chapter.subject,
      order: chapter.order,
      name: chapter.name,
      status: 'not_started',
      completionPercentage: 0,
      notes: '',
      hoursStudied: 0,
      revisionStatus: 'none',
      revisionDueDates: [],
      nextRevisionAt: null,
      lastUpdatedAt: new Date().toISOString(),
      completedAt: null,
      updatedBy: 'seed',
    } satisfies Chapter)
  )

  await Promise.all([...subjectWrites, ...chapterWrites])

  await setDoc(doc(db, 'analytics', 'summary'), {
    id: 'summary',
    groupId: GROUP_ID,
    totalHours: 0,
    totalCompleted: 0,
    totalPending: DEFAULT_CHAPTERS.length,
    streak: 0,
    weeklyHours: 0,
    estimatedCompletionDate: null,
    updatedAt: new Date().toISOString(),
  } satisfies AnalyticsSummary)
}

export function listenSubjects(callback: (items: Subject[]) => void) {
  return onSnapshot(query(col('subjects'), where('groupId', '==', GROUP_ID), orderBy('name')), (snapshot) => {
    callback(snapshot.docs.map((item) => withId(item.id, item.data() as Subject)))
  })
}

export function listenChapters(callback: (items: Chapter[]) => void) {
  return onSnapshot(query(col('chapters'), where('groupId', '==', GROUP_ID)), (snapshot) => {
    callback(snapshot.docs.map((item) => withId(item.id, item.data() as Chapter)).sort((a, b) => a.subjectId.localeCompare(b.subjectId) || a.order - b.order))
  })
}

export function listenStudyLogs(callback: (items: StudyLog[]) => void) {
  return onSnapshot(query(col('study_logs'), where('groupId', '==', GROUP_ID), orderBy('createdAt')), (snapshot) => {
    callback(snapshot.docs.map((item) => withId(item.id, item.data() as StudyLog)))
  })
}

export function listenRevisionQueue(callback: (items: RevisionItem[]) => void) {
  return onSnapshot(query(col('revision_queue'), where('groupId', '==', GROUP_ID), orderBy('dueDate')), (snapshot) => {
    callback(snapshot.docs.map((item) => withId(item.id, item.data() as RevisionItem)))
  })
}

export function listenAnalytics(callback: (item: AnalyticsSummary | null) => void) {
  return onSnapshot(doc(db, 'analytics', 'summary'), (snapshot) => {
    callback(snapshot.exists() ? withId(snapshot.id, snapshot.data() as AnalyticsSummary) : null)
  })
}

export async function createStudyLog(payload: Omit<StudyLog, 'id' | 'createdAt'>) {
  await addDoc(col('study_logs'), {
    ...payload,
    createdAt: new Date().toISOString(),
  })
}

export async function updateChapterProgress(chapterId: string, data: Partial<Chapter>) {
  await updateDoc(doc(db, 'chapters', chapterId), {
    ...data,
    lastUpdatedAt: new Date().toISOString(),
  })
}

export async function upsertChapterStatus(params: {
  chapterId: string
  subjectId: string
  subject: string
  chapterName: string
  status: Chapter['status']
  completionPercentage: number
  notes: string
  hoursStudied: number
  user: UserProfile
  tomorrowTarget: string
}) {
  const { chapterId, subjectId, subject, chapterName, status, completionPercentage, notes, hoursStudied, user, tomorrowTarget } = params
  const chapterRef = doc(db, 'chapters', chapterId)
  const now = new Date().toISOString()

  let revisionDueDates: string[] = []
  let nextRevisionAt: string | null = null
  let revisionStatus: Chapter['revisionStatus'] = 'none'
  let completedAt: string | null = null

  if (status === 'completed') {
    completedAt = now
    revisionStatus = 'due'
    revisionDueDates = REVISION_OFFSETS_DAYS.map((offset) => new Date(Date.now() + offset * 24 * 60 * 60 * 1000).toISOString())
    nextRevisionAt = revisionDueDates[0] || null
  }

  if (status === 'studying' || status === 'revision_pending') {
    revisionStatus = status === 'revision_pending' ? 'due' : 'none'
  }

  await setDoc(chapterRef, {
    id: chapterId,
    groupId: GROUP_ID,
    subjectId,
    subject,
    name: chapterName,
    status,
    completionPercentage,
    notes,
    hoursStudied,
    revisionStatus,
    revisionDueDates,
    nextRevisionAt,
    lastUpdatedAt: now,
    completedAt,
    updatedBy: user.uid,
  }, { merge: true })

  await createStudyLog({
    groupId: GROUP_ID,
    userId: user.uid,
    userName: user.displayName,
    subjectId,
    chapterId,
    chapterName,
    subject,
    status,
    hoursStudied,
    notes,
    tomorrowTarget,
  })

  if (status === 'completed') {
    const revisionWrites = REVISION_OFFSETS_DAYS.map((offset) =>
      addDoc(col('revision_queue'), {
        groupId: GROUP_ID,
        userId: user.uid,
        subjectId,
        chapterId,
        chapterName,
        subject,
        dueDate: new Date(Date.now() + offset * 24 * 60 * 60 * 1000).toISOString(),
        offsetDays: offset,
        status: 'pending',
        createdAt: now,
        completedAt: null,
        id: ''
      } satisfies RevisionItem)
    )
    await Promise.all(revisionWrites)
  }
}

export async function markRevisionDone(itemId: string) {
  await updateDoc(doc(db, 'revision_queue', itemId), {
    status: 'done',
    completedAt: new Date().toISOString(),
  })
}

export async function saveAnalytics(summary: Omit<AnalyticsSummary, 'id'>) {
  await setDoc(doc(db, 'analytics', 'summary'), {
    id: 'summary',
    ...summary,
  }, { merge: true })
}
