import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision
import urllib.request
import os
import math
import time


MODEL_PATH = "face_landmarker.task"
MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/"
    "face_landmarker/face_landmarker/float16/latest/face_landmarker.task"
)

_LEFT_EYE  = [33, 160, 158, 133, 153, 144]
_RIGHT_EYE = [362, 385, 387, 263, 373, 380]

EAR_THRESHOLD = 0.20
CLOSED_FRAMES = 15


def _ensure_model():
    if not os.path.exists(MODEL_PATH):
        print("[LunarGuard] Baixando modelo MediaPipe Face (~25 MB)...")
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)


def _ear(landmarks, indices, w, h):
    pts = [(int(landmarks[i].x * w), int(landmarks[i].y * h)) for i in indices]
    vert1 = math.dist(pts[1], pts[5])
    vert2 = math.dist(pts[2], pts[4])
    horiz = math.dist(pts[0], pts[3])
    if horiz == 0:
        return 1.0
    return (vert1 + vert2) / (2.0 * horiz)


class BlinkDetector:
    def __init__(self):
        _ensure_model()

        base_options = mp_python.BaseOptions(model_asset_path=MODEL_PATH)
        options = vision.FaceLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_faces=1,
            min_face_detection_confidence=0.4,
            min_face_presence_confidence=0.4,
            min_tracking_confidence=0.4,
        )
        self._landmarker = vision.FaceLandmarker.create_from_options(options)
        self._closed_count = 0
        self.face_landmarks = None
        self._last_closed = False

    def process(self, frame_rgb) -> bool:
        h, w = frame_rgb.shape[:2]
        ts = int(time.time() * 1000)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
        result = self._landmarker.detect_for_video(mp_image, ts)

        if not result.face_landmarks:
            self.face_landmarks = None
            self._closed_count = 0
            return self._last_closed

        lm = result.face_landmarks[0]
        self.face_landmarks = lm

        left_ear  = _ear(lm, _LEFT_EYE,  w, h)
        right_ear = _ear(lm, _RIGHT_EYE, w, h)
        avg_ear   = (left_ear + right_ear) / 2.0

        if avg_ear < EAR_THRESHOLD:
            self._closed_count += 1
        else:
            self._closed_count = max(0, self._closed_count - 1)

        self._last_closed = self._closed_count >= CLOSED_FRAMES
        return self._last_closed

    def close(self):
        self._landmarker.close()
