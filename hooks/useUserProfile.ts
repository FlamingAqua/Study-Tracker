'use client'

import { useEffect, useState } from 'react'
import { onAuthStateChanged } from 'firebase/auth'
import { doc, onSnapshot } from 'firebase/firestore'
import { auth, db } from '@/lib/firebase'
import type { UserProfile } from '@/lib/types'

export function useUserProfile() {
  const [profile, setProfile] = useState<UserProfile | null>(null)

  useEffect(() => {
    let unsubscribeProfile = () => {}

    const unsubscribeAuth = onAuthStateChanged(auth, (user) => {
      unsubscribeProfile()
      if (!user) {
        setProfile(null)
        return
      }

      const profileRef = doc(db, 'users', user.uid)
      unsubscribeProfile = onSnapshot(profileRef, (snapshot) => {
        setProfile(snapshot.exists() ? (snapshot.data() as UserProfile) : null)
      })
    })

    return () => {
      unsubscribeProfile()
      unsubscribeAuth()
    }
  }, [])

  return { profile }
}
