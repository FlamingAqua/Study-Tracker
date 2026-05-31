import { useEffect, useState } from "react";
import {
  collection,
  query,
  where,
  onSnapshot,
} from "firebase/firestore";

import { db } from "../firebase/firebase";

type AdminChapter = {
  docId: string;
  status?: string;
  [key: string]: any;
};

export default function useAdminChapters(selectedSubject: string) {
  const [chapters, setChapters] = useState<AdminChapter[]>([]);
  const [loading, setLoading] = useState(true);

  const [groupId, setGroupId] = useState<string | null>(null);

useEffect(() => {
  setGroupId(localStorage.getItem("groupId"));
}, []);

  useEffect(() => {
    if (!groupId) return;

    let q;

    if (selectedSubject === "all") {
      q = query(
        collection(db, "chapters"),
        where("groupId", "==", groupId)
      );
    } else {
      q = query(
        collection(db, "chapters"),
        where("groupId", "==", groupId),
        where("subjectId", "==", selectedSubject)
      );
    }

    const unsubscribe = onSnapshot(
      q,
      (snapshot) => {
        const data = snapshot.docs.map((doc) => ({
          docId: doc.id,
          ...doc.data(),
        }));

        setChapters(data);
        setLoading(false);
      },
      (error) => {
        console.error("Realtime fetch error:", error);
        setLoading(false);
      }
    );

    return () => unsubscribe();
  }, [selectedSubject, groupId]);

  const totalChapters = chapters.length;

  const completedChapters = chapters.filter(
    (c) => c.status === "completed"
  ).length;

  const completionPercentage =
    totalChapters === 0
      ? 0
      : Math.round((completedChapters / totalChapters) * 100);

  return {
    chapters,
    loading,
    totalChapters,
    completedChapters,
    completionPercentage,
  };
}