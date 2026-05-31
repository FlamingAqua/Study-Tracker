interface Chapter {
  name: string;
  status: "completed" | "pending" | string;
  subjectId: string;
  completionPercentage?: number;
  hoursStudied?: number;
  revisionStatus?: string;
}

interface ChapterCardProps {
  chapter: Chapter;
}

export default function ChapterCard({ chapter }: ChapterCardProps) {
  return (
    <div className="chapter-card">
      <div className="chapter-header">
        <h3>{chapter.name}</h3>

        <span
          className={
            chapter.status === "completed"
              ? "status completed"
              : "status pending"
          }
        >
          {chapter.status}
        </span>
      </div>

      <p className="subject-text">
        Subject: {chapter.subjectId}
      </p>

      <div className="progress-container">
        <div
          className="progress-fill"
          style={{
            width: `${chapter.completionPercentage || 0}%`,
          }}
        />
      </div>

      <div className="chapter-footer">
        <span>
          Progress: {chapter.completionPercentage || 0}%
        </span>

        <span>
          Hours: {chapter.hoursStudied || 0}
        </span>
      </div>

      <div className="revision-box">
        Revision:{" "}
        {chapter.revisionStatus || "Not Scheduled"}
      </div>
    </div>
  );
}