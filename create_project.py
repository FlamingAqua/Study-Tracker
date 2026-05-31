from pathlib import Path
from textwrap import dedent
from PIL import Image, ImageDraw

root = Path('/mnt/data/mbbs-study-tracker')

files = {
'package.json': dedent('''
{
  "name": "mbbs-study-tracker",
  "private": true,
  "version": "1.0.0",
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "clsx": "^2.1.1",
    "date-fns": "^3.6.0",
    "firebase": "^11.0.2",
    "html2canvas": "^1.4.1",
    "jspdf": "^3.0.2",
    "lucide-react": "^0.460.0",
    "next": "^15.3.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "recharts": "^2.15.4",
    "tailwind-merge": "^2.5.5"
  },
  "devDependencies": {
    "@types/node": "^22.10.0",
    "@types/react": "^19.0.2",
    "@types/react-dom": "^19.0.2",
    "autoprefixer": "^10.4.20",
    "postcss": "^8.4.49",
    "tailwindcss": "^3.4.17",
    "typescript": "^5.7.2"
  }
}
'''),
'next.config.js': dedent('''
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  trailingSlash: true,
  images: {
    unoptimized: true,
  },
  reactStrictMode: true,
}

module.exports = nextConfig
'''),
'tsconfig.json': dedent('''
{
  "compilerOptions": {
    "target": "es2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": false,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": {
      "@/*": ["./*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
'''),
'postcss.config.js': dedent('''
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
'''),
'tailwind.config.ts': dedent('''
import type { Config } from 'tailwindcss'

const config: Config = {
  darkMode: ['class'],
  content: [
    './app/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './hooks/**/*.{ts,tsx}',
    './lib/**/*.{ts,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#eefbf9',
          100: '#d3f6f1',
          200: '#a7ebe2',
          300: '#78d8cf',
          400: '#4bc0b5',
          500: '#2aa69d',
          600: '#1f827d',
          700: '#1d6864',
          800: '#1d5552',
          900: '#184746',
        },
      },
      boxShadow: {
        soft: '0 10px 30px rgba(15, 23, 42, 0.08)',
      },
      backgroundImage: {
        'medical-gradient': 'linear-gradient(135deg, rgba(42,166,157,0.12), rgba(255,255,255,0.8))',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(8px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
      },
      animation: {
        fadeIn: 'fadeIn 0.25s ease-out',
      },
    },
  },
  plugins: [],
}

export default config
'''),
'.env.example': dedent('''
NEXT_PUBLIC_FIREBASE_API_KEY=your_api_key
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your_auth_domain
NEXT_PUBLIC_FIREBASE_PROJECT_ID=your_project_id
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your_storage_bucket
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=your_messaging_sender_id
NEXT_PUBLIC_FIREBASE_APP_ID=your_app_id
NEXT_PUBLIC_FIREBASE_MEASUREMENT_ID=your_measurement_id
NEXT_PUBLIC_GROUP_ID=mbbs-family-001
NEXT_PUBLIC_ALLOWED_EMAILS=brother@example.com,sister@example.com
'''),
'firebase.json': dedent('''
{
  "hosting": {
    "public": "out",
    "ignore": [
      "firebase.json",
      "**/.*",
      "**/node_modules/**"
    ],
    "rewrites": [
      {
        "source": "**",
        "destination": "/index.html"
      }
    ]
  }
}
'''),
'firestore.rules': dedent('''
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    function signedIn() {
      return request.auth != null;
    }

    function isAllowedEmail() {
      return signedIn() && request.auth.token.email in [
        'brother@example.com',
        'sister@example.com'
      ];
    }

    function isGroupDoc() {
      return resource.data.groupId == 'mbbs-family-001' || request.resource.data.groupId == 'mbbs-family-001';
    }

    match /users/{userId} {
      allow read, write: if isAllowedEmail() && request.auth.uid == userId;
    }

    match /subjects/{subjectId} {
      allow read: if isAllowedEmail() && resource.data.groupId == 'mbbs-family-001';
      allow create, update, delete: if isAllowedEmail() && isGroupDoc();
    }

    match /chapters/{chapterId} {
      allow read: if isAllowedEmail() && resource.data.groupId == 'mbbs-family-001';
      allow create, update, delete: if isAllowedEmail() && isGroupDoc();
    }

    match /study_logs/{logId} {
      allow read: if isAllowedEmail() && resource.data.groupId == 'mbbs-family-001';
      allow create, update, delete: if isAllowedEmail() && isGroupDoc();
    }

    match /revision_queue/{itemId} {
      allow read: if isAllowedEmail() && resource.data.groupId == 'mbbs-family-001';
      allow create, update, delete: if isAllowedEmail() && isGroupDoc();
    }

    match /analytics/{docId} {
      allow read: if isAllowedEmail() && resource.data.groupId == 'mbbs-family-001';
      allow create, update, delete: if isAllowedEmail() && isGroupDoc();
    }
  }
}
'''),
'public/manifest.json': dedent('''
{
  "name": "MBBS Study Tracker",
  "short_name": "Study Tracker",
  "description": "Real-time MBBS study tracker for family accountability.",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#f8fafc",
  "theme_color": "#2aa69d",
  "icons": [
    {
      "src": "/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
'''),
'public/sw.js': dedent('''
const CACHE_NAME = 'mbbs-study-tracker-v1'
const ASSETS = ['/', '/manifest.json']

self.addEventListener('install', (event) => {
  event.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS)))
})

self.addEventListener('activate', (event) => {
  event.waitUntil(self.clients.claim())
})

self.addEventListener('fetch', (event) => {
  const { request } = event
  if (request.method !== 'GET') return
  event.respondWith(
    caches.match(request).then((cached) => {
      return (
        cached ||
        fetch(request)
          .then((response) => {
            const copy = response.clone()
            caches.open(CACHE_NAME).then((cache) => cache.put(request, copy))
            return response
          })
          .catch(() => caches.match('/'))
      )
    })
  )
})
'''),
'lib/constants.ts': dedent('''
import { generateChapterSeed } from '@/lib/seed-data'

export const GROUP_ID = process.env.NEXT_PUBLIC_GROUP_ID || 'mbbs-family-001'

export const ALLOWED_EMAILS = (process.env.NEXT_PUBLIC_ALLOWED_EMAILS || 'brother@example.com,sister@example.com')
  .split(',')
  .map((item) => item.trim().toLowerCase())
  .filter(Boolean)

export const SUBJECTS = [
  {
    id: 'forensic-medicine',
    name: 'Forensic Medicine',
    totalChapters: 60,
    color: 'from-cyan-500 to-teal-600',
  },
  {
    id: 'community-medicine',
    name: 'Community Medicine',
    totalChapters: 22,
    color: 'from-emerald-500 to-green-600',
  },
] as const

export const REVISION_OFFSETS_DAYS = [1, 3, 7, 21]

export const DEFAULT_CHAPTERS = generateChapterSeed()
'''),
'lib/seed-data.ts': dedent('''
export type SeedChapter = {
  id: string
  subjectId: 'forensic-medicine' | 'community-medicine'
  subject: string
  order: number
  name: string
}

export function generateChapterSeed(): SeedChapter[] {
  const forensic = Array.from({ length: 60 }, (_, index) => ({
    id: `fm-${String(index + 1).padStart(2, '0')}`,
    subjectId: 'forensic-medicine' as const,
    subject: 'Forensic Medicine',
    order: index + 1,
    name: `Chapter ${String(index + 1).padStart(2, '0')}`,
  }))

  const community = Array.from({ length: 22 }, (_, index) => ({
    id: `cm-${String(index + 1).padStart(2, '0')}`,
    subjectId: 'community-medicine' as const,
    subject: 'Community Medicine',
    order: index + 1,
    name: `Chapter ${String(index + 1).padStart(2, '0')}`,
  }))

  return [...forensic, ...community]
}
'''),
'lib/types.ts': dedent('''
export type UserRole = 'brother' | 'sister' | 'admin'
export type ChapterStatus = 'not_started' | 'studying' | 'completed' | 'revision_pending'
export type RevisionStatus = 'none' | 'due' | 'done'

export type Subject = {
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
'''),
'lib/utils.ts': dedent('''
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
'''),
'lib/firebase.ts': dedent('''
import { initializeApp, getApps, getApp } from 'firebase/app'
import { getAuth, GoogleAuthProvider } from 'firebase/auth'
import { collection, getFirestore } from 'firebase/firestore'

const firebaseConfig = {
  apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY,
  authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID,
  storageBucket: process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.NEXT_PUBLIC_FIREBASE_APP_ID,
  measurementId: process.env.NEXT_PUBLIC_FIREBASE_MEASUREMENT_ID,
}

const app = getApps().length ? getApp() : initializeApp(firebaseConfig)
export const auth = getAuth(app)
export const db = getFirestore(app)
export const googleProvider = new GoogleAuthProvider()
googleProvider.setCustomParameters({ prompt: 'select_account' })

export const collections = {
  users: collection(db, 'users'),
  subjects: collection(db, 'subjects'),
  chapters: collection(db, 'chapters'),
  studyLogs: collection(db, 'study_logs'),
  revisionQueue: collection(db, 'revision_queue'),
  analytics: collection(db, 'analytics'),
}
'''),
'lib/auth.ts': dedent('''
import { onIdTokenChanged, signInWithPopup, signOut, User } from 'firebase/auth'
import { doc, getDoc, serverTimestamp, setDoc } from 'firebase/firestore'
import { auth, db, googleProvider } from '@/lib/firebase'
import { ALLOWED_EMAILS, GROUP_ID } from '@/lib/constants'
import type { UserProfile } from '@/lib/types'

export function isAllowedUser(email?: string | null) {
  if (!email) return false
  return ALLOWED_EMAILS.includes(email.toLowerCase())
}

export async function signInWithGoogle() {
  const result = await signInWithPopup(auth, googleProvider)
  const email = result.user.email
  if (!isAllowedUser(email)) {
    await signOut(auth)
    throw new Error('This account is not authorized for the tracker.')
  }

  await upsertUserProfile(result.user)
  return result.user
}

export async function signOutUser() {
  await signOut(auth)
}

export function listenAuthState(callback: (user: User | null) => void) {
  return onIdTokenChanged(auth, callback)
}

export async function upsertUserProfile(user: User) {
  const profileRef = doc(db, 'users', user.uid)
  const snap = await getDoc(profileRef)
  const now = new Date().toISOString()
  const role = user.email?.toLowerCase().includes('brother') ? 'brother' : user.email?.toLowerCase().includes('sister') ? 'sister' : 'admin'

  const payload: UserProfile = {
    uid: user.uid,
    email: user.email || '',
    displayName: user.displayName || 'Family Member',
    photoURL: user.photoURL || '',
    role,
    groupId: GROUP_ID,
    lastSeenAt: now,
    createdAt: snap.exists() ? (snap.data() as UserProfile).createdAt : now,
  }

  await setDoc(profileRef, payload, { merge: true })
}
'''),
'lib/firestore.ts': dedent('''
import {
  addDoc,
  collection,
  doc,
  getDocs,
  limit,
  orderBy,
  query,
  serverTimestamp,
  setDoc,
  updateDoc,
  where,
  onSnapshot,
  Timestamp,
} from 'firebase/firestore'
import { db } from '@/lib/firebase'
import { DEFAULT_CHAPTERS, GROUP_ID, REVISION_OFFSETS_DAYS, SUBJECTS } from '@/lib/constants'
import type { AnalyticsSummary, Chapter, RevisionItem, StudyLog, Subject, UserProfile } from '@/lib/types'
import { toISODate } from '@/lib/utils'

function col(name: string) {
  return collection(db, name)
}

function withId<T extends Record<string, unknown>>(id: string, data: T) {
  return { id, ...data } as T & { id: string }
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
    callback(snapshot.docs.map((item) => ({ id: item.id, ...(item.data() as Subject) })))
  })
}

export function listenChapters(callback: (items: Chapter[]) => void) {
  return onSnapshot(query(col('chapters'), where('groupId', '==', GROUP_ID), orderBy('subjectId'), orderBy('order')), (snapshot) => {
    callback(snapshot.docs.map((item) => ({ id: item.id, ...(item.data() as Chapter) })))
  })
}

export function listenStudyLogs(callback: (items: StudyLog[]) => void) {
  return onSnapshot(query(col('study_logs'), where('groupId', '==', GROUP_ID), orderBy('createdAt')), (snapshot) => {
    callback(snapshot.docs.map((item) => ({ id: item.id, ...(item.data() as StudyLog) })))
  })
}

export function listenRevisionQueue(callback: (items: RevisionItem[]) => void) {
  return onSnapshot(query(col('revision_queue'), where('groupId', '==', GROUP_ID), orderBy('dueDate')), (snapshot) => {
    callback(snapshot.docs.map((item) => ({ id: item.id, ...(item.data() as RevisionItem) })))
  })
}

export function listenAnalytics(callback: (item: AnalyticsSummary | null) => void) {
  return onSnapshot(doc(db, 'analytics', 'summary'), (snapshot) => {
    callback(snapshot.exists() ? ({ id: snapshot.id, ...(snapshot.data() as AnalyticsSummary) }) : null)
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
    order: 0,
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
'''),
'hooks/useTheme.ts': dedent('''
'use client'

import { createContext, useContext, useEffect, useMemo, useState } from 'react'

type Theme = 'light' | 'dark'

type ThemeContextValue = {
  theme: Theme
  toggleTheme: () => void
  setTheme: (theme: Theme) => void
}

const ThemeContext = createContext<ThemeContextValue | null>(null)

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<Theme>('light')

  useEffect(() => {
    const stored = window.localStorage.getItem('mbbs-theme') as Theme | null
    if (stored) setTheme(stored)
  }, [])

  useEffect(() => {
    document.documentElement.classList.toggle('dark', theme === 'dark')
    window.localStorage.setItem('mbbs-theme', theme)
  }, [theme])

  const value = useMemo<ThemeContextValue>(() => ({
    theme,
    toggleTheme: () => setTheme((current) => (current === 'light' ? 'dark' : 'light')),
    setTheme,
  }), [theme])

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>
}

export function useTheme() {
  const value = useContext(ThemeContext)
  if (!value) throw new Error('useTheme must be used inside ThemeProvider')
  return value
}
'''),
'components/providers.tsx': dedent('''
'use client'

import { ThemeProvider } from '@/hooks/useTheme'
import { ToastProvider } from '@/components/ui/toast'

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider>
      <ToastProvider>{children}</ToastProvider>
    </ThemeProvider>
  )
}
'''),
'components/ui/toast.tsx': dedent('''
'use client'

import { createContext, useContext, useMemo, useState } from 'react'
import { CheckCircle2, AlertTriangle, Info } from 'lucide-react'
import { cn } from '@/lib/utils'

type ToastVariant = 'success' | 'error' | 'info'

type ToastItem = { id: string; title: string; description?: string; variant: ToastVariant }

type ToastContextValue = {
  toast: (item: Omit<ToastItem, 'id'>) => void
}

const ToastContext = createContext<ToastContextValue | null>(null)

export function ToastProvider({ children }: { children: React.ReactNode }) {
  const [toasts, setToasts] = useState<ToastItem[]>([])

  const value = useMemo<ToastContextValue>(() => ({
    toast: (item) => {
      const id = crypto.randomUUID()
      setToasts((current) => [...current, { ...item, id }])
      window.setTimeout(() => {
        setToasts((current) => current.filter((toast) => toast.id !== id))
      }, 3200)
    },
  }), [])

  return (
    <ToastContext.Provider value={value}>
      {children}
      <div className="fixed right-4 top-4 z-50 space-y-3">
        {toasts.map((toast) => (
          <div
            key={toast.id}
            className={cn(
              'w-[min(92vw,380px)] rounded-2xl border bg-white/90 p-4 shadow-soft backdrop-blur dark:border-slate-700 dark:bg-slate-900/90',
              'animate-fadeIn'
            )}
          >
            <div className="flex items-start gap-3">
              <div className={cn('mt-0.5 rounded-full p-1.5', toast.variant === 'success' && 'bg-emerald-100 text-emerald-700', toast.variant === 'error' && 'bg-rose-100 text-rose-700', toast.variant === 'info' && 'bg-brand-100 text-brand-700')}>
                {toast.variant === 'success' && <CheckCircle2 className="h-4 w-4" />}
                {toast.variant === 'error' && <AlertTriangle className="h-4 w-4" />}
                {toast.variant === 'info' && <Info className="h-4 w-4" />}
              </div>
              <div>
                <p className="font-semibold text-slate-900 dark:text-slate-100">{toast.title}</p>
                {toast.description ? <p className="mt-1 text-sm text-slate-600 dark:text-slate-300">{toast.description}</p> : null}
              </div>
            </div>
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  )
}

export function useToast() {
  const value = useContext(ToastContext)
  if (!value) throw new Error('useToast must be used inside ToastProvider')
  return value
}
'''),
'components/ui/button.tsx': dedent('''
'use client'

import { cn } from '@/lib/utils'
import type { ButtonHTMLAttributes } from 'react'

export function Button({ className, ...props }: ButtonHTMLAttributes<HTMLButtonElement>) {
  return (
    <button
      className={cn(
        'inline-flex items-center justify-center rounded-2xl bg-brand-600 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-brand-700 active:scale-[0.99] disabled:cursor-not-allowed disabled:opacity-60',
        className
      )}
      {...props}
    />
  )
}
'''),
'components/ui/card.tsx': dedent('''
import { cn } from '@/lib/utils'

export function Card({ className, children }: { className?: string; children: React.ReactNode }) {
  return <div className={cn('rounded-3xl border border-white/60 bg-white/80 p-5 shadow-soft backdrop-blur dark:border-slate-800 dark:bg-slate-900/80', className)}>{children}</div>
}
'''),
'components/ui/input.tsx': dedent('''
'use client'

import { cn } from '@/lib/utils'
import type { InputHTMLAttributes } from 'react'

export function Input({ className, ...props }: InputHTMLAttributes<HTMLInputElement>) {
  return <input className={cn('w-full rounded-2xl border border-slate-200 bg-white px-4 py-2.5 text-sm outline-none transition focus:border-brand-500 focus:ring-2 focus:ring-brand-100 dark:border-slate-700 dark:bg-slate-950 dark:text-slate-100', className)} {...props} />
}
'''),
'components/ui/select.tsx': dedent('''
'use client'

import { cn } from '@/lib/utils'
import type { SelectHTMLAttributes } from 'react'

export function Select({ className, ...props }: SelectHTMLAttributes<HTMLSelectElement>) {
  return <select className={cn('w-full rounded-2xl border border-slate-200 bg-white px-4 py-2.5 text-sm outline-none transition focus:border-brand-500 focus:ring-2 focus:ring-brand-100 dark:border-slate-700 dark:bg-slate-950 dark:text-slate-100', className)} {...props} />
}
'''),
'components/ui/badge.tsx': dedent('''
import { cn } from '@/lib/utils'

export function Badge({ className, children }: { className?: string; children: React.ReactNode }) {
  return <span className={cn('inline-flex items-center rounded-full px-3 py-1 text-xs font-semibold', 'bg-brand-50 text-brand-700 dark:bg-brand-950 dark:text-brand-200', className)}>{children}</span>
}
'''),
'components/ui/progress.tsx': dedent('''
import { cn } from '@/lib/utils'

export function Progress({ value, className }: { value: number; className?: string }) {
  return (
    <div className={cn('h-2.5 w-full rounded-full bg-slate-200 dark:bg-slate-800', className)}>
      <div className="h-2.5 rounded-full bg-gradient-to-r from-brand-500 to-emerald-500 transition-all" style={{ width: `${Math.max(0, Math.min(100, value))}%` }} />
    </div>
  )
}
'''),
'components/layout/Shell.tsx': dedent('''
'use client'

import Link from 'next/link'
import { BookOpenCheck, CalendarDays, LayoutDashboard, LogOut, MoonStar, Sparkles, SunMedium } from 'lucide-react'
import { usePathname } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'
import { useTheme } from '@/hooks/useTheme'
import { signOutUser } from '@/lib/auth'
import { useToast } from '@/components/ui/toast'

const nav = [
  { href: '/', label: 'Dashboard', icon: LayoutDashboard },
  { href: '/chapters', label: 'Chapters', icon: BookOpenCheck },
  { href: '/analytics', label: 'Analytics', icon: CalendarDays },
  { href: '/settings', label: 'Settings', icon: Sparkles },
]

export function Shell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname()
  const { theme, toggleTheme } = useTheme()
  const { toast } = useToast()

  async function handleLogout() {
    await signOutUser()
    toast({ title: 'Signed out', description: 'You are logged out safely.', variant: 'info' })
  }

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,_rgba(42,166,157,0.15),_transparent_42%),linear-gradient(to_bottom,_#f8fafc,_#eefbf9)] text-slate-900 dark:bg-[radial-gradient(circle_at_top,_rgba(42,166,157,0.15),_transparent_42%),linear-gradient(to_bottom,_#020617,_#0f172a)] dark:text-slate-100">
      <header className="sticky top-0 z-30 border-b border-white/50 bg-white/70 backdrop-blur dark:border-slate-800 dark:bg-slate-950/70">
        <div className="mx-auto flex max-w-7xl items-center justify-between gap-3 px-4 py-3 lg:px-8">
          <Link href="/" className="flex items-center gap-3">
            <div className="grid h-11 w-11 place-items-center rounded-2xl bg-gradient-to-br from-brand-500 to-emerald-500 text-white shadow-soft">
              <BookOpenCheck className="h-5 w-5" />
            </div>
            <div>
              <p className="text-sm font-semibold text-slate-900 dark:text-slate-100">MBBS Study Tracker</p>
              <p className="text-xs text-slate-500 dark:text-slate-400">Real-time family accountability</p>
            </div>
          </Link>

          <div className="hidden items-center gap-2 md:flex">
            {nav.map((item) => {
              const Icon = item.icon
              const active = pathname === item.href
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={cn(
                    'inline-flex items-center gap-2 rounded-2xl px-4 py-2 text-sm font-medium transition',
                    active ? 'bg-brand-600 text-white shadow-soft' : 'text-slate-600 hover:bg-white hover:text-slate-900 dark:text-slate-300 dark:hover:bg-slate-900 dark:hover:text-white'
                  )}
                >
                  <Icon className="h-4 w-4" />
                  {item.label}
                </Link>
              )
            })}
          </div>

          <div className="flex items-center gap-2">
            <Button type="button" className="bg-white text-slate-900 hover:bg-slate-100 dark:bg-slate-900 dark:text-slate-100" onClick={toggleTheme}>
              {theme === 'dark' ? <SunMedium className="h-4 w-4" /> : <MoonStar className="h-4 w-4" />}
              <span className="ml-2 hidden sm:inline">{theme === 'dark' ? 'Light' : 'Dark'}</span>
            </Button>
            <Button type="button" className="bg-rose-600 hover:bg-rose-700" onClick={handleLogout}>
              <LogOut className="h-4 w-4" />
              <span className="ml-2 hidden sm:inline">Logout</span>
            </Button>
          </div>
        </div>

        <div className="mx-auto flex max-w-7xl gap-2 overflow-x-auto px-4 pb-3 md:hidden">
          {nav.map((item) => {
            const Icon = item.icon
            const active = pathname === item.href
            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  'inline-flex min-w-fit items-center gap-2 rounded-full px-4 py-2 text-sm font-medium transition',
                  active ? 'bg-brand-600 text-white' : 'bg-white text-slate-600 dark:bg-slate-900 dark:text-slate-300'
                )}
              >
                <Icon className="h-4 w-4" />
                {item.label}
              </Link>
            )
          })}
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-4 py-6 lg:px-8">{children}</main>
    </div>
  )
}
'''),
'components/auth/LoginCard.tsx': dedent('''
'use client'

import { ShieldCheck, Chrome, Sparkles } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { signInWithGoogle } from '@/lib/auth'
import { useToast } from '@/components/ui/toast'

export function LoginCard() {
  const { toast } = useToast()

  async function handleSignIn() {
    try {
      await signInWithGoogle()
      toast({ title: 'Welcome back', description: 'Syncing your latest study progress.', variant: 'success' })
    } catch (error) {
      toast({ title: 'Login failed', description: error instanceof Error ? error.message : 'Please try again.', variant: 'error' })
    }
  }

  return (
    <div className="mx-auto grid min-h-[calc(100vh-8rem)] max-w-5xl place-items-center">
      <Card className="w-full max-w-3xl overflow-hidden p-0">
        <div className="grid gap-0 lg:grid-cols-2">
          <div className="bg-gradient-to-br from-brand-600 to-emerald-600 p-8 text-white">
            <div className="inline-flex items-center gap-2 rounded-full bg-white/15 px-3 py-1 text-xs font-semibold">
              <Sparkles className="h-3.5 w-3.5" />
              Medical study accountability
            </div>
            <h1 className="mt-5 text-3xl font-bold leading-tight">Track chapters, study hours, revisions, and streaks in real time.</h1>
            <p className="mt-4 text-sm leading-6 text-white/90">Built for a sister in MBBS and a brother who wants a clear, live view of progress, revision needs, and daily consistency.</p>
            <div className="mt-8 space-y-3 text-sm">
              <div className="flex items-center gap-2"><ShieldCheck className="h-4 w-4" /> Authorized Google accounts only</div>
              <div className="flex items-center gap-2"><ShieldCheck className="h-4 w-4" /> Realtime Firestore sync</div>
              <div className="flex items-center gap-2"><ShieldCheck className="h-4 w-4" /> Mobile-friendly dashboard</div>
            </div>
          </div>

          <div className="flex flex-col justify-center p-8">
            <h2 className="text-2xl font-bold text-slate-900 dark:text-slate-100">Sign in with Google</h2>
            <p className="mt-2 text-sm text-slate-500 dark:text-slate-400">Use one of the approved family accounts to access the tracker.</p>
            <Button className="mt-6 w-full" onClick={handleSignIn}>
              <Chrome className="h-4 w-4" />
              <span className="ml-2">Continue with Google</span>
            </Button>
            <p className="mt-5 text-xs text-slate-500 dark:text-slate-400">Tip: After signing in, the dashboard starts listening to Firestore updates instantly.</p>
          </div>
        </div>
      </Card>
    </div>
  )
}
'''),
'components/auth/AuthGate.tsx': dedent('''
'use client'

import { onAuthStateChanged } from 'firebase/auth'
import { useEffect, useState } from 'react'
import { auth } from '@/lib/firebase'
import { isAllowedUser, upsertUserProfile } from '@/lib/auth'
import { LoginCard } from '@/components/auth/LoginCard'
import { useToast } from '@/components/ui/toast'
import type { User } from 'firebase/auth'

export function AuthGate({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const { toast } = useToast()

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (firebaseUser) => {
      setLoading(true)
      try {
        if (firebaseUser?.email && isAllowedUser(firebaseUser.email)) {
          await upsertUserProfile(firebaseUser)
          setUser(firebaseUser)
        } else {
          setUser(null)
        }
      } catch (error) {
        toast({ title: 'Auth error', description: error instanceof Error ? error.message : 'Could not verify account.', variant: 'error' })
        setUser(null)
      } finally {
        setLoading(false)
      }
    })
    return () => unsubscribe()
  }, [toast])

  if (loading) {
    return <div className="grid min-h-[70vh] place-items-center text-slate-500">Loading secure session…</div>
  }

  if (!user) return <LoginCard />

  return <>{children}</>
}
'''),
'hooks/useTrackerData.ts': dedent('''
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
'''),
'lib/pdf.ts': dedent('''
'use client'

import html2canvas from 'html2canvas'
import jsPDF from 'jspdf'

export async function exportElementToPdf(elementId: string, fileName = 'mbbs-study-progress.pdf') {
  const element = document.getElementById(elementId)
  if (!element) throw new Error('PDF source element not found')

  const canvas = await html2canvas(element, { scale: 2, useCORS: true })
  const imgData = canvas.toDataURL('image/png')
  const pdf = new jsPDF('p', 'mm', 'a4')
  const pageWidth = pdf.internal.pageSize.getWidth()
  const pageHeight = (canvas.height * pageWidth) / canvas.width

  pdf.addImage(imgData, 'PNG', 0, 0, pageWidth, pageHeight)
  pdf.save(fileName)
}
'''),
'lib/notifications.ts': dedent('''
'use client'

export async function enableBrowserNotifications() {
  if (!('Notification' in window)) {
    throw new Error('Notifications are not supported in this browser.')
  }
  const permission = await Notification.requestPermission()
  if (permission !== 'granted') {
    throw new Error('Notification permission was not granted.')
  }
  return true
}

export function sendBrowserNotification(title: string, body: string) {
  if ('Notification' in window && Notification.permission === 'granted') {
    new Notification(title, { body })
  }
}
'''),
'components/dashboard/Dashboard.tsx': dedent('''
'use client'

import { useMemo, useState } from 'react'
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
              <p className="mt-2 max-w-2xl text-sm text-slate-500 dark:text-slate-400">Realtime view for brother + sister. Updates appear instantly when a chapter is changed on mobile.</p>
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
          <h2 className="text-lg font-semibold">AI study assistant placeholder</h2>
          <p className="mt-2 text-sm text-slate-500 dark:text-slate-400">This space can later hold a smart planner, viva prep helper, or question generator.</p>
          <div className="mt-4 rounded-3xl border border-dashed border-brand-300 bg-brand-50/50 p-5 dark:border-brand-900 dark:bg-brand-950/30">
            <p className="text-sm font-medium text-brand-700 dark:text-brand-300">Suggested prompt</p>
            <p className="mt-2 text-sm text-slate-600 dark:text-slate-300">“Summarize today’s chapter into viva points and generate 10 revision questions.”</p>
          </div>
          <StudyTimer onManualSave={async (minutes) => {
            toast({ title: 'Timer saved', description: `${minutes} minutes logged locally.`, variant: 'info' })
          }} />
          <div className="mt-4 rounded-2xl bg-slate-50 p-4 text-sm text-slate-600 dark:bg-slate-800/60 dark:text-slate-300">
            <p className="font-semibold text-slate-900 dark:text-slate-100">Realtime note</p>
            <p className="mt-1">Every update is written to Firestore, so the brother’s laptop view refreshes instantly through snapshot listeners.</p>
          </div>
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

function Metric({ icon: Icon, title, value, caption }: { icon: React.ComponentType<{ className?: string }>; title: string; value: string; caption: string }) {
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
'''),
'components/dashboard/StudyTimer.tsx': dedent('''
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
'''),
'hooks/useUserProfile.ts': dedent('''
'use client'

import { useEffect, useState } from 'react'
import { onAuthStateChanged } from 'firebase/auth'
import { doc, onSnapshot } from 'firebase/firestore'
import { auth, db } from '@/lib/firebase'
import type { UserProfile } from '@/lib/types'

export function useUserProfile() {
  const [profile, setProfile] = useState<UserProfile | null>(null)

  useEffect(() => {
    const unsubscribeAuth = onAuthStateChanged(auth, (user) => {
      if (!user) {
        setProfile(null)
        return
      }

      const profileRef = doc(db, 'users', user.uid)
      const unsubscribeProfile = onSnapshot(profileRef, (snapshot) => {
        setProfile(snapshot.exists() ? (snapshot.data() as UserProfile) : null)
      })

      return () => unsubscribeProfile()
    })

    return () => unsubscribeAuth()
  }, [])

  return { profile }
}
'''),
'app/layout.tsx': dedent('''
import './globals.css'
import type { Metadata } from 'next'
import { Providers } from '@/components/providers'

export const metadata: Metadata = {
  title: 'MBBS Study Tracker',
  description: 'Real-time MBBS study tracker for family accountability.',
  manifest: '/manifest.json',
}

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  )
}
'''),
'app/globals.css': dedent('''
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  color-scheme: light;
}

html.dark {
  color-scheme: dark;
}

body {
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

* {
  box-sizing: border-box;
}

::selection {
  background: rgba(42, 166, 157, 0.25);
}
'''),
'app/page.tsx': dedent('''
'use client'

import { AuthGate } from '@/components/auth/AuthGate'
import { Shell } from '@/components/layout/Shell'
import { Dashboard } from '@/components/dashboard/Dashboard'

export default function Page() {
  return (
    <AuthGate>
      <Shell>
        <Dashboard />
      </Shell>
    </AuthGate>
  )
}
'''),
'app/chapters/page.tsx': dedent('''
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
'''),
'app/analytics/page.tsx': dedent('''
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
'''),
'app/settings/page.tsx': dedent('''
'use client'

import { AuthGate } from '@/components/auth/AuthGate'
import { Shell } from '@/components/layout/Shell'
import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { useTheme } from '@/hooks/useTheme'
import { useToast } from '@/components/ui/toast'
import { enableBrowserNotifications } from '@/lib/notifications'
import { seedDemoData } from '@/lib/firestore'
import { useUserProfile } from '@/hooks/useUserProfile'
import { exportElementToPdf } from '@/lib/pdf'
import { toISODate } from '@/lib/utils'

export default function SettingsPage() {
  return <AuthGate><Shell><SettingsContent /></Shell></AuthGate>
}

function SettingsContent() {
  const { theme, toggleTheme } = useTheme()
  const { toast } = useToast()
  const { profile } = useUserProfile()

  async function handleSeed() {
    try {
      await seedDemoData()
      toast({ title: 'Seed completed', description: 'Default subjects and chapters are ready.', variant: 'success' })
    } catch (error) {
      toast({ title: 'Seed failed', description: error instanceof Error ? error.message : 'Could not seed demo data.', variant: 'error' })
    }
  }

  async function handlePdf() {
    try {
      await exportElementToPdf('dashboard-export', `mbbs-progress-${toISODate()}.pdf`)
      toast({ title: 'PDF exported', description: 'Report downloaded.', variant: 'success' })
    } catch (error) {
      toast({ title: 'Export failed', description: error instanceof Error ? error.message : 'Could not export PDF.', variant: 'error' })
    }
  }

  async function handleNotifications() {
    try {
      await enableBrowserNotifications()
      toast({ title: 'Notifications enabled', description: 'Browser reminders are now active.', variant: 'success' })
    } catch (error) {
      toast({ title: 'Notification error', description: error instanceof Error ? error.message : 'Could not enable notifications.', variant: 'error' })
    }
  }

  return (
    <div className="space-y-6">
      <Card>
        <h1 className="text-3xl font-bold">Settings</h1>
        <p className="mt-2 text-sm text-slate-500 dark:text-slate-400">Theme, notifications, seed data, and report export.</p>
      </Card>

      <Card>
        <div className="grid gap-4 md:grid-cols-2">
          <div>
            <p className="text-sm font-semibold">Signed in as</p>
            <p className="mt-1 text-sm text-slate-500">{profile?.displayName || 'Loading profile…'}</p>
            <p className="text-sm text-slate-500">{profile?.email}</p>
          </div>
          <div className="flex flex-wrap gap-3 md:justify-end">
            <Button onClick={toggleTheme}>Toggle {theme === 'dark' ? 'light' : 'dark'} mode</Button>
            <Button className="bg-white text-slate-900 hover:bg-slate-100 dark:bg-slate-900 dark:text-slate-100" onClick={handleNotifications}>Enable reminders</Button>
            <Button className="bg-slate-900 hover:bg-slate-800 dark:bg-white dark:text-slate-900" onClick={handlePdf}>Export PDF</Button>
            <Button className="bg-emerald-600 hover:bg-emerald-700" onClick={handleSeed}>Seed default data</Button>
          </div>
        </div>
      </Card>
    </div>
  )
}
'''),
'components/layout/index.ts': 'export * from "./Shell"\n',
'README.md': dedent('''
# MBBS Study Tracker

A static Next.js + Firebase web app for realtime MBBS chapter tracking, family accountability, revision reminders, analytics, and mobile-first progress updates.

## 1) Install

```bash
npm install
```

## 2) Environment variables

Copy `.env.example` to `.env.local` and fill in your Firebase web app values.

## 3) Firebase setup

1. Create a Firebase project.
2. Enable **Authentication → Google**.
3. Create a Firestore database.
4. Add a Web app and copy its config into `.env.local`.
5. Replace the placeholder emails in `firestore.rules` with your real brother and sister Google account emails.
6. Publish the rules.

## 4) Run locally

```bash
npm run dev
```

## 5) Build for Firebase Hosting

```bash
npm run build
```

The build outputs the static site into `out/` because `next.config.js` uses `output: 'export'`.

## 6) Deploy

```bash
firebase init hosting
firebase deploy
```

Use `out` as the public directory.

## 7) Firestore schema

Collections used:

- `users`
- `subjects`
- `chapters`
- `study_logs`
- `revision_queue`
- `analytics`

All records are scoped by `groupId` so the brother and sister share one live workspace.

## 8) Notes

- This app uses Firestore realtime listeners, not SSR.
- It is static-export compatible.
- The PWA manifest and service worker are included.
- Push notifications are browser-notification based; full remote push would need FCM + a backend.

## 9) Suggested Firebase rules update

Replace the placeholder emails in `firestore.rules` with the real authorized accounts.

## 10) First-seed data

The app seeds default subjects and chapters from the UI when a signed-in authorized user opens it.
'''),
}

# write files
for rel, content in files.items():
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.lstrip('\n'), encoding='utf-8')

# Create simple icons
for size in [192, 512]:
    img = Image.new('RGBA', (size, size), (42, 166, 157, 255))
    draw = ImageDraw.Draw(img)
    # white rounded card
    pad = size // 8
    draw.rounded_rectangle((pad, pad, size - pad, size - pad), radius=size // 8, fill=(255, 255, 255, 255))
    # teal medical cross
    c = size // 2
    cross_w = size // 10
    cross_h = size // 4
    draw.rounded_rectangle((c - cross_w//2, c - cross_h//2, c + cross_w//2, c + cross_h//2), radius=size//30, fill=(42, 166, 157, 255))
    draw.rounded_rectangle((c - cross_h//2, c - cross_w//2, c + cross_h//2, c + cross_w//2), radius=size//30, fill=(42, 166, 157, 255))
    img.save(root / 'public' / f'icon-{size}.png')

print('Project files created.')
