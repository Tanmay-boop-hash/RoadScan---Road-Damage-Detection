from app.models.yolo_loader import YOLOModel
from app.utils.image_utils import get_severity, annotate_image, CLASS_NAMES
import numpy as np
from PIL import Image
import io
import cv2

def run_detection(image_bytes : bytes):
    model = YOLOModel.get_model()

    # convert bytes to numpy array for OpenCV
    nparr = np.frombuffer(image_bytes, np.uint8)
    img_cv = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    h, w = img_cv.shape[:2]

    results = model(img_cv, verbose=False)[0]

    detections = []

    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        class_id = int(box.cls[0])
        confidence = float(box.conf[0])

        # normalized box area for severity
        box_area = ((x2 - x1)/ w) * ((y2 - y1)/ h)
        severity = get_severity(class_id, box_area, confidence)

        detections.append({
            "class_id": class_id,
            "class_name": CLASS_NAMES[class_id],
            "confidence": round(confidence, 3),
            "severity": severity,
            "bbox": [x1, y1, x2, y2]
        })

    annotated = annotate_image(image_bytes, detections)

    return detections, annotated