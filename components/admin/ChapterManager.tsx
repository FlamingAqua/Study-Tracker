"use client";

import { useEffect, useState } from "react";
import {
  collection,
  addDoc,
  onSnapshot,
  deleteDoc,
  doc,
  updateDoc,
  query,
  where,
  orderBy,
} from "firebase/firestore";

import { db } from "@/lib/firebase";
// Fallback/local stub for useAuth to avoid build errors when the project
// doesn't provide the '@/hooks/useAuth' module. This returns a shape
// expected by this component (profile possibly undefined with groupId).
function useAuth() {
  return { profile: undefined as { groupId?: string } | undefined };
}

type Chapter = {
  id: string;
  name: string;
  subjectId: string;
  subjectName: string;
  groupId: string;
  status: string;
  completionPercentage: number;
  hoursStudied: number;
  revisionState: string;
  studyStreak: number;
  notes: string;
};

export function ChapterManager() {
  const { profile } = useAuth();

  const [chapters, setChapters] = useState<Chapter[]>([]);
  const [loading, setLoading] = useState(true);

  const [chapterName, setChapterName] = useState("");
  const [subject, setSubject] = useState("Forensic Medicine");

  const groupId = profile?.groupId || "";

  useEffect(() => {
    if (!groupId) return;

    const q = query(
      collection(db, "chapters"),
      where("groupId", "==", groupId),
      orderBy("createdAt", "desc")
    );

    const unsub = onSnapshot(q, (snapshot) => {
      const data = snapshot.docs.map((doc) => ({
        id: doc.id,
        ...doc.data(),
      })) as Chapter[];

      setChapters(data);
      setLoading(false);
    });

    return () => unsub();
  }, [groupId]);

  async function addChapter() {
    if (!chapterName.trim()) return;

    await addDoc(collection(db, "chapters"), {
      name: chapterName,
      subjectId:
        subject === "Forensic Medicine"
          ? "forensic-medicine"
          : "community-medicine",

      subjectName: subject,

      groupId,

      status: "not_started",

      completionPercentage: 0,

      hoursStudied: 0,

      revisionState: "none",

      studyStreak: 0,

      notes: "",

      createdAt: new Date().toISOString(),

      updatedAt: new Date().toISOString(),
    });

    setChapterName("");
  }

  async function deleteChapter(id: string) {
    await deleteDoc(doc(db, "chapters", id));
  }

  async function markCompleted(id: string) {
    await updateDoc(doc(db, "chapters", id), {
      status: "completed",
      completionPercentage: 100,
      updatedAt: new Date().toISOString(),
    });
  }

  return (
    <div className="mx-auto max-w-6xl">
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-white">
          Chapter Management
        </h1>

        <p className="mt-2 text-slate-400">
          Admin chapter CRUD panel
        </p>
      </div>

      <div className="card mb-8 p-6">
        <h2 className="mb-4 text-xl font-semibold text-white">
          Add New Chapter
        </h2>

        <div className="grid gap-4 md:grid-cols-3">
          <input
            value={chapterName}
            onChange={(e) => setChapterName(e.target.value)}
            placeholder="Enter chapter name"
            className="input"
          />

          <select
            value={subject}
            onChange={(e) => setSubject(e.target.value)}
            className="input"
          >
            <option>Forensic Medicine</option>
            <option>Community Medicine</option>
          </select>

          <button
            onClick={addChapter}
            className="btn-primary"
          >
            Add Chapter
          </button>
        </div>
      </div>

      {loading ? (
        <div className="text-slate-300">
          Loading chapters...
        </div>
      ) : (
        <div className="grid gap-4">
          {chapters.map((chapter) => (
            <div
              key={chapter.id}
              className="card flex flex-col gap-4 p-5 md:flex-row md:items-center md:justify-between"
            >
              <div>
                <h3 className="text-lg font-semibold text-white">
                  {chapter.name}
                </h3>

                <p className="text-sm text-slate-400">
                  {chapter.subjectName}
                </p>

                <p className="mt-2 text-sm text-slate-300">
                  Status: {chapter.status}
                </p>
              </div>

              <div className="flex gap-3">
                <button
                  onClick={() => markCompleted(chapter.id)}
                  className="btn-primary"
                >
                  Complete
                </button>

                <button
                  onClick={() => deleteChapter(chapter.id)}
                  className="rounded-xl bg-red-500 px-4 py-2 text-white hover:bg-red-600"
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}