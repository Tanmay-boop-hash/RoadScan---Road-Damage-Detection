import { useRef } from "react"
import { ImagePlus } from "lucide-react"

interface Props {
  onUpload: (file: File) => void
  loading: boolean
  compact?: boolean
}

export default function UploadZone({ onUpload, loading, compact }: Props) {
  const inputRef = useRef<HTMLInputElement>(null)

  const handleFile = (file: File) => {
    if (!file.type.startsWith("image/")) return
    onUpload(file)
  }

  return (
    <div
      className={`upload-zone ${compact ? "upload-zone--compact" : ""} ${loading ? "upload-zone--loading" : ""}`}
      onClick={() => !loading && inputRef.current?.click()}
      onDragOver={(e) => e.preventDefault()}
      onDrop={(e) => {
        e.preventDefault()
        const file = e.dataTransfer.files[0]
        if (file && !loading) handleFile(file)
      }}
    >
      <input
        ref={inputRef}
        type="file"
        accept="image/*"
        style={{ display: "none" }}
        onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0])}
      />
      {loading ? (
        <p className="upload-zone__text">Analyzing...</p>
      ) : (
        <>
          <ImagePlus size={28} strokeWidth={1.5} color="#555" />
          <p className="upload-zone__text">Drop image here or click to browse</p>
          <p className="upload-zone__sub">JPG, PNG, WEBP supported</p>
        </>
      )}
    </div>
  )
}