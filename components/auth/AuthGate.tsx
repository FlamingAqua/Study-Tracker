'use client'

import { onAuthStateChanged } from 'firebase/auth'
import { useEffect, useState } from 'react'
import { auth } from "../../firebase/firebase";
import { isAllowedUser, upsertUserProfile } from '@/lib/auth'
import { LoginCard } from '@/components/auth/LoginCard'
import { useToast } from '@/components/ui/toast'
import type { User } from 'firebase/auth'
import { useRouter, usePathname } from "next/navigation";
import { doc, getDoc } from "firebase/firestore";
import { db } from "../../firebase/firebase";
import Image from "next/image";
export function AuthGate({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const pathname = usePathname();
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const { toast } = useToast()

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (firebaseUser) => {
  try {
    if (!firebaseUser) {
      setUser(null);
      setLoading(false);
      return;
    }

    setUser(firebaseUser);

    // Fetch user document from Firestore
    const userRef = doc(db, "users", firebaseUser.uid);

    const userSnap = await getDoc(userRef);

    if (userSnap.exists()) {
      const userData = userSnap.data();

      localStorage.setItem("role", userData.role || "student");
      localStorage.setItem("groupId", userData.groupId || "");

      // Role-based redirects
      if (pathname === "/") {
        if (userData.role === "admin") {
          router.push("/admin");
        } else {
          router.push("/");
        }
      }
    }

  } catch (error) {
    console.error("AuthGate error:", error);
  } finally {
    setLoading(false);
  }
});
    return () => unsubscribe()
  }, [toast])

  if (loading) {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center">
      <Image
        src="/branding/logo-light.png"
        alt="Loading"
        width={120}
        height={120}
        className="animate-pulse"
      />

      <p className="mt-4 text-slate-500">
        Loading Study Tracker...
      </p>
    </div>
  )
}

  if (!user) return <LoginCard />
  

  return <>{children}</>
}
