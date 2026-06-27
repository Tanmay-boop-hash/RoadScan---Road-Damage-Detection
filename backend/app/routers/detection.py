from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, Response
from app.services.detector import run_detection
import base64

router = APIRouter(prefix="/api", tags=["detection"])

@router.post("/detect")
async def detect(file: UploadFile = File(...)):
    if not file.content_type .startswith("image/"):
        raise HTTPException(status_code=400, detail = "File must be an image")
    
    image_bytes = await file.read()

    if len(image_bytes) > 10 * 1024 *1024:        # 10MB limit
        raise HTTPException(status_code=400, detail="Image too large, max 10MB")
    
    detections, annotated_image = run_detection(image_bytes)

    # encode annotated image as base64 so we can return everything in one JSON Response
    encoded_image = base64.b64encode(annotated_image).decode("utf-8")

    return JSONResponse({
        "detections": detections,
        "annotated_image": encoded_image,
        "total_detections": len(detections),
        "summary": {
            "severe": sum(1 for d in detections if d["severity"] == "Severe"),
            "moderate": sum(1 for d in detections if d["severity"] == "Moderate"),
            "minor": sum(1 for d in detections if d["severity"] == "Minor"),
        }
    })