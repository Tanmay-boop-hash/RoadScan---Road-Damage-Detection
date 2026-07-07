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

# Colors keyed by severity, not class — matching frontend exactly
SEVERITY_COLORS = {
    "Severe":   (68,  68,  255),  # #ff4444 in BGR
    "Moderate": (0,   170, 255),  # #ffaa00 in BGR
    "Minor":    (68,  187, 68),   # #44bb44 in BGR
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
        severity = det["severity"]
        color = SEVERITY_COLORS[severity]

        # Draw bounding box
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

        # Label with semi-transparent background
        label = f"{det['class_name']} · {severity}"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        thickness = 1
        (tw, th), _ = cv2.getTextSize(label, font, font_scale, thickness)

        # Draw dark background rectangle behind text
        cv2.rectangle(
            img,
            (x1, max(y1 - th - 8, 0)),
            (x1 + tw + 6, max(y1, th + 8)),
            (0, 0, 0),
            -1  # filled
        )
        # Draw text on top
        cv2.putText(
            img, label,
            (x1 + 3, max(y1 - 4, th + 4)),
            font, font_scale, color, thickness
        )

    # convert back to bytes
    _, buffer = cv2.imencode(".jpg", img)
    return buffer.tobytes()

