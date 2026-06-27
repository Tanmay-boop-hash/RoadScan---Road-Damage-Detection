from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.detection import router
from app.models.yolo_loader import YOLOModel

app = FastAPI(title="Pothole Detector API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # default vite port
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    YOLOModel.get_model()    # load model on startup, not on first request
    print("Model loaded and ready")

app.include_router(router)

@app.get("/health")
def health_check():
    return {"status": "ok"}