from ultralytics import YOLO
import os

class YOLOModel:
    _instance = None

    @classmethod
    def get_model(cls):
        if cls._instance is None:
            weights_path = os.path.join(
                os.path.dirname(__file__),
                "../../weights/best.pt"
            )
            cls._instance = YOLO(weights_path)
        return cls._instance
    