import cv2
import numpy as np
from PIL import Image
import io

CLASS_NAMES = {
    0: "Longitudinal Crack",
    1: "Transverse Crack",
    2: "Alligator Crack",
    3: "Pothole",
    4: "White Line Blur"
}

COLORS = {
    0: (255, 165, 0),   # orange
    1: (255, 255, 0),   # yellow
    2: (255, 0, 0),     # red
    3: (128, 0, 128),   # purple
    4: (0, 165, 255),   # light blue
}

def get_severity(class_id, box_area, confidence):
    if class_id == 3:         # pothole -> area matters most
        if box_area > 0.05:
            return "Severe"
        elif box_area > 0.02:
            return "Moderate"
        else:
            return "Minor"
    elif class_id == 2:       # alligator crack -> always at least Moderate 
        return "Severe" if box_area > 0.04 else "Moderate"
    else:
        return "Minor" if confidence < 0.6 else "Moderate"
     

def annotate_image(image_bytes, detections):
    # convert bytes to cv2 image
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR) 
    h, w = img.shape[:2]

    for det in detections:
        x1, y1, x2, y2 = det["bbox"]
        class_id = det["class_id"]
        severity = det["severity"]
        confidence = det["confidence"]
        color = COLORS.get(class_id, (0,255,0))

        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        label = f"{CLASS_NAMES[class_id]} | {severity} | {confidence: .2f}"
        cv2.putText(img, label, (x1, max(y1-8, 0)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # convert back to bytes
    _, buffer = cv2.imencode(".jpg", img)
    return buffer.tobytes()

