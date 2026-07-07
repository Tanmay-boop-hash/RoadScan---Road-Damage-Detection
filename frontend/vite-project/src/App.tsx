import { useState } from "react"
import axios from "axios"
import { RotateCcw } from "lucide-react"
import UploadZone from "./components/UploadZone"
import ResultPanel from "./components/ResultPanel"

interface Detection {
  class_name: string
  confidence: number
  severity: string
  bbox: number[]
}

interface Result {
  detections: Detection[]
  annotated_image: string
  total_detections: number
  summary: { severe: number; moderate: number; minor: number }
}

export default function App() {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<Result | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleUpload = async (file: File) => {
    setError(null)
    setResult(null)
    setLoading(true)

    const formData = new FormData()
    formData.append("file", file)

    try {
      const res = await axios.post(
        "http://localhost:8000/api/detect",
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      )
      setResult(res.data)
    } catch {
      setError("Detection failed. Make sure the backend is running.")
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    setResult(null)
    setError(null)
  }

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="header-left">
          <span className="header-title">RoadScan</span>
          <span className="header-sub">Road Damage Detection</span>
        </div>
        {result && (
          <button className="btn-reset" onClick={handleReset}>
            <RotateCcw size={14} />
            New Image
          </button>
        )}
      </header>

      <main className="main">
        {!result ? (
          <>
            <div className="hero-text">
              <h1>Detect road damage instantly</h1>
              <p>
                Upload a road image. YOLOv8 fine-tuned on RDD2022 India dataset
                classifies cracks, potholes, and surface damage by severity.
              </p>
            </div>
            <UploadZone onUpload={handleUpload} loading={loading} />
            {error && <p className="error">{error}</p>}
          </>
        ) : (
          <ResultPanel
            annotatedImage={result.annotated_image}
            detections={result.detections}
            summary={result.summary}
            totalDetections={result.total_detections}
            onReset={handleReset}
            onNewUpload={handleUpload}
          />
        )}
      </main>
    </div>
  )
}