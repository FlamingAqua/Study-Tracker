import React from "react";

type Subject = "all" | "forensic-medicine" | "community-medicine" | string;

interface SidebarProps {
  selectedSubject: Subject;
  setSelectedSubject: React.Dispatch<React.SetStateAction<Subject>>;
}

export default function Sidebar({
  selectedSubject,
  setSelectedSubject,
}: SidebarProps) {
  return (
    <div className="sidebar">
      <h2 className="logo">MBBS Tracker</h2>

      <div className="menu-section">
        <button
          className={
            selectedSubject === "all"
              ? "menu-btn active"
              : "menu-btn"
          }
          onClick={() => setSelectedSubject("all")}
        >
          All Subjects
        </button>

        <button
          className={
            selectedSubject === "forensic"
              ? "menu-btn active"
              : "menu-btn"
          }
          onClick={() => setSelectedSubject("forensic-medicine")}
        >
          Forensic Medicine
        </button>

        <button
          className={
            selectedSubject === "community"
              ? "menu-btn active"
              : "menu-btn"
          }
          onClick={() => setSelectedSubject("community-medicine")}
        >
          Community Medicine
        </button>
      </div>
    </div>
  );
}