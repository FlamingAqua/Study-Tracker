import { onIdTokenChanged, signInWithPopup, signOut, User } from 'firebase/auth'
import { doc, getDoc, serverTimestamp, setDoc } from 'firebase/firestore'
import { auth, db, googleProvider } from '@/lib/firebase'
import { ALLOWED_EMAILS, GROUP_ID } from '@/lib/constants'
import type { UserProfile, UserRole } from '@/lib/types'

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
  const ADMIN_EMAILS = [
    "rmanesh011@gmail.com",
    "raghupathyg8@gmail.com"
  ];
  
  const now = new Date().toISOString()
  const profileRef = doc(db, "users", user.uid);
  const snap = await getDoc(profileRef);
  const role = (ADMIN_EMAILS.includes(user.email || '') ? 'admin' : 'student') as UserRole;

  if (!snap.exists()) {
    await setDoc(profileRef, {
      uid: user.uid,
      email: user.email,
      displayName: user.displayName,
      photoURL: user.photoURL,
      role,
      groupId: GROUP_ID,
      createdAt: now,
      lastSeenAt: now,
    });
  } else {
    await setDoc(
      profileRef,
      {
        lastSeenAt: now,
      },
      { merge: true }
    );
  }

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
