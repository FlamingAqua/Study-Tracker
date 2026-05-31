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
