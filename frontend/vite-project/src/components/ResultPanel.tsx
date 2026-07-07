import UploadZone from "./UploadZone"

interface Detection {
  class_name: string
  confidence: number
  severity: string
  bbox: number[]
}

interface Summary {
  severe: number
  moderate: number
  minor: number
}

interface Props {
  annotatedImage: string
  detections: Detection[]
  summary: Summary
  totalDetections: number
  onReset: () => void
  onNewUpload: (file: File) => void
}

const SEVERITY_COLOR: Record<string, string> = {
  Severe: "#ff4444",
  Moderate: "#ffaa00",
  Minor: "#44bb44",
}

export default function ResultPanel({
  annotatedImage,
  detections,
  summary,
  totalDetections,
  onNewUpload,
}: Props) {
  return (
    <div className="result-layout">
      {/* Left — annotated image */}
      <div className="result-image-col">
        <img
          src={`data:image/jpeg;base64,${annotatedImage}`}
          alt="Annotated road"
          className="result-image"
        />
        <div className="upload-new-wrapper">
          <UploadZone onUpload={onNewUpload} loading={false} compact />
        </div>
      </div>

      {/* Right — report */}
      <div className="result-report-col">
        <p className="report-label">Detection Report</p>

        {/* Summary row */}
        <div className="summary-row">
          {(["Severe", "Moderate", "Minor"] as const).map((level) => (
            <div key={level} className="summary-card" style={{ borderColor: SEVERITY_COLOR[level] }}>
              <span className="summary-count" style={{ color: SEVERITY_COLOR[level] }}>
                {summary[level.toLowerCase() as keyof Summary]}
              </span>
              <span className="summary-label">{level}</span>
            </div>
          ))}
        </div>

        <p className="total-label">
          {totalDetections} detection{totalDetections !== 1 ? "s" : ""} found
        </p>

        {/* Detection list */}
        <div className="detection-list">
          {totalDetections === 0 ? (
            <p className="no-detections">No road damage detected in this image.</p>
          ) : (
            detections.map((d, i) => (
              <div
                key={i}
                className="detection-card"
                style={{ borderLeftColor: SEVERITY_COLOR[d.severity] }}
              >
                <div className="detection-name">{d.class_name}</div>
                <div className="detection-meta">
                  <span style={{ color: SEVERITY_COLOR[d.severity] }}>{d.severity}</span>
                  <span className="detection-dot">·</span>
                  <span>{(d.confidence * 100).toFixed(1)}% confidence</span>
                </div>
              </div>
            ))
          )}
        </div>

        {/* Limitation note */}
        <p className="limitation-note">
          Model trained on RDD2022 India subset · mAP50 0.39 · Best on dry paved roads
        </p>
      </div>
    </div>
  )
}