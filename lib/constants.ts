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
    completion: 0,
  },
  {
    id: 'community-medicine',
    name: 'Community Medicine',
    totalChapters: 22,
    color: 'from-emerald-500 to-green-600',
    completion: 0,
  },
] as const

export const REVISION_OFFSETS_DAYS = [1, 3, 7, 21]

export const DEFAULT_CHAPTERS = generateChapterSeed()
