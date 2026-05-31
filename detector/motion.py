import cv2


class MotionDetector:
    def __init__(self, min_area: int = 1500):
        self.min_area = min_area
        self._bg_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=500, varThreshold=50, detectShadows=True
        )

    def detect(self, frame) -> list[tuple]:
        fg_mask = self._bg_subtractor.apply(frame)

        _, thresh = cv2.threshold(fg_mask, 200, 255, cv2.THRESH_BINARY)

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        thresh = cv2.dilate(thresh, kernel, iterations=2)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        boxes = []
        for cnt in contours:
            if cv2.contourArea(cnt) >= self.min_area:
                boxes.append(cv2.boundingRect(cnt))

        return boxes
