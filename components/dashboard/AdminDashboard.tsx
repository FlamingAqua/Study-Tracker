import { useState } from "react";

import Sidebar from "./Sidebar";
import Topbar from "./Topbar";
import ChapterCard from "./ChapterCard";
// @ts-ignore: CSS import declared for bundler side effects
import "./dashboard.css";
import useAdminChapters from "../../hooks/useAdminChapters";
export default function AdminDashboard() {
  const [selectedSubject, setSelectedSubject] =
    useState("all");

  const {
    chapters,
    loading,
    totalChapters,
    completedChapters,
    completionPercentage,
  } = useAdminChapters(selectedSubject);

  return (
    <div className="dashboard-layout">
      <Sidebar
        selectedSubject={selectedSubject}
        setSelectedSubject={setSelectedSubject}
      />

      <div className="dashboard-main">
        <Topbar />

        <div className="stats-grid">
          <div className="stat-card">
            <h3>Total Chapters</h3>
            <p>{totalChapters}</p>
          </div>

          <div className="stat-card">
            <h3>Completed</h3>
            <p>{completedChapters}</p>
          </div>

          <div className="stat-card">
            <h3>Completion</h3>
            <p>{completionPercentage}%</p>
          </div>
        </div>

        {loading ? (
          <div className="loading-box">
            Loading chapters...
          </div>
        ) : (
          <div className="chapters-grid">
            {chapters.map((chapter: any) => (
              <ChapterCard
                key={chapter.docId}
                chapter={chapter}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}